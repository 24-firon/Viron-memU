# Repo-Map Index - memU

Reine Pfad-Uebersicht dieses Repos. Deterministisch erzeugt, KEIN LLM, KEIN Dateiinhalt.
Ergaenzt den vorhandenen graphify-Code-Graph (der nur parsebaren Code abbildet) um die
VOLLSTAENDIGE Datei-/Ordnerlandschaft.

## Dateien in diesem Ordner

- **FILES.txt** - Flache, sortierte Liste aller relativen Pfade zum Repo-Root (forward slashes,
  eine pro Zeile). Nur Pfade, keine Groessen, keine Zeitstempel, kein Inhalt.
- **TREE.txt** - Verzeichnisbaum (nur Struktur), gerendert aus FILES.txt - garantiert dieselben
  Excludes wie die Pfadliste.
- **DIRS.txt** - NUR Ordnerpfade (alle eindeutigen Verzeichnis-Praefixe aus FILES.txt), sortiert,
  ein Pfad pro Zeile mit abschliessendem `/`. Keine Dateien. Das ist die token-guenstigste
  Struktur-Ansicht - **bevorzugter Einstieg fuer reine Struktur-/Vergleichsfragen** ("welche
  Ordner gibt es", "wie ist das Repo gegliedert"), besonders bei sehr grossen Baeumen, wo
  TREE.txt/STRUCTURE_repomix.txt zehntausende Zeilen haetten.
- **TREE_DEPTH2.txt** - Baum wie TREE.txt, aber Dateien nur bis Ebene 2 (Ordnerstruktur bleibt
  IMMER vollstaendig sichtbar, tiefer liegende Dateien werden pro Ordner zu einer Zaehlzeile
  `… (N Dateien)` zusammengefasst). Guter Mittelweg, wenn DIRS.txt zu grob ist, aber die volle
  TREE.txt zu viel Datei-Rauschen enthaelt - **ebenfalls bevorzugter Einstieg fuer
  Struktur-Fragen**, bevor auf TREE.txt/STRUCTURE_repomix.txt zurueckgegriffen wird.
- **STRUCTURE_repomix.txt** - repomix-Struktur-Ansicht (`--no-files --no-file-summary`), zeigt
  die von repomix erkannte Projektstruktur ohne Dateiinhalte. Bei Fehler/Timeout steht hier eine
  kurze Fehlernotiz statt eines Abbruchs.

## Stand

- Datum: 2026-07-06
- Anzahl Eintraege (Zeilen FILES.txt): 1651
- Git-Repo: True

## Aktualisieren

```
pwsh -NoProfile -ExecutionPolicy Bypass -Command "& 'C:\Workspace\Repos\Context-Dispatcher-System\STORAGE\repo-map-tooling\build_repo_map.ps1' -Only @('memU')"
```

## SPAETER

Inhalts-Digest (repomix --compress) + graphify-Code-Graph als Ergaenzung - noch nicht erzeugt.
