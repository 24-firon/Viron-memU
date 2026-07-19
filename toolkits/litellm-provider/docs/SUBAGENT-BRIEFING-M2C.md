# SubAgent-Briefing M2.C — Settings + Test-Aktivierung

> **Briefing für:** SubAgent mit 🟡 MITTEL-Model
> **Voraussetzung am Working Tree:** M1 + M2 + M3 Patches bereits applied (siehe APPLY.md)
> **Output:** 2 File-Edits in `<TARGET>/` + 1 Patch-File im Bundle
> **Stop-Bedingungen:** Nach 3 Schritten oder 15 Minuten Timeout

---

## A) MISSION

Schließe die M2.C-Lücke:
1. **`config/settings.py`:** 3 neue Fields hinzufügen (`litellm_api_key`, `litellm_base_url`, `litellm_proxy`)
2. **`tests/providers/test_litellm_provider.py`:** Die 2 auskommentierten Settings-Tests aktivieren
3. **Patch generieren und im Bundle speichern**

**NICHT-ZIELE (separater SubAgent):**
- Admin-UI-Felder (`api/admin_config.py`) — separater Task
- `.env.example` — separater Task

## B) CONTEXT

### Warum diese Edits?
- Der LiteLLM-Provider ist implementiert, aber ohne Settings-Fields kann er nicht via .env konfiguriert werden
- Die existierenden 2 Settings-Tests in `test_litellm_provider.py:91-107` sind als Kommentar-Sketches abgelegt — sie müssen aktiviert werden, nachdem die Fields existieren

### Vorhandene Settings-Pattern

Lies `config/settings.py` Zeile 122-188 (OpenCode, OpenCode Go, Z.ai, Fireworks Provider-Felder). Pattern:

```python
# ==================== OpenCode Go Config ====================
opencode_go_api_key: str = Field(default="", validation_alias="OPENCODE_GO_API_KEY")
```

Plus die `validate_credential` Liste Zeile 420-435 enthält alle credential fields — `litellm_api_key` muss dort hinzugefügt werden.

Plus `proxy_attr` Pattern (siehe Zeile 178-188) — `litellm_proxy` muss dort auch eingefügt werden.

## C) SCOPE

### ✅ Erlaubt
- 3 Felder in `config/settings.py` hinzufügen
- 1 Liste (`validate_credential`) in `config/settings.py` erweitern
- 1 Test-File editieren (Kommentare entfernen, Tests aktivieren)
- Patch generieren: `git diff > <TOOLKIT>/patches/M2c-settings.patch`

### ❌ Verboten
- KEIN `git commit`
- KEIN `git add` (Working Tree bleibt mit Changes)
- Admin-UI nicht anfassen (separater Task)
- .env.example nicht anfassen (separater Task)
- `nvidia_nim_api_key`-Felder nicht ändern (Pre-Existing)
- `validate_credential`-Liste: NUR `litellm_api_key` hinzufügen, andere nicht

## D) ATOMARE SCHRITTE

### Schritt 1: Settings-Fields hinzufügen

Lies `<TARGET>/config/settings.py` Zeile 122-188 als Vorlage.

Füge NACH Zeile 132 (nach `fireworks_api_key`) einen neuen Block ein:

```python
    # ==================== LiteLLM Config ====================
    litellm_api_key: str = Field(default="", validation_alias="LITELLM_API_KEY")
    litellm_base_url: str = Field(
        default="http://127.0.0.1:4000",
        validation_alias="LITELLM_BASE_URL",
    )
    litellm_proxy: str = Field(default="", validation_alias="LITELLM_PROXY")
```

Füge in `validate_credential` (Zeile 420-435) `"litellm_api_key"` zur Liste der field-names hinzu. Die Liste ist nach Alphabet sortiert — füge zwischen `"kimi_api_key"` und `"nvidia_nim_api_key"` ein.

Füge in die `proxy_attr` Fields (Zeile 178-188) `litellm_proxy: str = Field(default="", validation_alias="LITELLM_PROXY")` zwischen `kimi_proxy` und `lmstudio_proxy` ein (nach Alphabet).

**WICHTIG:** Überprüfe mit `git diff -- config/settings.py | head -30` dass die Edits korrekt sind.

### Schritt 2: Tests aktivieren

Lies `<TARGET>/tests/providers/test_litellm_provider.py` Zeile 90-107 (die auskommentierten Settings-Tests).

