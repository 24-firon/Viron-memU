# SubAgent-Briefing M2.D — Admin-UI + .env.example

> **Briefing für:** SubAgent mit 🟡 MITTEL-Model
> **Voraussetzung am Working Tree:** M1 + M2 + M3 + M2c Patches bereits applied
> **Output:** 2 File-Edits + 1 Patch-File im Bundle
> **Stop-Bedingungen:** Nach 3 Schritten oder 15 Minuten Timeout

---

## A) MISSION

Schließe die M2.D-Lücke:
1. **`api/admin_config.py`:** 3 neue `ConfigFieldSpec` Einträge für LiteLLM hinzufügen
2. **`.env.example`:** LiteLLM-Sektion dokumentieren
3. **Patch generieren und im Bundle speichern**

## B) CONTEXT

### Warum diese Edits?
- Der LiteLLM-Provider ist implementiert (M1+M2) mit Settings (M2c) und Tests (M3)
- Das Admin-UI zeigt aktuell nur die bekannten Provider; LiteLLM muss für Operator konfigurierbar sein
- Die `.env.example` ist die Dokumentation für Operator, welche Env-Vars gesetzt werden können

### Vorhandene Admin-UI-Pattern

Lies `<TARGET>/api/admin_config.py` Zeile 161-178 (`OPENCODE_GO_API_KEY` und `OPENCODE_GO_PROXY` Specs). Pattern:

```python
ConfigFieldSpec(
    "OPENCODE_GO_API_KEY",
    "OpenCode Go API Key",
    "providers",
    "secret",
    settings_attr="opencode_go_api_key",
    secret=True,
    description="OpenCode Go subscription API key (separate from OpenCode Zen).",
),
ConfigFieldSpec(
    "OPENCODE_GO_PROXY",
    "OpenCode Go Proxy",
    "providers",
    "secret",
    settings_attr="opencode_go_proxy",
    secret=True,
    advanced=True,
),
```

### Vorhandene .env.example-Pattern

Lies `<TARGET>/.env.example` Zeile 21-27 (OpenCode Go Sektion). Pattern:

```bash
# OpenCode Go Config (OpenAI-compatible Chat Completions at opencode.ai/go/v1)
# Separate subscription from OpenCode Zen; uses 'go/' model id prefix.
OPENCODE_GO_API_KEY=""
```

Plus die Proxy-Sektion Zeile 84-93:

```bash
OPENCODE_PROXY=""
OPENCODE_GO_PROXY=""
ZAI_PROXY=""
```

## C) SCOPE

### ✅ Erlaubt
- 3 ConfigFieldSpec-Einträge in `api/admin_config.py` hinzufügen
- LiteLLM-Sektion in `.env.example` hinzufügen (API_KEY + BASE_URL Zeilen, evtl. PROXY)
- Patch generieren: `git diff > <TOOLKIT>/patches/M2d-admin-env.patch`

### ❌ Verboten
- KEIN `git commit`
- KEIN `git add`
- KEINE anderen Dateien anfassen
- `OPENCODE_GO_*` Specs nicht ändern (nur als Vorlage lesen)
- KEINE neuen Test-Files oder Settings-Fields (M2c hat das bereits gemacht)

## D) ATOMARE SCHRITTE

### Schritt 1: Admin-UI-ConfigFields hinzufügen

Lies `<TARGET>/api/admin_config.py` Zeile 161-180 als Vorlage.

Füge NACH dem `OPENCODE_GO_PROXY` ConfigFieldSpec-Block (Ende Zeile 180) einen neuen Block ein:

```python
    ConfigFieldSpec(
        "LITELLM_API_KEY",
        "LiteLLM API Key",
        "providers",
        "secret",
        settings_attr="litellm_api_key",
        secret=True,
        description="LiteLLM Proxy master key (or virtual key for budget tracking).",
    ),
    ConfigFieldSpec(
        "LITELLM_BASE_URL",
        "LiteLLM Base URL",
        "providers",
        settings_attr="litellm_base_url",
        default="http://127.0.0.1:4000",
        description="LiteLLM Proxy URL. Use 'http://litellm:4000' inside Docker.",
    ),
    ConfigFieldSpec(
        "LITELLM_PROXY",
        "LiteLLM Proxy",
        "providers",
        "secret",
        settings_attr="litellm_proxy",
        secret=True,
        advanced=True,
    ),
```

**WICHTIG:**
- Position: NACH `OPENCODE_GO_PROXY` Spec (alphabetisch nach Provider-Name, aber `litellm` kommt nach `opencode_go` — also direkt danach)
- `LITELLM_BASE_URL` ist NICHT `secret=True` (es ist eine URL, kein Geheimnis)
- `LITELLM_PROXY` ist `secret=True` und `advanced=True` (HTTP-Proxy kann credentials enthalten)

### Schritt 2: .env.example Sektion hinzufügen

