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

The established mitigation - run the command from a `.tmp_*.ps1`/`.py` script, redirect ALL output to files, then read the files with `read_file`:

- File handles have no 4KB pipe limit and no drain-rate throttle
- No shell merge point, no record wrapping, no merge OOM
- Grandchildren inherit file handles, not pipe write handles - the tool's pipes EOF at parent exit and the command returns immediately

This is mechanical, not folklore. Prefer it whenever a command writes more than a few KB.

## 3. Safe Command Patterns (Selection)

1. **Agent tools over shell** - grep_search, read_file, find_by_name for file operations; shell only for process execution
2. **Non-interactive flags** - `--yes`, `--no-pager`, `--ci`, `-NonInteractive`; git log/diff/show always with `--no-pager` and `-n <N>`
3. **Runner flags before `--`** - `npm create` / `npx` / `pnpm dlx` / `yarn create` are two-layer commands: the runner prompts on stdin ("Need to install ... Ok to proceed? (y)") before the scaffold tool starts, and everything after the `--` separator is forwarded to the tool, not the runner. Runner-level `--yes` must sit BEFORE `--`: `npm create --yes astro@latest . -- --template minimal` runs prompt-free; `npm create astro@latest . -- --template minimal --yes` still waits on stdin
4. **No stdin waits** - ban `Read-Host`, `pause`, `Get-Credential`, REPLs launched without input, `Get-Content -Wait`, `tail -f`
5. **No unbounded children** - ban `--watch` flags, `Wait-Process` without `-Timeout`; stop spawned processes after use
6. **Recursive enumeration** - prefer `rg.exe` (ripgrep, bundled with VS Code-based editors) over `Get-ChildItem -Recurse` / `Select-String -Recurse` on large trees
7. **Time caps** - every process-running command gets a cap ~3x its expected duration; on cap: kill the process tree, record in PROBLEMS.md, continue
8. **Timeout wrapper** - commands with no native safe parameter run via a separate process with redirect-to-file and process-tree kill on timeout (see the agent card template for the tested PowerShell pattern)

## 4. The Robustness Card

A robustness card (`__CARD_[TOPIC]-Robustness.md` in the project or session root) is the durable per-project protection: banned commands, time caps, always rules, on-cap behavior, kill procedure, findings feed.

### 4.1 Card lifecycle

```
copy agent ROBUSTNESS_CARD_TEMPLATE.md
└─> name __CARD_[TOPIC]-Robustness.md in project root
    └─> extend banned list + caps with project-specific entries
        ├─> chat mode: loaded before risky commands
        ├─> prompt sequences: hang-safety clause references the card
        ├─> /verify: instance checked against ROBUSTNESS_CARD_SKELETON.md
        └─> findings feed grows across sessions
```

### 4.2 Who consumes the card

- **Chat-mode agent**: reads the card before running risky commands; follows banned list and caps
- **Prompt sequences**: `/write-prompts` Step 1 builds the hang-safety clause from the card; every implementation prompt loads the card at startup
- **`/verify`**: checks card instances against `ROBUSTNESS_CARD_SKELETON.md` structure

### 4.3 Building the project banned list

1. Search the project for scripts containing `pause`, `Read-Host`, `ReadKey`, `Get-Credential`
2. Search for CLI entry points reading stdin when no arguments are given
3. Search for `--watch` flags in package.json scripts
4. Test each suspicious command with a 5-second timeout - if it hangs, ban it
5. Record findings in the card's Findings Feed

## 5. Consumption Modes

- **Chat mode** (no workflow active): SKILL.md dispatch + this guide + the project card govern command execution. The minimal rule in `agent-behavior.md` ("Terminal Hang Prevention") links here
- **Prompt-sequence mode**: `/write-prompts` loads this skill; the hang-safety clause in `PROMPTS_ROBUSTNESS_GUIDES.md` (write-documents skill) references the card; prompts load the card at startup

## 6. Two-Tier Defense

1. **Always rules** (tier 1, prevent): non-interactive flags, redirect-to-file, agent tools, caps
2. **Timeout wrapper** (tier 2, catch): separate process + redirect + process-tree kill - for commands without native safe parameters or with lock/network risk

Tier 1 covers the known; tier 2 catches the unknown. Both live in the agent card templates.

### 6.1 On-Cap Kill Escalation

For processes that may still exit cleanly: SIGTERM first (`Stop-Process -Id <pid> -Force` on Windows, `kill -TERM` on POSIX), wait 5 seconds, then SIGKILL (`taskkill /T /F /PID <pid>` on Windows, `kill -KILL` on POSIX), then sweep orphan processes by name. Why: SIGTERM lets the process flush buffers, release locks, write state; direct SIGKILL can leave resources locked, files half-written, ports dirty. For confirmed hangs (the tested timeout pattern, DevinCascade guide Section 3), kill directly - the grace period only delays and risks re-hang during cleanup.

## Review Checklist

- [ ] Classified the command risk before running (interactive / volume / child)
- [ ] Loaded the project card if it exists; created one from the agent template if not
- [ ] No `2>&1` on stderr-heavy commands; output redirected to files
- [ ] No stdin/pager waits; no unbounded background children
- [ ] Time cap set for every process-running command
- [ ] Kills recorded; new findings added to the card's Findings Feed
