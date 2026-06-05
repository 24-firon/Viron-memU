# memU Multi-Provider Infrastructure — Comprehensive Report

> **Purpose of this document:** This is a meta-document. It does not duplicate
> the technical details that already live in the source files. Instead, it
> explains the *what*, the *why*, the *how-it-fits-together*, the *problems
> we encountered along the way*, and the *strategic outlook* — written as
> flowing prose for a human reader who wants to understand the system as a
> whole before (or instead of) diving into the code.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [The Problem We Were Solving](#2-the-problem-we-were-solving)
3. [Architectural Overview](#3-architectural-overview)
4. [Component Walkthrough](#4-component-walkthrough)
5. [Configuration Cheat-Sheet](#5-configuration-cheat-sheet)
6. [Failure Modes and Mitigations](#6-failure-modes-and-mitigations)
7. [Synergies and Future Potentials](#7-synergies-and-future-potentials)
8. [Operational Runbook](#8-operational-runbook)
9. [Glossary](#9-glossary)
10. [Appendices](#10-appendices)

---

## 1. Executive Summary

memU is a memory framework: given unstructured text (a chat log, a document,
a personal note), it extracts the salient facts, indexes them as vector
embeddings, and later retrieves the most relevant ones for any given query.
Under the hood, it makes heavy use of Large Language Models (LLMs) — for
extraction, summarisation, classification, and embedding generation.

The problem we hit during development was both mundane and fundamental:
**the public LLM APIs we depend on impose strict rate limits, and those
limits are easy to blow past even in modest testing.** A single end-to-end
memorise call against a non-trivial document can fan out into 10–30 separate
LLM requests (one per category, one per re-ranking step, one per
embedding batch, etc.). At Google's free-tier rate of 15 requests per
minute, the pipeline collapses after the very first document.

The fix we built is a **multi-provider fallback chain**: instead of binding
memU to a single LLM provider, the application now treats providers as
*pluggable, ordered, fail-overable resources*. The primary provider is
tried first; on the first sign of rate-limiting (HTTP 429) or a transient
5xx error, the request is automatically re-issued to the next provider
in the chain. End users and downstream callers see a single, unified
`summarize()`, `embed()`, `vision()` API — they don't have to know or
care which provider actually answered.

The new production configuration is **`google` (primary) → `nvidia` (fallback) → `vllm` (local, last resort)**, which gives the system:

- **A cloud primary** with the best reasoning quality (Google Gemini Flash).
- **An independent cloud fallback** with OpenAI-compatible APIs and a generous free tier (Nvidia NIM, 1,000 free requests/month per key).
- **An on-prem last resort** (vLLM serving Qwen2.5-14B locally) that is rate-limit-free by definition.

The deliverable consists of three new code artefacts (one new module, two
configuration extensions) plus a smoke-test script that proves the
fallover works without touching the real APIs.

---

## 2. The Problem We Were Solving

### 2.1 The Symptom

During initial development, our `test-02-memorize.py` script — designed to
exercise the full "store a personal fact and verify it lands in the
database" pipeline — started failing with `HTTP 429 Too Many Requests`
after only the first memorise call. Investigation showed that the Google
AI Studio free tier enforces a per-model rate cap of approximately
15 requests per minute (and as low as 20 requests per **day** for
certain models like `gemini-2.5-flash`). memU's memorise workflow fans
out into multiple LLM calls: pre-process summarisation, category
embedding, per-category summarisation, relation extraction, and so on.
A single document trips the rate limit almost immediately.

### 2.2 The Root Cause

There are two compounding factors:

1. **Free-tier API economics.** Most public LLM providers cap free usage
   in one of three ways: requests-per-minute (RPM), requests-per-day
   (RPD), or input-tokens-per-minute. memU's chat-heavy workflow is
   particularly sensitive to RPM limits.
2. **memU's request shape.** A single user-visible operation
   (`memorise("document text")`) decomposes into a tree of LLM
   invocations. The user is not aware of this fan-out, but the
   provider is. A naïve integration makes the user pay the rate-limit
   tax on every internal step.

### 2.3 What "Solving It" Required

Three properties had to be guaranteed simultaneously:

- **No new abstraction for callers.** Every existing call site
  (`await memory.memorize(...)`, `await memory.retrieve(...)`,
  `await client.summarize(...)`) had to keep working unchanged.
- **Provider heterogeneity.** The fallback chain had to be able to mix
  providers with *incompatible* wire formats. Google AI uses an
  API-key-as-query-param style with a non-OpenAI JSON body; OpenAI,
  OpenRouter, Grok and Nvidia NIM all use Bearer-token authentication
  with OpenAI-style JSON bodies. Both styles had to coexist.
- **Embedding safety.** memU indexes embeddings in a pgvector column.
  Different providers emit vectors of different dimensions
  (OpenAI: 1536, Google: 3072, Nvidia NIM: 1024 or 2048 depending on
  the model). Falling back *mid-session* from a 3072-dim Google call
  to a 1536-dim OpenAI call would corrupt the index. Embeddings
  therefore have to remain pinned to a single provider per index.

### 2.4 What We Did *Not* Solve (and Why It's OK)

We did not implement a global rate-limiter that throttles the entire
process. That's a different problem — it would slow down valid traffic
rather than gracefully reroute it. The fallback strategy is "fail fast
on the primary, succeed on the secondary" rather than "wait politely
in a queue". For deployments that need both behaviours, the existing
memU interceptor registry in `LLMClientWrapper` is the right place to
plug in a `RateLimitInterceptor`; that is a follow-up project.

---

## 3. Architectural Overview

The system follows a strict layered architecture. Each layer has exactly
one job and a clearly-defined interface to the layer above it. This is
deliberate: it makes the fallback implementation testable in isolation
and keeps the blast radius of any future provider addition very small.

```
┌─────────────────────────────────────────────────────────────────┐
│  Callers (memorise, retrieve, custom code)                      │
│  ── see: clean async API (summarize, embed, vision, transcribe)│
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  LLMClientWrapper (memu/llm/wrapper.py)                        │
│  ── adds: interceptors, telemetry, token accounting             │
│  ── exposes: same async API as the underlying client            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  FallbackLLMClient   ◀── THIS IS THE NEW LAYER                 │
│  ── job: try provider[0], on retryable error try provider[1]…  │
│  ── exposes: summarize, embed (passthrough), vision, transcribe│
│  ── tracks: per-provider success / fallback_triggered / error    │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ HTTPLLMClient    │ │ HTTPLLMClient    │ │ HTTPLLMClient    │
│  (google)        │ │  (nvidia)        │ │  (vllm)          │
│  Gemini Flash    │ │  Llama 3.1 8B    │ │  Qwen 2.5 14B    │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

### 3.1 The Two Client Layers

**`HTTPLLMClient`** (existing) is the *single-provider* HTTP client. It
knows how to:

- Build the right request payload for its declared `provider` (one of
  `openai`, `doubao`, `google`, `grok`, `openrouter`, and now `nvidia`).
- Parse the response in the format that provider returns.
- Handle the provider's specific auth scheme (Bearer for OpenAI-style
  APIs, `?key=` query param for Google, etc.).
- Expose `summarize`, `embed`, `vision`, and `transcribe`.

Crucially, the `nvidia` provider does **not** need a new backend
implementation — Nvidia NIM exposes the OpenAI-compatible
`/v1/chat/completions` and `/v1/embeddings` endpoints with Bearer-token
auth. We register `nvidia` in `LLM_BACKENDS` as a simple alias for
`OpenAILLMBackend`, which is the most code-efficient way to support
it. (This pattern is also useful for any other OpenAI-compatible
service — Together.ai, Anyscale, Fireworks, etc. — and can be
extended later without code changes.)

**`FallbackLLMClient`** (new) sits one level above
`HTTPLLMClient`. It holds a *list* of `HTTPLLMClient` instances and
tries them in order. It delegates `embed()` to the primary client
deliberately (see § 2.3). For everything else, it implements a small
state machine: attempt the first provider, inspect the exception (if
any), and either re-raise (for non-retryable errors) or rotate to the
next provider (for HTTP 429 or transient 5xx).

### 3.2 Where the Layer Sits in memU

`FallbackLLMClient` slots in at exactly the same position as the
existing `HTTPLLMClient` does in `MemoryService._init_llm_client`. From
the rest of memU's perspective, it is a drop-in replacement. The
`LLMClientWrapper` that wraps it (for interceptors, logging, etc.)
sees a single object with the same method signatures. The
`LLMInterceptorRegistry` and the `WorkflowRunner` do not need to be
touched at all.

### 3.3 Configuration Flow

Configuration is read by `memu_factory.create_memory_instance`, which
constructs an `LLMProfilesConfig` (a Pydantic model) and passes it to
`MemoryService.__init__`. The service iterates the profiles and, for
the `default` profile, decides whether to instantiate a plain
`HTTPLLMClient` or a `FallbackLLMClient` based on whether the profile's
`fallback_providers` list is non-empty.

This means the activation cost for fallback is literally a single
function parameter (`enable_fallback=True` in the factory) and a single
Pydantic field. There is no global toggle, no environment variable
that has to be set, no monkey-patch. If you want fallback, you ask for
it; if you don't, you get the single-provider behaviour the codebase
has had all along.

---

## 4. Component Walkthrough

### 4.1 `LLMConfig` (settings.py)

We extended the existing Pydantic `LLMConfig` model with two new
fields:

- **`fallback_providers: list[dict]`** — an ordered list of
  additional provider configs. Each entry has the same shape as a
  top-level `LLMConfig` minus the `fallback_providers` field itself
  (no recursion). The factory populates this list automatically when
  `enable_fallback=True`; you can also set it manually for more
  exotic configurations.
- **`fallback_retry_status_codes: list[int]`** — the HTTP status
  codes that should trigger a rotation to the next provider. Defaults
  to `[429, 500, 502, 503, 504]`. Other 4xx codes (e.g. 401
  Unauthorized, 403 Forbidden) are *not* in this list because they
  indicate configuration errors that no other provider can fix.

The two new fields sit alongside the existing `provider`, `base_url`,
`api_key`, `chat_model`, `client_backend`, and `embed_model` fields.
Nothing about the old fields has changed; existing configurations keep
working.

### 4.2 `FallbackLLMClient` (fallback_client.py)

The new client is intentionally small — about 280 lines including
docstrings and the unit test seam. The public surface is four
methods:

| Method | Returns | Behaviour |
|---|---|---|
| `summarize(text, max_tokens, system_prompt)` | `(str, dict)` | Tries each provider in order. Stops at the first success. |
| `embed(inputs)` | `(list[list[float]], dict)` | Always uses the **primary** provider. See § 2.3. |
| `vision(prompt, image_path, ...)` | `(str, dict)` | Tries each provider in order. |
| `transcribe(audio_path, ...)` | `(str, dict)` | Tries each provider in order. |

Plus the introspection properties `chat_model`, `embed_model`, and
`provider` (which returns a synthetic name like
`fallback[google,nvidia,vllm]` so log lines are informative), and the
`stats` property which exposes the per-provider counters.

The retry decision tree is implemented in a single private method,
`_execute_with_fallback`, and is exhaustively documented in the
module's docstring. The logic is:

```
for provider in providers:
    for attempt in range(max_retries_per_provider):
        try:
            result = await provider.method(...)
        except HTTPStatusError as e:
            if e.response.status_code in retry_status_codes:
                log + rotate to next provider
                break  # exit inner loop
            raise  # non-retryable, propagate
        except (ConnectError, TimeoutException) as e:
            if more attempts available:
                sleep + retry
                continue
            rotate to next provider
            break
        except Exception as e:
            raise  # unknown error, propagate
        else:
            record_success + return result
raise last_exception
```

The behaviour is intentionally conservative: a 401 will *not*
trigger a rotation (you'd just hit the same auth problem on the next
provider), but a 429 will, because every provider in the chain has
its own rate-limit counter and one provider's quota exhaustion is
another provider's opportunity to shine.

### 4.3 `memu_factory.create_memory_instance` (memu_factory.py)

The factory was extended with:

- A new `enable_fallback: bool = True` keyword argument. (Yes, we made
  it default to `True` — the new behaviour is strictly better for
  production workloads, and the only cost is a few hundred milliseconds
  of extra startup time while the second client object is constructed.)
- A new helper, `_build_fallback_providers`, that auto-constructs the
  fallback list from the configured `PROVIDERS` dict. The order is
  hand-tuned for our specific use case (Google primary, Nvidia NIM as
  the first cloud fallback, local vLLM as the last resort), but
  callers can override it by passing their own `fallback_providers`
  list.
- Smarter `endpoint_overrides` handling: the original code assumed
  every provider was Google, which produced a broken URL for
  everything else. The new code only adds the Google-style
  `models/X:generateContent` endpoint override when the provider
  actually *is* Google.
- Better startup logging: the chain is printed to stdout so you can
  see at a glance which providers are active and in what order.

### 4.4 `service.py` (MemoryService)

`_init_llm_client` was restructured to:

1. Build the primary `HTTPLLMClient` exactly as before.
2. If `cfg.fallback_providers` is non-empty, build one
   `HTTPLLMClient` per fallback entry and wrap them all in a
   `FallbackLLMClient`.
3. Return either the primary or the wrapper, depending on step 2.

The SDK and `lazyllm_backend` paths emit a warning and fall back to
single-provider behaviour, because their error surfaces are different
and the failover logic would need additional work. (We could extend
the failover to SDK clients too in a follow-up; the current
`FallbackLLMClient` is designed with that future extension in mind.)

### 4.5 `http_client.py`

Two changes:

- Registered `nvidia` as an alias for `OpenAILLMBackend` in the
  `LLM_BACKENDS` dict. This is a one-liner that means every other
  piece of OpenAI-compat plumbing (payload format, response parsing,
  Bearer-token auth) just works.
- Updated the module docstring to reflect the new provider list.

### 4.6 `test_fallback_smoke.py`

A standalone smoke test with seven sub-tests, all of which pass on
the current code:

1. `FallbackLLMClient` imports cleanly.
2. `MemoryService` imports cleanly.
3. `LLMConfig` exposes the new fields with the correct defaults.
4. `nvidia` is registered in `LLM_BACKENDS` and points to
   `OpenAILLMBackend`.
5. `MemUConfig.PROVIDERS` contains the `nvidia` entry.
6. `create_memory_instance(provider="google", enable_fallback=True)`
   builds a `MemoryService` and the chain is printed to stdout.
7. A unit test using `unittest.mock` proves that when the primary
   provider raises `HTTPStatusError(429)`, the next provider is
   called and its response is returned, with the per-provider
   statistics correctly recorded.

The test takes well under a second to run, does not require a network
connection, and is safe to run as a pre-commit hook.

---

## 5. Configuration Cheat-Sheet

### 5.1 The `PROVIDERS` Dict

| Key | Name | Type | Default Model | API Key Env Var | Base URL |
|---|---|---|---|---|---|
| `vllm` | vLLM Local Server | Local | `qwen2.5-14b-instruct` | (none, key is `EMPTY`) | `http://localhost:8005/v1` |
| `ollama` | Ollama Local | Local | `mistral:latest` | (none, key is `ollama`) | `http://localhost:11434/v1` |
| `openrouter` | OpenRouter Cloud | Cloud | `google/gemini-2.0-flash-thinking-exp:free` | `OPENROUTER_API_KEY` | `https://openrouter.ai/api/v1` |
| `google` | Google AI Studio | Cloud | `gemini-flash-latest` | `GOOGLE_API_KEY` | `https://generativelanguage.googleapis.com/v1beta` |
| `nvidia` | Nvidia NIM | Cloud | `meta/llama-3.1-8b-instruct` | `NVIDIA_API_KEY` | `https://integrate.api.nvidia.com/v1` |

### 5.2 Quick-Start Configurations

**Single provider, no fallback (legacy mode):**
```python
memory = create_memory_instance(provider="vllm", enable_fallback=False)
```

**Multi-provider with auto-discovered chain:**
```python
memory = create_memory_instance(provider="google", enable_fallback=True)
# Chain: google -> nvidia -> vllm
```

**Custom chain (advanced):**
```python
from memu.app import MemoryService
memory = MemoryService(
    llm_profiles={
        "default": {
            "provider": "openai",
            "client_backend": "httpx",
            "base_url": "https://api.openai.com/v1",
            "api_key": os.environ["OPENAI_API_KEY"],
            "chat_model": "gpt-4o-mini",
            "fallback_providers": [
                {
                    "provider": "nvidia",
                    "client_backend": "httpx",
                    "base_url": "https://integrate.api.nvidia.com/v1",
                    "api_key": os.environ["NVIDIA_API_KEY"],
                    "chat_model": "meta/llama-3.1-70b-instruct",
                },
            ],
        },
        "embedding": {
            "provider": "openai",
            "client_backend": "httpx",
            "base_url": "https://api.openai.com/v1",
            "api_key": os.environ["OPENAI_API_KEY"],
            "embed_model": "text-embedding-3-small",
        },
    },
    database_config={...},
)
```

### 5.3 Environment Variables

| Variable | Required? | Purpose |
|---|---|---|
| `GOOGLE_API_KEY` | For Google provider | Gemini API key. Free tier at https://aistudio.google.com/app/apikey |
| `NVIDIA_API_KEY` | For Nvidia fallback | Starts with `nvapi-...`. Get one at https://build.nvidia.com |
| `OPENROUTER_API_KEY` | For OpenRouter | Optional |
| `OPENAI_API_KEY` | For OpenAI | Optional |
| `DB_PASSWORD` | Always | Postgres password (default: `mymemU_Postman`) |
| `VLLM_HOST` | For vLLM | Defaults to `http://localhost:8005` |
| `MEMU_LOG_LEVEL` | Optional | One of `DEBUG`, `INFO`, `WARNING`, `ERROR` |

---

## 6. Failure Modes and Mitigations

| Failure | Symptom | Mitigation |
|---|---|---|
| Primary provider is permanently down (network partition) | `httpx.ConnectError` for every request | `FallbackLLMClient` catches `ConnectError` and rotates after `max_retries_per_provider` attempts. |
| Primary provider returns 401 (bad API key) | `HTTPStatusError(401)` | **Not** in the retry list. Raised immediately. This is the right behaviour — a 401 means the key is wrong, and no other provider will fix that. The user must correct the key. |
| Primary provider returns 429 (rate limit) | `HTTPStatusError(429)` | In the retry list. Rotates to the next provider immediately. |
| All providers are down | Multiple `ConnectError`s in sequence | After exhausting all providers, the last exception is raised. The caller can catch it and decide whether to retry the entire `memorize` call after a delay. |
| Two providers emit embeddings of different dimensions | Mixed dimensions in pgvector | Embeddings are pinned to the primary provider by design. There is no way to "accidentally" fall back to a different embedding dimension. |
| A new provider is added with an incompatible backend | `ValueError: Unsupported LLM provider 'foo'` at startup | Add the provider to `LLM_BACKENDS` in `http_client.py` (or reuse an existing backend for OpenAI-compatible APIs). |
| `vLLM` container is not running | `_build_fallback_providers` detects missing container and skips it | The fallback list silently omits `vllm` and the chain becomes `google -> nvidia`. No error, no log spam. |
| `NVIDIA_API_KEY` env var is not set | `_build_fallback_providers` skips nvidia | The chain becomes `google -> vllm`. |

---

## 7. Synergies and Future Potentials

### 7.1 Near-Term Wins (Low Effort, High Value)

1. **Weighted Round-Robin** for providers that *don't* return 429
   (e.g. you want to split traffic 70/30 across two providers to
   use up multiple free tiers). The current `FallbackLLMClient` is
   first-success-only, but its `stats` property is the natural place
   to drive a weighted scheduler.

2. **Persistent Stats & Alerting.** The in-memory `stats` dict
   survives only as long as the Python process. A small
   `SQLAlchemyStore` adapter could persist these counters to a new
   `provider_stats` table and trigger an alert when a provider's
   fallback-triggered count exceeds a threshold.

3. **Per-Provider Rate Limiting.** We currently rely on the
   provider's own rate limiter. If we wanted to be a good citizen and
   not even *attempt* the 16th request in a minute, we could add an
   `asyncio.Semaphore` (or a token-bucket) at the top of each
   provider in the chain. The `LLMInterceptorRegistry` already
   provides the natural integration point.

4. **Cost Tracking.** Each call has an associated dollar cost. By
   tracking (provider, model, input_tokens, output_tokens) per call,
   we could expose a `cost_per_minute` metric and let operators
   decide which providers to use based on economics, not just
   availability.

### 7.2 Medium-Term Ideas

5. **Vertex AI Integration.** Google Cloud's Vertex AI offers
   much higher limits than AI Studio and a slightly different
   endpoint structure. The `GoogleLLMBackend` could be extended to
   detect a `vertex` flag and switch the auth from
   `?key=...` to OAuth bearer tokens. The fallback chain would not
   need any other changes.

6. **Caching Layer.** Some LLM calls (especially the
   category-embedding pre-compute) are deterministic. Wrapping
   `FallbackLLMClient` with a `CacheLLMClient` that memoises
   `(prompt, provider) -> response` pairs in Redis would cut costs
   and reduce rate-limit pressure simultaneously. memU's
   `LLMClientWrapper` interceptor hook is the right integration
   point.

7. **Streaming Responses.** memU currently uses non-streaming
   `summarize` calls. For long-context tasks the latency is
   significant. The fallback logic is orthogonal to streaming — we
   can add `summarize_stream` to the `FallbackLLMClient` without
   changing the fallback behaviour.

8. **Adaptive Ordering.** If the primary provider has been returning
   429s for the last N minutes, promote the next provider to be
   primary. This is a self-healing system that responds to changing
   conditions without human intervention.

### 7.3 Long-Term Vision

9. **Provider Health Dashboard.** Expose a `/health/providers` HTTP
   endpoint that returns the current `stats` for all chains across
   all profiles. A Grafana dashboard on top of that becomes the
   single pane of glass for "which provider is failing right now".

10. **Cross-Profile Fallback.** Currently each `llm_profile`
    (default, embedding, etc.) has its own fallback list. A more
    sophisticated setup could share fallback providers across
    profiles, with profile-specific overrides.

11. **Provider Plugins.** Package each provider's adapter
    (`OpenAILLMBackend`, `GoogleLLMBackend`, etc.) as a separate
    pip-installable plugin. New providers could be added without
    touching the memU core. The current codebase is *structured* for
    this — the `LLM_BACKENDS` registry is a single dict — but the
    packaging work is a real project on its own.

---

## 8. Operational Runbook

### 8.1 First-Time Setup

1. **Install dependencies:** `pip install -e .`
2. **Configure environment:** Copy `.env.example` to `.env` and fill
   in the API keys you have.
3. **Start Docker:** `Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"`
4. **Start containers:** `docker compose up -d`
5. **Smoke-test the fallback:** `python test_fallback_smoke.py`
6. **Run a real memorise:** `python test-02-memorize.py --provider google`

### 8.2 Diagnosing "Why is fallback not kicking in?"

```python
# After creating a MemoryService, inspect the chain:
memory = create_memory_instance(provider="google", enable_fallback=True)
llm_client = memory._llm_clients["default"]
print(llm_client.stats)
# {'google/gemini-flash-latest@https://...': {'success': 42, 'fallback_triggered': 0, 'error': 0},
#  'nvidia/meta/llama-3.1-8b-instruct@https://...': {'success': 0, 'fallback_triggered': 3, 'error': 0}}
```

If `fallback_triggered` is zero across all providers, then either the
primary has been working fine or the errors you're hitting are not
4xx/5xx status codes (e.g. JSON parse errors). Set
`MEMU_LOG_LEVEL=DEBUG` to see the full request/response payloads.

### 8.3 Diagnosing "Why is my call still failing?"

1. Check `docker ps` — is the database up?
2. Check `curl http://localhost:8005/v1/models` — is vLLM up?
3. Check `curl -H "Authorization: Bearer $NVIDIA_API_KEY" https://integrate.api.nvidia.com/v1/models` — is the Nvidia key valid?
4. Run `python test_fallback_smoke.py` — does the multi-provider path itself work?
5. Enable `MEMU_LOG_LEVEL=DEBUG` and re-run the failing test.

---

## 9. Glossary

| Term | Meaning |
|---|---|
| **LLM** | Large Language Model. The thing that turns "summarise this text" into a summary. |
| **Provider** | A commercial (or self-hosted) service that serves LLM requests over HTTP. Examples: OpenAI, Google AI Studio, Nvidia NIM, vLLM. |
| **Backend** | In memU, the code module that knows how to format a request for one provider and parse its response. One backend per provider *format*. |
| **Profile** | A named LLM configuration inside `LLMProfilesConfig`. The `default` profile is for chat, the `embedding` profile is for embeddings, etc. |
| **Primary** | The first provider in a fallback chain. Has the highest priority. |
| **Fallback** | A provider that is only invoked when the primary (or a higher-priority fallback) returns a retryable error. |
| **Chain** | The ordered list `[primary, fallback1, fallback2, ...]`. |
| **Rotation** | The act of moving from one provider to the next in the chain after a retryable error. |
| **Embeddings** | Vector representations of text, used for similarity search. Different models produce different dimensions. |
| **pgvector** | A Postgres extension that stores and indexes vectors. memU uses it for retrieval. |
| **RPM** | Requests Per Minute. The most common rate-limit metric. |
| **RPD** | Requests Per Day. A daily quota. |
| **OpenAI-compatible API** | An HTTP service that exposes the same `/v1/chat/completions` and `/v1/embeddings` endpoints as OpenAI, with the same JSON payload shape and Bearer-token auth. Nvidia NIM, OpenRouter, Together.ai and others all do this. |
| **HTTP 429** | "Too Many Requests". The status code returned when you exceed the provider's rate limit. |
| **HTTP 5xx** | A family of server-error codes. Some are retryable (502, 503, 504), some are not (500 can be permanent or transient). |
| **Stat** | A counter maintained by `FallbackLLMClient` per provider. Counts successes, fallback triggers, and hard errors. |

---

## 10. Appendices

### Appendix A: Files Touched in This Change

| File | Change Type | Lines Added | Lines Removed |
|---|---|---|---|
| `src/memu/llm/fallback_client.py` | NEW | 280 | 0 |
| `src/memu/llm/http_client.py` | Modified | 8 | 0 |
| `src/memu/app/service.py` | Modified | 60 | 25 |
| `src/memu/app/settings.py` | Modified | 25 | 0 |
| `memu_factory.py` | Modified | 80 | 15 |
| `test_fallback_smoke.py` | NEW | 130 | 0 |
| `.env` | Modified | 4 | 0 (not committed) |

**Total: 587 lines added, 40 removed across 7 files.**

### Appendix B: Commit History

```
08d0fb0 feat: add multi-provider fallback infrastructure (Google -> Nvidia NIM -> vLLM)
ccb0239 feat: integrate Google AI embedding backend (gemini-embedding-001, 3072-dim)
bb5b4ef chore: restore global governance and clean up mission core
```

### Appendix C: API Format Reference

| Provider | Auth | Endpoint | Payload |
|---|---|---|---|
| OpenAI | `Authorization: Bearer KEY` | `POST /chat/completions` | `{"model": "gpt-4o-mini", "messages": [...]}` |
| Google AI | `?key=KEY` query param | `POST /v1beta/models/{MODEL}:generateContent` | `{"contents": [{"parts": [{"text": "..."}]}]}` |
| Nvidia NIM | `Authorization: Bearer KEY` | `POST /v1/chat/completions` | Same as OpenAI |
| vLLM | `Authorization: Bearer EMPTY` | `POST /v1/chat/completions` | Same as OpenAI |

The OpenAI/Nvidia/vLLM trio is API-identical. The Google AI format is
the odd one out, which is why we have a separate `GoogleLLMBackend`
and a separate `GoogleEmbeddingBackend` in the codebase.

### Appendix D: Rate Limits (Free Tiers, as of 2026-05)

| Provider | Model | RPM | RPD |
|---|---|---|---|
| Google AI | `gemini-2.5-flash` | 15 | 20 |
| Google AI | `gemini-flash-latest` | 15 | unlimited |
| Nvidia NIM | Llama 3.1 8B | 40 | 1,000/month |
| OpenAI | GPT-4o-mini | 3 (free) | 200 (free) |
| OpenRouter | varies | per-model | per-model |

**Why `gemini-flash-latest` is our default:** it has the highest
uncapped RPD, which makes it ideal as a primary in a free-tier
development workflow.

### Appendix E: Tested Configurations

The smoke test (`test_fallback_smoke.py`) verifies:

1. Module imports (catches syntax errors, missing imports).
2. Pydantic config validation (catches schema mismatches).
3. Backend registration (catches typos in provider names).
4. Factory configuration (catches runtime init errors).
5. End-to-end fallback behaviour with `unittest.mock` (catches
   rotation logic bugs without needing a network connection).
6. Multi-provider chain construction.
7. Per-provider stats tracking.

The test runs in well under 1 second and is safe to run on every
commit.

### Appendix F: Glossary of File Paths

For readers new to the codebase:

```
memU/
├── memu_factory.py              # Central config factory
├── test-02-memorize.py          # End-to-end memorise test
├── test-03-retrieve.py          # End-to-end retrieve test
├── test_fallback_smoke.py       # NEW: Fallback unit + integration tests
├── src/memu/
│   ├── app/
│   │   ├── service.py           # MemoryService (the orchestrator)
│   │   ├── settings.py          # Pydantic config models
│   │   ├── memorize.py          # Memorise workflow
│   │   └── retrieve.py          # Retrieve workflow
│   ├── llm/
│   │   ├── http_client.py       # HTTPLLMClient (single-provider)
│   │   ├── fallback_client.py   # NEW: FallbackLLMClient
│   │   ├── wrapper.py           # LLMClientWrapper (interceptors)
│   │   ├── openai_sdk.py        # OpenAI SDK client
│   │   └── backends/            # Provider-specific payload formats
│   │       ├── base.py
│   │       ├── openai.py
│   │       ├── google.py
│   │       ├── nvidia.py        # (alias of openai.py)
│   │       ├── grok.py
│   │       ├── doubao.py
│   │       └── openrouter.py
│   ├── embedding/
│   │   ├── http_client.py
│   │   └── backends/
│   │       ├── google.py        # Google embedding parser
│   │       └── ...
│   └── database/
│       └── postgres/            # pgvector store
├── docker-compose.yml           # postgres, vllm, open-webui
├── .env                         # API keys (gitignored)
└── REPORT.md                    # This document
```

---

## A Final Note

The multi-provider fallback is not magic. It is a relatively small
piece of plumbing (~280 lines of well-tested code) that exists because
the world we live in has rate-limited, quota-bound, sometimes-broken
public LLM APIs. By treating providers as interchangeable, ordered
resources, we make memU more reliable, more cost-efficient, and more
adaptable to changing conditions.

The implementation is intentionally minimal so that it is easy to
audit, easy to test, and easy to extend. When the next provider
arrives — whether it's a self-hosted model, a new cloud service, or
an internal corporate LLM — adding it to the chain is a one-line
change in `memu_factory.py`'s `PROVIDERS` dict, and the fallback
logic just works.

If you only remember one thing from this report, remember this:
**the chain is data, not code.** Adding a provider is configuration,
not refactoring. That's the design philosophy.
