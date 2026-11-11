# Test Example 01: Robustness Card

Demonstrates a robustness card for test execution in agentic prompt sequences. Every implementation prompt loads this card to prevent agent hangs and process leaks.

## Context

An agentic workflow runs a test suite of 150+ tests across 16 categories. Tests spawn subprocesses, make mock HTTP calls, and write to disk. Without explicit hang prevention, agents wait indefinitely on stuck commands, burning API tokens on idle context windows.

The robustness card is a standalone document referenced by every prompt's hang-safety clause. It encodes four sections: banned commands, expected runtimes, always rules, and agent tool limits. Monitoring and failure recording are not card content: a run that shows progress runs to its end, the agent ends a run only on a hang verdict, and failures go to the Fails card (`agent-behavior.md` Terminal Hang Prevention).

## Document

```markdown
# Robustness Card: [PROJECT]

## Banned commands

- `| Select-Object` on test or product run output (buffers indefinitely, appears to hang)
- `Read-Host`, `pause`, `Get-Credential`, `Get-Content -Wait` (wait on stdin or stream forever)
- `git log`, `git diff`, `git show` without `--no-pager`; `git commit` without `-m`
- `2>&1` combined with blocking execution (PowerShell pipe deadlock); redirect stderr to a file instead
- `pytest` without a file scope in implementation prompts (full suite only in final verification)
- `pytest -m nightly` outside the final verification phase
- Any live API call in implementation phases (mock transport only)

## Expected runtimes

- Single test file: 60 s; none (passed as `-Expected` to the runner; starts the liveness check, never a kill limit)
- Full suite: 300 s; no output for up to 60 s during collection
- Nightly: 600 s; none
- Git operations: 10 s; `git push`: 20 s; none

## Always rules

- Tests: `[PYTHON] -m pytest <files> -q -x --no-header -p no:cacheprovider` inside a tmp script through the runner
- Default test command (final verification only): `python -m pytest tests/ --no-header -p no:cacheprovider -q -n auto` in `[SKILL_FOLDER]`
- After every test or product run: `Get-Process python* -ErrorAction SilentlyContinue` filtered to
  the venv path returns nothing; strays are stopped and recorded in the Fails card

## Agent tool limits

[verbatim copy of the executing agent's Tool-Call Payload Limit section]
```

## Key Decisions

- **Four fixed sections (Banned commands, Expected runtimes, Always rules, Agent tool limits)**: The structure matches `ROBUSTNESS_CARD_SKELETON.md` of the terminal-robustness skill. Agents know where to find each type of constraint without reading the whole card.
- **Banned commands are stack-specific**: Each project adds its own banned commands based on observed hangs. The examples above are PowerShell/pytest-specific. A Node.js project would ban different commands.
- **Expected runtimes, not limits**: A run that needs longer than expected and still shows progress runs to its end; ending it would throw away the finished part and force a second run. The values tell the agent when to start looking at the liveness signals, and the silent-phase note tells it when silence is normal.
- **No kill section**: the hang verdict and the stop file are defined in `agent-behavior.md` Terminal Hang Prevention. A card that restates this procedure drifts from the rule.
- **Default test command recorded once**: Every prompt uses the same invocation from this card. No drift between prompts on flag usage.
- **Generic placeholders `[PYTHON]`, `[SKILL_FOLDER]`, `[PROJECT]`**: The card uses workspace constants so it works across environments without hardcoded paths.
