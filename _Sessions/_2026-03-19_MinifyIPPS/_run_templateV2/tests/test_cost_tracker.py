"""Tests for cost tracker: tracking, atomic save, budget check (TK-007)."""
import json
import logging

import pytest
from lib.cost_tracker import init_costs, track_call, save_costs, load_costs, check_budget


class TestTrackCall:
    """TK-007: Cost tracking accumulation."""

    def test_track_call_accumulates(self):
        """TC-11: Total increases after tracking a call."""
        costs = init_costs()
        usage = {"input_tokens": 1000, "output_tokens": 500}
        track_call(costs, "compress", "file.md", usage, "claude-opus-4-6-20260204", cache_hit=False)
        assert costs["total_cost"] > 0
        assert costs["api_calls"] == 1

    def test_track_call_per_file(self):
        """TC-12: Entry appears in per_file list."""
        costs = init_costs()
        usage = {"input_tokens": 1000, "output_tokens": 500}
        track_call(costs, "compress", "rules/agent.md", usage, "claude-opus-4-6-20260204")
        assert len(costs["per_file"]) == 1
        assert costs["per_file"][0]["file"] == "rules/agent.md"
        assert costs["per_file"][0]["step"] == "compress"

    def test_track_call_cache_hit(self):
        """TC-13: cache_hit=true recorded in per_file entry."""
        costs = init_costs()
        usage = {
            "input_tokens": 1000, "output_tokens": 500,
            "cache_read_input_tokens": 800, "cache_creation_input_tokens": 0,
        }
        track_call(costs, "compress", "file.md", usage, "claude-opus-4-6-20260204", cache_hit=True)
        assert costs["per_file"][0]["cache_hit"] is True

    def test_cache_miss_logs_warning(self, caplog):
        """TC-29/EC-10: Warning with cost delta on non-first call cache miss."""
        costs = init_costs()
        usage = {"input_tokens": 1000, "output_tokens": 500}
        # First call - no warning
        track_call(costs, "compress", "a.md", usage, "claude-opus-4-6-20260204", cache_hit=False)

        # Second call - should warn about cache miss
        with caplog.at_level(logging.WARNING, logger="lib.cost_tracker"):
            track_call(costs, "compress", "b.md", usage, "claude-opus-4-6-20260204", cache_hit=False)
        assert any("Cache miss" in r.message for r in caplog.records)


class TestSaveCosts:
    """TK-007: Atomic cost saving."""

    def test_save_costs_atomic(self, tmp_run_dir):
        """TC-14: File exists, no partial writes (.tmp cleaned up)."""
        costs = init_costs()
        costs["total_cost"] = 1.5
        path = save_costs(costs, tmp_run_dir)
        assert path is not None
        assert path.exists()
        assert not (tmp_run_dir / "run_costs.json.tmp").exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["total_cost"] == 1.5

    def test_save_costs_write_failure(self, tmp_path, caplog):
        """TC-27/EC-08: Logs error, continues (returns None)."""
        # Use non-existent nested path that can't be created
        bad_dir = tmp_path / "nonexistent"
        with caplog.at_level(logging.ERROR, logger="lib.cost_tracker"):
            result = save_costs(init_costs(), bad_dir)
        assert result is None
        assert any("Failed to save" in r.message for r in caplog.records)

    def test_load_costs_roundtrip(self, tmp_run_dir):
        """Load returns what was saved."""
        costs = init_costs()
        costs["total_cost"] = 2.75
        costs["api_calls"] = 5
        save_costs(costs, tmp_run_dir)
        loaded = load_costs(tmp_run_dir)
        assert loaded["total_cost"] == 2.75
        assert loaded["api_calls"] == 5

    def test_load_costs_missing(self, tmp_run_dir):
        """Missing file returns fresh init_costs."""
        loaded = load_costs(tmp_run_dir)
        assert loaded["total_cost"] == 0.0
        assert loaded["api_calls"] == 0


class TestCheckBudget:
    """TK-007: Budget checking."""

    def test_check_budget_warning(self):
        """TC-15: Warning at 80% threshold."""
        costs = {"total_cost": 85.0}
        config = {"budget": {"max_total_usd": 100.0, "warning_threshold": 0.8}}
        ok, msg = check_budget(costs, config)
        assert ok is True
        assert "warning" in msg.lower()

    def test_check_budget_exceeded(self):
        """Budget exceeded returns ok=False."""
        costs = {"total_cost": 105.0}
        config = {"budget": {"max_total_usd": 100.0, "warning_threshold": 0.8}}
        ok, msg = check_budget(costs, config)
        assert ok is False
        assert "exceeded" in msg.lower()

    def test_check_budget_ok(self):
        """Under threshold returns ok=True, empty message."""
        costs = {"total_cost": 10.0}
        config = {"budget": {"max_total_usd": 100.0, "warning_threshold": 0.8}}
        ok, msg = check_budget(costs, config)
        assert ok is True
        assert msg == ""
