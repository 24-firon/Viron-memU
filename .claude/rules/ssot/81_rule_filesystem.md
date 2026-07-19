---
name: Rule Filesystem Policy — Index-Zwang
description: Verbot von Schatten-Regeln. Neue Regeln brauchen Kategorisierung, YAML-Header und einen Eintrag im Regel-Index des Repos.
trigger: conditional
scope: alle
repo: all
---
<!-- Kanon v1.2, ausgerollt 2026-07-19 -->

# 81_rule_filesystem.md

> **Tier-1-Rollout-Regel (universal)** — Quelle: `PLAYGROUND/viron_core_rules/81_rule_filesystem.md`,
> kuratiert Session 17 (KANON-SYSTEMREPARATUR_17, 2026-07-19).

> **STATUS:** CONDITIONAL
> **SCOPE:** Alle Domänen
> **BLOCK:** 80 — Regel-Evolution
> **TRIGGER:** WENN du eine neue Regel-Datei erstellst

## 1. Das Wildwuchs-Verbot

**SOG:** Erstelle niemals blind neue `.md`-Dateien in den Rules-Ordnern, ohne sie zu registrieren, DENN nicht-indexierte "Schatten-Regeln" werden vom Routing-System nicht gefunden und sind funktionslos.

## 2. Die 3-Pkt-Erstellungsregel

**SOG:** Folge bei jeder neuen Regel diesem Ablauf:

1. **Kategorisierung:** Ordne die Regel einem 10er-Block zu (00=System, 10=Safety, 20=Architektur, etc.). Ist sie ein X0-Kopf oder ein X1-X4-Detail?
2. **YAML-Pflicht:** Jede neue Regel braucht den standardisierten YAML-Header mit `name`, `description` (2 volle Sätze!), `trigger` und `scope`.
3. **Index-Eintrag:** Trage Name, Speicherort und Zweck in den Regel-Index des Repos ein (z.B. `DOCS/routing/_index.md` oder `DOCS/INDEX.md`), BEVOR die Regel aktiv wird.

## 3. Präfix-System

| Präfix | Bedeutung |
|:--|:--|
| **X0** | Kopf der Kategorie (always_on / Haupt-Regel) |
| **X1–X4** | Geroutete Details (conditional / sub-rules) |
| **X5–X9** | Payload/Storage (nur bei Bedarf) |

> Hinweis: Zur aktuell geltenden Präfix-Semantik siehe die K3-Notiz in
> `00_docs_storage_definition.md` §1 — bis zur Operator-Klärung gilt: JEDE Regel ist relevant,
> unabhängig von ihrer Nummer.

## 4. Verstoß

**Konsequenz:** Das Erstellen von Regeln ohne Index-Eintrag führt zum sofortigen Vertrauensverlust und zum Abbruch der aktuellen Task-Iteration.

## 🔗 Light Router
- **WENN** du das Docs/Storage/Skills-Konzept verstehen musst ➔ **LIES** `00_docs_storage_definition.md`
- **WENN** du das Routing-Protokoll (3-stufige Prüfung) brauchst ➔ **LIES** `00_routing_protocol.md`
