# GRUNDREGEL-BUNDLE — Basisregeln für alle Repos

> **Version:** 0.1 · **Status:** ENTWURF (Kuration durch Operator ausstehend)
> **Bereitstellung:** Diese Datei liegt EINMAL zentral hier und wird per absolutem Pfad
> in die `.claude/context-inject.json` aller Repos injiziert (SessionStart-Hook GEN 2).
> **Pfad ist stabil — NICHT verschieben/umbenennen**, ohne alle Listen anzupassen.
> **Repo-spezifische Regeln** gehören NICHT hierher, sondern in die Dateiliste des
> jeweiligen Repos (nach gezielter Prüfung der Alt-Regeln, siehe Task
> `Workbench/DESK/TASKS/active/2026-07-14_Altregeln-Review-pro-Repo_Task.md`).

---

## G1: Prompt ausführen, nicht analysieren

Ein vom Operator geposteter Prompt wird **ausgeführt**, nicht vorab analysiert oder
kritisiert. Ausnahme: Der Operator fragt explizit nach einer Analyse.

## G2: cp + edit statt write

Bestehende Dateien und Living Files werden **nie** blind überschrieben:
erst kopieren bzw. lesen, dann per Edit ändern. `write` nur für komplett neue Dateien.

## G3: Konservierung — nichts löschen

Nichts wird gelöscht. Verschieben in Quarantäne/`ARCHIVE/<name>_<YYYY-MM-DD>/` und
Protokoll-Eintrag (falls das Repo eines führt). Vor jedem Schreibzugriff auf fremde
oder System-Daten: vollständiges, verifiziertes Backup.

## G4: Max zwei Trial-and-Error-Schleifen, dann Recherche-Pflicht

Nach spätestens zwei gescheiterten Versuchen: **breite** Web-Recherche (mehrere
Formulierungen, deutsch UND englisch, GitHub-Issues/Foren/Blogs — nicht nur Doku).
Besser sofort einen Recherche-Subagenten losschicken.

## G5: Subagenten vollständig briefen, Modell explizit setzen

Subagenten starten kalt (kein CLAUDE.md). Briefing immer mit MISSION / CONTEXT /
SCOPE+VERBOTE / OUTPUT. `model:` immer explizit wählen (mechanisch → klein,
Urteil/Architektur → stark).

## G6: Kein Commit ohne Operator-GO

Conventional Commits, keine Emojis, `git diff --cached` vor dem Commit prüfen.
Standard-Account: `24-firon` (MIT Bindestrich; `24Firon` ist ein anderer Account).

## G7: Namenskonvention

`_` trennt Felder, `-` verbindet Wörter: `<Feld1>_<Feld2>_<YYYY-MM-DD>.ext`.
Verboten: Leerzeichen, Em-/En-Dashes (—/–), führender Bindestrich. Datum immer ISO
als eigenes Feld.

## G8: Signal-Protokoll

`?????` = sofort direkt antworten, keine Tools · `!!!!!`/`STOPP` = anhalten,
berichten, warten · `GO` = weiter.

## G9: Keine stillen Fehler

Jeder Tool-Fehler wird gelesen und gemeldet, nie mit "Erfolg" übertüncht. Blocker
sofort transparent machen statt eigenmächtig Workarounds zu bauen. Niemals behaupten,
etwas getan zu haben, das technisch anders gelöst wurde.

---

*Quellen v0.1: globale CLAUDE.md (festgesetzte Regeln 2026-07-13), Workbench
`AGENT_REGELN.md` (ENTWURF v1.0), Workbench-CLAUDE.md-Kernregeln. Kuration und
Erweiterung: Operator.*
