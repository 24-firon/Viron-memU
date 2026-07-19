<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht (G-26 — neuer Report-Typ, M2b-Redesign):**
>
> - Für Sessions, deren Kern (oder ein wesentlicher Teil) externe Recherche war (F33-Klausel:
>   Recherche ist jederzeit erlaubt) — Quellen, Befunde, Konfidenz, offene Fragen.
> - Unterscheidet sich vom Forensic-Report dadurch, dass der Fokus auf EXTERNEM Wissen liegt
>   (Doku, APIs, Community-Erfahrung), nicht auf internen Architektur-Entscheidungen.
> - **Ablage:** `DESK/reports/session-reports/[SESSION-TITEL]_RESEARCH.md` ODER als Artefakt direkt
>   im HANDOVER referenziert, wenn die Recherche Grundlage für einen Folge-Task ist (dann zusätzlich
>   `RESEARCH_PROMPT.md`-Artefakt für externe Recherche nutzen, falls die Recherche erst von der
>   Folgesession/dem Operator durchgeführt werden soll — siehe G-16).
<!-- TEMPLATE-EXPLANATION-END -->

---
session_title: [TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]
report_type: RESEARCH
date: [YYYY-MM-DD]
ersteller: [Session-Kennung + Stufe]
---

# RESEARCH — [Thema]

**Frage(n):** [Was sollte geklärt werden — 1-3 konkrete Fragen]
**Zeitraum-Constraint:** [z.B. „nur 2025/2026-Quellen" — falls relevant]

---

## 1. TL;DR

[Die harte Empfehlung/Antwort in 2-3 Sätzen.]

## 2. Quellen

| Quelle | Datum/Version | Vertrauenswürdigkeit | Kernaussage |
|:---|:---|:---|:---|
| `[Link/Pfad]` | [Datum] | [Offiziell/Community/Experimentell] | [1 Satz] |

## 3. Befunde nach Konfidenz

- **VERIFIZIERT:** [Direkt aus Primärquelle bestätigt]
- **WAHRSCHEINLICH:** [Starkes Indiz, keine Primärquelle]
- **OFFEN:** [Widersprüchliche oder fehlende Quellenlage]

## 4. Community-Reality-Check (falls abweichend von offizieller Doku)

- **⚠️ [Thema]:** [Offizielle Doku sagt X, reale Erfahrung zeigt Y]

## 5. Konsequenz für dieses Projekt

[Was folgt konkret daraus — Entscheidung, Task, Regel-Vorschlag?]

## 6. Offene Fragen

- [Was bleibt nach dieser Recherche ungeklärt?]

## 7. Selbstprüfung (Pflicht, 3-5 Zeilen — `PROMPTS/RESEARCH_REPORT_GENERATOR.md` §5)

- [Hängt jeder Befund an einer Quellen-Zeile? X von Y]
- [Schwächst-belegter Befund — entsprechend eingestuft?]
- [Veraltbare Fakten datiert? Trainingswissen markiert?]

---

**[RESEARCH ERSTELLT]**
