---
name: Git Policy — Commits, Secret-Scan, PR-Revert
description: Conventional Commits, Secret-Scan vor Commit, PR-Revert-Protokoll, Double-Turn-Lock, Commit-Mandate. Framework-neutral kuratiert.
trigger: always_on
scope: alle
repo: all
---
<!-- Kanon v1.2, ausgerollt 2026-07-19 -->

# 40_git_policy.md

> **Tier-1-Rollout-Regel (universal)** — Quelle: `PLAYGROUND/viron_core_rules/40_git_policy.md`
> gemergt mit `src/rules/1_cores/40_git_policy.md`, kuratiert Session 17
> (KANON-SYSTEMREPARATUR_17, 2026-07-19).
> **Kurations-Vermerk:** Die `24-viron`-Account-Altlast der Quell-Fassung wurde entfernt
> (Pflicht-Fix laut R5-Landkarte) — die gültige Account-Regel (`24-firon`) steht in
> `00_system_identity.md` §3.

> **STATUS:** ALWAYS_ON
> **SCOPE:** Alle Domänen
> **BLOCK:** 40 — Workflow & Planning

## 1. Conventional Commits

**SOG:** Folge ausnahmslos der Conventional Commits Spezifikation (`<type>[optional scope]: <description>`), DENN das ermöglicht eine intuitive Commit-Historie und automatisierte Changelog-Generierung.

**Typen:** `feat`, `fix`, `chore`, `docs`, `refactor`, `test`
**Verboten:** Emojis, vage Begriffe wie `update`, `change`, `wip` als komplette Beschreibung.

## 2. Secret-Scan vor Commit

**SOG:** Führe vor jedem Commit `git diff --cached | grep -iE '(api_key|password|token|secret)'` aus, DENN Secrets im Git-Verlauf sind öffentlich und irreversibel.

## 3. Commit-Mandate

**SOG:** Biete nach jedem abgeschlossenen Deliverable/Task einen Commit an und committe regelmäßig in logischen Blöcken, DENN untracked Dateien sind spurlos löschbar (`git clean`, kein Papierkorb, keine Historie) — nur Committetes ist reversibel. Die GO-Frage (ob vor dem Commit explizite Freigabe nötig ist) regelt das GRUNDREGEL-BUNDLE (G6) bzw. die Repo-eigene Konvention.

## 4. PR-Revert-Protokoll

**SOG:** Erstelle nach Feature-Abschluss einen Pull Request statt direkt auf `main` zu mergen, DENN ein PR erzeugt einen Merge Commit, der bei Problemen mit einem einzigen `git revert -m 1 <MERGE_COMMIT_HASH>` stressfrei rückgängig gemacht werden kann.

**Vorteil:** Die Historie bleibt makellos, keine Arbeit geht durch hartes Zurücksetzen verloren.

## 5. Double-Turn-Lock + Safety-Lock

**SOG:** Verifiziere vor dem Push den Branch-Zustand (pusht niemand anderes auf denselben Branch?), DENN parallele Pushes erzeugen Merge-Konflikte und brechen die saubere Historie.

**Safety-Lock:** Destruktive Kommandos (`git reset --hard`, `git push --force`, `git clean`) nur mit expliziter Operator-Autorisierung.

## 🔗 Light Router
- **WENN** du die Account-Regel brauchst ➔ **SIEHE** `00_system_identity.md` §3
- **WENN** du die Reversibilitäts-Doktrin (getrackt vs. untracked) brauchst ➔ **LIES** `EXPORT/GIT_BASELINE.md` (bzw. die ins Ziel-Repo ausgerollte Kopie)
