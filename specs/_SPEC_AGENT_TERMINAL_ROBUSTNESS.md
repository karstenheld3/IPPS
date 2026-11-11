# SPEC: Agent Terminal Robustness

**Doc ID**: AGENTTERMINAL-SP01
**Feature**: AGENT_TERMINAL_ROBUSTNESS
**Goal**: Specify the target state of all parts that keep agent terminal commands from hanging (rules, skill, runner, cards, prompt-writing files, audit workflows): which part owns which concept, how the parts work together, and which requirements they fulfill
**Timeline**: Created 2026-11-11, Updated 8 times (2026-11-11 - 2026-11-11)
**Target file(s)**:
- `PromptSystemV4.7/rules/agent-behavior.md`, `PromptSystemV4.7/rules/devin-cascade.md`, `PromptSystemV4.7/rules/tools-and-skills.md`
- `PromptSystemV4.7/skills/terminal-robustness/` (all files)
- `PromptSystemV4.7/skills/write-documents/PROMPTS_RULES.md`, `PROMPTS_ROBUSTNESS_GUIDES.md`, `PROMPTS_TEMPLATE.md`, `PROMPTS_CHECKS.md`, `PROMPTS_GUIDES.md`
- `PromptSystemV4.7/workflows/write-prompts.md`, `verify.md`, `cleanup.md`
- `.devin/` deployment mirror of all above

**Depends on:**
- `_SPEC_TERMINAL_ROBUSTNESS_SKILL.md [TERMROBUSTNESS-SP01]` for skill folder anatomy, agent variant subfolders, and GRUC (Guides, Rules, Checks) placement of the skill
- `_SPEC_GRUC_STANDARD.md [GRUC-SP01]` for GRUC file types and their consuming workflows
- `_SPEC_IPPS_PROMPT_FILE_FORMAT.md [IPPSPRMTFMT-SP01]` for prompt file syntax and execution model
- `_SPEC_AGENT_CREATED_FOLDERS.md [AGNTFOLDERS-SP01]` for `_agentwork/` placement and `.tmp_` lifecycle
- `_INFO_HOW_TO_PREVENT_AGENTS_FROM_HANGING.md [PRMTHANGFIX-IN04]` for evidence, bench results, and rejected alternatives

**Does not depend on:**
- `_SPEC_IPPS_KNOWLEDGE_BUNDLE_FORMAT.md [IPPSSKBNDL-SP01]` (no knowledge bundle involved)

**Supersedes in TERMROBUSTNESS-SP01:** FR-04 (skeleton sections), FR-07 and NFR-01 (rule section size), FR-11 (findings directive), FR-13 (consumption modes). All other SP01 items stay valid.

## MUST-NOT-FORGET

