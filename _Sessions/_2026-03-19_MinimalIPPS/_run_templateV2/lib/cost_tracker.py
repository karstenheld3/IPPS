"""Per-run cost tracking with atomic saves and budget checking."""
import json
import logging
from pathlib import Path

from lib.llm_client import calculate_cost

log = logging.getLogger(__name__)


def init_costs() -> dict:
    """Create fresh RunCosts schema."""
    return {
        "total_cost": 0.0,
        "input_cost": 0.0,
        "output_cost": 0.0,
        "cache_read_cost": 0.0,
        "cache_write_cost": 0.0,
        "total_input_tokens": 0,
        "total_output_tokens": 0,
        "total_cache_read_tokens": 0,
        "total_cache_creation_tokens": 0,
        "api_calls": 0,
        "per_file": [],
    }


def track_call(costs: dict, step: str, file_path: str, usage: dict,
               model: str, cache_hit: bool = False) -> dict:
    """
    Accumulate cost from a single API call.

    Args:
        costs: RunCosts dict (mutated in place)
        step: Pipeline step name (e.g., "compress", "verify")
        file_path: File being processed
        usage: Token usage dict from API response
        model: Model ID used
        cache_hit: Whether cache was hit on this call

    Returns: Updated costs dict
    """
    cost_result = calculate_cost(usage, model)

    costs["total_cost"] += cost_result["total_cost"]
    costs["input_cost"] += cost_result["input_cost"]
    costs["output_cost"] += cost_result["output_cost"]
    costs["cache_read_cost"] += cost_result.get("cache_read_cost", 0.0)
    costs["cache_write_cost"] += cost_result.get("cache_write_cost", 0.0)

    costs["total_input_tokens"] += usage.get("input_tokens", 0)
    costs["total_output_tokens"] += usage.get("output_tokens", 0)
    costs["total_cache_read_tokens"] += usage.get("cache_read_input_tokens", 0)
    costs["total_cache_creation_tokens"] += usage.get("cache_creation_input_tokens", 0)
    costs["api_calls"] += 1

    costs["per_file"].append({
        "file": file_path,
        "step": step,
        "model": model,
        "cost": cost_result["total_cost"],
        "input_tokens": usage.get("input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
        "cache_hit": cache_hit,
    })

    # EC-10: Warn on cache miss for non-first calls
    if not cache_hit and costs["api_calls"] > 1:
        cache_read = usage.get("cache_read_input_tokens", 0)
        if cache_read == 0:
            log.warning(
                "Cache miss on call #%d for %s (step=%s, model=%s). "
                "Cost delta vs cached: $%.4f",
                costs["api_calls"], file_path, step, model,
                cost_result["input_cost"] - cost_result.get("cache_read_cost", 0.0),
            )

    return costs


def save_costs(costs: dict, run_dir: Path) -> Path:
    """
    Atomically write run_costs.json (.tmp + rename).

    Returns: Path to run_costs.json, or None on failure.
    """
    costs_path = run_dir / "run_costs.json"
    tmp_path = costs_path.with_suffix(".json.tmp")
    try:
        tmp_path.write_text(
            json.dumps(costs, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        tmp_path.replace(costs_path)
        return costs_path
    except OSError as exc:
        log.error("Failed to save costs to %s: %s", costs_path, exc)
        # Clean up tmp if it exists
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass
        return None


def load_costs(run_dir: Path) -> dict:
    """Load run_costs.json from run directory. Returns init_costs() if missing."""
    costs_path = run_dir / "run_costs.json"
    if not costs_path.exists():
        return init_costs()
    return json.loads(costs_path.read_text(encoding="utf-8"))


def check_budget(costs: dict, config: dict) -> tuple:
    """
    Check if costs are within budget.

    Args:
        costs: RunCosts dict
        config: Pipeline config dict with budget.max_total_usd and budget.warning_threshold

    Returns: (ok: bool, message: str)
        ok=True: within budget
        ok=True + message: warning threshold reached
        ok=False: budget exceeded
    """
    budget = config.get("budget", {})
    max_usd = budget.get("max_total_usd", float("inf"))
    threshold = budget.get("warning_threshold", 0.8)

    total = costs.get("total_cost", 0.0)

    if total >= max_usd:
        return False, f"Budget exceeded: ${total:.4f} >= ${max_usd:.2f}"

    if max_usd > 0 and total >= max_usd * threshold:
        return True, f"Budget warning: ${total:.4f} >= {threshold*100:.0f}% of ${max_usd:.2f}"

    return True, ""
