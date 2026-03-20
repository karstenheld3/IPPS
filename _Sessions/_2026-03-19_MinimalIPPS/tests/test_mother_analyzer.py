"""Tests for lib/mother_analyzer.py (TC-20 to TC-24)."""
from unittest.mock import Mock

from lib.mother_analyzer import (
    analyze_call_tree,
    analyze_complexity,
    generate_strategy,
    get_never_compress_files,
    identify_excluded_files,
    parse_load_frequencies,
)


def _mock_client(response_text="mock response"):
    """Create mock AnthropicClient that returns given text."""
    client = Mock()
    client.call_with_cache.return_value = (response_text, {
        "input_tokens": 1000, "output_tokens": 500,
        "cache_creation_input_tokens": 0, "cache_read_input_tokens": 300000,
    })
    return client


def test_analyze_call_tree_writes_file(tmp_path):
    """TC-20: analyze_call_tree writes _01_FILE_CALL_TREE.md -> file exists with content."""
    client = _mock_client("# Call Tree\n\nrules/core.md: 5 references\n")
    result = analyze_call_tree(client, "bundle", "prompt", tmp_path)

    output = tmp_path / "_01_FILE_CALL_TREE.md"
    assert output.exists()
    assert "Call Tree" in output.read_text(encoding="utf-8")
    assert result == "# Call Tree\n\nrules/core.md: 5 references\n"
    client.call_with_cache.assert_called_once()


def test_parse_load_frequencies():
    """TC-21: parse_load_frequencies extracts per-file counts -> returns dict."""
    call_tree = (
        "rules/core.md: 8 references\n"
        "  - triggered by: workflows/build.md, skills/coding/SKILL.md\n"
        "workflows/build.md: 3 references\n"
        "skills/coding/SKILL.md: 1 references\n"
    )
    freqs = parse_load_frequencies(call_tree)

    assert freqs["rules/core.md"] == 8
    assert freqs["workflows/build.md"] == 3
    assert freqs["skills/coding/SKILL.md"] == 1


def test_analyze_complexity_writes_file(tmp_path):
    """TC-22: analyze_complexity writes _02_FILE_COMPLEXITY_MAP.md -> file exists."""
    client = _mock_client("# Complexity Map\n\n## Per-File Analysis\n")
    result = analyze_complexity(client, "bundle", "prompt", tmp_path)

    output = tmp_path / "_02_FILE_COMPLEXITY_MAP.md"
    assert output.exists()
    assert "Complexity Map" in result


def test_identify_excluded_files_both_criteria():
    """TC-23: identify_excluded_files applies both criteria -> files with < 100 lines
    AND <= 2 refs excluded; files meeting only one criterion NOT excluded."""
    complexity_map = (
        "### small_rarely_loaded.md\n"
        "- **Path**: small_rarely_loaded.md\n"
        "- **Lines**: 50\n\n"
        "### large_rarely_loaded.md\n"
        "- **Path**: large_rarely_loaded.md\n"
        "- **Lines**: 200\n\n"
        "### small_often_loaded.md\n"
        "- **Path**: small_often_loaded.md\n"
        "- **Lines**: 50\n"
    )
    load_frequencies = {
        "small_rarely_loaded.md": 1,   # < 100 lines AND <= 2 refs -> EXCLUDE
        "large_rarely_loaded.md": 1,   # >= 100 lines, only one criterion -> KEEP
        "small_often_loaded.md": 5,    # <= 100 lines but > 2 refs -> KEEP
    }
    config = {"thresholds": {"exclusion_max_lines": 100, "exclusion_max_references": 2}}

    excluded = identify_excluded_files(complexity_map, load_frequencies, config)

    assert "small_rarely_loaded.md" in excluded
    assert "large_rarely_loaded.md" not in excluded
    assert "small_often_loaded.md" not in excluded


def test_generate_strategy_excludes_files(tmp_path):
    """TC-24: generate_strategy writes _03_FILE_COMPRESSION_STRATEGY.md ->
    excluded files not in compression scope."""
    strategy_content = "# Strategy\n\n## Primary\n- rules/core.md\n"
    client = _mock_client(strategy_content)
    excluded = ["small_file.md"]

    result = generate_strategy(client, "bundle", "prompt", excluded, tmp_path)

    output = tmp_path / "_03_FILE_COMPRESSION_STRATEGY.md"
    assert output.exists()
    # Verify excluded files were passed in the prompt
    call_args = client.call_with_cache.call_args
    assert "small_file.md" in call_args[0][1]  # prompt argument
    assert "Strategy" in result


def test_get_never_compress_files():
    """get_never_compress_files returns file paths matching never_compress patterns."""
    all_files = [
        "rules/core.md",
        "workflows/build.md",
        "skills/llm-evaluation/prompts/score.md",
        "skills/llm-evaluation/prompts/rubric.md",
        "skills/coding/SKILL.md",
    ]
    patterns = ["skills/llm-evaluation/prompts/*"]

    result = get_never_compress_files(all_files, patterns)

    assert "skills/llm-evaluation/prompts/score.md" in result
    assert "skills/llm-evaluation/prompts/rubric.md" in result
    assert len(result) == 2
    assert "rules/core.md" not in result
