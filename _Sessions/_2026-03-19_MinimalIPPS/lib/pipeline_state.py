"""Pipeline state management with atomic writes and corruption recovery."""
import json
import logging
import shutil
from pathlib import Path

log = logging.getLogger(__name__)


def init_state() -> dict:
    """Create fresh pipeline state with all required fields."""
    return {
        "current_step": 0,
        "iteration": 1,
        "files_total": 0,
        "files_compressible": 0,
        "files_excluded": 0,
        "files_compressed": 0,
        "files_passed": 0,
        "files_failed": 0,
        "files_excluded_md": 0,
        "files_completed": [],
        "broken_references": 0,
        "cache_last_used": None,
        "cost": {
            "mother_input": 0.0,
            "mother_output": 0.0,
            "verification_input": 0.0,
            "verification_output": 0.0,
            "total": 0.0,
        },
    }


def load_state(path: Path) -> dict:
    """Load state from JSON file. On corruption (EC-08): backup and return fresh state."""
    if not path.exists():
        return init_state()
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, ValueError) as exc:
        backup = path.with_suffix(".json.bak")
        shutil.copy2(path, backup)
        log.warning(
            "Corrupted state file '%s', backed up to '%s': %s",
            path, backup, exc,
        )
        return init_state()


def save_state(path: Path, state: dict) -> None:
    """Atomic write: write to .tmp then rename to avoid partial writes."""
    tmp_path = path.with_suffix(".json.tmp")
    tmp_path.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    tmp_path.replace(path)


def update_step(state: dict, step: int) -> dict:
    """Set current pipeline step."""
    state["current_step"] = step
    return state


def add_completed_file(state: dict, file_path: str) -> dict:
    """Append file path to files_completed list."""
    if file_path not in state["files_completed"]:
        state["files_completed"].append(file_path)
    return state


def update_cost(
    state: dict,
    model: str,
    input_tokens: int,
    output_tokens: int,
    cache_read_tokens: int = 0,
    cache_write_tokens: int = 0,
) -> dict:
    """Update cost tracking in state using api_cost_tracker."""
    from lib.api_cost_tracker import calculate_cost

    cost = calculate_cost(model, input_tokens, output_tokens, cache_read_tokens, cache_write_tokens)
    if "anthropic" in model or "claude" in model:
        state["cost"]["mother_input"] += calculate_cost(model, input_tokens, 0, cache_read_tokens, cache_write_tokens)
        state["cost"]["mother_output"] += calculate_cost(model, 0, output_tokens)
    else:
        state["cost"]["verification_input"] += calculate_cost(model, input_tokens, 0)
        state["cost"]["verification_output"] += calculate_cost(model, 0, output_tokens)
    state["cost"]["total"] += cost
    return state
