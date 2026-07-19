<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# STRUKTUR_WISSENSBASIS — mitgelieferte Kurzfassung (Skill-Fallback)

> **Was das hier ist:** Die kompakte Struktur-Regel, die der Skill zum Funktionieren
> braucht. Sie liegt **im Skill selbst**, damit der Skill in JEDEM Repo sofort
> einsatzbereit ist — auch wenn das Repo keine eigene `CLAUDE.md` hat.
>
> **Vorrang-Regel:** Existiert im Root des aktuellen Arbeits-Repos eine eigene
> `CLAUDE.md` mit projektspezifischen Struktur-Angaben, gilt DIESE zusätzlich/vorrangig
> für Repo-Besonderheiten. Diese Datei hier ist der **Fallback**, der immer greift,
> auch ohne Repo-eigene `CLAUDE.md`.
>
> **Herkunft:** Destilliert aus der ausführlichen Playground-Wissensbasis
> (`PLAYGROUND/Handover_Bundle/CLAUDE.md` im Context-Dispatcher-System-Repo — dort
> liegt die vollständige Bau-Dokumentation als Rohmaterial, nicht live geladen).

---

## 1. WORKSPACE/\<session\>/ — Zwei-Ordner-Modell

Der Handover-Skill läuft am ENDE einer Session und arbeitet mit ZWEI Ordnern:

- **`WORKSPACE/<session>/`** — die AKTUELLE, abgebende Session. Existiert bereits,
  wurde während der Session laufend gepflegt. Der Skill FINALISIERT sie nur.
- **`WORKSPACE/<next-session>/`** — NEUER Ordner, den der Skill selbst baut, benannt
  nach den offenen Tasks (Namensschema Abschnitt 3). Fahrplan/Übergabe für die
  Folgesession.

```
WORKSPACE/<session>/
├── desk/                        ← Living Files FLACH (Ausnahmen: <thema>/- und walkthrough/-Ordner, s.u.)
│   ├── task.md                        (Pflicht-Kern)
│   ├── walkthrough.md                 (Pflicht-Kern — das PASSIERTE, kompakter Index)
│   ├── decision_log.md                (Pflicht-Kern)
│   ├── lessons_learned.md             (situativ, nur falls inhaltlich zutreffend)
│   ├── ideas_future_plans.md          (situativ)
│   ├── implementation_plan.md         (situativ — Plan-Träger: das GEPLANTE, D-005; P02 verweist nur hierher)
│   └── walkthrough/                   (optional, G-25/D-005: 1 Detail-Log pro Meilenstein `M<N>_<name>.md`
│                                        — bewusste Koexistenz mit walkthrough.md, kein Namenskonflikt;
│                                        erlaubte Ausnahme der Flach-Regel wie desk/<thema>/-Zusatzordner)
└── handover/                    ← Ingress/Egress für den Nachfolger
    ├── HANDOVER.md
    ├── P00_LESELISTE.md          ┐
    ├── P01_BOOTSTRAP.md          ├─ Tabu-Zone sobald fertiggestellt (für den User)
    └── P02_SESSION_INIT.md       ┘

WORKSPACE/<next-session>/
├── desk/                        ← vorbefüllt: task.md als Fahrplan
└── handover/                    ← P00/P01/P02 + HANDOVER.md
```

Wer welchen Ordner bearbeitet: Schritt 1,2,5,6,7 → `<next-session>`. Schritt 3,4 →
`<session>` (Finalisierung + Forensic-Report).

## 2. Root-`DESK/` — Projekt-SSoT, dauerhaft (gehört dem ORCHESTRATOR)

