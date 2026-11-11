# Terminal Robustness Guide (DevinCascade)

Full-findings variant for Devin/Cascade (Windsurf terminal tool). Load together with the shared guide. Every mechanism is empirically confirmed in the IPPS terminal-robustness investigation; evidence cited inline by log entry ID (`@I001.xxx`). Provenance and evidence sources: `specs/_SPEC_TERMINAL_ROBUSTNESS_SKILL.md` Section 8.

## 1. Confirmed Tool Behavior

### 1.1 The tool waits for pipe EOF on all streams, not child exit

The terminal tool returns when stdout AND stderr reach EOF, not when the direct child exits. Confirmed: parent exited in 1s, tool returned only at grandchild death (~43s later) [@I001.012, @I001.013].

Consequences:
- Background grandchildren inheriting pipe write handles (dev servers, watchers, `start /b` helpers) hang the terminal indefinitely
- Killing the parent does not help - the orphan holds the pipe open
- User cancel may not kill the process tree (GLOB-FL-0005 evidence: killed by PID after two ineffective cancels)

### 1.2 Un-merged stderr drains at ~2.3KB/s against a ~4KB buffer

Without `2>&1`, the tool drains the stderr pipe at roughly 2.3KB/s. A command writing 1MB of stderr takes ~7 minutes to drain - an apparent hang with the process alive and merely blocked [@I001.014, @I001.015]. Exit code stays intact. npm/pip/compiler output routinely exceeds 4KB.

### 1.3 `2>&1` makes pwsh the merge point - OOM or backpressure

With `2>&1`, pwsh must drain child stderr at full speed, wrap records as red-ANSI ErrorRecords, and re-emit at the tool's pace. Observed with a 1MB stderr flood: pwsh OutOfMemoryException, exit code 1 reported for a child that exited 0 [@I001.016, @I001.017]. Inferred variant (Hera HERAV1HRNS-FL-0001): backpressure hang. Small stderr merges cleanly but ANSI-wrapped and ~2x slower [@I001.009, M1/M3].

### 1.4 Long command lines echo mangled

Long commands echo duplicated and char-truncated in the tool output - observed live three times [@I001.011, @I001.025]. Cosmetic but misleading: do not parse the echo to verify what ran; check artifacts on disk instead.

### 1.5 stdin/pager waits behave as everywhere

`Read-Host`, `pause`, pagers, REPLs without input, `Get-Content -Wait` block until input or EOF - same as any terminal (generic rule, not tool-specific).

### 1.6 Completion detection is unreliable in both directions [TESTED 2026-11-11]

The tool missed the end of a finished sub-second command (1 of 13 live probes; the command had written its `DONE` line) and once reported DONE for a command that was still running (process list and growing files showed it). A `Blocking: true` call that misses completion waits forever. Defense: rule `devin-cascade.md` Terminal Limits (non-blocking call with timer, completion from the runner log).

### 1.7 Terminals are shared between concurrent conversations [TESTED 2026-11-11]

Tool output of one conversation contained the command line another Cascade conversation had run seconds before in the same shell-integration `pwsh` process. A command waiting on stdin can receive the other conversation's input. Defense: the runner gives the script an empty stdin file.

### 1.8 `>` redirect buffers output [TESTED 2026-11-11]

`script > out.txt` left `out.txt` empty for the whole run when output was small (10 lines in 10 s); larger output appears in blocks. Since PowerShell 7.4, pwsh reads the native child's stream and writes the file itself. Live output needs a file handle given to the child at start (`Start-Process -RedirectStandardOutput`, used by the runner); Python additionally needs `PYTHONUNBUFFERED=1` (set by the runner).

## 2. Confirmed Mitigation: tmp script + supervised runner + read_file

The work goes into a `_agentwork/.tmp_*.ps1`/`.py` script; `run-supervised.ps1` runs it (call line: `agent-behavior.md` Terminal Hang Prevention). All output goes to files, not the tool's pipes: no 4KB limit, no 2.3KB/s throttle, no merge point, no out-of-memory (OOM) error [@I001.019]. processkit puts the whole tree into a Windows Job Object: the stop file the agent creates after a hang verdict kills every descendant, and descendants cannot outlive the script, so the tool's pipes reach EOF. The runner has no deadline. Tmp script skeleton:

