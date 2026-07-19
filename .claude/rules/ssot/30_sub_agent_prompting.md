---
name: Sub-Agent Prompting — 4-Säulen-Template
description: Definiert das zwingende 4-Säulen-Prompt-Template (MISSION, CONTEXT, SCOPE+VERBOTE, OUTPUT) für jeden Sub-Agenten-Spawn, damit Sub-Agenten nicht blind wildern.
trigger: always_on
scope: alle
repo: all
---
<!-- Kanon v1.2, ausgerollt 2026-07-19 -->

# 30_sub_agent_prompting.md

> **Tier-1-Rollout-Regel (universal)** — Quelle: `.claude/rules/ssot/30_sub_agent_prompting.md`,
> kuratiert Session 17 (KANON-SYSTEMREPARATUR_17, 2026-07-19).
> **Kurations-Vermerk (E-6, GATE E Session 17):** Die 4-Säulen-Benennung wurde auf die
> Operator-verbindliche Fassung vereinheitlicht: **MISSION / CONTEXT / SCOPE+VERBOTE /
> OUTPUT(+STOPP-Kriterium)**. Die alte ssot-Benennung (Mission / Context Injection / Scope
> Boundary / Report-Struktur) ist inhaltlich identisch abgedeckt.

> **STATUS:** ALWAYS_ON
> **SCOPE:** Alle Domänen
> **BLOCK:** 30 — Kommunikation & Verhalten

## 1. Das 4-Säulen-Prompt-Template

**SOG:** Statte jeden Sub-Agenten beim Spawnen mit diesen vier Säulen aus, DENN Sub-Agenten starten kalt (kein CLAUDE.md, kein Repo-Kontext) und richten ohne präzise Grenzen massiven Schaden an oder verfallen in redundante Such-Schleifen.

**A) MISSION:** Kristallklare Definition der Aufgabe ("Why > What").
**B) CONTEXT:** Essenzielle Verhaltensregeln, Vorwissen und Leseliste für die spezifische Rolle.
**C) SCOPE+VERBOTE:** Exakte Dateipfade des "Spielfelds" (z.B. `src/frontend/`) UND explizite Verbote (was NICHT angefasst werden darf).
**D) OUTPUT (+STOPP-Kriterium):** Erwartete Ergebnis-Struktur (z.B. Markdown-Tabellen in `DESK/reports/`) und wann der Agent abbrechen und melden soll statt zu raten.

**Modell explizit setzen:** Bei jedem Spawn `model:` bewusst wählen — mechanisches Suchen/Filtern → klein, Urteil/Architektur/adversariale Prüfung → stark.

## 2. Rauschfreie Kommunikation + Rückkanal

**SOG:** Leite Sub-Agenten an, Diffs und Logs ausschließlich in `DESK/reports/` (bzw. dem Report-Ort des Repos) zu sammeln, DENN ein rauschfreier Haupt-Chat schützt den Fokus des Orchestrators und ermöglicht fehlerfreie Fortschrittsüberwachung.

**Rückkanal-Pflicht:** Jeder Auftrag, der eine Nachricht/ein Artefakt an eine ANDERE Session oder einen anderen Agenten übergeben soll, MUSS die Rückkanal-Anweisung enthalten (wohin schreiben, wer liest es wann), DENN ohne deklarierten Rückkanal wird der Operator zum Postboten (real passiert, N1 Session 15).

## 3. Blocker Integrity

**SOG:** Friere den Prozess bei Tool-Errors oder fehlenden Berechtigungen sofort ein und melde den Blocker dem Operator, DENN transparente Telemetrie beschleunigt die Lösungsfindung und verhindert korrumpierte Systemstände durch "Ghost-Fixes".

## 4. Ausnahme

Nur bei reinen Such-Aufträgen (`explore`-Agent sucht eine Variable in `src/`) kann auf das volle Setup verzichtet werden, DENN der Agent hat ohnehin keine Schreibrechte und kann keinen Schaden anrichten.

## 🔗 Light Router
- **WENN** du das Behavior-Kodex (11 Laws) brauchst ➔ **LIES** `30_behavior.md`
- **WENN** du komplexe Multi-Agent-Systeme koordinieren musst ➔ prüfe, ob das Repo einen Orchestrierungs-Skill mitbringt (z.B. `multi-agent-orchestration`)
