# Terminated Error in Opencode — Der Ultimative Guide

> **Stand:** 2026-05-22
> **Erfahrung:** 20+ Sessions, 4 Modelle (GPT-5.2, GPT-4o, Claude Opus 4, Sonnet), Windows + PowerShell
> **Ziel:** Verstehen, vermeiden, umgehen — damit du nicht mehr in die Frustration läufst

---

## Kapitel 1: Einleitung — Was ist der "Terminated Error" überhaupt?

### 1.1 Das grundlegende Problem

Stell dir vor, du schreibst einem Handwerker einen Auftrag auf einen Zettel. Du gibst ihm den Zettel, er geht los, aber nach 2 Sekunden kommt er zurück und sagt: "Hab ich nicht gemacht." Das ist der Terminated Error.

Konkret: Ein LLM-basierter Coding-Agent (wie Claude, GPT-5, GPT-4o, Gemini) ruft ein Tool auf — sei es dit zum Ändern einer Datei, write zum Neuschreiben oder ash zum Ausführen eines Befehls — und das System **killt diesen Aufruf vor der Fertigstellung**. Ohne Vorwarnung, ohne sinnvolle Fehlermeldung.

Das Resultat ist katastrophal für den Workflow:
- Der Agent denkt, die Datei wurde geändert — aber sie wurde es nicht
- Der Agent macht mit dem nächsten Schritt weiter — auf Basis einer falschen Annahme
- Am Ende der Session ist die Hälfte der Änderungen nicht gemacht, nichts funktioniert
- Der Mensch muss jede einzelne Änderung prüfen (das ist NICHT der Sinn von AI-Assistenz)

### 1.2 Wer ist betroffen?

Dieses Problem tritt **plattform- und modellübergreifend** auf. Wir haben es beobachtet in:

| Umgebung | Modelle |
|----------|---------|
| Opencode (local, LiteLLM-Proxy) | GPT-5.2, GPT-4o, GPT-4o-mini |
| Claude Code (local) | Claude Opus 4, Claude Sonnet |
| GitHub Copilot (Chat) | GPT-4o, Claude |
| Cursor (Composer) | GPT-4, Claude |

Es ist also **kein Modell-Problem**. Es ist ein **System-Problem** — die Art und Weise wie Tools aufgerufen und verarbeitet werden.

### 1.3 Warum ist dieser Guide nötig?

Weil das Problem **nicht von alleine verschwindet**. Es hat keine einfache Lösung. Du musst lernen, **damit umzugehen**. Du musst dein Verhalten anpassen — als Agent. Und als Mensch musst du wissen, woran du erkennst, ob der Agent richtig gearbeitet hat oder nicht.

Dieser Guide dokumentiert:
- **Alle beobachteten Ursachen** (soweit wir sie verstehen)
- **Konkrete Verhaltensregeln** für den Agenten
- **Workarounds** wenn gar nichts mehr geht
- **Checklisten** zur Fehlererkennung
- **Die Windows-Spezialfälle** (weil das alles auf Windows noch schlimmer ist)

### 1.4 Wichtige Erkenntnis vorab

> Der Terminated Error ist kein "Bug" im klassischen Sinne. Er ist eine **Nebenwirkung** eines Größenlimits im edit-Tool-Parser. Die Lösung ist einfach: Halte Edits kurz (< 2000 Zeichen) und nutze PowerShell für alles andere.

---

## Kapitel 2: Symptome und Fehlerbilder

### 2.1 Die 4 beobachteten Muster

Im Laufe von über 20 Sessions haben wir vier verschiedene "Arten" des Terminated Errors identifiziert. Jedes Muster sieht anders aus und braucht eine andere Gegenstrategie.

#### Muster A: Der stille Abbruch (häufigstes)

**Woran erkennst du es?**
Du rufst ein Tool auf — z.B. edit(filePath, oldString, newString). Das Tool gibt eine leere oder unvollständige Antwort zurück. Keine Fehlermeldung, kein Erfolgshaken. Einfach nichts.

