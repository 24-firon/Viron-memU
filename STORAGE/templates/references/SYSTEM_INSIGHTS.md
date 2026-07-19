<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht:**
>
> - Rollen-Definition: Hauptsession vs. SubAgents, Operator vs. Orchestrator
> - Stufen-Rotation (S1–S5, Norm in `MILESTONE_GATEWAY.md`) mit HARD STOP bei Wechsel
> - Lebendige Dateien pflegen (Pflicht-Kern task/walkthrough/decision_log immer + 3 situative)
> - SubAgent-Spawn-Protokoll (4 Säulen, STOPP-Punkte)
> - User-Kommunikations-Protokoll
>
> - **Bundle-Verwendung:** Diese Datei wird NICHT in die Arbeitskopie kopiert — sie ist systemisch.
<!-- TEMPLATE-EXPLANATION-END -->

# SYSTEMVERSTAENDNIS — Wer macht was, Model-Rotation, lebendige Dateien

> **Wann lesen:** Beim SubAgent-Spawn, bei Modell-Wechsel, bei Pflege der lebendigen Dateien.

## 1. Wer macht was? (Rollen-Taxonomie — D-001, normativ)

> **Operator = der MENSCH** (auch „Director" genannt): gibt Aufträge und GO, wechselt Modelle/Stufen,
> trifft die Entscheidungen an den Gateways. Alle folgenden Rollen sind KI/Code:
> Orchestrator (Manager-KI) → Specialist/Analyst (Experten-KI) → Executor (ausführende KI) →
> Worker/Script (deterministischer Code). „Operator" bezeichnet im ganzen Skill NIE eine Agenten-Rolle.

### Hauptsession (Session-Architect — KI)
- Plant die Übergabe
- Schreibt Berichte
- Füllt Handover aus
- Pflegt lebendige Dateien
- Entscheidet Modus/Report-Typen
- **Hat Veto-Recht** über SubAgent-Outputs
- **Delegiert den kritischen Schnitt:** Fährt die Hauptsession ein teures Reasoning-/
  Orchestrator-Modell, ist sie der **Assistent des Chirurgen** — sie brieft und spawnt den
  S5-Chirurg-Subagenten, prüft und integriert dessen Ergebnis, statt den Schnitt selbst
  auszuführen (MILESTONE_GATEWAY §2b, Operator-Korrektur 2026-07-18)

### Executor (ausführende KI, leichte bis mittlere Stufe S1–S3)
- Führt die Schritte ATOMAR aus (jeder Befehl einzeln, kein `&&`)
- Zeigt immer letzte 3-5 Zeilen Output als Beweis
- Schreibt Reports nach `WORKSPACE/<session>/desk/subagent/`
- Erstellt KEINE Pläne, ändert NICHT den Plan
- Macht STOPP wenn der Plan STOPP sagt

### Orchestrator (Planer-KI, starke Stufe S4–S5)
- Analysiert die Lage (Pre-Flight Radar)
- Erstellt Pläne (Linear, Stopp für Stopp)
- Schreibt Executor-Prompts (klar, konkret, mit Leseliste)
- Führt KEINE Befehle aus, editiert KEINE Dateien direkt
- Löst Probleme wenn der Executor stuck ist

### SubAgents (gespawnt von Hauptsession)
- **General Agent:** Führt komplexe, mehrstufige Aufgaben aus (z.B. Bundle-Restrukturierung)
- **Explorer Agent:** Liest/analysiert große Datenmengen (z.B. 100 Dateien scannen)
- **Read-Only Agent:** Stellt Fakten zusammen, schreibt keine Dateien

**Wichtig:** IMMER STOPP für Stufen-/Modellwechsel VOR SubAgent-Spawn.

## 2. Stufen-Rotation (IMMER einplanen)

**🛑 HARTER STOPP bei JEDEM Stufen-/Modellwechsel.** Das System darf die Ausführung niemals
fortsetzen ohne „Go" vom Operator — selbst wenn die geforderte Stufe angeblich schon aktiv ist.
**Die Stufenskala S1–S5, die Intensitäts-Achse und die Chirurg-Doktrin sind normativ definiert in
`references/MILESTONE_GATEWAY.md` (§2, §2b) — diese Tabelle ordnet nur die Session-Phasen zu:**

| Phase | Stufe | Zweck |
|:---|:---|:---|
| **P00** (Leseliste) | S1–S2 | Nur lesen — viele Dateien iterieren (Kleinkontext ok) |
| **P01** (Bootstrap) | S4 | Comprehension — Fragen beantworten, Verständnis prüfen |
| **P02** (Session Init) | S4–S5 | Planung, Meilensteine definieren |
| **M-Ausführung** | S3 | Befehle ausführen, vorformulierte Blöcke einbauen |
| **Mechanische Sweeps** | S1–S2 oder SKRIPT | deterministische Massen-Operationen (MILESTONE_GATEWAY §5) |
| **Kritischer Schnitt** (Formulierung/Code/Architektur) | S5 | der Chirurg — bevorzugt als S5-SUBAGENT, nicht durch die Orchestrator-Hauptsession selbst (MILESTONE_GATEWAY §2b) |
| **STOPPs** (Gateway-Berichte) | S4 | Evidence bewerten, Gateway-Block |
| **Session-Abschluss** | S2–S3 | Cleanup, Buchhaltung, git status |
| **SubAgent-Tasks** | je nach Auftrag S1–S5 | alle Charakter-Stufen spawnbar — Stufe im Briefing |
| **Reviews** | S3–S4 | Code-Review, Skill-Scan |

**Regel:** Niemals alles auf derselben Stufe machen — Rotation ist Pflicht (planen → delegieren →
orchestrieren, §2b). **Low-Intensität ist immer gesperrt.**
**Harte Regel:** Nach JEDEM Stufenwechsel: STOPP, User-Bestätigung abwarten.

## 3. Lebendige Dateien (HD-7)

**Definition:** Dateien, die WÄHREND der Session aktiv gepflegt werden, nicht nur am Ende.

| Datei | Pflicht? | Wann aktualisieren |
|:---|:---|:---|
| `task.md` | Pflicht-Kern | nach jedem Task-Abschluss |
| `walkthrough.md` | Pflicht-Kern | nach jedem Meilenstein |
| `decision_log.md` | Pflicht-Kern | bei jeder Architektur-/Strategie-Entscheidung (O-Ton-Pflicht) |
| `lessons_learned.md` | situativ | bei Fehler/Learning/Gotcha — nur falls angelegt |
| `ideas_future_plans.md` | situativ | bei zurückgestellten Ideen — nur falls angelegt |
| `implementation_plan.md` | situativ | bei mehrstufigem Bauplan, Status pro Meilenstein — nur falls angelegt |

> Die Taskliste heißt einheitlich `task.md` — es gibt keine separate `CURRENT_TASKLIST.md` mehr. `task.md` liegt sowohl als laufendes Living File in der AKTUELLEN `<session>/desk/` als auch — vorbefüllt als Fahrplan für die Folgesession, Schritt 5 — in `<next-session>/desk/` (Zwei-Ordner-Modell, siehe die CLAUDE.md dieses Repos Abschnitt 2.0, bzw. `STRUKTUR_WISSENSBASIS.md` §1). Alle Living Files liegen flach in `desk/` — Pflicht-Kern-Regel siehe dieselbe CLAUDE.md Abschnitt 6.3 bzw. STRUKTUR_WISSENSBASIS.md §5.

**Pflege-Zeitpunkt:** NACH Meilenstein, NICHT erst am Session-Ende.
**Begründung:** Konservierungs-Gesetz 3 (BEWEISPFLICHT) — wer nicht dokumentiert, hat nicht gearbeitet.

## 4. SubAgent-Spawn-Protokoll

### Vor dem Spawn
1. **STOPP** für Modell-Wechsel (Operator-Permission)
2. **SubAgent-Typ wählen** (General / Explorer / Read-Only)
3. **TASK_ENVELOPE** mit 4 Säulen erstellen:
   - **A) MISSION** — Warum gibt es diese Aufgabe?
   - **B) CONTEXT** — Welche Dateien MUSS der SubAgent lesen?
   - **C) SCOPE** — Was darf er anfassen, was ist Tabu?
   - **D) ATOMARE SCHRITTE** — Exakte Tool-Calls

