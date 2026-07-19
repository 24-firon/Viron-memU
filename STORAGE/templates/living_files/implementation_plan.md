<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht:**
>
> - Linearer Bauplan mit Meilensteinen (M1/M2/M3)
> - SubAgent-Orchestration (welche Agents für welche Schritte)
> - Stufen-Wahl pro Phase (S1–S5, MILESTONE_GATEWAY §2)
> - Abbruch-Bedingungen und Verifikations-Plan
>
> - **Wann pflegen:** Bei Status-Änderung pro Meilenstein
> - **Bundle-Verwendung:** Diese Datei wird nach `WORKSPACE/<session>/desk/` kopiert. Sie ist ein TEMPLATE zum Ausfüllen.
<!-- TEMPLATE-EXPLANATION-END -->

# implementation_plan.md — Template für linearen Session-Plan

> **Zweck:** Linearer Bauplan mit Meilensteinen, SubAgent-Zuweisung, Model-Wahl.
> **Wann pflegen:** Bei Status-Änderung pro Meilenstein.

---

## Kopfzeile

```
TASK-ID: [z.B. MIGRATE_01]
PHASE: [z.B. Phase A → B]
RISIKO: [Low / Medium / High]
GESCHÄTZTE DAUER: [z.B. ~30 Min]
SUBAGENTS-EINGESETZT: [Anzahl + Typen]
```

---

## M1: [Titel der ersten Phase]

**Ziel:** [Was ist erreicht wenn M1 fertig ist?]

### Schritte
- [ ] **Schritt 1.1** `[READ-ONLY]` — [konkrete Aktion]
- [ ] **Schritt 1.2** `[WRITE]` — [konkrete Aktion]
- [ ] **Schritt 1.3** `[TEST]` — [Verifikation]

### SubAgent-Orchestration
- WENN Schritt X zu groß → SubAgent spawnen (General Agent)
- TASK_ENVELOPE: 4-Säulen (Mission/Context/Scope/Schritte)
- STOPP vor SubAgent-Spawn für Stufenwechsel

### Stufen-Wahl (S1–S5, MILESTONE_GATEWAY §2)
- Planung: S4–S5
- Ausführung: S3
- Verifikation/Recherche: S1–S2
- Kritischer Schnitt (Formulierung/Code): S5 (§2b)
- Bei jedem Wechsel: STOPP

### DoD (Definition of Done)
- [Was muss erreicht sein damit M1 als fertig gilt?]

⏸️ **STOPP 1** — Berichte Ergebnis. Zeige letzte 5 Zeilen Output. Warte auf GO.

---

## M2: [Titel der zweiten Phase]

**Ziel:** [Was ist erreicht wenn M2 fertig ist?]

### Schritte
- [ ] **Schritt 2.1** `[WRITE]` — [konkrete Aktion]
- [ ] **Schritt 2.2** `[WRITE]` — [konkrete Aktion]
- [ ] **Schritt 2.3** `[VERIFY]` — [Verifikation]

### SubAgent-Orchestration
- [Welche SubAgents? Welche Aufträge?]

### Model-Wahl
- [Welche Modelle pro Schritt?]

### DoD
- [Was muss erreicht sein?]

⏸️ **STOPP 2** — Berichte Ergebnis. Warte auf GO.

---

## M3: [Titel der dritten Phase]

**Ziel:** [Was ist erreicht wenn M3 fertig ist?]

### Schritte
- [ ] **Schritt 3.1** `[TEST]` — [z.B. End-to-End-Smoke-Test]
- [ ] **Schritt 3.2** `[COMMIT]` — [z.B. Git commit mit conventional commit message]
- [ ] **Schritt 3.3** `[REPORT]` — [z.B. Session-Report schreiben]

### SubAgent-Orchestration
- [Welche SubAgents?]

### Model-Wahl
- [Welche Modelle?]

### DoD
- [Was muss erreicht sein?]

⏸️ **STOPP 3** — Abschluss. Vorbereitung für Session-Abschluss (6 Schritte).

---

## SubAgent-Prompts-Vorbereitung

**Falls SubAgent benötigt wird, vorbereiten:**
- [ ] TASK_ENVELOPE für [SubAgent-Auftrag 1] erstellt
- [ ] TASK_ENVELOPE für [SubAgent-Auftrag 2] erstellt
- [ ] Templates bereitgestellt: [Welche?]
- [ ] Kontextdateien geladen: [Welche?]

---

## Templates-Zuweisung

| Schritt | Template-Datei | Pfad |
|:---|:---|:---|
| Schritt X | P02_SESSION_INIT.md | `templates/P02_SESSION_INIT.md` |
| Schritt Y | REPORT_GENERATOR.md | `IMPORT/extraction_prompts/FORENSIC_REPORT_GENERATOR.md` (Repo-Root, D-005.6) |

---

## Kontextdateien-Zuweisung

| Schritt | Kontextdatei | Pfad |
|:---|:---|:---|
| Schritt X | AGENTS.md | `[REPO-ROOT]/AGENTS.md` |
| Schritt Y | README.md | `[REPO-ROOT]/README.md` |

---

## Abbruch-Bedingungen

Stopp SOFORT und Operator informieren wenn:
- Mehr als [X] Dateien betroffen sind als geplant
- Eine externe Abhängigkeit (API, Service) nicht erreichbar
- Konflikt mit existierender Architektur erkannt
- Mehr als [X] STOPPs ohne klares Ergebnis durchlaufen

---

## Verifikations-Plan

Pro Meilenstein definieren:
- [Was] wird verifiziert
- [Wie] (z.B. "ls zeigt Datei", "grep findet 0 Treffer")
- [Wer] ist verantwortlich (Agent vs. Operator)
