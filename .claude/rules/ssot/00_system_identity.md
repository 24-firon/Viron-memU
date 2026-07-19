---
name: System Identity & Environment (universal)
description: Universelle Umgebungs-Grundregeln: Browser-Disziplin, IDE-Koexistenz (Multi-Agent-Schutz) und Account-Authentizität.
trigger: always_on
scope: alle
repo: all
---
<!-- Kanon v1.2, ausgerollt 2026-07-19 -->

# 00_system_identity.md

> **Tier-1-Rollout-Regel (universal)** — Quelle: `.claude/rules/ssot/00_system_identity.md`,
> kuratiert Session 17 (KANON-SYSTEMREPARATUR_17, 2026-07-19).
> **Kurations-Vermerk:** Die Quell-Datei war GEMISCHT — der VAS-spezifische Abschnitt
> „Port & Dev-Server-Hygiene" (Port 3012, Next.js 16.2.6, `pnpm dev`, `remotion studio`) wurde
> beim Kopieren entfernt (gilt nur im Viron-agency-stack). Ziel-Repos mit eigenen Dev-Servern
> definieren Port-Regeln als Repo-eigenes Overlay (Tier 3).

> **STATUS:** ALWAYS_ON
> **SCOPE:** Alle Domänen
> **BLOCK:** 00 — System Identity & Routing

## 1. Browser-Disziplin

**SOG:** Nutze den Browser ausschließlich für Visual Audits und UI-Verifikation, DENN generische Recherche oder Server-Checks über den Browser verschwenden Agenten-Ressourcen und produzieren unstrukturierte Ergebnisse.

**Verboten:** Browser für Google-Recherche, Repo-Erstellung oder Server-Status-Checks.

## 2. IDE-Koexistenz (Multi-Agent-Schutz)

**SOG:** Berühre niemals Ordner ANDERER KI-Agenten (`.agent/`, `.agents/`, `.gemini/`, `.vscode/`, `.idea/`), DENN dies ist ein Multi-Agenten-Repository und das Löschen eines Fremdordners ist ein irreversibler Datenverlust-Vorfall.

**Verboten:** "Syncing" oder "Aufräumen" durch Löschen fremder Ordner. Alles, was mit einem Punkt (`.`) beginnt im Root, ist von automatischen Cleanup-Skripten ausgenommen.

## 3. Account-Authentizität

**SOG:** Nutze für alle Git-Operationen exakt den Account `24-firon` (MIT Bindestrich), DENN das ist der reale, per `git config user.name` belegte Git-User der Operator-Repos. `24Firon` (ohne Bindestrich) ist ein separater Account und eine Verwechslung bricht die Rechtestruktur. (Die alte Angabe `24-viron` stammte aus dem Viron-Kontext und ist überall falsch.)

## 🔗 Light Router
- **WENN** du das Docs/Storage/Skills-Konzept verstehen musst ➔ **LIES** `00_docs_storage_definition.md`
- **WENN** du wissen musst, WANN und WIE Payloads geladen werden ➔ **LIES** `00_routing_protocol.md`
