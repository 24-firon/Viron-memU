<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht:**
>
> - Sammlung wichtiger Ideen und Zukunftspläne (NICHT diese Session)
> - Status-Legende (HEUTE bis ARCHIV)
> - Konsolidierungs-Hinweis: Nach 5-10 Sessions in Regeln/Skills integrieren
>
> - **Wann pflegen:** Bei zukunftsweisenden Ideen
> - **Bundle-Verwendung:** Diese Datei wird nach `WORKSPACE/<session>/desk/` kopiert. Sie ist ein TEMPLATE zum Ausfüllen.
<!-- TEMPLATE-EXPLANATION-END -->

# ideas_future_plans.md — Template für Ideen und Zukunftspläne

> **Zweck:** Sammlung wichtiger Ideen und Pläne, die NICHT in dieser Session umgesetzt werden.
> **Wann pflegen:** Bei zukunftsweisenden Ideen, die in späteren Sessions aufgegriffen werden sollen.

---

## Status-Legende

- **HEUTE** — Idee, die in der aktuellen Session umgesetzt werden könnte
- **NÄCHSTE SESSION** — Idee für V2 / V[N+1]
- **SPÄTER** — Idee für zukünftige Sessions
- **ARCHIV** — Idee, die verworfen oder auf unbestimmte Zeit verschoben wurde

---

## Format pro Idee

```
### [YYYY-MM-DD] — [Kurzer Titel]

**Status:** [HEUTE / NÄCHSTE SESSION / SPÄTER / ARCHIV]

**Idee:** [Was ist die Idee?]

**Warum relevant?** [Welches Problem löst sie? Welches Potenzial hat sie?]

**Aufwand:** [Grob geschätzt: Stunden / Tage / Wochen]

**Voraussetzungen:** [Was muss vorher passieren?]

**Mögliche Umsetzung:** [Wie könnte man es angehen? SubAgent-Auftrag? Eigenes Bundle?]
```

---

## Beispiel-Eintrag

```
### 2026-06-07 — Such-Werkzeug für Reports

**Status:** NÄCHSTE SESSION

**Idee:** HTML-Tool / Windows-Popup, das Reports nach Session-Titel im INHALT durchsucht (YAML-Header, Überschriften). Erlaubt kurze Report-Dateinamen bei langen Session-Titeln.

**Warum relevant?** Aktuell sind Report-Dateinamen unhandlich lang, weil sie als Such-Schlüssel dienen. Mit Inhalts-Suche wären kurze Namen möglich.

**Aufwand:** 4-8 Stunden (SubAgent-Auftrag)

**Voraussetzungen:** 
- Reports haben YAML-Header mit `session_title` (gegeben)
- Reports liegen an konsistenten Pfaden (gegeben)
- SubAgent-Skill für Tool-Entwicklung vorhanden (zu prüfen)

**Mögliche Umsetzung:**
- SubAgent (General Agent) spawnt → Tool in Python oder HTML+JS
- Smart-Search: case-insensitive, ignoriert `_`, `-`, Leerzeichen
- Optional: Windows-Popup-Integration via PowerShell
```

---

## [Erste echte Idee hier eintragen]

```
### [DATUM] — [TITEL]

**Status:** ...

**Idee:** ...

**Warum relevant?** ...

**Aufwand:** ...

**Voraussetzungen:** ...

**Mögliche Umsetzung:** ...
```

---

## Konsolidierungs-Hinweis

> Decision Log, Hard-Learned Facts, Ideas werden gesammelt und später in Regeln, Task-Dateien, Skills und ähnliches konsolidiert.
>
> **Konsolidierungs-Zyklus:** alle 5-10 Sessions durchgehen und prüfen, welche Einträge sich zu Regeln/Skills verfestigt haben.
