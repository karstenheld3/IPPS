<DevSystem MarkdownTablesAllowed=true />

# INFO: STRUT Example Case Simulations

**Doc ID**: STRUT-IN03
**Goal**: Formalize all 10 test cases using STRUT notation with gates and repetition

**Depends on:**
- `INFO_STRUT_EXAMPLE_CASES.md [STRUT-IN02]` for case descriptions
- `INFO_STRUT_FEATURES.md [STRUT-IN01]` for notation reference

**Timeline**: Created 2026-01-17, 1 update, single day

## Key Principle

**STRUT is a PLAN, not a log.** It defines what WILL be done, independent of execution outcomes. The only modification allowed during execution is checking gate items (`[ ]` -> `[x]`). Annotations like `(quick)` or `(blocked)` are pre-categorizations known at planning time, not discovered outcomes.

## Summary

All 10 test cases formalized in STRUT notation with:
- Phase transitions with gate checkboxes (`[x]`/`[ ]`)
- Repetition notation (`|: :| xN`)
- Escalation patterns (CONSULT, DEFER, ABORT, DECOMPOSE)
- Nested workflows (NEST pattern in Case 6)
- Phase iteration (backtracking in Case 10)

Patterns demonstrated: Phase skip (1), Retry (2,5,6,7,8,10), NEST (6), DEFER (9), ABORT (7), DECOMPOSE (8), Iteration (10).

## Notation Reference

**Phases**: `[EXPLORE]` `[DESIGN]` `[IMPLEMENT]` `[REFINE]` `[DELIVER]`

**Verb syntax**: `[VERB](parameter)` - parameter uses natural spacing, not snake_case

**Verb outcomes** (implicit = success, only show deviations):
- (implicit) - success, continue to next verb
- `-FAIL` - failed, triggers explicit transition
- `-SKIPPED` - intentionally bypassed, continue

**Outcome transitions** (MUST be explicit in STRUT plans, per EDIRD):
- `[RESEARCH] -FAIL -> [CONSULT]`
- `[ASSESS] -FAIL -> [RESEARCH]`
- `[PLAN] -FAIL -> [RESEARCH] or [CONSULT]`
- `[VERIFY] -FAIL -> [FIX] -> [VERIFY]`
- `[TEST] -FAIL -> [FIX] -> [TEST]`
- `[VALIDATE] -FAIL -> [CONSULT]`
- `[CONSULT] -FAIL -> [QUESTION] or escalate`

**Repetition**:
- `|: [VERB] :| xN` - repeat max N times

**Gates**: `Gate:` with `[x]` checked, `[ ]` unchecked
- Gate failure: workflow loops within current phase until satisfied
- Gate items reference requirements: `(ref: FR-XX)`

**Phase control**:
- `SKIP [PHASE]` - bypass entire phase when gate permits

**Advanced patterns**:
- `[SOLVE](TYPE): "question"` - embedded sub-workflow
- `[BUILD](TYPE): "task"` - embedded sub-workflow
- `-FAIL -> [CONSULT]` - handler when nested workflow fails
- `DEFER(item, reason)` - postpone item, track in PROBLEMS.md
- `ABORT(reason)` - terminate workflow, document findings
- `DECOMPOSE(subtasks)` - split into smaller tasks after failure threshold

## Case 1: Simple Hotfix (COMPLEXITY-LOW, HOTFIX)

**Problem Type**: HOTFIX
**Workflow**: BUILD
**Phases**: EXPLORE -> IMPLEMENT -> DELIVER (skip DESIGN, REFINE)

```
[EXPLORE]: Understand the bug
├─ [ANALYZE](stack trace)
├─ [SCOPE](single file fix)
└─> Gate:
    ├─ [x] Root cause identified
    ├─ [x] Fix location known
    └─ [x] No design decision needed -> SKIP DESIGN

[IMPLEMENT]: Apply fix
├─ [IMPLEMENT](null check)
├─ [TEST](existing unit tests)
├─ [COMMIT](hotfix branch)
└─> Gate:
    ├─ [x] Fix applied
    ├─ [x] Tests pass
    └─ [x] No new tests needed -> SKIP REFINE

[DELIVER]: Deploy
├─ [DEPLOY](production)
├─ [CLOSE](ticket)
└─> DONE
```

**Patterns used**: Linear flow, phase skipping

