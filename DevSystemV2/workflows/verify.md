---
auto_execution_mode: 1
---

## Required Skills

Invoke these skills based on context:
- @write-documents for document verification
- @coding-conventions for code verification

First find out what the context is:

- Information Gathering
- Specifications
- Implementation Plans
- Implementations
- Testing

Then read relevant section below and create a verification task list.

## Verification Labels

Apply these labels to findings, requirements, and decisions in all document types (INFO, SPEC, IMPL, TEST):

- `[ASSUMED]` - Unverified assumption, needs validation
- `[VERIFIED]` - Finding verified by re-reading source or comparing with other sources
- `[TESTED]` - Tested in POC (Proof-Of-Concept) or minimal test script
- `[PROVEN]` - Proven to work in actual project via implementation or tests

**Usage:**
- INFO docs: Label key findings and source claims
- SPEC docs: Label design decisions and assumptions
- IMPL docs: Label edge case handling and implementation choices
- TEST docs: Label expected behaviors and test assertions

**Progression:** `[ASSUMED]` → `[VERIFIED]` → `[TESTED]` → `[PROVEN]`

**Information Gathering:**
- Think first: How would another person approach this? Is the scope and trajectory aligned with the problem or question?
- Verify sources. Read them again and verify or complete findings. Drop all sources that can't be found. 
- Ask questions that a reader might ask and clarify them.
- Read `[AGENT_FOLDER]/workflows/go-research.md` again and verify against instructions.

**Specifications:**
- Verify against the spec requirements and the existing code.
- Look for bugs, inconsistencies, contradictions, ambiguities, underspeced behavior
- Think of corner cases we haven't covered yet.
- Ensure we have a detailed changes / additions plan.
- Ensure we have an exhaustive implementation verification checklist at the end.
- Read @write-documents skill again and verify against rules.

**Implementation Plans:**
- Read spec again and verify against spec. Anything forgotten or not implemented as in SPEC?
- Read @coding-conventions skill again and verify against rules.

**Implementations:**
- Read specs and plans again and verify against specs.
- Are there existing tests that we can run to verify?
- Can we do quick one-off tests to verify we did not break things?
- Read @coding-conventions skill again and verify against rules.

**Testing (Test Plans):**
- Verify test strategy matches spec requirements
- Check test priority matrix:
  - MUST TEST: Critical business logic covered?
  - SHOULD TEST: Important workflows included?
  - DROP: Justified reasons for skipping?
- Verify test cases:
  - All edge cases from IMPL plan have corresponding TC-XX
  - Format: Description -> ok=true/false, expected result
  - Grouped by category
- Check test data:
  - Required fixtures defined?
  - Setup/teardown procedures clear?
- Verify test phases:
  - Ordered execution sequence logical?
  - Dependencies between phases documented?
- Cross-check against spec:
  - Every FR-XX (Functional Requirement) has at least one TC-XX (Test Case)
  - Every EC-XX (Edge Case) has corresponding test

**Session Tracking (NOTES.md, PROBLEMS.md, PROGRESS.md):**

Verify NOTES.md:
- Session Info complete (Started date, Goal)?
- Key Decisions documented?
- Important Findings recorded?
- Workflows to Run on Resume listed?
- Agent instructions still valid?

Verify PROBLEMS.md:
- All discovered issues documented?
- Status marked (Open/Resolved/Deferred)?
- Root cause identified for resolved items?
- Deferred items have justification?
- **Sync check**: Which problems should move to project-level PROBLEMS.md?

Verify PROGRESS.md:
- To Do list current?
- Done items marked with [x]?
- Tried But Not Used documented (avoid re-exploring)?
- Test coverage analysis up to date?
- **Sync check**: Which findings should move to project-level docs?

**Session Close Sync Checklist:**
- [ ] Resolved problems with project impact → sync to project PROBLEMS.md
- [ ] Reusable patterns/decisions → sync to project NOTES.md
- [ ] Discovered bugs in unrelated code → create issues or sync to PROBLEMS.md
- [ ] New agent instructions → sync to project rules or NOTES.md

Then re-read the previous conversation, provided and relevant files. Make an internal "MUST-NOT-FORGET" list and review / edit it after each step.

FINALLY:

Re-read relevant rules and session files. Identify de-prioritized or violated instructions. Add tasks to verification task list.

Work through verification task list.

After reaching the goal, verify again against MUST-NOT-FORGET list.
