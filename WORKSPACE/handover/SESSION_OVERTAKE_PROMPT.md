<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# SESSION_OVERTAKE_PROMPT — Bestehende Session übernehmen

<!-- ═══════════════════════════════════════════════════════════════════════════
     ERWARTETER REPO-ROOT: 
     (Optional. Absoluten Repo-Root eintragen. Ist er gesetzt, MUSS der per
     `git rev-parse --show-toplevel` ermittelte Root übereinstimmen, sonst
     STOPP → Phase 1.0. Leer = Prüfung entfällt.)
     ═══════════════════════════════════════════════════════════════════════════ -->

> **Version:** 1.1 · **Status:** LEBENDES DOKUMENT, versioniert wie die anderen Kanon-Prompts
> (gleicher Ordner: `KANON_STRUKTUR_SPEC.md`, `REPO_ETABLIERUNGS_PROMPT.md`,
> `TEMPLATE_EXTRAKTIONS_PROMPT.md`, `SESSION_START_PROMPT.md`, `ROLLOUT_BOARD.md`).
>
> **Pfad-Doktrin (v1.1 — identisch zu `SESSION_START_PROMPT.md` v2.5):** Alle Pfade sind relativ
> zum **REPO-ROOT** (`git rev-parse --show-toplevel`), NICHT zum cwd. `WORKSPACE/` heißt immer
> `<repo-root>/WORKSPACE/`. **Niemals** im Dateisystem nach einem `WORKSPACE/` suchen.
> Siehe Phase 1.0.
>
> **Was das hier ist:** Ein eigenständiger, kopierbarer Startprompt. Der Operator wirft ihn in
> eine neue Session im Repo, wenn eine BESTEHENDE Session (mit `status: aktiv` im
> `WORKSPACE/INDEX.md`) von einem neuen Agenten fortgesetzt werden soll. Im Gegensatz zu
> `SESSION_START_PROMPT.md` (der eine NEUE Session startet) übernimmt dieser Prompt eine
> LAUFENDE Session.
>
> **Einordnung:** Brücken-Prompt zwischen `SESSION_START_PROMPT.md` (neu) und dem Session-Ende
> via `session_handover_generator`-Skill. Wird gebraucht, wenn eine Session mitten im Workflow
> abbricht und ein neuer Agent übernehmen muss.

---

## Wann einsetzen

- Eine Session im `WORKSPACE/INDEX.md` hat `status: aktiv` UND es gibt offene Tasks.
- Der ursprüngliche Agent ist nicht mehr verfügbar (Session abgestürzt, Modell gewechselt,
  Session zu lang geworden, etc.).
- Der Operator will: „Mach da weiter, wo der andere aufgehört hat."

> **🔧 Wenn etwas schiefgeht → `RECOVERY_PROTOCOL.md`** (gleicher Ordner): Was du **selbst**
> korrigieren darfst (alles Reversible — getrackt+committet → `git mv`, autonom) und was **STOPP**
> bleibt (falsches Repo, Fork-Instanz, untrackte Daten). Für die Übernahme besonders relevant:
> **R-3** (Board sagt `aktiv`, HANDOVER sagt `übergeben` → HANDOVER gewinnt, Board nachziehen) und
> **R-8** (fremde Kennung auf deiner Zeile → STOPP, Parallel-Instanz).

## Wann NICHT einsetzen

- **Neue Session starten** → nutze `SESSION_START_PROMPT.md`.
- **Session beenden (Handover bauen)** → nutze den `session_handover_generator`-Skill.
- **Board-Inkonsistenz aufklären** → Manuell per `git`-Edit; nicht Aufgabe eines Prompts.

---

## PHASE 0 — Operator-Eingabe (VOR Phasen 1–4)

Der Operator MUSS vor dem Start dieses Prompts folgende Info in den Chat posten:

```
SESSION-TITEL: <vollständiger Session-Name aus WORKSPACE/INDEX.md>
GRUND: <Warum wird übernommen?>
ZIELE: <Was soll in dieser Übernahme erreicht werden?>
```

Beispiel:
```
SESSION-TITEL: TEMPLATE-EXTRAKTION_09_KANON-ROLLOUT_CDS_2026-07-12
GRUND: Vorheriger Agent hat Phase T1 (Inventur) nicht abgeschlossen
ZIELE: T1 fertigstellen, danach T2-Cluster starten
```

