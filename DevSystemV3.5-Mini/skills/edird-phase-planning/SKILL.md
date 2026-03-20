---
name: edird-phase-planning
description: Apply when doing planning for long-running tasks in sessions on top level
---

# EDIRD Phase Planning

## When to Invoke

- `/build` or `/solve` workflows
- [PLAN] - creating high-level plans to achieve goals
- Planning for long agentic runs for features, fixes, or research

NOT for document writing - Use `/write-spec`, `/write-impl-plan`, `/write-test-plan`, `/write-tasks-plan` instead.

## MUST-NOT-FORGET

- `/build` and `/solve` are the entry workflows
- Use `/write-spec`, `/write-impl-plan`, `/write-test-plan`, `/write-tasks-plan` for documents
- Check gates before phase transitions

## Quick Reference

Phases: EXPLORE → DESIGN → IMPLEMENT → REFINE → DELIVER

Workflow types: BUILD (code output) | SOLVE (knowledge/decision output)

Assessment: COMPLEXITY-LOW/MEDIUM/HIGH | PROBLEM-TYPE (RESEARCH/ANALYSIS/EVALUATION/WRITING/DECISION)

## Phase Gates

### EXPLORE → DESIGN
- [ ] Problem/goal clearly understood
- [ ] Workflow type determined (BUILD or SOLVE)
- [ ] Assessment complete (BUILD: COMPLEXITY | SOLVE: PROBLEM-TYPE)
- [ ] Scope boundaries defined
- [ ] No blocking unknowns requiring [ACTOR] input

### DESIGN → IMPLEMENT
- [ ] Approach documented (outline, spec, or plan)
- [ ] Risky parts proven via POC (if COMPLEXITY-MEDIUM+)
- [ ] No open questions requiring [ACTOR] decision
- [ ] For BUILD: SPEC, IMPL, TEST documents created
- [ ] For BUILD: TASKS document created via [PARTITION]
- [ ] For SOLVE: Structure/criteria validated

### IMPLEMENT → REFINE
- [ ] Core work complete (code written / document drafted)
- [ ] For BUILD: Tests pass, no TODO/FIXME left
- [ ] For SOLVE: All sections drafted
- [ ] Progress committed/saved

### REFINE → DELIVER
- [ ] Self-review complete
- [ ] Verification against spec/rules passed
- [ ] For BUILD COMPLEXITY-MEDIUM+: Critique and reconcile complete
- [ ] For SOLVE: Claims verified, arguments strengthened
- [ ] All found issues fixed

## Workflow Examples

### BUILD (COMPLEXITY-HIGH)
```
[EXPLORE] → [RESEARCH] → [ANALYZE] → [ASSESS] → [SCOPE] → Gate
[DESIGN]  → [PLAN] → [WRITE-SPEC] → [WRITE-IMPL-PLAN] → [PROVE] → [PARTITION] → Gate
[IMPLEMENT] → [IMPLEMENT] → [TEST] → [FIX] → [COMMIT] → Gate (loop until green)
[REFINE] → [REVIEW] → [VERIFY] → [CRITIQUE] → [RECONCILE] → Gate
[DELIVER] → [VALIDATE] → [MERGE] → [CLOSE] → [ARCHIVE]
```

### SOLVE (EVALUATION)
```
[EXPLORE] → [RESEARCH] → [ANALYZE] → [ASSESS] → EVALUATION → Gate
[DESIGN]  → [FRAME] → [OUTLINE] criteria → [DEFINE] framework → Gate
[IMPLEMENT] → [RESEARCH] options → [EVALUATE] → [SYNTHESIZE] → Gate
[REFINE] → [CRITIQUE] → [VERIFY] claims → [IMPROVE] → Gate
[DELIVER] → [CONCLUDE] → [RECOMMEND] → [VALIDATE] → [ARCHIVE]
```

Note: COMPLEXITY-LOW skips [PROVE], [CRITIQUE], [RECONCILE].

## Phase Plan Requirements

Plans via [PLAN] must define:
- Objectives - What success looks like
- Strategy - How to achieve objectives
- Deliverables - Concrete outputs with checkboxes
- Transitions - When to move to next phase

Planning Horizon: Plan EXPLORE, DESIGN, DELIVER now. IMPLEMENT after DESIGN gate. REFINE after IMPLEMENT gate.

## How to Plan Well

Goal Decomposition: Start with outcome → identify dependencies → find parallel opportunities → size steps for testability.

Scope Calibration:
- Too big: >30min AWT or >3 files → decompose
- Too small: <2min AWT → combine
- Right size: verifiable outcome, clear done criteria, single responsibility

Dependency Mapping - per step ask: What inputs needed? What outputs produced? Can this run concurrently?

Common Mistakes: Vague objectives → define specific criteria. Missing dependencies → explicit `← Px-Sy`. Over-sequencing → parallelize. No AWT estimates → add time budget. No verification step → add [TEST]/[VERIFY].

## Next Action Logic

1. Check phase gate → Pass? → Next phase, first verb
2. Gate fails? → Execute verb addressing unchecked item
3. Verb outcome: -OK → next | -FAIL → handle | -SKIP → next
4. No more verbs? → Re-evaluate gate
5. [DELIVER] done? → [CLOSE] and [ARCHIVE] if session-based

Failure handlers: -FAIL on [RESEARCH]/[ASSESS]/[PLAN] → [CONSULT] or more [RESEARCH]. -FAIL on [TEST]/[VERIFY] → [FIX] → retry.

## Effort Allocation

Time Units: AWT (Agentic Work Time) - agent processing, excludes user wait. HHW (Human-Hour Work) - human equivalent for sizing.

Phase Budgets (AWT): EXPLORE: 5/15/30min. DESIGN: 5/30/60min. IMPLEMENT: varies. REFINE: 5/15/30min. DELIVER: 2/5/10min (LOW/MEDIUM/HIGH).

Diminishing Returns: Phase at 2x budget without progress → [CONSULT]. Step retried 3x without improvement → [CONSULT]. Research yields nothing after 3 sources → move on.

Retry Limits: COMPLEXITY-LOW: infinite. COMPLEXITY-MEDIUM/HIGH: max 5 per phase, then [CONSULT].

## Mandatory Gate Output

```markdown
## Gate: [CURRENT_PHASE] → [NEXT_PHASE]

Complexity: [LOW/MEDIUM/HIGH] | Artifacts: [list created docs]

- [x] Item - Evidence: [specific evidence]
- [ ] Item - BLOCKED: [what's missing]

Gate status: PASS | FAIL
```