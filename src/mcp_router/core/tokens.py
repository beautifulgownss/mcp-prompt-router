def naive_token_estimate(text: str) -> int:
    if not text:
        return 0
    return max(1, len(text) // 4)
