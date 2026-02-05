# 🧠 MISSION CORE: Viron-memU Agent Entry Point

## 1. Identität & Auftrag

Du befindest dich im Repository **Viron-memU**. Dies ist ein **Langzeitgedächtnis-Framework** für KI-Agenten.
Dein Job ist es, dieses System zu warten, zu erweitern und zu bedienen.

**WICHTIGSTE REGEL:**
Du entscheidest NICHTS allein. Bei Unsicherheit: **FRAGE DEN USER.**
(Siehe `C:\Users\bachl\.gemini\gemini.md` für globale Regeln).

---

## 2. Architektur (Hybrid)

Wir arbeiten in einem **Hybrid-Modus** auf Windows.

### A. Der Code (Native Windows)

- **Pfad:** `C:\Workspace\Repos\memU` (Root)
- **Sprache:** Python 3.13 (in `.venv`)
- **Verantwortung:** Hier liegt die Logik (`src/memu`), Tests und Skripte.

### B. Die Infrastruktur (Docker)

- **Pfad:** `docker-compose.yml` (im Root)
- **Komponenten:**
  1.  **PostgreSQL + pgvector:** Datenbank für Langzeitgedächtnis (Port 5432).
  2.  **vLLM:** Lokale KI-Engine (Port 8000), kompatibel mit OpenAI-API.
  3.  **(Geplant) Open WebUI:** Chat-Interface für den User.

---

## 3. LLM-Steuerung (Das "Gehirn")

Das System ist flexibel. Du kannst zwischen **Lokal (vLLM)** und **Cloud (OpenAI/OpenRouter)** wechseln.

### Wie wechsle ich das Modell?

Die Konfiguration liegt in `.env` (oder `memu-factory.py` für Code-Steuerung).

#### Szenario A: Alles Lokal (Datenschutz / Kostenlos)

Setze in `.env`:

```ini
# Inference Engine (vLLM)
OPENAI_API_BASE="http://localhost:8000/v1"
OPENAI_API_KEY="sk-xxxx" # (Dummy Key für vLLM)
MODEL_NAME="Qwen/Qwen2.5-7B-Instruct" # Name des geladenen vLLM Modells
```

#### Szenario B: Cloud (OpenAI / OpenRouter)

Setze in `.env`:

```ini
# OpenAI
OPENAI_API_BASE="https://api.openai.com/v1"
OPENAI_API_KEY="sk-proj-..."
MODEL_NAME="gpt-4o"
```

### Wie wechsle ich die API im Code?

Bnutze die **Factory**, nicht den direkten Konstruktor!
Siehe `memu-factory.py`:

```python
# Beispiel: Wechsel auf OpenRouter
service = create_memu_service(
    provider="openrouter",
    model="anthropic/claude-3.5-sonnet"
)
```

---

## 4. Workflow & Orchestrierung

### Wie arbeite ich als Agent hier?

1.  **Context Loading:** Lies IMMER zuerst `TASK.md` (aktueller Stand) und `MISSION_CORE.md` (dieses File).
2.  **Planung:** Wenn der User eine neue Funktion will -> Erstelle einen Plan. Frag nach Erlaubnis.
3.  **Proaktivität:** Der Bot im Hintergrund (`proactive.py`) lernt mit. Wenn du etwas tust, speichert er es im Gedächtnis.

### Kommunikation mit dem User

- Sprache: **DEUTSCH**.
- Stil: Direkt, technisch präzise, aber höflich.
- Fehlerkultur: Wenn was schiefgeht -> Melden, Analysieren, Lösungsvorschlag (nicht einfach schweigen).

---

## 5. Chat Interface (User Frontend)

Der User will nicht immer per Skript chatten.
Wir nutzen **Open WebUI** (läuft als Docker Container).

- **URL:** `http://localhost:3000`
- **Backend:** Verbunden mit vLLM (Lokal) oder OpenAI.

---

## 6. Funktions-Matrix (Capabilities)

_Achtung: "Skill" meint hier technische Fähigkeit, nicht Viron-Agent-Skills._

| Funktion                 | Native (Python-Skript)                    | Via Open WebUI (Cockpit)                    |
| :----------------------- | :---------------------------------------- | :------------------------------------------ |
| **Gedächtnis schreiben** | ✅ **JA** (Direktzugriff)                 | ✅ **JA** (Via API Backend)                 |
| **Dateien erzeugen**     | ✅ **JA** (Via `write_file` Tool)         | ⚠️ **Jein** (Im Browser-Sandbox / Download) |
| **Projekt-Code ändern**  | ⚠️ **Möglich** (wenn Tool freigeschaltet) | ❌ **Nein** (Docker-Container ist isoliert) |
| **Code Ausführung**      | ❌ **Nein** (Logik hardcoded)             | ✅ **JA** (Python Code Interpreter)         |

### Kann ich das ändern? (Sandbox-Ausbruch)

Ja. Damit WebUI oder der Bot echte Dateien im Repo ändern darf, müssen wir:

1.  **Docker Volume:** Den Projekt-Ordner in den Container mounten.
2.  **Tools:** Dem Agenten explizit ein "File-System-Tool" geben.
    _Sicherheitshinweis: Das gibt dem Bot volle Macht über den Code._

---

## 7. Proaktivität & Trigger (Wie laufe ich?)

Ich bin nicht nur "Reagierer". Ich kann getriggert werden durch:

1.  **Endlosschleife (Loop):** (Aktuell in `proactive.py`) Ich wache alle X Minuten auf, prüfe Todos/Mails.
2.  **API / Webhooks:** (Muss konfiguriert werden) Externe Dienste pingen mich an (`POST /v1/chat/completions`).
3.  **Dateisystem-Events:** (File Watcher) Ich reagiere, wenn du eine Datei speicherst.
4.  **Cron-Jobs:** Zeitgesteuerte Aufgaben (z.B. "Jeden Morgen um 8:00").

---

### Erweiterung geplant?

Um dem Bot "Hände" zu geben (Dateien schreiben, Terminal), müssen wir **Tools** in Python definieren (`src/memu/tools`).
Aktuell ist er ein "Gehirn im Tank" (reiner Denker).

---
