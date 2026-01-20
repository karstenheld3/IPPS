# INFO: STRUT Selected Concepts for Specification

**Doc ID**: STRUT-IN04
**Goal**: Exhaustive inventory of formal concepts and syntax selected for SPEC_STRUT_STRUCTURED_THINKING.md

**Timeline**: Created 2026-01-17, single day

**Depends on:**
- `INFO_STRUT_FEATURES.md [STRUT-IN01]` for research findings
- `INFO_STRUT_EXAMPLE_CASE_SIMULATION.md [STRUT-IN03]` for validated notation

## Summary

This document consolidates all formal concepts and syntax needed to write SPEC_STRUT_STRUCTURED_THINKING.md. It resolves inconsistencies between research documents and selects the final notation.

**Key Principle**: STRUT is a PLAN, not a log. It defines what WILL be done. Only gate checkboxes may be modified during execution.

## Table of Contents

- Core Definitions
- Plan Structure
- Verb Syntax
- Outcome System
- Repetition and Loops
- Control Flow
- Escalation Patterns
- Gate System
- Advanced Patterns
- Notation Summary
- Design Decisions

## 1. Core Definitions

### 1.1 What is STRUT

**STRUT** = Structured Thinking for agent workflow planning

A notation for:
- Planning complex tasks with explicit verb sequences
- Verifying completion via gates
- Supporting autonomous long runs

**Note**: Progress tracking is done in PROGRESS.md, not in STRUT. STRUT defines the plan; gates verify completion.

### 1.2 What STRUT is NOT

STRUT does NOT include:
- **Priority** - determined by sequence order
- **Time estimates** - use TASKS document HHW (Human Hours of Work)
- **Resource allocation** - single agent assumption
- **Detailed instructions** - belong in workflows/skills
- **Step outcomes** - STRUT is static during phase execution

**Modification rules**: STRUT may be modified after phase failure (re-plan). During normal execution, only gate checkboxes change.

### 1.3 Three Use Cases

1. **Session Planning** - Generate plan at session start
2. **Autonomous Execution** - Determine next action from plan state
3. **Resume/Handoff** - New agent understands overall thinking and exact state

### 1.4 Key Constraint

STRUT is LLM-evaluated, not machine-parsed. Notation must be unambiguous for LLM and human readers.

## 2. Plan Structure

### 2.1 Phase Block

```
[PHASE]: Description
├─ [VERB](params)
├─ [VERB](params)
└─> Gate:
    ├─ [ ] Condition 1
    └─ [ ] Condition 2
```

**Elements:**
- `[PHASE]` - Phase name from model (e.g., EXPLORE, DESIGN, IMPLEMENT)
- Description - Brief purpose statement
- Verb tree - Ordered sequence of actions
- Gate - Boolean checklist for phase completion

### 2.2 Phase Transitions

```
[FROM] → [TO]: Combined description
```

Example: `[EXPLORE] → [DESIGN]: Understand requirements and plan approach`

### 2.3 Indentation Rules

- 2-space indentation per level
- Box-drawing characters: `├─` `└─` `│` `└─>`
- ASCII fallback for human editing: `+-` `+-` `|` `+->`
- Gate arrow: `└─>` or `+->` indicates transition condition

## 3. Verb Syntax

### 3.1 Basic Verb

```
[VERB](parameter)
```

- Verb name in UPPERCASE with brackets
- Parameter in parentheses, natural spacing (not snake_case)
- Examples: `[IMPLEMENT](add database index)`, `[TEST](verify improvement)`

### 3.2 Verb with Description

```
├─ [VERB](param): description
```

Colon separates parameter from optional description.

### 3.3 Named Block Labels

```
├─ label_name:
│   ├─ [VERB]
│   └─ [VERB]
```

Labels enable jump targets. Use snake_case for labels.

### 3.4 Verb Categories (from Agentic English)

