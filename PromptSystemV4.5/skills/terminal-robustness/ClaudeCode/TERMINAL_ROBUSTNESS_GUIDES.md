# Terminal Robustness Guide (ClaudeCode)

Minimum variant for Claude Code. Generic, verified patterns only - no claims about Claude Code tool internals (no empirical findings exist for this agent). Load together with the shared guide.

## 1. Scope

Only patterns that hold for any terminal tool on Windows/POSIX:

- The three OS-level mechanisms from the shared guide apply (pipe backpressure, handle inheritance, shell stream merge)
- What is NOT known for Claude Code: how its Bash tool drains streams, whether it waits for pipe EOF, its timeout and kill-on-cancel semantics. Do not assume - apply the safe patterns below and observe

## 2. Safe patterns (apply always)

1. **Redirect verbose output to files** - run from a script, redirect stdout/stderr to `.tmp_` files, read files with the file tool. Defeats backpressure, merge corruption, and handle inheritance in one step
2. **Non-interactive flags** - `--yes`, `--no-pager`, `--ci`, `-NonInteractive`; git log/diff/show always `--no-pager` and `-n <N>`
3. **No stdin/pager/key waits** - ban `Read-Host`, `pause`, `Get-Credential`, REPLs without input, `Get-Content -Wait`, `tail -f`
4. **No unbounded background children** - ban `--watch` flags, `Wait-Process` without `-Timeout`; stop spawned processes after use
5. **`rg.exe` over recursive shell enumeration** on large trees
6. **Time caps** on every process-running command; on cap: kill the process tree, record in PROBLEMS.md, continue
7. **Timeout wrapper** for commands without native safe parameters: `Start-Process -PassThru -RedirectStandardOutput/.tmp_x.txt -RedirectStandardError/.tmp_x_err.txt` + `WaitForExit(cap_ms)` + recursive `Stop-ProcessTree` on timeout

## 3. Card usage

Copy `ClaudeCode/ROBUSTNESS_CARD_TEMPLATE.md` to the project root as `__CARD_[TOPIC]-Robustness.md`, extend, and follow it. `/verify` checks it against `ROBUSTNESS_CARD_SKELETON.md`.

## 4. Observation duty

When a command hangs or behaves unexpectedly under Claude Code, record the observation (command, what happened, kill method used) in the card's Findings Feed. These observations are the raw material for a future ClaudeCode full-findings variant.
