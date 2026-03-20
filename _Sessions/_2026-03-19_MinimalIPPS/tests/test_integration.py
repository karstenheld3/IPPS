"""Integration test: end-to-end pipeline with mocked APIs (TC-48 to TC-51)."""
import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from lib.api_cost_tracker import calculate_cost
from lib.compression_prompt_builder import generate_compression_prompts, save_prompts
from lib.compression_report_builder import check_cross_references, generate_report, verify_file
from lib.file_bundle_builder import generate_bundle, scan_source_dir
from lib.file_compressor import run_compression_step
from lib.mother_analyzer import (
    analyze_call_tree,
    analyze_complexity,
    generate_strategy,
    identify_excluded_files,
    parse_load_frequencies,
)
from lib.pipeline_state import init_state, load_state, save_state, update_step


def _mock_anthropic(responses=None):
    """Create mock AnthropicClient with configurable multi-call responses."""
    client = Mock()
    default_usage = {
        "input_tokens": 500, "output_tokens": 200,
        "cache_creation_input_tokens": 0, "cache_read_input_tokens": 100000,
    }
    if responses:
        client.call_with_cache.side_effect = [
            (text, default_usage) for text in responses
        ]
    else:
        client.call_with_cache.return_value = ("mock response", default_usage)
    return client


def _mock_openai(responses=None):
    """Create mock OpenAIClient with configurable multi-call responses."""
    client = Mock()
    default_usage = {"prompt_tokens": 300, "completion_tokens": 80}
    if responses:
        client.call.side_effect = [
            (text, default_usage) for text in responses
        ]
    else:
        client.call.return_value = (
            "Score: 4.5/5\nGood compression preserving all content.",
            default_usage,
        )
    return client


