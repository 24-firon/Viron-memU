---
name: Sub-Agent Prompting — 4-Säulen-Template
description: Definiert das zwingende 4-Säulen-Prompt-Template (Mission, Context, Scope, Report) für jeden Sub-Agenten-Spawn, damit Sub-Agenten nicht blind wildern.
trigger: always_on
scope: alle
repo: all
---

# 30_sub_agent_prompting.md

> **STATUS:** ALWAYS_ON
> **SCOPE:** Alle Domänen (Factory, Studio, Lab)
> **BLOCK:** 30 — Kommunikation & Verhalten

## 1. Das 4-Säulen-Prompt-Template

**SOG:** Statte jeden Sub-Agenten beim Spawnen mit diesen vier Säulen aus, DENN Sub-Agenten starten ohne Kontext und richten ohne präzise Grenzen massiven Schaden an oder verfallen in redundante Such-Schleifen.

**A) Mission:** Kristallklare Definition der Aufgabe ("Why > What").
**B) Context Injection:** Essenzielle Verhaltensregeln für die spezifische Rolle.
**C) Scope Boundary:** Exakte Dateipfade des "Spielfelds" (z.B. `src/frontend/`).
**D) Report-Struktur:** Anweisung zur Ablage der Ergebnisse in Markdown-Tabellen im `DESK/reports/`-Verzeichnis.

## 2. Rauschfreie Kommunikation

**SOG:** Leite Sub-Agenten an, Diffs und Logs ausschließlich in `DESK/reports/` zu sammeln, DENN ein rauschfreier Haupt-Chat schützt den Fokus des Orchestrators und ermöglicht fehlerfreie Fortschrittsüberwachung.

## 3. Blocker Integrity

**SOG:** Friere den Prozess bei Tool-Errors oder fehlenden Berechtigungen sofort ein und melde den Blocker dem Operator, DENN transparente Telemetrie beschleunigt die Lösungsfindung und verhindert korrumpierte Systemstände durch "Ghost-Fixes".

## 4. Ausnahme

Nur bei reinen Such-Aufträgen (`explore`-Agent sucht eine Variable in `src/`) kann auf das volle Setup verzichtet werden, DENN der Agent hat ohnehin keine Schreibrechte und kann keinen Schaden anrichten.

## 🔗 Light Router
- **WENN** du das Behavior-Kodex (11 Laws) brauchst ➔ **LIES** `30_behavior.md`
- **WENN** du komplexe Multi-Agent-Systeme koordinieren musst ➔ **STARTE** den Skill `multi-agent-orchestration`
