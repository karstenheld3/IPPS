---
description: Post-execution drift detection - build DoD, compare output, fix gaps
---

# ADP Workflow

Post-execution drift detection and correction. Runs AFTER a workflow or agent instruction completes. Builds a Definition-of-Done (DoD) from the original instruction, compares against actual output through drift lenses, persists gaps, and fills them.

**Goal**: All instruction-following gaps identified, fixable gaps closed, unfixable gaps logged

**Why**: Agents report "done" while skipping process steps and forgetting requirements. This workflow catches and closes those gaps after execution.

Usage:
- `/adp` - full audit across all drift categories
- `/adp [directive]` - audit with specific focus (e.g., `/adp that all SPEC sections have acceptance criteria`)
- `/adp log` - detect and log all deviations to DRIFTS.md (no gap filling)

**Scope Boundary**: This workflow fixes **instruction-following failures** (drift from what was asked). Use `/verify` for rule/convention compliance. Use `/critique` for logic flaws and hidden risks.

## Required Skills

- @skills:adp for drift lenses, context detection, DoD extraction rules, and DoD template

## MUST-NOT-FORGET

1. Post-execution only: runs AFTER a workflow or instruction completes. Never before or during.
2. Resume first: If `__ADP_[TOPIC].md` exists, skip to Step 4 (FILL). Do NOT regenerate.
3. Re-read the original instruction BEFORE auditing - never audit from memory.
4. Two scored lenses (Output Structure, Process Discipline) + one observational lens (Meta-Criteria).
5. MISSED vs FAIL: MISSED = cannot retroactively fix. FAIL = fixable now.
6. DoD is the contract: once persisted, authoritative. Only add items for newly discovered requirements.
7. Atomic gap closure: one gap at a time. Fix, verify, update `__ADP` and planning docs.

## Mandatory Re-read

**SESSION-MODE**: NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md

**PROJECT-MODE**: !NOTES.md or NOTES.md, FAILS.md

## Prerequisites

- A workflow or agent instruction has completed → proceed
- Work is still in progress → do NOT run this workflow

# CONTEXT-SPECIFIC

Context detection and DoD extraction rules are in `@skills:adp` `ADP_WORKFLOW.md`. Read sections "Context Detection", "Default Sources", and the matching context section.

## No Context Match

If no SPEC/IMPL/TASKS and no research output exist: use Generic context. Build DoD entirely from conversation and planning artifacts (default sources).

# EXECUTION

## Steps

```
Step 1: ANALYZE - Detect context, build DoD
Step 2: COMPARE - Assess output through drift lenses
Step 3: PERSIST - Write __ADP_[TOPIC].md
Step 4: FILL    - Close FAIL gaps in priority order
Step 5: FINALIZE - Update status, report
```

### Step 1: ANALYZE - Build DoD

1. Determine `[TOPIC]` from context:
   - User specifies topic explicitly: use that
   - Planning files exist (`__STRUT_[TOPIC].md`, `__TASKS_[TOPIC].md`): extract from filename
   - Fallback: derive from session folder name or conversation subject
2. Search for existing `__ADP_[TOPIC].md`
3. If found: read file, spot-check 2-3 PASS items for regression, skip to Step 4
4. If not found: read `ADP_WORKFLOW.md` context detection + extraction rules, build new DoD

### Step 2: COMPARE - Assess Output

For each DoD item, assess status per `ADP_WORKFLOW.md` section "Assessment Statuses". Note meta-criteria presence/absence (observational).

### Step 3: PERSIST - Write __ADP_[TOPIC].md

Create in working directory using template from `@skills:adp` `ADP_TEMPLATE.md`.

### Step 3b: LOG MODE - Append to DRIFTS.md

If invoked as `/adp log`: skip Steps 4-5. Instead:

1. Append all FAIL and MISSED items to `DRIFTS.md` in current working directory
2. Use format from `@skills:adp` `ADP_WORKFLOW.md` section "DRIFTS.md Format"
3. Do NOT fix anything. Do NOT create `__ADP_[TOPIC].md`.
4. Report: "Logged [count] deviations to DRIFTS.md"
5. End workflow.

### Step 4: FILL - Close Gaps

Process TODO items: HIGH first, then MEDIUM, then LOW.

For each TODO:

1. Read the referenced DoD item
2. Execute minimum change to close gap
3. Verify: does the item now PASS?
4. Update `__ADP_[TOPIC].md`: FAIL → PASS, check off TODO
5. Next TODO

If a gap cannot be closed: mark BLOCKED with reason, move to next.

Session boundary: if context exhausted, update `__ADP` with current state. File persists for resume.

### Step 5: FINALIZE

When all TODOs are done or BLOCKED:

1. Update Status: all PASS/MISSED/N/A → `COMPLETE`, any BLOCKED → `BLOCKED`
2. Report summary:

```
## ADP Summary

**Topic**: [TOPIC]
**Context**: [Code Implementation | Deep Research | Generic]
**Directive**: [directive or "full audit"]
**Status**: [COMPLETE | BLOCKED]

**Scored Results**:
- Category 1 (Output Structure): [pass_count]/[total] PASS
- Category 2 (Process Discipline): [pass_count]/[total] PASS, [missed_count] MISSED

**Meta-Criteria Observations**:
- Present: [list]
- Absent: [list]

**Gaps Fixed**: [count]
**Gaps Blocked**: [count] (with reasons)
```

## Stuck Detection

If 3 consecutive TODO items cannot be closed:
1. Document in PROBLEMS.md
2. Mark remaining items BLOCKED
3. Proceed to FINALIZE

# FINALIZATION

## Verification

- [ ] All FAIL items resolved (PASS) or BLOCKED with reason
- [ ] `__ADP_[TOPIC].md` updated with final status
- [ ] No items left in FAIL status

## Output

- `__ADP_[TOPIC].md` in working directory (session folder or topic subfolder)
- ADP Summary reported to user

## Trigger

- `/adp` - after any `/build`, `/implement`, `/solve` completion
- `/adp` - after `/deep-research` completion
- `/adp [directive]` - when specific aspect needs verification
- `/adp log` - after any task to accumulate drift data for heuristic analysis
- As spot-check during long autonomous sessions (`/go`)
- After `/verify` passes but user suspects shallow compliance
