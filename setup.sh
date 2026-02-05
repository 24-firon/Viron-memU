#!/bin/bash
set -e  # Exit bei Fehler

# memU Production Setup - Automatisches Setup-Script
# Version: 1.0 (05.02.2026)
# Verwendung: ./setup.sh [--skip-tests] [--provider openrouter|ollama|vllm|google]

###############################################################################
# KONFIGURATION
###############################################################################

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMU_DIR="$PROJECT_ROOT/../memu"
SKIP_TESTS=false
PROVIDER="openrouter"

# Farben für Terminal-Output
C_GREEN="\033[92m"
C_RED="\033[91m"
C_YELLOW="\033[93m"
C_BLUE="\033[94m"
C_BOLD="\033[1m"
C_RESET="\033[0m"

###############################################################################
# HELPER FUNCTIONS
###############################################################################

log_info() {
    echo -e "${C_BLUE}ℹ INFO:${C_RESET} $1"
}

log_success() {
    echo -e "${C_GREEN}✔ SUCCESS:${C_RESET} $1"
}

log_error() {
    echo -e "${C_RED}✖ ERROR:${C_RESET} $1"
}

log_warn() {
    echo -e "${C_YELLOW}⚠ WARNING:${C_RESET} $1"
}

log_section() {
    echo ""
    echo -e "${C_BOLD}========================================${C_RESET}"
    echo -e "${C_BOLD}$1${C_RESET}"
    echo -e "${C_BOLD}========================================${C_RESET}"
    echo ""
}

check_command() {
    if command -v "$1" &> /dev/null; then
        log_success "$1 ist installiert"
        return 0
    else
        log_error "$1 ist NICHT installiert"
        return 1
    fi
}

###############################################################################
# ARGUMENT PARSING
###############################################################################

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --provider)
            PROVIDER="$2"
            shift 2
            ;;
        *)
            echo "Unbekannte Option: $1"
            echo "Verwendung: ./setup.sh [--skip-tests] [--provider openrouter|ollama|vllm|google]"
            exit 1
            ;;
    esac
done

###############################################################################
# SCHRITT 1: VORAUSSETZUNGEN PRÜFEN
###############################################################################

log_section "SCHRITT 1: Voraussetzungen prüfen"

REQUIREMENTS_MET=true

check_command git || REQUIREMENTS_MET=false
check_command docker || REQUIREMENTS_MET=false
check_command docker-compose || REQUIREMENTS_MET=false
check_command python3.13 || REQUIREMENTS_MET=false

if ! check_command uv; then
    log_warn "uv nicht installiert - wird für schnelleres venv empfohlen"
    log_info "Installation: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

if ! check_command gh; then
    log_warn "GitHub CLI (gh) nicht installiert - Fork muss manuell erfolgen"
    log_info "Installation: sudo apt install gh (oder brew install gh)"
fi

if [ "$REQUIREMENTS_MET" = false ]; then
    log_error "Nicht alle Voraussetzungen erfüllt. Bitte installiere fehlende Tools."
    exit 1
fi

# Docker-Status prüfen
if ! docker info > /dev/null 2>&1; then
    log_error "Docker läuft nicht. Bitte starten:"
    echo "  sudo systemctl start docker"
    echo "  oder: sudo service docker start"
    exit 1
fi

log_success "Alle Voraussetzungen erfüllt"

###############################################################################
# SCHRITT 2: GITHUB FORK & CLONE
###############################################################################

log_section "SCHRITT 2: GitHub Fork & Clone"

if [ -d "$MEMU_DIR" ]; then
    log_warn "memu/ Ordner existiert bereits - überspringe Clone"
    cd "$MEMU_DIR"
