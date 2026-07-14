---
name: Skill Routing Matrix — Tabelle & Rezepte
description: Die komplette Skill-Routing-Matrix: Welcher Skill für welchen Task-Kontext. Kombinations-Rezepte für Mehrfach-Skills. Immer injiziert, damit Agenten Skills finden.
trigger: always_on
scope: alle
repo: all
---

# 00_skill_matrix.md

> **STATUS:** ALWAYS_ON
> **SCOPE:** Alle Domänen (Factory, Studio, Lab)
> **BLOCK:** 00-09 — Meta-Konzepte (über allen Kategorien)

## 1. Skill-Routing-Matrix

**SOG:** Vor jeder technischen Aufgabe prüfe diese Matrix und lade den passenden Skill, DENN ohne Skill-Check arbeitest du blind und produzierst Code, der gegen Framework-Standards verstößt.

**Deklariere im Chat:** `SKILLS AKTIV: [Skill-Name] — [Grund]`

| Task-Kontext | Primärer Skill | Fallback | Gültig in |
|:--|:--|:--|:--|
| Business Logic / Entities | `clean-architecture` | — | packages/domain, packages/application |
| React Components (Struktur) | `feature-arch` | — | apps/web, apps/video |
| React Components (UI/Style) | `shadcn` | `tailwind` | packages/ui, apps/web |
| Tailwind v4 | `tailwind` | — | apps/web, packages/ui |
| Data Fetching / Caching | `tanstack-query` | — | apps/web |
| Formular-Validierung | `react-hook-form` | `zod` | apps/web |
| Schema-Validierung | `zod` | — | packages/application, apps/web |
| Web Animation | `framer-motion` | — | apps/web ONLY |
| Animation Philosophie | `emilkowal-animations` | — | Vor jeder framer-motion-Nutzung |
| 3D / Interactive | `spline-3d-integration` | — | apps/web (Hero, Landingpages) |
| Design Audit | `web-design-guidelines` | — | Vor visuellem Commit |
| Video (Visuals) | `remotion-studio` | `remotion-best-practices` | apps/video |
| Video (Infrastruktur) | `remotion-architect` | `remotion-best-practices` | apps/video |
| Monorepo / Build | `turborepo` | — | turbo.json, CI |
| Next.js / React Patterns | `vercel-react-best-practices` | — | apps/web |
| TDD Methodik | `tdd` | — | Test-first Entwicklung |
| Test-Implementation | `vitest` | — | Test-Dateien |
| Dead Code | `knip-deadcode` | — | Cleanup, CI |

## 2. Kombinations-Rezepte

| Rezept | Reihenfolge |
|:--|:--|
| **Neue Landing Page Section** | 1. emilkowal-animations → 2. framer-motion → 3. tailwind → 4. shadcn |
| **Hero mit 3D Spline Scene** | 1. spline-3d-integration → 2. emilkowal-animations → 3. framer-motion → 4. tailwind |
| **Formular-Sektion** | 1. react-hook-form → 2. zod → 3. shadcn → 4. framer-motion |
| **Dashboard-Panel mit Daten** | 1. tanstack-query → 2. zod → 3. feature-arch → 4. clean-architecture |
| **Remotion Video-Szene** | 1. remotion-studio ODER remotion-architect → 2. remotion-best-practices (nur bei Syntax-Fragen) |

## 3. Skill-Hierarchie & Conflict Resolution

Nicht alle Skills sind gleich. Bei Mehrfach-Treffern:

1. **Inline-gepatchte Base-Skills** (`clean-architecture`, `framer-motion`, `feature-arch`, `shadcn`) — haben Viron-spezifische Overrides inline.
2. **Remotion Extension-Skills** (`remotion-studio`, `remotion-architect`) — haben Vorrang vor `remotion-best-practices`.
3. **Vendor Skills** (`tailwind`, `zod`, `tanstack-query`, `react-hook-form`) — nur wenn Primär-Skill sie referenziert.

**Wenn generischer Skill ≠ Viron-Regel:** Folge der Viron-Variante. Details in `71_skill_routing.md`.

## 🔗 Light Router
- **WENN** du Conflict Resolution und Skill-Hierarchie-Details brauchst ➔ **LIES** `71_skill_routing.md`
- **WENN** du die Skill-Philosophie (Router statt Archiv) vertiefen willst ➔ **LIES** `80_rule_creation.md` (Section: Design für leere Kontextfenster)
