---
name: Verification Mandate — Definition of Done
description: Ein Task darf nur als erledigt markiert werden, wenn die physische Funktionalität auf dem Zielsystem verifiziert wurde. Verhindert "Halluzination der Fertigstellung".
trigger: always_on
scope: alle
repo: all
---

# 30_verification.md

> **STATUS:** ALWAYS_ON
> **SCOPE:** Alle Domänen (Factory, Studio, Lab)
> **BLOCK:** 30 — Kommunikation & Verhalten

## 1. Definition of Done

**SOG:** Markiere einen Task nur dann als "✅ Erledigt", wenn die physische Funktionalität auf dem Zielsystem verifiziert wurde, DENN ein Commit oder eine erfolgreiche Terminal-Ausgabe eines Deploy-Skripts reicht nicht aus.

**Pflicht vor dem Haken:**
1. **Health-Check:** Service-Endpoint (`/health`) oder Status (`systemctl is-active`) abfragen.
2. **Beweis sichern:** Ergebnis im Walkthrough oder als Kommentar in der `task.md` mit Zeitstempel dokumentieren.
3. **Operator-Bestätigung:** Bei User-interaktiven Diensten den Operator explizit fragen: "Bitte teste [Dienst] und gib ein Go."

## 2. Verbotene Zustände

**Verboten:** Markieren als "Erledigt" basierend auf "Annahme" oder "Sollte jetzt gehen".
**Verboten:** Ignorieren von `unhealthy` Docker-Status-Meldungen, nur weil die Logs gut aussehen.
**Verboten:** "Silent Passing": Tests, die grün zeigen, aber keine echte Logik prüfen.

**Konsequenz:** Bruch dieser Regel gilt als "Halluzination der Fertigstellung" und führt zum sofortigen STOPP.

## 3. No Silent Success

**SOG:** Validiere die tatsächliche Ausgabe (Output/Error Code) jedes Tools, DENN "Silent Failures" (das Übergehen oder Schönreden eines Fehlers) gelten als fundamentaler Regelverstoß.

**Pflicht:** Wenn eine Datei erstellt werden sollte, prüfe, ob sie danach existiert und den richtigen Inhalt hat (via `list_dir` oder Befehls-Output).

## 4. Such-Terminologie

**SOG:** Unterscheide strikt zwischen "Recherche" (Online/Web-Suche via `search_web`) und "Suche" (Offline/lokal via `grep_search`, `list_dir`), DENN das Durchsuchen des lokalen Repos bei der Aufforderung zur "Recherche" ist ein Kategorienfehler.

## 🔗 Light Router
- **WENN** du das Behavior-Kodex (11 Laws) brauchst ➔ **LIES** `30_behavior.md`
- **WENN** du den Planning-Mandate (Plan-Pflicht) brauchst ➔ **LIES** `40_planning.md`
