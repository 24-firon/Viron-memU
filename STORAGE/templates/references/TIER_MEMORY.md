<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht:**
>
> - 4-Tier-Shrink-Protokoll für historische Handover-Dateien
> - Archive-First, Shrink Later (eisernes Gesetz)
> - Tier-Definitionen (1 Gegenwart bis 4 Abgeschlossen)
> - Was niemals geschrumpft werden darf
>
> - **Wann das Protokoll greift:** Wenn `walkthrough.md`, `task.md` oder andere Handover-Dateien so stark gewachsen sind, dass sie das Token-Fenster belasten.
>
> - **Bundle-Verwendung:** Diese Datei wird NICHT in die Arbeitskopie kopiert — sie ist systemisch.
<!-- TEMPLATE-EXPLANATION-END -->

# TIER MEMORY — 4-Tier-Shrink-Protokoll

> **Zweck:** Kondensiert historische Handover-Dateien ohne Wissensverlust.
> **Regel:** Archive-First, Shrink Later. Niemals direkt kürzen.

---

## WANN DAS PROTOKOLL GREIFT

Wenn `walkthrough.md`, `task.md` oder andere Handover-Dateien so stark gewachsen sind, dass sie das Token-Fenster belasten.

---

## DAS EISERNE GESETZ: ARCHIVE-FIRST, SHRINK LATER

Bevor du auch nur EIN WORT löschst:

1. **Sichern:** Vollversion in `ARCHIVE/` mit Datumsstempel speichern
2. **Review:** Entwurf der gekürzten Datei erstellen — welche Abschnitte in welche Tier-Stufe?
3. **Approval:** Operator MUSS den Entwurf prüfen
4. **Commit:** Nach Shrink sowohl Archiv-Kopie als auch gekürzte Datei committen

---

## DIE 4 TIER

| Tier | Status | Format | Verbleib |
|:---|:---|:---|:---|
| **1 (Gegenwart)** | Aktueller Sprint | Code-Schnipsel, Terminal-Outputs, volle Details | Bleibt in aktiver Datei |
| **2 (Jüngste Vergangenheit)** | Letzte 1-2 Sprints | Bulletpoints: Was wurde gemacht? Welche Systeme betroffen? | Bleibt in aktiver Datei |
| **3 (Ältere Historie)** | Nur kontextuell relevant | EXAKT 2 Sätze: Warum wurde es entwickelt? Welchen Einfluss hat es aktuell? | Bleibt als "Echo" |
| **4 (Abgeschlossen)** | Inaktiver Ballast | Aus aktiver Datei ENTFERNT (erst nach Archiv-Sicherung, Archive-First), Pointer auf Archiv-Kopie bleibt | NUR in archivierter Vollversion — nie ersatzlos gelöscht (Gesetz 1) |

---

## WAS NIEMALS GESCHRUMPFT WERDEN DARF

- `implementation_plan.md` — hält nur die reine Zukunft; ein abgeschlossener Punkt wird NICHT ersatzlos gelöscht, sondern wandert vorher in den `walkthrough` (die real durchgeführte Version) bzw. in die Archiv-Kopie, **DENN** Konservierungsgesetz 1 (KEINE LÖSCHUNG) gilt auch hier — der Plan bleibt nur deshalb schlank, weil das Erledigte an anderer Stelle bewahrt ist, nicht weil es verschwindet.
- `DOCS/Lexicon/` Dateien — Gehören dem Operator
- `my*` Dateien — Persönliches Wissen des Operators

---

## VORHER / NACHHER BEISPIEL

**Vorher (Tier 4, 200 Zeilen):**
```
## 2025-12-15 — Bugfix Session
- Runde 1: Test geschrieben, gefailed
- Runde 2: Edge case gefunden, gefixt
- ... 200 Zeilen ...
```

**Nachher (Tier 4, 1 Zeile in aktiver Datei):**
```
## 2025-12-15 — Bugfix Session
Details: ARCHIVE/2025-12-15_SESSION.md
```

**Archiv-Datei (Tier 4) enthält die volle 200-Zeilen-Version.**

---

## GOLDENE REGEL

**Im Zweifel: Nicht shrinken.** Eine zu große Datei ist weniger schlimm als verlorene Information.
