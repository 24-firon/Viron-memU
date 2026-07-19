<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht (D-005.6-Klarstellung, 2026-07-11):** Der next-session-Extrakt aus
> dem Forensic-Report — NICHT ein optionaler Kurzüberblick für Menschen, sondern die eigentliche
> Pflichtlektüre der Folgesession (F27: der volle Forensic-Report gehört NIE auf die P00-Leseliste,
> nur dieses SUMMARY-Derivat). Enthält NUR, was die Folgesession wirklich braucht — nicht alles,
> was im Forensic-Report steht.
> **Wann nutzen:** IMMER, in jeder Session (Abschnitt 4.3) — keine Router-Ausnahme mehr für
> „kleine Sessions". Wird zusätzlich zum Forensic-Report abgeleitet, sobald der Forensic-Report
> im eigenen Kontext vorliegt (billige Verdichtung eines bereits vorhandenen Texts).
> **Ablage:** `DESK/reports/session-reports/[TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]_summary.md`
<!-- TEMPLATE-EXPLANATION-END -->
---
session_title: [TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]
report_type: SUMMARY
date: [YYYY-MM-DD]
ersteller: [Session-Kennung + Stufe, z.B. "CDS-Session 02, Stufe S4" — oder Agent-/Session-Kennung]
status: [aktiv | übergeben | erledigt | obsolet]
---

# Kurzbericht — [Session-Titel]

**BLUF:** [1–2 Sätze: Was wurde erreicht, was bleibt offen.]

## Was passiert ist
- [Kernpunkte der Session, 3–6 Stichpunkte]

## Entscheidungen
- [wichtigste Entscheidungen, je 1 Zeile — Detail steht im decision_log]

## Offen / Nächste Schritte
- [was die Folgesession konkret tun muss]

## Belege
- Forensic-Report: `DESK/reports/session-reports/[SESSION-TITEL].md` (der Forensic trägt KEIN `_forensic`-Suffix — der Dateiname IST der Session-Titel, SESSION_TITEL_SCHEMA §5)
- [Commits / Artefakte / grep-Nachweise]

---
**DoD:** BLUF vorhanden · verweist auf den Forensic-Report als Quelle · Entscheidungen & offene
Punkte decken sich mit `decision_log`/`task.md` · YAML mit `status:`-Feld.
