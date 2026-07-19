<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht:**
>
> - Session-Titel-Format: `[TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]` (= Chat-/Session-Name)
> - Ersteller NICHT im Titel → YAML-Feld `ersteller:` in HANDOVER + Report
> - Edge-Case: `-TO-` im TASK-Baustein bei Themenwechsel
> - Folgesession: NN hochzählen (pro Projekt-Strang), TASK aus offenen Aufgaben ableiten
> - Report-Dateinamen-Logik (kurz/lang + Such-Tool)
>
> - **Grundformat-SSoT:** `CLAUDE.md` Abschnitt 4 (bzw. `STRUKTUR_WISSENSBASIS.md` §3, falls keine
>   Repo-CLAUDE.md existiert). Diese Datei ergänzt nur die Detailregeln.
> - **Bundle-Verwendung:** systemisch, wird NICHT in die Arbeitskopie kopiert.
<!-- TEMPLATE-EXPLANATION-END -->

# SESSION_TITEL_SCHEMA — Vergabe-Logik für Session-Namen

> **Wann lesen:** BEIM Anlegen des Session-Ordners (Schritt 1) und beim Schreiben des Handover.
> Das Grundformat steht in `CLAUDE.md` Abschnitt 4 (bzw. `STRUKTUR_WISSENSBASIS.md` §3) — hier stehen die Detail- und Edge-Case-Regeln.

## 1. Standard-Format

```
[TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]
```

Der Session-Titel ist **identisch mit dem Chat-/Session-Namen** und mit dem Ordnernamen unter
`WORKSPACE/<session>/`.

**Bestandteile (in dieser Reihenfolge — TASK ganz vorne):**
- **TASK** — Name des Tasks, an dem DIESE Session arbeitet. Prägnant, mit `-` verbunden, aus den
  offenen Aufgaben (`task.md` / `DESK/TASKS/`) abgeleitet — NICHT nur ein generisches Schlagwort.
  Steht bewusst am Anfang: der Task-Name ist das primäre Auffind-Kriterium für Chats/Bundles.
- **NN** — zweistelliges, laufendes Präfix **pro Projekt-Strang** (`01`, `02`, `03` …): jede
  weitere Session am selben GESAMTPROJEKT zählt hoch — **auch wenn der TASK-Baustein wechselt**
  (Beispiel: `WORKSPACE-STRUKTUR_02_SKILL-REBOOT_…` → `ROLLOUT_03_SKILL-REBOOT_…`).
- **GESAMTPROJEKT** — Name des übergeordneten Projekts, unter dem der Task läuft (z.B. `SKILL-REBOOT`,
  `AUTH`, `WEBSHOP`). Das Projekt hat einen Namen, der Task hat einen Namen — beide sind getrennt.
- **REPO** — Repo-Kürzel (z.B. `CDS` für Context-Dispatcher-System). Kann mit GESAMTPROJEKT
  zusammenfallen, wenn Projekt und Repo deckungsgleich sind (dann z.B. `…_CDS_CDS_…`).
- **YYYY-MM-DD** — Datum der Session (Start), z.B. `2026-07-06`. Steht am Ende.

> **Task-Hierarchie (Baum, beliebig tief):** Tasks bilden einen Baum
> `GESAMTPROJEKT → Task → Untertask → …` — jeder Task kann Untertasks haben, auch über mehrere
> Schichten. **In den Titel kommt der SPEZIFISCHSTE Knoten**, an dem die Session tatsächlich
> arbeitet — nicht die Eltern-Kette. Die vollständige Hierarchie (mit IDs `T-NN`, `T-NN.N`,
> `T-NN.N.N` … in Punktnotation) lebt in der permanenten Gesamtplanung auf dem Root-DESK
> (`DESK/TASKS/`), die jede Session bei der Rückspiegelung pflegt. Beispiel: arbeitet eine
> Session am Unter-Untertask „Refresh-Rotation" von `AUTH → Token-Handling → Refresh-Rotation`,
> heißt sie `REFRESH-ROTATION_04_AUTH_WEBAPP_2026-07-08` — die Zuordnung zum Eltern-Task steht
> in der Gesamtplanung, nicht im Titel.

> **Ersteller gehört NICHT in den Namen.** Wer/welche Session/welches Modell den Titel erzeugt hat,
> wird als Metadatum in eine Datei geschrieben (YAML-Feld `ersteller:` in `HANDOVER.md` + Report),
> nicht in den Titel — siehe Abschnitt 4.

> **Wichtig — NN sortiert NICHT mehr das Dateisystem.** Weil TASK vorne steht, ist die alphabetische
> Ordner-Reihenfolge NICHT die chronologische. Die verbindliche Reihenfolge/Chronologie liefert
> `WORKSPACE/INDEX.md` (Status-Board, offizielles Living File), NICHT der Ordnername. Mechanismen,
> die früher auf das führende NN gebaut haben (Vorgänger-Findung, Q3-Auto-Archiv), nutzen jetzt
> `INDEX.md` bzw. die mtime — siehe `STEP_1A_PREDECESSOR.md` und `INSTRUCTIONS.md` 7.4.

