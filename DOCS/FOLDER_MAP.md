<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# FOLDER_MAP.md — Kurz-Wegweiser memU

> **Zweck:** „Ich will X → ich mache Y." Zonen-Überblick für jeden Agenten ab Sekunde 1.

## Die Zonen

| Zone | Zweck | Wann nutzen |
|:--|:--|:--|
| `DESK/` | Projekt-SSoT: Master-Trio, Tasks, Session-Reports | Aufträge + Berichte |
| `DOCS/` | Router + Wegweiser + **Upstream-Projektdoku** (integrations/, providers/, tutorials/ — Fork-Erbe von NevaMind-AI/memU, nicht anfassen) | Orientierung |
| `STORAGE/` | Payloads on-demand: `templates/` (Kanon-Sätze), `repo-map/` | Bei Trigger laden |
| `WORKSPACE/` | Eine Werkbank pro Session + `INDEX.md` (Status-Board) + `handover/` (Start-Prompts) | Session-Arbeit |
| `ARCHIVE/` | EINZIGER Archiv-Ort (Root) — nie löschen, nur hierher | Konservierung |
| `.claude/rules/ssot/` | Tier-1-Regelset (Kanon v1.2) + 3 Altlast-Regeln (s. Aufräum-Task) | nativ geladen |
| `src/`, `tests/`, `toolkits/`, `data/`, `pgdata/` | Projekt-Code/-Daten (LOCAL — nie Kanon-Gegenstand) | Fachliche Arbeit |

## Ich will … → ich mache …

| Ich will | Ich mache |
|:--|:--|
| Eine neue Session starten | `WORKSPACE/handover/SESSION_START_PROMPT.md` als erste Nachricht geben |
| Eine laufende Session übernehmen | `WORKSPACE/handover/SESSION_OVERTAKE_PROMPT.md` |
| Wissen ablegen, das nicht immer geladen sein muss | `STORAGE/` + Eintrag in `DOCS/INDEX.md`-Trigger-Tabelle |
| Etwas loswerden, ohne es zu verlieren | `ARCHIVE/<name>_<YYYY-MM-DD>/` + `PROTOCOL_LOG.md`-Eintrag |
| Wissen, welcher Kanon-Stand hier gilt | `DOCS/STRUKTUR_MANIFEST.md` |
