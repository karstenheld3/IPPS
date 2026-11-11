---
name: terminal-robustness
description: Prevent hanging terminal commands in chat mode and prompt sequences - mechanisms, safe patterns, robustness cards, agent variants (ClaudeCode minimum, DevinCascade full findings)
---

# Terminal Robustness Skill

**Goal**: Prevent terminal commands from hanging the session - in regular chat mode and in headless prompt sequences

## Overview

Agents issue commands that hang indefinitely: pipes that never EOF, stderr that throttles, merge operators that crash the shell, background grandchildren inheriting std handles, input waits, and terminal tools that miss the end of a finished command. This skill carries the confirmed mechanisms, the supervised runner `run-supervised.ps1`, and the card templates (Robustness, Fails) that make the protection durable per project.

Baseline rules are NOT repeated here: inline whitelist, runner call, monitoring, hang verdict, runtime check, hard bans live in `agent-behavior.md` Terminal Hang Prevention; agent tool mechanics (blocking mode, polling) live in the agent rule file. This skill adds only mechanisms, evidence, the runner, and templates.

## MUST-NOT-FORGET

- Read `TERMINAL_ROBUSTNESS_GUIDES.md` BEFORE running risky commands (anything spawning processes, building, testing, or writing >4KB stderr)
- Commands follow `agent-behavior.md` Terminal Hang Prevention (supervised runner, completion from the runner log)
- The goal is hang prevention, not runtime limits: a command that shows progress is never ended; only a hang verdict ends a command
- Determine your agent and load the matching variant subfolder (`ClaudeCode/` or `DevinCascade/`)
- If `_agentwork/__CARD_*-Robustness.md` exists, load it before running commands and follow its banned list and expected runtimes; if `_agentwork/__CARD_*-Fails.md` exists, check its "Never again" list before each command
- Never create a card from scratch - copy the agent's `ROBUSTNESS_CARD_TEMPLATE.md` or the Fails block of `ROBUSTNESS_CARD_SKELETON.md` and extend it
- CHECKS files are for post-execution audit only (`/drift-detect`, `/improve`) - never read them to game compliance

## Agent Dispatch

Determine the active agent, then load the variant files in addition to the shared files:

1. **DevinCascade** (you are Cascade; rule `devin-cascade.md`) → load `DevinCascade/TERMINAL_ROBUSTNESS_GUIDES.md` (full empirical findings) and `DevinCascade/ROBUSTNESS_CARD_TEMPLATE.md`
2. **ClaudeCode** (`.claude/` agent folder) → load `ClaudeCode/TERMINAL_ROBUSTNESS_GUIDES.md` (minimum: generic patterns only) and `ClaudeCode/ROBUSTNESS_CARD_TEMPLATE.md`
3. **Devin agent** (you are Devin, not Cascade; rule `devin-devin.md`) → no tested variant; load the `ClaudeCode/` minimum files and fill the card section `## Agent tool limits` from `devin-devin.md`

Dispatch keys on agent identity (system prompt), not on the agent folder: Cascade and the Devin agent both use `.devin/`. Shared files load regardless of agent.

## Core Procedures

### 1. Classify command risk (before running)

- Interactive risk: command may wait on stdin, a key, a pager, or a confirmation prompt
- Volume risk: command may write >4KB to stderr (package managers, compilers, test runners)
- Child risk: command may spawn background processes inheriting std handles (dev servers, watchers, daemons)
- Known-safe: reads, quick git operations, small file writes

### 2. Load protection

- Project robustness card exists → follow its banned list, expected runtimes, and always rules
- No card, risky commands expected → copy the agent's `ROBUSTNESS_CARD_TEMPLATE.md` to `_agentwork/__CARD_[TOPIC]-Robustness.md` of the current working folder, extend banned list and expected runtimes, then follow it

### 3. Execute safely

- Prefer agent tools (grep_search, read_file, find_by_name) over shell commands for file operations; where `grep_search` cannot reach a folder or returns nothing for text that exists, run `rg.exe` inside a tmp script through the runner, never an inline `Select-String` or `Get-ChildItem` pipeline
- Non-whitelisted commands run through `run-supervised.ps1` (call line in `agent-behavior.md` Terminal Hang Prevention); the runner contains the whole process tree, gives empty stdin, and writes the log with `ALIVE` liveness lines. It has no deadline: it kills the tree only when the agent creates the stop file after a hang verdict. While commands run it keeps the kill script `_agentwork/.tmp_kill_[TOPIC].ps1` (one line per running command); after a cancelled runner that script ends the leftover processes

### 4. Record failures

- Every failure (`KILLED` after a hang verdict, `ERROR`, unexpected exit, completion miss) and every runtime overrun goes into the Fails card of the working folder at once, with a "Never again" line; no card yet -> create it from the Fails block of `ROBUSTNESS_CARD_SKELETON.md`
- Promotion and carry-out at `/cleanup`: Fails card rules in `ROBUSTNESS_CARD_SKELETON.md`

## References

- `TERMINAL_ROBUSTNESS_GUIDES.md` - shared mechanisms, safe patterns, card lifecycle (read before risky work)
- `TERMINAL_ROBUSTNESS_RULES.md` - HG/EX/CD output standards for cards and command patterns (consumed by `/verify`)
- `TERMINAL_ROBUSTNESS_CHECKS.md` - process discipline (PD) and quality improvement (QI) audits (consumed by `/drift-detect`, `/improve`)
- `run-supervised.ps1` - supervised runner: processkit Job Object container, empty stdin, live UTF-8 output files, log with `START` / `ALIVE` (CPU time, output size every 30 s) / `DONE` / `KILLED` / `ERROR` and `elapsed=`; no deadline, whole-tree kill on the stop file; kill script `.tmp_kill_[TOPIC].ps1` (`-Topic`) with the living process IDs per running command, `LEFTOVER` log line after a cancelled runner (fallback without processkit: `Kill($true)`, logged as WARN)
- `ROBUSTNESS_CARD_SKELETON.md` - canonical structure of the Robustness card and the Fails card (`/verify` target for card instances)
- `ClaudeCode/TERMINAL_ROBUSTNESS_GUIDES.md` - minimum variant guide
- `ClaudeCode/ROBUSTNESS_CARD_TEMPLATE.md` - minimum re-usable card (copy + extend)
- `DevinCascade/TERMINAL_ROBUSTNESS_GUIDES.md` - full-findings variant guide
- `DevinCascade/ROBUSTNESS_CARD_TEMPLATE.md` - full re-usable card (copy + extend)
