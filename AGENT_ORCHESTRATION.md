# memU Setup Orchestrationsplan

## Ziel

Richte ein self-hosted memU-Setup ein (PostgreSQL/pgvector, Python 3.13, Hybrid-LLM),
ohne Änderungen am Upstream-Repo zu verlieren. Das Original-Repo soll updatebar bleiben,
meine eigenen Deploy-Skripte und Konfigurationen liegen außerhalb im selben Workspace.

## Randbedingungen

- OS: Linux oder WSL2
- Tools vorhanden oder zu installieren: git, docker, docker-compose, python3.13, uv, gh (GitHub CLI), curl
- IDE/Agent: darf Shell-Kommandos ausführen und Dateien schreiben
- memU Upstream-Repo: https://github.com/NevaMind-AI/memU

## Aufgabenübersicht

### 1. Repository & Fork

**1.1** Prüfe, ob die GitHub CLI `gh` installiert und authentifiziert ist.

```bash
gh --version
gh auth status
```

**1.2** Wenn nicht installiert: Vorschlag anzeigen und NICHT selbst installieren, nur Befehl vorschlagen:

```bash
# Ubuntu/Debian
sudo apt install gh
# macOS
brew install gh
# Nach Installation:
gh auth login
```

**1.3** Erstelle einen Fork von `NevaMind-AI/memU` in meinem GitHub-Account:

```bash
gh repo fork NevaMind-AI/memU --clone=false
```

**1.4** Klone den Fork in den Unterordner `memu/` direkt unter diesem Projektordner:

```bash
# Ersetze DEIN_GITHUB_USERNAME mit tatsächlichem Username
git clone https://github.com/DEIN_GITHUB_USERNAME/memU.git memu
cd memu
```

**1.5** Richte den `upstream`-Remote ein, der auf das Original-Repo zeigt:

```bash
git remote add upstream https://github.com/NevaMind-AI/memU.git
git fetch upstream
```

**1.6** Erstelle einen Branch `production-setup` und checke ihn aus:

```bash
git checkout -b production-setup
```

### 2. Python-Umgebung (im Unterordner `memu/`)

**2.1** Wechsle nach `memu/`:

```bash
cd memu
```

**2.2** Erstelle eine virtuelle Umgebung mit Python 3.13:

```bash
# Bevorzugt mit uv (schneller)
uv venv .venv --python 3.13

# Fallback ohne uv
python3.13 -m venv .venv
```

**2.3** Aktiviere die Umgebung:

```bash
source .venv/bin/activate
```

**2.4** Installiere memU im Editable-Mode:

```bash
pip install -e .
```

**2.5** Installiere zusätzliche Abhängigkeiten:

```bash
pip install psycopg2-binary python-dotenv httpx openai
```

### 3. Deployment-Schicht (im Root dieses Ordners)

**3.1** Wechsle zurück zum Projekt-Root (eine Ebene über `memu/`):

```bash
cd ..
```

**3.2** Stelle sicher, dass folgende Dateien im Projekt-Root liegen:

- `docker-compose.yml`
- `env-example.txt`
- `memu-factory.py`
- `test-01-database.py`
- `test-02-memorize.py`
- `test-03-retrieve.py`
- `README-SETUP.md`
- `AGENT_ORCHESTRATION.md` (diese Datei)

**3.3** Erstelle `.gitignore` im Projekt-Root, falls nicht vorhanden:

```bash
cat > .gitignore << 'EOF'
# Virtual Environment
.venv/
memu/.venv/

# Secrets
.env

# Docker Volumes
pgdata/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
EOF
```

### 4. Environment & Secrets

**4.1** Erstelle `.env` aus `env-example.txt`:

```bash
cp env-example.txt .env
```

**4.2** HALTE AN und fordere den User auf, API-Keys einzutragen:

```
⚠️  AKTION ERFORDERLICH ⚠️

Bitte bearbeite jetzt die Datei .env und trage folgende API-Keys ein:

1. OPENAI_API_KEY=sk-proj-...        (für Embeddings, zwingend erforderlich)
2. OPENROUTER_API_KEY=sk-or-...      (für Cloud-LLM, optional)
3. GOOGLE_API_KEY=...                (für Gemini, optional)

Die Datei liegt hier: .env

Wenn fertig, antworte mit "weiter" und ich setze das Setup fort.
```

**4.3** Nach User-Bestätigung: Validiere, dass `.env` existiert und nicht leer ist:

```bash
if [ -f .env ] && [ -s .env ]; then
    echo "✅ .env vorhanden und nicht leer"
else
    echo "❌ .env fehlt oder ist leer - bitte erstellen"
    exit 1
fi
```

### 5. Docker & Datenbank

**5.1** Prüfe, ob Docker läuft:

```bash
docker info > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Docker läuft"
else
    echo "❌ Docker läuft nicht. Starte Docker mit:"
    echo "   sudo systemctl start docker"
    echo "   oder: sudo service docker start"
    exit 1
fi
```

**5.2** Starte `docker-compose` im Projekt-Root:

```bash
docker-compose up -d
```

**5.3** Warte, bis der Container gesund ist (max 30 Sekunden):

