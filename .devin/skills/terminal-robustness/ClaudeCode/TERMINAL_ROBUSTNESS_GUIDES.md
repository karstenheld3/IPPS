# Terminal Robustness Guide (ClaudeCode)

Minimum variant for Claude Code. Generic, verified patterns only - no claims about Claude Code tool internals (no empirical findings exist for this agent). Load together with the shared guide.

## 1. Scope

Only patterns that hold for any terminal tool on Windows/POSIX:

- The three OS-level mechanisms from the shared guide apply (pipe backpressure, handle inheritance, shell stream merge)
- What is NOT known for Claude Code: how its Bash tool drains streams, whether it waits for pipe EOF, its timeout and kill-on-cancel semantics. Do not assume - apply the safe patterns below and observe

## 2. Safe patterns (apply always)

1. **Supervised runner for every non-whitelisted command** - call line and completion rule: `agent-behavior.md` Terminal Hang Prevention. The runner (`run-supervised.ps1`, PowerShell 7) works with any terminal tool: output goes to files; liveness lines, stop file, and tree kill do not depend on the tool
2. **Non-interactive flags** - `--yes`, `--no-pager`, `--ci`, `-NonInteractive`; git log/diff/show always `--no-pager` and `-n <N>`
3. **No stdin/pager/key waits** - ban `Read-Host`, `pause`, `Get-Credential`, REPLs without input, `Get-Content -Wait`, `tail -f`
4. **No unbounded background children** - ban `--watch` flags, `Wait-Process` without `-Timeout`; stop spawned processes after use
5. **`rg.exe` over recursive shell enumeration** on large trees
6. **Monitor, never cut off** - expected runtimes from the project card go to the runner as `-Expected`; a command that shows progress runs to its end, only a hang verdict ends it (shared guide Section 7). If the Bash tool has its own timeout, start long commands in the background so the tool timeout cannot end them

## 3. Card usage

Copy `ClaudeCode/ROBUSTNESS_CARD_TEMPLATE.md` to `_agentwork/__CARD_[TOPIC]-Robustness.md` of the current working folder, extend, and follow it. `/verify` checks it against `ROBUSTNESS_CARD_SKELETON.md`.

## 4. Observation duty

When a command hangs or behaves unexpectedly under Claude Code, record the observation (command, what happened, runner log line) in the Fails card of the working folder (created at the first failure). These observations are the raw material for a future ClaudeCode full-findings variant.
