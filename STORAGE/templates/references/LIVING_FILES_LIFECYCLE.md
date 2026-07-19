<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- LIVING_FILES_LIFECYCLE — Schritt 2/3 Detail-Vollzug -->
> **Trigger:** Immer dann, wenn unklar ist, wann welche Living-File-Datei gepflegt wird oder wie die
> VOR/WÄHREND/NACH-Phasen zusammenhängen.
> **Struktur-Update:** Living Files liegen jetzt FLACH in `WORKSPACE/<session>/desk/` (nicht mehr in
> einem `DESK/build/`-Zwischenlager). Das Handover-Paket (P00/P01/P02, HANDOVER.md, `task.md` als
> vorbefüllter Fahrplan) liegt getrennt davon in `WORKSPACE/<session>/handover/`. Siehe die CLAUDE.md
> im Root des aktuellen Arbeits-Repos, Abschnitt 2 (bzw. `STRUKTUR_WISSENSBASIS.md` §1, falls keine
> Repo-CLAUDE.md existiert) für die volle Begründung. Zum Zwei-Ordner-Modell
> `<session>` (aktuell) vs. `<next-session>` (neu, vom Handover-Skill gebaut) siehe dieselbe CLAUDE.md
> Abschnitt 2.0 bzw. STRUKTUR_WISSENSBASIS.md §1.

# LIVING-FILES-LIFECYCLE (desk/ = LEER oder LIVE)

> **Ohne klares Lifecycle-Verständnis verbleiben Living Files entweder permanent verwaist liegen
> (Verschmutzung von `WORKSPACE/`) oder werden nie gepflegt (Continuity-Verlust).**

## Pflicht-Kern-Erinnerung (siehe die CLAUDE.md dieses Repos, Abschnitt 6.3, bzw. `STRUKTUR_WISSENSBASIS.md` §5)

`task.md`, `walkthrough.md`, `decision_log.md` sind IMMER Pflicht, in jeder Session. `lessons_learned.md`, `ideas_future_plans.md`, `implementation_plan.md` werden NUR angelegt, wenn die Session sie inhaltlich hergibt. Alle folgenden Lifecycle-Regeln gelten für den Pflicht-Kern uneingeschränkt und für die drei situativen Dateien NUR, sofern sie angelegt wurden.

## Die 3 Phasen

| Phase | Zeitraum | `desk/`-Status | Living-Files-Pflege |
|---|---|---|---|
| **VOR Session** | zwischen Sessions | Es existiert noch kein `desk/` für DIESE Session | keine |
| **WÄHREND Session** | aktiv | LIVE, in `WORKSPACE/<session>/desk/` | PFLICHT nach jedem Meilenstein (HD-3) |
| **NACH Session** | Handover-Phase | Finalisiert, Inhalte in `handover/`-Paket eingeflossen | Living Files bleiben in `desk/` liegen (kein Verschieben!) |

## Detail-Phase 1: VOR Session (kein eigener `desk/`-Ordner existiert noch)

```
WORKSPACE/<vorgänger-session>/
├── desk/            (← Vorgänger-Living-Files, bleiben hier liegen, read-only als Referenzquelle)
└── handover/
    ├── HANDOVER.md   (← Letzter Übergabestand)
    └── ...

WORKSPACE/<diese-session>/   (existiert noch NICHT)
```

**In dieser Phase:**
- Die Vorgänger-Session-Living-Files liegen weiterhin in deren eigenem `desk/`-Ordner — es gibt keinen zentralen „Desk", der zwischen Sessions geleert wird.
- Wer Vorgänger-Living-Files lesen will: direkt `WORKSPACE/<vorgänger-session>/desk/decision_log.md` lesen.

## Detail-Phase 2: WÄHREND Session (`desk/` = LIVE)

**Beim Session-Start (Schritt 1 + 2 in `INSTRUCTIONS.md`):**
- Neuer Ordner `WORKSPACE/<diese-session>/{desk,handover}/` wird angelegt.
- Pflicht-Kern-Templates aus `LIVING_FILES/` werden nach `desk/` kopiert (`cp`, kein Zwischenlager mehr nötig).
- Vorgänger-Living-Files werden bei Bedarf zusätzlich als `_predecessor_*`-Kopien in dieselbe `desk/` gelegt (siehe `STEP_1A_PREDECESSOR.md`) — Vorgänger-Ordner selbst bleibt UNVERÄNDERT, hier wird nicht gearbeitet.

