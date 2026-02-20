---
description: Wie man die memU Infrastruktur (Phase 2) startet.
---

# 🚀 Deployment Workflow (Phase 2)

Dieses Workflow führt dich durch den Start der Docker-Infrastruktur.

## 1. Voraussetzungen prüfen

Stelle sicher, dass **Docker Desktop** läuft.

## 2. Container starten

Führe im Root-Verzeichnis (`C:\Workspace\Repos\memU`) folgenden Befehl aus:

// turbo

```bash
docker compose up -d
```

## 3. Health-Check

Prüfe, ob alle Dienste "UP" sind:

```bash
docker compose ps
```

Erwartete Dienste:

- `memu-postgres` (Port 5435)
- `memu-vllm` (Port 8005)
- `open-webui` (Port 3005)

## 4. Zugriff

- **Chat Interface:** Öffne [http://localhost:3005](http://localhost:3005) im Browser.
- **API (vLLM):** Erreichbar unter `http://localhost:8005/v1`.

## 5. Troubleshooting

Falls ein Container nicht startet:

```bash
docker compose logs -f [service-name]
```
