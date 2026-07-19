<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# P00 — Leseliste (erster Schritt im Session-Start)

> **Repo-Root:** Den liefert der SessionStart-Hook automatisch (SESSION-FAKTEN oben im Kontext) —
> hier NICHT nochmal eintragen. Alle Pfade unten sind relativ zum Repo-Root.
>
> **LESE-MODUS.** Lade alle Tier-1-Dateien physisch und mach dir pro Datei eine 3-5 Zeilen Notiz. **DENN** der nächste Schritt (P01_BOOTSTRAP) verlangt nachweisbares Verständnis der gelesenen Inhalte.

## ⛔ MERKSATZ (verbindlich, Leseliste-Prinzip 2026-07-18)

**Regeln stehen NICHT auf einer Leseliste — sie kommen injiziert; hier stehen nur Projekt- +
Task-Dateien.** Eine Leseliste enthält genau zwei Sorten Einträge: **(a) Projekt-Allgemeinwissen,
das für DIESE Task relevant ist** + **(b) task-spezifisches Material** — und zwar POSITIV
vollständig: **alle Dateien, die man WIRKLICH braucht, um die Aufgabe im höchsten Maße zu
erfüllen, MÜSSEN drauf.** Injizierte Regeln werden unten nur VERIFIZIERT, nie gelesen;
immer-gültige Orchestrierungs-Grundlagen sind Tier 1 oder injiziert, nie Tier 2.
*(Vollfassung + Herleitung: `references/LESELISTE_MECHANIK.md` §0.)*

---

## 📎 KONTEXT-INJEKTION (F28 — Ersteller trägt Ergebnis des 6.0-Checks ein)

**Injektion in diesem Repo:** `[VOLL — Quelle: <...> | TEILWEISE — CLAUDE.md-Auto-Load, <N> Dateien | NEIN]`

**Automatisch geladen — NICHT lesen, nur verifizieren:**
- `[Datei/Block]` — `[1 Zeile: was drinsteht]`
- `[...]`

**Verifikation** — 2-3 Checkfragen gegen den ECHTEN injizierten Inhalt (Ersteller formuliert sie
beim Bundle-Bau gegen die physisch geprüfte Injektionsquelle, nicht gegen Chat-Sekundärwissen):
- `[Checkfrage 1]` · `[Checkfrage 2]` · `[Checkfrage 3]`

Nicht beantwortbar ⇒ Injektion hat nicht gegriffen (häufigste Ursache: falsches cwd, B-10) ⇒ die
gelisteten Inhalte LESEND nachholen + im Bestätigungs-Block MELDEN (fail-open, aber gemeldet).
*(Varianten A/B/C im Detail, cwd-Falle B-10, Router-Filterung bei TEILWEISE, Historie:
`references/LESELISTE_MECHANIK.md` §1.)*

---

## Kurz-Checks vor Tier 1

- **⛔ F27 Report-Regel:** Kein VOLLER Forensic-Report auf dieser Liste (der ist ÜBER den
  Vorgänger); Derivate/Extrakte FÜR den Nachfolger (SUMMARY, Extraktions-Reports mit neuen
  O-Tönen) gehören dagegen auf Tier 1. *(Beispiele + Heuristik: `LESELISTE_MECHANIK.md` §2.)*
- **⚠️ Drift-Check (PFLICHT):** `git log --since="<date: aus HANDOVER.md dieser Session>" --oneline`
  — bei >0 Commits WARNUNG an Operator, sonst weiter. *(Deterministische Befehlsfassung + S-7-Fix:
  `LESELISTE_MECHANIK.md` §3.)*

---

## VOR DEM START

Bestätige den Lese-Start:
> "Ich beginne jetzt mit dem Lesen der Tier-1-Dateien. Nach dem Lesen: bereit für P01_BOOTSTRAP."

---

## TIER 1 — PFLICHT (aktiv lesen)

> Was laut Injektions-Block oben automatisch geladen ist, steht hier NICHT (Doppellese-Verbot —
> nur verifizieren). Jeder Eintrag trägt ein Ein-Zeilen-Warum. **Vollständigkeits-Pflicht:** Jede
> Datei, die ein Meilenstein des `implementation_plan.md` als Pflichtlektüre braucht, steht hier —
> oder ihre spätere Ladung ist im Plan ausdrücklich begründet.

### A) Projekt-Allgemeinwissen — nur was für DIESE Task relevant ist
- [ ] `[Datei, z.B. AGENTS.md/README.md — falls nicht injiziert]` — `[1 Zeile Warum: Repo-Identität, Zonen]`
- [ ] `[Immer-gültige Orchestrierungs-Grundlage, z.B. STATE_OF_THE_ART-WORKFLOW.md — falls nicht injiziert; NIE Tier 2]` — `[1 Zeile Warum]`
- [ ] `[Domain-SSoT / 1-2 zentrale DOCS-Dateien je nach Session-Fokus — NICHT alle]` — `[1 Zeile Warum]`

**Notiz (5 Zeilen):** Was ist die Mission? Was blockiert? Was sind die 3 Kern-Constraints?

### B) Task-Material — die Arbeitsgrundlage dieser Session
- [ ] `desk/task.md` — der aktuelle Auftrag (Scope, DoD, Blocker)
- [ ] `desk/implementation_plan.md` — der Bauplan (falls angelegt)
- [ ] `[Vorgänger-Living-Files: _predecessor_decision_log.md u.a.]` — `[1 Zeile: welche Entscheidungen bindend sind]`
- [ ] `[Report-DERIVAT des Vorgängers (SUMMARY/Extrakt) — F27-konform, nie der Voll-Forensic]` — `[1 Zeile Warum]`
- [ ] `[Task-spezifisches Material, z.B. Befund-/Lücken-Listen, Roadmaps — alles, was die Task WIRKLICH braucht]` — `[1 Zeile Warum]`

**Notiz (5 Zeilen):** Was ist der IST-Zustand? Was ist das SOLL? Welche Dateien sind betroffen?

---

## TIER 2 — BEI BEDARF (klar benannter Trigger, kein Abstellgleis für Pflichtwissen)

| Datei | Wann lesen |
|:---|:---|
| `[STORAGE/<topic>.md]` | `[Wenn <konkreter Task-Schritt> ansteht]` |
| `[Regel-QUELLEN nur als gekennzeichnetes **Task-Material** (z.B. Kandidaten-Korpus für Regel-Kuration) — NIE als „Regeln lesen"]` | `[Nur wenn der Task sie ausdrücklich braucht]` |

---

## WAS DU NICHT LIEST (SKIP)

- `node_modules/`, `.next/`, `dist/`, `build/` — Build-Artefakte
- `.git/` — Git-Metadaten
- `_ARCHIVE/` — Historisch
- `DELIVERY/` — Bundles, nicht für internes Verständnis

---

## BESTÄTIGUNG

> "P00 gelesen. [X]/[X] Dateien. 3 Notizen erstellt. Bereit für P01_BOOTSTRAP."

⏸️ **STOPP** — Stufe für den nächsten Schritt (P01): S4.
