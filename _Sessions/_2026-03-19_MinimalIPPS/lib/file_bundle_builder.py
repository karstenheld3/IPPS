"""File scanning, bundle generation, and token counting."""
import fnmatch
import logging
from pathlib import Path

import tiktoken

log = logging.getLogger(__name__)


class EmptySourceError(Exception):
    """Raised when source directory contains no matching files."""


def scan_source_dir(
    source_dir: Path,
    include_patterns: list[str] = None,
    skip_patterns: list[str] = None,
) -> dict[str, list[Path]]:
    """Scan source directory and categorize files.

    Args:
        source_dir: Root directory to scan
        include_patterns: Glob patterns for files to include (default: ["*.md"])
        skip_patterns: Glob patterns for files to skip

    Returns:
        Dict mapping category names to lists of file paths

    Raises:
        EmptySourceError: If no matching files found (EC-01)
    """
    if include_patterns is None:
        include_patterns = ["*.md"]
    if skip_patterns is None:
        skip_patterns = []

    source_dir = Path(source_dir)
    if not source_dir.exists():
        raise EmptySourceError(f"Source directory does not exist: {source_dir}")

    all_files = sorted(source_dir.rglob("*"))
    matched = []

    for file_path in all_files:
        if not file_path.is_file():
            continue
        rel = file_path.relative_to(source_dir).as_posix()

        # Check skip patterns
        if any(fnmatch.fnmatch(rel, pat) for pat in skip_patterns):
            log.debug("Skipping '%s' (matches skip pattern)", rel)
            continue

        # Check include patterns
        if not any(fnmatch.fnmatch(file_path.name, pat) for pat in include_patterns):
            log.debug("Excluding '%s' (no include pattern match)", rel)
            continue

        # Skip binary files (EC-03)
        try:
            file_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, ValueError):
            log.debug("Skipping binary file '%s'", rel)
            continue

        matched.append(file_path)

    if not matched:
        raise EmptySourceError(
            f"No matching files in '{source_dir}' "
            f"(include={include_patterns}, skip={skip_patterns})"
        )

    # Categorize by relative directory
    categories: dict[str, list[Path]] = {}
    for file_path in matched:
        rel = file_path.relative_to(source_dir)
        # Use first directory component as category, or "root" if in root
        parts = rel.parts
        category = parts[0] if len(parts) > 1 else "root"
        categories.setdefault(category, []).append(file_path)

    log.info(
        "Scanned '%s': %d files in %d categories",
        source_dir, len(matched), len(categories),
    )
    return categories


def generate_bundle(
    files: dict[str, list[Path]],
    source_dir: Path,
    output_path: Path = None,
) -> dict:
    """Generate concatenated bundle with ## [path] headers.

    Args:
        files: Dict from scan_source_dir
        source_dir: Root directory for relative paths
        output_path: Optional path to write bundle file

    Returns:
        Dict with keys: content, file_count, token_count
    """
    source_dir = Path(source_dir)
    parts = []
    file_count = 0

    for category in sorted(files.keys()):
        for file_path in sorted(files[category]):
            rel = file_path.relative_to(source_dir).as_posix()
            content = file_path.read_text(encoding="utf-8")
            line_count = content.count("\n") + (1 if content and not content.endswith("\n") else 0)
            token_est = count_tokens(content)
            parts.append(
                f"## [{rel}]\n"
                f"<!-- lines: {line_count}, tokens: ~{token_est} -->\n"
                f"{content}\n"
            )
            file_count += 1

    bundle_content = "\n".join(parts)
    token_count = count_tokens(bundle_content)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(bundle_content, encoding="utf-8")
        log.info(
            "Bundle written to '%s': %d files, ~%d tokens",
            output_path, file_count, token_count,
        )

    return {
        "content": bundle_content,
        "file_count": file_count,
        "token_count": token_count,
    }


def count_tokens(text: str) -> int:
    """Count tokens using tiktoken cl100k_base encoding."""
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))
