<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# HANDOVER — Datenübergabe (Kompakt)

> **Reine Datenübergabe** an den nächsten Session-Agent. Keine Fragen, keine Verifikation. **DENN** diese Datei ist der „Erste Hilfe"-Koffer für den Nachfolger.
> **Ablage:** `WORKSPACE/<next-session>/handover/HANDOVER.md` (D-02-Fix: kanonisch ist
> `<next-session>`, nicht `<session>` — HANDOVER.md ist Teil des Bundles für die FOLGE-Session,
> siehe Zwei-Ordner-Modell, INSTRUCTIONS Schritt 7.1)

---
session_title: [TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]
session_type: [z.B. WEBAPP_AUTH]
date: [YYYY-MM-DD]
next_session: [TASK]_[NN+1]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]
ersteller: [Session-Kennung + Stufe, z.B. "CDS-Session 02, Stufe S4" — oder Agent-/Session-Kennung]
status: [aktiv | übergeben | erledigt | obsolet]
kontext_quelle: [injektion voll (<Quelle: SessionStart-Hook+context-inject.json | opencode.jsonc>) | teilweise (CLAUDE.md, <N> Dateien) | nein] — Ergebnis des Injektions-Checks (INSTRUCTIONS 6.0, 3 Varianten A/B/C), bestimmt die P00-Variante der Folgesession
repo_root_abs: [absoluter Repo-Root, per `git rev-parse --show-toplevel` ermittelt, z.B. C:\Workspace\Repos\Context-Dispatcher-System]
---

> **⚓ Zum Feld `repo_root_abs` (PFLICHT, S-3):** Reine Datenangabe — für welches Repo dieses Bundle
> gilt. Der Skill und alle generischen Prompts bleiben pfad-frei; dieses Bundle gilt für genau EIN
> Repo und darf konkret sein.
>
> **Die Live-Prüfung macht der SessionStart-Hook**, nicht dieses Feld: Er meldet dem Nachfolger den
> tatsächlich ermittelten Repo-Root automatisch. Abgleich: Hook-Root == `repo_root_abs`?
> **JA** → weiterarbeiten, alle übrigen Pfade relativ dazu. **NEIN** → 🛑 **STOPP**, beide Pfade
> melden, nicht anlegen, nicht suchen.

## 1. BLUF (Bottom Line Up Front)

> [Ein dichter Satz: Was wurde in dieser Session erreicht?]
> Beispiel: "Phase A (Read-only Scan) abgeschlossen, 47 Top-Level-Verzeichnisse dokumentiert. Phase B (FOLDER.md anlegen) noch offen."

## 2. PROJEKT-SPEZIFISCHE DATEN

Was NIRGENDS anders im Repo steht und der nächste Agent explizit braucht:

| Schlüssel | Wert | Warum wichtig |
|:---|:---|:---|
| `[z.B. Branch]` | `[z.B. feat/cds-and-graph]` | `[Welcher HEAD aktiv]` |
| `[z.B. Server-IP]` | `[z.B. 195.201.36.240]` | `[SSH-Zugang, Hetzner]` |
| `[z.B. Port]` | `[z.B. 3012]` | `[Next.js Dev-Server]` |
| `[z.B. Env-Var]` | `[z.B. OPENCODE_GO_KEY]` | `[API-Key-Quelle]` |

## 3. ERLEDIGTE ARBEIT

| Was | Status | Wann |
|:---|:---:|:---|
| `[Aufgabe 1]` | ✅ | `[Datum]` |
| `[Aufgabe 2]` | ✅ | `[Datum]` |

## 4. ENTSCHEIDUNGEN

| Entscheidung | Warum | Reversibel? |
|:---|:---|:---:|
| `[z.B. Inkrementelles Graph-Update]` | `[Bestehende 1075 Nodes sind wertvoll]` | Ja |
| `[z.B. vis-network nicht patchen]` | `[Pro-Aufruf statt Library-global]` | Ja |

## 5. OFFENE TASKS

| Task | Priorität | Was zu tun |
|:---|:---:|:---|
| `[Task]` | P0 🔴 | `[Konkret was noch fehlt]` |
| `[Task]` | P1 🟡 | `[Konkret was noch fehlt]` |

## 6. BEKANNTE PROBLEME & WORKAROUNDS

| Problem | Workaround | Fix geplant? |
|:---|:---|:---:|
| `[z.B. Port 5432 öffentlich]` | `[ssh-tunnel statt direkter Connect]` | Ja |
| `[z.B. SESSION-RITUAL fehlt 5. Säule]` | `[Manuell bestätigen]` | Nein |

## 7. NÄCHSTE SCHRITTE (Konkret)

1. **[Schritt 1]** — [Konkrete Aktion, z.B. "FOLDER.md für apps/web anlegen"]
2. **[Schritt 2]** — [Konkrete Aktion]
3. **[Schritt 3]** — [Konkrete Aktion]

## 8. FEHLGESCHLAGENE PFADE (was NICHT funktioniert hat — spart dem Nachfolger die Wiederholung)

| Versuch | Warum gescheitert | Konsequenz für dich |
|:---|:---|:---|
| `[z.B. "pwd als Pfad-Basis (v2.3)"]` | `[z.B. "in Mono-Strukturen irreführend, Agent probte C:\ ab"]` | `[z.B. "Repo-Root ist die Basis, nicht cwd"]` |

*(Leer lassen, wenn nichts gescheitert ist — nicht künstlich befüllen. Ein ehrliches „nichts
gescheitert" ist ein gültiger Eintrag; eine erfundene Zeile ist Rauschen.)*

## 9. SUGGESTED SKILLS (welche Skills die Folgesession braucht)

| Skill | Wofür in DIESER Folgesession | Trigger |
|:---|:---|:---|
| `[z.B. session_handover_generator]` | `[z.B. "am Session-Ende, Bundle bauen"]` | `[z.B. "Sessionwechsel"]` |

## 10. RESTORATION PROCEDURE (wenn etwas schiefgeht)

- **Rollback-Anker:** `[Commit-Hash des Checkpoints, z.B. f0df4e6]`
- **Rückweg:** `[z.B. "git revert <hash>" oder "git checkout <hash> -- <pfad>"]`
- **Was NICHT rückholbar ist:** `[untrackte Dateien — vorher sichern; sonst "nichts"]`

## 11. REGEL-VORSCHLÄGE (F38b — optional, NUR falls diese Session eine Lessons-Ableitung „REGEL"
enthält, siehe `lessons_learned.md`-Triage-Tabelle; G-16/G-d-Fix, SKILL-AUDIT_07)

| Vorschlag | Regelwürdig weil | Wo verankern (Datei/Abschnitt) |
|:---|:---|:---|
| `[z.B. "Fork-Claim vor Board-Hochstufung prüfen"]` | `[welche Lesson/Entscheidung dahintersteht]` | `[z.B. .opencode/rules/… oder DOCS/00_SESSION_START_PFLICHTEN.md §X]` |

*(Sektion leer lassen — nicht künstlich befüllen —, wenn keine Lesson dieser Session eine
Ableitung REGEL trägt. Ein Recherche-Prompt-Artefakt aus F33(c) gehört NICHT hierher, sondern in
`templates/RESEARCH_PROMPT.md` bzw. dessen ausgefüllte Kopie — siehe Verweis dort.)*

---

> **Handover abgeschlossen.** Warte auf nächsten Operator-Auftrag.

**WICHTIG:** KEINE FRAGEN IN HANDOVER. Fragen gehören in `P01_BOOTSTRAP.md` Section „7 FRAGEN".
