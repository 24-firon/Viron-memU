---
name: Core Safety — Zerstörungsschutz
description: Gemergter Zerstörungsschutz: Read-before-Delete, Edit-overwrite-Verbot, Copy-Verify-Delete-Protokoll, Secrets-Schutz.
trigger: always_on
scope: alle
repo: all
---

# 10_core_safety.md

> **STATUS:** ALWAYS_ON
> **SCOPE:** Alle Domänen (Factory, Studio, Lab)
> **BLOCK:** 10 — Safety & Zerstörungsschutz
> **HERKUNFT:** Gemergt aus `10_deletion_safeguard.md`, `10_edit_overwrite_prohibition.md`, `10_file_operation_safety.md`, `10_security_basics.md`

## 1. Read-Before-Delete

**SOG:** Lies jede Datei vollständig (`Read`-Tool), bevor du sie löschst oder massiv änderst, DENN blindes Löschen basierend auf Annahmen führt zu irreversiblem Datenverlust von implizitem Wissen (Kommentare, Edge-Case-Handling, Typen).

**Frage vor jedem Delete:** "Verstehe ich zu 100%, warum dieser Code hier steht?" → Antwort NEIN: STOPP. Nicht löschen.

**Fallback:** Bei Unsicherheit verschiebe die Datei in `PLAYGROUND/` oder `ARCHIVE/` statt sie zu löschen.

## 2. Edit-Overwrite-Verbot (erweitert)

**SOG:** Nutze für bestehende Dateien immer das `edit`-Tool (nicht `write`), DENN `write` überschreibt die gesamte Datei ohne Kontext und löscht stillschweigend wichtige Kommentare, Struktur oder Metadata, die nicht im neuen Inhalt enthalten sind.

**Ausnahme:** `write` ist nur erlaubt, wenn:
- Die Datei nachweislich nicht existiert (vorher mit `read` oder `list_dir` geprüft)
- Der User explizit "komplett neu schreiben" beauftragt hat

**Proof-of-Reading:** Bevor du eine Datei mit `write` erstellst, prüfe mit `read` oder `list_dir`, ob sie bereits existiert, DENN blindes Überschreiben bestehender Dateien ist ein irreversibler Datenverlust-Vorfall.

**Anti-Kompression:** Wenn du eine bestehende Datei mit `edit` änderst, bewahre den ursprünglichen Formulierungsstil und die Präzision, DENN Agenten neigen zur Kompression von "gut genug" erscheinenden Inhalten — dabei gehen aber unmissverständliche Formulierungen verloren, die über Monate entwickelt wurden.

**Diff-Integrität:** `edit` erzeugt einen sauberen Diff der nur die tatsächliche Änderung zeigt. `write` zeigt die gesamte Datei als geändert — damit ist kein Review mehr möglich. Der Operator MUSS nachvollziehen können, was sich geändert hat. Bei `write` geht diese Nachvollziehbarkeit komplett verloren.

**Verboten:**
- "Kürzen" von als "wichtig" markierten Abschnitten
- Ersetzen von spezifischen Begriffen durch generische Synonyme
- Entfernen von Beispielen mit der Begründung "zu lang"

## 3. Copy-Verify-Delete-Protokoll (erweitert)

**SOG:** Nutze für Datei-Verschiebungen niemals `mv` oder `Move-Item`, sondern folge der Sequenz `mkdir` → `cp` → Verify (Datei > 0 Bytes) → `rm`, DENN bei nicht-existenten Zielordnern benennt `mv` die Datei fälschlicherweise um statt sie zu verschieben.

**mkdir-Verify:** Bevor du Dateien in einen neu erstellten Ordner verschiebst, verifiziere mit `list_dir`, dass der Zielordner erfolgreich erstellt wurde, DENN Agenten ignorieren oft mkdir-Errors und verschieben Dateien in nicht-existierende Ordner → Dateien sind weg.

**Ablauf:**
1. `mkdir <zielordner>` ausführen
2. `list_dir <zielordner>` → existiert der Ordner und ist leer?
3. JA → `mv` oder `cp` ausführen
4. NEIN → STOPP. Error analysieren. Nicht blind weitermachen.

**Anti-Symlink:** Erstelle niemals Symlinks (`ln -s`), DENN sie brechen in hybriden Windows/Linux-Git-Umgebungen.

## 4. Secrets-Schutz

**SOG:** Committe niemals `.env`-Dateien oder API-Keys, DENN Secrets im Git-Verlauf sind öffentlich und irreversibel. Nutze `.env.example` als Template und prüfe vor jedem Commit: `git diff --cached | grep -iE '(api_key|password|token|secret)'` — Ergebnis muss leer sein.

**Dependencies:** Installiere keine ungeprüften Pakete. Prüfe regelmäßig `npm audit`.

## 5. Versionierung bei Datei-Erstellung

**SOG:** Wenn du eine neue Task-Datei, einen Prompt oder ein Handover-Dokument erstellst, das eine bestehende Datei ersetzen würde, versioniere die alte Datei mit der aktuellen Session-ID oder dem aktuellen Task-Namen, DENN ohne Versionierung ist der historische Kontext nicht mehr nachvollziehbar.

**Format:** `<dateiname>_v<YYMMDD>_<session-id>.md` oder `<dateiname>_<task-name>.backup.md`

**Beispiel:**
- Alt: `task.md` → neu: `task_20260522_abc123.md`
- Alt: `implementation_plan.md` → neu: `implementation_plan_v20260522_abc123.md`

**User-Frage bei Versionierung:**
```
[VERSIONIERUNG ERFORDERLICH]
Eine Datei mit diesem Namen existiert bereits. Wie soll ich versionieren?

1. [ ] Session-basiert: task_20260522_abc123.md
2. [ ] Task-basiert: task_showcase-landing.md
3. [ ] Einfach nummerieren: task_v2.md
4. [ ] Alte Datei löschen (nicht empfohlen)
```

## 6. Light Router

- **WENN** du Versionierungs-Details (Session-ID, Archivierung) brauchst ➔ **LIES** `DOCS/plans/versioning.md`
- **WENN** du den Playground-Workflow für Skript-Tests brauchst ➔ **LIES** `40_playground.md`
- **WENN** du Windows-spezifische Shell-Regeln brauchst ➔ **LIES** `10_windows_shell.md`
