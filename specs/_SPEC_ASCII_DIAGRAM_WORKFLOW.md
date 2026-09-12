# SPEC: ASCII Diagram Workflow

**Doc ID**: ASCIIART-SP01
**Feature**: ascii-diagram-workflow
**Goal**: Specify the ascii-diagram workflow, its GRUC file set, example files, and scripts for creating and fixing ASCII art diagrams in markdown

**Timeline**: Created 2026-09-12

**Target file(s)**:
- `PromptSystemV4.4/workflows/ascii-diagram.md`
- `PromptSystemV4.4/skills/write-documents/ASCII_ART_GUIDES.md`
- `PromptSystemV4.4/skills/write-documents/ASCII_ART_RULES.md`
- `PromptSystemV4.4/skills/write-documents/ASCII_ART_CHECKS.md`
- `PromptSystemV4.4/skills/write-documents/ASCII_ART_EXAMPLES_*.md`
- `PromptSystemV4.4/skills/write-documents/SetAsciiBoxStyle.ps1`

**Depends on:**
- `specs/_SPEC_GRUC_STANDARD.md [GRUC-SP01]` for GRUC file type definitions, structure, and consumer mapping
- `docs/_INFO_GRUC_GUIDES_RULES_CHECKS.md [GRUC-IN01]` for GRUC explanatory companion
- `.devin/skills/write-documents/SPEC_TEMPLATE.md` for SPEC document structure
- `.devin/rules/core-conventions.md` for Unicode box-drawing character rules

**Does not depend on:**
- `specs/_SPEC_IPPS_SKILLS.md [IPPSSKLS-SP01]` (skill infrastructure, not ASCII art content)
- `specs/_SPEC_IPPS_WORKFLOWS.md [IPPSWFLW-SP01]` (workflow infrastructure, not ASCII art content)

## MUST-NOT-FORGET

