# INFO: GRUC - Guides, Rules, Checks

**Doc ID**: GRUC-IN01
**Goal**: Define the GRUC file types (GUIDE, RULES, CHECKS, EXAMPLE, TEMPLATE), their consumers, lifecycle positions, and content boundaries

**Depends on:**
- [`_INFO_AGENT_DRIFT_PREVENTION_APPROACH.md [ADP-IN01]`](_INFO_AGENT_DRIFT_PREVENTION_APPROACH.md) for GRUC's position in the PromptSystem

## Summary

- GRUC (Guides, Rules, Checks) pre-calculates compliance criteria into four primary file types plus EXAMPLE supplementary files per skill/workflow

**File types and consumers:**
- GUIDE = before execution (planning strategy). Consumer: working agent, `/critique`
- RULES = after execution (output verification). Consumer: `/verify`
- TEMPLATE = during and after execution (skeleton structure). Consumer: working agent (copy and fill), `/verify` (template adherence)
- CHECKS = after execution (process audit AND quality improvement). Two categories: PD (Process Discipline) consumed by `/drift-detect`, QI (Quality Improvement) consumed by `/improve`
- EXAMPLE = supplementary files linked from GUIDES. Shows larger GOOD examples beyond simple BAD/GOOD pairs. Referenced by `/critique` for quality comparison

**Design properties:**
- Separation prevents gaming: CHECKS invisible during work, GUIDE invisible during audit
- Each file type maps to a drift category: GUIDE → strategic quality, RULES → output structure (Cat 1), CHECKS PD → process discipline (Cat 2), CHECKS QI → quality improvement
- Content verifiability: RULES from artifacts alone, CHECKS PD from action evidence, CHECKS QI from judgment-based assessment

**Writing patterns:**
- RULES = Rule Index + BAD/GOOD pairs; GUIDE = numbered decision steps + review checklist + EXAMPLE links; TEMPLATE = skeleton document with XML comment annotations + bracket placeholders; CHECKS = PD items (action + evidence + failure indicator) + QI items (quality question + improvement tip); EXAMPLE = complete or substantial GOOD document showing use-case-specific solution

## Table of Contents

