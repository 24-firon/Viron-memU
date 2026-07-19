---
name: Architecture Constraints
description: Sechs fundamentale Architektur-Gesetze: Feature-Colocation, Server-Component-Default, Tailwind v4, Supabase-Security, Sandbox-First, Package-Boundaries.
trigger: always_on
scope: alle
repo: all
---

# 20_architecture_constraints.md

> **STATUS:** ALWAYS_ON
> **SCOPE:** Alle Domänen (Factory, Studio, Lab)
> **BLOCK:** 20 — Architektur & Boundaries
> **HERKUNFT:** `01-architecture-constraints.md` (ARCH-01 bis ARCH-06)

## ARCH-01 — Feature-Colocation Mandate

**SOG:** Lege Business-Logik in `apps/web/src/features/[feature]/` mit `server/`, `ui/`, `lib/`-Unterverzeichnissen, DENN `app/` ist nur Routing und darf keine `fetch()`-Calls enthalten.

**UI-Komponenten:** Das CLI routet über `components.json` nach `packages/ui`. Niemals UI-Elemente in `apps/web/components/ui` ablegen.
**Shared Domain-Logik:** → `packages/domain/`
**UI-Primitiven:** → `packages/ui/`

## ARCH-02 — Server-Component Default

**SOG:** Jede neue Datei in `app/` und `src/features/` ist standardmäßig ein React Server Component, DENN `"use client"` erzeugt Client-Boundaries, die Performance und Server-Rendering brechen.

**`"use client"` nur wenn:** Browser-APIs (`window`, `document`), Event-Handler direkt im JSX, Zustandsverwaltung (`useState`, `useReducer`), oder Hooks mit Browser-Abhängigkeiten (`useEffect`).

**Framer Motion:** Benötigt zwingend `"use client"` und muss isoliert am Rande des DOM-Baums gekapselt werden.

## ARCH-03 — No Config Tailwind

**SOG:** Konfiguriere Tailwind v4 ausschließlich über `@theme inline` in `packages/ui/src/styles.css`, DENN es existiert keine `tailwind.config.*` mehr — Tailwind v4 ist CSS-first.

**Verboten:** `tailwind.config.ts` oder `tailwind.config.js` im gesamten Monorepo.
**Erlaubt:** `@theme inline`, `@source` für externe Scan-Pfade, `@custom-variant` für neue Varianten.

## ARCH-04 — Supabase Security

**SOG:** Nutze `getClaims()` in der Middleware (JWT-Signatur validiert) und `getUser()` in Server Components (DB-verifiziert), DENN `getSession()` validiert die JWT-Signatur nicht und ist ein Sicherheitsrisiko.

**Verboten:** `getSession()` für Auth-Checks.
**Routing-Schutz:** Immer in Server Components, niemals in `middleware.ts`.

## ARCH-05 — Sandbox First

**SOG:** Erstelle neue Assets, Komponenten oder Frameworks zuerst in `apps/web/src/playground/`, DENN ungeprüfter Code im Core-System gefährdet die Stabilität der Produktion.

**Ausnahme Lab:** Im Lab (`/lab/*`) darf direkt gearbeitet werden — siehe `90_lab_exceptions.md`.

## ARCH-06 — Package Boundary Enforcement

**SOG:** Respektiere die Import-Hierarchie, DENN Packages dürfen keine Apps importieren und Apps dürfen keine anderen Apps importieren.

| Von \ Nach | packages/ui | packages/domain | apps/web | apps/video |
|:--|:--|:--|:--|:--|
| packages/ui | ✅ intern | ❌ verboten | ❌ verboten | ❌ verboten |
| packages/domain | ❌ verboten | ✅ intern | ❌ verboten | ❌ verboten |
| apps/web | ✅ erlaubt | ✅ erlaubt | ✅ intern | ❌ verboten |
| apps/video | ✅ erlaubt | ✅ erlaubt | ❌ verboten | ✅ intern |

## 🔗 Light Router
- **WENN** du die FSD Public API-Mandate für Features brauchst ➔ **LIES** `23_feature_arch.md`
- **WENN** du Clean Architecture-Regeln für Domain/Application brauchst ➔ **LIES** `24_clean_architecture.md`
- **WENN** du Dependency-Integrity (No Downgrade) brauchst ➔ **LIES** `20_dependency_integrity.md`
