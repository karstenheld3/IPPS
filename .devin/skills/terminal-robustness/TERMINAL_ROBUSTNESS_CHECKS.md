# Terminal Robustness Checks

Audits process discipline and quality of terminal command execution. Consumed AFTER execution: PD by `/drift-detect`, QI by `/improve`. Invisible to the working agent during execution (gaming prevention).

**Evidence sources:** command history in conversation, session PROBLEMS.md, robustness card Findings Feed, PROGRESS.md entries.

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
- Evidence: command history shows redirects to file, `--no-pager`, caps, non-interactive flags
- Failure indicator: any executed command matching HG-01 through HG-04 violations
- References: TERMROBUSTNESS-HG-01, HG-02, HG-03, HG-04

### TERMROBUSTNESS-PD-04: Caps and kill protocol followed

- Action: Time-capped commands with process-tree kill and PROBLEMS.md recording on cap
- Evidence: PROBLEMS.md entries for capped commands; no evidence of parent-only kills
- Failure indicator: command ran unbounded, or cap hit with no kill/record
- References: TERMROBUSTNESS-EX-02, EX-03

### TERMROBUSTNESS-PD-05: Findings recorded in the card

- Action: Hangs and near-hangs recorded in the card Findings Feed
- Evidence: Findings Feed entries added during or after the session
- Failure indicator: a hang discussed in conversation with no card entry
- References: TERMROBUSTNESS-CD-04

## Quality Improvement (QI)

### TERMROBUSTNESS-QI-01: Cap sizing judgment

- Question: Are the time caps proportionate to command class (roughly 3x expected duration), or generic one-size values?
- Improvement tip: Tune caps per command type in the card (e.g., 30s git, 3min single test file, 10min suite, 15min build) instead of a blanket cap

### TERMROBUSTNESS-QI-02: Banned-list completeness

- Question: Does the card's banned list cover the project's actual stack (build scripts, test runners, watchers), or only generic entries?
- Improvement tip: Run the Section 4.3 build procedure (search for pause/Read-Host/watch flags, 5-second probe tests) and add the findings

### TERMROBUSTNESS-QI-03: Redirect-pattern adoption

- Question: Could verbose inline commands have been replaced by the tmp-script + redirect + file-read pattern?
- Improvement tip: When output exceeds a few KB, switch to the redirect pattern rather than narrowing pipelines - it eliminates all three mechanisms at once

### TERMROBUSTNESS-QI-04: Card reuse across sessions

- Question: Is the card durable (project root) and extended over time, or recreated per session?
- Improvement tip: Store the card at project root, reference it from prompt sequences, and extend its Findings Feed - institutional memory beats per-session rediscovery