**Während der Session (HD-3):**
- **Meilenstein = ein abgeschlossener Schritt** des 7-Schritte-Ablaufs bzw. ein inhaltlicher Zwischenstand innerhalb eines Schritts.
- Nach JEDEM abgeschlossenen Task: `desk/task.md`.
- Nach JEDEM Meilenstein: `desk/walkthrough.md`.
- Nach JEDER Architektur-/Strategie-Entscheidung: `desk/decision_log.md` (O-Ton-Pflicht bei Operator-Zitaten).
- Nach Fehler/Learnings (falls angelegt): `desk/lessons_learned.md`.
- Bei offenen, bewusst zurückgestellten Ideen (falls angelegt): `desk/ideas_future_plans.md`.
- Bei Status-Änderung pro Meilenstein (falls angelegt): `desk/implementation_plan.md`.

## Detail-Phase 3: NACH Session (Handover-Paket wird geschnürt, `desk/` bleibt liegen)

> **Hinweis zum Zwei-Ordner-Modell:** `<diese-session>` in diesem Abschnitt meint die AKTUELLE,
> abgebende Session — entspricht `<session>` in der CLAUDE.md dieses Repos, Abschnitt 2.0 (bzw.
> `STRUKTUR_WISSENSBASIS.md` §1). Das dort
> geschnürte Handover-Paket (P00/P01/P02, HANDOVER.md, vorbefülltes `task.md`) landet physisch im
> NEUEN `<next-session>`-Ordner, nicht im `handover/` der aktuellen Session — siehe dieselbe
> CLAUDE.md Abschnitt 2.0 und Abschnitt 7 (bzw. STRUKTUR_WISSENSBASIS.md §1 + `INSTRUCTIONS.md`
> Abschnitt 2 für die schrittweise Zuordnung, falls keine Repo-CLAUDE.md existiert).

**Beim Session-Ende (Schritt 7 = HANDOVER.md + Root-DESK-Rückspiegelung):**
- Die Living Files bleiben, wo sie sind — `WORKSPACE/<diese-session>/desk/`. Es gibt KEIN Verschieben mehr in einen separaten Handover-Ordner-Baum wie im Alt-Schema.
- `HANDOVER.md` und die restlichen Handover-Paket-Dateien in `WORKSPACE/<diese-session>/handover/` VERWEISEN auf den fertigen Stand in `desk/` bzw. fassen ihn zusammen — sie duplizieren die Living Files nicht 1:1.
- `WORKSPACE/<diese-session>/` als Ganzes (mit `desk/` + `handover/`) ist ab jetzt der Referenzpunkt für die nächste Session (siehe `STEP_1A_PREDECESSOR.md`).
- `WORKSPACE/<diese-session>/` bleibt **liegen** — es gibt **keinen** Auto-Archiv-Mechanismus (Q3 gestrichen, K1/D-001 2026-07-17, siehe `INSTRUCTIONS.md` 7.4). Archivieren ist ein bewusster Akt des Operators/eines geplanten Tasks, Ziel ist immer die EINE Archiv-Zone Root-`ARCHIVE/` (D-007) — nie `WORKSPACE/_archive/`.

## Verstöße gegen LIVING-FILES-LIFECYCLE

| Verstoß | Konsequenz |
|---|---|
| Living Files nicht aus Vorgänger übernommen (Phase 2) | Continuity-Verlust |
| Living Files nur am Session-Ende gepflegt (nicht nach jedem Meilenstein) | HD-3-Verstoß |
| Living Files mit `write` überschrieben (statt `edit`) | Konservierungsgesetz-1-Verstoß |
| Living Files verschoben statt kopiert (Vorgänger-Übernahme) | Vorgänger-Session verliert Daten |
| Pflicht-Kern-Datei fehlt oder bleibt leere Hülle | Konservierungsgesetz-2-Verstoß (Umkehrung: vorgetäuschte Vollständigkeit) |
| Situative Datei künstlich befüllt, obwohl inhaltlich nicht hergegeben | widerspricht der Pflicht-Kern-Regel (CLAUDE.md dieses Repos, 6.3, bzw. STRUKTUR_WISSENSBASIS.md §5) |
| Direkt im Vorgänger-`desk/` editiert statt in der eigenen `desk/` zu arbeiten | Archiv-Zerstörung der Vorgänger-Session |
