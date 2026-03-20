"""Tests for run manager: folder creation, config snapshot, summary (TK-006)."""
import json
from pathlib import Path

import pytest
from lib.run_manager import create_run, snapshot_config, generate_run_summary, RUN_SUBDIRS


class TestCreateRun:
    """TK-006: Run folder creation."""

    def test_create_run_folder_structure(self, tmp_path):
        """TC-06: All 8 subdirs exist (7 leaf dirs + prompts parent has 3)."""
        run_dir, run_id = create_run(tmp_path, "test")
        assert run_dir.exists()
        for subdir in RUN_SUBDIRS:
            assert (run_dir / subdir).exists(), f"Missing subdir: {subdir}"

    def test_create_run_id_collision(self, tmp_path):
        """TC-07: Appends -2 suffix on collision."""
        run_dir1, run_id1 = create_run(tmp_path, "dup")
        run_dir2, run_id2 = create_run(tmp_path, "dup")
        assert run_dir1 != run_dir2
        assert run_id2.endswith("-2")

    def test_create_run_missing_runs_dir(self, tmp_path):
        """TC-10/EC-05: Creates parent runs/ dir if missing."""
        base = tmp_path / "deep" / "nested"
        # runs/ doesn't exist yet
        run_dir, run_id = create_run(base, "auto")
        assert (base / "runs").exists()
        assert run_dir.exists()

    @pytest.mark.skipif(
        __import__("sys").platform == "win32",
        reason="Windows does not enforce Unix-style chmod permissions",
    )
    def test_create_run_read_only_dir(self, tmp_path):
        """TC-26/EC-07: Aborts with error on read-only dir."""
        import stat
        ro_dir = tmp_path / "readonly"
        ro_dir.mkdir()
        ro_dir.chmod(stat.S_IRUSR | stat.S_IXUSR)
        try:
            with pytest.raises(OSError):
                create_run(ro_dir, "fail")
        finally:
            ro_dir.chmod(stat.S_IRWXU)


class TestSnapshotConfig:
    """TK-006: Config snapshot."""

    def test_snapshot_config_fields(self, tmp_run_dir):
        """TC-08: run_id, started_at present in snapshot."""
        config = {"models": {"mother": "claude-opus-4-6-20260204"}}
        path = snapshot_config(config, tmp_run_dir, "20260320-1430-test")
        assert path.exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["run_id"] == "20260320-1430-test"
        assert "started_at" in data
        assert data["models"]["mother"] == "claude-opus-4-6-20260204"


class TestGenerateRunSummary:
    """TK-006: Run summary generation."""

    def test_generate_run_summary(self, tmp_run_dir):
        """TC-09: Compression ratio and cost sections in output."""
        state = {
            "files_total": 20,
            "files_compressed": 15,
            "files_excluded": 3,
            "files_excluded_md": 0,
            "files_failed": 2,
        }
        costs = {
            "total_cost": 1.2345,
            "per_file": [
                {"file": "a.md", "cost": 0.5, "cache_hit": True},
                {"file": "b.md", "cost": 0.7, "cache_hit": False},
            ],
        }
        path = generate_run_summary(tmp_run_dir, state, costs)
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "Compression" in content
        assert "75.0%" in content
        assert "Cost" in content
        assert "$1.2345" in content
        assert "Cache hit rate: 1/2" in content
