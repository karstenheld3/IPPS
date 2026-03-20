"""Tests for lib/file_compressor.py (TC-15 to TC-20 from IMPL)."""
from pathlib import Path
from unittest.mock import Mock

import pytest

from lib.file_compressor import compress_file, run_compression_step, _parse_score


@pytest.fixture
def base_config():
    return {
        "thresholds": {
            "judge_min_score": 3.5,
            "max_refinement_attempts": 1,
            "exclusion_max_lines": 100,
            "exclusion_max_references": 2,
            "target_compression_percent": 40,
            "max_manual_review_files": 5,
        },
        "budget": {"max_total_usd": 100.0, "warn_at_percent": 80},
        "file_type_map": {"*": "compress_other"},
        "skip_patterns": [],
    }


def _mock_mother(compressed_text="# Compressed\nShort content."):
    """Mock AnthropicClient returning compressed text."""
    client = Mock()
    client.call_with_cache.return_value = (
        compressed_text,
        {"input_tokens": 1000, "output_tokens": 200,
         "cache_creation_input_tokens": 0, "cache_read_input_tokens": 300000},
    )
    return client


def _mock_verifier(score=4.0):
    """Mock OpenAIClient returning judge score."""
    client = Mock()
    client.call.return_value = (
        f"Score: {score}/5\nGood compression quality.",
        {"prompt_tokens": 500, "completion_tokens": 100},
    )
    return client


class TestCompressFile:
    """Tests for compress_file function."""

    def test_score_above_threshold_accepts(self, base_config):
        """TC-15: score >= 3.5 -> status='accepted', saved to output."""
        original = "# Rules\n" * 50  # ~100 tokens
        mother = _mock_mother("# Rules\nCompressed.")  # much shorter
        verifier = _mock_verifier(4.0)

        result = compress_file(
            mother, verifier, Path("rules/core.md"), original,
            "bundle", "transform {file_path} {file_content} {file_type}",
            "eval prompt", base_config,
        )

        assert result["status"] == "accepted"
        assert result["score"] == 4.0
        assert result["compressed_tokens"] < result["original_tokens"]

    def test_score_below_threshold_refine_succeeds(self, base_config):
        """TC-16: score < 3.5, refine succeeds -> status='refined'."""
        original = "# Rules\n" * 50
        mother = Mock()
        # First attempt: bad compression, second attempt: good
        mother.call_with_cache.side_effect = [
            ("Bad compress", {"input_tokens": 1000, "output_tokens": 200,
             "cache_creation_input_tokens": 0, "cache_read_input_tokens": 300000}),
            ("# Better\nGood.", {"input_tokens": 1000, "output_tokens": 200,
             "cache_creation_input_tokens": 0, "cache_read_input_tokens": 300000}),
        ]
        verifier = Mock()
        verifier.call.side_effect = [
            ("Score: 2.0/5\nToo much removed.", {"prompt_tokens": 500, "completion_tokens": 100}),
            ("Score: 4.0/5\nGood now.", {"prompt_tokens": 500, "completion_tokens": 100}),
        ]

        result = compress_file(
            mother, verifier, Path("rules/core.md"), original,
            "bundle", "transform {file_path} {file_content} {file_type}",
            "eval prompt", base_config,
        )

        assert result["status"] == "refined"
        assert result["score"] == 4.0

    def test_refine_fails_manual_review(self, base_config):
        """TC-17: refine fails -> status='manual_review'."""
        original = "# Rules\n" * 50
        mother = Mock()
        mother.call_with_cache.side_effect = [
            ("Bad", {"input_tokens": 1000, "output_tokens": 200,
             "cache_creation_input_tokens": 0, "cache_read_input_tokens": 300000}),
            ("Still bad", {"input_tokens": 1000, "output_tokens": 200,
             "cache_creation_input_tokens": 0, "cache_read_input_tokens": 300000}),
        ]
        verifier = Mock()
        verifier.call.side_effect = [
            ("Score: 2.0/5\nBad.", {"prompt_tokens": 500, "completion_tokens": 100}),
            ("Score: 2.5/5\nStill bad.", {"prompt_tokens": 500, "completion_tokens": 100}),
        ]

        result = compress_file(
            mother, verifier, Path("rules/core.md"), original,
            "bundle", "transform {file_path} {file_content} {file_type}",
            "eval prompt", base_config,
        )

        assert result["status"] == "manual_review"
        assert result["score"] < 3.5

    def test_token_increase_flagged(self, base_config):
        """TC-19: compression increases tokens -> status='token_increase'."""
        original = "Short."
        # Compressed is longer than original
        mother = _mock_mother("# This is a much longer compressed version with many more words than the original")

        result = compress_file(
            mother, Mock(), Path("rules/core.md"), original,
            "bundle", "transform {file_path} {file_content} {file_type}",
            "eval prompt", base_config,
        )

        assert result["status"] == "token_increase"
        assert result["compressed_tokens"] >= result["original_tokens"]


