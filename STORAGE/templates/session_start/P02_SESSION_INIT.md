<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# P02 — Session Init

> **EXECUTION-MODE.** Erst das Projekt begreifen, dann die Arbeitsweise, dann Comprehension Gate, dann Plan-Verweis. **DENN** ohne verstandenes Projekt und ohne Hard-Stop springt der Agent blind zu Aktionen.
> **Repo-Root (absolut):** `[REPO-ROOT]`
> **Session:** `[SESSION-TITEL]`

---

## TEIL 1 — PROJEKT VERSTEHEN (in eigenen Worten, kein Recall)

> Nach P00 (Tier-1 gelesen) + P01 (Verständnis geprüft) rekonstruierst du das Projekt AKTIV — in eigenen Worten, nicht abgeschrieben. Das ist der Beweis, dass du es begriffen hast, nicht nur gelesen.

### 1.1 Was ist dieses Projekt?
- **Zweck / Mission:** [Wofür existiert das Projekt? Endziel — 1-2 Sätze.]
- **Aktueller Stand:** [Was ist gebaut, was fehlt, wo hakt es?]
- **Diese Session konkret:** [Was soll DIESE Session erreichen? Warum jetzt? Woran ist Erfolg messbar?]

### 1.2 Struktur-Landkarte (wie ist es aufgebaut?)
- **Kern-Zonen / Ordner:** [Die 3-5 wichtigsten Verzeichnisse + je 1 Zeile wofür.]
- **SSoT-Dateien:** [Wo steht die Wahrheit? z.B. CLAUDE.md, INDEX.md, Register, _BUNDLE_MAP.md ...]
- **TABU / READ-ONLY:** [Was darf NICHT angefasst werden? Fremd-Repos, Live-Skills, Quellen ...]

**BEWEIS (im Chat abgeben):**
> „Projekt verstanden. Zweck: [1 Satz]. Diese Session: [1 Satz]. Kern-Zonen: [Liste]. TABU: [Liste]."

---

## TEIL 2 — ARBEITSWEISE IN DIESEM PROJEKT (projektspezifisch)

> Nicht wie man generell Git/Docker/Tools bedient — dafür gibt es eigene Skills. Sondern WIE HIER gearbeitet wird. Fülle nur, was in DIESEM Projekt wirklich gilt; verweise auf die konkrete Regel/Datei.

| Aspekt | Konvention in DIESEM Projekt | Quelle/Regel |
|:---|:---|:---|
| **Workspace / Ablage** | [Wo landet Arbeit? Ein Ordner pro Session? Struktur?] | [Datei/Regel] |
| **Namensgebung** | [Nach Zweck/Empfänger statt Absender? Bundle-ID-Regeln?] | [Datei/Regel] |
| **Persistenz / Living Files** | [Was muss sofort in Dateien? Wann Living Files pflegen?] | [Datei/Regel] |
| **Delegation** | [Was wird delegiert — SKRIPT / Subagent S1–S5 (kritischer Schnitt → S5-Chirurg-Subagent) / selbst nur Orchestrierung+Buchhaltung (MILESTONE_GATEWAY §5)? Verify-Gate beim Orchestrator?] | [Datei/Regel] |
| **Beweispflicht** | [Wie wird Fortschritt belegt? Reports, Diffs, Terminal-Output?] | [Datei/Regel] |
| **O-Ton-Erhalt** | [Operator-Erklärungen wörtlich, nicht zu Kurzformeln verdichten (Gesetz 2).] | [Datei/Regel] |
| **STOPP-Pflicht** | [Wobei immer erst Operator-GO? Was nie blind tun?] | [Datei/Regel] |

**BEWEIS (im Chat abgeben):**
> „Arbeitsweise erfasst. Die 3 wichtigsten Regeln hier: [1] [2] [3]. Wobei ich STOPP mache: [...]."

---

## TEIL 3 — COMPREHENSION GATE (HARD STOP)

BEVOR operative Arbeit beginnt, alle 4 Schritte:

### Schritt A: Kontext-Quelle klären
- [P00-Leseliste (aktiv gelesen) + CLAUDE.md (auto-geladen)?]
- **BEWEIS:** „[Y] Tier-1-Dateien aus P00 physisch gelesen. CLAUDE.md + @-Imports auto-geladen. Kontext-Quelle: P00 + CLAUDE.md."

