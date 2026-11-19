# Terminal Robustness Skill Setup

One-time setup for the supervised runner `run-supervised.ps1`: installs `processkit` (Job Object container) into the shared venv. Without it the runner still works but falls back to `Kill($true)` and logs a `WARN` line (misses orphaned grandchildren, HANGBENCH 25/27 instead of 27/27).

## Agent Self-Repair Trigger

Run this procedure without asking when a runner log contains `WARN processkit not found`. The install is idempotent and adds one pinned package to the shared venv; it changes no configuration file. After success: delete the pending PROBLEMS.md entry for the missing processkit (or do not create it), and tell the user in one line. Failure at any step: stop, create one PROBLEMS.md entry with the failing step and its output, continue with the fallback runner.

The agent runs every command of this procedure through the supervised runner (`agent-behavior.md` Terminal Hang Prevention): steps 2 and 3 use the network.

## Pre-Installation Verification

Read-only; nothing is modified.

1. Venv `pip` exists: step 1 prints `True`
2. processkit state: step 2 prints either the installed version or `not installed`
3. Pinned version exists on the package index: step 3 lists `1.5.0`
4. No runner is active: step 4 prints no `processkit` process (an active runner locks `processkit.exe` and the install fails)

Pre-Installation Checklist:
- [ ] Venv `pip.exe` found
- [ ] Current processkit state known
- [ ] Version `1.5.0` listed on the index
- [ ] No running `processkit` process

## 1. Set Paths

```powershell
$venvScripts = "[SKILL_TOOLS_FOLDER]\llm-venv\Scripts"
Test-Path "$venvScripts\pip.exe"
```

`False` -> the shared venv is missing: create it per @skills:llm-tools `SETUP.md`, then repeat. Never install into the system Python.

## 2. Check Current State

```powershell
& "$venvScripts\pip.exe" show processkit-py --disable-pip-version-check
Test-Path "$venvScripts\processkit.exe"
```

`pip show` exit code 1 means not installed (not an error). Installed with `Version: 1.5.0` and `processkit.exe` present -> setup is done, skip to step 5.

## 3. Check the Pinned Version

```powershell
& "$venvScripts\pip.exe" index versions processkit-py --disable-pip-version-check
```

Expected: `1.5.0` in the version list. Version `1.5.0` is the one tested in HANGBENCH (`DevinCascade/TERMINAL_ROBUSTNESS_GUIDES.md` Section 3); do not use a newer version without re-running the runner contract tests.

## 4. Check for Running processkit

```powershell
Get-Process processkit -ErrorAction SilentlyContinue | Select-Object Id, StartTime
```

Expected: no output. A listed process belongs to a running runner call: wait for its end line in the runner log, never kill it.

## 5. Install

```powershell
& "$venvScripts\pip.exe" install processkit-py==1.5.0 --disable-pip-version-check --progress-bar off --no-color
```

The two extra flags keep progress-bar control characters out of `_out.txt`; without them `read_file` can fail to decode the file.

Expected: `Successfully installed processkit-py-1.5.0` (or `Requirement already satisfied`).

## 6. Verify

Runner smoke test: create `_agentwork/.tmp_pkverify_[HHmmss].ps1` containing `Write-Output 'processkit ok'`, then run it with the runner (`-Expected 10`).

Expected:
- `.tmp_pkverify_[HHmmss]_log.txt` contains `START` and `DONE exit=0`, and NO `WARN` line
- `.tmp_pkverify_[HHmmss]_out.txt` contains `processkit ok`

A `WARN` line remains -> `Test-Path "$venvScripts\processkit.exe"` is `False`: pip installed into another environment. Re-run step 5 with the explicit `pip.exe` path of step 1.

Delete the smoke-test script and its outputs afterwards.
