---
name: Routing-Protokoll — 3-stufige Prüfung + Payload-Logging
description: Zwingt jeden Agent zur deterministischen 3-stufigen Prüfung (Docs → Storage → Skills) vor Task-Beginn und zur Protokollierung geladener Payloads in der walkthrough.md.
trigger: always_on
scope: alle
repo: all
---

# 00_routing_protocol.md

> **STATUS:** ALWAYS_ON
> **SCOPE:** Alle Domänen (Factory, Studio, Lab)
> **BLOCK:** 00-09 — Meta-Konzepte (über allen Kategorien)

## 1. Die 3-stufige Prüfung (VOR jeder Aufgabe)

Ein Agent, der diese Prüfung nicht durchläuft, handelt blind. Er lädt entweder irrelevante Payloads (Token-Verschwendung) oder vergisst kritische Regeln (Fehler).

**Stufe 1 — DOCS prüfen (immer aktiv, kein Laden nötig):**
- Ist die Antwort in den permanent injizierten Regeln?
- → JA: Handeln
- → NEIN: Weiter zu Stufe 2

**Stufe 2 — STORAGE prüfen (per Index):**
- Welche Kategorie betrifft mein Task?
- → LIES den Indexeintrag in `DOCS/routing/_index.md`
- → LADE die geroutete Datei
- → **DOKUMENTIERE** den Ladevorgang in der `walkthrough.md` (siehe Section 3)
- → Handle

**Stufe 3 — SKILLS prüfen (per Task-Match):**
- Gibt es einen Skill für meine Aufgabe?
- → Prüfe `.claude/skills/` (bzw. Skill-Tool) auf passende `SKILL.md`
- → Folge der Routing-Matrix des Skills
- → Handle

## 2. Kontext-Lebenszyklus

| Schicht | Nach Task-Ende | Nach Komprimierung |
|:--|:--|:--|
| **DOCS** | Bleiben permanent aktiv | Bleiben aktiv (via JSONC injiziert) |
| **STORAGE** | Verlassen den Kontext | **MÜSSEN neu geladen werden** (siehe Section 3) |
| **SKILLS** | Verlassen den Kontext | **MÜSSEN neu geladen werden** (siehe Section 3) |

## 3. Payload-Logging (Komprimierungs-Safety-Net)

**SOG:** Dokumentiere JEDES Laden einer conditional-Datei (Storage oder Skill) in der `walkthrough.md`, DENN nach einer Kontext-Komprimierung sind diese Dateien nicht mehr im aktiven Kontext und müssen bei Bedarf neu geladen werden.

**Format in `walkthrough.md`:**
```markdown
## Payload-Log
- [09:45] `50_supabase.md` geladen (conditional: Supabase-Task)
- [09:50] `51_framer_motion.md` geladen (conditional: Animation-Task)
- [10:00] ⚠️ Kontext-Komprimierung erkannt → Payloads neu geladen: `50_supabase.md`, `51_framer_motion.md`
```

**Nach einer Komprimierung MUSS der Agent:**
1. Die `walkthrough.md` lesen und prüfen, welche Payloads er bereits geladen hatte.
2. Die Brain-Dateien (`implementation_plan.md`, `task.md`) lesen, um den aktuellen Stand zu verstehen.
3. Entscheiden: Welche Payloads brauche ich für die **nächste** Aufgabe neu?
4. Diese Payloads neu laden und im Payload-Log vermerken.

## 4. Brain-Dateien als Anker

**SOG:** Die drei Brain-Dateien sind dein permanenter Anker durch den gesamten Session-Zyklus, DENN sie werden regelmäßig aktualisiert und überleben Komprimierungen, während flüchtiger Kontext verloren geht.

| Datei | Zweck | Update-Frequenz |
|:--|:--|:--|
| `implementation_plan.md` | Was ist geplant? Wie ist der Stand? | Bei jedem Meilenstein |
| `task.md` | Was ist erledigt, was offen? | Bei jedem Task-Abschluss |
| `walkthrough.md` | Was wurde wirklich getan? + Payload-Log | Nach jedem Tool-Call |

**Versionierung:** Bei Session-Start werden die Brain-Dateien versioniert (z.B. `task_v20260522_abc123.md`). Details in `DOCS/plans/versioning.md`.

**Diese Dateien werden vom SessionStart-Hook (`.claude/hooks/inject-context.cjs`) injiziert** und bleiben auch nach Komprimierung verfügbar.

## 5. Skill-Nutzungs-Mandat

Skills sind **Router, keine Archive**. Befolge bei komplexen Skills diesen Workflow:
1. `SKILL.md` scannen (YAML & Context-Block, max. 50 Zeilen)
2. Phase in der Bedingungs-Matrix identifizieren
3. **NUR** die Dateien laden, die für diese Phase geroutet sind
4. Ergebnis mit dem Example vergleichen, bevor du zur nächsten Phase gehst

**Verboten:** Blindes Laden aller Skill-Dateien auf einmal.

## 6. Storage-Nutzungs-Mandat

Storage-Dateien werden **nicht** automatisch geladen. Der Agent MUSS aktiv den Index (`DOCS/routing/_index.md`) konsultieren, wenn ein Task eine Kategorie betrifft, die nicht in den Docs abgedeckt ist.

- "Baue eine animierte Hero-Sektion" → LIES `DOCS/routing/_index.md` → LADE `62_animation.md`
- "Konfiguriere Supabase Auth" → LIES `DOCS/routing/_index.md` → LADE `50_supabase.md`
- "Erstelle einen Sub-Agenten" → LIES `DOCS/routing/_index.md` → LADE `30_sub_agent_prompting.md`

## 🔗 Light Router
- **WENN** du die Docs/Storage/Skills-Definition brauchst ➔ **LIES** `00_docs_storage_definition.md`
- **WENN** du die Skill-Matrix (welcher Skill für welchen Task) brauchst ➔ **SIEHE** `00_skill_matrix.md`
- **WENN** du den vollständigen Rule-Index brauchst ➔ **LIES** `DOCS/routing/_index.md`
