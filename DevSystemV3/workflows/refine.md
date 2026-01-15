---
description: REFINE phase - improve quality through review
phase: REFINE
---

# Refine Workflow

## Required Skills

- @edird-phase-model for gate details

## Phase: REFINE

**Entry gate:** IMPLEMENT→REFINE passed

### Verb Sequence

1. [REVIEW] self-review of work
2. [VERIFY] against spec/rules
3. [TEST] regression testing
4. [CRITIQUE] find problems (devil's advocate) - for COMPLEXITY-HIGH
5. [RECONCILE] bridge ideal vs practical - for COMPLEXITY-HIGH
6. [FIX] found issues
7. [IMPROVE] clarity and quality

### For COMPLEXITY-LOW

- [REVIEW] and [FIX] only
- Skip [CRITIQUE] and [RECONCILE]

### For COMPLEXITY-HIGH

- Run `/critique` for [CRITIQUE]
- Run `/reconcile` for [RECONCILE]

### Gate Check: REFINE→DELIVER

- [ ] Self-review complete
- [ ] Verification against spec/rules passed
- [ ] For BUILD COMPLEXITY-HIGH: Critique and reconcile complete
- [ ] For SOLVE: Claims verified, arguments strengthened
- [ ] All found issues fixed

**Pass**: Run `/deliver` | **Fail**: Continue [REFINE]

## Output

Update NOTES.md with current phase. Document any issues found in PROBLEMS.md.
