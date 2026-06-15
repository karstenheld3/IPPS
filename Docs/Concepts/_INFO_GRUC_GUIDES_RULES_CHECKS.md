# INFO: GRUC - Guides, Rules, Checks

**Doc ID**: GRUC-IN01
**Goal**: Define the three GRUC file types, their consumers, lifecycle positions, and content boundaries

**Depends on:**
- `_INFO_AGENT_DRIFT_PREVENTION_APPROACH.md [ADP-IN01]` for GRUC's position in the DevSystem

## Summary

- GRUC pre-calculates compliance criteria into three purpose-specific files per skill/workflow
- GUIDE = before execution (planning strategy). Consumer: working agent
- RULES = whole lifecycle (output verification). Consumer: `/verify`, `/improve`
- CHECKS = after execution only (process audit). Consumer: `/adp` (Agent Drift Prevention)
- Separation prevents gaming: CHECKS invisible during work, GUIDE invisible during audit
- Each file type maps to a drift category: GUIDE → strategic quality, RULES → output structure (Cat 1), CHECKS → process discipline (Cat 2)
- Content MUST be verifiable: RULES from artifacts alone, CHECKS from action evidence
- Writing patterns: RULES = Rule Index + BAD/GOOD pairs; GUIDE = numbered decision steps + review checklist; CHECKS = action + evidence + failure indicator + severity

## Table of Contents

