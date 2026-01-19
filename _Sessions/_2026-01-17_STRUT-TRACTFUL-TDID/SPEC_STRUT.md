# SPEC: STRUT (Structured Thinking)

**Doc ID (TDID)**: STRUT-SP01
**Goal**: Define STRUT tree notation for planning and tracking autonomous agent work
**Timeline**: Created 2026-01-19

**Depends on:**
- `SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP02]` for verb definitions

## MUST-NOT-FORGET

- STRUT is a pure tree notation using box-drawing characters
- Every phase, step, deliverable has unique ID: `P1`, `P1-S1`, `P1-D1`
- Tree nodes: Objectives, Strategy, Steps (verbs), Deliverables, Transitions
- Steps use AGEN verbs: `P1-S1 [VERB](params)`
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
- Format: `P1-S1 [VERB](params)`
- Steps use AGEN verbs
- Steps are a flat list

**STRUT-FR-04: Objectives**
- Format: `[ ] Goal description` (no IDs)

**STRUT-FR-05: Strategy**
- Free text, may include AWT estimates

**STRUT-FR-06: Deliverables**
- Format: `[ ] P1-D1: Description`

**STRUT-FR-07: Transitions**
- Format: `- Condition → Target`
- Targets: `[PHASE-NAME]`, `[CONSULT]`, `[END]`

## 3. Notation Reference

### Phase Template

```
P1 [PHASE-NAME]: Description
├─ Objectives:
│   ├─ [ ] Goal 1
│   └─ [ ] Goal 2
├─ Strategy: Approach description
│   - Sub-item if needed
├─ P1-S1 [VERB](params)
├─ P1-S2 [VERB](params)
├─ P1-S3 [VERB](params)
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
P1 [IMPLEMENT]: Fix and verify
├─ Objectives:
│   └─ [ ] Bug no longer reproduces
├─ Strategy: Locate bug, apply minimal fix, test, commit
├─ P1-S1 [ANALYZE](stack trace)
├─ P1-S2 [IMPLEMENT](null check fix)
├─ P1-S3 [TEST]
├─ P1-S4 [FIX](if tests fail)
├─ P1-S5 [COMMIT]("fix: null check in getUserById")
├─ Deliverables:
│   ├─ [x] P1-D1: Root cause identified
│   ├─ [x] P1-D2: Fix implemented
│   ├─ [x] P1-D3: Tests pass
│   └─ [x] P1-D4: Committed
└─> Transitions:
    - P1-D1 - P1-D4 checked → [END]
    - Tests fail after 3 attempts → [CONSULT]
```

### Example 2: Feature Build (Multi-Phase)

