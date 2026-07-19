<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# SESSION RITUAL (Kompakt)

> **⚠️ NUR VERFAHREN, NICHT KOPIEREN (F24)** — wird in Schritt 6.4 der INSTRUCTIONS.md DIREKT AUSGEFÜHRT, nicht in den Session-Ordner kopiert.

> 5-Säulen-Checkliste. Alle GRÜN = Session sauber abgeschlossen. **DENN** eine Session ohne Ritual startet der nächste Agent bei Null.

## 5 SÄULEN

### 1. BUCHHALTUNG (todowwrite)
- Setze JEDEN Task der Session auf `completed` oder `cancelled`
- **Verifikation:** Keine Tasks im Status `in_progress` oder `pending`
- **Was passiert wenn nicht:** Nächster Agent sieht offene Tasks und weiß nicht ob sie erledigt sind

### 2. ARTEFAKT-HYGIENE (Workspace-Cleanup)
- Lösche temporäre Dateien: `.tmp`, `.log`, `.fake`, `.json`-Dumps
- **Verifikation:** `ls` oder `glob` zeigt keine verwaisten Drafts
- **Was passiert wenn nicht:** Nächster Agent liest temporäre Dateien und verwechselt sie mit echten Artefakten

### 3. BEWEISSICHERUNG (Report-Pflicht)
- Strukturierter Report unter `DESK/reports/session-reports/[SESSION].md`
- **Verifikation:** Der Report muss physisch existieren
- **Was passiert wenn nicht:** Nächster Agent weiß nicht was passiert ist und fängt von vorne an

### 4. GIT-STATUS (Versions-Integrität)
- Führe `git status` aus
- **Verifikation:** `git status` muss `clean` oder `staged` zeigen
- **Was passiert wenn nicht:** Uncommitteter Code geht bei einem Reset verloren

### 5. ABSCHLUSS-MARKER
- Erst wenn alle 4 vorherigen GRÜN:
> "Session sauber abgeschlossen. Alle Artefakte gesichert, Workspace ist clean."

## REPORT-MUSTER (gutes Beispiel)

```markdown
# SESSION REPORT — [Datum]

## Was wurde getan?
- [X] Dateien erstellt
- [Y] Dateien geändert

## Was wurde nicht getan?
- [Z] Task konnte nicht abgeschlossen werden weil [Grund]

## Evidence
[Terminal-Output / Git-Diff]

## Lese-Beweise
| Datei | Beweis |
|:---|:---|
| [Pfad] | "Gelesen: X Zeilen, Inhalt Y" |
```

## WAS PASSIERT WENN EINE SÄULE NICHT GRÜN IST?

- **Säule 1 (todowrite):** Fehlende Einträge erstellen BEVOR du fortfährst
- **Säule 2 (Cleanup):** Temporäre Dateien löschen BEVOR du fortfährst
- **Säule 3 (Report):** Report erstellen BEVOR du fortfährst
- **Säule 4 (git status):** Änderungen stage oder commit BEVOR du fortfährst
- **Säule 5 (Marker):** Erst wenn alle 4 vorherigen GRÜN

**Golden:** Keine Abkürzungen. Jede Säule muss physisch verifiziert werden.
