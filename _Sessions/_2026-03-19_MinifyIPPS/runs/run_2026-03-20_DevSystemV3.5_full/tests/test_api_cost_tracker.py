"""Tests for lib/api_cost_tracker.py (TC-10 to TC-14)."""
import pytest

from lib.api_cost_tracker import PRICING, calculate_cost, check_budget


def test_calculate_cost_anthropic_all_token_types():
    """TC-10: calculate_cost for Anthropic with all token types -> matches manual calculation."""
    # 1000 input, 500 output, 300000 cache_read, 300000 cache_write
    cost = calculate_cost(
        "claude-opus-4-6",
        input_tokens=1000,
        output_tokens=500,
        cache_read_tokens=300000,
        cache_write_tokens=300000,
    )
    # Manual: (1000/1M)*15 + (500/1M)*75 + (300000/1M)*1.50 + (300000/1M)*30.00
    expected = (1000 / 1e6) * 15.00 + (500 / 1e6) * 75.00 + (300000 / 1e6) * 1.50 + (300000 / 1e6) * 30.00
    assert abs(cost - expected) < 0.0001


def test_calculate_cost_openai():
    """TC-11: calculate_cost for OpenAI -> matches manual calculation."""
    cost = calculate_cost("gpt-5-mini", input_tokens=500, output_tokens=100)
    # Manual: (500/1M)*0.25 + (100/1M)*2.00
    expected = (500 / 1e6) * 0.25 + (100 / 1e6) * 2.00
    assert abs(cost - expected) < 0.0001


def test_check_budget_warning_at_80_percent():
    """TC-12: check_budget at 80% -> returns (False, 'warning: ...')."""
    state = {"cost": {"total": 80.0}}
    config = {"budget": {"max_total_usd": 100.0, "warn_at_percent": 80}}
    halt, msg = check_budget(state, config)
    assert halt is False
    assert "warning" in msg
    assert "80%" in msg


def test_check_budget_halt_at_100_percent():
    """TC-13: check_budget at 100% -> returns (True, 'halt: ...')."""
    state = {"cost": {"total": 100.0}}
    config = {"budget": {"max_total_usd": 100.0, "warn_at_percent": 80}}
    halt, msg = check_budget(state, config)
    assert halt is True
    assert "halt" in msg


def test_calculate_cost_unknown_model():
    """TC-14: calculate_cost with unknown model -> raises KeyError."""
    with pytest.raises(KeyError, match="Unknown model"):
        calculate_cost("nonexistent-model", input_tokens=100, output_tokens=50)
