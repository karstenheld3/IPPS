# Session Notes: GRUC Formalization

**Started**: 2026-09-12
**Goal**: Formalize and verify GRUC implementation - extend CHECKS purpose, separate workflow concerns, add EXAMPLE file type

## Current Phase

**Phase**: EXPLORE
**Workflow**: (pending assessment)
**Assessment**: (pending)

## User Prompts

### Prompt 1 (2026-09-12 12:54)

Change 1: Extension of CHECKS purpose.
- Currently CHECKS focuses on Process Discipline analysis after generation
- Add high level checks with tips for improvements for every document type
- Example: For SPECs the CHECKS should contain the question: Is the SPEC serving the stated goal? Did it make all necessary decisions? Does it avoid unnecessary complexity of dependencies? Did we fact-check all assumptions?

Change 2: Separation of concerns:
1. verify.md ONLY verifies against [TOPIC]_RULES.md
2. critique.md ONLY reads [TOPIC]_GUIDES.md (if exists) and tries to find out what the current state or implementation is missing and what the [ACTOR] did wrong. [TOPIC]_GUIDES.md links to example files if these exist.
3. drift-control (drift-detect.md): Keep current behavior but ONLY consults [TOPIC]_CHECKS.md to assess agent instruction following and drift measurement.
4. improve.md: Keep current behavior but ONLY consults [TOPIC]_CHECKS.md which is also the place for ALL improvement ideas. Like for example add diagrams to info files, fact-checking or extending or deepening research documents, write better summaries.

I want to reduce the overlap and duplicate work done using verify.md, critique.md, drift-control and improve.md.

Example files:
- go beyond simple BAD and GOOD comparisions
- they show larger GOOD examples that show how to solve different use cases
- they follow [TOPIC]_EXAMPLE_[NN]-[ExampleName].md (e.g. "SPEC_EXAMPLE_01-TodoListReactApp")

## Key Findings

### Current State

- 21 `*_RULES.md` files exist across 3 skills (write-documents, coding-conventions, deep-research)
- 6 `*_GUIDES.md` files exist in write-documents only
- 0 `*_CHECKS.md` files exist (not yet implemented)
- 0 `*_EXAMPLE_*` files exist (new file type)
- `verify.md` currently does much more than RULES: includes SOCAS conceptual verification, fact-checking, privacy scans, formatting checks
- `critique.md` currently reads FAILS.md, does research, uses SOCAS - does NOT read GUIDES
- `drift-detect.md` builds DoD from sources (SPEC, IMPL, etc.) - does NOT consume CHECKS files
- `improve.md` reads RULES, does SOCAS scanning, research - does NOT consume CHECKS files
- `drift-control/SKILL.md` describes CHECKS as process-only, invisible to executor

### Architecture Changes Needed

1. CHECKS gets dual purpose: Process Discipline (existing) + Quality Improvement Checks (new)
2. verify.md strips to RULES-only (remove SOCAS, fact-check, privacy scan - or move to CHECKS)
3. critique.md switches from SOCAS/research to GUIDES-driven review
4. drift-detect.md switches from DoD-from-sources to CHECKS-driven assessment
5. improve.md switches from RULES+SOCAS to CHECKS-driven improvements
6. New EXAMPLE file type added to GRUC naming conventions
7. GUIDES link to EXAMPLE files

## IMPORTANT: Cascade Agent Instructions

- This is a DESIGN phase task - need SPEC before implementation
- Changes affect 4 workflows + 1 INFO doc + drift-control skill + potentially SKILL_RULES
- Must preserve existing RULES file IDs and structure
- Must not break existing workflow references across the system
- EXAMPLE files are a new GRUC type - need naming convention, structure pattern, writing guide

## Integration Tasks (Pending)

The following integration tasks must be done after the GRUC formalization SPECs are approved:

### Sync to PromptSystemV4.4

1. Sync `_INFO_GRUC_GUIDES_RULES_CHECKS.md` to `PromptSystemV4.4/docs/` (or update existing copy)
2. Sync `specs/_SPEC_IPPS_SKILLS.md` to `PromptSystemV4.4/specs/`
3. Sync `specs/_SPEC_IPPS_WORKFLOWS.md` to `PromptSystemV4.4/specs/`

### Update WORKFLOW_RULES.md GRUC Section

4. Update `PromptSystemV4.4/skills/write-documents/WORKFLOW_RULES.md` section "GRUC Verification" to reflect:
   - CHECKS now have dual purpose (PD + QI)
   - EXAMPLE file type added
   - Consumer mapping: verify→RULES, critique→GUIDES, drift-detect→CHECKS PD, improve→CHECKS QI
   - Current GRUC section (L610-661) only mentions PD checks, needs QI checks added

### Update SKILL_RULES.md

5. Add rule for GRUC file set requirement to `PromptSystemV4.4/skills/write-documents/SKILL_RULES.md`:
   - SKILL.md must list all GRUC companion files in References section
   - SKILL_RULES.md is always required
   - SKILL_GUIDES.md required for complex decision skills
   - SKILL_CHECKS.md required for quality-critical skills

### Create EXAMPLE Files

6. Create first EXAMPLE files for SPEC and INFO document types:
   - `SPEC_EXAMPLE_01-TodoListReactApp.md` - complete SPEC for a simple app
   - `INFO_EXAMPLE_01-TechEvaluation.md` - complete INFO for a technology comparison

### Update Existing Workflows

7. Update `/verify` to consume only RULES files (remove SOCAS, fact-check, privacy scan)
8. Update `/critique` to consume only GUIDES files (remove research phase, SOCAS)
9. Update `/drift-detect` to consume only CHECKS PD files (replace DoD-from-sources)
10. Update `/improve` to consume only CHECKS QI files (remove Phase 2 fix violations, SOCAS)

### Update Drift-Control Skill

11. Update `PromptSystemV4.4/skills/drift-control/SKILL.md` to reflect CHECKS dual purpose
12. Update `PromptSystemV4.4/skills/drift-control/DRIFT_DETECTION.md` for CHECKS PD consumption

### Verify

13. Run `/verify` on all new and modified files
14. Run `/fact-check` on all new SPEC files
15. Verify GRUC separation: no workflow reads multiple GRUC types
