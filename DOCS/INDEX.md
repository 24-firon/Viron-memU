<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# DOCS/INDEX.md — Router (Aktuell aktiv + Trigger-Tabelle)

> **Zweck:** Die „lokale Router"-Funktion: Was ist gerade aktiv, und bei welchem Trigger lade
> ich welche Payload? DOCS-Dateien ZEIGEN nur (Pfade), sie kopieren keine Inhalte (Anti-Drift).

## Aktuell aktiv

- **Kanon-Stand:** v1.2, etabliert 2026-07-19 (CDS-Session PILOT-ROLLOUT_18) — Details:
  `DOCS/STRUKTUR_MANIFEST.md`
- **Aktive Arbeit:** siehe `WORKSPACE/INDEX.md` (Status-Board) + `DESK/TASKS/00_Master_Task_State.md`
- **Offene Aufräum-Punkte nach Rollout:** `DESK/TASKS/active/AUFRAEUMEN-NACH-ROLLOUT_2026-07-19_Task.md`

## Trigger-Tabelle (Situation → lade)

| Trigger / Situation | dann lade |
|:--|:--|
| Session-Start / -Übernahme | `WORKSPACE/handover/SESSION_START_PROMPT.md` bzw. `SESSION_OVERTAKE_PROMPT.md` |
| Living Files anlegen (M0) | `STORAGE/templates/living_files/` |
| Session-Ende / Report | `STORAGE/templates/reports/` + `STORAGE/templates/session_start/HANDOVER.md` |
| Git-Sicherheits-/Reversibilitäts-Frage | `GIT_BASELINE.md` (Root) |
| Eigener Fehler passiert — wie reagieren? | `RECOVERY_PROTOCOL.md` (Root) |
| Konservierungs-/Gateway-/Titel-Konventionen | `STORAGE/templates/references/` |
| memU-Fachwissen (Memory-Framework, Upstream) | `README.md`, `MISSION_CORE.md`, `DOCS/tutorials/`, `DOCS/integrations/`, `DOCS/providers/` |
| LiteLLM-Provider-Muster | `toolkits/litellm-provider/` (README + RECIPE) |
| Repo-Struktur-Überblick | `STORAGE/repo-map/00_INDEX.md` |

## Verlauf

| Datum | Ereignis |
|:--|:--|
| 2026-07-19 | Kanon v1.2 etabliert (Zonen, Templates, Tier-1-Regelset) — diese Datei angelegt |
