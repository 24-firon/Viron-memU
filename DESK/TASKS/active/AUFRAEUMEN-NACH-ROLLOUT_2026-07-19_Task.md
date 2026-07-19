<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# Task: Aufräumen nach Kanon-Rollout (T-01)

> **Angelegt:** 2026-07-19 durch CDS-Session PILOT-ROLLOUT_18 (Leitplanke 8/9: Aufräumen =
> eigener Task für eine Nachfolgesession, NICHT Teil des Rollouts).
> **Priorität:** P2 · **Voraussetzung:** keine — alles reversibel vorbereitet.

## Posten (je einzeln Operator-Entscheid einholen, nichts löschen — nur ARCHIVE/)

- [ ] **A) VAS-Altlast-Regeln entfernen:** `.claude/rules/ssot/{00_skill_matrix,20_architecture_constraints,20_dependency_integrity}.md`
      sind Next.js/Tailwind/Supabase-Regeln in einem Python-Repo (ungefilterter Alt-Rollout
      2026-07-14). Kopie liegt bereits in `ARCHIVE/ssot-Altbestand-vor-Kanon-v1.2_2026-07-19/`
      → bei GO: aus `ssot/` entfernen (`git rm`), Archiv bleibt.
- [ ] **B) `pgdata/` aus Git:** Postgres-Datenverzeichnis ist getrackt (133+ Dauer-dirty-Dateien,
      Binärdaten im Verlauf). Klären: `.gitignore` + `git rm --cached` — Vorsicht, benötigt
      laufende-Container-Prüfung.
- [ ] **C) `memU-multi-provider-v1.0.zip`:** Herkunft/Zweck klären (untracked, 560K) —
      committen, archivieren oder als Build-Artefakt ignorieren?
- [ ] **D) `src/memu/embedding/backends/google.py`:** modifiziert, nie committet — WIP von wem?
      Committen oder verwerfen (Operator).
- [ ] **E) `ANDERER WIN NUTZER/`:** herkunftsunklar (3 Dateien, Leerzeichen im Namen verletzt
      Namenskonvention). Klären → ggf. `ARCHIVE/` mit konformem Namen.
- [ ] **F) `.agent/` (Windsurf) + `.agents/skills/` (leer):** Zombie-Ordner fremder Frameworks —
      IDE-Koexistenz-Regel beachten (NICHT löschen ohne expliziten Operator-Auftrag).
