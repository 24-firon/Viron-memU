# 🧠 DECISION LOG: Viron-memU

This file documents binding decisions agreed upon by the USER.
High-Priority Constraints override all other defaults.

## 🔴 CRITICAL CONSTRAINTS (NON-NEGOTIABLE)

### 1. Architecture: Docker Mandatory

- **Decision:** The system MUST run on Docker Desktop (Windows).
- **Anti-Pattern:** Bypassing Docker for "Native Mode" hacking.
- **Status:** **ACTIVE** (User insisted despite technical hurdles).

### 2. LLM Provider: Local vLLM

- **Decision:** Primary Inference Engine is LOCAL (`vLLM`).
- **Forbidden:** Do NOT default to OpenAI/Cloud APIs unless explicitly requested for a specific sub-task (e.g. embeddings, if local fails).
- **Reason:** Privacy & Control.

## 🟠 ARCHITECTURAL DECISIONS

### 3. Identity

- **Name:** `Viron-memU`
- **Fork:** Based on `NevaMind-AI/memU`.
- **Repo Location:** `C:\Workspace\Repos\memU`.

### 4. Memory Strategy

- **Mode:** Hybrid (Pointer System).
- **Database:** PostgreSQL + pgvector (via Docker).
- **Architecture:** Layer 1-3 (Raw -> Categories -> Items).
- **Safety:** Single-Writer-Rule enforcement.

### 5. Proactivity Pattern

- **Trigger:** Cron (pg_cron/External) > While-Loop.
- **Webhooks:** Async processing (Start Thread -> Return 200 OK immediately).

---

_Last Updated: 2026-02-05_
