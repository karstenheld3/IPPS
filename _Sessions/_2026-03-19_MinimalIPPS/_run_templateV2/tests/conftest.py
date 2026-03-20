"""Shared test fixtures for MinimalIPPS V2 tests."""
import json
import shutil
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Project root = _run_templateV2/
PROJECT_ROOT = Path(__file__).parent.parent
CONFIGS_DIR = PROJECT_ROOT / "configs"


@pytest.fixture
def tmp_run_dir(tmp_path):
    """Create temp run folder with standard subdirs, cleaned up after test."""
    run_dir = tmp_path / "runs" / "20260320-1430-test"
    for subdir in [
        "analysis", "context", "prompts/step", "prompts/transform",
        "prompts/eval", "verification", "output",
    ]:
        (run_dir / subdir).mkdir(parents=True, exist_ok=True)
    return run_dir


@pytest.fixture
def mock_anthropic_client():
    """Patched Anthropic client returning configurable mock responses."""
    client = MagicMock()
    response = MagicMock()
    response.model = "claude-opus-4-6-20260204"
    response.stop_reason = "end_turn"

    # Default: single text block
    text_block = MagicMock()
    text_block.type = "text"
    text_block.text = "Mock response text"
    del text_block.thinking  # text blocks don't have thinking attr
    response.content = [text_block]

    response.usage = MagicMock()
    response.usage.input_tokens = 1000
    response.usage.output_tokens = 500
    response.usage.cache_creation_input_tokens = 0
    response.usage.cache_read_input_tokens = 0

    client.messages.create.return_value = response
    return client


@pytest.fixture
def mock_openai_client():
    """Patched OpenAI client returning configurable mock responses."""
    client = MagicMock()
    response = MagicMock()
    response.model = "gpt-5-mini"

    choice = MagicMock()
    choice.message.content = "Mock response text"
    choice.finish_reason = "stop"
    response.choices = [choice]

    response.usage = MagicMock()
    response.usage.prompt_tokens = 1000
    response.usage.completion_tokens = 500
    client.chat.completions.create.return_value = response
    return client


@pytest.fixture
def sample_config():
    """Valid V2 pipeline_config dict."""
    return {
        "source_dir": ".windsurf/",
        "models": {
            "mother": "claude-opus-4-6-20260204",
            "verifier": "gpt-5-mini",
        },
        "reasoning_effort": "high",
        "output_length": "high",
        "thresholds": {
            "judge_min_score": 3.5,
            "max_refinement_attempts": 1,
            "exclusion_max_lines": 100,
            "exclusion_max_references": 2,
            "target_compression_percent": 40,
            "max_manual_review_files": 5,
        },
        "budget": {
            "max_total_usd": 100.0,
            "warning_threshold": 0.8,
        },
        "file_type_map": {
            "rules/*.md": "compress_rules",
            "*": "compress_other",
        },
        "include_patterns": ["*.md"],
        "skip_patterns": ["__pycache__/*"],
        "never_compress": [],
        "api_timeout_seconds": 600,
    }


@pytest.fixture
def sample_usage():
    """Anthropic usage dict with cache fields."""
    return {
        "input_tokens": 5000,
        "output_tokens": 2000,
        "cache_creation_input_tokens": 3000,
        "cache_read_input_tokens": 1500,
    }


@pytest.fixture
def sample_pricing():
    """Model-pricing.json dict with standard rates."""
    return {
        "_pricing_tier": "standard",
        "pricing": {
            "anthropic": {
                "claude-opus-4-6-20260204": {
                    "input_per_1m": 10.00,
                    "cached_per_1m": 1.00,
                    "output_per_1m": 50.00,
                    "context_window_k": 200,
                    "currency": "USD",
                },
            },
            "openai": {
                "gpt-5-mini": {
                    "input_per_1m": 0.25,
                    "cached_per_1m": 0.025,
                    "output_per_1m": 2.00,
                    "context_window_k": 256,
                    "currency": "USD",
                },
            },
        },
    }