## Case 2: Bug Investigation (COMPLEXITY-MEDIUM, BUGFIX)

**Problem Type**: BUGFIX
**Workflow**: BUILD
**Phases**: EXPLORE -> DESIGN -> IMPLEMENT -> REFINE -> DELIVER

```
[EXPLORE]: Investigate root cause
├─ [GATHER](logs, user reports)
├─ [ANALYZE](cart calculation code)
├─ [PROVE](add logging)
├─ [DEPLOY](staging instrumented)
├─ |: [TEST](reproduce issue) :| x3
│   └─ -FAIL -> [ANALYZE](more logs)
├─ [ASSESS](COMPLEXITY-MEDIUM)
└─> Gate:
    ├─ [x] Root cause identified: race condition
    ├─ [x] Reproduction steps documented
    └─ [x] Complexity assessed

[DESIGN]: Plan fix
├─ [PLAN](optimistic locking)
├─ [WRITE-SPEC](fix approach)
└─> Gate:
    ├─ [x] Fix approach documented
    └─ [x] No POC needed (known pattern)

[IMPLEMENT]: Apply fix and add test
├─ [IMPLEMENT](optimistic lock)
├─ [TEST](new regression test)
│   └─ -FAIL -> [FIX] -> [TEST]
├─ [COMMIT](bugfix branch)
└─> Gate:
    ├─ [x] Fix implemented
    ├─ [x] New test added
    └─ [x] Tests pass

[REFINE]: Verify fix
├─ [REVIEW](self review)
├─ [TEST](full regression)
│   └─ -FAIL -> [FIX] -> [TEST]
└─> Gate:
    ├─ [x] Self-review complete
    └─ [x] Regression tests pass

[DELIVER]: Deploy
├─ [DEPLOY](production)
├─ [CLOSE](ticket)
└─> DONE
```

**Patterns used**: Bounded retry in EXPLORE, named cycle in IMPLEMENT

## Case 3: Add API Endpoint (COMPLEXITY-MEDIUM, FEATURE)

**Problem Type**: FEATURE
**Workflow**: BUILD
**Phases**: Full EDIRD

```
[EXPLORE]: Understand requirements
├─ [RESEARCH](existing api patterns)
│   └─ -FAIL -> [CONSULT]
├─ [GATHER](requirements: pagination, filtering, rate limit)
├─ [ASSESS](COMPLEXITY-MEDIUM)
├─ [SCOPE](single endpoint, 3 query params)
└─> Gate:
    ├─ [x] Requirements gathered
    ├─ [x] Existing patterns understood
    └─ [x] Scope defined

[DESIGN]: Spec and plan
├─ [PLAN](controller service repo layers)
│   └─ -FAIL -> [RESEARCH] or [CONSULT]
├─ [WRITE-SPEC](endpoint spec)
├─ [WRITE-IMPL-PLAN](implementation steps)
├─ [WRITE-TEST-PLAN](test coverage)
├─ [DECOMPOSE](5 implementation steps)
└─> Gate:
    ├─ [x] _SPEC_*.md exists
    ├─ [x] _IMPL_*.md exists
    ├─ [x] _TEST_*.md exists
    └─ [x] Plan decomposed

[IMPLEMENT]: Build endpoint
├─ step 1:
│   ├─ [IMPLEMENT](repository query)
│   ├─ [TEST](unit test repo)
│   │   └─ -FAIL -> [FIX] -> [TEST]
│   └─ [COMMIT](step 1)
├─ step 2:
│   ├─ [IMPLEMENT](service layer)
│   ├─ [TEST](unit test service)
│   │   └─ -FAIL -> [FIX] -> [TEST]
│   └─ [COMMIT](step 2)
├─ step 3:
│   ├─ [IMPLEMENT](controller)
│   ├─ [TEST](integration test)
│   │   └─ -FAIL -> [FIX] -> [TEST]
│   └─ [COMMIT](step 3)
├─ step 4:
│   ├─ [IMPLEMENT](pagination filtering)
│   ├─ [TEST](pagination tests)
│   │   └─ -FAIL -> [FIX] -> [TEST]
│   └─ [COMMIT](step 4)
├─ step 5:
│   ├─ [IMPLEMENT](rate limiting)
│   ├─ [TEST](rate limit tests)
│   │   └─ -FAIL -> [FIX] -> [TEST]
│   └─ [COMMIT](step 5)
└─> Gate:
    ├─ [x] All 5 steps complete
    ├─ [x] All tests pass
    └─ [x] No TODO/FIXME

[REFINE]: Review and docs
├─ [REVIEW](self review)
├─ [VERIFY](against spec)
│   └─ -FAIL -> [FIX] -> [VERIFY]
├─ [WRITE](api documentation)
└─> Gate:
    ├─ [x] Self-review complete
    ├─ [x] Verification passed
    └─ [x] API docs updated

[DELIVER]: Merge
├─ [VALIDATE](with product team)
│   └─ -FAIL -> [CONSULT]
├─ [MERGE](feature branch)
├─ [CLOSE](ticket)
└─> DONE
```

