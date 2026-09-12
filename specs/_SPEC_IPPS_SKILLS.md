# SPEC: IPPS Skills

**Doc ID**: IPPSSKLS-SP01
**Goal**: Define the structure, GRUC file requirements, and compliance criteria for skills in the IPPS PromptSystem

**Depends on:**
- `docs/_INFO_GRUC_GUIDES_RULES_CHECKS.md [GRUC-IN01]` for GRUC file type definitions
- `.devin/skills/write-documents/SKILL_RULES.md` for skill document rules (SK-* IDs)
- `.devin/skills/write-documents/SKILL_GUIDES.md` for skill writing guidance

**Does not depend on:**
- `_SPEC_IPPS_WORKFLOWS.md [IPPSWFLW-SP01]` (workflows consume skills, not vice versa)

## Summary

- Skills are the primary capability unit in IPPS - each skill teaches an agent HOW and WHEN to use a tool or concept
- Every skill must implement a GRUC-compliant file set: SKILL.md (entry point), SKILL_RULES.md (output standards), optional SKILL_GUIDES.md (process guidance), optional SKILL_CHECKS.md (process discipline + quality improvement)
- Skills with complex decision-making must add SKILL_GUIDES.md; skills with quality-critical output must add SKILL_CHECKS.md
- EXAMPLE files are optional, linked from SKILL_GUIDES.md, showing larger GOOD examples
- `/verify` checks skill output against SKILL_RULES.md and SKILL_TEMPLATE.md (if exists); `/critique` reviews skill approach against SKILL_GUIDES.md; `/drift-detect` audits process against SKILL_CHECKS.md PD items; `/improve` applies SKILL_CHECKS.md QI items

## Table of Contents

