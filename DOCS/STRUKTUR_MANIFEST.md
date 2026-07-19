<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# STRUKTUR_MANIFEST — memU

Kanon-Version bei letztem Rollout: **v1.2**
Rollout-Datum: **2026-07-19**
Rollout-Phase erreicht: **II (etabliert)** — Zonen + Templates (Stufe 2) + Regel-Set (Stufe 2b)
Ausgerollt durch: CDS-Session `PILOT-ROLLOUT_18_KANON-ROLLOUT_CDS_2026-07-19` (erster Pilot-Rollout)
Migrations-Dossier: `Context-Dispatcher-System/WORKSPACE/PILOT-ROLLOUT_18_.../desk/MIGRATIONS_DOSSIER_memU_2026-07-19.md`

## Besonderheit dieses Repos

memU ist ein **Fork** von Upstream-OSS (`NevaMind-AI/memU` → `24-firon/Viron-memU`) und hatte
bereits am 2026-07-14 (Commit `d037da6`) einen undokumentierten Teil-Rollout auf Regel-Ebene
erhalten. Dieser Rollout war daher ein **Update auf gedrifteten Bestand**, kein Erstbezug.

## Waiver / bewusste Abweichungen

| Element | Abweichung | Begründung | Operator-GO (Datum) |
|---|---|---|---|
| `DOCS/` | enthält zusätzlich Upstream-Projektdoku (integrations/, providers/, tutorials/, 3 Fach-md) | Fork-Erbe; Verschieben würde Upstream-Referenzen brechen. Kanon-Router-Dateien (INDEX, FOLDER_MAP) koexistieren daneben | 2026-07-19 (docs→DOCS-Rename beauftragt, Inhalt erhalten) |
| `.claude/rules/ssot/` | trägt 3 VAS-Regeln, die NICHT zum Tier-1-Set gehören (`00_skill_matrix`, `20_architecture_constraints`, `20_dependency_integrity`) | Altlast des ungefilterten 14.07.-Rollouts; Entfernung = Aufräum-Task T-01, nicht Rollout | 2026-07-19 („liegen lassen + Task", Freigabe nach Empfehlung) |
| `pgdata/`, `memU-multi-provider-v1.0.zip`, `src/.../google.py` (WIP) | vom Rollout unberührt | außerhalb Rollout-Scope (Leitplanke 8) | 2026-07-19 |

## Learn-back-Kandidaten aus diesem Repo (an Kanon gemeldet)

| Kandidat | Status |
|---|---|
| L-1 Dossier-Ablageort widerspricht Phase-I-read-only (Prompt-Defekt, betrifft jeden Rollout) | gemeldet (`IMPORT/kanon_vorschlaege/memU_L1_dossier-ablageort.md`) |
| L-2 Kanon-Versions-Stempel fehlte als Pflicht in Stufe 2b → Folge-Rollouts brauchen Forensik | gemeldet (`…/memU_L2_versions-stempel.md`) |
| L-3 Fork-Repos: Kanon kennt keine Upstream-Merge-Strategie | gemeldet (`…/memU_L3_fork-strategie.md`) |
| L-4 Windows-Case-Collision bei Zonen-Casing (docs↔DOCS): Spec braucht Rename-Anweisung | gemeldet (`…/memU_L4_case-collision.md`) |
