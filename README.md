# MCP Prompt Router

**Policy-driven AI routing service with safety guardrails and full observability.**

The MCP Prompt Router is a **FastAPI-based microservice** that routes prompts to the right LLM (OpenAI, Anthropic, etc.) based on **policy profiles** (cost, latency, safety). It applies **pre- and post-guardrails** (PII scrub, schema validation) and logs all requests into a **trace store** for debugging, analytics, and evaluation.

---

## ✨ Features
- **Policy-based routing**  
  - Profiles: `fast-cheap-safe`, `best-quality`, `strict-compliance`  
  - Selects provider + model based on budget, latency, and safety constraints.
- **Safety guardrails**  
  - Pre-guard: PII scrubbing (emails, phones).  
  - Post-guard: JSON Schema output validation.  
  - Regex denylist for restricted content.
- **Observability**  
  - SQLite trace store with JSONL and CSV export.  
  - `trace_id` returned on every call for reproducibility.  
  - `/traces/recent` endpoint to inspect last N runs.
- **Providers (pluggable)**  
  - OpenAI (gpt-4o-mini, gpt-4.1)  
  - Anthropic (Claude 3 family)  
  - Easily extended to other adapters.
- **Developer-friendly**  
  - REST API with OpenAPI docs (`/docs`).  
  - Simple `.env` config for keys and defaults.  
  - Lightweight, no external infra needed.

---

## 🚀 Quickstart

```bash
# clone repo
git clone https://github.com/<your-username>/mcp-prompt-router.git
cd mcp-prompt-router

# setup env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add API keys

# run
make run
# open http://127.0.0.1:8000/docs
