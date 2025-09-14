import json
import time
import requests
from pathlib import Path

def run_evaluation():
    # Load golden tasks
    tasks_file = Path('src/mcp_router/eval/golden_tasks.json')
    if not tasks_file.exists():
        print("Error: golden_tasks.json not found")
        return
    
    tasks = json.loads(tasks_file.read_text())
    base_url = 'http://127.0.0.1:8000/v1/route'
    
    print(f"Running evaluation on {len(tasks)} tasks...")
    results = []
    
    for task in tasks:
        print(f"Testing {task['id']}: {task['task'][:50]}...")
        
        # Prepare request
        payload = {
            "task": task["task"],
            "profile": task["profile"],
            "constraints": task["constraints"]
        }
        
        # Time the request
        start_time = time.time()
        
        try:
            response = requests.post(base_url, json=payload, timeout=10)
            request_time = int((time.time() - start_time) * 1000)
            
            if response.status_code == 200:
                data = response.json()
                
                result = {
                    "id": task["id"],
                    "status": "success",
                    "request_latency_ms": request_time,
                    "router_latency_ms": data.get("metrics", {}).get("latency_ms", 0),
                    "cost_cents": data.get("metrics", {}).get("cost_cents", 0),
                    "tokens_prompt": data.get("metrics", {}).get("tokens_prompt", 0),
                    "tokens_output": data.get("metrics", {}).get("tokens_output", 0),
                    "provider": data.get("decision", {}).get("provider", "unknown"),
                    "model": data.get("decision", {}).get("model", "unknown"),
                    "policy_path": data.get("policy_path", []),
                    "deny_hits": data.get("validation", {}).get("deny_hits", []),
                    "trace_id": data.get("trace_id", ""),
                    "constraints_met": {
                        "latency": request_time <= task["constraints"]["latency_sla_ms"],
                        "budget": data.get("metrics", {}).get("cost_cents", 0) <= task["constraints"]["budget_cents"]
                    }
                }
            else:
                result = {
                    "id": task["id"],
                    "status": "http_error",
                    "error": f"HTTP {response.status_code}",
                    "request_latency_ms": request_time
                }
                
        except Exception as e:
            result = {
                "id": task["id"], 
                "status": "exception",
                "error": str(e),
                "request_latency_ms": int((time.time() - start_time) * 1000)
            }
        
        results.append(result)
    
    # Save results
    output_dir = Path('data/evals')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_file = output_dir / 'report.json'
    report_file.write_text(json.dumps(results, indent=2))
    
    # Print summary
    print(f"\n=== Evaluation Complete ===")
    print(f"Results saved to: {report_file}")
    print(f"Total tasks: {len(results)}")
    
    success_count = sum(1 for r in results if r.get('status') == 'success')
    print(f"Successful: {success_count}/{len(results)}")
    
    if success_count > 0:
        avg_latency = sum(r.get('request_latency_ms', 0) for r in results if r.get('status') == 'success') / success_count
        total_cost = sum(r.get('cost_cents', 0) for r in results if r.get('status') == 'success')
        
        print(f"Average latency: {avg_latency:.1f}ms")
        print(f"Total cost: {total_cost:.3f} cents")
        
        # Constraint compliance
        latency_ok = sum(1 for r in results if r.get('constraints_met', {}).get('latency', False))
        budget_ok = sum(1 for r in results if r.get('constraints_met', {}).get('budget', False))
        
        print(f"Latency SLA met: {latency_ok}/{success_count}")
        print(f"Budget constraints met: {budget_ok}/{success_count}")

if __name__ == "__main__":
    run_evaluation()
