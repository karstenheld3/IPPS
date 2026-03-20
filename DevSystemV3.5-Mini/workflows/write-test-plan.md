---
description: Create test plan from spec
auto_execution_mode: 1
---

# Write Test Plan Workflow

## Required Skills

- @write-documents for document structure and formatting rules

## MUST-NOT-FORGET

- Run `/verify` after plan complete

## Prerequisites

- `_SPEC_[COMPONENT].md` exists
- `_IMPL_[COMPONENT].md` exists (optional)
- Read @write-documents skill

## Steps

1. **Create Test Plan File** - `_TEST_[COMPONENT].md` in session folder with header block (Goal, Target file, Dependencies)
2. **Define Test Strategy** - Approach (unit/integration/snapshot/manual), what to test vs skip with reasons
3. **Create Test Priority Matrix**
   - MUST TEST: Critical business logic
   - SHOULD TEST: Important workflows
   - DROP: Not worth testing (external deps, UI-only)
   - Include testability and effort estimates
4. **Define Test Data** - Fixtures, setup/teardown, sample inputs and expected outputs
5. **Write Test Cases** - Group by category, number as XXXX-TC-01, format: Description -> ok=true/false, expected result
6. **Define Test Phases** - Ordered execution sequence with inter-phase dependencies
7. **Create Verification Checklist** - All test cases with checkboxes, manual verification steps
8. **Verify** - Run `/verify`, check coverage against spec requirements