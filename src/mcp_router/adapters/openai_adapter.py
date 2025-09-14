import os
import json
from typing import Dict, Any

class OpenAIAdapter:
    name = 'openai'
    
    def completions(self, prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        # Check if real calls are enabled
        if os.getenv('ROUTER_REAL_CALLS', '0') == '1':
            return self._real_completion(prompt, model, **kwargs)
        else:
            return self._stub_completion(prompt, model, **kwargs)
    
    def _real_completion(self, prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        try:
            import httpx
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                return {"output": "[error] OPENAI_API_KEY not set", "error": "missing_key"}
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 100
            }
            
            with httpx.Client() as client:
                response = client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=10.0
                )
                
            if response.status_code == 200:
                data = response.json()
                return {
                    "output": data["choices"][0]["message"]["content"],
                    "usage": data.get("usage", {})
                }
            else:
                return {
                    "output": f"[openai-error] HTTP {response.status_code}",
                    "error": "api_error"
                }
                
        except Exception as e:
            return {
                "output": f"[openai-error] {str(e)}",
                "error": "exception"
            }
    
    def _stub_completion(self, prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        return {
            "output": f"[openai-stub] {prompt[:40]}...",
            "usage": {
                "prompt_tokens": len(prompt) // 4,
                "completion_tokens": 20,
                "total_tokens": len(prompt) // 4 + 20
            }
        }
