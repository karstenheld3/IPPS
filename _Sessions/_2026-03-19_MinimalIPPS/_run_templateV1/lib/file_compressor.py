"""Step 6: File compression loop with judge scoring and resume support (FR-06)."""
import fnmatch
import logging
import re
from datetime import datetime, timezone
from pathlib import Path

from lib.api_cost_tracker import calculate_cost, check_budget
from lib.file_bundle_builder import count_tokens
from lib.pipeline_state import update_cost

log = logging.getLogger(__name__)


def compress_file(
    client,
    verifier,
    file_path: Path,
    file_content: str,
    bundle: str,
    transform_prompt: str,
    eval_prompt: str,
    config: dict,
) -> dict:
    """Compress a single file, judge with verifier, refine once if needed.

    Args:
        client: AnthropicClient (Mother)
        verifier: OpenAIClient (Verification)
        file_path: Relative path of the file
        file_content: Original file content
        bundle: Full bundle content (cached)
        transform_prompt: Type-specific transform prompt
        eval_prompt: Type-specific eval prompt
        config: Pipeline config

    Returns:
        Dict with keys: compressed, score, status, usage
        status: "accepted", "refined", "manual_review", "token_increase"
    """
    min_score = config["thresholds"]["judge_min_score"]
    max_attempts = config["thresholds"]["max_refinement_attempts"]
    original_tokens = count_tokens(file_content)

    # Build compression prompt: embed file content + type-specific instructions
    file_type = _get_file_type(str(file_path), config)
    prompt = (
        f"Compress this DevSystem file. Output ONLY the compressed markdown "
        f"content - no explanations, no wrapping, no commentary.\n\n"
        f"**Path**: {file_path}\n**Type**: {file_type}\n\n"
        f"## Original Content\n\n{file_content}\n\n"
        f"## Type-Specific Compression Instructions\n\n{transform_prompt}\n\n"
        f"## Output Rules\n\n"
        f"1. Output ONLY the compressed file - nothing else\n"
        f"2. Output must be SHORTER than original ({original_tokens} tokens)\n"
        f"3. Preserve all functional content: rules, conditions, steps\n"
        f"4. Valid markdown that an agent can parse and follow"
    )

    compressed_text, comp_usage = client.call_with_cache(bundle, prompt)
    compressed_tokens = count_tokens(compressed_text)

    # EC-16: Token increase check
    if compressed_tokens >= original_tokens:
        log.warning(
            "Compression increased tokens for '%s': %d -> %d",
            file_path, original_tokens, compressed_tokens,
        )
        return {
            "compressed": compressed_text,
            "score": 0.0,
            "status": "token_increase",
            "original_tokens": original_tokens,
            "compressed_tokens": compressed_tokens,
            "usage": comp_usage,
        }

    # Judge the compression
    score, judge_feedback, judge_usage = _judge_compression(
        verifier, file_content, compressed_text, eval_prompt, file_path
    )

    if score >= min_score:
        return {
            "compressed": compressed_text,
            "score": score,
            "status": "accepted",
            "original_tokens": original_tokens,
            "compressed_tokens": compressed_tokens,
            "usage": {**comp_usage, "judge": judge_usage},
        }

    # Refine once if below threshold
    for attempt in range(max_attempts):
        log.info(
            "Score %.1f < %.1f for '%s', refining (attempt %d/%d)",
            score, min_score, file_path, attempt + 1, max_attempts,
        )
        refine_prompt = (
            f"{prompt}\n\n"
            f"## Previous attempt scored {score}/5. Feedback:\n{judge_feedback}\n\n"
            f"Improve the compression based on this feedback. "
            f"Output ONLY the improved compressed content."
        )
        compressed_text, refine_usage = client.call_with_cache(bundle, refine_prompt)
        compressed_tokens = count_tokens(compressed_text)

        # EC-16 recheck
        if compressed_tokens >= original_tokens:
            return {
                "compressed": compressed_text,
                "score": 0.0,
                "status": "token_increase",
                "original_tokens": original_tokens,
                "compressed_tokens": compressed_tokens,
                "usage": refine_usage,
            }

        score, judge_feedback, judge_usage = _judge_compression(
            verifier, file_content, compressed_text, eval_prompt, file_path
        )

        if score >= min_score:
            return {
                "compressed": compressed_text,
                "score": score,
                "status": "refined",
                "original_tokens": original_tokens,
                "compressed_tokens": compressed_tokens,
                "usage": {**refine_usage, "judge": judge_usage},
            }

    # Failed after refinement -> manual review
    log.warning(
        "File '%s' scored %.1f after refinement, adding to manual review",
        file_path, score,
    )
    return {
        "compressed": compressed_text,
        "score": score,
        "status": "manual_review",
        "original_tokens": original_tokens,
        "compressed_tokens": compressed_tokens,
        "usage": {**comp_usage, "judge": judge_usage},
    }


