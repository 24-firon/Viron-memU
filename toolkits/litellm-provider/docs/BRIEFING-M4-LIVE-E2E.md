# SubAgent-Briefing M4 — Live-E2E mit echtem LiteLLM-Proxy

> **Briefing für:** Hauptmodel bewertet (🔴 STARK), NICHT SubAgent — M4 ist Operator-Aktion
> **Ziel:** Vollständiges End-to-End mit echtem LiteLLM-Proxy auf `127.0.0.1:4000`
> **Voraussetzung:** M1+M2+M3+M2c+M2d Patches applied, `LITELLM_API_KEY` in persönliche `.env`

---

## A) MISSION

Verifikation des LiteLLM-Providers mit echtem LiteLLM-Proxy:

1. **LiteLLM-Proxy-Erreichbarkeit prüfen** (vor dem Patch-Apply)
2. **Persönliche `.env` konfigurieren** (LITELLM_API_KEY + LITELLM_BASE_URL)
3. **Patches anwenden** (M1+M2+M3+M2c+M2d)
4. **Server starten + Model-Discovery testen**
5. **End-to-End mit echtem Claude-CLI**
6. **Doku-Updates** in `<CONFIG_REPO>/`

**WICHTIG:** M4 ist KEIN SubAgent-Task. M4 erfordert Operator-Interaktion (LiteLLM-Proxy muss laufen, persönliche `.env` muss editiert werden, Claude-CLI muss manuell getestet werden). Hauptmodel führt Schritt 1-3 aus, Operator führt 4-5 aus, Hauptmodel schreibt Doku.

## B) CONTEXT

### Warum M4?
Die statische Konfiguration ist fertig (M1-M2d). Aber wir wissen nicht, ob die Integration **tatsächlich** mit echtem LiteLLM-Proxy funktioniert. M4 verifiziert:
- LiteLLM-Proxy antwortet
- /v1/models listet LiteLLM-Modelle
- Proxy-Request via `/v1/messages` (Claude-CLI-Format) wird zu OpenAI-Format konvertiert
- OpenAI-Chat-Completion-Response wird zu Anthropic-SSE konvertiert
- Tool-Calls funktionieren (falls vorhanden)
- Thinking-Blocks werden korrekt weitergereicht

### LiteLLM-Proxy-Architektur
```
Claude-CLI (Anthropic-Format)
    ↓ POST /v1/messages
FCC-Proxy (`<TARGET>` auf 127.0.0.1:18082)
    ↓ Model-Routing: litellm/<model> → LiteLLMProvider
LiteLLM-Proxy (auf 127.0.0.1:4000)
    ↓ Model-Routing
OpenAI / OpenRouter / NIM / local-vllm
```

## C) VORBEDINGUNG

### Vor M4-Start prüfen

1. **LiteLLM-Proxy läuft auf `127.0.0.1:4000`:**
   ```bash
   curl -s -H "Authorization: Bearer $LITELLM_MASTER_KEY" http://127.0.0.1:4000/v1/models | jq '.data | length'
   ```
   **Erwartet:** 22+ Modelle

2. **Persönliche `.env` existiert:** `<TARGET>/.env`

3. **`fcc-claude` Helper im PowerShell-Profil:** Aus `<CONFIG_REPO>/fcc-profile.ps1` installiert

4. **Claude-CLI installiert:**
   ```bash
   Get-Command claude
   ```
   **Erwartet:** Pfad zu `claude.exe` (npm-Installation)

## D) ATOMARE SCHRITTE

### Schritt 1: Pre-Flight-Check (Hauptmodel, 🔴 STARK)

LiteLLM-Proxy-Erreichbarkeit testen:

```bash
curl -s -H "Authorization: Bearer $LITELLM_MASTER_KEY" http://127.0.0.1:4000/v1/models | Select-String "data"
```

**Erwartet:** JSON mit `data`-Array

Falls LiteLLM nicht erreichbar: STOPP. Operator informieren: "LiteLLM-Proxy muss auf 127.0.0.1:4000 laufen. Bitte starten."

### Schritt 2: Persönliche `.env` editieren (Operator-Aktion)

Operator editiert `<TARGET>/.env` und fügt hinzu:

