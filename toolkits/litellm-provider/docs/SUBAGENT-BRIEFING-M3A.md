# SubAgent-Briefing M3.A — LiteLLM Provider Tests

> **Briefing für:** SubAgent mit 🟡 MITTEL-Model
> **Ziel:** 1 neue Test-Datei + 2 Appends in `<TARGET>/tests/`
> **Voraussetzung am Working Tree:** M1 + M2 Patches müssen applied sein (siehe `APPLY.md`)
> **Stop-Bedingungen:** Nach allen 3 Test-Files oder 20 Minuten Timeout

---

## A) MISSION

Erstelle Tests für den LiteLLM-Provider. Insgesamt 3 Files/Appends:

1. **NEU:** `tests/providers/test_litellm_provider.py` (5 Test-Funktionen, ~80 Zeilen)
2. **APPEND:** `tests/config/test_config.py` (2 Test-Funktionen)
3. **APPEND:** `tests/providers/test_registry.py` (1 Test-Funktion)

## B) CONTEXT

### Warum diese Tests?
Der LiteLLM-Provider wurde in M1 (Catalog + Factory + Defaults) und M2 (Provider-Klasse + Request-Builder) implementiert. M3 verifiziert:
- ProviderDescriptor-Felder sind korrekt
- LiteLLMProvider instanziiert ohne Fehler
- Build-Request-Body funktioniert mit AnthropicRequest-Mock
- Settings-Loading funktioniert
- Registry erkennt litellm als unterstützten Provider

### Aktueller Test-Stand
- 1354 Tests grün auf origin/main (kein M1+M2 applied)
- 1354 Tests grün MIT M1+M2 applied (keine Regression, 0 Failures)
- 12 Provider inkl. litellm

### Vorhandene Test-Pattern (Vorlagen)

**`tests/providers/test_registry.py`** zeigt wie Provider getestet werden:
```python
def test_create_provider_instantiates_each_builtin():
    settings = _make_settings()
    cases = {
        "nvidia_nim": NvidiaNimProvider,
        ...
    }
    with patch("providers.openai_compat.AsyncOpenAI"), patch("httpx.AsyncClient"):
        for provider_id, provider_cls in cases.items():
            assert isinstance(create_provider(provider_id, settings), provider_cls)
```

**`tests/config/test_config.py`** zeigt wie Settings-Env-Vars getestet werden:
```python
def test_wafer_api_key_from_env(self, monkeypatch):
    monkeypatch.setenv("WAFER_API_KEY", "wafer-key")
    settings = Settings()
    assert settings.wafer_api_key == "wafer-key"
```

**`tests/config/test_config.py:130`** zeigt wie absolute Pfade getestet werden:
```python
assert settings.claude_cli_bin == (
    "C:\\Users\\bachl\\AppData\\Roaming\\npm\\node_modules\\"
    "@anthropic-ai\\claude-code\\bin\\claude.exe"
)
```

## C) SCOPE

### ✅ Erlaubt
- 1 neue Datei erstellen in `tests/providers/`
- 2 Edits in bestehenden Test-Files (append, nicht überschreiben)
- Tests mit Mocks (kein Live-LiteLLM-Proxy nötig)

### ❌ Verboten
- Production-Code ändern (Settings, Registry, etc.)
- `.env.example` ändern
- Tests in `tests/providers/test_converter.py` oder `tests/providers/test_nvidia_nim.py` oder `tests/providers/test_fireworks.py` anfassen — die haben pre-existing failures, das ist ein separater Fix
- Tests im `tests/cli/test_entrypoints.py` anfassen — auch pre-existing

## D) ATOMARE SCHRITTE

### Schritt 1: Vorlage lesen
Lies 3 Files VOLLSTÄNDIG:
1. `tests/providers/test_registry.py` (siehe `_make_settings()` Helper, `cases`-Dict, `patch`-Pattern)
2. `tests/config/test_config.py` (siehe `monkeypatch.setenv` Pattern, `Settings()`-Aufruf)
3. `providers/litellm/{__init__.py, client.py, request.py}` (die zu testenden Module)

### Schritt 2: `tests/providers/test_litellm_provider.py` NEU erstellen (5 Tests, ~80 Zeilen)

