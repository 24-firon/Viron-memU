# SubAgent-Briefing — Bundle-Dokumentation für litellm-provider

> **Briefing für:** SubAgent mit 🟡 MITTEL-Model
> **Output-Verzeichnis:** `<TOOLKIT>/`
> **Schreibrechte:** nur in diesem Verzeichnis (nicht in `<TARGET>/`)
> **Stop-Bedingungen:** Nach 4 Dateien oder 15 Minuten Timeout

---

## A) MISSION

Erstelle 4 Dokumentations-Dateien für das `litellm-provider` Bundle. Diese beschreiben, was das Bundle tut, wie es angewendet wird, und wie man es verifiziert.

## B) CONTEXT

### Was ist das Bundle?
Ein Patch-Bundle, das den LiteLLM-Provider in das `<TARGET>` Repo integriert. Der LiteLLM-Proxy ist ein Single-Entry-Point für 22+ Modelle. Die Integration erfolgt über Patches (git diff outputs), die manuell auf `<TARGET>/` angewendet werden.

### Aktueller Stand
- M1 fertig: Patch `patches/M1-scaffolding.patch` existiert (21 Zeilen, 3 Dateien)
- M2-M4 noch offen

### Vorhandene Dateien im Bundle
```
toolkits/litellm-provider/
├── README.md                ← ZU ERSTELLEN
├── STATUS.md                ← ZU ERSTELLEN
├── APPLY.md                 ← ZU ERSTELLEN
├── docs/
│   └── PLAN-LITELLM-PROVIDER.md  ← existiert (von früherer Session)
├── patches/
│   └── M1-scaffolding.patch ← existiert
└── tests/
    └── verify-m1.md         ← ZU ERSTELLEN
```

### Patch-Inhalt (M1)
`patches/M1-scaffolding.patch` enthält:
- `config/provider_catalog.py`: +`LITELLM_DEFAULT_BASE = "http://127.0.0.1:4000"`, +ProviderDescriptor für "litellm"
- `providers/defaults.py`: +`LITELLM_DEFAULT_BASE` in Import + `__all__`
- `providers/registry.py`: +`_create_litellm` Factory (lazy import), +Entry in `PROVIDER_FACTORIES`

## C) SCOPE

### ✅ Erlaubt
- 4 Dateien erstellen in `<TOOLKIT>/`

### ❌ Verboten
- Schreibrechte in `<TARGET>/` (ist read-only für dieses Bundle)
- Ausführen von `git apply` oder anderen Commands
- Bestehende Dateien ändern (`patches/M1-scaffolding.patch`, `docs/PLAN-LITELLM-PROVIDER.md`)

## D) ATOMARE SCHRITTE

### Schritt 1: `README.md` erstellen (~50 Zeilen)
Struktur:
```markdown
# LiteLLM-Provider Bundle

> Patch-Bundle zur Integration des LiteLLM-Providers in `<TARGET>`.

## Zweck
[2-3 Sätze: Was macht der Patch, warum ist er nötig]

## Inhalt
- `patches/M1-scaffolding.patch` — ProviderDescriptor, Factory, Defaults
- `docs/PLAN-LITELLM-PROVIDER.md` — Vollständiger Plan mit M1-M4
- `STATUS.md` — Aktueller Stand der Implementierung
- `APPLY.md` — Anleitung zum Anwenden der Patches
- `tests/verify-m1.md` — Verifikations-Schritte für M1

## Voraussetzungen
- `<TARGET>` (geklont, auf origin/main)
- Python 3.14, uv installiert
- Working Tree sauber (keine anderen Modifikationen)

## Workflow
1. Patch anwenden: `git apply patches/M1-scaffolding.patch`
2. Verifizieren: siehe `tests/verify-m1.md`
3. Committen: `git commit -m "Bundle LiteLLM-Provider: M1 - ..."`
4. Analog für M2-M4

## Erstellungsdatum
2026-06-27
```

### Schritt 2: `STATUS.md` erstellen (~30 Zeilen)
Struktur:
```markdown
# Status: LiteLLM-Provider Bundle

## M1 — Scaffolding + ProviderCatalog
- **Status:** ✅ Fertig
- **Patch:** `patches/M1-scaffolding.patch`
- **Zeilen:** +21 (3 Dateien)
- **Verifiziert:** 2026-06-27 (Smoke-Test, 11/11 test_registry.py grün)
- **Inhalt:**
  - LITELLM_DEFAULT_BASE = "http://127.0.0.1:4000"
  - ProviderDescriptor für "litellm" (openai_chat, LITELLM_API_KEY)
  - LITELLM_DEFAULT_BASE in providers/defaults.py re-exportiert
  - _create_litellm Factory in providers/registry.py (lazy import)
  - 12 Provider total (vorher 11)

## M2 — Settings + SubAgent-Planung + Implementation
- **Status:** ⏳ Geplant
- **Geplant für:** nach M1-GO
- **Inhalt:**
  - SubAgent-Briefing M2.A
  - providers/litellm/{__init__.py, client.py, request.py}
  - Settings-Erweiterung (litellm_api_key, litellm_base_url, litellm_proxy)
  - Admin-UI-Felder (api/admin_config.py)
  - .env.example LiteLLM-Sektion

## M3 — Tests + Validation
- **Status:** ⏳ Geplant
- **Inhalt:** Mind. 5 neue Tests grün, alle bestehenden weiterhin grün

## M4 — Live-E2E
- **Status:** ⏳ Geplant
- **Inhalt:** End-to-End mit echtem LiteLLM-Proxy, Doku-Updates in `<CONFIG_REPO>/`

## Notizen
- Patch wurde auf origin/main getestet (12 Provider, ohne opencode_go)
- opencode_go existiert auf origin/main NICHT — anders als in früheren Sessions dokumentiert
```