> **Injektions-Notiz (F28, D-003 — 3 Varianten, KEIN binäres MIT/OHNE):** Die Kontext-Quelle hängt
> vom Repo ab (Injektions-Check, INSTRUCTIONS 6.0): **Variante A (VOLL)** = injizierter Kontext
> (per P00-Checkfragen VERIFIZIERT!) + P00-Restliste + CLAUDE.md; **Variante C (TEILWEISE)** =
> Root-`CLAUDE.md` mit `@`-Imports lädt einen kleinen Kern automatisch (per Checkfragen wie A
> VERIFIZIERT) + Rest über STORAGE-Router oder P00-Tier-1 aktiv gelesen; **Variante B (NEIN)** =
> P00 (aktiv) + CLAUDE.md (auto, falls überhaupt vorhanden). Ein Repo mit Root-CLAUDE.md-`@`-Imports
> ist NIEMALS „NEIN" — das war der D-003-Fehler (CLAUDE.md-Auto-Load fälschlich als „OHNE Injektion"
> behandelt). Beide Frameworks werden unterstützt — Claude Code injiziert via SessionStart-Hook +
> `.claude/context-inject.json`, OpenCode via `opencode.jsonc → instructions`.

### Schritt B: Referenzen verifizieren (per ls/glob, BEVOR du sie annimmst)
- [Die kritischen Pfade/Referenzen aus P00 real prüfen — beim ersten toten Ref STOPP.]
- **Drift-Check:** Hat eine Parallel-Session die Struktur seit dem Handover verändert?

### Schritt C: Bestätigung
> „Comprehension Gate bestanden. Projekt + Arbeitsweise dargelegt. [Y] Tier-1-Dateien gelesen, Referenzen verifiziert. Bereit für operative Arbeit."

### Schritt D: Rollback-Plan (vor dem ersten Edit)
- [Git-Status sauber? — Backup-Strategie? — Ab wann ist ein Rollback nötig?]

**Ohne Bestätigung: KEINE EDITS. KEINE BASH-BEFEHLE. KEINE SUB-AGENTS.**

---

## TEIL 4 — PLAN-VERWEIS (P02 enthält KEINEN Meilenstein-Plan — D-005)

