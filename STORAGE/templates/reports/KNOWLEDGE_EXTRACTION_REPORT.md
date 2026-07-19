<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht (G-26 — neuer Report-Typ, M2b-Redesign):**
>
> - **Kein Selbst-Anwendungs-Template.** Dieser Report-Typ wird NICHT vom Skill-Agenten aus dem
>   eigenen Gedächtnis über die eigene Session erzeugt (D-003: Advisory-Degradation +
>   Selbstbild-Färbung verfälschen genau diese Extraktion). Er entsteht durch Anwendung eines der
>   zwei Extraktions-Prompts aus `PROMPTS/` — `UNIVERSAL_CHAT_EXTRACTOR.md` (technische/Dev-Chats,
>   Dual-Output) oder `CASUAL_CHAT_DISTILLATION_PROTOCOL.md` (Casual/Mixed-Chats) — angewendet
>   entweder vom OPERATOR (Prompt in die laufende Session geworfen, VOR dem Handover-Skill-Trigger)
>   oder von einer FRISCHEN Session über den Chat-Export (D-003.1).
> - **Diese Datei hier ist nur der STRUKTUR-RAHMEN**, in den der Skill das bereits erzeugte
>   Extraktionsergebnis einordnet/verlinkt — er strukturiert, er extrahiert nicht selbst.
> - **Ablage:** `DESK/reports/session-reports/[SESSION-TITEL]_KNOWLEDGE-EXTRACTION.md`
<!-- TEMPLATE-EXPLANATION-END -->

---
session_title: [TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]
report_type: KNOWLEDGE-EXTRACTION
extraktor_verwendet: [UNIVERSAL_CHAT_EXTRACTOR v1.1 | CASUAL_CHAT_DISTILLATION_PROTOCOL v1.0]
angewendet_von: [Operator (eingeworfen) | frische Session (Chat-Export)]
date: [YYYY-MM-DD]
ersteller: [Session-Kennung + Stufe]
---

# KNOWLEDGE-EXTRACTION — [Quelle: Session-/Chat-Titel]

**Quelle des Rohmaterials:** [Chat-Export-Pfad oder Session-Referenz]
**Angewendeter Extraktor:** [siehe YAML — Anwendungs-Doktrin D-003 eingehalten? JA/NEIN + wie]

---

## 1. Vollversion (Sicherheitsnetz — Pflicht, ohne Rückfrage)

[Verweis auf die vom Extraktor erzeugte Vollversion, ODER Inline-Einbettung, falls kurz genug.
Anti-Erfindungs-Regel gilt: `[IM CHAT NICHT VORGEKOMMEN]` statt Auffüllen.]

## 2. Kuratierte Auswahl (interaktiv, falls vom Extraktor erzeugt)

[Verweis auf die zweite Extraktor-Datei — Modus A/B/C/D je nach Nutzerwahl.]

## 3. Kondensierte Knowledge Items (das eigentliche Ziel dieses Reports)

Pro Item: Regel-/Doku-Kandidat, mit Rohzitat-Beleg (Konservierungsgesetz 2).

- **[Item 1]:** [Kondensierte Aussage] — Beleg (Rohzitat): „[...]"
- **[Item 2]:** [...]

## 4. Manifestierungs-Vorschlag (D-015/F38-Anschluss)

| Knowledge Item | Ziel-Ort | Status |
|:---|:---|:---|
| [Item 1] | [Regel-Datei / DOCS/ / Skill-Fix / Task] | vorgeschlagen / manifestiert |

## 5. Selbstprüfung (Pflicht laut Extraktor-Doktrin)

[Hat der Extraktor seine eigene Selbstprüfungs-Sektion durchlaufen? Ergebnis übernehmen.]

---

**[KNOWLEDGE-EXTRACTION ERSTELLT]**
