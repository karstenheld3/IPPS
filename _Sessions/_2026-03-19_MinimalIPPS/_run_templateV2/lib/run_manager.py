"""Run management: create isolated run folders, snapshot config, generate summaries."""
import json
import logging
from datetime import datetime
from pathlib import Path

log = logging.getLogger(__name__)

# Standard subdirectories for a run folder
RUN_SUBDIRS = [
    "analysis",
    "context",
    "prompts/step",
    "prompts/transform",
    "prompts/eval",
    "verification",
    "output",
]


def create_run(base_dir: Path, label: str = "run") -> tuple:
    """
    Create isolated run folder under base_dir/runs/.

    Args:
        base_dir: Project root (contains runs/ directory)
        label: Human-readable label for the run

    Returns: (run_dir: Path, run_id: str)

    Run ID format: YYYYMMDD-HHMM-<label>
    Creates parent runs/ dir if missing (EC-05).
    Appends -2, -3 suffix on ID collision (TC-07).
    Raises OSError if directory creation fails (EC-07).
    """
    runs_dir = base_dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    base_id = f"{now.strftime('%Y%m%d-%H%M')}-{label}"
    run_id = base_id
    run_dir = runs_dir / run_id

    # Handle collision
    suffix = 2
    while run_dir.exists():
        run_id = f"{base_id}-{suffix}"
        run_dir = runs_dir / run_id
        suffix += 1

    # Create all subdirectories
    for subdir in RUN_SUBDIRS:
        (run_dir / subdir).mkdir(parents=True, exist_ok=True)

    log.info("Created run folder: %s", run_dir)
    return run_dir, run_id


def snapshot_config(config: dict, run_dir: Path, run_id: str) -> Path:
    """
    Write run_config.json with config snapshot + run metadata.

    Returns: Path to run_config.json
    """
    snapshot = {
        "run_id": run_id,
        "started_at": datetime.now().isoformat(),
        **config,
    }
    config_path = run_dir / "run_config.json"
    config_path.write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return config_path


def generate_run_summary(run_dir: Path, state: dict, costs: dict) -> Path:
    """
    Write run_summary.md with human-readable run results.

    Args:
        run_dir: Run folder path
        state: Pipeline state dict (files_total, files_compressed, etc.)
        costs: RunCosts dict (total_cost, per_file, etc.)

    Returns: Path to run_summary.md
    """
    total_files = state.get("files_total", 0)
    compressed = state.get("files_compressed", 0)
    excluded = state.get("files_excluded", 0) + state.get("files_excluded_md", 0)
    failed = state.get("files_failed", 0)

    ratio = (compressed / total_files * 100) if total_files > 0 else 0

    total_cost = costs.get("total_cost", 0.0)
    per_file = costs.get("per_file", [])

    lines = [
        f"# Run Summary: {run_dir.name}",
        "",
        "## Compression",
        "",
        f"- Files total: {total_files}",
        f"- Files compressed: {compressed}",
        f"- Files excluded: {excluded}",
        f"- Files failed: {failed}",
        f"- Compression ratio: {ratio:.1f}%",
        "",
        "## Cost",
        "",
        f"- Total cost: ${total_cost:.4f}",
        f"- Files tracked: {len(per_file)}",
    ]

    # Cache efficiency
    cache_hits = sum(1 for f in per_file if f.get("cache_hit"))
    cache_total = len([f for f in per_file if "cache_hit" in f])
    if cache_total > 0:
        lines.append(f"- Cache hit rate: {cache_hits}/{cache_total} ({cache_hits/cache_total*100:.0f}%)")

    lines.append("")

    summary_path = run_dir / "run_summary.md"
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    return summary_path
