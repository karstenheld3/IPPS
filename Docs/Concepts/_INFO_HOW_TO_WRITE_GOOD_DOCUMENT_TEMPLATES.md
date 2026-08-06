# INFO: How to Write Good Document Templates

**Doc ID**: DOCTMPLS-IN01
**Goal**: Define patterns and rules for writing unambiguous document templates that agents can reliably instantiate
**Timeline**: Created 2026-08-05, Updated 1 time (2026-08-06)

## Summary

**Core pattern:**
- Template IS the document skeleton; all annotations use XML comments, no exceptions [VERIFIED]
- Placeholders use `[BRACKETS]` for values; conditional sections use `<!-- Conditional: ... -->` [VERIFIED]
- Full examples in fenced code blocks with `<!-- EXAMPLE: Reference only -->` annotation [VERIFIED]
- Complex rules belong in `*_RULES.md` or `*_GUIDE.md` companion files [VERIFIED]

**Header and structural standards (per-task documents only):**
- `**Doc ID**:` without suffixes; Topic ID XML comment for nested ID guidance [VERIFIED]
- `**Target file(s)**:` with list format; `**Timeline**:` for versioned documents [VERIFIED]
- Document History required in all per-task document templates [VERIFIED]
- Per-task: INFO, SPEC, IMPL, TEST, TASKS, REVIEW, MINTO, DEFERRED, FIXES [VERIFIED]

## Table of Contents

