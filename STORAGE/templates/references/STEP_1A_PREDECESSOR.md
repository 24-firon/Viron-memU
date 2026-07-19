<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- STEP_1A_PREDECESSOR — START-Aktion der FOLGE-SESSION, NICHT Teil der 7 Ende-Schritte des Handover-Skills -->
> **Trigger:** NUR bei Folgesessionen (diese Session hat einen Vorgänger in `WORKSPACE/`).
> **Wichtig — wer führt das aus, wann:** Dies ist eine Aktion, die die FOLGE-SESSION bei IHREM
> EIGENEN START ausführt — sie liest dabei die Living Files ihres Vorgängers. Es ist NICHT Teil der
> 7 Ende-Schritte des Handover-Skills (siehe die CLAUDE.md im Root des aktuellen Arbeits-Repos,
> Abschnitt 7 — bzw. `STRUKTUR_WISSENSBASIS.md` §1, falls keine Repo-CLAUDE.md existiert):
> Der Handover-Skill (der abgebende, am Sessionende laufende Skill) erstellt in seinem
> Schritt 1 nur den leeren `<next-session>`-Ordner; die hier beschriebene Übernahme der
> Vorgänger-Living-Files macht danach die neu gestartete Folgesession selbst, zu Beginn ihrer eigenen
> Session (Zwei-Ordner-Modell, dieselbe CLAUDE.md Abschnitt 2.0 bzw. STRUKTUR_WISSENSBASIS.md §1).
> **Warum ausgelagert:** Spart Zeilen in `INSTRUCTIONS.md` (erste Sessions einer Kette laden es nicht).
> **Wichtig — Struktur-Update:** Der frühere `DESK/build/predecessor/` + `DESK/build/working/`-
> Mechanismus **entfällt vollständig**. Weil Living Files jetzt direkt und flach in
> `WORKSPACE/<session>/desk/` liegen (siehe die CLAUDE.md dieses Repos, Abschnitt 2, bzw.
> `STRUKTUR_WISSENSBASIS.md` §1), ist die Vorgänger-Übernahme
> nur noch: **lies/kopiere aus dem `desk/`-Ordner der Vorgänger-Session.** Kein Zwischenlager mehr
> nötig.

# Schritt 1.3: Living Files aus Vorgänger-Session übernehmen (PFLICHT, falls Folgesession — Start-Aktion der Folgesession selbst)

**WENN** dies eine Folgesession ist (es existiert ein Vorgänger-Ordner in `WORKSPACE/`), DANN MÜSSEN die Living Files aus der Vorgänger-Session gelesen und in diese Session kopiert werden. **Ohne diese Übernahme verliert die Folgesession die Vorgänger-Continuity.**

## 1.3.0 — Board-Claim (Fork-/Parallel-Schutz, G-23 — VOR der Living-Files-Übernahme)

**Warum:** Der Skill kannte bisher keinen Fall, in dem ZWEI Instanzen derselben Session gleichzeitig
existieren (Fork, versehentlicher Parallel-Start desselben Chats). Beide Instanzen würden sonst
konkurrierend am selben `<next-session>`-Bundle und derselben `WORKSPACE/INDEX.md`-Zeile arbeiten,
ohne voneinander zu wissen — das ist real passiert (Session 03).

**Pflicht-Ablauf, bevor irgendetwas geschrieben wird:**
1. Lies die eigene Zeile in `WORKSPACE/INDEX.md`. Steht sie bereits auf Status `aktiv` (nicht
   `geplant`) und trägt sie bereits eine fremde Kennung/einen fremden Zeitstempel? ⇒ **STOPP.**
   Operator fragen: „Läuft eine Parallel-/Fork-Instanz dieser Session?" Kein blindes Weiterarbeiten.
2. Ist die Zeile noch `geplant` (Normalfall): hebe sie auf `aktiv` und trage eine Kennung +
   Zeitstempel ein (z.B. `aktiv (Fable-S5, 2026-07-11 14:32)`), damit eine zweite, später
   startende Instanz den Konflikt in Schritt 1 sofort erkennt.
3. **Handover-Claim:** Existiert der für DIESE Session geplante `<next-session>`-Ordner (aus dem
   eigenen `task.md`/`HANDOVER.md` bekannt) bereits UND enthält bereits Inhalt (nicht nur eine
   leere Hülle)? ⇒ Das deutet auf eine andere, bereits weiter fortgeschrittene Instanz hin.
   **NICHT überschreiben** — Operator-Gate: Zustand melden, auf Entscheidung warten.
4. Eine Session, die sich selbst als Fork/Parallel-Instanz erkannt hat (Schritt 1 oder 3 ausgelöst),
   baut **KEIN eigenes Handover-Bundle** ohne expliziten Operator-Auftrag — sie könnte sonst ein
   bereits von der anderen Instanz geschnürtes Bundle konkurrierend überschreiben.

## 1.3.1 — Vorgänger-Session identifizieren

**Wenn der Vorgänger-Session-Name bereits bekannt ist** (z.B. aus dem HANDOVER.md, das der User in den neuen Chat kopiert hat):

