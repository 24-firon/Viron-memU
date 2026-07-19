# SubAgent-Briefing M2.A — LiteLLM Provider Implementation

> **Briefing für:** SubAgent mit 🟡 MITTEL-Model
> **Ziel-Verzeichnis:** `<TARGET>/providers/litellm/`
> **Vorlage:** `<TARGET>/providers/opencode/` (3 Dateien)
> **Output:** 3 Dateien erstellen + Patch generieren + Tests verifizieren
> **Stop-Bedingungen:** Nach 3 Dateien oder 10 Minuten Timeout

---

## A) MISSION

Erstelle die LiteLLM-Provider-Implementation im Verzeichnis `providers/litellm/`. Pattern ist 1:1 wie `providers/opencode/`, mit folgenden Substitutionen:
- Klassenname: `LiteLLMProvider`
- Log-Tag: `LITELLM`
- Base-URL-Import: `LITELLM_DEFAULT_BASE`
- Request-Log-Tag: `LITELLM_REQUEST`

**WICHTIG:** Die Edits werden NUR im Working Tree gemacht, NICHT committed. Nach Verifikation wird ein Patch generiert und in `toolkits/litellm-provider/patches/M2-implementation.patch` gespeichert.

## B) CONTEXT

### Warum dieser Provider?
LiteLLM-Proxy ist ein Single-Entry-Point für 22+ Modelle. Erbt von `OpenAIChatTransport` (LiteLLM spricht `/v1/chat/completions`).

### Vorhandene Vorlage
`providers/opencode/` enthält:
- `__init__.py` (10 Zeilen)
- `client.py` (31 Zeilen)
- `request.py` (35 Zeilen)

### Wichtige Imports
```python
from providers.base import ProviderConfig
from providers.defaults import LITELLM_DEFAULT_BASE
from providers.openai_compat import OpenAIChatTransport
```

`LITELLM_DEFAULT_BASE` ist in `providers/defaults.py` bereits re-exportiert.

## C) SCOPE

### ✅ Erlaubt
- 3 Dateien in `<TARGET>/providers/litellm/` erstellen
- Smoke-Test mit `uv run python`
- Patch generieren und in Bundle speichern
- **Edits im Working Tree (kein Commit)**

### ❌ Verboten
- `git commit` — KEIN Commit!
- `git add` für `providers/litellm/` — Working Tree bleiben lassen
- Andere Dateien anfassen

## D) ATOMARE SCHRITTE

### Schritt 1: Vorlage lesen
Lies 3 Dateien VOLLSTÄNDIG:
1. `<TARGET>/providers/opencode/__init__.py`
2. `<TARGET>/providers/opencode/client.py`
3. `<TARGET>/providers/opencode/request.py`

### Schritt 2: `providers/litellm/__init__.py` erstellen (10 Zeilen)
Muster wie `opencode/__init__.py`, mit:
- Import `LITELLM_DEFAULT_BASE` aus `providers.defaults`
- Import `LiteLLMProvider` aus `.client`
- `__all__` mit beiden Namen

### Schritt 3: `providers/litellm/request.py` erstellen (35 Zeilen)
Muster wie `opencode/request.py`, mit:
- Logger-Tag-Strings: `"LITELLM_REQUEST: conversion start model=..."` und `"LITELLM_REQUEST: conversion done model=..."`
- Funktion: `def build_request_body(request_data: Any, *, thinking_enabled: bool) -> dict:`

### Schritt 4: `providers/litellm/client.py` erstellen (31 Zeilen)
Muster wie `opencode/client.py`, mit:
- Klassenname: `class LiteLLMProvider(OpenAIChatTransport):`
- `__init__`: `provider_name="LITELLM"`, `base_url=config.base_url or LITELLM_DEFAULT_BASE`
- Docstring: `"""LiteLLM provider using \`http://127.0.0.1:4000/v1/chat/completions\`."""`

### Schritt 5: Smoke-Test
```bash
cd <TARGET>
uv run python -c "from providers.litellm import LiteLLMProvider, LITELLM_DEFAULT_BASE; print('OK:', LITELLM_DEFAULT_BASE)"
```
**Erwartet:** `OK: http://127.0.0.1:4000`

### Schritt 6: Patch generieren
```bash
cd <TARGET>
mkdir -p <TOOLKIT>/patches
git diff -- providers/litellm/ > <TOOLKIT>/patches/M2-implementation.patch
```

### Schritt 7: Patch prüfen
```bash
ls -la <TOOLKIT>/patches/M2-implementation.patch
head -20 <TOOLKIT>/patches/M2-implementation.patch
```

### Schritt 8: Working Tree NICHT committen
**WICHTIG:** KEIN `git add`, KEIN `git commit`. Working Tree bleibt mit den neuen Dateien (untracked), Patch ist im Bundle.

### Schritt 9: Stop
STOP und auf Bewertung warten.

## E) EDGE-CASES

1. **Verzeichnis `providers/litellm/` existiert nicht:** Erstelle es mit `New-Item -ItemType Directory -Path "<TARGET>/providers/litellm" -Force`

2. **Loguru-Lock-Deadlock in Tests:** IGNORIEREN — Pre-Existing.

3. **`git diff -- providers/litellm/` ist leer:** Falls Working Tree keine Änderungen zeigt, wurden die Dateien nicht erkannt. Stelle sicher dass `providers/litellm/__init__.py` etc. existieren und `git status` sie als untracked zeigt.

## F) ERFOLGS-KRITERIEN

- [ ] 3 Dateien in `providers/litellm/` erstellt
- [ ] Smoke-Test: `OK: http://127.0.0.1:4000` ausgegeben
- [ ] Patch `M2-implementation.patch` existiert im Bundle (sollte ~80 Zeilen sein)
- [ ] Working Tree zeigt `providers/litellm/__init__.py` etc. als untracked
- [ ] KEIN `git commit` ausgeführt

## G) MODEL-STÄRKE

🟡 MITTEL — Klare 1:1 Vorlage, 4 Substitutionen. Pattern-Mutation.
