"""Tests for lib/llm_clients.py (TC-10 to TC-14 from IMPL, mocked SDK)."""
from unittest.mock import Mock, patch, PropertyMock

import anthropic
import openai
import pytest

from lib.llm_clients import AnthropicClient, OpenAIClient, APIError


@pytest.fixture
def anthropic_config():
    return {
        "models": {
            "mother": {
                "provider": "anthropic",
                "model": "claude-opus-4-6",
                "max_context": 1000000,
                "thinking": False,
            },
            "verification": {
                "provider": "openai",
                "model": "gpt-5-mini",
                "max_context": 128000,
            },
        },
        "api_timeout_seconds": 10,
    }


@pytest.fixture
def openai_config():
    return {
        "models": {
            "mother": {
                "provider": "anthropic",
                "model": "claude-opus-4-6",
                "max_context": 1000000,
                "thinking": False,
            },
            "verification": {
                "provider": "openai",
                "model": "gpt-5-mini",
                "max_context": 128000,
            },
        },
        "api_timeout_seconds": 10,
    }


def _make_anthropic_response(text="response text", cache_hit=False):
    """Create mock Anthropic messages.create() response."""
    resp = Mock()
    block = Mock()
    block.text = text
    block.type = "text"
    resp.content = [block]
    resp.usage = Mock(
        input_tokens=100 if cache_hit else 1000,
        output_tokens=500,
        cache_creation_input_tokens=0 if cache_hit else 300000,
        cache_read_input_tokens=300000 if cache_hit else 0,
    )
    resp.model = "claude-opus-4-6"
    return resp


def _make_openai_response(text="Score: 4.0/5\nGood compression."):
    """Create mock OpenAI chat.completions.create() response."""
    resp = Mock()
    resp.choices = [Mock(message=Mock(content=text))]
    resp.usage = Mock(prompt_tokens=500, completion_tokens=100)
    resp._request_id = "req_test_12345"
    resp.model = "gpt-5-mini"
    return resp


class TestAnthropicClient:
    """Tests for AnthropicClient."""

    @patch("lib.llm_clients.anthropic.Anthropic")
    def test_cache_hit(self, mock_cls, anthropic_config):
        """IMPL TC-10: Anthropic call_with_cache returns cache hit -> usage includes cache_read > 0."""
        mock_instance = Mock()
        mock_cls.return_value = mock_instance
        mock_instance.messages.create.return_value = _make_anthropic_response(
            "call tree output", cache_hit=True
        )

        client = AnthropicClient(anthropic_config)
        text, usage = client.call_with_cache("bundle content", "analyze this")

        assert text == "call tree output"
        assert usage["cache_read_input_tokens"] > 0
        assert usage["cache_creation_input_tokens"] == 0

    @patch("lib.llm_clients.time.sleep")
    @patch("lib.llm_clients.anthropic.Anthropic")
    def test_timeout_retry_succeeds(self, mock_cls, mock_sleep, anthropic_config):
        """IMPL TC-11: Anthropic timeout -> retries 3x with backoff, succeeds on 3rd attempt."""
        mock_instance = Mock()
        mock_cls.return_value = mock_instance
        mock_instance.messages.create.side_effect = [
            anthropic.APITimeoutError(request=Mock()),
            anthropic.APITimeoutError(request=Mock()),
            _make_anthropic_response("success after retry"),
        ]

        client = AnthropicClient(anthropic_config)
        text, usage = client.call_with_cache("bundle", "prompt")

        assert text == "success after retry"
        assert mock_sleep.call_count == 2
        assert mock_instance.messages.create.call_count == 3

    @patch("lib.llm_clients.time.sleep")
    @patch("lib.llm_clients.anthropic.Anthropic")
    def test_rate_limit_retry(self, mock_cls, mock_sleep, anthropic_config):
        """IMPL TC-12: Anthropic rate limit (429) -> waits and retries per Retry-After."""
        mock_instance = Mock()
        mock_cls.return_value = mock_instance

        rate_limit_resp = Mock()
        rate_limit_resp.headers = {"retry-after": "2"}
        rate_limit_resp.status_code = 429
        rate_limit_exc = anthropic.RateLimitError(
            message="rate limited",
            response=rate_limit_resp,
            body=None,
        )

        mock_instance.messages.create.side_effect = [
            rate_limit_exc,
            _make_anthropic_response("after rate limit"),
        ]

        client = AnthropicClient(anthropic_config)
        text, usage = client.call_with_cache("bundle", "prompt")

        assert text == "after rate limit"
        mock_sleep.assert_called_once_with(2.0)


class TestOpenAIClient:
    """Tests for OpenAIClient."""

    @patch("lib.llm_clients.openai.OpenAI")
    def test_call_success(self, mock_cls, openai_config):
        """IMPL TC-13: OpenAI call success -> returns response text and usage dict."""
        mock_instance = Mock()
        mock_cls.return_value = mock_instance
        mock_instance.chat.completions.create.return_value = _make_openai_response()

        client = OpenAIClient(openai_config)
        text, usage = client.call("evaluate this file")

        assert "Score: 4.0/5" in text
        assert usage["prompt_tokens"] == 500
        assert usage["completion_tokens"] == 100

    @patch("lib.llm_clients.time.sleep")
    @patch("lib.llm_clients.openai.OpenAI")
    def test_api_failure_after_retries(self, mock_cls, mock_sleep, openai_config):
        """IMPL TC-14: API failure after 3 retries -> raises APIError with retry count."""
        mock_instance = Mock()
        mock_cls.return_value = mock_instance

        timeout_exc = openai.APITimeoutError(request=Mock())
        mock_instance.chat.completions.create.side_effect = [
            timeout_exc,
            timeout_exc,
            timeout_exc,
        ]

        client = OpenAIClient(openai_config)
        with pytest.raises(APIError) as exc_info:
            client.call("test prompt")

        assert exc_info.value.retries == 3
        assert mock_sleep.call_count == 3
