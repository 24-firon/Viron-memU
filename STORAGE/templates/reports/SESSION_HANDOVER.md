<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# SESSION HANDOVER — Forensischer Bericht (Kompakt)

> Kurzer Forensik-Bericht am Session-Ende. **8 Sektionen** (G-08-Fix: ehrliche Zählung — das
> Voll-Format `templates/FORENSIC_REPORT.md` hat 9, weil es zusätzlich eine eigene
> Research-Sektion führt; diese KOMPAKT-Variante lässt Research bei Token-Knappheit bewusst weg
> und faltet Research-Funde stattdessen kurz in §2 Architektur-Entscheidungen ein, falls
> vorhanden), kalt und präzise. **DENN** jeder Satz ohne VERIFIZIERT/WAHRSCHEINLICH/OFFEN ist
> wertlos für Auditor und Nachfolger.
> **Ablage:** `DESK/reports/session-reports/[TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD].md`

---
session_title: [TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]
session_type: FORENSIC
bundle_mode: KOMPAKT
date: [YYYY-MM-DD]
next_session: [TASK]_[NN+1]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]
ersteller: [Session-Kennung + Stufe, z.B. "CDS-Session 02, Stufe S4" — oder Agent-/Session-Kennung]
report_type: FORENSIC
---

**Session-Titel:** [Titel]
**Datum:** [YYYY-MM-DD]
**Projekt/Repo:** [Name]
**Scope:** [Backend, Frontend, Auth, DB, DevOps, Research, Monorepo, Security]
**Session-Modus:** [Execution / Read-Only / Research / Debug / Mixed]
**Stufen-Tag:** [S1–S5·Intensität — Stufe, mit der die Session gefahren wurde (MILESTONE_GATEWAY §2)]

---

## 1. SYSTEMLAGE

[1-3 dichte Absätze: Ausgangslage, was war kaputt/unklar/gefährlich, warum architektonisch relevant]

## 2. ARCHITEKTUR-ENTSCHEIDUNGEN

- **[Thema]:** [Harter Fakt]
  *Warum:* [Architekturgrund]
- **[Thema]:** [Harter Fakt]
  *Warum:* [Begründung]

Falls keine Änderungen: validierte Erkenntnisse dokumentieren.

## 3. DATEIEN, PFADE & KONFIGURATIONEN

### Geändert
- `[Pfad]` — [Was wurde geändert]

### Neu angelegt
- `[Pfad]` — [Zweck]

### Nicht verändert
- `[Pfad]` — [Warum bewusst nicht angefasst]

## 4. DIAGNOSTIK, TESTS & BEWEISLAGE

- **Verifiziert:** [Beobachtung / Test / Log-Befund]
- **Wahrscheinlich:** [Starker Verdacht, nicht final bewiesen]
- **Offen:** [Nicht geprüft / nicht validiert]

## 5. REPOSITORY-HYGIENE

- Altlasten reduziert: [was]
- Workarounds noch da: [was]
- Doppelte Zustände: [was]

## 6. RISIKEN, TECHNICAL DEBT

- **[Risiko]:** [Beschreibung]
  *Auswirkung:* [Was kann kaputtgehen?]
  *Wahrscheinlichkeit:* [Niedrig / Mittel / Hoch]
  *Empfehlung:* [Was tun?]

## 7. HANDOVER FÜR DEN NÄCHSTEN AGENTEN

### Aktueller belastbarer Zustand
- Funktioniert: [was]
- Teilweise abgesichert: [was]
- Ungeklärt: [was]

### Verbotene Aktionen
- [Was darf der nächste Agent NICHT blind tun?]

### Nächste logische Schritte
1. [Erster konkreter Schritt]
2. [Zweiter konkreter Schritt]
3. [Dritter konkreter Schritt]

## 8. KURZFAZIT

[Ein dichter Satz, der den Zustand der Session präzise auf den Punkt bringt]

---

**[SESSION REPORT ERSTELLT]**

**Ablage:** `DESK/reports/session-reports/[TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD].md`

## Mini-DoD (G-08-Fix)

- [ ] YAML-Header vollständig (7 Felder, wie im Kopf dieser Datei)
- [ ] Alle 8 Sektionen befüllt (keine leeren Platzhalter `[...]`)
- [ ] Jede Aussage in §4 als VERIFIZIERT/WAHRSCHEINLICH/OFFEN markiert
- [ ] §7 „Nächste logische Schritte" ist konkret (kein „weitermachen")
- [ ] Research-Funde (falls vorhanden) in §2 eingefaltet, nicht stillschweigend weggelassen
