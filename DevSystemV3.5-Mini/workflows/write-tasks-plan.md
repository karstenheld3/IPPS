---
description: Create tasks plan document from IMPL/TEST
auto_execution_mode: 1
---

# Write Tasks Plan Workflow

Create partitioned task documents from IMPL plans. Combines `/partition` with document creation.

## Required Skills

- @write-documents for TASKS template

## MUST-NOT-FORGET

- Run `/partition` to split IMPL into tasks

## Prerequisites

- IMPL plan exists (`_IMPL_[TOPIC].md`)
- Optionally: TEST plan (`_TEST_[TOPIC].md`)

## Steps

1. Run `/partition` with STRATEGY if specified, collect tasks
2. Create `TASKS_[TOPIC].md` in session folder with Doc ID, Goal, Source documents
3. Group tasks by phase/component, include dependencies, mark parallel vs sequential
4. Link each task to TEST plan test cases or define temporary verification
5. Copy task list to PROGRESS.md "To Do", link to TASKS document

## Document Structure

```markdown
# TASKS: [TOPIC] Tasks Plan

Doc ID (TDID): [TOPIC]-TK01
Feature: [FEATURE_SLUG]
Goal: Partitioned tasks for [TOPIC] implementation
Source: `IMPL_[TOPIC].md [TOPIC-IP01]`, `TEST_[TOPIC].md [TOPIC-TP01]`
Strategy: PARTITION-[STRATEGY]

## Task Overview

- Total tasks: N
- Estimated total: X HHW
- Parallelizable: M tasks

## Task 0 - Baseline (MANDATORY)

- [ ] Run existing tests, record pass/fail baseline
- [ ] Note pre-existing failures (not caused by this feature)

## Tasks

### Phase/Component Name

- [ ] [TOPIC]-TK-001 - Description
  - Files: [files affected]
  - Done when: [specific completion criteria]
  - Verify: [commands to run]
  - Guardrails: [must not change X]
  - Depends: none
  - Parallel: [P] or blank
  - Est: 0.5 HHW

## Task N - Final Verification (MANDATORY)

- [ ] Compare test results to Task 0 baseline
- [ ] New failures = regressions (must fix)
- [ ] Run /verify workflow
- [ ] Update PROGRESS.md - mark complete

## Dependency Graph

TK-001 ─> TK-003
TK-002 ─> TK-003

## Document History

[YYYY-MM-DD HH:MM]
- Initial tasks plan created from IMPL/TEST
```