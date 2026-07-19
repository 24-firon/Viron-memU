<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht:**
>
> - Der ausführliche, chronologische **Detail-Log** dieser Session: was das Problem war, roh und
>   vollständig — mit konkreten Beispielen, Text, Verweisen (Dateipfad, Befehl, Fehlermeldung),
>   Gesamtkontext konserviert. Kein gekürztes Fazit, sondern das volle Bild.
> - Pro Eintrag: Was passiert (mit Beispielen/O-Ton), Erkenntnis, warum wichtig, Anwendung in Zukunft.
> - **Ableitungs-PFLICHT (Sofort-Triage, D-015):** Jede Lesson wird NOCH IN DIESER SESSION triagiert:
>   Wird daraus eine Regel (global/lokal), eine Skill-Änderung, ein neuer Skill, ein Hook, ein Task —
>   oder bleibt es reines Wissen? Das `ABLEITUNG:`-Feld ist Pflichtteil jedes Eintrags; eine Lesson
>   ohne Ableitung ist UNVOLLSTÄNDIG (Gate in INSTRUCTIONS 7.0/7.3). Das volle Rohmaterial bleibt
>   trotzdem erhalten — wer kürzt, zerstört das Material, aus dem die Regel entsteht.
> - **Abgrenzung zu DOCS:** Die kondensierte, projektweite Essenz aus vielen `lessons_learned.md`-
>   Einträgen landet SEPARAT in `DOCS/hard_learned_facts` (+ `DOCS/LESSONS_LEARNED.md`, projektweit).
>   Das ist NICHT Teil dieses Skills — der Handover-Skill schreibt/pflegt `DOCS/` nicht (siehe
>   die CLAUDE.md im Root des aktuellen Arbeits-Repos, Abschnitt 6.2/6.3 zum Skill-Scope — bzw.
>   `STRUKTUR_WISSENSBASIS.md` §6, falls keine Repo-CLAUDE.md existiert). Diese Datei hier ist ausschließlich die
>   Session-lokale Rohfassung.
>
> - **Wann pflegen:** Bei Fehlern, „Aha-Momenten", neuen Erkenntnissen
> - **Bundle-Verwendung:** Diese Datei wird nach `WORKSPACE/<session>/desk/` kopiert. TEMPLATE zum Ausfüllen.
<!-- TEMPLATE-EXPLANATION-END -->

# lessons_learned.md — Ausführlicher Detail-Log dieser Session

> **Zweck:** Der vollständige, rohe Detail-Log — was funktioniert hat, was nicht, was überraschte.
> Nicht die kurze Essenz, sondern der komplette Beleg-Trail: Beispiele, Zitate, Dateipfade,
> Fehlermeldungen. Aus diesem Rohmaterial werden Regeländerungen/fehlender Kontext abgeleitet.
> **Wann pflegen:** Bei Fehlern, Erkenntnissen, „Aha-Momenten" (HD-3).

---

## Pflicht-Regeln (DoD pro Eintrag)

- **Be Specific:** Keine vagen Sätze. Nicht „Bug gefixt", sondern „NullReference in `auth.ts` durch
  Initialisierung des User-Objekts behoben".
