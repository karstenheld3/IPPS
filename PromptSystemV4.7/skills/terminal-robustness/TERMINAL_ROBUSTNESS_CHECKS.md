# Terminal Robustness Checks

Audits process discipline and quality of terminal command execution. Consumed AFTER execution: PD by `/drift-detect`, QI by `/improve`. Invisible to the working agent during execution (gaming prevention).

**Evidence sources:** command history in conversation, runner logs (`_agentwork/.tmp_*_log.txt`), Fails card, session PROBLEMS.md, PROGRESS.md entries.

## Process Discipline (PD)

### TERMROBUSTNESS-PD-01: Risk classification before risky commands

- Action: Agent classified command risk (interactive / volume / child) before running process-spawning commands
- Evidence: conversation shows classification or card load before the command
- Failure indicator: process-running command appears with no prior risk consideration
- References: TERMROBUSTNESS-EX-02

### TERMROBUSTNESS-PD-02: Card loaded or created before risky work

- Action: Agent loaded the project `__CARD_*-Robustness.md`, or created one from the agent template when none existed
- Evidence: card file exists with template sections; conversation shows load before commands
- Failure indicator: risky commands ran with no card in scope and none created
- References: TERMROBUSTNESS-CD-01, TERMROBUSTNESS-CD-02

### TERMROBUSTNESS-PD-03: No banned patterns in executed commands

- Action: No `2>&1` on stderr-heavy commands, no stdin/pager waits, no unbounded children in executed commands
- Evidence: command history shows redirects to file, `--no-pager`, non-interactive flags
- Failure indicator: any executed command matching HG-01 through HG-04 violations
- References: TERMROBUSTNESS-HG-01, HG-02, HG-03, HG-04

### TERMROBUSTNESS-PD-04: Monitored, ended only on a hang verdict

- Action: Every non-whitelisted command ran through the supervised runner with `-Expected`; the agent read the `ALIVE` lines while waiting; a command was ended only after a hang verdict, through the stop file
- Evidence: runner log lines with `expected=`; for each `KILLED` line a Fails card entry with hang evidence (wait shown in the output, or unchanged `ALIVE` values and their time span)
- Failure indicator: command ran without the runner; `KILLED` while the preceding `ALIVE` lines showed growing `cpu=`, `out=`, or `err=` and no endless-loop evidence; `KILLED` with no record; a finished command re-run only because it was slow; agent waited on a command whose output showed an input prompt
- References: TERMROBUSTNESS-EX-02, EX-03

### TERMROBUSTNESS-PD-05: Failures recorded in the Fails card

- Action: Every `KILLED`, `ERROR`, unexpected exit, runtime overrun, and completion miss recorded at once in the Fails card of the working folder (created at the first failure if absent), with a "Never again" line
- Evidence: Fails card entries whose time matches the runner log line; card exists after the first failure in chat tasks as well as in prompt sequences
- Failure indicator: a hang discussed in conversation with no card entry
- References: TERMROBUSTNESS-CD-04

### TERMROBUSTNESS-PD-06: Non-whitelisted commands ran as temp scripts through the runner

- Action: Every command outside the inline whitelist ran as `_agentwork/.tmp_` script through `run-supervised.ps1`; results read with the file tool
- Evidence: command history shows only whitelisted inline commands and `run-supervised.ps1 -Script _agentwork/.tmp_*` lines
- Failure indicator: inline pipeline, multi-statement, loop, or long command line in the terminal; results read from terminal output
- References: TERMROBUSTNESS-EX-04

### TERMROBUSTNESS-PD-07: Temp files removed after consumption

- Action: Temp scripts and their output files deleted once their content was consumed
- Evidence: no `.tmp_*` files from the task remain in `_agentwork/` at task end
- Failure indicator: `.tmp_*` scripts or `_out.txt` / `_err.txt` files left after the task
- References: TERMROBUSTNESS-EX-05

## Quality Improvement (QI)

### TERMROBUSTNESS-QI-01: Expected-runtime accuracy and hang-verdict quality

- Question: Do the card's expected runtimes match the `elapsed=` values of the runner logs, and are known silent phases noted? Was every hang verdict right (the replacement command finished), and was any real hang left waiting far longer than the verdict rule requires?
- Improvement tip: Replace starting values with measured ones per command class; note silent phases ("no output until the summary") so that silence there is not read as a hang. Give silent long scripts a progress line per step so the liveness signal is unambiguous

### TERMROBUSTNESS-QI-02: Banned-list completeness

- Question: Does the card's banned list cover the project's actual stack (build scripts, test runners, watchers), or only generic entries?
- Improvement tip: Run the Section 4.3 build procedure (search for pause/Read-Host/watch flags, 5-second probe tests) and add the findings

### TERMROBUSTNESS-QI-03: Redirect-pattern adoption

- Question: Did inline commands stay within the whitelist, or did borderline commands slip through inline?
- Improvement tip: When in doubt, use a temp script through the runner rather than narrowing pipelines - it eliminates the pipe mechanisms and adds containment and liveness lines

### TERMROBUSTNESS-QI-04: Card reuse within the working folder

- Question: Are the Robustness and Fails cards in `_agentwork/` reused over the working folder's lifetime, or recreated per prompt? Did the final checkpoint prompt promote "Never again" lines, and did `/cleanup` carry recurring lines out before deleting the cards?
- Improvement tip: Keep one card of each kind per working folder; promote per the Fails card rules in `ROBUSTNESS_CARD_SKELETON.md`
