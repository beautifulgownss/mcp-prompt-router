from .openai_adapter import OpenAIAdapter
from .anthropic_adapter import AnthropicAdapter

ADAPTERS = {
    "openai": OpenAIAdapter(),
    "anthropic": AnthropicAdapter()
}
