"""Tests for lib/compression_prompt_builder.py (TC-27 to TC-29)."""
import json
from unittest.mock import Mock

from lib.compression_prompt_builder import (
    generate_compression_prompts,
    save_prompts,
)


def _mock_client(prompts_dict):
    """Create mock AnthropicClient returning JSON prompts."""
    client = Mock()
    client.call_with_cache.return_value = (
        json.dumps(prompts_dict),
        {"input_tokens": 1000, "output_tokens": 500,
         "cache_creation_input_tokens": 0, "cache_read_input_tokens": 300000},
    )
    return client


def test_generate_prompts_per_file_type():
    """TC-27: generates prompts for each file type in config."""
    expected = {
        "compress_rules": {"transform": "compress rules", "eval": "eval rules"},
        "compress_workflows": {"transform": "compress wf", "eval": "eval wf"},
        "compress_other": {"transform": "compress other", "eval": "eval other"},
    }
    client = _mock_client(expected)
    file_types = ["compress_rules", "compress_workflows", "compress_other"]

    result = generate_compression_prompts(
        client, "bundle", "strategy", file_types, "template {file_types_list}"
    )

    assert "compress_rules" in result
    assert "compress_workflows" in result
    assert "compress_other" in result
    assert result["compress_rules"]["transform"] == "compress rules"


def test_save_prompts_to_directories(tmp_path):
    """TC-28: save_prompts writes to transform/ and eval/ directories."""
    prompts = {
        "compress_rules": {"transform": "T-rules", "eval": "E-rules"},
        "compress_other": {"transform": "T-other", "eval": "E-other"},
    }
    transform_dir = tmp_path / "prompts" / "transform"
    eval_dir = tmp_path / "prompts" / "eval"

    save_prompts(prompts, transform_dir, eval_dir)

    assert (transform_dir / "compress_rules.md").read_text(encoding="utf-8") == "T-rules"
    assert (eval_dir / "compress_rules.md").read_text(encoding="utf-8") == "E-rules"
    assert (transform_dir / "compress_other.md").exists()
    assert (eval_dir / "compress_other.md").exists()


def test_generate_prompts_includes_compress_other_fallback():
    """TC-29: result always includes compress_other fallback prompt pair."""
    expected = {
        "compress_rules": {"transform": "t", "eval": "e"},
        "compress_other": {"transform": "fallback t", "eval": "fallback e"},
    }
    client = _mock_client(expected)

    result = generate_compression_prompts(
        client, "bundle", "strategy",
        ["compress_rules", "compress_other"],
        "template {file_types_list}",
    )

    assert "compress_other" in result
    assert result["compress_other"]["transform"] == "fallback t"
