"""Compare two pipeline runs side-by-side (IS-15)."""
import json
import sys
from pathlib import Path


def load_run_data(run_dir: Path) -> dict:
    """Load run_config.json and run_costs.json from a run directory.
    
    Returns dict with config, costs, and summary info.
    Raises FileNotFoundError if run directory doesn't exist.
    """
    if not run_dir.exists():
        raise FileNotFoundError(f"Run directory not found: {run_dir}")

    data = {"run_dir": str(run_dir), "run_id": run_dir.name}

    config_path = run_dir / "run_config.json"
    if config_path.exists():
        data["config"] = json.loads(config_path.read_text(encoding="utf-8"))
    else:
        data["config"] = {}

    costs_path = run_dir / "run_costs.json"
    if costs_path.exists():
        data["costs"] = json.loads(costs_path.read_text(encoding="utf-8"))
    else:
        data["costs"] = {}

    summary_path = run_dir / "run_summary.md"
    if summary_path.exists():
        data["summary"] = summary_path.read_text(encoding="utf-8")
    else:
        data["summary"] = ""

    return data


def compare_runs(run_a: dict, run_b: dict) -> dict:
    """Compare two runs and return structured comparison.
    
    Returns dict with:
        - cost_delta: total cost difference (B - A)
        - cost_delta_pct: percentage change
        - token_delta: token usage difference
        - regressions: list of metrics that got worse
        - improvements: list of metrics that improved
    """
    costs_a = run_a.get("costs", {})
    costs_b = run_b.get("costs", {})

    total_a = costs_a.get("total_cost", 0.0)
    total_b = costs_b.get("total_cost", 0.0)
    cost_delta = total_b - total_a
    cost_delta_pct = (cost_delta / total_a * 100) if total_a > 0 else 0.0

    tokens_a = costs_a.get("total_input_tokens", 0) + costs_a.get("total_output_tokens", 0)
    tokens_b = costs_b.get("total_input_tokens", 0) + costs_b.get("total_output_tokens", 0)
    token_delta = tokens_b - tokens_a

    cache_read_a = costs_a.get("total_cache_read_tokens", 0)
    cache_read_b = costs_b.get("total_cache_read_tokens", 0)

    regressions = []
    improvements = []

    if cost_delta > 0:
        regressions.append(f"Cost increased: ${total_a:.4f} -> ${total_b:.4f} (+${cost_delta:.4f}, +{cost_delta_pct:.1f}%)")
    elif cost_delta < 0:
        improvements.append(f"Cost decreased: ${total_a:.4f} -> ${total_b:.4f} (${cost_delta:.4f}, {cost_delta_pct:.1f}%)")

    if token_delta > 0:
        regressions.append(f"Token usage increased: {tokens_a} -> {tokens_b} (+{token_delta})")
    elif token_delta < 0:
        improvements.append(f"Token usage decreased: {tokens_a} -> {tokens_b} ({token_delta})")

    if cache_read_b > cache_read_a:
        improvements.append(f"Cache utilization improved: {cache_read_a} -> {cache_read_b} read tokens")
    elif cache_read_b < cache_read_a and cache_read_a > 0:
        regressions.append(f"Cache utilization decreased: {cache_read_a} -> {cache_read_b} read tokens")

    api_calls_a = costs_a.get("api_calls", 0)
    api_calls_b = costs_b.get("api_calls", 0)
    if api_calls_b > api_calls_a:
        regressions.append(f"API calls increased: {api_calls_a} -> {api_calls_b}")
    elif api_calls_b < api_calls_a:
        improvements.append(f"API calls decreased: {api_calls_a} -> {api_calls_b}")

    return {
        "run_a": run_a.get("run_id", "?"),
        "run_b": run_b.get("run_id", "?"),
        "cost_delta": round(cost_delta, 6),
        "cost_delta_pct": round(cost_delta_pct, 1),
        "token_delta": token_delta,
        "regressions": regressions,
        "improvements": improvements,
    }


def format_comparison(comparison: dict) -> str:
    """Format comparison dict as human-readable text."""
    lines = [
        f"# Run Comparison: {comparison['run_a']} vs {comparison['run_b']}",
        "",
        f"- Cost delta: ${comparison['cost_delta']:+.4f} ({comparison['cost_delta_pct']:+.1f}%)",
        f"- Token delta: {comparison['token_delta']:+d}",
        "",
    ]

    if comparison["improvements"]:
        lines.append("## Improvements")
        for item in comparison["improvements"]:
            lines.append(f"- {item}")
        lines.append("")

    if comparison["regressions"]:
        lines.append("## Regressions")
        for item in comparison["regressions"]:
            lines.append(f"- {item}")
        lines.append("")

    if not comparison["improvements"] and not comparison["regressions"]:
        lines.append("No significant differences detected.")
        lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print("Usage: python compare_runs.py <run_dir_a> <run_dir_b>")
        sys.exit(1)

    run_dir_a = Path(sys.argv[1])
    run_dir_b = Path(sys.argv[2])

    try:
        data_a = load_run_data(run_dir_a)
        data_b = load_run_data(run_dir_b)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    comparison = compare_runs(data_a, data_b)
    print(format_comparison(comparison))


if __name__ == "__main__":
    main()
