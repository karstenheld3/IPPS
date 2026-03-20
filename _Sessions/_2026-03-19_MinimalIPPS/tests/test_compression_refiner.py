"""Tests for lib/compression_refiner.py."""
from unittest.mock import Mock

import pytest

from lib.compression_refiner import (
    get_files_to_recompress,
    review_report,
    update_strategy,
)


def _mock_client(response_text):
    """Create mock AnthropicClient returning given text."""
    client = Mock()
    client.call_with_cache.return_value = (
        response_text,
        {"input_tokens": 1000, "output_tokens": 500,
         "cache_creation_input_tokens": 0, "cache_read_input_tokens": 300000},
    )
    return client


def test_review_report_produces_updates():
    """review_report sends report to Mother -> returns updates dict and file list."""
    client = _mock_client(
        "## Strategy Updates\n"
        "- rules/core.md: Keep all rule definitions, only compress examples\n"
        "- workflows/build.md: Preserve step ordering\n\n"
        "## Files to Recompress\n"
        "- rules/core.md\n"
        "- workflows/build.md\n"
    )

    result = review_report(client, "bundle", "# Report\nSome issues found.")

    assert "rules/core.md" in result["updates"]
    assert "workflows/build.md" in result["updates"]
    assert "rules/core.md" in result["files_to_recompress"]
    assert len(result["files_to_recompress"]) == 2


def test_update_strategy_modifies_file(tmp_path):
    """update_strategy modifies strategy content -> file updated with guidance."""
    strategy_path = tmp_path / "_03_FILE_COMPRESSION_STRATEGY.md"
    strategy_path.write_text(
        "# Strategy\n\n## Primary\n- rules/core.md\n",
        encoding="utf-8",
    )
    updates = {"rules/core.md": "Keep all rule definitions intact"}

    result = update_strategy(strategy_path, updates)

    assert "Iteration Updates" in result
    assert "Keep all rule definitions" in result
    assert "Strategy" in strategy_path.read_text(encoding="utf-8")


def test_get_files_to_recompress_parses_flagged():
    """get_files_to_recompress parses report -> returns flagged file paths."""
    report = (
        "# Compression Report\n\n"
        "### [rules/core.md]\n"
        "1. **Structural changes**: Flattened\n"
        "2. **Removed features**: None\n"
        "3. **Simplified content**: Merged\n"
        "4. **Sacrificed details**: Examples\n"
        "5. **Possible impact**: Minor\n\n"
        "### [workflows/build.md]\n"
        "1. **Structural changes**: Reordered\n"
        "2. **Removed features**: None\n"
        "3. **Simplified content**: Shortened\n"
        "4. **Sacrificed details**: None\n"
        "5. **Possible impact**: None\n"
        "- BROKEN_REF: 'nonexistent.md' in workflows/build.md -> target not found\n"
    )

    files = get_files_to_recompress(report)

    assert "workflows/build.md" in files
    assert "rules/core.md" not in files  # No issues


def test_get_files_to_recompress_no_report():
    """EC-07: missing report raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError, match="No compression report"):
        get_files_to_recompress("")


def test_update_strategy_missing_file(tmp_path):
    """Strategy file not found -> raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError, match="Strategy file not found"):
        update_strategy(tmp_path / "nonexistent.md", {"a": "b"})
