## Dateien, die ein anderer Agent für fehlerfreien LiteLLM-Betrieb braucht

**Pflicht (KRITISCH — ohne diese startet LiteLLM nicht):**

| Datei                                           | Zweck                             | Aktueller Stand                 |
| ----------------------------------------------- | --------------------------------- | ------------------------------- |
| `C:\Workspace\Repos\LiteLLM\docker-compose.yml` | Service-Definition (LiteLLM + DB) | ✅ funktioniert                  |
| `C:\Workspace\Repos\LiteLLM\config.yaml`        | 30 Modelle, Routing, Settings     | ✅ funktioniert (nach Hook-Fix)` |
| `C:\Workspace\Repos\LiteLLM\.env`               | Echte API-Keys + DB-Credentials   | ✅ existiert, NICHT committed    |
| `C:\Workspace\Repos\LiteLLM\.env.example`       | Vorlage für Keys (committed)      | ✅ existiert                     |
| `C:\Workspace\Repos\LiteLLM\.gitignore`         | Verhindert `.env`-Leak            | ✅ existiert                     |

**Pflicht (für Übergang/Kontext):**

| Datei          | Zweck                                             |
| -------------- | ------------------------------------------------- |
| `README.md`    | Start, Health-Check, Model-Abfrage                |
| `BLUESMIND.md` | BluesMind-Integration (8 Modelle, Config-Vorlage) |

**Referenz/Doku (in `STORAGE/`):**

| Datei                                  | Zweck                                                        |
| -------------------------------------- | ------------------------------------------------------------ |
| `ALL_MODELS.md`                        | Komplettinventar aller Modelle aus 4 Providern               |
| `MODEL_CATALOG.md`                     | BluesMind-Detail-Katalog                                     |
| `ALLOWED_MODELS.md`                    | Aktive Allowed-Liste (via `ALLOWED_MODELS`-env)              |
| `BLACKLISTED_MODELS.md`                | Differenz ALL − ALLOWED                                      |
| `llm_model_master_database_v4.csv`     | Master-Datenbank mit 139 Modellen, Benchmarks, Web-Verweisen |
| `LLM_Model_Essentials_Stack_v1.csv`    | 54 kuratierte Essentials (Deutsch, hochwertig)               |
| `LLM_Essentials_Stack_Selected_v2.csv` | 61 Modelle (English, mittlere Qualität — Referenz)           |

**Was NICHT nötig ist:**

- `LLM_Essential_Stack_DE_v1.csv` — Boilerplate, Duplikate
- `LLM_Essential_Stack_Pro_v1.csv` — gute Daten, aber redundant zu Selected v2
- `DOCS/` (LiteLLM) — eigene Doku, nicht zwingend

**Wichtig:** Der **Proxy** auf `C:\Workspace\Repos\claude-code-proxy\` braucht nur seine eigene `.env` (`LITELLM_API_KEY` + `LITELLM_BASE_URL`) — keine andere Datei.

---

**Kurzfassung für den nächsten Agent:**

1. **LiteLLM selbst:** `docker-compose.yml`, `config.yaml`, `.env` (gitignored)
2. **Proxy-Verbindung:** `claude-code-proxy/.env` Zeile `LITELLM_*` + `MODEL=litellm/<name>`
3. **Health-Check:** `curl http://127.0.0.1:4000/health/readiness` → `{"status":"healthy","db":"connected"}`
4. **E2E-Test:** `curl http://127.0.0.1:18082/v1/messages -H "x-api-key: $ANTHROPIC_AUTH_TOKEN"` mit `model: "litellm/minimax-m3"`
