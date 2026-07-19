---
name: Read Discipline — 50-Zeilen-Regel
description: Bevor große Dateien gelesen werden, zuerst die ersten 50 Zeilen (ToC prüfen), dann gezielte Extraktion. Verhindert Context-Bloat.
trigger: always_on
scope: alle
repo: all
---

# 40_read_discipline.md

> **STATUS:** ALWAYS_ON
> **SCOPE:** Alle Domänen (Factory, Studio, Lab)
> **BLOCK:** 40 — Workflow & Planning

## 1. Die 50-Zeilen-Regel

**SOG:** Bevor du eine unklare oder große Datei (z.B. `PROTOCOL_LOG.md`, fremde Dokumentationen, große Source-Files) liest, limitiere auf die ersten 50 Zeilen, DENN so findest du ein Inhaltsverzeichnis (ToC) und kannst gezielt die relevanten Sektionen laden, statt den gesamten Inhalt blind zu konsumieren.

**Fail:** Kompletter `cat` oder unlimitierter `Read` auf eine über 200 Zeilen lange Datei, die ein ToC gehabt hätte.

## 2. Gezielte Extraktion

**SOG:** Wenn das ToC sagt "Phase 12 beginnt bei Zeile 450", extrahiere NUR diesen Block (via `sed -n '450,550p'` oder `Read`-Tool mit `StartLine=450, EndLine=550`), DENN Bulk-Reads explodieren das Kontext-Fenster und verdrängen aktive Regeln.

## 3. Ausnahmen

**Erlaubt:** Vollständiges Lesen, wenn die Datei offensichtlich sehr klein ist (unter 300 Zeilen, kurze Configs).
**Erlaubt:** Vollständiges Lesen, wenn du bereits das ToC gelesen hast und festgestellt hast, dass keine Sektionierung existiert.

**Prinzip:** Token-Ökonomie. Denke immer: "Könnte diese Datei meinen Kontext explodieren lassen?" → Wenn ja: HEAD nutzen.

## 🔗 Light Router
- **WENN** du den Planning-Mandate (Plan-Pflicht) brauchst ➔ **LIES** `40_planning.md`
- **WENN** du den Git-Policy (Commits, PR-Revert) brauchst ➔ **LIES** `40_git_policy.md`
