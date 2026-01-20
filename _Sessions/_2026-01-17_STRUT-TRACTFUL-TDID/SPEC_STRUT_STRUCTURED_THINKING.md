# SPEC: STRUT (Structured Thinking)

**Doc ID (TDID)**: STRUT-SP01
**Goal**: Define STRUT tree notation for planning and tracking autonomous agent work
**Timeline**: Created 2026-01-19

**Depends on:**
- `SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP01]` for verb definitions

## MUST-NOT-FORGET

- STRUT is a pure tree notation using box-drawing characters
- Every phase, step, deliverable has unique ID: `P1`, `P1-S1`, `P1-D1`
- Tree nodes: Objectives, Strategy, Steps (verbs), Deliverables, Transitions
- Steps use AGEN verbs: `[ ] P1-S1 [VERB](params)`
- Checkbox states: `[ ]` pending, `[x]` done, `[N]` done N times
- Strategy can include AWT (Agentic Work Time) estimates
- Transitions define flow control at phase end

## 1. Scenario

**Problem:** Agents need to plan work, track progress, enable resume/handoff.

**Solution:** Pure tree notation with unique IDs and five node types.

## 2. Functional Requirements

**STRUT-FR-01: Unique IDs**
- Phase ID: `P1`, `P2`, `P3`...
- Step ID: `P1-S1`, `P1-S2`, `P2-S1`...
- Deliverable ID: `P1-D1`, `P1-D2`, `P2-D1`...
- IDs are unique within a STRUT plan

**STRUT-FR-02: Phase Structure**
- Header: `P1 [PHASE-NAME]: Description`
- Children in order: Objectives, Strategy, Steps, Deliverables, Transitions
- Phase complete when Transition condition met

**STRUT-FR-03: Step Format**
- Format: `[ ] P1-S1 [VERB](params)`
- Steps use AGEN verbs
- Steps are a flat list with checkboxes

**STRUT-FR-04: Checkbox States**
- `[ ]` - Not done (pending)
- `[x]` - Done (completed once)
- `[N]` - Done N times (e.g., `[2]` = executed twice, for loops/retries)

**STRUT-FR-05: Objectives**
- Format: `[ ] Goal description` (no IDs, uses checkbox states)

**STRUT-FR-06: Strategy**
- Free text, may include AWT estimates

**STRUT-FR-07: Deliverables**
- Format: `[ ] P1-D1: Description` (uses checkbox states)

**STRUT-FR-08: Transitions**
- Format: `- Condition → Target`
- Targets: `[PHASE-NAME]`, `[CONSULT]`, `[END]`

## 3. Notation Reference

### Phase Template

```
[ ] P1 [PHASE-NAME]: Description
├─ Objectives:
│   ├─ [ ] Goal 1
│   └─ [ ] Goal 2
├─ Strategy: Approach description
│   - Sub-item if needed
├─ [ ] P1-S1 [VERB](params)
├─ [ ] P1-S2 [VERB](params)
├─ [ ] P1-S3 [VERB](params)
├─ Deliverables:
│   ├─ [ ] P1-D1: Outcome 1
│   └─ [ ] P1-D2: Outcome 2
└─> Transitions:
    - P1-D1, P1-D2 checked → [NEXT-PHASE]
    - Otherwise → P1-S2
```

## 4. Examples

### Example 1: Simple Hotfix

```
[ ] P1 [IMPLEMENT]: Fix and verify
├─ Objectives:
│   └─ [ ] Bug no longer reproduces
├─ Strategy: Locate bug, apply minimal fix, test, commit
├─ [ ] P1-S1 [ANALYZE](stack trace)
├─ [ ] P1-S2 [IMPLEMENT](null check fix)
├─ [ ] P1-S3 [TEST]
├─ [ ] P1-S4 [FIX](if tests fail)
├─ [ ] P1-S5 [COMMIT]("fix: null check in getUserById")
├─ Deliverables:
│   ├─ [ ] P1-D1: Root cause identified
│   ├─ [ ] P1-D2: Fix implemented
│   ├─ [ ] P1-D3: Tests pass
│   └─ [ ] P1-D4: Committed
└─> Transitions:
    - P1-D1 - P1-D4 checked → [END]
    - Tests fail after 3 attempts → [CONSULT]
```