**Patterns used**: Decomposed steps, incremental commits

## Case 4: Evaluate Database Options (SOLVE, EVALUATION)

**Problem Type**: EVALUATION
**Workflow**: SOLVE
**Phases**: Full EDIRD (knowledge output)

```
[EXPLORE]: Define evaluation scope
├─ [RESEARCH](current sqlite limits)
│   └─ -FAIL -> [CONSULT]
├─ [GATHER](performance requirements)
├─ [SCOPE](3 options: postgres, mysql, sqlite optimized)
├─ [ASSESS](EVALUATION)
└─> Gate:
    ├─ [x] Problem understood
    ├─ [x] Options identified
    └─ [x] Scope defined

[DESIGN]: Define evaluation framework
├─ [PLAN](evaluation methodology)
│   └─ -FAIL -> [RESEARCH] or [CONSULT]
├─ [DEFINE](criteria: performance, cost, migration effort, expertise)
├─ [OUTLINE](info document structure)
└─> Gate:
    ├─ [x] Criteria defined
    ├─ [x] Methodology planned
    └─ [x] Output structure outlined

[IMPLEMENT]: Conduct evaluation
├─ [RESEARCH](postgresql capabilities)
│   └─ -FAIL -> [CONSULT]
├─ [RESEARCH](mysql capabilities)
│   └─ -FAIL -> [CONSULT]
├─ [RESEARCH](sqlite optimization)
│   └─ -FAIL -> [CONSULT]
├─ [PROVE](benchmark each option)
│   ├─ [TEST](postgres benchmark)
│   ├─ [TEST](mysql benchmark)
│   └─ [TEST](sqlite benchmark)
├─ [EVALUATE](options against criteria)
├─ [WRITE-INFO](evaluation findings)
└─> Gate:
    ├─ [x] All options evaluated
    ├─ [x] Benchmarks complete
    └─ [x] Findings documented

[REFINE]: Verify findings
├─ [REVIEW](evaluation logic)
├─ [VERIFY](benchmark methodology)
│   └─ -FAIL -> [FIX] -> [VERIFY]
├─ [CRITIQUE](are criteria complete)
└─> Gate:
    ├─ [x] Logic verified
    ├─ [x] Methodology sound
    └─ [x] No gaps in analysis

[DELIVER]: Present and decide
├─ [PRESENT](findings to team)
├─ [PROPOSE](postgresql recommendation)
├─ [VALIDATE](team accepts)
│   └─ -FAIL -> [CONSULT]
├─ [DECIDE](PostgreSQL)
├─ [CLOSE](evaluation)
└─> DONE: Decision = PostgreSQL
```

**Patterns used**: SOLVE workflow, multiple parallel research, decision output

## Case 5: Refactor Authentication Module (COMPLEXITY-HIGH, REFACTORING)

**Problem Type**: REFACTORING
**Workflow**: BUILD
**Phases**: Full EDIRD with comprehensive docs

