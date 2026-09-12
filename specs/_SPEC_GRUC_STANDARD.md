# SPEC: GRUC Standard

**Doc ID**: GRUC-SP01
**Goal**: Define the enforceable standard for GRUC (Guides, Rules, Checks, Examples) file types, their structure, consumers, and separation rules

**Depends on:**
- `docs/_INFO_GRUC_GUIDES_RULES_CHECKS.md [GRUC-IN01]` for explanatory companion (WHY GRUC exists, HOW to write good GRUC documents)
- `.devin/skills/write-documents/APAPALAN_RULES.md` for writing quality rules
- `.devin/skills/write-documents/MECT_WRITING_RULES.md` for writing quality rules

**Does not depend on:**
- `specs/_SPEC_IPPS_SKILLS.md [IPPSSKLS-SP01]` (skills implement GRUC, this SPEC defines GRUC)
- `specs/_SPEC_IPPS_WORKFLOWS.md [IPPSWFLW-SP01]` (workflows consume GRUC, this SPEC defines GRUC)

## Summary

- GRUC pre-calculates compliance criteria into five file types: GUIDE, RULES, CHECKS, EXAMPLE, TEMPLATE
- Each file type has a defined purpose, consumer, lifecycle position, and content structure
- Each workflow consumes exactly one GRUC file type - except `/verify` which reads RULES and TEMPLATE (both are structural verification files)
- CHECKS have dual structure: Process Discipline (PD) and Quality Improvement (QI)
- CHECKS are invisible to the working agent during execution (gaming prevention)
- EXAMPLE files are linked from GUIDES, not consumed directly by any workflow
- This SPEC is the enforceable standard; the INFO doc is the explanatory companion

## Table of Contents

