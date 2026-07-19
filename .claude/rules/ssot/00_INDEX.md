<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# 00_INDEX.md — Tier-1-Rollout-Regelset (universal)

> **Stand:** 2026-07-19 · **Kuratiert:** Session KANON-SYSTEMREPARATUR_17 (M4, Naht 2, E-2)
> **Was das ist:** Das kuratierte, framework-neutrale Regel-Set, das der
> `REPO_ETABLIERUNGS_PROMPT.md` (Stufe 2b) in Ziel-Repos verteilt. Basis-Linie laut GATE-E-Entscheid
> E-2: `.claude/rules/ssot/` (die einzige real zur Laufzeit gelebte Regel-Linie), ergänzt um
> universelle Regeln aus `src/rules/1_cores/` und `PLAYGROUND/viron_core_rules/` (R5-Landkarte).
> Definiert als MANAGED-Pflichtelement in `KANON_STRUKTUR_SPEC.md` §3 (`rules/… Tier-1-Set`).
>
> **⛔ Bewusst NICHT enthalten:** VAS-/Framework-/Tech-Stack-spezifische Regeln (Next.js, Tailwind,
> Supabase, Remotion, Zod/React-Versionen, Port-Governance, Skill-Matrizen). Sie kommen als
> **Repo-eigenes Overlay** (Tier 2 Domain / Tier 3 Repo, Spec §4.3) — niemals über dieses Set.

## Das Set (16 Regeln — 18 Dateien auf der Platte inkl. `GRUNDREGEL-BUNDLE.md` + dieser Index)

| # | Datei | Zweck (1 Satz) | Quelle |
|:--|:--|:--|:--|
| 1 | `00_docs_storage_definition.md` | 3-Schichten-Kontext (DOCS/STORAGE/SKILLS) + Präfix-System inkl. K3-Notiz „jede Regel relevant, egal welche Nummer". | ssot |
| 2 | `00_routing_protocol.md` | 3-stufige Prüfung vor jeder Aufgabe + Payload-Logging + Brain-Dateien-Anker; Dual-Framework-Hinweis. | ssot |
| 3 | `00_system_identity.md` | Browser-Disziplin, IDE-Koexistenz (Multi-Agent-Schutz), Account-Authentizität `24-firon`. | ssot (VAS-Port-Abschnitt entfernt) |
| 4 | `10_core_safety.md` | Zerstörungsschutz: Read-before-Delete, Edit-statt-Write, Copy-Verify-Delete, Secrets-Schutz, Versionierung. | ssot |
| 5 | `10_windows_shell.md` | Windows-Shell-Disziplin (Claude Code): Bash vs. PowerShell, `/dev/null` statt `NUL`, keine interaktiven Befehle. | ssot |
| 6 | `30_behavior.md` | Die 11 Verhaltensgesetze (Anti-Hide bis No Silent Failures). | ssot |
| 7 | `30_communication.md` | Deutsch, Copy-Ready-Blöcke, `?????`-Signal, `!!!!!`-Notbremse, Anti-Jammerei. | ssot |
| 8 | `30_sub_agent_prompting.md` | 4-Säulen-Briefing (MISSION/CONTEXT/SCOPE+VERBOTE/OUTPUT, E-6-harmonisiert) + Rückkanal-Pflicht (N1). | ssot (E-6/N1 eingearbeitet) |
| 9 | `30_verification.md` | Definition of Done: physischer Beweis vor jedem Haken, No Silent Success. | ssot |
| 10 | `40_planning.md` | Plan-Pflicht, Approval-Gate-Block, Ambiguity Killer, Step-by-Step-Mandat. | ssot |
| 11 | `40_read_discipline.md` | 50-Zeilen-Regel + gezielte Extraktion gegen Context-Bloat. | ssot |
| 12 | `40_git_policy.md` | Conventional Commits, Secret-Scan, Commit-Mandate, PR-Revert, Double-Turn-Lock (Account-Altlast entfernt). | viron_core_rules + 1_cores (Merge) |
| 13 | `40_naming_convention_fields.md` | Namenskonvention: `_` trennt Felder, `-` verbindet Wörter (Operator-Kanon 2026-07-13). | src/rules/1_cores |
| 14 | `50_script_engineering_standards.md` | Skript-Hygiene: Memory, UTF-8 ohne BOM, Cross-Platform-Pfade. | src/rules/1_cores |
| 15 | `80_rule_creation.md` | Why > What, Ausführlichkeit vor Kürze, Design für leere Kontextfenster. | viron_core_rules |
| 16 | `81_rule_filesystem.md` | Index-Zwang für neue Regeln — keine Schatten-Regeln. | viron_core_rules |
| — | `GRUNDREGEL-BUNDLE.md` | G1–G9 Basisregeln — Fallback-Kopie; primär läuft die zentrale Injektion aus CDS (siehe Kopf-Hinweis der Datei). | ssot |

## Zugehörige EXPORT-Top-Level-Dokumente (nicht dupliziert)

`GIT_BASELINE.md` (Reversibilitäts-Doktrin) und `RECOVERY_PROTOCOL.md` (Verhalten nach eigenem
Fehler) sind Operator-gesetzte Tier-1-Kandidaten (R5) und liegen bereits als Top-Level-Dateien in
`EXPORT/` — sie werden dort gepflegt und NICHT in `rules/` dupliziert (eine Kopie weniger, die
driften kann). Der Etablierungs-Prompt verteilt sie zusammen mit diesem Set.

## Bewusst AUSGESCHLOSSEN (Verdikt je Datei — K7b: sichtbar durchentschieden)

| Datei (Quelle `.claude/rules/ssot/`) | Verdikt | Grund |
|:--|:--|:--|
| `00_skill_matrix.md` | ❌ VAS/Repo-spezifisch | Skill-Matrizen listen real installierte Skills — die sind pro Repo verschieden; jedes Ziel-Repo baut seine eigene (CDS-Fassung: D-004 K2). |
| `20_architecture_constraints.md` | ❌ VAS-spezifisch | ARCH-01…06 setzen `apps/web`-Monorepo, Tailwind v4, Supabase, RSC voraus — existiert in beliebigen Ziel-Repos nicht. |
| `20_dependency_integrity.md` | ❌ VAS-spezifisch | Zod v4/React 19/pnpm-lock/Viron-Vendor-Liste; das universelle Prinzip „Fix the Code, not the Dependency" ist Kandidat für eine spätere neutralisierte Fassung. |
| `00_system_identity.md` §„Port & Dev-Server-Hygiene" | ❌ VAS-Teil (Datei getrennt) | Port 3012/Next.js 16.2.6/`pnpm dev`/`remotion studio` — nur VAS; Rest der Datei ist im Set (#3). |

## Kollisions-Regel bei Verteilung (hart)

Existiert im Ziel-Repo bereits eine gleichnamige oder konzeptgleiche Regel: **NICHT überschreiben**
→ melden, Verdikt-Tabelle (`übernehmen`/`anpassen`/`learn-back`/`koexistenz`), Operator entscheidet.
Details: `REPO_ETABLIERUNGS_PROMPT.md` Stufe 2b + `KANON_STRUKTUR_SPEC.md` §1.3/§4.3.
