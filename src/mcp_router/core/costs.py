from dataclasses import dataclass

@dataclass
class Price:
    prompt_per_1k: float
    completion_per_1k: float

PRICES = {
    'gpt-4o-mini': Price(0.15, 0.60),
    'claude-3-haiku': Price(0.25, 1.25),
    'gpt-4o': Price(2.50, 10.00),
    'claude-3-opus': Price(15.00, 75.00)
}

def estimate_cost_cents(model: str, prompt_tokens: int, output_tokens: int) -> float:
    price = PRICES.get(model)
    if not price:
        return 0.0
    cost_dollars = (prompt_tokens / 1000) * price.prompt_per_1k + (output_tokens / 1000) * price.completion_per_1k
    return cost_dollars * 100
