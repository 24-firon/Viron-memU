<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# KONSERVIERUNGS_MANIFEST (Kompakt)

> 4 fundamentale Gesetze gegen Datenverlust. **DENN** Datenverlust ist der größte Schmerzfaktor für Operator und zukünftige Agenten.

## DIE 4 GESETZE

### 1. KEINE LÖSCHUNG
Einmal dokumentierte Items dürfen **NIEMALS** gelöscht werden.
- Dateien, Regeln, Skills, Learnings — nichts wird zerstört
- Archivierung ist der einzige legitime Weg in die Vergangenheit
- **Ausnahme:** Operator erteilt expliziten schriftlichen Löschbefehl mit Begründung
- **Beispiel:** Statt `rm config.yaml` → `mv config.yaml _ARCHIVE/2026-06-05_config.yaml`

### 2. KEINE REDUKTION
Granulare Beschreibungen dürfen **NIEMALS** gekürzt oder durch Zusammenfassungen ersetzt werden.
- `//...`-Abkürzungen sind verboten (Golden Axiom: "Intelligenz ist Integrität")
- Tabellen bleiben vollständig. Listen bleiben vollständig. Code bleibt zu 100%
- **Die Ausnahme:** "Archive First, Shrink Later" (siehe TIER_MEMORY)

### 3. BEWEISPFLICHT
Jeder Fortschritt muss durch physische Artefakte dokumentiert werden.
- "Ich habe es gelesen" ist KEIN Beweis — ein Report in `REPORTS/` ist ein Beweis
- "Ich habe es verstanden" ist KEIN Beweis — ein `DECISION_LOG.md`-Eintrag ist ein Beweis
- **Terminal-Output** (letzte 5 Zeilen) ist der härteste Beweis
- **Beispiel:** Statt "Tests passed" → "Tests passed. Output: 5/5 ok, 0 fail, 0 skip"

### 4. INTEGRATION
Der Plan ist lebendig. Strategie-Updates werden **an die korrekte Stelle** integriert, nicht als Append an das Ende geklebt.
- Neue Phasen gehören ans Ende (Append)
- Korrekturen in bestehende Blöcke (**Replace**)
- Kein "Ich habe das mal eben schnell geändert" — jeder Edit muss dokumentiert sein

## ANWENDUNG AUF CDS

| Gesetz | CDS-Konkretisierung |
|:---|:---|
| KEINE LÖSCHUNG | `_ARCHIVE/` ist ein Museum. Nichts wird gelöscht. Alte V1-Regeln wandern dorthin, aber verschwinden nie. |
| KEINE REDUKTION | Boot-Regeln 5-15 Zeilen (Thin Triggers). Heavy Payloads in DOCS/ bleiben vollständig. |
| BEWEISPFLICHT | Jede Rule-Erstellung erzeugt einen `DECISION_LOG.md`-Eintrag. Jeder SubAgent schreibt einen Report nach `REPORTS/`. |
| INTEGRATION | Regeln werden per `edit` (nicht `write`) in die korrekte Stelle integriert. Neue Regeln ins `src/rules/` + `.opencode/rules/` (Regel 90). |

## WAS PASSIERT WENN EIN AGENT DIESE GESETZE BRICHT?

| Verstoß | Konsequenz | Verifikation |
|:---|:---|:---|
| Datei gelöscht ohne Archiv | Datenverlust — irreversibel | Git-History prüfen |
| `//...`-Abkürzung eingefügt | Information verloren | Code-Review |
| Behauptung ohne Evidence | Halluzination | Report-Pflicht (P99) |
| Plan ans Ende appended statt integriert | Architektur-Drift | Decision-Log prüfen |