### Nach dem SubAgent-Report
1. **STOPP** — Bericht lesen
2. **Bewertung** (S4) — passt das Ergebnis?
3. **Integration** — SubAgent-Output in lebendige Dateien einarbeiten
4. **ERST DANN:** GO für nächsten Schritt

### Was SubAgents NICHT dürfen
- Dateien außerhalb des definierten SCOPE anfassen
- Haupt-Entscheidungen treffen (Modus-Wechsel, User-Kommunikation)
- Ohne STOPP-Punkt weitermachen

### Sub-Subagenten (ERLAUBT — D-001, 2026-07-18)
Das frühere pauschale Sub-Sub-Agent-Verbot ist AUFGEHOBEN. O-Ton Operator (D-001, Session 14):
„Alle generischen iterativen und tokenlastigen Prozesse müssen an Subagenten delegiert werden,
die wiederum weitere eigene Subagenten delegieren dürfen, wenn es die Aufgabe erfordert."
Bedingungen: Briefing-Pflicht kaskadiert (jeder Spawn mit 4-Säulen-Briefing), Verify-Gate bleibt
beim jeweiligen Orchestrator (wer spawnt, prüft), Stufe/Modell pro Spawn bewusst gewählt.

## 5. User-Kommunikations-Protokoll

**Wann User kontaktieren:**
- Vor Cross-Cutting-Entscheidungen (Modus, Report-Typen, Architektur)
- Nach jedem Meilenstein (Status-Bericht)
- Bei STOPP-Punkten (GO-Anfrage)
- Bei Token-Budget-Warnung (Schwarz-Status)
- Bei SubAgent-Output-Bewertung (auffällige Ergebnisse)

**Wann User NICHT kontaktieren:**
- Bei atomaren SubAgent-Tasks
- Bei reinen Lese-Operationen
- Bei Cache-/Performance-Optimierungen (kein Architektur-Impact)
- Bei Standard-Wartung (z.B. `.tmp`-Cleanup)

## 6. Verbindung zu INSTRUCTIONS.md

- **Modus-/Default-Entscheidung** → INSTRUCTIONS.md Abschnitt 1 (Defaults Q-A..Q-D)
- **Token-Fenster-Logik** → references/TOKEN_WINDOW_GUARD.md
- **Session-Titel-Logik** → SESSION_TITEL_SCHEMA.md
- **Konservierungs-Gesetze** → KONSERVIERUNGS_GESETZE.md
