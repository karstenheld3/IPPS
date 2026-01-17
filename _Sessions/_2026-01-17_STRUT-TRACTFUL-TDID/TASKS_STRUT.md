# TASKS: STRUT-TRACTFUL-TDID Tasks Plan

**Doc ID (TDID)**: STRUT-TK01
**Feature**: strut-tractful-tdid-formalization
**Goal**: Partitioned tasks for formalizing STRUT, TRACTFUL, TDID concepts and creating DevSystemV3.1
**Source**: `NOTES.md`, `PROBLEMS.md`, `SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP02]`, `SPEC_EDIRD_PHASE_MODEL.md [EDIRD-SP05]`
**Strategy**: PARTITION-DEFAULT

## Task Overview

- Total tasks: 18
- Estimated total: 8.0 HHW
- Parallelizable: 6 tasks

## Task 0 - Baseline (MANDATORY)

Run before starting any implementation:
- [ ] Verify DevSystemV3 exists and is current baseline
- [ ] Note existing workflow/skill/rule file counts
- [ ] Record current AGEN verb count and EDIRD structure

## Tasks

### EXPLORE Phase - Analysis

- [ ] **STRUT-TK-001** - Analyze AGEN spec for extension points
  - Files: `SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP02]`
  - Done when: Extension points identified for new verbs (RECAP, CONTINUE, GO, LEARN, READ, RESEARCH, PARTITION) and CONSTANT syntax
  - Verify: List of extension points documented in NOTES.md
  - Parallel: [P]
  - Est: 0.5 HHW

- [ ] **STRUT-TK-002** - Analyze EDIRD spec for decoupling opportunities
  - Files: `SPEC_EDIRD_PHASE_MODEL.md [EDIRD-SP05]`
  - Done when: Phase model dependencies on workflows identified; decoupling strategy defined
  - Verify: Decoupling strategy documented in NOTES.md
  - Parallel: [P]
  - Est: 0.5 HHW

- [ ] **STRUT-TK-003** - Define STRUT concept boundaries
  - Files: NOTES.md, INITIAL_PROMPT.md
  - Done when: STRUT scope clearly separated from EDIRD, TRACTFUL, AGEN
  - Verify: Boundaries documented in NOTES.md "Key Decisions"
  - Depends: TK-001, TK-002
  - Est: 0.5 HHW

- [ ] **STRUT-TK-004** - Define TRACTFUL scope vs write-documents skill
  - Files: `.windsurf/skills/write-documents/SKILL.md`
  - Done when: TRACTFUL responsibilities vs skill responsibilities defined
  - Verify: Scope documented in NOTES.md "Key Decisions"
  - Parallel: [P]
  - Est: 0.25 HHW

- [ ] **STRUT-TK-005** - Define TDID requirements for global uniqueness
  - Files: `.windsurf/rules/devsystem-ids.md`
  - Done when: Uniqueness mechanism defined (registry location, validation rules)
  - Verify: Requirements documented in NOTES.md "Key Decisions"
  - Parallel: [P]
  - Est: 0.25 HHW

- [ ] **STRUT-TK-006** - Define CONSTANT vs INSTRUCTION syntax rules
  - Files: `SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP02]`
  - Done when: Clear distinction between CONSTANT (uppercase, no brackets) and [INSTRUCTION] (brackets)
  - Verify: Syntax rules documented in NOTES.md "Key Decisions"
  - Parallel: [P]
  - Est: 0.25 HHW

### DESIGN Phase - Specifications

- [ ] **STRUT-TK-007** - Write SPEC_STRUT.md
  - Files: `SPEC_STRUT.md [STRUT-SP01]` (new)
  - Done when: STRUT spec with FR, DD, IG, AC sections complete
  - Verify: Spec follows SPEC_TEMPLATE.md structure
  - Depends: TK-003
  - Est: 1.0 HHW

- [ ] **STRUT-TK-008** - Write SPEC_TRACTFUL.md
  - Files: `SPEC_TRACTFUL.md [TRACTFUL-SP01]` (new)
  - Done when: TRACTFUL spec with document types, templates, verb mappings complete
  - Verify: Spec follows SPEC_TEMPLATE.md structure
  - Depends: TK-004
  - Est: 1.0 HHW

- [ ] **STRUT-TK-009** - Write SPEC_TDID.md
  - Files: `SPEC_TDID.md [TDID-SP01]` (new)
  - Done when: TDID spec with ID formats, registry rules, validation complete
  - Verify: Spec follows SPEC_TEMPLATE.md structure
  - Depends: TK-005
  - Est: 0.5 HHW

- [ ] **STRUT-TK-010** - Update SPEC_AGEN.md with new verbs and CONSTANT syntax
  - Files: `SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP02]`
  - Done when: New verbs added, CONSTANT syntax formalized, addresses PR-002, PR-004
  - Verify: All new verbs documented with examples
  - Depends: TK-001, TK-006
  - Est: 0.5 HHW

