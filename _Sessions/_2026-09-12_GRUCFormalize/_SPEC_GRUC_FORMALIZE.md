# SPEC: GRUC Formalization - Extended CHECKS, Workflow Separation, EXAMPLE File Type

**Doc ID**: GRUC-SP01
**Goal**: Formalize GRUC architecture by extending CHECKS with quality improvement checks, separating workflow concerns to eliminate overlap, and adding EXAMPLE file type

**Timeline**: Created 2026-09-12, 0 updates, target 2026-09-12

**Depends on:**
- `docs/_INFO_GRUC_GUIDES_RULES_CHECKS.md [GRUC-IN01]` for current GRUC theory
- `.devin/skills/drift-control/SKILL.md` for current CHECKS placement
- `.devin/workflows/verify.md` for current verify behavior
- `.devin/workflows/critique.md` for current critique behavior
- `.devin/workflows/drift-detect.md` for current drift-detect behavior
- `.devin/workflows/improve.md` for current improve behavior

**Does not depend on:**
- Any SPEC or IMPL for specific project code

## MUST-NOT-FORGET

1. Preserve existing RULES file IDs and structure - no renaming or renumbering
2. Do not break workflow references from other workflows (21 files reference `/verify`, 8 reference `/critique`, 3 reference `/improve`)
3. CHECKS files remain invisible to working agent during execution
4. EXAMPLE files are a new GRUC type - need naming convention, structure, writing guide
5. Each workflow reads exactly ONE GRUC file type as primary source
6. Reduce overlap - no workflow duplicates another's checking scope
7. GUIDES link to EXAMPLE files - this is the connection mechanism
8. CHECKS QI items are high-level quality questions, NOT structural rules (those stay in RULES)

## 1. Problem

Current GRUC implementation has three issues:

### 1.1 CHECKS Too Narrow

CHECKS currently covers only Process Discipline (action evidence post-execution). Missing: high-level quality assessment with improvement tips per document type. Example: "Is the SPEC serving the stated goal? Did it make all necessary decisions? Does it avoid unnecessary complexity? Did we fact-check all assumptions?"

### 1.2 Workflow Overlap

Four quality workflows (`/verify`, `/critique`, `/drift-detect`, `/improve`) overlap significantly:

- `/verify` reads RULES + SOCAS + fact-check + privacy scan + formatting checks
- `/critique` reads FAILS + SOCAS + research + context-specific review questions
- `/improve` reads RULES + SOCAS + research + context-specific improvements
- `/drift-detect` builds DoD from SPEC/IMPL/TASKS (not from CHECKS)

SOCAS appears in 3 of 4 workflows. RULES are read by both verify and improve. Research is done by both critique and improve. This wastes tokens and produces duplicate findings.

### 1.3 No EXAMPLE File Type

RULES files contain BAD/GOOD pairs (small snippets). Missing: larger GOOD examples showing how to solve different use cases. Agents need to see complete or substantial document examples to understand quality expectations.

## 2. Solution

### 2.1 Extended CHECKS Purpose (GRUC-FR-01)

CHECKS files get two categories:

**Process Discipline (PD)** - existing, unchanged:
- Actions that must have happened (tests run, sources visited, backups made)
- Evidence requirements, sequence compliance, depth indicators
- Consumed by `/drift-detect`

**Quality Improvement (QI)** - new:
- High-level quality questions per document type
- Improvement tips ("Add diagrams to INFO files", "Deepen research", "Write better summaries")
- Not structural rules (those stay in RULES) - judgment-based assessment
- Consumed by `/improve`

