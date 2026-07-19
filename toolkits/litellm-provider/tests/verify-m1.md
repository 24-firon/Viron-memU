# Verifikation M1

## Voraussetzung

Patch M1 wurde angewendet (siehe `../APPLY.md`).

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

## M4 Live-E2E Verifikation

### Voraussetzung
M1+M2+M3+M2c+M2d Patches angewendet, Server gestartet.

### Test 1: LiteLLM-Modelle sichtbar
```bash
cd <TARGET>
curl -s -H "x-api-key: $ANTHROPIC_AUTH_TOKEN" http://127.0.0.1:18082/v1/models | Select-String "litellm/"
```
**Erwartet:** Zeilen mit `anthropic/litellm/` Prefix (22 Modelle)

### Test 2: Full Regression
```bash
uv run python -m pytest tests/ --tb=no -q
```
**Erwartet:** `1362 passed, 0 failed`
