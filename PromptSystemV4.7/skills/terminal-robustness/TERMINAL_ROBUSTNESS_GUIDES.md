# Terminal Robustness Guide (Shared)

Read BEFORE running risky terminal commands. Agent-independent layer: OS-level mechanisms and the card system. Agent-specific behaviors live in the variant subfolder (`ClaudeCode/` or `DevinCascade/`) - see SKILL.md Agent Dispatch.

## 1. How Commands Hang (OS-Level Mechanisms)

Three mechanisms, independent of which terminal tool is in use:

### 1.1 Pipe-buffer backpressure

Every child process writes stdout/stderr into an OS pipe with a small buffer (~4KB on Windows anonymous pipes). If the reader (the terminal tool) drains slower than the child writes, the child blocks on write. A command producing 1MB of un-drained output at a slow drain rate looks like a hang while the process is alive and merely blocked.

### 1.2 Std-handle inheritance by grandchildren

A child that spawns background processes (dev servers, watchers, daemons, `start /b` helpers) hands them the pipe write handles. The parent exits, but the pipe does not reach EOF until every handle holder dies - so the tool that waits for stream EOF waits indefinitely. Killing only the parent does not help; the orphaned grandchild keeps the pipe open.

### 1.3 Shell stream-merge corruption

`2>&1` makes the shell the merge point: it must read child stderr at full speed, wrap records (PowerShell wraps them as ErrorRecords with ANSI color codes), and re-emit at the reader's pace. With large stderr this either backpressures into a hang or exhausts the shell's memory (PowerShell OutOfMemoryException) - and the reported exit code is wrong (observed: exit code 1 for a child that exited 0). Small stderr merges cleanly but slowly and mangled.

## 2. Why the Redirect Pattern Defeats All Three

The established mitigation - run the command from a `_agentwork/.tmp_*.ps1`/`.py` script, redirect ALL output to `_agentwork/.tmp_` files, then read the files with `read_file`:

- File handles have no 4KB pipe limit and no drain-rate throttle
- No shell merge point, no record wrapping, no merge OOM
- Grandchildren inherit file handles, not pipe write handles - the tool's pipes EOF at parent exit and the command returns immediately

This is mechanical, not folklore. Redirecting alone does not stop waits (input, network, locks, loops): the supervised runner `run-supervised.ps1` adds the Job Object container, empty stdin, liveness lines, and the whole-tree kill the agent triggers after a hang verdict (Section 7). Call line and completion rule: `agent-behavior.md` Terminal Hang Prevention.

## 3. Safe Command Patterns (Selection)

1. **Agent tools over shell** - grep_search, read_file, find_by_name for file operations; shell only for process execution
2. **Non-interactive flags** - `--yes`, `--no-pager`, `--ci`, `-NonInteractive`; git log/diff/show always with `--no-pager` and `-n <N>`
3. **Runner flags before `--`** - `npm create` / `npx` / `pnpm dlx` / `yarn create` are two-layer commands: the runner prompts on stdin ("Need to install ... Ok to proceed? (y)") before the scaffold tool starts, and everything after the `--` separator is forwarded to the tool, not the runner. Runner-level `--yes` must sit BEFORE `--`: `npm create --yes astro@latest . -- --template minimal` runs prompt-free; `npm create astro@latest . -- --template minimal --yes` still waits on stdin
4. **No stdin waits** - ban `Read-Host`, `pause`, `Get-Credential`, REPLs launched without input, `Get-Content -Wait`, `tail -f`
5. **No unbounded children** - ban `--watch` flags, `Wait-Process` without `-Timeout`; stop spawned processes after use
6. **Recursive enumeration** - prefer `rg.exe` (ripgrep, bundled with VS Code-based editors) over `Get-ChildItem -Recurse` / `Select-String -Recurse` on large trees
7. **Monitor, never cut off** - every non-whitelisted command runs through the runner; a command that shows progress runs to its end, and only a hang verdict ends it (rule: `agent-behavior.md` Terminal Hang Prevention steps 4 and 5)

## 4. The Robustness Card

A robustness card (`_agentwork/__CARD_[TOPIC]-Robustness.md` in the current working folder; `[WORKSPACE_FOLDER]/_agentwork/` in PROJECT-MODE) is the per-working-folder protection, kept until `/cleanup` deletes `_agentwork/`: project banned commands, expected runtimes, project always rules, agent tool limits. A Fails card (`_agentwork/__CARD_[TOPIC]-Fails.md`) is the failure memory of the same working folder, shared by chat tasks and prompt sequences and created at the first failure: "Never again" list and failure entries. Structure of both: `ROBUSTNESS_CARD_SKELETON.md`.

