<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht (G-16/G-d-Fix, SKILL-AUDIT_07 — Gefäß für F33(c)):**
>
> - F33(c) erlaubt einen dritten Weg für den Frische-Check vor dem Handover: statt selbst zu
>   recherchieren (a) oder einen Recherche-Subagenten zu spawnen (b), einen **fertigen Prompt als
>   Artefakt** ins Handover legen, den der Operator EXTERN (z.B. Perplexity, ein anderes Tool)
>   ausführt und das Ergebnis zurückbringt. Bis SKILL-AUDIT_07 hatte dieser Weg kein Gefäß — G-16
>   benannte das 2026-07-11 als offenen Befund, der aus allen Fix-Paketen herausfiel.
> - **Abgrenzung zu `RESEARCH_REPORT.md`:** Jenes Template dokumentiert eine bereits VON DIESER
>   SESSION durchgeführte Recherche (Ergebnis). Dieses Template hier ist der PROMPT für eine
>   Recherche, die noch nicht stattgefunden hat — der Ersteller weiß, dass sie nötig ist, kann sie
>   aber nicht selbst leisten (Zeit/Tool-Zugriff/Aktualität), und formuliert sie präzise vor.
> - **Ablage:** `WORKSPACE/<next-session>/handover/RESEARCH_PROMPT_[Thema].md` (Tabu-Zone wie P00-P02
>   — für den Operator bestimmt, nicht für den nächsten Agenten). Verweis darauf gehört ins
>   HANDOVER (Sektion 7 „Nächste Schritte" oder Sektion 11 „Regel-Vorschläge", je nach Kontext).
<!-- TEMPLATE-EXPLANATION-END -->

# RESEARCH-PROMPT — [Thema]

**Für:** Operator, extern auszuführen (z.B. Perplexity, Web-Recherche-Tool)
**Warum diese Session es nicht selbst klärt:** [z.B. „Erfordert Live-Preisdaten, die nach
Trainingsstand nicht verlässlich sind" / „Zeitbudget dieser Session reicht nicht für eine seriöse
Tiefenrecherche" / „Braucht Zugriff auf ein Tool, das dieser Session nicht zur Verfügung steht"]

---

## 1. Die Frage(n) — präzise, beantwortbar

1. [Konkrete Frage 1 — so formuliert, dass ein externes Tool sie ohne weiteren Kontext beantworten kann]
2. [Konkrete Frage 2, falls vorhanden]

## 2. Kontext, den der Ausführende braucht

[Alles, was NICHT im externen Tool bereits bekannt ist — Projekt-Constraints, bereits geprüfte und
verworfene Optionen (damit nicht dieselbe Sackgasse nochmal empfohlen wird), Zeitraum-Constraint
(z.B. „nur Stand 2026 relevant").]

## 3. Format der erwarteten Antwort

[Was soll zurückkommen — Tabelle? Ja/Nein + Begründung? Eine Zahl mit Quelle? So konkret wie
möglich, damit das Ergebnis direkt in `RESEARCH_REPORT.md` oder `decision_log.md` übernommen
werden kann, ohne weitere Rückfragen.]

## 4. Was mit dem Ergebnis passiert

[Wohin fließt die Antwort — welche Entscheidung/welcher Task hängt daran? Wer trägt sie ein
(Operator selbst / nächste Session per `templates/RESEARCH_REPORT.md`)?]

---

**[RESEARCH-PROMPT ERSTELLT — bereit zum Kopieren in ein externes Tool]**