**Doktrin (Operator, D-014):** Der Root-DESK gehört dem Orchestrator — hier wird GEPLANT. Keine
Session „parkt" dort ihre Arbeitsdateien (historische Lektion: zugemüllter Root-DESK) — jede
Session arbeitet in ihrem eigenen `WORKSPACE/<session>/`-Ordner; beim Handover kommen die
vorbereiteten Living Files in den NEUEN `WORKSPACE/<next-session>/desk/`. Auf `DESK/TASKS/` lebt
die **permanente Checkbox-Gesamtplanung `00_Master_Tasklist.md`** (F25): hierarchischer Task-Baum
Projekt→Task→Untertask (IDs `P-NN`/`T-NN.N…`, Eltern-✓ erst wenn alle Kinder ✓, Session-Referenz
pro Knoten) — zwei Ebenen: Session-`task.md` (temporär) + Gesamtplanung (permanent), beide werden
gepflegt, die Gesamtplanung bei der Rückspiegelung (7.3/F38).

```
DESK/                              ← NIE durch WORKSPACE ersetzt
├── TASKS/
│   ├── 00_Master_Task.md
│   ├── 00_Master_Implementation_Plan.md
│   ├── 00_Master_Task_State.md    ← lebendes Dashboard, Skill zieht es am Ende nach
│   ├── active/
│   └── done/
├── <Haupt-Living-Files>           ← projektweite Living Files, flach auf DESK/
└── reports/
    └── session-reports/          ← klein geschrieben! Reports landen hier.
```

Rückspiegel-Pflicht: Der Skill aktualisiert am Sessionende zwingend
`00_Master_Task_State.md` und verschiebt den betroffenen Task zwischen `active/`
und `done/`.

## 3. Namensschema für `<session>`

```
[TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]
```

TASK = konkreter Fokus, aus offenen Tasks abgeleitet, nicht erraten — steht vorne.
NN = zweistellig laufend pro PROJEKT-Strang (zählt bei TASK-Wechsel weiter). GESAMTPROJEKT = Projektname (z.B. aus
`DESK/TASKS/active/`). REPO = Kürzel. Datum am Ende. TASK vorne ⇒ Ordner-Sortierung
ist NICHT chronologisch; Chronologie liefert `WORKSPACE/INDEX.md`.
Ordnername entsteht zu Session-Beginn, nicht rückwirkend.

## 4. Casing-Regel (Drei-Klassen-Logik)

1. **Root-Hauptordner + ID-artige Bausteine → GROSS:** `DESK/`, `DOCS/`, `STORAGE/`,
   `WORKSPACE/`, `TASK_[SESSION]_V[N]`-Ordnernamen, Namensschema-Bausteine
   (`CDS`, `SKILL-REBOOT` ...).
2. **Bootstrap-/Protokoll-/Schema-Dateien → GROSS**, unabhängig vom Ordner-Casing:
   `HANDOVER.md`, `P00_LESELISTE.md`, `P01_BOOTSTRAP.md`, `P02_SESSION_INIT.md`,
   `SESSION_TITEL_SCHEMA.md`, `CLAUDE.md`, `SKILL.md`.
3. **Strukturelle Unter-Container + Living Files → klein:** `desk/`, `handover/`,
   `reports/`, `session-reports/`, `active/`, `done/`, sowie `task.md`,
   `walkthrough.md`, `decision_log.md`, `lessons_learned.md`,
   `ideas_future_plans.md`, `implementation_plan.md`.

## 5. Living Files — Pflicht-Kern-Regel

`task.md`, `walkthrough.md`, `decision_log.md` sind IMMER Pflicht, jede Session.
`lessons_learned.md`, `ideas_future_plans.md`, `implementation_plan.md` nur, wenn
die Session sie inhaltlich hergibt — keine künstlich befüllten Hüllen.

