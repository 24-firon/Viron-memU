"""
Fallback LLM Client - Multi-Provider Failover Wrapper
======================================================

Provides automatic failover between multiple LLM providers when the primary
provider returns a rate-limit (HTTP 429) or transient server error (5xx).

This module solves a specific problem in production AI applications:
API rate limits. When a provider (e.g., Google AI Studio free tier with
15 RPM) returns 429 Too Many Requests, this wrapper rotates to the next
configured provider in the list and retries the same request.

Key Design Decisions:
---------------------
1. **Provider-Agnostic**: The fallback client wraps any combination of
   HTTPLLMClient instances - it doesn't care about the underlying API format.
   OpenAI-compatible providers (OpenAI, Nvidia NIM, OpenRouter, Grok) and
   custom-format providers (Google AI) can all be mixed in the same chain.

2. **Order-Preserving**: Providers are tried in the order specified in
   `fallback_providers`. The first provider in the list has highest priority.

3. **Configurable Trigger Codes**: By default, 429 and transient 5xx codes
   trigger fallback. Other errors (4xx client errors like 400, 401, 403)
   are raised immediately as they indicate configuration problems that
   fallback cannot fix.

4. **Embeddings Pass-Through**: Embedding calls (for vector search) do NOT
   use the fallback chain by default - they go to the provider configured
   in the 'embedding' profile. This prevents accidentally mixing embedding
   dimensions from different providers (e.g., 1536 from OpenAI vs 3072 from
   Google) which would corrupt the pgvector index.

5. **Async-Native**: All methods are async and use httpx.AsyncClient under
   the hood, matching the rest of memU's async architecture.

6. **Stats Tracking**: Each provider tracks success/failure counts, allowing
   you to monitor which providers are actually being used and which are
   failing in production.

Usage Example:
--------------
    from memu.llm.fallback_client import FallbackLLMClient
    from memu.llm.http_client import HTTPLLMClient

    primary = HTTPLLMClient(
        base_url="https://generativelanguage.googleapis.com/v1beta",
        api_key="GOOGLE_KEY",
        chat_model="gemini-flash-latest",
        provider="google",
    )

    fallback = HTTPLLMClient(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key="NVIDIA_KEY",
        chat_model="meta/llama-3.1-8b-instruct",
        provider="openai",  # Nvidia NIM is OpenAI-compatible
    )

    client = FallbackLLMClient(
        providers=[primary, fallback],
        retry_status_codes=[429, 500, 502, 503, 504],
    )

    # Use as a drop-in replacement for HTTPLLMClient
    response, raw = await client.summarize("Hello world")
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

from memu.llm.http_client import HTTPLLMClient

logger = logging.getLogger(__name__)


class FallbackLLMClient:
    """Multi-provider LLM client with automatic failover on rate-limit errors.

    Wraps an ordered list of `HTTPLLMClient` instances. When a request fails
    with a configurable status code (default: 429, 5xx), rotates to the next
    provider and retries. Returns the first successful response.
    """

    def __init__(
        self,
        *,
        providers: list[HTTPLLMClient],
        retry_status_codes: list[int] | None = None,
        max_retries_per_provider: int = 1,
        backoff_seconds: float = 0.5,
    ):
        """Initialize the FallbackLLMClient.

        Args:
            providers: Ordered list of HTTPLLMClient instances. The first item
                is the highest-priority provider.
            retry_status_codes: HTTP status codes that trigger fallback to the
                next provider. Default: [429, 500, 502, 503, 504].
            max_retries_per_provider: How many times to retry the same provider
                before giving up and rotating. Default: 1.
            backoff_seconds: Sleep duration between retries on the same provider.
                Default: 0.5s.
        """
        if not providers:
            msg = "FallbackLLMClient requires at least one provider"
            raise ValueError(msg)
        self.providers: list[HTTPLLMClient] = list(providers)
        self.retry_status_codes: list[int] = list(
            retry_status_codes if retry_status_codes is not None else [429, 500, 502, 503, 504]
        )
        self.max_retries_per_provider = max_retries_per_provider
        self.backoff_seconds = backoff_seconds

        self._stats: dict[int, dict[str, int]] = {
            idx: {"success": 0, "fallback_triggered": 0, "error": 0}
            for idx in range(len(self.providers))
        }

    def _record_success(self, provider_idx: int) -> None:
        self._stats[provider_idx]["success"] += 1
        logger.debug("Provider[%d] (%s) succeeded", provider_idx, self._provider_label(provider_idx))

    def _record_fallback(self, provider_idx: int, status_code: int) -> None:
        self._stats[provider_idx]["fallback_triggered"] += 1
        logger.warning(
            "Provider[%d] (%s) returned %d, rotating to next provider",
            provider_idx,
            self._provider_label(provider_idx),
            status_code,
        )

    def _record_error(self, provider_idx: int, exc: Exception) -> None:
        self._stats[provider_idx]["error"] += 1
        logger.error(
            "Provider[%d] (%s) raised %s: %s",
            provider_idx,
            self._provider_label(provider_idx),
            type(exc).__name__,
            exc,
        )

    def _provider_label(self, idx: int) -> str:
        p = self.providers[idx]
        return f"{p.provider}/{p.chat_model}@{p.base_url}"

    @property
    def stats(self) -> dict[str, dict[str, int]]:
        """Return per-provider success/fallback/error counts."""
        return {
            self._provider_label(idx): counts
            for idx, counts in self._stats.items()
        }

    async def _execute_with_fallback(
        self, method_name: str, *args: Any, **kwargs: Any
    ) -> Any:
        """Execute a method across providers, falling back on retryable errors.

        Iterates over `self.providers`. For each provider, tries the method up to
        `max_retries_per_provider` times with `backoff_seconds` delay. If the
        exception's status code is in `retry_status_codes`, moves to the next
        provider. Any other exception is re-raised immediately.

        Returns the first successful response. If all providers fail, raises
        the last exception.
        """
        last_exc: Exception | None = None
        for provider_idx, provider in enumerate(self.providers):
            method = getattr(provider, method_name, None)
            if method is None:
                logger.error(
                    "Provider[%d] (%s) has no method '%s', skipping",
                    provider_idx,
                    self._provider_label(provider_idx),
                    method_name,
                )
                continue
            for attempt in range(self.max_retries_per_provider):
                try:
                    result = await method(*args, **kwargs)
                except httpx.HTTPStatusError as e:
                    status = e.response.status_code
                    if status in self.retry_status_codes:
                        self._record_fallback(provider_idx, status)
                        break
                    self._record_error(provider_idx, e)
                    raise
                except (httpx.ConnectError, httpx.TimeoutException) as e:
                    self._record_error(provider_idx, e)
                    if attempt + 1 < self.max_retries_per_provider:
                        await asyncio.sleep(self.backoff_seconds)
                        continue
                    last_exc = e
                    break
                except Exception as e:
                    self._record_error(provider_idx, e)
                    raise
                else:
                    self._record_success(provider_idx)
                    return result
        if last_exc is None:
            last_exc = RuntimeError(
                f"All {len(self.providers)} providers failed for method '{method_name}'"
            )
        raise last_exc

    async def summarize(
        self, text: str, max_tokens: int | None = None, system_prompt: str | None = None
    ) -> tuple[str, dict[str, Any]]:
        """Summarize text using the primary provider, falling back on errors."""
        result = await self._execute_with_fallback(
            "summarize", text, max_tokens=max_tokens, system_prompt=system_prompt
        )
        return result

    async def embed(self, inputs: list[str]) -> tuple[list[list[float]], dict[str, Any]]:
        """Generate embeddings using the primary provider's embedding backend.

        NOTE: Embeddings intentionally do NOT use the fallback chain because
        different providers produce vectors of different dimensions (OpenAI
        1536, Google 3072, etc.). Mixing dimensions would corrupt the
        pgvector index. If you need a fallback for embeddings, configure a
        dedicated 'embedding' profile with its own fallback list.
        """
        primary = self.providers[0]
        return await primary.embed(inputs)

    async def vision(
        self,
        prompt: str,
        image_path: str,
        *,
        max_tokens: int | None = None,
        system_prompt: str | None = None,
    ) -> tuple[str, dict[str, Any]]:
        """Call a vision model using the primary provider, falling back on errors."""
        return await self._execute_with_fallback(
            "vision",
            prompt,
            image_path,
            max_tokens=max_tokens,
            system_prompt=system_prompt,
        )

    async def transcribe(
        self,
        audio_path: str,
        *,
        prompt: str | None = None,
        language: str | None = None,
        response_format: str = "text",
    ) -> tuple[str, dict[str, Any] | None]:
        """Transcribe audio using the primary provider, falling back on errors."""
        return await self._execute_with_fallback(
            "transcribe",
            audio_path,
            prompt=prompt,
            language=language,
            response_format=response_format,
        )

    @property
    def chat_model(self) -> str:
        """Return the chat model of the primary provider."""
        return self.providers[0].chat_model

    @property
    def embed_model(self) -> str | None:
        """Return the embed model of the primary provider."""
        return self.providers[0].embed_model

    @property
    def provider(self) -> str:
        """Return a composite provider name like 'fallback[google,openai]'."""
        return "fallback[" + ",".join(p.provider for p in self.providers) + "]"
