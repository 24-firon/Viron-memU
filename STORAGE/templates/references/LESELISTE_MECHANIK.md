<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# LESELISTE-MECHANIK — Referenz zum Template `templates/P00_LESELISTE.md`

> **Herkunft (2026-07-18, Leseliste-Philosophie (g)):** Dieser Meta-Prozess-Text stand bis heute
> VOLLSTÄNDIG im Leseliste-Template selbst und erdrückte dort den eigentlichen Inhalt („was lesen,
> warum"). Er wurde per Konservierungsgesetz 1 (nichts löschen) hierher AUSGELAGERT — das Template
> behält je Block nur 1-2 Zeilen + Verweis hierher. **Zielgruppe:** der ERSTELLER einer Leseliste
> (Handover-Schritt 6.2) und ein Nachfolger, der die Mechanik im Detail nachschlagen will. Die
> generierte Leseliste selbst bleibt eine kurze, gewichtete Datei-Liste.

---

## 0. Das Leseliste-Prinzip (verbindlich, Operator-Doktrin 2026-07-18)

O-Ton Operator: „eine Leseliste ist alles, was der Agent für das Projekt allgemein wissen muss
und alles, was er für die Task wissen muss. Plus die Regeln … die aber eigentlich automatisch
rein gerückt werden." / „Regeln werden injiziert, die man braucht. … Warum haben wir noch mehr
Regeln, die wir lesen müssen?" / „die Dateien, die man wirklich lesen muss, um diese Aufgaben im
höchsten Maße erfüllen zu können, müssen da halt draufstehen."

1. **Nur zwei Sorten Einträge:** (a) Projekt-Allgemeinwissen, das für DIESE Task relevant ist,
   + (b) task-spezifisches Material. Sonst nichts. **POSITIV formuliert: die Dateien, die man
   WIRKLICH braucht, um die Aufgabe im höchsten Maße zu erfüllen, MÜSSEN vollständig drauf** —
   das ist der eigentliche Zweck der Liste, nicht das Weglassen.
2. **Regeln kommen injiziert — sie stehen NIE als Lese-Aufgabe auf der Liste.** Auto-geladene
   Regeln (Injektion, `CLAUDE.md`-`@`-Imports, native `.claude/rules/`-Mechanismen) werden nur im
   Injektions-Block VERIFIZIERT (2-3 Checkfragen), nie „gelesen". `.opencode/rules/*` und andere
   Alt-/Fremd-Regelsätze gehören GAR NICHT drauf; nur wenn eine Task sie ausdrücklich als
   Kandidaten-Quelle braucht (z.B. Regel-Kuration), als **Task-Material** gekennzeichnet, nicht
   als „Regel".
3. **Immer-gültige Orchestrierungs-Grundlagen** (z.B. `STATE_OF_THE_ART-WORKFLOW.md`) werden NIE
   auf Tier 2 verbannt — sie sind Tier-1-Pflicht ODER (besser) injiziert. Prüffrage: gehört die
   Datei in die `CLAUDE.md`-`@`-Import-Liste, wenn sie in JEDER Session gilt?
4. **Meta-Prozess-Ballast raus aus der Leseliste selbst** — der steht HIER. Die Leseliste bleibt
   eine kurze, gewichtete Datei-Liste mit Ein-Zeilen-Warum + knappem Injektions-Verifikations-Block.

---

## 1. Injektions-Varianten A / B / C (F28 — Vollfassung)

Der Ersteller bestimmt die Variante in INSTRUCTIONS 6.0 (Injektions-Check) und trägt das Ergebnis
in den Injektions-Block der Leseliste ein. Bei TEILWEISE: den Env-Wert eines Hooks tatsächlich
prüfen — ein deaktivierter Hook zählt NICHT als VOLL, auch wenn die Config-Datei noch existiert.

### Variante A — nur wenn INJEKTION=VOLL: „Bereits injiziert — NICHT lesen, VERIFIZIEREN"

> **⚠️ Voraussetzung (B-10-Fix, real erlebt):** Injektion via SessionStart-Hook feuert NUR, wenn
> die Folgesession mit `cwd` IM Ziel-Repo startet. Startet sie versehentlich in einem anderen Repo
> (z.B. weil der User im falschen Chat-Fenster weiterarbeitet), feuert der Hook NICHT — die
> Checkfragen sind dann unbeantwortbar. **In diesem Fall: NICHT als Skill-Fehler werten, sondern
> sofort auf Variante B umschalten** (Tier 1 lesend nachholen) und den cwd-Mismatch im
> Bestätigungs-Block melden (fail-open, aber gemeldet — das ist der korrekte, gelebte Fall B-10).

Die injizierten Inhalte werden im Injektions-Block gelistet (Datei/Block + 1 Zeile Inhalt) und
**nicht nochmal gelesen**. Stattdessen **Verifikation statt Lektüre**: 2-3 Checkfragen zum
injizierten Kontext, die der Nachfolger im Bestätigungs-Block beantwortet.

> **Ersteller-Hinweis (B-10-Fix):** Formuliere die Checkfragen gegen den ECHTEN injizierten
> Inhalt (den du selbst physisch geprüft hast, z.B. per `cat`/`ls` auf die Injektionsquelle) —
> NICHT gegen dein eigenes Sekundärwissen aus dem Chat-Verlauf dieser Session. Sonst sind die
> Fragen auch bei korrekt feuernder Injektion unbeantwortbar, weil sie etwas abfragen, das gar
> nicht im injizierten Set steht.

Kann der Nachfolger sie NICHT beantworten ⇒ die Injektion hat nicht gegriffen (oder
cwd-Voraussetzung verletzt, siehe oben) ⇒ die gelisteten Inhalte LESEND nachholen und das im
Bestätigungs-Block MELDEN (fail-open, aber gemeldet).

### Variante C — nur wenn INJEKTION=TEILWEISE: „CLAUDE.md-Kern automatisch, Rest über Router"

> Ein Repo mit Root-`CLAUDE.md` + `@`-Imports lädt einen fest definierten, aber KLEINEN Kern
> automatisch (typisch 5-10 Dateien) — kein Bundle-Transport wie Variante A, aber auch nicht
> „nichts". Behandle den Kern trotzdem wie Variante A (verifizieren statt lesen, WEIL er
> tatsächlich automatisch da ist) — behandle aber NICHT den Rest des Repos so, als wäre nichts
> automatisch da (das war der Fehler, den diese Variante behebt: vorher lief das als Variante B).

