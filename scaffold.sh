#!/bin/bash
# scaffold.sh — creates the project structure for MCP Prompt Router

mkdir -p src/mcp_router/{api,core,adapters,policies,evals,tests}
mkdir -p data/{logs,traces,evals}
mkdir -p scripts

# Core entrypoints
touch src/mcp_router/__init__.py
touch src/mcp_router/api/{__init__.py,main.py,routes.py}
touch src/mcp_router/core/{__init__.py,router.py,trace_store.py}
touch 
src/mcp_router/adapters/{__init__.py,openai_adapter.py,anthropic_adapter.py}
touch src/mcp_router/policies/{__init__.py,policy_loader.py}
touch src/mcp_router/evals/{__init__.py,runner.py,metrics.py}
touch src/mcp_router/tests/{__init__.py,test_router.py}

# Env + config
cat > .env.example <<EOF
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
EOF

# Requirements snapshot
cat > requirements.txt <<EOF
fastapi
uvicorn
pydantic>=2
httpx
typer
rich
python-dotenv
duckdb
sqlite-utils
pytest
pytest-cov
EOF

echo "✅ Project scaffold created."
