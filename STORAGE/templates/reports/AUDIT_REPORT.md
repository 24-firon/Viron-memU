<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
<!-- TEMPLATE-EXPLANATION-START -->
> **Was in dieser Datei steht (G-26 — neuer Report-Typ, M2b-Redesign):**
>
> - Für Sessions, deren Kern eine PRÜFUNG war (Audit, Verifikation, Gesamtlogikcheck) — nicht eine
>   Fehlersuche (dafür `DEBUG_REPORT.md`) und nicht eine Umsetzung (dafür Forensic-Report).
> - Kernstück: eine BEFUNDLISTE mit Evidenz + Fix-Status. Diese Session (SKILL-V5-VERIFY_04) war
>   der ungeplante Erstfall — Vorbild: `desk/GESAMTLOGIKCHECK.md` dieser Session (26 Befunde,
>   5-Linsen-Methodik, Fix-Pakete-Tabelle).
> - **Ablage:** `DESK/reports/session-reports/[SESSION-TITEL].md` (wie Forensic — Zielpublikum
>   Mensch/Audit/Historie, F23/F27, NICHT auf P00-Leseliste außer begründeter Ausnahme).
<!-- TEMPLATE-EXPLANATION-END -->

---
session_title: [TASK]_[NN]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]
report_type: AUDIT
date: [YYYY-MM-DD]
next_session: [TASK]_[NN+1]_[GESAMTPROJEKT]_[REPO]_[YYYY-MM-DD]
ersteller: [Session-Kennung + Stufe]
---

# AUDIT/VERIFY — [Titel des geprüften Gegenstands]

**Prüfgegenstand:** [Was wurde geprüft — Skill, Codebase, Prozess, Regelwerk?]
**Methodik:** [Wie wurde geprüft — z.B. N-Linsen-Audit, Dogfooding-Simulation, Cross-Reference-Sweep]
**Abdeckung:** [Wie vollständig — X von Y Dateien/Komponenten, wo bewusst nicht geprüft]

---

## 1. Methodik

[Beschreibe die Prüf-Linsen/-Kriterien. Jede Linse als 1 Zeile: Name — Frage, die sie stellt.]

## 2. Befunde

Pro Befund: ID, Schweregrad (🔴 HOCH / 🟡 MITTEL / 🟢 NIEDRIG), Fundstelle (Datei+Zeile), Beschreibung,
Konsequenz, Fix-Richtung.

### [KATEGORIE-1]

#### [ID-01] 🔴/🟡/🟢 — [Kurztitel]
[Beschreibung, Fundstelle, Konsequenz, Fix-Richtung.]

## 3. Positivbefunde (was hält)

- [Was wurde geprüft und ist korrekt/konsistent — stichprobenverifiziert]

## 4. Fix-Status

| Befund | Status | Beleg |
|:---|:---:|:---|
| [ID-01] | ✅ gefixt / 🟡 dokumentiert / ⏳ offen | [Commit/Verweis] |

## 5. Offene Operator-Entscheidungen (Gate-Befunde)

- **[ID]:** [Frage] — [Optionen A/B/C]

## 6. Selbstprüfung (Pflicht, 3-5 Zeilen — `PROMPTS/AUDIT_REPORT_GENERATOR.md` §5)

- [Dünnste Abdeckung — steht sie ehrlich im Kopf?]
- [Befunde mit Fundstelle: X von Y]
- [Am ehesten anfechtbarer Schweregrad]

---

**[AUDIT/VERIFY ERSTELLT]**
