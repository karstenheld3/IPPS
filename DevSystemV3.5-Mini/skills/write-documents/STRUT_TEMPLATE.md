# STRUT Template

Source: `docs/specs/SPEC_STRUT_STRUCTURED_THINKING.md [STRUT-SP01]`

Embed in: PROGRESS.md, IMPL documents, TASKS documents, NOTES.md, or any document needing structured planning with progress tracking.

## Core Rules

- Every phase, step, deliverable has unique ID: `P1`, `P1-S1`, `P1-D1`
- Steps use AGEN verbs: `[ ] P1-S1 [VERB](params)`
- Checkbox states: `[ ]` pending, `[x]` done, `[N]` done N times (retry count)
- Objectives link to Deliverables: `[ ] Goal ← P1-D1, P1-D2`
- Use box-drawing characters: `├─` `└─` `│` `└─>`
- IDs are unique within a STRUT plan (ephemeral, session-scoped)
- Verify STRUT plans via /verify workflow (Planning + Transition contexts)

## Phase Template

```
[ ] P1 [PHASE-NAME]: Description
├─ Objectives:
│   ├─ [ ] Goal 1 ← P1-D1, P1-D2
│   └─ [ ] Goal 2 ← P1-D3
├─ Strategy: Approach description (may include AWT estimate)
│   - Model: Claude Opus for analysis and implementation, Sonnet for fixes, Haiku for chores
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

## ID Formats

- Phase ID: `P1`, `P2`, `P3`...
- Step ID: `P1-S1`, `P1-S2`, `P2-S1`...
- Deliverable ID: `P1-D1`, `P1-D2`, `P2-D1`...

## Node Types

1. Objectives - Success criteria linked to Deliverables (`← P1-Dx`), checkboxes, no IDs
2. Strategy - Approach summary, may include AWT estimates and model hints
3. Steps - Actions using AGEN verbs (flat list with checkboxes and IDs)
4. Deliverables - Expected outputs (checkboxes with IDs)
5. Transitions - Flow control conditions at phase end

## Model Hints

Strategy sections may include model hints for auto model switching. Model definitions in `!NOTES.md` under `## Cascade Model Switching`. Hints are recommendations - agent decides based on actual task.

## Checkbox States

- `[ ]` - Not done (pending)
- `[x]` - Done (completed once)
- `[N]` - Done N times (e.g., `[2]` = executed twice, for loops/retries)

## Transition Targets

- `[PHASE-NAME]` - Next phase (e.g., `[DESIGN]`, `[IMPLEMENT]`)
- `[CONSULT]` - Escalate to [ACTOR]
- `[END]` - Plan complete

## Concurrent Blocks

Group parallel steps under a `Concurrent:` virtual step.

### Syntax

```
├─ [ ] P1-S1 [VERB](params)
├─ Concurrent: <strategy explaining why parallel>
│   ├─ [ ] P1-S2 [VERB](params)
│   ├─ [ ] P1-S3 [VERB](params)
│   └─ [ ] P1-S4 [VERB](params)
├─ [ ] P1-S5 [VERB](params)          ← implicit barrier, waits for S2-S4
```

### Rules

- `Concurrent: <strategy>` - Virtual step (no checkbox) describing parallel group
- Steps inside run concurrently
- First step after Concurrent block is implicit barrier (waits for all)
- Concurrent blocks can nest (discouraged beyond 1 level)

### Step Dependencies

Use `← Px-Sy` suffix for explicit dependencies.

- `← P1-S2` - Wait only for S2
- `← P1-S2, P1-S3` - Wait for S2 AND S3
- No arrow after Concurrent block = wait for ALL steps in block
- No arrow within Concurrent block = no dependencies (truly parallel)

```
[ ] P1 [IMPLEMENT]: Build auth system
├─ [ ] P1-S1 [IMPLEMENT](User model)
├─ Concurrent: Independent services, build in parallel
│   ├─ [ ] P1-S2 [IMPLEMENT](password hashing)
│   ├─ [ ] P1-S3 [IMPLEMENT](JWT tokens) ← P1-S2
│   └─ [ ] P1-S4 [IMPLEMENT](email service)
├─ [ ] P1-S5 [IMPLEMENT](login endpoint) ← P1-S2, P1-S3
├─ [ ] P1-S6 [IMPLEMENT](register endpoint) ← P1-S4, P1-S5
├─ [ ] P1-S7 [TEST]
```

## Example: Simple Hotfix

```
[ ] P1 [IMPLEMENT]: Fix and verify
├─ Objectives:
│   └─ [ ] Bug no longer reproduces ← P1-D2, P1-D3
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

## Example: Multi-Phase Feature

```
[ ] P1 [EXPLORE]: Understand requirements
├─ Objectives:
│   ├─ [ ] Know what to build ← P1-D3
│   └─ [ ] Assess complexity ← P1-D1, P1-D2
├─ Strategy: Ready for design in 5min AWT
├─ [ ] P1-S1 [GATHER](requirements from ticket)
├─ [ ] P1-S2 [ANALYZE](existing code)
├─ [ ] P1-S3 [ASSESS](complexity)
├─ Deliverables:
│   ├─ [ ] P1-D1: Workflow = BUILD
│   ├─ [ ] P1-D2: Complexity determined
│   └─ [ ] P1-D3: Requirements list
└─> Transitions:
    - P1-D1 - P1-D3 checked → P2 [DESIGN]

[ ] P2 [DESIGN]: Plan implementation
├─ Objectives:
│   └─ [ ] SPEC, IMPL, TEST ready ← P2-D1, P2-D2, P2-D3
├─ Strategy: TBD based on P1 findings
├─ [ ] P2-S1 [WRITE-SPEC]
├─ [ ] P2-S2 [WRITE-IMPL-PLAN]
├─ [ ] P2-S3 [WRITE-TEST-PLAN]
├─ Deliverables:
│   ├─ [ ] P2-D1: SPEC created
│   ├─ [ ] P2-D2: IMPL plan created
│   └─ [ ] P2-D3: TEST plan created
└─> Transitions:
    - P2-D1 - P2-D3 checked → P3 [IMPLEMENT]
```

## Usage

Creating: Phase header → Objectives → Strategy → Steps → Deliverables → Transitions

Executing: Start at P1-S1, execute steps, check Deliverables, follow Transitions until `[END]`

Resuming: Find first unchecked Deliverable, read Strategy, continue

## Embedding in Documents

1. Add under a section heading (e.g., `## Plan`, `## Phase Plan`)
2. Maintain existing document structure
3. STRUT IDs are local to the plan (not TDID system)