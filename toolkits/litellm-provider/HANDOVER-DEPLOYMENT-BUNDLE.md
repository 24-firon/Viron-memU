# HANDOVER: LiteLLM Deployment-Bundle-Plan für nächsten Agent

> **Zweck:** Dieser Prompt ist für einen frischen Chat in dem Repo, wo das `litellm-provider`-Bundle leben soll. Den kompletten Prompt kopieren, in den neuen Chat pasten, der Agent schreibt einen Plan, der Auftraggeber reviewt.

---

# PROMPT — für neuen Agent

Du bist ein Planungs-Agent. Deine einzige Aufgabe ist es, einen umsetzbaren Plan zu schreiben. Du führst **keine Edits** aus, **keine Commands** außer Lesen, **keine git-Operationen**. Am Ende steht ein Markdown-Plan, den der Auftraggeber (menschlich) reviewt.

## Kontext

Der Auftraggeber will ein **Deployment-Bundle** für LiteLLM: ein Ordner, den er Kunden gibt, die mit einem Befehl LiteLLM auf einer frischen Maschine starten.

Im Bundle-Ordner liegen aktuell noch 5 `git-diff` Patches, die gegen eine andere Architektur (`claude-code-proxy`) gebaut wurden. Diese Patches sind **nicht Teil des Zielprodukts** — sie wandern in ein `archive/`-Unterverzeichnis. Was die Kunden bekommen, ist ein Docker-basierendes Deployment-Bundle.

Du baust jetzt den Plan, der das Bundle vom aktuellen Zustand in den Zielzustand überführt.

## Was der Auftraggeber will (Produkt-Vision)

**Zielgruppe:** Endkunden, die LiteLLM als Single-Entry-Point für 22+ LLM-Modelle (OpenAI, Anthropic, Gemini, Mistral, Ollama, NVIDIA NIM, etc.) lokal betreiben wollen.

**Produkt:** Ein Ordner `toolkits/litellm-provider/` mit folgendem Inhalt:

```
toolkits/litellm-provider/
├── RECIPE.md                      ← Was ist das Bundle + wie nutzt der Kunde es
├── CONCEPT.md                     ← Was ist LiteLLM, warum ist es nützlich
├── docker-compose.yml             ← LiteLLM-Container + (optional) Admin-UI
├── config/
│   ├── litellm.yaml               ← Model-Liste, Routing-Regeln, Master-Key
│   └── secrets.example.yaml       ← API-Keys der Upstream-Provider (Template)
├── scripts/
│   ├── setup.sh                   ← Linux/Mac: 1-Befehl-Setup
│   ├── setup.ps1                  ← Windows: 1-Befehl-Setup
│   └── verify.sh                  ← Health-Check: "läuft LiteLLM?"
├── examples/
│   ├── memu/                      ← Wie memU das Bundle nutzt
│   ├── openai-python/             ← Wie openai-SDK das Bundle nutzt
│   ├── raw-curl/                  ← Wie cURL das Bundle nutzt
│   └── README.md                  ← Wie man die Beispiele nutzt
└── archive/                       ← Die alten 5 Patches (historisch, NICHT ausgeliefert)
    ├── README.md                  ← "Diese Patches waren für claude-code-proxy..."
    └── patches/                   ← Die 5 .patch Dateien unverändert
```

**Kunden-Erfahrung (so soll es laufen):**

```bash
# Auf einer frischen Maschine mit Docker installiert:
cd toolkits/litellm-provider
cp config/secrets.example.yaml config/secrets.yaml
# secrets.yaml editieren: echte OpenAI/Anthropic-Keys eintragen
docker compose up -d
./scripts/verify.sh

# Im eigenen Agent-Code (egal ob memU, openai-SDK, eigener Code):
#   base_url = "http://127.0.0.1:4000/v1"
#   api_key  = "sk-litellm-master-..."  (kommt aus config/litellm.yaml)
#   model    = "gpt-4" oder was in litellm.yaml konfiguriert ist
```

