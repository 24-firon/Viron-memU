---
name: Dependency Integrity
description: Verbot von Library-Downgrades zur Fehlerumgehung, Lockfile-Sanctity und Vendor-Integrity für den Cutting-Edge-Stack.
trigger: always_on
scope: alle
repo: all
---

# 20_dependency_integrity.md

> **STATUS:** ALWAYS_ON
> **SCOPE:** Alle Domänen (Factory, Studio, Lab)
> **BLOCK:** 20 — Architektur & Boundaries

## 1. No Lazy Downgrade

**SOG:** Senke niemals eine Library-Version, nur um einen Type-Error zu beheben, DENN der Viron-Stack nutzt Cutting Edge (Zod v4, React 19) und ein Downgrade führt zu veralteten Libs mit potenziellen Sicherheitslücken und Inkompatibilitäten.

**Verboten:** "Zod v3 installieren, weil der Resolver meckert."
**Lösung:** Fix the Code, not the Dependency. Im Notfall `as any` casts nutzen, aber Downgrade ist Tabu.

## 2. Lockfile Sanctity

**SOG:** Behandle `pnpm-lock.yaml` als die Wahrheit, DENN manuelle Lockfile-Änderungen ohne `pnpm install` erzeugen inkonsistente Dependency-States.

**Pflicht:** Nach Dependency-Änderungen `pnpm install` ausführen und verifizieren, dass keine unnötigen Änderungen im Lockfile entstehen.

## 3. Vendor Integrity

**SOG:** Installiere keine Pakete, die nicht im Viron-Standard (Radix, Lucide, TanStack) enthalten sind, ohne explizite Genehmigung, DENN ungeprüfte Dependencies können Sicherheitslücken, Bundle-Bloat oder Lizenzkonflikte einführen.

**Pflicht:** Neue Dependencies müssen im Decision Log dokumentiert werden.
