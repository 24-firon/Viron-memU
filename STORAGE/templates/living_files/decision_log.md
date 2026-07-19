<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht:**
>
> - Chronologische Sammlung wichtiger Entscheidungen, je mit Sequential-ID (D-001, D-002, ...)
> - Pro Eintrag: Kontext, Entscheidung, Begründung, Reversibilität, Konsequenzen
> - IDs sind PER-SESSION (D-001 in V2 ≠ D-001 in V3). Innerhalb-Session-Ref: `#D-003`.
>   Cross-Session-Ref: `→ WORKSPACE/<session>/desk/decision_log.md#D-003`
>
> - **Wann pflegen:** Bei jeder Architektur-/Strategie-Entscheidung (Konservierungs-Gesetz 4)
> - **Bundle-Verwendung:** Diese Datei wird nach `WORKSPACE/<session>/desk/` kopiert. TEMPLATE zum Ausfüllen.
<!-- TEMPLATE-EXPLANATION-END -->

# decision_log.md — Template für chronologische Entscheidungs-Sammlung

> **Zweck:** Chronologische Sammlung wichtiger Entscheidungen mit Begründung, referenzierbar per ID.
> **Wann pflegen:** Bei jeder Architektur-Entscheidung (HD-3 + Konservierungs-Gesetz 4: INTEGRATION).

---

## Pflicht-Regeln (DoD pro Eintrag)

- **Sequential-ID:** Jeder Eintrag beginnt mit `D-00N` (ID zuerst). Per-Session neu ab `D-001`.
  Referenz innerhalb: `#D-003`. Cross-Session: `→ WORKSPACE/<session>/desk/decision_log.md#D-003`.
- **Be Specific:** Keine vagen Sätze. Nicht „DB-Wahl getroffen", sondern „Postgres 16 statt SQLite, weil …".
- **Include Artifacts:** konkrete Dateipfade, Befehle, Variablennamen nennen, wo relevant.
- **O-Ton-Pflicht (Konservierungs-Gesetz 2):** Stammt die Entscheidung aus einer Operator-Erklärung,
  MUSS mindestens ein direktes Operator-Zitat WÖRTLICH im Kontext-Feld stehen — nicht paraphrasieren.
  > Leitsatz (Operator, wörtlich): „Wir sind gerade am Anfang, wir müssen alles vermerken und erklären
  > und ablegen, was wir lernen und entscheiden. Sonst funktioniert das nicht."
  Ein Eintrag ohne O-Ton (wo einer nötig wäre) gilt als unvollständig. Im Zweifel zu ausführlich, nie zu knapp.
- **Konsequenzen-Sweep-Pflicht (G-f/H-01, SKILL-AUDIT_07 — Wurzel-Fix gegen die K1-Kernkrankheit
  „nicht generalisierte Fixes"):** Ändert eine Entscheidung ein Vokabular, einen Pfad oder eine
  Norm-Formulierung (z.B. „Datei X verschoben", „Feld Y heißt jetzt Z", „Regel A gilt jetzt auch für
  Fall C"), MUSS die Konsequenzen-Zeile einen **grep-Sweep-Beleg** enthalten: `grep` über das
  ALT-Vokabular durch den GESAMTEN Skill-Ordner UND `Handover_Bundle/CLAUDE.md` (nicht nur die
  offensichtlichen Dateien) + die Treffer-Liste (gefixt / bewusst belassen mit Begründung). Ein
  Eintrag, dessen Konsequenzen-Feld nur „Datei X geändert" nennt, OHNE dass ein Sweep über
  Neben-Templates/SSoT belegt ist, gilt als unvollständig. **DENN** drei von vier Phase-1-Befunden
  des SKILL-AUDIT_07 (A-01, B-01, C-01) waren exakt dieses Muster: der Fix landete im
  Haupt-Dokument, aber Neben-Templates oder die SSoT-Wissensbasis wurden nie gegrept.

---

## Format pro Entscheidung

```
### D-00N — [YYYY-MM-DD HH:MM] — [Kurzer Titel]

**Kontext:** [Situation? Welche Optionen? Bei Operator-Ursprung: wörtliches Zitat.]

**Entscheidung:** [Was wurde konkret entschieden? Spezifisch, mit Artefakten (Pfad/Befehl).]

**Begründung:** [Warum diese Option? Welche Alternative wurde verworfen, warum?]

**Reversibel?** [Ja / Nein / Teilweise] — [Falls nicht: warum nicht?]

**Konsequenzen:** [Was ändert sich? Welche Dateien/Pfade betroffen?]
```

---

## Beispiel-Eintrag

```
### D-001 — 2026-06-15 10:15 — State in HttpOnly-Cookie (nicht Session-Storage)

**Kontext:** State-Token muss gegen CSRF gesichert werden. Optionen: Session-Storage, Local-Storage,
HttpOnly-Cookie. Operator, wörtlich: „Das Cookie darf niemals per JS lesbar sein, sonst ist die ganze
Auth wertlos."

**Entscheidung:** HttpOnly-Cookie mit SameSite=Lax, server-side via `iron-session` in `lib/auth/session.ts`.

**Begründung:** XSS-resistent (HttpOnly blockt JS-Zugriff). SameSite=Lax erlaubt OAuth-Redirect
(Top-Level-Navigation). SameSite=Strict verworfen, weil es den Callback-Redirect blockt.

**Reversibel?** Ja — Migration zu SameSite=Strict möglich, falls ein Security-Audit es verlangt.

**Konsequenzen:** Cookie-Helper in `lib/auth/session.ts`. Alle Auth-Cookies erben HttpOnly-Default.
```

---

## [Erste echte Entscheidung hier eintragen]

```
### D-001 — [DATUM ZEIT] — [TITEL]

**Kontext:** ...

**Entscheidung:** ...

**Begründung:** ...

**Reversibel?** ...

**Konsequenzen:** ...
```
