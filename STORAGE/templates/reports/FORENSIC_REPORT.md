<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
---
session_title: [TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]
session_type: FORENSIC
bundle_mode: AUSFÜHRLICH
date: [YYYY-MM-DD]
next_session: [TASK]_[NN+1]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]
ersteller: [Session-Kennung + Stufe, z.B. "CDS-Session 04, Stufe S4" — Ersteller NICHT im Titel]
report_type: FORENSIC
---

# SESSION REPORT: [Titel der Session]

**Zielpublikum (F23):** Mensch / Audit / Historie — **NICHT** die primäre Pflichtlektüre der Folge-Session (das ist `HANDOVER.md` + `decision_log.md`). Der Forensic-Report dient als interne Extraktions- und Audit-Quelle. Nur die explizit für die Folge-Session geschriebenen Klein-Reports (SUMMARY, TTS-Operator-Summary, ggf. DEBUG) werden als Handover-Beigabe mitgeliefert und DÜRFEN auf der P00-Leseliste stehen. Forensic-Reports gehören **NICHT** auf die P00-Leseliste (nur bei begründeten Ausnahmen, z.B. wenn die Folge-Session explizit forensische Tiefe braucht).

**Ablage:** `DESK/reports/session-reports/[TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD].md`

**Datum:** [YYYY-MM-DD]
**Projekt/Repo:** [Name oder Kontext]
**Scope:** [z. B. Backend, Frontend, Auth, DB, DevOps, Research, Monorepo, CMS, Video, Security]
**Session-Modus:** [Execution / Read-Only / Research / Debug / Advisory / Mixed]

---

## 1. Systemlage

[Beschreibe in 1-3 dichten Absätzen die tatsächliche Ausgangslage. Kein Gelaber. Nur die operative Realität:
- Was war der Zustand?
- Was war kaputt, unklar oder gefährlich?
- Warum war die Lage architektonisch relevant?]

---

## 2. Architektur-Entscheidungen & Reparaturen

[Beschreibe die Kernentscheidungen in operativ verwertbarer Form.]

- **[Thema / Konflikt]:** [Harter Fakt, Änderung, Port, Pfad, Policy, UI-Setting, Verhalten]
  *Warum:* [Architekturgrund / technischer Konflikt / verworfene Alternative]

- **[Thema / Konflikt]:** [Harter Fakt]
  *Warum:* [Begründung]

- **[Thema / Konflikt]:** [Harter Fakt]
  *Warum:* [Begründung]

[Falls keine Änderungen durchgeführt wurden, dokumentiere stattdessen die validierten Erkenntnisse und warum bewusst nicht eingegriffen wurde.]

---

## 3. Dateien, Pfade & Konfigurationen

[Nur harte Fakten. Keine Codeblöcke.]

### Geändert
- `[Pfad/Datei]` - [Was wurde geändert?]
- `[Pfad/Datei]` - [Was wurde geändert?]

### Neu angelegt
- `[Pfad/Datei]` - [Zweck]

### Verschoben / Umbenannt / Archiviert
- `[Altpfad]` -> `[Neupfad]` - [Grund]

### Nicht verändert
- `[Pfad/Datei/Systembereich]` - [Warum bewusst nicht angefasst]

### Relevante Konfigurationen / Zustände
- `[Variable / Setting / Policy / Port / Endpoint / Branch / Container / Rolle]` - [Aktueller Zustand]
- `[Variable / Setting / Policy / Port / Endpoint / Branch / Container / Rolle]` - [Aktueller Zustand]

---

## 4. Diagnostik, Tests & Beweislage

[Dokumentiere die relevanten Beobachtungen der Session.]

- **Verifiziert:** [Beobachtung / Test / Log-Befund / HTTP-Verhalten / UI-Zustand]
- **Verifiziert:** [Beobachtung]
- **Wahrscheinlich:** [Starker Verdacht, aber nicht final bewiesen]
- **Offen:** [Nicht geprüft / nicht validiert / widersprüchlich]

[Wenn eine frühere Annahme korrigiert wurde, dokumentiere das explizit:]
- **Korrigierte Fehleinschätzung:** [Was wurde zunächst angenommen, was stellte sich als richtig heraus?]

---

## 5. Repository-Hygiene & Operative Ordnung

[Beschreibe, ob diese Session das Repo/systemisch sauberer oder fragiler gemacht hat.]

- Welche Altlasten wurden reduziert?
- Welche temporären Workarounds existieren noch?
- Gibt es doppelte Zustände, Ghost-Dateien, versteckte Konfigurationsquellen, manuelle UI-Abhängigkeiten oder andere kognitive Fallen?

---

## 6. Risiken, Technical Debt & Systemische Bruchstellen

[Liste die Risiken ohne Beschönigung.]

- **[Risiko]:** [Beschreibung]
  *Auswirkung:* [Was kann kaputtgehen?]
  *Wahrscheinlichkeit:* [Niedrig / Mittel / Hoch]
  *Empfohlene Absicherung:* [Was sollte als Nächstes passieren?]

- **[Risiko]:** [Beschreibung]
  *Auswirkung:* [...]
  *Wahrscheinlichkeit:* [...]
  *Empfohlene Absicherung:* [...]

---

## 7. Research, Einordnung & Korrektur von Denkfehlern

[Pflicht, wenn die Session Research, externe Doku, Reports oder ältere Agentenannahmen berührt hat.]

- Welche vorherigen Annahmen waren korrekt?
- Welche waren falsch oder veraltet?
- Welche Dokumentation / welcher Bericht war hilfreich?
- Welche "Best Practice" erwies sich im konkreten Setup als irreführend?
- Welche Architekturwahrheit gilt jetzt stattdessen?

---

## 8. Handover für den nächsten Agenten

[Schreibe diesen Abschnitt so, dass der nächste Agent ohne erneute Eskalation ansetzen kann.]

### Aktueller belastbarer Zustand
- [Was funktioniert sicher?]
- [Was ist nur teilweise abgesichert?]
- [Was ist ungeklärt?]

### Verbotene oder riskante Aktionen
- [Was darf der nächste Agent auf keinen Fall blind tun?]
- [Welche destruktiven Schritte sind tabu?]

### Nächste logische Schritte
1. [Erster konkreter Schritt]
2. [Zweiter konkreter Schritt]
3. [Dritter konkreter Schritt]

### Falls sofort weitergearbeitet wird
- [Welche Datei / welcher Service / welcher Screen / welcher Befehl ist der sinnvollste Einstiegspunkt?]

---

## 9. Kurzfazit in einem Satz

[Ein einziger dichter Satz, der den Zustand der Session präzise auf den Punkt bringt.]

---

**[FORENSIC SESSION REPORT ERSTELLT]**

---

## DoD-Kriterien (Selbstprüfung)

- [ ] YAML-Header mit `session_title`, `session_type`, `bundle_mode`, `date`, `next_session`, `ersteller`, `report_type` (7 Felder)
- [ ] 9 Sektionen in exakter Reihenfolge (Systemlage → Kurzfazit)
- [ ] Architektur-Entscheidungen mit Warum
- [ ] Dateien-Tabelle mit "Geändert/Neu/Nicht verändert"
- [ ] Diagnostik mit VERIFIZIERT/WAHRSCHEINLICH/OFFEN
- [ ] Risiken mit Auswirkung + Wahrscheinlichkeit + Absicherung
- [ ] Handover für nächsten Agenten mit verbotenen Aktionen
- [ ] Kurzfazit in 1 Satz
- [ ] KEINE erfundenen Fakten - wenn nicht geprüft, steht "OFFEN" dabei