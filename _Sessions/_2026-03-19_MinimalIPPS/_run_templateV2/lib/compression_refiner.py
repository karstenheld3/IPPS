"""Iteration: review report, update strategy, identify files to recompress (FR-08)."""
import logging
import re
from pathlib import Path

log = logging.getLogger(__name__)


def review_report(client, bundle: str, report: str) -> dict:
    """Send compression report to Mother for review with cached context.

    Args:
        client: AnthropicClient instance
        bundle: Full file bundle content (cached)
        report: Content of _04_FILE_COMPRESSION_REPORT.md

    Returns:
        Dict with keys: updates (dict of file-level guidance changes),
        files_to_recompress (list of file paths)
    """
    prompt = (
        "Review this compression report. For each file that had issues "
        "(broken references, low scores, lost content), provide:\n"
        "1. Specific guidance changes for the compression strategy\n"
        "2. Which files need to be recompressed\n\n"
        "Format your response as:\n"
        "## Strategy Updates\n"
        "- [file_path]: [what to change in compression approach]\n\n"
        "## Files to Recompress\n"
        "- [file_path]\n\n"
        f"## Report\n{report}"
    )
    text, usage = client.call_with_cache(bundle, prompt)
    log.info("Report review complete (%d output tokens)", usage["output_tokens"])

    # Parse response
    updates = {}
    files_to_recompress = []

    in_updates = False
    in_recompress = False

    for line in text.split("\n"):
        line = line.strip()
        if "Strategy Updates" in line:
            in_updates = True
            in_recompress = False
            continue
        if "Files to Recompress" in line:
            in_updates = False
            in_recompress = True
            continue

        if in_updates and line.startswith("- "):
            match = re.match(r"-\s*\[?([^\]:\n]+\.md)\]?\s*:\s*(.+)", line)
            if match:
                updates[match.group(1).strip()] = match.group(2).strip()
        elif in_recompress and line.startswith("- "):
            match = re.match(r"-\s*\[?([^\]:\n]+\.md)\]?", line)
            if match:
                files_to_recompress.append(match.group(1).strip())

    return {"updates": updates, "files_to_recompress": files_to_recompress}


def update_strategy(strategy_path: Path, updates: dict) -> str:
    """Modify compression strategy file based on review findings.

    Args:
        strategy_path: Path to _03_FILE_COMPRESSION_STRATEGY.md
        updates: Dict mapping file path to guidance change string

    Returns:
        Updated strategy content
    """
    if not strategy_path.exists():
        raise FileNotFoundError(
            f"Strategy file not found: {strategy_path}. Run Steps 2-4 first."
        )

    content = strategy_path.read_text(encoding="utf-8")

    # Append iteration updates section
    update_lines = ["\n## Iteration Updates\n"]
    for file_path, guidance in updates.items():
        update_lines.append(f"- **{file_path}**: {guidance}")

    updated_content = content + "\n".join(update_lines) + "\n"
    strategy_path.write_text(updated_content, encoding="utf-8")
    log.info("Strategy updated with %d file-level guidance changes", len(updates))
    return updated_content


def get_files_to_recompress(report: str) -> list[str]:
    """Parse compression report for files that need recompression.

    Identifies files with:
    - Broken references
    - Low scores (mentioned as failed/flagged)
    - Manual review status

    Args:
        report: Content of _04_FILE_COMPRESSION_REPORT.md

    Returns:
        List of file paths that should be recompressed

    Raises:
        FileNotFoundError: If report content is empty (EC-07)
    """
    if not report or not report.strip():
        raise FileNotFoundError(
            "No compression report content provided. Run Step 7 (verify) first."
        )

    files = []

    # Parse ### [file_path] sections that have issues
    current_file = None
    has_issues = False

    for line in report.split("\n"):
        # Match section headers: ### [rules/core.md]
        header_match = re.match(r"###\s+\[([^\]]+\.md)\]", line)
        if header_match:
            if current_file and has_issues:
                files.append(current_file)
            current_file = header_match.group(1)
            has_issues = False
            continue

        # Check for issue indicators
        if current_file:
            if "BROKEN_REF" in line:
                has_issues = True
            if re.search(r"manual.review|failed|flagged|token.increase", line, re.IGNORECASE):
                has_issues = True

    # Don't forget last file
    if current_file and has_issues:
        files.append(current_file)

    log.info("Found %d files to recompress from report", len(files))
    return files