**CHECKS structure pattern:**

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
**Evidence**: [What proves compliance / What to assess]
**Failure indicator**: [What absence or contradiction indicates non-compliance]
**Improvement tip**: [For QI: specific tip for improvement]
**Severity**: CRITICAL | HIGH | MEDIUM
```

**Example QI items for SPECs:**
- GRUC-QI-01: Is the SPEC serving the stated goal? (Check: Goal field vs actual content)
- GRUC-QI-02: Did the SPEC make all necessary decisions? (Check: open questions, unresolved alternatives)
- GRUC-QI-03: Does the SPEC avoid unnecessary complexity in dependencies? (Check: dependency count, simpler alternatives)
- GRUC-QI-04: Were all assumptions fact-checked? (Check: [ASSUMED] labels without verification)

### 2.2 Workflow Separation (GRUC-FR-02)

Each workflow reads exactly ONE GRUC file type:

```
verify.md    → ONLY reads [TOPIC]_RULES.md
critique.md  → ONLY reads [TOPIC]_GUIDES.md (+ EXAMPLE files linked from GUIDES)
drift-detect → ONLY reads [TOPIC]_CHECKS.md (PD section)
improve.md   → ONLY reads [TOPIC]_CHECKS.md (QI section)
```

**What moves where:**

| Current location | Content | Moves to |
|---|---|---|
| verify.md | SOCAS conceptual verification | critique.md (GUIDES-driven) |
| verify.md | Minimal fact-check | improve.md (CHECKS QI) |
| verify.md | Privacy leak scan | Stays as RULES content (already in agent-behavior.md) |
| verify.md | Formatting/acronym/table/emoji rules | Already in RULES files (APAPALAN, core-conventions) |
| critique.md | Research phase (5 topics, web search) | Removed (GUIDES provide direction) |
| critique.md | FAILS.md reading | Removed (FAILS is for /learn, not critique) |
| critique.md | SOCAS application | Replaced by GUIDES-driven review |
| drift-detect | DoD from SPEC/IMPL/TASKS | Replaced by CHECKS PD items |
| improve.md | RULES reading (Phase 2) | Removed (verify.md handles rule violations) |
| improve.md | SOCAS scanning | Replaced by CHECKS QI items |
| improve.md | Research phase | Replaced by CHECKS QI improvement tips |

### 2.3 Updated Workflow Behaviors

#### verify.md (GRUC-FR-03)

**Scope**: Structural compliance only. Reads RULES files, checks output against them.

**Removed**: Conceptual verification (SOCAS), minimal fact-check, privacy leak scan (already in RULES via agent-behavior.md and core-conventions.md).

**Kept**: 
- GLOBAL-RULES that reference existing RULES files (formatting, acronyms, tables, emojis)
- Verification labels ([ASSUMED], [VERIFIED], [TESTED], [PROVEN])
- Context-specific sections that read RULES files
- Cross-document verification (reads Source vs File, checks alignment)
- Final Steps (re-read, check MNF)

**Procedure**:
1. Detect context (document type)
2. Read applicable RULES files
3. Create verification task list from RULES
4. Check each rule against output
5. Apply fixes immediately
6. Final Steps (re-read, verify MNF)

#### critique.md (GRUC-FR-04)

**Scope**: Strategic gap analysis. Reads GUIDES files to find what's missing, what went wrong, what the [ACTOR] did incorrectly.

**Removed**: Research phase (5 topics, web search), FAILS.md reading, SOCAS application.

**Kept**:
- Devil's Advocate questions (generic quality questions)
- Context-specific review questions (adapted to use GUIDES as reference)
- Output files (_REVIEW.md, FAILS.md for actual failures found)
- Final Checklist

**New**:
- Read GUIDES files for the document type being reviewed
- Use GUIDES decision frameworks to assess whether the right approach was taken
- Use GUIDES quality heuristics to find gaps
- Follow EXAMPLE file links from GUIDES to compare against ideal output
- Report what's missing vs what GUIDES recommend

**Procedure**:
1. Determine context (document type)
2. Read applicable GUIDES files (if no GUIDES exist, report "No GUIDE available for [type], limited review possible")
3. Follow EXAMPLE links from GUIDES for quality reference
4. Create Devil's Advocate task list from GUIDES criteria
5. Work through task list:
   - Compare output against GUIDES decision frameworks
   - Check if recommended approaches were taken
   - Find gaps between GUIDES recommendations and actual output
   - Update _REVIEW.md with findings
6. Run Final Checklist

#### drift-detect.md (GRUC-FR-05)

**Scope**: Process discipline audit. Reads CHECKS files (PD section) to assess instruction following and drift.

**Removed**: DoD extraction from SPEC/IMPL/TASKS/etc. Replaced by CHECKS PD items.

**Kept**:
- Context detection (Code Implementation, Deep Research, Generic)
- Assessment statuses (PASS, FAIL, MISSED, N/A)
- Drift report format
- Log mode (DRIFTS.md)

**New**:
- Read CHECKS files for the relevant skill/workflow
- Use PD items as assessment criteria (replaces DoD)
- Meta-criteria observations remain (observational, not scored)

**Procedure**:
1. Detect context and topic
2. Read applicable CHECKS files (PD section)
3. For each PD item, assess status against action evidence
4. Note meta-criteria observations
5. Persist to __DRIFT_[TOPIC].md
6. Report

#### improve.md (GRUC-FR-06)

**Scope**: Quality improvement. Reads CHECKS files (QI section) for improvement ideas and tips.

**Removed**: Phase 2 (fix rule violations - handled by verify.md), RULES reading, SOCAS scanning.

**Kept**:
- Phase 1 (scan) - now scans CHECKS QI items instead of SOCAS
- Phase 3 (focused improvement) - selects ONE improvement from QI items
- Phase 4 (quality polish) - APAPALAN + MECT
- Pragmatic filter
- Backup gate
- STRUT self-tracking
- Deferred improvements file

**New**:
- Read CHECKS QI items as improvement candidates
- Each QI item is a pre-calculated improvement opportunity
- QI items may reference specific improvement actions (add diagrams, fact-check, deepen research)

**Procedure**:
1. Setup (scope, context, backup, STRUT)
2. Phase 1: Read CHECKS QI items, classify as improvement candidates
3. Phase 2: (removed - verify.md handles rule violations)
4. Phase 3: Select ONE QI improvement, research, apply pragmatic filter, apply or defer
5. Phase 4: Quality polish (APAPALAN + MECT)
6. Evaluation, cleanup

### 2.4 EXAMPLE File Type (GRUC-FR-07)

**Purpose**: Show larger GOOD examples that demonstrate how to solve different use cases. Go beyond simple BAD/GOOD pairs in RULES.

**Naming**: `[TOPIC]_EXAMPLE_[NN]-[ExampleName].md`
- Example: `SPEC_EXAMPLE_01-TodoListReactApp.md`
- Example: `INFO_EXAMPLE_01-ApiComparison.md`

**Location**: In skill folders, alongside RULES and GUIDES:
```
[AGENT_FOLDER]/skills/write-documents/
├── SKILL_GUIDES.md
├── SPEC_RULES.md
├── SPEC_EXAMPLE_01-TodoListReactApp.md
├── SPEC_EXAMPLE_02-AuthenticationSystem.md
└── ...
```

**Structure pattern**:
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

**Principles**:
1. **Complete or substantial** - Not snippets. Show enough to understand the full approach
2. **Use-case specific** - Each example solves a specific problem type
3. **Linked from GUIDES** - GUIDES reference EXAMPLE files for quality reference
4. **No BAD examples** - EXAMPLES show only GOOD. BAD/GOOD pairs stay in RULES
5. **Generic content** - No project-specific data (Pre-Write Privacy Gate applies)

**GUIDES linking pattern**:
```markdown
## 2. Determine Skill Type