**Information Gathering**: GATHER, RESEARCH, ANALYZE, ASSESS, SCOPE
**Planning**: PLAN, DEFINE, OUTLINE, DECOMPOSE, PARTITION
**Validation**: VERIFY, TEST, REVIEW, CRITIQUE, RECONCILE
**Documentation**: WRITE-SPEC, WRITE-IMPL-PLAN, WRITE-TEST-PLAN, WRITE-INFO, DOCUMENT
**Implementation**: IMPLEMENT, FIX, COMMIT, DEPLOY, MERGE
**Communication**: CONSULT, QUESTION, PRESENT, PROPOSE, RECOMMEND
**Completion**: VALIDATE, CLOSE, FINALIZE, DECIDE

## 4. Outcome System

### 4.1 Verb Outcomes

- **(none)** - Success, continue (implicit)
- **-OK** - Explicit success (optional)
- **-FAIL** - Failed, triggers handler (required)
- **-SKIP** - Intentionally bypassed (required)

**Rule**: Success is implicit. Only show `-FAIL`, `-SKIP` when needed.

### 4.2 Outcome Transitions

```
├─ [VERB]
│   └─ -FAIL → [RECOVERY]
```

Explicit transitions define what happens on failure.

### 4.3 Standard Outcome Transitions (from EDIRD)

```
[RESEARCH] -FAIL → [CONSULT]
[ASSESS] -FAIL → [RESEARCH]
[PLAN] -FAIL → [RESEARCH] or [CONSULT]
[VERIFY] -FAIL → [FIX] → [VERIFY]
[TEST] -FAIL → [FIX] → [TEST]
[VALIDATE] -FAIL → [CONSULT]
[CONSULT] -FAIL → [QUESTION] or escalate
```

## 5. Retry Blocks

### 5.1 [RETRY] Verb (SELECTED NOTATION)

```
├─ [RETRY](xN) until [VERB]:
│   └─ [FIX]
├─ [CONSULT] on -FAIL
├─ [COMMIT]
```

**Syntax:** `[RETRY](xN) until [VERB]:`

**Elements:**
- `[RETRY]` - Retry verb (from AGEN vocabulary)
- `(xN)` - Max N attempts in parameter
- `until [VERB]` - Deciding verb that determines success/failure
- Block body - Steps to run between retry attempts
- `on -FAIL` - Handler when all N attempts exhausted

### 5.2 [RETRY] Semantics

**Flow:**
1. Run block steps (e.g., [FIX])
2. Evaluate UNTIL verb
3. If UNTIL verb succeeds (-OK) → exit retry, continue to next sibling
4. If UNTIL verb fails (-FAIL) → repeat from step 1 (up to N times)
5. If N attempts exhausted → trigger `on -FAIL` handler

**Key principle:** Success is implicit. Only exhaustion triggers explicit handler.

### 5.3 [RETRY] Control Flow

```
UNTIL verb succeeds (any attempt) → continue to next sibling
UNTIL verb fails N times → execute on -FAIL handler
```

### 5.4 For-Loop (Iteration)

```
├─ for item[n] in 1..N:
│   ├─ [IMPLEMENT](item[n])
│   ├─ [RETRY](x3) until [TEST](item[n]):
│   │   └─ [FIX]
│   ├─ [CONSULT] on -FAIL
│   └─ [COMMIT](item[n])
```

**Syntax:** `for item[n] in 1..N:` - iterate over range

## 6. Control Flow

### 6.1 Conditional Verb

```
├─ if CONDITION: [VERB]
```

Example: `├─ if COMPLEXITY-HIGH: [PROVE]`

### 6.2 Choice (Alternation)

```
├─ ([VERB-A] | [VERB-B])
```

Choose one of the alternatives.

### 6.3 Named Checkpoint and Jump (Dal Segno style)

```
├─ 𝄋 [VERB]                    ← named checkpoint
├─ ... other verbs ...
├─ D.S. [VERB] if -FAIL        ← jump back to checkpoint
```

**Note**: Prefer block labels over musical symbols for clarity.

### 6.4 Phase Skip

```
└─> Gate:
    └─ [x] No design needed → SKIP [DESIGN]
```

Gate condition can trigger phase skip.

### 6.5 Phase Iteration

```
├─ ITERATE: Back to [PHASE]
```

Restart phase from beginning after gate failure or rejection.

