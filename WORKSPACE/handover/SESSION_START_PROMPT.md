<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# SESSION_START_PROMPT — M0 Session-Start-Mechanik (generisch, wiederverwendbar)

<!-- ═══════════════════════════════════════════════════════════════════════════
     ERWARTETER REPO-ROOT: C:/Workspace/Repos/memU
     (Optional. Absoluten Repo-Root eintragen — vom Operator oder vom
     Handover-Skill beim Bundle-Bau. Ist er gesetzt, MUSS der per
     `git rev-parse --show-toplevel` ermittelte Root damit übereinstimmen,
     sonst STOPP → siehe 1.1 „Prüfsummen-Block". Leer = Prüfung entfällt.)
     ═══════════════════════════════════════════════════════════════════════════ -->

> **Version:** 2.6 · **Status:** LEBENDES DOKUMENT, versioniert wie die anderen Kanon-Prompts
> (gleicher Ordner: `KANON_STRUKTUR_SPEC.md`, `REPO_ETABLIERUNGS_PROMPT.md`,
> `TEMPLATE_EXTRAKTIONS_PROMPT.md`, `ROLLOUT_BOARD.md`).
>
> **Was das hier ist:** Ein eigenständiger, kopierbarer Startprompt. Der Operator wirft ihn in
> eine NEUE Session im Ziel-Repo. Der Agent macht zuerst NUR Read-Only-Checks, fragt dann:
> „Welcher Task?" — und baut ERST NACH der Task-Vergabe die Werkbank. Die Reihenfolge ist
> immer: **Task → Name → Struktur → kopieren → lesen → anpassen.**
>
> **WICHTIG — Workflow (v2.2, Task-First):**
> 1. Operator postet diesen Prompt.
> 2. **Agent macht NUR Read-Only-Checks** (Kanon-Konformität, Vorgänger identifizieren, `git status` ansehen). KEINE Schreiboperation.
> 3. **Agent meldet den Befund und fragt: „Welcher Task?"** — dann WARTEN.
> 4. Task kommt (i.d.R. als Task-Datei in `DESK/TASKS/active/<TASK>_<YYYY-MM-DD>/task.md` oder als Kickoff-Prompt) → **Agent LIEST die Task-Datei vollständig** → Session-Titel aus dem Task (bzw. Vorgänger-HANDOVER) ableiten.
> 5. **Agent postet einen kurzen Plan im Chat** — welche Ordner er anlegt, was er kopiert, wie er die Task abarbeitet (Kein Blindflug: ankündigen, DANN tun). Kein GO nötig, direkt weiter.
> 6. **JETZT erst** Werkbank anlegen, **Board-Claim (Phase 3.0, Fork-Schutz G-23)**, Vorgänger-Kopien ziehen, Skelette anlegen, INDEX-Zeile verifizieren, **Checkpoint-Commit (Phase 7.1a, UNBEDINGT)** (Phasen 2–7). Kopierte Dateien werden GELESEN und gemäß Task ANGEPASST — kein blindes Kopieren.
> 7. Danach task-spezifische Arbeit gemäß Task-Datei bzw. aufgabenspezifischem Prompt (T0+).
>
> **GATE 0 — HART: Keine Schreiboperation (mkdir/cp/edit/write) vor der Task-Vergabe.**
> Der Ordnername hängt am Task — wer vorher baut, baut Wegwerf-Strukturen und muss umbenennen.
>
> **Alle Pfade sind relativ zum REPO-ROOT** (`git rev-parse --show-toplevel`), NICHT zum cwd.
> `WORKSPACE/` heißt `<repo-root>/WORKSPACE/`. Erster Schritt: Repo-Root bestimmen, dann alles
> dagegen auflösen. Kein cwd-Raten, keine Extra-Regel — der Repo-Root ist die einzige Basis.
> Ein optional gesetzter `ERWARTETER REPO-ROOT` (Kopf oben) dient als **Prüfsumme**, nie als
> Arbeitspfad (1.1).
>
> **🛑 ZWEI HARTE STOPPS (v2.5) — hier wird nicht geraten und nicht gesucht:**
> 1. **`git rev-parse` schlägt fehl** (kein Git-Repo) → STOPP, Operator fragen.
> 2. **`<repo-root>/WORKSPACE/` fehlt/ist leer** → STOPP, melden + fragen (1.3-B). Das Repo ist
>    nicht eingerichtet ODER es ist das falsche Repo — **beides baut dieser Prompt NICHT auf.**
>    Einrichten/Reparieren ist ein eigener Vorgang mit eigenem Prompt.
>
> **Niemals** im Dateisystem nach einem `WORKSPACE/` suchen (kein `C:\`-Scan, keine Eltern-/
> Nachbar-Ordner). Fehlt es am einzig erlaubten Ort, ist es ein Befund — keine Suchaufgabe.
>
> **🔧 Wenn doch etwas schiefgeht → `RECOVERY_PROTOCOL.md`** (gleicher Ordner). Es sagt dir, was du
> **selbst korrigieren darfst** (alles Reversible: getrackt+committet → `git mv`, autonom, ohne zu
> fragen) und was **STOPP** bleibt (falsches Repo, Fork-Instanz, untrackte Daten). Ein Fehler ist
> kein Grund zu eskalieren — nur ein unreversibler ist es.
> Bei sonstigen Unklarheiten (Vorgänger mehrdeutig, Titel unklar): ebenfalls STOPP.
>
> **Einordnung im Kanon:** Entspricht **M0 (Session-Start-Mechanik)** des
> `MILESTONE_GATEWAY` (§2c, Anti-Farce-Gate) und entspricht **Schritt 1a (STEP_1A,
> Vorgänger-Übernahme)**. Dieser Prompt ist die BRÜCKE zwischen dem Ende der
> Vorgänger-Session und dem Start der neuen Session.
>
> **Stufe:** S1–S2 oder SKRIPT (reine Mechanik, kein Reasoning). Anti-Farce-Gate: NICHT auf der
> Planungs-Stufe ablaufen lassen. Der Chirurg wischt nicht den Boden.
>
> **Dauer:** < 5 Minuten bei sauberem Git-Stand.

---

## Wann einsetzen

- Am Anfang **JEDE neuen Session** in einem Kanon-konformen Repo.
- Read-Only-Checks (Phase 1) direkt nach Prompt-Eingang; alles Weitere (Phasen 2–7) **erst
  nach Task-Vergabe** (GATE 0).

## Wann NICHT einsetzen

- **Repo noch nicht kanonisiert:** Weder `WORKSPACE/INDEX.md` noch `WORKSPACE/<session>/desk/`
  existieren → zuerst `REPO_ETABLIERUNGS_PROMPT.md` laufen lassen (Phase I + Phase II).
- **Erste Session im Repo überhaupt:** Es gibt keinen Vorgänger → dieser Prompt springt auf
  **Erststart-Modus** (siehe Phase 1, Sonderfall) — Werkbank wird angelegt, aber es gibt **keine
  `_predecessor_*`-Kopien**. Living-Files-Skelette werden **nur mit Session-Header** erzeugt.
  **WICHTIG: Auch im Erststart-Modus gilt GATE 0 — die EINE Pflichtfrage „Welcher Task?" kommt
  VOR jedem Setup. Kein P01/P02 in M0. Nach der Task-Vergabe: mechanisches Setup (Ordner,
  Skelette, INDEX-Zeile, Git-Check), dann direkt Weiterarbeiten mit dem aufgabenspezifischen
  Prompt — kein weiterer STOPP.**
- **Kein Kanon-konformes Repo:** Bei Nicht-Kanon-Repos (z.B. reine Code-Repos ohne
  Organisationsstruktur) ist dieser Prompt nicht anwendbar — der Operator bekommt einen Hinweis.

---

## WENN STRUKTUREN FEHLEN ODER ALTE HANDOVER-ORDNER VORHANDEN SIND

**Grundregel:** Dieser Prompt kümmert sich nur um M0 der NEUEN Session. Bestehende Strukturen
(alte Handover-Ordner, fremde WORKSPACE-Verzeichnisse, defekte Vorlagen) werden NICHT
repariert, migriert oder zusammengeführt. Das ist Aufräumarbeit und gehört in eine separate
Session mit eigenem Fokus.

| Situation | Verhalten |
|---|---|
| `WORKSPACE/INDEX.md` fehlt, `WORKSPACE/` existiert | Weiterarbeiten; Board in Phase 6 anlegen. Existierende Sessions werden nicht aus dem Nichts rekonstruiert. |
| **`<repo-root>/WORKSPACE/` fehlt oder ist leer** | 🛑 **STOPP — melden + fragen (1.3-B).** Repo ist nicht eingerichtet ODER falsches Repo. **NICHT bauen, NICHT suchen.** Aufbau/Reparatur läuft über das Etablierungs-/Reparatur-Paket, nicht über diesen Prompt. |
| **`git rev-parse` schlägt fehl** | 🛑 **STOPP — Operator fragen.** Kein Git-Repo unter dem cwd. Nicht im Dateisystem nach einem Repo/WORKSPACE suchen. |
| **`ERWARTETER REPO-ROOT` im Kopf ≠ ermittelter Root** | 🛑 **STOPP — falsches Repo.** Beide Pfade melden (1.1 Prüfsummen-Block). |
| Alte Handover-Ordner (z.B. `HANDOVER/`, `WORKSPACE/old_handover/`, `WORKSPACE/_archive/`) vorhanden | In Ruhe lassen. Nicht migrieren, nicht zusammenführen, nicht löschen. |
| `_predecessor_*` aus früheren Overtake-Versuchen vorhanden | Nicht überschreiben. Neuere `_predecessor_*` mit höherer NN (z.B. `_predecessor_v2_*`) sind erlaubt. |
| `STORAGE/templates/` existiert nicht oder ist leer | Den aufgabenspezifischen Prompt trotzdem starten. Der Agent nutzt die Skill-Quellen direkt (Modell B: Skill hat Vorrang, CDS-Mirror ist Fallback). |
| `DESK/TASKS/` fehlt komplett | Im Walkthrough dokumentieren. Nicht selbst anlegen — das ist `REPO_ETABLIERUNGS_PROMPT.md` Phase II Aufgabe. |
| `git status` ist dirty (FREMDE offene Änderungen, nicht aus dieser M0) | Im Walkthrough dokumentieren, kurz anhalten und Operator informieren — fremde Änderungen NICHT eigenmächtig committen. (Der unbedingte M0-Checkpoint-Commit, Phase 7.1a, staget nur die M0-eigenen Artefakte.) |

**Faustregel:** Wenn etwas fehlt, das der Prompt voraussetzt → dokumentieren, nicht reparieren.
Wenn etwas Altes im Weg steht → drumherum arbeiten, nicht aufräumen. Aufräumen ist ein eigener Task.

---

## LEITPLANKEN (hart)

0. **GATE 0 — Task vor Schreibzugriff:** Keine Schreiboperation (`mkdir`, `cp`, `edit`, `write`)
   bevor der Operator den Task vergeben hat. Reihenfolge immer: Task → Name → Struktur →
   kopieren → lesen → anpassen.
1. **STRIKT Mechanik:** Kein Reasoning, keine Analyse. Nur `mkdir`, `cp`, `edit`, `git status`,
   `ls`/`glob`. Wenn denkend, dann nur zum Verifizieren (Datei existiert? Vorgänger richtig?).
2. **Konservierungsgesetze (Kanon §1.2):** KEINE LÖSCHUNG · KEINE REDUKTION · BEWEISPFLICHT ·
   INTEGRATION. Vorgänger-Ordner und dessen Living Files werden NIE `mv`'d, nur `cp`'d.
3. **Anti-Farce-Gate (MILESTONE_GATEWAY §2c):** Stufe S1–S2/SKRIPT. Operator darf nicht mit einem
   Reasoning-Modell Dateien kopieren. Falls der Agent ohnehin auf S4/S5 läuft (weil der
   aufgabenspezifische Prompt das verlangt): für diese M0-Phase das Modell per `/model` senken
   ODER die Phase als deterministisches PowerShell-Skript ausführen.
4. **Operator-Entscheidungen sind decision-log-würdig:** Falls eine Unsicherheit auftritt
   (Vorgänger unklar, Session-Titel unklar, WORKSPACE-Zustand fragwürdig) → STOPP, Operator fragen.
   Keine eigene Entscheidung treffen — M0 ist reine Ausführung, keine Interpretation.
5. **Kein Edit am Vorgänger:** Vorgänger-Living-Files werden ausschließlich READ-ONLY gelesen
   und als Kopie (`_predecessor_*`) in die eigene `desk/` geholt. Vorgänger-Ordner unangetastet.
6. **Keine Skill-Abhängigkeit (geborgen aus v1.1, F5a-Bergung 2026-07-17):** Der Session-Start ist
   eigenständig. Templates und Living-Files werden aus `STORAGE/templates/` bezogen (SSoT-Mirror).
   Der Skill `session_handover_generator` ist für das **ENDE** einer Session zuständig
   (Handover-Paket erstellen), **nicht für den Start** — du musst ihn für M0 NICHT laden.
   **Session-Handover:** Living-Files gehören zum System; am Session-Ende werden sie für den
   nächsten Agenten aufbereitet und die Handover-Dateien erstellt — dann (und nur dann) ist der
   Skill dran.
7. **Aufräumen = eigener Task:** Aufräumarbeiten (Migration, Konsolidierung, Dedup)
   werden NICHT in M0 erledigt. Sie werden als Tasks in `DESK/TASKS/`
   für die **Nachfolgesession** geplant (Priorität, Scope, Dependencies).
8. **Fehler dokumentieren → Task anlegen:** Jede Inkonsistenz, jeder Fehler,
   jedes "unklar" im M0 wird als Task in `task.md` eingetragen
   (Priorität, Beschreibung, Link zum Walkthrough-Eintrag).
9. **Nachfolgesession für Aufräumen planen:** Falls Aufräum-Bedarf erkannt wird,
   Eintrag im Walkthrough: `NÄCHSTE SESSION: Aufräumen [Scope]`.

---

## PHASE 1 — Vorgänger identifizieren (S1, Read-Only)

### 1.1 Repo-Root bestimmen, dann Kanon-Konformität prüfen

```powershell
$root = git rev-parse --show-toplevel     # DER Anker — alles Weitere relativ dazu
Test-Path "$root/WORKSPACE/INDEX.md"
Test-Path "$root/WORKSPACE/"
```

**Maßgebliche Basis = der REPO-ROOT (`git rev-parse --show-toplevel`). PUNKT.**

- Alle relativen Pfade (`WORKSPACE/`, `STORAGE/templates/`, `DESK/TASKS/`) beziehen sich auf
  den Repo-Root, NICHT auf das cwd. Der cwd kann ein Unterordner sein (`…/00_ADMIN/…`) —
  `git rev-parse --show-toplevel` liefert trotzdem den Repo-Root, und genau der ist die Basis.
- So funktioniert der Prompt in JEDEM Repo, ohne absolute Pfade und ohne Sonderregel: relativ
  zum Repo-Root aufgelöst stimmt `WORKSPACE/` überall.

#### Die Auswertung — vier Fälle, alle abschließend geregelt (v2.5)

| Befund | Verhalten |
|:--|:--|
| `WORKSPACE/INDEX.md` **und** `WORKSPACE/` vorhanden | ✅ Kanon-konform → weiter zu 1.2 |
| `WORKSPACE/` vorhanden (mit Session-Ordnern), `INDEX.md` fehlt | ✅ weiter zu 1.2; Board-Lücke im Walkthrough vermerken (Board wird in Phase 6 angelegt) |
| **`git rev-parse` schlägt fehl** (kein Git-Repo / nicht installiert) | 🛑 **STOPP. Operator fragen.** NIEMALS im Dateisystem nach einem `WORKSPACE/` suchen — weder im cwd, noch in Eltern-, Nachbar- oder Laufwerks-Ordnern. Meldung: „Kein Git-Repo unter `<cwd>` — ist das der richtige Arbeitsort?" |
| **`<repo-root>/WORKSPACE/` fehlt** (oder ist leer) | 🛑 **STOPP. Melden + fragen** (siehe 1.3) — **NICHT eigenmächtig aufbauen.** |

> **⛔ ABSOLUTES SUCHVERBOT (v2.5, Wurzel-Fix der „C:\-Workbench-Sucherei"):** Es gibt genau EINEN
> Ort, an dem `WORKSPACE/` liegen darf: `<repo-root>/WORKSPACE/`. Ist es dort nicht, existiert es
> für dich **nicht**. Kein `Get-ChildItem C:\`, kein Durchsuchen von `C:\Viron`, kein Raten, kein
> „vielleicht liegt es ja eine Ebene höher". Ein fehlendes `WORKSPACE/` ist ein **Befund**, den du
> meldest — keine Suchaufgabe, die du löst.

#### Optionaler Prüfsummen-Block: ERWARTETER REPO-ROOT

Hat der Operator (oder der Handover-Skill beim Bundle-Bau) im Kopf dieses Prompts einen
`ERWARTETER REPO-ROOT: <absoluter Pfad>` eingetragen, dann gilt:

```powershell
# Nur ausführen, wenn der Kopf einen ERWARTETER REPO-ROOT trägt:
if ($root -ne $erwarteterRoot) { "MISMATCH — STOPP" }
```

- **Stimmt überein** → alles gut, weiterarbeiten (relativ zum Root, wie immer).
- **Weicht ab** → 🛑 **STOPP.** Du bist im falschen Repo. Melden:
  „Erwartet: `<erwartet>` · Tatsächlich: `<ermittelt>` — bitte klären."
- **Kein Block im Kopf** → übersprin­gen, kein Fehler (der Block ist optional).

> **Warum so:** Relative Pfade bleiben relativ (der Prompt bleibt in jedem Repo einsetzbar).
> Der absolute Pfad ist **nur Prüfsumme**, nie Arbeitspfad. Damit ist beides gleichzeitig wahr:
> portabel UND deterministisch.

---

### 1.2 Vorgänger-Session identifizieren (Normalmodus)

**Einfache Regel:** Suche im `WORKSPACE/INDEX.md` die jüngste Zeile mit `status: übergeben` oder
`status: erledigt`. Nimm diese als Vorgänger.

- `status: übergeben` → idealer Vorgänger (HANDOVER-Bundle existiert in `handover/`)
- `status: erledigt` → auch Vorgänger, aber HANDOVER evtl. nicht vollständig
- `status: aktiv` → **IGNORIEREN.** Das ist eine laufende Session, kein Vorgänger.
- `status: geplant` → **IGNORIEREN.** Das ist eine zukünftige Session, kein Vorgänger.
- Nichts gefunden → **Erststart-Modus**

**Wenn du einen vermeintlichen Vorgänger mit `status: aktiv` oder `status: geplant` findest:**
Nicht übernehmen, nicht entscheiden. Das ist eine andere laufende/geplante Session.
Für Übernahme einer bestehenden Session nutze den separaten `SESSION_OVERTAKE_PROMPT.md`.

**Jüngster = höchstes Datums-Suffix im Ordnernamen** (`…_YYYY-MM-DD`), nicht die letzte
Tabellenzeile. Bei mehreren `übergeben`/`erledigt` am gleichen Datum: nach `TASK` alphabetisch.

### 1.3 Sonderfall: Erststart-Modus

> **⚠️ ZWEI FÄLLE, DIE NICHT VERWECHSELT WERDEN DÜRFEN (v2.5-Klarstellung — bisher vermischt):**
>
> | Fall | Bedeutung | Verhalten |
> |:--|:--|:--|
> | **1.3-A — kein VORGÄNGER** (`WORKSPACE/` existiert, 1.2 findet keine `übergeben`/`erledigt`-Zeile) | Das Repo **kennt das System**; dies ist nur die erste Session darin. | ✅ **Erststart-Modus, wie unten** — bauen ist richtig. |
> | **1.3-B — kein SYSTEM** (`<repo-root>/WORKSPACE/` fehlt ganz oder ist leer) | Das Repo ist **nicht eingerichtet** — oder du bist im **falschen Repo**. | 🛑 **STOPP, melden + fragen** (Block unten). **NICHT bauen.** |

#### 1.3-B — Kein System im Repo: melden und fragen (NICHT aufbauen)

Dieser Prompt ist der **Alltags-Startprompt** für Repos, die den Kanon bereits haben. Das
**Einrichten/Reparieren** eines Repos ist ein eigener, umfangreicher Vorgang mit eigenem Prompt
(`REPO_ETABLIERUNGS_PROMPT.md` bzw. dessen Reparatur-Nachfolger) — mit Ist-Dossier,
Operator-Gate, Checkpoint-Commit und Alt-Bestands-Bergung. **Das kann und darf dieser Prompt
nicht nebenbei erledigen.**

Melde stattdessen im Chat und **warte**:

```
🛑 KEIN SYSTEM IM REPO
Repo-Root:  <ermittelter absoluter Root>
Befund:     <repo-root>/WORKSPACE/ fehlt (bzw. ist leer) → dieses Repo ist nicht kanon-eingerichtet.
Ich habe NICHT gebaut und NICHT gesucht.

Zwei Möglichkeiten:
 (a) Falsches Repo — dann bitte im richtigen Repo neu starten.
 (b) Repo noch nicht eingerichtet — dann ist das Einrichtungs-/Reparatur-Paket zuständig,
     nicht dieser Startprompt.

👉 DU: (a) oder (b)?
```

#### 1.3-A — Kein Vorgänger (Repo IST eingerichtet): normal bauen

- Werkbank wird in Phase 2 angelegt.
- Phase 3.1–3.3 (Vorgänger-Kopien) fallen aus — im Walkthrough notieren: „Erststart-Modus, kein
  Vorgänger". **Phase 3.0 (Board-Claim) gilt AUCH im Erststart-Modus** — existiert noch keine
  eigene INDEX-Zeile (oder kein INDEX), greift der dortige Sonderfall.
- **Kein temporärer Identifier, kein Umbenennen:** Der Task ist zu diesem Zeitpunkt bereits
  bekannt (GATE 0 — „Welcher Task?" wurde VOR Phase 2 gestellt und beantwortet). Der Titel
  wird direkt aus dem Task abgeleitet: `[TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]`.

**⚠️ WICHTIG — ERSTSTART-MODUS REGELN (gelten für 1.3-A):**
- **Genau EINE Pflichtfrage:** „Welcher Task?" — VOR jeder Schreiboperation (GATE 0). Danach
  keine weiteren Fragen, AUSSER bei unklarem Befund (Leitplanke 4: STOPP, Operator fragen).
- **KEIN P01, KEIN P02** werden erzeugt.
- Die Phase-8-Template-Platzhalter (`<vorgänger-titel oder „kein (Erststart)">` etc.) sind **KEINE Fragen** — der Agent füllt sie selbst aus dem Kontext aus.
- **P00/P01/P02 werden NICHT in M0 erzeugt** — sie werden am **Session-Ende** für die **FOLGE-Session** erstellt.
- M0 macht NACH der Task-Vergabe NUR: Werkbank anlegen, Living-Files-Skelette aus lokalen Templates ziehen (cp + edit), INDEX-Zeile schreiben, Git prüfen. **Kein weiterer STOPP nach M0.**

### 1.4 Session-Titel festlegen

- **Normalmodus:** Vorgänger-HANDOVER.md `next_session`-Feld (höchste Autorität).
- **Erststart:** Titel aus dem vergebenen Task ableiten (Task liegt dank GATE 0 bereits vor):
  `[TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]`.
- **NIEMALS einen Titel erfinden** — entweder aus Vorgänger oder aus Task ableiten.

### 1.5 Sub-Agent-Strategie (für Geschwindigkeit, optional)

Die M0-Mechanik ist klein, aber wenn du Graphify- oder Repo-Abbilder im `STORAGE/` oder `.graphify/` findest, nutze **Sub-Agents parallel** für die Erkundung. Mehrere Perspektiven sind möglich:

- **Repo-Abbild-Leser:** Liest `STORAGE/repo-map/` oder `STORAGE/repo-map-tooling/` falls vorhanden — beschleunigt die Strukturerfassung.
- **Graphify-Updater:** Falls `.graphify/` existiert UND veraltet ist, `graphify update` starten. Falls aktuell, direkt nutzen.
- **Verweis-Inventar-Agent:** Bei großen Repos: paralleler `grep`-Sweep für Alt-Pfad-Muster (z.B. `HANDOVER/`, `TASKS/` außerhalb DESK).

**Mehrere Sub-Agents derselben Perspektive sind OK**, wenn das Repo umfangreich ist (CDS hat z.B. 80+ md-Dateien in `src/rules/`). Nutze das große Token-Fenster-Modell für Sub-Agents.

**Aufruf-Schema (4-Säulen-Briefing, Modell B):**
```
MISSION: [Was soll gefunden/analysiert werden?]
CONTEXT: [CDS-Repo, Phase I, welche Strukturen?]
SCOPE+VERBOTE: [Read-only, keine Edits, keine Sub-Sub-Agents]
OUTPUT: [Konkrete Markdown-Tabelle / Datei-Pfad in PLAYGROUND/...]
```

### 1.6 Task entgegennehmen, LESEN, Plan ankündigen (GATE 0 → offen)

Nach der Frage „Welcher Task?" antwortet der Operator — i.d.R. mit einem Verweis auf eine
Task-Datei (`DESK/TASKS/active/<TASK>_<YYYY-MM-DD>/task.md`) oder einem Kickoff-Prompt.

1. **Task-Datei VOLLSTÄNDIG lesen.** Nicht nur den Titel — die Task bestimmt, wie die
   Living Files angepasst werden (Phase 4/5) und was nach M0 kommt.
2. **Session-Titel ableiten** (siehe 1.4) — aus Task-Kürzel bzw. Vorgänger-HANDOVER.
3. **Plan im Chat posten (Kein Blindflug — ankündigen, DANN tun):** kurz sagen,
   welche Ordner angelegt werden, was kopiert wird, wie die Task abgearbeitet wird.
   Kein GO nötig — nach dem Plan direkt mit Phase 2 weitermachen.

Erst NACH diesem Schritt ist GATE 0 offen und Schreiboperationen sind erlaubt.

---

## PHASE 2 — Werkbank-Ordner anlegen (S1, SKRIPT — ERST NACH TASK-VERGABE, GATE 0)

### 2.1 Ordner-Struktur

Im Ziel-Repo (CDS oder anderes Kanon-konformes Repo):

```powershell
$S = "WORKSPACE/<neuer-session-titel>"
$P = "PLAYGROUND"   # falls aufgaben-spezifische Arbeitsordner nötig sind — sonst auslassen

New-Item -ItemType Directory -Force "$S/desk", "$S/handover" | Out-Null
#Optionale aufgabenspezifische Unterordner (z.B. für TEMPLATE-EXTRAKTION):
#New-Item -ItemType Directory -Force "$P/Kanon_Rollout/01_inventur", "$P/Kanon_Rollout/templates" | Out-Null
```

Aufgabenspezifische Unterordner (z.B. `PLAYGROUND/Kanon_Rollout/01_inventur/`) werden vom
aufgabenspezifischen Prompt angelegt, NICHT von diesem Start-Prompt. Dieser Prompt macht nur
`WORKSPACE/<session>/desk + handover`.

### 2.2. DoD Phase 2

- `WORKSPACE/<neuer-session-titel>/desk/` existiert
- `WORKSPACE/<neuer-session-titel>/handover/` existiert

---

## PHASE 3 — Vorgänger-Living-Files kopieren (STEP_1A des Skills, S1)

> **Naming-Hinweis:** Die `_predecessor_*`-Konvention (führender Unterstrich) ist eine
> etablierte Ausnahme der CDS-Naming-Regel „Lower-Kebab und Higher-Snake, keine Unterstrich-
> Präfixe". Sie stammt aus der **Namenskonvention** (siehe `references/SESSION_TITEL_SCHEMA.md`).
> `STORAGE/templates/skill_core/INSTRUCTIONS.md` und `STORAGE/templates/references/STEP_1A_PREDECESSOR.md`)
> und ist in vergangenen CDS-Sessions bereits so gelebt worden
> (z.B. `WORKSPACE/F37-UMSETZUNG_06_.../desk/_predecessor_A1_...`). **Beibehalten** als
> Skill-Konvention, nicht generalisieren. Nur in der `desk/` von WORKSPACE-Sessions.

### 3.0 Board-Claim (Fork-/Parallel-Schutz, G-23 — VOR jeder inhaltlichen Schreiboperation)

**M0-Baustein 1 gemäß `DOCS/00_SESSION_START_PFLICHTEN.md` §4 Punkt 1 (Wortlaut übernommen):**
eigene Zeile in `WORKSPACE/INDEX.md` von `geplant` auf `aktiv` heben. Steht sie BEREITS auf
`aktiv` → **STOPP**, Operator fragen („läuft eine Parallel-/Fork-Instanz?"). Kein blindes
Weiterarbeiten an einem Bundle, das eine andere Instanz schon bearbeitet.

- Beim Heben auf `aktiv` eine Kennung + Zeitstempel eintragen (z.B. `aktiv (Fable-S5,
  2026-07-19 14:32)`), damit eine zweite, später startende Instanz den Konflikt sofort erkennt.
- **Sonderfall keine eigene Zeile** (Vorgänger-Handover hat keine `geplant`-Zeile angelegt, oder
  Erststart 1.3-A): Zeile JETZT mit `status: aktiv` + Kennung + Zeitstempel anfügen — das IST
  der Claim. Phase 6 verifiziert sie dann nur noch.
- **Sonderfall `WORKSPACE/INDEX.md` fehlt** (Erststart ohne Board): Befund im Walkthrough
  vermerken; das Board wird in Phase 6.2 angelegt (dann inkl. eigener `aktiv`-Zeile mit Kennung).
- **Detail-Verfahren:** Dieser Schritt ist **gleichbedeutend mit** dem Board-Claim in
  `references/STEP_1A_PREDECESSOR.md` Abschnitt **1.3.0** (Skill-Referenz, inkl. Handover-Claim
  für den `<next-session>`-Ordner). Das Detail-Verfahren wird hier bewusst NICHT dupliziert —
  bei Konflikt-/Zweifelsfällen dort nachlesen.

**DoD 3.0:** Eigene INDEX-Zeile steht auf `aktiv` mit Kennung + Zeitstempel (oder dokumentierter
Sonderfall bzw. STOPP). Erst danach dürfen Living Files kopiert/geschrieben werden.

### 3.1 Pflicht-Kern kopieren

Aus `<vorgänger-session>/desk/` in eigene `desk/`, je mit Prefix `_predecessor_`:

```powershell
$VORG = "WORKSPACE/<vorgänger-session-titel>"
$EIGEN = "WORKSPACE/<neuer-session-titel>/desk"

# Pflicht-Kern
foreach ($n in @("task","walkthrough","decision_log")) {
  $quelle = "$VORG/desk/$n.md"
  if (Test-Path $quelle) {
    Copy-Item $quelle "$EIGEN/_predecessor_$n.md"
  } else {
    Write-Warning "Vorgänger hat keine $n.md — übersprungen. Im Walkthrough notieren."
  }
}

# Situative (nur falls im Vorgänger vorhanden)
foreach ($n in @("implementation_plan","lessons_learned","ideas_future_plans")) {
  $quelle = "$VORG/desk/$n.md"
  if (Test-Path $quelle) {
    Copy-Item $quelle "$EIGEN/_predecessor_$n.md"
  }
}
```

**Niemals `mv`** — Vorgänger-Dateien bleiben unangetastet (Konservierungsgesetz 1).

### 3.2. Vorgänger-Handover-Bundle kopieren (optional, aber empfohlen)

Das Handover-Bundle (`<vorgänger>/handover/HANDOVER.md`, `P00_LESELISTE.md`, `P01_BOOTSTRAP.md`,
`P02_SESSION_INIT.md`) wird NUR als LESEREFERENZ in die eigene `desk/`'Sprach' kopiert — die eigene
`handover/`-Zone bleibt LEER (sie wird erst am Session-Ende vom Skill gefüllt, HD-5).

```powershell
foreach ($n in @("HANDOVER","P00_LESELISTE","P01_BOOTSTRAP","P02_SESSION_INIT","IMPLEMENTATION_PLAN")) {
  $quelle = "$VORG/handover/$n.md"
  if (Test-Path $quelle) {
    Copy-Item $quelle "$EIGEN/_predecessor_handover_$n.md"
  }
}
```

Warum `_predecessor_handover_*` in `desk/` (nicht in `handover/`)? `handover/` ist die Tabu-Zone
des Skills (für die Folge-Session). Vorgänger-Bundle ist LESEREferenz für diese Session jetzt.
Also in `desk/`, nicht in der eigenen Tabu-Zone.

### 3.3 DoD Phase 3

- `_predecessor_task.md`, `_predecessor_walkthrough.md`, `_predecessor_decision_log.md` in
  eigener `desk/` (falls Vorgänger sie hatte).
- `_predecessor_handover_*.md` in eigener `desk/` (falls Vorgänger-Bundle existierte).
- Vorgänger-Ordner unangetastet (`git status` im Vorgänger-Repo zeigt nichts — gilt nur, wenn
  der Vorgänger in einem anderen Repo lag; im selben Repo wird nur der neue `WORKSPACE/<neu>/`
  sichtbar).

---

## PHASE 4 — Eigene Living-Files-Skelette anlegen (S1)

### 4.1 Pflicht-Kern — cp + read + edit (kopieren → LESEN → ANPASSEN)

Living-Files aus `STORAGE/templates/living_files/` per `cp` nach `desk/`. Dann die Kopien
im Ziel **LESEN** und per `edit` **an die Task anpassen**: Session-Header einsetzen UND
task-spezifische Inhalte eintragen, soweit die Task-Datei sie vorgibt (z.B. Task-Ziel in
`task.md`, erster Meilenstein). **Kein blindes Kopieren** — eine unangepasste Template-Kopie
ist kein Living File.

### 4.2 Situative Living Files NICHT anlegen

**NICHT** anlegen:
- `implementation_plan.md` — erst bei 3+ Meilensteinen oder Cross-Abhängigkeiten
- `lessons_learned.md` — erst bei echtem Fehler/Learning/Gotcha
- `ideas_future_plans.md` — erst bei zurückgestellten Ideen

Leere Hüllen dieser situativen Files sind nicht nötig (Konservierungsgesetz 2, Umkehrung:
leere Pflicht-Hüllen sind ein Integritätsproblem).

### 4.3 DoD Phase 4

- `task.md`, `walkthrough.md`, `decision_log.md` existieren in eigener `desk/` mit
  Session-Header.
- M0-Eintrag bereits im `walkthrough.md` (wird in Phase 7 finalisiert).

---

## PHASE 5 — Vorgänger-Tasks in eigene `task.md` übersetzen (S2)

### 5.1 Lesen + Übersetzen, NICHT kopieren

`_predecessor_task.md` lesen. Offene, nicht abgehakte Tasks identifizieren. Diese Tasks in die
eigene `task.md` übernehmen — unter „Offene Tasks", mit Checkboxen. Bereits erledigte Tasks des
Vorgängers NUR als Referenz erwähnen („Vorgänger hat [X] erledigt, s. _predecessor_walkthrough.md").

**Format-Beispiel für die eigene `task.md`:**

```markdown
## Offene Tasks (aus Vorgänger <vorgänger-titel> übernommen)

### SILO A — [Silo-Name aus Vorgänger]
- [ ] [Task 1 — aus Vorgänger]
- [ ] [Task 2 — aus Vorgänger]

### SILO B — [Silo-Name]
- [ ] [Task]

## Eigene Tasks (diese Session)
- [ ] [Sind erst nach P01/P02 des aufgabenspezifischen Prompts klar]
```

### 5.2 DoD Phase 5

- Eigene `task.md` enthält die offenen Vorgänger-Tasks.
- `_predecessor_task.md` bleibt unangetastet als Referenz.

---

## PHASE 6 — WORKSPACE/INDEX.md-Zeile schreiben (S1)

### 6.1 Eigene Zeile verifizieren (der Claim war Phase 3.0 — NICHT doppelt anfügen)

Existiert `WORKSPACE/INDEX.md`: Die eigene Zeile wurde bereits in **Phase 3.0 (Board-Claim)** auf
`aktiv` gehoben bzw. angefügt. Hier nur noch: verifizieren (Zeile existiert, `status: aktiv`,
Kennung + Zeitstempel gesetzt) und das `ergebnis`-Feld nachtragen, falls noch leer.

```powershell
# Per edit (nicht write!) — nur Verifikation/ergebnis-Nachtrag, KEINE zweite Zeile anhängen
# Konservierungsgesetz 4: bestehende Zeilen NIE löschen
```

Format (v2 laut Skill INSTRUCTIONS Schritt 7.2):

```markdown
| session | generation | status | ergebnis (1 Satz) | datum |
|---|---|---|---|---|
| TEMPLATE-EXTRAKTION_01_KANON-ROLLOUT_CDS_2026-07-12 | ✅ Aktuell | aktiv | <ein Satz Ziel, aus Vorgänger-HANDOVER „Nächste Schritte" extrahiert ODER aus aufgabenspezifischem Prompt> | 2026-07-12 |
```

Vorgänger-Zeile: **NICHT** anfassen. Sie bleibt auf `übergeben` oder `erledigt` stehen — der
Vorgänger ist nicht mehr `aktiv`. Nur die neue Session bekommt `aktiv`.

### 6.2 Falls INDEX.md nicht existiert (Erststart)

Neu anlegen mit der Kopfzeile + eigener ersten Zeile (`status: aktiv` + Kennung + Zeitstempel —
das holt den Board-Claim aus Phase 3.0 nach). `write` erlaubt für neue Dateien (HD-2).
Format-Hebung gilt: die `generation`-Spalte ist Pflicht — von Anfang an. Keine historischen
Formate ohne `generation` verwenden.

### 6.3 DoD Phase 6

- Eigene Zeile in `WORKSPACE/INDEX.md` existiert, mit `generation: ✅ Aktuell`, `status: aktiv`.
- Vorgänger-Zeile(n) unverändert.

---

## PHASE 7 — Git-Status prüfen + Checkpoint-Commit + Walkthrough-Eintrag finalisieren (S1)

### 7.1 Git-Status prüfen

```powershell
git status
```

- **Nur M0-eigene Änderungen** (neuer `WORKSPACE/<neu>/`-Ordner plus INDEX-Zeile) → weiter zu
  7.1a (Checkpoint-Commit, UNBEDINGT). Vorher `git check-ignore WORKSPACE/` prüfen — ist
  `WORKSPACE/` gitignored, wäre der Checkpoint wirkungslos → Befund melden, Operator informieren.
- **dirty mit FREMDEN Änderungen** (nicht aus dieser M0, z.B. offene Edits der Vorgänger-Session)
  → Operator informieren. Fremde Änderungen NIEMALS eigenmächtig mit committen — der
  Checkpoint-Commit in 7.1a staget ausschließlich die M0-eigenen Artefakte.
- **merge conflict** → STOPP, Operator informieren. M0 darf nicht in einem unsauberen Repo
  laufen.

### 7.1a Checkpoint-Commit (UNBEDINGT — M0-Baustein 3, kein „falls", kein „optional")

**Wortlaut `DOCS/00_SESSION_START_PFLICHTEN.md` §4 Punkt 3:** „**Checkpoint-Commit** als
Rollback-Anker vor der ersten inhaltlichen Änderung."

- **Immer ausführen** — unabhängig davon, ob der Working Tree vorher clean oder dirty war.
  (Bis v2.5 war dieser Schritt konditional — „dirty → Operator fragen, ob Checkpoint-Commit" —
  das widersprach §4 und ist mit v2.6 behoben.)
- Gestagt und committet werden NUR die M0-eigenen Artefakte: `WORKSPACE/<neu>/`
  (Living-File-Skelette, `_predecessor_*`-Kopien) + `WORKSPACE/INDEX.md` (Board-Claim-Zeile).
- Conventional Commit, z.B.:
  `chore(session): M0 Board-Claim + Werkbank <session-titel> (Checkpoint)`
- Dieser Checkpoint ist die EINE kanonische Ausnahme von „Kein Commit ohne Operator-GO" — er ist
  als M0-Baustein 3 vorgeschrieben und macht die Session rollback-fähig, BEVOR inhaltlich
  gearbeitet wird.

### 7.2 Walkthrough-M0-Eintrag finalisieren

Per `edit` (nicht `write`) den M0-Eintrag in eigener `walkthrough.md` vollständig machen:

```markdown
## M0 — Session-Start-Mechanik — ⏸️ STUFE S1–S2/SKRIPT
- **Vorgänger:** <vorgänger-session-titel oder „kein (Erststart)">
- **Session-Titel:** <neuer titel> (aus Vorgänger-HANDOVER.next_session / Operator-Vorgabe)
- **Werkbank angelegt:** WORKSPACE/<neuer titel>/{desk,handover}/
- **Vorgänger-Kopien:** <N>× _predecessor_*.md in eigener desk/
- **Eigene Skelette:** task.md, walkthrough.md, decision_log.md
- **WORKSPACE/INDEX.md:** neue Zeile geschrieben, Vorgänger-Zeile unangetastet
- **Board-Claim (3.0):** eigene INDEX-Zeile auf `aktiv` (Kennung: <…>) / Sonderfall: <…>
- **git status:** <nur M0-Artefakte / dirty (fremd): [Was] / merge conflict>
- **Checkpoint-Commit (7.1a, UNBEDINGT):** <Commit-Hash>

⏸️ GATEWAY M0 — Start-Mechanik erledigt
✅ FERTIG:   Werkbank + Living-Files-Skelette + INDEX + git geprüft — Beweis: ls-Ausgabe + git status
▶️ JETZT:    T0 des aufgabenspezifischen Prompts (z.B. „T0 — Rüstzeug lesen" für TEMPLATE-EXTRAKTION)
🎚️ STUFE:    S4 (Comprehension, typischer T0-Einstieg) — Begründung: inhaltliches Lesen, Verstehen
🤖 WIE:      SELBST (keine Delegation in T0)
❓ OFFEN:    <oder „keine">
──────────────────────────────────────
👉 DU: Stufe senken/skript beenden, dann auf S4 für T0 wechseln. 
```

### 7.3 DoD Phase 7

- Git-Status geprüft und dokumentiert.
- Checkpoint-Commit gesetzt (7.1a, Hash im Walkthrough dokumentiert).
- Walkthrough-M0-Eintrag vollständig.
- ⏸️ GATEWAY M0 sichtbar im Walkthrough.

## PHASE 8 — Bestätigung im Chat + Weiter

⚠️ **WICHTIG — KEINE NEUEN FRAGEN, KEIN P02:**

Der Task wurde bereits VOR Phase 2 vergeben (GATE 0) — hier sind keine neuen Fragen mehr nötig.
Die folgende Vorlage enthält Platzhalter (`<...>`) — das sind **KEINE Fragen**. Der Agent füllt sie **selbst aus dem Kontext aus** und gibt die Bestätigung im Chat ab.
- **KEINE 7 Fragen** zum Beantworten.
- **KEIN P01, KEIN P02** werden in M0 erzeugt.
- **KEIN STOPP** nach M0 — der Task ist bekannt, es geht direkt in die task-spezifische Arbeit.
- P00/P01/P02 werden vom Skill `session_handover_generator` in Phase 6 für die **FOLGE-Session** erzeugt.

### 8.1 Chat-Bestätigung

> „M0 Session-Start-Mechanik abgeschlossen.
>
> **Vorgänger:** <vorgänger-titel oder „kein (Erststart)">
> **Neuer Session-Titel:** <neuer titel>
> **Werkbank:** WORKSPACE/<neuer titel>/{desk,handover}/ existiert
> **Vorgänger-Kopien:** <N>× _predecessor_*.md (inkl. _predecessor_handover_*.md falls vorhanden)
> **Eigene Skelette:** task.md, walkthrough.md, decision_log.md
> **WORKSPACE/INDEX.md:** eigene Zeile auf `aktiv` (Board-Claim Phase 3.0, Vorgänger unangetastet)
> **git status:** <nur M0-Artefakte / dirty (fremd): [Was]>
> **Checkpoint-Commit:** <Hash> (7.1a, UNBEDINGT)
> **Nächster Schritt:** T0 des aufgabenspezifischen Prompts. Stufe anheben auf S4 (Comprehension)
> ODER aufgabenspezifische Stufe."

**Kein STOPP. Der Agent arbeitet nach M0 direkt mit dem aufgabenspezifischen Prompt weiter.**

### 8.2 DoD Phase 8

- Bestätigung im Chat abgegeben.
- Walkthrough-Eintrag vollständig.
- Bereit für T0/Aufgabenstart — direkt weiterarbeiten, nicht auf GO warten.

---

## WAS M0 NICHT MACHT

- Keine inhaltliche Bearbeitung des fachlichen Tasks — das kommt im aufgabenspezifischen Prompt.
- Kein Lesen von Skill-Quellen (`templates/`, `LIVING_FILES/` im Skill-Verzeichnis) — deren
  Lese-Pflicht kommt im aufgabenspezifischen T0 (z.B. TEMPLATE-EXTRAKTIONS_PROMPT T0.A liest
  `SKILL.md` + `INSTRUCTIONS.md`). Skill-Dateien liegen auch als gespiegelte Kopien in
  `STORAGE/templates/skill_core/` (CDS-Mirror) — falls der Skill-Pfad nicht erreichbar ist
  (z.B. OpenCode-vs-Claude-Code-Pfadunterschied), nutze den CDS-Mirror.
- Kein Edit an der Vorgänger-Session — Kopieren ja, Editieren nein.
- Kein Edit am Handover-Skill — Skill-Quellen sind strikt READ-ONLY (HD-2). Gleiches gilt
  für die CDS-Mirror-Kopien — sie sind Back-up, keine Arbeitskopien.
- Kein Commit ohne Operator-GO — **einzige Ausnahme:** der unbedingte M0-Checkpoint-Commit
  (Phase 7.1a, M0-Baustein 3 gemäß `DOCS/00_SESSION_START_PFLICHTEN.md` §4).
- Keine Living-Files-Befüllung mit künstlichem Inhalt — Skelette haben nur Session-Header.
- Keine situativen Living Files (`implementation_plan.md` etc.) anlegen — erst bei Bedarf.

---

## ABNAHME-CHECKLISTE

- [ ] GATE 0 eingehalten — Task erfragt und erhalten VOR der ersten Schreiboperation?
- [ ] Task-Datei VOLLSTÄNDIG gelesen (nicht nur Titel)?
- [ ] Plan im Chat angekündigt BEVOR Ordner/Dateien angelegt wurden (Kein Blindflug)?
- [ ] Kopierte Living Files gelesen und gemäß Task angepasst (kein blindes Kopieren)?
- [ ] Vorgänger identifiziert (oder Erststart-Modus dokumentiert)?
- [ ] Session-Titel aus Vorgänger-HANDOVER `next_session` ODER Operator-Vorgabe, NICHT erfunden?
- [ ] `WORKSPACE/<neu>/{desk,handover}/` existiert?
- [ ] Pflicht-Kern `_predecessor_*` kopiert (falls Vorgänger existierte)?
- [ ] `_predecessor_handover_*` kopiert (falls Vorgänger-Bundle existierte)?
- [ ] Eigene `task.md`, `walkthrough.md`, `decision_log.md` existieren mit Session-Header?
- [ ] Eigene `task.md` enthält offene Vorgänger-Tasks?
- [ ] Board-Claim (Phase 3.0): eigene INDEX-Zeile auf `aktiv` gehoben (bzw. mit Kennung
      angelegt), Fork-Fall geprüft (bereits `aktiv` → STOPP), Vorgänger-Zeile unangetastet?
- [ ] git status geprüft und dokumentiert?
- [ ] Checkpoint-Commit UNBEDINGT gesetzt (Phase 7.1a, nur M0-Artefakte, Hash dokumentiert)?
- [ ] Walkthrough-M0-Eintrag vollständig mit ⏸️ GATEWAY M0?
- [ ] Chat-Bestätigung abgegeben?
- [ ] KEIN Edit am Vorgänger-Session-Ordner (nur `cp`)?
- [ ] KEIN Edit am Handover-Skill (nur Lesen)?
- [ ] KEIN Commit ohne Operator-GO (einzige Ausnahme: der unbedingte M0-Checkpoint-Commit 7.1a)?

---

## ABHÄNGIGKEITEN / VORAUSSETZUNGEN

| Voraussetzung | Wenn fehlend |
|---|---|
| `WORKSPACE/INDEX.md` existiert (oder Repo ist Kanon-konform) | Repo ist noch nicht kanonisiert → `REPO_ETABLIERUNGS_PROMPT.md` laufen lassen |
| Vorgänger-Session mit `status: übergeben` oder `erledigt` | Erststart-Modus (s. Phase 1.3) — Operator MUSS Session-Titel vorgeben |
| Operator anwesend für GO/STOPP bei Unklarheiten | M0 STOPP bei erster Unsicherheit — kein eigenständiges Entscheiden |
| Git-Repo sauber (kein laufender Merge, kein Dirty-Code von Drittsession) | STOPP, Operator fragen — M0 läuft nicht in unreinem Repo |

---

## RELATION ZU ANDEREN KANON-PROMPTS

| Prompt | Rolle | Wann |
|---|---|---|
| **SESSION_START_PROMPT** (dieser) | M0 Mechanik — Vorgänger kopieren, Werkbank anlegen | AM ANFANG JEDE neuen Session |
| `REPO_ETABLIERUNGS_PROMPT.md` | Repo zum ersten Mal kanon-konform machen (Phase I + II) | Bei neuen Repos ODER stark verwilderten |
| `TEMPLATE_EXTRAKTIONS_PROMPT.md` | Kanon-Templates aus 5 Quellen destillieren | Nur bei der Template-Erstellungs-Session — nicht jede Session |
| `KANON_STRUKTUR_SPEC.md` | Ziel-Raster, living document | Jederzeit, Referenz |
| `ROLLOUT_BOARD.md` | Repo-Status, living document | Jederzeit, Referenz |

Dieser Prompt ist der **ENTRY POINT** für jede Session. Danach läuft der aufgabenspezifische
Prompt (der dann T0/T1/T2/T3 definiert). M0 ist die gemeinsame Basis aller aufgabenspezifischen
Prompts.

---

## SKRIPT-VARIANTE (optional, für dieselbe Session-Titel-Vergabe)

Falls der Operator denselben Workflow öfter ausführt, kann dieser Prompt als PowerShell-Skript
abgelegt werden — DAO-Gedanke, einmalig debuggt, dann deterministisch reproduzierbar. Skript
unter `ops/scripts/session_start_m0.ps1` (falls Ops-Ordner im Repo existiert) ODER
`PLAYGROUND/Kanon_Rollout/scripts/session_start_m0.ps1`. Entspricht MILESTONE_GATEWAY §2c
Anti-Farce-Empfehlung (Skript statt Reasoning-Modell).

Skript-Signatur (nur Idee, nicht im Prompt fixieren):

```powershell
# ops/scripts/session_start_m0.ps1
# Parameter: -SessionTitle <neuer-titel> [-Vorgänger <vorgänger-titel>] [-Repo <pfad>]
# Macht: M0.1 bis M0.7 deterministisch, dann Stopp mit Chat-Bestätigung.
```

Skript wird in einer späteren Session gebaut — heute reicht der Prompt.

---

## CHANGELOG

- **v2.6 (2026-07-19):** **Naht-1-Schluss (Session KANON-SYSTEMREPARATUR_17, M3 —
  `KONSOLIDIERUNGS_LUECKEN.md` Teil A, blockierender Befund B7):** Die drei kanonischen
  M0-Bausteine aus `DOCS/00_SESSION_START_PFLICHTEN.md` §4 (Board-Claim → STEP_1A →
  Checkpoint-Commit) sind jetzt ALLE in dieser einen M0-Quelle abgedeckt:
  - **NEU Phase 3.0 — Board-Claim (Fork-/Parallel-Schutz G-23):** eigene INDEX-Zeile von
    `geplant` auf `aktiv` heben; steht sie BEREITS auf `aktiv` → STOPP, Operator fragen
    („läuft eine Parallel-/Fork-Instanz?"). Wortlaut aus §4 Punkt 1; Detail-Verfahren
    gleichbedeutend mit `STEP_1A_PREDECESSOR.md` 1.3.0 (bewusst nicht dupliziert, nur
    referenziert). Gilt AUCH im Erststart-Modus (dort fallen nur 3.1–3.3 aus). Vorher gab es
    KEINEN Claim: Phase 6.1 hängte blind eine neue `aktiv`-Zeile an, ohne Fork-Prüfung →
    Phase 6.1 deshalb von „Neue Zeile anfügen" auf „Eigene Zeile verifizieren" umgestellt
    (kein Doppel-Eintrag).
  - **Checkpoint-Commit von konditional auf UNBEDINGT (NEU Phase 7.1a):** vorher „clean → kein
    Commit nötig / dirty → Operator fragen, ob Checkpoint-Commit" — das widersprach §4 Punkt 3
    („Checkpoint-Commit als Rollback-Anker vor der ersten inhaltlichen Änderung" — kein „falls",
    kein „optional"). Jetzt: immer committen, aber NUR die M0-eigenen Artefakte; fremde dirty
    Änderungen bleiben draußen (Operator informieren). „Kein Commit ohne Operator-GO"
    (WAS M0 NICHT MACHT + Abnahme-Checkliste) trägt diese eine kanonische Ausnahme jetzt
    explizit, statt dem neuen 7.1a zu widersprechen.
  - Mitgezogen: Workflow-Kopf (Punkt 6), Dirty-Tabellenzeile, 1.3-A, Phase-6.2-Erststart
    (Board-Neuanlage inkl. `aktiv`-Zeile + Kennung), Walkthrough-M0-Template, Chat-Bestätigung
    8.1, DoD 7.3, Abnahme-Checkliste.
- **v2.5 (2026-07-17):** **Abschluss der Pfad-Doktrin** (Session KANON-ROLLOUT-REPARATUR_12, Fix F1) —
  v2.4 hatte die richtige Basis (Repo-Root), aber drei Löcher offen gelassen, durch die die
  „Agent sucht ein WORKSPACE auf C:\"-Fehlerklasse weiterhin passieren konnte:
  - **Fehlerfall `git rev-parse`** (kein Git-Repo) war UNBEHANDELT → jetzt harter STOPP.
    Vorher: Verhalten undefiniert, Agent fiel ins Raten/Suchen zurück.
  - **`WORKSPACE/` fehlt → Erststart-Modus baute STILL Strukturen auf.** Jetzt: STOPP, melden,
    fragen (1.3-B). **Zwei bisher vermischte Fälle sauber getrennt:** 1.3-A „kein VORGÄNGER"
    (Repo IST eingerichtet → bauen ist richtig) vs. 1.3-B „kein SYSTEM" (nicht eingerichtet oder
    falsches Repo → nicht bauen). Aufbau/Reparatur gehört ins Etablierungs-/Reparatur-Paket, das
    Dossier, Operator-Gate und Checkpoint-Commit mitbringt — nicht in den Alltags-Startprompt.
  - **ABSOLUTES SUCHVERBOT** explizit verankert (1.1): fehlt `WORKSPACE/` am einzig erlaubten Ort
    (`<repo-root>/WORKSPACE/`), ist das ein **Befund**, keine Suchaufgabe. Kein `C:\`-Scan.
  - **NEU: optionaler Prüfsummen-Block `ERWARTETER REPO-ROOT`** im Kopf. Relative Pfade bleiben
    relativ (portabel), der absolute Pfad ist NUR Prüfsumme — Mismatch = STOPP. Gegenstück:
    der Handover-Skill trägt ihn beim Bundle-Bau ein (Skill-Fix S-3, Stufe 1).
  - **Bergung aus v1.1 (F5a):** Leitplanke 6 trug in v1.1 die Klarstellung „Keine
    Skill-Abhängigkeit — der Skill ist für das ENDE zuständig, nicht für den Start". Sie war in
    v2.0 still verschwunden (in KEINEM Changelog dokumentiert) → wieder eingesetzt, ergänzt um
    die v2.4-Handover-Aussage. Beleg: `desk/subagent/F5a_BERGUNG_ALTFASSUNGEN_2026-07-17.md`.
- **v2.4 (2026-07-15):** **Rücknahme des v2.3-Fehlers** — der eigentliche, seit ~20 Anläufen
  gesuchte Fix. Alle Pfade sind **relativ zum REPO-ROOT** (`git rev-parse --show-toplevel`),
  nicht zum cwd. `WORKSPACE/` = `<repo-root>/WORKSPACE/`. Das ist die einzige richtige Basis und
  funktioniert in JEDEM Repo ohne absolute Pfade und ohne Sonderregel.
  - v2.3 hatte fälschlich `git rev-parse` ENTFERNT und „nur pwd zählt" behauptet — das war rückwärts:
    Der zweite Fehlstart-Agent ging korrekt zum Repo-Root, v2.3 verbot ihm genau das als „Probing".
  - Repo-Root-Bestimmung als erster Schritt in 1.1; STOPP-Tabelle + Kopf + 1.1 durchgängig auf
    Repo-Root-relativ umgestellt. „Falscher Ort" heißt jetzt „falsches REPO", nicht „falscher cwd".
- **v2.3 (2026-07-15, ÜBERHOLT durch v2.4):** Arbeitsverzeichnis-Determinismus (nach zweitem Fehlstart:
  Agent probte per `Get-ChildItem C:\Viron` nach einem WORKSPACE). **War falsch — s. v2.4.**
  - ~~Maßgeblich ist NUR das aktuelle Arbeitsverzeichnis (pwd). Git-Root (`git rev-parse`) ist~~
    in Mono-Strukturen irreführend und wurde aus 1.1 ENTFERNT.
  - VERBOTEN: nach `WORKSPACE/` anderswo suchen (Git-Root, Eltern-/Nachbar-Ordner) oder dazu
    eine Gegenfrage stellen. Fehlt WORKSPACE im pwd → Erststart-Modus, Befund miterwähnen.
  - Read-Only-Checks sind abschließend definiert: die zwei `Test-Path` aus 1.1 + INDEX-Lektüre.
  - Die v2.1-STOPP-Tabellenzeile („existiert aber woanders → Operator fragen") war die Wurzel
    des Probings und wurde durch die deterministische Regel ersetzt.
- **v2.2 (2026-07-15):** Rest der Operator-Vorgaben nachgetragen (fehlten in v2.1 noch):
  - NEU Phase 1.6: Task-Datei VOLLSTÄNDIG lesen (i.d.R. `DESK/TASKS/active/…/task.md`),
    Titel ableiten, dann **Plan im Chat ankündigen** (Kein Blindflug: ankündigen, DANN tun)
    — erst danach ist GATE 0 offen.
  - Phase 4.1 geschärft: kopieren → LESEN → gemäß Task ANPASSEN. Kein blindes Kopieren —
    eine unangepasste Template-Kopie ist kein Living File.
  - Abnahme-Checkliste um Task-gelesen / Plan-angekündigt / Kopien-angepasst erweitert.
- **v2.1 (2026-07-14):** Task-First-Korrektur (Operator-Vorgabe nach Fehlstart am 2026-07-14).
  - v2.0 hatte die Operator-Regel INVERTIERT („startet SOFORT, braucht keinen Task") — Agenten
    legten Strukturen vor der Task-Vergabe an. Das ist die falsche Reihenfolge.
  - NEU GATE 0: keine Schreiboperation (mkdir/cp/edit/write) vor Task-Vergabe. Reihenfolge:
    Task → Name → Struktur → kopieren → lesen → anpassen.
  - „Welcher Task?" kommt jetzt VOR Phase 2 (direkt nach den Read-Only-Checks), nicht danach.
  - STOPP-Regel geschärft: unklarer Befund (z.B. WORKSPACE fehlt im Zielverzeichnis, existiert
    aber woanders) → sofort Operator fragen, nicht weiterforschen.
  - Kein temporärer Session-Identifier mehr im Erststart-Modus (Titel kommt direkt aus dem Task).
  - Tippfehler bereinigt (interactice / finalettiert / Agentführt).
- **v2.0 (2026-07-12):** Workflow-Korrektur + Bugfixes.
  - M0 läuft SOFORT nach Prompt-Eingang, kein Warten auf Task/Build Mode
  - "Welcher Task?" als erster interactiver Schritt
  - Template-Quelle: STORAGE/templates/living_files/
  - cp+edit statt inline-Skelette
  - Session-Titel aus Task abgeleitet, nicht vom Operator erbeten
  - Doppelte 1.2 Überschrift entfernt
- **v1.1 (2026-07-12):** Strukturen-fehlen-Patch + Sub-Agent-Strategie.
- **v1.0 (2026-07-12):** Initiale Fassung.