1. [Why Template Design Matters](#1-why-template-design-matters)
2. [Core Principle](#2-core-principle)
3. [Template Structure](#3-template-structure)
4. [Annotation Techniques](#4-annotation-techniques)
5. [Header Block Standards](#5-header-block-standards)
6. [Structural Section Standards](#6-structural-section-standards)
7. [Anti-Patterns](#7-anti-patterns)
8. [Template Audit Checklist](#8-template-audit-checklist)
9. [Sources](#9-sources)
10. [Document History](#10-document-history)

## 1. Why Template Design Matters

Templates are the DNA of a documentation system. Every document an agent produces is an instantiation of a template. If the template is ambiguous, every output inherits that ambiguity. If annotation formats drift, agents interpret the drift as intentional signal (Minimal Explicit Consistent Terminology - MECT: "readers interpret ALL variation as intentional") and produce inconsistent documents.

This creates a compounding problem. Unlike code, where a bug is fixed once, template inconsistencies multiply through usage. A `[conditional - ...]` marker in one template and a `<!-- Conditional: ... -->` in another teaches the agent that both formats are valid. The agent then produces documents mixing both formats. A downstream `/verify` run finds the mixed formats and cannot determine which is correct because both exist in authoritative sources. The cost of NOT standardizing templates compounds with every document produced.

**Connection to MECT, APAPALAN (As Precise As Possible, As Little As Necessary), SOCAS (Signs of Confusion and Sloppiness), and GRUC (Guides, Rules, Checks):**

- **MECT Signal vs Noise** - Every formatting choice in a template is either signal (carries information) or noise (arbitrary variation the reader misinterprets). Inconsistent annotation formats are noise that agents amplify. See `_INFO_MECT_PHILOSOPHY.md [MECT-IN01]` section 2.2.
- **APAPALAN AP-PR-09** - "Repeat established structures. Do not invent new forms for similar content." Templates ARE the established structures. If the template itself uses inconsistent forms, no downstream document can be consistent. See `_INFO_APAPALAN_PRINCIPLE.md [APAPALAN-IN01]` section 4.1.
- **SOCAS-08** - Information vs Noise Imbalance. Template annotations that look like content (italic markers, bracket markers) are noise that the agent may preserve in output. XML comments are automatically filtered - zero noise leakage risk.
- **GRUC boundary** - This document defines WHAT templates must look like (RULES territory). HOW to write them is in companion `*_GUIDE.md` files. WHY is in this section. See `_INFO_GRUC_GUIDES_RULES_CHECKS.md [GRUC-IN01]` section 4.

## 2. Core Principle

**The template IS the document.** Every template file is a skeleton that the agent copies, fills in, and strips of XML comments. No exceptions.

Every line in a template is one of:
- **Template content** - Markdown headings, fields, placeholder values. Becomes part of the output document.
- **XML comment** - Annotations: rules, conditional markers, optional fields. Removed after instantiation.

Templates do not teach. Teaching belongs in `*_RULES.md` and `*_GUIDE.md` companion files. The template is the skeleton, the rules file explains when and how to fill it.

## 3. Template Structure

```
<!-- TOP COMMENT BLOCK (optional)
Template metadata: naming convention, creation trigger, lifecycle.
"Remove this comment block after creating the document."
-->

# [Document Title]: [PLACEHOLDER]

**Doc ID**: [TOPIC]-[TYPE][NN]
**Goal**: [Single sentence]
**Timeline**: Created YYYY-MM-DD, Updated N times (YYYY-MM-DD - YYYY-MM-DD)

## Section 1

<!-- Instruction: when to include, what to put here. -->

[Template content with [PLACEHOLDERS]]

## Section 2

[More template content]

## Document History

**[YYYY-MM-DD HH:MM]**
- Initial document created

<!-- EXAMPLE: Reference only. Do not copy into new documents. Shows a completed document with real values. -->

## Full Example

` ` `markdown
[Complete filled-in example here]
` ` `
```

### 3.1 Rules

1. **No prose descriptions between sections** - If a section needs explanation, use an XML comment inside it
2. **No meta-headings** - Never use `## Header Block`, `## Section Structure`, `## Full Example Description`. The sections ARE the template.
3. **Placeholders in brackets** - `[TOPIC]`, `[Single sentence describing purpose]`, `[YYYY-MM-DD HH:MM]`
4. **Enumerated options in brackets** - `[Minimal | Low | Medium | High]`, `[VERIFIED / ASSUMED]`
5. **Repeatable items show one instance** - Show one `### D-01:` entry, not three. Agent understands repetition.
6. **Conditional sections** - Use XML comment with insertion criteria: `<!-- Conditional: insert when [criteria]. Per [rule reference] -->`
7. **Full example at end** - Always in fenced code block, always preceded by `<!-- EXAMPLE: Reference only -->` annotation
8. **Rules go in companion files** - Complex rules, categories, and decision logic belong in `*_RULES.md` or `*_GUIDE.md`, not in the template

### 3.2 Exemplar Templates

- `INFO_TEMPLATE.md` - Clean. MNF uses `<!-- Remove this section -->`.
- `DEFERRED_IMPROVEMENTS_TEMPLATE.md` - Top comment block for naming convention, inline XML comments for field options.
- `RESEARCH_SUMMARY_TEMPLATE.md` (deep-research skill) - Conditional sections use `<!-- Conditional: ... -->` XML comments.

## 4. Annotation Techniques

### 4.1 XML Comments for Annotations

```markdown
<!-- Remove this comment block after creating the document. -->

<!-- D-[NN] numbering is sequential across all runs, never reused. -->

<!-- Optional fields per candidate:
- **Status**: PARTIALLY ADDRESSED | SUPERSEDED | BLOCKED BY [ref]
- **Remaining**: [What is left to do if partially addressed]
-->

<!-- EXAMPLE: Reference only. Do not copy into new documents. -->
```

**Annotation types** (all XML comments, no exceptions):

- **Removal instruction**: `<!-- Remove this section/block after creating the document. -->`
- **Inline rule**: `<!-- D-[NN] numbering is sequential across all runs, never reused. -->`
- **Optional fields**: `<!-- Optional fields per candidate:\n- **Field**: [values] -->`
- **Conditional section**: `<!-- Conditional: insert when 3+ audiences benefit. Per RULES.md SD-ES-06 -->`
- **Example annotation**: `<!-- EXAMPLE: Reference only. Do not copy into new documents. -->`
- **Scope restriction**: `<!-- Include only for UI specifications. -->`

### 4.2 Bracket Placeholders

- **Value to fill**: `[Single sentence describing purpose]`
- **Enumerated choice**: `[Minimal | Low | Medium | High]`
- **ID pattern**: `[TOPIC]-DF[NN]`
- **Date pattern**: `YYYY-MM-DD` (no brackets - format IS the placeholder)
- **Repeating pattern**: `[NN]`, `[NNNN]`

### 4.3 What NOT to Use for Annotations

- **Prose paragraphs between sections** - Looks like template content
- **Headings that describe sections** - `## Header Block` instead of the actual header
- **BAD/GOOD examples inline** - Confuses instruction with template content (wrap in XML comment)
- **Rule lists that look like document content** - "Location Rules", "Management Rules" sections
- **Bracket markers** - `[conditional - ...]` creates polysemy with `[placeholder]` format (AP-NM-01)
- **Italic markers** - `*(For UI specs only)*` is visible noise in rendered output (SOCAS-08)

## 5. Header Block Standards

### 5.1 Template Categories

**Per-task documents** are created once per task, versioned, and referenced by Doc ID:
INFO, SPEC, IMPL, TEST, TASKS, REVIEW, MINTO, DEFERRED_IMPROVEMENTS, FIXES.

All other templates (FAILS, LEARNINGS, MINTO-DRAFT, CONVERSATION, SKILL, WORKFLOW, STRUT) are tracking logs, scaffolding, reusable artifacts, or embedded notation. Doc ID, Timeline, and Document History do not apply.

### 5.2 Required Fields (Per-Task Documents)

- **Doc ID**: `[TOPIC]-[TYPE][NN]` - Every document has a unique ID
- **Goal**: Single sentence describing purpose

### 5.3 Doc ID Label Format

Use `**Doc ID**:` without suffixes. `(TDID)` is redundant - all Doc IDs follow the Topic-based pattern (AP-NM-01).

```markdown
<!-- BAD -->
**Doc ID (TDID)**: [TOPIC]-SP[NN]

<!-- GOOD -->
**Doc ID**: [TOPIC]-SP[NN]
```

### 5.4 Doc ID Applicability

Per-task documents only. Not applicable for tracking logs, scaffolding, reusable artifacts, embedded notation, or conversation tracking (see Template categories above).

### 5.5 Topic ID XML Comment

All templates with a Doc ID field must include the Topic ID guidance comment:

```markdown
**Doc ID**: [TOPIC]-SP[NN]
<!-- Topic IDs: 7-14 uppercase chars. Inside T##/S## folders use nested: [TOPIC]-[SUBTOPIC]-SP[NN] -->
```

### 5.6 Conditional Fields

- **Timeline**: `Created YYYY-MM-DD, Updated N times (YYYY-MM-DD - YYYY-MM-DD)` - All versioned documents
- **Target file(s)**: List format with `- \`path\`` items - Documents that reference code or other files
- **Feature**: `[FEATURE_SLUG]` - SPEC, IMPL, TEST, TASKS
- **Depends on**: List of document dependencies
- **Does not depend on**: Explicit exclusions (SPEC only)
- **Source**: Reference to upstream documents (TASKS, MINTO)

### 5.7 Target File(s) Format

Always use plural `Target file(s):` with list format, even for single targets:

```markdown
**Target file(s)**:
- `[path/to/file1.py]`
- `[path/to/file2.py]`
```

### 5.8 Timeline Field

Per-task documents only (see Template categories above).

## 6. Structural Section Standards

Structural sections beyond the header block.

### 6.1 Document History

Per-task documents only. Format per `core-conventions.md`: reverse chronological, action prefixes (Added, Changed, Fixed, Removed, Moved).

### 6.2 MUST-NOT-FORGET

Required for planning documents per `SKILL.md`: SPEC, IMPL, TEST.

Also used in: INFO (research scope), CONVERSATION (formatting rules).

Not required for: REVIEW, MINTO, MINTO-DRAFT, FIXES, DEFERRED, FAILS, LEARNINGS, TASKS.

### 6.3 Table of Contents

Required when document has 4+ numbered sections.

## 7. Anti-Patterns

### 7.1 AP-01: Meta-wrapper (CRITICAL)

Template describes itself instead of being the document.

**BAD**:
```markdown
# TASKS Template

Template for creating task plan documents.

## Header Block

` ` `markdown
# TASKS: [TOPIC] Tasks Plan
**Doc ID**: [TOPIC]-TK01
` ` `

## Task Item Structure

` ` `markdown
- [ ] **[TOPIC]-TK-001** - Description
` ` `
```

**GOOD**:
```markdown
<!-- TASKS TEMPLATE. Remove this comment after creating. -->

# TASKS: [TOPIC] Tasks Plan

**Doc ID**: [TOPIC]-TK01
**Goal**: Partitioned tasks for [TOPIC] implementation
```

### 7.2 AP-02: Instruction Sections Disguised as Content (HIGH)

Sections with rules, categories, or management instructions that look like document content.

**BAD**:
```markdown
## Failure Categories

- `[CRITICAL]` - Flawed assumption causing production failure
- `[HIGH]` - Logic error likely to cause failure

## Location Rules

- **SESSION-MODE**: `[SESSION_FOLDER]/FAILS.md`
```

**GOOD**:
```markdown
<!-- Failure categories:
- [CRITICAL] - Flawed assumption causing production failure
- [HIGH] - Logic error likely to cause failure
-->

<!-- Location: SESSION-MODE -> [SESSION_FOLDER]/FAILS.md, PROJECT-MODE -> [WORKSPACE_FOLDER]/FAILS.md -->
```

### 7.3 AP-03: Inline Teaching Examples (MEDIUM)

BAD/GOOD code comparisons embedded in template sections.

**BAD**:
```markdown
## 4. Functional Requirements

**BAD:**
` ` `
- Toast notifications should support info, success, error types
` ` `

**GOOD:**
` ` `
**UI-FR-01: Toast Notifications**
- Support info, success, error, warning message types
` ` `
```

**GOOD**:
```markdown
## 4. Functional Requirements

<!-- BAD: "Toast notifications should support info, success, error types" (no ID, vague)
     GOOD: "**UI-FR-01: Toast Notifications** - Support info, success, error, warning message types" (ID + specific) -->

**[PREFIX]-FR-01: [Requirement Title]**
- [Requirement detail 1]
```

### 7.4 AP-04: Prose Annotations Between Template Sections (MEDIUM)

Explanatory text that reads like content but is actually guidance.

**BAD**:
```markdown
## 2. Edge Cases

Derive from domain objects and actions:

...

**Categories to consider:**
- Input boundaries (empty, null, max length, invalid format)
- State transitions (invalid state, concurrent modifications)
```

**GOOD**:
```markdown
## 2. Edge Cases

<!-- Derive from domain objects and actions. Categories: input boundaries, state transitions, external failures, data anomalies. -->

- **[PREFIX]-IP01-EC-01**: [Boundary/failure description] -> [Expected behavior]
```

### 7.5 AP-05: Non-XML Annotation Formats (MEDIUM)

Bracket markers or italic text instead of XML comments.

**BAD**:
```markdown
[conditional - insert when 3+ audiences benefit. Per RULES.md SD-ES-06]

*(For UI specs only)*
```

**GOOD**:
```markdown
<!-- Conditional: insert when 3+ audiences benefit. Per RULES.md SD-ES-06 -->

<!-- Include only for UI specifications. -->
```

**Why**: Bracket markers `[text]` overlap with placeholder convention (AP-NM-01 polysemy). Italic markers `*(text)*` are visible noise in rendered output (SOCAS-08). XML comments are the single established format for all template annotations (AP-PR-09).

## 8. Template Audit Checklist

When creating or reviewing a template:

- [ ] **Template IS the document**: Not a description of it, not wrapped in code blocks
- [ ] **Annotations as XML comments**: No prose, brackets, or italic markers for annotations
- [ ] **BAD/GOOD examples**: Wrapped in XML comments, not inline as section content
- [ ] **Complex rules in companion files**: `*_RULES.md` or `*_GUIDE.md`, not in the template
- [ ] **Doc ID label**: Uses `**Doc ID**:` not `**Doc ID (TDID)**:`
- [ ] **Doc ID present**: Required for per-task documents, not for tracking logs or reusable artifacts
- [ ] **Topic ID comment**: Present after Doc ID field (nested ID guidance)
- [ ] **Header block complete**: Doc ID, Goal, Timeline (if versioned), Target file(s) (if applicable)
- [ ] **Target file(s) plural**: Uses list format even for single targets
- [ ] **Document History**: Present in per-task templates, not in reusable artifacts
- [ ] **MUST-NOT-FORGET**: Present in planning documents (SPEC, IMPL, TEST)
- [ ] **Full example present**: In fenced code block with `<!-- EXAMPLE: Reference only -->` annotation
- [ ] **Placeholders consistent**: `[BRACKETS]` for values, `YYYY-MM-DD` for dates (no brackets)
- [ ] **Conditional sections marked**: XML comments with insertion criteria, not bracket markers
- [ ] **Instruction sections**: Rules, categories, location rules wrapped in XML comments, not headings

## 9. Sources

- `DOCTMPLS-IN01-SC-DFTMPL-CURR`: Current state audit of 15 write-documents templates (2026-08-05) [VERIFIED]
- `DOCTMPLS-IN01-SC-RSRTMPL-REF`: `RESEARCH_SUMMARY_TEMPLATE.md` (deep-research skill) - exemplar template with XML comment conditionals [VERIFIED]
- `DOCTMPLS-IN01-SC-DFRIMP-REF`: `DEFERRED_IMPROVEMENTS_TEMPLATE.md` - template with XML comment annotations and annotated full example [VERIFIED]

## 10. Document History

**[2026-08-06 00:14]**
- Fixed: Subsection decimal notation added to all 21 subsections (INFO-SN-02)
- Fixed: Acronyms MECT, APAPALAN, SOCAS, GRUC expanded at first use (AP-PR-06)

**[2026-08-06 00:11]**
- Added: Section 1 "Why Template Design Matters" - philosophy, compounding cost, MECT/APAPALAN/SOCAS/GRUC connections
- Changed: Sections renumbered (1-9 -> 1-10)

**[2026-08-06 00:10]**
- Fixed: AP-01 GOOD example showed `Doc ID (TDID)` contradicting Section 5.2 rule (SOCAS-01)
- Fixed: AP-04/AP-05 out of sequence (SOCAS-14, MECT Topology)
- Fixed: 'annotation' / 'instruction' polysemy unified to 'annotation' (AP-NM-01)
- Fixed: 'should' replaced with 'must' where obligation intended (MW-VO-04)
- Changed: Summary grouped into 2 named clusters (AP-ST-07)
- Changed: Template categories defined once, exclusion lists replaced by category references (AP-BR-03, SOCAS-03)
- Removed: Stale status observations ('Currently only...', 'Previously affected') (SOCAS-08, SOCAS-12)
- Removed: Verbose Doc ID explanation tightened (AP-BR-02)

**[2026-08-05 23:58]**
- Changed: Unified all annotations to XML comments (no bracket markers, no italic markers)
- Added: AP-05 anti-pattern for non-XML annotation formats (AP-NM-01, AP-PR-09, SOCAS-08)
- Added: Scope restriction annotation type (`<!-- Include only for UI specifications. -->`)
- Added: "What NOT to use" items for bracket and italic markers
- Changed: Conditional section format from `[conditional - ...]` to `<!-- Conditional: ... -->`

**[2026-08-05 23:53]**
- Added: Doc ID label format rule (no TDID suffix), Doc ID applicability per template type
- Added: Topic ID XML comment standardization
- Added: Section 5 - Structural Section Standards (Document History, MNF, TOC requirements)
- Changed: Audit checklist expanded with 4 new items

**[2026-08-05 23:51]**
- Unified to single pattern: template IS the document (removed Pattern A/B distinction)
- Rules and teaching belong in companion `*_RULES.md` / `*_GUIDE.md` files

**[2026-08-05 23:49]**
- Initial document created from template audit findings
- Documented 4 anti-patterns with BAD/GOOD examples
- Created audit checklist for template review