## 7. Escalation Patterns

### 7.1 CONSULT (Human in the Loop)

**When**: Agent lacks knowledge, authority, or capability.

```
├─ [VERB]{N, [CONSULT]}: description
│   └─ -FAIL ×N → [CONSULT](reason)
```

**Behavior**: Pause, present to user, wait for guidance, resume.

### 7.2 DEFER (Postpone and Continue)

**When**: Failure blocks one path but alternatives exist.

```
├─ [DEFER](items: reason)
│   ├─ item 1: reason
│   ├─ item 2: reason
│   └─ track in: PROBLEMS.md
```

**Behavior**: Mark as DEFERRED, log to PROBLEMS.md, continue with next verb.

### 7.3 ABORT (Fail Fast)

**When**: Failure is fundamental and continuing is wasteful.

```
├─ -FAIL ×N → ABORT(reason)
│   ├─ [DOCUMENT](findings)
│   └─ EXIT: ABORTED
```

**Behavior**: Stop all execution, record failure, require explicit restart.

### 7.4 DECOMPOSE (Adaptive Re-partitioning)

**When**: Task too large or complex.

```
├─ -FAIL → DECOMPOSE(subtasks):
│   ├─ subtask 1
│   ├─ subtask 2
│   └─ subtask 3
```

**Behavior**: Break down failing task, retry with smaller pieces.

### 7.5 Escalation Decision Matrix

```
                    Can continue without this verb?
                        YES                 NO
Human can help?  YES  → [DEFER]            [CONSULT]
                 NO   → [DEFER]            [ABORT]
```

## 8. Gate System

### 8.1 Gate Structure

```
└─> Gate:
    ├─ [ ] Condition 1
    ├─ [ ] Condition 2 (ref: FR-01)
    └─ [ ] Condition 3
```

**Rules:**
- Gates are boolean checklists
- Items use `[ ]` unchecked, `[x]` checked
- Gates can reference FR/IG/AC IDs
- Gate passes when ALL items checked

### 8.2 Gate as Plan Element

Gates are part of the PLAN. They define expected completion criteria BEFORE execution.

**Correct**: `[ ]` in plan, `[x]` when satisfied during execution
**Incorrect**: Pre-checking gates, using gates as outcome logs

### 8.3 Gate Failure

```
└─> Gate:
    └─ -FAIL → [ITERATE] [PHASE]
    └─ -FAIL ×2 → [CONSULT]
```

Gate failure triggers phase iteration or escalation.

## 9. Advanced Patterns

### 9.1 NEST (Nested Workflow)

```
├─ ┌─ NEST([WORKFLOW]): "sub-goal"
│  │  [EXPLORE] → ...
│  │  [DESIGN] → ...
│  │  [DELIVER] → Output: result
│  └─ END NEST
│  └─ -FAIL → [CONSULT]
├─ [VERB](result): continues with NEST output
```

**Semantics:**
- NEST creates complete sub-workflow with own phases and gates
- Parent pauses until NEST completes
- NEST output becomes input to next verb
- Nesting depth discouraged beyond 2 levels

### 9.2 Bounded Retry Shorthand

```
├─ [VERB]{N}: description              ← retry N times, then [CONSULT]
├─ [VERB]{N, [ESC]}: description       ← retry N times, then [ESC]
├─ [VERB]{∞}: description              ← infinite retries (COMPLEXITY-LOW)
```

### 9.3 Terminal States

```
└─> DONE                               ← workflow complete
└─> DONE: summary                      ← with outcome summary
└─> EXIT: ABORTED                      ← workflow aborted
```

## 10. Notation Summary

### 10.1 Symbols Reference

