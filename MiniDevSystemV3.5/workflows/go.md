---
description: Autonomous loop until goal reached
---

# Go Workflow

Autonomous `/recap` + `/continue` loop.

## Required Reading

- `rules/devsystem-core.md` - Workflow Reference

## MUST-NOT-FORGET

- Check if goal already reached (Step 1) before any work
- Log blockers to PROBLEMS.md immediately
- Run `/verify` before declaring goal reached
- Never sacrifice requirements - implement 100%
- No shortcuts, no lazy programming

## Step 1: Completion Check

1. Read STRUT plan (PROGRESS.md or session document)
2. Run `/verify`: All final-phase Deliverables checked? Final Transition → `[END]`?

If complete: Output "Goal already reached. No further work needed." Stop. Do not re-verify on subsequent `/go` calls.

If not complete: Proceed to Step 2.

## Step 2: Recap

Run `/recap` - determine last action, current state, blockers.

## Step 3: Pre-Flight Check

1. Gather more context if unclear
2. Verify stop/acceptance criteria exist
3. Make internal MNF list from conversation
4. List all scripts and skills needed

## Step 4: Execute

Run `/continue` - execute next task, update progress, check completion.

## Step 5: Loop

```
iteration_count = 0
WHILE goal not reached AND iteration_count < 5:
    iteration_count += 1
    /recap
    /continue
    
    IF iteration_count >= 5:
        Ask user: "Reached 5 iterations. Continue?"
    
    IF blocker:
        Log to PROBLEMS.md with [BLOCKER] id
        /write-info `.tmp_INFO_[BLOCKER].md` (root cause analysis)
        /critique -> /reconcile -> /write-tasks-plan `.tmp_TASK_[BLOCKER].md`
        /verify -> /implement -> /verify
```

## Stopping Conditions

- All tasks complete (final Transition = `[END]` checked)
- Blocker requires user input
- User interruption
- Retry limit exceeded (5 attempts for MEDIUM/HIGH complexity)

## Idempotent Behavior

Multiple `/go` on completed work: Output "Goal already reached", no re-verification, no action. Prevents wasted tokens, misinterpreting queued `/go`, overengineering.