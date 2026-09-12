# SPEC: IPPS Workflows

**Doc ID**: IPPSWFLW-SP01
**Goal**: Define the structure, GRUC consumption rules, context branching, and compliance criteria for workflows in the IPPS PromptSystem

**Depends on:**
- `docs/_INFO_GRUC_GUIDES_RULES_CHECKS.md [GRUC-IN01]` for GRUC file type definitions
- `.devin/skills/write-documents/WORKFLOW_RULES.md` for workflow document rules (WF-* IDs)
- `specs/_SPEC_IPPS_SKILLS.md [IPPSSKLS-SP01]` for skill GRUC file structure

**Does not depend on:**
- Individual workflow files (this SPEC defines the standard, not specific workflows)

## Summary

- Workflows are the execution unit in IPPS - each workflow defines a repeatable process for a specific task type
- Every workflow must implement: frontmatter, Goal/Why, MUST-NOT-FORGET, Mandatory Re-read, GLOBAL-RULES, CONTEXT-SPECIFIC with branching, Phases, Quality Gate
- Each workflow consumes exactly one GRUC file type, exception: `/verify` reads RULES and TEMPLATE, `/critique` reads GUIDES, `/drift-detect` reads CHECKS PD, `/improve` reads CHECKS QI
- Workflows must branch by document type or mode, with a "No Context Match" fallback
- Workflows must reference skills via `@skills:` format and other workflows via inline code `/name`
- No content replication from GRUC files - reference by rule ID only

## Table of Contents

