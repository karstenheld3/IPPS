"""Spot-check verification of Mother outputs using OpenAI verification model (FR-11)."""
import logging
import random

log = logging.getLogger(__name__)


def spot_check_document(
    client,
    document: str,
    source_files: list[str],
    sample_size: int = 15,
) -> dict:
    """Spot-check a Mother-generated document against source files.

    Picks random files from source_files list, asks verification model to
    check if claims about those files in the document are accurate.

    Args:
        client: LLMClient instance (OpenAI)
        document: Content of Mother-generated document to verify
        source_files: List of (path, content) tuples for source files
        sample_size: Number of files to check (default 15)

    Returns:
        Dict with keys: checked_count, issues (list of issue dicts)
    """
    if not source_files:
        return {"checked_count": 0, "issues": []}

    sample = random.sample(source_files, min(sample_size, len(source_files)))
    issues = []

    for path, content in sample:
        prompt = (
            f"Compare the following source file against claims made about it "
            f"in the analysis document.\n\n"
            f"## Source file: {path}\n```\n{content[:2000]}\n```\n\n"
            f"## Analysis document excerpt (search for references to '{path}'):\n"
            f"{document[:3000]}\n\n"
            f"Are the claims about this file accurate? "
            f"Reply with 'ACCURATE' if correct, or describe any inaccuracies found. "
            f"Be specific about what is wrong."
        )
        result = client.call(prompt, max_tokens=300)
        response_text = result["text"]

        if "ACCURATE" not in response_text.upper().split("\n")[0]:
            issues.append({
                "file": path,
                "claim": "See analysis document",
                "verification": response_text.strip(),
            })

    log.info(
        "Spot-checked %d files: %d issues found",
        len(sample), len(issues),
    )
    return {"checked_count": len(sample), "issues": issues}


def report_issues(issues: list[dict]) -> str:
    """Format spot-check issues into readable report.

    Args:
        issues: List of issue dicts from spot_check_document

    Returns:
        Formatted string with file path, claim, and verification result per issue
    """
    if not issues:
        return "No issues found during spot-check verification."

    lines = [f"## Spot-Check Issues ({len(issues)} found)\n"]
    for i, issue in enumerate(issues, 1):
        lines.append(f"### Issue {i}: {issue['file']}")
        lines.append(f"- **Claim**: {issue['claim']}")
        lines.append(f"- **Verification**: {issue['verification']}")
        lines.append("")

    return "\n".join(lines)