- The goal is hang prevention, not runtime limits: no command is ended for its runtime; only a hang verdict of the agent ends a command (AGENTTERMINAL-FR-21, DD-13)
- One home per concept; every other file references the home and never restates the procedure (AGENTTERMINAL-FR-01)
- Existing project scripts run unchanged; protection wraps them from outside (AGENTTERMINAL-FR-03)
- Finished = runner log line, never the terminal tool's status (AGENTTERMINAL-FR-05)
- The fallback without processkit is degraded (25/27), never presented as equivalent (AGENTTERMINAL-DD-03)
- No change to the runner or the execution pattern ships without a full bench pass (AGENTTERMINAL-FR-17)
- Fails card = run failures; Findings card = content glitches; PROBLEMS.md = deferred problems and prompt stops. No entry in two places (AGENTTERMINAL-FR-13)
- Cards and promoted template lines hold command shapes, never secret values; synced files stay generic (Pre-Write Privacy Gate, AGENTTERMINAL-IG-06)
- This spec defines WHAT and WHO OWNS IT, not the wording of the owned content

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Design Decisions](#6-design-decisions)
7. [Implementation Guarantees](#7-implementation-guarantees)
8. [Key Mechanisms](#8-key-mechanisms)
9. [Action Flow](#9-action-flow)
10. [Data Structures](#10-data-structures)
11. [Logging Requirements](#11-logging-requirements)
12. [Technical Constraints](#12-technical-constraints)
13. [Change Plan](#13-change-plan)
14. [Implementation Verification Checklist](#14-implementation-verification-checklist)
15. [Document History](#15-document-history)

## 1. Scenario

**Problem:**
- Three different failures look identical to the user ("the step is spinning"): 1) the process hangs (pipe held open, input wait, unbounded child), 2) the process finished but the terminal tool never reports completion, 3) the conversation or IDE crashes
- Text rules alone do not hold: agents break the inline whitelist at the point of action, and a hang observed in one prompt is not recorded, so later prompts repeat it
- The same terminal rules existed in more than 10 files (rules, skill, card templates, prompt rules, prompt template, workflow examples) with different on-cap targets; each copy drifted
- Agent-written wrappers per command were long, varied per call, and error-prone
- Existing project scripts (100+) cannot be rewritten to add logging or timeouts

**Solution:**
- One shipped supervised runner wraps every non-whitelisted command from outside: process-tree container, empty stdin, live output files, liveness and completion log, whole-tree kill on the agent's request, kill script for leftovers. It has no deadline
- The agent monitors: a command that shows progress runs to its end; the agent ends a command if and only if the evidence shows a hang
- One home per concept: generic rule, agent tool rule, skill (mechanisms, evidence, runner, templates), project card, run failure card, prompt-writing files
- Three defense layers: prevent (whitelist, bans, "Never again" list), catch (liveness lines, hang verdict, whole-tree kill, runtime check), remember (Fails card, promotion to the project card and agent templates)
- Prompt files carry exactly two robustness lines per implementation prompt: one hang-safety reference line and one runtime-check line

**What we don't want:**
- A time limit that ends a command which still makes progress: the finished part is lost and the command runs again, which costs more than waiting
- Rewriting existing project scripts to add logging, flushing, or timeouts
- Monitoring, hang-verdict, kill, or cleanup steps restated in prompts, cards, or workflow examples
- Completion decided from the terminal tool's status or output
- Blocking terminal calls
- The same failure recorded in the Fails card, the Findings card, and PROBLEMS.md
- An untested execution pattern rolled out; the fallback runner presented as equivalent to the processkit runner
- A command hook as the enforcement layer before it is tested live

### Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Layer 1  Rules (always loaded)                                               │
│   agent-behavior.md ......... whitelist, runner call, runtime check,         │
│                               hard bans, failure target                      │
│   devin-cascade.md .......... non-blocking calls, polling, shared terminals  │
│   tools-and-skills.md ....... processkit location, long-running commands     │
├──────────────────────────────────────────────────────────────────────────────┤
│ Layer 2  Skill terminal-robustness (loaded before risky work)                │
│   SKILL.md ── dispatch ──> ClaudeCode/ | DevinCascade/ (guide + template)    │
│   GUIDES (mechanisms, evidence) · RULES (/verify) · CHECKS (/drift-detect,   │
│   /improve) · ROBUSTNESS_CARD_SKELETON.md · run-supervised.ps1               │
├──────────────────────────────────────────────────────────────────────────────┤
│ Layer 3  Working-folder artifacts (_agentwork/)                              │
│   __CARD_[TOPIC]-Robustness.md ... bans, expected runtimes, alternatives     │
│   __CARD_[TOPIC]-Fails.md ........ run failures, "Never again" list          │
│   __CARD_[TOPIC]-Findings.md ..... content glitches (not terminal)           │
│   .tmp_[purpose].ps1 + _log/_out/_err/_in.txt ... one runner call each       │
├──────────────────────────────────────────────────────────────────────────────┤
│ Layer 4  Prompt files (_PROMPTS_[NN]-[Topic].md)                             │
│   per implementation prompt: 1 hang-safety line + 1 runtime-check line       │
│   written by /write-prompts per PROMPTS_RULES.md + PROMPTS_ROBUSTNESS_GUIDES │
└──────────────────────────────────────────────────────────────────────────────┘
```

## 2. Context

- Evidence base: HANGBENCH test bench (27 cases: hang, legitimate long-running, and cancel cases) and live probes in Cascade, documented in PRMTHANGFIX-IN04. Results: processkit-backed runner 27/27; Process Governor 26/27; every other tested pattern (PowerShell-only tree kills, GNU `timeout`) 24/27 or less; the former card pattern (tmp script + redirect) 8/27
- Those results come from the first runner version, which ended every command at a time cap. The cap was removed on 2026-11-11 (PRMTHANGFIX-FL-0001: it ended slow work that would have finished and forced a second run). Bench run `runner5` of the deadline-free runner: 27/27 with processkit, 25/27 in the fallback; in hang cases the harness plays the agent and creates the stop file, in the cancel case it runs the kill script
- Terminal tool behavior observed in Cascade: missed completion of a finished command (1 in 13 sub-second commands), "done" reported for a running command, terminals shared between concurrent conversations
- PowerShell `>` redirects deliver output only after the process exits; live output of an unchanged script needs `Start-Process` output files and, for Python, `PYTHONUNBUFFERED=1`
- TERMROBUSTNESS-SP01 created the skill and the robustness card; this spec defines the full system around it (runner, Fails card, ownership, prompt integration)
- Content is authored in `PromptSystemV4.7/`, mirrored to `.devin/`, and synced to consumer workspaces

### Concept ownership (BEFORE)

```
whitelist ........... agent-behavior.md, GUIDES, RULES, card templates
caps + on-cap ....... card templates, PROMPTS_RULES, PROMPTS_TEMPLATE, write-prompts examples
kill procedure ...... DevinCascade guide (Common Information Model (CIM) tree kill), ClaudeCode guide, card templates
failure record ...... card Findings Feed, Findings card, PROBLEMS.md (3 targets)
completion .......... terminal tool status
```

### Concept ownership (AFTER)

```
whitelist, runner call, runtime check, bans ... agent-behavior.md
monitoring, hang verdict, kill script use ..... agent-behavior.md
Fails card rules, promotion procedure ......... ROBUSTNESS_CARD_SKELETON.md
prompt lines (hang-safety, runtime check) ..... PROMPTS_ROBUSTNESS_GUIDES.md Sections 2 and 2b
long-running commands (over 60 s) ............. tools-and-skills.md Long-Running Commands
file search outside the workspace ............. terminal-robustness SKILL.md (Execute safely)
tool mechanics (blocking, polling) ............ agent rule file (devin-cascade.md)
containment, liveness, kill, stdin, log ....... run-supervised.ps1 (mechanism) + Robustness card (expected runtimes)
failure record ................................ Fails card of the working folder (chat mode and prompt sequences)
completion .................................... runner log end line DONE / KILLED / ERROR
```

## 3. Domain Objects

### Generic Terminal Rule

- **What**: Section "Terminal Hang Prevention" in `rules/agent-behavior.md`; always in context for every agent
- **Owns**: inline whitelist criteria, runner call line, completion criterion, monitoring rule, hang verdict, runtime check, kill script use, failure target, hard bans, pointers to agent tool rule, skill, and project card
- **Does not own**: mechanisms, evidence, expected runtimes per project, agent tool parameters

### Agent Tool Rule

- **What**: Section "Terminal Limits" in the agent-specific rule file (Cascade: `rules/devin-cascade.md`)
- **Owns**: how the agent's terminal tool is called (non-blocking, bounded first wait, polling until the runner log line appears), shared-terminal warnings, pointer to the skill variant
- **Does not own**: anything that holds for all agents

### Supervised Runner

- **What**: `skills/terminal-robustness/run-supervised.ps1`; the only containment and kill mechanism. It has no deadline
- **Input**: one tmp script (PowerShell or Python), expected seconds (logged only), topic (names the kill script), optional supervisor path
- **Owns**: process-tree container, liveness lines, whole-tree kill on the stop file, kill script, leftover report, empty stdin, live output files, unbuffered Python output, log lines, exit code propagation, degraded fallback when processkit is absent

### Runner Artifacts

- **What**: per call in `_agentwork/`: `.tmp_[purpose].ps1|.py` (agent-written work), `_log.txt` (runner lines), `_out.txt`, `_err.txt` (live child output), `_in.txt` (empty stdin), `_stop.txt` (written by the agent after a hang verdict; line 1 = reason)
- **Kill script**: `.tmp_kill_[TOPIC].ps1`, one per topic and working folder; one line per running runner call with the living process IDs of its tree
- **Lifecycle**: `.tmp_` per AGNTFOLDERS-SP01; deleted by the agent once consumed; leftovers removed by `/cleanup`

### Terminal Robustness Skill

- **What**: `skills/terminal-robustness/` per TERMROBUSTNESS-SP01: `SKILL.md` (entry, dispatch), shared GUIDES / RULES / CHECKS, `ROBUSTNESS_CARD_SKELETON.md`, agent variant folders with guide and card template, the runner
- **Owns**: mechanisms, evidence and bench results, card structures, card templates with tested defaults, audit criteria

### Robustness Card

- **What**: `_agentwork/__CARD_[TOPIC]-Robustness.md`, one per working folder, kept until `/cleanup`; copied from the agent card template
- **Owns**: project-specific banned commands with reason and source, expected runtimes per command class with known silent phases (seconds, passed to the runner as expected value; never a limit), project safe alternatives, agent tool limits (verbatim copy)
- **Does not own**: generic rules, hang verdict, kill steps, failure log

### Fails Card

- **What**: `_agentwork/__CARD_[TOPIC]-Fails.md`, one per working folder, kept until `/cleanup`; created by `/write-prompts` or by the agent at the first failure
- **Owns**: "Never again" list (command shape + trigger → replacement) and one entry per run failure
- **Consumers**: every command in the working folder, in chat mode and in prompt sequences (checked before run); promotion (source)

### Findings Card

- **What**: `__CARD_[TOPIC]-Findings.md`, one per prompt sequence
- **Owns**: content glitches only (spec/code mismatch, test drift, naming); no terminal failures

### PROBLEMS.md

- **What**: session tracking file; in PROJECT-MODE (no session) the workspace `PROBLEMS.md`
- **Owns**: deferred problems (e.g. processkit missing) and prompt stops after a repeated failure

### Prompt Robustness Lines

- **Hang-safety line**: one line in Constraints of every implementation prompt; references the generic terminal rule and the Robustness card; carries no procedure
- **Runtime-check line**: exactly one line per implementation prompt; names the Fails card and the check (monitor, end only on a hang verdict, expected vs `elapsed=`, write entry, stop on repeat)

### Prompt-Writing Files

- **What**: `PROMPTS_RULES.md` (PRMT-HS-01..11, PRMT-RB-01..08), `PROMPTS_ROBUSTNESS_GUIDES.md` (line templates, card roles), `PROMPTS_TEMPLATE.md`, `PROMPTS_CHECKS.md`, `workflows/write-prompts.md`
- **Owns**: where and how often the two lines appear, which cards a sequence creates or reuses, the promotion step in the final checkpoint prompt, verification of all three

### Audit Workflows

- `/verify`: card instances against skeleton and TERMROBUSTNESS-CD (card definition) rules; prompt files against PRMT-HS (hang safety) and PRMT-RB (robustness) rules
- `/drift-detect`: TERMINAL_ROBUSTNESS_CHECKS PD (process discipline) items: runner used, no command ended while it showed progress, failures recorded
- `/improve`: TERMINAL_ROBUSTNESS_CHECKS QI (quality improvement) items: expected runtimes measured, hang verdicts right, banned list complete, promotion done
- `/cleanup`: removes runner artifacts and `.tmp_` leftovers

### HANGBENCH

- **What**: hang test bench outside the shipped system; 27 hang cases (IDs HC-01..HC-27), one adapter per execution pattern, including the shipped runner and its fallback
- **Role**: rollout gate for every change to the runner or the execution pattern

### processkit

- **What**: external supervisor (`processkit-py`, tested version 1.5.0) in the shared Python venv; location registered in `rules/tools-and-skills.md`
- **Role**: provides the Job Object container and its tree kill to the runner; its deadline option is not used

## 4. Functional Requirements

**AGENTTERMINAL-FR-01: One Home per Concept**
- Each concept in Section 2 "Concept ownership (AFTER)" has exactly one owning file
- Every other file references the owner by file and section name and does not restate the procedure
- Examples, BAD/GOOD pairs, and superseded-pattern notes may quote a concept; they are marked as example or history
- One declared exception: the runtime-check line in prompts (AGENTTERMINAL-DD-07), copied verbatim from its single template in `PROMPTS_ROBUSTNESS_GUIDES.md` Section 2b; its thresholds equal those of the generic terminal rule

**AGENTTERMINAL-FR-02: Inline Whitelist**
- A command runs inline only if it meets all whitelist criteria of the generic terminal rule (single command, no pipe, no multiple statements, no loop, no stream merge, short line, short runtime, small output)
- Every other command runs through the supervised runner

**AGENTTERMINAL-FR-03: Supervised Execution Without Script Changes**
- The agent writes the work into one tmp script in `_agentwork/` and runs it through the runner
- Every `[purpose]` name ends with a time suffix (`HHmmss`), so concurrent calls of one agent or of concurrent conversations in the same working folder never share artifacts; if the name already exists (same second), the agent appends a letter; the runner overwrites the artifacts of an earlier call with the same name
- Existing project scripts are called from the tmp script unchanged; no project script needs logging, flushing, or timeout code
- PowerShell and Python scripts are supported

**AGENTTERMINAL-FR-04: Runner Contract**
- Sets no deadline: the child runs until it exits or until the stop file appears
- With processkit: on the stop file, ends the whole process tree, including grandchildren and orphans
- Gives the child an empty stdin
- Writes child stdout and stderr to separate files that grow while the child runs
- Writes one `START` line, one `ALIVE` line every 30 s (elapsed seconds, CPU seconds of the whole tree, bytes of both output files, living processes), and one `DONE` or `KILLED` line with exit code, elapsed and expected seconds; `KILLED` carries the reason from the stop file
- A child that exits with its own code 124 is logged as `DONE`
- Returns the child's exit code
- Without processkit: runs a fallback, writes a `WARN` line naming the degraded mode
- If the runner fails before the child starts (script or interpreter not found), it writes an `ERROR` line instead of `START` and exits with code 2, so the log never stays empty
- Child output is UTF-8: Python via `PYTHONIOENCODING`, PowerShell via the console output encoding set before the script runs, so `_out.txt` and `_err.txt` stay readable with the agent's file tool

**AGENTTERMINAL-FR-05: Completion from the Runner Log**
- A command is finished only when its `_log.txt` contains an end line: `DONE`, `KILLED`, or `ERROR`
- Terminal tool status and terminal output never decide completion

**AGENTTERMINAL-FR-06: Agent Tool Call Discipline**
- Every terminal call is non-blocking with a bounded first wait derived from the expected runtime
- While the log line is missing, the agent waits in bounded steps and re-reads the log, for as long as the `ALIVE` lines show progress; no wait count and no time limit ends a command
- Runner-gone check: no `START` line 60 s after the call (a queued terminal starts late), or no new `ALIVE` line for 90 s and no end line → the agent checks whether the runner process exists (`pid=` of the `START` line); no runner process → failure (class completion miss or runner error), surviving processes are ended and the failure is recorded
- Parameters live only in the agent tool rule

**AGENTTERMINAL-FR-07: Runtime Check**
- Before each runner call the agent states the expected seconds: the Robustness card value for the command class, else its own estimate
- The expected value starts the liveness check and feeds the comparison; it never ends a command
- After the end line the agent compares with `elapsed=` from the log
- Failure = `KILLED`, `ERROR`, unexpected exit code
- Runtime overrun = `DONE` with elapsed above both 3x expected and expected + 30 s: the result is valid and is used; the command is never re-run for being slow; the agent finds the cause, records it, and corrects the card's expected runtime

**AGENTTERMINAL-FR-08: Immediate Failure Recording**
- Every failure is recorded before any other step in the Fails card of the working folder; if none exists, the agent creates it from the Fails block of the skeleton at the first failure (chat mode and prompt sequences alike)
- Entries record command shapes, file names, and exit codes, never secret values (tokens, keys, passwords) from the command or its output
- Failure classes: process hang, completion miss, error exit, runtime overrun, runner error, parse error, tool-call drop, command repeated after it failed once
- Each entry carries a "Never again" line

**AGENTTERMINAL-FR-09: Repeat Prevention**
- Before each command the agent checks the Fails card "Never again" list and uses the replacement on a match
- Ending a command that still showed progress is itself a failure (false hang verdict) and is recorded as one
- The same failure twice in one prompt (chat mode: in one task) stops the prompt or task with a PROBLEMS.md entry; the sequence continues with the next prompt

**AGENTTERMINAL-FR-10: Promotion**
- "Never again" lines move to the Robustness card banned list at two triggers: the final checkpoint prompt of each prompts file, and when the list exceeds about 15 lines
- `/cleanup` deletes `_agentwork/` with both cards; before that it carries recurring lines out of the folder, generalized to a generic command shape (no project paths, names, or values): in IPPS into the agent card template, in downstream workspaces into workspace `FAILS.md` (the template is synced from IPPS and a local edit would be overwritten)

**AGENTTERMINAL-FR-11: Robustness Card Content**
- Created by copying the agent card template, then extended with project probes
- Contains only project-specific bans, expected runtimes in seconds with known silent phases, safe alternatives, and the verbatim agent tool limits
- Structure matches the Robustness block of the card skeleton

**AGENTTERMINAL-FR-12: Fails Card Content**
- Created from the Fails block of the card skeleton: by `/write-prompts` if absent, or by the agent at the first failure; reused by later sequences and chat tasks in the same working folder
- "Never again" lines describe a command shape plus trigger, not one exact command, so variants match too
- The replacement is a complete alternative the agent can run without further research (tool, call form, where completion is read)
- One line per root cause: a second failure with the same root cause extends the existing line; the list stays at about 15 lines so it can be read in full before every command [ASSUMED - limit not tested]

**AGENTTERMINAL-FR-13: Separate Records**
- Terminal and tool failures → Fails card; content glitches → Findings card; deferred problems and prompt stops → PROBLEMS.md
- No event is recorded in two of these places; PROBLEMS.md entries for prompt stops reference the Fails entry ID

**AGENTTERMINAL-FR-14: Prompt Integration**
- Every implementation prompt contains the hang-safety line and exactly one runtime-check line
- Prompts state no time limits, hang-verdict steps, kill steps, or cleanup steps
- `/write-prompts` creates or reuses the Robustness card and the Fails card and creates the Findings card before writing prompts
- The final checkpoint prompt of each prompts file contains the promotion step (FR-10)
- Verification sections use agent tools for search; folders outside the workspace use a tmp script through the runner

**AGENTTERMINAL-FR-15: Agent Variant Dispatch**
- `SKILL.md` selects the variant by agent identity (system prompt), not by agent folder
- An agent without a tested variant uses the minimum variant and fills agent tool limits from its own rule file

**AGENTTERMINAL-FR-16: Audit Coverage**
- `/verify` checks card instances and prompt files; `/drift-detect` checks process discipline; `/improve` checks quality; `/cleanup` removes runner artifacts
- Audit criteria reference the runner log and the Fails card as evidence

**AGENTTERMINAL-FR-17: Bench Gate**
- HANGBENCH lives in a versioned IPPS folder that is excluded from downstream sync, so the gate survives session archiving
- Every change to the runner or the execution pattern passes all HANGBENCH cases through the shipped file before rollout
- Results (per mode, failed case IDs) are recorded in the DevinCascade guide

**AGENTTERMINAL-FR-18: Setup and Deployment**
- processkit location and install command live in `rules/tools-and-skills.md`; the runner's default supervisor path is that location
- All files are authored in `PromptSystemV4.7/`, mirrored to `.devin/`, and synced downstream

**AGENTTERMINAL-FR-19: Long-Running Commands**
- Before a command expected to run over 60 s, the agent tells the user the estimated duration; a silent multi-minute command looks like a hang
- No time limit; repo-wide operations (history rewrite, gc) start only after a check for concurrent activity in the same repo
- While running, the agent reads the `ALIVE` lines and `_out.txt` between waits; only a hang verdict (FR-21) ends the command
- After a cancel or a `KILLED`, the agent confirms that no process of the command survives (FR-22)

**AGENTTERMINAL-FR-20: File Search Without Shell Pipelines**
- File search and read use agent tools
- Where the agent search tool cannot reach a folder (outside the workspace, or empty results for existing text), the search runs as `rg.exe` inside a tmp script through the runner, never as an inline `Select-String` or `Get-ChildItem` pipeline

**AGENTTERMINAL-FR-21: Monitoring and Hang Verdict**
- While a command runs, the agent compares successive `ALIVE` lines. Progress = CPU seconds or output bytes grew, or the work wrote its own files. A command with progress runs to its end, however far past its expected runtime
- The agent ends a command if and only if one of three conditions holds: 1) the last output lines show a wait that cannot end (input prompt, pager, key wait, lock nobody releases); 2) elapsed is past the expected runtime, no progress signal changed for 5 minutes, and the script has no known silent phase of that length; 3) endless loop: elapsed is above 3x expected and for 10 minutes only CPU seconds grew while no output and no file the work writes changed
- Ending = the agent creates the stop file with the reason; the runner kills the whole tree and logs `KILLED` with that reason
- In doubt the agent waits one more window. Thresholds live only in the generic terminal rule [ASSUMED - 5 and 10 minutes not tested live]

**AGENTTERMINAL-FR-22: Kill Script**
- While a command runs, the runner keeps its line in `.tmp_kill_[TOPIC].ps1` of the working folder: the living process IDs of the tree, refreshed when the set changes, restricted to processes started before the last refresh (a reused process ID is not hit)
- `[TOPIC]` comes from the runner parameter `-Topic` (topic of the running prompt file or STRUT, in chat mode the session topic), so sequences sharing one `_agentwork/` folder keep separate kill scripts; parallel commands of one topic each hold one line
- At the end of a command the runner removes its line and deletes the file when it is empty
- After a cancelled or crashed runner the line stays. The next runner start in the folder checks every kill script: lines whose processes are gone are dropped; for lines with living processes it writes `LEFTOVER script=... pids=... kill=[file]` before `START`
- Agent or human runs the kill script to end the leftover processes

## 5. Non-Functional Requirements

**AGENTTERMINAL-NFR-01: Context Cost - Always-Loaded Text**
- Generic terminal rule: at most 15 lines; agent tool rule terminal section: at most 10 lines
- Prompt robustness text: 2 lines per implementation prompt
- Verification: line count during `/verify`

**AGENTTERMINAL-NFR-02: Maintainability - No Duplicated Procedures**
- No procedure text (hang-verdict conditions, kill steps, whitelist criteria, runner call line) outside its owner, except marked examples and history notes
- Verification: text search over `PromptSystemV4.7/` during `/verify` for the phrases `On cap`, `-Cap `, `Time caps`, `at the cap`, `kill the process tree`, `Stop-ProcessTree`, `Findings Feed`, `non-blocking with a`, `_out.txt 2>`, `under 200 characters`; every hit is the owner, a marked example, or a history note

**AGENTTERMINAL-NFR-03: Reliability - Bench Result**
- Runner with processkit: 27/27 HANGBENCH cases, no surviving process; no legitimate case ended. Hang cases pass with the stop file, the cancel case with the kill script
- Runner fallback: result recorded with failed case IDs; never counted as passing
- Verification: HANGBENCH run through the shipped runner file

**AGENTTERMINAL-NFR-04: Observability - Live Progress**
- Output of an unchanged Python or PowerShell script (1 line per second or more) is readable from `_out.txt` within 2 s of being written, while the script runs
- Verification: streaming test through the shipped runner (lines visible before exit)

**AGENTTERMINAL-NFR-05: Isolation - Shared Terminals**
- No supervised command reads the terminal's stdin; input waits end within about 3 s with empty input, without any action of the agent
- Verification: HANGBENCH input-wait cases end before the harness creates the stop file

## 6. Design Decisions

**AGENTTERMINAL-DD-01:** Shipped runner instead of an agent-written wrapper per command. Rationale: one tested file replaces a pattern the agent rewrote per call in varying, error-prone forms; the bench tests exactly what agents run.

**AGENTTERMINAL-DD-02:** processkit as supervisor. Rationale: only tool with 27/27 in the bench of the deadline version, including runner cancellation (bench hang case HC-27) where Process Governor fails; without its deadline option processkit did not end the tree on runner cancellation (run `runner3`), which DD-14 covers; GNU `timeout` and the PowerShell-only patterns (24/27) miss pipe-holding grandchildren and orphans, because only a Job Object contains every descendant.

**AGENTTERMINAL-DD-03:** Fallback runs degraded instead of refusing. The runner logs `WARN`; at the first `WARN` of a session the agent tells the user and adds one PROBLEMS.md entry (deferred: install processkit); rollout requires processkit. Rationale: work stays possible on machines without the venv, while the known gaps (HC-11, HC-21) stay visible instead of silent.

**AGENTTERMINAL-DD-04:** Completion from a file written by the runner, not from the terminal tool. Rationale: the tool missed completion and reported early completion in live probes; no supervisor fixes the tool side, only a marker the command writes itself.

**AGENTTERMINAL-DD-05:** Separate Fails card instead of extending the Findings card or the Robustness card. Rationale: the Findings card got 0 hang entries in an 8-prompt sequence with an observed hang; a dedicated, short "Never again" list checked before each command is the point-of-action reminder [ASSUMED - effect not measured until the live test CP-16]; the Robustness card stays a stable project artifact.

**AGENTTERMINAL-DD-06:** Expected runtimes in the Robustness card, hang verdict in the generic rule, kill in the runner, no limit or kill text in prompts. Rationale: prompts are the copy most often ignored and most often drifted. Superseded part: cap enforcement by the runner (see DD-13).

**AGENTTERMINAL-DD-07:** The runtime-check line is the one deliberate repetition in prompts. Rationale: headless prompts compact context; one line per prompt keeps the Fails card at the point of action at minimal cost.

**AGENTTERMINAL-DD-08:** Empty stdin file for every supervised child. Rationale: shared terminals can deliver another conversation's input; empty stdin also ends input waits in about 3 s without any verdict.

**AGENTTERMINAL-DD-09:** Command hook deferred. Rationale: the hook candidate classified sample command lines correctly offline, but live blocking in Cascade is untested; text rules + runner + Fails card come first.

**AGENTTERMINAL-DD-10:** No idle timeout. Rationale: the idle-timeout variant killed legitimate silent work in the bench (HC-03 silent 8 s run, HC-24 `Select-Object -Last` buffering). Silence is a diagnosis input for the agent (Section 8), not a kill trigger. Superseded part: "deadline only" (see DD-13).

**AGENTTERMINAL-DD-11:** No process outlives its runner call. Rationale: the Job Object ends every member when the leader exits, so a detached child is removed too (HC-19 returned after 1.48 s with zero survivors) [ASSUMED from timing]; for unattended agents this is the wanted behavior. Long-lived servers and watchers are not started through the runner; they stay banned unless the user explicitly asks for one.

**AGENTTERMINAL-DD-13:** No deadline; the agent decides. The runner never ends a command on its own; it reports liveness, and the agent ends a command only on a hang verdict (FR-21). Rationale: a time cap ends legitimate work that only needs longer than estimated; the finished part is lost and the command runs again, so the cap costs more time than it saves (PRMTHANGFIX-FL-0001). The bench hid this because every legitimate case got a cap above its runtime. Every automatic kill on one signal (elapsed time, silence) has a legitimate case that looks the same; only the combination of signals, read with knowledge of what the script does, separates a hang from slow work. Cost: a real hang without a telling output line is ended after minutes instead of at a cap, and the verdict depends on the agent following the rule [ASSUMED - not tested live].

**AGENTTERMINAL-DD-14:** Kill script instead of kill-on-runner-death. Rationale: a runner that was cancelled cannot act, and processkit without its deadline option did not end the tree in 3 of 3 bench repeats. A file with the living process IDs, kept current by the runner, survives the runner; the next runner start reports leftovers, and agent or human can end them with one command. Rejected: a runner-owned kill-on-close Job Object (about 20 lines of native Windows calls in a synced file, untested). The topic in the file name keeps sequences that share one `_agentwork/` folder apart.

**AGENTTERMINAL-DD-12:** One Fails card per working folder for chat mode and prompt sequences, instead of one per sequence with PROBLEMS.md as the chat-mode target. Rationale: repeated failures in normal chat work are the most frequent case; PROBLEMS.md is not read before each command, so it cannot prevent repeats. One target removes a branch from the rule; promotion at the 15-line mark keeps the list short.

## 7. Implementation Guarantees

**AGENTTERMINAL-IG-01:** No project script is modified to gain protection; the runner wraps it from outside

**AGENTTERMINAL-IG-02:** In processkit mode, no descendant process of a supervised command survives a kill on the stop file; after a cancelled runner, every surviving process ID seen at the last tree scan is in the kill script

**AGENTTERMINAL-IG-07:** The runner never ends a command on its own; every `KILLED` line carries the reason the agent wrote into the stop file

**AGENTTERMINAL-IG-03:** Every `KILLED` and every runtime-check failure has exactly one failure record in the Fails card of the working folder, with a "Never again" line

**AGENTTERMINAL-IG-04:** A card instance can be verified against `ROBUSTNESS_CARD_SKELETON.md` without reading any write-documents file

**AGENTTERMINAL-IG-05:** A prompt written by `/write-prompts` passes PRMT-HS-01..05 and PRMT-RB-08 without containing any procedure text

**AGENTTERMINAL-IG-06:** No card, runner artifact kept beyond its task, or promoted template line contains a secret value; promoted template lines contain no project paths or names

## 8. Key Mechanisms

**Three defense layers** (each catches what the previous one misses):
- **Prevent**: inline whitelist, hard bans, Robustness card bans, Fails card "Never again" list checked before each command
- **Catch**: empty stdin (input waits); liveness lines, hang verdict, and whole-tree kill on the stop file (process hangs); runner log line and polling (tool completion misses); kill script and `LEFTOVER` line (cancelled runner); runtime check (slow work)
- **Remember**: immediate Fails card entry; stop on second repeat; promotion Fails card → Robustness card → agent card template

**Reference chain** (how a reader reaches the owner):
- Hang-safety line → generic terminal rule → agent tool rule / skill → Robustness card
- Runtime-check line → Fails card → skeleton (Fails card rules)
- Card → skeleton (structure) → skill RULES (CD rules)
- Workflow → skill (workflows point to skills; skill files do not point to other skills' GRUC files, per TERMROBUSTNESS-SP01)

**State diagnosis from runner files** (the only basis for the agent's next step; tool status is ignored):
- `START` + `DONE` with expected exit code, elapsed within the runtime check → finished; continue, even if the tool still shows running (completion miss, record it)
- `START` + `DONE`, elapsed above both 3x expected and expected + 30 s → slow work; use the result, record the runtime overrun, correct the expected runtime; never re-run
- `START` + `DONE` with unexpected exit code → error exit; read `_err.txt`
- `START`, no end line, `ALIVE` values growing (output bytes or CPU seconds) → working; keep polling, however long
- `START`, no end line, last output line is a prompt, pager, or lock message → hang; create the stop file at once
- `START`, no end line, all `ALIVE` values unchanged for 5 minutes past the expected time, no known silent phase → hang; create the stop file
- `START`, no end line, only CPU seconds growing for 10 minutes above 3x expected, no file of the work changed → endless loop; create the stop file
- `KILLED` → the agent ended a hang; the Fails entry carries the hang evidence
- `LEFTOVER` before `START` → processes of a cancelled command still run; run the named kill script
- `ERROR` or no `START` within the polling bound → runner error or launch problem (parse error, wrong path)

**Two card scopes:**
- Robustness card: per working folder, project knowledge, stable across sequences
- Fails card: per working folder, raw run knowledge from chat tasks and sequences, grows with every failure, emptied into the Robustness card by promotion

**Failure-to-defense map:**
- Continuation prompt from a long inline line with nested quotes → whitelist forbids that line shape; typed anyway, it runs unsupervised and only the non-blocking call keeps the agent free; Fails card prevents the repeat
- Pipe held by a grandchild or orphan → runner tree kill (processkit only)
- Input or pager wait → empty stdin; hang verdict from the output line as backstop
- Network wait, lock file, `Wait-Process`, endless loop → project bans and native timeouts; hang verdict from unchanged liveness values as backstop
- Slow legitimate work → runs to its end; never ended
- stderr flood or `2>&1` merge (pipe throttle, shell out-of-memory error) → hard ban on `2>&1`; output goes to files, not pipes
- Unbounded child (watcher, dev server) → hard ban; runner kills descendants when the script ends
- Tool misses completion → bounded non-blocking wait + runner log line
- Tool reports done too early → missing log line keeps the agent polling
- UI cancel kills only the top process → kill script with the tree's process IDs; `LEFTOVER` line at the next runner start
- Known failure repeated → "Never again" check; stop on second repeat
- Conversation or IDE crash → not prevented; cards, logs, and PROGRESS.md on disk let the next prompt resume

## 9. Action Flow

Chat mode (no prompt sequence):
```
Agent needs a command
├─> whitelist met? ── yes ──> run inline
└─> no
    ├─> Robustness card present? ──> apply bans, take expected runtime
    ├─> Fails card present? ──> check "Never again" list, use replacement on match
    ├─> write _agentwork/.tmp_[purpose].ps1 (calls existing scripts unchanged)
    ├─> state expected seconds
    ├─> terminal call: runner, non-blocking, bounded first wait
    ├─> poll _log.txt: ALIVE shows progress ──> keep waiting
    │   └─> hang verdict (FR-21) ──> write _stop.txt ──> runner kills tree, logs KILLED
    ├─> end line DONE | KILLED | ERROR
    ├─> read _out.txt / _err.txt
    ├─> runtime check
    │   └─> failure ──> Fails card entry at once (create card if absent)
    │       └─> same failure again in this task ──> stop task + PROBLEMS.md entry
    └─> delete tmp script + artifacts
```

Prompt sequence:
```
/write-prompts
├─> Robustness card: reuse, or copy agent template + extend
├─> Fails card: reuse, or create from skeleton
├─> Findings card: create
└─> each implementation prompt: hang-safety line + runtime-check line

Prompt NN runs
├─> read Robustness card + Fails card "Never again" list
├─> per command: check list ──> chat-mode flow above
│   └─> failure ──> Fails card entry at once ──> fix root cause ──> continue
│       └─> same failure again in this prompt ──> stop + PROBLEMS.md entry (references FL-NN)
└─> content glitch ──> Findings card

Final checkpoint prompt of the prompts file | list over ~15 lines
└─> Fails "Never again" lines ──> Robustness card banned list

/cleanup (before deleting _agentwork/)
└─> recurring lines ──> generic shape ──> IPPS: agent ROBUSTNESS_CARD_TEMPLATE.md | downstream: workspace FAILS.md
```

Audit:
```
/verify ........ cards vs skeleton + CD rules; prompts vs PRMT-HS / PRMT-RB
/drift-detect .. CHECKS PD (runner used, no kill while progress, failures recorded)
/improve ....... CHECKS QI (expected runtimes measured, verdicts right, bans complete, promotion done)
/cleanup ....... .tmp_ scripts and runner artifacts removed
```

## 10. Data Structures

**Runner log** (`_agentwork/.tmp_[purpose]_log.txt`):
```
2026-01-15 10:00:00 START expected=60s pid=4321 script=.tmp_build_100000.ps1
2026-01-15 10:00:30 ALIVE elapsed=30s cpu=21.4s out=1830 err=0 procs=3
2026-01-15 10:00:42 DONE exit=0 elapsed=42.3s expected=60s
```
```
2026-01-15 10:05:00 START expected=30s pid=4388 script=.tmp_test_100500.ps1
2026-01-15 10:05:30 ALIVE elapsed=30s cpu=0.4s out=96 err=0 procs=2
2026-01-15 10:06:00 ALIVE elapsed=60s cpu=0.4s out=96 err=0 procs=2
2026-01-15 10:06:04 KILLED exit=124 elapsed=64.1s expected=30s reason=hang: output ends with Ok to proceed
```
```
2026-01-15 10:10:00 WARN processkit not found, fallback Kill($true) misses orphaned grandchildren
2026-01-15 10:10:00 LEFTOVER script=.tmp_test_100500.ps1 pids=5120,5148 kill=.tmp_kill_EXAMPLE.ps1
2026-01-15 10:10:00 START expected=30s pid=4402 script=.tmp_test_101000.ps1
```
```
2026-01-15 10:15:00 ERROR reason=script-not-found script=.tmp_check_101500.ps1
```

**Kill script** (`_agentwork/.tmp_kill_[TOPIC].ps1`, one line per running runner call):
```
Get-Process -Id 5120,5148 -ErrorAction SilentlyContinue | Where-Object { $_.StartTime -le [datetime]'2026-01-15 10:05:05.120' } | Stop-Process -Force  # runner=4388 script=.tmp_test_100500.ps1
```

**Prompt robustness lines** (one implementation prompt, Constraints; runtime-check line abbreviated, full text in the Section 2b template):
```
- Hang safety: commands per `agent-behavior.md` Terminal Hang Prevention (supervised runner); bans and expected runtimes per `_agentwork/__CARD_01-Robustness.md`.
- Runtime check: before each command state the expected seconds and check the "Never again" list in `_agentwork/__CARD_01-Fails.md`; while it runs read the `ALIVE` lines in the runner log and end it only on a hang verdict, never for its runtime; after it compare with `elapsed=`; [failure definition, record, no re-run of slow finished commands, stop on repeat]
```

**Fails card "Never again" line:**
```
- `npm test` without file filter in a watch-mode project -> `npm test -- --ci tests/unit/example.test.ts` (FL-01)
```

## 11. Logging Requirements

**Applicable logging types:**
- [x] Script-Level (SC) - `LOGGING-RULES-SCRIPT-LEVEL.md`: the runner log is read by the agent as the only completion signal

**Script-level logging (runner log):**
- **Audience**: the executing agent; secondarily `/drift-detect` and the user reviewing a failure
- **Goal**: know whether the command still works (liveness), whether it finished, how (exit code or kill on the agent's request), how long it took against its expected runtime, whether processes of a cancelled command survive, and whether the run was degraded
- **Key operations**: start, liveness every 30 s, normal end, kill on the stop file, leftover report, fallback mode, runner error before start
- Format per line: `YYYY-MM-DD HH:MM:SS` timestamp, keyword (`START`, `ALIVE`, `DONE`, `KILLED`, `ERROR`, `LEFTOVER`, `WARN`), `key=value` fields (`WARN`: free-text message; `reason=`: free text to the line end); exactly one end line (`DONE`, `KILLED`, or `ERROR`) per run (Section 10)

Child output is not reformatted: `_out.txt` and `_err.txt` contain the child's own streams.

## 12. Technical Constraints

- Windows with PowerShell 7; the runner itself is a PowerShell script
- processkit-py 1.5.0 is the tested supervisor version; other versions need a bench pass (AGENTTERMINAL-FR-17)
- Cascade terminal tool: max 4 concurrent terminals; terminals shared across concurrent conversations; completion reporting unreliable (Section 2)
- Cascade tool-call payload limit applies to writing cards and tmp scripts; owner is `devin-cascade.md` Tool-Call Payload Limit
- GRUC consumer mapping (GRUC-SP01): CHECKS are read only by audit workflows, never by the working agent during execution
- `.tmp_` and `_agentwork/` naming and lifecycle per AGNTFOLDERS-SP01
- Known limits of the target state:
  - Fallback without processkit passes 25/27 (fails HC-11 pipe-holding grandchild, HC-21 orphan)
  - A cancelled runner ends nothing by itself; leftover processes live until agent or human runs the kill script. Processes started after the last tree scan (scans at 1 to 5 s, then every 5 s) are not in the kill script
  - The hang verdict is a text rule followed by the agent; its thresholds (5 and 10 minutes) and its error rate are not tested live. A real hang without a telling output line costs those minutes
  - The kill script ends every running command of its topic, not one selected command
  - Bench and streaming results come from one run each; no repeat statistics
  - Live acceptance in a Cascade prompt sequence (deliberate hangs + completion miss, 0 human cancels) not yet run
  - A PowerShell child with very little total output can stay buffered until exit; larger output arrives in blocks (NFR-04 holds for 1 line per second or more)
  - Silent-by-design scripts that also use no CPU (waiting on a network call or another process) give no progress signal; the Robustness card must note such silent phases, else the agent may end them after 5 minutes
  - processkit-py is a young project; Process Governor is the tested alternative but fails runner cancellation (HC-27) [ASSUMED: maturity risk]
  - The upper limit of the Cascade first wait (`WaitMsBeforeAsync`) is unknown; the agent tool rule caps it at 60 s [ASSUMED]
  - Inline whitelisted commands run without supervisor; only the whitelist criteria limit their risk
  - Processes started outside the process tree (WMI/CIM `Win32_Process.Create`, scheduled tasks, services) are not in the Job Object and survive a kill; the hard ban on unbounded children is the only defense
  - The Job Object needs nested-job support (Windows 8 or later) and an outer job that permits nesting; under the Cascade terminal it worked in every runner call on 2026-11-11 [TESTED]
  - Scope is Windows hosts: the runner is a PowerShell script and relies on Job Objects; agents on Linux or macOS are out of scope; processkit portability not checked [ASSUMED]
  - IDE and conversation crashes are not prevented

## 13. Change Plan

Delta between the target state and the files as of 2026-11-11. Done items are listed so the plan stays complete.

**Status 2026-11-11 19:15** (AGENTTERMINAL-IP01): done CP-08 to CP-13, CP-17 to CP-23, CP-15 stage 1 (`.devin/` mirror). Open: CP-14 (processkit install, user), CP-15 downstream sync, CP-16 (live acceptance test, `_PROMPTS_99-HangAcceptance.md`).

**Status 2026-11-11 20:10** (cap removal, PRMTHANGFIX-FL-0001): done CP-24 to CP-28. Open: CP-14, CP-15 (`.devin/` mirror and downstream sync), CP-16 (the acceptance prompts must be adapted to the hang verdict first).

**Done:**
- **CP-24** `run-supervised.ps1`: deadline removed; `-Expected`, `ALIVE` lines, stop file, `KILLED` end line; kill script with `-Topic`, `LEFTOVER` line (FR-04, FR-21, FR-22)
- **CP-25** `rules/agent-behavior.md`, `rules/devin-cascade.md`: monitoring, hang verdict, runtime overrun without re-run, kill script use, polling without time limit (FR-06, FR-07, FR-21, FR-22)
- **CP-26** Skill, card skeleton and templates (`## Expected runtimes`), RULES, CHECKS, coding-conventions test documents, prompt-writing files, `write-prompts.md`, `cleanup.md`: every cap instruction replaced
- **CP-27** HANGBENCH: harness creates the stop file in hang cases and runs the kill script in the cancel case; contract tests TC-07, TC-09 to TC-12; run `runner5`
- **CP-28** This spec: FR-21, FR-22, DD-13, DD-14, IG-07; FR-04 to FR-09, FR-19, DD-06, DD-10 changed
- **CP-01** `rules/agent-behavior.md`: whitelist, runner call, completion from log, runtime check, failure target, hard bans
- **CP-02** `rules/devin-cascade.md`: non-blocking calls, polling on the runner log, shared terminals
- **CP-03** `rules/tools-and-skills.md`: processkit location and install command
- **CP-04** `skills/terminal-robustness/`: runner, skeleton with Robustness and Fails blocks, lean card templates, guides with bench results, RULES and CHECKS referencing runner and Fails card
- **CP-05** Prompt-writing files: two prompt lines, PRMT-RB-08, Findings card limited to content glitches, examples without procedure text
- **CP-06** `workflows/cleanup.md`: scan through the runner
- **CP-07** `_SPEC_TERMINAL_ROBUSTNESS_SKILL.md`: superseded items marked

**Open:**
- **CP-08** `run-supervised.ps1`: write an `ERROR` line when the script or interpreter is not found (FR-04)
- **CP-09** `rules/devin-cascade.md`: bounded polling limits (no `START` after 60 s, no end line 60 s after the cap, then runner-process check) (FR-06)
- **CP-10** `rules/agent-behavior.md`: end line includes `ERROR`; `[purpose]` with `HHmmss` suffix (FR-03, FR-05); cap = largest of card class cap, 3x expected, 30 s (FR-07); first `WARN` → tell user + one PROBLEMS.md entry (DD-03)
- **CP-11** `PROMPTS_RULES.md` PRMT-RB-07 / RB-08: PROBLEMS.md stop entry references the Fails entry ID (FR-13)
- **CP-12** `workflows/verify.md`: Prompts Files context names PRMT-HS and PRMT-RB categories; Required Skills names Fails card instances besides Robustness cards (FR-16)
- **CP-13** HANGBENCH: rerun after CP-08 (FR-17)
- **CP-14** Setup: install processkit-py 1.5.0 into the shared venv (FR-18)
- **CP-15** Deployment: mirror `PromptSystemV4.7/` to `.devin/`, then `/sync` downstream (FR-18)
- **CP-16** Live acceptance test in Cascade: short prompt sequence with deliberate hangs and one completion miss; pass = 0 human cancels, every failure in the Fails card, runtime check flags the slow command
- **CP-17** `skills/terminal-robustness/SKILL.md` Execute safely: `rg.exe` through the runner where the agent search tool cannot reach a folder (FR-20)
- **CP-18** `ROBUSTNESS_CARD_SKELETON.md` Fails block: add failure classes "runner error" and "command repeated after it failed once"; "Never again" writing rules (complete replacement, extend line on same root cause) (FR-08, FR-12)
- **CP-19** Fails card per working folder, created at the first failure, PROBLEMS.md branch removed for failures: `rules/agent-behavior.md` step 5, `SKILL.md` step 4, `ROBUSTNESS_CARD_SKELETON.md` block heading, `write-prompts.md` (reuse or create), `PROMPTS_ROBUSTNESS_GUIDES.md` card roles, TERMINAL_ROBUSTNESS_CHECKS PD-05 (FR-08, FR-12, DD-12)
- **CP-20** Promotion triggers: final checkpoint prompt template in `PROMPTS_TEMPLATE.md` and `write-prompts.md`; `/cleanup` step before card deletion; generic-shape rule for template promotion in `ROBUSTNESS_CARD_SKELETON.md` (FR-10, IG-06)
- **CP-21** Retry rule for slow legitimate work and secret-free entries: `ROBUSTNESS_CARD_SKELETON.md` Fails card rules (FR-08, FR-09)
- **CP-22** Move HANGBENCH from the private session folder into a versioned IPPS folder excluded from downstream sync; update the DevinCascade guide reference (FR-17)
- **CP-23** `run-supervised.ps1`: UTF-8 child output (FR-04)

## 14. Implementation Verification Checklist

- [ ] FR-01, NFR-02: text search over `PromptSystemV4.7/` for procedure phrases finds only owners, marked examples, history notes
- [ ] FR-02: whitelist criteria appear only in `agent-behavior.md`
- [ ] FR-03, IG-01: an unchanged project script runs through a tmp script and the runner
- [ ] FR-04, IG-02, NFR-03: HANGBENCH 27/27 through the shipped runner with processkit; fallback result recorded with failed case IDs
- [ ] FR-04: missing script and missing interpreter each produce an `ERROR` line
- [ ] FR-05, FR-06: agent tool rule states non-blocking call, bounded first wait, polling without time limit, runner-gone check
- [ ] FR-07: generic rule states the failure definition (KILLED, ERROR, exit code) and the runtime overrun (both thresholds, result used, no re-run)
- [ ] FR-21, DD-13, IG-07: runner has no deadline parameter; generic rule states the three hang-verdict conditions; no file tells the agent to end a command for its runtime
- [ ] FR-22, DD-14: runner contract tests cover kill script, `LEFTOVER`, and `-Topic`; generic rule names the kill script
- [ ] FR-08, FR-12, IG-03: Fails block in skeleton has all failure classes and the "Never again" field
- [ ] FR-09: generic rule and runtime-check line both require the "Never again" check before each command
- [ ] FR-10: skeleton and CHECKS QI items describe both promotion steps
- [ ] FR-11, IG-04: both agent card templates match the Robustness block of the skeleton and contain no generic rule
- [ ] FR-13: Findings card rules exclude terminal failures; PROBLEMS.md rules cover deferred problems and prompt stops only
- [ ] FR-14, IG-05: `PROMPTS_TEMPLATE.md`, example sequence, and `write-prompts.md` examples contain exactly the two lines per implementation prompt
- [ ] FR-15: `SKILL.md` dispatch keys on agent identity
- [ ] FR-16: `/verify`, `/drift-detect`, `/improve`, `/cleanup` reference the runner log or Fails card where listed
- [ ] FR-17: DevinCascade guide lists the latest bench result per mode with failed case IDs
- [ ] FR-18: processkit path in `tools-and-skills.md` equals the runner's default; `.devin/` mirror equals `PromptSystemV4.7/`
- [ ] NFR-01: generic rule section at most 15 lines, agent tool terminal section at most 10 lines
- [ ] NFR-04: streaming test shows lines in `_out.txt` before the child exits (Python and PowerShell)
- [ ] NFR-05: HANGBENCH input-wait cases end within about 3 s, before the stop file
- [ ] FR-19: `tools-and-skills.md` Long-Running Commands states user notice, no time limit, concurrency check, liveness check, survivor check, and points to the runner
- [ ] FR-20: `SKILL.md` names the `rg.exe` runner fallback; no shell search pipeline in any example outside BAD blocks
- [ ] DD-10, DD-11: no file proposes an idle timeout or a background process started through the runner
- [ ] FR-08, DD-12: no rule sends terminal failures to PROBLEMS.md; Fails card creation at first failure is stated in the generic rule and the skeleton
- [ ] FR-10: final checkpoint prompt template and `/cleanup` contain the promotion step
- [ ] IG-06: Fails card skeleton and promotion rule forbid secret values and project paths in template lines
- [ ] FR-17: HANGBENCH folder is versioned and excluded from downstream sync
- [ ] FR-01: runtime-check line in every prompt equals the `PROMPTS_ROBUSTNESS_GUIDES.md` Section 2b template; its thresholds equal the generic rule

## 15. Document History

**[2026-11-11 21:12]**
- Changed (reverse-update from rule compaction): section Long-Running Commands moved from `rules/agent-behavior.md` to `rules/tools-and-skills.md`, content unchanged (architecture diagram, ownership table, FR-19 checklist item). Reason: Cascade loads only about the first 12,000 bytes of an always-on rule file; `agent-behavior.md` was cut off before Terminal Hang Prevention

**[2026-11-11 20:10]**
- Changed (user correction, PRMTHANGFIX-FL-0001): the time cap is removed from the whole system. The runner has no deadline; the agent monitors liveness lines and ends a command only on a hang verdict (FR-21, DD-13, IG-07); a slow finished command is used and never re-run (FR-07, FR-09)
- Added: kill script per topic with leftover report for cancelled runners (FR-22, DD-14); runner log lines `ALIVE`, `KILLED`, `LEFTOVER`; stop file
- Changed: FR-04, FR-05, FR-06, FR-11, FR-14, FR-19, NFR-03, NFR-05, DD-02, DD-03, DD-06, DD-08, DD-10, IG-02, IG-03, Sections 8 to 12; Robustness card section "Time caps" renamed "Expected runtimes"
- Changed: bench result run `runner5` (27/27 with processkit, 25/27 fallback); CP-24 to CP-28

**[2026-11-11 19:15]**
- Changed: Change Plan status after AGENTTERMINAL-IP01 implementation; bench gate: runner 27/27, fallback 24/27, runner contract tests 10/10

**[2026-11-11 19:55]**
- Changed (reverse-update from AGENTTERMINAL-IP01 spec feedback): FR-10 `/cleanup` carries generic lines out of the folder (IPPS template, downstream `FAILS.md`) instead of promoting into the card it deletes; FR-04 runner exit code 2 for `ERROR`, UTF-8 child output; FR-03 letter on name collision; CP-23 added

**[2026-11-11 19:30]**
- Fixed (`/verify`): log examples use the `HHmmss` name suffix (FR-03); `ERROR` example follows the `key=value` format; runner error added to logging key operations
- Added: ownership rows for cap rule, Fails card rules and promotion, prompt lines (FR-01 completeness); reference chain for the runtime-check line
- Changed: Context bench summary names GNU `timeout`; acronyms GRUC and CIM written out; Prompt-Writing Files owns the promotion step

**[2026-11-11 19:20]**
- Changed (`/critique` → `/reconcile` → `/implement`): one Fails card per working folder for chat mode and prompt sequences, created at the first failure; PROBLEMS.md no longer receives terminal failures (FR-08, FR-12, DD-12)
- Changed: cap = largest of card class cap, 3x expected, 30 s (FR-07); one retry with raised cap for slow legitimate work (FR-09); `START` polling bound 15 s → 60 s with runner-process check (FR-06); `[purpose]` time suffix (FR-03)
- Added: promotion triggers and owners (FR-10, FR-14); secret-free cards and generic template lines (FR-08, IG-06, MUST-NOT-FORGET); declared runtime-check-line exception (FR-01); versioned bench location (FR-17)
- Added: known limits for processes outside the Job Object, nested-job requirement, Windows-only scope; measurable NFR-02 phrase list and NFR-04 threshold; DD-05 effect labeled [ASSUMED]
- Added: CP-19..CP-22 and checklist items

**[2026-11-11 19:05]**
- Added (`/improve` after comparison with PRMTHANGFIX-IN04): state diagnosis from runner files (Section 8); failure-map rows for continuation prompt, unbounded waits, stderr flood
- Added: FR-19 long-running commands, FR-20 file search without shell pipelines, DD-10 deadline only (no idle timeout), DD-11 no process outlives its runner call
- Added: failure class "command repeated after it failed once"; "Never again" writing rules (FR-12); sequence continues after a prompt stop (FR-09)
- Added: known limits processkit maturity, Cascade first-wait limit; CP-17, CP-18; checklist items for FR-19, FR-20, DD-10, DD-11
- Changed: DD-02 names GNU `timeout` and the Job Object reason; DD-11 HC-19 claim labeled [ASSUMED from timing] as in the source

**[2026-11-11 18:55]**
- Added: Change Plan (Section 13) and Implementation Verification Checklist (Section 14)
- Added: corner cases - artifact name collision (FR-03), runner `ERROR` end line (FR-04, FR-05), bounded polling (FR-06), exit code 124 collision and unsupervised inline commands (Section 12)
- Changed: FR-04 tree-kill guarantees scoped to processkit mode; DD-03 degraded mode recorded once in PROBLEMS.md (deferred problem, per FR-13); NFR-05 "at once" replaced by "within about 2 s"; IG-03 "exactly one failure record"
- Changed: acronyms written out (CD, PD, QI, PRMT-HS, PRMT-RB, HC)

**[2026-11-11 18:45]**
- Initial specification created from the implemented lean design (critique → reconcile → implement) and PRMTHANGFIX-IN04
