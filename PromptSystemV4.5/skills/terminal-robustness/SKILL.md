---
name: terminal-robustness
description: Prevent hanging terminal commands in chat mode and prompt sequences - mechanisms, safe patterns, robustness cards, agent variants (ClaudeCode minimum, DevinCascade full findings)
---

# Terminal Robustness Skill

**Goal**: Prevent terminal commands from hanging the session - in regular chat mode and in headless prompt sequences

## Overview

Agents issue commands that hang indefinitely: pipes that never EOF, stderr that throttles, merge operators that crash the shell, background grandchildren inheriting std handles. This skill carries the confirmed mechanisms, the safe command patterns, and the robustness card system that makes the protection durable per project.

## MUST-NOT-FORGET

- Read `TERMINAL_ROBUSTNESS_GUIDES.md` BEFORE running risky commands (anything spawning processes, building, testing, or writing >4KB stderr)
- Three hard bans always apply: no `2>&1` on stderr-heavy commands, no unbounded background children, no stdin/pager waits
- Determine your agent and load the matching variant subfolder (`ClaudeCode/` or `DevinCascade/`)
- If the project has a `__CARD_*-Robustness.md`, load it before running commands and follow its banned list and caps
- Never create a robustness card from scratch - copy the agent's `ROBUSTNESS_CARD_TEMPLATE.md` and extend it
- CHECKS files are for post-execution audit only (`/drift-detect`, `/improve`) - never read them to game compliance

## Agent Dispatch

Determine the active agent, then load the variant files in addition to the shared files:

1. **DevinCascade** (`.devin/` agent folder, Windsurf/Devin IDE terminal tool) → load `DevinCascade/TERMINAL_ROBUSTNESS_GUIDES.md` (full empirical findings) and `DevinCascade/ROBUSTNESS_CARD_TEMPLATE.md`
2. **ClaudeCode** (`.claude/` agent folder) → load `ClaudeCode/TERMINAL_ROBUSTNESS_GUIDES.md` (minimum: generic patterns only) and `ClaudeCode/ROBUSTNESS_CARD_TEMPLATE.md`

Dispatch keys on the agent folder in use or explicit user context. Shared files load regardless of agent.

## Core Procedures

### 1. Classify command risk (before running)

- Interactive risk: command may wait on stdin, a key, a pager, or a confirmation prompt
- Volume risk: command may write >4KB to stderr (package managers, compilers, test runners)
- Child risk: command may spawn background processes inheriting std handles (dev servers, watchers, daemons)
- Known-safe: reads, quick git operations, file writes under the cap

### 2. Load protection

- Project robustness card exists → follow its banned list, caps, and always rules
- No card, risky commands expected → copy the agent's `ROBUSTNESS_CARD_TEMPLATE.md` to the project root as `__CARD_[TOPIC]-Robustness.md`, extend banned list and caps, then follow it

### 3. Execute safely

- Prefer agent tools (grep_search, read_file, find_by_name) over shell commands for file operations
- Redirect verbose output to a `.tmp_` file and read it with `read_file` - never merge stderr with `2>&1`
- Run hang-risky commands non-blocking with a time cap; poll status
- On cap: kill the process tree, record command and cap in PROBLEMS.md, continue

### 4. Record findings

- Hangs, near-hangs, and unexpected command behavior go into the project card's Findings Feed and session PROBLEMS.md
- New banned commands discovered during execution are added to the card, not just remembered

## References

- `TERMINAL_ROBUSTNESS_GUIDES.md` - shared mechanisms, safe patterns, card lifecycle (read before risky work)
- `TERMINAL_ROBUSTNESS_RULES.md` - HG/EX/CD output standards for cards and command patterns (consumed by `/verify`)
- `TERMINAL_ROBUSTNESS_CHECKS.md` - process discipline (PD) and quality improvement (QI) audits (consumed by `/drift-detect`, `/improve`)
- `ROBUSTNESS_CARD_SKELETON.md` - canonical card structure (`/verify` target for card instances)
- `ClaudeCode/TERMINAL_ROBUSTNESS_GUIDES.md` - minimum variant guide
- `ClaudeCode/ROBUSTNESS_CARD_TEMPLATE.md` - minimum re-usable card (copy + extend)
- `DevinCascade/TERMINAL_ROBUSTNESS_GUIDES.md` - full-findings variant guide
- `DevinCascade/ROBUSTNESS_CARD_TEMPLATE.md` - full re-usable card (copy + extend)