For SPEC documents, consider the complexity:
- Simple CRUD → See `SPEC_EXAMPLE_01-TodoListReactApp.md`
- Multi-component system → See `SPEC_EXAMPLE_02-AuthenticationSystem.md`
```

### 2.5 Updated Consumer Mapping (GRUC-FR-08)

```
GUIDE
├── Working agent (during /build, /implement, /solve)
└── /critique (strategic gap analysis using GUIDES + EXAMPLES)

RULES
└── /verify (structural compliance, output-only verification)

CHECKS (PD)
└── /drift-detect (process discipline audit, action evidence)

CHECKS (QI)
└── /improve (quality improvement, judgment-based assessment)

EXAMPLES
├── Linked from GUIDES
└── Referenced by /critique for quality comparison
```

**No overlap**: Each workflow consumes exactly one GRUC component. EXAMPLES are linked from GUIDES, not consumed directly by workflows.

### 2.6 Updated Lifecycle Positioning (GRUC-FR-09)

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
│   └── RULES consumed by /verify
│       "Does the output meet structural standards?"
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

## 3. Design Decisions

### GRUC-DD-01: CHECKS QI items are not RULES

RULES are verifiable from output alone (structural). QI items are judgment-based quality questions. They require reading and understanding the document, not just checking structure. This distinction keeps RULES mechanical and CHECKS QI thoughtful.

### GRUC-DD-02: critique.md no longer does external research

The research phase (5 web search topics) added value but created overlap with improve.md. GUIDES now contain the strategic knowledge that research was meant to bring. If GUIDES are insufficient, the solution is to improve the GUIDES, not to do research in critique.md.

### GRUC-DD-03: improve.md Phase 2 removed

Phase 2 (fix rule violations) duplicated verify.md's purpose. With verify.md handling all rule violations, improve.md focuses on quality improvement (Phase 3) and polish (Phase 4). This eliminates the overlap.

### GRUC-DD-04: drift-detect DoD replaced by CHECKS PD

Currently drift-detect builds DoD from SPEC/IMPL/TASKS. This is expensive (reads many files) and duplicates knowledge already encoded in CHECKS. CHECKS PD items are pre-calculated process discipline criteria. This is the original GRUC vision - pre-calculate once, look up fast.

### GRUC-DD-05: EXAMPLES linked from GUIDES, not consumed directly

EXAMPLES are not a fourth GRUC file type consumed by a workflow. They are a resource linked from GUIDES. This keeps the 1:1 workflow-to-GRUC mapping clean while providing rich examples.

### GRUC-DD-06: Privacy scan stays in verify.md via RULES

Privacy scan is currently embedded in verify.md's GLOBAL-RULES. The actual privacy rules are in `agent-behavior.md` (a rules file). verify.md keeps the privacy scan procedure but reads the criteria from the rules file. This is consistent with "verify.md ONLY reads RULES".

## 4. Affected Files

### Files to Modify

1. `docs/_INFO_GRUC_GUIDES_RULES_CHECKS.md` - Update with new CHECKS purpose, EXAMPLE type, consumer mapping, lifecycle
2. `.devin/workflows/verify.md` - Strip to RULES-only
3. `.devin/workflows/critique.md` - Switch to GUIDES-driven review
4. `.devin/workflows/drift-detect.md` - Switch to CHECKS-driven assessment
5. `.devin/workflows/improve.md` - Switch to CHECKS-driven improvements, remove Phase 2
6. `.devin/skills/drift-control/SKILL.md` - Update CHECKS description for dual purpose
7. `.devin/skills/drift-control/DRIFT_DETECTION.md` - Update to consume CHECKS PD items

### Files to Create

8. First CHECKS file (e.g., `SPEC_CHECKS.md` in write-documents) - to demonstrate the new QI pattern

### Files NOT Modified

- Existing `*_RULES.md` files - no changes to IDs or structure
- Existing `*_GUIDES.md` files - may add EXAMPLE links later, but not in this change
- `reconcile.md` - unchanged (consumes _REVIEW.md files, not GRUC files directly)
- Other workflows referencing `/verify`, `/critique`, `/improve` - references still valid

## 5. Acceptance Criteria

- **GRUC-AC-01**: verify.md reads ONLY RULES files, no SOCAS, no fact-check, no conceptual verification
- **GRUC-AC-02**: critique.md reads ONLY GUIDES files, no research phase, no FAILS.md, no SOCAS
- **GRUC-AC-03**: drift-detect.md reads ONLY CHECKS files (PD), no DoD extraction from SPEC/IMPL
- **GRUC-AC-04**: improve.md reads ONLY CHECKS files (QI), no RULES reading, no SOCAS, no Phase 2
- **GRUC-AC-05**: CHECKS files have PD and QI sections
- **GRUC-AC-06**: EXAMPLE file type defined with naming convention and structure pattern
- **GRUC-AC-07**: GRUC INFO document updated with all changes
- **GRUC-AC-08**: No existing RULES IDs broken
- **GRUC-AC-09**: No workflow references from other workflows broken
- **GRUC-AC-10**: Consumer mapping shows 1:1 workflow-to-GRUC with no overlap

## Document History

**[2026-09-12 13:10]**
- Initial specification created
