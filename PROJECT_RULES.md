# PROJEKT-REGELN (VIRON-MEMU)

## 1. ORDNUNG

- Das Repo bleibt strikt im Root `C:\Workspace\Repos\memU`.
- Der lokale Ordner heißt `memU`.
- Keine unnötigen Unterordner wie `Setup` erstellen, es sei denn explizit gefordert.

## 2. DOCKER-INFRASTRUKTUR

- `docker-compose.yml` und `.env` liegen im Root.
- Umgebung in `memU.code-workspace` definieren.

## 3. TECHNOLOGIE-CONSTRAINTS (HART)

- **Docker Mandatory:** Es wird NICHTS "nativ" auf Windows gehackt. Wenn Docker streikt, wird Docker gefixt.
- **LLM Provider:** **Local vLLM** ist der Standard. OpenAI ist verboten (außer explizit für Embeddings erlaubt).
