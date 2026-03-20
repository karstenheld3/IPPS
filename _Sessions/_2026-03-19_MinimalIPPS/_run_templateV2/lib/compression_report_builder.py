"""Step 7: Verification report generation with cross-reference checking (FR-07)."""
import logging
import re
from pathlib import Path

log = logging.getLogger(__name__)


def verify_file(
    client,
    original: str,
    compressed: str,
    prompt: str,
    file_path: str,
) -> dict:
    """Verify a single compressed file against its original using verification model.

    Produces exactly 5 lines per file per SPEC Step 7 report format.

    Args:
        client: OpenAIClient instance
        original: Original file content
        compressed: Compressed file content
        prompt: Step 7 verification prompt template
        file_path: Relative file path

    Returns:
        Dict with keys: file_path, report_lines (list of 5 strings), broken_refs (list)
    """
    filled_prompt = prompt.replace("{file_path}", file_path)
    filled_prompt = filled_prompt.replace("{original_content}", original[:4000])
    filled_prompt = filled_prompt.replace("{compressed_content}", compressed[:4000])

    text, _usage = client.call(filled_prompt, max_tokens=500)

    # Parse 5-line report and broken refs
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    report_lines = []
    broken_refs = []

    for line in lines:
        if line.startswith("BROKEN_REF:"):
            broken_refs.append(line)
        elif len(report_lines) < 5:
            report_lines.append(line)

    # Pad to exactly 5 lines if needed
    while len(report_lines) < 5:
        report_lines.append("(no data)")

    return {
        "file_path": file_path,
        "report_lines": report_lines[:5],
        "broken_refs": broken_refs,
    }


def check_cross_references(
    compressed_files: dict[str, str],
    excluded_files: list[str],
) -> list[str]:
    """Scan all compressed and excluded files for broken cross-file references (EC-15).

    Looks for markdown references to .md files and checks if the target exists
    in the compressed_files dict or excluded_files list.

    Args:
        compressed_files: Dict mapping relative path -> compressed content
        excluded_files: List of excluded file relative paths

    Returns:
        List of broken reference descriptions
    """
    all_known = set(compressed_files.keys()) | set(excluded_files)
    broken = []

    for file_path, content in compressed_files.items():
        # Find references to .md files in content
        refs = re.findall(r"(?:[\w/\-]+\.md)", content)
        for ref in refs:
            # Normalize: strip leading ./ or /
            normalized = ref.lstrip("./")
            if normalized not in all_known and normalized != file_path:
                # Check if it could be a partial match (filename only)
                basename = Path(normalized).name
                if not any(Path(k).name == basename for k in all_known):
                    broken.append(
                        f"BROKEN_REF: '{ref}' in {file_path} -> target not found"
                    )

    log.info(
        "Cross-reference check: %d broken references in %d files",
        len(broken), len(compressed_files),
    )
    return broken


def generate_report(
    results: list[dict],
    cross_ref_issues: list[str],
    output_path: Path = None,
) -> str:
    """Generate _04_FILE_COMPRESSION_REPORT.md with summary and per-file entries.

    Args:
        results: List of dicts from verify_file
        cross_ref_issues: List from check_cross_references
        output_path: Optional path to write report file

    Returns:
        Report content string
    """
    total = len(results)
    passed = sum(1 for r in results if not r["broken_refs"])
    pass_rate = (passed / total * 100) if total > 0 else 0
    broken_count = len(cross_ref_issues) + sum(len(r["broken_refs"]) for r in results)

    lines = [
        "# Compression Report\n",
        "## Summary\n",
        f"- **Files verified**: {total}",
        f"- **Pass rate**: {pass_rate:.0f}%",
        f"- **Broken references**: {broken_count}",
        "",
    ]

    # Per-file entries
    for result in results:
        lines.append(f"### [{result['file_path']}]")
        for i, report_line in enumerate(result["report_lines"], 1):
            label = [
                "Structural changes",
                "Removed features",
                "Simplified content",
                "Sacrificed details",
                "Possible impact",
            ][i - 1]
            # Strip existing label if present
            clean = re.sub(r"^\d+\.\s*\*\*[^*]+\*\*:\s*", "", report_line)
            lines.append(f"{i}. **{label}**: {clean}")
        if result["broken_refs"]:
            for ref in result["broken_refs"]:
                lines.append(f"- {ref}")
        lines.append("")

    # Cross-reference section
    if cross_ref_issues:
        lines.append("## Cross-Reference Issues\n")
        for issue in cross_ref_issues:
            lines.append(f"- {issue}")
        lines.append("")

    content = "\n".join(lines)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        log.info("Report written to '%s'", output_path)

    return content