## 2. Edge-Case: Thema hat sich drastisch geändert

**WENN** sich das Thema in der aktuellen Session komplett geändert hat, DANN wird der Wechsel im
**TASK**-Baustein mit `-TO-` abgebildet:

```
[VORHER]-TO-[NEU]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]
```

**Beispiele:**

| Session-Titel | Bedeutung |
|:---|:---|
| `BUNDLE-REPAIR-TO-STRUKTUR_04_SKILL-REBOOT_CDS_2026-07-06` | Startete als Bundle-Repair, wurde zu Struktur-Arbeit |
| `CALLBACK-TO-TOKEN-REFRESH_02_AUTH_WEBAPP_2026-07-06` | Startete als Callback, wechselte zu Token-Refresh |

**Faustregel:** `-TO-` nur verwenden, wenn das NEUE Thema mindestens 30 % der Session ausmachte.

## 3. Folgesession-Logik (Nummerierung + Task aus offenen Aufgaben)

**Wenn Vorgänger-Titel vorhanden:** NN hochzählen (pro Projekt-Strang), Datum neu, GESAMTPROJEKT + REPO
i.d.R. gleich (solange dasselbe Projekt läuft), **TASK aus den OFFENEN Aufgaben der Folgesession neu
bestimmen** (nicht den erledigten alten Task übernehmen) — der neue TASK darf dabei ein Untertask-Knoten
des Baums sein (siehe Hierarchie-Kasten in Abschnitt 1).

| Aktueller Titel | Folgesession-Titel |
|:---|:---|
| `WORKSPACE-STRUKTUR_02_SKILL-REBOOT_CDS_2026-07-06` | `ROLLOUT_03_SKILL-REBOOT_CDS_2026-07-07` |
| `CALLBACK_01_AUTH_WEBAPP_2026-07-01` | `TOKEN-REFRESH_02_AUTH_WEBAPP_2026-07-03` |

> Der TASK-Wechsel zwischen den Zeilen ist gewollt: der Name der Folgesession beschreibt, was SIE
> tun soll — abgeleitet aus `task.md`, nicht aus dem schon Erledigten. NN zählt weiter, solange
> dasselbe GESAMTPROJEKT fortgeführt wird — der TASK-Wechsel setzt NN NICHT zurück.

**Wenn KEIN Vorgänger-Titel vorhanden (F19 — Bootstrap-Regel):**
1. Lies `DESK/TASKS/00_Master_Task.md` + `DESK/TASKS/active/` → welches GESAMTPROJEKT + welcher TASK
   ist dran?
2. Extrahiere REPO-Kürzel aus der Repo-Identität.
3. Bestimme TASK aus dem obersten offenen Punkt der `task.md`.
4. **Existiert noch keine Session im aktiven Schema im Repo**, beginnt NN bei `01` (F19 — Bootstrap
   für Erst-Adoption). Sonst NN = höchstes vorhandenes NN des Projekt-Strangs + 1 (Chronologie/vorhandene
   Sessions aus `WORKSPACE/INDEX.md` lesen, NICHT aus der alphabetischen Ordner-Reihenfolge).

## 4. Speicherorte für Session-Titel + Ersteller-Feld

**Schreibe den Session-Titel an ALLEN dieser Stellen (Redundanz, Konservierungsgesetz 4):**
1. `WORKSPACE/<session>/`-Ordnername (= Titel)
2. `HANDOVER.md` — YAML-Header (`session_title:`)
3. Report-Dateiname — `[TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD].md` ODER Kurzname + Langtitel im YAML
4. Walkthrough-Eintrag — `## [YYYY-MM-DD] — [SESSION-TITEL]`
5. Commit-Message (falls Git) — Prefix

**Ersteller — PFLICHT als Metadatum, NICHT im Titel:**

Der Titel enthält KEINEN Ersteller. Wer/welche Session/welches Modell den Handover erzeugt hat,
kommt als YAML-Feld in `HANDOVER.md` UND den Report:

```yaml
ersteller: [z.B. "CDS-Session 02, Modell-Stufe S4" oder Agent-/Session-Kennung]
```

> **Warum getrennt:** Der Titel bleibt kurz und beschreibt Zweck/Task; die Herkunft ist Metadatum
> und gehört in ein Feld, nicht in den Namen. So sind Titel und Ersteller unabhängig recherchierbar.

> **Vollständige YAML-Feldlisten** (`session_title` und `ersteller` sind Teilmengen davon): Report =
> 7 Felder (`session_title, session_type, bundle_mode, date, next_session, ersteller, report_type`);
> HANDOVER = 6 Felder (`session_title, session_type, date, next_session, ersteller, status`). Diese
> Datei beschreibt nur die Titel-/Ersteller-Facette im Detail; die vollständige Feldliste ist hier
> als Referenz vermerkt.

## 5. Reports: Lange Namen vs. Kurze Dateinamen

**Dilemma:** Session-Titel sind lang und beschreibend. Report-Dateinamen sollten eher kurz sein.
**Lösung:** Reports tragen den **Langtitel im YAML-Header**, der **Dateiname kann kurz sein** — aber
NUR wenn ein Such-Werkzeug existiert. Ablage immer unter `DESK/reports/session-reports/` (klein).

