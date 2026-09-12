# SPEC: IPPS Templates

**Doc ID**: IPPSTMPL-SP01
**Goal**: Define the structure, GRUC file requirements, and compliance criteria for templates in the IPPS PromptSystem

**Depends on:**
- `specs/_SPEC_GRUC_STANDARD.md [GRUC-SP01]` for GRUC file type definitions
- `.devin/skills/write-documents/TEMPLATE_RULES.md` for template document rules (TMPL-* IDs)
- `.devin/skills/write-documents/TEMPLATE_GUIDES.md` for template writing guidance

**Does not depend on:**
- `specs/_SPEC_IPPS_SKILLS.md [IPPSSKLS-SP01]` (skills produce templates, this SPEC defines templates)

## Summary

- Templates are skeleton documents that agents copy, fill in, and strip of XML comments to produce output documents
- Every template IS the document - every line is either template content or an XML comment annotation
- Templates do not teach - rules and guidance belong in companion `*_RULES.md` and `*_GUIDES.md` files
- `/verify` checks instantiated output against `TEMPLATE_RULES.md` and `*_TEMPLATE.md` (template adherence)
- `/drift-detect` audits template creation process against `TEMPLATE_CHECKS.md` PD items
- `/improve` applies `TEMPLATE_CHECKS.md` QI items to improve template quality

## Table of Contents