```
[EXPLORE]: Map current state
├─ [ANALYZE](15 auth files)
├─ [GATHER](dependency map)
├─ [RESEARCH](auth best practices)
│   └─ -FAIL -> [CONSULT]
├─ [ASSESS](COMPLEXITY-HIGH)
├─ [SCOPE](consolidate to single module, maintain backward compat)
└─> Gate:
    ├─ [x] All auth code mapped
    ├─ [x] Dependencies documented
    ├─ [x] Scope defined with constraints

[DESIGN]: Comprehensive planning
├─ [PLAN](new module architecture)
│   └─ -FAIL -> [RESEARCH] or [CONSULT]
├─ [WRITE-SPEC](auth module spec)
├─ [PROVE](adapter pattern poc)
│   └─ -FAIL -> [RESEARCH]
├─ [WRITE-IMPL-PLAN](12 ordered steps)
├─ [WRITE-TEST-PLAN](test strategy)
├─ [DECOMPOSE](steps with rollback points)
└─> Gate:
    ├─ [x] _SPEC_AUTH.md exists
    ├─ [x] _IMPL_AUTH.md exists (12 steps)
    ├─ [x] _TEST_AUTH.md exists
    ├─ [x] POC validated adapter pattern
    └─ [x] Each step has rollback plan

[IMPLEMENT]: Incremental refactor
├─ |: step[n] for n in 1..12 :|
│   ├─ [IMPLEMENT](step[n])
│   │   └─ -FAIL -> |: [FIX] :| x2
│   │       └─ -FAIL -> [CONSULT](tech lead)
│   ├─ [TEST](step[n] tests)
│   │   └─ -FAIL -> [FIX] -> [TEST]
│   ├─ [VERIFY](backward compat)
│   │   └─ -FAIL -> [FIX] -> [VERIFY]
│   └─ [COMMIT](step[n])
└─> Gate:
    ├─ [x] All 12 steps complete
    ├─ [x] All tests pass
    ├─ [x] Backward compatibility verified
    └─ [x] No deprecated code remains

[REFINE]: Comprehensive review
├─ [REVIEW](full module)
├─ [VERIFY](against spec)
│   └─ -FAIL -> [FIX] -> [VERIFY]
├─ [TEST](full regression)
│   └─ -FAIL -> [FIX] -> [TEST]
├─ [CRITIQUE](architecture review)
├─ [RECONCILE](critique findings)
└─> Gate:
    ├─ [x] Self-review complete
    ├─ [x] Spec verification passed
    ├─ [x] All critique items addressed
    └─ [x] Regression tests pass

[DELIVER]: Merge and document
├─ [VALIDATE](with team)
│   └─ -FAIL -> [CONSULT]
├─ [MERGE](refactor branch)
├─ [WRITE](migration guide)
├─ [CLOSE](refactor ticket)
└─> DONE
```

**Patterns used**: Bounded retry with escalation, loop over steps, comprehensive docs

## Case 6: Feature with Embedded Research (NEST pattern)

**Problem Type**: FEATURE (with embedded EVALUATION)
**Workflow**: BUILD with nested SOLVE
**Phases**: Full EDIRD with NEST

```
[EXPLORE]: Understand password reset feature
├─ [GATHER](requirements: email reset flow)
├─ [ANALYZE](existing auth code)
├─ [ASSESS](COMPLEXITY-HIGH, unknown: email provider)
├─ [SCOPE](password reset with email)
└─> Gate:
    ├─ [x] Requirements clear
    ├─ [x] Existing code analyzed
    └─ [ ] Email provider: UNKNOWN -> triggers [SOLVE]

[DESIGN]: Design with nested decision
├─ [PLAN](reset flow architecture)
│   └─ -FAIL -> [RESEARCH] or [CONSULT]
├─ ┌─ [SOLVE](EVALUATION): "Which email provider?"
│  │  [EXPLORE]:
│  │  ├─ [RESEARCH](sendgrid)
│  │  │   └─ -FAIL -> [CONSULT]
│  │  ├─ [RESEARCH](mailgun)
│  │  │   └─ -FAIL -> [CONSULT]
│  │  ├─ [RESEARCH](aws ses)
│  │  │   └─ -FAIL -> [CONSULT]
│  │  └─> Gate: [x] Options researched
│  │  
│  │  [DESIGN]:
│  │  ├─ [DEFINE](criteria: cost, api, deliverability)
│  │  └─> Gate: [x] Criteria defined
│  │  
│  │  [IMPLEMENT]:
│  │  ├─ [EVALUATE](options against criteria)
│  │  └─> Gate: [x] Evaluation complete
│  │  
│  │  [DELIVER]:
│  │  ├─ [DECIDE](SendGrid)
│  │  └─> Output: provider = SendGrid
│  ├─ -FAIL -> [CONSULT](product owner): "no suitable provider found"
│  └─ END [SOLVE]
├─ [WRITE-SPEC](reset with sendgrid)
├─ [WRITE-IMPL-PLAN](implementation steps)
└─> Gate:
    ├─ [x] Email provider decided: SendGrid
    ├─ [x] _SPEC_*.md exists
    └─ [x] _IMPL_*.md exists

[IMPLEMENT]: Build feature
├─ [IMPLEMENT](reset token generation)
├─ [IMPLEMENT](sendgrid integration)
├─ [IMPLEMENT](reset endpoint)
├─ |: [TEST] :| x3
│   └─ -FAIL -> [FIX](mock config)
├─ [IMPLEMENT](failure handling: retry, fallback)
├─ [TEST](end to end)
│   └─ -FAIL -> [FIX] -> [TEST]
├─ [COMMIT](feature)
└─> Gate:
    ├─ [x] All components implemented
    ├─ [x] Tests pass
    └─ [x] Failure handling in place

[REFINE]: Review
├─ [REVIEW](security review)
├─ [VERIFY](against spec)
│   └─ -FAIL -> [FIX] -> [VERIFY]
└─> Gate:
    ├─ [x] Security verified
    └─ [x] Spec compliance verified

[DELIVER]: Merge
├─ [VALIDATE](with team)
│   └─ -FAIL -> [CONSULT]
├─ [MERGE](feature branch)
├─ [CLOSE](ticket)
└─> DONE
```

