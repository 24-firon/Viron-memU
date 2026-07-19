<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht:**
>
> - Das "Gesetz der Persistenz" — 4 fundamentale Gesetze gegen Datenverlust
> - Anwendung auf das Context-Dispatcher-System
> - Konsequenzen bei Verstoß
>
> - **Wann anwenden:** IMMER. Bei jeder Datei-Operation, jedem Edit, jeder Löschung.
>
> - **Skill-Self-Location:** Detail-Version. Konstante (kompakte) Variante → siehe `ADDITIONAL/KONSERVIERUNGS_MANIFEST.md` im Skill-Verzeichnis.
<!-- TEMPLATE-EXPLANATION-END -->

# KONSERVIERUNGS-MANIFEST (Gesetz der Persistenz)

> **WARUM:** Datenverlust ist der größte Schmerzfaktor für den Operator und zukünftige Agenten. Diese 4 Gesetze sind NICHT VERHANDELBAR.

## Die 4 Gesetze

### 1. KEINE LÖSCHUNG
Einmal dokumentierte Items dürfen **NIEMALS** gelöscht werden.
- Dateien, Regeln, Skills, Learnings — nichts wird zerstört.
- Archivierung ist der einzige legitime Weg in die Vergangenheit.
- **Ausnahme:** Operator erteilt expliziten schriftlichen Löschbefehl mit Begründung.

### 2. KEINE REDUKTION
Granulare Beschreibungen dürfen **NIEMALS** gekürzt oder durch Zusammenfassungen ersetzt werden.
- `//...`-Abkürzungen sind verboten (Golden Axiom: "Intelligenz ist Integrität").
- Tabellen bleiben vollständig. Listen bleiben vollständig. Code bleibt zu 100%.
- **Die Ausnahme heißt "Archive First, Shrink Later"** (siehe `references/TIER_MEMORY.md`).

### 3. BEWEISPFLICHT
Jeder Fortschritt muss durch physische Artefakte (Dateien, Reports, Diffs) dokumentiert werden.
- "Ich habe es gelesen" ist kein Beweis. Ein Report in `REPORTS/` ist ein Beweis.
- "Ich habe es verstanden" ist kein Beweis. Ein `DECISION_LOG.md`-Eintrag ist ein Beweis.
- **Terminal-Output** (letzte 5 Zeilen) ist der härteste Beweis.

### 4. INTEGRATION
Der Plan ist lebendig. Strategie-Updates werden **an die korrekte Stelle** integriert, nicht als Append an das Ende geklebt.
- Neue Phasen gehören ans Ende (Append).
- Korrekturen in bestehende Blöcke (**Replace**).
- Kein "Ich habe das mal eben schnell geändert" — jeder Edit muss dokumentiert sein.

---

## Anwendung auf CDS

| Gesetz | CDS-Konkretisierung |
|:---|:---|
| KEINE LÖSCHUNG | `ARCHIVE/` ist ein Museum. Nichts wird gelöscht. Alte V1-Regeln wandern dorthin, aber verschwinden nie. |
| KEINE REDUKTION | Boot-Regeln 5-15 Zeilen (Thin Triggers). Heavy Payloads in DOCS/ bleiben vollständig. |
| BEWEISPFLICHT | Jede Rule-Erstellung erzeugt einen `DECISION_LOG.md`-Eintrag. Jeder SubAgent schreibt einen Report nach `REPORTS/`. |
| INTEGRATION | Regeln werden per `edit` (nicht `write`) in die korrekte Stelle integriert. |

---

## Was passiert wenn ein Agent dieses Gesetz bricht?

| Verstoß | Konsequenz | Verifikation |
|:---|:---|:---|
| Datei gelöscht ohne Archiv | Datenverlust — irreversibel | Git-History prüfen |
| `//...`-Abkürzung eingefügt | Information verloren | Code-Review |
| Behauptung ohne Evidence | Halluzination | Report-Pflicht |
| Plan ans Ende appended statt integriert | Architektur-Drift | Decision-Log prüfen |