- **`[VERB]`** - Action verb
- **`(param)`** - Verb parameter
- **`:`** - Label or description separator
- **`├─`** - Tree branch (more siblings)
- **`└─`** - Tree branch (last sibling)
- **`└─>`** - Gate arrow
- **`│`** - Tree continuation
- **`[ ]`** - Unchecked gate item
- **`[x]`** - Checked gate item
- **`→`** - Transition arrow
- **`-FAIL`** - Failure outcome
- **`-OK`** - Success outcome (usually implicit)
- **`[RETRY](xN)`** - Retry verb with max N attempts
- **`until [VERB]`** - Deciding verb for retry
- **`on -FAIL`** - Exhaustion handler
- **`for item in 1..N:`** - For-loop iteration
- **`( | )`** - Choice/alternation
- **`𝄋`** - Checkpoint marker (optional)
- **`D.S.`** - Jump to checkpoint (optional)

### 10.2 Complete Example (Case 9 Pattern)

```
[IMPLEMENT]: Fix endpoints
├─ fix_endpoint_A:
│   ├─ [IMPLEMENT](add database index)
│   ├─ [RETRY](x3) until [TEST](verify improvement):
│   │   └─ [FIX]
│   ├─ [CONSULT] on -FAIL
│   └─ [COMMIT](fix A)
│
├─ [DEFER](C, D: blocked items)
│   ├─ C: requires architecture decision
│   └─ track in: PROBLEMS.md
│
└─> Gate:
    ├─ [ ] Fixable items addressed
    └─ [ ] Deferred items tracked
```

## 11. Design Decisions

### STRUT-DD-01: Verb-centric, not task-centric
Plan uses AGEN verbs, not arbitrary task descriptions. Ensures consistency with workflow definitions.

### STRUT-DD-02: Phase model agnostic
Works with EDIRD or alternative phase models. Phase names come from model, not hardcoded in STRUT.

### STRUT-DD-03: No time estimates
Tracks sequence and state, not duration. Time estimates belong in TASKS documents.

### STRUT-DD-04: Single agent assumption
No parallel execution or resource allocation. Agent executes verbs sequentially.

### STRUT-DD-05: Gate items are boolean
Checked/unchecked state only. No partial completion for gates.

### STRUT-DD-06: Implicit success
Success is the default outcome. Only failures and deviations require explicit notation.

### STRUT-DD-07: Bounded loops required
All loops must have `×N` max iterations. Prevents infinite loops in autonomous execution.

### STRUT-DD-08: STRUT is a plan, not a log
Defines what WILL be done. Only gate checkboxes may be modified during execution.

## 12. Consistency Rules

### 12.1 Notation Consistency

- Use `→` (Unicode arrow) not `->` (ASCII)
- Use `×` (Unicode multiplication) not `x` for iterations
- Use `├─` `└─` `│` (box-drawing) not `+-|` (ASCII)
- Use natural spacing in parameters, not snake_case

### 12.2 Label Naming

- Block labels: `snake_case` (e.g., `test_fix_cycle`, `commit_A`)
- Labels end with colon when declaring: `label:`
- Labels used without colon when referencing: `→ label`

### 12.3 Gate Formatting

- Gate keyword followed by colon: `Gate:`
- Each item on own line with checkbox
- Reference IDs in parentheses: `(ref: FR-01)`

## Document History

**[2026-01-17 18:46]**
- Changed: Replaced all loop notation with `[RETRY](xN) until [VERB]:` syntax
- Added: `for item in 1..N:` for-loop iteration syntax
- Removed: `|: :|` loop markers and labeled blocks (superseded by [RETRY])
- Changed: Section 5 renamed to "Retry Blocks"

**[2026-01-17 18:27]**
- Changed: Loop notation to use separate labeled blocks for fail/ok paths
- Removed: `-FAIL ×N` syntax inside loops (replaced with fall-through to fail_label)
- Removed: `<DevSystem>` tag (tables converted to lists per session rules)

**[2026-01-17 18:07]**
- Removed: `-PARTIAL` outcome (not used in examples, contradicts static plan principle)
- Added: ASCII fallback characters for human editing
- Added: Step outcomes excluded from STRUT
- Added: Modification rules (re-plan after phase failure only)
- Changed: Resume/Handoff use case wording

**[2026-01-17 17:55]**
- Initial document created
- Consolidated concepts from STRUT-IN01 and STRUT-IN03
- Selected final notation (block labels, loop markers, explicit outcomes)
- Added consistency rules
- Added 8 design decisions