**Verifikation** — wie Variante A: 2-3 Checkfragen gegen den ECHTEN `@`-importierten Inhalt.

**Der Rest ist NICHT automatisch da, aber auch KEINE flache Tier-1-Liste ohne Struktur:** Existiert
im Repo ein STORAGE-Router (z.B. `DOCS/routing/_index.md`, referenziert von
`.opencode/rules/00_routing_protocol.md` Stufe 2), dort nachschlagen und NUR die für DIESE Session
per Task relevanten Zeilen in Tier 1/2 übernehmen — NICHT pauschal den ganzen Router abkopieren
(das wäre wieder Bulk-Injektion durch die Hintertür, exakt das Problem, das Variante A in Claude
Code hatte). Existiert kein Router im Repo: Tier-1-Liste wie in Variante B behandeln (alles aktiv
lesen).

### Variante B — immer (bzw. komplette Liste wenn INJEKTION=NEIN): „Aktiv lesen"

Die Tier-1/Tier-2-Liste der Leseliste. **Doppellese-Verbot:** Was als injiziert (VOLL) oder per
CLAUDE.md automatisch geladen (TEILWEISE) gelistet ist, steht NICHT nochmal in der Leseliste.
Reihenfolge bleibt immer: P00 → P01 → P02.

### Historische Notiz (P00/P01-Nummerierung)

In der OpenCode-Ära hieß das erste Gate `P00_BOOTSTRAP` (Fragen zum injizierten Kontext) und die
Leseliste war `P01`. Beim Claude-Code-Umzug wanderte die Leseliste auf P00, weil Injektion damals
fehlte. Heute ist sie wieder möglich (z.B. SessionStart-Hook) — Variante A holt das alte
Injektions-Gate-Muster als BLOCK in die P00 zurück, die Nummerierung P00→P01→P02 bleibt.

---

## 2. Report-Regel (F27 — hart, Vollfassung)

**NUR der VOLLE Forensic-Report gehört NICHT auf die Leseliste** — er ist die interne Extraktion
der VORGÄNGER-Session (Archiv/Audit), kein Briefing. Auf die Leseliste gehören AUSSCHLIESSLICH
Dokumente, die ausdrücklich FÜR die Folgesession geschrieben wurden: task-passende
Klein-Reports/Derivate, Living Files, Handover-Material. **Prüffrage vor dem Eintragen jeder Datei:**
„Wurde das für den NACHFOLGER geschrieben — oder ÜBER den Vorgänger?" Nur Ersteres kommt auf die Liste.