**Patterns used**: NEST for embedded SOLVE, retry in IMPLEMENT

## Case 7: Payment Integration with Failures (RETRY, CONSULT, ABORT)

**Problem Type**: FEATURE
**Workflow**: BUILD
**Phases**: Full EDIRD with escalation patterns

```
[EXPLORE]: Understand integration
├─ [RESEARCH](payment api docs)
│   └─ -FAIL -> [CONSULT]
├─ [GATHER](requirements: payments, refunds)
├─ [ASSESS](COMPLEXITY-HIGH)
└─> Gate:
    ├─ [x] API docs reviewed
    └─ [x] Requirements gathered

[DESIGN]: Plan integration
├─ [PLAN](payment client architecture)
│   └─ -FAIL -> [RESEARCH] or [CONSULT]
├─ [WRITE-SPEC](integration spec)
├─ [WRITE-IMPL-PLAN](steps)
└─> Gate:
    ├─ [x] _SPEC_*.md exists
    └─ [x] _IMPL_*.md exists

[IMPLEMENT]: Build with failures and recovery
├─ [IMPLEMENT](payment client)
├─ |: [TEST](sandbox) :| x3
│   ├─ -FAIL: undocumented api behavior
│   │   └─ [FIX](adjust to actual response)
│   ├─ -FAIL: sandbox timeout
│   │   └─ [FIX](increase timeout) -FAIL
│   ├─ -FAIL: sandbox still timing out
│   │   └─ [CONSULT](tech lead)
│   │       ├─ [CONSULT](vendor)
│   │       ├─ vendor response: sandbox issue, workaround provided
│   │       └─ [FIX](apply workaround)
├─ [IMPLEMENT](remaining edge cases)
├─ [TEST](full suite)
│   └─ -FAIL -> [FIX] -> [TEST]
├─ [COMMIT](integration)
└─> Gate:
    ├─ [x] Integration complete
    ├─ [x] Tests pass with workaround
    └─ [x] Edge cases handled

[REFINE]: Review
├─ [REVIEW](self review)
├─ [VERIFY](against spec)
│   └─ -FAIL -> [FIX] -> [VERIFY]
└─> Gate:
    ├─ [x] Self-review complete
    └─ [x] Spec verified

[DELIVER]: Deploy
├─ [VALIDATE](with team)
│   └─ -FAIL -> [CONSULT]
├─ [MERGE](feature branch)
├─ [DEPLOY](production)
├─ [CLOSE](ticket)
└─> DONE
```

**ABORT Scenario (edge case)**:
```
├─ |: [TEST](sandbox) :| x3
│   └─ -FAIL -> [CONSULT](tech lead)
│       ├─ [CONSULT](vendor)
│       ├─ vendor response: API DEPRECATED NO REPLACEMENT
│       └─ ABORT(integration impossible)
│           ├─ [DOCUMENT](findings, blockers)
│           ├─ [REPORT](to stakeholders)
│           └─ EXIT: ABORTED
```

