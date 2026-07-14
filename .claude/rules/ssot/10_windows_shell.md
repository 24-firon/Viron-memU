---
name: Windows Shell Execution (Claude Code)
description: Shell-Disziplin unter Windows in Claude Code — Bash (Git Bash) vs. PowerShell getrennt halten, keine interaktiven/blockierenden Befehle, Fach-Tools vor Shell.
trigger: always_on
scope: alle
repo: all
harness: claude-code
---

# 10_windows_shell.md (Claude-Code-Fassung)

> **STATUS:** ALWAYS_ON
> **SCOPE:** Alle Domänen — Windows-Plattform, Harness **Claude Code**
> **BLOCK:** 10 — Safety & Zerstörungsschutz
>
> ⚠️ **Harness-Hinweis:** Die OpenCode-/Antigravity-Fassung dieser Regel
> (`STORAGE/rules/core/10_windows_shell.md`) verlangt `cmd /c` vor **jedem** Befehl, um den
> **Antigravity-Graphite-EOF-Bug** zu umgehen. Dieser Bug existiert in Claude Code **nicht**.
> Dort würde die Präfixierung nur Quoting zerstören und Befehle unnötig verschachteln.
> **In Claude Code gilt: KEIN `cmd /c`-Zwang.**

## 1. Zwei Shells, zwei Syntaxen — bewusst wählen

Claude Code stellt unter Windows **zwei getrennte Tools** bereit:

| Tool | Shell | Wofür |
|:--|:--|:--|
| **Bash** | Git Bash (POSIX `sh`) | POSIX-Skripte, `git`, Pipes, Heredocs |
| **PowerShell** | pwsh 7+ | Windows-Cmdlets, Registry, `$env:`, .NET-Objekte |

**SOG:** Wähle **ein** Tool pro Befehl und halte dessen Syntax konsequent durch, DENN
Bash-Syntax im PowerShell-Tool (und umgekehrt) ist ein Parser-Fehler, kein stiller Fallback.

- **Bash:** `/dev/null`, Forward-Slashes, `$VAR`, Heredocs.
- **PowerShell:** `$null`, `Test-Path`, `$env:VAR`, Here-Strings (`@'…'@`; schließendes `'@` auf Spalte 0).

## 2. Verbote — interaktiv und blockierend

**Verboten:** Alles, was auf eine Eingabe wartet und damit die Session aufhängt:
`git rebase -i`, `git add -i`, `Read-Host`, `Get-Credential`, `pause`, `powershell -NoExit`,
Editoren im Vordergrund.

**SOG:** Setze bei destruktiven Cmdlets `-Confirm:$false`, DENN sonst wartet der Prozess auf
eine Bestätigung, die nie kommt.

**SOG:** Starte lange Läufe (Dev-Server, Builds, Watcher) im **Hintergrund**
(`run_in_background`), niemals blockierend im Vordergrund.

## 3. Fach-Tools vor Shell

**SOG:** Nutze **Read / Edit / Write / Glob / Grep** statt `cat`/`sed`/`find`/`grep` in der
Shell, DENN die Fach-Tools sind schneller, liefern klickbare Pfade und umgehen Quoting-Fallen.
Shell nur dort, wo kein Fach-Tool passt (git, Paketmanager, Skript-Ausführung).
