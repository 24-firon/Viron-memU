<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# RECOVERY_PROTOCOL — Wenn etwas schiefgeht: selbst korrigieren, nicht eskalieren

> **Version:** 1.0 · **Status:** LEBENDES DOKUMENT, versioniert wie die anderen Kanon-Dateien
> (gleicher Ordner: `KANON_STRUKTUR_SPEC.md`, `SESSION_START_PROMPT.md`, `GIT_BASELINE.md`,
> `ROLLOUT_BOARD.md`).
>
> **Ownership:** MANAGED (Kanon-Kern, wird in Ziel-Repos nachgezogen)
>
> **Was das hier ist:** Die vierte Kanon-Datei. Sie beantwortet die Frage, die das System bisher
> **gar nicht** gestellt hat: *Was tust du, wenn du merkst, dass DU einen Fehler gemacht hast?*
>
> **Warum es das braucht (der Schmerz, belegt):** Das System kannte bisher nur zwei Reaktionen —
> **STOPP + Operator fragen** oder **gar nichts**. Jeder reale Fehlstart (der 09-Agent, die zwei
> Fehlstarts am 2026-07-14/15) wurde **nachträglich durch Prompt-Editieren** repariert. Die
> Changelogs SIND das Fehlerarchiv — aber kein Agent kann daraus **zur Laufzeit** handeln.
>
> Operator, wörtlich (2026-07-17):
> > „Es ist ja okay, wenn ein Agent was falsch versteht, aber dann muss es halt nicht ausarten,
> > sondern korrigiert werden. Und das voll autonom. vom Skill aus selbst zum Beispiel."
>
> **Herkunft:** MASTER_BEFUND §6.2 (`WORKSPACE/KANON-ROLLOUT-REPARATUR_12_…/desk/`) + globale
> Regel 7 (Reversibilitäts-Doktrin). Entscheid: D-004 (Session `KANON-HAERTUNG_13`).

---

## 0. Das Grundprinzip: Reversibilität, nicht Wichtigkeit

**Ein Agent kann „Wichtigkeit" nicht beurteilen — „Reversibilität" schon, deterministisch.**

Das ist der ganze Trick. Statt zu raten, ob etwas wertvoll ist (unmöglich, führt zu Datenverlust
oder zu Lähmung), fragst du **eine Frage mit einer maschinellen Antwort**:

```bash
git ls-files --error-unmatch <pfad>    # Exit 0 = getrackt · Exit 1 = untracked
```

| Zustand | Bedeutung | Was du DARFST |
|:--|:--|:--|
| **getrackt + committet** | Jede Änderung ist rückholbar (`git revert`, `git checkout`) | **Autonom korrigieren.** `git mv` (Historie bleibt), Umbau, Aufräumen — ohne zu fragen. Dokumentieren im `walkthrough.md`. |
| **untracked / gitignored** | Löschen wäre **endgültig** — kein Papierkorb, keine Historie | **Nur verschieben, NIE löschen.** Operator fragen. (So gingen bereits Kanon-Prompts verloren.) |

**Merke:** Autonomie ist kein Freibrief, sondern eine Folge von Reversibilität. Wo du zurück kannst,
darfst du handeln. Wo nicht, fragst du.

---

## 1. Die Symptom-Tabelle (die eigentliche Arbeitsgrundlage)

Alle Fälle sind **real aufgetreten** — keiner ist konstruiert.