```bash
# LiteLLM Provider (für E2E-Test)
LITELLM_API_KEY="<master-key-aus-liteLLM-proxy>"
LITELLM_BASE_URL="http://127.0.0.1:4000"
# LITELLM_PROXY=""  # leer lassen (kein HTTP-Proxy für Upstream)
```

`LITELLM_API_KEY` ist der Master-Key des LiteLLM-Proxys (nicht der OpenRouter-Key o.ä.).

### Schritt 3: Patches anwenden (Hauptmodel, 🔴 STARK)

```bash
$BP = "<TOOLKIT>/patches"
cd <TARGET>
git apply "$BP/M1-scaffolding.patch"
git apply "$BP/M2-implementation.patch"
git apply "$BP/M3-tests.patch"
git apply "$BP/M2c-settings.patch"
git apply "$BP/M2d-admin-env.patch"
```

**Erwartet:** Alle 5 Patches ohne Fehler

Smoke-Test:
```bash
cd <TARGET>
uv run python -c "
from providers.litellm import LiteLLMProvider, LITELLM_DEFAULT_BASE
from providers.registry import PROVIDER_FACTORIES
from config.settings import Settings
assert LITELLM_DEFAULT_BASE == 'http://127.0.0.1:4000'
assert 'litellm' in PROVIDER_FACTORIES
print('OK: 12 provider, litellm registered')
"
```

### Schritt 4: Server starten + Model-Discovery (Hauptmodel, 🟡 MITTEL)

```bash
fcc-restart
```

Wait 5-10 Sekunden. Dann:

```bash
fcc-status
```

**Erwartet:** "Status: RUNNING (PID: xxx)"

Model-Discovery prüfen:
```bash
curl -s -H "x-api-key: $ANTHROPIC_AUTH_TOKEN" http://127.0.0.1:18082/v1/models | jq '.data | map(.id) | map(select(startswith("litellm/"))) | length'
```

**Erwartet:** 22 (oder Anzahl LiteLLM-Modelle)

Falls 0 Modelle: STOPP. LiteLLM-Proxy antwortet nicht korrekt. Logs prüfen mit `Get-Content C:\Users\bachl\.fcc\logs\server.log -Tail 20`.

### Schritt 5: End-to-End-Test (Operator-Aktion)

Operator startet in PowerShell:
```powershell
fcc-claude
```

Im Claude-CLI-Prompt:
```
/model litellm/<model-name>
```

Wähle ein LiteLLM-Modell, z.B. `litellm/gpt-4o-mini` oder `litellm/claude-3-5-sonnet`. Dann:

```
Reply with exactly: PONG
```

**Erwartet:** Antwort "PONG" oder ähnlich

Falls Crash oder Timeout: Logs prüfen:
```powershell
Get-Content C:\Users\bachl\.fcc\logs\server.log -Tail 50
```

Häufige Fehler:
- **401 Unauthorized:** `LITELLM_API_KEY` falsch oder fehlt
- **404 Model not found:** Model-Name falsch (Format: `litellm/<name>`)
- **500 Internal Server Error:** LiteLLM-Proxy kann Upstream nicht erreichen
- **Timeout:** `http_read_timeout=300` (in Settings) könnte zu kurz sein

### Schritt 6: Erweiterte Tests (Operator-Aktion, optional)

Falls einfacher E2E-Test grün, teste komplexere Szenarien:

```
/model litellm/<thinking-model>
Was ist 2+2? Zeige dein Thinking.
```

**Erwartet:** Thinking-Block + Text-Block in Antwort

Falls Tool-Calls benötigt werden:
```
/model litellm/<tool-capable-model>
List files in current directory.
```

**Erwartet:** Tool-Call (Bash oder Read) + Antwort

### Schritt 7: Doku-Updates (Hauptmodel, 🔴 STARK)

Wenn E2E-Test grün:

1. **`<CONFIG_REPO>/HANDOVER.md`** aktualisieren:
   - Neuer Abschnitt "LiteLLM-Provider (M4 Live-E2E grün)"
   - Liste der LiteLLM-Modelle, die getestet wurden
   - Hinweise zu Edge-Cases

2. **`<CONFIG_REPO>/BETRIEBSHANDBUCH.md`** aktualisieren:
   - LiteLLM in Modell-Liste aufnehmen
   - Quick-Reference: "Modell wechseln auf LiteLLM"
   - Troubleshooting-Section für LiteLLM-spezifische Fehler

