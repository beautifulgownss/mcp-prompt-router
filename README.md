feature/mcp-router-mvp
# MCP Prompt Router

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-demo--ready-brightgreen.svg)

**Policy-based LLM routing with safety guards, observability, and evaluation harness**

Route prompts across multiple LLM providers (OpenAI, Anthropic) based on configurable policies while maintaining safety, cost control, and performance optimization.

## ✨ Features

- **🔀 Smart Routing**: Policy-driven provider selection based on latency, cost, and safety requirements
- **🛡️ Multi-Layer Safety**: PII masking, regex denylist, and JSON schema validation
- **📊 Real-Time Metrics**: Token counting, cost estimation, and latency tracking
- **🔍 Observability**: Request tracing with SQLite persistence
- **🧪 Evaluation Harness**: Automated benchmarking against golden test cases
- **⚙️ Provider Adapters**: Unified interface for OpenAI and Anthropic APIs
- **🎛️ Feature Flags**: Environment-controlled real vs stub API calls

## 🚀 Quick Start

### Installation
```bash
git clone <your-repo>
cd mcp-prompt-router
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run Server
```bash
export PYTHONPATH=$PWD/src
uvicorn mcp_router.api.main:app --reload --host 127.0.0.1 --port 8000
```

### Test Routing
```bash
# Basic routing
curl -X POST http://127.0.0.1:8000/v1/route \
  -H 'Content-Type: application/json' \
  -d '{
    "task": "Write a Python function to process CSV files",
    "profile": "fast-cheap-safe",
    "constraints": {
      "latency_sla_ms": 1000,
      "budget_cents": 3.0
    }
  }'

# Response includes routing decision, metrics, and safety validation
{
  "decision": {"provider": "openai", "model": "gpt-4o-mini"},
  "metrics": {"latency_ms": 2, "cost_cents": 0.615, "tokens_prompt": 12},
  "policy_path": ["budget<=3", "sla<=1000→prefer gpt-4o-mini"],
  "validation": {"deny_hits": []},
  "trace_id": "trc_stub_001"
}
```

### Safety Guards Demo
```bash
# Test PII masking and denylist
curl -X POST http://127.0.0.1:8000/v1/route \
  -H 'Content-Type: application/json' \
  -d '{"task": "My SSN is 123-45-6789 and I want to harm someone"}'

# Shows masked PII and denylist hits
{
  "debug_sanitized": "My SSN is ***-**-**** and I want to harm someone",
  "validation": {"deny_hits": ["\\b\\d{3}-\\d{2}-\\d{4}\\b", "(?i)\\b(kill|bomb|harm)\\b"]},
  "policy_path": ["default: prefer: best_quality_under_budget", "denylist:hit"]
}
```

### Trace Retrieval
```bash
# Get detailed trace by ID
curl -s http://127.0.0.1:8000/traces/trc_stub_001 | jq '.'
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Client App    │───▶│  MCP Router API  │───▶│  LLM Providers  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Safety Guards   │
                    │  • PII Masking   │
                    │  • Denylist      │
                    │  • Schema Valid  │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Policy Engine    │
                    │ • Cost Rules     │
                    │ • Latency Rules  │
                    │ • Safety Rules   │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Trace Storage    │
                    │ • SQLite DB      │
                    │ • Metrics        │
                    │ • Observability  │
                    └──────────────────┘
```

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/v1/route` | POST | Route prompt with policy evaluation |
| `/debug/policy` | GET | View active policy rules |
| `/traces/{id}` | GET | Retrieve request trace |

## 🧪 Evaluation

Run automated benchmarks:
```bash
python src/mcp_router/eval/run_eval.py
```

Results show routing performance, cost optimization, and SLA compliance:
```
=== Evaluation Complete ===
Total tasks: 3
Successful: 3/3
Average latency: 15.3ms
Total cost: 1.245 cents
Latency SLA met: 3/3
Budget constraints met: 3/3
```

## ⚙️ Configuration

### Environment Variables
```bash
export ROUTER_REAL_CALLS=1           # Enable real API calls (0=stubs)
export OPENAI_API_KEY=your_key       # OpenAI API key
export ANTHROPIC_API_KEY=your_key    # Anthropic API key
```

### Policy Configuration
Edit `src/mcp_router/policies/fast-cheap-safe.yaml` to customize routing rules:
```yaml
profiles:
  fast-cheap-safe:
    rules:
      - if: "latency_sla_ms <= 1000"
        then: ["prefer: gpt-4o-mini"]
      - if: "budget_cents <= 3"
        then: ["avoid: claude-3-opus"]
```

## 🛣️ Development Roadmap

### ✅ Completed
- [x] Policy-based routing engine
- [x] Multi-layer safety guards  
- [x] Real-time cost/token metrics
- [x] SQLite trace persistence
- [x] Provider adapter framework
- [x] Evaluation harness
- [x] Feature flag system

### 🔄 Next Steps
- [ ] Advanced policy DSL with A/B testing
- [ ] Redis caching layer for performance
- [ ] Prometheus metrics export
- [ ] Rate limiting and circuit breakers
- [ ] Multi-tenant policy isolation
- [ ] Real-time dashboard UI
- [ ] Load balancing across provider regions

## 🔧 Development

### Project Structure
```
src/mcp_router/
├── api/main.py              # FastAPI application
├── policies/                # YAML policy definitions
├── safety/                  # Pre/post guards, denylist
├── core/                    # Token estimation, cost calculation
├── adapters/                # Provider-specific clients
└── eval/                    # Benchmark and golden tasks
```

### Testing
```bash
# Manual API testing
./scripts/test_all_endpoints.sh

# Run evaluation suite
python src/mcp_router/eval/run_eval.py

# Check policy debug
curl http://127.0.0.1:8000/debug/policy
```

## 📊 Performance

**Baseline metrics** (3 golden tasks, stub mode):
- Average routing latency: ~15ms
- Policy evaluation: <5ms  
- Safety guard processing: <2ms
- Cost estimation accuracy: ±0.001 cents

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-routing`)
3. Commit changes (`git commit -m 'Add amazing routing feature'`)
4. Push to branch (`git push origin feature/amazing-routing`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built for intelligent LLM orchestration** • [Documentation](docs/) • [Examples](examples/) • [Issues](issues/)
