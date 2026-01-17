<DevSystem MarkdownTablesAllowed=true />

# INFO: STRUT Example Cases

**Doc ID**: STRUT-IN02
**Goal**: Define 10 realistic test cases for STRUT notation, from simple to complex

**Depends on:**
- `INFO_STRUT_FEATURES.md [STRUT-IN01]` for notation reference

**Timeline**: Created 2026-01-17, 2 updates, single day

## Summary

10 realistic test cases for validating STRUT notation:
- Cases 1-3: LOW to MEDIUM complexity (hotfix, bugfix, feature)
- Cases 4: SOLVE workflow (evaluation/decision)
- Cases 5-8: HIGH complexity patterns (refactor, nested, retry/escalate, decompose)
- Cases 9-10: Advanced patterns (defer, phase iteration)

Key patterns covered: Phase skip, retry, NEST, DEFER, ABORT, DECOMPOSE, iteration.

## Purpose

These test cases validate that STRUT notation can express real-world development scenarios. Each case is described in plain English first, then later formalized with 3 scenario variations (happy path, failure recovery, edge case).

## Test Cases

### Case 1: Simple Hotfix (COMPLEXITY-LOW)

**Situation**: Production logs show a null pointer exception in the user profile page. Stack trace points to `getUserById()` returning null when user ID doesn't exist. Fix is obvious: add null check.

**What happens**:
- Developer reads stack trace, identifies the line
- Adds null check with appropriate error handling
- Runs existing unit tests to confirm no regression
- Commits and deploys

**Why this is simple**:
- Single file change
- No design decisions needed
- Existing tests cover the area
- No documentation required

### Case 2: Bug Investigation (COMPLEXITY-LOW to MEDIUM)

**Situation**: Users report that "sometimes" the shopping cart total is wrong. No consistent reproduction steps. Could be a rounding error, race condition, or data corruption.

**What happens**:
- Developer gathers logs and user reports
- Analyzes cart calculation code
- Adds logging to track calculation steps
- Deploys instrumented code to staging
- Reproduces issue, identifies race condition in concurrent add-to-cart
- Implements fix with optimistic locking
- Writes regression test
- Commits and deploys

**Why this is harder than Case 1**:
- Investigation phase before fix
- Root cause not immediately obvious
- Multiple files involved (cart service, tests)
- Requires new test to prevent regression

### Case 3: Add API Endpoint (COMPLEXITY-MEDIUM)

**Situation**: Product team needs a new REST endpoint to return user activity history for the mobile app. Must include pagination, date filtering, and rate limiting.

**What happens**:
- Developer reviews existing API patterns in codebase
- Writes spec for new endpoint (request/response format, query params)
- Implements controller, service layer, and repository query
- Adds unit tests for service layer
- Adds integration tests for endpoint
- Updates API documentation
- Commits

**Why this is medium complexity**:
- Multiple files across layers
- Needs specification before implementation
- Pagination and filtering require design decisions
- Must follow existing patterns for consistency

### Case 4: Evaluate Database Options (SOLVE workflow)

**Situation**: The current SQLite database is hitting performance limits. Team needs to decide between PostgreSQL, MySQL, or staying with SQLite with optimizations.

**What happens**:
- Developer researches each option's capabilities
- Defines evaluation criteria (performance, hosting cost, migration effort, team expertise)
- Tests each option with representative queries
- Documents findings with benchmarks
- Presents recommendation to team
- Team decides on PostgreSQL
- Decision recorded for future reference

**Why this is different**:
- Output is a decision, not code
- Requires research and comparison
- Multiple stakeholders involved
- Creates INFO document, not implementation

### Case 5: Refactor Authentication Module (COMPLEXITY-HIGH)

**Situation**: Authentication code is scattered across 15 files with duplicated logic. New feature (OAuth) is blocked until this is cleaned up. Must maintain backward compatibility.

