# CONCEPT > Was ist LiteLLM?

## Die Grundidee

LiteLLM ist ein **lokaler Proxy**, der eine einzige OpenAI-kompatible API auf Port 4000 bereitstellt. Hinter dieser API vereint er 22+ verschiedene LLM-Provider (OpenAI, Anthropic, Gemini, Mistral, Ollama, NVIDIA NIM, OpenRouter, etc.) zu einem einzigen Endpunkt.

**Das Problem, das LiteLLM löst:**

Du hast heute:
- OpenAI-Key für GPT-Modelle
- Anthropic-Key für Claude
- Gemini-Key für Gemini
- Lokales Ollama für Llama
- NVIDIA NIM-API für bestimmte Modelle

Jeder Client, der mit diesen Modellen reden will, muss die jeweilige API-Integration kennen: anderes Auth, anderes Request-Format, andere Fehlerbehandlung, andere Streaming-Spezifikation. Das ist ein Wartungs-Albtraum.

**Was LiteLLM bietet:**

Ein Endpunkt. Ein Auth-Schema (Bearer-Token). Ein Request-Format (OpenAI Chat Completions). Eine Fehlerbehandlung. Ein Streaming-Format. Du schreibst deinen Client einmal gegen OpenAI-Standard, und LiteLLM routet im Hintergrund an den richtigen Provider.

```
Dein Agent-Client
       ↓ OpenAI-kompatibel (immer gleich)
   LiteLLM (Port 4000)
       ↓
   ┌───┴────┬────────┬────────┬─────────┐
   ↓        ↓        ↓        ↓         ↓
 OpenAI  Anthropic  Gemini  Ollama   NIM
```

## Die Schlüsseleigenschaft: OpenAI-Kompatibilität

LiteLLM spricht exakt das OpenAI Chat Completions API-Format. Das ist der entscheidende Punkt, weil:

- `openai-python` SDK funktioniert direkt (nur `base_url` ändern)
- `langchain` mit `ChatOpenAI` funktioniert direkt
- `memU` mit `llm_profiles` funktioniert direkt
- Eigener HTTP-Client funktioniert direkt
- Jeder andere LLM-Client, der OpenAI spricht, funktioniert direkt

**Du musst keinen Code in deinem Projekt patchen.** Du setzt nur `base_url` auf LiteLLM und schon spricht dein Agent mit allen 22 Modellen.

## Wann LiteLLM sinnvoll ist

✓ Du nutzt mehrere LLM-Provider (z.B. OpenAI + Anthropic + lokales Modell)
✓ Du willst Modell-Fallback (wenn Provider A down ist, nimm Provider B)
✓ Du willst Budget-Tracking (welcher User/Projekt hat wieviel verbraucht)
✓ Du willst Virtual-Keys (verschiedene Keys für verschiedene Zwecke)
✓ Du willst Rate-Limiting zentral
✓ Du willst nur EINE Integration in deinem Code statt 5

## Wann LiteLLM NICHT sinnvoll ist

✗ Du nutzt nur einen Provider (z.B. nur OpenAI) — dann ist LiteLLM Overhead
✗ Du brauchst keine Multi-Provider-Flexibilität
✗ Du hast strikte Latenz-Anforderungen (jeder Hop kostet ~10-50ms)

## Architektur im Detail

**Master-Key vs. Virtual-Keys:**
- Master-Key (`sk-litellm-master-...`): Vollzugriff, kann Modelle hinzufügen, Admin-UI nutzen
- Virtual-Keys: Können pro User/Projekt/Use-Case erstellt werden, mit Budget-Limits

**Routing:**
LiteLLM kann Anfragen intelligent routen. Z.B.:
- "GPT-4 nicht verfügbar → fallback auf Claude"
- "Anthropic-Rate-Limit erreicht → fallback auf OpenRouter"
- "Bestimmtes Modell pro User"

**Cost-Tracking:**
LiteLLM loggt jeden Request mit Token-Count und kann Kosten zuordnen.

**Admin-UI:**
Optional unter `http://127.0.0.1:4000/ui` — Usage-Stats, Model-Management, Test-Playground.

## Wie es zu deinem Code passt

**Beispiel: openai-python SDK**

```python
# Vorher (direkt zu OpenAI):
from openai import AsyncOpenAI
client = AsyncOpenAI(api_key="sk-...")

# Nachher (über LiteLLM):
from openai import AsyncOpenAI
client = AsyncOpenAI(
    base_url="http://127.0.0.1:4000/v1",
    api_key="sk-litellm-master-...",
)
# Gleiche API, andere Modelle möglich
```

**Beispiel: memU (ein konkretes Framework)**

Siehe `examples/memu/` für ein vollständiges Beispiel.

**Beispiel: Rohes HTTP**

Siehe `examples/raw-curl/` für cURL-Beispiele.

## Was du im Bundle findest

| Datei | Zweck |
|---|---|
| `RECIPE.md` | Schritt-für-Schritt Setup-Anleitung |
| `CONCEPT.md` | Diese Datei — Konzept-Erklärung |
| `docker-compose.yml` | LiteLLM + Admin-UI Container |
| `config/litellm.yaml` | Model-Liste und Routing-Regeln |
| `config/secrets.example.yaml` | API-Keys Template |
| `scripts/setup.sh` / `setup.ps1` | 1-Befehl-Setup |
| `scripts/verify.sh` | Health-Check |
| `examples/` | Code-Beispiele für verschiedene Frameworks |
| `archive/` | Historische Patches (nicht relevant für Setup) |

## Sicherheits-Hinweise

- **Master-Key geheim halten.** Wer den Key hat, kann deinen LiteLLM nutzen (und damit deine Upstream-Provider-Kosten verursachen).
- **`secrets.yaml` nicht in Git committen.** Die Datei gehört in `.gitignore`.
- **Nur lokal binden.** Standard: `127.0.0.1:4000`. Wenn du es im Netzwerk exponierst, sorge für Authentifizierung.

## Mehr Informationen

- LiteLLM-Doku: https://docs.litellm.ai/
- Unterstützte Provider: https://docs.litellm.ai/docs/providers
- Config-Format: https://docs.litellm.ai/docs/proxy/configs
