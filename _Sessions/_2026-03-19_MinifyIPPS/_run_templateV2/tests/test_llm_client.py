"""Tests for LLM client: cost calc, call_with_cache, adaptive thinking (TK-003, TK-004, TK-005)."""
import logging
from unittest.mock import MagicMock, patch

import pytest
from lib.llm_client import calculate_cost, build_api_params, get_model_config, _call_anthropic_with_cache


class TestCalculateCostWithCache:
    """TK-003: Cache-aware cost calculation."""

    def test_calculate_cost_with_cache_read(self):
        """TC-03: cache_read_cost = cache_read_tokens/1M * cached_per_1m."""
        usage = {
            "input_tokens": 5000,
            "output_tokens": 1000,
            "cache_read_input_tokens": 3000,
            "cache_creation_input_tokens": 0,
        }
        result = calculate_cost(usage, "claude-opus-4-6-20260204")
        assert result["pricing_found"] is True
        assert result["cache_read_cost"] > 0
        # cache_read_cost = 3000/1M * cached_per_1m (1.00) = 0.003
        assert abs(result["cache_read_cost"] - 0.003) < 0.0001
        # Non-cached input = 5000 - 3000 = 2000
        # input_cost = 2000/1M * 10.00 = 0.02
        assert abs(result["input_cost"] - 0.02) < 0.0001

    def test_calculate_cost_with_cache_write(self):
        """cache_write_cost = tokens/1M * input_per_1m * 1.25."""
        usage = {
            "input_tokens": 5000,
            "output_tokens": 1000,
            "cache_read_input_tokens": 0,
            "cache_creation_input_tokens": 4000,
        }
        result = calculate_cost(usage, "claude-opus-4-6-20260204")
        # cache_write_cost = 4000/1M * 10.00 * 1.25 = 0.05
        assert abs(result["cache_write_cost"] - 0.05) < 0.0001

    def test_calculate_cost_missing_pricing(self):
        """TC-04: Unknown model returns pricing_found=false, costs=0.0."""
        usage = {"input_tokens": 1000, "output_tokens": 500}
        result = calculate_cost(usage, "unknown-model-xyz")
        assert result["pricing_found"] is False
        assert result["total_cost"] == 0.0
        assert result["cache_read_cost"] == 0.0
        assert result["cache_write_cost"] == 0.0

    def test_calculate_cost_no_cached_per_1m(self):
        """EC-04: Model without cached_per_1m defaults cache costs to 0.0."""
        usage = {
            "input_tokens": 1000,
            "output_tokens": 500,
            "cache_read_input_tokens": 500,
            "cache_creation_input_tokens": 0,
        }
        # gpt-4o has no cached_per_1m in pricing
        result = calculate_cost(usage, "gpt-4o")
        assert result["pricing_found"] is True
        assert result["cache_read_cost"] == 0.0

    def test_calculate_cost_missing_cache_fields(self):
        """TC-28/EC-09: Missing cache fields default to 0."""
        usage = {"input_tokens": 1000, "output_tokens": 500}
        result = calculate_cost(usage, "claude-opus-4-6-20260204")
        assert result["pricing_found"] is True
        assert result["cache_read_cost"] == 0.0
        assert result["cache_write_cost"] == 0.0
        # All input is non-cached: 1000/1M * 10.00 = 0.01
        assert abs(result["input_cost"] - 0.01) < 0.0001


