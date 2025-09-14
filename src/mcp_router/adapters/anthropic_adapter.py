import os
from typing import Dict, Any

class AnthropicAdapter:
    name = 'anthropic'
    
    def completions(self, prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        # Check if real calls are enabled
        if os.getenv('ROUTER_REAL_CALLS', '0') == '1':
            return self._real_completion(prompt, model, **kwargs)
        else:
            return self._stub_completion(prompt, model, **kwargs)
    
    def _real_completion(self, prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        try:
            import httpx
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                return {"output": "[error] ANTHROPIC_API_KEY not set", "error": "missing_key"}
            
            headers = {
                "x-api-key": api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            payload = {
                "model": model,
                "max_tokens": 100,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            with httpx.Client() as client:
                response = client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=headers,
                    json=payload,
                    timeout=10.0
                )
                
            if response.status_code == 200:
                data = response.json()
                return {
                    "output": data["content"][0]["text"],
                    "usage": data.get("usage", {})
                }
            else:
                return {
                    "output": f"[anthropic-error] HTTP {response.status_code}",
                    "error": "api_error"
                }
                
        except Exception as e:
            return {
                "output": f"[anthropic-error] {str(e)}",
                "error": "exception"
            }
    
    def _stub_completion(self, prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        return {
            "output": f"[anthropic-stub] {prompt[:40]}...",
            "usage": {
                "input_tokens": len(prompt) // 4,
                "output_tokens": 25,
                "total_tokens": len(prompt) // 4 + 25
            }
        }
