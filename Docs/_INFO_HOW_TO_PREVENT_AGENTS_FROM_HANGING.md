# INFO: How to Prevent Agents from Hanging

**Doc ID**: PRMTHANGFIX-IN04
**Goal**: Explain every layer that protects agent terminal commands from hanging (agent rules, terminal-robustness skill, prompt-file cards), the test evidence behind each, the proposed changes, and how all parts work together
**Timeline**: Created 2026-11-11, Updated 3 times (2026-11-11 - 2026-11-11)

**Depends on:**
- `_INFO_PRMTHANGFIX-IN01_WindowsHangPreventionTools.md [PRMTHANGFIX-IN01]` for Windows tool options and the Cascade hook
- `_INFO_PRMTHANGFIX-IN02_ClassicHangSupervisionPatterns.md [PRMTHANGFIX-IN02]` for classic supervision rules
- `_INFO_PRMTHANGFIX-IN03_WindowsSupervisorTools.md [PRMTHANGFIX-IN03]` for procgov and processkit-py
- `_INFO_TERMROBUSTNESS-01_HangingCommandInvestigation.md [TERMROBUSTNESS-IN01]` for the measured pipe mechanisms

## Summary

- Three different failures look identical to the user ("the step is spinning"): 1) the process really hangs, 2) the process finished but the terminal tool never reports completion, 3) the conversation or IDE crashes. Each needs a different defense [VERIFIED]
- Correction 2026-11-11 (section 7.6): the first design ended every command at a time cap. A cap also ends slow work that would have finished; the finished part is lost and the command runs again. The cap is removed. The runner now only contains the process tree and reports liveness; the agent ends a command if and only if the evidence shows a hang [TESTED: runner 27/27 without deadline; hang verdict by the agent ASSUMED, not tested live]
- Process hangs are ended reliably only by a whole-tree kill from outside the script. In the 27-case bench (all solutions with a 5 s deadline), [processkit-py](https://pypi.org/project/processkit-py/) passed 27/27, [Process Governor](https://github.com/lowleveldesign/process-governor) 26/27, every PowerShell-only pattern 24/27 or less [TESTED]
- The current card's main pattern (tmp script + `-NonInteractive` + redirect) stops 1 of 18 hang types (8/27 total). It prevents pipe problems, not waits [TESTED]
- The terminal tool sometimes misses completion of a finished command (1 miss in 13 sub-second commands) and once reported "done" for a command still running. No process supervisor helps here; only a bounded wait plus a completion marker written by the command itself [TESTED]
- Concurrent Cascade conversations share the same terminal processes: one conversation's command text appeared in another conversation's output [TESTED]
- `>` redirects in PowerShell deliver output only after the process exits. Live output of an unchanged script works only via `Start-Process -RedirectStandardOutput`; Python additionally needs `PYTHONUNBUFFERED=1` set by the wrapper [TESTED]
- Existing project scripts need no change: the shipped runner logs `START` / `DONE`, sets the environment, and launches the script; logging, streaming, and the processkit Job Object together pass all 27 cases [TESTED]
- Text rules alone do not hold: agents break the inline whitelist at the point of action, and hangs are not recorded (0 findings-card entries after 8 prompts with an observed hang), so later prompts repeat them [VERIFIED]
- Fails card (section 7.2, implemented as template): a separate `__CARD_[TOPIC]-Fails.md` with a "Never again" list (pattern -> replacement). The agent reads it at prompt start and checks every planned command against it, writes an entry immediately after any failure, stops a prompt on the second repeat, and promotes the lines to the robustness card at sequence end [ASSUMED - design]
- Implemented in `PromptSystemV4.7/` (section 7.5): one shipped runner `run-supervised.ps1` instead of an agent-written wrapper per command; one home per rule, every other file references it; Fails card replaces the robustness card findings feed; prompts carry 2 robustness lines instead of a restated procedure [TESTED: runner 27/27 in HANGBENCH, live output for unchanged Python and PowerShell scripts]

## Table of Contents

1. [The Problem](#1-the-problem)
2. [Root Causes](#2-root-causes)
3. [Current System: Layers and How They Interact](#3-current-system-layers-and-how-they-interact)
4. [Evidence from Investigations and Live Probes](#4-evidence-from-investigations-and-live-probes)
5. [HANGBENCH: Repeatable Test Bench](#5-hangbench-repeatable-test-bench)
6. [Monitoring Without Rewriting Scripts](#6-monitoring-without-rewriting-scripts)
7. [Proposed Changes](#7-proposed-changes)
8. [Target Architecture: How Everything Works Together](#8-target-architecture-how-everything-works-together)
9. [Failure-to-Defense Map](#9-failure-to-defense-map)
10. [Open Questions and Untested Parts](#10-open-questions-and-untested-parts)
11. [Next Steps](#11-next-steps)
12. [Sources](#12-sources)
13. [Document History](#13-document-history)

## 1. The Problem

Prompt sequences run unattended: an execution engine sends prompt 1, waits for the agent to finish, sends prompt 2, and so on. One terminal call that never returns stops the whole sequence until a human cancels it. In observed sequences of 12-14 prompts, a single stuck call left 6-10 prompts queued [VERIFIED].

The goal of all layers described here: **no command may need a human cancel**, and every failure is recorded so later prompts do not repeat it.

### 1.1 Three failures that look the same

```
User sees: step spinning, no output
│
├─> A) Process hang: the command or a child process really waits
│   └─> examples: stdin prompt, pager, ">>" continuation prompt, network wait,
│       child holding the output pipe open, infinite loop
│
├─> B) Completion miss: the command finished, the terminal tool did not notice
│   └─> work done (output files written), tool still shows "running"
│
└─> C) Crash: conversation or IDE dies; cause unknown in observed cases
```

- **A** is fixed by a supervisor that contains the whole process tree and kills it when asked. Who asks: in the first design a deadline, in the current design the agent after a hang verdict (section 7.6)
- **B** is fixed only by never waiting on the tool without a time limit and by reading a completion marker the command writes itself
- **C** is outside the scope of command design; the defenses for A and B limit the damage (state is on disk, the next prompt can resume)

### 1.2 Why it matters more in prompt sequences than in chat

- In chat, the user sees the spinner and cancels after a minute. In a sequence nobody watches
- A cancel in the Cascade UI may kill only the top process; children keep running and keep holding files or terminals [VERIFIED]
- After a cancel and "continue", agents resume without recording what hung, so the next prompt issues the same pattern again [VERIFIED]

## 2. Root Causes

Root causes (RC) found in the 2026-11-11 analysis. Labels show the evidence state. Hang case IDs (HC-01 to HC-27) refer to the bench cases in section 5.2.

- **RC-1 Rules exist, agents ignore them at the point of action** [VERIFIED]: prompts carried the full hang-safety clause and a correct robustness card, yet agents typed inline multi-statement PowerShell (pipes, `;`, nested quotes, over 200 characters). The clause is one of about 7 similar constraint bullets; long workflows dispatched by the prompt push it out of focus. Text rule, no mechanical gate
- **RC-2 Incomplete input waits forever** [TESTED]: a long inline line with nested quotes (`"...$(...)"`) leaves PowerShell at the `>>` continuation prompt, waiting for more input on stdin. The echo showed duplicated statements and `>>`. Bench case HC-10 reproduces it
- **RC-3 No expected duration, so no cap fires** [VERIFIED]: card caps cover tests, installs, builds, git. Ad-hoc analysis commands get no expected time and run blocking; a blocking Cascade call has no timeout. Corrected reading (section 7.6): the missing piece was a way to see and end a hang, not a cap. This wording led to the cap design
- **RC-4 Hangs are not recorded** [VERIFIED]: after 8 of 14 prompts the sequence's findings card had 0 entries despite an observed hang. Recording is one duty among many in the findings card
- **RC-5 No cross-prompt learning** [VERIFIED]: consequence of RC-4; later prompts load nothing about earlier hangs
- **RC-6 Agent search tool unavailable outside the workspace** [VERIFIED]: `grep_search` rejects paths outside the open workspace and sometimes returns empty results for existing strings. Agents fall back to shell `Select-String` pipelines, the exact command type of RC-2
- **RC-7 Contradicting examples** [VERIFIED]: `PROMPTS_ROBUSTNESS_GUIDES.md` sections 5.1 and 7.3 show inline `Select-String -Pattern ... -Path src/` as acceptable in Verify sections; agents generalize this to inline pipelines
- **RC-8 Tool misses completion of a finished command** [TESTED]: a script that printed one line and wrote a JSON file finished within seconds (file timestamp), the call kept spinning. Reproduced live: 1 miss in 13 sub-second commands. The blocking call itself is the hang point
- **RC-9 Concurrent conversations share terminals** [TESTED]: output of one conversation's probe contained the command line another conversation had run seconds before in the same terminal process
- **RC-10 Outer `>` redirect delivers output only at exit** [TESTED]: `script > out.txt` left `out.txt` empty during the whole run; content appeared when the process ended

## 3. Current System: Layers and How They Interact

State of `PromptSystemV4.7` on 2026-11-11, before any proposed change. Four layers, each loaded at a different time.

```
Layer 1  Agent rules ─── always loaded
         ├─> agent-behavior.md: inline whitelist, tmp-script pattern, hard bans
         └─> devin-cascade.md: Cascade terminal limits, Blocking=false for slow tasks

Layer 2  terminal-robustness skill ─── loaded before risky commands
         ├─> SKILL.md dispatch -> shared GUIDES + agent variant (DevinCascade/)
         └─> RULES (HG/EX/CD), CHECKS, card SKELETON + agent card TEMPLATE

Layer 3  Cards in _agentwork/ ─── per working folder, loaded per prompt
         ├─> __CARD_[TOPIC]-Robustness.md: banned list, caps, kill procedure
         └─> __CARD_[TOPIC]-Findings.md: glitches, root causes, prevention

Layer 4  Prompt files ─── _PROMPTS_[NN]-[Topic].md, one prompt per turn
         └─> hang-safety clause + findings-card directive in every implementation
             prompt; built by /write-prompts from PROMPTS_ROBUSTNESS_GUIDES.md
```

### 3.1 Layer 1: Agent rules

`rules/agent-behavior.md` section "Terminal Hang Prevention" [VERIFIED]:
- **Inline whitelist**: a command may run inline only if ALL apply: single command, no `|`, no `;`, no loop or script block, no `2>&1`, under 200 characters, under 10 seconds, under 50 output lines. Examples: `git status`, `git --no-pager log -n 5`
- **Tmp-script pattern** for everything else: write `_agentwork/.tmp_[purpose].ps1`, run `pwsh -NoProfile -NonInteractive -File ... > _out.txt 2> _err.txt` "non-blocking with time cap ~3x expected duration when runtime is uncertain", read results only with `read_file`, delete script and output files after use
- **Hard bans**: 1) no `2>&1`, 2) no unbounded background children (`--watch`, dev servers), 3) no stdin or pager waits (`Read-Host`, `pause`, pagers, `Get-Content -Wait`)
- **On cap**: kill the process tree, record in PROBLEMS.md

`agent-behavior.md` section "Long-Running Commands (over 60 seconds)" [VERIFIED]:
- State the estimated duration before start; a silent multi-minute command is indistinguishable from a hang
- Warn that canceling the Cascade step does NOT kill the spawned process
- If the log has not grown for 2 minutes, check liveness (CPU, StartTime); Python buffers stdout to files, so an empty log does not mean a dead process
- If runtime exceeds 2x the estimate: kill the process tree by PID, report

`rules/devin-cascade.md` section "Terminal Limits" [VERIFIED]:
- Max 4 concurrent terminals (observed 2026-03-09); additional terminals are queued
- Non-whitelisted commands: `run_command` runs only the `pwsh ... -File .tmp_*.ps1 > ... 2> ...` line
- `Blocking: false` for parallel or slow tasks, poll with `command_status`. Not required for every call

Gap: Layer 1 says what to do but cannot enforce it. Nothing stops an agent from typing a 400-character pipeline with `Blocking=true` (RC-1).

### 3.2 Layer 2: terminal-robustness skill

`skills/terminal-robustness/` structure [VERIFIED]:
- `SKILL.md`: dispatch by agent identity (Cascade -> `DevinCascade/`, Claude Code -> `ClaudeCode/`, Devin agent -> `ClaudeCode/` minimum); core procedure: 1) classify risk (interactive, volume, child, known-safe), 2) load or create the card, 3) execute safely, 4) record findings
- `TERMINAL_ROBUSTNESS_GUIDES.md` (shared): three OS-level mechanisms (pipe-buffer backpressure, std-handle inheritance by grandchildren, shell stream-merge corruption), why the redirect pattern defeats all three, safe patterns, card lifecycle, two-tier defense (tier 1 always rules prevent, tier 2 timeout wrapper catches)
- `DevinCascade/TERMINAL_ROBUSTNESS_GUIDES.md`: measured Cascade tool behavior (waits for pipe EOF on stdout and stderr, not child exit; un-merged stderr drains at ~2.3KB/s; `2>&1` makes pwsh the merge point with out-of-memory (OOM) errors; long echoes mangled), the tmp-script skeleton, the tier-2 timeout pattern (`Start-Process` + `WaitForExit` + recursive Common Information Model (CIM) `Stop-ProcessTree`), non-blocking polling
- `TERMINAL_ROBUSTNESS_RULES.md`: HG-01..04 (no merge, no stdin/pager, no unbounded children, no recursive shell enumeration), EX-01..05 (redirect, cap, tree kill with survivor sweep, inline whitelist, delete tmp files), CD-01..04 (card from template, six sections, evidence per entry, findings feed on every hang)
- `TERMINAL_ROBUSTNESS_CHECKS.md`: post-execution audits for `/drift-detect` and `/improve`
- `ROBUSTNESS_CARD_SKELETON.md` + `DevinCascade/ROBUSTNESS_CARD_TEMPLATE.md`: card structure and Cascade defaults (banned list with evidence, caps per command class, always rules, on-cap behavior, kill procedure, execution pattern, agent tool limits, findings feed)

Gap: the skill's tier-2 pattern was tested against the 2026-09 mechanisms only. The 2026-11 bench shows it misses grandchildren that hold the pipe and orphans that lost their parent (section 5).

### 3.3 Layers 3 and 4: Prompt files and cards

`/write-prompts` Compose Step 1 builds the robustness layer of a sequence [VERIFIED]:
1. Load `PROMPTS_ROBUSTNESS_GUIDES.md` (write-documents skill) and the terminal-robustness skill variant
2. If `_agentwork/__CARD_[TOPIC]-Robustness.md` exists: build the hang-safety clause from its banned list and caps. Else copy the agent's `ROBUSTNESS_CARD_TEMPLATE.md`, extend it with project entries (scripts with `pause`, CLIs reading stdin, `--watch` scripts)
3. Copy the agent's Tool-Call Payload Limit verbatim into the card section `## Agent tool limits` (PRMT-HS-11)
4. Designate `_agentwork/__CARD_[TOPIC]-Findings.md` for the sequence

Every implementation prompt then carries two blocks [VERIFIED]:
- **Hang-safety clause** in Constraints (PRMT-HS-01..06): prohibition (no key, stdin, pager, unbounded child), tmp-script rule, banned list by card reference, time cap, on-cap behavior ("kill the process tree, record command and cap in PROBLEMS.md, continue")
- **Findings-card directive** (PRMT-RB-01..07): load the findings card at startup for unresolved entries, file glitches before the end-of-prompt commit. Entry format: severity, expected state, actual state, root cause, resolution, prevention

Card system protocol when a rules card (card 00) is used [VERIFIED]:
- Start of prompt: verify session anchor, read cards, check PROGRESS.md for resume, load findings card
- End of prompt: verification passed, file findings, mark STRUT step, append PROGRESS.md, record blockers in PROBLEMS.md, commit

Where hangs go today: PROBLEMS.md (blocker) plus the findings card (root cause). Both share the entry with spec mismatches, naming glitches and test drift.

### 3.4 How the layers play together today, and where the chain breaks

```
/write-prompts
├─> creates Robustness card + Findings card
└─> writes prompts with hang-safety clause + findings directive
    │
    v
Execution engine sends prompt N
└─> agent reads cards (Layer 3) -> rules (Layer 1) -> skill on demand (Layer 2)
    └─> agent issues run_command
        ├─> compliant: tmp script + redirect
        │   ├─> pipe problems avoided (tested 2026-09)
        │   └─> waits NOT avoided: stdin, network, lock, loop run forever  <- break 1
        ├─> non-compliant inline pipeline (RC-1, RC-6, RC-7)
        │   └─> ">>" prompt or pipe hang                                  <- break 2
        └─> Blocking=true, tool misses completion (RC-8)                  <- break 3
            │
            v
Human cancels, says "continue"
└─> agent resumes; findings card not updated (RC-4)                       <- break 4
    └─> prompt N+1 repeats the pattern (RC-5)
```

- **Break 1**: the always rules prevent pipe-level hangs only. A tmp script that starts a native child waiting for input (`cmd /c pause`), waits on a lock or a network socket runs forever (`-NonInteractive` stops only PowerShell's own `Read-Host`) because nothing enforces a deadline from outside
- **Break 2**: text rules are not a gate; agents break them under workflow load
- **Break 3**: even a perfect command can block the agent when the tool misses completion
- **Break 4**: recording is buried among other duties and skipped after a human cancel

## 4. Evidence from Investigations and Live Probes

### 4.1 Measured pipe mechanisms (investigation 2026-09-29)

A test rig with synthetic child processes measured the Cascade terminal tool [TESTED]:
- Windows anonymous pipe buffer fills at about 4KB; a child writing more blocks until the reader drains
- The tool returns when stdout AND stderr reach end of file (EOF), not when the direct child exits: parent exited after 1 s, tool returned only when a grandchild holding the pipe died about 43 s later
- Un-merged stderr drains at about 2.3KB/s: 1MB of stderr takes about 7 minutes, an apparent hang with a live process
- `2>&1` with a 1MB stderr flood: pwsh OutOfMemoryException and exit code 1 reported for a child that exited 0
- Mitigation confirmed: tmp script with all output redirected to files. File handles have no 4KB limit and no drain throttle; grandchildren inherit file handles, so the tool's pipes reach EOF at parent exit

A cross-repository scan of FAILS, PROBLEMS, NOTES and card files listed 18 hang mechanisms in total, including approval waits, full test suites, orphaned terminals, ineffective UI cancels, pagers, stdin prompts and inline quoting corruption [VERIFIED].

### 4.2 Field cases (2026-11-11)

- **Continuation prompt** [VERIFIED]: an update sequence (14 prompts) stalled at prompt 8. The echo showed an inline `Select-String ... | Select-Object` and a multi-statement `$lines = ...; ...; Write-Output "...$(...)"` line, statements duplicated 3x and a `>>` marker. Root causes RC-1, RC-2, RC-6, RC-7
- **Completion miss** [VERIFIED]: a documentation sequence (12 prompts) stalled at prompt 2. The command was card-compliant (`pwsh -NoProfile -NonInteractive -File .tmp_ledger.ps1`, no redirect), the script reads files, prints one line, starts no child, reads no stdin. Its JSON output carried a timestamp a few seconds after the start; the call kept spinning with no output. Root cause RC-8

### 4.3 Live probes in the real Cascade terminal

A probe script (`live-probe.ps1`) wrote its own start and end timestamps to a JSONL file and finished in under 1 s. Each call used `Blocking=false` with `WaitMsBeforeAsync=8000`, so a missed completion returned "Background command ID" after 8 s instead of blocking [TESTED]:
- 13 short commands (9 probes, 4 diagnostics): 12 detected, 1 missed. The missed command had written its `DONE` line; `command_status` reported done only later
- Inverse error: during a 2.5-minute stream test, `command_status` reported DONE after about 65 s while the test was still running its third of nine variants (process list and growing files confirmed it)
- Output capture is unreliable: echoes duplicated or truncated, the first character lost, output overwriting the echo, "No output" for a command that printed lines
- Shared terminals (RC-9): one probe's output contained another conversation's command line; process IDs showed both ran in the same shell-integration `pwsh` process

Conclusion [TESTED]: tool status and tool output are not a reliable completion signal in either direction. The only reliable signal is an artifact the command writes itself and the agent reads with `read_file`.

## 5. HANGBENCH: Repeatable Test Bench

Goal: test every candidate solution against the same set of hang cases, on Windows with PowerShell 7, and repeat the test after every change.

### 5.1 Design

- `hang-cases.ps1`: case library; one case per call (`-Case HC-04 -RunTag <tag>`). Every spawned process carries the run tag in its command line so the harness can find orphans. Every case limits itself (60 s default) as a second safety net
- `hangbench.ps1`: harness. Starts each case through each solution with stdout and stderr piped (like the terminal tool), measures exit time and pipe EOF time separately, snapshots descendants every 0.3 s, applies a watchdog (solution cap + 15 s), counts survivors after a 1.5 s grace period, kills leftovers, writes one JSON Lines (JSONL) record per run and a Markdown report
- `wrappers.ps1`: in-house patterns under test (card tier 1, card tier 2, `Kill($true)`, watch-tree)
- Verdicts: **Hang** cases pass only if the solution ends them within cap + 5 s with zero survivors; **Legit** cases pass only if they finish with exit 0, their `DONE` line, and zero survivors (no false kill); **Cancel** case passes only if killing the solution's top process leaves zero survivors

### 5.2 Case library (27 cases)

Every case is traced to an observed incident or a card ban [VERIFIED]:
- **Controls and legit long runs (8)**: HC-01 fast exit, HC-02 8 s with progress, HC-03 8 s silent, HC-12 1MB stderr unmerged, HC-13 1MB stderr with `2>&1`, HC-14 5MB stdout, HC-19 detached child with file handles, HC-24 `Select-Object -Last` buffering an 8 s producer
- **Waits on input (8)**: HC-06 `Read-Host`, HC-07 `cmd pause`, HC-08 pager, HC-09 `python` without script (interactive read-eval-print loop), HC-10 `>>` continuation prompt, HC-22 `rg` without path reads stdin, HC-23 native y/n prompt (`set /p`), HC-26 read stdin to EOF
- **Unbounded waits (6)**: HC-04 sleep forever, HC-05 CPU spin, HC-15 HTTP server that never answers, HC-16 lock file that never disappears, HC-17 `Wait-Process` without timeout, HC-18 `Get-Content -Wait`
- **Process trees (4)**: HC-11 grandchild holds the pipe after the parent exits, HC-20 3-level sleeping tree, HC-21 grandchild whose parent already exited, HC-25 GUI program that waits
- **Cancel (1)**: HC-27 only the top process is killed (models a UI cancel)

### 5.3 Solutions tested

- `raw`: no protection (baseline)
- `cardline`: card tier 1 (tmp script + `-NonInteractive` + redirect, no cap)
- `cardtree`: card tier 2 verbatim (`Start-Process` + `WaitForExit` + recursive CIM `Stop-ProcessTree`)
- `killtree`: PowerShell 7 `Process.Kill($true)` + empty stdin file
- `watchtree`: `killtree` + descendant snapshots + idle timeout (in-house reference)
- `gnutimeout`: Git for Windows GNU `timeout.exe -k 2` (GNU General Public License)
- `procgov`: [Process Governor](https://github.com/lowleveldesign/process-governor) 4.1, Job Object, `-t <cap>s --recursive --terminate-job-on-exit` (MIT)
- `processkit`: [processkit-py](https://pypi.org/project/processkit-py/) 1.5.0, `processkit run --timeout <cap> --kill-on-parent-death`, Job Object with kill-on-close (MIT)
- `pkidle`: `processkit` + `--idle-timeout 6`

### 5.4 Results (run `full1`, hang cap 5 s, 243 runs)

Passed cases per solution (total, hang, legit, cancel) and failed cases:
- **processkit**: 27/27 (hang 18/18, legit 8/8, cancel 1/1); failed: none
- **procgov**: 26/27 (18/18, 8/8, 0/1); failed: HC-27
- **pkidle**: 25/27 (18/18, 6/8, 1/1); failed: HC-03, HC-24 (false idle kill)
- **cardtree**: 24/27 (16/18, 8/8, 0/1); failed: HC-11, HC-21, HC-27
- **killtree**: 24/27 (16/18, 8/8, 0/1); failed: HC-11, HC-21, HC-27
- **gnutimeout**: 24/27 (16/18, 8/8, 0/1); failed: HC-11, HC-21, HC-27
- **watchtree**: 23/27 (17/18, 6/8, 0/1); failed: HC-03, HC-21, HC-24, HC-27
- **cardline**: 8/27 (1/18, 7/8, 0/1); failed: all hang cases except HC-06, plus HC-03 and HC-27
- **raw**: 8/27 (0/18, 8/8, 0/1); failed: all hang cases, HC-27

What the results mean [TESTED]:
- Only Job Object tools contain every descendant: a process assigned to a Job cannot escape by losing its parent (HC-21) and cannot keep the pipe open after the leader exits (HC-11)
- processkit ends the whole job when the leader exits: HC-11 ended at 1.15 s; HC-19 (detached child) returned after 1.48 s instead of 9-12 s with zero survivors, so the detached child was removed with the leader [ASSUMED from timing]. Consequence: an agent cannot leave a background process running through processkit; for agents this is the wanted behavior
- procgov keeps the job alive when only procgov itself is killed (HC-27); with a timer-bounded agent (section 7) this case becomes rare, but it is a real gap
- Idle timeouts kill legit silent work (HC-03, HC-24). A deadline looked safe only because every legit case got a cap above its runtime (8 s of work, 15 s cap); with a cap below the real runtime it kills legit work the same way (section 7.6)
- PowerShell-only tree kills miss HC-11 and HC-21: `Start-Process -NoNewWindow` passes the wrapper's inheritable pipe handles to the child, and a grandchild whose parent exited is invisible to a ParentProcessId walk. The card tier-2 pattern also needed up to 18 s for a 5 s cap in a pilot run because the CIM tree walk is slow
- The card tier-1 pattern prevents pipe problems but no wait; `-NonInteractive` catches only PowerShell's own `Read-Host`

### 5.5 Limits of the bench

- The harness pipes are not the Cascade terminal tool: RC-8 (completion miss) and RC-9 (shared terminals) cannot be reproduced here; they were tested live (section 4.3)
- One full run; no repeat statistics yet. The pilot showed one result (cardtree HC-27) that the full run did not confirm
- The final wrapper of section 7 (processkit + `Start-Process` + log file) has not run against the 27 cases yet

## 6. Monitoring Without Rewriting Scripts

Constraint: a workspace has 100+ existing scripts (Python and PowerShell). None of them may need a change. The agent must still tell "finished", "still working" and "hung" apart.

### 6.1 What the agent can and cannot read

- **Tool status and tool output**: unreliable in both directions (section 4.3) [TESTED]
- **`_out.txt` of an outer `> _out.txt` redirect**: empty until the process exits (RC-10) [TESTED]
- **File timestamps via `find_by_name`**: not available for `_agentwork/.tmp_*` files because the tool skips gitignored files [VERIFIED]
- **Any file a process writes with `Add-Content` or through a file handle given at process start**: readable with `read_file` while the process runs [TESTED]

### 6.2 Streaming test (stream-test.ps1, 9 variants)

An unchanged script prints one line per second for 10 s. It runs under `processkit run --timeout 30 --kill-on-parent-death`, started by an outer `pwsh` that redirects with `>` (like the Cascade terminal). A wrapper writes `START` and `DONE` lines to its own log with `Add-Content`. A sampler counts visible lines every second [TESTED]:

Variant, script type, how the wrapper starts it, and lines visible after 5 s:
- **A** Python, `& python x.py > inner.txt`: 0
- **B** Python, as A + `PYTHONUNBUFFERED=1`: 0
- **C** Python, `Start-Process -RedirectStandardOutput inner.txt`: 0
- **D** Python, as C + `PYTHONUNBUFFERED=1`: 4 (live)
- **E** PowerShell, `& pwsh -File x.ps1 > inner.txt`: 0
- **F** Python, output to the outer `out.txt`, `PYTHONUNBUFFERED=1`: 0
- **G** Python, output to the outer `out.txt`: 0
- **H** PowerShell, output to the outer `out.txt`: 0
- **I** PowerShell, `Start-Process -RedirectStandardOutput inner.txt`: 3 (live)

- The wrapper's `START` line was on disk 2-3 s after launch in all 9 variants; `DONE` appeared when the script ended
- Every PowerShell `>` redirect of a native command delivered output only at exit, even with unbuffered Python (B, F): the buffering is in the PowerShell redirect, not in the script
- `Start-Process -RedirectStandardOutput` hands the file directly to the child: output is live for PowerShell (I) and for Python when the wrapper sets `PYTHONUNBUFFERED=1` (D). Without it, Python buffers in its own runtime (C)

### 6.3 Wrapper pattern derived from the test

The agent writes one wrapper per command; the project script stays unchanged:

```powershell
$log = "$PSScriptRoot\.tmp_[purpose]_log.txt"
function Write-Log([string]$Text) { Add-Content -Path $log -Value "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $Text" }
Write-Log 'START expected=20s'
$env:PYTHONUNBUFFERED = '1'
$process = Start-Process -FilePath 'python' -ArgumentList '"scripts\existing_script.py"' -NoNewWindow -Wait -PassThru `
  -RedirectStandardOutput "$PSScriptRoot\.tmp_[purpose]_out.txt" -RedirectStandardError "$PSScriptRoot\.tmp_[purpose]_err.txt"
Write-Log "DONE exit=$($process.ExitCode)"
```

What the agent can conclude from the files:
- `START` and `DONE` present: finished, whatever the tool reports
- `START` present, no `DONE`, `_out.txt` growing: working
- `START` present, no `DONE`, `_out.txt` not growing past the expected time: suspected hang; the processkit deadline ends it at the cap (superseded: no deadline, the agent decides from the liveness lines, section 7.6)
- No `START`: blocked before the wrapper ran (parse error, launch problem)

`Start-Process -NoNewWindow` passes the wrapper's inheritable handles to the child (section 5.4). Under processkit this is expected to be harmless because the job ends all members when the wrapper exits [ASSUMED, test T1].

Open [ASSUMED, test needed]: whether `Start-Process` needs `-RedirectStandardInput` with an empty file so that input waits fail at once instead of waiting for the cap; whether processkit's own `--stdout-file` gives the same live output without `Start-Process`.

## 7. Proposed Changes

Status: proposed, not implemented, pending the tests in section 10. Session requirements behind them: 1) no command may need a human cancel, 2) all failures and hanging commands go into a separate Fails card that the agent uses proactively to prevent repeats during the run, 3) exactly one runtime-check instruction line per prompt.

### 7.1 Change set

- **C1 Supervised execution**: every non-whitelisted command runs through a wrapper under processkit with a deadline (section 6.3, section 8.2). Fixes A-type hangs (RC-2, RC-3)
- **C2 Bounded tool calls**: every `run_command` uses `Blocking=false` with `WaitMsBeforeAsync` = expected seconds + 5 (max 60 s; the tool's own upper limit is unknown [ASSUMED]); completion is read from the wrapper log, never from tool status. Fixes B-type hangs (RC-8)
- **C3 Fails card**: new separate card `__CARD_[TOPIC]-Fails.md` with a "Never again" list, read before every command. Fixes RC-4, RC-5
- **C4 Runtime-check line**: one instruction line per prompt comparing expected and actual runtime; overruns become Fails entries. Fixes RC-3, feeds C3
- **C5 Clean examples**: remove inline `Select-String` examples (RC-7); add the fallback `rg.exe` via wrapper when `grep_search` cannot reach a folder (RC-6)
- **C6 Rule summary**: a short "Terminal Calls" section in `devin-cascade.md` so the core rules hold without loading the skill (RC-1)
- **C7 Hook (optional)**: a `pre_run_command` hook that blocks inline commands outside the whitelist; only after a live test shows the hook can block (RC-1, RC-2)

### 7.2 The Fails card: proactive prevention of repeated failures

The Fails card is the sequence's memory of what went wrong. Unlike the findings card it holds only failures, stays short, and is consulted before every command, not only at the start of a prompt.

File: `_agentwork/__CARD_[TOPIC]-Fails.md`, created by `/write-prompts` beside the robustness and findings cards.

```markdown
# Fails Card: [TOPIC]

## Never again
- [command pattern] -> [replacement] (FL-[NN])

## Entries

### FL-[NN]: [short title]
- **Prompt**: [NN] of [sequence file]
- **Command**: [exact command or wrapper name]
- **Class**: process hang / completion miss / error exit / runtime overrun / parse error / tool-call drop
- **Expected / actual**: [N] s / [N] s (from wrapper log START and DONE lines)
- **Root cause**: [mechanism] [VERIFIED or ASSUMED]
- **Fix**: [what was changed to continue]
- **Never again**: [pattern] -> [replacement]
```

How to write "Never again" lines so the agent can match them before a command:
- **Pattern = command shape + trigger**, not the exact command text, so variants match too: "inline command with `;`, `|` or nested quotes", not one specific `Select-String` line
- **Replacement = complete alternative** the agent can run without further research: tool, call form, and where completion is read
- **One line per root cause**: a second failure with the same root cause extends the existing line instead of adding a new one; target at most about 15 lines so the list stays readable before every command [ASSUMED - limit not tested]

Worked example (generic values, derived from the cases in section 4; entry FL-03 omitted for length):

```markdown
## Never again
- Inline command with `;`, `|` or nested quotes (`"...$(...)"`) -> wrapper script under processkit (FL-01)
- `run_command` with `Blocking=true` -> `Blocking=false` + `WaitMsBeforeAsync`, completion from wrapper log (FL-02)
- Shell search (`Select-String`, `Get-ChildItem -Recurse`) when `grep_search` rejects the folder -> `rg.exe` inside a wrapper script (FL-03)

## Entries

### FL-01: Inline analysis pipeline stuck at continuation prompt
- **Prompt**: 08 of `_PROMPTS_01-[Topic].md`
- **Command**: inline `Select-String ... | Select-Object ...; $lines = ...; Write-Output "...$(...)"`
- **Class**: process hang
- **Expected / actual**: 5 s / no result after 60 s (inline command, no wrapper log)
- **Root cause**: unterminated string; pwsh waits at `>>` for more input [TESTED: HC-10]
- **Fix**: same query as wrapper script under processkit
- **Never again**: inline command with `;`, `|` or nested quotes -> wrapper script under processkit

### FL-02: Finished command reported as running
- **Prompt**: 02 of `_PROMPTS_01-[Topic].md`
- **Command**: `.tmp_ledger.ps1` wrapper
- **Class**: completion miss
- **Expected / actual**: 5 s / wrapper log `START` to `DONE` 3 s; tool still running after 60 s
- **Root cause**: terminal tool missed completion (RC-8) [TESTED]
- **Fix**: result read from the wrapper log; continued
- **Never again**: `run_command` with `Blocking=true` -> `Blocking=false` + `WaitMsBeforeAsync`, completion from wrapper log
```

Walkthrough of the check with this card: the agent plans `Get-ChildItem -Recurse | Select-String 'TODO'` for a folder outside the workspace. The line FL-01 matches (pipe) and FL-03 matches (shell search, `grep_search` unavailable). The agent writes `rg.exe 'TODO' [folder]` into a wrapper script and runs it under processkit instead.

What counts as a failure (all go in, not only hangs):
- Deadline hit (processkit exit 124), tool completion miss, unexpected non-zero exit, runtime overrun from the runtime check, parse error, an agent tool call dropped or stalled on payload size, a command repeated after it failed once

How the agent uses it during a run:

```
Prompt start
└─> read "Never again" list completely (short by design)
    │
    v
Before each command
├─> planned command matches a "Never again" pattern?
│   ├─> yes: use the listed replacement instead
│   └─> no:  run it (C1 + C2)
    │
    v
After each command
├─> success within expected time: continue
└─> failure (any class above):
    ├─> 1) write entry + "Never again" line NOW, before any other step
    ├─> 2) fix root cause or use replacement, continue
    └─> 3) same pattern fails a second time in this prompt: stop the prompt,
           PROBLEMS.md entry, sequence continues with the next prompt
    │
    v
End of sequence
└─> promote "Never again" lines to the robustness card banned list
    (kept for later sequences in the same working folder until /cleanup)
```

Design reasons:
- **Separate card** because hangs mixed with spec mismatches and naming glitches were not recorded at all (RC-4: 0 entries after 8 prompts)
- **Write immediately** because a later crash or cancel must not lose the entry; end-of-prompt recording was skipped after human cancels
- **"Never again" list on top** because a list of one-line entries is short enough to read in full before every command; full entries are read only when a pattern matches
- **Stop on the second repeat** follows the classic restart limit (`_INFO_PRMTHANGFIX-IN02`): retry once for transient causes, never loop
- **Promotion to the robustness card** carries one sequence's lessons into later sequences of the same working folder; lines that recur across folders go into the card template (section 11, step 5)

Relation to the other cards:
- **Robustness card**: rules for the working folder (banned list, caps, execution pattern), kept until `/cleanup`. Receives promoted "Never again" lines
- **Findings card**: content glitches (spec mismatches, test drift, naming). No longer holds hangs or command failures
- **PROBLEMS.md**: problems that stopped a prompt and need later work

### 7.3 The runtime-check line

Exactly one instruction line per prompt, placed next to the hang-safety clause in Constraints:

```
- Runtime check: before each command state the expected seconds and check the Fails card "Never again" list; after it compare the wrapper log START and DONE times with the expectation; on failure or when actual exceeds both 3x expected and expected + 30 s write a Fails card entry at once, fix the root cause, then continue
```

Superseded by section 7.6: the line now also tells the agent to read the `ALIVE` lines while a command runs and to end it only on a hang verdict; a slow finished command is used, not re-run.

Diagnosis the agent derives from the wrapper log and output files:
- `START` to `DONE` long: the work itself is slow; narrow scope or choose a better tool
- `DONE` present, tool still reports running: completion miss (RC-8); continue, record class "completion miss"
- `START` present, no `DONE`, output stopped: hang inside the script; processkit ends it at the cap (exit 124)
- No `START`: blocked before or at launch (parse error, stdin wait in the launch line)

### 7.4 Changes per file (all in `PromptSystemV4.7/`, then synced to the agent folder)

- **`skills/terminal-robustness/DevinCascade/ROBUSTNESS_CARD_TEMPLATE.md`**: replace "Execution pattern" with the processkit wrapper (section 8.2); add always rules "never `Blocking=true`" and "completion = `DONE` in the wrapper log"; replace "Kill procedure" (recursive CIM walk) with "processkit kills the job"; add bans for inline multi-statement lines (HC-10) and for the tier-1 pattern without supervisor (8/27); point the findings feed to the Fails card
- **`skills/terminal-robustness/ROBUSTNESS_CARD_SKELETON.md`**: add the Fails card skeleton (section 7.2) as a second block
- **`skills/terminal-robustness/SKILL.md`**: step 3 points to the card execution pattern; step 4 records failures in the Fails card; MUST-NOT-FORGET gains "never `Blocking=true`" and "check Fails card before each command"
- **`skills/terminal-robustness/DevinCascade/TERMINAL_ROBUSTNESS_GUIDES.md`**: add RC-8, RC-9, RC-10, the streaming findings, and the bench results; mark the CIM tree-kill pattern as superseded
- **`skills/write-documents/PROMPTS_TEMPLATE.md`** and **`PROMPTS_ROBUSTNESS_GUIDES.md`**: add the runtime-check line, the Fails card directive and its load step at prompt start; replace the inline `Select-String` examples in sections 5.1 and 7.3 with `grep_search` and the `rg.exe` wrapper fallback; update the review checklist
- **`workflows/write-prompts.md`**: Step 1 creates `__CARD_[TOPIC]-Fails.md`; Step 5 verifies the runtime-check line and the Fails directive in every implementation prompt
- **`rules/devin-cascade.md`**: new "Terminal Calls" section: always `Blocking=false` with timer, completion from the wrapper log, processkit wrapper, no command that reads stdin (shared terminals)
- **`rules/agent-behavior.md`**: tmp-script step 2 changes from `pwsh ... > out 2> err` to the supervised wrapper; on cap: Fails card instead of PROBLEMS.md only
- **`rules/tools-and-skills.md`**: tool location of `processkit.exe` in the shared Python venv
- **Setup**: `pip install processkit-py==1.5.0` into the shared venv (version tested in the bench)

### 7.5 Reconciled design (implemented 2026-11-11)

Critique `_INFO_HOW_TO_PREVENT_AGENTS_FROM_HANGING_CRITIQUE.md` [PRMTHANGFIX-IN04-RV01] found two design flaws in 7.1-7.4: the wrapper of section 6.3 would be rewritten by the agent for every command and copied into 6+ files, and the terminal rule already existed in 10+ copies with different on-cap targets. Implemented change:

- **Shipped runner** `skills/terminal-robustness/run-supervised.ps1`: logs `START` / `DONE` / `TIMEOUT` with `elapsed=`, empty stdin, `PYTHONUNBUFFERED`, `Start-Process` with output files, processkit deadline and Job Object; fallback `Kill($true)` with a WARN line. Call: `pwsh -NoProfile -NonInteractive -File [AGENT_FOLDER]/skills/terminal-robustness/run-supervised.ps1 -Script _agentwork/.tmp_[purpose].ps1 -Cap [seconds]` [TESTED]
- **Bench result for the shipped file**: with processkit 27/27; input waits end after about 1.8 s instead of at the cap; fallback without processkit 24/27 (fails HC-11, HC-21, HC-27) [TESTED]
- **Live output through the runner**: unchanged Python script 5 lines visible after 5 s, unchanged PowerShell script 4 lines [TESTED]

One home per concept (every other file references, never restates):
- **Whitelist, runner call, runtime check, hard bans, failure target**: `rules/agent-behavior.md` Terminal Hang Prevention
- **Cascade tool mechanics** (`Blocking: false` + timer, polling, shared terminals): `rules/devin-cascade.md` Terminal Limits
- **Mechanisms, evidence, runner, card structures**: `skills/terminal-robustness/` (guides, `run-supervised.ps1`, `ROBUSTNESS_CARD_SKELETON.md`)
- **Project bans and caps**: robustness card (no generic rules; no on-cap, kill or findings sections)
- **Run failures**: Fails card (replaces the robustness card findings feed; findings card keeps content glitches only)
- **Prompt integration**: `PROMPTS_ROBUSTNESS_GUIDES.md` Sections 2 and 2b, `PROMPTS_RULES.md` PRMT-HS-01..05 and PRMT-RB-08
- **Prompt text**: one hang-safety line (references) + one runtime-check line

Differences to the proposal in 7.1-7.4: the agent no longer writes the wrapper (C1 is a file, not a pattern); no launch line with a venv path in prompts; the hook (C7) is still not included.

Superseded in part by section 7.6: the runner no longer has `-Cap`, a deadline, or a `TIMEOUT` line.

Not yet done: processkit installed into the shared venv (`pip install processkit-py==1.5.0`); sync of `PromptSystemV4.7/` into the agent folder; live acceptance test T3.

### 7.6 Correction: no deadline, the agent decides (implemented 2026-11-11)

The design of 7.5 ended every command at a time cap (`-Cap`, `processkit run --timeout`, log line `TIMEOUT`). The user rejected this (failure record PRMTHANGFIX-FL-0001): the goal is hang prevention, not a time slot for every command.

Why a cap is wrong:
- Elapsed time says how long a command runs, not whether it still works. A test suite that needs 16 minutes under a 15-minute cap is ended at minute 15 and run again with a raised cap: 31 minutes or more instead of 16
- The bench hid the problem: every legitimate case got a cap above its runtime
- The same argument that rejected the idle timeout (it kills legitimate silent work) applies to the deadline (it kills legitimate slow work). Every automatic kill on one signal has a legitimate case that looks the same

Current design:
- **Runner without deadline** (`run-supervised.ps1 -Script ... -Expected [seconds] -Topic [TOPIC]`): Job Object container, empty stdin, live output files. The expected seconds are only logged
- **Liveness lines**: every 30 s the runner logs `ALIVE elapsed= cpu= out= err= procs=` (CPU seconds of the whole tree, bytes of both output files, living processes)
- **Hang verdict by the agent**, the only reason to end a command: 1) the last output lines show a wait that cannot end (prompt, pager, lock); 2) past the expected runtime, no liveness value changed for 5 minutes, and the script has no known silent phase; 3) endless loop: above 3x expected, for 10 minutes only CPU grew and the work wrote nothing
- **Stop file**: the agent writes `.tmp_[purpose]_stop.txt` with the reason; the runner kills the whole tree and logs `KILLED reason=...`
- **Slow but finished** (`DONE` far above expected): the result is used and never re-run; the cause is recorded and the card's expected runtime corrected
- **Robustness card**: section "Time caps" became "Expected runtimes" with a note on known silent phases
- **Kill script**: while commands run, the runner keeps `.tmp_kill_[TOPIC].ps1` with one line per running command (living process IDs of its tree). The line is removed when the command ends. After a cancelled runner the line stays; the next runner start logs `LEFTOVER ... pids=... kill=[file]`, and agent or human runs the script. The topic in the name keeps several sequences in one `_agentwork/` folder apart

Evidence [TESTED 2026-11-11]:
- Bench run `runner5` (the harness plays the agent: stop file after 5 s in hang cases, kill script after the cancel): runner with processkit 27/27, fallback 25/27 (HC-11, HC-21). No legitimate case ended; input waits end after 1.3 to 2.9 s through the empty stdin without any verdict
- Without the kill script a cancelled runner left its tree alive (run `runner3`: HC-27 failed in 3 of 3 repeats, 7 survivors). processkit `--kill-on-parent-death` without `--timeout` did not end the tree; cause not verified
- Runner contract tests 14/14: stop file, `ALIVE` lines, 7 s of work with 2 s expected runs to `DONE`, kill script, `LEFTOVER`, `-Topic`

Not tested [ASSUMED]: whether agents apply the hang verdict correctly in live runs, and whether 5 and 10 minutes are the right thresholds. A real hang without a telling output line now costs those minutes instead of ending at a cap.

## 8. Target Architecture: How Everything Works Together

Sections 8.1 to 8.3 describe the design of 7.1 to 7.5, which still had a deadline. Where they say "cap", "deadline", or "exit 124 at the cap", the current behaviour is section 7.6: the agent's hang verdict and the stop file.

### 8.1 Layers after the change

```
Layer 1  Agent rules ─────────── always loaded
         ├─> inline whitelist (unchanged)
         ├─> every other command: supervised wrapper (C1)
         └─> every run_command: Blocking=false + timer, completion from log (C2, C6)

Layer 2  terminal-robustness skill ─── loaded before process-running commands
         ├─> mechanisms + evidence (2026-09 rig, 2026-11 bench, live probes)
         └─> card templates: Robustness (execution pattern) + Fails skeleton

Layer 3  Cards in _agentwork/ ─── per working folder
         ├─> Robustness card: banned list, caps, execution pattern (per folder)
         ├─> Fails card: "Never again" list + failure entries (per sequence)  (C3)
         └─> Findings card: content glitches only

Layer 4  Prompt files ─── one prompt per turn
         ├─> hang-safety clause -> Robustness card
         ├─> runtime-check line -> Fails card                                 (C4)
         └─> findings directive -> Findings card

Optional pre_run_command hook ─── blocks non-whitelisted inline commands      (C7)
```

### 8.2 Lifecycle of one command

1. Agent states the expected runtime and checks the Fails card "Never again" list
2. Agent writes the wrapper `_agentwork/.tmp_[purpose].ps1` (section 6.3): `START` line, environment (`PYTHONUNBUFFERED=1`), `Start-Process` with output files, `DONE exit=N` line. The project script is not touched
3. Agent runs one short launch line:

```powershell
[VENV]\Scripts\processkit.exe run --timeout [cap] --kill-on-parent-death -- pwsh -NoProfile -NonInteractive -File _agentwork\.tmp_[purpose].ps1 > _agentwork\.tmp_[purpose]_launch.txt 2> _agentwork\.tmp_[purpose]_launch_err.txt
```

   with `Blocking=false` and `WaitMsBeforeAsync` = (expected + 5) * 1000, max 60000
4. Agent reads `.tmp_[purpose]_log.txt` with `read_file`:
   - `DONE` present: read `_out.txt` / `_err.txt`, compare runtime, continue
   - no `DONE`: `command_status` with `WaitDurationSeconds=60` (returns early if the tool sees completion), then read the log again; repeat until `DONE` or the cap
5. At the cap processkit kills the whole job (exit 124, message in `_launch_err.txt` after exit); agent writes the Fails entry
6. Agent deletes the wrapper and output files after use

Why each part is there:
- **processkit**: the only tested solution that ends every hang type and every descendant (27/27)
- **Wrapper log**: the only completion signal that is reliable in both directions (section 4.3)
- **`Start-Process` + `PYTHONUNBUFFERED`**: the only tested way to see live output of unchanged scripts (section 6.2)
- **Timer on every call**: bounds the agent's wait even when the tool misses completion
- **Short launch line**: under 200 characters of logic, no nested quotes, so no `>>` prompt (RC-2)

### 8.3 Lifecycle of one prompt and one sequence

```
/write-prompts
├─> Robustness card (from template) + Fails card (empty) + Findings card
└─> prompts: hang-safety clause + runtime-check line + findings directive
    │
    v
Prompt N starts
├─> read cards; read Fails "Never again" list
├─> for each command: section 8.2
│   └─> failure -> Fails entry at once; second repeat -> stop prompt
└─> end: findings filed, PROGRESS.md, commit
    │
    v
Prompt N+1 starts
└─> reads the Fails card -> avoids every recorded pattern
    │
    v
Sequence end
└─> "Never again" lines promoted to the Robustness card banned list
```

## 9. Failure-to-Defense Map

Which layer catches which failure after the change. "First defense" prevents, "backstop" ends it, "memory" prevents the repeat.

- **`>>` continuation prompt (RC-2)**: first defense short launch line + whitelist (C1, C7); backstop hang verdict + stop file; memory Fails card
- **stdin, pager, REPL, native y/n prompt**: first defense card bans + `-NonInteractive`; backstop empty stdin (ends within about 3 s), then hang verdict from the output line; memory Fails card
- **Network, lock, `Wait-Process`, `Get-Content -Wait`, infinite loop**: first defense card bans and native timeouts; backstop hang verdict from unchanged liveness values + stop file; memory Fails card
- **Slow legitimate work**: runs to its end; recorded as runtime overrun, never ended and never re-run
- **Grandchild holding the pipe, orphan without parent, deep tree**: backstop processkit Job Object (HC-11, HC-20, HC-21 passed); PowerShell tree kills do not cover this
- **stderr flood, `2>&1` merge**: first defense redirect to files and ban on `2>&1` (measured 2026-09)
- **Tool completion miss (RC-8)**: first defense timer on every call (C2); detection `DONE` in the wrapper log; memory Fails card class "completion miss"
- **Tool reports done too early**: detection missing `DONE` in the wrapper log; agent keeps polling
- **UI cancel kills only the top process (HC-27)**: backstop kill script with the tree's process IDs, `LEFTOVER` line at the next runner start (passed when the kill script is run); processkit `--kill-on-parent-death` passed only together with `--timeout`
- **Shared terminal reads another conversation's input (RC-9)**: first defense no command that reads stdin; untested whether this alone prevents all cross-talk
- **Repeat of a known failure (RC-5)**: Fails card "Never again" list checked before every command; stop on second repeat
- **Conversation or IDE crash**: not prevented; state on disk (cards, logs, PROGRESS.md) lets the next prompt resume

## 10. Open Questions and Untested Parts

Must pass before roll-out:
- **T1 Final wrapper against the 27 cases**: done with the shipped `run-supervised.ps1`: 27/27, also without deadline (run `runner5`, section 7.6) [TESTED]
- **T2 stdin under the runner**: done: the empty stdin file ends input waits after 1.3 to 2.9 s [TESTED]
- **T4 Hang verdict in live runs**: whether agents end real hangs and leave slow work alone; thresholds 5 and 10 minutes. Status: not run [ASSUMED]
- **T3 Live run in Cascade**: a short test sequence (about 5 prompts) that deliberately triggers 3 hang types and 1 completion miss; success = 0 human cancels, every failure in the Fails card, runtime check flags the slow command. Status: not run

Open, lower priority:
- **processkit `--stdout-file`** as an alternative to `Start-Process` for live output [ASSUMED]
- **processkit maturity**: young project (crate created 2026-05-31); procgov is older but fails HC-27. Facts [VERIFIED]; risk judgment [ASSUMED]
- **Hook**: whether a Cascade `pre_run_command` hook can block a call live and see the `Blocking` setting; the candidate classified 23/23 sample command lines correctly, offline only [TESTED]; live blocking [ASSUMED]
- **RC-8 frequency and trigger**: 1 in 13 in one sample; link to shared terminals (RC-9) not shown [ASSUMED]
- **Idle detection**: the agent judges progress from the `ALIVE` lines (CPU seconds, output bytes); scripts that are silent and use no CPU by design (waiting on a network call) need a silent-phase note in the Robustness card, else the agent may end them after 5 minutes
- **IDE crashes** during the bench work: cause unknown; no leftover bench processes were found afterwards

## 11. Next Steps

Steps 1 to 3 are done (sections 7.5 and 7.6). Open: mirror and sync of `PromptSystemV4.7/`, T3 and T4 in a real Cascade session (the acceptance prompts must be adapted to the hang verdict first), step 5.

1. Run T1 and T2 with the bench (`hangbench.ps1` with a new solution adapter for the final wrapper)
2. Decide the change set (C1-C7) based on T1/T2 results
3. Implement in `PromptSystemV4.7/` per section 7.4, then sync to the agent folder
4. Run T3 as acceptance test in a real Cascade session
5. After the first real sequences: review Fails cards, promote recurring "Never again" lines into the robustness card template

## 12. Sources

**PromptSystem files (state 2026-11-11):**
- `PRMTHANGFIX-IN04-SC-PSYS-AGBHV`: `PromptSystemV4.7/rules/agent-behavior.md` - Terminal Hang Prevention, Long-Running Commands, `_agentwork/` lifecycle [VERIFIED]
- `PRMTHANGFIX-IN04-SC-PSYS-DVCSC`: `PromptSystemV4.7/rules/devin-cascade.md` - Terminal Limits, Tool-Call Payload Limit [VERIFIED]
- `PRMTHANGFIX-IN04-SC-PSYS-TRSKL`: `PromptSystemV4.7/skills/terminal-robustness/SKILL.md` - dispatch, core procedure [VERIFIED]
- `PRMTHANGFIX-IN04-SC-PSYS-TRGDS`: `PromptSystemV4.7/skills/terminal-robustness/TERMINAL_ROBUSTNESS_GUIDES.md` - OS mechanisms, card lifecycle, two-tier defense [VERIFIED]
- `PRMTHANGFIX-IN04-SC-PSYS-TRRLS`: `PromptSystemV4.7/skills/terminal-robustness/TERMINAL_ROBUSTNESS_RULES.md` - HG, EX, CD rules [VERIFIED]
- `PRMTHANGFIX-IN04-SC-PSYS-TRDCG`: `PromptSystemV4.7/skills/terminal-robustness/DevinCascade/TERMINAL_ROBUSTNESS_GUIDES.md` - measured tool behavior, tier-2 pattern [VERIFIED]
- `PRMTHANGFIX-IN04-SC-PSYS-TRCRD`: `PromptSystemV4.7/skills/terminal-robustness/DevinCascade/ROBUSTNESS_CARD_TEMPLATE.md` and `ROBUSTNESS_CARD_SKELETON.md` - card structure and defaults [VERIFIED]
- `PRMTHANGFIX-IN04-SC-PSYS-PRRBG`: `PromptSystemV4.7/skills/write-documents/PROMPTS_ROBUSTNESS_GUIDES.md` - hang-safety clause, findings card, examples 5.1 and 7.3 [VERIFIED]
- `PRMTHANGFIX-IN04-SC-PSYS-WRPRM`: `PromptSystemV4.7/workflows/write-prompts.md` - Step 1 card creation, PRMT-HS and PRMT-RB checks [VERIFIED]

**Investigations and research (session documents):**
- `PRMTHANGFIX-IN04-SC-TRINV-IN01`: `_INFO_TERMROBUSTNESS-01_HangingCommandInvestigation.md` - 18 hang mechanisms from downstream repos [VERIFIED]
- `PRMTHANGFIX-IN04-SC-TRINV-LOG`: `_LOG_TERMROBUSTNESS.md` - rig measurements: 4KB buffer, pipe EOF wait, 2.3KB/s stderr drain, merge OOM [TESTED]
- `PRMTHANGFIX-IN04-SC-PHFIX-IN01`: `_INFO_PRMTHANGFIX-IN01_WindowsHangPreventionTools.md` - Windows tools, Cascade hook [VERIFIED]
- `PRMTHANGFIX-IN04-SC-PHFIX-IN02`: `_INFO_PRMTHANGFIX-IN02_ClassicHangSupervisionPatterns.md` - deadline, inactivity timeout, restart limit [VERIFIED]
- `PRMTHANGFIX-IN04-SC-PHFIX-IN03`: `_INFO_PRMTHANGFIX-IN03_WindowsSupervisorTools.md` - procgov and processkit-py features, licenses, maturity [VERIFIED]

**Test bench (`_Sessions/!TerminalHangBench/`, moved from the session folder on 2026-11-11):**
- `PRMTHANGFIX-IN04-SC-HBNCH-CASES`: `hang-cases.ps1` - 27 cases with evidence per case [TESTED]
- `PRMTHANGFIX-IN04-SC-HBNCH-FULL1`: `results/full1.jsonl`, `results/full1.md` - 243 runs, 9 solutions [TESTED]
- `PRMTHANGFIX-IN04-SC-HBNCH-PROBE`: `live-probe.ps1`, `results/live-probe.jsonl` - completion detection in the real terminal [TESTED]
- `PRMTHANGFIX-IN04-SC-HBNCH-STRM`: `stream-test.ps1`, `results/streamtest.jsonl` - 9 streaming variants [TESTED]
- `PRMTHANGFIX-IN04-SC-HBNCH-HOOK`: `hook-candidate.ps1`, `results/hooktest-*.json` - offline hook classification 23/23 [TESTED]

**External tools:**
- `PRMTHANGFIX-IN04-SC-GHPGV-HOME`: https://github.com/lowleveldesign/process-governor - Process Governor, MIT, Job Object, `--timeout`, `--recursive` [VERIFIED]
- `PRMTHANGFIX-IN04-SC-PYPI-PKPY`: https://pypi.org/project/processkit-py/ - processkit-py 1.5.0, MIT [VERIFIED]
- `PRMTHANGFIX-IN04-SC-PKPY-CLI`: https://zelanton.github.io/processkit-py/cli.html - `run` flags, exit codes 123 and 124 [VERIFIED]

## 13. Document History

**[2026-11-11 20:20]**
- Added: Section 7.6 - time cap removed after user correction (PRMTHANGFIX-FL-0001); runner without deadline, liveness lines, hang verdict by the agent, stop file, kill script per topic; bench run `runner5` and contract tests 14/14
- Changed: Summary, sections 1.1, 2 (RC-3), 5.4, 6.3, 7.3, 7.5, 8 (note), 9, 10, 11 - every conclusion that recommended a deadline corrected or marked superseded

**[2026-11-11 18:35]**
- Added: Section 7.5 reconciled and implemented design (shipped runner, one home per concept, bench and streaming results) after `/critique` and `/reconcile`
- Changed: Summary and section 10 (T1, T2 done)

**[2026-11-11 18:20]**
- Added: Section 7.2 rules for writing "Never again" lines and a worked Fails card example with walkthrough (`/improve` Phase 3)
- Changed: Results and streaming tables converted to lists (tables tag removed, only the user may set it)
- Changed: Acronyms written out (RC, HC, OOM, CIM, EOF, JSONL, GPL); non-standard verification labels replaced
- Changed: Runtime-check threshold made unambiguous (both 3x expected and expected + 30 s)
- Changed: Robustness card described as per working folder until `/cleanup`, not permanent
- Fixed: HC-19 claim labeled [ASSUMED from timing]; completion-miss count phrased as 13 commands
- Added: Note on `Start-Process -NoNewWindow` handle inheritance under processkit [ASSUMED, test T1]

**[2026-11-11 18:04]**
- Initial research document created: current layers, root causes RC-1 to RC-10, HANGBENCH results, streaming test, proposed Fails card and change set