```
P1 [EXPLORE]: Understand requirements
├─ Objectives:
│   ├─ [ ] Know what to build
│   ├─ [ ] Correct API documentation researched
│   ├─ [ ] Assess complexity
│   └─ [ ] Create [DESIGN] phase STRUT
├─ Strategy: Ready for design in 5min AWT
│   - Read all project documents first
├─ P1-S1 [GATHER](requirements from ticket AUTH-123)
├─ P1-S2 [ANALYZE](existing auth module)
├─ P1-S3 [RESEARCH](JWT library version)
├─ P1-S4 [ASSESS](complexity of feature)
├─ P1-S5 [BRAINSTORM](3 design options)
├─ Deliverables:
│   ├─ [ ] P1-D1: Workflow = BUILD
│   ├─ [ ] P1-D2: Complexity = MEDIUM
│   ├─ [ ] P1-D3: API version verified with examples
│   ├─ [ ] P1-D4: Requirements list (5+ items)
│   └─ [ ] P1-D5: Next phase STRUT created
└─> Transitions:
    - P1-D1 - P1-D5 checked → [DESIGN]
    - Otherwise → P1-S2

P2 [DESIGN]: Plan implementation
├─ Objectives:
│   ├─ [ ] Architecture decided (from 2+ options)
│   └─ [ ] SPEC, IMPL, TEST ready
├─ Strategy: TBD based on P1 findings
├─ P2-S1 [PLAN](token-based password reset)
├─ P2-S2 [WRITE-SPEC](_SPEC_PASSWORD_RESET.md)
├─ P2-S3 [WRITE-IMPL-PLAN](_IMPL_PASSWORD_RESET.md)
├─ P2-S4 [WRITE-TEST-PLAN](_TEST_PASSWORD_RESET.md)
├─ Deliverables:
│   ├─ [ ] P2-D1: Architecture = token-based, 24h expiry
│   ├─ [ ] P2-D2: SPEC created and verified
│   └─ [ ] P2-D3: IMPL plan created
└─> Transitions:
    - P2-D1 - P2-D3 checked → [IMPLEMENT]

P3 [IMPLEMENT]: Build feature
├─ Objectives:
│   ├─ [ ] Feature working
│   └─ [ ] Tests passing
├─ Strategy: Implement per IMPL plan, test-fix loop
├─ P3-S1 [IMPLEMENT](ResetToken model)
├─ P3-S2 [IMPLEMENT](/forgot-password endpoint)
├─ P3-S3 [IMPLEMENT](/reset-password endpoint)
├─ P3-S4 [TEST]
├─ P3-S5 [FIX](if tests fail)
├─ P3-S6 [COMMIT]("feat(auth): add password reset")
├─ Deliverables:
│   ├─ [ ] P3-D1: ResetToken model
│   ├─ [ ] P3-D2: /forgot-password endpoint
│   ├─ [ ] P3-D3: /reset-password endpoint
│   ├─ [ ] P3-D4: Tests pass
│   └─ [ ] P3-D5: Committed
└─> Transitions:
    - P3-D1 - P3-D5 checked → [REFINE]
    - Tests fail after 5 attempts → [CONSULT]

P4 [REFINE]: Review
├─ Objectives:
│   └─ [ ] Code matches SPEC
├─ Strategy: Verify, test integration
├─ P4-S1 [VERIFY](code matches SPEC)
├─ P4-S2 [TEST](integration)
├─ Deliverables:
│   ├─ [ ] P4-D1: SPEC satisfied
│   └─ [ ] P4-D2: Integration tests pass
└─> Transitions:
    - P4-D1, P4-D2 checked → [DELIVER]

P5 [DELIVER]: Complete
├─ Objectives:
│   └─ [ ] Feature delivered
├─ Strategy: Validate, close ticket
├─ P5-S1 [VALIDATE](manual test)
├─ P5-S2 [CLOSE](ticket AUTH-123)
├─ Deliverables:
│   ├─ [ ] P5-D1: Manual test passed
│   └─ [ ] P5-D2: Ticket closed
└─> Transitions:
    - P5-D1, P5-D2 checked → [END]
```

### Example 3: Research Task

```
P1 [EXPLORE]: Research OAuth providers
├─ Objectives:
│   ├─ [ ] Understand OAuth landscape
│   └─ [ ] Make recommendation
├─ Strategy: Gather providers, research, define criteria, evaluate, recommend
├─ P1-S1 [GATHER](provider list)
├─ P1-S2 [RESEARCH](Auth0, Okta, Firebase, Cognito)
├─ P1-S3 [DEFINE](criteria: price, docs, SDKs)
├─ P1-S4 [EVALUATE](each provider against criteria)
├─ P1-S5 [RECOMMEND](Auth0)
├─ Deliverables:
│   ├─ [ ] P1-D1: 5 providers identified
│   ├─ [ ] P1-D2: Criteria defined
│   ├─ [ ] P1-D3: Comparison complete
│   └─ [ ] P1-D4: Recommendation = Auth0
└─> Transitions:
    - P1-D1 - P1-D4 checked → [DESIGN]

P2 [DESIGN]: Document decision
├─ Objectives:
│   └─ [ ] Decision documented
├─ Strategy: Write INFO document
├─ P2-S1 [WRITE-INFO](_INFO_OAUTH_EVALUATION.md)
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

**[2026-01-19 09:35]**
- Minimized spec: removed DD, IG, redundant sections
- Simplified checkbox states to `[ ]` and `[x]` only
- Steps are flat list

**[2026-01-19 08:30]**
- Initial specification created
