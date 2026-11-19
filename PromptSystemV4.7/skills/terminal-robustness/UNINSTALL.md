# Terminal Robustness Skill Uninstall

Removes what SETUP.md installed: the `processkit-py` package in the shared venv. The skill modifies no configuration file. The runner keeps working afterwards with the `Kill($true)` fallback (logs `WARN processkit not found`).

## Pre-Uninstall Verification

Read-only; nothing is removed.

1. Installed state:

```powershell
& "[SKILL_TOOLS_FOLDER]\llm-venv\Scripts\pip.exe" show processkit-py --disable-pip-version-check
```

Expected: `Version: 1.5.0`. Exit code 1 means nothing to remove: stop here.

2. No running runner (an active runner locks `processkit.exe`):

```powershell
Get-Process processkit -ErrorAction SilentlyContinue | Select-Object Id, StartTime
```

Expected: no output. A listed process belongs to a running command: wait for its `DONE`, `KILLED`, or `ERROR` log line first.

3. Leftover kill scripts: `Get-ChildItem -Recurse -Force -Filter ".tmp_kill*.ps1" "[WORKSPACE_FOLDER]"` lists scripts of cancelled runners (recursive search: the agent runs it through the supervised runner). Run them before removing processkit (`pwsh -NoProfile -File [path]`), so leftover processes end.

4. Other users of processkit: other skills use no processkit; only `run-supervised.ps1` references it.

Pre-Uninstall Checklist:
- [ ] processkit installed, version noted
- [ ] No running `processkit` process
- [ ] Leftover kill scripts executed or none found

If all checks pass, proceed.

## 1. Remove the Package

```powershell
& "[SKILL_TOOLS_FOLDER]\llm-venv\Scripts\pip.exe" uninstall processkit-py -y --disable-pip-version-check
```

## 2. Remove the Skill Files (only for a full skill removal)

Delete `[AGENT_FOLDER]\skills\terminal-robustness\`. Also remove the rule text that depends on it: `agent-behavior.md` section Terminal Hang Prevention and `tools-and-skills.md` entry `processkit`. In a PromptSystem workspace, delete in `[PROMPTSYSTEM_FOLDER]` first (source of truth), then mirror to `[AGENT_FOLDER]`.

## Post-Uninstall Verification

```powershell
Test-Path "[SKILL_TOOLS_FOLDER]\llm-venv\Scripts\processkit.exe"
& "[SKILL_TOOLS_FOLDER]\llm-venv\Scripts\pip.exe" show processkit-py --disable-pip-version-check
```

Expected: `False`, and `pip show` reports `Package(s) not found` (exit code 1). With the skill files kept: the next runner call logs `WARN processkit not found` and still ends with `DONE`.

Manual cleanup: none. Do not self-repair after an intentional uninstall: record the decision in workspace NOTES.md so the agent skips SETUP.md on the `WARN` line.