**Patterns used**: Bounded retry, CONSULT escalation chain, ABORT for unrecoverable

## Case 8: Task Decomposition After Failure (DECOMPOSE-ON-FAIL)

**Problem Type**: FEATURE
**Workflow**: BUILD
**Decomposition trigger**: 3 failures for COMPLEXITY-MEDIUM

```
[EXPLORE]: Understand export feature
├─ [GATHER](requirements: 5 data types, csv format)
├─ [ASSESS](COMPLEXITY-MEDIUM)
└─> Gate:
    ├─ [x] Requirements gathered
    └─ [x] Complexity assessed

[DESIGN]: Initial plan (too coarse)
├─ [PLAN](single export module)
│   └─ -FAIL -> [RESEARCH] or [CONSULT]
├─ [WRITE-IMPL-PLAN](monolithic approach)
└─> Gate:
    ├─ [x] Plan exists
    └─ [x] Ready to implement

[IMPLEMENT]: Attempt monolithic -> fail -> decompose
├─ attempt monolithic:
│   ├─ [IMPLEMENT](unified export) -FAIL: complexity overwhelming
│   ├─ [FIX](simplify approach) -FAIL: still too complex
│   ├─ [FIX](different strategy) -FAIL: third failure
│   └─ TRIGGER: 3 failures reached -> DECOMPOSE
│
├─ DECOMPOSE(into 5 subtasks):
│   ├─ subtask 1: export users
│   ├─ subtask 2: export orders
│   ├─ subtask 3: export products
│   ├─ subtask 4: export transactions
│   └─ subtask 5: export audit logs
│
├─ |: subtask[n] for n in 1..5 :|
│   ├─ [IMPLEMENT](subtask[n])
│   ├─ [TEST](subtask[n])
│   │   └─ -FAIL -> [FIX] -> [TEST]
│   └─ [COMMIT](subtask[n])
│
├─ [IMPLEMENT](aggregation module)
├─ [TEST](integration test)
│   └─ -FAIL -> [FIX] -> [TEST]
├─ [COMMIT](unified export)
└─> Gate:
    ├─ [x] All 5 subtasks complete
    ├─ [x] Aggregation complete
    └─ [x] Integration test passes

[REFINE]: Review
├─ [REVIEW](all components)
├─ [VERIFY](against requirements)
│   └─ -FAIL -> [FIX] -> [VERIFY]
└─> Gate:
    └─ [x] All verified

[DELIVER]: Merge
├─ [MERGE](feature branch)
├─ [CLOSE](ticket)
└─> DONE
```

**Patterns used**: DECOMPOSE-ON-FAIL trigger, loop over subtasks, aggregation

## Case 9: Performance Sprint with DEFER (partial completion)

**Problem Type**: CHORE
**Workflow**: BUILD
**Pattern**: DEFER for blocked items

