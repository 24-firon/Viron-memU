---
toolkit: litellm-provider
version: 2.0
stand: 2026-06-28
zweck: LiteLLM als lokalen OpenAI-kompatiblen Proxy deployen
---

# RECIPE > litellm-provider

Dieses Bundle installiert **LiteLLM als OpenAI-kompatiblen Proxy** auf deiner Maschine. Einmal aufgesetzt, kann jeder OpenAI-kompatible Client (Python, Node, cURL, jeder LLM-Agent) LiteLLM als Backend nutzen.

**Was dieses Bundle macht:**
- LiteLLM Docker-Container starten
- 22+ Modelle (OpenAI, Anthropic, Gemini, Mistral, Ollama, NVIDIA NIM, OpenRouter) konfigurieren
- Eine einzige OpenAI-kompatible API auf `http://127.0.0.1:4000/v1` bereitstellen

**Was dieses Bundle NICHT macht:**
- Deinen Agent-Code patchen
- Deine Provider-Registry erweitern
- Eine Web-UI für dich bauen

**Was du brauchst:**
- Docker installiert
- API-Keys für die Upstream-Provider, die du nutzen willst
- 5 Minuten Zeit

---

## Schritt 0: Voraussetzungen prüfen

Bevor du loslegst:

```bash
docker --version
docker ps
```

Erwartet: Docker ist installiert und der Daemon läuft. Falls nicht: Installiere [Docker Desktop](https://www.docker.com/products/docker-desktop/).

---

## Schritt 1: Konfiguration vorbereiten

Kopiere die Template-Config:

```bash
cp config/secrets.example.yaml config/secrets.yaml
```

Öffne `config/secrets.yaml` und trage deine echten API-Keys ein:

```yaml
OPENAI_API_KEY: "sk-..."
ANTHROPIC_API_KEY: "sk-ant-..."
```

Welche Keys du brauchst, hängt davon ab, welche Modelle du nutzen willst. Die auskommentierten Zeilen in `secrets.example.yaml` zeigen dir, was optional ist.

---

## Schritt 2: LiteLLM starten

```bash
docker compose up -d
```

Startet den LiteLLM-Container im Hintergrund. Beim ersten Start werden die Modelle geladen (30-60 Sekunden).

Prüfe, ob alles läuft:

```bash
./scripts/verify.sh
```

Erwartet: `✅ LiteLLM läuft auf http://127.0.0.1:4000`

---

## Schritt 3: Verbindung testen

Schnellster Test mit cURL:

```bash
curl http://127.0.0.1:4000/v1/models \
  -H "Authorization: Bearer sk-litellm-master-..."
```

Erwartet: JSON-Liste mit allen konfigurierten Modellen.

Test-Chat-Completion:

```bash
curl http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer sk-litellm-master-..." \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4o-mini", "messages": [{"role": "user", "content": "Hello!"}]}'
```

Erwartet: JSON-Antwort mit `choices[0].message.content`.

---

## Schritt 4: In deinem Agent nutzen

In jedem OpenAI-kompatiblen Client setzt du:

```python
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url="http://127.0.0.1:4000/v1",  # LiteLLM statt direkt OpenAI
    api_key="sk-litellm-master-...",       # Master-Key aus config/litellm.yaml
)

response = await client.chat.completions.create(
    model="gpt-4o-mini",  # oder jedes andere LiteLLM-konfigurierte Modell
    messages=[{"role": "user", "content": "Hello!"}],
)
```

**Weitere Beispiele** in `examples/`:
- `examples/openai-python/` — openai-SDK
- `examples/memu/` — memU Framework
- `examples/raw-curl/` — direkte HTTP-Calls

---

## Logs und Troubleshooting

Logs anschauen:

```bash
docker logs litellm-proxy -f
```

Häufige Probleme:

| Problem | Lösung |
|---|---|
| Port 4000 schon belegt | Andere Instanz stoppen oder `docker-compose.yml` Port ändern |
| `401 Unauthorized` | Master-Key in `secrets.yaml` prüfen |
| Modell antwortet nicht | Upstream-API-Key in `secrets.yaml` prüfen |
| `docker compose` nicht gefunden | Docker Desktop installieren |

---

## Update

```bash
docker compose pull
docker compose up -d
```

---

## Stoppen

```bash
docker compose down
```

---

## Mehr Informationen

- `CONCEPT.md` — Was ist LiteLLM und warum ist es nützlich
- `config/litellm.yaml` — Die Model-Liste und Routing-Konfiguration
- `examples/` — Code-Beispiele für verschiedene Frameworks
- `archive/` — Historische Patches (nicht relevant für Setup)
