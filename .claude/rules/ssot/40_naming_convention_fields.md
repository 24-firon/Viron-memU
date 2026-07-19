---
name: naming_convention_fields
description: "_" trennt Felder, "-" verbindet Wörter — in Datei-/Ordnernamen UND generierten Titeln
trigger: Bei JEDER Erzeugung von Dateien, Ordnern, Session-Titeln, Artefakten, Reports
type: core
---
<!-- Kanon v1.2, ausgerollt 2026-07-19 -->

# RULE: Namenskonvention — Feldtrenner vs. Wortverbinder

> **Tier-1-Rollout-Regel (universal)** — Quelle: `src/rules/1_cores/40_naming_convention_fields.md`,
> kuratiert Session 17 (KANON-SYSTEMREPARATUR_17, 2026-07-19).

> **Kanon seit 2026-07-13** (Operator-Entscheidung, Session „Chat-Recovery"). Bestehende
> Altnamen im Ziel-Repo müssen nicht migriert werden — diese Regel gilt für alles **Neue**.

## Rule

Benenne jedes Artefakt nach dem Schema `<Feld1>_<Feld2>_<Feld3>.ext` — **`_` trennt Felder, `-` verbindet Wörter** —, **DENN** ISO-Datumsangaben (`2026-07-12`) enthalten bereits Bindestriche, und wer Felder ebenfalls mit Bindestrich trennt, macht den Namen maschinell unzerlegbar.

```
"_"  trennt FELDER      (Ebene 2 — semantische Einheiten)
"-"  verbindet WÖRTER   (Ebene 1 — innerhalb eines Feldes)
```

## Der Beweis (die Begründung IST die Regel — nicht wegkürzen)

```
RICHTIG:  "CDS-Grundstruktur_2026-07-12".split("_")
          →  ["CDS-Grundstruktur", "2026-07-12"]        ✅ Titel und Datum sauber getrennt

FALSCH:   "cds-grundstruktur-2026-07-12".split("-")
          →  ["cds", "grundstruktur", "2026", "07", "12"]  ❌ Datum zerhackt, Grenze unauffindbar
```

**Das eigentliche Problem ist die Inversion:** Die Zuordnung wird immer wieder **umgedreht** — plötzlich verbindet der Unterstrich Wörter und der Bindestrich trennt Felder. Das ist der Fehler, den diese Regel verhindert. Es geht nicht um Ästhetik.

## Ausnahmslos verboten

| Verboten | Warum |
|:--|:--|
| **Leerzeichen** in Datei-/Ordnernamen | Zerbricht Shell-Aufrufe und jedes naive Parsing |
| **Em-Dash (—) / En-Dash (–)** | Sehen aus wie `-`, sind aber andere Unicode-Zeichen → zerlegen jedes `split("-")` unbemerkt. **Gilt auch für generierte Titel**, nicht nur Dateinamen. |
| **Führender Bindestrich** | Die Shell interpretiert ihn als Flag |
| **Führender Unterstrich** (`_ssot`, `_index.md`) | Operator-Festlegung — gilt für Ordner UND Dateien |

## Positive Guidance — so erzeugst du korrekte Namen

Beim Bauen eines Feldes aus freiem Text:

1. Em-/En-Dash → `-`
2. Leerzeichen → `-`
3. **Vorhandene `_` im Text → `-`** (sonst entsteht eine falsche Feldgrenze!)
4. Mehrfache `-` zusammenfassen
5. Führende `-` / `.` entfernen

Datum immer **ISO** (`YYYY-MM-DD`) und als **eigenes Feld**.

## Angewandtes Beispiel: Session-Titel

```
<HINWEIS>_<Titel>_<Datum>_(fork-n)

Hallo_2026-07-12
AKTIV_CDS-Grundstruktur_2026-07-12
Hallo_2026-07-12_(fork-2)
```

- **Hinweis/Status vorne** (z.B. `AKTIV`, `WIP`, `BLOCK`, `REF`, `DONE`) — der Operator will ihn sehen.
- **Datum hinten** (ISO) — ausdrückliche Operator-Entscheidung.
- **System-Suffixe ganz hinten:** Die Claude-App hängt `(fork 2)` **mit Leerzeichen** an → normalisieren zu `_(fork-2)`, damit es ein sauberes Feld wird.

## Modell-Tier

`min_model_tier: weak`

Diese Regel ist ein **Krückstock**: Ein hinreichend starkes Modell erkennt die Konvention am gelebten Kanon des Repos und braucht sie nicht explizit. Sobald genug korrekt benannte Artefakte existieren, darf sie für starke Modelle abgeschaltet werden.
