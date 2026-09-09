---
description: Record a failure in FAILS.md, either from user input or by analyzing context
auto_execution_mode: 1
---

# Fail Workflow

Record failures to prevent repetition.

## Required Skills

- @write-documents for FAILS_TEMPLATE.md structure

## MUST-NOT-FORGET

- Suggest `/learn` after problem is resolved
- Session entries sync to workspace on `/session-finalize`

## Trigger

- `/fail [description]` - [ACTOR] reports failure
- `/fail` - Agent runs discovery analysis

## Step 1: Check for Explicit Input

If description provided → skip to Step 3.
If no description → Step 2.

## Step 2: Analyze Context (Discovery Mode)

Search in order:
1. Recent conversation - error messages, "doesn't work", "fails", "broken", corrections
2. Test status - run suite, note failing tests
3. Code state - git status, recent TODO/FIXME, syntax/lint errors
4. Logs - application, build, console errors
5. Documents - PROBLEMS.md unresolved, NOTES.md blocked, PROGRESS.md stuck

If nothing found: report "No failures detected in current context" and exit.

## Step 3: Classify Severity

- [CRITICAL] - Will definitely cause production failure
- [HIGH] - Likely failure under normal conditions
- [MEDIUM] - Possible failure under specific conditions
- [LOW] - Minor, unlikely to cause failure

## Step 4: Collect Evidence

- When: Current timestamp
- Where: File/function/line or document section
- What: Exact problem description
- Evidence: Link, test output, or example proving the issue

## Step 5: Re-read Failed Workflow/Rules

CRITICAL: Before root cause analysis, re-read what SHOULD have happened:

1. Workflow failure → re-read workflow file completely, note MNF/rules/constraints/scripts, follow references to other docs
2. Rule violation → re-read relevant rule files, note specific violated requirements
3. Configuration issue → re-read NOTES.md, !NOTES.md, referenced config sections

Compare instructions vs actual execution:
- What did workflow/rules say to do?
- What config values applied?
- What did I actually do?
- Where is the gap?

Produces "Workflow re-read findings" for FAILS entry.

## Step 6: Analyze Root Cause

Compare instructions to execution:
- What was specified vs what was executed?
- Why the gap? (rushed, assumed, invented, ignored)
- Cite line numbers when possible

## Step 7: Suggest Fix

Brief, actionable recommendation for resolution.

## Step 8: Create FAILS Entry

1. Determine location:
   - SESSION-MODE → `[SESSION_FOLDER]/FAILS.md` (create if needed)
   - PROJECT-MODE → `[WORKSPACE_FOLDER]/FAILS.md` or `[PROJECT_FOLDER]/FAILS.md`

2. Generate ID: `[TOPIC]-FL-[NNN]`
3. Add entry at top using FAILS_TEMPLATE.md structure
4. Include code example if applicable (before/after)

## Step 9: Report

Confirm to [ACTOR]:
- Created `[TOPIC]-FL-NNN` in FAILS.md
- Brief summary of what was recorded
- Suggest `/learn` for deeper analysis

## Quality Gate

- [ ] Failed workflow/rules re-read (Step 5 completed)
- [ ] "Workflow re-read findings" included in entry
- [ ] Severity correctly classified
- [ ] Evidence is concrete (not vague)
- [ ] Location is specific (file:line when applicable)
- [ ] Root cause compares instructions vs execution
- [ ] Suggested fix is actionable