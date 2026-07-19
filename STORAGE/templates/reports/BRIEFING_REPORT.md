<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht (G-15/G-26 — neuer Report-Typ, M2b-Redesign):**
>
> - Der EINZIGE Report-Typ, dessen ADRESSAT der NACHFOLGER ist — nicht der Vorgänger, nicht der
>   Operator, nicht das Audit-Archiv. Alle anderen Reports (Forensic, SUMMARY, TTS, DEBUG, AUDIT,
>   POSTMORTEM, RESEARCH) berichten ÜBER die abgebende Session. Das BRIEFING berichtet FÜR die
>   kommende Aufgabe der Folgesession.
> - Pro FOLGE-TASK (nicht pro Session) ein eigener Klein-Report: Was du zu Task X wissen musst /
>   welche Fallen es gibt / wo du weitermachst / welche Belege es gibt.
> - **Ablage:** `WORKSPACE/<next-session>/handover/BRIEFING_[TASK-KURZNAME].md` — NICHT in
>   `session-reports/` (Adressat ist der Nachfolger, nicht das Archiv, F27-Regel).
> - **DARF auf die P00-Leseliste** (im Gegensatz zum Forensic-Report, F27) — genau dafür wurde es gebaut.
> - **Bundle-Verwendung:** Nach `WORKSPACE/<next-session>/handover/` kopieren, EINE Datei pro
>   klar abgrenzbarem Folge-Task (bei nur einem Folge-Task genügt eine Datei).
<!-- TEMPLATE-EXPLANATION-END -->

---
session_title: [TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]
report_type: BRIEFING
zieltask: [Name des Folge-Tasks, für den dieses Briefing geschrieben wurde]
date: [YYYY-MM-DD]
ersteller: [Session-Kennung + Stufe]
---

# BRIEFING — [Folge-Task-Titel]

**Für wen:** Die Folgesession, wenn sie mit [Folge-Task] beginnt.
**Woher stammt dieses Wissen:** [Forensic-Report dieser Session / direkte Beobachtung / Operator-Aussage]

---

## 1. Was du zu diesem Task wissen musst

[1-3 dichte Absätze: Kontext, den man NICHT aus task.md allein bekommt — das WARUM hinter dem Task,
relevante Vorgeschichte, was schon probiert und verworfen wurde.]

## 2. Fallen (konkret, nicht generisch)

- **[Falle 1]:** [Was schiefgehen kann, warum, wie du es erkennst]
- **[Falle 2]:** [...]

## 3. Wo du konkret weitermachst

**Erster Handgriff:** [Exakte Datei / exakter Befehl / exakter Einstiegspunkt]
**Danach:** [Nächste 2-3 Schritte in Reihenfolge]

## 4. Belege

- `[Pfad]` — [was dort zu finden ist]
- `[Commit-Hash]` — [was er zeigt]

## 5. Selbstprüfung (Pflicht, 3-5 Zeilen — `PROMPTS/BRIEFING_REPORT_GENERATOR.md` §5)

- [Könnte ein fabrikneuer Agent allein hieraus + P00 nahtlos starten? Was fehlt ggf. wo?]
- [Unsicherste Aussage + ihre Kennzeichnung]
- [Nur-Gedächtnis-Behauptungen statt Belege?]

---

**[BRIEFING ERSTELLT — für Folge-Task: [Name]]**
