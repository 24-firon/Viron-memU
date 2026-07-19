<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht:**
>
> - Atomare Task-Verwaltung pro Session (M1/M2/M3)
> - Silo-Struktur mit Checkboxen und Prioritäten
> - SubAgent-Orchestration-Matrix
> - Model-Wechsel-Prüfpunkte pro Meilenstein
>
> - **Wann pflegen:** Nach jedem Task-Abschluss (HD-7)
> - **Bundle-Verwendung:** Diese Datei wird nach `WORKSPACE/<session>/desk/` kopiert. Sie ist ein TEMPLATE zum Ausfüllen.
<!-- TEMPLATE-EXPLANATION-END -->

# task.md — Template für Session-Task-Tracking

> **Zweck:** Atomare Task-Verwaltung pro Session. Haupt- und Unterpunkte, Meilensteine, Model-Wechsel-Prüfpunkte.
> **Wann pflegen:** Nach jedem Task-Abschluss, NICHT erst am Session-Ende (HD-7).

---

## Session-Header

```
SESSION: [TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]
DATUM: [YYYY-MM-DD]
START: [HH:MM]
TOKEN-STATUS: [ausreichend]
STUFE: [S3 — S1–S5 laut MILESTONE_GATEWAY §2]
ZÄHLER: offen / erledigt / blockiert
```

---

## Hauptaufgabe (M1)

**Ziel:** [Was ist das große Ziel dieser Session?]

**DoD für M1:** [Was muss am Ende dieses Meilensteins erreicht sein? — Silo-Denken: bei mehreren
parallelen Themensträngen in dieser Session diese hier als eigene Silos führen, z.B. "SILO A:
AUDIT", "SILO B: REFACTORING" statt alles unter M1 zu vermischen.]

- [ ] **TS-01.10** `[READ-ONLY]` — [atomare Aktion, z.B. "Scanne `app/api/auth/`"]
- [ ] **TS-01.20** `[READ-ONLY]` — [atomare Aktion]
- [ ] **TS-01.30** `[WRITE]` — [atomare Aktion]
- [ ] **TS-01.40** `[TEST]` — [Verifikation]

⏸️ **STOPP 1** — Berichte Ergebnis. Zeige letzte 5 Zeilen Output. Warte auf GO.

**Model-Wechsel-Check:** Modell-Wechsel nach M1? WENN ja → STOPP für Wechsel.

---

## Meilenstein 2 (M2)

**Ziel:** [Was wird in M2 erreicht?]

**DoD für M2:** [Definition of Done — konkret und verifizierbar]

- [ ] **TS-02.10** `[WRITE]` — [atomare Aktion]
- [ ] **TS-02.20** `[WRITE]` — [atomare Aktion]
- [ ] **TS-02.30** `[VERIFY]` — [Verifikation]

⏸️ **STOPP 2** — Berichte Ergebnis. Warte auf GO.

**Model-Wechsel-Check:** Modell-Wechsel nach M2? WENN ja → STOPP für Wechsel.

---

## Meilenstein 3 (M3)

**Ziel:** [Was wird in M3 erreicht?]

**DoD für M3:** [Definition of Done — konkret und verifizierbar]

- [ ] **TS-03.10** `[TEST]` — [Verifikation]
- [ ] **TS-03.20** `[DOC]` — [Dokumentation]
- [ ] **TS-03.30** `[REPORT]` — [Session-Report schreiben]

⏸️ **STOPP 3** — Abschluss. Vorbereitung für Session-Abschluss (6 Schritte).

**Hinweis Silo-Struktur:** Bei Sessions mit mehreren klar getrennten, parallel laufenden
Themensträngen (statt einer linearen M1→M2→M3-Kette) können Meilensteine stattdessen als
**Silos** geführt werden (`SILO 01: [Name]`, `SILO 02: [Name]`, ...), jedes mit eigenem
`DoD für Silo NN`-Feld und eigener `TS-NN.xx`-Nummerierung — Format bleibt identisch zu oben,
nur die Überschrift wechselt von "Meilenstein" zu "Silo" und die Reihenfolge ist nicht zwingend
linear-abhängig.

---

## SubAgent-Orchestration

| SubAgent | Auftrag | Status | Output-Pfad |
|:---|:---|:---:|:---|
| [General Agent] | [z.B. "Bundle-Migration"] | ✅/⏳/❌ | [Pfad] |
| [Explorer] | [z.B. "Vergleiche 4 Bundles"] | ✅/⏳/❌ | [Pfad] |
| [Read-Only] | [z.B. "Zähle alle .md-Dateien"] | ✅/⏳/❌ | [Pfad] |

**Vor jedem SubAgent-Spawn:** STOPP für Modell-Wechsel (Operator-Permission).

**Nach jedem SubAgent-Report:** STOPP, Bewertung, Integration in LIVING_FILES.

---

## Blockierte Tasks

- [!] **[Task-Name]** — blockiert durch: [Grund], WORKAROUND: [Workaround]

---

## Prioritäten

- **P0 KRITISCH** — Sofort, blockiert alles andere
- **P1 HOCH** — Diese Session, wichtig
- **P2 NORMAL** — Nächste Session
- **P3 NIEDRIG** — Irgendwann