**Ohne diese Eingabe:** Agent fragt EINMAL nach (eine Frage, nicht eine Schleife).
Wenn der Operator auch dann nicht antwortet → STOPP, keine Aktion.

---

## PHASE 1 — Session-Status aufnehmen (S1, Read-Only)

### 1.0 Repo-Root bestimmen (v1.1 — ZUERST, vor allem anderen)

```powershell
$root = git rev-parse --show-toplevel     # DER Anker — alles Weitere relativ dazu
```

| Befund | Verhalten |
|:--|:--|
| Root ermittelt, `<root>/WORKSPACE/` existiert | ✅ weiter zu 1.1 |
| **`git rev-parse` schlägt fehl** (kein Git-Repo) | 🛑 **STOPP, Operator fragen.** Nicht im Dateisystem suchen. |
| **`<root>/WORKSPACE/` fehlt** | 🛑 **STOPP.** Hier gibt es keine Session zum Übernehmen. Melden: „Kein `WORKSPACE/` im Repo-Root `<root>` — falsches Repo?" **Kein Aufbau** (das ist Sache des Etablierungs-/Reparatur-Prompts, nicht dieses). |
| **`ERWARTETER REPO-ROOT` (Kopf) ≠ ermittelter Root** | 🛑 **STOPP — falsches Repo.** Beide Pfade melden. |

