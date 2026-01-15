# Devil's Advocate Review: EDIRD Phase Model v2

**Reviewed**: 2026-01-15 19:35
**Document**: `_SPEC_EDIRD_PHASE_MODEL_2.md [EDIRD-SP04]`
**Focus**: Flawed assumptions, logic errors, hidden risks

## MUST-NOT-FORGET (Review Constraints)

- Goal is "deterministic next-action logic for autonomous agent operation"
- Agent should ALWAYS know what to do next
- Gates determine phase transitions
- Two workflow types: BUILD (code) and SOLVE (knowledge/decisions)

## Critical Issues

### ❌ `EDIRD-RV-01` Determinism Claim is Incomplete

**Where**: Section 4 (Concept), Section 9 (Next Action Logic)

**Claim**: `next_action = f(workflow_type, current_phase, last_verb_outcome, gate_status)`

**Problem**: The function is not fully defined:
- What if **multiple gate items** are unchecked? Which verb executes first?
- What if **one verb addresses multiple** unchecked items?
- The **mapping from unchecked gate item → specific verb** is never defined

**Evidence**: Gate EXPLORE→DESIGN has 5 items. If items 2 and 4 are unchecked, which verb runs? Spec says "execute verb that addresses unchecked item" but never defines which verb addresses which item.

**Impact**: Agent may make arbitrary choices, breaking determinism guarantee.

**Suggested fix**: Add explicit gate-item-to-verb mapping table for each gate.

### ❌ `EDIRD-RV-02` Infinite Loop Risk in Gate Evaluation

**Where**: Section 7 (Phase Gates), Section 9 (Next Action Logic)

**Claim**: "If any unchecked → remain in [EXPLORE], execute next verb"

**Problem**: No termination condition if progress stalls:
- What if verbs don't address the unchecked items?
- What if a gate item is impossible to satisfy?
- No maximum iteration count defined

**Evidence**: Pseudocode shows `EXECUTE current_verb` in a loop but no exit condition for stuck states.

**Impact**: Agent could loop forever trying to satisfy an unsatisfiable gate.

**Suggested fix**: Add maximum iteration count per phase. After N attempts, [CONSULT] with [ACTOR] or escalate.

### ❌ `EDIRD-RV-03` No Timeout/Escalation for Stuck Verb Loops

**Where**: Section 9 (Verb Outcome Transitions)

**Problem**: Several verb handlers create potential infinite loops:
- `[VERIFY]-FAIL → [FIX] → [VERIFY]` (loop until OK)
- `[TEST]-FAIL → [FIX] → [TEST]` (loop until OK)

**What if**: The fix doesn't work? Or the test is flaky? Or the issue is unfixable?

**Impact**: Agent loops forever without escalating to [ACTOR].

**Suggested fix**: Add loop counter. After 3 [FIX] attempts, [CONSULT] with [ACTOR].

## High Priority Issues

### ⚠️ `EDIRD-RV-04` HOTFIX/BUGFIX Category Confusion

**Where**: Section 3 (Domain Objects), Section 5 (Workflow Types), Section 10 (SOLVE HOTFIX Flow)

**Problem**: HOTFIX and BUGFIX are categorized as SOLVE problem types, but:
- SOLVE is defined as "Primary output is knowledge, decisions, or documents"
- HOTFIX flow includes `[FIX] apply fix`, `[DEPLOY] immediately` - this produces **working code**, not documents
- The output of HOTFIX is a deployed fix, which is code

**Contradiction**: Is HOTFIX output a "decision" (SOLVE) or "working code" (BUILD)?

**Impact**: Agent may misclassify work or apply wrong verb emphasis.

**Questions**:
1. Should HOTFIX/BUGFIX be BUILD workflows with abbreviated phases?
2. Or should they remain SOLVE with code as secondary output?

### ⚠️ `EDIRD-RV-05` [CONSULT]-FAIL Handler is Vague

**Where**: Section 9 (Verb Outcome Transitions)

**Claim**: `[CONSULT]-FAIL → [QUESTION] more specifically, or escalate`

