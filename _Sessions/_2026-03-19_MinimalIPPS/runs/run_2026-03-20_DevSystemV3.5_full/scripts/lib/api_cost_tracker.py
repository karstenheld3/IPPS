"""API cost tracking with budget guard. Rates from NOTES.md Anthropic Pricing Reference."""

# Standard API rates (2x batch tier). Per 1M tokens.
PRICING = {
    "claude-opus-4-6": {
        "input": 15.00,
        "cached_read": 1.50,
        "cached_write": 30.00,
        "output": 75.00,
    },
    "gpt-5-mini": {
        "input": 0.25,
        "output": 2.00,
    },
}


def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    cache_read_tokens: int = 0,
    cache_write_tokens: int = 0,
) -> float:
    """Calculate cost in USD for a single API call.

    Args:
        model: Model name matching PRICING dict key
        input_tokens: Non-cached input tokens
        output_tokens: Output/completion tokens
        cache_read_tokens: Anthropic cache read tokens
        cache_write_tokens: Anthropic cache write tokens

    Returns:
        Cost in USD

    Raises:
        KeyError: If model not in PRICING dict
    """
    if model not in PRICING:
        raise KeyError(f"Unknown model '{model}' - not in PRICING dict. Available: {list(PRICING.keys())}")
    rates = PRICING[model]
    cost = 0.0
    cost += (input_tokens / 1_000_000) * rates["input"]
    cost += (output_tokens / 1_000_000) * rates["output"]
    if "cached_read" in rates:
        cost += (cache_read_tokens / 1_000_000) * rates["cached_read"]
    if "cached_write" in rates:
        cost += (cache_write_tokens / 1_000_000) * rates["cached_write"]
    return cost


def check_budget(state: dict, config: dict) -> tuple[bool, str]:
    """Check if budget threshold is reached.

    Returns:
        (halt, message) tuple:
        - halt=True, message="halt: ..." when at/over 100% budget
        - halt=False, message="warning: ..." when at/over warn_at_percent
        - halt=False, message="" when under warning threshold
    """
    total = state["cost"]["total"]
    max_budget = config["budget"]["max_total_usd"]
    warn_pct = config["budget"]["warn_at_percent"]

    if max_budget <= 0:
        return False, ""

    pct = (total / max_budget) * 100

    if pct >= 100:
        return True, f"halt: budget exceeded - ${total:.2f} / ${max_budget:.2f} ({pct:.0f}%)"
    if pct >= warn_pct:
        return False, f"warning: {pct:.0f}% of budget used - ${total:.2f} / ${max_budget:.2f}"
    return False, ""