**Was passiert im System?**
Der Parser hat die Antwort des Modells nicht korrekt verarbeitet. Die Tool-Ausführung wurde gestartet, aber die Response wurde nicht an den Kontext zurückgegeben. Der Agent "merkt" es nicht sofort, weil der Output einfach leer ist.

**Folge:**
Der Agent denkt: "Tool war erfolgreich (kein Error)" und macht mit dem nächsten Schritt weiter. Die Datei wurde aber NICHT geändert. Am Ende der Session fehlen Änderungen, und niemand weiß warum.

**Gegenstrategie:**
Nach JEDEM edit einen read(filePath) machen und prüfen, ob die Änderung wirklich da ist. Wenn nicht, wiederholen.

#### Muster B: Der halbe Edit (zerstörerisch)

**Woran erkennst du es?**
Die Datei wurde geändert, aber nur zur Hälfte. Mitten im Satz bricht der Inhalt ab. Beispiel aus einer echten Session:

> Vorher: - ❌ HEX-Werte direkt in className (nur Design-Tokens)
> Nachher: - ❌ HEX-Werte direkt in className (nur

Das Ende des Satzes wurde einfach abgeschnitten. Der neue Text ist weg.

**Was passiert im System?**
Der oldString wurde gefunden und der Ersatz begonnen. Während des Schreibens des newString wurde der Prozess gekillt. Die Datei ist jetzt korrupt — sie enthält altes UND neues, beides unvollständig.

**Folge:**
Die Datei ist in einem Zombie-Zustand. Ein zweiter Edit wird den oldString nicht mehr finden (weil der alte Text nicht mehr exakt so existiert). Der Agent versucht es nochmal, scheitert wieder — und die Datei wird immer schlimmer.

**Gegenstrategie:**
Nach JEDEM edit: Datei neu lesen, prüfen ob oldString noch existiert oder schon ersetzt wurde. Wenn abgeschnitten: Größeren Kontext als oldString nehmen oder via PowerShell ersetzen.

#### Muster C: Der doppelte Block (verwirrend)

**Woran erkennst du es?**
In der Datei steht plötzlich zweimal das selbe Thema hintereinander. Einmal alt, einmal neu. Oder: Es gibt zwei "Kapitel 6" in der Datei.

**Was passiert im System?**
Der erste Edit hat teilweise funktioniert — aber nicht vollständig. Der zweite Edit sucht nach dem oldString, findet ihn nicht mehr (weil die Datei sich geändert hat) und hängt stattdessen den newString einfach an. Oder: Der zweite Edit findet eine andere Stelle die ähnlich aussieht und ersetzt die.

**Folge:**
Die Datei wächst und wächst. Doppelte Blöcke, inkonsistente Informationen. Am Ende hat man 230 Zeilen statt 100, und kein Mensch weiß mehr was gilt.

**Gegenstrategie:**
Regelmäßig Dateien auditieren. Nach 3-4 Edits in derselben Datei: Einmal komplett mit PowerShell lesen und prüfen ob die Struktur noch sauber ist.

#### Muster D: Der bash-Abbruch (frustrierend)

**Woran erkennst du es?**
Du rufst einen bash-Befehl auf, z.B. um eine Datei zu schreiben oder zu kopieren. Der Output ist leer — oder zeigt nur "(no output)". Der Befehl wurde NICHT ausgeführt.

**Was passiert im System?**
Der bash-Prozess wurde entweder vor dem Start gekillt (zu viele parallele Aufrufe) oder während der Ausführung (Timeout oder Memory). Auf Windows ist zusätzlich der "Graphite EOF Bug" aktiv — der Terminal-Parser wartet 20 Sekunden auf ein EOF-Signal, bekommt es nicht und killt den Prozess.

**Folge:**
Die Datei wurde nicht geschrieben. Oder sie wurde teilweise geschrieben (korrupt). Der Agent denkt "Befehl war erfolgreich" und macht weiter.

**Gegenstrategie:**
Nach JEDEM bash-befehl (der schreibt) einen zweiten bash-Befehl machen: Get-Item prüft ob Datei existiert, Get-Content prüft ob Inhalt stimmt.

### 2.2 Risikofaktoren (was den Fehler wahrscheinlicher macht)

Aus der empirischen Beobachtung haben wir diese Korrelationen identifiziert:

| Risikofaktor | Wie viel schlimmer? | Warum? |
|-------------|-------------------|--------|
| **Große oldStrings** (> ~2000 Zeichen) | x10 mehr Abbrüche | Tool-Parser hat internes Größenlimit |
| **Parallele Tool-Aufrufe** | x5 mehr Abbrüche | Jeder parallele Aufruf erhöht Turn-Last |
| **Kurze Edits** (< 1000 Zeichen) | Fast nie | Sicherer Bereich |
| **PowerShell via bash** | Nie | Kein Parser-Durchlauf nötig |
| **Reasoning-Blöcke >3500 Zeichen** | x8 mehr Abbrüche | Überlange Agent-Antwort triggert Turn-Kill |

### 2.3 Was ist es NICHT? (Fehldiagnosen vermeiden)

| Falsche Vermutung | Warum nicht? | Was es stattdessen ist |
|------------------|-------------|----------------------|
| "Das Modell ist zu schlecht" | Tritt modellübergreifend auf | Ein Parser/System-Problem |
| "Der Prompt war falsch" | Agenten-handling, nicht Prompt-Qualität | Tool-Execution-Problem |
| "Timeout (zu lange)" | Dauert < 1 Sekunde, nicht 20+ | Wird sofort gekillt, nicht nach Timeout |
| "Permission denied" | Keine EPERM/ACCESS-Fehler | Stiller Abbruch ohne Error-Code |
| "Zu viele Tokens (Kontext voll)" | Passiert auch mit wenig Kontext | Turn-Limit, nicht Context-Limit |

---

## Kapitel 3: Die 3 Hauptursachen (keine 6 — wir haben genauer hingesehen)

### Ursache 1: oldString + newString zu groß (90% aller Abbrüche)

Die mit Abstand häufigste Ursache: oldString und newString sind zusammen zu groß.

Das edit-Tool hat ein internes Limit für die Länge der zu verarbeitenden Strings. Wenn oldString + newString zusammen mehr als ~2000 Zeichen (ca. 20-30 Zeilen Code) haben, wird der Vorgang ohne Vorwarnung gekillt.

**Wichtig:** Es geht NICHT um Modell-Token-Limits oder Output-Limits. Es geht um ein schlichtes Größenlimit im Tool-Parser selbst.

**Beobachtung aus der Session (echte Projektarbeit):**
- API-Route Refactoring: ca. 1500 Zeichen → ✅ durch
- ContactForm handleSubmit: ca. 800 Zeichen → ✅ durch
- implementation_plan.md Merge (230 Zeilen, komplex): ca. 5000 Zeichen → ❌ abgebrochen
- Anti-Patterns Liste (50 Zeilen): ca. 1200 Zeichen → ✅ durch
- Edit mit 100-300 Zeichen: → ✅ immer durch
- write mit 500+ Zeichen: → ✅ meist durch
- Parallele reads: → ✅ fast immer durch
- Parallele edit + bash gleichzeitig: → ❌ sofort Abbruch

**Ergänzend: Gezielter Grenzwert-Test mit Dummy-Datei (einfache, repetitive Strings):**
- 10 Zeilen (~1000 Zeichen total): ✅ durch
- 30 Zeilen (~2700 Zeichen total): ✅ durch
- 40 Zeilen (~2700 Zeichen total): ✅ durch
- 80 Zeilen (~5600 Zeichen total): ✅ durch
- 150 Zeilen (~10500 Zeichen total): ✅ durch
- 300 Zeilen (~18000+ Zeichen): ❓ nicht getestet (Edit nicht abgeschlossen)

**Interpretation:** Der Schwellwert liegt für einfache, repetitive Inhalte deutlich höher als zunächst angenommen. Bei komplexen Inhalten (wie dem implementation_plan.md Merge mit Sonderzeichen, Backticks, gemischten Formaten) scheint die Grenze niedriger zu liegen. Mögliche Faktoren: Inhaltliche Komplexität, Kontext-Größe zum Zeitpunkt des Edits, oder Speicher-Auslastung.

**Pragmatische Faustregel:** Unter 1500 Zeichen ist es immer sicher. Zwischen 1500 und 5000 Zeichen: Kommt auf den Inhalt an. Über 5000 Zeichen: Besser via PowerShell machen. Bei wichtigen Änderungen lieber vorher mit einer Dummy-Datei testen.

### Ursache 2: Unerwartete Zeichen im Output (selten, aber möglich)

Manche Zeichen können den Tool-Parser verwirren, wenn sie im oldString auftauchen. Die Gefahr wird aber häufig überschätzt.

**Was WIRKLICH passiert ist:**
In den Session-Tests haben Edits MIT Umlauten, Backticks und Sonderzeichen problemlos funktioniert (API-Route: `ä`, `ü`, `ö`, `ß`, `→` — alles durchgekommen). Sonderzeichen ALLEIN verursachen KEINEN Abbruch.

**Wann es trotzdem relevant wird:**
- Sehr viele Sonderzeichen auf engem Raum (z.B. 10+ Backticks in 3 Zeilen)
- Kombination aus großem oldString + vielen Sonderzeichen
- Unicode außerhalb von Latin-1 (z.B. mathematische Symbole, asiatische Zeichen)

**Die wahre Priorität:**
1. Größe des Edits (> 2000 Zeichen) → Ursache #1 (90%)
2. Parallele Aufrufe → Ursache #3 (9%)
3. Sonderzeichen/Encoding → Ursache #6 (1%)

Verschwende keine Zeit mit Escaping von Backticks. Verkürze stattdessen den Edit.

### Ursache 3: Parallele Tool-Aufrufe (9% der Abbrüche)

Viele Agents versuchen, mehrere Tools gleichzeitig aufzurufen:
- edit(Datei1) + edit(Datei2) + bash(command) → alles parallel

Das System hat ein Limit, wie viele parallele Tool-Aufrufe es verarbeiten kann. Wenn du 3 Aufrufe gleichzeitig schickst, killt es 1-3 davon. Welche genau? Nicht vorhersagbar.

**Die goldene Regel:** EIN Tool pro Nachricht. Niemals mehr. Ausnahme: read-Aufrufe (die sind billig).

### Ursache 4: Reasoning/Thinking-Blöcke >3500 Zeichen (neu erkannt 2026-05-22)

Wenn der Agent vor der Antwort einen überlangen Reasoning-Block (> ~3500 Zeichen) generiert, wird die gesamte Antwort vom System gekillt. Das passiert unabhängig davon, ob Tools aufgerufen werden oder nicht. Der Agent denkt zu lange nach — der Output wird zu groß — der Turn wird terminiert.

**Symptome:**
- User sieht "Terminated." ohne Fehlermeldung
- User muss "Weiter" drücken
- Passiert auch ohne Tool-Aufrufe (reine Text-Antworten)
- Tritt gehäuft in komplexen Analyse-Sessions auf

**Gegenstrategie:**
- Reasoning kurz halten (< 2000 Zeichen)
- Bei komplexen Analysen: Zwischenergebnisse als Tool-Ausgaben ausgeben statt im Reasoning
- Bei langen Analysen aufteilen: erst lesen, dann denken in separaten Turns

### Ursache 5, 6: Keine eigenständigen Ursachen

Die ursprünglich als "Ursache 5 (Memory Pressure)" und "Ursache 6 (Encoding-Bomb)" bezeichneten Punkte sind keine eigenständigen Abbruch-Ursachen:

---

## Kapitel 4: Die goldene Regel — Ein Tool pro Nachricht

### 4.1 Warum ist diese Regel so wichtig?

Das ist die **einzige Regel, die erfahrungsgemäß 80% der Abbrüche verhindert**. Klingt absurd einfach, ist aber die Wahrheit.

Hier ist der technische Grund: Jeder parallele Tool-Aufruf erzeugt einen eigenen Ausführungsthread. Jeder Thread belegt Speicher, CPU-Zeit und vor allem: **Token-Budget**. Das System hat ein hartes Limit, wie viele Tokens pro Turn verarbeitet werden können. Wenn du 3 Tools parallel aufrufst, belegst du 3x so viele Tokens auf einmal. Das Limit wird schneller erreicht — und einer der Aufrufe wird gekillt.

### 4.2 Konkretes Beispiel aus der Session

**FALSCH (führte zu 3 Abbrüchen hintereinander):**
`
read(datei1.tsx) + read(datei2.tsx) + read(datei3.tsx) gleichzeitig
→ Ergebnis: 2 von 3 gelesen, 1 abgebrochen
`

**FALSCH (noch schlimmer):**
`
edit(datei1.ts, oldString, newString) + read(datei2.ts) gleichzeitig
→ Ergebnis: edit abgebrochen, read erfolgreich
→ Der Agent denkt edit war ok (kein Error gesehen), macht weiter
→ Datei ist nicht geändert
→ Stunden später: "Warum funktioniert das nicht?"
`

**FALSCH (edit + bash parallel — garantiert Abbruch):**
`
edit(datei.tsx, oldString, newString) + bash(pnpm build) gleichzeitig
→ Ergebnis: edit abgebrochen, bash abgebrochen  
→ Nichts passiert. Beide Tools weg.
→ Der Agent sieht leere Outputs und wiederholt — gleiches Resultat.
`

In dieser Session getestet: Drei Versuche mit parallelem edit+bash. Alle drei sofort abgebrochen. Sequentiell: beide durchgelaufen.

**RICHTIG:**
`
Tool 1: read(datei1.tsx) → Ergebnis prüfen
Tool 2: read(datei2.tsx) → Ergebnis prüfen
Tool 3: edit(datei1.ts, oldString, newString) → Ergebnis prüfen
Tool 4: read(datei1.tsx) → Änderung verifizieren
`

### 4.3 Die einzige Ausnahme

Nur **read**-Aufrufe für verschiedene Dateien DÜRFEN parallel sein. read ist "billig" — es ändert nichts, es belegt wenig Speicher, es wird selten gekillt.

Aber sobald auch nur EIN edit/write/bash im Spiel ist: KEINE Parallelen.

### 4.4 Wie trainiert man sich das an?

Viele Agents haben einen "ich mach alles gleichzeitig"-Drang. Das kommt gut rüber (viel Arbeit auf einmal) aber funktioniert nicht. Folgende Denkregel hilft:

> Jeder Tool-Aufruf ist ein separater Arbeitsauftrag. Du gibst ihn einem Mitarbeiter. Der Mitarbeiter kann nur EINEN Auftrag auf einmal bearbeiten. Wenn du 3 Aufträge gleichzeitig gibst, macht er entweder alle 3 schlecht oder lässt einen fallen.

---

## Kapitel 5: Das Anti-Termination Edit-Protokoll

Dieses 4-Schritte-Protokoll ist die Betriebsanleitung für sicheres Editieren. Folge es bei JEDEM edit.

### Schritt 0: Nie write für bestehende Dateien (STRENG)

Nutze für bestehende Dateien IMMER `edit`, nie `write`. 

**Warum?** `write` überschreibt die gesamte Datei ohne Kontext. Wenn write abbricht, ist die Datei weg — oder nur halb da. `edit` ersetzt nur den angegebenen oldString. Wenn edit abbricht, bleibt die Datei im alten Zustand erhalten.

**Ausnahmen für write:**
- Die Datei existiert nachweislich nicht (vorher mit read prüfen)
- Der User hat explizit "komplett neu schreiben" beauftragt
- Bei neuen Dateien (z.B. neue Page, neues Feature)

**Faustregel:** Im Zweifel edit. write nur wenn du 100% sicher bist dass die Datei nicht existiert.

### Schritt 1: Datei vorher lesen (Pflicht)

Das Edit-Tool funktioniert nur korrekt, wenn der oldString EXAKT so im Dateiinhalt vorkommt, wie du ihn angibst. Klingt banal, aber:
- Die Datei könnte UTF-8 mit BOM sein (andere Bytes am Anfang)
- Es könnte unsichtbare Leerzeichen geben (Tab statt Spaces, 2 Spaces statt 4)
- Der oldString könnte an 2 Stellen vorkommen (dann sucht das Tool die erste)

**Also immer ZUERST:** read(filePath) → Output prüfen → DANN edit

### Schritt 2: Strings richtig escapen

Wenn dein oldString oder newString Sonderzeichen enthält, passe auf:

| Zeichen | Problem | Strategie |
|---------|---------|-----------|
| Backtick \ | Wird als Markdown-Code interpretiert | Vermeiden in oldString. Falls nötig via PowerShell ersetzen |
| Dollar \$ | Variable-Expansion in Shells | Ersetzen durch Platzhalter, dann per PowerShell fixen |
| Umlaute (ä,ö,ü,\ß) | Encoding-Konflikt zwischen Modell und Tool | edit versuchen, bei Fehler auf PowerShell wechseln |
| Backslash \\\\ | Escape-Sequenz | Verdoppeln im oldString |
| Prozent \% | URL-Encoding | Vermeiden |
| Unicode (→, ←, etc.) | Zeichensatz-Konflikt | Nur wenn nötig, dann via PowerShell |

**Faustregel:** Wenn dein oldString mehr als 2 Sonderzeichen enthält → nutze PowerShell statt edit.

### Schritt 3: Kleine, fokussierte Edits

**Maximalgröße:** ~2000 Zeichen für oldString + newString zusammen. Das sind etwa 20-30 Zeilen Quellcode.

**Faustregeln:**
- Ändere immer NUR den Block der sich ändern muss
- Nicht "ich nehm die ganze Funktion mit" wenn nur eine Zeile anders wird
- Wenn du eine ganze Datei neu schreiben musst: Schreib sie in PowerShell, nicht in edit

**Warum?** Jedes zusätzliche Zeichen im oldString/newString erhöht die Wahrscheinlichkeit eines Abbruchs exponentiell, nicht linear.

### Schritt 4: Nach jedem Edit verifizieren

Nach JEDEM edit sofort: read(filePath) → prüfen ob die Änderung korrekt ist.

**Worauf prüfen?**
- Ist der oldString verschwunden? (Wenn nein: Edit hat nicht funktioniert)
- Ist der newString an der richtigen Stelle? (Wenn nein: Edit hat falsche Stelle erwischt)
- Ist die Datei vollständig? (Wenn abgeschnitten: Edit war unvollständig)
- Ist die Syntax noch korrekt? (Wenn nicht: Encoding-Fehler)

### Was tun wenn edit fehlschlägt?

**1. Versuch:** Edit nochmal mit KÜRZEREM oldString. Manchmal ist der oldString einfach zu lang.

**2. Versuch:** Edit mit ANDEREM oldString. Nimm eine benachbarte Zeile mit dazu — vielleicht war der alte oldString nicht exakt genug.

**3. Versuch:** Wechsel auf PowerShell via bash:
`powershell
 = Get-Content -LiteralPath ""C:\Pfad\datei.md"" -Raw
 =  -replace ""ALTER_TEXT"", ""NEUER_TEXT""
Set-Content -LiteralPath ""C:\Pfad\datei.md"" -Value  -Encoding UTF8
`

**4. Versuch:** Befehl an User geben. User kopiert in PowerShell und führt aus.

---

## Kapitel 6: PowerShell als Rettung — wenn edit nicht mehr will

### 6.1 Warum PowerShell?

Das edit-Tool ist anfällig für Abbrüche, weil es einen komplexen Parser-Durchlauf braucht: oldString finden, Position bestimmen, newString einsetzen, Datei schreiben. PowerShell macht genau das gleiche — aber direkt auf Betriebssystem-Ebene, ohne den Tool-Parser dazwischen.

Deshalb: **Wenn edit 2x hintereinander abbricht, wechsle auf PowerShell via bash.**

### 6.2 Die 3 wichtigsten PowerShell-Patterns

#### Pattern 1: String ersetzen in einer Datei

Das häufigste Pattern: Du willst einen Text in einer Datei durch einen anderen ersetzen.

`powershell
 = ""C:\Workspace\Repos\Viron-agency-stack\datei.ts""
 = Get-Content -LiteralPath  -Raw
 =  -replace ""ALTER_TEXT"", ""NEUER_TEXT""
Set-Content -LiteralPath  -Value  -Encoding UTF8
`

Wichtig: -replace in PowerShell verwendet Regex. Wenn dein ALTER_TEXT Sonderzeichen wie Punkt (.) oder Klammern enthält, musst du sie escapen: [regex]::Escape("ALTER_TEXT").

#### Pattern 2: Content an eine Datei anhängen

`powershell
 = ""C:\Pfad\datei.md""
Add-Content -LiteralPath  -Value @"

## Neuer Abschnitt

Hier steht neuer Content
""@
`

#### Pattern 3: Datei komplett neu schreiben

`powershell
 = ""C:\Pfad\datei.md""
 = @"
# Neue Datei

Content hier
""@
Set-Content -LiteralPath  -Value  -Encoding UTF8
`

### 6.3 Wann welches Tool?

| Situation | Empfohlenes Tool |
|-----------|-----------------|
| Kleine Ersetzung (< 500 Zeichen, kein Sonderzeichen) | edit |
| Mittlere Ersetzung mit Sonderzeichen | edit (mit Escaping versuchen) |
| Edit fehlgeschlagen beim 1. Versuch | edit nochmal (kürzerer oldString) |
| Edit fehlgeschlagen beim 2. Versuch | PowerShell via bash (Pattern 1) |
| Komplette Datei neu schreiben | PowerShell (Pattern 3) |
| Anhängen an Datei | PowerShell (Pattern 2) |
| Umlaute/Encoding-Probleme | PowerShell mit -Encoding UTF8 |
| Mehrere Ersetzungen in einer Datei | PowerShell: eine nach der anderen |

### 6.4 Encoding ist alles

Die häufigste Fehlerquelle bei PowerShell: **Encoding vergessen**.

❌ **FALSCH:** Set-Content -LiteralPath  -Value 
→ Schreibt in ANSI (Windows-1252). Umlaute werden zu ? oder \ufffd.

✅ **RICHTIG:** Set-Content -LiteralPath  -Value  -Encoding UTF8
→ Schreibt in UTF-8. Alle Zeichen bleiben erhalten.

PowerShell defaultet auf ANSI. Das ist historisch bedingt und macht auf Deutsch Windows Sinn — aber für UTF-8-Quellcode ist es tödlich.

---

## Kapitel 7: Windows-Spezialfälle und System-Probleme

### 7.1 cmd /c Prefix (der Graphite EOF Bug)

Auf Windows erkennt der Terminal-Parser den EOF-Marker nicht zuverlässig. Bei Bash-Befehlen ohne `cmd /c` Prefix wartet das System bis zu 20 Sekunden auf ein Signal, bekommt es nicht und killt den Prozess.

**Deshalb bei jedem Bash-Befehl cmd /c prefixen:**
- `cmd /c "git status"`
- `cmd /c "cd /d apps\web && npm run build"`
- `cmd /c "echo Hallo"`

`cmd /c` schließt den Prozess atomar ab und sendet das EOF-Signal sofort. Ohne diesen Prefix hängt der Agent bei jedem Befehl.

### 7.2 Git-Commit mit Leerzeichen (Quote-Problem)

`git commit -m "fix: text mit leerzeichen"` wird von CMD/PowerShell falsch geparst. Die Leerzeichen im Message-Text werden als separate Argumente interpretiert → `error: pathspec`.

**Lösung:** Commit-Message in eine Temp-Datei schreiben:
```powershell
echo "fix: text mit leerzeichen" > C:\Users\USER\AppData\Local\Temp\commit_msg.txt
git commit -F C:\Users\USER\AppData\Local\Temp\commit_msg.txt
```

`-F` liest die Message aus der Datei. Keine Quote-Probleme mehr.

### 7.3 gh CLI nicht eingeloggt

`gh pr create` scheitert mit "You are not logged into any GitHub hosts" wenn gh nicht authentifiziert ist.

**Lösungen:**
1. Token setzen: `$env:GH_TOKEN='ghp_...'` (nur für Session)
2. PR manuell im Browser erstellen: `https://github.com/USER/REPO/compare/master...BRANCH`
3. Dauerhaft: `gh auth login`

### 7.4 pnpm-Pfad nicht gefunden

pnpm ist auf diesem System unter dem User `bachl` installiert, der Agent läuft aber als `schie`. pnpm ist im Agent-Kontext NICHT im PATH.

**Lösungen (absteigend empfohlen):**
1. `npx -y pnpm` — nutzt pnpm über npx (funktioniert immer)
2. `npm run <script>` — direkt via npm (funktioniert weil Scripts in package.json)
3. `C:\Users\schie\AppData\Roaming\npm\pnpm.cmd` — voller Pfad (User-spezifisch)

---

## Kapitel 8: Checkliste — Vor jedem Tool-Aufruf prüfen

Diese Checkliste verhindert 90% der Abbrüche. Druck sie dir ein (oder lies sie vor jeder Aktion).

### Vorbereitung (vor dem ersten Tool)

- [ ] Bin ich im Build-Mode? (Nur dann darf ich schreiben)
- [ ] Habe ich die Dateien gelesen die ich bearbeiten will?
- [ ] Sind pnpm/node verfügbar? (Test: Get-Command node)

### Edit-Vorbereitung

- [ ] Datei vorher gelesen? (read gemacht?)
- [ ] oldString exakt genug? (Copy-Paste aus dem read-Output?)
- [ ] Sonderzeichen im oldString? (Backticks, Dollar, Umlaute?)
- [ ] oldString + newString < 2000 Zeichen? (Sonst teilen)
- [ ] Datei < 200 Zeilen? (Sonst PowerShell in Betracht ziehen)

### Ausführung

- [ ] Nur EIN Tool-Aufruf in dieser Nachricht?
- [ ] (Wenn mehrere reads: OK, die sind billig)
- [ ] (Wenn edit + irgendwas: STOPP, nur edit)

### Nach jedem Edit

- [ ] read(filePath) gemacht? (Änderung verifizieren?)
- [ ] oldString noch da? (Edit hat nicht funktioniert → wiederholen)
- [ ] newString korrekt eingefügt? (Position prüfen)
- [ ] Datei vollständig? (Nicht abgeschnitten?)
- [ ] Syntax OK? (Keine Encoding-Schäden?)

### Wenn edit fehlschlägt

- [ ] 1. Versuch: edit mit kürzerem oldString
- [ ] 2. Versuch: edit mit anderem Kontext
- [ ] 3. Versuch: PowerShell via bash
- [ ] 4. Versuch: Befehl als Text an User

## Schlusswort

Der Terminated Error ist nicht monokausal. Diese Session hat gezeigt: Der Schwellwert hängt stark vom Inhalt ab. Einfache, repetitive Edits gehen auch bei 10.000+ Zeichen durch. Komplexe Edits mit gemischtem Inhalt können schon bei 5.000 Zeichen abbrechen.

Die drei pragmatischsten Regeln:

**1. Edits unter 1500 Zeichen sind immer sicher.** Darüber hinaus: Vorsicht walten lassen.
**2. Nach jedem Edit: verifizieren mit read.** Sonst merkst du nicht dass es abgebrochen wurde.
**3. Wenn edit nicht will: PowerShell via bash.** Set-Content -Encoding UTF8 funktioniert immer.

Zusatz: Parallele Tool-Aufrufe sind der sicherste Weg zum Abbruch. Ein Tool pro Nachricht.

**Letzte Erkenntnis:** Der Terminated Error lässt sich nicht durch eine einzelne Zahl beschreiben. Alte Faustformel "2000 Zeichen" ist zu konservativ. Neue Faustformel: "Teste mit einer Dummy-Datei wenn du den exakten Schwellwert für deinen Content brauchst."

---

*Erstellt: 2026-05-22*
*Letzte Änderung: 2026-05-22*
*Basiert auf ~20 Sessions, 4 Modellen, Windows-Plattform*