3. **`<TOOLKIT>/STATUS.md`** aktualisieren:
   - M4-Status auf "✅ Fertig" setzen
   - Getestete Modelle auflisten

4. **`<CONFIG_REPO>/PLAN-LITELLM-PROVIDER.md`** aktualisieren:
   - M4 DoD-Check abhaken
   - Bundle-Status: alle 5 Patches + alle Tests grün

### Schritt 8: Working Tree cleanen (Hauptmodel, 🟡 MITTEL)

**WICHTIG:** KEIN git commit. Patches sind im Bundle, Working Tree muss clean sein.

```bash
cd <TARGET>
git checkout -- .
Remove-Item -LiteralPath "providers\litellm" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath "tests\providers\test_litellm_provider.py" -Force -ErrorAction SilentlyContinue
```

### Schritt 9: Bundle committen (Operator-Aktion, optional)

Falls Operator das Bundle in `<CONFIG_REPO>` versionieren will:
```bash
cd <CONFIG_REPO>
git status
git add <TOOLKIT_PARENT>/
git commit -m "Bundle LiteLLM-Provider: M1+M2+M2c+M3+M2d komplett, E2E grün"
```

## E) EDGE-CASES

1. **LiteLLM-Proxy-Version:** Verschiedene LiteLLM-Versionen haben verschiedene Model-Listen. Aktuelle Version (lt. SUBAGENT_2_CONTAINER_TEST_REPORT) ist `ghcr.io/berriai/litellm:v1.85.0`. Bei Updates Model-Count prüfen.

2. **Anthropic-zu-OpenAI-Konvertierung:** Der Proxy konvertiert Anthropic-Format zu OpenAI-Format via `AnthropicToOpenAIConverter`. Edge-Cases: Tool-Use, Thinking, Multi-Turn. Alle in M2's `request.py` getestet.

3. **Streaming vs Non-Streaming:** Claude-CLI nutzt Streaming. Test sollte als Stream laufen. Falls Operator `claude --print` nutzt, ist es Non-Streaming. Beide sollten funktionieren.

4. **Rate-Limits:** LiteLLM-Proxy hat eigene Rate-Limits. Bei vielen schnellen Requests könnte 429 zurückkommen. Bei M4 nur ein Test-Request.

5. **Virtual-Keys:** Operator könnte später Virtual-Keys (statt Master-Key) nutzen. Für M4 reicht Master-Key.

6. **HTTPS vs HTTP:** Lokales LiteLLM ist HTTP. Falls Operator TLS aktiviert hat, URL anpassen.

## F) ERFOLGS-KRITERIEN

- [ ] LiteLLM-Proxy erreichbar (Pre-Flight grün)
- [ ] Persönliche `.env` mit `LITELLM_API_KEY` und `LITELLM_BASE_URL` editiert
- [ ] 5 Patches ohne Fehler angewendet
- [ ] Smoke-Test grün
- [ ] `fcc-restart` startet Server sauber
- [ ] `/v1/models` listet 22+ LiteLLM-Modelle
- [ ] `fcc-claude` + Model-Wechsel + Test-Message → Antwort erhalten
- [ ] Optional: Thinking-Test grün
- [ ] Optional: Tool-Call-Test grün
- [ ] Doku-Updates in `<CONFIG_REPO>/` geschrieben
- [ ] Working Tree clean in `<TARGET>/`

## G) OUTPUT-BERICHT

Gib mir:
- "Pre-Flight: [erreichbar/nicht]"
- "Patches: [alle 5 angewendet ja/nein]"
- "Server-Status: [RUNNING/FAILED]"
- "Model-Discovery: [N Modelle]"
- "E2E-Test: [PONG erhalten/Fehler: ...]"
- "Doku-Updates: [geschrieben/nicht]"
- "Working Tree: [clean/dirty]"

## H) MODEL-STÄRKE

🔴 STARK für gesamtes M4 — E2E-Tests erfordern Interpretation von Fehlern und architektonisches Verständnis der Provider-Kette. Operator führt 2-3 manuelle Schritte aus (PowerShell, Claude-CLI), Hauptmodel koordiniert.