**Problems**:
- What does "escalate" mean concretely? To whom? How?
- If `[ACTOR] = Agent` (autonomous mode), how does agent consult with itself?
- "More specifically" is subjective - how many retries?

**Impact**: Agent may get stuck when [CONSULT] fails in autonomous mode.

**Suggested fix**: Define escalation path explicitly. For autonomous mode, define fallback behavior (e.g., pause and wait for human, or proceed with documented assumption).

### ⚠️ `EDIRD-RV-06` Hybrid Workflow State Tracking Undefined

**Where**: Section 11 (Hybrid Situations - BUILD with Embedded SOLVE)

**Problem**: When doing "mini SOLVE" within BUILD:
- How is BUILD workflow state preserved?
- How does agent know when to "resume" BUILD vs continue SOLVE?
- What if mini SOLVE changes the understanding (e.g., reveals COMPLEXITY-HIGH)?
- Is the mini SOLVE a full 5-phase workflow or abbreviated?

**Impact**: Agent may lose context when switching workflows, or not know when to return.

**Suggested fix**: Define state preservation mechanism. Define explicit "return trigger" for embedded SOLVE.

## Medium Priority Issues

### ⚡ `EDIRD-RV-07` Gate Checklist Items are Subjective

**Where**: Section 7 (Phase Gates)

**Examples**:
- "Problem or goal clearly understood" - How does agent objectively verify this?
- "No blocking unknowns requiring [ACTOR] input" - How does agent know what it doesn't know?
- "Self-review complete" - What constitutes complete?

**Impact**: Different interpretations lead to inconsistent gate evaluation.

**Suggested fix**: Add measurable criteria or verification questions for subjective items.

### ⚡ `EDIRD-RV-08` EDIRD-IG-04 vs Verb Failure Handlers Conflict

**Where**: Section 15 (Implementation Guarantees), Section 9 (Verb Outcome Transitions)

**Statements**:
- EDIRD-IG-04: "Gate failures loop back within current phase, not to previous phases"
- Verb transitions: `[PROVE]-FAIL → [RESEARCH] (back to explore fundamentals)`

**Conflict**: [PROVE] is in DESIGN phase. If it fails, does agent:
- Stay in DESIGN (per IG-04)?
- Go back to EXPLORE to [RESEARCH] (per verb handler)?

**Impact**: Ambiguous behavior when [PROVE] fails.

**Suggested fix**: Clarify that IG-04 applies to gate failures, verb failures follow their specific handlers.

### ⚡ `EDIRD-RV-09` BUILD COMPLEXITY-LOW Skips Research

**Where**: Section 10 (BUILD COMPLEXITY-LOW Flow)

**Flow**: `[ANALYZE] → [ASSESS] → [DECIDE]` (no [RESEARCH])

**Problem**: What if there's nothing to analyze without research first? Single-file changes may still require checking documentation or existing patterns.

**Impact**: Agent may make uninformed decisions for simple tasks.

**Suggested fix**: Allow optional [RESEARCH] even for COMPLEXITY-LOW, or clarify when [ANALYZE] alone suffices.

## Questions That Need Answers

1. **Gate-to-verb mapping**: Which specific verb addresses each gate checklist item?

2. **Loop limits**: What's the maximum number of verb retries before escalation?

3. **HOTFIX identity**: Is HOTFIX output "code" or "decision"? Should it be BUILD?

4. **Autonomous [CONSULT]**: How does agent handle [CONSULT]-FAIL when [ACTOR] = Agent?

5. **Embedded SOLVE return**: What triggers return from mini SOLVE to parent BUILD?

6. **Subjective gates**: How to objectively verify "clearly understood" or "complete"?

## Summary

| Priority | Count | Status |
|----------|-------|--------|
| ❌ Critical | 3 | Needs resolution before implementation |
| ⚠️ High | 3 | Should address for robust operation |
| ⚡ Medium | 3 | Worth clarifying |

**Overall Assessment**: The spec provides a solid conceptual framework but has gaps in determinism guarantees. The "agent always knows what to do" claim is not fully supported by the specification. Critical issues center around undefined mappings and missing termination conditions.

**Recommendation**: Address Critical issues before using this spec for autonomous agent implementation.