| # | Symptom | Diagnose (wie du es erkennst) | **Autonome Korrektur** | Beleg |
|:--|:--|:--|:--|:--|
| **R-1** | **Strukturen am falschen Ort angelegt** (Werkbank, `desk/`, Session-Ordner) | Dein angelegter Pfad liegt nicht unter `<repo-root>/WORKSPACE/` | **Zurückbauen.** Getrackt → `git mv` an den richtigen Ort. Untracked → `cp` → verifizieren (Datei > 0 Bytes, Inhalt stimmt) → `rm` am Alt-Ort. **Nicht liegenlassen, nicht fragen, ob du aufräumen darfst.** Vorgang in `walkthrough.md` belegen + im Chat melden. | 09-Agent, 2 Fehlstarts 07-14/15 |
| **R-2** | **Falsches Repo** | ermittelter Root ≠ `repo_root_abs` (HANDOVER) bzw. ≠ `ERWARTETER REPO-ROOT` (Startprompt-Kopf) | 🛑 **STOPP — der einzige Fall OHNE autonome Korrektur.** Beide Pfade im Klartext melden: „Erwartet: `<X>` · Tatsächlich: `<Y>`". **Nichts anlegen, nichts suchen, nicht in den Erststart-Modus fallen.** DENN: Im falschen Repo ist jede „Korrektur" ein zweiter Fehler. | v2.5 §1.1 |
| **R-3** | **Board-Inkonsistenz** — `WORKSPACE/INDEX.md` sagt `aktiv`, das HANDOVER sagt `übergeben` | Zeile vs. YAML-Feld `status:` widersprechen sich | **HANDOVER gewinnt** (es ist das Ende-Artefakt, geschrieben als letztes). Board per `edit` nachziehen, Diskrepanz im `walkthrough.md` vermerken. **Kein STOPP** — das ist Buchhaltung, keine Architekturfrage. | 09-Vorfall („Leicht-Bundle ohne Ritual") |
| **R-4** | **Vorgänger mehrdeutig** | Mehrere Kandidaten mit `übergeben`/`erledigt`, kein eindeutig jüngster | Reihenfolge: **Board** (`WORKSPACE/INDEX.md`) → **mtime** → **STOPP**. Nie raten, nie nach Ordnername sortieren (TASK steht vorne, Alphabet ≠ Chronologie). `aktiv`/`geplant` sind **keine** Vorgänger (S-2). | `STEP_1A_PREDECESSOR` |
| **R-5** | **Template-Kopie unangepasst** — Living File trägt noch „Template für…" + Platzhalter-Header | `grep "Template für\|\[SESSION-TITEL\]\|\[REPO-ROOT\]"` in deiner `desk/`/`handover/` | **Sofort nachziehen** (Session-Header, Root, Task-Bezug). Eine unangepasste Kopie ist **kein** Living File. Kein STOPP, kein Fragen — das ist Nacharbeit an der eigenen Mechanik. | real: Session 13 erhielt unangepasste Kopien |
| **R-6** | **`git status` dirty von einer Fremd-Session** | Änderungen, die du nachweislich nicht verursacht hast | **Dokumentieren, NICHT committen, weiterarbeiten.** Kein Blocker. Fremde Arbeit gehört nicht in deinen Commit — im `walkthrough.md` + HANDOVER vermerken. | Session 12/13 |
| **R-7** | **Skill-/Master-Pfad nicht erreichbar** | `~/.claude/skills/…` bzw. `PLAYGROUND/Kanon_Rollout/` fehlt | **Auf den CDS-Mirror ausweichen** (`STORAGE/templates/`, Modell B: Skill = Autorität, Mirror = Fallback) und den Ausfall melden. Kein STOPP — fail-open, aber gemeldet. | B-10 |
| **R-8** | **Fork/Doppel-Instanz** — deine Board-Zeile steht schon auf `aktiv` mit fremder Kennung, oder dein `<next-session>`-Bundle hat bereits Inhalt | Board-Claim schlägt fehl (STEP_1A 1.3.0) | 🛑 **STOPP.** Operator fragen: „Läuft eine Parallel-/Fork-Instanz?" **Nichts überschreiben**, kein eigenes Bundle bauen. DENN: Zwei Instanzen, die dasselbe Bundle schnüren, zerstören einander. | Session 03 |
| **R-9** | **Kontext-Kompaktierung erkannt** | Du erinnerst Payloads/Entscheidungen nur vage; der Verlauf wirkt abgeschnitten | `walkthrough.md` + Payload-Log lesen → Payloads gezielt neu laden → im Log vermerken. Kein STOPP. | Routing-Protokoll §3 |
| **R-10** | **Gelesener Stand ≠ Ist-Stand** (Drift durch Parallel-Arbeit) | Deine Aussage über eine Datei widerspricht dem, was `grep`/`git log` zeigt | **Ist-Stand gewinnt, immer.** Neu greppen, eigenen Befund korrigieren, Korrektur offen benennen (nicht stillschweigend anpassen). **Vorgänger-Artefakte VOR der eigenen Analyse lesen**, nicht danach. | real: Session 13 las 4 Prompts je eine Version zu alt, während Session 12 parallel fixte |

---

## 2. Der Ablauf (immer gleich, vier Schritte)

```
1. SYMPTOM erkennen      → Tabelle §1. Nicht weiterarbeiten, als wäre nichts.
2. DIAGNOSE stellen      → Reversibilität prüfen (§0): git ls-files --error-unmatch <pfad>
3. KORRIGIEREN           → getrackt: autonom (git mv/Umbau) · untracked: verschieben + fragen
                           · R-2/R-8: STOPP (die einzigen zwei)
4. BELEGEN               → walkthrough.md: Was war falsch, was hast du getan, Beweis (Befehl+Output).
                           Im Chat melden — kurz, ohne Entschuldigungs-Prosa.
```

**Was NICHT passiert:**
- ❌ Kein „ich frage mal lieber, ob ich meinen eigenen Fehler aufräumen darf" bei reversiblen Dingen.
- ❌ Kein stilles Weiterarbeiten über einen erkannten Fehler hinweg (No Silent Failures).
- ❌ Keine Entschuldigungs-Schleifen. **Melden ist Pflicht, Zerknirschung ist Rauschen.**
- ❌ Kein Löschen von Untracktem. Niemals.

---

## 3. Abgrenzung — wann trotzdem STOPP

Autonome Korrektur gilt für **deine eigenen, reversiblen Fehler**. Sie ist **kein** Freibrief für:

| Fall | Warum STOPP |
|:--|:--|
| **Falsches Repo (R-2)** | Jede Aktion dort ist ein zweiter Fehler — auch das „Aufräumen". |
| **Fork/Parallel-Instanz (R-8)** | Du siehst die andere Instanz nicht. Korrektur = Kollision. |
| **Untrackte Daten** | Verlust wäre endgültig. Verschieben ja, entscheiden nein. |
| **Fremde Working Copy / fremdes Repo** | Übergriffig. Nur der Operator entscheidet. |
| **Der Fehler ist eine Entscheidung, kein Versehen** | „Ich habe die Architektur missverstanden" korrigiert man nicht im Vorbeigehen — das ist ein Gateway. |

**Faustregel:** *Mechanik korrigierst du selbst. Urteil legst du vor.*

---

## 4. Verhältnis zu den anderen Kanon-Dateien

| Datei | Rolle | Verhältnis |
|:--|:--|:--|
| `SESSION_START_PROMPT.md` v2.5 | **verhindert** den Fehler (Root-Anker, STOPPs, Suchverbot) | greift VORHER |
| **`RECOVERY_PROTOCOL.md`** (dies) | **heilt** ihn, wenn er trotzdem passiert | greift NACHHER |
| `GIT_BASELINE.md` | liefert das **Sicherheitsnetz** (tracken+committen), das autonome Korrektur überhaupt erlaubt | ist die **Voraussetzung** |
| `KANON_STRUKTUR_SPEC.md` | definiert das Ziel-Raster (u.a. EINE Archiv-Zone) | liefert das Soll |

> **Die Kette:** Ohne `GIT_BASELINE` (alles getrackt) gibt es keine Reversibilität. Ohne
> Reversibilität keine autonome Korrektur. Ohne autonome Korrektur eskaliert jeder Fehler zum
> Operator — genau der Zustand, den dieses Dokument beendet.

---

## 5. Changelog

- **v1.0 (2026-07-17):** Initiale Fassung. Session `KANON-HAERTUNG_13_KANON-ROLLOUT_CDS_2026-07-17`,
  Entscheid D-004. Quellen: MASTER_BEFUND §6.2 (Symptom-Tabelle) + §6.3 (Reversibilitäts-Doktrin),
  globale CLAUDE.md Regel 7, Operator-O-Ton 2026-07-17.
  Neu gegenüber der MASTER_BEFUND-Vorlage: R-5 (unangepasste Template-Kopie) und R-10 (gelesener
  Stand ≠ Ist-Stand) — beide **in der Session real aufgetreten**, die sie geschrieben hat.
