# REVIEW: Cascade Auto Model Switcher

**Doc ID**: CAMS-SP01-RV01
**Reviewing**: `_SPEC_CASCADE_MODEL_SWITCHER.md [CAMS-SP01]`
**Reviewer**: Devil's Advocate
**Date**: 2026-01-26

## Critical Finding: Fundamental Execution Model Flaw

**Severity**: CRITICAL - Design is not feasible as specified

### The Problem

The spec assumes the agent can switch models during workflow execution. This is **impossible** due to how Cascade works:

```
[User sends message]
       ↓
[Model is selected] ← FIXED for entire response
       ↓
[Agent generates response]
       ↓
[Response complete]
       ↓
[Next user message] ← Only here can model change
```

**Key insight**: The model is chosen BEFORE the agent starts responding. The agent cannot change its own model mid-turn.

### What the Spec Assumes (Incorrectly)

```markdown
## Execution Sequence
1. [CHORES] Read session files     ← Agent thinks it can
2. [HIGH] Analyze problem          ← switch between these
3. [MID] Implement fix             ← steps automatically
```

**Reality**: All steps in a single response use the SAME model.

### Why Phase 3 Will Never Work

From the spec:
> **Phase 3: Fully Automatic (Requires Hook)**
> 1. Agent detects tier change needed
> 2. Agent calls model switch script
> 3. Script switches model
> 4. Agent continues in new model

Step 4 is impossible. The agent that called the script is still the old model. The new model would need a NEW conversation turn to activate.

## Flawed Assumptions

### FA-01: Agent can switch models mid-execution

**Assumed**: Agent can trigger a model switch and continue in the new model
**Reality**: Model is fixed for the entire response. Switch only takes effect on NEXT user message.

### FA-02: Workflow execution is interruptible

**Assumed**: `/continue` can pause between steps for model switches
**Reality**: `/continue` executes as a single agent response. All steps use the same model.

### FA-03: STRUT plans can have per-step models

**Assumed**: `[MODEL:tier]` annotations cause automatic switching
**Reality**: Annotations are just text. Agent has no mechanism to switch itself.

## What Could Actually Work

### Alternative A: User-Driven Switching (Phase 1 Only)

The ONLY feasible approach with current Cascade architecture:

```
User: /continue
Agent (HIGH): "Next step needs CHORES tier. Please switch to SWE-1.5 and say 'continue'"
User: [manually switches model]
User: continue
Agent (CHORES): [executes chore tasks]
Agent: "Chores complete. Please switch back to HIGH and say 'continue'"
```

**Cost**: Extremely high friction. User must manually switch for EVERY tier change.

### Alternative B: Pre-Planned Single-Tier Batches

Instead of per-step switching, plan entire PHASES by tier:

```markdown
## Phase 1: CHORES Phase
Model: SWE-1.5 Fast
Tasks: Read files, run git status, list directories

## Phase 2: HIGH Phase  
Model: Claude Opus 4.5 (Thinking)
Tasks: Analyze problem, write spec, design solution

## Phase 3: MID Phase
Model: Claude Sonnet 4.5
Tasks: Implement fixes, verify code
```

User switches model ONCE per phase, not per step.

### Alternative C: Workflow-Level Model Recommendations

Instead of step-level switching, recommend models for ENTIRE workflows:

```markdown
/prime → Use CHORES model
/critique → Use HIGH model
/commit → Use CHORES model
```

User selects model BEFORE invoking workflow, not during.

### Alternative D: Accept Single Model Per Session

Simplest approach: Pick one model for the entire session based on dominant activity.

```
Session goal: "Write new feature spec" → Use HIGH for whole session
Session goal: "Run batch commits" → Use CHORES for whole session
```

## Revised Feasibility Assessment

| Approach | Feasible? | User Friction | Cost Savings |
|----------|-----------|---------------|--------------|
| Per-step switching | NO | N/A | N/A |
| User-driven (Phase 1) | YES | Very High | ~40% |
| Phase-level batching | YES | Medium | ~30% |
| Workflow-level | YES | Low | ~20% |
| Single model per session | YES | None | 0% |

## Recommendation

**Revise the spec to use Alternative B (Phase-Level Batching):**

1. Remove per-step `[MODEL:tier]` annotations
2. Add phase-level model recommendations
3. User switches model at phase boundaries (2-4 switches per session)
4. Agent reminds user when phase changes

**Example revised workflow:**

```markdown
## Execution Plan

### [MODEL:CHORES] Preparation Phase
1. Read session files
2. Check git status
3. List pending tasks
→ "Preparation complete. Switch to HIGH for Analysis phase."

### [MODEL:HIGH] Analysis Phase
4. Analyze problem
5. Design solution
6. Write spec section
→ "Analysis complete. Switch to MID for Implementation phase."

### [MODEL:MID] Implementation Phase
7. Implement changes
8. Verify code
9. Run tests
→ "Implementation complete. Switch to CHORES for Commit phase."

### [MODEL:CHORES] Commit Phase
10. Stage changes
11. Create commit
→ "Session complete."
```

## Summary

The spec as written cannot work because:
1. Models are fixed per response, not switchable mid-execution
2. Agent cannot switch its own model
3. Only user action between turns can change models

Revise to phase-level batching with user-initiated switches at phase boundaries.

## Document History

**[2026-01-26 12:18]**
- Initial critique identifying fundamental execution model flaw