- [ ] **STRUT-TK-011** - Update SPEC_EDIRD.md to decouple from workflows
  - Files: `SPEC_EDIRD_PHASE_MODEL.md [EDIRD-SP05]`
  - Done when: Workflows no longer depend on EDIRD internals, addresses PR-001
  - Verify: No phase names in workflow files
  - Depends: TK-002
  - Est: 0.5 HHW

- [ ] **STRUT-TK-012** - Add AC section to SPEC template
  - Files: `.windsurf/skills/write-documents/SPEC_TEMPLATE.md`
  - Done when: Acceptance Criteria section added, addresses PR-007
  - Verify: Template updated, example AC provided
  - Est: 0.25 HHW

- [ ] **STRUT-TK-013** - Add TASKS_TEMPLATE.md to write-documents skill
  - Files: `.windsurf/skills/write-documents/TASKS_TEMPLATE.md`
  - Done when: TASKS template exists with full structure
  - Verify: Template follows skill conventions
  - Est: 0.25 HHW

### IMPLEMENT Phase - DevSystemV3.1

- [ ] **STRUT-TK-014** - Create DevSystemV3.1 folder structure
  - Files: `DevSystemV3.1/` (new folder)
  - Done when: Folder structure mirrors DevSystemV3 (rules/, workflows/, skills/)
  - Verify: All subfolders exist
  - Est: 0.25 HHW

- [ ] **STRUT-TK-015** - Copy and update rules from V3
  - Files: `DevSystemV3.1/rules/*.md`
  - Done when: All rules copied, updated with STRUT/TRACTFUL/TDID references
  - Verify: Rules reference new concepts
  - Depends: TK-014, TK-007, TK-008, TK-009
  - Est: 0.5 HHW

- [ ] **STRUT-TK-016** - Copy and update workflows from V3
  - Files: `DevSystemV3.1/workflows/*.md`
  - Done when: Workflows copied, EDIRD dependencies removed (addresses PR-001)
  - Verify: No phase: field in workflow frontmatter
  - Depends: TK-014, TK-011
  - Est: 0.5 HHW

- [ ] **STRUT-TK-017** - Copy and update skills from V3
  - Files: `DevSystemV3.1/skills/*/`
  - Done when: Skills copied, write-documents updated with TASKS template
  - Verify: TASKS_TEMPLATE.md exists in write-documents skill
  - Depends: TK-014, TK-012, TK-013
  - Est: 0.5 HHW

### REFINE Phase - Verification

- [ ] **STRUT-TK-018** - Verify all specs are harmonized
  - Files: All SPEC files in session
  - Done when: No overlap, clear responsibilities, all phases covered
  - Verify: Cross-reference check passes
  - Depends: TK-007, TK-008, TK-009, TK-010, TK-011
  - Est: 0.5 HHW

## Task N - Final Verification (MANDATORY)

Run after all tasks complete:
- [ ] Verify separation of concerns (STRUT/EDIRD/TRACTFUL/AGEN/TDID)
- [ ] Verify workspace-wide CONSTANT uniqueness solution works
- [ ] Verify TASKS template integration complete
- [ ] All 7 problems in PROBLEMS.md addressed
- [ ] Run /verify workflow
- [ ] Update PROGRESS.md - mark complete

## Dependency Graph

```
TK-001 ─┬─> TK-003 ─> TK-007 ─┬─> TK-015 ─> TK-018
TK-002 ─┘                      │
TK-001 ─> TK-010 ─────────────┘
TK-002 ─> TK-011 ─> TK-016
TK-004 ─> TK-008 ─> TK-015
TK-005 ─> TK-009 ─> TK-015
TK-006 ─> TK-010

TK-014 ─┬─> TK-015
        ├─> TK-016
        └─> TK-017

TK-012 ─> TK-017
TK-013 ─> TK-017

TK-007, TK-008, TK-009, TK-010, TK-011 ─> TK-018
```

## Problem Coverage

- **PR-001** (Workflows depend on EDIRD): TK-002, TK-011, TK-016
- **PR-002** (Verbs cannot be extended): TK-001, TK-010
- **PR-003** (No central TOPIC registry): TK-005, TK-009
- **PR-004** (AGEN syntax ambiguity): TK-006, TK-010
- **PR-005** (IMPL plans too free): TK-007 (STRUT addresses this)
- **PR-006** (FAILS.md technical only): TK-007 (STRUT extends FAILS categories)
- **PR-007** (No AC in SPECs): TK-012

## Document History

**[2026-01-17 14:52]**
- Initial tasks plan created from session NOTES/PROBLEMS
