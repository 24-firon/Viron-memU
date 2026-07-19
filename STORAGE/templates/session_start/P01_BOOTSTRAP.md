<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# P01 — Bootstrap Fragen (nach P00 Leseliste)

> **G-20-Fix — Kopfklarstellung:** Die 10 Fragen unten sind **generische BEISPIEL-Fragen** zu den
> immer-aktiven Grundregeln (Injektion, Routing, Rollen) — sie zeigen das FORMAT (Anwendung statt
> Recall). `INSTRUCTIONS.md` 6.1 verlangt vom Ersteller **3–5 NEUE, session-spezifische**
> Anwendungsfragen zum konkreten TASK der Folgesession (gut: „Was passiert wenn du X ignorierst?",
> schlecht: „Was steht in der Datei?"). Die 10 Beispiele hier NICHT unverändert 1:1 in eine
> generierte P01 kopieren — sie sind das Muster, nicht der Inhalt.
>
> **READ-ONLY.** Diese Fragen prüfen dein Verständnis des Systems.
> Du hast **eine primäre Wissensquelle** in Claude Code: was du in P00 (Leseliste) aktiv gelesen hast — ergänzt durch `CLAUDE.md` (Repo-Root, + `@`-Imports), das einzige in CC automatisch geladene Dokument.
>
> **DENN** wer die Regeln nicht durchdrungen hat, wird in der ersten Session scheitern.
> **Framework-Hinweis:** Die Fragen sind so gestaltet, dass du sie aus der P00-Leseliste + CLAUDE.md beantworten kannst. Wo das nicht reicht, lade gezielt nach.

---

## 1. WAS DU NACH P00 WEISST

### Aus der Leseliste (P00) gelesen
- **BATCH 1:** `AGENTS.md` (Repo-Identität), `RULE_REGISTRY.md` oder `.opencode/rules/` (aktive Regeln), `task.md` (Scope, DoD, Blocker)
- **BATCH 2:** `LESSONS_LEARNED.md` (Agenten-Fehler), `DECISION_LOG.md` (Architektur-Entscheidungen), letzter `HANDOVER.md` (vorheriger Session-Stand)
- **BATCH 3:** `implementation_plan.md` (Bauplan), `task.md` (Task-Liste), domain-spezifische SSoTs

### Injektions-Notiz (framework-abhängig — Ergebnis steht in P00, INSTRUCTIONS 6.0)
> Zwei Wege, wie Dateien beim Session-Start automatisch im Kontext landen (BEIDE Frameworks können das):
> - **OpenCode:** `opencode.jsonc` → `instructions`-Array injiziert das gelistete Set (~15 Rules, DOCS, LESSONS_LEARNED etc.).
> - **Claude Code:** SessionStart-Hook + `.claude/context-inject.json` injiziert das dort gelistete Set. Zusätzlich lädt `CLAUDE.md` (+ `@`-Imports) statisch auto.
>
> **Ob DIESES Repo injiziert, steht im P00-Injektions-Block — DREI mögliche Varianten (D-003, nicht
> binär): Variante A = VOLL (SessionStart-Hook/opencode.jsonc, per Checkfragen verifiziert),
> Variante C = TEILWEISE (Root-`CLAUDE.md` mit `@`-Imports lädt einen kleinen Kern automatisch, per
> Checkfragen wie A verifiziert, Rest über STORAGE-Router oder P00-Tier-1), Variante B = NEIN (P00
> aktiv lesen).** Ein Repo mit `CLAUDE.md`-`@`-Imports ist NIEMALS automatisch „Variante B" — das
> war der D-003-Fehler. Bei Variante B MÜSSEN die Dateien explizit über P00 (Tier 1) gelesen werden;
> sehr umfangreiche Sets kommen via `CLAUDE.md`-`@`-Import (Strategie „Aggregator", F9). **Nie
> annehmen „in CC gibt es keine Injektion" — das war eine überholte Pauschalannahme (D-012).**

### Was du (auch nach P00) NICHT automatisch hast
- `DESK/TASKS/active/task.md` — der aktuelle Auftrag (muss geladen werden)
- `DESK/TASKS/active/implementation_plan.md` — der Bauplan (muss geladen werden)
- `.opencode/skills/` — werden bei Bedarf via `skill()` geladen
- `IMPORT/` — Postbox für neues Wissen (on-demand)
- `STORAGE/` — Payload-Wissen (on-demand)

---

## 2. DIE 10 FRAGEN (testen ANWENDUNG, nicht RECALL)

Die folgenden Fragen testen ob du das System verstanden hast. Du kannst sie aus ALLEN verfügbaren Quellen beantworten:
- **aus P00** (Leseliste — was du aktiv gelesen hast)
- **aus CLAUDE.md** (Repo-Root, + `@`-Imports — einzige Auto-Injection in Claude Code)
- **aus dem Skill selbst** (SKILL.md + INSTRUCTIONS.md)

### 1. Injektions-Mechanismus
Du hast Dateien die automatisch da sind (DOCS) und Dateien die du laden musst (STORAGE, SKILLS). Was passiert, wenn du eine DOCS-Datei behandelst als müsstest du sie mit `read` laden? Was ist die Konsequenz?

### 2. Thin Triggers & Rule-Fatigue
Eine Boot-Regel in `.opencode/rules/` ist 200 Zeilen lang. Was ist die konkrete Konsequenz? Warum ist das schlimmer als eine Regel mit 5-15 Zeilen?

### 3. 10er-Routing
Du findest eine Regel mit dem Präfix `12_`. Was ist das Problem? Wie lautet die korrekte Konvention (00, 10, 20...)?

### 4. DENN-Z Gesetz
Formuliere eine kurze Regel im DENN-Z-Format: "Mache X, um Y zu erreichen, DENN Z." Warum ist Sog (DENN-Z) besser als Push (kein DENN)?

### 5. Local Override
Globale Skill-Regel erlaubt etwas, `.opencode/rules/` verbietet es. Welche Regel gilt? Was passiert wenn du die globale nimmst?

### 6. Dispatcher Role Isolation
Eine Regel sagt: "Deploye niemals ohne Operator-Approval." Bist du als aktueller Agent daran gebunden, oder gilt das nur für Sub-Agents? Warum?

### 7. Skill-Routing (50-Zeilen-Regel)
Ein Skill hat 579 Zeilen. Was liest du zuerst (YAML-Header + wie viele Zeilen)? Was passiert wenn du stattdessen blind von Zeile 1 bis 600 liest?

### 8. Engineering Standard & Branches
Ein Python-Skript soll 100 Archiv-Dateien verarbeiten. Darfst du das in `src/` auf einem Branch tun, oder muss das in PLAYGROUND/ entwickelt werden? Was sind die Bedingungen?

### 9. Sub-Agent-Briefing (4 Säulen)
Du spawnst einen Sub-Agent für eine schreibende Aufgabe. Welche 4 Säulen MUSS dein Briefing enthalten? Was passiert, wenn du nur die Mission schickst?

### 10. Comprehension Gate
Du hast P00 gelesen, P01 beantwortet. Was ist der nächste Schritt? Welche 3 Dinge musst du vor dem ersten Edit tun? Wann darfst du EDITS machen?

---

## 3. CLAUDE-MD-CHECK (Claude Code — Standard)

**Claude Code lädt `CLAUDE.md` statisch automatisch** (Repo-Root + verschachtelte CLAUDE.md, transitiv via `@`-Imports). Zusätzlich kann ein **SessionStart-Hook** (`.claude/context-inject.json`) ein weiteres Datei-Set injizieren — ob dieses Repo das tut, steht im P00-Injektions-Block (6.0). Alles, was weder statisch geladen noch injiziert ist, MUSS aktiv gelesen werden.

**Vorgehen:**
1. **Existiert** `CLAUDE.md` im Repo-Root? (`Test-Path CLAUDE.md` oder `ls`)
2. **Lies** sie — notiere, welche `@pfad`-Imports sie zieht.
3. **Lies** die direkt importierten Dateien (typisch 5–10 universelle Kern-Regeln).
4. **Vergleiche** mit der P00-Leseliste: sind alle dort als Tier-1 markierten Dateien entweder gelesen ODER über CLAUDE.md auto-geladen?
5. **Wenn Lücke:** Lade die fehlende Tier-1-Datei SOFORT mit `read` und melde dem User: „CLAUDE.md + @-Imports decken [X] Dateien. [Y] Tier-1-Dateien aus P00 fehlten und wurden nachgeladen."

**BEWEIS:** „CLAUDE.md + @-Imports gelesen: [X] Dateien automatisch. P00 Tier-1 vollständig: [Y] Dateien aktiv gelesen. [Z] Lücken nachgeladen."

**OpenCode-Variante:** In einem OpenCode-Setup übernimmt `opencode.jsonc` mit `instructions`-Array die Rolle der Injektion — prüfe analog. In Claude Code ist das Pendant der SessionStart-Hook + `.claude/context-inject.json` (siehe 6.0/P00-Injektions-Block); beide Frameworks werden unterstützt.

---

## 4. BESTÄTIGUNG

> „P01 bestanden. 10/10 Fragen beantwortet. Wissen aus [P00 Leseliste] + [CLAUDE.md] verarbeitet. Bereit für P02_SESSION_INIT."

⏸️ **STOPP** — Warte auf GO vom Operator. Stufe für den nächsten Schritt (P02): S4–S5.

---

## ANHANG: Prüfe deine Quellen

| Frage | Kann aus P00 kommen | Kann aus CLAUDE.md kommen |
|:---|:---:|:---:|
| 1. Injektions-Mechanismus | ✅ LESSONS_LEARNED | ✅ DOCS/Regeln |
| 2. Thin Triggers | ✅ LESSONS_LEARNED | ✅ .opencode/rules/ |
| 3. 10er-Routing | ✅ LESSONS_LEARNED | ✅ Rule-Numbering-Konzept |
| 4. DENN-Z Gesetz | ✅ DECISION_LOG.md | ✅ Omega Constitution |
| 5. Local Override | ✅ LESSONS_LEARNED | ✅ Local-Rule-Priority |
| 6. Dispatcher Role | ✅ LESSONS_LEARNED | ✅ ADR-004 |
| 7. Skill-Routing | ✅ LESSONS_LEARNED | ✅ Skill-Philosophy |
| 8. Engineering Standard | ✅ Lessons/Standards | ✅ Engineering-Standard-Rule |
| 9. Sub-Agent-Briefing | ✅ Beispiel-Templates | ✅ Orchestration-Rule |
| 10. Comprehension Gate | ✅ P02_SESSION_INIT | ✅ P02_SESSION_INIT |