1. [File Types](#1-file-types)
2. [CHECKS Dual Structure](#2-checks-dual-structure)
3. [EXAMPLE File Type](#3-example-file-type)
4. [Consumer Mapping](#4-consumer-mapping)
5. [Lifecycle Positioning](#5-lifecycle-positioning)
6. [Separation Rules](#6-separation-rules)
7. [Naming Conventions](#7-naming-conventions)
8. [Content Structure Per File Type](#8-content-structure-per-file-type)
9. [Design Decisions](#9-design-decisions)
10. [Acceptance Criteria](#10-acceptance-criteria)

## 1. File Types

### GRUC-FR-01: Five GRUC File Types

GRUC consists of five file types, each with a distinct purpose:

- **GUIDE** - Process guidance, strategic coaching. Tells agent HOW to approach work. Consumed before and reviewed after execution.
- **RULES** - Output standards, verification criteria. Defines what correct output looks like. Consumed during verification.
- **CHECKS** - Process discipline audit and quality improvement. Verifies HOW the agent worked and suggests improvements. Consumed after execution.
- **EXAMPLE** - Supplementary quality reference. Shows larger GOOD examples beyond BAD/GOOD pairs. Linked from GUIDES.
- **TEMPLATE** - Skeleton structure for document creation. Provides section layout and placeholders that agents copy and adapt. Consumed by `/verify` alongside RULES.

### GRUC-FR-02: Consumer Mapping

Each GRUC file type maps to exactly one workflow as its primary consumer. Two exceptions: CHECKS is one file type with two sections (PD and QI), each consumed by a different workflow. TEMPLATE is consumed by `/verify` alongside RULES since both are structural verification files:

- GUIDE → `/critique` (strategic gap analysis after execution)
- RULES → `/verify` (structural compliance check)
- TEMPLATE → `/verify` (template adherence check, if TEMPLATE exists)
- CHECKS PD → `/drift-detect` (process discipline audit)
- CHECKS QI → `/improve` (quality improvement application)

### GRUC-FR-03: Working Agent Access

The working agent reads GUIDE files before and during execution. The working agent must NOT read CHECKS files during execution. RULES files are read by `/verify` after execution, not by the working agent during execution.

## 2. CHECKS Dual Structure

### GRUC-FR-04: CHECKS Have PD and QI Sections

Every CHECKS file must contain two sections:

- **Process Discipline (PD)** - Action evidence checks. Each item: action + evidence + failure indicator. Verifies the agent followed the correct process.
- **Quality Improvement (QI)** - Judgment-based improvement tips. Each item: quality question + improvement tip. Not binary pass/fail.

### GRUC-FR-05: PD Items Reference Rule IDs

PD items must reference rule IDs from the companion RULES file they verify. No content replication - reference by ID only.

### GRUC-FR-06: QI Items Are Judgment-Based

QI items must not be binary pass/fail. Each QI item poses a quality question and provides an improvement tip. The answer requires judgment, not mechanical checking.

## 3. EXAMPLE File Type

### GRUC-FR-07: EXAMPLE Naming Convention

EXAMPLE files must follow the naming convention: `[TOPIC]_EXAMPLE_[NN]-[ExampleName].md`

Example: `SPEC_EXAMPLE_01-TodoListReactApp.md`

### GRUC-FR-08: EXAMPLE Content Rules

EXAMPLE files:
- Show complete or substantial GOOD documents
- Are use-case-specific (each example solves a specific problem type)
- Document key decisions and rationale
- Must NOT contain BAD examples (BAD/GOOD pairs stay in RULES)
- Must be linked from GUIDE files, not from RULES or CHECKS

### GRUC-FR-09: EXAMPLE Not Directly Consumed

No workflow consumes EXAMPLE files directly. EXAMPLE files are linked from GUIDE files and referenced by `/critique` for quality comparison during strategic gap analysis.

## 4. Consumer Mapping

### GRUC-IG-01: Single GRUC Type Per Workflow

Each workflow consumes exactly one GRUC file type as its primary source. Exception: `/verify` consumes both RULES and TEMPLATE, since both are structural verification files consumed post-execution. No gaming risk (both are post-execution). No overlap (RULES define standards, TEMPLATE defines structure). This prevents:
- Token waste (agent reads content it does not need)
- Overlap (two workflows reading the same GRUC type duplicate work)
- Gaming risk (if CHECKS are visible during execution, agent performs superficially)

### GRUC-IG-02: No Content Replication

GRUC files must not replicate content from each other. RULES define output standards, GUIDES define process strategy, CHECKS define process audit and improvement. Cross-reference by rule ID, never copy content.

### GRUC-IG-03: CHECKS Invisible During Execution

CHECKS files must not be referenced in any step the working agent executes. CHECKS are consumed only by `/drift-detect` and `/improve` after execution completes. This prevents the agent from gaming the checks.

## 5. Lifecycle Positioning

### GRUC-FR-10: Lifecycle Stages

GRUC files map to stages in the agent activity lifecycle:

```
Agent Activity Lifecycle
│
├── BEFORE (Planning)
│   └── GUIDE consumed by working agent
│       "How should I approach this?"
│       EXAMPLES linked from GUIDE for quality reference
│
├── DURING (Execution)
│   └── Working agent executes
│       CHECKS invisible (gaming prevention)
│
├── AFTER (Verification)
│   └── RULES + TEMPLATE consumed by /verify
│       "Does the output meet structural standards?"
│       "Does the output follow the template structure?"
│
├── AFTER (Strategic Review)
│   └── GUIDE consumed by /critique
│       "Did the agent choose the right approach?"
│       EXAMPLES used for quality comparison
│
├── AFTER (Process Audit)
│   └── CHECKS PD consumed by /drift-detect
│       "Did the agent follow the correct process?"
│
└── AFTER (Quality Improvement)
    └── CHECKS QI consumed by /improve
        "How can the output be improved?"
```

## 6. Separation Rules

### GRUC-FR-11: Content Boundary Per File Type

Each GRUC file type has a strict content boundary:

- **RULES** contain: output standards, structural requirements, BAD/GOOD pairs, rule IDs. No process guidance, no strategic coaching, no audit items.
- **GUIDES** contain: numbered decision steps, strategic options, EXAMPLE links, review criteria. No output standards, no audit items.
- **CHECKS PD** contain: action + evidence + failure indicator, rule ID references. No output standards, no strategic coaching.
- **CHECKS QI** contain: quality questions + improvement tips. No output standards, no strategic coaching.
- **EXAMPLES** contain: complete GOOD documents, key decisions, rationale. No BAD examples, no rules, no checks.
- **TEMPLATES** contain: section layout, placeholders, structural skeleton. No rules, no process guidance, no audit items. Optional - not all document types have a template.

### GRUC-FR-12: Boundary Test

To determine which file type a piece of content belongs to:

- "Does the output have X section?" → RULES (structural requirement)
- "Should the agent consider Y before starting?" → GUIDE (strategic decision)
- "Did the agent do Z during execution?" → CHECKS PD (process evidence)
- "Could the output be improved by doing W?" → CHECKS QI (quality improvement)
- "Show me a complete example of a good X" → EXAMPLE (quality reference)
- "What sections should this document type have?" → TEMPLATE (structural skeleton)

## 7. Naming Conventions

### GRUC-FR-13: GRUC File Naming

GRUC files use the following naming patterns within skill folders:

- `SKILL_RULES.md` - Skill output standards
- `SKILL_GUIDES.md` - Skill process guidance
- `SKILL_CHECKS.md` - Skill process audit and quality improvement
- `[TOPIC]_EXAMPLE_[NN]-[ExampleName].md` - Example files

For document-type-specific GRUC files within `@skills:write-documents`:

- `[DOCUMENT_TYPE]_RULES.md` - e.g., `SPEC_RULES.md`, `INFO_RULES.md`
- `[DOCUMENT_TYPE]_GUIDES.md` - e.g., `SKILL_GUIDES.md`, `INFO_GUIDES.md`
- `[DOCUMENT_TYPE]_CHECKS.md` - e.g., `SKILL_CHECKS.md`, `WORKFLOW_CHECKS.md`
- `[DOCUMENT_TYPE]_TEMPLATE.md` - e.g., `SKILL_TEMPLATE.md`, `WORKFLOW_TEMPLATE.md`

### GRUC-FR-14: GRUC File Placement

GRUC files reside in the skill folder they belong to. No cross-skill GRUC references. Each skill is self-contained with its own GRUC file set.

## 8. Content Structure Per File Type

### GRUC-FR-15: RULES File Structure

```
# [Domain] Rules

[One-line scope statement]

**Writing quality:** Apply `APAPALAN_RULES.md`. Key rules: [list 3-4 most relevant]

## Rule Index

[Category] ([2-letter prefix])
- [PREFIX]-[CAT]-[NN]: [One-line rule statement]

## [Rule ID]: [Rule Name]

**BAD:**
[example of violation]

**GOOD:**
[example of compliance]
```

### GRUC-FR-16: GUIDE File Structure

```
# [Domain] Guide

[One-line purpose statement: what to read BEFORE doing what]

## 1. [First Decision/Step]

[Actionable guidance: tell agent what to DO]

## 2. [Second Decision/Step]

[Actionable guidance]

## Review Checklist

- [ ] [checklist item]
```

### GRUC-FR-17: CHECKS File Structure

```
# [Domain] Checks

[One-line: what this audits - process discipline AND quality improvement]

**Evidence sources:** [list of evidence types]

## Process Discipline (PD)

### [PREFIX]-PD-01: [Check Name]

- Action: [what the agent should have done]
- Evidence: [where to find proof]
- Failure indicator: [what failure looks like]
- References: [rule IDs from RULES file]

## Quality Improvement (QI)

### [PREFIX]-QI-01: [Check Name]

- Question: [quality question]
- Improvement tip: [actionable improvement suggestion]
```

### GRUC-FR-18: EXAMPLE File Structure

```
# [Domain] Example [NN]: [ExampleName]

[One-line: what use case this demonstrates]

## Context

[What problem this example solves]

## Document

[Complete or substantial GOOD document]

## Key Decisions

- [Decision 1]: [rationale]
- [Decision 2]: [rationale]
```

### GRUC-FR-19: TEMPLATE File Structure

```
# [Domain] Template

[One-line: what document type this template creates]

## [Section 1]

[Placeholder content with inline comments showing what to fill]

## [Section 2]

[Placeholder content]
```

Templates use `_TEMPLATE` suffix (SK-FL-07). Templates contain only structural skeleton and placeholders - no rules, no guidance, no examples.

## 9. Design Decisions

### GRUC-DD-01: Why Five File Types Instead of One

A single "standards" file mixes output requirements with process guidance with audit criteria. The agent cannot tell which section to read when. Five files with strict boundaries means each consumer reads exactly what it needs.

### GRUC-DD-02: Why CHECKS Have Dual Structure (PD + QI)

PD checks verify process discipline (did the agent follow the correct steps). QI checks suggest quality improvements (how can the output be better). These are fundamentally different: PD is evidence-based and binary, QI is judgment-based and subjective. Separating them within the same file keeps related audit content together while maintaining distinct verification approaches.

### GRUC-DD-03: Why CHECKS Are Invisible During Execution

If the working agent sees CHECKS during execution, it performs actions superficially to pass checks rather than genuinely following the process. This defeats the purpose of process discipline. CHECKS are consumed only after execution by `/drift-detect` (PD) and `/improve` (QI).

### GRUC-DD-04: Why EXAMPLE Files Are Separate from RULES

RULES contain BAD/GOOD pairs that show a single rule's compliance or violation. EXAMPLES show complete documents demonstrating how multiple rules interact in a real use case. Mixing them would make RULES files enormous and dilute the quick-lookup pattern. EXAMPLES are linked from GUIDES because `/critique` uses them for quality comparison during strategic review.

### GRUC-DD-05: Why Single GRUC Type Per Workflow (With TEMPLATE Exception)

Multiple GRUC types in one workflow cause token waste, overlap, and gaming risk. Single type per workflow eliminates all three. Exception: `/verify` consumes both RULES and TEMPLATE. This is safe because both are post-execution structural files with no gaming risk, no overlap (RULES define standards, TEMPLATE defines structure), and minimal token cost (templates are small).

### GRUC-DD-06: Why This SPEC Is Permanent (Not Session-Scoped)

GRUC is a permanent architectural pattern, not a one-time change. A permanent SPEC in `specs/` gives `/verify` a lasting standard to check GRUC files against. The INFO doc explains WHY; this SPEC enforces WHAT. Future GRUC changes update this SPEC (reverse-sync from code).

## 10. Acceptance Criteria

### GRUC-AC-01: File Types Correct

- [ ] Each GRUC file is one of: GUIDE, RULES, CHECKS, EXAMPLE, TEMPLATE
- [ ] No file mixes content from multiple GRUC types
- [ ] Each file follows its type-specific structure (GRUC-FR-15 through GRUC-FR-19)

### GRUC-AC-02: CHECKS Dual Structure

- [ ] Every CHECKS file has "Process Discipline (PD)" section
- [ ] Every CHECKS file has "Quality Improvement (QI)" section
- [ ] PD items have: action + evidence + failure indicator + references
- [ ] QI items have: quality question + improvement tip
- [ ] PD items reference rule IDs, not replicate rule content

### GRUC-AC-03: Consumer Mapping Correct

**Rule and template files:**
- [ ] `/verify` references `*_RULES.md` files and `*_TEMPLATE.md` files (if TEMPLATE exists)
- [ ] `/critique` references only `*_GUIDES.md` files and EXAMPLE links

**Check files:**
- [ ] `/drift-detect` references only `*_CHECKS.md` PD items
- [ ] `/improve` references only `*_CHECKS.md` QI items
- [ ] No workflow references multiple GRUC types

### GRUC-AC-04: CHECKS Invisible During Execution

- [ ] No workflow step executed by the working agent references `*_CHECKS.md`
- [ ] CHECKS files are referenced only in `/drift-detect` and `/improve` contexts

### GRUC-AC-05: EXAMPLE Files Correct

- [ ] EXAMPLE files follow naming: `[TOPIC]_EXAMPLE_[NN]-[ExampleName].md`
- [ ] EXAMPLE files contain no BAD examples
- [ ] EXAMPLE files are linked from GUIDE files
- [ ] No workflow consumes EXAMPLE files directly

### GRUC-AC-06: No Content Replication

- [ ] RULES files do not contain process guidance
- [ ] GUIDE files do not contain output standards
- [ ] CHECKS files do not contain output standards or process guidance
- [ ] TEMPLATE files contain only structural skeleton and placeholders
- [ ] Cross-references use rule IDs, not copied content

## Document History

**[2026-09-12 14:40]**
- Added: TEMPLATE as fifth GRUC file type (GRUC-FR-01, FR-19, FR-13)
- Changed: `/verify` now consumes RULES and TEMPLATE (GRUC-FR-02, IG-01, DD-05)
- Changed: Lifecycle, separation, boundary test, ACs updated for TEMPLATE

**[2026-09-12 14:30]**
- Fixed: GRUC-FR-02 title and wording to clarify CHECKS is one file type with two sections
- Fixed: GRUC-AC-03 grouped into clusters (AP-ST-07 compliance)

**[2026-09-12 14:20]**
- Initial specification created