1. [The Problem GRUC Solves](#1-the-problem-gruc-solves)
2. [Three File Types](#2-three-file-types)
3. [Lifecycle Positioning](#3-lifecycle-positioning)
4. [Content Boundaries](#4-content-boundaries)
5. [Consumers and Workflows](#5-consumers-and-workflows)
6. [Naming Conventions](#6-naming-conventions)
7. [Accumulation from FAILS.md](#7-accumulation-from-failsmd)
8. [Current Implementation Status](#8-current-implementation-status)
9. [How to Write Good GRUC Documents](#9-how-to-write-good-gruc-documents)

## 1. The Problem GRUC Solves

Quality assurance workflows (`/verify`, `/adp`, `/improve`) need compliance criteria to check against. Without pre-calculated criteria, each workflow must:

1. Re-read the entire skill/workflow definition
2. Derive what "correct output" looks like
3. Derive what "correct process" looks like
4. Spend tokens on derivation instead of checking

GRUC eliminates this by pre-calculating criteria into lookup-ready files. The core insight: compliance criteria are **constants** knowable in advance from skill definitions and accumulated failures. Calculate once, store, look up.

## 2. Three File Types

### 2.1 GUIDE - Process Guidance (Before)

**Purpose**: Tell the working agent HOW to approach the work before starting.

**Content**:
- Decision frameworks (when to choose approach A vs B)
- Strategy patterns (how to structure the work)
- Common pitfalls to avoid (proactive, not reactive)
- Quality heuristics (what "good" looks like for this skill)

**Key property**: Read BEFORE execution. Shapes behavior during work. Does not verify afterward.

**Example**: `SKILL_GUIDE.md` in `@skills:write-documents` tells agents how to structure skill files, what skill types exist, and how to optimize for LLM consumption.

### 2.2 RULES - Output Standards (Whole Lifecycle)

**Purpose**: Define verifiable output quality standards checkable from artifacts alone.

**Content**:
- Structural requirements (sections present, format correct)
- Naming conventions (file names, IDs, references)
- Content completeness (required fields filled, no placeholders)
- Cross-reference integrity (all refs point to existing targets)

**Key property**: Verifiable from OUTPUT ALONE. No action traces needed. An auditor can check rules by reading the delivered artifacts without knowing how they were produced.

**Example**: `WORKFLOW_RULES.md` in `@skills:write-documents` defines WF-HD-01 through WF-EX-01 - all checkable by reading a workflow file.

### 2.3 CHECKS - Process Discipline (After Only)

**Purpose**: Audit whether required process steps were actually performed.

**Content**:
- Actions that must have happened (tests run, sources visited, backups made)
- Evidence requirements (what proves the action occurred)
- Sequence compliance (steps done in correct order)
- Depth indicators (thoroughness markers vs superficial execution)

**Key property**: Requires ACTION EVIDENCE. Cannot be verified from output alone. Needs conversation logs, git history, terminal output, or file timestamps. NOT visible to the working agent during execution.

**Why invisible**: Visible checklists produce superficial compliance. Agent optimizes for checkbox-checking instead of genuine quality. Unaware agents produce honest evidence.

## 3. Lifecycle Positioning

```
Agent Activity Lifecycle
│
├── BEFORE (Planning)
│   └── GUIDE consumed by working agent
│       "How should I approach this?"
│
├── DURING (Execution)
│   └── No GRUC files consumed
│       Agent works from GUIDE knowledge + MNF constraints
│
├── AFTER (Verification - Output)
│   └── RULES consumed by /verify, /improve
│       "Does the output meet structural standards?"
│
└── AFTER (Verification - Process)
    └── CHECKS consumed by /adp
        "Were required actions actually performed?"
```

**Temporal separation is intentional**:
- GUIDE influences behavior (before)
- RULES verify artifacts (after, output-focused)
- CHECKS audit behavior (after, process-focused)

No file serves two lifecycle positions. This prevents conflation of "how to do it" with "did you do it correctly."

## 4. Content Boundaries

### What Goes in GUIDE (not RULES or CHECKS)

- "When writing a SPEC, start with user stories before requirements" → GUIDE (strategy)
- "Consider 3 alternative approaches before committing" → GUIDE (decision framework)
- "For research, use breadth-first before depth-first" → GUIDE (approach pattern)

### What Goes in RULES (not GUIDE or CHECKS)

- "Every SPEC must have FR-XX, DD-XX, and IG-XX sections" → RULES (structural)
- "File names must match `_[TYPE]_[TOPIC]_[NN].md` pattern" → RULES (naming)
- "All source IDs must follow `[TOPIC]-[DOC]-SC-[SOURCE_ID]-[REF]`" → RULES (format)

### What Goes in CHECKS (not GUIDE or RULES)

- "Agent must have run `/verify` after implementation" → CHECKS (action evidence)
- "Sources must have been actually visited, not hallucinated" → CHECKS (process proof)
- "Tests must have been executed, not just written" → CHECKS (execution evidence)
- "Tracking files updated after each commit" → CHECKS (sequence evidence)

### Boundary Test

Ask: "Can I verify this by reading the delivered files?"
- Yes → RULES
- No, needs action traces → CHECKS
- Neither, it's strategic advice → GUIDE

## 5. Consumers and Workflows

```
GUIDE
├── Working agent (during /build, /implement, /solve)
└── /critique (implicit standards for logic review)

RULES
├── /verify (primary consumer - structural compliance)
├── /improve (fix quality issues against standards)
└── /reconcile (prioritize fixes using rules as reference)

CHECKS
└── /adp (audit process discipline post-execution)
```

**No overlap**: Each workflow consumes exactly one GRUC component as primary source. This prevents token waste from reading irrelevant criteria.

## 6. Naming Conventions

### Per-Skill Files

```
[AGENT_FOLDER]/skills/[skill-name]/
├── SKILL.md              (entry point)
├── SKILL_GUIDE.md        (approach guidance)
├── SKILL_RULES.md        (output verification rules)
├── SKILL_CHECKS.md       (process discipline checks)
└── [other files]
```

### Domain-Specific Rules Files

When a skill has multiple distinct domains, rules split by domain:

```
[AGENT_FOLDER]/skills/write-documents/
├── SKILL_GUIDE.md         (general writing guidance)
├── SKILL_RULES.md         (general output rules)
├── WORKFLOW_RULES.md      (workflow-specific rules)
├── SPEC_RULES.md          (specification-specific rules)
├── TRANSLATION_RULES.md   (translation-specific rules)
└── CONVERSATION_RULES.md  (conversation-specific rules)
```

Pattern: `[DOMAIN]_RULES.md` when SKILL_RULES.md would exceed ~200 lines.

### Per-Workflow Files (Future)

```
[AGENT_FOLDER]/workflows/
├── verify.md
├── verify_CHECKS.md       (what /adp checks about /verify executions)
└── ...
```

## 7. Accumulation from FAILS.md

GRUC files are NOT static. They accumulate over time:

1. Agent makes a mistake → logged in FAILS.md
2. User invokes `/learn` → extracts pattern
3. Pattern becomes a new rule or check:
   - Output quality failure → new item in RULES
   - Process discipline failure → new item in CHECKS
   - Strategic error → new item in GUIDE

**Direction**: FAILS.md → `/learn` → GRUC file update (user-triggered only)

This creates a feedback loop where past failures become future prevention criteria.

## 8. Current Implementation Status

**Realized:**
- `*_RULES.md` files exist in `@skills:write-documents` (7 files), `@skills:coding-conventions` (10 files), `@skills:deep-research` (5 files)
- `SKILL_GUIDE.md` exists in `@skills:write-documents`
- `/verify` consumes RULES files
- `/adp` workflow deployed (does not yet consume CHECKS files)

**Not yet realized:**
- `SKILL_CHECKS.md` files do not exist in any skill
- `/adp` does not look for or consume CHECKS files
- Most skills lack GUIDE files
- No per-workflow CHECKS files exist

**Next steps:**
1. Create first `SKILL_CHECKS.md` for a well-understood skill (e.g., `@skills:deep-research`)
2. Update `/adp` to consume CHECKS files when present
3. Add GUIDE files to skills that involve complex decision-making

## 9. How to Write Good GRUC Documents

### 9.1 Writing RULES Files

A RULES file is a verification lookup table. Its reader is `/verify` or `/improve` - workflows that need to check output against standards fast.

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

A GUIDE file is strategic coaching. Its reader is the working agent before starting a task. It shapes HOW the agent approaches work.

**Structure pattern** (derived from `SKILL_GUIDE.md`):

```
# [Domain] Guide

[One-line purpose statement]

## 1. [First Decision/Step]

[Decision framework or classification]

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

**Anti-patterns:**

- Verifiable output requirements → belongs in RULES (move it there)
- Checklist of "must have X section" → RULES content disguised as guidance
- Overly prescriptive step-by-step → becomes a workflow, not a guide
- No decision points → guide adds no value over the workflow steps themselves

### 9.3 Writing CHECKS Files

A CHECKS file is a process discipline audit. Its reader is `/adp` after the working agent finished. The working agent NEVER sees this file during execution.

**Structure pattern** (not yet implemented; designed from GRUC theory):

```
# [Domain] Checks

[One-line: what process discipline this audits]

**Evidence sources:** conversation logs, git history, file timestamps, terminal output

## Check Index

Process ([2-letter prefix])
- [PREFIX]-[CAT]-[NN]: [Action that must have happened]

## [Check ID]: [Check Name]

**Evidence**: [What proves the action occurred]
**Failure indicator**: [What absence or contradiction indicates non-compliance]
**Severity**: CRITICAL | HIGH | MEDIUM
```

**Principles:**

1. **Action-oriented** - Each check describes something the agent MUST HAVE DONE, not something the output must contain. "Agent ran `/verify`" not "Document passes verification."
2. **Evidence-based** - Every check specifies what evidence proves compliance. Without defined evidence, a check is unenforceable.
3. **Failure indicators** - Describe what NON-compliance looks like. Helps the auditing workflow detect violations quickly.
4. **Severity levels** - CRITICAL (indicates fundamental process failure), HIGH (significant quality risk), MEDIUM (process shortcut with limited impact).
5. **Invisible to executor** - CHECKS files must NOT be referenced in workflows, SKILL.md intent lookups, or MNF sections. Only `/adp` reads them.
6. **No output requirements** - If checkable from the delivered files alone, it belongs in RULES. CHECKS require action traces: timestamps, conversation evidence, git commits, command output.
7. **Sequence matters** - Order checks by expected execution sequence. First checks verify early-stage actions (planning, research), later checks verify late-stage actions (verification, commit).

**Anti-patterns:**

- "Output file must have section X" → RULES content (move to RULES file)
- Check without evidence definition → unenforceable guess
- Check visible to working agent → gaming risk (agent performs action superficially to pass)
- Too many CRITICAL checks → severity inflation, everything becomes noise

### 9.4 Cross-File Consistency

When writing a complete GRUC set for a skill:

1. **No overlaps** - Each requirement lives in exactly one file. If uncertain, apply the Boundary Test (section 4).
2. **No gaps** - Together, GUIDE + RULES + CHECKS should cover strategy, output, and process. Missing file = missing coverage.
3. **Consistent terminology** - Same concept uses same name across all three files. If RULES calls it "Rule Index", GUIDE should not call it "Rule Summary."
4. **Same prefix** - All IDs within one skill use the same prefix. `WF-HD-01` (RULES), `WF-` prefix for hypothetical CHECKS items.
5. **GUIDE references RULES** - GUIDE may say "Apply SK-FL-* rules for file layout" pointing to RULES for specifics. GUIDE provides strategy, RULES provides exact standards.
6. **CHECKS references neither** - CHECKS stands alone. Auditor should not need GUIDE or RULES to evaluate process compliance.

## Document History

**[2026-06-12 17:42]**
- Added: Section 9 (How to Write Good GRUC Documents) with patterns from existing RULES and GUIDE files

**[2026-06-12 17:36]**
- Initial document created