```
VORGÄNGER = WORKSPACE/<vorgänger-session>/
```

**Beispiel** (Namensschema `[TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]`, siehe die CLAUDE.md dieses Repos, Abschnitt 4, bzw. `STRUKTUR_WISSENSBASIS.md` §3):
- Diese Session = `LIVING-FILES_03_SKILL-REBOOT_CDS_2026-07-07` → Vorgänger = `WORKSPACE/WORKSPACE-STRUKTUR_02_SKILL-REBOOT_CDS_2026-07-06/`

**Wenn der Vorgänger-Session-Name NICHT bekannt ist:**

> **Achtung — NICHT nach Ordnername sortieren.** Im aktuellen Schema steht TASK vorne, NN nicht mehr.
> `sort -V`/alphabetische Ordner-Sortierung ist damit NICHT chronologisch und findet den falschen
> Vorgänger. Verbindliche Reihenfolge liefert `WORKSPACE/INDEX.md`, die technische Chronologie die mtime.

1. **Primär — `WORKSPACE/INDEX.md`** (Status-Board, offizielles Living File, siehe die CLAUDE.md dieses
   Repos, Abschnitt 9): die jüngste Zeile mit Status **`übergeben`** oder **`erledigt`** ist der
   Vorgänger.

   > **⛔ `aktiv` ist KEIN Vorgänger (S-2-Fix, 2026-07-17).** Eine Zeile mit `aktiv` ist eine
   > **laufende** Session — womöglich eine Parallel-Instanz. Sie zu „übernehmen" heißt, einer
   > anderen Instanz ins Steuer zu greifen. Ebenso wenig ist `geplant` ein Vorgänger (das ist
   > Zukunft). Beide werden **ignoriert**.
   > **Willst du eine laufende Session fortsetzen** → das ist ein anderer Vorgang:
   > `SESSION_OVERTAKE_PROMPT.md` (Kanon_Rollout), nicht dieser Weg.
   > **Warum der Fix:** Skill und `SESSION_START_PROMPT` §1.2 sagten das Gegenteil voneinander
   > („`übergeben` **oder aktiv**" vs. „`aktiv` → IGNORIEREN") — zwei Wahrheiten im selben System
   > (Befund A-4). Der Prompt hat recht; der Skill zieht hiermit nach.

2. **Fallback — mtime** (falls INDEX.md fehlt/unvollständig):
   ```bash
   ls -dt WORKSPACE/*/ | sed -n '2p'
   # ls -dt = jüngste zuerst; die 2. Zeile = Vorgänger (die 1. ist ggf. der bereits angelegte eigene Ordner)
   ```

## 1.3.2 — Living Files aus Vorgänger-`desk/` lesen

**Pflicht-Reads (mindestens der Pflicht-Kern, Rest falls vorhanden):**

| Datei | Pfad im Vorgänger | Zweck | Pflicht? |
|---|---|---|---|
| `task.md` | `WORKSPACE/<vorgänger-session>/desk/task.md` | Atomare Tasks verstehen | IMMER (Pflicht-Kern) |
| `walkthrough.md` | `WORKSPACE/<vorgänger-session>/desk/walkthrough.md` | Chronologischer Kontext | IMMER (Pflicht-Kern) |
| `decision_log.md` | `WORKSPACE/<vorgänger-session>/desk/decision_log.md` | Architektur-Entscheidungen verstehen | IMMER (Pflicht-Kern) |
| `lessons_learned.md` | `WORKSPACE/<vorgänger-session>/desk/lessons_learned.md` | Lessons Learned nicht wiederholen | NUR falls in Vorgänger-Session angelegt |
| `ideas_future_plans.md` | `WORKSPACE/<vorgänger-session>/desk/ideas_future_plans.md` | Offene Ideen/Aufgaben übernehmen | NUR falls in Vorgänger-Session angelegt |
| `implementation_plan.md` | `WORKSPACE/<vorgänger-session>/desk/implementation_plan.md` | Plan-Stand übernehmen | NUR falls in Vorgänger-Session angelegt |

Zusätzlich sinnvoll: `WORKSPACE/<vorgänger-session>/handover/HANDOVER.md` lesen — dort steht die kuratierte Zusammenfassung samt offener Tasks. Dein eigener Fahrplan liegt bereits als `task.md` in DEINER `desk/` (vom Vorgänger vorbefüllt — D-014: task.md gehört auf den Desk, nicht ins handover/).

## 1.3.3 — Living Files in die eigene `desk/` kopieren (NICHT verschieben)

**Wichtig:** Konservierungsgesetz 1 (KEINE LÖSCHUNG). Living Files werden KOPIERT, nicht verschoben. Ziel ist die eigene, in Schritt 1.2 bereits angelegte `WORKSPACE/<diese-session>/desk/` — **kein Zwischenlager, kein `DESK/build/` mehr.**