1. [The Problem GRUC Solves](#1-the-problem-gruc-solves)
2. [File Types](#2-file-types)
3. [Lifecycle Positioning](#3-lifecycle-positioning)
4. [Content Boundaries](#4-content-boundaries)
5. [Consumers and Workflows](#5-consumers-and-workflows)
6. [Naming Conventions](#6-naming-conventions)
7. [Accumulation from FAILS.md](#7-accumulation-from-failsmd)
8. [Current Implementation Status](#8-current-implementation-status)
9. [How to Write Good GRUC Documents](#9-how-to-write-good-gruc-documents)

## 1. The Problem GRUC Solves

Quality assurance workflows (`/verify`, `/critique`, `/drift-detect`, `/improve`) need compliance criteria to check against. Without pre-calculated criteria, each workflow must:

1. Re-read the entire skill/workflow definition
2. Derive what "correct output" looks like
3. Derive what "correct process" looks like
4. Spend tokens on derivation instead of checking

GRUC eliminates this by pre-calculating criteria into lookup-ready files. The core insight: compliance criteria are **constants** knowable in advance from skill definitions and accumulated failures. Calculate once, store, look up.

## 2. File Types

### 2.1 GUIDE - Process Guidance (Before)

**Purpose**: Tell the working agent HOW to approach the work before starting.

**Content**:
- Decision frameworks (when to choose approach A vs B)
- Strategy patterns (how to structure the work)
- Common pitfalls to avoid (proactive, not reactive)
- Quality heuristics (what "good" looks like for this skill)
- Links to EXAMPLE files for quality reference

**Key property**: Read BEFORE execution. Shapes behavior during work. Does not verify afterward.

**Consumers**: Working agent (before execution), `/critique` (after execution - strategic gap analysis)

**Example**: `SKILL_GUIDES.md` in `@skills:write-documents` tells agents how to structure skill files, what skill types exist, and how to optimize for LLM consumption.

### 2.2 RULES - Output Standards (After)

**Purpose**: Define verifiable output quality standards checkable from artifacts alone.

**Content**:
- Structural requirements (sections present, format correct)
- Naming conventions (file names, IDs, references)
- Content completeness (required fields filled, no placeholders)
- Cross-reference integrity (all refs point to existing targets)

**Key property**: Verifiable from OUTPUT ALONE. No action traces needed. An auditor can check rules by reading the delivered artifacts without knowing how they were produced.

**Consumer**: `/verify` (structural compliance verification)

**Example**: `WORKFLOW_RULES.md` in `@skills:write-documents` defines WF-HD-01 through WF-EX-01 - all checkable by reading a workflow file.

### 2.3 CHECKS - Process Discipline AND Quality Improvement (After Only)

**Purpose**: Audit whether required process steps were performed (PD) AND assess quality with improvement tips (QI).

**Two categories**:

**PD (Process Discipline)** - existing:
- Actions that must have happened (tests run, sources visited, backups made)
- Evidence requirements (what proves the action occurred)
- Sequence compliance (steps done in correct order)
- Depth indicators (thoroughness markers vs superficial execution)

**QI (Quality Improvement)** - new:
- High-level quality questions per document type ("Is the SPEC serving the stated goal?")
- Improvement tips ("Add diagrams to INFO files", "Deepen research", "Write better summaries")
- Judgment-based assessment, not structural rules (those stay in RULES)
- Not purely verifiable from output - requires reading and understanding the document

**Key property**: Requires ACTION EVIDENCE (PD) or JUDGMENT (QI). NOT visible to the working agent during execution.

**Consumers**: `/drift-detect` (PD items), `/improve` (QI items)

**Why invisible**: Visible checklists produce superficial compliance. Agent optimizes for checkbox-checking instead of genuine quality. Unaware agents produce honest evidence.

### 2.4 EXAMPLE - Supplementary Quality Reference (Linked from GUIDE)

**Purpose**: Show larger GOOD examples that demonstrate how to solve different use cases. Go beyond simple BAD/GOOD pairs in RULES.

**Content**:
- Complete or substantial documents showing the GOOD approach
- Use-case-specific (each example solves a specific problem type)
- Key decisions and rationale documented
- No BAD examples (BAD/GOOD pairs stay in RULES)

**Key property**: Not consumed directly by any workflow. Linked from GUIDES. Referenced by `/critique` for quality comparison.

**Example**: `SPEC_EXAMPLE_01-TodoListReactApp.md` shows a complete SPEC for a simple Create, Read, Update, Delete (CRUD) app, demonstrating how to structure requirements, design decisions, and acceptance criteria for a straightforward use case.

### 2.5 TEMPLATE - Skeleton Structure (During and After)

**Purpose**: Provide a copy-and-fill skeleton for document creation. The template IS the document - every line is either template content or an XML comment annotation.

**Content**:
- Document structure with sections and placeholders
- XML comment annotations for removal instructions, conditional sections, inline rules
- Bracket notation `[PLACEHOLDERS]` for values, IDs, and enumerated choices
- No rules, no guidance, no audit items (those belong in companion RULES, GUIDES, CHECKS)

**Key property**: Consumed by the working agent (copy and fill) AND by `/verify` (template adherence check). Complex rules stay in companion `*_RULES.md` files, referenced by ID.

**Consumer**: Working agent (before and during execution), `/verify` (after execution - template adherence)

**Example**: `SPEC_TEMPLATE.md` in `@skills:write-documents` provides the skeleton for SPEC documents. The agent copies it, fills in placeholders, strips XML comments, and produces a SPEC. `/verify` then checks the result against both `SPEC_RULES.md` (structural rules) and `SPEC_TEMPLATE.md` (template adherence).

## 3. Lifecycle Positioning

```
Agent Activity Lifecycle
│
├── BEFORE (Planning)
│   └── GUIDE consumed by working agent
│       "How should I approach this?"
│       EXAMPLES linked from GUIDE for quality reference
│
├── DURING (Execution)
│   └── No GRUC files consumed
│       Agent works from GUIDE knowledge + MNF constraints
│
├── AFTER (Verification - Output Structure)
│   └── RULES + TEMPLATE consumed by /verify
│       "Does the output meet structural standards?"
│       "Does the output follow the template skeleton?"
│
├── AFTER (Verification - Strategic Quality)
│   └── GUIDE consumed by /critique
│       "Did the agent take the right approach? What's missing?"
│       EXAMPLES used for quality comparison
│
├── AFTER (Verification - Process Discipline)
│   └── CHECKS (PD) consumed by /drift-detect
│       "Were required actions actually performed?"
│
└── AFTER (Improvement)
    └── CHECKS (QI) consumed by /improve
        "What quality improvements are possible?"
```

**Temporal separation is intentional**:
- GUIDE influences behavior (before) and assesses strategic quality (after, via `/critique`)
- RULES verify artifacts (after, output structure)
- TEMPLATE provides skeleton structure (during, copy-and-fill) and is checked by `/verify` alongside RULES (after, template adherence)
- CHECKS PD audit behavior (after, process-focused)
- CHECKS QI assess quality and suggest improvements (after, judgment-focused)

Each workflow reads exactly ONE GRUC file type. Exception: `/verify` reads both RULES and TEMPLATE (both are structural verification files). No other overlap. This prevents token waste from reading irrelevant criteria.

## 4. Content Boundaries

### What Goes in GUIDE (not RULES or CHECKS)

- "When writing a SPEC, start with user stories before requirements" → GUIDE (strategy)
- "Consider 3 alternative approaches before committing" → GUIDE (decision framework)
- "For research, use breadth-first before depth-first" → GUIDE (approach pattern)

### What Goes in RULES (not GUIDE or CHECKS)

- "Every SPEC must have FR-XX, DD-XX, and IG-XX sections" → RULES (structural)
- "File names must match `_[TYPE]_[TOPIC]_[NN].md` pattern" → RULES (naming)
- "All source IDs must follow `[TOPIC]-[DOC]-SC-[SOURCE_ID]-[REF]`" → RULES (format)

### What Goes in CHECKS PD (not GUIDE, RULES, or CHECKS QI)

- "Agent must have run `/verify` after implementation" → CHECKS PD (action evidence)
- "Sources must have been actually visited, not hallucinated" → CHECKS PD (process proof)
- "Tests must have been executed, not just written" → CHECKS PD (execution evidence)
- "Tracking files updated after each commit" → CHECKS PD (sequence evidence)

### What Goes in CHECKS QI (not GUIDE, RULES, or CHECKS PD)

- "Is the SPEC serving the stated goal?" → CHECKS QI (quality question)
- "Did the SPEC make all necessary decisions?" → CHECKS QI (quality question)
- "Does the SPEC avoid unnecessary complexity in dependencies?" → CHECKS QI (quality question)
- "Were all assumptions fact-checked?" → CHECKS QI (quality question)
- "Add diagrams to INFO files" → CHECKS QI (improvement tip)
- "Deepen research by adding more primary sources" → CHECKS QI (improvement tip)

### What Goes in EXAMPLE (not GUIDE, RULES, CHECKS, or TEMPLATE)

- Complete SPEC showing how to structure a simple CRUD app → EXAMPLE (use-case demonstration)
- Substantial INFO showing how to organize a multi-source comparison → EXAMPLE (use-case demonstration)
- Full IMPL showing how to sequence risky implementation steps → EXAMPLE (use-case demonstration)

### What Goes in TEMPLATE (not GUIDE, RULES, CHECKS, or EXAMPLE)

- Skeleton structure with `[PLACEHOLDERS]` → TEMPLATE (copy-and-fill document)
- XML comment annotations for removal instructions → TEMPLATE (invisible in rendered output)
- Conditional section markers with criteria → TEMPLATE (when to include/exclude sections)
- Full example at end for reference → TEMPLATE (wrapped in `<!-- EXAMPLE: -->` annotation)

### Boundary Test

Ask: "Can I verify this by reading the delivered files?"
- Yes, structurally → RULES
- No, needs action traces → CHECKS PD
- No, needs judgment about quality → CHECKS QI
- Neither, it's strategic advice → GUIDE
- It's a complete good example showing a use case → EXAMPLE
- It's a skeleton to copy and fill → TEMPLATE

## 5. Consumers and Workflows

```
GUIDE
├── Working agent (during /build, /implement, /solve)
└── /critique (strategic gap analysis using GUIDES + EXAMPLES)

RULES
└── /verify (structural compliance, output-only verification)

TEMPLATE
├── Working agent (copy and fill before execution)
└── /verify (template adherence, if template exists)

CHECKS (PD)
└── /drift-detect (process discipline audit, action evidence)

CHECKS (QI)
└── /improve (quality improvement, judgment-based assessment)

EXAMPLES
├── Linked from GUIDES (not consumed directly by workflows)
└── Referenced by /critique for quality comparison
```

**No overlap**: Each workflow consumes exactly one GRUC component as primary source. Exception: `/verify` reads both RULES and TEMPLATE (both are structural verification files). EXAMPLES are linked from GUIDES, not consumed directly. This prevents token waste from reading irrelevant criteria.

## 6. Naming Conventions

### Per-Skill Files

```
[AGENT_FOLDER]/skills/[skill-name]/
├── SKILL.md              (entry point)
├── SKILL_GUIDES.md        (approach guidance, links to EXAMPLES)
├── SKILL_RULES.md        (output verification rules)
├── SKILL_CHECKS.md       (process discipline + quality improvement checks)
├── SKILL_TEMPLATE.md     (skeleton structure for document creation)
├── [TOPIC]_EXAMPLE_[NN]-[Name].md  (use-case examples)
└── [other files]
```

### Domain-Specific Rules Files

When a skill has multiple distinct domains, rules split by domain:

```
[AGENT_FOLDER]/skills/write-documents/
├── SKILL_GUIDES.md         (general writing guidance)
├── SKILL_RULES.md         (general output rules)
├── WORKFLOW_RULES.md      (workflow-specific rules)
├── SPEC_RULES.md          (specification-specific rules)
├── SPEC_EXAMPLE_01-TodoListReactApp.md    (SPEC use-case example)
├── SPEC_EXAMPLE_02-AuthenticationSystem.md  (SPEC use-case example)
├── TRANSLATION_RULES.md   (translation-specific rules)
└── CONVERSATION_RULES.md  (conversation-specific rules)
```

Pattern: `[DOMAIN]_RULES.md` when SKILL_RULES.md would exceed ~200 lines.
Pattern: `[TOPIC]_EXAMPLE_[NN]-[ExampleName].md` for example files. ExampleName uses PascalCase.

### Per-Workflow Files (Future)

```
[AGENT_FOLDER]/workflows/
├── verify.md
├── verify_CHECKS.md       (what /drift-detect checks about /verify executions)
└── ...
```

## 7. Accumulation from FAILS.md

GRUC files are NOT static. They accumulate over time:

1. Agent makes a mistake → logged in FAILS.md
2. User invokes `/learn` → extracts pattern
3. Pattern becomes a new rule, check, or example:
   - Output quality failure → new item in RULES
   - Process discipline failure → new item in CHECKS (PD)
   - Quality improvement opportunity → new item in CHECKS (QI)
   - Strategic error → new item in GUIDE
   - Missing use-case demonstration → new EXAMPLE file

**Direction**: FAILS.md → `/learn` → GRUC file update (user-triggered only)

This creates a feedback loop where past failures become future prevention criteria.

## 8. Current Implementation Status

**Realized:**
- `*_RULES.md` files exist in `@skills:write-documents` (14 files), `@skills:coding-conventions` (10 files, `*-RULES.md` dash pattern), `@skills:deep-research` (6 files)
- `*_GUIDES.md` files exist in `@skills:write-documents` (6 files)
- `/verify` consumes RULES files (structural compliance only)
- `/critique` deployed (switching to GUIDES-driven review)
- `/drift-detect` and `/drift-correct` workflows deployed (switching to CHECKS-driven assessment)
- `/improve` deployed (switching to CHECKS QI-driven improvements)

**In progress:**
- Workflow separation: verify → RULES only, critique → GUIDES only, drift-detect → CHECKS PD only, improve → CHECKS QI only
- CHECKS files with PD + QI categories being created
- EXAMPLE file type being added

**Not yet realized:**
- `SKILL_CHECKS.md` files do not exist in any skill (PD + QI structure defined, creation pending)
- No EXAMPLE files exist yet
- Most skills lack GUIDE files
- No per-workflow CHECKS files exist

**Next steps:**
1. Create first `SKILL_CHECKS.md` with PD + QI items for `@skills:write-documents`
2. Create first EXAMPLE files for SPEC and INFO document types
3. Update `/drift-detect` to consume CHECKS PD files
4. Update `/improve` to consume CHECKS QI files
5. Add GUIDE files to skills that involve complex decision-making

## 9. How to Write Good GRUC Documents

### 9.1 Writing RULES Files

A RULES file is a verification lookup table. Its consumer is `/verify` - the workflow that checks output against structural standards fast.

**Structure pattern** (derived from `WORKFLOW_RULES.md`, `SPEC_RULES.md`, `RESEARCH_RULES.md`, `SKILL_RULES.md`):

```
# [Domain] Rules

[One-line scope statement]

**Writing quality:** Apply `APAPALAN_RULES.md`. Key rules: [list 3-4 most relevant]

## Rule Index

[Category] ([2-letter prefix])
- [PREFIX]-[CAT]-[NN]: [One-line rule statement]
- [PREFIX]-[CAT]-[NN]: [One-line rule statement]

## [Rule ID]: [Rule Name]

**BAD:**
[example of violation]

**GOOD:**
[example of compliance]
```

**Principles:**

1. **Rule Index first** - Complete list of all rules as one-liners at the top. Reader scans index to find relevant rules without reading the full document.
2. **Categorize rules** - Group by aspect: Header (HD), Structure (ST), Content (CT), Files (FL), Format (FT). Use 2-letter prefix.
3. **Unique IDs** - Every rule gets `[PREFIX]-[CAT]-[NN]`. IDs must never change once published. New rules append to category.
4. **BAD/GOOD pairs** - Each rule expanded below the index with concrete examples showing violation and compliance. No abstract explanations.
5. **Checkable from output** - Each rule must be verifiable by reading delivered artifacts. If verification needs action traces, it belongs in CHECKS.
6. **Scope statement** - First line after title states what document type or output these rules apply to. Enables `/verify` to detect applicability.
7. **No process instructions** - RULES say WHAT must be true, not HOW to achieve it. Process belongs in GUIDE.
8. **Detection section** (optional) - When rules apply conditionally, list file patterns or context markers that trigger applicability. See `RESEARCH_RULES.md` "Detection" section.
9. **Verification Procedure** (optional) - Ordered sequence showing HOW to check all rules. Useful for complex rule sets with dependencies between checks.

**Anti-patterns:**

- Rule without example → unenforceable (agent interprets differently each time)
- Rule that says "should" → ambiguous (change to "must" or remove)
- Rule that references process ("after reading X, do Y") → belongs in GUIDE or workflow
- Rule index missing → agent reads full document every time (token waste)

### 9.2 Writing GUIDE Files

A GUIDE file is strategic coaching. Its consumers are the working agent before starting a task AND `/critique` after execution. It shapes HOW the agent approaches work and provides criteria for strategic gap analysis.

**Structure pattern** (derived from `SKILL_GUIDES.md`):

```
# [Domain] Guide

[One-line purpose statement]

## 1. [First Decision/Step]

[Decision framework or classification]

For [use case], see `[TOPIC]_EXAMPLE_[NN]-[Name].md`

## 2. [Second Decision/Step]

[Strategy with options and when-to-use-each]

## N. Review Checklist

- [ ] [Verification question]
- [ ] [Verification question]
```

**Principles:**

1. **Numbered procedural steps** - Agent follows top-to-bottom. Order reflects decision sequence: classify first, then choose approach, then execute details.
2. **Decision frameworks** - Give the agent branching logic: "If X, do A. If Y, do B." Reduces arbitrary choices.
3. **Classify-then-act** - First step always classifies the input (type, complexity, scope). Classification determines which subsequent steps apply.
4. **Token optimization section** - For LLM-consumed output, include explicit keep/remove guidance. Agent otherwise defaults to verbose.
5. **Review checklist at end** - Final checkpoint before the agent considers the work done. Questions, not rules.
6. **Strategy over structure** - GUIDE says "approach research breadth-first, then depth-first." RULES says "summary section must exist with 5-15 sentences." Different concerns.
7. **Proactive pitfall warnings** - Include "Common mistakes" inline where the mistake would be made, not in a separate section at the end.
8. **Link to EXAMPLES** - When a decision point has a corresponding EXAMPLE file, link to it inline: "For [use case], see `[TOPIC]_EXAMPLE_[NN]-[Name].md`". This gives the agent and `/critique` a quality reference without embedding large examples in the GUIDE.

**Anti-patterns:**

- Verifiable output requirements → belongs in RULES (move it there)
- Checklist of "must have X section" → RULES content disguised as guidance
- Overly prescriptive step-by-step → becomes a workflow, not a guide
- No decision points → guide adds no value over the workflow steps themselves
- No EXAMPLE links → `/critique` lacks quality reference for comparison

### 9.3 Writing CHECKS Files

A CHECKS file is a process discipline audit AND quality improvement reference. Its consumers are `/drift-detect` (PD items) and `/improve` (QI items) after the working agent finished. The working agent NEVER sees this file during execution.

**Structure pattern:**

```
# [Domain] Checks

[One-line: what this audits - process discipline AND quality improvement]

**Evidence sources:** conversation logs, git history, file timestamps, terminal output

## Check Index

Process Discipline (PD)
- [PREFIX]-PD-[NN]: [Action that must have happened]

Quality Improvement (QI)
- [PREFIX]-QI-[NN]: [Quality question with improvement tip]

## [Check ID]: [Check Name]

**Type**: Process Discipline | Quality Improvement
**Evidence**: [What proves the action occurred / What to assess]
**Failure indicator**: [What absence or contradiction indicates non-compliance]
**Improvement tip**: [For QI: specific tip for improvement]
**Severity**: CRITICAL | HIGH | MEDIUM
```

**PD Principles (Process Discipline):**

1. **Action-oriented** - Each PD check describes something the agent MUST HAVE DONE, not something the output must contain. "Agent ran `/verify`" not "Document passes verification."
2. **Evidence-based** - Every PD check specifies what evidence proves compliance. Without defined evidence, a check is unenforceable.
3. **Failure indicators** - Describe what NON-compliance looks like. Helps the auditing workflow detect violations quickly.
4. **Severity levels** - CRITICAL (indicates fundamental process failure), HIGH (significant quality risk), MEDIUM (process shortcut with limited impact).
5. **Invisible to executor** - CHECKS files must NOT be referenced in workflows, SKILL.md intent lookups, or MNF sections. Only `/drift-detect` and `/improve` read them.
6. **No output requirements** - If checkable from the delivered files alone, it belongs in RULES. PD checks require action traces: timestamps, conversation evidence, git commits, command output.
7. **Sequence matters** - Order PD checks by expected execution sequence. First checks verify early-stage actions (planning, research), later checks verify late-stage actions (verification, commit).

**QI Principles (Quality Improvement):**

1. **Question-oriented** - Each QI check is a high-level quality question, not a structural rule. "Is the SPEC serving the stated goal?" not "SPEC must have Goal field."
2. **Judgment-based** - QI checks require reading and understanding the document, not just checking structure. They assess whether the right approach was taken.
3. **Improvement tips** - Every QI check includes a specific tip for improvement. Not just "this could be better" but "add diagrams to INFO files" or "deepen research by adding primary sources."
4. **Not structural** - If a check is verifiable from output structure alone, it belongs in RULES. QI checks assess quality beyond structure: goal alignment, decision completeness, complexity, assumption verification.
5. **Per document type** - QI checks are specific to document types. SPEC QI checks differ from INFO QI checks differ from IMPL QI checks.
6. **Invisible to executor** - Same as PD. The working agent should not optimize for QI tips during generation.

**Example QI items for SPECs:**
- GRUC-QI-01: Is the SPEC serving the stated goal? (Check: Goal field vs actual content alignment)
- GRUC-QI-02: Did the SPEC make all necessary decisions? (Check: open questions, unresolved alternatives)
- GRUC-QI-03: Does the SPEC avoid unnecessary complexity in dependencies? (Check: dependency count, simpler alternatives)
- GRUC-QI-04: Were all assumptions fact-checked? (Check: [ASSUMED] labels without verification)

**Anti-patterns:**

- "Output file must have section X" → RULES content (move to RULES file)
- PD check without evidence definition → unenforceable guess
- QI check that is purely structural → RULES content (move to RULES file)
- Check visible to working agent → gaming risk (agent performs action superficially to pass)
- Too many CRITICAL checks → severity inflation, everything becomes noise
- QI check without improvement tip → unactionable criticism

### 9.4 Writing EXAMPLE Files

An EXAMPLE file is a quality reference. Its consumers are the working agent (via GUIDE links before execution) and `/critique` (for quality comparison after execution). EXAMPLES show larger GOOD examples that go beyond simple BAD/GOOD pairs in RULES.

**Structure pattern:**

```
# [Domain] Example [NN]: [ExampleName]

[One-line: what use case this demonstrates]

## Context

[What problem does this example solve? What makes this use case different?]

## Example

[Full or substantial document showing the GOOD approach]

## Key Decisions

[What decisions were made in this example and why]

## What This Example Teaches

[What can be learned from this example]
```

**Principles:**

1. **Complete or substantial** - Not snippets. Show enough to understand the full approach. A SPEC example shows the complete structure with real content, not placeholder text.
2. **Use-case specific** - Each example solves a specific problem type. "TodoListReactApp" demonstrates a simple CRUD SPEC. "AuthenticationSystem" demonstrates a multi-component SPEC.
3. **Linked from GUIDES** - EXAMPLES are referenced in GUIDES at the relevant decision point. Not consumed directly by workflows.
4. **No BAD examples** - EXAMPLES show only GOOD. BAD/GOOD pairs stay in RULES. EXAMPLES demonstrate what good looks like, not what bad looks like.
5. **Generic content** - No project-specific data. Pre-Write Privacy Gate applies. Use fictional names, generic data, placeholder domains.
6. **Key Decisions section** - Document what decisions were made and why. This teaches the reader when this example applies vs when a different approach is needed.
7. **Naming** - `[TOPIC]_EXAMPLE_[NN]-[ExampleName].md`. ExampleName uses PascalCase. NN is 2-digit sequential.

**Anti-patterns:**

- Snippet instead of complete document → too small to show full approach (expand or move to RULES as BAD/GOOD pair)
- Project-specific data → privacy violation (replace with generic)
- No link from GUIDE → orphan example, never discovered
- BAD example included → confusing (BAD/GOOD pairs belong in RULES)
- No Key Decisions section → reader cannot determine when to apply this example

### 9.5 Cross-File Consistency

When writing a complete GRUC set for a skill:

1. **No overlaps** - Each requirement lives in exactly one file. If uncertain, apply the Boundary Test (section 4).
2. **No gaps** - Together, GUIDE + RULES + TEMPLATE + CHECKS (PD + QI) + EXAMPLES should cover strategy, output, skeleton, process, quality, and use-case demonstration. Missing file = missing coverage.
3. **Consistent terminology** - Same concept uses same name across all files. If RULES calls it "Rule Index", GUIDE should not call it "Rule Summary."
4. **Same prefix** - All IDs within one skill use the same prefix. `WF-HD-01` (RULES), `WF-PD-01` (CHECKS PD), `WF-QI-01` (CHECKS QI).
5. **GUIDE references RULES and EXAMPLES** - GUIDE may say "Apply SK-FL-* rules for file layout" pointing to RULES for specifics. GUIDE links to EXAMPLES at decision points. GUIDE provides strategy, RULES provides exact standards, TEMPLATE provides skeleton, EXAMPLES provide quality reference.
6. **TEMPLATE references RULES by ID** - TEMPLATE contains only skeleton and placeholders. Complex rules are referenced by ID from companion `*_RULES.md`, never inlined.
7. **CHECKS references neither** - CHECKS stands alone. Auditor should not need GUIDE or RULES to evaluate process compliance or quality improvement.
8. **EXAMPLES reference neither** - EXAMPLES are standalone demonstrations. They do not reference RULES or CHECKS. They may reference the GUIDE that links to them.

## Document History

**[2026-09-12 14:55]**
- Added: TEMPLATE as fifth GRUC file type (section 2.5) - skeleton structure for document creation
- Added: TEMPLATE to file type listing, consumer mapping, lifecycle diagram, content boundaries, naming conventions
- Updated: Summary from "three primary" to "four primary" file types (RULES, GUIDE, TEMPLATE, CHECKS + EXAMPLE supplementary)
- Updated: Lifecycle diagram shows RULES + TEMPLATE consumed by `/verify`
- Updated: Consumer mapping shows TEMPLATE -> working agent + `/verify`
- Updated: Boundary test includes TEMPLATE
- Updated: Cross-file consistency (section 9.5) for 5 file types
- Updated: Naming conventions include SKILL_TEMPLATE.md

**[2026-09-12 13:15]**
- Changed: CHECKS extended with QI (Quality Improvement) category in addition to PD (Process Discipline)
- Changed: RULES consumer reduced to `/verify` only (removed `/improve`)
- Changed: CHECKS consumers now `/drift-detect` (PD) and `/improve` (QI)
- Changed: GUIDE consumer now explicitly includes `/critique` (strategic gap analysis)
- Changed: Lifecycle positioning updated with strategic quality and improvement stages
- Changed: Consumer mapping updated - each workflow reads exactly one GRUC type
- Changed: Summary grouped into clusters (AP-ST-07 compliance)
- Changed: Standardized "consumer" terminology in section 9 (SOCAS-02 fix)
- Added: EXAMPLE file type (section 2.4) - supplementary quality reference linked from GUIDES
- Added: EXAMPLE naming convention `[TOPIC]_EXAMPLE_[NN]-[ExampleName].md`
- Added: Section 9.4 (Writing EXAMPLE Files) with structure pattern and principles
- Added: Boundary test entries for CHECKS QI and EXAMPLE
- Added: QI principles and example QI items for SPECs
- Added: CRUD acronym expansion (AP-PR-06 compliance)
- Updated: Section 9.3 (Writing CHECKS Files) with PD + QI dual structure
- Updated: Section 9.5 (Cross-File Consistency) for 5 file types
- Updated: Implementation status (section 8) with current state and corrected file counts

**[2026-06-24 15:24]**
- Changed: All `/adp` workflow references replaced with `/drift-detect` (workflow split into `/drift-detect` + `/drift-correct`)

**[2026-06-12 17:42]**
- Added: Section 9 (How to Write Good GRUC Documents) with patterns from existing RULES and GUIDE files

**[2026-06-12 17:36]**
- Initial document created