- All GRUC files follow GRUC-SP01 structure and consumer mapping
- CHECKS files are invisible to the working agent during execution (GRUC-FR-03, GRUC-IG-03)
- EXAMPLE files are linked from GUIDES, not consumed directly by workflows (GRUC-FR-09)
- All content must be generic - no project-specific data (Pre-Write Privacy Gate)
- Unicode box-drawing characters are the default per core-conventions.md
- Postpone md.py - develop individual PowerShell scripts per problem, consolidate later

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Design Decisions](#6-design-decisions)
7. [Implementation Guarantees](#7-implementation-guarantees)
8. [Key Mechanisms](#8-key-mechanisms)
9. [Action Flow](#9-action-flow)
10. [Technical Constraints](#10-technical-constraints)
11. [Acceptance Criteria](#11-acceptance-criteria)
12. [Logging Requirements](#12-logging-requirements)
13. [Document History](#13-document-history)

## 1. Scenario

**Problem:** Agents produce inconsistent ASCII art diagrams with frame glitches, mixed character sets, broken alignment, and wrong character tiers. No standardized process exists for creating, editing, or fixing diagrams. The existing 2331-line research document is too large to load into agent context during writing workflows.

**Solution:**
- Split research into concise GRUC files (GUIDES, RULES, CHECKS) in the write-documents skill
- Group worked examples by topic into EXAMPLE files (charts, UX design, architecture, etc.)
- Provide a thin `ascii-diagram.md` workflow with two modes: create and fix
- Provide PowerShell scripts for automated frame detection and style conversion
- Agent decides when to load EXAMPLE files - they are not mandatory

**What we don't want:**
- A single monolithic file loaded into every writing workflow (token waste)
- EXAMPLE files mandatory for every diagram creation (token waste when simple diagrams suffice)
- md.py monolith before individual scripts are proven (premature consolidation)
- ASCII art in a separate skill (fragments the write-documents skill)
- Rules mixed with guides or checks (violates GRUC separation)

## 2. Context

The write-documents skill currently has 14 RULES files, 6 GUIDES files, and multiple TEMPLATE files. No CHECKS or EXAMPLE files exist yet. The ASCII art GRUC set will be the first complete GRUC implementation (GUIDE + RULES + CHECKS + EXAMPLES) in the skill, serving as a reference implementation for GRUC-SP01.

The existing `ASCII_ART_GUIDES.md` (2331 lines, Doc ID `LANAV2DGRM-IN01`) in the session folder is research material. It must be split: concise operational content goes into the GRUC files; deep research stays as a reference INFO document in `docs/`.

PROBLEMS.md item 12 (DVSYS-FT-0001) defines the original requirements: guides, rules, templates, scripts, and a workflow for ASCII art diagrams and UX designs.

## 3. Domain Objects

### GRUC File Set

A **GRUC File Set** is the collection of GUIDE, RULES, CHECKS, and EXAMPLE files for one domain within a skill.

**Storage:** `PromptSystemV4.4/skills/write-documents/`
**Definition:** This SPEC

**Key properties:**
- `ASCII_ART_GUIDES.md` - High-level tips, common problems with solutions, example lookup. Consumer: working agent (before), `/critique` (after)
- `ASCII_ART_RULES.md` - Concrete verification rules with BAD/GOOD pairs. Consumer: `/verify`
- `ASCII_ART_CHECKS.md` - High-level checks of diagram optimality with improvement tips. Consumer: `/drift-detect` (PD), `/improve` (QI)
- `ASCII_ART_EXAMPLES_*.md` - Worked examples grouped by topic. Consumer: linked from GUIDES, referenced by `/critique`

### Example File

An **Example File** shows complete or substantial GOOD diagrams for a specific topic.

**Naming:** `ASCII_ART_EXAMPLES_[TOPIC].md` where TOPIC is uppercase topic name (e.g., `CHARTS`, `UXDESIGN`, `ARCHITECTURE`, `STATEMACHINE`)

**Key properties:**
- Each file contains multiple worked examples for one diagram category
- Linked from `ASCII_ART_GUIDES.md` at the relevant decision point
- Agent decides when to load - not mandatory for simple diagrams
- No BAD examples (BAD/GOOD pairs stay in RULES)

### Reference INFO Document

A **Reference INFO Document** contains the deep research material, too large for skill loading.

**Storage:** `docs/_INFO_ASCII_ART_DIAGRAMS.md`
**Doc ID:** `ASCIIART-IN01`

**Key properties:**
- Contains: full research, sources, all worked examples, image-generation guidance
- Not loaded during writing workflows
- Read when creating new diagram types or troubleshooting
- Source material from which GRUC files are distilled

### Helper Script

A **Helper Script** is a PowerShell script for automated ASCII art formatting tasks.

**Storage:** `PromptSystemV4.4/skills/write-documents/`
**Key properties:**
- `SetAsciiBoxStyle.ps1` - Detects and converts box styles (plain/unicode, normal/dotted/dashed/double/heavy/rounded)
- Future scripts added per-problem, consolidated into md.py later

## 4. Functional Requirements

**ASCIIART-FR-01: Two Workflow Modes**

The `ascii-diagram.md` workflow must support two modes determined by verb semantics:
- **Create mode** ("create", "add") - Creates new ASCII art diagrams based on context and guides
- **Fix mode** ("fix", "change", "modify", "set") - Changes existing ASCII diagrams, uses scripts to solve formatting problems and verify formatting

**ASCIIART-FR-02: GRUC File Set in write-documents**

All GRUC files must reside in `PromptSystemV4.4/skills/write-documents/`:
- `ASCII_ART_GUIDES.md` - High-level tips, common problems with solutions, example lookup references
- `ASCII_ART_RULES.md` - Concrete verification rules with BAD/GOOD pairs, checkable from output alone
- `ASCII_ART_CHECKS.md` - PD items (process discipline) and QI items (quality improvement with tips)

**ASCIIART-FR-03: Example Files Grouped by Topic**

Example files must be grouped by diagram topic:
- `ASCII_ART_EXAMPLES_CHARTS.md` - Bar charts, sparklines, proportion bars
- `ASCII_ART_EXAMPLES_UXDESIGN.md` - UI mockups, wireframes, modal dialogs
- `ASCII_ART_EXAMPLES_ARCHITECTURE.md` - System architecture, component diagrams, layer diagrams
- `ASCII_ART_EXAMPLES_STATEMACHINE.md` - State machines, flowcharts, decision trees
- Additional topic files added as needed

**ASCIIART-FR-04: Example Files Not Mandatory**

The workflow and SKILL.md must not make EXAMPLE files mandatory reads. The agent must decide when to load examples based on diagram complexity and familiarity with the diagram type.

**ASCIIART-FR-05: Example Lookup in GUIDES and CHECKS**

`ASCII_ART_GUIDES.md` must contain an example lookup section listing available example files with one-line descriptions and the wildcard pattern to find them.

`ASCII_ART_CHECKS.md` QI items must reference example files as improvement tips when a diagram could benefit from a specific example pattern.

**ASCIIART-FR-06: Wildcard Pattern in Workflow**

The `ascii-diagram.md` workflow must note the wildcard pattern `ASCII_ART_EXAMPLES_*.md` so the agent can discover available example files by listing the skill folder.

**ASCIIART-FR-07: Reference INFO Document**

The deep research material must be moved to `docs/_INFO_ASCII_ART_DIAGRAMS.md` with Doc ID `ASCIIART-IN01`. This file is not loaded during writing workflows. It serves as reference material for creating new GRUC content or troubleshooting.

**ASCIIART-FR-08: Helper Scripts in write-documents**

PowerShell scripts must reside in `PromptSystemV4.4/skills/write-documents/` alongside the GRUC files. Scripts are called by the fix mode of the workflow.

**ASCIIART-FR-09: SKILL.md Verb Mapping**

The write-documents `SKILL.md` must add a verb mapping entry:
- `[ASCII-DIAGRAM]` - Create or fix ASCII art diagrams (read `ASCII_ART_GUIDES.md` before execution; `ASCII_ART_RULES.md` consumed by `/verify` post-execution)

**ASCIIART-FR-10: GRUC Compliance**

All GRUC files must comply with GRUC-SP01:
- GUIDE follows GRUC-FR-16 structure (numbered decision steps, review checklist, example links)
- RULES follows GRUC-FR-15 structure (rule index, BAD/GOOD pairs, checkable from output)
- CHECKS follows GRUC-FR-17 structure (PD section with action+evidence+failure, QI section with question+tip)
- EXAMPLES follow GRUC-FR-18 structure (context, document, key decisions)

## 5. Non-Functional Requirements

**ASCIIART-NFR-01: GRUC File Conciseness**

- `ASCII_ART_GUIDES.md` must not exceed 150 lines
- `ASCII_ART_RULES.md` must not exceed 300 lines
- `ASCII_ART_CHECKS.md` must not exceed 100 lines
- Verification: line count check

**ASCIIART-NFR-02: Character Compliance**

All diagrams in GRUC files and examples must use Unicode box-drawing characters per `core-conventions.md`. No ASCII `+` `-` `|` for boxes. No `▼` (U+25BC); use `v` instead. Arrow `→` must have spaces: `A → B`.

**ASCIIART-NFR-03: Generic Content**

All content in GRUC files, examples, and scripts must be generic. No project-specific data, paths, or identifiers. Pre-Write Privacy Gate applies.

## 6. Design Decisions

**ASCIIART-DD-01: All files in write-documents, no separate skill.** Rationale: User explicitly requested no extra skill. ASCII art is a writing concern, belongs with document writing.

**ASCIIART-DD-02: Postpone md.py, develop individual PowerShell scripts.** Rationale: Individual scripts are easier to test and iterate. Consolidation into md.py happens after scripts are proven. Avoids premature monolith.

**ASCIIART-DD-03: Examples not mandatory, agent decides.** Rationale: Simple diagrams (tree, basic flow) do not need example lookup. Making examples mandatory would waste tokens on every diagram creation. Agent loads examples when facing unfamiliar diagram types or complex layouts.

**ASCIIART-DD-04: Example lookup in GUIDES and CHECKS, not in workflow.** Rationale: GUIDES are read before execution (agent discovers examples there). CHECKS QI items suggest examples as improvement tips. The workflow only notes the wildcard pattern for discovery. This follows GRUC consumer mapping: GUIDE → working agent, CHECKS QI → `/improve`.

**ASCIIART-DD-05: Split research from operational GRUC.** Rationale: The 2331-line research document is too large for context loading during writing workflows. Concise GRUC files (total under 550 lines) provide operational guidance. Deep research stays as reference INFO in `docs/`.

**ASCIIART-DD-06: Example files use topic grouping, not sequential numbering.** Rationale: `ASCII_ART_EXAMPLES_CHARTS.md` is self-describing. `ASCII_ART_EXAMPLES_01.md` is not. Topic grouping makes discovery via wildcard intuitive.

## 7. Implementation Guarantees

**ASCIIART-IG-01:** The workflow must not reference `ASCII_ART_CHECKS.md` in any step the working agent executes. CHECKS are invisible during execution per GRUC-IG-03.

**ASCIIART-IG-02:** The workflow must not reference `ASCII_ART_RULES.md` in any step. RULES are consumed by `/verify` only, per GRUC-FR-02. Fix mode may suggest running `/verify` post-repair but must not load RULES directly.

**ASCIIART-IG-03:** Example files must be linked from `ASCII_ART_GUIDES.md` only, not from RULES or CHECKS, per GRUC-FR-08.

## 8. Key Mechanisms

### Workflow Mode Detection

The `ascii-diagram.md` workflow detects mode from the user's verb:
- "create", "add" → create mode: read `ASCII_ART_GUIDES.md`, choose diagram type, draw, optionally load examples
- "fix", "change", "modify", "set" → fix mode: identify existing diagram, run scripts for formatting issues, suggest `/verify` for rule compliance

### Example Discovery

Agent discovers example files via:
1. Wildcard pattern `ASCII_ART_EXAMPLES_*.md` noted in the workflow
2. Example lookup section in `ASCII_ART_GUIDES.md` listing available files with descriptions
3. QI items in `ASCII_ART_CHECKS.md` suggesting specific example files as improvement tips

### Script Integration

Fix mode calls PowerShell scripts from the write-documents skill folder:
- `SetAsciiBoxStyle.ps1` - Convert between box styles (plain/unicode variants)
- Future scripts added per-problem (frame alignment, width detection, etc.)

## 9. Action Flow

### Create Mode

```
User says "create" or "add" diagram
├─> Read ASCII_ART_GUIDES.md
│   ├─> Classify diagram type (tree, flow, layers, swimlane, state, UI, chart)
│   ├─> Choose character tier (Tier 2 Unicode default)
│   └─> Decide: load example file? (agent discretion)
│       ├─> Yes: read ASCII_ART_EXAMPLES_[TOPIC].md
│       └─> No: proceed with guides knowledge
├─> Draw diagram following guides
├─> Self-verify alignment, character consistency, width limits
└─> Insert into target document
```

### Fix Mode

```
User says "fix", "change", "modify", or "set" diagram
├─> Identify existing diagram in file (line range)
├─> Detect problem type (frame glitch, wrong style, mixed chars, alignment)
├─> Run appropriate script
│   ├─> SetAsciiBoxStyle.ps1 (style conversion)
│   └─> Future scripts (frame repair, width check, etc.)
├─> Apply script output to diagram
└─> Suggest running /verify for rule compliance
```

## 10. Technical Constraints

- All GRUC files use `ASCIIART` as the ID prefix (e.g., `ASCIIART-FR-01`, `ASCIIART-DD-01`)
- Rule IDs in `ASCII_ART_RULES.md` use 2-letter category prefixes (e.g., `AA-CH-01` for Characters, `AA-ST-01` for Structure)
- Scripts must have `-DryRun` mode for preview before applying changes
- Scripts must accept `-Path`, `-FirstLine`, `-LastLine` parameters for targeting specific diagrams
- Scripts must use UTF-8 encoding for all file I/O
- The reference INFO document (`docs/_INFO_ASCII_ART_DIAGRAMS.md`) is not referenced by the workflow or SKILL.md

## 11. Acceptance Criteria

### ASCIIART-AC-01: GRUC File Set Complete

- [ ] `ASCII_ART_GUIDES.md` exists in `PromptSystemV4.4/skills/write-documents/`
- [ ] `ASCII_ART_RULES.md` exists in same folder
- [ ] `ASCII_ART_CHECKS.md` exists in same folder
- [ ] At least one `ASCII_ART_EXAMPLES_*.md` file exists
- [ ] All files comply with GRUC-SP01 structures (GRUC-FR-15 through FR-19)

### ASCIIART-AC-02: GRUC Consumer Mapping Correct

- [ ] `ascii-diagram.md` workflow references only `ASCII_ART_GUIDES.md` (not RULES, not CHECKS)
- [ ] No workflow step executed by the working agent references `ASCII_ART_CHECKS.md`
- [ ] No workflow step references `ASCII_ART_RULES.md` directly
- [ ] EXAMPLE files linked from GUIDES only, not from RULES or CHECKS

### ASCIIART-AC-03: Workflow Two Modes

- [ ] Create mode activates on "create" or "add" verbs
- [ ] Fix mode activates on "fix", "change", "modify", or "set" verbs
- [ ] Create mode reads `ASCII_ART_GUIDES.md` before drawing
- [ ] Fix mode runs scripts and suggests `/verify` post-repair

### ASCIIART-AC-04: Example Files Correct

- [ ] Example files follow naming: `ASCII_ART_EXAMPLES_[TOPIC].md`
- [ ] Example files contain no BAD examples
- [ ] Example files are linked from `ASCII_ART_GUIDES.md`
- [ ] Example files are not mandatory reads in workflow or SKILL.md
- [ ] Wildcard pattern `ASCII_ART_EXAMPLES_*.md` noted in workflow

### ASCIIART-AC-05: Conciseness Limits

- [ ] `ASCII_ART_GUIDES.md` does not exceed 150 lines
- [ ] `ASCII_ART_RULES.md` does not exceed 300 lines
- [ ] `ASCII_ART_CHECKS.md` does not exceed 100 lines

### ASCIIART-AC-06: Character Compliance

- [ ] All diagrams in GRUC files and examples use Unicode box-drawing characters
- [ ] No ASCII `+` `-` `|` for boxes in any GRUC or example file
- [ ] No `▼` (U+25BC) in any GRUC or example file
- [ ] Arrow `→` has spaces in all files: `A → B`

### ASCIIART-AC-07: Generic Content

- [ ] No project-specific data, paths, or identifiers in any GRUC, example, or script file
- [ ] No real names, addresses, or session-specific references in illustrative content

### ASCIIART-AC-08: SKILL.md Integration

- [ ] `SKILL.md` contains `[ASCII-DIAGRAM]` verb mapping
- [ ] Verb mapping references `ASCII_ART_GUIDES.md` for pre-execution reading
- [ ] Verb mapping does not make RULES or CHECKS mandatory during execution

## 12. Logging Requirements

N/A: This SPEC defines document structure, workflow steps, and GRUC file content. The PowerShell scripts produce console output but are not specified here - script logging belongs in the script implementation and `@skills:coding-conventions` logging rules.

## 13. Document History

**[2026-09-12 16:30]**
- Fixed: IG-02 expanded from "creation steps" to "any step" - RULES consumed by `/verify` only, fix mode suggests `/verify` instead of loading RULES directly (GRUC-FR-02 compliance)
- Fixed: Key Mechanisms and Action Flow fix mode no longer reference `ASCII_ART_RULES.md` directly
- Added: Acceptance Criteria section (8 AC groups, 33 checklist items) following GRUC-SP01 pattern

**[2026-09-12 16:15]**
- Fixed: FR-09 verb mapping clarified - RULES consumed by `/verify` post-execution, not by working agent during creation (SOCAS-02)
- Added: Logging Requirements section (SPEC-LG-01 compliance)
- Fixed: TOC updated for new section numbering

**[2026-09-12 15:55]**
- Initial specification created