`lessons_learned.md` = ausführlicher, roher Detail-Log dieser Session (Beispiele,
Verweise, volles Problem) — **plus Sofort-Triage (D-015): jede Lesson trägt ein
`ABLEITUNG:`-Pflichtfeld** (REGEL·global / REGEL·projekt / SKILL·fix / SKILL·neu /
HOOK / TASK / WISSEN) und ist bei der Rückspiegelung MANIFESTIERT (Aktion ausgeführt
oder Task angelegt) — Gate in INSTRUCTIONS 7.0(g)/7.3. Getrennt davon:
`DOCS/hard_learned_facts` = projektweite, kondensierte Essenz — das ist NICHT Teil
dieses Skills, sondern ein separater Prozess außerhalb (der Skill fasst `DOCS/`
nicht an).

## 6. Skill-Scope (hart)

Der Handover-Skill aktualisiert AUSSCHLIESSLICH (a) seine eigenen Session-Dateien
in `WORKSPACE/<session>/{desk,handover}/` und (b) den Root-`DESK/`
(`00_Master_Task_State.md` + `active/`↔`done/`). Er fasst `DOCS/` NICHT an.

## 7. Report-Kaskade

Forensic-Report ist IMMER Pflicht, Quelle der Wahrheit, liegt unter
`DESK/reports/session-reports/[SESSION-TITEL].md` (kein zusätzliches Datum davor,
der Titel enthält es schon). SUMMARY + TTS-Summary werden standardmäßig mit
abgeleitet; DEBUG-Report nur bei Fehlersuche-Sessions.

## 8. Status-Board (offizielles Living File, F26)

`WORKSPACE/INDEX.md` ist ein **offizielles Living File** (Pflege-Pflicht wie der
Pflicht-Kern, aber repo-weit statt session-lokal). Format (v2/F31):
`| session | generation | status | ergebnis | datum |`.
- **Status:** `geplant · aktiv · übergeben · erledigt · obsolet` (+ `unklar` nur mit
  Fußnote + Operator-Klärung). Jede Session stuft ihre Zeile beim Start von `geplant`
  auf `aktiv`, am Ende auf `übergeben`/`erledigt`; der Handover trägt die Folgesession
  als `geplant` ein. Handover ohne aktualisierte INDEX-Inventur = UNVOLLSTÄNDIG.
- **Generation:** `✅ Aktuell` · `📦 Alt` (Alt-Schema, unangetastet) · `📦 Archiv`
  (nach Root-`ARCHIVE/<name>_<YYYY-MM-DD>/` verschoben — EINE Archiv-Zone, D-007; NIE
  `WORKSPACE/_archive/`. Kein Automatismus: Q3 gestrichen, K1/D-001 2026-07-17). Zeilen werden NIE gelöscht.
- `status:`-Feld im HANDOVER-YAML spiegelt denselben Wert.

## 8b. Root-Pflichtdateien der v2-Struktur (Kontext für die Rückspiegelung)

Zur v2-Struktur gehören neben den Zonen zwei Repo-Root-Pflichtdateien und das DOCS-Duo
— die der Rückspiegel-Vierklang (INSTRUCTIONS 7.3, F29) nachführt, sofern vorhanden:
- **`PROTOCOL_LOG.md`** (Repo-Root, append-only): jede Struktur-Operation + jeder
  Auto-Archiv-Lauf wird angehängt, nie editiert.
- **`DOCS/INDEX.md`** („Aktuell aktiv"-Zeiger + Verlaufstabelle + Trigger-Tabelle) und
  **`DOCS/FOLDER_MAP.md`** (Zonen-Wegweiser). Anti-Drift: DOCS ZEIGT nur (Pfade), kopiert
  keine Inhalte. Der Skill fasst `DOCS/` inhaltlich nicht an, führt aber den Zeiger nach.

## 9. Die 4 Konservierungsgesetze

1. **KEINE LÖSCHUNG** — archivieren statt löschen.
2. **KEINE REDUKTION** — keine `//...`-Kürzungen, O-Töne wörtlich.
3. **BEWEISPFLICHT** — physische Artefakte (Reports, Diffs, Terminal-Output).
4. **INTEGRATION** — `edit` für Korrekturen, `append` nur für neue Phasen.
