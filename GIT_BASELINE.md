<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# GIT_BASELINE — Git ist Best Practice, kein Sonderfall

> **Version:** 1.0 · **Status:** LEBENDES DOKUMENT, versioniert wie die anderen Kanon-Dateien
> **Ownership:** MANAGED · **Tier:** 1 (gilt in JEDEM Repo, nicht verhandelbar)
>
> **Warum es das braucht (der Schmerz, belegt):** Git wird in jedem Repo anders und unzuverlässig
> genutzt. Das hat real Daten gekostet — nicht theoretisch.
>
> Operator, wörtlich (D-003, Session 12):
> > „git wird immer ncoh in jedem Repo unterschiedlich und unzuverlässig genutzt. Die git Skills
> > werden nicht genutzt. Die wichtigsten Regeln müssen jedem Agent bekannt werden und ein
> > sinnvolles system kanon werden."
>
> **Herkunft:** MASTER_BEFUND §6.3 · globale CLAUDE.md Regel 7 · Entscheid D-003 (Session 12).

---

## 1. Die Reversibilitäts-Doktrin (das Fundament — hier steht sie, alle anderen verweisen hierher)

**Ein Agent kann „Wichtigkeit" nicht beurteilen — „Reversibilität" schon, deterministisch:**

```bash
git ls-files --error-unmatch <pfad>    # Exit 0 = getrackt · Exit 1 = untracked
```

| Zustand | Bedeutung | Erlaubt |
|:--|:--|:--|
| **getrackt + committet** | Löschen/Verschieben ist rückholbar | Agent darf **autonom** entscheiden · `git mv` (Historie bleibt) |
| **untracked / gitignored** | Löschen ist **endgültig** | **nur verschieben, nie löschen** · Operator fragen |

**Das ersetzt die unbeantwortbare Frage „ist das wichtig?" durch eine maschinelle.** Es ist zugleich
die Voraussetzung für `RECOVERY_PROTOCOL.md`: Ohne Tracking keine Reversibilität, ohne
Reversibilität keine autonome Selbstkorrektur.

---

## 2. Tracken + Committen ist die Aufgabe, nicht die Ausnahme

**Nachdenken WAS committet wird: ja. Fragen OB committet werden darf: nein.**
Eine Regel „kein Commit ohne Erlaubnis" ist in einer Git-Session Unfug — Committen **ist** die
Arbeit. Ausnahmen (echte): Secrets, Riesen-Binaries, fremde Working Copies.

**Sofort tracken+committen gilt für alles Kanon-Relevante:** Prompts, Regeln, Templates, Reports,
Living Files, Bundles.

> **Der belegte Schmerz:** Die verlorenen Kanon-Prompts (`FORENSIC_REPORT_GENERATOR.md`,
> `CASUAL_CHAT_DISTILLATION_PROTOCOL.md` u.a.) hatten **null Git-Historie** — untracked +
> `git clean`-Altpermission war die Tatwaffe. Der Fix war nie „vorsichtiger sein", sondern
> **„vorher committen"**.

---

## 3. Checkpoint-Commit vor jeder Struktur-Änderung

Vor dem ersten inhaltlichen Eingriff einer Session/eines Rollouts: **Checkpoint-Commit** als
Rollback-Anker. Danach **strikt additiv** arbeiten, in logischen Blöcken committen.