```
[EXPLORE]: Profile slow endpoints
├─ [ANALYZE](performance profiling)
├─ [GATHER](5 slow endpoints: A, B, C, D, E)
├─ [ASSESS](COMPLEXITY-MEDIUM)
└─> Gate:
    ├─ [ ] Slow endpoints identified
    └─ [ ] Profiling data collected

[DESIGN]: Plan fixes
├─ [PLAN](fix strategy per endpoint):
│   ├─ A: add index (quick)
│   ├─ B: fix n plus 1 (quick)
│   ├─ C: add cache layer (architectural)
│   ├─ D: external service optimization (blocked)
│   └─ E: optimize serialization (quick)
│   └─ -FAIL → [RESEARCH] or [CONSULT]
└─> Gate:
    └─ [ ] Fix strategy defined

[IMPLEMENT]: Fix what we can, defer rest
├─ fix_endpoint_A:
│   ├─ [IMPLEMENT](add database index)
│   ├─ |: test_A :| ×3:
│   │   ├─ [TEST](verify improvement)
│   │   │   └─ -FAIL → [FIX] → test_A
│   │   │   └─ -OK → commit_A
│   │   └─ -FAIL ×3 → [CONSULT]
│   └── commit_A:
│       └─ [COMMIT](fix A)
│
├─ fix_endpoint_B:
│   ├─ [IMPLEMENT](fix n plus 1 query)
│   ├─ |: test_B :| ×3:
│   │   ├─ [TEST](verify improvement)
│   │   │   └─ -FAIL → [FIX] → test_B
│   │   │   └─ -OK → commit_B
│   │   └─ -FAIL ×3 → [CONSULT]
│   └── commit_B:
│       └─ [COMMIT](fix B)
│
├─ fix_endpoint_E:
│   ├─ [IMPLEMENT](optimize serialization)
│   ├─ |: test_E :| ×3:
│   │   ├─ [TEST](verify improvement)
│   │   │   └─ -FAIL → [FIX] → test_E
│   │   │   └─ -OK → commit_E
│   │   └─ -FAIL ×3 → [CONSULT]
│   └── commit_E:
│       └─ [COMMIT](fix E)
│
├─ [DEFER](C, D: blocked endpoints)
│   ├─ C: requires architecture decision
│   ├─ D: waiting on platform team
│   └─ track in: PROBLEMS.md
│
└─> Gate:
    ├─ [ ] All fixable endpoints addressed (A, B, E)
    └─ [ ] Deferred items tracked in PROBLEMS.md (C, D)

[REFINE]: Review completed fixes
├─ [REVIEW](fixes A B E)
├─ |: verify_perf :| ×3:
│   ├─ [VERIFY](performance improvement)
│   │   └─ -FAIL → [FIX] → verify_perf
│   │   └─ -OK → refine_done
│   └─ -FAIL ×3 → [CONSULT]
└── refine_done:
    └─> Gate:
        ├─ [ ] Completed fixes verified
        └─ [ ] Deferred items documented

[DELIVER]: Deploy completed, track deferred
├─ [DEPLOY](production)
├─ [DOCUMENT](deferred items for next sprint)
├─ [CLOSE](sprint ticket, partial: 3/5)
└─> DONE: 3/5 complete, 2 deferred
```

**Patterns used**: DEFER as planning verb, boolean gates only

**Key principle**: STRUT is a PLAN of what WILL be done, not a log. Gates are boolean (pass/fail). DEFER appears in the plan body as an action, not as a gate state.

## Case 10: Full Workflow with Phase Iteration

**Problem Type**: FEATURE
**Workflow**: BUILD
**Pattern**: Phase backtracking, stakeholder iteration

```
[EXPLORE]: Gather requirements (with conflict)
├─ [GATHER](stakeholder A requirements)
├─ [GATHER](stakeholder B requirements)
├─ [GATHER](stakeholder C requirements)
├─ [ANALYZE](requirements) -> CONFLICT DETECTED
├─ [CONSULT](product owner):
│   ├─ conflict: A wants charts, B wants tables, C wants both
│   └─ resolution: start with charts, add tables later
├─ [SCOPE](dashboard with charts, tables phase 2)
├─ [ASSESS](COMPLEXITY-HIGH)
└─> Gate:
    ├─ [x] Requirements gathered
    ├─ [x] Conflicts resolved
    └─ [x] Scope defined

[DESIGN]: Initial design (rejected, iterate)
├─ [PLAN](react with chartjs)
│   └─ -FAIL -> [RESEARCH] or [CONSULT]
├─ [WRITE-SPEC](dashboard spec v1)
├─ [VALIDATE](with stakeholders) -FAIL
│   └─ rejection: "ChartJS not flexible enough, need D3"
│   └─ -FAIL -> [CONSULT]
│
├─ ITERATE: Back to [PLAN]
│   ├─ [PLAN](react with d3)
│   ├─ [WRITE-SPEC](dashboard spec v2)
│   ├─ [PROVE](d3 integration poc)
│   │   └─ -FAIL -> [RESEARCH]
│   └─ [VALIDATE](with stakeholders)
│       └─ -FAIL -> [CONSULT]
│
├─ [WRITE-IMPL-PLAN](implementation steps)
├─ [DECOMPOSE](component by component)
└─> Gate:
    ├─ [x] D3 approach validated
    ├─ [x] POC successful
    ├─ [x] _SPEC_*.md exists (v2)
    └─ [x] _IMPL_*.md exists

[IMPLEMENT]: Build dashboard
├─ |: component[n] for n in 1..5 :|
│   ├─ [IMPLEMENT](component[n])
│   │   └─ -FAIL -> |: [FIX] :| x3
│   │       └─ -FAIL -> [CONSULT](tech lead)
│   ├─ [TEST](component[n])
│   │   └─ -FAIL -> [FIX] -> [TEST]
│   └─ [COMMIT](component[n])
│
└─> Gate:
    ├─ [x] All components complete
    ├─ [x] Tests pass
    └─ [x] No TODO/FIXME

[REFINE]: Review with issues found
├─ [REVIEW](self review)
├─ [VERIFY](against spec)
│   └─ -FAIL -> [FIX] -> [VERIFY]
├─ [CRITIQUE](accessibility review) -> ISSUES FOUND
│   └─ issue: missing ARIA labels
├─ [FIX](add aria labels)
├─ [TEST](accessibility tests)
│   └─ -FAIL -> [FIX] -> [TEST]
├─ [VALIDATE](stakeholder review) -> MISSING CHART TYPE
│   └─ issue: need pie chart, not just bar/line
│   └─ -FAIL -> [CONSULT]
├─ |: iterate on feedback :|
│   ├─ [IMPLEMENT](pie chart component)
│   ├─ [TEST](pie chart)
│   │   └─ -FAIL -> [FIX] -> [TEST]
│   └─ [COMMIT](add pie chart)
├─ [TEST](full regression)
│   └─ -FAIL -> [FIX] -> [TEST]
├─ [VALIDATE](stakeholder final)
│   └─ -FAIL -> [CONSULT]
└─> Gate:
    ├─ [x] Self-review complete
    ├─ [x] Accessibility issues fixed
    ├─ [x] Missing chart type added
    └─ [x] Stakeholder approved

[DELIVER]: Final deployment
├─ [VALIDATE](sign off)
│   └─ -FAIL -> [CONSULT]
├─ [MERGE](feature branch)
├─ [DEPLOY](production)
├─ [CLOSE](ticket)
└─> DONE
```

