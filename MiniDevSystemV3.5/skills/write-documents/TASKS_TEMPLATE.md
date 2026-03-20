# TASKS Template

## Header Block

```markdown
# TASKS: [TOPIC] Tasks Plan

**Doc ID (TDID)**: [TOPIC]-TK01
**Feature**: [FEATURE_SLUG]
**Goal**: Partitioned tasks for [TOPIC] implementation
**Source**: `IMPL_[TOPIC].md [TOPIC-IP01]`, `TEST_[TOPIC].md [TOPIC-TP01]`
**Strategy**: PARTITION-[STRATEGY]
```

## Task Overview Section

```markdown
## Task Overview

- Total tasks: N
- Estimated total: X HHW
- Parallelizable: M tasks
```

## Task 0 - Baseline (MANDATORY)

```markdown
## Task 0 - Baseline (MANDATORY)

Run before starting any implementation:
- [ ] Run existing tests, record pass/fail baseline
- [ ] Note pre-existing failures (not caused by this feature)
```

## Task Item Structure

```markdown
- [ ] **[TOPIC]-TK-001** - Description
  - Files: [files affected]
  - Done when: [specific completion criteria]
  - Verify: [commands to run]
  - Guardrails: [must not change X]
  - Depends: none | TK-NNN
  - Parallel: [P] or blank
  - Model: Sonnet | Opus | Haiku
  - Est: 0.5 HHW
```

**Required:** Task ID + description, Files, Done when, Est
**Optional:** Verify, Guardrails, Depends, Parallel, Model

Model hints are recommendations from `!NOTES.md` `## Cascade Model Switching` - agent decides based on actual task.

## Task N - Final Verification (MANDATORY)

```markdown
## Task N - Final Verification (MANDATORY)

Run after all tasks complete:
- [ ] Compare test results to Task 0 baseline
- [ ] New failures = regressions (must fix)
- [ ] Run /verify workflow
- [ ] Update PROGRESS.md - mark complete
```

## Dependency Graph Section

```markdown
## Dependency Graph

TK-001 ─> TK-003
TK-002 ─> TK-003
TK-003 ─> TK-004
```

## Document History Section

```markdown
## Document History

**[YYYY-MM-DD HH:MM]**
- Initial tasks plan created from IMPL/TEST
```