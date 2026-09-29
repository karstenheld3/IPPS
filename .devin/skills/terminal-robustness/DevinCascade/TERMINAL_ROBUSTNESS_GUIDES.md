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

Long commands echo duplicated and char-truncated in the tool output - observed live twice [@I001.011]. Cosmetic but misleading: do not parse the echo to verify what ran; check artifacts on disk instead.

### 1.5 stdin/pager waits behave as everywhere

`Read-Host`, `pause`, pagers, REPLs without input, `Get-Content -Wait` block until input or EOF - same as any terminal (generic rule, not tool-specific).

## 2. Confirmed Mitigation: tmp-script + redirect + read_file

Run the command from a `.tmp_*.ps1`/`.py` script, redirect ALL output to files, then read the files with `read_file`. The child's handles point at files, not the tool's pipes: no 4KB limit, no 2.3KB/s throttle, no merge point, no OOM, and grandchildren inherit file handles - the tool's pipes EOF at parent exit [@I001.019]. This is the default pattern for anything writing more than a few KB.

## 3. Timeout Execution Pattern (tier 2) `[TESTED]`

For commands with no native safe parameter (locked files, network risk):

```powershell
function Stop-ProcessTree {
  param([int]$ProcessId)
  $children = Get-CimInstance Win32_Process | Where-Object { $_.ParentProcessId -eq $ProcessId }
  foreach ($child in $children) { Stop-ProcessTree -ProcessId $child.ProcessId }
  try { Stop-Process -Id $ProcessId -Force } catch {}
}

$proc = Start-Process -FilePath "pwsh" -ArgumentList "-NoProfile","-Command", "<command>" -PassThru -NoNewWindow -RedirectStandardOutput ".tmp_cmd_stdout.txt" -RedirectStandardError ".tmp_cmd_stderr.txt"
if (-not $proc.WaitForExit(<cap_ms>)) {
  Stop-ProcessTree -ProcessId $proc.Id
  Write-Output "TIMEOUT: <command> exceeded <cap> cap"
} else {
  (Get-Content ".tmp_cmd_stdout.txt" -Raw) ?? ''
}
```

Why each property `[TESTED]`:
- Recursive tree kill: recurses children and grandchildren; `Stop-Job` does not kill children; flat CIM queries miss grandchildren
- No pipe deadlock: stderr to file via `-RedirectStandardError`, never `2>&1`
- Self-contained: timeout + kill + record in one block, no agent cooperation needed
- Null-safe output: `Get-Content -Raw` returns `$null` on empty files - use `?? ''`
- Dead-PID safe: `try/catch` handles processes that exit between timeout and kill
- Direct kill, no SIGTERM escalation: the process is already hung - a grace period only delays and risks re-hang during cleanup. Contrast: the general on-cap pattern in `PROMPTS_ROBUSTNESS_GUIDES.md` Section 6.2 escalates SIGTERM -> SIGKILL for processes that may still exit cleanly

Gotchas `[TESTED]`:
- `Start-Process -ArgumentList` strips double quotes inside `-Command` - use single quotes (doubled inside single-quoted strings)
- PowerShell `Write-Error` writes to the error stream, not OS stderr; `[Console]::Error.WriteLine()` writes real stderr
- Orphaned children (parent exited fast, e.g. `cmd /c start /b`) cannot be found via ParentProcessId - sweep by command-line pattern instead

## 4. Non-Blocking Execution with Polling

The tool supports non-blocking execution (`WaitMsBeforeAsync` / background mode) with status polling. Prefer it for anything possibly slow: start non-blocking, poll the command status with short waits (cap total wait time), kill the tree on cap. Polling shows liveness; blind blocking does not.

## 5. Liveness Checks for Zero-Progress Long Runs

A process blocked on a full pipe is alive but produces nothing - blind polling cannot distinguish it from progress [@I001.015]. For long runs: estimate duration before start, redirect output to file (buffering-safe), use `Get-Process` CPU as a liveness signal, and prefer `python -u` / `$env:PYTHONUNBUFFERED` for Python output written to files.

## 6. Card Usage

Copy `DevinCascade/ROBUSTNESS_CARD_TEMPLATE.md` to the project root as `__CARD_[TOPIC]-Robustness.md`, extend, follow it. The card absorbs the `[TESTED]` defaults from this variant; prompts reference the card instead of repeating patterns.
