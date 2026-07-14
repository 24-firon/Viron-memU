---
name: Docs vs. Storage vs. Skills — 3-Schichten-Kontext
description: Definiert die drei Kontext-Schichten (Docs permanent via JSONC, Storage per Index, Skills per Task-Match) und das Präfix-System der Regeldateien.
trigger: always_on
scope: alle
repo: all
---

# 00_docs_storage_definition.md

> **STATUS:** ALWAYS_ON
> **SCOPE:** Alle Domänen (Factory, Studio, Lab)
> **BLOCK:** 00-09 — Meta-Konzepte (über allen Kategorien)

## 1. Das Präfix-System

Dateinamen nutzen ein **hierarchisches Präfix-System**. Der Präfix definiert die **Kategorie**, nicht den always_on-Status. Ob eine Regel always_on oder conditional ist, steht im YAML-Header (`trigger:`).

| Präfix-Block | Kategorie | always_on (X0) | conditional (X3-X9) |
|:--|:--|:--|:--|
| **00-09** | Meta-Konzepte (über allen Kategorien) | 00 | — |
| **10-19** | Safety & Zerstörungsschutz | 10 | — |
| **20-29** | Architektur & Boundaries | 20 | 23, 24 |
| **30-39** | Kommunikation & Verhalten | 30 | — |
| **40-49** | Workflow & Planning | 40 | 44 |
| **50-59** | Tech Stack | — | 50, 51, 52, 53, 54 |
| **60-69** | Design & Qualität | 60 | 61, 62, 63 |
| **70-79** | Agent & Knowledge | — | 70, 71, 72, 73 |
| **80-89** | Regel-Evolution | — | 80, 81 |
| **90-99** | Lab Exceptions | — | 90 |

**Innerhalb jedes Blocks:**
- **X0** = Kopf der Kategorie (Haupt-Regel) + alle always_on Sub-Regeln
- **X1–X4** = Zugehörige Details (sub-rules)
- **X5–X9** = Payload/Storage (nur bei Bedarf)

**Beispiel:** `20_architecture_constraints.md` (X0, always_on) ist der Kopf. `20_dependency_integrity.md` (X0, always_on) ist eine Sub-Regel im selben Block – immer X0 für always_on. `23_feature_arch.md` (X3, conditional) ist ein zugehöriges Detail.

## 2. Die 3-Schichten-Architektur

Jedes Viron-Repo orchestriert Kontext in drei Ebenen. Ein Agent, der diese Ebenen nicht unterscheidet, lädt entweder zu viel (Rule-Fatigue) oder zu wenig (Amnesie).

| Schicht | Mechanik | Wann aktiv | Beispiel |
|:--|:--|:--|:--|
| **DOCS** | Permanent injiziert via SessionStart-Hook + nativ `.claude/rules/` + `CLAUDE.md` | Immer, jeder Turn | Safety, Identity, Communication, diese Datei, Router |
| **STORAGE** | Conditional — per Index-Datei in `DOCS/routing/` geladen | Bei Task-Bedarf | Tech-Rules, Design, Git, Agent-Delegation |
| **SKILLS** | Conditional — per Task-Match geladen | Bei Skill-Match | Deployment-Workflow, Forensic-Protokoll |

## 3. DOCS (Permanent)

**Definition:** Dateien, die **jeder Agent in jeder Session braucht** und die sich **während der Session nicht ändern**.

**Vorteil:** Sie rutschen nie im Kontext-Fenster nach hinten, überleben Session-Komprimierung und sind bei jedem Turn präsent. Kein einmaliges Lesen, das dann verblasst.

**Inhalt:** Diese Datei, Safety, Identity, Communication, Architektur-Grundgesetze, Routing-Direktive, Skill-Matrix.

## 4. STORAGE (Conditional)

**Definition:** Knowledge-Dateien in `DOCS/`, die **nicht** in einen Skill gehören, aber **nicht permanent injiziert** werden müssen.

**Mechanik:** Eine Index-Datei (`DOCS/routing/_index.md`) liegt im Docs-Bereich. Der Agent liest den Index bei Bedarf und lädt nur die relevante Datei.

## 5. SKILLS (Conditional)

**Definition:** Strukturierte Instruktionspakete mit eigener Ordnerstruktur (`SKILL.md` + `examples/` + `templates/`).

**Mandat:** Skills sind **Router, keine Archive**. Die `SKILL.md` sagt: "Wenn du X tust, lies Datei Y." Lade nur die Dateien, die für deine aktuelle Phase relevant sind.

## 6. Für Agenten, die selbst Regeln schreiben

1. **Schicht bestimmen:** Braucht sie permanenten Schutz (Docs) oder ist sie kontextabhängig (Storage/Skill)?
2. **Präfix bestimmen:** Welcher 10er-Block? X0-Kopf oder X1-X4-Detail?
3. **Index-Eintrag:** Jede neue Storage-Datei MUSS in `DOCS/routing/_index.md` registriert werden.
4. **SOG-Format:** "Um [Ziel] zu erreichen, nutze [Methode], DENN [Konsequenz]."

## 🔗 Light Router
- **WENN** du das Routing-Protokoll (3-stufige Prüfung + Payload-Logging) brauchst ➔ **LIES** `00_routing_protocol.md`
- **WENN** du die Skill-Matrix (welcher Skill für welchen Task) brauchst ➔ **SIEHE** `00_skill_matrix.md` (immer injiziert)
- **WENN** du den vollständigen Rule-Index mit allen Triggern brauchst ➔ **LIES** `DOCS/routing/_index.md`