**Patterns used**: Phase iteration (DESIGN rejected/restart), stakeholder loops, CRITIQUE/FIX cycle, late requirements

## Summary: Patterns Demonstrated

| Case | Phase Skip | Retry | NEST | DEFER | ABORT | DECOMPOSE | Iteration |
|------|------------|-------|------|-------|-------|-----------|-----------|
| 1    | Yes        | -     | -    | -     | -     | -         | -         |
| 2    | -          | Yes   | -    | -     | -     | -         | -         |
| 3    | -          | -     | -    | -     | -     | -         | -         |
| 4    | -          | -     | -    | -     | -     | -         | -         |
| 5    | -          | Yes   | -    | -     | -     | -         | -         |
| 6    | -          | Yes   | Yes  | -     | -     | -         | -         |
| 7    | -          | Yes   | -    | -     | Yes   | -         | -         |
| 8    | -          | Yes   | -    | -     | -     | Yes       | -         |
| 9    | -          | -     | -    | Yes   | -     | -         | -         |
| 10   | -          | Yes   | -    | -     | -     | -         | Yes       |

## Document History

**[2026-01-17 16:46]**
- Changed: Notation refinements across all 10 cases based on user feedback:
  - Removed explicit `-OK` (success is now implicit)
  - Changed snake_case to natural spacing in parameters
  - Simplified gates from `Gate: FROM->TO` to `Gate:`
  - Changed `NEST(SOLVE:...)` to `[SOLVE](...)`
  - Changed `[ASSESS] -> VALUE` to `[ASSESS](VALUE)`
  - Added explicit `-FAIL` transitions per EDIRD verb outcome rules
  - Added `-SKIPPED` outcome for intentional bypasses
- Changed: Notation Reference updated with new conventions

**[2026-01-17 16:23]**
- Added: Expanded Notation Reference with gate failure behavior, retry semantics
- Added: Advanced patterns section (NEST, NEST-FAIL, DEFER, ABORT, DECOMPOSE, named cycles)
- Added: NEST-FAIL handler to Case 6

**[2026-01-17 16:16]**
- Added: DevSystem tag for table usage
- Added: Timeline field
- Added: Summary section with key findings

**[2026-01-17 16:15]**
- Initial document created
- All 10 test cases formalized in STRUT notation
- Gates included for all phase transitions
- Repetition notation used where applicable
- All escalation patterns demonstrated (CONSULT, DEFER, ABORT, DECOMPOSE)