**Wichtig:** Der Kunde patcht **keinen Code in seinem Repo**. Er setzt nur die `base_url` seines OpenAI-Clients. Das ist's. **Das ist der Grund, warum die 5 git-diff Patches der falsche Ansatz waren.**

## Dein Auftrag

### Schritt 1 — Kontext aufbauen (LIES, nicht editieren!)

Lies die folgenden Dateien, um den aktuellen Stand zu verstehen:

1. `toolkits/litellm-provider/RECIPE.md` (aktueller Einstiegspunkt, beschreibt die alte Patches-Vision)
2. `toolkits/litellm-provider/README.md` (kurze Übersicht)
3. `toolkits/litellm-provider/STATUS.md` (M1-M4 Status der Patches)
4. `toolkits/litellm-provider/APPLY.md` (wie die Patches angewendet werden)
5. `toolkits/litellm-provider/docs/PRE-FLIGHT-CHECK.md` (LiteLLM-Erreichbarkeits-Check)
6. `toolkits/litellm-provider/docs/SUBAGENT-BRIEFING-M2A.md` (Provider-Implementation Briefing)
7. `toolkits/litellm-provider/docs/SUBAGENT-BRIEFING-M2C.md` (Settings-Fields Briefing)
8. `toolkits/litellm-provider/docs/SUBAGENT-BRIEFING-M2D.md` (Admin-UI + .env Briefing)
9. `toolkits/litellm-provider/docs/SUBAGENT-BRIEFING-M3A.md` (Tests Briefing)
10. `toolkits/litellm-provider/docs/SUBAGENT-BRIEFING-DOCS.md` (Doku-Erstellung)
11. `toolkits/litellm-provider/docs/BRIEFING-M4-LIVE-E2E.md` (Live-E2E Briefing)
12. `toolkits/litellm-provider/patches/M1-scaffolding.patch` (Beispiel-Patch)
13. `toolkits/litellm-provider/patches/M2-implementation.patch`
14. `toolkits/litellm-provider/patches/M2c-settings.patch`
15. `toolkits/litellm-provider/patches/M2d-admin-env.patch`
16. `toolkits/litellm-provider/patches/M3-tests.patch`
17. `toolkits/litellm-provider/tests/verify-m1.md`

### Schritt 2 — LiteLLM-Konfiguration verstehen (LIES, nicht editieren!)

Schaue dir die **laufende LiteLLM-Instanz** an, um die aktuelle Config zu verstehen. Das System läuft bereits produktiv:

- **Docker-Container:** ID `9623182fc0a3` (laut Aufzeichnungen), Image `ghcr.io/berriai/litellm:v1.85.0`
- **Port:** 4000
- **Master-Key:** `sk-litellm-factory-zT4nP7vR2mQ9xL5jW8bE3sH6fA1cD0gUyK` (aus dem `factory-litellm-router` Setup)
- **22 Modelle** sind live erreichbar
- **Bekannte Beispiel-Modelle aus der bisherigen Arbeit:** `gpt-4o-mini`, `claude-3-5-sonnet`, `minimax-m3`, `deepseek-*`, plus wahrscheinlich OpenRouter-, NVIDIA-NIM-, Ollama-Modelle

**Lese die `config.yaml` und `secrets.yaml` aus dem laufenden Container**, damit du weißt:
- Welche 22 Modelle aktuell konfiguriert sind
- Welche Upstream-Provider benutzt werden
- Welche API-Keys im secrets-File stehen (nur Variablen-Namen, nicht die Werte!)
- Welche Routing-Regeln existieren

**Wie du an die Config kommst (read-only!):**
```bash
# Inspiziere den laufenden Container (read-only)
docker ps -a | grep litellm
docker inspect <container-id> | grep -A 5 "Mounts"
docker exec <container-id> cat /app/config.yaml 2>/dev/null
# oder: docker cp <container-id>:/app/config.yaml /tmp/litellm-config.yaml
```

