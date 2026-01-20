---
description: Sequence of [RECAP] + [CONTINUE] until goal reached
---

# Go Workflow

Implements [GO] verb - autonomous execution loop using /recap and /continue.

## Usage

```
/go
```

## Pre-Flight Check

1. Do we have enough context? If unclear, [CONSULT] with [ACTOR].
2. Do we have stop or acceptance criteria?
3. Re-read conversation, make internal MUST-NOT-FORGET list.

## Execution Loop

```
WHILE goal not reached:
    /recap   # Assess current state
    /continue # Execute next item
    
    IF blocker:
        [CONSULT] with [ACTOR]
        WAIT for guidance
```

## Step 1: Recap

Run `/recap` to determine:
- Last completed action
- Current state
- Any blockers

## Step 2: Continue

Run `/continue` to:
- Execute next task from plan
- Update progress
- Check for completion

## Step 3: Loop or Stop

- **Goal reached?** Stop, output summary
- **Blocker?** Log to PROBLEMS.md, [CONSULT]
- **More work?** Return to Step 1

## Stopping Conditions

- All tasks complete
- Blocker requires [ACTOR] input
- [ACTOR] interruption
- Retry limit exceeded (5 attempts for MEDIUM/HIGH complexity)