**What happens**:
- Developer analyzes all auth-related code
- Maps dependencies and call sites
- Designs new auth module structure
- Writes spec with before/after architecture
- Creates implementation plan with ordered steps
- Implements incrementally with tests at each step
- Each step verified before proceeding
- Updates all call sites to use new module
- Removes deprecated code
- Full regression test
- Commits in logical chunks

**Why this is high complexity**:
- Many files affected
- Breaking changes possible
- Needs comprehensive spec and plan
- Incremental implementation required
- High risk if done wrong

### Case 6: Feature with Embedded Research (BUILD with nested SOLVE)

**Situation**: Implement email sending for password reset. Developer doesn't know which email service to use or how to handle delivery failures.

**What happens**:
- Developer starts BUILD workflow for password reset
- Realizes email provider decision is blocking
- Pauses BUILD, starts embedded SOLVE
- Researches SendGrid vs Mailgun vs AWS SES
- Evaluates based on cost, API simplicity, deliverability
- Decides on SendGrid
- Resumes BUILD with decision
- Implements email sending with SendGrid
- Handles failure cases (retry, fallback)
- Tests with mock and real endpoints
- Commits

**Why this involves nesting**:
- Main workflow is BUILD (code output)
- Sub-workflow is SOLVE (decision output)
- Decision feeds back into BUILD
- Parent workflow resumes after child completes

### Case 7: Multi-Step Implementation with Failures (retry and escalation)

**Situation**: Integrate third-party payment processor. API documentation is incomplete, sandbox is flaky, and some edge cases aren't documented.

**What happens**:
- Developer writes integration spec based on docs
- Implements payment client
- Tests fail due to undocumented API behavior
- Fixes implementation based on actual API responses
- Tests fail again due to sandbox timeout
- Retries with longer timeout - still fails
- Escalates to tech lead who contacts vendor
- Vendor confirms sandbox issue, provides workaround
- Fixes tests with workaround
- Implements remaining edge cases
- Commits

**Why this tests retry and escalation**:
- Multiple failures requiring different responses
- Some failures are fixable by developer
- Some failures require external help
- Bounded retries before escalation
- Recovery from [CONSULT] to resume work

**ABORT scenario** (edge case for scenarios):
- If vendor confirms API is deprecated with no replacement
- Developer must [ABORT] integration, report to stakeholders
- Work is documented but not completed
- Different exit path than success or defer

### Case 8: Task Decomposition After Failure (DECOMPOSE-ON-FAIL)

**Situation**: Implement data export feature. Initial attempt as single task fails because it's too complex - export needs to handle 5 different data types with different formats.

**Decomposition trigger**: After N consecutive [FIX] failures on same issue, where N = complexity-based threshold (LOW: 5, MEDIUM: 3, HIGH: 2). Trigger signals task scope exceeds safe iteration limit.

**What happens**:
- Developer attempts to implement export feature
- Gets overwhelmed by complexity, makes mistakes
- Test fails, [FIX] attempt fails, second [FIX] attempt fails
- Threshold reached (3 failures for MEDIUM complexity)
- Triggers [DECOMPOSE] - task is too big for single iteration
- Decomposes into 5 subtasks (one per data type)
- Implements CSV export for users - succeeds
- Implements CSV export for orders - succeeds
- Implements CSV export for products - succeeds
- Implements CSV export for transactions - succeeds
- Implements CSV export for audit logs - succeeds
- Aggregates into unified export module
- Integration test passes
- Commits

**Why this tests decomposition**:
- Initial task too large
- Failure triggers automatic decomposition
- Each subtask is independently testable
- Aggregation step combines results
- Overall task succeeds through decomposition

### Case 9: Parallel Investigation with Deferred Items (DEFER pattern)

**Situation**: Performance optimization sprint. Multiple slow endpoints identified. Some fixes are quick, some require architectural changes, some depend on external teams.