class TestRunCompressionStep:
    """Tests for run_compression_step function."""

    def test_resume_skips_completed(self, tmp_path, base_config):
        """TC-18: resume from files_completed -> skips already completed files."""
        source = tmp_path / "source"
        output = tmp_path / "output"
        (source / "rules").mkdir(parents=True)
        (source / "rules" / "core.md").write_text("# Core\n" * 50, encoding="utf-8")
        (source / "rules" / "extra.md").write_text("# Extra\n" * 50, encoding="utf-8")

        state = {
            "current_step": 6,
            "files_completed": ["rules/core.md"],  # Already done
            "files_compressed": 1,
            "files_passed": 1,
            "files_failed": 0,
            "cost": {"total": 0.0, "mother_input": 0.0, "mother_output": 0.0,
                     "verification_input": 0.0, "verification_output": 0.0},
        }

        mother = _mock_mother("# Compressed\nShort.")
        verifier = _mock_verifier(4.0)
        prompts = {"compress_other": {"transform": "t {file_path} {file_content} {file_type}", "eval": "e"}}

        result = run_compression_step(
            mother, verifier, "bundle", source, output,
            base_config, state, prompts,
        )

        # Only extra.md should have been compressed (core.md skipped)
        assert "rules/extra.md" in result["files_completed"]
        # Mother should have been called once (for extra.md only)
        assert mother.call_with_cache.call_count == 1

    def test_budget_exceeded_halts(self, tmp_path, base_config):
        """TC-20: budget exceeded -> halts compression loop."""
        source = tmp_path / "source"
        output = tmp_path / "output"
        (source / "rules").mkdir(parents=True)
        (source / "rules" / "a.md").write_text("# A\n" * 50, encoding="utf-8")
        (source / "rules" / "b.md").write_text("# B\n" * 50, encoding="utf-8")

        state = {
            "current_step": 6,
            "files_completed": [],
            "files_compressed": 0,
            "files_passed": 0,
            "files_failed": 0,
            "cost": {"total": 100.0, "mother_input": 50.0, "mother_output": 50.0,
                     "verification_input": 0.0, "verification_output": 0.0},
        }

        mother = _mock_mother("# Compressed\nShort.")
        verifier = _mock_verifier(4.0)
        prompts = {"compress_other": {"transform": "t {file_path} {file_content} {file_type}", "eval": "e"}}

        result = run_compression_step(
            mother, verifier, "bundle", source, output,
            base_config, state, prompts,
        )

        # No files should have been compressed since budget is at 100%
        assert mother.call_with_cache.call_count == 0


class TestParseScore:
    """Tests for score parsing edge cases."""

    def test_valid_score(self):
        assert _parse_score("Score: 4.2/5\nGood.") == 4.2

    def test_invalid_score_returns_1(self):
        """EC-14: score outside 1-5 range treated as 1.0."""
        assert _parse_score("Score: 7.0/5\nGreat.") == 1.0

    def test_no_score_returns_1(self):
        """EC-14: unparseable response treated as 1.0."""
        assert _parse_score("This has no score.") == 1.0
