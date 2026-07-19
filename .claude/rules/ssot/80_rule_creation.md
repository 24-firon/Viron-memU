---
name: Rule Creation Policy — Why > What
description: Jede Regel MUSS das "Warum" (den Grund) ausführlich erklären. Begründungspflicht, Ausführlichkeit vor Kürze, Design für leere Kontextfenster.
trigger: conditional
scope: alle
repo: all
---
<!-- Kanon v1.2, ausgerollt 2026-07-19 -->

# 80_rule_creation.md

> **Tier-1-Rollout-Regel (universal)** — Quelle: `PLAYGROUND/viron_core_rules/80_rule_creation.md`,
> kuratiert Session 17 (KANON-SYSTEMREPARATUR_17, 2026-07-19).

> **STATUS:** CONDITIONAL
> **SCOPE:** Alle Domänen
> **BLOCK:** 80 — Regel-Evolution
> **TRIGGER:** WENN du eine neue Regel formulierst, eine bestehende patchst oder Architektur-Wissen dokumentierst

## 1. Das "Why > What"-Prinzip

**SOG:** Erkläre bei jeder Regel, jedem Architektur-Dokument und jedem Skill-Readme zwingend das "Warum" (den Grund), DENN KIs brauchen den Kontext, um Entscheidungen logisch abzuwiegen — ohne "Warum" verkommt das System zu sinnlosen Dogmen, die umgangen oder falsch angewendet werden.

**Beispiel:**
- ❌ Falsch: "Nutze immer `asyncpg.connect()` statt `pool.add_listener()`."
- ✅ Richtig: "Nutze immer `asyncpg.connect()`, WEIL `pool.add_listener()` die Connection beim Release in den Pool verliert (asyncpg Issue #519) und der Worker danach lautlos keine Events mehr empfängt."

## 2. Ausführlichkeit schlägt Kürze

**SOG:** Formuliere Regeln extrem detailliert und nutze lieber drei Sätze mehr, um ein Konzept wasserdicht zu machen, DENN eine KI darf Wissen niemals eigenmächtig komprimieren — dabei geht immer Kontext verloren.

**Verboten:** Regeln der Länge wegen zusammenfassen. Reduzieren kann der menschliche Operator im Nachhinein.

## 3. Design für leere Kontextfenster

**SOG:** Schreibe so, dass ein Agent, der zum allerersten Mal aufwacht, sofort die Historie, den Schmerz vergangener Fehler und die exakte Intention der Regel begreift, DENN die nächste KI hat ein völlig leeres Kontextfenster und braucht den vollen Kontext für Edge-Case-Entscheidungen.

## 🔗 Light Router
- **WENN** du die Regel-Erstellung im Dateisystem (Index-Pflicht) brauchst ➔ **LIES** `81_rule_filesystem.md`
