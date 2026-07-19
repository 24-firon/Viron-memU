<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# 🗺️ IMPLEMENTATION PLAN (Vollständig): [PROJEKT-NAME]

> **System Architecture:** [Kernsystem Version]
> **Current Phase:** [Phase A → Phase B Transition]
> **Infrastructure Target:** [Ziel-Umgebung / Cloud / Bare-Metal]
> **Status:** 🛠️ ACTIVE DEVELOPMENT (Session Hand-Off State)
>
> **Atomarer Plan** mit Meilensteinen. Jeder Schritt ist ein konkreter Tool-Call.
> Jeder STOPP enthält den **GATEWAY-Block** (`references/MILESTONE_GATEWAY.md` §3 — normatives
> Ansage-Format, keine eigene Zählweise) + LIVING_FILES-Pflicht + Commit-Überlegung.
> **DENN** ohne atomare Schritte + erzwungene Reflexion springt der Agent zu komplexen Aktionen.
>
> **Plan-Träger (D-005, 2026-07-11):** Diese Datei (als Living File `desk/implementation_plan.md`)
> ist der EINZIGE Ort des Meilenstein-Plans — die P02 verweist nur hierher (Teil 4 Plan-Verweis),
> sie enthält selbst KEINEN Plan. O-Ton Operator: „P02 hat keinen Implementation Plan. Der
> Implementation Plan ist das, was geplant ist, und Walkthrough ist das, was wirklich passiert
> ist." Sie hält also das GEPLANTE fest; die real durchgeführte Version dokumentiert
> `desk/walkthrough.md` (+ ggf. `desk/walkthrough/M<N>_<name>.md`, G-25).

---

## 1. STRATEGIC OBJECTIVE & ARCHITECTURAL SHIFT
[Kurze Beschreibung des Architektur-Shifts — was war das Problem, was ist die Lösung]

### Core Target Metrics:
*   **Context Window Optimization:** [Quantifiziertes Ziel — z.B. Token-Reduktion in %]
*   **Tenant Isolation:** [Mandantentrennung — welche Mechanismen]
*   **Gateway Reliability:** [API-Gateway — welche Absicherungen]

### 1.1 MODELL-ROTATION (Eisenhart)

> 🛑 **HARTER STOPP bei JEDEM Stufenwechsel.** Operator-Permission zwingend.
> Stufen S1–S5 (Charakter) × Intensität (Low gesperrt / Medium / High / Extra-Max) — Norm:
> `references/MILESTONE_GATEWAY.md` §2. **Kritischer Schnitt (Formulierung/Code/Architektur) = S5**
> (Chirurg-Doktrin §2b).

| Phase | Stufe | Zweck | Stopp-Pflicht |
|:---|:---|:---|:---|
| **Comprehension** | S4 | Verstehen, Verständnisfragen | Ja — bei jedem Schritt |
| **Planung** | S4–S5 | Meilensteine definieren, DoD | Ja — vor jedem M-Wechsel |
| **Schritt-Ausführung** | S3 | Befehle, Edits, Tool-Calls | Ja — bei jedem Stufenwechsel |
| **Recherche** | S1–S2 | Nur lesen, viele Dateien iterieren | Ja — bei jedem Stufenwechsel |
| **Reviews** | S3–S4 | Code-Review, Validierung, Skill-Scan | Ja — bei jedem Stufenwechsel |
| **Forensik / kritischer Schnitt** | S4–S5 | 9-Sektionen-Reports, tiefe Analyse, finale Formulierung | Ja — bei jedem Stufenwechsel |

**Regel:** Niemals alles auf derselben Stufe. Rotation ist Pflicht (planen → delegieren → orchestrieren).

### 1.2 AGENTEN-BRIEFING (SubAgent-Spawn — 4 Säulen)

> 🛑 **STOPP vor jedem SubAgent-Spawn.** Operator-Permission + Briefing schreiben.

| Säule | Frage | Beispiel |
|:---|:---|:---|
| **MISSION** | Was soll der SubAgent konkret tun? | "Scanne `C:\Workspace\Repos\...\.graphify\`" |
| **KONTEXT** | Welche Dateien muss er lesen? | `STORAGE/learnings/*.md`, `decision_log.md` |
| **OUTPUT** | Was muss er liefern? Format, Pfad | `DESK/reports/graphify-report.md`, Markdown |
| **STOPP** | Wann meldet er zurück? | "Bei 100% Scan oder 5 Min Timeout" |

**Regel:** Ohne 4-Säulen-Briefing kein SubAgent-Spawn. Der SubAgent bekommt das Briefing im Auftrag-Prompt.

