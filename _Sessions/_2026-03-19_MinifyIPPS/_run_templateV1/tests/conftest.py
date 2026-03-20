"""Shared fixtures and helpers for MinifyIPPS tests."""
import json
from pathlib import Path
from unittest.mock import Mock

import pytest


@pytest.fixture
def sample_config(tmp_path):
    """Valid pipeline_config.json dict matching SPEC section 9."""
    config = {
        "source_dir": str(tmp_path / "source"),
        "output_dir": str(tmp_path / "output"),
        "models": {
            "mother": {
                "provider": "anthropic",
                "model": "claude-opus-4-6",
                "max_context": 1000000,
                "thinking": True,
            },
            "verification": {
                "provider": "openai",
                "model": "gpt-5-mini",
                "max_context": 128000,
            },
        },
        "thresholds": {
            "judge_min_score": 3.5,
            "max_refinement_attempts": 1,
            "exclusion_max_lines": 100,
            "exclusion_max_references": 2,
            "target_compression_percent": 40,
            "max_manual_review_files": 5,
        },
        "cache": {"ttl": "1h"},
        "budget": {"max_total_usd": 100.0, "warn_at_percent": 80},
        "file_type_map": {"rules/*.md": "compress_rules", "*": "compress_other"},
        "include_patterns": ["*.md"],
        "skip_patterns": ["pricing-sources/*"],
        "never_compress": ["skills/llm-evaluation/prompts/*"],
        "api_timeout_seconds": 120,
    }
    return config


@pytest.fixture
def sample_state():
    """Valid pipeline_state.json dict with realistic field values."""
    return create_sample_state()


@pytest.fixture
def corrupted_state_file(tmp_path):
    """File with invalid JSON content for EC-08 testing."""
    state_path = tmp_path / "pipeline_state.json"
    state_path.write_text("{invalid json content!!!}", encoding="utf-8")
    return state_path


@pytest.fixture
def mock_source_dir(tmp_path):
    """tmp_path with mixed files (.md, .py, .json, binary)."""
    source = tmp_path / "source"
    (source / "rules").mkdir(parents=True)
    (source / "workflows").mkdir()
    (source / "skills" / "coding").mkdir(parents=True)
    # .md files (compressible)
    (source / "rules" / "core.md").write_text("# Core Rules\n" * 50, encoding="utf-8")
    (source / "workflows" / "build.md").write_text(
        "# Build\n" * 30, encoding="utf-8"
    )
    (source / "skills" / "coding" / "SKILL.md").write_text(
        "# Skill\n" * 10, encoding="utf-8"
    )
    # Non-.md files (excluded from output)
    (source / "skills" / "coding" / "script.py").write_text(
        "print('hello')", encoding="utf-8"
    )
    (source / "skills" / "coding" / "config.json").write_text(
        "{}", encoding="utf-8"
    )
    # Binary file
    (source / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    return source


@pytest.fixture
def mock_source_dir_with_prompts(mock_source_dir):
    """Extends mock_source_dir with a never-compress prompt file."""
    prompts_dir = mock_source_dir / "skills" / "llm-eval" / "prompts"
    prompts_dir.mkdir(parents=True)
    (prompts_dir / "score.md").write_text(
        "# Eval Prompt\nScore 1-5.\n", encoding="utf-8"
    )
    return mock_source_dir


@pytest.fixture
def sample_bundle():
    """Concatenated .md content with ## [path] headers."""
    return (
        "## [rules/core.md]\n"
        "# Core Rules\n" * 10
        + "\n## [workflows/build.md]\n"
        + "# Build\n" * 5
    )


@pytest.fixture
def mock_strategy():
    """Sample _03_FILE_COMPRESSION_STRATEGY.md content."""
    return (
        "# Compression Strategy\n\n"
        "## Primary (keep mostly as-is)\n"
        "- rules/core.md\n\n"
        "## Secondary (compress)\n"
        "- workflows/build.md\n\n"
        "## Drop (remove entirely)\n"
        "- skills/coding/SKILL.md\n"
    )


@pytest.fixture
def mock_report():
    """Sample _04_FILE_COMPRESSION_REPORT.md content."""
    return (
        "# Compression Report\n\n"
        "## Summary\n"
        "- Pass rate: 85%\n"
        "- Compression ratio: 45%\n"
        "- Broken references: 0\n\n"
        "### [rules/core.md]\n"
        "1. **Structural changes**: Flattened 3 sections into 1\n"
        "2. **Removed features**: None\n"
        "3. **Simplified content**: Merged duplicate rules\n"
        "4. **Sacrificed details**: Removed BAD/GOOD examples\n"
        "5. **Possible impact**: Agent may miss formatting nuances\n"
    )


def create_mock_anthropic_response(content: str, cache_hit: bool = False) -> Mock:
    """Create mock Anthropic messages.create() response.

    Args:
        content: Text content of response
        cache_hit: If True, usage shows cache_read_input_tokens > 0
    """
    response = Mock()
    response.content = [Mock(text=content)]
    response.usage = Mock(
        input_tokens=1000 if not cache_hit else 100,
        output_tokens=500,
        cache_creation_input_tokens=300000 if not cache_hit else 0,
        cache_read_input_tokens=300000 if cache_hit else 0,
    )
    response.model = "claude-opus-4-6"
    return response


def create_mock_openai_response(content: str, score: float = 4.0) -> Mock:
    """Create mock OpenAI chat.completions.create() response.

    Args:
        content: Text content of response (or use score to auto-generate judge response)
        score: Judge score to embed in content if content not provided
    """
    response = Mock()
    response.choices = [
        Mock(
            message=Mock(
                content=content or f"Score: {score}/5\nGood compression."
            )
        )
    ]
    response.usage = Mock(prompt_tokens=500, completion_tokens=100)
    response._request_id = "req_test_12345"
    response.model = "gpt-5-mini"
    return response


def create_sample_state(step: int = 0, files_completed: list = None) -> dict:
    """Create valid pipeline_state.json dict."""
    return {
        "current_step": step,
        "iteration": 1,
        "files_total": 10,
        "files_compressible": 8,
        "files_excluded": 2,
        "files_compressed": 0,
        "files_passed": 0,
        "files_failed": 0,
        "files_excluded_md": 2,
        "files_completed": files_completed or [],
        "broken_references": 0,
        "cost": {
            "mother_input": 0.0,
            "mother_output": 0.0,
            "verification_input": 0.0,
            "verification_output": 0.0,
            "total": 0.0,
        },
    }


def assert_file_contains(path, expected_substring: str):
    """Assert file exists and contains expected substring."""
    assert path.exists(), f"File not found: {path}"
    content = path.read_text(encoding="utf-8")
    assert expected_substring in content, (
        f"Expected '{expected_substring}' in {path.name}, "
        f"got first 200 chars: {content[:200]}"
    )