Entferne die `# `-Präfixe, sodass:
```python
class TestLiteLLMSettings:
    """Test LiteLLM settings fields (after M2.C adds them to config/settings.py)."""

    def test_litellm_api_key_from_env(self, monkeypatch):
        from config.settings import Settings
        monkeypatch.setenv("LITELLM_API_KEY", "sk-litellm-test")
        settings = Settings()
        assert settings.litellm_api_key == "sk-litellm-test"

    def test_litellm_base_url_from_env(self, monkeypatch):
        from config.settings import Settings
        monkeypatch.setenv("LITELLM_BASE_URL", "http://custom:5000")
        settings = Settings()
        assert settings.litellm_base_url == "http://custom:5000"
```

(SubAgent muss auch die `import pytest` Zeile oben prüfen — `monkeypatch` ist pytest-Fixture, sollte bereits importiert sein.)

### Schritt 3: Tests ausführen

```bash
cd <TARGET>
uv run python -m pytest tests/providers/test_litellm_provider.py -v 2>&1 | Select-Object -Last 15
```

**Erwartet:** 7 passed (5 alte + 2 neue aktivierte)

Falls ein Test fehlschlägt:
- `validate_credential` Validation: leerer String erlaubt, also `LITELLM_API_KEY=""` sollte nicht failen
- `validate_model_format`: nicht relevant, weil Settings-Fields keine `MODEL_*` sind

### Schritt 4: Patch generieren

```bash
cd <TARGET>
git diff -- config/settings.py tests/providers/test_litellm_provider.py > <TOOLKIT>/patches/M2c-settings.patch
```

### Schritt 5: Working Tree NICHT committen

**WICHTIG:** KEIN `git commit`, KEIN `git add`. Patch ist im Bundle.

### Schritt 6: STOP

STOP. SubAgent-Output an Hauptmodel. Hauptmodel bewertet mit 🔴 STARK.

## E) EDGE-CASES & GOTCHAS

1. **Encoding-Probleme bei Settings-File:** Das bestehende `settings.py` ist UTF-8. Verwende keine Sonderzeichen außer ASCII.

2. **Alphabetische Sortierung in Listen:** `validate_credential` und `proxy_attr` sind alphabetisch sortiert. Beim Einfügen strikt einhalten.

3. **pytest monkeypatch:** `monkeypatch.setenv` braucht `pytest` import. Stelle sicher dass `import pytest` oben im Test-File vorhanden ist. Falls nicht, hinzufügen.

4. **`_make_settings` in test_registry.py:** Nicht relevant für Settings-Tests. Settings-Tests rufen `Settings()` direkt auf (wie `test_wafer_api_key_from_env`).

5. **Loguru-Lock-Warnings:** Ignorieren.

6. **CRLF-Warnings:** Ignorieren (Windows).

7. **M3-tests.patch bereits applied:** Die `test_litellm_provider.py` ist im Working Tree. SubAgent muss die existierende Datei editieren, nicht neu erstellen.

## F) ERFOLGS-KRITERIEN

- [ ] 3 Felder in `config/settings.py` hinzugefügt
- [ ] `litellm_api_key` in `validate_credential` Liste
- [ ] `litellm_proxy` in proxy-Feldern
- [ ] 2 Settings-Tests aktiviert (Kommentare entfernt)
- [ ] 7 Tests grün in `test_litellm_provider.py` (5 alte + 2 neue)
- [ ] Patch `M2c-settings.patch` im Bundle generiert
- [ ] Working Tree clean von Commits (Changes untracked/staged sind OK)
- [ ] KEIN `git commit`

## G) OUTPUT-BERICHT

Gib mir zurück:
- "Settings-Fields: [litellm_api_key, litellm_base_url, litellm_proxy] hinzugefügt"
- "validate_credential erweitert: ja/nein"
- "Settings-Tests aktiviert: ja/nein"
- "Test-Result: [passed/failed counts]"
- "Patch: [Pfad + Bytes]"
- "Working Tree Status: [M oder A oder nichts pro file]"

## H) MODEL-STÄRKE

🟡 MITTEL — Settings-Field-Pattern ist bekannt (Kopiere von opencode_go). Test-Aktivierung ist mechanisch (Kommentare entfernen). Keine Architektur-Entscheidungen, nur Pattern-Mutation + Listen-Erweiterung.