### Example 2: Feature Build (Multi-Phase)

```
[ ] P1 [EXPLORE]: Understand requirements
├─ Objectives:
│   ├─ [ ] Know what to build
│   ├─ [ ] Correct API documentation researched
│   ├─ [ ] Assess complexity
│   └─ [ ] Create [DESIGN] phase STRUT
├─ Strategy: Ready for design in 5min AWT (agent work time)
│   - Read all project documents first
├─ [ ] P1-S1 [GATHER](requirements from ticket AUTH-123)
├─ [ ] P1-S2 [ANALYZE](existing auth module)
├─ [ ] P1-S3 [RESEARCH](JWT library version) → [VERIFY]
├─ [ ] P1-S4 [ASSESS](complexity of feature)
├─ [ ] P1-S5 [PROPOSE](3 design options)
├─ [ ] P1-S6 [PLAN](next phase STRUT)
├─ Deliverables:
│   ├─ [ ] P1-D1: Workflow = BUILD
│   ├─ [ ] P1-D2: Complexity = MEDIUM
│   ├─ [ ] P1-D3: P1-S3 outout = API version verified with examples
│   ├─ [ ] P1-D4: Requirements list (5+ items)
│   └─ [ ] P1-D5: Next phase STRUT created
└─> Transitions:
    - P1-D1 - P1-D5 checked → P2 [DESIGN]
    - Otherwise → P1-S2

[ ] P2 [DESIGN]: Plan implementation
├─ Objectives:
│   ├─ [ ] Architecture decided (from 2+ options)
│   └─ [ ] SPEC, IMPL, TEST ready
├─ Strategy: TBD based on P1 findings
├─ [ ] P2-S1 [PLAN](token-based password reset)
├─ [ ] P2-S2 [WRITE-SPEC](_SPEC_PASSWORD_RESET.md) → [VERIFY] → [REVIEW] → [VERIFY]
├─ [ ] P2-S3 [WRITE-IMPL-PLAN](_IMPL_PASSWORD_RESET.md) → [VERIFY] → [REVIEW] → [CROSSCHECK] → [VERIFY]
├─ [ ] P2-S4 [WRITE-TEST-PLAN](_TEST_PASSWORD_RESET.md) → [VERIFY]
├─ [ ] P2-S5 [PLAN](next phase STRUT) → [VERIFY]
├─ [ ] P2-S6 [REVIEW](Phase documents: SPEC, IMPL, TEST) 
├─ Deliverables:
│   ├─ [ ] P2-D1: Architecture = token-based, 24h expiry
│   ├─ [ ] P2-D2: SPEC created, verified, reviewed
│   ├─ [ ] P2-D3: IMPL plan created, verified, reviewed
│   ├─ [ ] P2-D4: P2-S6 [REVIEW] yielded no critical findings 
│   └─ [ ] P2-D5: Next phase STRUT created, verified
└─> Transitions:
    - P2-D1 - P2-D4 checked → P3 [IMPLEMENT]
    - Otherwise: → P2-S1 [PLAN](fix P2-S6 critical findings)

[ ] P3 [IMPLEMENT]: Build feature
├─ Objectives:
│   ├─ [ ] Feature working
│   └─ [ ] Tests passing
├─ Strategy: Implement per IMPL plan, test-fix loop
├─ [ ] P3-S1 [IMPLEMENT](ResetToken model)
├─ [ ] P3-S2 [IMPLEMENT](/forgot-password endpoint)
├─ [ ] P3-S3 [IMPLEMENT](/reset-password endpoint)
├─ [ ] P3-S4 [TEST]
├─ [ ] P3-S5 [FIX](if tests fail)
├─ [ ] P3-S6 [COMMIT]("feat(auth): add password reset")
├─ Deliverables:
│   ├─ [ ] P3-D1: ResetToken model
│   ├─ [ ] P3-D2: /forgot-password endpoint
│   ├─ [ ] P3-D3: /reset-password endpoint
│   ├─ [ ] P3-D4: Tests pass
│   └─ [ ] P3-D5: Committed
└─> Transitions:
    - P3-D1 - P3-D5 checked → P4 [REFINE]
    - Tests fail after 5 attempts → [CONSULT]

[ ] P4 [REFINE]: Review
├─ Objectives:
│   └─ [ ] Code matches SPEC
├─ Strategy: Verify, test integration
├─ [ ] P4-S1 [VERIFY](code matches SPEC)
├─ [ ] P4-S2 [TEST](integration)
├─ Deliverables:
│   ├─ [ ] P4-D1: SPEC satisfied
│   └─ [ ] P4-D2: Integration tests pass
└─> Transitions:
    - P4-D1, P4-D2 checked → [DELIVER]

[ ] P5 [DELIVER]: Complete
├─ Objectives:
│   └─ [ ] Feature delivered
├─ Strategy: Validate, close ticket
├─ [ ] P5-S1 [VALIDATE](manual test)
├─ [ ] P5-S2 [CLOSE](ticket AUTH-123)
├─ Deliverables:
│   ├─ [ ] P5-D1: Manual test passed
│   └─ [ ] P5-D2: Ticket closed
└─> Transitions:
    - P5-D1, P5-D2 checked → [END]
```

