---
description: Verify work against specs and rules
auto_execution_mode: 1
---

# Verify Workflow

Verify work against specs, rules, and quality standards.

## Required Skills

- @write-documents for document verification
- @coding-conventions for code verification

**CRITICAL**: Also read supporting files from skill output (e.g., `PYTHON-RULES.md`, `WORKFLOW-RULES.md`).

## Mandatory Re-read

**SESSION-MODE**: NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md, LEARNINGS.md (if exists)

**PROJECT-MODE**: README.md, !NOTES.md or NOTES.md, !PROBLEMS.md or PROBLEMS.md (if exists), !PROGRESS.md or PROGRESS.md (if exists), FAILS.md, LEARNINGS.md (if exists)

## Workflow

1. Determine context (INFO, SPEC, IMPL, Code, TEST, Session, Workflow, Skill)
2. Read GLOBAL-RULES and Verification Labels
3. Read relevant Context-Specific section
4. Create verification task list
5. Work through task list
6. Run Final Steps

## GLOBAL-RULES

Apply to ALL contexts:

- Write out acronyms on first usage: `Service Principal Name (SPN)` not `SPN`
- Use verification labels consistently
- Re-read relevant rules and session files before verifying
- Make internal MNF list, check after each step
- Verify product name spelling (web research if needed): `SharePoint` not `Sharepoint`
- **Avoid Markdown tables** - convert to lists with bold labels
  - Exception: README.md may use tables without `<DevSystem>` tag
  - Only [ACTOR] may add `<DevSystem MarkdownTablesAllowed=true />` to other files
  - If tables allowed: verify formatting per `core-conventions.md`
- **Avoid emojis** - replace with text equivalents
  - Exception: README.md may use emojis without `<DevSystem>` tag
  - Only [ACTOR] may add `<DevSystem EmojisAllowed=true />` to other files

## Conceptual Verification

Look for: inconsistencies, new solutions for solved problems, ambiguities, underspecified behavior, unverified assumptions, over-engineering, flawed thinking, underestimated complexity.

## Verification Labels

- `[ASSUMED]` - Unverified, needs validation
- `[VERIFIED]` - Confirmed by re-reading source
- `[TESTED]` - Tested in POC or script
- `[PROVEN]` - Works in actual implementation

**By doc type:** INFO=findings/claims, SPEC=decisions/assumptions, IMPL=edge cases/choices, TEST=behaviors/assertions

**Progression:** `[ASSUMED]` → `[VERIFIED]` → `[TESTED]` → `[PROVEN]`

## Final Steps

1. Re-read conversation, provided and relevant files
2. Identify de-prioritized or violated instructions
3. Add tasks to verification list
4. Work through list
5. Verify against MNF list

# CONTEXT-SPECIFIC

## Information Gathering (INFO)

- Would another person approach this differently? Scope aligned with problem?
- Summary section exists with copy/paste-ready findings (mandatory)
- Re-read and verify sources; drop unfindable sources
- Anticipate reader questions, clarify them
- Verify Timeline field present and accurate
- Verify Document History exists and current
- Re-read `[AGENT_FOLDER]/workflows/research.md`, verify compliance
- Verify against @write-documents `APAPALAN_RULES.md`, `MECT_WRITING_RULES.md`

## Specifications (SPEC)

- Verify Timeline, MNF section, Document History
- Verify against spec requirements and existing code
- Look for bugs, inconsistencies, contradictions, ambiguities, underspecified behavior
- Think of uncovered corner cases
- Ensure detailed changes/additions plan exists
- Ensure exhaustive verification checklist at end
- Re-read @write-documents skill, verify against rules
- Verify against `SPEC_RULES.md`, `APAPALAN_RULES.md`, `MECT_WRITING_RULES.md`

## Implementation Plans (IMPL)

- Verify Timeline, MNF section, Document History
- Re-read spec; anything forgotten or divergent?
- Re-read @coding-conventions, verify against rules
- Verify against `APAPALAN_RULES.md`, `MECT_WRITING_RULES.md`

## Implementations (Code)

- Re-read specs/plans, verify compliance
- Run existing tests if available; quick one-off tests for regression
- Re-read @coding-conventions, verify against rules
- Verify against `MECT_CODING_RULES.md`

