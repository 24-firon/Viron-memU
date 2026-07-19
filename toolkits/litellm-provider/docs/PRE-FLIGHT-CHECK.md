# PRE-FLIGHT-CHECK — Vor jedem Provider-Bundle

> **Single Point of Truth** für die Phase 0 vor jedem Provider-Bundle.
> **Lessons Learned:** Beim LiteLLM-Provider-Bundle (M1-M4) wurden 3 Stunden Code-Architektur investiert, BEVOR geprüft wurde, ob die Ziel-Infrastruktur überhaupt mit den vorhandenen Credentials erreichbar ist. Hätte 30 Sekunden gedauert.

## Wann diesen Check ausführen?

**VOR M1** (ProviderDescriptor im Catalog). Nicht nach M2, nicht nach M3. Vor dem ersten Patch.

## 4-Schritte-Check (Dauer: ca. 2-5 Minuten)

### 1. Läuft der Ziel-Dienst überhaupt?

```bash
# Docker-Container?
docker ps | grep <service-name>

# Port offen?
Test-NetConnection -ComputerName 127.0.0.1 -Port <port>

# Health-Endpoint?
curl -s http://127.0.0.1:<port>/health
curl -s http://127.0.0.1:<port>/health/readiness   # LiteLLM-spezifisch
```

**Erwartet:** Service antwortet (200 OK oder Auth-401). Wenn keine Antwort: STOPP, Service erst starten.

### 2. Haben wir gültige Credentials?

```bash
# Versuche es mit den vorhandenen API-Keys aus der .env
docker inspect <container-name> 2>&1 | Select-String "MASTER_KEY|API_KEY"
# oder manuell:
curl -s -H "Authorization: Bearer $KEY" http://127.0.0.1:<port>/v1/models
```

**Was zu prüfen ist:**
- Schlüssel-Format (manche Proxies verlangen `sk-` Prefix, manche nicht)
- Authentifizierung akzeptiert (200 OK vs 401 Unauthorized)
- Response-Body valid (JSON mit erwarteten Feldern)

**Wenn 401:** Schlüssel-Format prüfen, in Container-Env nachschauen, ggf. neuen Master-Key generieren.

### 3. Welches Transport-Format erwartet der Dienst?

| Format | Beispiel | Provider-Kategorie im `<TARGET>` |
|---|---|---|
| OpenAI Chat Completions | `/v1/chat/completions` | `openai_chat` |
| Anthropic Messages | `/v1/messages` | `anthropic_messages` |
| Custom | z.B. `/generate` | Eigener Adapter nötig |

**Prüfung:**
```bash
# OpenAI-kompatibel? Teste mit:
curl -s -X POST -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"model":"gpt-3.5-turbo","messages":[{"role":"user","content":"hi"}]}' \
  http://127.0.0.1:<port>/v1/chat/completions
```

Falls `/v1/chat/completions` antwortet: → OpenAI-Chat-Provider (`OpenAIChatTransport`)
Falls `/v1/messages` antwortet: → Anthropic-Messages-Provider (`AnthropicMessagesTransport`)
Falls was anderes: Eigener Adapter nötig (nicht 1:1 wie opencode-Pattern)

### 4. Welche Modelle sind verfügbar?

```bash
curl -s -H "Authorization: Bearer $KEY" http://127.0.0.1:<port>/v1/models
```

**Notieren:**
- Anzahl Modelle (für späteren Vergleich nach Provider-Bau)
- Echte Modell-IDs (für `MODEL=provider_id/<model_id>` Konfiguration)
- Free vs Paid Marker (für Default-MODEL-Wahl)

**Beispiel LiteLLM-Response:**
```json
{"data": [{"id": "llama-3.1-70b"}, {"id": "minimax-m3"}, ...]}
```

## Checklist für den Provider-Code

Erst NACH diesem Check anfangen zu coden. Vorher nicht.

- [ ] Service läuft
- [ ] Credentials funktionieren (kein 401)
- [ ] Transport-Format identifiziert
- [ ] Model-Liste dokumentiert
- [ ] Mindestens 1 Modell für E2E-Test verfügbar
- [ ] Operator-Aktionen klar (Wer startet den Service? Wer hat die Keys?)

## Bei Mismatch oder Failure

**NICHT** mit dem Code-Bau anfangen. Stattdessen:

1. Operator informieren: "Pre-Flight-Check fehlgeschlagen. Bitte Service-Setup prüfen."
2. Bundle dokumentieren mit Status "blocked" statt "in progress"
3. Optional: Mock-Service für statische Tests nutzen, Live-E2E auf später verschieben

## Wann diesen Check RE-RUN?

- Vor jedem neuen Bundle-Build
- Nach Windows-Update (kann Ports/Env-Vars ändern)
- Nach Docker-Container-Recreate
- Nach Provider-Wechsel im `MODEL=`

## Referenz: LiteLLM-Bundle-Erfahrung

**Was lief gut:** Patch-Struktur, SubAgent-Workflow, Tests grün.

**Was schief ging:** 3 Stunden Code-Architektur, DANN erst gemerkt, dass der LiteLLM-Proxy auf Port 4000 mit unserer Master-Key nicht funktioniert. Master-Key war im Container-Env (`docker inspect`), nicht in unserer `.env`. **30-Sekunden-Check hätte das vermieden.**

**Was wir beim nächsten Mal machen:** DIESER CHECK steht am Anfang der Bundle-Doku.
