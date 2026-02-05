# LOCAL GEMINI RULES (VIRON-MEMU)

_Behavioral rules specific to this project context._

## 1. DOKUMENTATION

- **Protocol Log**: Maintain `PROTOCOL_LOG.md` for all actions.
- **Decision Log**: Maintain `DECISION_LOG.md` for arch/tech choices (Postgres, vLLM).

## 2. FILE SCOPE

- **Native execution**: Use `python` directly (since Docker is bypassed).
- **Testing**: Use `uv run` for tests.
