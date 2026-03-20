"""Mother analysis: call tree (Step 2), complexity map (Step 3), compression strategy (Step 4)."""
import fnmatch
import logging
import re
from pathlib import Path

log = logging.getLogger(__name__)


def analyze_call_tree(client, bundle: str, prompt: str, output_dir: Path) -> str:
    """Step 2: Call Mother to analyze file call tree (FR-02).

    Args:
        client: LLMClient instance (Anthropic)
        bundle: Full file bundle content
        prompt: Step 2 prompt content
        output_dir: Directory to write _01_FILE_CALL_TREE.md

    Returns:
        Call tree document content
    """
    result = client.call_with_cache(bundle, prompt)
    text, usage = result["text"], result["usage"]
    output_path = output_dir / "_01_FILE_CALL_TREE.md"
    output_path.write_text(text, encoding="utf-8")
    log.info("Call tree written to '%s' (%d tokens output)", output_path, usage["output_tokens"])
    return text


def parse_load_frequencies(call_tree: str) -> dict[str, int]:
    """Extract per-file reference counts from call tree output.

    Looks for patterns like:
        [file_path]: N references
    or counts how many times each file path appears in "triggered by" lists.

    Returns:
        Dict mapping file paths to integer reference counts
    """
    frequencies: dict[str, int] = {}

    # Pattern 1: explicit count format "[path]: N references"
    for match in re.finditer(r"^\s*\[?([^\]\n:]+\.md)\]?\s*:\s*(\d+)\s*reference", call_tree, re.MULTILINE):
        path = match.group(1).strip()
        count = int(match.group(2))
        frequencies[path] = count

    # Pattern 2: count appearances in "triggered by" or "loaded by" lines
    if not frequencies:
        # Fallback: count how many times each .md file is mentioned
        file_mentions: dict[str, int] = {}
        for match in re.finditer(r"(?:[\w/\-]+\.md)", call_tree):
            path = match.group(0)
            file_mentions[path] = file_mentions.get(path, 0) + 1
        # Normalize: subtract 1 for the file's own entry
        for path, count in file_mentions.items():
            frequencies[path] = max(0, count - 1)

    return frequencies


def analyze_complexity(client, bundle: str, prompt: str, output_dir: Path) -> str:
    """Step 3: Call Mother to create complexity map (FR-03).

    Args:
        client: LLMClient instance (Anthropic)
        bundle: Full file bundle content
        prompt: Step 3 prompt content
        output_dir: Directory to write _02_FILE_COMPLEXITY_MAP.md

    Returns:
        Complexity map document content
    """
    result = client.call_with_cache(bundle, prompt)
    text, usage = result["text"], result["usage"]
    output_path = output_dir / "_02_FILE_COMPLEXITY_MAP.md"
    output_path.write_text(text, encoding="utf-8")
    log.info("Complexity map written to '%s' (%d tokens output)", output_path, usage["output_tokens"])
    return text


def identify_excluded_files(
    complexity_map: str,
    load_frequencies: dict[str, int],
    config: dict,
) -> list[str]:
    """Apply exclusion criteria: files with < max_lines AND <= max_references.

    Both criteria must be met for exclusion. Files meeting only one criterion are NOT excluded.

    Args:
        complexity_map: Content of _02_FILE_COMPLEXITY_MAP.md
        load_frequencies: Dict from parse_load_frequencies
        config: Pipeline config with thresholds

    Returns:
        List of file paths to exclude from compression
    """
    max_lines = config["thresholds"]["exclusion_max_lines"]
    max_refs = config["thresholds"]["exclusion_max_references"]

    excluded = []

    # Parse line counts from complexity map
    # Expected format: "- **Path**: file.md" ... "- **Lines**: N"
    # or "| file.md | N lines |" etc.
    file_lines: dict[str, int] = {}
    current_file = None

    for line in complexity_map.split("\n"):
        # Pattern: "- **Path**: some/file.md" or "### some/file.md"
        path_match = re.search(r"(?:\*\*Path\*\*:\s*|###\s+)([^\s*]+\.md)", line)
        if path_match:
            current_file = path_match.group(1).strip()
            continue

        # Pattern: "- **Lines**: 42" or "Lines: 42"
        lines_match = re.search(r"(?:\*\*Lines\*\*:\s*|Lines:\s*)(\d+)", line)
        if lines_match and current_file:
            file_lines[current_file] = int(lines_match.group(1))
            current_file = None

    for path, line_count in file_lines.items():
        ref_count = load_frequencies.get(path, 0)
        if line_count < max_lines and ref_count <= max_refs:
            excluded.append(path)
            log.debug(
                "Excluding '%s': %d lines (< %d) AND %d refs (<= %d)",
                path, line_count, max_lines, ref_count, max_refs,
            )

    log.info("Identified %d files for exclusion", len(excluded))
    return excluded


def get_never_compress_files(all_files: list[str], patterns: list[str]) -> list[str]:
    """Return file paths matching any never_compress glob pattern.

    Args:
        all_files: List of relative file paths (forward slashes)
        patterns: Glob patterns from pipeline_config.json never_compress

    Returns:
        List of file paths that should be copied as-is
    """
    matched = [f for f in all_files if any(fnmatch.fnmatch(f, p) for p in patterns)]
    if matched:
        log.info("Never-compress: %d files match patterns", len(matched))
    return matched


def generate_strategy(
    client,
    bundle: str,
    prompt: str,
    excluded: list[str],
    output_dir: Path,
) -> str:
    """Step 4: Call Mother to create compression strategy (FR-04).

    Args:
        client: LLMClient instance (Anthropic)
        bundle: Full file bundle content
        prompt: Step 4 prompt content
        excluded: List of excluded file paths
        output_dir: Directory to write _03_FILE_COMPRESSION_STRATEGY.md

    Returns:
        Strategy document content
    """
    full_prompt = (
        f"{prompt}\n\n"
        f"## Excluded Files (do not include in compression scope)\n\n"
        + "\n".join(f"- {f}" for f in excluded)
    )
    result = client.call_with_cache(bundle, full_prompt)
    text, usage = result["text"], result["usage"]
    output_path = output_dir / "_03_FILE_COMPRESSION_STRATEGY.md"
    output_path.write_text(text, encoding="utf-8")
    log.info("Strategy written to '%s' (%d tokens output)", output_path, usage["output_tokens"])
    return text