- **Include Artifacts:** konkrete Dateipfade, Befehle, Fehlermeldungen, Log-Zeilen.
- **Preserve Gotchas:** nicht-offensichtliche Fallstricke festhalten (z.B. „OpenSSL braucht Flag X, sonst Crash").
- **O-Ton-Pflicht (Konservierungs-Gesetz 2):** Stammt die Erkenntnis aus einer Operator-Erklärung,
  MUSS ein wörtliches Operator-Zitat im „Was ist passiert?"-Feld stehen — nicht paraphrasieren.
  > Leitsatz (Operator, wörtlich): „Wir sind gerade am Anfang, wir müssen alles vermerken und erklären
  > und ablegen, was wir lernen und entscheiden. Sonst funktioniert das nicht."
  Im Zweifel zu ausführlich, nie zu knapp.
- **ABLEITUNGS-PFLICHT (D-015):** Jeder Eintrag endet mit dem `ABLEITUNG:`-Feld (Triage-Tabelle
  unten). Spätestens bei der Rückspiegelung (Schritt 7.3) ist jede Ableitung MANIFESTIERT —
  d.h. die Ziel-Aktion ist ausgeführt oder als Task angelegt, nicht nur benannt.
  > Operator, wörtlich: „das ist einer der wichtigsten Schritte, die wir überhaupt haben. dass auch
  > klargestellt wird, was da jetzt wirklich sozusagen abgeleitet werden soll. Ob das dann eine Regel
  > wird oder ob daraus ein Skill gebaut werden muss oder sowas. […] wir müssen uns da ja im Grunde
  > gleich die wichtige Arbeit vorwegnehmen."

---

## ABLEITUNGS-TRIAGE (Pflicht pro Lesson — kanalisiert die „unendlichen Möglichkeiten")

| Kategorie | Wann | Ziel-Artefakt (Manifestierung) |
|:--|:--|:--|
| **REGEL·global** | gilt für ALLE Repos/Sessions des Operators | globale CLAUDE.md / globale Rules (bzw. Regel-Export-Paket) — Umsetzung ggf. Operator-Gate |
| **REGEL·projekt** | gilt nur für dieses Repo | Projekt-CLAUDE.md / Injektionsquelle des Repos |
| **SKILL·fix** | ein bestehender Skill-Ablauf war lücken-/fehlerhaft | Eintrag in dessen Fix-Datei ODER direkter Skill-Edit (Werkbank-Regel) |
| **SKILL·neu** | wiederkehrender Ablauf ohne Zuhause | Task „Skill bauen" in der Gesamtplanung |
| **HOOK/AUTOMATION** | muss ERZWUNGEN werden, Erinnerung reicht nicht | Hook-/Automation-Task (z.B. SessionStart/Stop-Hook) |
| **TASK** | arbeitsauslösend, aber nicht regelwürdig | Knoten in `DESK/TASKS/00_Master_Tasklist.md` (mit ID) |
| **WISSEN** | reine Erkenntnis, keine Aktion nötig | bleibt hier; Kandidat für Konsolidierung (unten) |

**Format des Felds:** `ABLEITUNG: <Kategorie> → <Ziel/Task-ID> · Manifestiert: [JA <wo/Commit> / Task <ID> / OPERATOR-GATE <Frage>]`

---

## Format pro Fact

```
### [YYYY-MM-DD HH:MM] — [Kurzer Titel]

**Was ist passiert?** [Situation konkret. Bei Operator-Ursprung: wörtliches Zitat.]

**Was war die Erkenntnis?** [Was wurde gelernt — technisch präzise, mit Artefakt (Pfad/Befehl/Log).]

**Warum war das wichtig?** [Welche Konsequenz? Was wäre ohne diese Erkenntnis schiefgegangen?]

**Anwendung in Zukunft:** [Wie nutzen wir das? Welche Regel/welches Verhalten ab jetzt?]

**ABLEITUNG:** [Kategorie aus der Triage-Tabelle] → [Ziel] · Manifestiert: [JA <wo> / Task <ID> / OPERATOR-GATE <Frage>]
```

---

## Beispiel-Eintrag

```
### 2026-06-15 11:30 — Auth0 Token-Exchange verlangt HTTPS, sonst CORS-Fehler

**Was ist passiert?** Lokal ohne HTTPS getestet → Browser blockte den Token-Exchange (mixed-content).
Fehler im Callback: `net::ERR_CERT_...`, kein lauter Server-Error.

**Was war die Erkenntnis?** OAuth-Provider lehnen `http://localhost`-Redirects ab; CORS-Pre-Flight blockt.
Dev braucht ein `https://localhost`-Cert.

**Warum war das wichtig?** Der Token-Exchange schlug „heimlich" fehl — nur ein blockierter Redirect,
kein eindeutiger Fehler. Ohne diese Gotcha stundenlange Fehlersuche.

**Anwendung in Zukunft:** Lokales OAuth-Dev IMMER mit self-signed HTTPS-Cert oder ngrok/Cloudflare-Tunnel.

**ABLEITUNG:** REGEL·projekt → Projekt-CLAUDE.md Abschnitt „Lokales Dev-Setup" · Manifestiert: JA (CLAUDE.md editiert, Commit abc1234)
```

---

## [Erstes echtes Fact hier eintragen]

```
### [DATUM ZEIT] — [TITEL]

**Was ist passiert?** ...

**Was war die Erkenntnis?** ...

**Warum war das wichtig?** ...

**Anwendung in Zukunft:** ...
```

---

## Konsolidierungs-Brücke (lessons_learned → DOCS/hard_learned_facts + DOCS/LESSONS_LEARNED)

> **Verhältnis zur Sofort-Triage (D-015):** Die ABLEITUNG pro Lesson passiert IMMER sofort in der
> Session (siehe oben) — sie wird durch diesen Zyklus NICHT ersetzt. Der Konsolidierungs-Zyklus ist
> die ZWEITE Stufe: WISSEN-Einträge, die sich über mehrere Sessions wiederholen, werden nachträglich
> doch zu Regeln verdichtet.
>
> **Konsolidierungs-Zyklus:** alle 5-10 Sessions durchgehen und prüfen, welche Einträge sich verfestigt haben.
>
> **Beispiel-Pfad:**
> 1. `lessons_learned.md` enthält wiederholt „iron-session Cookie in Safari hat ITP-Limit bei 7 Tagen"
> 2. Die Erkenntnis wiederholt sich über mehrere Sessions
> 3. Wird zu einer projektweiten Regel verdichtet (z.B. `.opencode/rules/30_session_cookies.md` bzw.
>    kondensiert in `DOCS/hard_learned_facts` / `DOCS/LESSONS_LEARNED.md`)
> 4. In `lessons_learned.md` wird fortan auf die Regel verwiesen (nicht mehr dupliziert)
>
> **Abgrenzung:** `lessons_learned.md` (diese Datei, Living File dieses Skills) = session-lokal, roh,
> chronologisch, vollständig — der Beleg-Trail. `DOCS/hard_learned_facts` = projektweit, kurz,
> kondensierte Essenz, NICHT Teil dieses Skills (separate Pflege außerhalb des Handover-Skills).
> `decision_log` = Entscheidungen (Wahl), nicht Erkenntnisse (Erfahrung).
>
> **`DOCS/hard_learned_facts.md` existiert wieder** (wiederhergestellt 2026-07-19 nach
> unbeauftragter Entfernung beim V5-Reboot 2026-07-07) und wird aktiv gepflegt.