### 4.1 Card lifecycle

```
copy agent ROBUSTNESS_CARD_TEMPLATE.md
└─> name _agentwork/__CARD_[TOPIC]-Robustness.md in working folder
    └─> extend banned list + expected runtimes with project-specific entries
        ├─> chat mode: loaded before risky commands
        ├─> prompt sequences: hang-safety clause references the card
        ├─> /verify: instance checked against ROBUSTNESS_CARD_SKELETON.md
        └─> banned list grows from promoted Fails card lines until /cleanup
```

### 4.2 Who consumes the card

- **Chat-mode agent**: reads the card before running risky commands; follows the banned list and takes the expected runtimes
- **Prompt sequences**: `/write-prompts` Step 1 builds the hang-safety clause from the card; every implementation prompt loads the card at startup
- **`/verify`**: checks card instances against `ROBUSTNESS_CARD_SKELETON.md` structure

### 4.3 Building the project banned list

1. Search the project for scripts containing `pause`, `Read-Host`, `ReadKey`, `Get-Credential`
2. Search for CLI entry points reading stdin when no arguments are given
3. Search for `--watch` flags in package.json scripts
4. Probe each suspicious command through the runner: if its output shows an input wait within 5 seconds, end it with the stop file and ban it
5. Add each confirmed hang to the banned list with its evidence

## 5. Consumption Modes

- **Chat mode** (no workflow active): SKILL.md dispatch + this guide + the project card govern command execution. The minimal rule in `agent-behavior.md` ("Terminal Hang Prevention") links here
- **Prompt-sequence mode**: `/write-prompts` loads this skill; the hang-safety clause in `PROMPTS_ROBUSTNESS_GUIDES.md` (write-documents skill) references the card; prompts load the card at startup

## 6. Three-Tier Defense

1. **Prevent** (card bans and always rules): non-interactive flags, agent tools, no `2>&1`
2. **Catch** (supervised runner + monitoring agent): empty stdin ends input waits within seconds; `ALIVE` lines show CPU time and output growth; on a hang verdict the agent's stop file ends the whole Job Object tree - catches the hangs tier 1 missed, including unknown ones, without ending work that still makes progress (HANGBENCH result: DevinCascade guide)
3. **Remember** (Fails card): every failure becomes a "Never again" line checked before the next command

The runner kills directly on the stop file (Job Object termination, no graceful signal on Windows): the verdict says the process is hung, a grace period only delays.

## 7. Hang or Slow: Reading the Liveness Signals

Elapsed time does not separate a hang from slow work. Ending slow work throws away its whole runtime and forces a second run, which costs more than waiting. The runner therefore has no deadline. It writes one `ALIVE` line every 30 s (`elapsed=`, `cpu=` CPU seconds of the whole tree, `out=` / `err=` bytes of the output files, `procs=` living processes); the agent compares two lines:

- `out=` or `err=` grew, or the work wrote its own files -> working. Keep waiting
- Only `cpu=` grew -> computing or buffering (silent phase, compile step, pipeline that emits at the end). Keep waiting
- All values unchanged and the last output line is a prompt, a pager, or a lock message -> hang. End it at once
- All values unchanged and the script is inside a known silent wait (network call with its own timeout, sleep, wait for another process) -> not a hang yet. Wait until that phase must have ended
- All values unchanged for 5 minutes past the expected runtime, no known silent phase -> hang. End it
- Only `cpu=` grew for 10 minutes, elapsed above 3x expected, and no file the work writes has changed -> endless loop. End it
- No new `ALIVE` line for 90 s and no end line -> the runner itself is gone (agent rule file: runner-gone check)

Ending = creating the stop file; thresholds and wording: `agent-behavior.md` Terminal Hang Prevention step 5. A `DONE` far above the expected runtime is a runtime overrun: the result is used, the cause is recorded, the card's expected runtime is corrected. It is never re-run.

Why no automatic kill: in HANGBENCH an idle timeout on output killed legitimate silent work (HC-03, HC-24), and a deadline kills legitimate work that only needs longer than estimated. Each single signal has a legitimate case that looks the same; only the combination, read with knowledge of what the script does, separates them.

## Review Checklist

- [ ] No command ended while it showed progress; every `KILLED` has hang evidence in its Fails entry
- [ ] Classified the command risk before running (interactive / volume / child)
- [ ] Loaded the project card if it exists; created one from the agent template if not
- [ ] Non-whitelisted commands ran through `run-supervised.ps1`; completion read from the runner log
- [ ] Temp scripts and output files deleted after consumption
- [ ] Every failure written to the Fails card of the working folder at once, with a "Never again" line