> **⛔ SUCHVERBOT:** `WORKSPACE/` liegt an genau EINEM Ort: `<repo-root>/WORKSPACE/`. Ist es dort
> nicht, existiert es für dich nicht. Kein `C:\`-Scan, keine Eltern-/Nachbar-Ordner, kein Raten.

### 1.1 Session-Ordner finden

```powershell
$SESSION = "$root/WORKSPACE/<operator-eingegebener-session-titel>"
Test-Path $SESSION
```

Wenn der Ordner nicht existiert → STOPP, Operator informieren („Session nicht gefunden").
Wenn er existiert → weiter.

### 1.2 Aktuelle Living-Files lesen

Reihenfolge (vom neuesten zum ältesten Stand):

1. `$SESSION/desk/task.md` — Was ist offen?
2. `$SESSION/desk/walkthrough.md` — Was wurde bisher gemacht?
3. `$SESSION/desk/decision_log.md` — Welche Entscheidungen sind getroffen?
4. `$SESSION/desk/implementation_plan.md` (falls vorhanden) — Was war der Plan?
5. `$SESSION/desk/lessons_learned.md` (falls vorhanden) — Was wurde gelernt?
6. `$SESSION/desk/ideas_future_plans.md` (falls vorhanden) — Was steht noch aus?

### 1.3 WORKSPACE/INDEX.md-Zeile lesen

Status und Vorgänger-Beziehungen prüfen. Die Zeile dieser Session MUSS `status: aktiv` zeigen.
Wenn sie einen anderen Status hat → STOPP, Operator informieren.

### 1.4 Vorgänger-Living-Files prüfen (nur lesen)

Falls `_predecessor_*`-Dateien in `desk/` existieren → als historischer Kontext lesen, nicht
überschreiben.

### 1.5 Chat-Bestätigung Phase 1

Im Chat ausgeben:
> „Overtake gestartet für Session `<TITEL>`.
> Aktueller Stand: <Zusammenfassung der Living-Files, max. 5 Sätze>
> Offene Tasks: <Anzahl> (<Titel der ersten 3>)
> Nächster Schritt: <Aus dem Plan/Task abgeleitet>"

Keine STOPP. Weiter zu Phase 2.

---

## PHASE 2 — Eigene Living-Files übernehmen (S1)

### 2.1 task.md erweitern

Oben in `task.md` einen neuen Abschnitt ergänzen:

```markdown
## Overtake-Notiz (YYYY-MM-DD HH:MM)
- Vorheriger Agent: [falls aus Lessons ableitbar]
- Übernommen weil: <Grund aus Operator-Input>
- Aktueller Stand-Index: <Zeile aus walkthrough.md, letzter Meilenstein>
- Offene Tasks (aus Phase 1.2): <Liste>
```

NICHT die alten Inhalte von `task.md` löschen — nur OBEN DRAN setzen.

### 2.2 walkthrough.md erweitern

Neuen Eintrag oben in `walkthrough.md`:

```markdown
## Overtake-Eintrag (YYYY-MM-DD HH:MM)
Neuer Agent übernimmt Session `<TITEL>`. Letzter Meilenstein: <aus Phase 1.2>.
Overtake-Prompt: SESSION_OVERTAKE_PROMPT.md v1.0.
```

### 2.3 decision_log.md — keine Änderung nötig

Die alten Entscheidungen stehen schon drin. Neue Entscheidungen, die DU triffst, kommen normal
dazu (per `edit` am Ende der Tabelle).

### 2.4 _predecessor_*-Dateien nicht verändern

Falls die Vorgänger-Living-Files als `_predecessor_*` im `desk/` liegen: NUR lesen, nicht
überschreiben (Konservierungsgesetz 1).

---

## PHASE 3 — Mit der Arbeit fortfahren (Stufe wie aufgabenspezifisch)

Die Arbeit wird genauso fortgesetzt, wie der vorherige Agent sie begonnen hätte:

1. Den aufgabenspezifischen Prompt lesen (z.B. `TEMPLATE_EXTRAKTIONS_PROMPT.md`).
2. Mit der Phase fortfahren, die laut `implementation_plan.md` als nächstes ansteht.
3. Normale Living-Files-Pflege (HD-3 des Skills).
4. Keine Sonderbehandlung — nur ein neuer Agent, der da weitermacht wo der andere aufgehört hat.

---

## PHASE 4 — Bestätigung im Chat

> „Overtake abgeschlossen. Session `<TITEL>` ist übernommen. Letzter Meilenstein: <X>.
> Nächster Schritt: <Y>. Stufe: <Z>."

Kein STOPP. Der Agent arbeitet direkt weiter.

---

## WAS DIESER PROMPT NICHT MACHT

- Keine **neue** Session starten → das ist `SESSION_START_PROMPT.md`.
- Kein **Handover** bauen → das ist der `session_handover_generator`-Skill.
- Kein **Board reparieren** → das ist Operator-Handarbeit per `git edit`.
- Keine **Vorgänger-Session übernehmen** (`status: übergeben`/`erledigt`) → das ist
  `SESSION_START_PROMPT.md` Phase 1.2.

---

## ABNAHME-CHECKLISTE

- [ ] Operator-Eingabe (SESSION-TITEL + GRUND + ZIELE) im Chat erhalten
- [ ] Session-Ordner existiert
- [ ] WORKSPACE/INDEX.md-Zeile hat `status: aktiv`
- [ ] Living-Files gelesen (task, walkthrough, decision_log, ggf. implementation_plan)
- [ ] Chat-Bestätigung Phase 1 ausgegeben
- [ ] task.md um Overtake-Notiz erweitert (nicht überschrieben)
- [ ] walkthrough.md um Overtake-Eintrag erweitert
- [ ] _predecessor_* nicht verändert
- [ ] Phase 4 Bestätigung im Chat
- [ ] Mit aufgabenspezifischem Prompt fortgesetzt

---

## CHANGELOG

- **v1.1 (2026-07-17):** **Pfad-Doktrin nachgezogen** (Session KANON-ROLLOUT-REPARATUR_12, Fix F2).
  Dieser Prompt war auf dem Stand VOR der v2.4-Korrektur des `SESSION_START_PROMPT` und hatte
  **gar keinen Repo-Root-Anker** — er löste `WORKSPACE/<titel>` relativ ohne definierte Basis auf
  und reproduzierte damit exakt die Fehlerklasse („Agent sucht Workbench im Dateisystem"), die im
  Startprompt ~20 Anläufe gekostet hat. Neu:
  - **Phase 1.0** (Repo-Root zuerst): `git rev-parse --show-toplevel` als einzige Basis,
    4-Fälle-Tabelle mit harten STOPPs (rev-parse-Fehlschlag · kein WORKSPACE · Root-Mismatch).
  - **Absolutes Suchverbot** + optionaler Prüfsummen-Block `ERWARTETER REPO-ROOT` im Kopf —
    identisch zu `SESSION_START_PROMPT.md` v2.5, damit beide Prompts EINE Doktrin sprechen.
  - Pfad in 1.1 auf `$root/WORKSPACE/...` umgestellt.
- **v1.0 (2026-07-12):** Initiale Fassung. Entstanden aus dem 09-Agent-Vorfall, der mit
  `SESSION_START_PROMPT.md` versucht hat, eine bestehende Session mit `status: aktiv` zu
  „übernehmen". Trennung der beiden Use-Cases (NEUE Session vs. BESTEHENDE Session übernehmen).