### 5.1 Mit Such-Werkzeug (Ziel)
- **Pfad + Dateiname:** `DESK/reports/session-reports/[SESSION-TITEL].md` — der Dateiname IST der
  Session-Titel selbst, z.B. `DESK/reports/session-reports/STRUKTUR_04_SKILL-REBOOT_CDS_2026-07-06.md`.
  KEIN zusätzliches vorangestelltes `[YYYY-MM-DD]_`, weil der Session-Titel das Datum als
  `…_[YYYY-MM-DD]`-Baustein bereits enthält (Abschnitt 1).
- **YAML-Header:** `session_title: STRUKTUR_04_SKILL-REBOOT_CDS_2026-07-06` (+ `ersteller:`-Feld)
- **Suche:** Tool durchsucht YAML-Header + Inhalt; case-insensitive, ignoriert `_`, `-`, Leerzeichen.

### 5.2 Ohne Such-Werkzeug (Status quo)
- **Pfad + Dateiname:** `DESK/reports/session-reports/[TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD].md`
  (lang, aber eindeutig) — KEIN zusätzliches vorangestelltes `[YYYY-MM-DD]_`, das Datum steckt
  bereits im `…_[YYYY-MM-DD]`-Baustein des Titels selbst.
- **YAML-Header:** `session_title: [...]` + `ersteller: [...]`

### 5.3 Empfehlung
**Aktuell:** Lange Dateinamen verwenden (Such-Werkzeug fehlt noch). **Ziel:** Such-Werkzeug bauen —
Details in `ideas_future_plans.md`.

## 6. Beispiele (gültig vs. ungültig)

**Gültig:**
- `WORKSPACE-STRUKTUR_02_SKILL-REBOOT_CDS_2026-07-06` ✓
- `CALLBACK_00_AUTH_WEBAPP_2026-07-01` ✓
- `BUNDLE-REPAIR-TO-STRUKTUR_04_SKILL-REBOOT_CDS_2026-07-06` ✓ (Themenwechsel im TASK-Baustein)

**Ungültig (Ersteller im Namen — gehört ins `ersteller:`-Feld):**
- `STRUKTUR_02_SKILL-REBOOT_CDS-OPUS_2026-07-06` ✗

**Ungültig (generisch, kein echter Task):**
- `WORK_00_SKILL-REBOOT_CDS_2026-07-06` ✗
- `SESSION_1` ✗

**Ungültig (altes Schema, abgelöst — siehe Abschnitt 9 Historie):**
- `CDS_BUNDLE_REPAIR_V1` ✗ (V[N]-Logik, abgelöst)
- `02_2026-07-06_CDS_SKILL-REBOOT_STRUKTUR` ✗ (NN-/Datum-vorne-Schema, abgelöst — TASK gehört nach vorne)

**Faustregel:** ≤ 60 Zeichen; nur `-` als Sonderzeichen; TASK + NN + Gesamtprojekt + Repo + Datum; kein Ersteller.

## 7. Default nutzen

**Default wenn User nichts sagt:** Agent wählt den passendsten Titel nach dem Schema und dokumentiert
ihn. User sieht die Arbeit live und greift ein, wenn er etwas ändern will.

## 8. Verbindung zu Konservierungs-Gesetzen

- **Gesetz 3 (BEWEISPFLICHT):** Session-Titel IST der Beweis, welche Session was gemacht hat.
- **Gesetz 4 (INTEGRATION):** Titel muss in Ordnername, HANDOVER.md, Report UND Walkthrough identisch sein.

## 9. Historie der Titel-Schemata (abgelöst — nur zur Wiedererkennung alter Ordner)

> Diese Schemata sind **nicht mehr gültig**. Sie stehen hier, damit ältere Session-Ordner erkennbar
> bleiben — bestehende Ordner werden NICHT umbenannt (Konservierungsgesetz 1). Neue Sessions nutzen
> ausschließlich das Format aus Abschnitt 1.

| Generation | Format | Status |
|:---|:---|:---|
| **Aktuell** | `[TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]` | ✅ gültig (Abschnitt 1) |
| Vorgänger | `[NN]_[YYYY-MM-DD]_[REPO]_[HAUPTTASK]_[SUBTASK]` | ❌ abgelöst (NN/Datum vorne) |
| Alt | `[REPO]_[TASK]_V[N]` (z.B. `CDS_BUNDLE_REPAIR_V1`) | ❌ abgelöst (V[N]-Logik) |

**Mapping Vorgänger → Aktuell** (für die Zuordnung alter Ordner): der alte **SUBTASK** wird zum
neuen **TASK** (wandert nach vorne), der alte **HAUPTTASK** wird zum neuen **GESAMTPROJEKT**, **REPO**
bleibt, NN + Datum behalten ihren Wert und wandern an die neue Position. Beispiel:
`02_2026-07-06_CDS_SKILL-REBOOT_WORKSPACE-STRUKTUR` → `WORKSPACE-STRUKTUR_02_SKILL-REBOOT_CDS_2026-07-06`.