### Schritt 3: `APPLY.md` erstellen (~30 Zeilen)
Struktur:
```markdown
# Wie wende ich die Patches an?

## M1 anwenden

### Voraussetzungen prüfen
```bash
cd <TARGET>
git status  # muss clean sein
git log --oneline -1  # muss origin/main sein (z.B. 439d821)
```

### Patch applizieren
```bash
git apply --check <TOOLKIT>/patches/M1-scaffolding.patch
# Wenn kein Fehler:
git apply <TOOLKIT>/patches/M1-scaffolding.patch
```

### Verifizieren
Siehe `tests/verify-m1.md`.

### Committen
```bash
git add config/provider_catalog.py providers/defaults.py providers/registry.py
git commit -m "Bundle LiteLLM-Provider: M1 - Scaffolding + ProviderCatalog"
```

## Rollback

Falls Probleme:
```bash
git reset --hard HEAD~1
```

Falls Commit weg ist (Hard-Reset) und Patch weg ist: Patch ist im Bundle gespeichert, einfach nochmal apply.
```

### Schritt 4: `tests/verify-m1.md` erstellen (~30 Zeilen)
Struktur:
```markdown
# Verifikation M1

## Voraussetzung
Patch M1 wurde angewendet (siehe `APPLY.md`).

## Smoke-Tests

### Test 1: ProviderDescriptor in Catalog
```bash
cd <TARGET>
uv run python -c "
from config.provider_catalog import PROVIDER_CATALOG
d = PROVIDER_CATALOG['litellm']
assert d.provider_id == 'litellm'
assert d.transport_type == 'openai_chat'
assert d.credential_env == 'LITELLM_API_KEY'
assert d.default_base_url == 'http://127.0.0.1:4000'
print('OK')
"
```
**Erwartet:** `OK`

### Test 2: Defaults re-export
```bash
uv run python -c "
from providers.defaults import LITELLM_DEFAULT_BASE
assert LITELLM_DEFAULT_BASE == 'http://127.0.0.1:4000'
print('OK')
"
```
**Erwartet:** `OK`

### Test 3: Factory in PROVIDER_FACTORIES
```bash
uv run python -c "
from providers.registry import PROVIDER_FACTORIES, _create_litellm
assert PROVIDER_FACTORIES['litellm'] is _create_litellm
print('OK')
"
```
**Erwartet:** `OK`

### Test 4: Sync der drei Sets
```bash
uv run python -c "
from config.provider_catalog import PROVIDER_CATALOG, SUPPORTED_PROVIDER_IDS
from providers.registry import PROVIDER_FACTORIES
assert set(PROVIDER_CATALOG) == set(PROVIDER_FACTORIES) == set(SUPPORTED_PROVIDER_IDS)
assert len(SUPPORTED_PROVIDER_IDS) == 12
print('OK:', len(SUPPORTED_PROVIDER_IDS), 'provider, all in sync')
"
```
**Erwartet:** `OK: 12 provider, all in sync`

### Test 5: Lazy-Import respektiert
```bash
uv run python -c "
import sys
from providers import registry
assert 'providers.litellm' not in sys.modules
print('OK: lazy import respected')
"
```
**Erwartet:** `OK: lazy import respected`

## Regression-Test

```bash
uv run python -m pytest tests/providers/test_registry.py -v
```

**Erwartet:** 11/11 PASSED
```

### Schritt 5: Stop
Nach 4 Dateien → STOP. Operator bewertet mit 🔴 STARK.

## E) ERFOLGS-KRITERIEN

- [ ] 4 Dateien existieren: `README.md`, `STATUS.md`, `APPLY.md`, `tests/verify-m1.md`
- [ ] Keine Datei außerhalb von `toolkits/litellm-provider/` geändert
- [ ] Markdown-Format konsistent mit existierender `docs/PLAN-LITELLM-PROVIDER.md`
- [ ] STATUS.md erwähnt explizit: "opencode_go existiert auf origin/main NICHT"

## F) MODEL-STÄRKE

🟡 MITTEL — Strukturiertes Schreiben mit klarer Vorlage. Keine Architektur-Entscheidungen. STARK wäre Overkill, SCHWACH zu riskant (könnte Markdown-Format verfehlen).

## Referenz
- Vor neuem Bundle-Bau IMMER `docs/PRE-FLIGHT-CHECK.md` lesen
