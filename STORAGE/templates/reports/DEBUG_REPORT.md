<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht:** Fehlersuche-Protokoll (Report-Derivat) für Debug-Sessions.
> **Wann nutzen:** Router-Entscheid in INSTRUCTIONS — die Session war überwiegend Fehlersuche.
> Ergänzt (ersetzt nicht) den Forensic-Report; die Root-Cause + Lesson fließen in lessons_learned.
> **Ablage:** `DESK/reports/session-reports/[TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]_debug.md`
<!-- TEMPLATE-EXPLANATION-END -->
---
session_title: [TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]
report_type: DEBUG
date: [YYYY-MM-DD]
ersteller: [Session-Kennung + Modell]
status: [aktiv | übergeben | erledigt | obsolet]
---

# Debug-Report — [Symptom in Kürze]

## 1. Symptom
[Beobachtetes Fehlverhalten, exakt. Repro-Schritte. Erwartetes vs. tatsächliches Verhalten.]

## 2. Hypothesen
| # | Hypothese | Plausibilität (hoch/mittel/niedrig) |
|:--|:--|:--|
| H1 | [...] | [...] |

## 3. Tests & Beobachtungen
[Je Hypothese: durchgeführter Test → Ergebnis (BESTÄTIGT / WIDERLEGT), mit Beleg (Output/Log/Zeile).]

## 4. Root Cause
[Die eine bestätigte Ursache — mit Beweis, nicht Vermutung. Falls nicht gefunden: „OFFEN" + Stand.]

## 5. Fix
[Was geändert wurde: Datei:Zeile + warum genau das die Ursache behebt. Falls nur Workaround: markieren.]

## 6. Lesson / Prävention
[Was die Wiederholung verhindert → Kandidat für `lessons_learned`.]

---
**DoD:** Symptom reproduzierbar beschrieben · ≥1 Hypothese bestätigt/widerlegt mit Beleg · Root
Cause bewiesen oder ehrlich „OFFEN" · Fix mit Datei:Zeile · Lesson für lessons_learned · YAML `status:`.