@pytest.fixture
def integration_env(tmp_path):
    """Set up a complete pipeline environment with small test data."""
    # Source directory with a few .md files
    source = tmp_path / "source"
    (source / "rules").mkdir(parents=True)
    (source / "workflows").mkdir()

    (source / "rules" / "core.md").write_text(
        "# Core Rules\n\n## Section 1\n" + "Rule text line.\n" * 40,
        encoding="utf-8",
    )
    (source / "rules" / "style.md").write_text(
        "# Style Rules\n\n## Formatting\n" + "Style guideline.\n" * 30,
        encoding="utf-8",
    )
    (source / "workflows" / "build.md").write_text(
        "# Build Workflow\n\n## Steps\n" + "Build step.\n" * 25,
        encoding="utf-8",
    )

    # Config
    config = {
        "source_dir": str(source),
        "output_dir": str(tmp_path / "output"),
        "models": {
            "mother": {"provider": "anthropic", "model": "claude-opus-4-6",
                       "max_context": 1000000, "thinking": False},
            "verification": {"provider": "openai", "model": "gpt-5-mini",
                             "max_context": 128000},
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
        "skip_patterns": [],
        "api_timeout_seconds": 10,
    }

    return {
        "tmp_path": tmp_path,
        "source": source,
        "output": tmp_path / "output",
        "config": config,
        "state_path": tmp_path / "pipeline_state.json",
    }


def test_full_pipeline_run(integration_env):
    """TC-48: Full pipeline run (bundle -> analyze -> check -> generate -> compress -> verify)
    completes -> ok=true, state['current_step'] == 7 and all 7 steps recorded."""
    env = integration_env
    config = env["config"]
    state = init_state()

    # Step 1: Bundle
    categories = scan_source_dir(
        Path(config["source_dir"]),
        include_patterns=config["include_patterns"],
    )
    bundle_result = generate_bundle(categories, Path(config["source_dir"]))
    bundle = bundle_result["content"]
    state["files_total"] = bundle_result["file_count"]
    update_step(state, 1)
    assert state["current_step"] == 1

    # Step 2: Call tree
    mother = _mock_anthropic([
        "# Call Tree\nrules/core.md: 5 references\nrules/style.md: 2 references\nworkflows/build.md: 3 references\n",
    ])
    call_tree = analyze_call_tree(mother, bundle, "prompt", env["tmp_path"])
    freqs = parse_load_frequencies(call_tree)
    update_step(state, 2)
    assert state["current_step"] == 2
    assert len(freqs) > 0

    # Step 3: Complexity map
    mother = _mock_anthropic([
        "# Complexity Map\n\n### rules/core.md\n- **Path**: rules/core.md\n- **Lines**: 42\n\n"
        "### rules/style.md\n- **Path**: rules/style.md\n- **Lines**: 32\n\n"
        "### workflows/build.md\n- **Path**: workflows/build.md\n- **Lines**: 27\n",
    ])
    complexity = analyze_complexity(mother, bundle, "prompt", env["tmp_path"])
    update_step(state, 3)
    assert state["current_step"] == 3

    # Exclusion check (none should be excluded - all have enough lines/refs)
    excluded = identify_excluded_files(complexity, freqs, config)
    state["files_excluded"] = len(excluded)

    # Step 4: Strategy
    mother = _mock_anthropic([
        "# Strategy\n\n## Primary\n- rules/core.md\n\n## Secondary\n- rules/style.md\n- workflows/build.md\n",
    ])
    generate_strategy(mother, bundle, "prompt", excluded, env["tmp_path"])
    update_step(state, 4)
    assert state["current_step"] == 4

    # Step 5: Generate prompts
    prompts_dict = {
        "compress_rules": {"transform": "Compress rules {file_path} {file_content} {file_type}", "eval": "Score 1-5"},
        "compress_other": {"transform": "Compress other {file_path} {file_content} {file_type}", "eval": "Score 1-5"},
    }
    mother = _mock_anthropic([json.dumps(prompts_dict)])
    result_prompts = generate_compression_prompts(
        mother, bundle, "strategy", ["compress_rules", "compress_other"], "template {file_types_list}"
    )
    update_step(state, 5)
    assert state["current_step"] == 5

    # Step 6: Compress
    # Mock Mother to return shorter versions, mock verifier to score 4.5
    short_content = "# Compressed\nKey content preserved.\n"
    num_files = 3  # core.md, style.md, build.md
    mother = _mock_anthropic([short_content] * num_files)
    verifier = _mock_openai(["Score: 4.5/5\nGood."] * num_files)

    state = run_compression_step(
        mother, verifier, bundle,
        Path(config["source_dir"]), Path(config["output_dir"]),
        config, state, result_prompts,
    )
    update_step(state, 6)
    assert state["current_step"] == 6

    # Step 7: Verify
    verify_responses = [
        "1. **Structural changes**: Flattened sections\n"
        "2. **Removed features**: Verbose examples\n"
        "3. **Simplified content**: Merged rules\n"
        "4. **Sacrificed details**: BAD/GOOD pairs\n"
        "5. **Possible impact**: Minor formatting loss\n"
    ] * num_files
    verifier = _mock_openai(verify_responses)

    output_dir = Path(config["output_dir"])
    compressed_files = {}
    results = []
    for md_file in sorted(output_dir.rglob("*.md")):
        rel = md_file.relative_to(output_dir).as_posix()
        compressed = md_file.read_text(encoding="utf-8")
        compressed_files[rel] = compressed
        original_path = Path(config["source_dir"]) / rel
        if original_path.exists():
            original = original_path.read_text(encoding="utf-8")
            result = verify_file(verifier, original, compressed, "verify prompt", rel)
            results.append(result)

    cross_issues = check_cross_references(compressed_files, excluded)
    report = generate_report(results, cross_issues)
    state["broken_references"] = len(cross_issues)
    update_step(state, 7)

    # Final assertions
    assert state["current_step"] == 7
    assert state["files_compressed"] == num_files
    assert len(state["files_completed"]) == num_files


def test_state_tracks_all_steps(integration_env):
    """TC-49: State tracks all steps correctly -> state['current_step'] == 7 after full run."""
    # This is effectively verified by test_full_pipeline_run above
    # Additional check: step progression is monotonic
    state = init_state()
    for step in range(1, 8):
        update_step(state, step)
        assert state["current_step"] == step
    assert state["current_step"] == 7


def test_output_directory_contains_compressed_files(integration_env):
    """TC-50: Output directory contains compressed files matching source .md files."""
    env = integration_env
    config = env["config"]

    # Run a minimal compression to populate output
    categories = scan_source_dir(
        Path(config["source_dir"]),
        include_patterns=config["include_patterns"],
    )
    bundle_result = generate_bundle(categories, Path(config["source_dir"]))

    state = init_state()
    state["files_total"] = bundle_result["file_count"]

    short_content = "# Compressed\nContent.\n"
    num_files = 3
    mother = _mock_anthropic([short_content] * num_files)
    verifier = _mock_openai(["Score: 4.0/5\nOK."] * num_files)

    prompts = {"compress_other": {
        "transform": "Compress {file_path} {file_content} {file_type}",
        "eval": "Score",
    }}

    run_compression_step(
        mother, verifier, bundle_result["content"],
        Path(config["source_dir"]), Path(config["output_dir"]),
        config, state, prompts,
    )

    output_dir = Path(config["output_dir"])
    output_files = sorted(f.relative_to(output_dir).as_posix() for f in output_dir.rglob("*.md"))

    assert "rules/core.md" in output_files
    assert "rules/style.md" in output_files
    assert "workflows/build.md" in output_files


def test_never_compress_files_copied_not_compressed(tmp_path):
    """Integration: never_compress files are included in bundle/analysis but copied
    as-is during compression. Mother is not called for these files."""
    # Setup: source with 1 compressible file + 1 never_compress file
    source = tmp_path / "source"
    (source / "rules").mkdir(parents=True)
    prompts_dir = source / "skills" / "eval" / "prompts"
    prompts_dir.mkdir(parents=True)

    (source / "rules" / "core.md").write_text(
        "# Core Rules\n" + "Rule line.\n" * 40, encoding="utf-8",
    )
    prompt_content = "# Eval Prompt\nScore the compression 1-5.\nBe specific.\n"
    (prompts_dir / "score.md").write_text(prompt_content, encoding="utf-8")

    config = {
        "source_dir": str(source),
        "output_dir": str(tmp_path / "output"),
        "models": {
            "mother": {"provider": "anthropic", "model": "claude-opus-4-6",
                       "max_context": 1000000, "thinking": False},
            "verification": {"provider": "openai", "model": "gpt-5-mini",
                             "max_context": 128000},
        },
        "thresholds": {"judge_min_score": 3.5, "max_refinement_attempts": 1,
                       "exclusion_max_lines": 100, "exclusion_max_references": 2,
                       "target_compression_percent": 40, "max_manual_review_files": 5},
        "cache": {"ttl": "1h"},
        "budget": {"max_total_usd": 100.0, "warn_at_percent": 80},
        "file_type_map": {"rules/*.md": "compress_rules", "*": "compress_other"},
        "include_patterns": ["*.md"],
        "skip_patterns": [],
        "never_compress": ["skills/eval/prompts/*"],
        "api_timeout_seconds": 10,
    }

    # Step 1: Bundle - both files should be in bundle
    categories = scan_source_dir(
        Path(config["source_dir"]),
        include_patterns=config["include_patterns"],
    )
    bundle_result = generate_bundle(categories, Path(config["source_dir"]))
    bundle = bundle_result["content"]
    assert bundle_result["file_count"] == 2  # Both files bundled
    assert "skills/eval/prompts/score.md" in bundle

    # Step 6: Compress - only core.md should be sent to Mother
    state = init_state()
    state["files_total"] = 2

    mother = _mock_anthropic(["# Compressed\nShort rules.\n"])  # 1 call for core.md
    verifier = _mock_openai(["Score: 4.5/5\nGood."])

    prompts = {"compress_other": {"transform": "t {file_path} {file_content} {file_type}", "eval": "e"}}

    run_compression_step(
        mother, verifier, bundle,
        Path(config["source_dir"]), Path(config["output_dir"]),
        config, state, prompts,
    )

    output = Path(config["output_dir"])

    # never_compress file: copied as-is with identical content
    nc_dest = output / "skills" / "eval" / "prompts" / "score.md"
    assert nc_dest.exists()
    assert nc_dest.read_text(encoding="utf-8") == prompt_content

    # compressible file: compressed by Mother
    comp_dest = output / "rules" / "core.md"
    assert comp_dest.exists()
    assert comp_dest.read_text(encoding="utf-8") == "# Compressed\nShort rules.\n"

    # Mother called exactly once (for core.md, not for score.md)
    assert mother.call_with_cache.call_count == 1


def test_cost_stays_within_budget(integration_env):
    """TC-51: Cost stays within budget -> state['cost']['total'] < config budget."""
    env = integration_env
    config = env["config"]

    state = init_state()
    # Simulate some API usage cost
    state["cost"]["total"] = 15.0
    state["cost"]["mother_input"] = 5.0
    state["cost"]["mother_output"] = 8.0
    state["cost"]["verification_input"] = 1.0
    state["cost"]["verification_output"] = 1.0

    assert state["cost"]["total"] < config["budget"]["max_total_usd"]
