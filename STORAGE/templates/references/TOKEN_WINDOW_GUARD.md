<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht:**
>
> - Token-Budget-Logik mit Realitäts-Aufschlag (50-100%)
> - Re-Asking-Protokoll
> - Notfall-Protokoll (Schwarz), Compaction-Fork-Option
>
> - **Bundle-Verwendung:** Diese Datei wird NICHT in die Arbeitskopie kopiert — sie ist systemisch.
<!-- TEMPLATE-EXPLANATION-END -->

# TOKEN_WINDOW_GUARD — Token-Budget-Logik

> **Wann lesen:** VOR jedem Ladevorgang in diesem Skill. Pflicht-Datei bei < 60% Restbudget.

## 0. Geltungsbereich (G-10-Fix, D-005.2 — HART, real verwechselt worden)

**Die Token-Frage in §3 gehört an den START DES SKILL-WORKFLOWS selbst** (Session-ENDE, direkt
nach der HD-1-Bestätigung, VOR der Report-Kaskade in Schritt 4) — **NICHT** an den Start einer
frischen Session. **DENN** eine gerade erst gestartete Session hat naturgemäß ein volles Fenster;
die Frage dort zu stellen ist reine Störung und ein Kategorienfehler (Regel-Genese-Verwechslung,
D-004). Wer diesen Skill triggert, weil er GERADE ans Session-Ende gekommen ist, bekommt die
Token-Frage als eine der ersten Aktionen dieses Workflows (siehe `INSTRUCTIONS.md` Abschnitt 0).
„HD-0" existiert NICHT in der HD-Tabelle (`SKILL.md`) — das Label war ein Altfehler und wird hier
nicht mehr verwendet; die Frage ist stattdessen eine feste Start-Interaktion dieses Skills, keine
harte Direktive im HD-Sinn.

## 1. Zweck

Verhindert Compaction während des Handover-Workflows. Compaction = System kompromittiert, weil:
- Berichte abgeschnitten
- Handover unvollständig
- Session-Titel geht verloren
- Cross-References brechen

## 2. Realitäts-Aufschlag (KRITISCH)

**Erfahrungswert aus User-Praxis:**
- LLM-Schätzungen für Token sind **50-100% ZU NIEDRIG**
- Beispiel: 50KB Datei → LLM sagt 10-15K Tokens → real sind 20-25K Tokens
- **Konsequenz:** Immer konservativ planen, +50% auf alle Schätzungen aufschlagen

**Anwendung in der Tabelle (Abschnitt 3):**
- 🟢 > 60% — Aufschlag +50%
- 🟡 30-60% — Aufschlag +75% (kann knapp werden)
- 🔴 < 30% — Aufschlag +100% (deutlich weniger möglich)
- ⚫ < 15% — Notfall

## 3. Restbudget-Schätzung

**Frage an User (PFLICHT, vor Workflow-Start des SKILLS — nicht vor Session-Start, siehe §0):**

> "Wie ist dein aktuelles Token-Fenster?"

**Antwort-Optionen:**

| Status | Bereich | Farbe | Erlaubte Aktionen | Realitäts-Aufschlag |
|:---|:---|:---|:---|:---|
| **Grün** | > 60% | 🟢 | alles (SKILL.md + INSTRUCTIONS.md voll + alle references/ + examples/) | +50% |
| **Gelb** | 30-60% | 🟡 | **`INSTRUCTIONS_REDUCED.md`** (Checklisten-Fassung derselben 7 Schritte, G-e-Fix — nicht die Voll-INSTRUCTIONS) + max. 2 references/, keine examples/ | +75% |
| **Rot** | < 30% | 🔴 | nur SKILL.md + TOKEN_WINDOW_GUARD.md, kein Detail-Workflow | +100% |
| **Schwarz** | < 15% | ⚫ | NOTFALL: `INSTRUCTIONS_NOTFALL.md` + `notfall/`-Bundle, Rest abbrechen | — |

## 4. Re-Asking-Protokoll

**WENN User nicht antwortet:**

| Schritt | Wann | Aktion |
|:---|:---|:---|
| 1. Frage stellen | t=0 | "Wie ist dein Token-Fenster?" |
| 2. Warten | t=0-60s | Passiv warten |
| 3. Nachfragen | t=60s | "Keine Antwort. Bitte Status angeben (🟢/🟡/🔴/⚫). Sonst nehme ich Gelb an." |
| 4. Warten | t=60-120s | Passiv warten |
| 5. Default | t=120s | **Default "Gelb"** annehmen, Workflow starten mit reduziertem Scope |
| 6. Bei "Schwarz"-Implikation | sofort | "Compaction-Risiko — bitte Session in neuem Chat fortsetzen." |

## 5. Notfall-Protokoll (Schwarz)

WENN Restbudget < 15%:

1. **Sofortiger Abbruch** des Detail-Workflows
2. **Speichere** aktuellen Zustand in HANDOVER.md (Notfall-Mini-Version, siehe `notfall/HANDOVER_MINIMAL.md` — 5 Sektionen)
3. **User-Warnung:** "Compaction-Risiko — bitte Session in neuem Chat fortsetzen. Notfall-Handover unter [Pfad]."
4. **KEINE** examples/ laden
5. **KEINE** SubAgents spawnen
6. **NUR:** notfall/-Bundle nutzen — `notfall/HANDOVER_MINIMAL.md` (5 Sektionen), `notfall/REPORT_MINIMAL.md` (4 Sektionen), `notfall/CHECKLIST_MINIMAL.md` (6 Punkte) + Bestätigungs-Formel
7. **Nutze** `notfall/` (eingebettetes Minimal-Bundle) als Backup-Quelle

## 6. Compaction-Fork-Option (User-Mitteilung)

**BEFORE Compaction-Crash:**
- Handover-Bundle erstellen lassen (Notfall-Modus)
- Nach Compaction: Bundle laden, neue Session starten
- **ABER:** Vorgänger-Session steht nicht mehr als Ansprechpartner zur Verfügung
- **Ausnahme:** Mit Fork arbeiten (parallele Session-Fortsetzung)
- **Empfehlung:** Nicht zu empfehlen ohne Fork — vorbeugende Handover-Bundle-Erstellung nur in Krisen-Szenarien

## 7. Präventiv-Maßnahmen

- **Vor großen Lade-Vorgängen:** Token-Check
- **Nach jedem Meilenstein:** Token-Check (kann sich schnell ändern)
- **Beim SubAgent-Spawn:** Token-Check VOR und NACH
- **Bei Modus-Wechsel:** Token-Check (Modi-Wechsel kann zusätzliche Token laden)

## 8. Was NICHT in den Token-Guard gehört

- Welche Dateien geladen werden → SKILL.md „Wo was steht" + INSTRUCTIONS.md
- Welcher Modus gewählt wird → INSTRUCTIONS.md Abschnitt 1 (Defaults) bzw. INSTRUCTIONS_REDUCED.md (🟡, G-e-Fix) / INSTRUCTIONS_NOTFALL.md (🔴/⚫)
- Session-Titel-Logik → SESSION_TITEL_SCHEMA.md

## 9. Verbindung zu Konservierungs-Gesetzen

- **Gesetz 1 (KEINE LÖSCHUNG):** Auch im Notfall keine Dateien löschen — nur in `ARCHIVE/` sichern
- **Gesetz 3 (BEWEISPFLICHT):** Notfall-Handover MUSS als Beweis existieren, sonst Session wertlos
- **Gesetz 4 (INTEGRATION):** Token-Guard-Entscheidungen in laufende Session integrieren, nicht stillschweigend überspringen