```bash
echo "Warte auf PostgreSQL Container..."
for i in {1..30}; do
    HEALTH=$(docker inspect --format='{{.State.Health.Status}}' memu_production_db 2>/dev/null)
    if [ "$HEALTH" = "healthy" ]; then
        echo "✅ Container ist healthy"
        break
    fi
    echo "  Versuch $i/30: Status=$HEALTH"
    sleep 1
done

if [ "$HEALTH" != "healthy" ]; then
    echo "❌ Container nicht healthy nach 30s. Logs:"
    docker-compose logs
    exit 1
fi
```

**5.4** Verifiziere Container-Status:

```bash
docker-compose ps
```

### 6. Verknüpfung memU ↔ Deployment

**6.1** Stelle sicher, dass `test-*.py` Skripte den `memu`-Code finden können.

Die Test-Skripte haben bereits:

```python
sys.path.insert(0, str(Path(__file__).parent))
```

Das funktioniert, weil `memu-factory.py` im selben Ordner liegt wie die Tests.

**6.2** Aktiviere die virtuelle Umgebung aus `memu/.venv`:

```bash
source memu/.venv/bin/activate
```

**6.3** Verifiziere, dass memU importierbar ist:

```bash
python -c "from memu import Memory; print('✅ memU importierbar')"
```

### 7. Test-Pipeline

**7.1** Führe Test 1 aus (Database):

```bash
python test-01-database.py
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Test 1 bestanden"
else
    echo "❌ Test 1 fehlgeschlagen (Exit Code: $EXIT_CODE)"
    echo "Behebe die Fehler, bevor du fortfährst."
    exit 1
fi
```

**7.2** Wenn Test 1 erfolgreich, führe Test 2 aus (Memorize):

```bash
python test-02-memorize.py --provider openrouter
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Test 2 bestanden"
else
    echo "❌ Test 2 fehlgeschlagen (Exit Code: $EXIT_CODE)"
    exit 1
fi
```

**7.3** Wenn Test 2 erfolgreich, führe Test 3 aus (Retrieve):

```bash
python test-03-retrieve.py --provider openrouter
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Test 3 bestanden"
elif [ $EXIT_CODE -eq 2 ]; then
    echo "⚠️  Test 3 teilweise erfolgreich"
else
    echo "❌ Test 3 fehlgeschlagen"
fi
```

**7.4** Erstelle Status-Zusammenfassung:

```bash
echo ""
echo "=========================================="
echo "SETUP ABGESCHLOSSEN"
echo "=========================================="
echo ""
echo "✅ Fork erstellt und geklont"
echo "✅ Python-Umgebung eingerichtet"
echo "✅ Docker-Container läuft"
echo "✅ Tests bestanden"
echo ""
echo "Nächste Schritte:"
echo "1. Testen: python -c 'from memu_factory import create_memory_instance; m = create_memory_instance(\"test\", \"test\"); print(m)'"
echo "2. Beispiele: cd memu/examples/proactive && python proactive.py"
echo "3. Integration in deine Anwendung"
echo ""
```

### 8. Idempotenz & Wiederholbarkeit

**8.1** Alle Schritte sind so gestaltet, dass sie mehrfach ausgeführt werden können:

- `git clone`: Prüfe vorher, ob `memu/` existiert
- `docker-compose up -d`: Startet nur, wenn nicht schon läuft
- `pip install`: Überschreibt bei erneuter Ausführung
- Tests: Erstellen eigene Test-User-IDs, überschreiben sich nicht

**8.2** Vor jedem potentiell destruktiven Befehl: Existenzprüfung

```bash
# Beispiel: Clone nur, wenn Ordner nicht existiert
if [ ! -d "memu" ]; then
    git clone https://github.com/DEIN_GITHUB_USERNAME/memU.git memu
else
    echo "memu/ existiert bereits, überspringe Clone"
fi
```

## Wichtige Regeln für den Agenten

1. **Keine Secrets leaken**: Lese `.env` NIEMALS aus und poste den Inhalt nicht
2. **Bei Unsicherheit fragen**: Lieber nachfragen als raten
3. **Kommandos ankündigen**: Beschreibe, was du gleich tun wirst
4. **Fehler nicht ignorieren**: Bei Exit Code != 0 sofort stoppen und reporten
5. **Strikte Reihenfolge**: Halte dich an die Nummerierung 1-8
6. **User-Interaktion**: Bei Schritt 4.2 auf User-Input warten

## Erfolgskriterien

- ✅ Fork auf GitHub existiert
- ✅ `memu/` Ordner enthält geklontes Repo
- ✅ `upstream` Remote ist konfiguriert
- ✅ Branch `production-setup` existiert
- ✅ Virtuelle Umgebung in `memu/.venv/` funktioniert
- ✅ memU ist installiert (`pip list | grep memU`)
- ✅ Docker-Container läuft und ist healthy
- ✅ `.env` existiert mit API-Keys
- ✅ Alle 3 Tests bestanden (Exit Code 0)

## Update-Strategie (für später)

Wenn das Original-Repo Updates bekommt:

```bash
cd memu
git fetch upstream
git checkout production-setup
git merge upstream/main
# Konflikte auflösen falls nötig
git push origin production-setup
```

Die Deployment-Dateien (docker-compose.yml, test-*.py) im Root bleiben unberührt!

---

**Version:** 1.0 (05.02.2026)
**Lizenz:** Apache 2.0
