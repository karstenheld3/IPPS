# SPEC: AGEN - Agentic English

**Doc ID**: AGEN-SP01
**Goal**: Define a controlled vocabulary for agent-human communication in workflows, skills, and documents

**See also:**
- `SPEC_EDIRD_PHASE_MODEL.md [EDIRD-SP04]` for phase model using these verbs

## Table of Contents

- [Purpose](#purpose)
- [Usage](#usage)
- [Syntax](#syntax)
- [Placeholders](#placeholders)
- [Atomic Activities (Verbs)](#atomic-activities-verbs)
- [Labels](#labels)
- [States](#states)
- [Document History](#document-history)

## Purpose

Agentic English is a controlled vocabulary that prevents ambiguous instructions and hardcoded values in agent-facing content. It provides:

- **Consistency** - Same verb means the same action across all workflows
- **Composability** - Verbs can be chained, nested, and parameterized
- **Traceability** - Outcomes can be tracked (`-OK`, `-FAIL`, `-SKIP`)
- **Abstraction** - Placeholders like `[ACTOR]` adapt to context (user or agent)

## Usage

### In Workflows

Workflows use `[VERBS]` to define steps and reference skills using `@skill-name`:

```
## Required Skills
- @write-documents for document structure

## Steps
1. [RESEARCH] existing solutions
2. [ANALYZE] affected code
3. [CONSULT] with [ACTOR] if unclear
4. [IMPLEMENT] changes
5. [VERIFY] against spec
```

### In Skills

Skills are **extensions to verbs** - they provide detailed instructions for complex verb actions. Skills use `[PLACEHOLDERS]` but not `[VERBS]`:

```
## File Naming
- Create `_SPEC_[COMPONENT].md` in [SESSION_FOLDER]
- See `[AGENT_FOLDER]/rules/devsystem-ids.md` for IDs
```

When a workflow needs `[WRITE-SPEC]`, it invokes `@write-documents` skill for detailed guidance.

### In Documents (SPEC, IMPL, TEST)

Documents use `[VERBS]` and `[PLACEHOLDERS]` in their structure:

```
## Implementation Steps
1. [CONFIGURE] database connection at [SRC_FOLDER]/config
2. [IMPLEMENT] API endpoints
3. [TEST] with sample data
```

### In Notes (NOTES.md, PROGRESS.md)

Tracking files use verbs for status:

```
## Current Status
- [RESEARCH]-OK: Found 3 options
- [PROVE]-FAIL: POC did not work, need [CONSULT]
```

## Syntax

Agentic English has two token types with distinct syntax:

### Instructions `[BRACKETS]`

Use brackets for tokens that appear in **instructions** - things the agent reads and DOES:

- `[VERB]` - Action to execute (e.g., `[RESEARCH]`, `[VERIFY]`, `[IMPLEMENT]`)
- `[PLACEHOLDER]` - Value to substitute (e.g., `[ACTOR]`, `[WORKSPACE_FOLDER]`)
- `[LABEL]` - Classification to apply (e.g., `[UNVERIFIED]`, `[CRITICAL]`)

**Important:** Only UPPERCASE tokens in brackets are instructions. Lowercase content like `[x]` (checkbox) or `[link text](url)` is regular Markdown, not AGEN syntax.

**Verb modifiers:**

- `[VERB]-OK` - Successful outcome, proceed to next step
- `[VERB]-FAIL` - Failed outcome, re-iterate or escalate
- `[VERB]-SKIP` - Intentionally skipped (complexity doesn't require it)
- `[VERB-VARIANT]` - Specific variant (e.g., `[WRITE-IMPL-PLAN]`, `[WRITE-TEST-PLAN]`)
- `[VERB](input)` - Verb with parameter (e.g., `[WRITE-IMPL-PLAN](SPEC)`)

**Example instruction:**
```
In [WORKSPACE_FOLDER], [WRITE-INFO] about dependencies. Mark as [UNVERIFIED] if no source.
```

### States `NO-BRACKETS`

No brackets for tokens that appear in **conditions** - things the agent checks for branching:

- `PREFIX-VALUE` format (e.g., `SINGLE-PROJECT`, `COMPLEXITY-HIGH`, `HOTFIX`)
- Used in conditional headers and branching logic
- Never substituted or executed - only checked

**Example branching:**
```
## For SINGLE-PROJECT
[WRITE-INFO] in [WORKSPACE_FOLDER]

## For MONOREPO  
[WRITE-INFO] in [PROJECT_FOLDER] for each project

## If COMPLEXITY-HIGH
[PROVE] with POC before [IMPLEMENT]
```

### Quick Reference

- **Brackets `[XXX]`** = Instruction stream (do / substitute / tag)
- **No brackets `XXX-YYY`** = Condition headers (if / when / for)
- **Grep instructions**: `\[[A-Z_-]+\]`
- **Grep conditions**: `[A-Z]+(-[A-Z]+)?`

## Placeholders

### Decision Context

- **[ACTOR]** - Decision-making entity (default: user, in /go-autonomous: agent)

### Folder Paths

- **[WORKSPACE_FOLDER]** - Absolute path of root folder where agent operates
- **[PROJECT_FOLDER]** - Absolute path of project folder (same as workspace if no monorepo)
- **[SESSION_FOLDER]** - Absolute path of currently active session folder
- **[SRC_FOLDER]** - Absolute path of source folder
- **[AGENT_FOLDER]** - Agent config folder (`.windsurf/` or `.claude/`)

**Override example in `!NOTES.md`:**
```
[SESSION_FOLDER]: [WORKSPACE_FOLDER]\_PrivateSessions
[DEFAULT_SESSIONS_FOLDER]: [WORKSPACE_FOLDER]\_PrivateSessions
[SESSION_ARCHIVE_FOLDER]: [DEFAULT_SESSIONS_FOLDER]\_Archive
```

### Configuration

- **[DEVSYSTEM]** - Current DevSystem version (e.g., `DevSystemV2.1`)
- **[DEVSYSTEM_FOLDER]** - Path to DevSystem folder
- **[RULES]** - Agent rules in `[AGENT_FOLDER]/rules/`
- **[WORKFLOWS]** - Agent workflows in `[AGENT_FOLDER]/workflows/`
- **[SKILLS]** - Agent skills in `[AGENT_FOLDER]/skills/`

### Document Templates

- **[COMPONENT]** - Component name for file naming (e.g., `_SPEC_[COMPONENT].md`)
- **[TOPIC]** - Topic prefix for IDs (e.g., `AUTH`, `CRWL`)

## Atomic Activities (Verbs)

Reusable activities that can be used within any phase. Use as markers like `[RESEARCH]`, `[PROVE]`, `[TEST]`.

**Extensibility**: Verbs are abstract concepts that CAN be concretized as dedicated workflows, but this is not required. Complex verbs benefit from workflows (e.g., `[COMMIT]` → `/commit`, `[CRITIQUE]` → `/critique`), while simple verbs work inline within phase workflows. New verbs can be added to extend the vocabulary as needed.

### Information Gathering

- **[RESEARCH]** - Web search, read docs, explore options
- **[ANALYZE]** - Study code, data, or documents
- **[EXPLORE]** - Open-ended investigation without specific target
- **[INVESTIGATE]** - Focused inquiry into specific issue or question
- **[GATHER]** - Collect information, logs, context, requirements
- **[PRIME]** - Load most relevant information into model context
- **[READ]** - Careful, thorough reading of provided content with attention to detail

### Thinking and Planning

- **[SCOPE]** - Define boundaries and constraints
- **[FRAME]** - Structure the problem or approach
- **[PLAN]** - Create structured approach with steps
- **[DECOMPOSE]** - Break large plan into small testable steps, each with verification criteria
- **[DECIDE]** - Make a choice between options
- **[ASSESS]** - Assess effort, time, risk, or complexity
- **[PRIORITIZE]** - Order by importance or urgency
- **[EVALUATE]** - Compare options against criteria, score, rank
- **[SYNTHESIZE]** - Combine findings into coherent understanding
- **[CONCLUDE]** - Draw conclusions from analysis
- **[DEFINE]** - Establish clear definitions or criteria
- **[RECAP]** - Analyze context, revisit plan, identify current status
- **[CONTINUE]** - Forward-looking assessment, execute next items on plan
- **[GO]** - Sequence of [RECAP] + [CONTINUE] until goal reached

### Validation and Proof

- **[PROVE]** - POC (Proof of Concept), spike, minimal test to validate idea
- **[PROTOTYPE]** - Build working draft to test approach at scale
- **[VERIFY]** - Check against formal rules, specs, and conventions (compliance)
- **[TEST]** - Run automated tests
- **[REVIEW]** - Inspect work (open-minded)
- **[CRITIQUE]** - Find flaws in logic, strategy, and goal alignment (disregards formal rules)
- **[RECONCILE]** - Bridge gap between ideal and feasible, balance trade-offs (disregards formal rules)

### Documentation

- **[WRITE]** - Generic write action (based on context)
- **[WRITE-INFO]** - Write INFO document (research findings)
- **[WRITE-SPEC]** - Write SPEC document (specification)
- **[WRITE-IMPL-PLAN]** - Write IMPL document (implementation plan)
- **[WRITE-TEST-PLAN]** - Write TEST document (test plan)
- **[OUTLINE]** - Create high-level structure
- **[SUMMARIZE]** - Create concise summary of longer content
- **[EXPLAIN]** - Provide clear explanation of concept or decision
- **[DOCUMENT]** - Record information for future reference
- **[DRAFT]** - Create initial version for review

### Implementation

- **[IMPLEMENT]** - Write code or implement proposed changes
- **[CONFIGURE]** - Set up or update environment/settings
- **[INTEGRATE]** - Connect components
- **[REFACTOR]** - Restructure code per stated goal (SPEC, IMPL, or instruction)
- **[FIX]** - Correct issues
- **[IMPROVE]** - General quality improvements (robustness, error handling, flow, clarity, comments)
- **[OPTIMIZE]** - Performance, memory, or efficiency improvements only

### Communication

- **[CONSULT]** - Request input, clarification, decisions from [ACTOR]
- **[CLARIFY]** - Make something clearer or resolve ambiguity
- **[QUESTION]** - Ask specific questions to gather information
- **[STATUS]** - Write status report
- **[PROPOSE]** - Present multiple options for [ACTOR] to choose from
- **[RECOMMEND]** - Suggest single option with rationale (use with [DECIDE])
- **[VALIDATE]** - Confirm approach or result with [ACTOR]
- **[ENUMERATE]** - Generate comprehensive list before proposing
- **[PRESENT]** - Share findings or results with [ACTOR]
- **[COMPARE]** - Show side-by-side differences (not scored like [EVALUATE])

### Completion

- **[HANDOFF]** - Transfer to next phase/person
- **[COMMIT]** - Git commit
- **[MERGE]** - Combine branches
- **[DEPLOY]** - Push to environment
- **[FINALIZE]** - Perform all activities to allow for task closure
- **[CLOSE]** - Mark as done and sync data to container (task, project, session, feature)
- **[ARCHIVE]** - Archive closed

## Labels

Labels classify and mark items. Unlike verbs (actions) and placeholders (substitutions), labels categorize.

### Assumption Labels

Use in reviews and problem tracking:

- **[UNVERIFIED]** - Assumption made without evidence
- **[CONTRADICTS]** - Logic conflicts with other statement/code
- **[OUTDATED]** - Assumption may no longer be valid
- **[INCOMPLETE]** - Reasoning missing critical considerations

### Failure Categories

Use in FAILS.md:

- **[CRITICAL]** - Will definitely cause production failure
- **[HIGH]** - Likely to cause failure under normal conditions
- **[MEDIUM]** - Could cause failure under specific conditions
- **[LOW]** - Minor issue, unlikely to cause failure

### Status Labels

Use in tracking files:

- **[RESOLVED]** - Issue fixed, documented for reference
- **[WONT-FIX]** - Acknowledged risk, accepted trade-off
- **[NEEDS-DISCUSSION]** - Requires [CONSULT] with [ACTOR]

## States

States are condition tokens (no brackets) used for branching. Format: `PREFIX-VALUE`.

### Workspace Context

Detected during `/prime`:

- **SINGLE-PROJECT** - Workspace contains one project
- **MONOREPO** - Workspace contains multiple independent projects
- **SINGLE-VERSION** - One active version, no migration
- **MULTI-VERSION** - Side-by-side versions (e.g., V1 and V2 coexisting)
- **SESSION-BASED** - Time-limited session with specific goals
- **PROJECT-WIDE** - Work spans entire project without session boundaries

### Complexity Assessment

Determined during `[ASSESS]`, maps to semantic versioning:

- **COMPLEXITY-LOW** - Single file, clear scope, no dependencies → patch version
- **COMPLEXITY-MEDIUM** - Multiple files, some dependencies, backward compatible → minor version
- **COMPLEXITY-HIGH** - Breaking changes, new patterns, external APIs, architecture → major version

### Operation Modes

Determines where implementation outputs are placed:

- **IMPL-CODEBASE** - (default) Output to project source folders. For: SPEC, IMPL, TEST, [IMPLEMENT], HOTFIX, BUGFIX
- **IMPL-ISOLATED** - Output to `[SESSION_FOLDER]/` only. For: [PROVE], POCs, prototypes, self-contained test scripts. Requires active session.

## Document History

**[2026-01-20 19:05]**
- Added: [READ] - Careful reading of provided content (Information Gathering)
- Added: [RECAP] - Analyze context, revisit plan, identify status (Thinking and Planning)
- Added: [CONTINUE] - Forward-looking assessment, execute next items (Thinking and Planning)
- Added: [GO] - Sequence of RECAP + CONTINUE until goal reached (Thinking and Planning)

**[2026-01-20 10:41]**
- Fixed: Updated stale EDIRD cross-references to consolidated SPEC_EDIRD_PHASE_MODEL.md [EDIRD-SP04]

**[2026-01-15 23:48]**
- Added: Operation Modes states (IMPL-CODEBASE, IMPL-ISOLATED)

**[2026-01-15 20:09]**
- Added: [PRIME] - Load most relevant information into model context (Information Gathering)

**[2026-01-15 19:53]**
- Added: [DECOMPOSE] - Break large plan into small testable steps (Thinking and Planning)

**[2026-01-15 19:18]**
- Added: Information Gathering - [EXPLORE], [INVESTIGATE], [GATHER]
- Added: Thinking and Planning - [SCOPE], [FRAME], [DEFINE]
- Added: Documentation - [SUMMARIZE], [EXPLAIN], [DOCUMENT], [DRAFT]
- Added: Communication - [CLARIFY], [QUESTION], [PRESENT], [COMPARE]
- Changed: Improved descriptions for existing verbs
- Removed: Workflow Type and Problem Type (moved to EDIRD spec)

**[2026-01-15 19:12]**
- Added: Workflow Type states (BUILD, SOLVE)
- Added: SOLVE problem types (RESEARCH, ANALYSIS, EVALUATION, WRITING, DECISION)
- Changed: Renamed "Problem Type" to "Problem Type (BUILD workflow)"
- Added: Cross-references to EDIRD variation specs

**[2026-01-15 19:09]**
- Added: [EVALUATE] - Compare options against criteria, score, rank (Thinking)
- Added: [SYNTHESIZE] - Combine findings into coherent understanding (Thinking)
- Added: [CONCLUDE] - Draw conclusions from analysis (Thinking)
- Added: [RECOMMEND] - Suggest single option with rationale (Communication)
- Changed: [PROPOSE] description clarified - present multiple options for choice

**[2026-01-15 18:39]**
- Fixed: Verb disambiguation (OPTIMIZE=performance, IMPROVE=general quality, REFACTOR=per goal)
- Fixed: Grep pattern for states to match single-word states

**[2026-01-15 18:23]**
- Fixed: Document type INFO → SPEC in title
- Changed: Cross-reference to EDIRD Phase Model spec

**[2026-01-15 17:42]**
- Changed: Rewrote Syntax section with clear instruction vs condition distinction
- Changed: Merged Complexity Levels and Problem Types into States section
- Added: Workspace States (SINGLE-PROJECT, MONOREPO, etc.)
- Added: Quick Reference with grep patterns
- Added: Example branching syntax
- Updated: TOC to reflect new structure

**[2026-01-15 17:30]**
- Added: Labels section with Assumption, Failure, and Status labels
- Updated: TOC to include Labels

**[2026-01-15 17:17]**
- Added: Table of Contents
- Added: Cross-reference to INFO_PROJECT_PHASES_OPTIONS.md
- Fixed: Clarified why STATE-NAME doesn't use brackets

**[2026-01-15 16:54]**
- Fixed: Placeholders section with correct definitions from devsystem-core.md
- Added: Folder Paths, Configuration, Document Templates subsections

**[2026-01-15 16:52]**
- Changed: Clarified usage relationships - workflows use [VERBS], skills extend verbs
- Changed: Skills use [PLACEHOLDERS] but not [VERBS]
- Changed: Documents use both [VERBS] and [PLACEHOLDERS]

**[2026-01-15 16:46]**
- Initial document created from INFO_PROJECT_PHASES_OPTIONS.md
- Added: Purpose section explaining why Agentic English exists
- Added: Usage section with examples for workflows, skills, documents, notes
- Added: Complete verb reference with categories
