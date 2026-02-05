# memU Production Setup - Vollständige Anleitung

**Zielgruppe:** Technical Architects, Full-Stack Developers  
**System:** Linux/WSL2, Docker, Python 3.13+  
**Datum:** 05.02.2026

## 📦 Paket-Inhalt

Dieses Deployment-Paket enthält 7 produktionsreife Dateien:

1. **docker-compose.yml** - PostgreSQL/pgvector Container
2. **env-example.txt** - Environment-Template (umbenennen zu .env)
3. **memu-factory.py** - Zentrale Konfiguration (4 Provider)
4. **test-01-database.py** - Database Validation
5. **test-02-memorize.py** - Write Path Tests
6. **test-03-retrieve.py** - Read Path Tests (RAG vs LLM)
7. **README-SETUP.md** - Diese Anleitung

## 🚀 Quick Start (5 Schritte)

### 1. Voraussetzungen

```bash
# Docker installieren
sudo apt-get update
sudo apt-get install -y docker.io docker-compose

# Python 3.13 + uv
sudo apt-get install -y python3.13 python3.13-venv python3.13-dev
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
```

### 2. memU Repository klonen

```bash
git clone https://github.com/NevaMind-AI/memU.git
cd memU
git checkout v1.2.0  # Stable Release

# Python Environment
uv venv .venv --python 3.13
source .venv/bin/activate

# Dependencies
uv pip install -e .
uv pip install psycopg2-binary python-dotenv openai httpx
```

### 3. Deployment-Dateien einrichten

```bash
mkdir -p ~/memu-prod
cd ~/memu-prod

# Kopiere alle 7 Dateien hierher
# Dann:
mv env-example.txt .env
nano .env  # API Keys eintragen
```

### 4. Datenbank starten

```bash
docker-compose up -d
docker-compose ps  # Check: Status = "healthy"
```

### 5. Tests ausführen

```bash
source ~/memU/.venv/bin/activate

python test-01-database.py     # Erwartung: 4/4 passed
python test-02-memorize.py     # Erwartung: 3/3 passed
python test-03-retrieve.py     # Erwartung: 3/3 passed
```

**✅ Alle grün = Production Ready!**

## 🔧 Provider-Konfiguration

### Verfügbare Provider

| Provider | Use Case | Kosten | Latenz |
|----------|----------|--------|--------|
| **ollama** | Lokal | Gratis | 10-60s |
| **vllm** | High-Perf Local | Gratis | 5-20s |
| **openrouter** | Cloud Fallback | ~$0.001/1k | 1-5s |
| **google** | Gemini | ~$0.0005/1k | 1-3s |

### Verwendung

```python
from memu_factory import create_memory_instance

memory = create_memory_instance(
    user_id="admin",
    provider="openrouter"  # oder ollama, vllm, google
)

# Write
result = memory.memorize("Wichtige Information")

# Read (schnell)
context = memory.retrieve("Was war das?", method="rag")

# Read (langsam, besser)
context = memory.retrieve("Was war das?", method="llm")
```

## ⚠️ Wichtige Hinweise

### Embeddings

**Nutze immer OpenAI für Embeddings**, auch wenn Chat lokal läuft!

Grund: memU v1.2 erwartet 1536 Dimensionen (OpenAI). Ollama hat oft 4096 → Dimension Mismatch.

```bash
# In .env
OPENAI_API_KEY=sk-proj-...  # Nur für Embeddings, ~$0.0001/1k tokens
```

### Ollama Timeouts

Lokale Inferenz ist langsam. In `memu-factory.py` erhöhen:

```python
"timeout": 180.0,  # 3 Minuten statt 120s
```

## 🔍 Troubleshooting

### "Connection refused"

```bash
docker ps -a
docker-compose down
docker-compose up -d
docker-compose logs -f
```

### "Table not found"

memU erstellt Tabellen beim ersten `Memory()` Aufruf:

```bash
python test-02-memorize.py  # Triggert Schema-Init
```

### "Vector dimension mismatch"

Du nutzt lokale Embeddings mit falscher Dimension. Lösung: OpenAI Embeddings nutzen.

## 📊 Deine Entscheidungen

| Entscheidung | Konsequenz |
|--------------|-----------|
| **Postgres** | Produktions-Grade, Multi-Instanz fähig |
| **Self-Hosted** | 100% Datenkontrolle, keine Rate-Limits |
| **Hybrid LLM** | Fallback bei Local-Failure |
| **RAG Default** | 90% günstiger als LLM-only |

## 🔒 Sicherheit

- `.env` nie committen (ist in .gitignore)
- Port-Binding: `127.0.0.1:5432` (nur localhost)
- Regelmäßig `./pgdata` Verzeichnis sichern
- API Keys regelmäßig rotieren

## 📚 Ressourcen

- **GitHub:** https://github.com/NevaMind-AI/memU
- **HackerNews:** https://news.ycombinator.com/item?id=46525174
- **Cloud Service:** https://memu.so

## 🎯 Nächste Schritte

1. Proactive Loop testen: `examples/proactive/proactive.py`
2. Mehrere Instanzen für verschiedene User/Projekte
3. Integration in deine Anwendung
4. Monitoring & Backup-Strategie einrichten

---

**Version:** 1.0 (05.02.2026)  
**Lizenz:** Apache 2.0
