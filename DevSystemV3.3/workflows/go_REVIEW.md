# Devil's Advocate Review: go.md

**Reviewed**: `DevSystemV3.3/workflows/go.md`
**Date**: 2026-03-03
**Profile**: Senior engineer hunting flawed assumptions and logic errors

## MUST-NOT-FORGET (from FAILS.md)

- `GLOB-FL-004`: Gate checks require evidence - cannot claim completion without deliverables
- `MNF-FL-001`: MNF items must match ACTUAL workflow instructions
- Agent self-discipline fails without hard enforcement mechanisms

## Research Findings

**Industry patterns consulted:**
- AI SDK: Default stop at 20 steps; explicit `stopWhen` conditions
- LangGraph: Error classification (retry vs LLM-recoverable vs human-escalate)
- Production agents: Checkpoint-based recovery, attempts counter critical

**Key insight from research**: "Without an attempts counter, you get infinite loops. The LLM becomes the error handler, but must be bounded."

## Devil's Advocate Task List

1. Analyze termination conditions - are they enforceable?
2. Check blocker handling logic - is it complete?
3. Evaluate retry limits - are they actually enforced?
4. Examine self-verification claims - can agent cheat?
5. Review step ordering - does flow make sense?
6. Check for missing failure modes

---

## Findings

### [HIGH] `GO-RV-001` No Hard Step Limit - Infinite Loop Risk

**Location**: Step 4: Execution Loop

**Problem**: The workflow says "WHILE goal not reached" but has no maximum iteration counter. Stopping conditions mention "Retry limit exceeded (5 attempts)" but this is not enforced in the loop pseudocode.

**Flawed assumption**: Agent will honestly assess when it's stuck after 5 attempts.

**Evidence from FAILS.md**: `GLOB-FL-004` shows agent bypassed gates by self-reporting completion without evidence. Same self-discipline failure will occur with retry counting.

**Industry pattern**: AI SDK defaults to `stepCountIs(20)` - hard stop after 20 steps regardless of completion status.

**Risk**: Token burn, API costs, user frustration from runaway agent.

**Recommendation**: Add explicit `max_iterations = 20` counter that HARD STOPS the loop regardless of goal status. Not a soft suggestion - a mandatory termination.

---

### [HIGH] `GO-RV-002` Blocker Handling Creates Unbounded Recursion

**Location**: Step 4, IF blocker section

**Problem**: When blocker detected, workflow triggers:
```
/write-info -> /critique -> /reconcile -> /write-task-plan -> VCRIV -> /write-test-plan -> VCRIV
```

This is 7+ nested workflow invocations. Each of those workflows could also hit blockers, creating recursive blocker handling with no depth limit.

**Flawed assumption**: Nested workflows will succeed and not create their own blockers.

**Risk**: Cascading workflow explosion. Agent spends hours in blocker-handling workflows instead of asking user.

**Recommendation**: 
1. Add `blocker_depth` counter - max 1 level of blocker handling
2. If blocker handling itself fails, IMMEDIATE user escalation
3. Consider simpler blocker handling: Log + Ask User (not 7-workflow chain)

---

### [HIGH] `GO-RV-003` No Checkpointing - Progress Lost on Interruption

**Location**: Entire workflow

**Problem**: If user interrupts or session crashes mid-execution, there's no mechanism to resume from last completed step. The workflow mentions reading PROGRESS.md but doesn't mandate writing progress after each step.

**Industry pattern**: LangGraph uses checkpoint-based recovery with state saved at every node boundary.

**Risk**: Agent processes 10 of 15 tasks, crashes, restarts from zero.

**Recommendation**: Add explicit "Update PROGRESS.md" after each `/continue` execution, marking completed steps with timestamps.

---

### [MEDIUM] `GO-RV-004` Step 2 (Pre-Flight Check) Comes AFTER Step 1 (Recap)

**Location**: Steps 1-2

**Problem**: Step 1 runs `/recap` to assess state. Step 2 does Pre-Flight Check asking "Do we have enough context?" This is backwards - you should check if you have context BEFORE assessing state.

**Flawed logic**: Can't accurately recap without first ensuring you have the right context loaded.

**Recommendation**: Swap Steps 1 and 2, or merge Pre-Flight into Step 0.

---

### [MEDIUM] `GO-RV-005` Duplicate Step Numbering

**Location**: Step 2, items 3 and 3

**Problem**: 
```
3. Re-read conversation, make internal MUST-NOT-FORGET list.
3. Research and list all scripts and skills...
```

Two items numbered "3". This is a typo but indicates hasty editing without verification.

**Risk**: Instructions may be skipped or misinterpreted.

**Recommendation**: Fix numbering to 3, 4.

---

### [MEDIUM] `GO-RV-006` VCRIV Workflow Referenced But Not Defined

**Location**: Step 4, blocker handling

**Problem**: Workflow references "run VCRIV workflow" but VCRIV is not a workflow file - it's an acronym from ID-REGISTRY.md meaning `/verify` -> `/critique` -> `/reconcile` -> `/implement` -> `/verify`.

**Flawed assumption**: Agent knows VCRIV expands to 5 workflow calls.

**Risk**: Agent may fail to execute VCRIV correctly, or skip it entirely.

**Recommendation**: Either:
1. Create `/vcriv` workflow, or
2. Expand inline: "Run: /verify -> /critique -> /reconcile -> /implement -> /verify"

---

### [MEDIUM] `GO-RV-007` Typo in Blocker Section

**Location**: Step 4

**Problem**: "will tat address the blocker" - should be "will that address".

**Risk**: Minor, but indicates lack of proofreading.

---

### [LOW] `GO-RV-008` `.tmp_IMPL_[BLOCKER].md` Referenced But Never Created

**Location**: Step 4, blocker handling

**Problem**: Line says `run VCRIV workflow on .tmp_IMPL_[BLOCKER].md` but the creation step creates `.tmp_TASK_[BLOCKER].md`, not `.tmp_IMPL_[BLOCKER].md`.

**Risk**: VCRIV runs on non-existent file.

**Recommendation**: Fix reference to `.tmp_TASK_[BLOCKER].md` or add step to create IMPL file.

---

### [LOW] `GO-RV-009` Principle Statement Has Typo

**Location**: Line 10

**Problem**: "All reqirements must be implemented" - should be "requirements".

---

## Summary

| Severity | Count | Key Issues |
|----------|-------|------------|
| HIGH | 3 | No hard step limit, unbounded blocker recursion, no checkpointing |
| MEDIUM | 4 | Step ordering, duplicate numbering, VCRIV undefined, typos |
| LOW | 2 | File reference mismatch, spelling |

## Recommendations Priority

1. **Add hard iteration limit** (e.g., 20 steps max) - CRITICAL
2. **Simplify blocker handling** - reduce from 7 workflows to: Log + Analyze + Ask User
3. **Add progress checkpointing** - write to PROGRESS.md after each step
4. **Fix step ordering** - Pre-Flight before Recap
5. **Define or expand VCRIV** - make executable
6. **Fix typos and numbering** - quality signal

## MNF Verification

- [x] Checked against FAILS.md patterns
- [x] Research findings incorporated
- [x] All findings have specific line/location references
- [x] Recommendations are actionable
