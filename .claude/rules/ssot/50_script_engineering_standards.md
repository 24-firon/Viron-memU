---
name: Script Engineering Standards
description: Skript-Hygiene ohne Tech-Stack-Bezug: Memory-Effizienz, Encoding, Cross-Platform-Pfade, sequenzielle Ausführung.
trigger: conditional
scope: alle
repo: all
---
<!-- Kanon v1.2, ausgerollt 2026-07-19 -->

# RULE: Script Engineering Standards

> **Tier-1-Rollout-Regel (universal)** — Quelle: `src/rules/1_cores/50_script_engineering_standards.md`,
> kuratiert Session 17 (KANON-SYSTEMREPARATUR_17, 2026-07-19).

## Rule
Nutze Array-Generierung oder List-Comprehensions anstelle von String-Konkatenation (`+=`) in großen Schleifen, **DENN** das verhindert O(n²)-Performance-Einbrüche durch den Memory-Allocator.

## Standards
- **Memory Efficiency:** Avoid inefficient loops. Use `StringBuilder` or list comprehensions for large data processing.
- **Encoding Safety:** Explicitly use `UTF-8` (no BOM) for all file outputs.
- **Cross-Platform Pathing:** Convert backslashes to forward-slashes for Linux compatibility.
- **Sequential Execution:** Favor step-by-step terminal operations over complex batch scripts for critical tasks.
