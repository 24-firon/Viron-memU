# SESSION PROTOCOL (ACTIONS LOG)

## Session: 2026-02-05

### 📝 Executed Actions

1.  **Mission Core Cleanup**: Removed duplicate Section 7 (Lines 150-172).
2.  **Rule Move**: Moved "Meta-Rule" from `PROJECT_RULES.md` to `gemini.md` (Rule 13).
3.  **Decision Log Mandate**: Added Rule 14 to `gemini.md`.
4.  **File Renaming**: Renamed `memu-factory.py` to `memu_factory.py`.
5.  **Artifact Creation**: Created `session_failures.md` for error tracking.

### ❌ Failed Attempts

1.  **Mission Core Update**: Failed ~15 times to update Section 7 text (Loop vs Cron).
2.  **Infrastructure**: Failed to verify DB/vLLM (Network Isolation).
3.  **Rule 11 Update**: Failed to update "Push Protocol" to include Commits (Tool Error).

### 🔍 Result

- **Status:** ✅ **SUCCESS** (Native Phase 1 Active).
- **Outcome:** Rules standardized, Backup secured, Loop running.

## Session: 2026-02-05 (Part 2)

### 🛠️ Task: Docker Infrastructure Diagnosis

- **Goal:** Fix "Connection Refused" between Agent and Docker.
- **Hypothesis:** WSL2 Networking / Named Pipe issue.
- **Context:** User plans Windows Reinstall (System Instability).
- **Status:** Connectivity Tests passed (Network OK, Application Layer blocked).
- **Action:** Docs updated (MISSION_CORE.md fixed: Hybrid RAG + Prompts).
- **State:** Moving to Phase 2. Docker Containers successfully created/recreated.
- **Status:** All services (Postgres, vLLM, WebUI) are UP. Phase 2 Infrastructure Live.
- **Action:** Ready for functional testing and conceptual changes.

## Session: 2026-07-19 — Kanon-Etablierung v1.2 (CDS PILOT-ROLLOUT_18)

### Executed Actions

1.  **Reversibilitaets-Sicherung**: 211 zuvor untracked Dateien committet (`b6a0f2f`) — STORAGE/, IMPORT/, toolkits/, .graphify/, data/, "ANDERER WIN NUTZER"/, 4x .claude-Backups.
2.  **Zonen-Rename**: `docs/` -> `DOCS/` per git mv, Upstream-Inhalt erhalten (`1068ec9`).
3.  **Stufe 2 — Templates**: 41 Dateien verteilt (Start-Prompts nach WORKSPACE/handover/, GIT_BASELINE + RECOVERY_PROTOCOL nach Root, 5 Template-Kategorien nach STORAGE/templates/), 0 Kollisionen (`45546e0`).
4.  **Stufe 2b — Tier-1-Regelset v1.2**: 18 Dateien in .claude/rules/ssot/ (5 neu, 12 Verdikt "uebernehmen", Manifest). Alt-Bestand nach ARCHIVE/ssot-Altbestand-vor-Kanon-v1.2_2026-07-19/ (`6ed8192`). Account-Fix 24-viron -> 24-firon.
5.  **SEEDED-Geruest**: WORKSPACE/INDEX.md (Board), DOCS/INDEX.md (Router), DOCS/FOLDER_MAP.md, Master-Trio, DOCS/STRUKTUR_MANIFEST.md, Aufraeum-Task T-01.

### Bewusst NICHT angefasst

- 3 VAS-Altlast-Regeln in ssot/ (Aufraeum-Task T-01/A), pgdata/, memU-multi-provider-v1.0.zip, src/memu/embedding/backends/google.py (WIP), .agent/ + .agents/ (fremde Frameworks).
