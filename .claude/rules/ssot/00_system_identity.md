---
name: System Identity & Environment
description: Definiert die Betriebs-Umgebung: Browser-Disziplin, Port-Konfiguration, Dev-Server-Hygiene und IDE-Koexistenz.
trigger: always_on
scope: alle
repo: all
---

# 00_system_identity.md

> **STATUS:** ALWAYS_ON
> **SCOPE:** Alle Domänen (Factory, Studio, Lab)
> **BLOCK:** 00 — System Identity & Routing

## 1. Browser-Disziplin

**SOG:** Nutze den Browser ausschließlich für Visual Audits und UI-Verifikation, DENN generische Recherche oder Server-Checks über den Browser verschwenden Agenten-Ressourcen und produzieren unstrukturierte Ergebnisse.

**Verboten:** Browser für Google-Recherche, Repo-Erstellung oder Server-Status-Checks.

## 2. Port & Dev-Server-Hygiene

**SOG:** Setze `PORT=3012` zwingend in der aktiven Shell (`$env:PORT='3012'; pnpm dev`), DENN Next.js 16.2.6 liest `PORT` nicht aus `.env.local` — ein falscher Port führt zu sofortigen Kollisionen mit anderen Agenten-Tools.

**Verboten:** Parallele Instanzen von `pnpm dev` oder `remotion studio`. Führe vor dem Start `taskkill /F /IM node.exe` aus.

**Verboten:** Standard-Ports (3000, 5000, 8080). Kollisionsvermeidung mit anderen Systemen.

## 3. IDE-Koexistenz (Multi-Agent-Schutz)

**SOG:** Berühre niemals Ordner ANDERER KI-Agenten (`.agent/`, `.agents/`, `.gemini/`, `.vscode/`, `.idea/`), DENN dies ist ein Multi-Agenten-Repository und das Löschen eines Fremdordners ist ein irreversibler Datenverlust-Vorfall.

**Verboten:** "Syncing" oder "Aufräumen" durch Löschen fremder Ordner. Alles, was mit einem Punkt (`.`) beginnt im Root, ist von automatischen Cleanup-Skripten ausgenommen.

## 4. Account-Authentizität

**SOG:** Nutze für alle Git-Operationen exakt den Account `24-viron` (MIT Bindestrich), DENN `24Viron` (ohne Bindestrich) ist ein separater Account und eine Verwechslung bricht die Rechtestruktur.

## 🔗 Light Router
- **WENN** du das Docs/Storage/Skills-Konzept verstehen musst ➔ **LIES** `00_docs_storage_definition.md`
- **WENN** du wissen musst, WANN und WIE Payloads geladen werden ➔ **LIES** `00_routing_protocol.md`
