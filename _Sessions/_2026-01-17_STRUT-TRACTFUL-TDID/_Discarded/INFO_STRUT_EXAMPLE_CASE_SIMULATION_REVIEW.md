# Devil's Advocate Review: STRUT Example Case Simulations

**Reviewed**: 2026-01-17 16:20
**Document**: `INFO_STRUT_EXAMPLE_CASE_SIMULATION.md [STRUT-IN03]`
**Focus**: Assumptions, logic flaws, notation ambiguities

## MUST-NOT-FORGET (verified against)

1. Gate checks require evidence - cannot claim complete without artifacts
2. STRUT is phase-model agnostic - notation should not hardcode EDIRD
3. Single developer assumption is intentional
4. Problem types vs verbs must be disambiguated
5. Decomposition trigger is complexity-based

## Industry Research Findings

**BPMN/State Machine patterns**:
- BPMN uses explicit gateway symbols for branching (XOR, AND, OR)
- STRUT mixes inline conditionals with tree structure - potential parsing ambiguity

**Process Algebra known issues**:
- CSP deadlock detection requires formal analysis tools
- STRUT has no deadlock prevention - what if NEST never completes?

**DSL anti-patterns**:
- Overloading syntax (same symbol, different meanings in context)
- STRUT uses `->` for both sequence and conditional branch

**CI/CD gate patterns**:
- Quality gates are typically pass/fail with explicit failure actions
- STRUT gates show only checkboxes, no explicit failure path from gate

## Critical Issues

### ❌ C-01: Notation inconsistency - multiple arrow meanings

**What**: The `->` symbol has 3 different meanings:
- Sequence: `[VERB] -> -OK`
- Phase transition: `EXPLORE -> IMPLEMENT`
- Conditional: `-FAIL -> [FIX]`

**Why it's wrong**: Readers must infer meaning from context. In Case 7 line 434:
```
-FAIL{1}: undocumented_api_behavior
    └─ [FIX](adjust_to_actual_response) -> -OK
```
Is `-> -OK` a sequence or outcome assertion?

**Risk**: Parsing ambiguity if STRUT becomes machine-readable.

**Suggested fix**: Use distinct symbols:
- `→` for sequence
- `⇒` for conditional/outcome
- `↪` for phase transition

### ❌ C-02: Gate failure path undefined

**What**: All gates show only checked items. No case demonstrates what happens when a gate item is unchecked.

**Why it's wrong**: Gates are decision points. The notation shows:
```
└─> Gate: EXPLORE->DESIGN
    ├─ [x] Root cause identified
    └─ [x] Reproduction steps documented
```

But what if `[ ] Root cause identified`? Does workflow loop? Block? The notation is silent.

**Risk**: Agent implementing STRUT won't know how to handle gate failures.

**Suggested fix**: Add explicit gate failure handler syntax:
```
└─> Gate: EXPLORE->DESIGN
    ├─ [x] Root cause identified
    └─ [ ] Reproduction steps -> LOOP [ANALYZE]
```

### ❌ C-03: NEST completion assumption

**What**: Case 6 assumes NEST always completes successfully. No NEST-FAIL pattern shown.

**Why it's wrong**: What if email provider evaluation is inconclusive? What if all options are rejected?

**Evidence** (line 346):
```
└─ [ ] Email provider: UNKNOWN -> triggers NEST
```
NEST is triggered, but no path for NEST failure.

**Risk**: Nested workflows can fail, and parent must handle it.

**Suggested fix**: Add NEST-FAIL handling in Case 6:
```
│  └─ NEST-FAIL -> [CONSULT](product_owner) "no suitable provider"
```

## High Priority Issues

### ⚠️ H-01: Phase names hardcoded to EDIRD

**What**: All examples use `[EXPLORE]`, `[DESIGN]`, `[IMPLEMENT]`, `[REFINE]`, `[DELIVER]`.

**Why it matters**: NOTES.md states "STRUT is phase-model agnostic" (KD-02), but examples only show EDIRD phases.

**Risk**: Future users may assume STRUT only works with EDIRD.

**Suggested fix**: Add one example (or note) showing alternative phase model:
```
[DEFINE] -> [BUILD] -> [CHECK] -> [SHIP]  (hypothetical simplified model)
```

### ⚠️ H-02: Retry counter semantics unclear

**What**: Case 7 uses `-FAIL{1}`, `-FAIL{2}`, `-FAIL{3}` notation.

