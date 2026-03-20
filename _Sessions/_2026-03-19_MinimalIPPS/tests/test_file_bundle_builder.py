"""Tests for lib/file_bundle_builder.py (TC-01 to TC-05)."""
import pytest

from lib.file_bundle_builder import (
    EmptySourceError,
    count_tokens,
    generate_bundle,
    scan_source_dir,
)


def test_scan_mixed_files(mock_source_dir):
    """TC-01: Scan source dir with mixed files -> returns categorized dict, .md files only."""
    categories = scan_source_dir(mock_source_dir)
    all_files = [f for files in categories.values() for f in files]

    # Only .md files should be included
    assert all(f.suffix == ".md" for f in all_files)
    # .py, .json, .png should be excluded
    extensions = {f.suffix for f in all_files}
    assert ".py" not in extensions
    assert ".json" not in extensions
    assert ".png" not in extensions
    # Should have 3 .md files: core.md, build.md, SKILL.md
    assert len(all_files) == 3


def test_scan_empty_directory(tmp_path):
    """TC-02: Scan empty directory -> raises EmptySourceError with directory path."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    with pytest.raises(EmptySourceError, match=str(empty_dir).replace("\\", "\\\\")):
        scan_source_dir(empty_dir)


def test_scan_skip_patterns(mock_source_dir):
    """TC-03: Skip files matching skip_patterns -> matched files absent from result."""
    categories = scan_source_dir(
        mock_source_dir,
        skip_patterns=["workflows/*"],
    )
    all_files = [f for files in categories.values() for f in files]
    all_names = [f.name for f in all_files]

    assert "build.md" not in all_names
    assert "core.md" in all_names


def test_generate_bundle_with_headers(mock_source_dir):
    """TC-04: Generate bundle with headers -> each file prefixed with ## [path], metadata line."""
    categories = scan_source_dir(mock_source_dir)
    result = generate_bundle(categories, mock_source_dir)

    content = result["content"]
    assert "## [rules/core.md]" in content
    assert "## [workflows/build.md]" in content
    assert "<!-- lines:" in content
    assert result["file_count"] == 3
    assert result["token_count"] > 0


def test_token_count_estimation():
    """TC-05: Token count estimation -> result within 10% of tiktoken cl100k_base encoding."""
    import tiktoken

    text = "# Core Rules\n" * 100
    enc = tiktoken.get_encoding("cl100k_base")
    expected = len(enc.encode(text))

    actual = count_tokens(text)

    # Must be within 10% (in practice should be exact since we use same encoding)
    assert abs(actual - expected) / max(expected, 1) < 0.10