Falls der Container nicht (mehr) läuft oder die ID nicht mehr stimmt: suche im Repo unter Pfaden wie `docker/`, `infra/`, `deploy/` nach `litellm.yaml` oder `config.yaml`.

### Schritt 3 — Vergleich zu LiteLLM-Doku

Vergleiche die gefundene Config mit der LiteLLM-Doku (https://docs.litellm.ai/docs/proxy/configs). Stelle sicher, dass du die YAML-Struktur verstehst:
- `model_list:` — die Modelle
- `litellm_settings:` — globale Settings (Drop-Pricing, Logging)
- `general_settings:` — Master-Key, Admin-UI
- `router_settings:` — Routing-Strategien

### Schritt 4 — Plan schreiben (das ist dein **einziges Deliverable**)

Schreibe einen Markdown-Plan, der folgende Abschnitte enthält:

#### A) Was passiert mit den alten 5 Patches?

Entscheide: bleiben sie als `archive/`-Inhalt, oder werden sie gelöscht? Begründe.

#### B) Was sind die neuen Dateien (Inhalt + Zweck)?

Für jede neue Datei beschreibe:
- Pfad
- Zweck (1 Satz)
- Inhalts-Skizze (Struktur, nicht der ganze Inhalt)
- Geschätzte Größe in Zeilen

Dateien:
- `RECIPE.md` — soll die alte RECIPE ersetzen, aber jetzt mit Deployment-Vision
- `CONCEPT.md` — neu
- `docker-compose.yml` — neu
- `config/litellm.yaml` — neu
- `config/secrets.example.yaml` — neu
- `scripts/setup.sh` — neu
- `scripts/setup.ps1` — neu
- `scripts/verify.sh` — neu
- `examples/memu/` — Verzeichnis mit kurzem Code-Snippet
- `examples/openai-python/` — Verzeichnis
- `examples/raw-curl/` — Verzeichnis
- `examples/README.md` — neu

#### C) Was wird aus den alten Dateien?

Für jede Datei unter `toolkits/litellm-provider/`, entscheide:
- `RECIPE.md` → umschreiben
- `README.md` → umschreiben
- `STATUS.md` → entweder archivieren oder umschreiben (entscheide)
- `APPLY.md` → archivieren
- `docs/PRE-FLIGHT-CHECK.md` → umschreiben (jetzt für Setup-Phase, nicht für Patch-Phase)
- `docs/SUBAGENT-BRIEFING-*.md` (5 Stück) → archivieren
- `docs/BRIEFING-M4-LIVE-E2E.md` → archivieren
- `docs/SUBAGENT-BRIEFING-DOCS.md` → archivieren
- `patches/*.patch` (5 Stück) → archivieren in `archive/patches/`
- `tests/verify-m1.md` → archivieren

#### D) Welche Schritte muss der Build-Agent (nächste Session) ausführen?

In welcher Reihenfolge? Was passiert parallel? Welche Sub-Agents sind sinnvoll?

#### E) Was sind die Akzeptanzkriterien?

Wie testet der Kunde, dass das Bundle funktioniert? Liste 3-5 Smoke-Tests.

#### F) Welche Risiken gibt es?

- Was kann schiefgehen, wenn der Kunde Windows benutzt?
- Was, wenn der Kunde schon LiteLLM auf Port 4000 laufen hat?
- Was, wenn die secrets.yaml fehlerhaft ist?
- Was, wenn der Kunde kein Docker hat?

#### G) Was ist NICHT im Scope?

Explizit auflisten, was dieses Bundle NICHT macht:
- Kein Patchen von Kunden-Code
- Kein Hinzufügen von LiteLLM-Provider zu memU/claude-code-proxy
- Kein Web-UI für den Kunden
- etc.

#### H) Geschätzter Aufwand

In Stunden, mit Begründung pro Phase.

### Schritt 5 — Plan ausgeben

Schreibe den Plan als eine einzige Markdown-Antwort. Verwende klare Überschriften, Listen, Code-Blöcke für YAML-Skizzen. Der Plan sollte zwischen 800-1500 Zeilen lang sein — detailliert genug, dass der nächste Build-Agent ihn 1:1 ausführen kann.

**Wo du den Plan hinschreibst:** Als Chat-Antwort, nicht als Datei. Der Auftraggeber kopiert ihn manuell.

## Constraints (harte Regeln)

1. **Keine Edits.** Kein Write, kein Edit, kein hier-doc. Du gibst den Plan nur als Chat-Antwort aus.
2. **Keine git-Operationen.** Kein commit, kein apply, kein checkout.
3. **Keine Datei-Erstellung im Repo.** Du schreibst nichts in `toolkits/litellm-provider/`. Du analysierst nur.
4. **Keine Patches anwenden.** Auch nicht probeweise.
5. **Lese-Operationen sind erlaubt.** Du darfst alle Dateien lesen, Container inspizieren (read-only), `docker ps`/`docker inspect`/`docker exec cat`/`docker cp` benutzen.
6. **Sub-Agents sind erlaubt.** Du darfst `explore`-Sub-Agents spawnen, um parallel zu recherchieren.
7. **Sprache:** Deutsch (passt zur Auftraggeber-Sprache).
8. **Format:** Markdown, klar strukturiert, mit YAML-Code-Blöcken für Skizzen.

## Was du NICHT tun sollst

- **Nicht** die 5 Patches "universell machen". Das wurde versucht, hat 6 Stunden gekostet, ist gescheitert.
- **Nicht** TYPE_MAPPING.md schreiben. Das war ein Symptom des falschen Ansatzes.
- **Nicht** versuchen, die Patches in irgendein anderes Repo zu integrieren. Der Kunde will das nicht.
- **Nicht** den LiteLLM-Provider in memU/claude-code-proxy einbauen. Nicht im Scope.
- **Nicht** ohne Container-Inspektion planen. Du brauchst die echte Config.

## Bei Unklarheiten

Falls du eine Annahme treffen musst, dokumentiere sie explizit im Plan unter "Annahmen". Beispiel:
> **Annahme:** Der Kunde hat Docker installiert. Falls nicht, muss er Docker Desktop installieren.

## Definition of Done

Dein Auftrag ist erfüllt, wenn:
1. Du alle 17 Dateien in Schritt 1 gelesen hast.
2. Du die LiteLLM-Container-Config inspiziert hast (Schritt 2).
3. Du einen vollständigen Markdown-Plan mit allen Abschnitten A-H geschrieben hast.
4. Der Plan detailliert genug ist, dass der nächste Agent ihn ohne Rückfragen ausführen kann.
5. Du den Plan als Chat-Antwort (nicht als Datei) ausgegeben hast.

**Wichtiger Hinweis:** Der Auftraggeber hat heute schon viel Zeit investiert. Halte den Plan **fokussiert**. Lieber 1000 Zeilen, die alles abdecken, als 3000 Zeilen, die um den heißen Brei reden.

---

# ANFANG DEINER ARBEIT

Bestätige dem Auftraggeber kurz:
1. Dass du den Auftrag verstanden hast.
2. Dass du in Plan-Mode bist (keine Edits).
3. Welche Schritte du als Nächstes tust.

Dann arbeite los.

---

# Metadaten zu diesem Handover

**Erstellt:** 2026-06-28
**Erstellt von:** Session in `memU`-Repo (Auftraggeber: bachl)
**Kontext:** 6+ Stunden vergeblicher Versuch, 5 git-diff Patches in verschiedene Repos zu portieren. Erkenntnis: das Bundle sollte gar kein Patch-Bundle sein, sondern ein Deployment-Bundle.
**Status:** Ready für neuen Chat. Prompt oben kopieren, in neuen Chat pasten.
**Aufwand-Schätzung für Plan-Agent:** 30-60 min Lese-Phase + 60-90 min Plan-Schreibphase = 1.5-2.5 Stunden.
**Aufwand-Schätzung für Build-Agent (nächste Phase):** 2-3 Stunden.
