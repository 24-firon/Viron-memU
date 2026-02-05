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

## 4. DIE "REGEL DER REGELN" (META-KOMPETENZ)

**Jede** explizite Benutzer-Entscheidung (z.B. Architektur, Tools, Verbote) MUSS sofort in eine Regel-Datei geschrieben werden.

1.  **Erkennen:** User sagt "Mach X nicht" oder "Nutze Y".
2.  **Schreiben:** Sofort `PROJECT_RULES.md` oder `DECISION_LOG.md` updaten.
3.  **Bestätigen:** "Regel angelegt in [Datei]."
    **Verbot:** Niemals nur "Verstanden" sagen. Ohne Datei existiert die Regel nicht.
