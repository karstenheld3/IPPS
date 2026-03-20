"""Tests for lib/compression_report_builder.py (TC-21 to TC-24 from IMPL)."""
from unittest.mock import Mock

from lib.compression_report_builder import (
    check_cross_references,
    generate_report,
    verify_file,
)


def _mock_verifier(response_text):
    """Create mock OpenAIClient returning given text."""
    client = Mock()
    client.call.return_value = (
        response_text,
        {"prompt_tokens": 500, "completion_tokens": 200},
    )
    return client


def test_verify_file_produces_5_line_report():
    """TC-21: verify_file produces exactly 5-line report -> format matches SPEC."""
    verifier = _mock_verifier(
        "1. **Structural changes**: Flattened 3 sections\n"
        "2. **Removed features**: Dropped examples\n"
        "3. **Simplified content**: Merged duplicate rules\n"
        "4. **Sacrificed details**: Removed BAD/GOOD pairs\n"
        "5. **Possible impact**: Agent may miss edge cases\n"
    )
    result = verify_file(
        verifier,
        original="# Original\n" * 50,
        compressed="# Compressed\nShort.",
        prompt="Compare {file_path}: {original_content} vs {compressed_content}",
        file_path="rules/core.md",
    )

    assert result["file_path"] == "rules/core.md"
    assert len(result["report_lines"]) == 5
    assert "Flattened" in result["report_lines"][0]
    assert result["broken_refs"] == []


def test_check_cross_references_finds_broken_ref():
    """TC-22: check_cross_references finds broken ref -> broken list non-empty."""
    compressed_files = {
        "rules/core.md": "See also rules/nonexistent.md for details.",
        "workflows/build.md": "Uses rules/core.md as base.",
    }
    excluded_files = []

    broken = check_cross_references(compressed_files, excluded_files)

    assert len(broken) >= 1
    assert any("nonexistent.md" in b for b in broken)


def test_check_cross_references_all_resolve():
    """TC-23: all references resolve -> broken_references = 0."""
    compressed_files = {
        "rules/core.md": "See also workflows/build.md for details.",
        "workflows/build.md": "Uses rules/core.md as base.",
    }
    excluded_files = []

    broken = check_cross_references(compressed_files, excluded_files)

    assert len(broken) == 0


def test_generate_report_includes_summary():
    """TC-24: generate_report includes summary -> contains pass rate, broken refs count."""
    results = [
        {
            "file_path": "rules/core.md",
            "report_lines": [
                "Flattened sections",
                "Dropped examples",
                "Merged rules",
                "Removed pairs",
                "Edge cases missed",
            ],
            "broken_refs": [],
        },
        {
            "file_path": "workflows/build.md",
            "report_lines": [
                "Reordered steps",
                "None",
                "Shortened descriptions",
                "Removed verbose notes",
                "Minor behavior change",
            ],
            "broken_refs": ["BROKEN_REF: 'nonexistent.md' in workflows/build.md"],
        },
    ]
    cross_ref_issues = []

    content = generate_report(results, cross_ref_issues)

    assert "Pass rate" in content
    assert "50%" in content  # 1 of 2 passed (one has broken refs)
    assert "Broken references" in content
    assert "rules/core.md" in content
    assert "workflows/build.md" in content
