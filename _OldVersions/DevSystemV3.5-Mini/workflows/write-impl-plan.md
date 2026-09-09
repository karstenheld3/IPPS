---
description: Create implementation plan from spec
auto_execution_mode: 1
---

# Write Implementation Plan Workflow

## Required Skills

- @write-documents for document structure and formatting rules

## MUST-NOT-FORGET

- Run `/verify` after plan complete

## Prerequisites

- Specification exists (`_SPEC_[COMPONENT].md`)
- Read spec completely before starting
- Read @write-documents skill

## Steps

1. Create `_IMPL_[COMPONENT].md` in session folder with header: Plan ID, Goal, Target files (NEW/EXTEND/MODIFY)

2. File Structure - Tree diagram of files, mark each [NEW], [EXTEND +N lines], [MODIFY]

3. Edge Cases from spec domain objects/actions, numbered XXXX-IP01-EC-01. Categories: input boundaries, state transitions, external failures, data anomalies

4. Implementation Steps numbered XXXX-IP01-IS-01. Each: Location, Action, Code snippet, Notes. Keep small and verifiable.

5. Test Cases grouped by category, numbered XXXX-IP01-TC-01. Format: Description -> expected result

6. Verification Checklist numbered XXXX-IP01-VC-01, checkbox format. Include: Prerequisites, Implementation steps, Verification

7. Verify - Run `/verify`, cross-check against spec for completeness