else
    if command -v gh &> /dev/null; then
        log_info "Prüfe GitHub-Authentifizierung..."
        if gh auth status &> /dev/null; then
            log_info "Erstelle Fork von NevaMind-AI/memU..."
            gh repo fork NevaMind-AI/memU --clone=false
            
            log_info "Hole GitHub-Username..."
            GH_USER=$(gh api user -q .login)
            log_info "GitHub-User: $GH_USER"
            
            log_info "Clone Fork nach memu/..."
            git clone "https://github.com/$GH_USER/memU.git" "$MEMU_DIR"
        else
            log_error "GitHub CLI nicht authentifiziert. Bitte ausführen: gh auth login"
            exit 1
        fi
    else
        log_error "GitHub CLI nicht verfügbar. Manuelle Schritte erforderlich:"
        echo "1. Gehe zu https://github.com/NevaMind-AI/memU"
        echo "2. Klicke auf 'Fork'"
        echo "3. Clone deinen Fork: git clone https://github.com/DEIN_USER/memU.git memu"
        exit 1
    fi
    
    cd "$MEMU_DIR"
fi

# Upstream Remote einrichten
log_info "Richte upstream-Remote ein..."
if git remote get-url upstream &> /dev/null; then
    log_warn "upstream-Remote existiert bereits"
else
    git remote add upstream https://github.com/NevaMind-AI/memU.git
    log_success "upstream-Remote hinzugefügt"
fi

git fetch upstream

# Production-Branch erstellen
if git show-ref --verify --quiet refs/heads/production-setup; then
    log_warn "Branch production-setup existiert bereits"
    git checkout production-setup
else
    git checkout -b production-setup
    log_success "Branch production-setup erstellt"
fi

###############################################################################
# SCHRITT 3: PYTHON-UMGEBUNG
###############################################################################

log_section "SCHRITT 3: Python-Umgebung"

cd "$MEMU_DIR"

if [ -d ".venv" ]; then
    log_warn ".venv existiert bereits - überspringe Erstellung"
else
    log_info "Erstelle virtuelle Umgebung..."
    if command -v uv &> /dev/null; then
        uv venv .venv --python 3.13
    else
        python3.13 -m venv .venv
    fi
    log_success "Virtuelle Umgebung erstellt"
fi

log_info "Aktiviere virtuelle Umgebung..."
source .venv/bin/activate

log_info "Installiere memU..."
pip install -e . --quiet

log_info "Installiere Abhängigkeiten..."
pip install psycopg2-binary python-dotenv httpx openai --quiet

log_success "Python-Umgebung eingerichtet"

# Verifiziere Installation
log_info "Verifiziere memU-Installation..."
if python -c "from memu import Memory; print('OK')" 2>/dev/null; then
    log_success "memU ist importierbar"
else
    log_error "memU kann nicht importiert werden"
    exit 1
fi

###############################################################################
# SCHRITT 4: DEPLOYMENT-DATEIEN
###############################################################################

log_section "SCHRITT 4: Deployment-Dateien"

cd "$PROJECT_ROOT"

# .gitignore erstellen
if [ ! -f .gitignore ]; then
    log_info "Erstelle .gitignore..."
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
    log_success ".gitignore erstellt"
else
    log_warn ".gitignore existiert bereits"
fi

# .env erstellen
if [ ! -f .env ]; then
    log_info "Erstelle .env aus env-example.txt..."
    cp env-example.txt .env
    log_success ".env erstellt"
    echo ""
    echo -e "${C_YELLOW}========================================${C_RESET}"
    echo -e "${C_YELLOW}⚠️  AKTION ERFORDERLICH ⚠️${C_RESET}"
    echo -e "${C_YELLOW}========================================${C_RESET}"
    echo ""
    echo "Bitte bearbeite jetzt die Datei .env und trage deine API-Keys ein:"
    echo ""
    echo "1. OPENAI_API_KEY=sk-proj-...        (zwingend für Embeddings)"
    echo "2. OPENROUTER_API_KEY=sk-or-...      (optional für Cloud-LLM)"
    echo "3. GOOGLE_API_KEY=...                (optional für Gemini)"
    echo ""
    echo "Datei-Pfad: $PROJECT_ROOT/.env"
    echo ""
    read -p "Drücke Enter, wenn du die API-Keys eingetragen hast..."
else
    log_warn ".env existiert bereits"
fi

# Validiere .env
if [ ! -s .env ]; then
    log_error ".env ist leer - bitte API-Keys eintragen"
    exit 1
fi

log_success "Deployment-Dateien konfiguriert"

###############################################################################
# SCHRITT 5: DOCKER STARTEN
###############################################################################

log_section "SCHRITT 5: Docker & Datenbank"

cd "$PROJECT_ROOT"