Struktur:
```python
"""Tests for LiteLLM provider (Bundle LiteLLM-Provider M3)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestLiteLLMDescriptor:
    """Test the litellm ProviderDescriptor in the catalog."""

    def test_descriptor_in_catalog(self):
        """litellm is registered in PROVIDER_CATALOG."""
        from config.provider_catalog import PROVIDER_CATALOG
        assert "litellm" in PROVIDER_CATALOG

    def test_descriptor_fields(self):
        """ProviderDescriptor has the expected field values."""
        from config.provider_catalog import PROVIDER_CATALOG
        d = PROVIDER_CATALOG["litellm"]
        assert d.provider_id == "litellm"
        assert d.transport_type == "openai_chat"
        assert d.credential_env == "LITELLM_API_KEY"
        assert d.credential_attr == "litellm_api_key"
        assert d.base_url_attr == "litellm_base_url"
        assert d.proxy_attr == "litellm_proxy"
        assert d.default_base_url == "http://127.0.0.1:4000"
        assert "chat" in d.capabilities
        assert "streaming" in d.capabilities
        assert "tools" in d.capabilities

    def test_default_base_url_in_defaults(self):
        """LITELLM_DEFAULT_BASE is re-exported from providers.defaults."""
        from providers.defaults import LITELLM_DEFAULT_BASE
        assert LITELLM_DEFAULT_BASE == "http://127.0.0.1:4000"


class TestLiteLLMProviderInstantiation:
    """Test that LiteLLMProvider can be created and behaves correctly."""

    def test_provider_instantiation(self):
        """LiteLLMProvider can be instantiated with a ProviderConfig."""
        from providers.litellm import LiteLLMProvider
        from providers.base import ProviderConfig
        config = ProviderConfig(
            api_key="sk-test",
            base_url="http://127.0.0.1:4000",
        )
        with patch("providers.openai_compat.AsyncOpenAI"):
            provider = LiteLLMProvider(config)
        assert provider._provider_name == "LITELLM"
        assert provider._base_url == "http://127.0.0.1:4000"

    def test_provider_uses_default_base_url(self):
        """When config.base_url is None, the default URL is used."""
        from providers.litellm import LiteLLMProvider
        from providers.base import ProviderConfig
        config = ProviderConfig(
            api_key="sk-test",
            base_url=None,
        )
        with patch("providers.openai_compat.AsyncOpenAI"):
            provider = LiteLLMProvider(config)
        assert provider._base_url == "http://127.0.0.1:4000"
```

### Schritt 3: APPEND zu `tests/config/test_config.py` (2 Tests)

Füge DIESE 2 Tests an das Ende der `TestSettings`-Klasse hinzu (suche nach `class TestSettingsOptionalStr` als Anker, füge davor ein):

```python
    def test_litellm_api_key_from_env(self, monkeypatch):
        """LITELLM_API_KEY env var is loaded into settings."""
        from config.settings import Settings
        monkeypatch.setenv("LITELLM_API_KEY", "sk-litellm-test")
        settings = Settings()
        assert settings.litellm_api_key == "sk-litellm-test"

    def test_litellm_base_url_from_env(self, monkeypatch):
        """LITELLM_BASE_URL env var overrides the default."""
        from config.settings import Settings
        monkeypatch.setenv("LITELLM_BASE_URL", "http://custom:5000")
        settings = Settings()
        assert settings.litellm_base_url == "http://custom:5000"
```

**WICHTIG:** Diese Tests erfordern, dass `litellm_api_key` und `litellm_base_url` als Settings-Fields existieren. **Sie existieren aktuell NICHT in `config/settings.py`** — das ist eine bewusste Auslassung in M1/M2. 

**Option:** Wenn diese Settings-Fields fehlen, schreibe die Tests als commented-out Sketches in `tests/providers/test_litellm_provider.py` und dokumentiere in `STATUS.md`:
```
"M3.A Tests: 5/7 implementiert. 2 Settings-Tests als commented-out Sketches
in test_litellm_provider.py abgelegt, weil LITELLM_API_KEY und LITELLM_BASE_URL
Settings-Fields in M1/M2 nicht hinzugefügt wurden (sind Teil von M2.C laut
PLAN-LITELLM-PROVIDER.md). Nach M2.C werden die 2 Tests aktiviert."
```

### Schritt 4: APPEND zu `tests/providers/test_registry.py` (1 Test)

Füge DIESEN Test am Ende der Datei hinzu:

```python


def test_create_provider_instantiates_litellm() -> None:
    """litellm is added to the create_provider cases."""
    from providers.litellm import LiteLLMProvider
    settings = _make_settings()
    with patch("providers.openai_compat.AsyncOpenAI"):
        provider = create_provider("litellm", settings)
    assert isinstance(provider, LiteLLMProvider)
```

**WICHTIG:** Beachte dass `_make_settings` KEIN `litellm_api_key` setzt. Falls der Provider-Code `api_key` als required field hat, muss der Test das ggf. monkey-patchen oder die Settings anpassen. Test-Pattern siehe `test_create_provider_instantiates_each_builtin` Zeile 119-137 in der Vorlage.

