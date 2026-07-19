<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht (G-26 — neuer Report-Typ, M2b-Redesign):**
>
> - Für Sessions, die GESCHEITERT sind oder abgebrochen werden mussten (Kontext-Verlust,
>   Fehlplanung, wiederholter Gateway-Verstoß) — der ANALYTISCHE Zwilling zum Re-Start-Workflow
>   (G-24, `INSTRUCTIONS.md` 1.1 Fall 4): Der Re-Start-Workflow kopiert das Bundle und macht
>   praktisch weiter; dieser Report analysiert, WARUM es scheiterte, damit es nicht wieder passiert.
> - Fokus: Root Cause, nicht Schuldzuweisung. Kalt, präzise (Doktrin wie `FORENSIC_REPORT_GENERATOR.md`).
> - **Ablage:** `DESK/reports/session-reports/[SESSION-TITEL]_POSTMORTEM.md` (Suffix, weil neben
>   dem eigentlichen — ggf. unvollständigen — Forensic-Report der gescheiterten Session steht).
<!-- TEMPLATE-EXPLANATION-END -->

---
session_title: [TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]
report_type: POSTMORTEM
date: [YYYY-MM-DD]
ersteller: [Session-Kennung + Stufe]
---

# POSTMORTEM — [Titel]

**Was ist gescheitert:** [1 Satz — konkret, nicht vage]
**Re-Start-Ordner (falls G-24 angewendet):** `WORKSPACE/[neuer-ordner]/`

---

## 1. Zeitlicher Ablauf (nur die relevanten Wendepunkte)

1. [Zeitpunkt/Meilenstein] — [was passierte]
2. [Zeitpunkt/Meilenstein] — [was passierte, wo es kippte]

## 2. Root Cause

[1-3 dichte Absätze: die TATSÄCHLICHE Ursache, nicht das Symptom. Unterscheide explizit: Was war
der Auslöser (Trigger)? Was war die tieferliegende Ursache (Root Cause)?]

## 3. Was war NICHT die Ursache (Fehleinschätzungen unterwegs)

- [Was zunächst vermutet wurde, sich aber als falsch herausstellte]

## 4. Frühwarnzeichen (im Nachhinein erkennbar)

- [Was hätte VOR dem Scheitern auffallen müssen?]

## 5. Konkrete Prävention

- **Regel/Gate-Vorschlag:** [Was verhindert eine Wiederholung — Skill-Fix, neue Regel, neues Gate?]
- **Manifestiert?** [JA — wo/Commit / NEIN — als Task angelegt: wo]

## 6. Was gerettet werden konnte

- [Welcher Teil der Arbeit ist trotzdem verwertbar — z.B. via Re-Start-Bundle-Kopie]

## 7. Selbstprüfung (Pflicht, 3-5 Zeilen — `PROMPTS/POSTMORTEM_REPORT_GENERATOR.md` §5)

- [Root Cause belegt oder plausibelste Hypothese — und so gekennzeichnet?]
- [Jede Prävention manifestiert (Commit/Task/Gate)?]
- [Verhindert die Prävention den Fall — oder nur ein Symptom?]

---

**[POSTMORTEM ERSTELLT]**
