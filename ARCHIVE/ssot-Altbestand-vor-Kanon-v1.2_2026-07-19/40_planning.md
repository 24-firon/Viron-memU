---
name: Planning Mandate
description: Plan-Pflicht vor komplexen Tasks, Ambiguity Killer (verbotene Weichmacher), Approval-Gate-Block für destruktive Aktionen, Step-by-Step-Mandat.
trigger: always_on
scope: alle
repo: all
---

# 40_planning.md

> **STATUS:** ALWAYS_ON
> **SCOPE:** Alle Domänen (Factory, Studio, Lab)
> **BLOCK:** 40 — Workflow & Planning

## 1. Plan-Pflicht

**SOG:** Erstelle vor jedem komplexen Task (Research, Refactoring, Feature) einen schriftlichen Plan in `task.md` oder Scratchpad, DENN "Wild Guessing" oder "Blind Execution" ohne Plan produziert fehlerhafte Architektur und kostet den Operator Korrekturzeit.

## 2. Ask-First-Protokoll (Planning Mode)

**SOG:** Im Planning Mode darfst du Projektdateien nicht ohne explizite Freigabe modifizieren, DENN die Sequenz ist: Plan vorschlagen → auf "Proceed" oder "Go" warten → zu Execution wechseln → ausführen.

## 3. Approval-Gate-Block

**SOG:** Vor jeder destruktiven Aktion, jedem Deployment, Datenbank-Drop oder massivem Refactoring MUSST du diesen Block ausgeben und warten, bis der User explizit "Go" bestätigt:

```markdown
⚠️ APPROVAL ERFORDERLICH
Aktion: [exakte Beschreibung]
Betroffen: [Dateipfad / Container / Repository]
Reversibel: JA / NEIN
Backup vorhanden: JA / NEIN
→ Bestätige mit: "Go"
```

## 4. Ambiguity Killer

**SOG:** Definiere Wörter wie "Portierung", "Anpassung", "Bereinigung" explizit, DENN diese Weichmacher führen zu Missverständnissen zwischen Agenten und Operator.

**Verbotene Weichmacher:** "Anpassen" (Worauf?), "Refactorn" (Welches Pattern?), "Optimieren" (Auf welche Metrik?), "Umsetzen" (Nach welchem Spec?).

**Pflicht:** Der Plan muss so präzise sein, dass er als Prompt für einen neuen Agenten dienen könnte, ohne dass Wissen verloren geht.

## 5. Step-by-Step-Mandat

**SOG:** Zerlege komplexe Aufgaben in atomare Schritte, DENN "Implementiere Feature X" ist zu vage für deterministische Ausführung.

**Gebot:**
1. Erstelle Datei X.
2. Füge Funktion Y hinzu.
3. Importiere Z.
4. Validiere mit Test A.

## 6. Ausführlichkeit

**SOG:** Nutze 1000–10.000 Zeichen für Pläne und Erklärungen bei komplexen Themen, DENN Intelligenz ist Integrität — Kompression ist Datenverlust, und kurze Antworten führen zu Ambiguität.

## 🔗 Light Router
- **WENN** du die Read Discipline (50-Zeilen-Regel) brauchst ➔ **LIES** `40_read_discipline.md`
- **WENN** du den Git-Policy (Commits, PR-Revert) brauchst ➔ **LIES** `40_git_policy.md`