**What happens**:
- Developer profiles 5 slow endpoints
- Endpoint A: adds database index - fixed
- Endpoint B: optimizes N+1 query - fixed
- Endpoint C: requires cache layer - defers (architectural change)
- Endpoint D: depends on external service - defers (waiting on other team)
- Endpoint E: optimizes serialization - fixed
- Documents deferred items with reasons
- Gate check: 3/5 fixed, 2 deferred with plan
- Proceeds to deliver fixed items
- Deferred items tracked for next sprint

**Why this tests defer pattern**:
- Not all items can be completed
- Some items are blocked by external factors
- Work continues despite incomplete items
- Deferred items explicitly tracked
- Gate passes with documented exclusions

### Case 10: Full Workflow with Phase Iteration (Complex multi-phase)

**Situation**: Build new reporting dashboard. Requirements are vague, technology choice is open, and stakeholders have conflicting priorities.

**What happens**:
- EXPLORE: Gathers requirements from 3 stakeholders
- EXPLORE: Discovers conflicting requirements
- EXPLORE: Consults with product owner to resolve conflicts
- EXPLORE: Requirements clarified, scope defined
- DESIGN: Proposes React dashboard with Chart.js
- DESIGN: Stakeholder review - rejected, needs D3 for custom visualizations
- DESIGN: Revises design with D3
- DESIGN: Creates spec and implementation plan
- DESIGN: Proves risky D3 integration with POC
- IMPLEMENT: Builds dashboard component by component
- IMPLEMENT: Test failure on responsive layout
- IMPLEMENT: Fixes responsive issues
- IMPLEMENT: Commits working version
- REFINE: Self-review finds accessibility issues
- REFINE: Fixes accessibility
- REFINE: Stakeholder review finds missing chart type
- REFINE: Adds missing chart, runs full regression
- DELIVER: Stakeholder sign-off
- DELIVER: Merges and deploys
- DELIVER: Closes task

**Why this is the most complex**:
- Full 5-phase workflow
- Phase iteration (DESIGN rejected, restart)
- Multiple stakeholder interactions
- Nested investigation (D3 POC)
- Multiple fix cycles in IMPLEMENT and REFINE
- Gate checks at each transition

## Test Case Summary

| Case | Type | Complexity | Key Patterns |
|------|------|------------|--------------|
| 1 | HOTFIX | LOW | Linear, no retry |
| 2 | BUGFIX | LOW-MEDIUM | Investigation + fix |
| 3 | FEATURE | MEDIUM | Multi-file, spec needed |
| 4 | EVALUATION | MEDIUM | SOLVE workflow, decision output |
| 5 | REFACTORING | HIGH | Incremental, backward compatible |
| 6 | FEATURE | HIGH | Nested SOLVE in BUILD |
| 7 | FEATURE | HIGH | Retry, escalate, recover |
| 8 | FEATURE | HIGH | Decompose-on-fail |
| 9 | CHORE | MEDIUM | Defer, partial completion |
| 10 | FEATURE | HIGH | Full phases, iteration |

## Next Steps

For each test case, define 3 scenarios:
1. **Happy Path** - Everything works as expected
2. **Failure Recovery** - Failures occur but are handled
3. **Edge Case** - Unusual situation requiring special handling

These scenarios will be expressed in STRUT notation to validate the notation can handle real-world complexity.

## Document History

**[2026-01-17 16:16]**
- Added: DevSystem tag for table usage
- Added: Timeline field
- Added: Summary section with key findings

**[2026-01-17 16:12]**
- Added: ABORT scenario to Case 7 for edge case coverage
- Added: Explicit decomposition trigger definition to Case 8 (complexity-based thresholds)
- Changed: Case 8 steps to use [FIX] and [DECOMPOSE] verb notation

**[2026-01-17 16:10]**
- Initial document created
- 10 test cases defined in plain English
- Cases range from simple hotfix to complex multi-phase workflow
- Summary table added