1. [Skill Anatomy](#1-skill-anatomy)
2. [Required Files](#2-required-files)
3. [GRUC Files for Skills](#3-gruc-files-for-skills)
4. [Optional Files](#4-optional-files)
5. [Skill Types and GRUC Density](#5-skill-types-and-gruc-density)
6. [Consumer Mapping](#6-consumer-mapping)
7. [Design Decisions](#7-design-decisions)
8. [Acceptance Criteria](#8-acceptance-criteria)

## 1. Skill Anatomy

A skill is a folder under `[AGENT_FOLDER]/skills/` containing at minimum a `SKILL.md` entry point. Skills teach agents how to use tools, follow conventions, or execute domain-specific procedures.

**Skill folder structure (GRUC-complete):**

```
[skill-name]/
  SKILL.md              # Required: entry point, procedures, MNF, intent lookup
  SKILL_RULES.md        # Required: output standards with BAD/GOOD pairs
  SKILL_GUIDES.md       # Conditional: process guidance, decision steps
  SKILL_CHECKS.md       # Conditional: PD + QI items
  SKILL_TEMPLATE.md     # Optional: template for skill-specific documents
  SETUP.md              # Optional: installation (if tool requires it)
  UNINSTALL.md          # Required if SETUP.md exists
  [SKILLPREFIX]_*.md    # Skill-specific reference files
  [TOPIC]_EXAMPLE_*    # Optional: EXAMPLE files linked from GUIDES
```

## 2. Required Files

### IPPSSKLS-FR-01: SKILL.md Entry Point

Every skill must have a `SKILL.md` file as the entry point. Must follow `SKILL_RULES.md` (SK-HD-01 through SK-CT-06).

- YAML frontmatter with `name`, `description`, optional `compatibility`
- MUST-NOT-FORGET section (3-10 items, ordered by impact)
- Intent Lookup when skill covers multiple use cases
- Core Procedures with numbered steps
- References section listing all companion files

### IPPSSKLS-FR-02: SKILL_RULES.md Output Standards

Every skill must have a `SKILL_RULES.md` file defining output standards for artifacts produced using this skill.

- Rule Index at top with all rule IDs and one-line descriptions
- Every non-trivial rule has BAD/GOOD example pair
- Rule IDs use consistent prefix format: `[PREFIX]-[CATEGORY]-[NN]`
- Rules are testable (answerable yes/no for any given artifact)
- No Document History section (SK-CT-06)

### IPPSSKLS-FR-03: SKILL.md References Section

SKILL.md must list all companion GRUC files in its References section so consumers know what exists.

- Reference entries include filename and one-line purpose
- References section is the discovery mechanism for GRUC files

## 3. GRUC Files for Skills

### IPPSSKLS-FR-04: SKILL_GUIDES.md (Conditional)

Required when skill involves complex decision-making, multi-step strategies, or trade-offs.

- Numbered decision steps (not free prose)
- Each section is actionable (tells agent what to DO, not what to know)
- Links to EXAMPLE files if they exist
- References companion SKILL_RULES.md for verification
- No verification checklists (those belong in RULES)

### IPPSSKLS-FR-05: SKILL_CHECKS.md (Conditional)

Required when skill produces quality-critical output or when process discipline matters.

- Two sections: Process Discipline (PD) and Quality Improvement (QI)
- PD items: action + evidence + failure indicator
- QI items: quality question + improvement tip
- PD items reference rule IDs they verify
- QI items are judgment-based, not binary pass/fail
- Ordered by execution sequence
- Invisible to working agent during execution (gaming prevention)

### IPPSSKLS-FR-06: EXAMPLE Files (Optional)

EXAMPLE files show larger GOOD examples that go beyond simple BAD/GOOD pairs in RULES.

- Naming: `[TOPIC]_EXAMPLE_[NN]-[ExampleName].md`
- Complete or substantial documents showing the GOOD approach
- Use-case-specific (each example solves a specific problem type)
- Key decisions and rationale documented
- No BAD examples (BAD/GOOD pairs stay in RULES)
- Linked from SKILL_GUIDES.md, not consumed directly by any workflow

## 4. Optional Files

### IPPSSKLS-FR-07: SETUP.md and UNINSTALL.md

If skill requires system modification, SETUP.md is required. UNINSTALL.md is required if SETUP.md exists.

- SETUP.md must include pre-installation verification with checklist (SK-ST-05)
- Installation must be idempotent with backup-before-modify (SK-ST-06)
- UNINSTALL.md must include pre-uninstall verification (SK-ST-07)

### IPPSSKLS-FR-08: SKILL_TEMPLATE.md

Template files for skill-specific document types. Must use `_TEMPLATE` suffix (SK-FL-07).

### IPPSSKLS-FR-09: Skill-Specific Reference Files

Skill-specific reference files use uppercase prefix derived from skill domain (SK-FL-03). Example: `PLAYWRIGHT_TOOLS.md`, `RESEARCH_TOOLS.md`.

## 5. Skill Types and GRUC Density

### IPPSSKLS-DD-01: GRUC Density by Skill Type

Skill type determines which GRUC files are required:

- **Instructional** (multi-step procedures): SKILL.md + SKILL_RULES.md required; SKILL_GUIDES.md required if complex decisions; SKILL_CHECKS.md required if quality-critical
- **Resource/lookup** (URL collections, reference lists): SKILL.md + SKILL_RULES.md required; SKILL_GUIDES.md and SKILL_CHECKS.md typically not needed
- **Setup-heavy** (tool installation): SKILL.md + SKILL_RULES.md + SETUP.md + UNINSTALL.md required; SKILL_GUIDES.md and SKILL_CHECKS.md typically not needed

### IPPSSKLS-DD-02: GRUC File Placement

All GRUC files for a skill reside in the skill's own folder. No cross-skill GRUC references. Each skill is self-contained.

## 6. Consumer Mapping

### IPPSSKLS-IG-01: Workflow-to-GRUC Consumption

Per `GRUC-IG-01`, each workflow consumes exactly one GRUC file type from each skill. Exception: `/verify` consumes both RULES and TEMPLATE:

- `/verify` reads `SKILL_RULES.md` and `SKILL_TEMPLATE.md` (if exists) (structural compliance + template adherence)
- `/critique` reads `SKILL_GUIDES.md` only (strategic gap analysis) and links EXAMPLE files
- `/drift-detect` reads `SKILL_CHECKS.md` PD items only (process discipline)
- `/improve` reads `SKILL_CHECKS.md` QI items only (quality improvement)

### IPPSSKLS-IG-02: Working Agent Access

Per `GRUC-FR-03` and `GRUC-IG-03`, the working agent reads `SKILL.md` and `SKILL_GUIDES.md` (if exists) before and during execution. The working agent must NOT read `SKILL_CHECKS.md` during execution (gaming prevention).

### IPPSSKLS-IG-03: No Content Replication

Per `GRUC-IG-02`, GRUC files must not replicate content from each other. Reference by ID, never copy.

## 7. Design Decisions

### IPPSSKLS-DD-03: Why SKILL_RULES.md Is Always Required

Every skill produces some output (code, documents, configurations). Output must be verifiable. Without RULES, `/verify` has no standards to check against. Even resource/lookup skills need rules for entry format and reference quality.

### IPPSSKLS-DD-04: Why SKILL_GUIDES.md Is Conditional

Not all skills involve decision-making. Resource/lookup skills are direct lookups with no strategic choices. Forcing GUIDE files on them adds noise without value. The trigger for requiring GUIDE: "Does the agent need to make decisions about HOW to approach the task?"

### IPPSSKLS-DD-05: Why SKILL_CHECKS.md Is Conditional

Not all skills have quality-critical process steps. Simple lookups and direct tool invocations have no process discipline to audit. The trigger for requiring CHECKS: "Does it matter HOW the agent arrived at the output, or only that the output is correct?"

## 8. Acceptance Criteria

### IPPSSKLS-AC-01: Skill Has Required Files

- [ ] SKILL.md exists and follows SK-HD-01 through SK-CT-06
- [ ] SKILL_RULES.md exists with Rule Index and BAD/GOOD pairs
- [ ] SKILL.md References section lists all companion GRUC files

### IPPSSKLS-AC-02: Conditional GRUC Files Present When Required

- [ ] If skill involves complex decisions: SKILL_GUIDES.md exists with numbered decision steps
- [ ] If skill produces quality-critical output: SKILL_CHECKS.md exists with PD + QI sections
- [ ] If SETUP.md exists: UNINSTALL.md also exists

### IPPSSKLS-AC-03: GRUC Separation Enforced

- [ ] SKILL_RULES.md contains no process guidance (that belongs in GUIDES)
- [ ] SKILL_GUIDES.md contains no output standards (that belongs in RULES)
- [ ] SKILL_CHECKS.md PD items reference rule IDs from RULES, not duplicate content
- [ ] SKILL_CHECKS.md is not referenced in SKILL.md procedures (gaming prevention)

### IPPSSKLS-AC-04: EXAMPLE Files Follow Convention

- [ ] EXAMPLE files use naming `[TOPIC]_EXAMPLE_[NN]-[ExampleName].md`
- [ ] EXAMPLE files are linked from SKILL_GUIDES.md
- [ ] EXAMPLE files contain no BAD examples

## Document History

**[2026-09-12 14:40]**
- Changed: IG-01 updated to reflect `/verify` consumes RULES and TEMPLATE per GRUC-IG-01
- Changed: Summary updated for `/verify` + TEMPLATE

**[2026-09-12 14:30]**
- Fixed: IG-01, IG-02, IG-03 now reference GRUC standard by ID instead of re-defining (SOCAS-03)

**[2026-09-12 14:00]**
- Initial specification created