---

## 2. HARD SYSTEM STATE & PRE-REQUISITES
Bevor der nächste Agent operativen Code anfasst, MÜSSEN folgende Systemzustände verifiziert sein:
1.  **Environment Variables:** [Welche Env-Vars müssen gesetzt sein]
2.  **Package Manager:** [Welcher PM in welcher Version — keine Leichen]
3.  **Local Services:** [Welche lokalen Services müssen laufen]

---

## 3. MILESTONE MATRIX & DEPENDENCY GRAPH

```

[M1: Audit & Discovery] ──> [M2: Refactoring Layer] ──> [M3: Schema/Type Enforcement]
│
└──> [M4: E2E Verification]

```

| Milestone ID | Definition of Done (DoD) | Target Path | Risk Level |
| :--- | :--- | :--- | :--- |
| **M1: Audit** | [Was ist das Audit-Ergebnis?] | `[Pfad/Context-Map]` | 🟢 Low |
| **M2: Refactor** | [Was ist der Refactor-Erfolg?] | `[Pfad/Components]` | 🟡 Medium |
| **M3: Gateway** | [Was ist der Gateway-Erfolg?] | `[Pfad/API-Routes]` | 🔴 High |
| **M4: Deploy** | [Was ist der Deploy-Erfolg?] | `[Pfad/Config]` | 🟡 Medium |

---

## 4. LINEAR RUNBOOK & EXECUTION STEPS (Atomar pro Meilenstein)

> **Jeder Meilenstein** hat Ziel, Modell-Rotation, SubAgent, atomare Schritte, GATEWAY-Block (§3-Ansage-Format), LIVING_FILES-Pflicht, Commit-Überlegung, DoD.
>
> **Living-Files-Pflicht = Pflicht-Kern** (`task.md`, `walkthrough.md`, `decision_log.md` in `desk/`) + situative Dateien, falls angelegt (siehe die CLAUDE.md im Root des aktuellen Arbeits-Repos, Abschnitt 6.3, bzw. `STRUKTUR_WISSENSBASIS.md` §5, falls keine Repo-CLAUDE.md existiert). `HANDOVER.md` ist ein `handover/`-Artefakt — es wird NICHT pro Meilenstein gepflegt, sondern erst in Schritt 7 geschrieben (HD-5: HANDOVER.md immer zuletzt). Der Fahrplan der Folgesession ist `task.md` selbst (keine separate `CURRENT_TASKLIST.md` mehr).

### MEILENSTEIN 0: Session-Start-Mechanik (Buchhaltung + STEP_1A + Checkpoint) — **S1–S2 oder SKRIPT**

> **⚠️ ANTI-FARCE-GATE (MILESTONE_GATEWAY §2c) — NICHT AUF DER PLANUNGS-STUFE:** Das hier ist reine
> Mechanik (INDEX-Zeile umstellen, Vorgänger-Living-Files `cp`, Checkpoint-Commit). Nach der
> Plan-Freigabe NICHT einfach auf S4/S5 weiterrutschen und Dateien kopieren — **erst Stufe senken
> (S1–S2) oder ein Skript feuern.** Der Chirurg wischt nicht den Boden.

**Schritte (deterministisch → idealerweise EIN Skript):**
- [ ] **0.1** eigene `WORKSPACE/INDEX.md`-Zeile `geplant`→`aktiv` (edit) + Header `desk/task.md` füllen
- [ ] **0.2** STEP_1A: Vorgänger-Living-Files als `_predecessor_*` in die eigene `desk/` kopieren (`cp`, nie `mv`) — inkl. Nicht-Standard-Artefakte (Backlog-8)
- [ ] **0.3** Checkpoint-Commit (Rollback-Anker vor M1)

#### ⏸️ GATEWAY M0 — Start-Mechanik erledigt
```
⏸️ GATEWAY M0 — Start-Mechanik erledigt
✅ FERTIG:   [Buchhaltung + _predecessor_-Kopien + Checkpoint] — Beweis: [cmp/ls/Commit]
▶️ JETZT:    M1 [erste inhaltliche Phase]
🎚️ STUFE:    [S für M1 laut Matrix §4]·[Intensität]
🤖 WIE:      [SELBST / SKRIPT / SUBAGENT]
❓ OFFEN:    [oder „keine"]
──────────────────────────────
👉 DU: [Stufe für M1 im Klartext, dann GO]
```

⏸️ **STOPP 0** — M0 ist Mechanik: **auf S1–S2 wechseln oder als Skript ausführen**, DANN GO.

---

### MEILENSTEIN 1: [Titel — konkret, kurz]