### Example 3: Research Task

```
[ ] P1 [EXPLORE]: Research OAuth providers
├─ Objectives:
│   ├─ [ ] Understand OAuth landscape
│   └─ [ ] Make recommendation
├─ Strategy: Gather providers, research, define criteria, evaluate, recommend
├─ [ ] P1-S1 [GATHER](provider list)
├─ [ ] P1-S2 [RESEARCH](Auth0, Okta, Firebase, Cognito)
├─ [ ] P1-S3 [DEFINE](criteria: price, docs, SDKs)
├─ [ ] P1-S4 [EVALUATE](each provider against criteria)
├─ [ ] P1-S5 [RECOMMEND](Auth0)
├─ Deliverables:
│   ├─ [ ] P1-D1: 5 providers identified
│   ├─ [ ] P1-D2: Criteria defined
│   ├─ [ ] P1-D3: Comparison complete
│   └─ [ ] P1-D4: Recommendation = Auth0
└─> Transitions:
    - P1-D1 - P1-D4 checked → [DESIGN]

[ ] P2 [DESIGN]: Document decision
├─ Objectives:
│   └─ [ ] Decision documented
├─ Strategy: Write INFO document
├─ [ ] P2-S1 [WRITE-INFO](_INFO_OAUTH_EVALUATION.md)
├─ Deliverables:
│   └─ [ ] P2-D1: INFO document created
└─> Transitions:
    - P2-D1 checked → [END]
```

## 5. Usage

**Creating:** Phase header → Objectives → Strategy → Steps → Deliverables → Transitions

**Executing:** Start at P1-S1, execute steps, check Deliverables, follow Transitions until `[END]`

**Resuming:** Find first unchecked Deliverable, read Strategy, continue

## Document History

**[2026-01-20 10:42]**
- Added: STRUT-FR-04 Checkbox States with `[ ]`, `[x]`, `[N]` for repeat count
- Changed: All examples updated with checkboxes on phases and steps
- Changed: Renumbered FR-05 through FR-08

**[2026-01-20 10:41]**
- Fixed: Cross-reference from [AGEN-SP02] to [AGEN-SP01]

**[2026-01-19 09:35]**
- Minimized spec: removed DD, IG, redundant sections
- Steps are flat list

**[2026-01-19 08:30]**
- Initial specification created
