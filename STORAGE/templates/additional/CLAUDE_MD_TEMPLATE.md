<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# CLAUDE.md — Reference Template (Auto-Load-Anker)

> **Zweck:** Reference-Vorlage für `CLAUDE.md` in Ziel-Repos, die mit `session_handover_generator` arbeiten.
>
> **Strategie „Aggregator" (F9):** In Claude Code ist `CLAUDE.md` die einzige **statisch** auto-geladene Datei (Repo-Root + verschachtelte CLAUDE.md, transitiv via `@`-Imports). Davon zu unterscheiden ist die optionale **Session-Start-Injektion** (SessionStart-Hook + `.claude/context-inject.json`, INSTRUCTIONS 6.0) — falls das Repo sie hat, wird zusätzlich ein Datei-Set beim Start injiziert. Diese Vorlage ersetzt den kritischen Kern des ehemaligen `opencode.jsonc` → `instructions`-Arrays.
>
> **NICHT alle ~140 Dateien `@`-importieren → Token-Explosion.** Realistisch 5–10 konsolidierte Kern-Dateien. Der Rest bleibt auf der P00-Leseliste (on-demand).
>
> **Platzierung:** Diese Datei ist ein **Template**. In Ziel-Repos (Viron-Admin, Viron-agency-stack, …) wird sie als `CLAUDE.md` ins Root gelegt. NICHT hier im Skill — sie gehört in die ausrollenden Repos.

---

```markdown
# CLAUDE.md — [Repo-Name]

> Auto-geladen in Claude Code (statischer Anker). Ersetzt `opencode.jsonc` → `instructions`. Konsolidierter Kern.
> **DENN** sonst ist nur eine etwaige Session-Start-Injektion automatisch da (falls das Repo einen SessionStart-Hook hat, INSTRUCTIONS 6.0) — alles Weitere kommt über die P00-Leseliste.

## @-Imports (5–10 universelle Kern-Dateien)

<!-- Wähle die 5–10 WIRKLICH kritischen, universellen Regeln. Beispiele: -->
- @AGENTS.md
- @.opencode/rules/00_omega_constitution.md
- @.opencode/rules/10_conduct.md
- @.opencode/rules/30_discipline_of_knowledge_capture.md
- @.opencode/rules/80_skill_philosophy_and_workflow.md
- @DOCS/LESSONS_LEARNED.md
- @DOCS/REPO_ORIENTATION.md
- @DOCS/architecture/decisions/DECISION_LOG.md

> **Heuristik:** Was MUSS ein Agent in den ersten 5 Minuten verstanden haben, um nicht zu halluzinieren? Diese ~5–10 Dateien. Alles andere: P00-Leseliste.

## Was du NICHT automatisch hast

- `DESK/TASKS/active/task.md` — der aktuelle Auftrag (muss via P00 gelesen werden)
- `DESK/TASKS/active/implementation_plan.md` — der Bauplan
- `STORAGE/` — Payload-Wissen (on-demand)
- `IMPORT/` — Postbox für neues Wissen
- `.opencode/skills/` — werden via `skill()` geladen

## Subagenten

- Subagenten starten **kalt** (kein Vor-Kontext, kein CLAUDE.md). Briefing muss vollständig sein.
- **NICHT** `Explore`/`Plan` für handover-kritisches Lesen (überspringen CLAUDE.md und Git-Status).
- Stufe pro Subagent (S1–S5, MILESTONE_GATEWAY §2); technisch pro Subagent im Frontmatter-Feld `model:` wählbar (Mechanik — Stufe→Modell mappt der Operator, keine Namens-Defaults im Skill).
- Im Main: `/model` für Wechsel.

## STOPP-Signale

- `?????` — Operator-Pause, sofortige Antwort
- `STOPP` — halten, berichten
- `GO` — weiter
```

---

**Verwendung:** Diese Datei im Skill dient nur als Vorlage. Das eigentliche `CLAUDE.md` muss pro Repo erstellt werden, mit den **konkreten** Kern-Dateien dieses Repos.