**Ziel:** [1 Satz: was ist erreicht wenn M1 fertig]

**Stufe:** [S1–S5]·[Intensität] — [Begründung laut MILESTONE_GATEWAY §4]

**SubAgent:** [JA — Art / NEIN — Begründung]

#### Schritte (atomar)
- [ ] **Step 1.1** `[TOOL]` — [konkrete Aktion mit Befehl oder Tool-Call, kein "und dann..."]
- [ ] **Step 1.2** `[TOOL]` — [atomare Aktion, ein Schritt = ein Tool-Call]
- [ ] **Step 1.3** `[VERIFY]` — [was genau prüft ob es funktioniert hat]

#### ⏸️ GATEWAY M1 — [2–4-Wort-Titel]

Pflichtformat, wörtlich aus `references/MILESTONE_GATEWAY.md` §3 (die einzige normative
Gateway-Quelle — dieses Template darf davon nicht abweichen):

```
⏸️ GATEWAY M1 — [Titel]
✅ FERTIG:   [Status: was ist passiert, Soll vs. Ist, vollständig vs. teilweise] — Beweis: [Evidence: letzte 3-5 Zeilen Output, Datei-Pfade mit Zeilenzahlen, Git-Diff]
▶️ JETZT:    [was als Nächstes passiert]
🎚️ STUFE:    S<X>·<Intensität> — [Begründung laut MILESTONE_GATEWAY §4]
🤖 WIE:      [SELBST / SKRIPT (1 Lauf) / SUBAGENT S<X>×N, disjunkt]
❓ OFFEN:    [Offene Punkte + Operator-Entscheidung(en) + Risiken/Blocker/Dependencies — oder „keine"]
──────────────────────────────
👉 DU: [genau EINE Handlung — Stufe/Modell im Klartext, dann was]
```

#### LIVING_FILES (PFLICHT vor STOPP-Auflösung — Pflicht-Kern)
- [ ] `task.md` — Erledigte Tasks abhaken, neue hinzufügen
- [ ] `walkthrough.md` — Meilenstein-Eintrag (Datum, Was gemacht, Geändert, Entscheidungen, Verifikation)
- [ ] `decision_log.md` — Neue Entscheidungen dokumentieren (ID, Wert, Reversibel, Begründung)

#### Situativ (falls angelegt)
- [ ] `implementation_plan.md` — Status aktualisieren (✅/⏳/❌)
- [ ] `lessons_learned.md` — Neue Lernpunkte eintragen (Was sich als falsch erwiesen hat, was bestätigt wurde)

#### Commit-Überlegung
- [ ] Ist ein Git-Commit sinnvoll? → `git add` + `git commit -m "beschreibende Message"`
- [ ] Wenn nein: dokumentiere warum (z.B. "nur UI-Konfiguration, kein Repo-Commit nötig")

#### Model/SubAgent-Check
- [ ] Modell-Wechsel nötig? → HARTER STOPP, Operator-Permission
- [ ] SubAgent spawnen? → STOPP, Briefing vorbereiten (4 Säulen aus §1.2)
- [ ] Umplanung nötig? → STOPP, neuen Plan schreiben

**DoD (Definition of Done):**
- [ ] [Konkretes Kriterium 1 — verifizierbar]
- [ ] [Konkretes Kriterium 2 — verifizierbar]
- [ ] [Konkretes Kriterium 3 — verifizierbar]

---

### MEILENSTEIN 2: [Titel — konkret, kurz]

**Ziel:** [1 Satz]

**Stufe:** [S1–S5]·[Intensität] — [Begründung]

**SubAgent:** [JA/NEIN]

#### Schritte (atomar)
- [ ] **Step 2.1** `[TOOL]` — [atomare Aktion]
- [ ] **Step 2.2** `[TOOL]` — [atomare Aktion]
- [ ] **Step 2.3** `[VERIFY]` — [Verifikation]

#### ⏸️ GATEWAY M2 — [2–4-Wort-Titel]
[gleiches Format wie GATEWAY M1 — MILESTONE_GATEWAY §3]

#### LIVING_FILES (PFLICHT — Pflicht-Kern)
- [ ] `task.md` — Update
- [ ] `walkthrough.md` — Eintrag
- [ ] `decision_log.md`

#### Situativ (falls angelegt)
- [ ] `implementation_plan.md` — Status
- [ ] `lessons_learned.md`

#### Commit-Überlegung
- [ ] Ja/Nein + Begründung

#### Model/SubAgent-Check
- [ ] Wechsel? Spawn? Umplanung?

**DoD:**
- [ ] [Kriterium 1]
- [ ] [Kriterium 2]

