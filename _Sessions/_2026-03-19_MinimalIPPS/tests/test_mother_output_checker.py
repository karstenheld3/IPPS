"""Tests for lib/mother_output_checker.py (TC-25, TC-26)."""
from unittest.mock import Mock

from lib.mother_output_checker import report_issues, spot_check_document


def _mock_openai_client(responses=None):
    """Create mock OpenAIClient with configurable responses."""
    client = Mock()
    if responses is None:
        responses = [("ACCURATE", {"prompt_tokens": 100, "completion_tokens": 50})]
    client.call.side_effect = responses
    return client


def test_spot_check_samples_correct_count():
    """TC-25: spot_check_document samples correct count -> calls OpenAI exactly sample_size times."""
    # Create 20 source files so we can sample 15
    source_files = [
        (f"file_{i}.md", f"# Content {i}\nSome text here.")
        for i in range(20)
    ]
    responses = [
        ("ACCURATE - claims are correct", {"prompt_tokens": 100, "completion_tokens": 50})
        for _ in range(15)
    ]
    client = _mock_openai_client(responses)

    result = spot_check_document(
        client,
        document="# Analysis\nAll files are well structured.",
        source_files=source_files,
        sample_size=15,
    )

    assert client.call.call_count == 15
    assert result["checked_count"] == 15
    assert isinstance(result["issues"], list)


def test_report_issues_formats_findings():
    """TC-26: report_issues formats findings -> output contains file path, claim, and verification."""
    issues = [
        {
            "file": "rules/core.md",
            "claim": "See analysis document",
            "verification": "Line count reported as 50 but actual is 75.",
        },
        {
            "file": "workflows/build.md",
            "claim": "See analysis document",
            "verification": "Missing reference to skills/coding/SKILL.md.",
        },
    ]

    output = report_issues(issues)

    assert "rules/core.md" in output
    assert "workflows/build.md" in output
    assert "Line count reported as 50" in output
    assert "Missing reference" in output
    assert "2 found" in output


def test_report_issues_no_issues():
    """Verify empty issues list returns clean message."""
    output = report_issues([])
    assert "No issues found" in output
