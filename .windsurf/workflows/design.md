---
description: Plan before executing
---

# Design Workflow

Implements planning phase - structure approach, create documents.

## Required Skills

- @write-documents for document templates

## Steps

1. Plan structured approach
2. Outline high-level structure
3. Run `/write-spec` for specification document
4. Prove risky parts with POC (if COMPLEXITY-MEDIUM or higher)
   - POC code goes in `[SESSION_FOLDER]/poc/` (IMPL-ISOLATED mode)
   - NEVER place POC in workspace root or project source folders
5. Decompose into small testable steps
6. Run `/write-impl-plan` for implementation plan
7. Run `/write-test-plan` for test plan
8. Validate design with user (if needed)

### For COMPLEXITY-LOW

Minimal documents - concise 1-2 page versions of SPEC, IMPL, TEST.

### For COMPLEXITY-HIGH

- Prove required for risky parts
- Propose options to user before proceeding

## Quality Gate

- [ ] Approach documented (outline, spec, or plan)
- [ ] Risky parts proven via POC (if COMPLEXITY-MEDIUM or higher)
- [ ] No open questions requiring user decision
- [ ] For BUILD: SPEC, IMPL, TEST documents created
- [ ] For BUILD: Plan decomposed into small testable steps
- [ ] For SOLVE: Structure/criteria validated

## Output

Create documents in session folder:
- `_SPEC_[TOPIC].md`
- `_IMPL_[TOPIC].md`
- `_TEST_[TOPIC].md` (if applicable)