```bash
# KORREKT: aus Vorgänger-desk/ direkt in die eigene desk/ kopieren (Vorgänger bleibt unangetastet)
cp WORKSPACE/<vorgänger-session>/desk/task.md              WORKSPACE/<diese-session>/desk/_predecessor_task.md
cp WORKSPACE/<vorgänger-session>/desk/walkthrough.md       WORKSPACE/<diese-session>/desk/_predecessor_walkthrough.md
cp WORKSPACE/<vorgänger-session>/desk/decision_log.md      WORKSPACE/<diese-session>/desk/_predecessor_decision_log.md
# situativ, nur falls im Vorgänger vorhanden:
cp WORKSPACE/<vorgänger-session>/desk/lessons_learned.md    WORKSPACE/<diese-session>/desk/_predecessor_lessons_learned.md
cp WORKSPACE/<vorgänger-session>/desk/ideas_future_plans.md    WORKSPACE/<diese-session>/desk/_predecessor_ideas_future_plans.md
cp WORKSPACE/<vorgänger-session>/desk/implementation_plan.md   WORKSPACE/<diese-session>/desk/_predecessor_implementation_plan.md

# FALSCH: verschieben (Vorgänger-Session verliert Daten)
mv WORKSPACE/<vorgänger-session>/desk/decision_log.md WORKSPACE/<diese-session>/desk/decision_log.md
```

**Namenskonvention für die Kopien:** Präfix `_predecessor_`, damit sie sich nicht mit den frisch aus `LIVING_FILES/`-Templates kopierten, eigenen Living Files dieser Session überschreiben (die eigene `task.md` dieser Session bleibt `task.md`, ohne Präfix). Nach dem Lesen und Einarbeiten der relevanten Inhalte in die eigenen Living Files dieser Session können die `_predecessor_*`-Kopien als Referenz liegen bleiben (kein Löschzwang, Konservierungsgesetz 1) oder — falls der Agent es für sauberer hält — in einen `desk/predecessor_reference/`-Unterordner sortiert werden (erlaubt, siehe CLAUDE.md 2.1/6.3 zu thematischen `desk/`-Unterordnern für Zusatzdateien).

## 1.3.4 — Übernahme-Verifikation

Nach dem Kopieren prüfen:
- [ ] Vorgänger-Session korrekt identifiziert (Ordnername folgt Namensschema)
- [ ] Pflicht-Kern (`task.md`, `walkthrough.md`, `decision_log.md`) aus Vorgänger gelesen
- [ ] Situative Dateien gelesen, falls im Vorgänger vorhanden
- [ ] Kopien liegen als `_predecessor_*` in der eigenen `desk/` (oder in `desk/predecessor_reference/`)
- [ ] **Nicht-Standard-Artefakte (Backlog-8):** Vorgänger-`desk/` KOMPLETT aufgelistet — jede Datei außerhalb der 6 Standard-Living-Files (z.B. `GESAMTKONTEXT.md`, Recherche-Dumps, `EXECUTION_DRAFTS.md`) ebenfalls übernommen ODER dem Operator mit Dateiname + erster Überschrift gemeldet („mitnehmen ja/nein?"). Nichts stillschweigend zurücklassen.
- [ ] Vorgänger-`desk/`-Dateien sind UNVERÄNDERT (Konservierungsgesetz 1)
- [ ] Relevante Inhalte (offene Entscheidungen, Learnings, offene Ideen) sind in die EIGENEN Living Files dieser Session eingearbeitet
- [ ] Diese Session kann ohne Verlust der Vorgänger-Continuity starten

## 1.3.5 — Bei der ersten Session einer Kette (KEIN Vorgänger)

**Wenn dies die erste Session ist oder keine Vorgänger-Session in `WORKSPACE/` existiert:**

Kein Kopiervorgang nötig — die in Schritt 2.1 frisch aus `LIVING_FILES/*.md` (Skill-Templates) kopierten Living Files in `WORKSPACE/<diese-session>/desk/` sind der Startpunkt. Dokumentiere explizit „keine Vorgänger-Session — Startpunkt dieser Kette" im `decision_log.md` (D-001), damit spätere Folgesessionen wissen, wo die Kette beginnt.

## DoD-Kriterien für Schritt 1.3

- [ ] Vorgänger-Session identifiziert (oder „keine Vorgänger" dokumentiert)
- [ ] Pflicht-Kern der Vorgänger-Living-Files gelesen (falls Vorgänger existiert)
- [ ] Alle im Vorgänger tatsächlich vorhandenen Living Files in diese Session kopiert (NICHT verschoben)
- [ ] **Nicht-Standard-Artefakte gemeldet (Backlog-Punkt 8):** kompletten Vorgänger-`desk/` per `ls` aufgelistet; JEDE Datei, die NICHT zu den 6 Standard-Living-Files und nicht zu den `_predecessor_*`-Kopien gehört (z.B. ein `GESAMTKONTEXT.md`, Recherche-Dumps, Entwürfe), dem Operator mit Dateiname + erster Überschrift gemeldet („vermutlich übernehmen — ja/nein?") — Verlust solcher Zusatz-Artefakte darf nie vom zufälligen Zurückblicken abhängen
- [ ] Vorgänger-`desk/` ist unverändert
- [ ] Erste Continuity hergestellt (mindestens `decision_log.md` gelesen und relevante offene Punkte übernommen)