log_info "Starte Docker-Container..."
docker-compose up -d

log_info "Warte auf Container (max 30 Sekunden)..."
for i in {1..30}; do
    HEALTH=$(docker inspect --format='{{.State.Health.Status}}' memu_production_db 2>/dev/null || echo "starting")
    if [ "$HEALTH" = "healthy" ]; then
        log_success "Container ist healthy"
        break
    fi
    echo "  Versuch $i/30: Status=$HEALTH"
    sleep 1
done

if [ "$HEALTH" != "healthy" ]; then
    log_error "Container nicht healthy nach 30 Sekunden"
    log_info "Container-Logs:"
    docker-compose logs
    exit 1
fi

log_info "Container-Status:"
docker-compose ps

log_success "Datenbank läuft"

###############################################################################
# SCHRITT 6: TESTS AUSFÜHREN
###############################################################################

if [ "$SKIP_TESTS" = true ]; then
    log_section "SCHRITT 6: Tests (übersprungen)"
    log_warn "Tests wurden mit --skip-tests übersprungen"
else
    log_section "SCHRITT 6: Tests ausführen"
    
    cd "$PROJECT_ROOT"
    source "$MEMU_DIR/.venv/bin/activate"
    
    # Test 1: Database
    log_info "Führe Test 1 aus (Database)..."
    if python test-01-database.py; then
        log_success "Test 1 bestanden"
    else
        log_error "Test 1 fehlgeschlagen"
        exit 1
    fi
    
    echo ""
    
    # Test 2: Memorize
    log_info "Führe Test 2 aus (Memorize)..."
    if python test-02-memorize.py --provider "$PROVIDER"; then
        log_success "Test 2 bestanden"
    else
        log_error "Test 2 fehlgeschlagen"
        exit 1
    fi
    
    echo ""
    
    # Test 3: Retrieve
    log_info "Führe Test 3 aus (Retrieve)..."
    EXIT_CODE=0
    python test-03-retrieve.py --provider "$PROVIDER" || EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        log_success "Test 3 bestanden"
    elif [ $EXIT_CODE -eq 2 ]; then
        log_warn "Test 3 teilweise erfolgreich"
    else
        log_error "Test 3 fehlgeschlagen"
        exit 1
    fi
fi

###############################################################################
# SCHRITT 7: ZUSAMMENFASSUNG
###############################################################################

log_section "SETUP ABGESCHLOSSEN"

echo -e "${C_GREEN}✅ Fork erstellt und geklont${C_RESET}"
echo -e "${C_GREEN}✅ Python-Umgebung eingerichtet${C_RESET}"
echo -e "${C_GREEN}✅ Docker-Container läuft${C_RESET}"

if [ "$SKIP_TESTS" = false ]; then
    echo -e "${C_GREEN}✅ Tests bestanden${C_RESET}"
fi

echo ""
echo -e "${C_BOLD}Projekt-Struktur:${C_RESET}"
echo "  $PROJECT_ROOT/"
echo "  ├── memu/                 (Fork, updatebar)"
echo "  ├── docker-compose.yml    (Dein Setup)"
echo "  ├── .env                  (Deine Secrets)"
echo "  └── test-*.py             (Deine Tests)"
echo ""
echo -e "${C_BOLD}Nächste Schritte:${C_RESET}"
echo "  1. Testen:"
echo "     source memu/.venv/bin/activate"
echo "     python -c 'from memu_factory import create_memory_instance; m = create_memory_instance(\"test\", \"test\"); print(m)'"
echo ""
echo "  2. Beispiele anschauen:"
echo "     cd memu/examples/proactive"
echo "     python proactive.py"
echo ""
echo "  3. Updates vom Upstream holen:"
echo "     cd memu"
echo "     git fetch upstream"
echo "     git merge upstream/main"
echo ""
echo -e "${C_BOLD}Provider:${C_RESET} $PROVIDER"
echo -e "${C_BOLD}PostgreSQL:${C_RESET} localhost:5432"
echo -e "${C_BOLD}Daten-Ordner:${C_RESET} $PROJECT_ROOT/pgdata/"
echo ""
echo -e "${C_GREEN}🚀 memU ist produktionsbereit!${C_RESET}"
echo ""
