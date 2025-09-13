from typing import Any, Dict

def route_task(task: str, inputs: Dict[str, Any] | None, constraints: Dict[str, Any] | None, profile: str | None):
    # Minimal placeholder logic; will be replaced by policy engine + adapters
    decision = {"provider": "openai", "model": "gpt-4o-mini"}
    metrics = {"latency_ms": 123, "tokens_prompt": 200, "tokens_output": 80, "cost_cents": 1.2}
    policy_path = ["default: prefer fast-cheap-safe"]
    output = f"(stub) Routed '{task[:40]}...' to {decision['provider']}:{decision['model']}"
    return {
        "decision": decision,
        "metrics": metrics,
        "policy_path": policy_path,
        "output": output,
        "trace_id": "trc_stub_001"
    }