**Logging Verification (if code contains logging/output/print):**

1. Read @coding-conventions `LOGGING-RULES.md`
2. Identify type, read corresponding file:
   - User-facing → `LOGGING-RULES-USER-FACING.md` (users always know what's happening)
   - App-level → `LOGGING-RULES-APP-LEVEL.md` (human-readable AND machine-parseable)
   - Script-level → `LOGGING-RULES-SCRIPT-LEVEL.md` (all failure info in logs alone)
3. Verify core principles: APAPALAN, Least Surprise, Full Disclosure, Visible Structure, Announce > Track > Report
4. Verify against all applicable LOG-* rules

## Testing (TEST)

- Verify Timeline, MNF section, Document History
- Test strategy matches spec requirements
- Verify against `APAPALAN_RULES.md`, `MECT_WRITING_RULES.md`
- Priority matrix: MUST TEST covered? SHOULD TEST included? DROP justified?
- Test cases: all EC-XX have TC-XX, correct format, grouped by category
- Test data: fixtures defined, setup/teardown clear
- Test phases: logical sequence, dependencies documented
- Cross-check: every FR-XX has TC-XX, every EC-XX has test

## Workflows

- Read @coding-conventions `WORKFLOW-RULES.md`, verify compliance
- Structure follows GLOBAL-RULES + CONTEXT-SPECIFIC pattern
- References use `/verify` format, skills use `@skills:name` format
- Frontmatter has `description`, steps numbered and actionable
- No hardcoded paths (use `[WORKSPACE_FOLDER]` etc.)
- Verify against `APAPALAN_RULES.md`, `MECT_WRITING_RULES.md`

## Skills

- Read @coding-conventions `AGENT-SKILL-RULES.md`, verify all sections
- SKILL.md exists with required content (Section 2.1)
- SETUP.md exists → UNINSTALL.md must exist, pre-installation verification present
- Token optimization (Section 8): no `**bold**` in LLM resource files, no verbose prefixes where compact works, no redundant prose, keywords/trigger present, all URLs preserved. Test: "Remove token → LLM loses info?" No → flag.
- File format matches type: resource=compact, instructional=rich, SETUP/UNINSTALL=verbose
- Run Section 9 Review Checklist

## Session Tracking (NOTES, PROBLEMS, PROGRESS)

**NOTES.md:** Session Info complete? Key Decisions documented? Important Findings recorded? Workflows to Run on Resume listed? Agent instructions valid?

**PROBLEMS.md:** All issues documented? Status marked (Open/Resolved/Deferred)? Root cause for resolved? Deferred justified? **Sync check**: problems for project-level?

**PROGRESS.md:** To Do current? Done marked [x]? Tried But Not Used documented? Test coverage current? **Sync check**: findings for project-level?

**Session Close Sync:**
- [ ] Resolved problems with project impact → project PROBLEMS.md
- [ ] Reusable patterns/decisions → project NOTES.md
- [ ] Bugs in unrelated code → issues or PROBLEMS.md
- [ ] New agent instructions → project rules or NOTES.md

## STRUT Plans (Planning Phase)

- [ ] Every Objective links to at least one Deliverable (`← P1-Dx`)
- [ ] Unlinked Objectives flagged - require [ACTOR] confirmation at transition
- [ ] All Deliverables have clear completion criteria
- [ ] Transitions reference Deliverables (not Objectives)
- [ ] Steps use valid AGEN verbs with `[VERB](params)` format
- [ ] Problem/goal addressed by Objectives?
- [ ] Strategy includes approach summary (AWT estimate optional)

## STRUT Plans (Transition Phase)

- [ ] All Deliverables in Transition condition checked?
- [ ] For each Objective: ALL linked Deliverables checked?
- [ ] Deliverable evidence supports Objective claim?
- [ ] Unlinked Objectives: [ACTOR] confirmation obtained?
- [ ] Transition target valid (`[PHASE-NAME]`, `[CONSULT]`, or `[END]`)?

**Objective Verification Rule:** Objective verified when ALL linked Deliverables checked. No links (`←`) → require explicit [ACTOR] confirmation.