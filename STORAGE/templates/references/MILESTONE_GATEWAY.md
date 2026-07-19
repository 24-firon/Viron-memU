<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht:**
>
> - Die 5 Arbeits-Stufen **S1–S5** — die EINZIGE normative Stufen-Definition des Skills
>   (alle anderen Dateien verweisen hierher, keine führt eine eigene Skala)
> - Das **MEILENSTEIN-GATEWAY**: Pflicht-Block an JEDEM ⏸️ STOPP (Modellwechsel-Orchestrierung)
> - Zuordnungsmatrix Arbeit→Stufe + Delegations-Entscheid SKRIPT vs. SUBAGENT vs. CHIRURG-SUBAGENT vs. SELBST
> - Verdrahtung: generierte P00/P01/P02 MÜSSEN Gateways/Stufen enthalten (DoD + Prüfschleife)
>
> - **Bundle-Verwendung:** systemisch, wird NICHT in die Arbeitskopie kopiert.
<!-- TEMPLATE-EXPLANATION-END -->

# MILESTONE_GATEWAY — Stufen S1–S5 & Meilenstein-Stopp-Protokoll

> **Wann lesen:** Beim Bauen der Startprompts (Schritt 5/6 — die Fahrpläne ERBEN dieses Format),
> an JEDEM Meilenstein-STOPP der eigenen Session, vor jedem Subagent-Spawn und vor jeder
> Delegations-Entscheidung.

## 1. Warum es dieses Gateway gibt

Der Operator fährt ein Modell-Portfolio von extrem schnellen Instruct-Modellen bis extrem
reasoning-starken Modellen und wechselt das Modell der Hauptsession **manuell an
Meilenstein-Grenzen**. Die Session kennt die konkreten Modellnamen nicht und nennt nie welche —
sie kennt nur **Stufen**. Damit der Operator wechseln kann, MUSS die Session an jedem STOPP
ansagen: was fertig ist, was als Nächstes kommt, welche Stufe dafür erwartet wird und ob
delegiert wird. **Ein STOPP ohne diese Ansage ist wertlos** — der Operator kann dann weder
wechseln noch delegieren noch priorisieren.

## 2. Das Stufen-Modell (zweiachsig — normativ, einzige Quelle im Skill)

Eine „Stufe" hat ZWEI Achsen. Beide zusammen ergeben die reale Abstufung (~10 Kombinationen).

**Achse A — Charakter der Stufe** (was für ein Kopf arbeitet):

| Stufe | Charakter | Typischer Einsatz |
|:--|:--|:--|
| **S1** | Instruct, **Kleinkontext** | NUR Leselisten/Massen-Reads am Session-Start (Kontextfenster zu klein für mehr) |
| **S2** | ausgewogen, Arbeitsboden | atomare Ausführung nach explizitem Plan, Cleanup, Kopier-/Struktur-Operationen |
| **S3** | ausgewogen, erhöht | Standard-Ausführung, Code, Einbau vorformulierter Blöcke, Reviews |
| **S4** | Reasoning-Standard | Planung, Forensik, Bewertung an STOPPs, Reports, Orchestrierung |
| **S5** | Reasoning-**strategisch** | die kritischen, präzisen Schnitte: echte Umsetzung (Formulierung, Code, Architektur), Grundsatz/Neu-Planung, Endabnahme — anderer Charakter, nicht bloß „stärker" (siehe §2b) |

**Achse B — Intensität** (wie tief dieselbe Stufe rechnet):

- **Low = IMMER gesperrt.** Auch die stärkste Stufe wird auf Low unbrauchbar. Nie einsetzen.
- **Medium = Arbeitsboden** (unterste zulässige Intensität für echte Arbeit).
- **High = Standard** für die meiste Arbeit.
- **Extra/Max = nur wenn wirklich kritisch** — höhere Intensität bringt erfahrungsgemäß kaum
  Mehrwert, aber stark steigende Kosten. Bewusst dosieren.

