<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# memU — MASTER TASK STATE

> **Zweck:** Aktueller Sprint-Zustand: Blocker, validierte Entscheidungen, Rückspiegelungen.
> **Regel:** Nur editieren/anhängen, nicht überschreiben. Gerüst angelegt 2026-07-19 (SEEDED).

## Blocker

| Thema | Status | Priorität |
|:--|:--:|:--:|
| `pgdata/` (Postgres-Datenverzeichnis) ist git-getrackt → Dauer-dirty | 🟡 BEKANNT | P2 — Aufräum-Task T-01 |
| 3 VAS-Altlast-Regeln in `.claude/rules/ssot/` (Next.js/Tailwind in Python-Repo) | 🟡 BEKANNT | P2 — Aufräum-Task T-01, Operator-Entscheid |
| Branch `production-setup` ahead of origin, Push-Entscheid offen | 🟡 BEKANNT | P2 — T-03 |

## Rückspiegelung 2026-07-19 — Kanon-Etablierung (CDS-Session PILOT-ROLLOUT_18)

| Was | Status | Beleg |
|:--|:--:|:--|
| Reversibilitäts-Sicherung: 211 zuvor untracked Dateien committet | ✅ | Commit `b6a0f2f` |
| `docs/` → `DOCS/` (Spec §2.5), Upstream-Inhalt erhalten | ✅ | Commit `1068ec9` |
| Templates + Start-Prompts verteilt (41 Dateien, 0 Kollisionen) | ✅ | Commit `45546e0` |
| Tier-1-Regelset v1.2 (18 Dateien: 5 neu, 12 Updates, Manifest) | ✅ | Commit `6ed8192` |
| SEEDED-Gerüste (Board, Router, FOLDER_MAP, Trio, Manifest) | ✅ | dieser Commit |