**Question**: Is this:
- (a) The Nth failure attempt? 
- (b) A labeled failure type?
- (c) Retry counter state?

**Evidence** (lines 433-437):
```
├─ -FAIL{1}: undocumented_api_behavior
├─ -FAIL{2}: sandbox_timeout
├─ -FAIL{3}: sandbox_still_timing_out
```
The colon after suggests (b) - labeled type. But `|: :| x3` suggests bounded retries where `{N}` is counter.

**Risk**: Notation collision between failure labels and retry counters.

**Suggested fix**: Clarify in Notation Reference:
- `{N}` after `-FAIL` = failure attempt number
- `:label` after `{N}` = failure reason annotation

### ⚠️ H-03: [COMMIT] verb overused as checkpoint

**What**: Every implementation step ends with `[COMMIT]`. 

**Why it matters**: Git commit is specific action. Some steps may warrant save/checkpoint without git commit.

**Evidence**: Case 5 has 12 steps, each with `[COMMIT]`. That's 12 git commits for one refactor.

**Question**: Is this realistic? Or should STRUT have `[CHECKPOINT]` for non-git saves?

**Suggested fix**: Distinguish `[COMMIT]` (git) from `[SAVE]` (generic checkpoint).

## Medium Priority Issues

### ⚠️ M-01: Parallel execution not shown

**What**: All cases show sequential execution. No parallel verb execution demonstrated.

**Evidence**: Case 9 fixes endpoints A, B, E sequentially, but these could run in parallel.

**Risk**: STRUT may not support parallelism, limiting expressiveness.

**Suggested fix**: Add parallel notation to Case 9:
```
├─ PARALLEL:
│   ├─ endpoint_A: [IMPLEMENT] -> [TEST] -> [COMMIT]
│   ├─ endpoint_B: [IMPLEMENT] -> [TEST] -> [COMMIT]
│   └─ endpoint_E: [IMPLEMENT] -> [TEST] -> [COMMIT]
```

### ⚠️ M-02: Time/duration completely absent

**What**: No case shows estimated or actual duration.

**Why it matters**: NOTES.md says "STRUT does NOT include time/priority" (KD-03). But for tracking, elapsed time per verb could be valuable.

**Not a bug**: This is intentional per KD-03. But worth noting that replay/simulation cannot estimate duration.

### ⚠️ M-03: ABORT lacks cleanup specification

**What**: Case 7 ABORT scenario shows:
```
└─ [ABORT](integration_impossible)
    ├─ [DOCUMENT](findings, blockers)
    ├─ [REPORT](to_stakeholders)
    └─ EXIT: ABORTED
```

**Question**: What about partial work cleanup? Rollback? Branch deletion?

**Risk**: ABORT may leave system in inconsistent state.

**Suggested fix**: Add cleanup verbs to ABORT pattern:
```
└─ [ABORT](integration_impossible)
    ├─ [ROLLBACK](partial_changes)
    ├─ [DOCUMENT](findings, blockers)
    ...
```

## Low Priority Issues

### L-01: Case 4 skips REFINE phase details

Case 4 (SOLVE workflow) has minimal REFINE phase compared to BUILD cases. May be intentional (SOLVE is lighter) but asymmetry is notable.

### L-02: Notation Reference incomplete

Missing from Notation Reference section:
- NEST syntax
- DECOMPOSE syntax  
- DEFER syntax
- ABORT syntax
- Named cycles (`impl_cycle:`)

These are used in cases but not defined in reference.

## Questions That Need Answers

1. **Can gates have partial pass?** (e.g., 3/5 items checked, proceed with caveat)
2. **Is NEST depth limited?** (NEST within NEST within NEST?)
3. **How does STRUT express rollback?** (Beyond [ABORT])
4. **Can verbs have multiple outcomes?** (e.g., -OK, -PARTIAL, -FAIL)
5. **How are external events represented?** (e.g., "user cancels", "timeout")

## Summary

| Category | Count |
|----------|-------|
| Critical | 3 |
| High | 3 |
| Medium | 3 |
| Low | 2 |
| Questions | 5 |

**Top 3 Actions**:
1. **Disambiguate `->` symbol** - Critical for machine parsing
2. **Define gate failure handling** - Critical for completeness
3. **Add NEST-FAIL pattern** - High impact for nested workflows

## Document History

**[2026-01-17 16:20]**
- Initial Devil's Advocate review
- 3 critical, 3 high, 3 medium, 2 low issues identified
- 5 open questions raised
