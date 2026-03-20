"""Tests for compare_runs (TK-015)."""
import json

import pytest
from compare_runs import load_run_data, compare_runs, format_comparison


class TestLoadRunData:
    """TK-015: Load run data."""

    def test_load_existing_run(self, tmp_path):
        """TC-30: Loads config, costs, summary from run dir."""
        run_dir = tmp_path / "runs" / "20260320-1430-test"
        run_dir.mkdir(parents=True)
        (run_dir / "run_config.json").write_text(
            json.dumps({"run_id": "20260320-1430-test", "models": {"mother": "claude-opus-4-6"}}),
            encoding="utf-8",
        )
        (run_dir / "run_costs.json").write_text(
            json.dumps({"total_cost": 1.5, "api_calls": 10, "total_input_tokens": 5000,
                        "total_output_tokens": 2000, "total_cache_read_tokens": 3000}),
            encoding="utf-8",
        )
        data = load_run_data(run_dir)
        assert data["config"]["run_id"] == "20260320-1430-test"
        assert data["costs"]["total_cost"] == 1.5

    def test_load_nonexistent_run(self, tmp_path):
        """TC-31: FileNotFoundError for missing run dir."""
        with pytest.raises(FileNotFoundError, match="not found"):
            load_run_data(tmp_path / "nonexistent")

    def test_load_run_missing_files(self, tmp_path):
        """Missing costs/config files return empty dicts."""
        run_dir = tmp_path / "runs" / "empty-run"
        run_dir.mkdir(parents=True)
        data = load_run_data(run_dir)
        assert data["config"] == {}
        assert data["costs"] == {}


class TestCompareRuns:
    """TK-015: Run comparison logic."""

    def test_compare_cost_regression(self):
        """TC-32: Detects cost regression."""
        run_a = {"run_id": "run-a", "costs": {
            "total_cost": 1.0, "total_input_tokens": 5000,
            "total_output_tokens": 2000, "total_cache_read_tokens": 0, "api_calls": 5,
        }}
        run_b = {"run_id": "run-b", "costs": {
            "total_cost": 2.0, "total_input_tokens": 8000,
            "total_output_tokens": 3000, "total_cache_read_tokens": 0, "api_calls": 8,
        }}
        result = compare_runs(run_a, run_b)
        assert result["cost_delta"] > 0
        assert len(result["regressions"]) > 0
        assert any("Cost increased" in r for r in result["regressions"])

    def test_compare_cost_improvement(self):
        """Detects cost improvement."""
        run_a = {"run_id": "run-a", "costs": {
            "total_cost": 2.0, "total_input_tokens": 8000,
            "total_output_tokens": 3000, "total_cache_read_tokens": 0, "api_calls": 8,
        }}
        run_b = {"run_id": "run-b", "costs": {
            "total_cost": 1.0, "total_input_tokens": 5000,
            "total_output_tokens": 2000, "total_cache_read_tokens": 3000, "api_calls": 5,
        }}
        result = compare_runs(run_a, run_b)
        assert result["cost_delta"] < 0
        assert any("Cost decreased" in i for i in result["improvements"])
        assert any("Cache utilization improved" in i for i in result["improvements"])

    def test_compare_identical_runs(self):
        """No regressions or improvements for identical runs."""
        costs = {"total_cost": 1.0, "total_input_tokens": 5000,
                 "total_output_tokens": 2000, "total_cache_read_tokens": 0, "api_calls": 5}
        run_a = {"run_id": "run-a", "costs": costs}
        run_b = {"run_id": "run-b", "costs": costs.copy()}
        result = compare_runs(run_a, run_b)
        assert result["cost_delta"] == 0
        assert len(result["regressions"]) == 0
        assert len(result["improvements"]) == 0

    def test_format_comparison(self):
        """Format produces readable output."""
        comparison = {
            "run_a": "run-a", "run_b": "run-b",
            "cost_delta": 0.5, "cost_delta_pct": 50.0,
            "token_delta": 1000,
            "regressions": ["Cost increased"],
            "improvements": [],
        }
        text = format_comparison(comparison)
        assert "run-a" in text
        assert "run-b" in text
        assert "Regressions" in text
