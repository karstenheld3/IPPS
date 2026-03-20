"""Tests for mipps_pipeline.py CLI (TC-25 to TC-28 from IMPL)."""
import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Base directory for the pipeline
BASE_DIR = Path(__file__).parent.parent


def _run_cli(*args, expect_fail=False):
    """Run mipps_pipeline.py with given args, return (stdout, returncode)."""
    result = subprocess.run(
        [sys.executable, str(BASE_DIR / "mipps_pipeline.py"), *args],
        capture_output=True, text=True, cwd=str(BASE_DIR),
        timeout=30,
    )
    if not expect_fail:
        assert result.returncode == 0, f"CLI failed: {result.stderr}\n{result.stdout}"
    return result.stdout, result.returncode


class TestCLIBundle:
    """TC-25: bundle command."""

    def test_bundle_creates_output(self, tmp_path):
        """TC-25: bundle --source-dir [path] -> creates bundle file and state."""
        # Create a small source dir
        source = tmp_path / "source"
        (source / "rules").mkdir(parents=True)
        (source / "rules" / "core.md").write_text("# Core\nRule 1\n" * 10, encoding="utf-8")
        (source / "rules" / "extra.md").write_text("# Extra\nRule 2\n" * 5, encoding="utf-8")

        stdout, rc = _run_cli("bundle", "--source-dir", str(source))

        assert "Bundle created" in stdout
        assert "2 files" in stdout
        # Verify state was updated
        state_path = BASE_DIR / "pipeline_state.json"
        if state_path.exists():
            state = json.loads(state_path.read_text(encoding="utf-8"))
            assert state["current_step"] >= 1
            # Cleanup
            state_path.unlink()
        # Cleanup bundle
        bundle_path = BASE_DIR / "context" / "all_files_bundle.md"
        if bundle_path.exists():
            bundle_path.unlink()
            bundle_path.parent.rmdir()


class TestCLIStatus:
    """TC-26: status command."""

    def test_status_displays_progress(self):
        """TC-26: status with existing state -> displays current_step, files, cost."""
        # Create a state file
        state_path = BASE_DIR / "pipeline_state.json"
        state = {
            "current_step": 3, "iteration": 1,
            "files_total": 50, "files_compressible": 40,
            "files_excluded": 10, "files_compressed": 20,
            "files_passed": 18, "files_failed": 2,
            "files_excluded_md": 10, "files_completed": [],
            "broken_references": 0,
            "cost": {"mother_input": 5.0, "mother_output": 30.0,
                     "verification_input": 0.5, "verification_output": 0.3, "total": 35.8},
        }
        state_path.write_text(json.dumps(state), encoding="utf-8")

        try:
            stdout, rc = _run_cli("status")
            assert "Step: 3" in stdout
            assert "Complexity map done" in stdout
            assert "20/50" in stdout
            assert "$35.80" in stdout
        finally:
            state_path.unlink(missing_ok=True)


class TestCLICompressPrereq:
    """TC-27: compress without prior bundle."""

    def test_compress_without_bundle_fails(self):
        """TC-27: compress without prior bundle -> exits with error about prerequisites."""
        # Ensure no state exists (or state with step 0)
        state_path = BASE_DIR / "pipeline_state.json"
        state_path.write_text(json.dumps({"current_step": 0}), encoding="utf-8")

        try:
            stdout, rc = _run_cli("compress", expect_fail=True)
            assert rc != 0 or "Run 'generate' first" in stdout
        finally:
            state_path.unlink(missing_ok=True)


class TestCLIIteratePrereq:
    """TC-28: iterate without report."""

    def test_iterate_without_report_fails(self):
        """TC-28: iterate without report -> exits with error or auto-runs verify."""
        state_path = BASE_DIR / "pipeline_state.json"
        state_path.write_text(json.dumps({"current_step": 5}), encoding="utf-8")
        report_path = BASE_DIR / "_04_FILE_COMPRESSION_REPORT.md"
        report_path.unlink(missing_ok=True)

        try:
            # iterate will try to run verify first (EC-07), which requires step 6
            # So it should fail with prerequisite error
            stdout, rc = _run_cli("iterate", expect_fail=True)
            assert rc != 0 or "Run" in stdout
        finally:
            state_path.unlink(missing_ok=True)
