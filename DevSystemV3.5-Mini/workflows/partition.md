---
description: Partition plans into discrete tasks
auto_execution_mode: 1
---

# Partition Workflow

Split implementation plans into discrete, testable tasks.

## Required Skills

- @write-documents for document structure

## Rules

- Output to PROGRESS.md only - never create separate TASKS document
- For TASKS_[TOPIC].md, use `/write-tasks-plan` instead

## Step 1: Determine Strategy

If STRATEGY parameter provided, use it. Otherwise:
1. Check NOTES.md for hints
2. BUILD + technical → PARTITION-DEPENDENCY
3. BUILD + user-facing → PARTITION-SLICE
4. High uncertainty → PARTITION-RISK
5. Default: PARTITION-DEFAULT (0.5 HHW chunks)

## Step 2: Gather Input

Read in order: SPEC (FR, DD) → IMPL (steps, edge cases) → TEST (test cases)

## Step 3: Apply Strategy

DEFAULT - Estimate HHW per item, chunk into max 0.5 HHW, preserve document order

DEPENDENCY - Build dependency graph, topological sort (leaves first), group independent as parallel

SLICE - Map each AC/FR to components, one task per vertical slice, order by value/risk

RISK - Rate by uncertainty, unknowns before knowns, front-load integration points

## Step 4: Output to PROGRESS.md

Update "To Do" section:

```markdown
## To Do

### [Phase] Phase

- [ ] [TOPIC]-TK-001 - Task description (0.5 HHW)
- [ ] [TOPIC]-TK-002 - Task description (0.25 HHW)
```

## Task Properties

Each task must be:
- Atomic - One edit session between commits
- Testable - Defined test cases or temp script verification
- Scoped - Does one thing only
- Estimated - HHW estimate (max 0.5 HHW)