1. [Workflow Anatomy](#1-workflow-anatomy)
2. [Required Sections](#2-required-sections)
3. [Context Branching](#3-context-branching)
4. [GRUC Consumption Rules](#4-gruc-consumption-rules)
5. [GRUC Files for Workflow Creation](#5-gruc-files-for-workflow-creation)
6. [Workflow References](#6-workflow-references)
7. [Autonomous Execution](#7-autonomous-execution)
8. [Design Decisions](#8-design-decisions)
9. [Acceptance Criteria](#9-acceptance-criteria)

## 1. Workflow Anatomy

A workflow is a markdown file under `[AGENT_FOLDER]/workflows/` with YAML frontmatter and structured sections.

```
[workflow-name].md
  ---
  description: [When to apply this workflow]
  auto_execution_mode: [optional: 1 for auto-run]
  ---
  # [Workflow Name]
  [Goal + Why]
  ## Required Skills
  ## MUST-NOT-FORGET
  ## Mandatory Re-read
  ## GLOBAL-RULES
  # CONTEXT-SPECIFIC
    ## [Context A]
    ## [Context B]
    ## No Context Match
  ## Phases (numbered)
  ## Quality Gate
```

## 2. Required Sections

### IPPSWFLW-FR-01: Frontmatter

YAML frontmatter with `description` field required (WF-HD-01). Optional `auto_execution_mode: 1` for auto-run workflows.

### IPPSWFLW-FR-02: Goal and Why

After the title, state Goal (expected outcome) and Why (purpose). Reader knows WHY before HOW (WF-HD-02, AP-ST-01).

### IPPSWFLW-FR-03: MUST-NOT-FORGET Section

Simple list of 3-10 critical items. No subheadings or explanations (WF-ST-03). Order by impact: most common mistake first, data loss risks, API gotchas.

### IPPSWFLW-FR-04: Mandatory Re-read Section

Branch by mode (SESSION-MODE, PROJECT-MODE), list documents to re-read before starting (WF-ST-01 variant).

- SESSION-MODE: NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md
- PROJECT-MODE: README.md, !NOTES.md or NOTES.md, FAILS.md

### IPPSWFLW-FR-05: GLOBAL-RULES Section

Universal rules that apply to ALL contexts before any context-specific steps. Numbered, actionable, concise (WF-ST-01).

### IPPSWFLW-FR-06: CONTEXT-SPECIFIC Section

Use H1 for section, H2 for contexts. Include "No Context Match" fallback (WF-BR-01, WF-BR-02). Each context has numbered, actionable steps.

### IPPSWFLW-FR-07: Phases and Steps

Phases and top-level steps start at 1 with no gaps (WF-ST-07). Sub-numbering must be numeric only (`1.1`, `1.2` - no `1a`, `1b`). Steps must be numbered and actionable (WF-ST-02).

### IPPSWFLW-FR-08: Quality Gate

Final checklist before completion (WF-ST-06). Checkbox format with Pass/Fail actions.

### IPPSWFLW-FR-09: Verification Section

Reference `/verify` with specific checks (WF-ST-04). Not a generic "make sure everything is correct" - list specific items to verify.

### IPPSWFLW-FR-10: Scope Boundary

One line clarifying what the workflow does NOT do (WF-HD-04). Prevents overlap with other workflows.

## 3. Context Branching

### IPPSWFLW-FR-11: Branch by Document Type or Mode

Workflows must branch by document type (INFO, SPEC, IMPL, Code, TEST) or mode (SESSION-MODE, PROJECT-MODE). Each branch has specific steps tailored to that context (WF-BR-01).

### IPPSWFLW-FR-12: No Context Match Fallback

Every workflow must include a "No Context Match" fallback section with defined behavior (WF-BR-02). Fallback must not ask questions - it must define a default action.

### IPPSWFLW-FR-13: Gate Checks

Transitions between phases use checkbox format with Pass/Fail actions (WF-BR-03).

### IPPSWFLW-FR-14: Trigger Section

How the workflow is invoked (WF-BR-04). List trigger patterns: `/name [args]` for user invocation, `/name` for agent-detected invocation.

## 4. GRUC Consumption Rules

### IPPSWFLW-FR-15: Single GRUC Type Per Workflow

Per `GRUC-IG-01`, each workflow consumes exactly one GRUC file type as its primary source. Exception: `/verify` consumes both RULES and TEMPLATE. No workflow reads multiple GRUC types beyond this exception.

- `/verify` reads `*_RULES.md` and `*_TEMPLATE.md` files (if TEMPLATE exists)
- `/critique` reads `*_GUIDES.md` files only and links EXAMPLE files
- `/drift-detect` reads `*_CHECKS.md` PD items only
- `/improve` reads `*_CHECKS.md` QI items only

### IPPSWFLW-FR-16: No Content Replication from GRUC Files

Per `GRUC-IG-02` and WF-RF-05, workflows must never copy rule descriptions, examples, or checklists from GRUC files. Reference by file + rule ID only. If the source changes, replicas drift silently.

### IPPSWFLW-FR-17: GRUC File Discovery

Workflows discover GRUC files by scanning the skill folder referenced in Required Skills. The workflow reads only the GRUC file type it is designated to consume.

### IPPSWFLW-FR-18: Invisible CHECKS During Execution

Per `GRUC-IG-03`, `*_CHECKS.md` files must not be referenced in workflow steps that the working agent executes. CHECKS are consumed only by `/drift-detect` and `/improve` after execution completes.

## 5. GRUC Files for Workflow Creation

Workflows are created using GRUC files maintained in `@skills:write-documents`. These files guide workflow creation and must exist and be maintained:

### IPPSWFLW-FR-19: WORKFLOW_RULES.md Required

`WORKFLOW_RULES.md` must exist in `@skills:write-documents`. Defines output standards for workflow documents (WF-* rule IDs). Consumed by `/verify`.

### IPPSWFLW-FR-20: WORKFLOW_GUIDES.md Required

`WORKFLOW_GUIDES.md` must exist in `@skills:write-documents`. Provides process guidance for writing workflows. Consumed by `/critique`.

### IPPSWFLW-FR-21: WORKFLOW_CHECKS.md Required

`WORKFLOW_CHECKS.md` must exist in `@skills:write-documents`. Provides process discipline (PD) and quality improvement (QI) checks for workflow creation. Consumed by `/drift-detect` (PD) and `/improve` (QI).

### IPPSWFLW-FR-22: WORKFLOW_TEMPLATE.md Optional

`WORKFLOW_TEMPLATE.md` may exist in `@skills:write-documents` as a template for new workflow documents. Must use `_TEMPLATE` suffix per SK-FL-07. Provides a skeleton structure that agents copy and adapt.

## 6. Workflow References

### IPPSWFLW-FR-23: Workflow Reference Format

References to other workflows use inline code with slash prefix: `/verify`, `/implement` (WF-RF-01).

### IPPSWFLW-FR-24: Skill Reference Format

References to skills use `@skills:` format: `@skills:write-documents` (WF-RF-02).

### IPPSWFLW-FR-25: No Hardcoded Paths

Use standard placeholders: `[WORKSPACE_FOLDER]`, `[PROJECT_FOLDER]`, `[SESSION_FOLDER]`, `[AGENT_FOLDER]`, `[PROMPTSYSTEM_FOLDER]` (WF-RF-03, WF-RF-04).

## 7. Autonomous Execution

### IPPSWFLW-FR-26: No Unnecessary Confirmation Gates

Workflows must execute without unnecessary pauses (WF-EX-01). Only request confirmation for:
- Destructive actions (renaming files, deleting content, overwriting user data)
- Ambiguous actions (multiple candidates, no way to determine correct one)

Non-destructive actions (creating files, extracting data, reading context) require no confirmation.

### IPPSWFLW-FR-27: Stuck Detection

Workflows must define a stuck threshold and actions (e.g., "If 3 consecutive attempts fail: document in PROBLEMS.md, ask user for guidance").

### IPPSWFLW-FR-28: Output Format

Workflows must define expected output structure inline (WF-ST-05). Show the format, don't describe it.

## 8. Design Decisions

### IPPSWFLW-DD-01: Why Single GRUC Type Per Workflow

Multiple GRUC types in one workflow cause:
- Token waste: agent reads content it does not need for this workflow
- Overlap: two workflows reading the same GRUC type duplicate work
- Gaming risk: if CHECKS are visible during execution, agent performs actions superficially to pass

Single GRUC type per workflow eliminates all three problems.

### IPPSWFLW-DD-02: Why No Content Replication

Replicating rule content from GRUC files creates maintenance dependencies. When the source file changes, replicas drift silently. Reference by ID ensures the workflow always points to the current version.

### IPPSWFLW-DD-03: Why Context Branching Is Required

Different document types need different verification steps. A one-size-fits-all workflow either over-verifies simple documents or under-verifies complex ones. Branching ensures each context gets appropriate treatment.

### IPPSWFLW-DD-04: Why No Context Match Must Not Ask Questions

Workflows are autonomous execution units. If the context is unknown, the workflow must define a default action (treat as external document type, apply standard pipeline). Asking questions breaks autonomous execution.

## 9. Acceptance Criteria

### IPPSWFLW-AC-01: Required Sections Present

**Header and structure:**
- [ ] Frontmatter with `description` field
- [ ] Goal and Why after title
- [ ] Scope boundary (one line, what workflow does NOT do)

**Core sections:**
- [ ] MUST-NOT-FORGET section (simple list, 3-10 items)
- [ ] Mandatory Re-read section (branched by mode)
- [ ] GLOBAL-RULES section (numbered, actionable)
- [ ] CONTEXT-SPECIFIC section with "No Context Match" fallback

**Execution sections:**
- [ ] Phases numbered from 1 with no gaps
- [ ] Quality Gate with checkbox format
- [ ] Verification section referencing `/verify`

### IPPSWFLW-AC-02: GRUC Consumption Correct

- [ ] Workflow reads exactly one GRUC file type (per `GRUC-IG-01`, exception: `/verify` reads RULES + TEMPLATE)
- [ ] No content replicated from GRUC files (reference by ID only, per `GRUC-IG-02`)
- [ ] CHECKS files not referenced in agent-executed steps (per `GRUC-IG-03`)

### IPPSWFLW-AC-03: GRUC Files for Workflow Creation Exist

- [ ] `WORKFLOW_RULES.md` exists in `@skills:write-documents`
- [ ] `WORKFLOW_GUIDES.md` exists in `@skills:write-documents`
- [ ] `WORKFLOW_CHECKS.md` exists in `@skills:write-documents` with PD + QI sections

### IPPSWFLW-AC-04: Context Branching Correct

- [ ] Branches by document type or mode
- [ ] "No Context Match" fallback defines default action (not a question)
- [ ] Gate checks use checkbox format with Pass/Fail

### IPPSWFLW-AC-05: References Correct

- [ ] Workflow references use inline code: `/name`
- [ ] Skill references use `@skills:` format
- [ ] No hardcoded paths (uses standard placeholders)
- [ ] No acronyms used without expansion on first use

### IPPSWFLW-AC-06: Autonomous Execution

- [ ] No unnecessary confirmation gates
- [ ] Stuck detection threshold defined
- [ ] Output format shown inline

## Document History

**[2026-09-12 14:40]**
- Changed: FR-15 updated to reflect `/verify` consumes RULES and TEMPLATE per GRUC-IG-01
- Changed: AC-02 updated for `/verify` + TEMPLATE exception

**[2026-09-12 14:30]**
- Added: Section 5 (GRUC Files for Workflow Creation) with FR-19 through FR-22 for WORKFLOW_RULES/GUIDES/CHECKS/TEMPLATE
- Added: AC-03 (GRUC Files for Workflow Creation Exist)
- Fixed: FR-15, FR-16, FR-18 now reference GRUC standard by ID instead of re-defining (SOCAS-03)
- Fixed: AC-01 grouped into 3 clusters (AP-ST-07 compliance)
- Fixed: FR numbering updated to reflect new section 5

**[2026-09-12 14:10]**
- Initial specification created