> **P02 ist Session-Init, kein Implementation Plan** (Operator-Entscheid 2026-07-11, D-005
> Session 06, O-Ton: „P02 hat keinen Implementation Plan. Der Implementation Plan ist das, was
> geplant ist, und Walkthrough ist das, was wirklich passiert ist."). Die Meilensteine, Stufen und
> GATEWAY-Blöcke leben im Living File **`../desk/implementation_plan.md`** (bzw. bei kleinen,
> linearen Sessions direkt in `../desk/task.md`) — dort werden sie WÄHREND der Session
> fortgeschrieben. P02 ist nach Fertigstellung Tabu-Zone — ein Plan, der hier stünde, könnte nie
> aktualisiert werden.

- **Der Plan:** `../desk/implementation_plan.md` — [X] Meilensteine, je mit Stufe (S1–S5) und
  GATEWAY-Block (MILESTONE_GATEWAY §3). [1-Satz-Überblick: M0 … M<N> …]
- **Erster Meilenstein ist IMMER M0 (Session-Start-Mechanik):** Board-Claim + STEP_1A +
  Checkpoint-Commit — **S1–S2 oder SKRIPT**, NIE die Planungs-Stufe (Anti-Farce-Gate,
  MILESTONE_GATEWAY §2c). Details + Gateway-Blöcke: im Plan.
- **Realität dokumentieren:** Was pro Meilenstein WIRKLICH passiert (inkl. Fehler/Schleifen/
  Subagenten), gehört in `../desk/walkthrough.md` (+ ggf. `../desk/walkthrough/M<N>_<name>.md`)
  — nicht in diese Datei, nicht in den Plan.

---

## SUBAGENT-PROTOKOLL (Claude Code idiomatisch)

**Grundregel — Claude-Code-Eigenheit:** Subagenten starten **kalt** (frischer Kontext, KEINE Vererbung von Eltern-Verlauf oder CLAUDE.md). Fortsetzung desselben Subagenten ist nur experimentell (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` + `SendMessage`). → **STOPP/GO gehört in den MAIN-Thread ZWISCHEN einzelne, je voll gebriefte Subagent-Aufrufe** — NICHT mid-task im selben Subagent.

**Stufenwahl:** Stufe pro Subagent im Briefing (MODELL-Säule = Stufe S1–S5, MILESTONE_GATEWAY §2); technisch in CC pro Subagent im Frontmatter-Feld festlegbar (Mechanik — das Mapping Stufe→konkretes Modell macht der Operator, KEINE Namens-Defaults). Im Main via `/model`. **NICHT** `Explore`/`Plan` für handover-kritisches Lesen verwenden — diese Built-ins überspringen CLAUDE.md und Git-Status.

**Chirurg-Delegation:** Kritische Schnitte (Formulierung/Code/Architektur/tiefe Diagnose) gehen bevorzugt an einen **S5-Chirurg-Subagenten** — die Orchestrator-Hauptsession schneidet nicht selbst, sie brieft, spawnt, prüft und integriert (MILESTONE_GATEWAY §2b/§5).

**VOR jedem SubAgent:** STOPP + Operator nach Modell fragen (oder Frontmatter setzen) + 4-Säulen-Briefing:

```
MISSION:   [Warum diese Aufgabe? Was passiert, wenn sie nicht erledigt wird?]
CONTEXT:   [Welche Dateien MUSS der Sub-Agent lesen? Exakte Pfade. ANNAHME: er hat KEINEN Vor-Kontext.]
SCOPE:     [Was darf er anfassen / was ist TABU? Sub-Sub-Agents ERLAUBT (D-001, 2026-07-18) — Briefing-Pflicht kaskadiert (4 Säulen je Spawn), Verify-Gate beim jeweiligen Orchestrator.]
SCHRITTE:  [Atomare Schritt-für-Schritt-Anleitung + wohin der Bericht kommt + wann STOPP.]
STUFE:     [S1–S5 laut MILESTONE_GATEWAY §4 — oder "STOPP für Stufen-Klärung" wenn unklar]
```

**Zwei Muster für mehrstufige Subagent-Aufgaben:**
- **(a) Komplett-Auftrag:** Subagent macht Schritte 1–4 am Stück, Main-Thread reviewt nur den Endbericht. STOPP NUR am Ende.
- **(b) Gestaffelter Auftrag:** Zwei getrennte, je voll gebriefte Subagent-Aufrufe (1–2, dann 3–4). STOPP/GO im Main-Thread ZWISCHEN den Aufrufen. **Empfohlen** wenn das Zwischenergebnis die zweite Briefung beeinflusst.

Nach jedem SubAgent-Report: STOPP, Bewertung, Integration in LIVING_FILES, GO. Verify-Gate bleibt beim Orchestrator. Jede Subagenten-Aussage mit Beleg (Zitat/Zeile) — sonst gegenprüfen.

---

## STUFENWECHSEL-ENTSCHEIDUNG (pro Gateway)

Stufen: **S1–S5** (Charakter) × **Intensität** (Low gesperrt · Medium Boden · High Standard ·
Extra/Max nur kritisch) — normativ in `references/MILESTONE_GATEWAY.md` §2 (keine Modellnamen).

```
GATEWAY-N: Erwartete Stufe [S1|S2|S3|S4|S5]·[Intensität] · Aktuell [ ] · Wechsel [JA→STOPP / NEIN→weiter]
```

**STOPP-Pflicht bei Stufenwechsel:** kein Weitermachen ohne explizites „Go" vom Operator.

---

## 4 GESETZE DER PERSISTENZ (Verweis)

1. **KEINE LÖSCHUNG** — archivieren statt löschen
2. **KEINE REDUKTION** — 100% Erhalt, keine Abkürzungen, **O-Töne wörtlich**
3. **BEWEISPFLICHT** — physische Artefakte (Reports, Diffs, Terminal-Output)
4. **INTEGRATION** — Korrekturen an die richtige Stelle (`edit`), neue Phasen ans Ende (append)

Detail → `references/KONSERVIERUNGS_GESETZE.md`

---

## MINDSET

- **Surgical Precision:** Dateien nur nativ ändern (`edit`/`write`).
- **Evidence-Based:** Traue keinem `exit 0` — liefere Output.
- **Linearer Gehorsam:** Schritte nacheinander, nicht parallelisieren.
- **Approval-Gates:** Kritische Aktionen brauchen „GO".
- **Struktur frisch scannen:** nie der mentalen Karte trauen.
- **Fremd-Thema ablehnen:** Aufgaben außerhalb des Session-Scopes sofort ablehnen, nichts anfassen.

---

## BESTÄTIGUNG

> „P02 initialisiert. Projekt + Arbeitsweise dargelegt. Gate bestanden. [Y] Tier-1-Dateien, Referenzen geprüft, Rollback-Plan steht. Plan-Verweis geprüft (`../desk/implementation_plan.md`, [X] Meilensteine). Bereit für Ausführung."

⏸️ **STOPP** — Nach Plan-Freigabe kommt zuerst **M0 (Session-Start-Mechanik) = S1–S2 oder SKRIPT**, NICHT die Planungs-Stufe (Anti-Farce-Gate, MILESTONE_GATEWAY §2c). Also: Stufe senken bzw. Skript vorbereiten, DANN mit M0 starten.
