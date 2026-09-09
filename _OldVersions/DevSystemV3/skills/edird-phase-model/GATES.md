# Phase Gates

Gates are checklists that must pass before transitioning. Agent evaluates gates automatically.

## EXPLORE → DESIGN

- [ ] Problem or goal clearly understood
- [ ] Workflow type determined (BUILD or SOLVE)
- [ ] Assessment complete (BUILD: COMPLEXITY | SOLVE: PROBLEM-TYPE)
- [ ] Scope boundaries defined
- [ ] No blocking unknowns requiring [ACTOR] input

**Pass**: proceed to [DESIGN] | **Fail**: remain in [EXPLORE]

## DESIGN → IMPLEMENT

- [ ] Approach documented (outline, spec, or plan)
- [ ] Risky parts proven via POC (if COMPLEXITY-MEDIUM or higher)
- [ ] No open questions requiring [ACTOR] decision
- [ ] For BUILD: SPEC, IMPL, TEST documents created
- [ ] For BUILD: Plan decomposed into small testable steps
- [ ] For SOLVE: Structure/criteria validated

**Pass**: proceed to [IMPLEMENT] | **Fail**: remain in [DESIGN]

## IMPLEMENT → REFINE

- [ ] Core work complete (code written / document drafted)
- [ ] For BUILD: Tests pass
- [ ] For BUILD: No TODO/FIXME left unaddressed
- [ ] For SOLVE: All sections drafted
- [ ] Progress committed/saved

**Pass**: proceed to [REFINE] | **Fail**: remain in [IMPLEMENT]

## REFINE → DELIVER

- [ ] Self-review complete
- [ ] Verification against spec/rules passed
- [ ] For BUILD COMPLEXITY-MEDIUM or higher: Critique and reconcile complete
- [ ] For SOLVE: Claims verified, arguments strengthened
- [ ] All found issues fixed

**Pass**: proceed to [DELIVER] | **Fail**: remain in [REFINE]

## Gate Evaluation

After completing verbs in a phase:
1. Check each gate item
2. If all checked → transition to next phase
3. If unchecked items → execute verb that addresses first unchecked item
4. Re-evaluate after each verb completion

## Mandatory Gate Output (REQUIRED)

Before proceeding to next phase, agent MUST output this block:

```markdown
---
## Gate: [CURRENT_PHASE] → [NEXT_PHASE]

**Complexity**: [LOW/MEDIUM/HIGH] | **Triggers**: [list or "none"]

**Checklist**:
- [x] Item - Evidence: [specific evidence]
- [ ] Item - BLOCKED: [what's missing]

**Artifacts**:
- INFO: [filename] | NOT REQUIRED | MISSING
- SPEC: [filename] | NOT REQUIRED | MISSING
- IMPL: [filename] | NOT REQUIRED | MISSING
- TEST: [filename] | NOT REQUIRED | MISSING

**Gate status**: PASS | FAIL
---
```

Gate CANNOT pass if:
- Required artifacts are MISSING (based on complexity/triggers)
- Research triggers detected but no sources cited
- Any checklist item unchecked without justification