Eine vollständige Angabe lautet also z.B. **„S4·High"** oder **„S5·Max"**. Wo dieser Text nur die
Charakter-Stufe nennt (`S3`), ist Intensität = Arbeitsstandard (Medium–High) gemeint.

**Regeln:**
- Der Skill nennt **NIE konkrete Modellnamen** — weder als Empfehlung, noch in STOPP-Zeilen,
  noch in Subagent-Briefings. Das Mapping Stufe→konkretes Modell macht der Operator aus seinem
  Portfolio. (Ausnahmen: `ersteller:`-Metadaten dokumentieren die tatsächliche Herkunft als Fakt;
  technische Mechanik-Hinweise wie „Modellwahl per Frontmatter/`/model`" bleiben ohne Namen.)
- **Jede Charakter-Stufe ist je nach Auftrag als Subagent spawnbar** — die strategische
  Stufe (S5) kommt sogar BEVORZUGT als Subagent (siehe §2b: der Chirurg operiert im Regelfall
  delegiert, mit frischem Kontext).
- **Historie:** Diese Achsen ersetzen die früheren Skalen `FAST/MIDDLE/STRONG` (3-stufig) und
  `⚡ LIGHT / 🟡 MITTEL / 🟢 STANDARD / 🔴 STARK` (4-stufig, Ampel-Emojis). Alt-Vorkommen werden
  bei Sichtung auf S1–S5 gehoben. **Nicht verwechseln:** Die Token-Ampel 🟢🟡🔴⚫ in
  `TOKEN_WINDOW_GUARD.md` ist eine BUDGET-Ampel, keine Stufen-Skala — sie bleibt unverändert.

## 2b. Orchestrierungs-Doktrin (Chirurg-Prinzip — vorausgesetzt, nicht optional)

Der Skill setzt diese Arbeitsteilung als selbstverständlich voraus (kurz, weil bekannt):

> **Die strategische Stufe (S5) ist der Chirurg.** Sie wird für die kritischen, präzisen Schnitte
> gerufen — die echte Umsetzung: Texte final formulieren, Code schreiben, Architektur festlegen,
> Endabnahme. Alles davor — Vorbereitung, Recherche, Massen-Edits, Review, „Visite" — machen
> leichtere Stufen (S1–S4), als Hauptsession oder als Subagenten. Der Chirurg macht nicht die
> Visite und wischt nicht den Boden.

**Orchestrator-Hauptsession ≠ Chirurg (Operator-Korrektur 2026-07-18).** Fährt die Hauptsession
ein teures Reasoning-/Orchestrator-Modell, ist sie der **Assistent des Chirurgen**, nicht der
Chirurg selbst: Sie plant, zerlegt, brieft, spawnt den S5-Chirurg-Subagenten, empfängt und prüft
dessen Ergebnis (Verify-Gate), integriert es und kommuniziert mit dem Operator — den Schnitt
führt sie NICHT selbst aus, **DENN** jede selbst ausgeführte Umsetzung verbrennt teuren
Orchestrator-Kontext mit Arbeit, die ein frisch gestarteter, gezielt bemodellter Subagent
billiger und mit sauberem Kontext erledigt. O-Ton Operator: „Opus ist der Orchestrator, der
Assistent des Chirurgen. Er gibt dem Chirurg Bescheid, wenn er gebraucht [wird], und dann
spawnst du einen Fable Subagent."

Praktische Konsequenz für jeden Meilenstein: **planen → delegieren → orchestrieren.** Wer plant
(S4/S5) zerlegt die Arbeit und brieft; wer ausführt, bekommt genau seine Stufe; für den einen
kritischen Schnitt wird gezielt S5 gerufen — **bevorzugt als S5-SUBAGENT** mit frischem Kontext;
ein Hauptsession-Wechsel auf S5 ist die Ausnahme für Fälle, in denen der nötige Sessionkontext
nicht sinnvoll in ein Briefing passt — danach sofort zurück zur Orchestrierung. **Ausnahme vom
Delegieren:** winzige, exakt vorformulierte Änderungen ohne Reasoning-Bedarf sind Executor-Arbeit
(S3), kein „Schnitt" — die darf die Hauptsession selbst einbauen. **Nie alles auf einer Stufe
durchziehen** — das ist entweder zu teuer (S5 für Putzarbeit) oder zu schwach (S2 für den Schnitt).

Diese Doktrin steuert den Delegations-Entscheid in §5 und die STUFE-Zeile jedes Gateways in §3.

## 2c. Der kritischste Stufenwechsel: Plan-Freigabe → Ausführung (ANTI-FARCE-GATE)

Direkt nach der Planung (S4/S5) kommt fast IMMER **Mechanik**: Ordner anlegen, Vorgänger-Living-Files
kopieren (STEP_1A), Status-Board umstellen, Checkpoint-Commit. Das ist **S1–S2 oder — besser — EIN
SKRIPT** (§5 Prio 1), NIEMALS Arbeit für die teure Planungs-Stufe.

> **Die Falle (real passiert):** Der Operator gibt den Plan frei — und die Session, noch auf der
> Planungs-Stufe (z.B. S5·High), rutscht direkt ins `cp`/`mkdir`/`git`. Ein strategisches
> Reasoning-Modell kopiert Dateien. Das ist Geldverbrennung und ein Bruch der Chirurg-Doktrin
> (§2b: der Chirurg wischt nicht den Boden). O-Ton Operator: „dass er nachdem ich ihm den Plan
> freigebe einfach anfängt als Fable-Pfeife mit High-Reasoning Dateien zu kopieren, ist eine Farce."

**Pflicht-Gate:** Zwischen Plan-Freigabe und dem ERSTEN mechanischen Schritt steht ein GATEWAY-Block
(§3). Seine `👉 DU:`-Zeile senkt die Stufe: „Stell auf S1–S2 (oder führ die Session-Start-Mechanik
als Skript aus), dann GO." Erst nach dem Wechsel wird kopiert. Kein „ich mach das schnell noch auf S5".

**Am besten gar kein Modell:** Die Session-Start-Mechanik (mkdir + STEP_1A-`cp` + INDEX-Zeile +
Checkpoint-Commit) ist deterministisch → **ein einziges Skript**, geprüft, einmal gefeuert, Output
als Beweis. Dann braucht es dafür weder S5 noch überhaupt einen Stufenwechsel.

**Regel für Fahrplan-Ersteller:** Der ERSTE Meilenstein eines generierten Plans (Session-Start /
Buchhaltung / STEP_1A) trägt IMMER Stufe **S1–S2 oder `SKRIPT`** und ein eigenes Gate davor — nie
die Stufe des Planungs-Meilensteins erben. Ein Plan, dessen Mechanik-Schritte auf S4/S5 laufen, ist
FALSCH (Prüfung: INSTRUCTIONS 6.3-DoD + 7.0).

## 2d. Post-Plan-Freigabe-Gate (R-NEU-3, Operator-Regel 2026-07-18/19 — schärft §2c)

Eine Plan-Freigabe (ExitPlanMode approved / „Plan ist gut") ist NUR das Signal „der Plan ist
gut" — **kein Startsignal**. Unmittelbar danach, VOR jeder Ausführung, PFLICHT:

1. **Klartext-Bericht**, was der Plan enthält — der Operator liest Pläne nicht im Seitenfenster mit.
2. **Gegenfragen** zur Interpretations-Kontrolle (nur echte, keine Alibi-Fragen).
3. **Modell-Ansage** — Wechsel oder Bleiben EXPLIZIT ansagen (Format: §3-MODELL-Zeile).
4. **KOMPLETTER STOPP** bis GO. O-Ton Operator: „Das ist kein Signal zum Rennen."

**Technische Begründung, warum Punkt 3 „Ansage" heißt und nie entfallen darf
(Plan-Mode-Modell-Kontinuität, Operator-Korrektur 2026-07-19):** Der Agent verlässt den
Plan-Mode IMMER mit dem Modell, mit dem er hineinging — die Freigabe-Interaktion bietet
technisch keinen Wechsel-Mechanismus. Das nach der Freigabe aktive Modell ist also NIE eine
Operator-Entscheidung, sondern ein Artefakt des Plan-Mode-EINTRITTS. Daraus folgt hart:
**„Das richtige Modell läuft ja schon" ist als Weiterlauf-Begründung UNZULÄSSIG** — nach jeder
Plan-Freigabe kommt das STOPP-Gate mit MODELL-Zeile, und der Operator schaltet. O-Ton: „du
kommst immer automatisch mit demselben model aus dem planmod raus mit dem du reingekommen bist.
Und dann muss ich es wechseln. Da gibt es gar nichts zu diskutieren."

## 3. Der GATEWAY-Block (Pflichtformat an JEDEM Meilenstein-STOPP)

Kurz, scanbar, und die **letzte Zeile ist eine Ansage** — der Operator soll NICHT im Fließtext
suchen, welches Modell/welche Stufe er setzen soll. Format:

```
⏸️ GATEWAY M<N> — <2–4-Wort-Titel>
✅ FERTIG:   <1 Satz, was erreicht ist> — Beweis: <Commit/Diff/grep>
▶️ JETZT:    <1 Satz, was als Nächstes passiert>
🎚️ STUFE:    S<X>·<Intensität> — <Halbsatz warum>
🤖 WIE:      <SELBST / SKRIPT (1 Lauf) / SUBAGENT S<X>×N, disjunkt>
❓ OFFEN:    <Operator-Entscheidung(en) — oder „keine">
──────────────────────────────
👉 DU: <genau EINE Handlung — Modell/Stufe im Klartext, dann was>
```

Die `👉 DU:`-Zeile steht IMMER ganz unten und nennt die konkrete Handlung im Klartext — in der
gelebten Session das reale Modell (z.B. „Stell auf S5·High und sag GO"), im Skill-Template als
Platzhalter `S<X>`. Keine Modell-Info irgendwo mitten im Text vergraben.

**Live-Block vs. Template (W5-Zweiteilung, 2026-07-18/19):** Templates nennen nur Stufen (S1–S5,
portabel über Modell-Generationen — die „NIE Modellnamen"-Regel aus §2 gilt für TEMPLATES). Der
im Chat LIVE ausgegebene Gateway-Block nennt ZUSÄTZLICH den konkreten Modellnamen + wer schaltet
(z.B. „🎚️ MODELL: S3 · Sonnet — du wechselst per /model"), **DENN** der Operator rechnet das
Mapping Stufe→Modell nicht an jedem Gate selbst. Die fünf Pflichtfelder jedes LIVE-Blocks:
1. **FERTIG** mit Beweis-Artefakt (Commit/Diff/grep) — nie nur behauptet.
2. **JETZT** konkret im Chat — was als Nächstes passiert, kein Verweis „siehe Plan".
3. **MODELL** = Stufe + Klartext-Modellname + wer schaltet (Operator per /model / Frontmatter).
4. **WIE** inkl. Subagent-Modell + Token-Budget, falls delegiert wird.
5. **👉 DU** als letzte Zeile — genau EINE Handlung.
Fehlt die MODELL-Zeile im Live-Block, ist das Gate NICHT bestanden (Operator-Rüge 2026-07-19:
„Die Angabe der zu erwartenden Modeltyps fehlt im Gate nach ⏸️ STOPP … Es geht einfach gar nicht").

**Harte Regeln:**
1. Nach dem Block ist **STOPP**. Kein Weiterarbeiten ohne explizites „GO" — auch wenn die
   erwartete Stufe scheinbar schon aktiv ist (`SYSTEM_INSIGHTS.md` §2).
2. `✅ FERTIG` ohne Beweis-Artefakt = Gateway NICHT bestanden (Konservierungsgesetz 3).
3. Steht eine Operator-Entscheidung aus (`❓ OFFEN` ≠ „keine"), wird sie VOR dem betroffenen
   Meilenstein beantwortet oder der betroffene Teil explizit als blockiert markiert.
4. Kein Modellwechsel nötig (gleiche Stufe geht weiter)? Dann sagt `👉 DU:` genau das
   („Bleib auf S<X>, sag GO") — nie leer lassen.

## 4. Zuordnung Arbeit → Stufe (Default-Matrix)

| Arbeit | Stufe |
|:--|:--|
| P00 abarbeiten (Leseliste, viele Dateien lesen) | S1–S2 |
| P01 Bootstrap (Verständnis beweisen) | S4 |
| P02 Session-Init (Projekt begreifen, Meilensteine planen) | S4–S5 |
| Neu-/Umplanung, Architektur-Entscheidungen | S5 |
| Schema-Design, Gateway-Logik, kritische Formulierungen | S4 |
| Standard-Ausführung, Einbau vorformulierter Blöcke, Code | S3 |
| Mechanische Sweeps, Kopier-/Struktur-Arbeit | S1–S2 — oder SKRIPT (siehe §5) |
| Meilenstein-Bewertung, Evidence-Check an STOPPs | S4 |
| Forensic-/Abschluss-Reports | S4 |
| Session-Cleanup, git status, Buchhaltung | S2–S3 |
| Endabnahme, Deploy-Entscheid | S4–S5 |

Die Fahrplan-Ersteller (Schritt 5/6) tragen pro Meilenstein die Stufe aus dieser Matrix ein;
Abweichungen sind erlaubt, aber im Fahrplan zu begründen.

## 5. Delegations-Entscheid: SKRIPT vs. SUBAGENT vs. CHIRURG-SUBAGENT vs. SELBST

**Prüfreihenfolge (in dieser Reihenfolge, erste zutreffende gewinnt):**

1. **SKRIPT** — Ist die Aufgabe DETERMINISTISCH beschreibbar (exakte Ersetzungen, Kopien,
   Ordner-Anlagen, Umbenennungs-Listen)? → EIN Skript schreiben, prüfen, EINMAL ausführen,
   Output als Beweis anhängen. Ein Skript ist schneller, billiger und auditierbarer als jeder
   Agent — und hat keine Interpretations-Drift.
2. **SUBAGENT (S1–S2)** — Braucht die Aufgabe Sprachverständnis, aber KEIN Projekt-Reasoning
   (viele Dateien lesen/zusammenfassen, gleichartige kontextabhängige Edits)? → Subagent(en)
   mit **disjunkten Dateimengen**, kalt gestartet + voll gebrieft (4-Säulen-Briefing,
   `SYSTEM_INSIGHTS.md` §4; MODELL-Säule nennt die STUFE, keinen Namen), Endabnahme immer in
   der Hauptsession.
3. **CHIRURG-SUBAGENT (S5)** — Ist die Aufgabe ein kritischer Schnitt (Projekt-Reasoning,
   Formulierungs-Qualität, tiefe Diagnose, Architektur)? → An einen **S5-Chirurg-Subagenten**
   delegieren (frischer Kontext, voll gebrieft, Verify-Gate beim Orchestrator — §2b), **DENN**
   die teure Orchestrator-Hauptsession verbrennt sonst ihren Kontext mit Ausführung, die sich
   delegieren lässt.
4. **SELBST** — Nur was übrig bleibt: Orchestrierung (zerlegen, briefen, spawnen, prüfen,
   integrieren), Buchhaltung, Operator-Kommunikation — sowie winzige, exakt vorformulierte
   Änderungen ohne Reasoning-Bedarf (Executor-Arbeit S3, kein „Schnitt" — §2b-Ausnahme).

**Subagent-Grundregeln** (`SYSTEM_INSIGHTS.md` §4): Sub-Subagenten sind ERLAUBT (D-001,
2026-07-18 — das frühere Pauschalverbot ist aufgehoben), sofern die Briefing-Pflicht kaskadiert
(jeder Spawn mit 4-Säulen-Briefing) und Stufe/Modell je Spawn bewusst gewählt sind; kein
Scope-Ausbruch, Verify-Gate beim jeweiligen Orchestrator (wer spawnt, prüft), jede Aussage mit Beleg.

## 6. Verdrahtung (wo dieses Gateway erzwungen wird)

Dieses Protokoll ist **authoritative**, die Prompts sind advisory. Erzwungen wird es an sechs
Stellen:

1. **INSTRUCTIONS Schritt 5 (Fahrplan `task.md`):** Jeder Meilenstein im vorbefüllten Fahrplan
   trägt eine Stufen-Angabe (`— S<X>`) und endet mit einer GATEWAY-Zeile.
2. **INSTRUCTIONS Schritt 5/6 (Fahrplan + Startprompts, D-005 2026-07-11):** Der generierte PLAN
   (`<next-session>/desk/implementation_plan.md` bzw. `task.md`) MUSS pro Meilenstein einen
   GATEWAY-Block im Format §3 enthalten. Die generierte P02 enthält KEINEN Meilenstein-Plan —
   nur den Plan-Verweis (Teil 4); generierte P00/P01 enden mit
   „⏸️ STOPP — Stufe für den nächsten Schritt: S<X>". **DoD-Checks in 5 (Plan) + 6.2/6.3.**
3. **INSTRUCTIONS 7.0 (Prüfschleife):** „Enthält der generierte PLAN die GATEWAY-Blöcke (§3)?
   Enthält die P02 KEINEN Plan (D-005)? Stufen statt Modellnamen überall? Sonst FAIL →
   nachbessern, nicht durchwinken."
4. **`templates/P02_SESSION_INIT.md` TEIL 4 (D-005):** enthält KEINEN Meilenstein-Plan mehr, nur
   den Plan-Verweis auf `desk/implementation_plan.md`. Das §3-Format + die M0-Session-Start-
   Mechanik mit Anti-Farce-Gate (§2c: S1–S2/SKRIPT, nicht Planungs-Stufe) leben im Plan-Träger
   `templates/IMPLEMENTATION_PLAN.md` (MEILENSTEIN 0 + Punkt 6 unten).
5. **Anti-Farce-Gate (§2c):** INSTRUCTIONS DoD-Schritt-5 + 6.3 prüfen, dass der erste
   (mechanische) Meilenstein jedes generierten Plans S1–S2/SKRIPT trägt und ein
   Stufen-Senkungs-Gate nach Plan-Freigabe hat; Verstoß ⇒ FAIL.
6. **`templates/IMPLEMENTATION_PLAN.md` (G-06-Fix):** jeder Meilenstein-GATEWAY nutzt das §3-Format
   wörtlich (kein eigenes „5-Punkte-Gateway" mehr) — Status/Evidence → `✅ FERTIG`, Offene
   Punkte/Entscheidung/Risiko → `❓ OFFEN`, plus die 🎚️/🤖/👉-Zeilen. Ein zweites, nicht
   harmonisiertes Gateway-Format in diesem Template ist FAIL (war der Ausgangsbefund G-06 —
   „wieso muss ich suchen, welches Model ich einstellen soll?").

## 7. Verbindung zu anderen Referenzen

- Rollen + Subagent-Spawn-Protokoll + Living-Files-Pflege → `SYSTEM_INSIGHTS.md`
- Token-Budget-Ampel (NICHT Modell-Stufen!) → `TOKEN_WINDOW_GUARD.md`
- Konservierungsgesetze (Beweispflicht am Gateway = Gesetz 3) → `KONSERVIERUNGS_GESETZE.md`