**Konkrete Beispiele, damit „Derivat" nicht abstrakt bleibt (Fehler real passiert, 2026-07-11:
alle 4 wurden vom Vorgänger weggelassen, obwohl sie F27-konform PFLICHT gewesen wären):**
- Das **SUMMARY-Derivat** (`..._summary.md`) IMMER auf Tier 1 — es ist der next-session-Extrakt,
  nicht der Forensic selbst (siehe `templates/SUMMARY_REPORT.md`).
- **Extraktions-Reports** (`..._extract-voll.md`, `..._extract-casual.md`, `..._extract-select.md`,
  falls per D-003-Prompt erzeugt) gehören ebenfalls auf Tier 1, sofern sie neue, bindende
  Operator-Entscheidungen (O-Töne, D-00X) enthalten, die sonst NIRGENDS sonst auf der Leseliste
  auftauchen — sie sind kein „Forensic über den Vorgänger", sondern eigenständig extrahiertes,
  für die Folgesession bindendes Entscheidungsmaterial.
- Prüf-Heuristik bei Unsicherheit: Enthält die Datei eine Operator-Entscheidung/O-Ton, die NICHT
  bereits vollständig im `decision_log.md` steht? → Tier 1. Ist sie reine Prosa-Nacherzählung
  ohne neue bindende Fakten? → Tier 2 oder Skip.

---

## 3. Drift-Check (PFLICHT vor Tier-1 — Vollfassung mit Befehlen)

**Hat sich das Repo seit dem letzten Handover verändert?**

> **Deterministisch (S-7-Fix 2026-07-17):** Das Datum kommt aus **DEM EIGENEN** HANDOVER
> (`handover/HANDOVER.md` dieser Session) — NICHT aus einem Glob über `WORKSPACE/*/`. Der alte
> Glob nahm `Select-Object -First 1` über ALLE Sessions und zog damit ein **beliebiges** Datum,
> nicht das des Vorgängers (Befund A-6). Bei mehreren Sessions war der Check schlicht falsch.

```powershell
# Eigenes Handover-Datum (der Prompt liegt im selben handover/-Ordner)
$HANDOVER_DATE = (Select-String -Path "$PSScriptRoot/HANDOVER.md" -Pattern "^date:" |
                  Select-Object -First 1).Line -replace '^date:\s*', ''
# Fallback, falls $PSScriptRoot nicht greift (Prompt wurde in den Chat kopiert):
# Datum manuell aus dem YAML-Header des HANDOVER.md ablesen und eintragen.

# Commits seit dem letzten Handover (Repo-Root ist die Basis)
git log --since="$HANDOVER_DATE" --oneline | Select-Object -First 20
```

**Wenn >0 Commits:** WARNUNG an Operator: „Repo hat sich seit HANDOVER verändert. Vor Tier-1
bitte diff mit Vorgänger-Session prüfen."

**Wenn 0 Commits:** Weiter mit Tier 1.

---

## 4. Tier-1-Priorisierungs-Hinweis (historisch, jetzt vom Prinzip §0 abgedeckt)

Alte Template-Formulierung (konserviert): „Tier-1 = Variante B/C (aktiv lesen, ggf. per Router
gefiltert). Was laut Injektions-Block bereits injiziert (VOLL) oder per CLAUDE.md automatisch
geladen (TEILWEISE) ist, ÜBERSPRINGEN (nur verifizieren). Der Rest MUSS explizit gelesen werden —
bei TEILWEISE gefiltert über den STORAGE-Router (siehe Variante C), sonst komplett. Priorisiere:
Verfassung, Routing, Konservierungs-Gesetze, Sicherheit — nicht stumpf alle ~140. Den Rest über
`CLAUDE.md` (Strategy „Aggregator", F9) oder Tier 2 abdecken."

**Einordnung 2026-07-18:** Die Aufzählung „Verfassung, Routing, Konservierung, Sicherheit" meinte
REGEL-Kategorien — nach Prinzip §0.2 stehen Regeln aber gar nicht mehr als Lese-Aufgabe auf der
Liste (sie kommen injiziert). Was von diesem Hinweis bleibt: injiziertes überspringen
(Doppellese-Verbot), Rest gewichtet statt pauschal.