### Schritt 5: Tests ausführen

```bash
cd <TARGET>
uv run python -m pytest tests/providers/test_litellm_provider.py -v 2>&1 | Select-Object -Last 15
uv run python -m pytest tests/config/test_config.py -k litellm -v 2>&1 | Select-Object -Last 10
uv run python -m pytest tests/providers/test_registry.py::test_create_provider_instantiates_litellm -v 2>&1 | Select-Object -Last 5
```

**Erwartet:**
- Mind. 3 Tests grün in test_litellm_provider.py
- Settings-Tests ggf. skipped oder commented-out (siehe Schritt 3)
- Registry-Test grün oder mit klarem Skip-Marker wenn `_make_settings` nicht erweitert wurde

### Schritt 6: Regression-Check

```bash
cd <TARGET>
uv run python -m pytest tests/ --tb=no -q 2>&1 | Select-String -Pattern '\d+ (failed|passed)'
```

**Erwartet:** `X passed, 0 failed` (X = 1354 + neue Tests)

### Schritt 7: Patch generieren für die neuen Tests

Falls Tests in neuen Files sind:
```bash
cd <TARGET>
git diff --no-index /dev/null tests/providers/test_litellm_provider.py > <TOOLKIT>/patches/M3-tests.patch 2>&1
```

Falls Tests in bestehenden Files sind (Appends):
```bash
cd <TARGET>
git diff -- tests/config/test_config.py tests/providers/test_registry.py > <TOOLKIT>/patches/M3-tests.patch 2>&1
```

**WICHTIG:** Falls BEIDE (neues File + Appends), füge die Appends an den Patch mit `>>` an.

### Schritt 8: Working Tree cleanen
```bash
cd <TARGET>
git checkout -- .
```

### Schritt 9: STOP
STOP. SubAgent-Output an Hauptmodel. Hauptmodel bewertet mit 🔴 STARK.

## E) EDGE-CASES & GOTCHAS

1. **`Settings()`-Aufruf braucht .env-file override:** In manchen Tests wird `monkeypatch.setitem(Settings.model_config, "env_file", ())` gemacht, um .env-Lookup zu verhindern. Folge dem Pattern der existierenden `TestSettings`-Tests.

2. **`_make_settings()` ist nicht vollständig:** Der Helper in `test_registry.py` deckt nicht alle Provider ab. Für den litellm-Test musst du ggf. die `nvidia_nim_api_key`-Mocks wiederverwenden oder einen eigenen Mock bauen.

3. **CRLF-Warnings:** Ignoriere. Windows-spezifisch.

4. **Loguru-Lock-Deadlock:** Pre-Existing in bestimmten Test-Szenarien. Ignoriere.

5. **`patch("providers.openai_compat.AsyncOpenAI")`:** Standard-Pattern für OpenAIChatTransport-basierte Provider-Tests. MUSS genutzt werden, sonst versucht der Test einen echten HTTP-Client zu erstellen.

6. **Settings-Fields fehlen:** Wenn `litellm_api_key` und `litellm_base_url` als Settings-Fields nicht existieren, schreibe die Tests als commented-out Sketches (siehe Schritt 3).

## F) ERFOLGS-KRITERIEN

- [ ] 3 Files editiert/erstellt: 1 neu + 2 Appends
- [ ] Mind. 3 Tests grün in `test_litellm_provider.py` (die Settings-Tests dürfen ggf. commented-out sein)
- [ ] Registry-Test grün (oder mit Skip-Marker, falls `_make_settings` Probleme macht)
- [ ] Regression: 1354+ grün, 0 zusätzliche Failures
- [ ] Patch `M3-tests.patch` im Bundle generiert
- [ ] Working Tree clean in `<TARGET>/`

## G) OUTPUT-BERICHT

Gib mir zurück:
- "Tests erstellt: [Anzahl] in [Files]"
- "Test-Result: [passed/failed Counts]"
- "Patch: [Pfad + Bytes]"
- "Working Tree Status: [clean/dirty]"
- "Settings-Fields-Status: [existieren als commented-out / fehlen dokumentiert]"

## H) MODEL-STÄRKE

🟡 MITTEL — Standard Test-Writing mit klaren Vorlagen (test_registry.py, test_config.py). Keine Architektur-Entscheidungen, nur Pattern-Mutation. STARK wäre Overkill, SCHWACH zu riskant (würde vermutlich `_make_settings` Probleme nicht lösen).
