---
description: Verify work against specs and rules
auto_execution_mode: 1
---

# Verify Workflow

Verify work against specs, rules, and quality standards.

## Required Skills

- @write-documents for document verification
- @coding-conventions for code verification

**CRITICAL**: Skill invocation returns instructions only. You MUST also read supporting files listed in skill output (e.g., `PYTHON-RULES.md`, `WORKFLOW-RULES.md`).

## Mandatory Re-read

**SESSION-MODE** - Re-read: NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md, LEARNINGS.md (if exists)

**PROJECT-MODE** - Re-read: README.md, !NOTES.md or NOTES.md, !PROBLEMS.md or PROBLEMS.md (if exists), !PROGRESS.md or PROGRESS.md (if exists), FAILS.md, LEARNINGS.md (if exists)

## Workflow

1. Determine context (INFO, SPEC, IMPL, Code, TEST, Session, Workflow, Skill)
2. Read GLOBAL-RULES and Verification Labels
3. Read relevant Context-Specific section
4. Create verification task list
5. Work through verification task list
6. Run Final Steps

## GLOBAL-RULES

Apply to ALL document types and contexts:

- Write out acronyms on first usage. BAD: `SPN not supported.` GOOD: `Service Principal Name (SPN) not supported.`
- Use verification labels consistently
- Re-read relevant rules and session files before verifying
- Make internal MUST-NOT-FORGET list, check after each step
- Verify product name spelling via web research. BAD: Sharepoint GOOD: SharePoint
- **Avoid Markdown tables** - Convert to lists
  - Exception: README.md may use tables without `<DevSystem>` tag
  - Only [ACTOR] may add `<DevSystem MarkdownTablesAllowed=true />` to other files
  - If tables allowed: verify formatting per `core-conventions.md` (aligned columns)
- **Avoid emojis** - Replace with text equivalents
  - Exception: README.md may use emojis without `<DevSystem>` tag
  - Only [ACTOR] may add `<DevSystem EmojisAllowed=true />` to other files

## Conceptual verification

When reviewing architecture, design, solution strategy, look for:
- inconsistencies
- new solutions for already solved problems
- ambiguities
- underspeced behavior
- unverified assumptions
- over-engineering and unwanted complexity
- flawed thinking and underestimated complexity

## Verification Labels

- `[ASSUMED]` - Unverified assumption, needs validation
- `[VERIFIED]` - Verified by re-reading source or comparing sources
- `[TESTED]` - Tested in POC or minimal test script
- `[PROVEN]` - Proven in actual project via implementation or tests

**Usage:** INFO: key findings/claims. SPEC: decisions/assumptions. IMPL: edge cases/choices. TEST: expected behaviors/assertions.

**Progression:** `[ASSUMED]` → `[VERIFIED]` → `[TESTED]` → `[PROVEN]`

## Final Steps

1. Re-read previous conversation, provided and relevant files
2. Identify de-prioritized or violated instructions
3. Add tasks to verification task list
4. Work through verification task list
5. Verify again against MUST-NOT-FORGET list

# CONTEXT-SPECIFIC

## Information Gathering (INFO)

- How would another person approach this? Is scope aligned with problem?
- Verify Summary section with copy/paste-ready key findings (mandatory)
- Re-read and verify/complete sources. Drop unfindable sources.
- Ask questions a reader might ask and clarify them
- Verify Timeline field present and accurate
- Verify Document History exists and is current
- Re-read `[AGENT_FOLDER]/workflows/research.md` and verify against instructions
- Verify against @write-documents `APAPALAN_RULES.md`, `MECT_WRITING_RULES.md`

## Specifications (SPEC)

- Verify Timeline field present and accurate
- Verify MUST-NOT-FORGET section exists and rules followed
- Verify against spec requirements and existing code
- Look for bugs, inconsistencies, contradictions, ambiguities, underspeced behavior
- Think of uncovered corner cases
- Ensure detailed changes/additions plan exists
- Ensure exhaustive implementation verification checklist at end
- Verify Document History exists and is current
- Re-read @write-documents skill and verify against rules
- Verify against @write-documents `SPEC_RULES.md` (required), `APAPALAN_RULES.md`, `MECT_WRITING_RULES.md`

## Implementation Plans (IMPL)

- Verify Timeline field present and accurate
- Verify MUST-NOT-FORGET section exists and rules followed
- Re-read spec and verify against it. Anything forgotten or divergent?
- Verify Document History exists and is current
- Re-read @coding-conventions skill and verify against rules
- Verify against @write-documents `APAPALAN_RULES.md`, `MECT_WRITING_RULES.md`

## Implementations (Code)

- Re-read specs/plans and verify code against them
- Run existing tests if available
- Run quick one-off tests to check for regressions
- Re-read @coding-conventions skill and verify against rules
- Verify against @coding-conventions `MECT_CODING_RULES.md`

**Logging Verification (automatic, language-agnostic):**

If code contains logging/output/print statements:

1. Read @coding-conventions `LOGGING-RULES.md`
2. Identify logging type, read corresponding rules:
   - User-facing (console, SSE) → `LOGGING-RULES-USER-FACING.md` (users always know what is happening)
   - App-level (server logs, debug) → `LOGGING-RULES-APP-LEVEL.md` (human-readable AND machine-parseable)
   - Script-level (test/QA output) → `LOGGING-RULES-SCRIPT-LEVEL.md` (all failure info in logs alone)
3. Verify core principles: APAPALAN, Least Surprise, Full Disclosure, Visible Structure, Announce > Track > Report
4. Verify code against all applicable LOG-* rules

## Testing (TEST)

- Verify Timeline field present and accurate
- Verify MUST-NOT-FORGET section exists and rules followed
- Verify test strategy matches spec requirements
- Verify against @write-documents `APAPALAN_RULES.md`, `MECT_WRITING_RULES.md`
- Check test priority matrix:
  - MUST TEST: Critical business logic covered?
  - SHOULD TEST: Important workflows included?
  - DROP: Justified reasons for skipping?
- Verify test cases:
  - All edge cases from IMPL have corresponding TC-XX
  - Format: Description -> ok=true/false, expected result
  - Grouped by category
- Check test data: fixtures defined? Setup/teardown clear?
- Verify test phases: execution sequence logical? Dependencies documented?
- Cross-check: every FR-XX has at least one TC-XX, every EC-XX has corresponding test
- Verify Document History exists and is current

## Workflows

- Read @coding-conventions `WORKFLOW-RULES.md` and verify
- Verify GLOBAL-RULES + CONTEXT-SPECIFIC structure (recommended)
- Verify workflow references use inline code: `/verify`, `/research`
- Verify frontmatter has `description` field
- Verify steps numbered and actionable
- Verify skill references use `@skills:skill-name` format
- Verify against @write-documents `APAPALAN_RULES.md`, `MECT_WRITING_RULES.md`
- Verify no hardcoded paths (use placeholders like `[WORKSPACE_FOLDER]`)

## Skills

- Read @coding-conventions `AGENT-SKILL-RULES.md` and verify against all sections
- Verify SKILL.md exists with required content (Section 2.1)
- If SETUP.md exists: verify UNINSTALL.md also exists
- If SETUP.md exists: verify pre-installation verification section present
- Verify token optimization (Section 8):
  - No `**bold**` in LLM-consumed resource files
  - No verbose prefixes where compact format works
  - No redundant prose restating headings
  - Keywords/trigger line present for lookup skills
  - All URLs and technical detail preserved
  - Test: "If I remove this token, does LLM lose information?" If no, flag it.
- Verify skill files match type:
  - Resource/lookup: compact format (one line per resource)
  - Instructional: richer format for multi-step reasoning
  - SETUP/UNINSTALL: verbose with verification steps
- Run Section 9 Review Checklist from AGENT-SKILL-RULES.md

## Session Tracking (NOTES, PROBLEMS, PROGRESS)

**Verify NOTES.md:**
- Session Info complete (Started date, Goal)?
- Key Decisions documented?
- Important Findings recorded?
- Workflows to Run on Resume listed?
- Agent instructions still valid?

**Verify PROBLEMS.md:**
- All discovered issues documented?
- Status marked (Open/Resolved/Deferred)?
- Root cause identified for resolved items?
- Deferred items have justification?
- **Sync check**: Which problems should move to project-level PROBLEMS.md?

**Verify PROGRESS.md:**
- To Do list current?
- Done items marked with [x]?
- Tried But Not Used documented?
- Test coverage analysis current?
- **Sync check**: Which findings should move to project-level docs?

**Session Close Sync Checklist:**
- [ ] Resolved problems with project impact → sync to project PROBLEMS.md
- [ ] Reusable patterns/decisions → sync to project NOTES.md
- [ ] Discovered bugs in unrelated code → create issues or sync to PROBLEMS.md
- [ ] New agent instructions → sync to project rules or NOTES.md

## STRUT Plans (Planning Phase)

Verify when STRUT plan is created or updated:

- [ ] Every Objective links to at least one Deliverable (`← P1-Dx`)
- [ ] Unlinked Objectives flagged - require [ACTOR] confirmation at transition
- [ ] All Deliverables have clear completion criteria
- [ ] Transitions reference Deliverables (not Objectives)
- [ ] Steps use valid AGEN verbs with `[VERB](params)` format
- [ ] Problem/goal addressed by Objectives?
- [ ] Strategy includes approach summary (AWT estimate optional)

## STRUT Plans (Transition Phase)

Verify before phase transition:

- [ ] All Deliverables in Transition condition are checked?
- [ ] For each Objective: are ALL linked Deliverables checked?
- [ ] Deliverable evidence supports Objective claim?
- [ ] Unlinked Objectives: [ACTOR] confirmation obtained?
- [ ] Transition target is valid (`[PHASE-NAME]`, `[CONSULT]`, or `[END]`)?

**Objective Verification Rule:**
- Objective verified when ALL linked Deliverables checked
- Check Objective checkbox only after confirming linked Deliverables
- If Objective has no links (`←`), require explicit [ACTOR] confirmation