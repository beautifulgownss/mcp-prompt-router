from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

from mcp_router.policies.loader import load_policy
from mcp_router.safety.pre import mask_pii
from mcp_router.safety.post import validate_json_schema

app = FastAPI(title="MCP Prompt Router", version="0.1.0")


# ---------- Models ----------
class RouteConstraints(BaseModel):
    latency_sla_ms: Optional[int] = Field(default=1200)
    budget_cents: Optional[float] = Field(default=5.0)
    safety: Optional[str] = Field(default="standard")  # "standard" | "strict"


class RouteRequest(BaseModel):
    task: str
    inputs: Optional[Dict[str, Any]] = None
    constraints: Optional[RouteConstraints] = None
    profile: Optional[str] = Field(default="fast-cheap-safe")
    metadata: Optional[Dict[str, Any]] = None


# ---------- Policy evaluation ----------
def evaluate_policy(profile: str, constraints: RouteConstraints) -> Dict[str, Any]:
    data = load_policy("fast-cheap-safe.yaml")
    profiles = data.get("profiles", {})
    prof = profiles.get(profile, {})
    rules = prof.get("rules", [])

    latency = constraints.latency_sla_ms if constraints else 1200
    budget = constraints.budget_cents if constraints else 5.0
    safety = constraints.safety if constraints else "standard"

    decision_model = "gpt-4o-mini"
    path: List[str] = []

    for rule in rules:
        if "if" in rule:
            cond = rule["if"]
            acts = rule.get("then", [])
            if cond == "safety == 'strict'" and safety == "strict":
                path.append("safety:strict→guards")
            if cond == "latency_sla_ms <= 1000" and latency <= 1000:
                if "prefer: gpt-4o-mini" in acts:
                    decision_model = "gpt-4o-mini"
                    path.append("sla<=1000→prefer gpt-4o-mini")
                if "fallback: claude-3-haiku" in acts:
                    path.append("fallback: claude-3-haiku")
            if cond == "budget_cents <= 3" and budget <= 3:
                path.append("budget<=3")
                if "avoid: claude-3-opus" in acts:
                    path.append("avoid: claude-3-opus")
        elif "default" in rule:
            if not path:
                def_acts = rule["default"]
                path.append("default: " + ", ".join(def_acts))

    if not path:
        path.append("default: prefer fast-cheap-safe")

    return {"provider": "openai", "model": decision_model, "policy_path": path}


# ---------- Routes ----------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/v1/route")
def route(req: RouteRequest):
    constraints = req.constraints or RouteConstraints()

    # Apply pre-guard (mask PII)
    raw_task = req.task
    sanitized_task = mask_pii(raw_task)

    # Evaluate policy
    decision = evaluate_policy(req.profile or "fast-cheap-safe", constraints)

    # Optional post-guard schema validation
    validation = None
    schema = None
    if req.metadata and isinstance(req.metadata, dict):
        schema = req.metadata.get("schema")

    if schema:
        extraction_result = {"name": "John Q Doe", "email": "***@***"}  # stub
        ok, errors = validate_json_schema(extraction_result, schema)
        validation = {
            "ok": ok,
            "errors": errors,
            "checked_keys": list(extraction_result.keys())
        }

    return {
        "decision": {
            "provider": decision["provider"],
            "model": decision["model"]
        },
        "metrics": {
            "latency_ms": 123,
            "tokens_prompt": 200,
            "tokens_output": 80,
            "cost_cents": 1.2
        },
        "policy_path": decision["policy_path"],
        "output": f"(stub) Routed '{sanitized_task[:20]}...' "
                  f"to {decision['provider']}:{decision['model']}",
        "debug_sanitized": sanitized_task,
        "validation": validation,
        "trace_id": "trc_stub_001"
    }


@app.get("/debug/policy")
def debug_policy():
    data = load_policy("fast-cheap-safe.yaml")
    profiles = list((data.get("profiles") or {}).keys())
    rules = (data.get("profiles") or {}).get("fast-cheap-safe", {}).get("rules", [])
    return {"profiles": profiles, "rule_count": len(rules), "rules": rules}