Lies `<TARGET>/.env.example` Zeile 21-28.

Füge NACH der OpenCode Go Sektion (Ende Zeile 28) einen neuen Block ein:

```bash

# LiteLLM Config (OpenAI-compatible Chat Completions at litellm-server)
# Use LiteLLM Proxy as a single-entry-point for 22+ models from
# NVIDIA NIM, OpenCode Go/Zen, OpenRouter, local-vllm, etc.
LITELLM_API_KEY=""
LITELLM_BASE_URL="http://127.0.0.1:4000"
```

Plus in der Provider-Proxy-Sektion (Zeile 84-93), füge zwischen `OPENCODE_GO_PROXY=""` und `ZAI_PROXY=""` ein:

```bash
LITELLM_PROXY=""
```

**WICHTIG:**
- Format ist exakt wie OpenCode Go: API_KEY + Kommentar + BASE_URL-Zeile mit Default
- Position: nach OpenCode Go, vor ZAI (alphabetisch)
- Default BASE_URL: `http://127.0.0.1:4000` (lokales LiteLLM)

### Schritt 3: Verifikation

Prüfe mit `git diff -- api/admin_config.py .env.example | head -40` ob die Edits korrekt sind.

Optional: Smoke-Test mit dem Admin-UI-Endpoint (falls Server läuft):
```bash
cd <TARGET>
uv run python -c "
from api.admin_config import FIELDS
keys = [f.key for f in FIELDS]
assert 'LITELLM_API_KEY' in keys
assert 'LITELLM_BASE_URL' in keys
assert 'LITELLM_PROXY' in keys
print('Admin-UI-LiteLLM-Fields:', [k for k in keys if 'LITELLM' in k])
"
```
**Erwartet:** `['LITELLM_API_KEY', 'LITELLM_BASE_URL', 'LITELLM_PROXY']`

### Schritt 4: Patch generieren

```bash
cd <TARGET>
git diff -- api/admin_config.py .env.example > <TOOLKIT>/patches/M2d-admin-env.patch
```

### Schritt 5: Working Tree NICHT committen

**WICHTIG:** KEIN `git commit`, KEIN `git add`. Patch ist im Bundle.

### Schritt 6: STOP

STOP. SubAgent-Output an Hauptmodel. Hauptmodel bewertet mit 🔴 STARK.

## E) EDGE-CASES & GOTCHAS

1. **Encoding:** `.env.example` ist Plain-Text, UTF-8. Keine Sonderzeichen außer ASCII.

2. **Kommentar-Stil in .env.example:** Beginnen mit `# ` (Hash + Space), dann Beschreibung. Siehe Vorlage.

3. **Position in `FIELDS` Liste:** `ConfigFieldSpec` ist eine flache Tuple-Liste, nicht in Sektionen unterteilt (Sections werden separat definiert). Position nach Provider-Name alphabetisch.

4. **Validation in `ConfigFieldSpec`:** `field_type="secret"` für Secrets, `"text"` für URLs, `"number"` für Zahlen, `"select"` für Enums. `LITELLM_BASE_URL` ist ein Text-Input.

5. **`description`-Text:** Kurz, prägnant. Maximal 1-2 Sätze. Siehe Vorlagen.

6. **Section `providers`:** Alle Provider-bezogenen ConfigFieldSpecs gehören in Section `providers` (nicht `models`, `runtime`, etc.).

7. **CRLF-Warnings:** Ignorieren (Windows).

## F) ERFOLGS-KRITERIEN

- [ ] 3 ConfigFieldSpec-Einträge in `api/admin_config.py` (LITELLM_API_KEY, LITELLM_BASE_URL, LITELLM_PROXY)
- [ ] LiteLLM-Sektion in `.env.example` mit LITELLM_API_KEY und LITELLM_BASE_URL
- [ ] LITELLM_PROXY in Proxy-Sektion
- [ ] Optional: Smoke-Test grün (FIELDS enthält LITELLM_*)
- [ ] Patch `M2d-admin-env.patch` im Bundle generiert
- [ ] Working Tree hat Changes (M oder A), aber KEIN `git commit`

## G) OUTPUT-BERICHT

Gib mir zurück:
- "Admin-UI-Fields: [3 Specs hinzugefügt]"
- ".env.example Sektion: [vorhanden ja/nein]"
- "Smoke-Test: [OK/Nicht ausgeführt]"
- "Patch: [Pfad + Bytes]"
- "Working Tree Status: [M/A pro file]"

## H) MODEL-STÄRKE

🟡 MITTEL — Pattern-Mutation: kopiere `OPENCODE_GO_*` ConfigFieldSpec, substituiere `OPENCODE_GO` → `LITELLM`. Position in alphabetischer Reihenfolge. Kommentar-Text in .env.example leicht angepasst. Keine Architektur-Entscheidungen.