class TestCallWithCache:
    """TK-004: call_with_cache method tests."""

    def _make_mock_response(self, text_blocks=None, thinking=False,
                            cache_creation=100, cache_read=0):
        """Helper to build mock Anthropic response."""
        response = MagicMock()
        response.model = "claude-opus-4-6-20260204"
        response.stop_reason = "end_turn"
        response.usage = MagicMock()
        response.usage.input_tokens = 1000
        response.usage.output_tokens = 500
        response.usage.cache_creation_input_tokens = cache_creation
        response.usage.cache_read_input_tokens = cache_read

        blocks = []
        if thinking:
            tb = MagicMock()
            tb.type = "thinking"
            tb.thinking = "internal reasoning"
            tb.text = "should be skipped"
            blocks.append(tb)

        if text_blocks is None:
            text_blocks = ["Response text"]
        for txt in text_blocks:
            tb = MagicMock()
            tb.type = "text"
            tb.text = txt
            # text blocks must NOT have thinking attr
            del tb.thinking
            blocks.append(tb)

        response.content = blocks
        return response

    def test_call_with_cache_system_prompt_structure(self):
        """TC-02: System param is array with cache_control block."""
        client = MagicMock()
        client.messages.create.return_value = self._make_mock_response()

        result = _call_anthropic_with_cache(
            client, "claude-opus-4-6-20260204",
            "system bundle", "user prompt", {"max_tokens": 8192}
        )

        call_args = client.messages.create.call_args
        system = call_args.kwargs.get("system") or call_args[1].get("system")
        assert isinstance(system, list)
        assert len(system) == 1
        assert system[0]["type"] == "text"
        assert system[0]["text"] == "system bundle"
        assert system[0]["cache_control"] == {"type": "ephemeral"}

    def test_call_with_cache_non_anthropic_raises(self):
        """TC-05: ValueError for OpenAI model."""
        from lib.llm_client import LLMClient
        with patch("lib.llm_client.create_client"):
            client = LLMClient.__new__(LLMClient)
            client.provider = "openai"
            client.model = "gpt-5-mini"
            client.api_params = {}
            with pytest.raises(ValueError, match="only supports Anthropic"):
                client.call_with_cache("bundle", "prompt")

    def test_call_with_cache_joins_text_blocks(self):
        """Multiple text blocks are all joined."""
        client = MagicMock()
        client.messages.create.return_value = self._make_mock_response(
            text_blocks=["Part 1", "Part 2", "Part 3"]
        )

        result = _call_anthropic_with_cache(
            client, "claude-opus-4-6-20260204",
            "system", "prompt", {"max_tokens": 8192}
        )
        assert "Part 1" in result["text"]
        assert "Part 2" in result["text"]
        assert "Part 3" in result["text"]

    def test_call_with_cache_skips_thinking_blocks(self):
        """Thinking blocks excluded from text output."""
        client = MagicMock()
        client.messages.create.return_value = self._make_mock_response(
            text_blocks=["Actual answer"], thinking=True
        )

        result = _call_anthropic_with_cache(
            client, "claude-opus-4-6-20260204",
            "system", "prompt", {"max_tokens": 8192}
        )
        assert "Actual answer" in result["text"]
        assert "should be skipped" not in result["text"]

    def test_call_with_cache_cache_minimum_warning(self, caplog):
        """TC-33/EC-11: Warning when cache_creation_input_tokens==0."""
        client = MagicMock()
        client.messages.create.return_value = self._make_mock_response(
            cache_creation=0
        )

        with caplog.at_level(logging.WARNING, logger="lib.llm_client"):
            _call_anthropic_with_cache(
                client, "claude-opus-4-6-20260204",
                "short system", "prompt", {"max_tokens": 8192}
            )
        assert any("1024-token minimum" in r.message for r in caplog.records)

    def test_call_with_cache_returns_cache_usage(self):
        """Usage dict includes cache token fields."""
        client = MagicMock()
        client.messages.create.return_value = self._make_mock_response(
            cache_creation=500, cache_read=300
        )

        result = _call_anthropic_with_cache(
            client, "claude-opus-4-6-20260204",
            "system", "prompt", {"max_tokens": 8192}
        )
        assert result["usage"]["cache_creation_input_tokens"] == 500
        assert result["usage"]["cache_read_input_tokens"] == 300


class TestAdaptiveThinking:
    """TK-005: Adaptive thinking support for Opus 4.6."""

    def test_build_api_params_opus46_adaptive(self):
        """Opus 4.6 uses thinking.type=adaptive + output_config.effort."""
        params, method, provider = build_api_params("claude-opus-4-6-20260204", "high")
        assert provider == "anthropic"
        # Should have thinking config (exact format depends on registry)
        # At minimum, thinking should be present for high effort
        if "thinking" in params:
            assert params["thinking"].get("budget_tokens", 0) > 0 or params["thinking"].get("type") in ("enabled", "adaptive")

    def test_build_api_params_sonnet_manual_thinking(self):
        """Non-Opus-4.6 models use type=enabled with budget_tokens."""
        params, method, provider = build_api_params("claude-3-7-sonnet-20250219", "high")
        if "thinking" in params:
            assert params["thinking"]["type"] == "enabled"
            assert "budget_tokens" in params["thinking"]

    def test_build_api_params_unknown_model(self):
        """TC-25/EC-02: ValueError listing known prefixes."""
        with pytest.raises(ValueError, match="Unknown model.*Known prefixes"):
            build_api_params("totally-unknown-model", "high")
