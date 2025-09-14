from typing import Protocol, Dict, Any

class ProviderAdapter(Protocol):
    name: str
    
    def completions(self, prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        ...