def run_compression_step(
    client,
    verifier,
    bundle: str,
    source_dir: Path,
    output_dir: Path,
    config: dict,
    state: dict,
    prompts: dict,
) -> dict:
    """Run Step 6 compression loop over all non-excluded, compressible files.

    Handles resume via files_completed in state. Copies excluded .md files as-is.

    Args:
        client: AnthropicClient (Mother)
        verifier: OpenAIClient (Verification)
        bundle: Full bundle content (cached)
        source_dir: Source directory path
        output_dir: Output directory path
        config: Pipeline config
        state: Current pipeline state (modified in-place)
        prompts: Dict of type -> {"transform": str, "eval": str}

    Returns:
        Updated state dict
    """
    from lib.pipeline_state import add_completed_file, save_state

    source_dir = Path(source_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Collect .md files to compress
    all_md = sorted(source_dir.rglob("*.md"))
    skip_patterns = config.get("skip_patterns", [])
    never_compress = config.get("never_compress", [])
    excluded_files = state.get("_excluded_files", [])

    manual_review = []
    total = len(all_md)

    for i, file_path in enumerate(all_md, 1):
        rel = file_path.relative_to(source_dir).as_posix()

        # Evaluation order: skip → never_compress → exclusion → compress

        # Skip non-include files (exclude from output entirely)
        if any(fnmatch.fnmatch(rel, pat) for pat in skip_patterns):
            continue

        # Copy never_compress files as-is (before exclusion criteria)
        if any(fnmatch.fnmatch(rel, pat) for pat in never_compress):
            dest = output_dir / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(file_path.read_text(encoding="utf-8"), encoding="utf-8")
            log.info("Never-compress copied as-is: '%s'", rel)
            continue

        # Copy excluded files as-is
        if rel in excluded_files:
            dest = output_dir / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(file_path.read_text(encoding="utf-8"), encoding="utf-8")
            continue

        # Resume: skip already completed files
        if rel in state.get("files_completed", []):
            log.debug("Skipping already completed: '%s'", rel)
            continue

        # Budget check
        halt, msg = check_budget(state, config)
        if halt:
            log.warning("Budget exceeded, halting compression: %s", msg)
            break

        log.info("Compressing file %d/%d: %s", i, total, rel)

        file_content = file_path.read_text(encoding="utf-8")
        file_type = _get_file_type(rel, config)
        prompt_pair = prompts.get(file_type, prompts.get("compress_other", {}))

        result = compress_file(
            client, verifier, Path(rel), file_content, bundle,
            prompt_pair.get("transform", ""), prompt_pair.get("eval", ""),
            config,
        )

        # Write compressed output
        dest = output_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(result["compressed"], encoding="utf-8")

        # Accumulate API costs into state (FR-10)
        usage = result.get("usage", {})
        mother_model = config["models"]["mother"]["model"]
        verif_model = config["models"]["verification"]["model"]
        if usage:
            update_cost(
                state, mother_model,
                usage.get("input_tokens", 0),
                usage.get("output_tokens", 0),
                usage.get("cache_read_input_tokens", 0),
                usage.get("cache_creation_input_tokens", 0),
            )
            judge_usage = usage.get("judge", {})
            if judge_usage:
                update_cost(
                    state, verif_model,
                    judge_usage.get("prompt_tokens", 0),
                    judge_usage.get("completion_tokens", 0),
                )
        state["cache_last_used"] = datetime.now(timezone.utc).isoformat()

        # Update state
        add_completed_file(state, rel)
        state["files_compressed"] = len(state["files_completed"])

        if result["status"] == "accepted":
            state["files_passed"] += 1
        elif result["status"] == "refined":
            state["files_passed"] += 1
        elif result["status"] in ("manual_review", "token_increase"):
            state["files_failed"] += 1
            manual_review.append({"file": rel, **result})

    # Write manual review queue if needed
    if manual_review:
        _write_manual_review(manual_review, output_dir.parent / "_05_MANUAL_REVIEW_QUEUE.md")

    return state


def _judge_compression(
    verifier, original: str, compressed: str, eval_prompt: str, file_path: Path
) -> tuple[float, str, dict]:
    """Judge compression quality using verification model.

    Returns:
        (score, feedback_text, usage_dict)
    """
    prompt = (
        f"{eval_prompt}\n\n"
        f"## Original ({file_path}):\n```\n{original[:3000]}\n```\n\n"
        f"## Compressed:\n```\n{compressed[:3000]}\n```\n\n"
        f"Respond with EXACTLY this format on the first line:\n"
        f"Score: N.N/5\n"
        f"Then explain your scoring briefly."
    )
    text, usage = verifier.call(prompt, max_tokens=4096)

    # Parse score from response
    score = _parse_score(text)
    return score, text, usage


def _parse_score(text: str) -> float:
    """Extract score from judge response. EC-14: invalid score treated as 1.0."""
    # Try multiple patterns: "Score: 4.2/5", "Final score = 3.8", "4.2/5", standalone decimals
    patterns = [
        r"Score:\s*([\d.]+)",
        r"Final\s+score[=:]\s*([\d.]+)",
        r"([\d.]+)\s*/\s*5",
        r"(?<![/\d.])([1-5](?:\.[0-9])?)(?![/\d])",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                score = float(match.group(1))
                if 1.0 <= score <= 5.0:
                    return score
                log.warning("Score %.1f outside 1-5 range, treating as 1.0", score)
            except ValueError:
                pass
    log.warning("Could not parse score from judge response, treating as 1.0")
    return 1.0


def _get_file_type(rel_path: str, config: dict) -> str:
    """Match file path to file_type_map entry."""
    for pattern, file_type in config.get("file_type_map", {}).items():
        if pattern == "*":
            continue
        if fnmatch.fnmatch(rel_path, pattern):
            return file_type
    return "compress_other"


def _write_manual_review(items: list[dict], output_path: Path) -> None:
    """Write manual review queue file."""
    lines = ["# Manual Review Queue\n"]
    for item in items:
        lines.append(f"## {item['file']}")
        lines.append(f"- **Status**: {item['status']}")
        lines.append(f"- **Score**: {item.get('score', 'N/A')}")
        lines.append(f"- **Original tokens**: {item.get('original_tokens', 'N/A')}")
        lines.append(f"- **Compressed tokens**: {item.get('compressed_tokens', 'N/A')}")
        lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Manual review queue written: %d files to '%s'", len(items), output_path)