```powershell
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
# work here: absolute paths, non-interactive flags; existing project scripts are called unchanged
```

## 3. Supervised Runner Evidence `[TESTED 2026-11-11]`

HANGBENCH (`_Sessions/!TerminalHangBench/` in IPPS, not synced; 27 cases: input waits, unbounded waits, network and lock waits, pipe-holding grandchildren, orphans whose parent exited, output floods, legit long runs, cancel of the top process). Latest run `runner5` (runner without deadline, with kill script; the harness plays the agent: it creates the stop file after 5 s in hang cases and runs the kill script after the cancel in HC-27):
- `run-supervised.ps1` with processkit: 27/27. Input waits end after about 1.3 to 2.9 s (empty stdin); the stop file ends the other hangs within 1 s, including the orphan whose parent exited (HC-21) and the 3-level tree (HC-20); no legitimate case is ended
- Cancel of the runner itself (HC-27): the runner cannot act after its own death. Without the kill script the process tree stayed alive (run `runner3`: 7 survivors, 3 of 3 repeats; `--kill-on-parent-death` without `--timeout` did not end it [cause not verified]). With the kill script run after the cancel: 0 survivors. The pass therefore depends on the agent or the user running `.tmp_kill_[TOPIC].ps1` (`agent-behavior.md` Terminal Hang Prevention step 8)
- `run-supervised.ps1` fallback without processkit (`Kill($true)`): 25/27; misses a grandchild holding the pipe after the script exits (HC-11) and an orphan whose parent exited (HC-21). Install processkit to close these gaps
- Superseded pattern (former tier 2: `Start-Process` + `WaitForExit` + recursive CIM `Stop-ProcessTree`): 24/27; misses pipe-holding grandchildren and orphans, needed up to 18 s to end a tree after a 5 s limit
- Former tier 1 (tmp script + `-NonInteractive` + `>` redirect, no supervisor): 8/27; stops only `Read-Host`
- Runner contract tests (`runner-tests.ps1`): 14/14 - kill script holds the tree's process IDs while the command runs, the next runner call logs `LEFTOVER` after a cancelled runner, the kill script ends the survivors, the file is deleted when empty, `-Topic` gives each topic its own kill script in one folder; `ERROR` line with exit 2 for a missing script and a missing interpreter, non-ASCII output decodes as UTF-8 (PowerShell and Python), exit codes propagate, `KILLED exit=124` with the reason after the stop file, 7 s of work with 2 s expected runs to `DONE` and logs `ALIVE` lines, a script exiting with its own code 124 is `DONE`, live Python output before exit, paths with spaces, fallback `WARN` line; also passes when the runner itself runs inside another runner (nested Job Objects)

Gotchas kept from the former pattern `[TESTED]`:
- `Start-Process -ArgumentList` joins arguments without quoting and strips double quotes - the runner quotes every argument itself
- PowerShell `Write-Error` writes to the error stream, not OS stderr; `[Console]::Error.WriteLine()` writes real stderr

## 4. Non-Blocking Calls and Polling

Rule: `devin-cascade.md` Terminal Limits. Reason: section 1.6. Polling reads the runner log, not `command_status` output.

## 5. Liveness During Long Runs

`_out.txt` grows live under the runner (section 1.8). No growth during a known silent phase is normal. The `ALIVE` lines in the runner log (`cpu=`, `out=`, `err=` every 30 s) show whether a silent process works; reading them and the hang verdict: shared guide Section 7. Nothing ends a command automatically.

## 6. Card Usage

Copy `DevinCascade/ROBUSTNESS_CARD_TEMPLATE.md` to `_agentwork/__CARD_[TOPIC]-Robustness.md` of the current working folder, extend with project bans and expected runtimes, follow it. Run failures go to the Fails card (`ROBUSTNESS_CARD_SKELETON.md`).
