<!-- Kanon v1.2, ausgerollt 2026-07-19 -->
# WORKSPACE WALKTHROUGH (Kompakt)

> Topology + Reading List für den nächsten Agent. **DENN** ohne Kontext über die Repo-Struktur verliert er 30 Minuten beim Suchen.

## 1. TECHNICAL TOPOLOGY

Kurze Verzeichnis-Landkarte mit Erklärung was wo liegt:

```
[REPO-ROOT]/
├── [Ordner 1]/         — [Beschreibung, z.B. "Next.js Web-App"]
│   ├── [sub-1]/        — [Beschreibung, z.B. "App Router"]
│   └── [sub-2]/        — [Beschreibung]
├── [Ordner 2]/         — [Beschreibung, z.B. "Shared Packages"]
├── [Ordner 3]/         — [Beschreibung, z.B. "Doku (read-only)"]
├── plans/               — [Beschreibung, z.B. "Active Execution Scripts"]
└── docs/                — [Beschreibung, z.B. "Read-Only Specs"]
```

**Modifiziere NIEMALS Dateien außerhalb deines explizit zugewiesenen Silos!**

## 2. READING LIST (Pflicht vor Code-Änderung)

Reihenfolge der Dateien die der Agent lesen MUSS:

1. **`[Pfad-1]`** — [warum kritisch, z.B. "vorheriger Session-Stand"]
2. **`[Pfad-2]`** — [warum kritisch, z.B. "aktuelle Task-Liste"]
3. **`[Pfad-3]`** — [warum kritisch, z.B. "kritische Infrastruktur-Datei"]

## 3. CORE LOGIC (Wie Daten fließen)

Kurze Erklärung der Architektur-Patterns:

- **Data Injection:** [Wie werden Daten in die App geladen — z.B. "Props vom Parent-Loader via Supabase"]
- **Styling:** [Welches System — z.B. "Tailwind v4 CSS-First, keine tailwind.config.ts"]
- **State Management:** [z.B. "Server Components default, 'use client' nur als Ausnahme"]
- **Animation:** [z.B. "Framer Motion, nur opacity + transform animieren (GPU-Guard)"]

## 4. NICHT ANFASSEN (TABU)

| Pfad/Bereich | Warum tabu |
|:---|:---|
| `[z.B. _ARCHIVE/]` | Historisch, nicht mehr aktiv |
| `[z.B. node_modules/]` | Dependencies |
| `[z.B. .opencode/rules/]` (außer auf Anweisung) | Boot-Regeln, externe Abhängigkeit |
