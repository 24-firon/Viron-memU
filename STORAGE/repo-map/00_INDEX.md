# Repo-Map Index - memU

Reine Pfad-Uebersicht dieses Repos. Deterministisch erzeugt, KEIN LLM, KEIN Dateiinhalt.
Ergaenzt den vorhandenen graphify-Code-Graph (der nur parsebaren Code abbildet) um die
VOLLSTAENDIGE Datei-/Ordnerlandschaft.

## Dateien in diesem Ordner

- **FILES.txt** - Flache, sortierte Liste aller relativen Pfade zum Repo-Root (forward slashes,
  eine pro Zeile). Nur Pfade, keine Groessen, keine Zeitstempel, kein Inhalt.
- **TREE.txt** - Verzeichnisbaum (nur Struktur), gerendert aus FILES.txt - garantiert dieselben
  Excludes wie die Pfadliste.
- **STRUCTURE_repomix.txt** - repomix-Struktur-Ansicht (`--no-files --no-file-summary`), zeigt
  die von repomix erkannte Projektstruktur ohne Dateiinhalte. Bei Fehler/Timeout steht hier eine
  kurze Fehlernotiz statt eines Abbruchs.

## Stand

- Datum: 2026-07-06
- Anzahl Eintraege (Zeilen FILES.txt): 1574
- Git-Repo: True

## Aktualisieren

```
pwsh -NoProfile -ExecutionPolicy Bypass -Command "& 'C:\Workspace\Repos\Context-Dispatcher-System\STORAGE\repo-map-tooling\build_repo_map.ps1' -Only @('memU')"
```

## SPAETER

Inhalts-Digest (repomix --compress) + graphify-Code-Graph als Ergaenzung - noch nicht erzeugt.
