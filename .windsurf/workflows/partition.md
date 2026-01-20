---
description: Partition plans into discrete tasks
---

# Partition Workflow

## Required Skills

- @write-documents for document structure

## Rules

- **Output to PROGRESS.md only** - Never create a separate TASKS document
- To create a TASKS_[TOPIC].md document, use /write-tasks-plan instead

## Step 1: Determine Strategy

If STRATEGY parameter provided, use it. Otherwise:
1. Check NOTES.md for partitioning hints
2. If BUILD + technical work → PARTITION-DEPENDENCY
3. If BUILD + user-facing → PARTITION-SLICE
4. If high uncertainty noted → PARTITION-RISK
5. Default: PARTITION-DEFAULT (0.5h HWT chunks)

## Step 2: Gather Input Documents

Read all relevant documents in order:
1. SPEC (requirements, FR, DD, AC)
2. IMPL (steps, edge cases)
3. TEST (test cases, test strategy, verification approach)

If TEST plan exists:
- Extract TC (Test Case) IDs and their target IS/FR references
- Note test priority levels
- Identify integration test boundaries

If no TEST plan exists:
- Proceed with IMPL-only partitioning
- Flag in output: "No TEST plan - tasks lack test coverage mapping"

## Step 3: Apply Strategy

### PARTITION-DEFAULT

- Estimate HWT per item
- Chunk into max 0.5h HWT tasks
- Preserve document order

### PARTITION-DEPENDENCY

- Build component dependency graph
- Topological sort (leaves first)
- Group independent items as parallel

### PARTITION-SLICE

- Map each AC/FR to required components
- Create one task per vertical slice
- Order by value or risk

### PARTITION-RISK

- Rate items by uncertainty
- Order unknowns before knowns
- Front-load integration points

## Step 4: Output to PROGRESS.md

Update PROGRESS.md "To Do" section with partitioned tasks:

```markdown
## To Do

### [Phase] Phase

- [ ] **[TOPIC]-TK-001** - Task description (0.5h HWT) [TC-01, TC-02]
- [ ] **[TOPIC]-TK-002** - Task description (0.25h HWT) [TC-03]
...
```

Include TC references when TEST plan exists. Omit brackets if no test coverage.

## Task Properties

Each task must be:
- **Atomic** - Implementable in one edit session between commits
- **Testable** - Has defined test cases or can be verified with temp script
- **Scoped** - Does one thing only
- **Estimated** - Has HWT estimate (target: max 0.5h HWT)
