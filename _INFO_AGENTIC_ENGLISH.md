# INFO: Agentic English

**Doc ID**: AGEN-IN01
**Goal**: Define a controlled vocabulary for agent-human communication in workflows, skills, and documents

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

**Use in all workflows to prevent ambiguous instructions and hardcoded values:**

- `[VERB]` - Defined activity, entity, or placeholder (e.g., `[RESEARCH]`, `[VERIFY]`, `[ACTOR]`)
- `[VERB]-OK` - Successful outcome of activity, proceed to next step
- `[VERB]-FAIL` - Failed outcome, re-iterate or escalate
- `[VERB]-SKIP` - Intentionally skipped (complexity doesn't require it)
- `[VERB-VARIANT]` - Specific variant of a verb (e.g., `[WRITE-IMPL]`, `[WRITE-TEST]`)
- `[VERB](input)` - Verb with input parameter (e.g., `[WRITE-IMPL](SPEC)` = write impl plan from spec)
- `STATE-NAME` - Defined state that maps to different verb sequences (e.g., `COMPLEXITY-HIGH`, `HOTFIX`)

## Placeholders

### Decision Context

- **[ACTOR]** - Decision-making entity (default: user, in /go-autonomous: agent)

### Folder Paths

- **[WORKSPACE_FOLDER]** - Absolute path of root folder where agent operates
- **[PROJECT_FOLDER]** - Absolute path of project folder (same as workspace if no monorepo)
- **[SESSION_FOLDER]** - Absolute path of currently active session folder
- **[SRC_FOLDER]** - Absolute path of source folder
- **[AGENT_FOLDER]** - Agent config folder (`.windsurf/` or `.claude/`)

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

### Information Gathering

- **[RESEARCH]** - Web search, read docs, explore options
- **[ANALYZE]** - Study code, data, or documents

### Thinking and Planning

- **[PLAN]** - Create structured approach
- **[DECIDE]** - Make a choice between options
- **[ASSESS]** - Assess effort/time/risk
- **[PRIORITIZE]** - Order by importance

### Validation and Proof

- **[PROVE]** - POC (Proof of Concept), spike, minimal test to validate idea
- **[PROTOTYPE]** - Build working draft to test approach at scale
- **[VERIFY]** - Check against rules/specs
- **[TEST]** - Run automated tests
- **[REVIEW]** - Inspect work (open-minded)
- **[CRITIQUE]** - Find problems (devil's advocate)
- **[RECONCILE]** - Bridge gap between ideal and feasible (pragmatic programmer)

### Documentation

- **[WRITE]** - Generic write action (use specific variants below)
- **[WRITE-INFO]** - Write INFO document (research findings)
- **[WRITE-SPEC]** - Write SPEC document (specification)
- **[WRITE-IMPL]** - Write IMPL document (implementation plan)
- **[WRITE-TEST]** - Write TEST document (test plan)
- **[OUTLINE]** - Create high-level structure

### Implementation

- **[IMPLEMENT]** - Write code or implement proposed changes
- **[CONFIGURE]** - Set up or update environment/settings
- **[INTEGRATE]** - Connect components
- **[REFACTOR]** - Restructure existing code to meet requirements
- **[FIX]** - Correct issues
- **[IMPROVE]** - Enhance quality
- **[OPTIMIZE]** - Rewrite or change existing code to work more efficiently

### Communication

- **[CONSULT]** - Request input, clarification, decisions
- **[STATUS]** - Write status report
- **[PROPOSE]** - Suggest options for decision (2 for linear, 3+ for multi-dimensional problems)
- **[VALIDATE]** - Confirm with [ACTOR]
- **[ENUMERATE]** - Generate list of options before proposing

### Completion

- **[HANDOFF]** - Transfer to next phase/person
- **[COMMIT]** - Git commit
- **[MERGE]** - Combine branches
- **[DEPLOY]** - Push to environment
- **[FINALIZE]** - Perform all activities to allow for task closure
- **[CLOSE]** - Mark as done and sync data to container (task, project, session, feature)
- **[ARCHIVE]** - Archive closed

## Complexity Levels

Maps to semantic versioning:

- **COMPLEXITY-LOW** - Single file, clear scope, no dependencies → patch version
- **COMPLEXITY-MEDIUM** - Multiple files, some dependencies, backward compatible → minor version
- **COMPLEXITY-HIGH** - Breaking changes, new patterns, external APIs, architecture → major version

## Problem Types

- **HOTFIX** - Production down, immediate action required
- **BUGFIX** - Defect in existing functionality
- **CHORE** - Technical debt, cleanup, refactoring
- **MIGRATION** - Data or API migration
- **REVIEW** - Code review, audit
- **ASSESSMENT** - Research and options analysis

## Document History

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
