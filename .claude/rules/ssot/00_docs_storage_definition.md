---
name: Docs vs. Storage vs. Skills — 3-Schichten-Kontext
description: Definiert die drei Kontext-Schichten (Docs permanent, Storage per Index, Skills per Task-Match) und das Präfix-System der Regeldateien.
trigger: always_on
scope: alle
repo: all
---
<!-- Kanon v1.2, ausgerollt 2026-07-19 -->

# 00_docs_storage_definition.md

> **Tier-1-Rollout-Regel (universal)** — Quelle: `.claude/rules/ssot/00_docs_storage_definition.md`,
> kuratiert Session 17 (KANON-SYSTEMREPARATUR_17, 2026-07-19).

> **STATUS:** ALWAYS_ON
> **SCOPE:** Alle Domänen
> **BLOCK:** 00-09 — Meta-Konzepte (über allen Kategorien)

## 1. Das Präfix-System

> ⚠️ **BEKANNTE INKONSISTENZ — Fix vertagt (D-004, 2026-07-19, Stammrepo CDS).** Im Kanon-Stammrepo
> existiert eine zweite, abweichende Block-Kategorien-Tabelle (`RULE_NUMBERING_CONCEPT.md`).
> Der Operator klärt die Präfix-Semantik zu einem späteren Zeitpunkt selbst. **Bis dahin gilt
> verbindlich: JEDE Regel ist relevant, unabhängig von ihrer Nummer. Die Nummer steuert AKTUELL
> NICHT, ob eine Regel geladen oder genutzt wird** — kein Agent darf eine Regel wegen ihres
> Präfixes (krumme Zahl, „Payload-Range" o.ä.) als optional oder nicht-geladen behandeln.

Dateinamen nutzen ein **hierarchisches Präfix-System**. Der Präfix definiert die **Kategorie**, nicht den always_on-Status. Ob eine Regel always_on oder conditional ist, steht im YAML-Header (`trigger:`).

| Präfix-Block | Kategorie |
|:--|:--|
| **00-09** | Meta-Konzepte (über allen Kategorien) |
| **10-19** | Safety & Zerstörungsschutz |
| **20-29** | Architektur & Boundaries |
| **30-39** | Kommunikation & Verhalten |
| **40-49** | Workflow & Planning |
| **50-59** | Tech Stack |
| **60-69** | Design & Qualität |
| **70-79** | Agent & Knowledge |
| **80-89** | Regel-Evolution |
| **90-99** | Repo-spezifische Ausnahmen |

**Innerhalb jedes Blocks:**
- **X0** = Kopf der Kategorie (Haupt-Regel) + alle always_on Sub-Regeln
- **X1–X4** = Zugehörige Details (sub-rules)
- **X5–X9** = Payload/Storage (nur bei Bedarf)

**Beispiel:** `10_core_safety.md` (X0, always_on) ist der Kopf des Safety-Blocks. `10_windows_shell.md` (X0, always_on) ist eine Sub-Regel im selben Block — immer X0 für always_on.

## 2. Die 3-Schichten-Architektur

Jedes Repo orchestriert Kontext in drei Ebenen. Ein Agent, der diese Ebenen nicht unterscheidet, lädt entweder zu viel (Rule-Fatigue) oder zu wenig (Amnesie).

| Schicht | Mechanik | Wann aktiv | Beispiel |
|:--|:--|:--|:--|
| **DOCS** | Permanent injiziert (SessionStart-Hook, nativ `.claude/rules/`, `CLAUDE.md`-Imports bzw. `opencode.jsonc` je nach Framework) | Immer, jeder Turn | Safety, Identity, Communication, diese Datei, Router |
| **STORAGE** | Conditional — per Index-Datei (z.B. `DOCS/routing/_index.md`) geladen | Bei Task-Bedarf | Tech-Rules, Design, Git, Agent-Delegation |
| **SKILLS** | Conditional — per Task-Match geladen | Bei Skill-Match | Deployment-Workflow, Forensic-Protokoll |

## 3. DOCS (Permanent)

**Definition:** Dateien, die **jeder Agent in jeder Session braucht** und die sich **während der Session nicht ändern**.

**Vorteil:** Sie rutschen nie im Kontext-Fenster nach hinten, überleben Session-Komprimierung und sind bei jedem Turn präsent. Kein einmaliges Lesen, das dann verblasst.

**Inhalt:** Diese Datei, Safety, Identity, Communication, Architektur-Grundgesetze, Routing-Direktive.

## 4. STORAGE (Conditional)

**Definition:** Knowledge-Dateien, die **nicht** in einen Skill gehören, aber **nicht permanent injiziert** werden müssen.

**Mechanik:** Eine Index-Datei (z.B. `DOCS/routing/_index.md`) liegt im Docs-Bereich. Der Agent liest den Index bei Bedarf und lädt nur die relevante Datei.

## 5. SKILLS (Conditional)

**Definition:** Strukturierte Instruktionspakete mit eigener Ordnerstruktur (`SKILL.md` + `examples/` + `templates/`).

**Mandat:** Skills sind **Router, keine Archive**. Die `SKILL.md` sagt: "Wenn du X tust, lies Datei Y." Lade nur die Dateien, die für deine aktuelle Phase relevant sind.

## 6. Für Agenten, die selbst Regeln schreiben

1. **Schicht bestimmen:** Braucht sie permanenten Schutz (Docs) oder ist sie kontextabhängig (Storage/Skill)?
2. **Präfix bestimmen:** Welcher 10er-Block? X0-Kopf oder X1-X4-Detail?
3. **Index-Eintrag:** Jede neue Storage-Datei MUSS im Regel-Index des Repos registriert werden.
4. **SOG-Format:** "Um [Ziel] zu erreichen, nutze [Methode], DENN [Konsequenz]."

## 🔗 Light Router
- **WENN** du das Routing-Protokoll (3-stufige Prüfung + Payload-Logging) brauchst ➔ **LIES** `00_routing_protocol.md`
- **WENN** du wissen willst, wie neue Regeln registriert werden ➔ **LIES** `81_rule_filesystem.md`