---

### MEILENSTEIN 3: [Titel — konkret, kurz]

**Ziel:** [1 Satz]

**Stufe:** [S1–S5]·[Intensität] — [Begründung]

**SubAgent:** [JA/NEIN]

#### Schritte (atomar)
- [ ] **Step 3.1** `[TOOL]` — [atomare Aktion]
- [ ] **Step 3.2** `[TOOL]` — [atomare Aktion]
- [ ] **Step 3.3** `[TEST]` — [Test- oder Verifikations-Aktion]

#### ⏸️ GATEWAY M3 — [2–4-Wort-Titel]
[gleiches Format wie GATEWAY M1 — MILESTONE_GATEWAY §3]

#### LIVING_FILES (PFLICHT — Pflicht-Kern)
- [ ] `task.md` — Update
- [ ] `walkthrough.md` — Eintrag
- [ ] `decision_log.md`

#### Situativ (falls angelegt)
- [ ] `implementation_plan.md` — Status
- [ ] `lessons_learned.md`

#### Commit-Überlegung
- [ ] Ja/Nein + Begründung

#### Model/SubAgent-Check
- [ ] Wechsel? Spawn? Umplanung?

**DoD:**
- [ ] [Kriterium 1]
- [ ] [Kriterium 2]

---

## 5. STOPP-TABELLE (Zusammenfassung aller Gateway-Checklisten)

> **Jeder STOPP pflegt den Living-Files-Pflicht-Kern** (`task.md`, `walkthrough.md`, `decision_log.md` in `desk/`) + situative Living Files, falls angelegt, + Commit-Überlegung + Stufen-/SubAgent-Check. `HANDOVER.md` ist ein `handover/`-Artefakt (Schritt 7), NICHT pro Meilenstein-STOPP (Pflicht-Kern-Regel: siehe die CLAUDE.md dieses Repos, Abschnitt 6.3, bzw. `STRUKTUR_WISSENSBASIS.md` §5, falls keine Repo-CLAUDE.md existiert). Ohne diese Pflicht-Checkliste ist der STOPP ungültig.

| STOPP | Wann | Pflicht-Kern (desk/) | Situativ (falls angelegt) | Commit | Stufen-Check | SubAgent-Check |
|:---|:---|:---|:---|:---|:---|:---|
| 1 | M1 done | `task.md`, `walkthrough.md`, `decision_log.md` | `lessons_learned.md`, `ideas_future_plans.md`, `implementation_plan.md` | Nein/optional | S1→S4 bei Wechsel | Briefing nötig? |
| 2 | M2 done | Pflicht-Kern fortschreiben | + ggf. weitere | JA | — | — |
| 3 | M3 done | Pflicht-Kern fortschreiben | + Abschluss-Erkenntnisse | JA | S3 | — |
| 4+ | M4+ | Pflicht-Kern fortschreiben | + neue | Variabel | Variabel | Variabel |

**Goldene Regel:** Kein STOPP ohne Pflicht-Kern-Update. Kein STOPP ohne GATEWAY-Block (§3-Ansage-Format, `references/MILESTONE_GATEWAY.md`). Kein STOPP ohne Commit-Überlegung. Kein STOPP ohne Model/SubAgent-Check.

## 6. ABBRUCH-BEDINGUNGEN

Stopp SOFORT und Operator informieren wenn:

- [Mehr als X Dateien betroffen als ursprünglich geplant]
- [Eine externe Abhängigkeit (API, Service, Repo) ist nicht erreichbar]
- [Konflikt mit existierender Architektur erkannt — Risiko für Live-System]
- [Mehr als X STOPPs ohne klares Ergebnis durchlaufen — Agent dreht sich im Kreis]
- [SubAgent ohne 4-Säulen-Briefing gestartet — Verstoß gegen Spawn-Regel]
- [Commit ohne vorherige Verifikation der Änderungen — ungeprüfter Code in Repo]
- [Modell-Wechsel ohne Operator-Permission — Verstoß gegen Rotation-Pflicht]

## 7. OFFENE FRAGEN (vor Session-Start klären)

| # | Frage | Wer entscheidet | Klärung vor |
|:---|:---|:---|:---|
| 1 | [Frage, z.B. "Welche Routing-Strategie: least-busy oder x-litellm-tags?"] | [Operator / Agent / SubAgent] | M1 / M2 / M3 |
| 2 | [Frage] | [Entscheider] | [Zeitpunkt] |
| 3 | [Frage] | [Entscheider] | [Zeitpunkt] |
| 4 | [Frage] | [Entscheider] | [Zeitpunkt] |
