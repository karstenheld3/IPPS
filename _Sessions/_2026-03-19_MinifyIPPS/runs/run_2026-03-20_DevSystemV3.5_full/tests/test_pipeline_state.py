"""Tests for lib/pipeline_state.py (TC-06 to TC-09)."""
import json

from lib.pipeline_state import (
    add_completed_file,
    init_state,
    load_state,
    save_state,
    update_step,
)


def test_load_valid_state(tmp_path):
    """TC-06: Load valid state file -> returns dict with all PipelineState fields."""
    state = init_state()
    state["current_step"] = 3
    state["files_total"] = 50
    state_path = tmp_path / "pipeline_state.json"
    state_path.write_text(json.dumps(state), encoding="utf-8")

    loaded = load_state(state_path)

    assert loaded["current_step"] == 3
    assert loaded["files_total"] == 50
    assert "cost" in loaded
    assert "files_completed" in loaded


def test_load_corrupted_state(tmp_path):
    """TC-07: Load corrupted state file -> creates .bak backup, returns fresh init_state()."""
    state_path = tmp_path / "pipeline_state.json"
    state_path.write_text("{invalid json!!!", encoding="utf-8")

    loaded = load_state(state_path)

    assert loaded == init_state()
    backup = state_path.with_suffix(".json.bak")
    assert backup.exists()
    assert backup.read_text(encoding="utf-8") == "{invalid json!!!"


def test_update_step(sample_state):
    """TC-08: update_step sets current_step -> state['current_step'] equals new value."""
    updated = update_step(sample_state, 5)
    assert updated["current_step"] == 5


def test_add_completed_file(sample_state):
    """TC-09: add_completed_file appends to list -> file path in state['files_completed']."""
    updated = add_completed_file(sample_state, "rules/core.md")
    assert "rules/core.md" in updated["files_completed"]

    # Adding same file again should not duplicate
    updated = add_completed_file(updated, "rules/core.md")
    assert updated["files_completed"].count("rules/core.md") == 1


def test_save_state_atomic(tmp_path):
    """Verify atomic write pattern: no .tmp file left after save."""
    state_path = tmp_path / "pipeline_state.json"
    state = init_state()
    state["current_step"] = 2

    save_state(state_path, state)

    assert state_path.exists()
    assert not state_path.with_suffix(".json.tmp").exists()
    loaded = json.loads(state_path.read_text(encoding="utf-8"))
    assert loaded["current_step"] == 2