**Effekt:** Jeder Schritt ist einzeln per `git revert` rücknehmbar. Das ist die abgesegnete
Rollout-Sicherung (Operator: „Deine Sicherheitsmaßnahme für Repo-Einrichtung hört sich super
sinnvoll an.").

---

## 4. Harte Verbote

| Verboten | Warum |
|:--|:--|
| **`git clean`** | Löscht Untracktes spurlos. War die Wurzel der Prompt-Verluste. Es gibt keinen legitimen Anwendungsfall in diesen Repos. |
| **`git reset --hard`** ohne Operator-GO | Vernichtet uncommittete Arbeit — auch fremde. |
| **`.gitignore` blind übernehmen** | Ein `archive/`-Eintrag aus einem Shielding-Workflow für FREMDE Repos traf auf Windows (case-insensitiv!) das eigene `ARCHIVE/` → **4.278 Archiv-Dateien lagen außerhalb von Git**. „Archivieren statt löschen" war damit **wirkungslos**: Archivieren nahm die Datei AUS Git heraus. (Gefunden + gefixt 2026-07-17.) |
| **Force-Push** auf geteilte Branches | Fremde Arbeit verschwindet. |
| **Hooks umgehen** (`--no-verify`) | Ohne expliziten Auftrag nie. |

**Prüfung, die jedes Archiv bestehen muss:**
```bash
find ARCHIVE -type f | wc -l          # physisch
git ls-files ARCHIVE | wc -l          # in Git
# Weichen die Zahlen ab -> das Archiv ist keins, sondern ein Haufen Dateien auf der Platte.
```

---

## 5. Commit-Handwerk

- **Conventional Commits:** `<type>(<scope>): <beschreibung>` — `feat`, `fix`, `chore`, `docs`,
  `refactor`, `test`. Keine Emojis. Kein `update`/`wip`/`change` als ganze Aussage.
- **Das WARUM in den Body**, nicht nur das WAS. Der Diff zeigt das WAS bereits.
- **Secret-Scan vor jedem Commit:**
  ```bash
  git diff --cached | grep -iE '(api_key|password|token|secret)\s*[:=]'
  ```
- **Account explizit pro Repo prüfen:** `git config user.name`.
  In CDS ist das **`24-firon`** (MIT Bindestrich, G-B/2026-07-17) — geerbte Regeln, die etwas
  anderes behaupten (z.B. `24-viron` aus dem Viron-Kontext), sind **falsch**:
  **die Git-Realität gewinnt gegen die geerbte Regel.**

---

## 6. Plattform-Fallen (Windows/Git Bash) — real aufgetreten, beide teuer

| Falle | Regel |
|:--|:--|
| **`NUL` statt `/dev/null`** | In Git Bash ist `NUL` **kein Gerät**, sondern erzeugt eine **echte Datei**. Git kann sie nicht indizieren → **der gesamte `git add` bricht mit Exit 128 ab** („unable to index file"). 25 solcher 0-Byte-Dateien blockierten die Versionierung eines ganzen Archivs. **Immer `/dev/null`.** |
| **Zwei Shells, zwei Syntaxen** | Bash-Tool = POSIX (`$VAR`, Heredoc `<<'EOF'`, `/dev/null`). PowerShell-Tool = pwsh (`$env:VAR`, Here-String `@'…'@`, `$null`). **PowerShell-Syntax im Bash-Tool ist ein stiller Fehler** — z.B. landet `@'` als Literal in der Commit-Message (real passiert, 2026-07-17). |
| **`cmd /c`-Präfix** | Ein **Antigravity**-Workaround (Graphite-EOF-Bug). In Claude Code existiert der Bug nicht — der Präfix zerstört dort nur das Quoting. **Nicht verwenden.** |

---

## 7. Verhältnis zu den anderen Kanon-Dateien

| Datei | Verhältnis |
|:--|:--|
| **`RECOVERY_PROTOCOL.md`** | **Baut direkt hierauf auf.** Ohne Tracking (§2) keine Reversibilität (§1), ohne Reversibilität keine autonome Korrektur. |
| `KANON_STRUKTUR_SPEC.md` §1.2 | Konservierungsgesetz 1 („archivieren statt löschen") ist **nur wirksam, wenn `ARCHIVE/` versioniert ist** (§4). |
| `SESSION_START_PROMPT.md` v2.5 | Prüft `git status` in M0; Checkpoint-Commit (§3) ist Teil der Start-Mechanik. |

---

## 8. Changelog

- **v1.0 (2026-07-17):** Initiale Fassung. Session `KANON-HAERTUNG_13_KANON-ROLLOUT_CDS_2026-07-17`.
  Quellen: MASTER_BEFUND §6.3, globale CLAUDE.md Regeln 7+9, Operator-O-Ton D-003 (Session 12).
  Belege aus realen Vorfällen: `.gitignore`-Archiv-Kollision (4.278 Dateien), NUL-Blockade
  (25 Dateien), Prompt-Verluste (untracked + `git clean`), PowerShell-Syntax im Bash-Tool.
