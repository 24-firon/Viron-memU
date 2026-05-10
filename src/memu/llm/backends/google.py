from __future__ import annotations

from typing import Any

from memu.llm.backends.base import LLMBackend


class GoogleLLMBackend(LLMBackend):
    """Stub backend for Google AI — only embedding is supported via this profile."""

    name = "google"
    summary_endpoint = "/v1beta/models:generateContent"

    def build_summary_payload(
        self, *, text: str, system_prompt: str | None, chat_model: str, max_tokens: int | None
    ) -> dict[str, Any]:
        msg = "Google LLM chat is not supported via this backend; use the OpenAI-compatible endpoint with vLLM instead."
        raise NotImplementedError(msg)

    def parse_summary_response(self, data: dict[str, Any]) -> str:
        msg = "Google LLM chat is not supported via this backend."
        raise NotImplementedError(msg)

    def build_vision_payload(
        self,
        *,
        prompt: str,
        base64_image: str,
        mime_type: str,
        system_prompt: str | None,
        chat_model: str,
        max_tokens: int | None,
    ) -> dict[str, Any]:
        msg = "Google vision is not supported via this backend."
        raise NotImplementedError(msg)
