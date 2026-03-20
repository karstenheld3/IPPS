"""Tests for pipeline state: init, load/save, update_cost (TK-008)."""
import json
from pathlib import Path

import pytest
from lib.pipeline_state import init_state, load_state, save_state, update_cost, add_completed_file


class TestInitState:
    """TK-008: State initialization with run metadata."""

    def test_init_state_has_run_fields(self):
        """run_id and run_dir present in initial state."""
        state = init_state(run_id="20260320-1430-test", run_dir="/tmp/runs/test")
        assert state["run_id"] == "20260320-1430-test"
        assert state["run_dir"] == "/tmp/runs/test"

    def test_init_state_defaults(self):
        """Default state has zeroed costs and empty lists."""
        state = init_state()
        assert state["run_id"] is None
        assert state["current_step"] == 0
        assert state["files_completed"] == []
        assert state["cost"]["total"] == 0.0
        assert state["cost"]["cache_read"] == 0.0
        assert state["cost"]["cache_write"] == 0.0


class TestLoadSaveState:
    """TK-008: Atomic load/save with corruption recovery."""

    def test_save_load_roundtrip(self, tmp_path):
        """State survives save + load cycle."""
        path = tmp_path / "pipeline_state.json"
        state = init_state(run_id="test-run")
        state["files_total"] = 42
        save_state(path, state)
        loaded = load_state(path)
        assert loaded["run_id"] == "test-run"
        assert loaded["files_total"] == 42

    def test_load_missing_returns_fresh(self, tmp_path):
        """Missing file returns fresh state."""
        state = load_state(tmp_path / "nonexistent.json")
        assert state["current_step"] == 0

    def test_load_corrupted_backs_up(self, tmp_path):
        """TC-16/EC-08: Corrupted file backed up, fresh state returned."""
        path = tmp_path / "pipeline_state.json"
        path.write_text("{{invalid json", encoding="utf-8")
        state = load_state(path)
        assert state["current_step"] == 0
        assert (tmp_path / "pipeline_state.json.bak").exists()

    def test_save_atomic_no_tmp_left(self, tmp_path):
        """No .tmp file left after save."""
        path = tmp_path / "pipeline_state.json"
        save_state(path, init_state())
        assert not path.with_suffix(".json.tmp").exists()
        assert path.exists()


class TestUpdateCost:
    """TK-008: Cost calculation via llm_client."""

    def test_update_cost_anthropic(self):
        """TC-17: Anthropic costs go to mother_input/output."""
        state = init_state()
        update_cost(state, "claude-opus-4-6-20260204", 1000, 500)
        assert state["cost"]["mother_input"] > 0
        assert state["cost"]["mother_output"] > 0
        assert state["cost"]["verification_input"] == 0.0

    def test_update_cost_openai(self):
        """OpenAI costs go to verification_input/output."""
        state = init_state()
        update_cost(state, "gpt-5-mini", 1000, 500)
        assert state["cost"]["verification_input"] > 0
        assert state["cost"]["verification_output"] > 0
        assert state["cost"]["mother_input"] == 0.0

    def test_update_cost_with_cache(self):
        """TC-17: Cache tokens tracked in cost.cache_read/cache_write."""
        state = init_state()
        update_cost(state, "claude-opus-4-6-20260204", 5000, 1000,
                    cache_read_tokens=3000, cache_write_tokens=2000)
        assert state["cost"]["cache_read"] > 0
        assert state["cost"]["cache_write"] > 0
        assert state["cost"]["total"] > 0

    def test_update_cost_total_accumulates(self):
        """Multiple calls accumulate total."""
        state = init_state()
        update_cost(state, "claude-opus-4-6-20260204", 1000, 500)
        first = state["cost"]["total"]
        update_cost(state, "gpt-5-mini", 1000, 500)
        assert state["cost"]["total"] > first