1. [Template Anatomy](#1-template-anatomy)
2. [Required Files](#2-required-files)
3. [GRUC Files for Templates](#3-gruc-files-for-templates)
4. [Template Categories](#4-template-categories)
5. [Consumer Mapping](#5-consumer-mapping)
6. [Design Decisions](#6-design-decisions)
7. [Acceptance Criteria](#7-acceptance-criteria)

## 1. Template Anatomy

A template is a markdown file with `_TEMPLATE` suffix that serves as a skeleton for a specific document type. Templates live in the skill folder that produces the document type.

**Template structure:**

```
[DOCUMENT_TYPE]_TEMPLATE.md
  <!-- Top comment block (optional: naming, lifecycle) -->
  # [Document Title]: [PLACEHOLDER]
  **Doc ID**: [TOPIC]-[TYPE][NN]           (per-task only)
  <!-- Topic ID XML comment -->             (per-task only)
  **Goal**: [Single sentence]
  ## [Section 1]
  <!-- Inline annotation -->
  [Template content with [PLACEHOLDERS]]
  ## Document History                       (per-task only)
  <!-- EXAMPLE: Reference only -->
  ## Full Example                           (when 3+ sections)
```

## 2. Required Files

### IPPSTMPL-FR-01: TEMPLATE File

Every template must use `_TEMPLATE.md` suffix (documents) or `_template.ext` suffix (scripts) per SK-FL-07.

### IPPSTMPL-FR-02: Companion RULES File

Every template must have a companion `*_RULES.md` file defining output standards for the document type. Templates reference rules by ID, never inline them.

### IPPSTMPL-FR-03: Companion GUIDES File

Templates with complex decision-making (conditional sections, dynamic components) must have a companion `*_GUIDES.md` file providing process guidance for template creation.

## 3. GRUC Files for Templates

### IPPSTMPL-FR-04: TEMPLATE_RULES.md

Defines output standards for templates. Must contain:

- Rule Index at top with all TMPL-* rule IDs and one-line descriptions
- BAD/GOOD example pairs for every non-trivial rule
- Rules are testable (answerable yes/no for any given template)
- No Document History section

### IPPSTMPL-FR-05: TEMPLATE_GUIDES.md

Provides process guidance for writing templates. Must contain:

- Numbered decision steps for template construction
- Annotation type guidance (removal instructions, conditional sections, inline rules)
- Placeholder type guidance
- Exemplar template references
- References companion TEMPLATE_RULES.md for verification

### IPPSTMPL-FR-06: TEMPLATE_CHECKS.md (Conditional)

Required when template quality is critical. Contains:

- Process Discipline (PD) items: action + evidence + failure indicator, referencing TMPL-* rule IDs
- Quality Improvement (QI) items: quality question + improvement tip
- Invisible to working agent during template creation (gaming prevention)

### IPPSTMPL-FR-07: EXAMPLE Files (Optional)

EXAMPLE files show complete filled-in documents demonstrating template instantiation. Linked from TEMPLATE_GUIDES.md, not consumed directly by any workflow.

- Naming: `[TOPIC]_EXAMPLE_[NN]-[ExampleName].md`
- Show a correctly completed instance, not the template itself
- Use generic data per privacy rules

## 4. Template Categories

### IPPSTMPL-DD-01: Per-Task vs Other Templates

Templates fall into two categories with different required fields:

**Per-task documents** (created once per task, versioned, Doc ID referenced):
- Templates: INFO, SPEC, IMPL, TEST, TASKS, REVIEW, MINTO, DEFERRED_IMPROVEMENTS, FIXES
- Required fields: Doc ID, Topic ID comment, Goal, Timeline, Document History
- MUST-NOT-FORGET section required for planning documents (SPEC, IMPL, TEST)

**Other templates** (tracking logs, scaffolding, reusable artifacts, embedded notation):
- Templates: FAILS, LEARNINGS, MINTO-DRAFT, CONVERSATION, SKILL, WORKFLOW, STRUT
- No Doc ID, no Timeline, no Document History
- Template IS the document format, not a per-task instance

### IPPSTMPL-DD-02: Template File Placement

Templates reside in the skill folder that produces the document type. No cross-skill template references. Each skill is self-contained with its own templates.

Examples:
- `write-documents/SPEC_TEMPLATE.md` - SPEC document template
- `write-documents/INFO_TEMPLATE.md` - INFO document template
- `session-management/NOTES_TEMPLATE.md` - Session notes template
- `drift-control/DRIFT_TEMPLATE.md` - Drift tracking template

## 5. Consumer Mapping

### IPPSTMPL-IG-01: Workflow-to-GRUC Consumption

Per `GRUC-IG-01`, each workflow consumes exactly one GRUC file type for templates. Exception: `/verify` consumes both RULES and TEMPLATE:

- `/verify` reads `TEMPLATE_RULES.md` (template rule compliance) and `*_TEMPLATE.md` (template adherence check, if template exists)
- `/critique` reads `TEMPLATE_GUIDES.md` only (strategic gap analysis for template design)
- `/drift-detect` reads `TEMPLATE_CHECKS.md` PD items only (process discipline for template creation)
- `/improve` reads `TEMPLATE_CHECKS.md` QI items only (quality improvement for templates)

### IPPSTMPL-IG-02: Working Agent Access

The working agent reads `*_TEMPLATE.md` files before and during document creation (to copy and fill in). The working agent must NOT read `TEMPLATE_CHECKS.md` during template creation (gaming prevention).

### IPPSTMPL-IG-03: No Content Replication

Per `GRUC-IG-02`, template GRUC files must not replicate content. RULES define template standards, GUIDES define template writing strategy, CHECKS define process audit. Reference by ID, never copy.

## 6. Design Decisions

### IPPSTMPL-DD-03: Why Templates Are Not RULES

Templates define structure (what sections exist). RULES define standards (what makes each section correct). Mixing them creates files that are both skeleton and rulebook, confusing the agent: does it copy the template or follow the rules? Separation means the agent copies the template and `/verify` checks the result against RULES.

### IPPSTMPL-DD-04: Why Templates Use XML Comments for Annotations

XML comments are invisible in rendered output. Bracket markers `[conditional - ...]` overlap with placeholder convention `[value to fill]`, creating polysemy (AP-NM-01). Italic markers `*(text)*` are visible noise in rendered output (SOCAS-08). XML comments are the only format that is both unambiguous and invisible.

### IPPSTMPL-DD-05: Why Templates Do Not Teach

Templates are copied and filled in. Teaching content (BAD/GOOD pairs, rule explanations, decision trees) would be preserved in the output if not wrapped in XML comments. Even wrapped, it adds noise. Complex rules belong in companion `*_RULES.md` or `*_GUIDES.md` files, referenced by ID.

### IPPSTMPL-DD-06: Why Full Examples Are at the End

A full example shows what a correctly completed document looks like, resolving ambiguities that instructions alone cannot. Placing it at the end with `<!-- EXAMPLE: -->` annotation prevents the agent from copying it into the output. The example is reference only.

## 7. Acceptance Criteria

### IPPSTMPL-AC-01: Template Has Required Files

- [ ] `*_TEMPLATE.md` exists with `_TEMPLATE` suffix (SK-FL-07)
- [ ] Companion `*_RULES.md` exists with Rule Index and BAD/GOOD pairs
- [ ] If template has complex decisions: companion `*_GUIDES.md` exists with numbered decision steps

### IPPSTMPL-AC-02: Template Structure Correct

- [ ] Template IS the document, not a meta-wrapper (TMPL-ST-01)
- [ ] No prose between sections (TMPL-ST-02)
- [ ] No meta-headings describing sections (TMPL-ST-03)
- [ ] Repeatable items show one instance (TMPL-ST-04)
- [ ] Complex rules in companion files, not inline (TMPL-ST-06)

### IPPSTMPL-AC-03: Annotations Correct

- [ ] All annotations use XML comments (TMPL-AN-01)
- [ ] Conditional sections have criteria and rule reference (TMPL-AN-02)
- [ ] No bracket markers or italic markers (TMPL-AN-03, TMPL-AN-04)
- [ ] No inline BAD/GOOD examples as content (TMPL-AN-05)
- [ ] No instruction sections disguised as content (TMPL-AN-06)

### IPPSTMPL-AC-04: Placeholders and Header Correct

- [ ] Values and IDs use bracket notation (TMPL-PH-01)
- [ ] Date patterns use format directly, no brackets (TMPL-PH-02)
- [ ] Doc ID present for per-task templates, absent for others (TMPL-HD-02)
- [ ] Topic ID XML comment after Doc ID for per-task templates (TMPL-HD-03)
- [ ] Target file(s) uses plural with list format (TMPL-HD-04)

### IPPSTMPL-AC-05: Category-Specific Fields Correct

- [ ] Per-task templates have Doc ID, Timeline, Document History (TMPL-SN-01)
- [ ] Planning templates (SPEC, IMPL, TEST) have MUST-NOT-FORGET (TMPL-SN-02)
- [ ] Templates with 4+ numbered sections have Table of Contents (TMPL-SN-03)
- [ ] Other templates (FAILS, LEARNINGS, etc.) do NOT have per-task fields

### IPPSTMPL-AC-06: GRUC Separation Enforced

- [ ] TEMPLATE_RULES.md contains no process guidance (belongs in GUIDES)
- [ ] TEMPLATE_GUIDES.md contains no output standards (belongs in RULES)
- [ ] TEMPLATE_CHECKS.md PD items reference rule IDs from RULES, not duplicate content
- [ ] TEMPLATE_CHECKS.md is not referenced in template creation steps (gaming prevention)

## Document History

**[2026-09-12 14:50]**
- Initial specification created
