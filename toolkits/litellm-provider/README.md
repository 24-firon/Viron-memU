# LiteLLM-Provider Bundle

> Patch-Bundle zur Integration des LiteLLM-Providers in `<TARGET>`.

## Zweck

Der LiteLLM-Provider macht den LiteLLM-Proxy als Single-Entry-Point für 22+ Modelle (OpenAI, Anthropic, Gemini, Mistral, Ollama, ...) im `<TARGET>` nutzbar. Das Bundle liefert atomare Patches (git-diff outputs), die manuell auf einen sauberen `origin/main` Stand des `<TARGET>` Repos angewendet werden — so bleibt die Integration reproduzierbar und rollback-fähig.

## Inhalt

- `patches/M1-scaffolding.patch` — ProviderDescriptor, Factory, Defaults
- `docs/PLAN-LITELLM-PROVIDER.md` — Vollständiger Plan mit M1–M4
- `STATUS.md` — Aktueller Stand der Implementierung
- `APPLY.md` — Anleitung zum Anwenden der Patches
- `tests/verify-m1.md` — Verifikations-Schritte für M1

## Voraussetzungen

- `<TARGET>` ist geklont und liegt auf `origin/main` (Working Tree sauber)
- Python 3.14, `uv` ist installiert
- Keine weiteren Modifikationen im Working Tree

## Workflow

1. **Pre-Flight-Check:** `docs/PRE-FLIGHT-CHECK.md` lesen **bevor** Patches angewendet werden
2. Patch anwenden: `git apply patches/M1-scaffolding.patch`... (siehe `APPLY.md`)
3. Verifizieren: siehe `tests/verify-m1.md`
4. Committen: optional, siehe `APPLY.md`

## M4 Live-E2E
- Ziel-Proxy: factory-litellm-router (Port 4000, 22 Modelle)
- Key: LITELLM_API_KEY=sk-litellm-factory-... (aus Docker-Container-Env)
- Status: ✅ erfolgreich getestet

## Erstellungsdatum
2026-06-27
