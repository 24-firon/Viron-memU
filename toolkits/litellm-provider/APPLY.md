# Wie wende ich die Patches an?

## ⚠️ Vor dem ersten Patch: Pre-Flight-Check

**Lies `docs/PRE-FLIGHT-CHECK.md` vollständig.** Dieser Check prüft bevor du irgendeinen Code anwendest:

1. **Läuft der Ziel-Dienst?** → `docker ps | grep litellm`
2. **Haben wir gültige Credentials?** → `curl -H "Authorization: Bearer $KEY" http://127.0.0.1:4000/v1/models`
3. **Welches Transport-Format?** → LiteLLM = OpenAI Chat Completions
4. **Welche Modelle?** → 22 Modelle gelistet

Erst wenn dieser Check grün ist → Patches anwenden.

### Kurz-Check für LiteLLM
```bash
curl -s -H "Authorization: Bearer $LITELLM_API_KEY" http://127.0.0.1:4000/v1/models | Select-String "data"
```
**Erwartet:** Nicht-leeres JSON mit Modell-Liste (22 Modelle).

## Patches anwenden (Gesamtablauf)

Patches WERDEN in dieser Reihenfolge angewendet (M1 → M2 → M3 → M2c → M2d):

**M1 — Provider-Catalog + Factory + Defaults**
```bash
cd <TARGET>
git apply --check toolkits/litellm-provider/patches/M1-scaffolding.patch
```
Siehe `tests/verify-m1.md` für Verifikation.

**M2 — Provider Implementation (3 Dateien)**
```bash
git apply toolkits/litellm-provider/patches/M2-implementation.patch
```

**M3 — Tests (8 Tests)**
```bash
git apply toolkits/litellm-provider/patches/M3-tests.patch
# Verifikation:
cd <TARGET>
uv run python -m pytest tests/providers/test_litellm_provider.py -v
```

**M2c — Settings-Fields (config/settings.py)**
```bash
git apply toolkits/litellm-provider/patches/M2c-settings.patch
```

**M2d — Admin-UI + .env.example**
```bash
git apply toolkits/litellm-provider/patches/M2d-admin-env.patch
```

### Smoke-Test nach ALLEN Patches
```bash
cd <TARGET>
uv run python -c "
from providers.litellm import LiteLLMProvider, LITELLM_DEFAULT_BASE
assert LITELLM_DEFAULT_BASE == 'http://127.0.0.1:4000'
print('OK: 12 Provider, litellm registered')
"
```

## Committen (optional)

Wenn Patches erfolgreich angewendet wurden, optional einzeln committen:

```bash
cd <TARGET>
git add config/provider_catalog.py providers/defaults.py providers/registry.py
git commit -m "Bundle LiteLLM-Provider: M1 - Scaffolding + ProviderCatalog"
# Analog für M2, M3, M2c, M2d...
```

## Vollständiger Test-Run nach Commit

```bash
cd <TARGET>
uv run python -m pytest tests/ --tb=no -q
```

**Erwartet:** `1354+ passed, 0 failed` (8 neue LiteLLM-Tests)

## Rollback

Falls Probleme:

```bash
git reset --hard HEAD~1   # letzten Commit rückgängig
git checkout -- .         # Working Tree säubern
Remove-Item -LiteralPath "providers\litellm" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath "tests\providers\test_litellm_provider.py" -Force -ErrorAction SilentlyContinue
```

Falls Patch angewendet aber kein Commit: einfach `git checkout -- .` für tracked files + `Remove-Item` für neue untracked files.
