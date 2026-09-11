# IPPS - Insanely Productive Programming System

A development system for AI-assisted coding workflows, optimized for a single programmer working with AI agents.

**Philosophy:** One programmer, structured workflows, AI handling the cognitive overhead. Inspired by Douglas Engelbart's intelligence augmentation and Frederick Brooks' "surgical team" concept - but replacing the support team entirely with AI. No sync meetings, no communication costs, minimum coordination necessary.

**Why all this structure?** AI agents are powerful but inconsistent. Without constraints, they:
- Interpret instructions differently each time
- Skip important steps or over-engineer simple tasks
- Lose context across sessions
- Make the same mistakes repeatedly

IPPS solves this through **deterministic agent behavior**:
- **AGEN** (AGENtic English) eliminates ambiguity - same verb always means same action (users can extend)
- **EDIRD** (Explore, Design, Implement, Refine, Deliver) prevents skipped steps - gates enforce quality before progress
- **STRUT** (STRUctured Thinking) tracks state - agent always knows where it is in the plan
- **TRACTFUL** (Traceable Requirements Artifacts and Coded Templates For Unified Lifecycle) preserves knowledge - every detail is covered by documents that survive session boundaries

The goal: Run [`/go`](.devin/workflows/go.md) and watch the agent execute a multi-session project autonomously, picking up exactly where it left off, never repeating past failures.

## Core Concepts

IPPS is built on ten integrated concepts that enable autonomous agent operation:

- **[AGEN - Agentic English](specs/_SPEC_AGEN_AGENTIC_ENGLISH.md)** - Controlled vocabulary with verbs `[VERB]`, placeholders `[PLACEHOLDER]`, and states `STATE`. Eliminates ambiguity in agent instructions. **When**: Writing workflows, specs, or any instruction the agent must execute reliably.

- **[EDIRD - Phase Model](specs/_SPEC_EDIRD_PHASE_MODEL.md)** - Five-phase workflow (Explore, Design, Implement, Refine, Deliver) with gates and deterministic next-action logic. Supports BUILD (code) and SOLVE (knowledge) workflows. **When**: Any multi-step task - the `/go` workflow follows EDIRD automatically.

- **[STRUT - Structured Thinking](specs/_SPEC_STRUT_STRUCTURED_THINKING.md)** - Tree notation for planning and tracking agent work. Uses unique IDs (`P1`, `P1-S1`, `P1-D1`), checkbox states (`[ ]`, `[x]`, `[N]`), and transitions for flow control. **When**: Complex tasks with multiple steps, dependencies, or parallel work streams.

- **[TRACTFUL - Document Framework](specs/_SPEC_TRACTFUL_DOCUMENT_FRAMEWORK.md)** - Document types (INFO, SPEC, IMPL, TEST, TASKS) with unique IDs and traceability. Defines how documents reference each other and track progress. **When**: Specification-driven development - research → spec → plan → test → implement.

- **[MNF - MUST-NOT-FORGET Technique](specs/_INFO_MNF_TECHNIQUE.md)** - Checklist technique preventing critical oversights. Workflows and documents declare MNF items; agent verifies compliance before completion. **When**: Tasks where skipping a step causes data loss, security issues, or broken deployments.

- **[APAPALAN - Writing Principle](specs/_INFO_APAPALAN_PRINCIPLE.md)** - As Precise As Possible (Priority 1), As Little As Necessary (Priority 2). Enforceable rules in [`APAPALAN_RULES.md`](.devin/skills/write-documents/APAPALAN_RULES.md) for precision, brevity, structure, and naming. **When**: Writing any document, code comment, or agent instruction.

- **[MECT - Minimal Explicit Consistent Terminology](specs/_INFO_MECT_PHILOSOPHY.md)** - Writing quality philosophy. Rules in [`MECT_WRITING_RULES.md`](.devin/skills/write-documents/MECT_WRITING_RULES.md) (voice, word choice, terminology, headings, lists) and [`MECT_CODING_RULES.md`](.devin/skills/coding-conventions/MECT_CODING_RULES.md) (naming, functions, comments, logs, errors). **When**: Naming variables, writing headings, ensuring one term per concept.

- **[SOCAS - Signs of Confusion and Sloppiness](specs/_INFO_SOCAS_SIGNS_OF_CONFUSION_AND_SLOPPINESS.md)** - 17 criteria for ranking web search results and evaluating agent output quality. Rules in [`SOCAS_RULES.md`](.devin/skills/write-documents/SOCAS_RULES.md). Used by `/deep-research`, `/improve`, and `/verify`. **When**: Evaluating research quality, reviewing agent output, ranking search results.

- **[GRUC - Guides, Rules, Checks](specs/_INFO_GRUC_GUIDES_RULES_CHECKS.md)** - Drift-prevention technique using three file types: GUIDE (before execution, planning strategy), RULES (whole lifecycle, output verification), CHECKS (after execution, process audit). Separation prevents gaming: CHECKS invisible during work, GUIDE invisible during audit. **When**: Building skills that need quality enforcement without self-gaming.

- **[AMINTON - Agentic MINTO Notation](specs/_INFO_AGENTIC_MINTO_ARTICLES.md)** - Tree notation for Minto Pyramid articles. Node types: A (root argument), Q (questions), QnAn (answers), QnAn-Sn (sub-questions), QnAn-SnEn (evidence). Enables machine verification of argument completeness. Used by `/propose-minto` and `/write-minto`. **When**: Writing structured argumentative articles with verifiable completeness.

**How they work together:**
```
AGEN provides the language    → Verbs, placeholders, outcomes (-OK, -FAIL, -SKIP)
EDIRD provides the phases     → EXPLORE → DESIGN → IMPLEMENT → REFINE → DELIVER
STRUT provides the notation   → Tree structure for plans with progress tracking
TRACTFUL provides the docs    → INFO, SPEC, IMPL, TEST, TASKS with unique IDs
MNF provides the safety net   → Critical items that must be verified before completion
APAPALAN provides precision   → Precision first, brevity second (35 enforceable rules)
MECT provides consistency     → Voice, terminology, naming across documents and code
SOCAS provides quality gates  → 17 criteria detecting confusion and sloppiness
GRUC prevents drift           → Pre-calculated criteria for verify, drift-detect, improve
AMINTON provides arguments    → Tree notation for structured, verifiable Minto articles
```

**Design principle:** Each spec has a single responsibility. AGEN defines vocabulary. EDIRD defines phases and gates. STRUT defines notation. TRACTFUL defines documents. MNF prevents oversights. APAPALAN enforces precision and brevity. MECT ensures consistent terminology. SOCAS detects quality degradation. GRUC prevents drift. AMINTON structures arguments. Workflows orchestrate them without hardcoding phase knowledge.

**Example** - A hotfix plan in STRUT notation:
```
[ ] P1 [IMPLEMENT]: Fix and verify
├─ Objectives:
│   └─ [ ] Bug no longer reproduces ← P1-D2, P1-D3
├─ Strategy: Locate bug, apply minimal fix, test, commit
├─ [ ] P1-S1 [ANALYZE](stack trace)
├─ [ ] P1-S2 [IMPLEMENT](null check fix)
├─ [ ] P1-S3 [TEST]
├─ [ ] P1-S4 [FIX](if tests fail)
├─ [ ] P1-S5 [COMMIT]("fix: null check in getUserById")
├─ Deliverables:
│   ├─ [ ] P1-D1: Root cause identified
│   ├─ [ ] P1-D2: Fix implemented
│   ├─ [ ] P1-D3: Tests pass
│   └─ [ ] P1-D4: Committed
└─> Transitions:
    - P1-D1 - P1-D4 checked → [END]
    - Tests fail after 3 attempts → [CONSULT]
```

**Key elements**: Objectives link to Deliverables (`← P1-D2, P1-D3`), steps use AGEN verbs, checkboxes track state.

## Table of Contents

- [Core Concepts](#core-concepts)
- [Overview](#overview)
- [How to Add to Your Project](#how-to-add-to-your-project)
- [Workflows Reference](#workflows-reference)
- [Skills Reference](#skills-reference)
- [File Naming Conventions](#file-naming-conventions)
- [Usage Examples](#usage-examples)
- [Agentic English](#agentic-english)
- [EDIRD Phase Model](#edird-phase-model---explore-design-implement-refine-deliver)
- [STRUT - Structured Thinking](#strut---structured-thinking)
- [TRACTFUL - Document Framework](#tractful---document-framework)
- [Agentic Concepts and Strategies](#agentic-concepts-and-strategies)
- [Key Conventions](#key-conventions)
- [Agent Tools](#agent-tools)
- [Project Structure](#project-structure)
- [Workspaces and Sessions](#workspaces-and-sessions)
- [PromptSystem Versions](#promptsystem-versions)
- [Agent Compatibility](#agent-compatibility)

## Overview

IPPS provides structured rules, workflows, and skills for AI agents to follow consistent conventions during pair programming sessions. The current version (V4.4) features ten integrated concepts: AGEN vocabulary, EDIRD phases, STRUT notation, TRACTFUL documents, MNF checklists, APAPALAN precision, MECT (Minimal Explicit Consistent Terminology) consistency, SOCAS quality criteria, GRUC drift prevention, and AMINTON (Agentic Minto) arguments.

### Who is this for?

- **Solo developers** who use AI agents (Windsurf Cascade, Claude Code, etc.) as their primary coding partner and want consistent, repeatable results
- **Teams** who need agents to follow the same conventions across sessions, projects, and repositories
- **Anyone** who has experienced an AI agent "forgetting" context, skipping steps, or making the same mistake twice

### What does it look like in practice?

A typical workflow session:

1. You open your IDE and type `/prime` - the agent reads your project rules, past failures, and current state
2. You type `/go "Add pagination to the user list endpoint"` - the agent creates a session, researches the codebase, writes a spec, creates a STRUT plan, implements the code, runs tests, and commits
3. If the agent makes a mistake, you type `/fail "Forgot to handle empty result sets"` - the failure is recorded in `FAILS.md`
4. Next session, `/prime` reads that failure - the agent will not repeat it
5. When you type `/go "Fix the pagination bug"` next week, the agent reads the failure, avoids the mistake, and fixes it correctly the first time

Over time, the `FAILS.md` file becomes a hardening layer - each mistake is recorded and prevented in future sessions. The agent gets better at your specific project because it learns from its errors.

## How to Add to Your Project

Copy the `.devin/` folder to your VS Code or Windsurf workspace root:
```
your-project/
└── .devin/
    ├── rules/
    ├── workflows/
    └── skills/
```

Then configure workspace files:
1. **NOTES.md** — Copy from [DEV_REPO_NOTES_TEMPLATE.md](.devin/skills/workspace-management/DEV_REPO_NOTES_TEMPLATE.md), set `[WORKSPACE_FOLDER]` and other constants
2. **ID-REGISTRY.md** — Copy from [ID-REGISTRY_TEMPLATE.md](.devin/skills/workspace-management/ID-REGISTRY_TEMPLATE.md), add your project topics
3. **SOPS.md** — Create standard operating procedures for your project
4. **SETUP.md** — Run in each skill folder that requires external tools (pdf-tools, llm-evaluation, github, etc.)

Or run [`/workspace-setup`](.devin/workflows/workspace-setup.md) for an interactive guided setup.

### Quick Start (3 steps)

1. **Copy `.devin/` to your project root** - That's it. The agent now has rules, workflows, and skills.
2. **Create `NOTES.md`** - Copy the template, fill in your project name and goal. This is the first file the agent reads.
3. **Start working** - Type `/prime` in your IDE chat, then `/go "your task description"`. The agent handles the rest.

### What happens after setup?

```
You type: /prime
  → Agent reads NOTES.md, rules, FAILS.md, ID-REGISTRY.md
  → Agent knows your project name, conventions, and past mistakes

You type: /go "Add user registration endpoint"
  → Agent creates a session folder
  → Agent follows EDIRD: research → spec → plan → implement → test → commit
  → Agent creates tracking files (NOTES.md, PROGRESS.md, PROBLEMS.md)
  → Agent implements the code, runs tests, commits

You close IDE, come back next day:
You type: /prime, then /session-load
  → Agent reads session PROGRESS.md, picks up where it left off
```

## Workflows Reference

48 workflows in `.devin/workflows/`. Workflows are invoked by typing the slash command in your IDE chat (e.g., `/go`, `/verify`).

**Entry Points** - Start here. Use `/prime` at session start, `/go` for any task.
- [`/go`](.devin/workflows/go.md) - Autonomous loop until goal reached (BUILD or SOLVE mode, auto-creates session, follows EDIRD)
  - **Creates**: session folder (`_YYYY-MM-DD_Topic/`) with `NOTES.md`, `PROBLEMS.md`, `PROGRESS.md`; SPEC/IMPL/TEST/TASKS documents in session folder; `__STRUT_*.md` plan files; source code files in `src/`
  - **Edits**: source code, session tracking files, `FAILS.md` (on failures), `LEARNINGS.md` (on learning)
  - **When**: Primary entry point for any task. Pass a goal string: `/go "Add user auth"`. Run without arguments to resume.
- [`/prime`](.devin/workflows/prime.md) - Prime context with workspace files
  - **Creates**: nothing (read-only)
  - **Edits**: nothing (read-only)
  - **When**: At the start of every session. Reads `!NOTES.md`, `PROBLEMS.md`, `FAILS.md`, `LEARNINGS.md`, `ID-REGISTRY.md`, all `.devin/rules/*.md`

**Document Cycle** - Spec-Driven Development pipeline. Use for COMPLEXITY-MEDIUM/HIGH features.
- [`/research`](.devin/workflows/research.md) - Structured research with verification labels and source retention
  - **Creates**: `_INFO_[TOPIC].md` in session folder (research findings with `[VERIFIED]`/`[ASSUMED]` labels, source links)
  - **Edits**: nothing (creates new file only)
  - **When**: Gathering information before writing a spec. Use for any research that needs source tracking.
- [`/deep-research`](.devin/workflows/deep-research.md) - Deep research (MEPI or MCPI) with domain-specific patterns
  - **Creates**: `_INFO_[TOPIC].md` with multi-source analysis; `__TASKS_[TOPIC]_RESEARCH.md` (scaffolding for research tracking)
  - **Edits**: nothing (creates new files only)
  - **When**: Multi-source technology evaluation, product comparison, or any question requiring thorough investigation with MEPI (curated options) or MCPI (exhaustive options) patterns.
- [`/write-info`](.devin/workflows/write-info.md) - Create INFO document from research
  - **Creates**: `_INFO_[TOPIC].md` from template, populated with research findings
  - **Edits**: nothing (creates new file only)
  - **When**: Formalize research findings into a structured document with source IDs and verification labels.
- [`/write-spec`](.devin/workflows/write-spec.md) - Create specification from requirements
  - **Creates**: `_SPEC_[TOPIC].md` with FR (requirements), DD (design decisions), IG (implementation guarantees), AC (acceptance criteria)
  - **Edits**: nothing (creates new file only)
  - **When**: Before implementation. Defines WHAT to build, not HOW. Required for COMPLEXITY-MEDIUM/HIGH.
- [`/write-impl-plan`](.devin/workflows/write-impl-plan.md) - Create implementation plan from spec
  - **Creates**: `_IMPL_[TOPIC].md` with IS (implementation steps), EC (edge cases), VC (verification checklist)
  - **Edits**: nothing (creates new file only)
  - **When**: After `/write-spec`. Defines HOW to build. References spec by Doc ID.
- [`/write-test-plan`](.devin/workflows/write-test-plan.md) - Create test plan from spec
  - **Creates**: `_TEST_[TOPIC].md` with TC (test cases), test phases, setup/teardown
  - **Edits**: nothing (creates new file only)
  - **When**: After `/write-spec`, before or after `/write-impl-plan`. References spec requirements by FR-XX IDs.
- [`/write-tasks-plan`](.devin/workflows/write-tasks-plan.md) - Create tasks plan from IMPL/TEST
  - **Creates**: `TASKS_[TOPIC].md` with TK (task items) partitioned from IMPL steps
  - **Edits**: nothing (creates new file only)
  - **When**: After `/write-impl-plan` and `/write-test-plan`. Mandatory before `/implement`. Partitions work into executable items.
- [`/write-strut`](.devin/workflows/write-strut.md) - Create STRUT plans with proper format
  - **Creates**: `__STRUT_[TOPIC].md` (standalone scaffolding) or embeds STRUT in `_IMPL_*.md` / `_TASKS_*.md`
  - **Edits**: existing IMPL/TASKS documents if embedding STRUT into them
  - **When**: Complex multi-step plans with dependencies, parallel work, or conditional transitions.
- [`/write-prompts`](.devin/workflows/write-prompts.md) - Create prompt queue files for sequential headless execution
  - **Creates**: `_PROMPTS_[Topic].md` with numbered prompts for sequential LLM execution
  - **Edits**: nothing (creates new file only)
  - **When**: Batch operations where each prompt picks up where the last left off (e.g., multi-document transcription, bulk API docs update).
- [`/propose-minto`](.devin/workflows/propose-minto.md) - Generate 3 scored Agentic Minto (AMINTON) argument candidates
  - **Creates**: `_MINTO_DRAFT_[TOPIC].md` with 3 scored argument trees in AMINTON notation
  - **Edits**: nothing (creates new file only)
  - **When**: After research, before writing a structured argumentative article. You select the best candidate.
- [`/write-minto`](.devin/workflows/write-minto.md) - Develop full Minto Pyramid article from draft
  - **Creates**: `_MINTO_[TOPIC].md` with tree-first structure, then prose
  - **Edits**: the draft from `/propose-minto` (develops selected candidate into full article)
  - **When**: After `/propose-minto` and candidate selection. Produces the final article.
- [`/implement`](.devin/workflows/implement.md) - Implement approved changes
  - **Creates**: source code files in `src/` (or session folder for IMPL-ISOLATED); may create `_REVIEW.md` files from review pipelines
  - **Edits**: source code, configuration files, existing documents (if review pipeline context)
  - **When**: After `/write-tasks-plan`. Executes tasks from TASKS document. Detects context: Build (SPEC/IMPL to code) or Review Pipeline (`*_REVIEW.md` to corrections).
- [`/test`](.devin/workflows/test.md) - Run tests based on scope and context
  - **Creates**: nothing (runs existing tests, reports results)
  - **Edits**: nothing (read-only execution)
  - **When**: After `/implement`, before `/commit`. Agent detects test scope from context (unit, integration, full suite).

**Quality** - Use after implementation or document creation. `/verify` is the most common.
- [`/verify`](.devin/workflows/verify.md) - Verify work against specs and rules
  - **Creates**: nothing (read-only check, reports findings in chat)
  - **Edits**: nothing (read-only)
  - **When**: After implementation or document creation. Checks code against SPEC, documents against rules, IDs against registry.
- [`/critique`](.devin/workflows/critique.md) - Find flawed assumptions, logic errors, hidden risks
  - **Creates**: `_CRITIQUE_REVIEW.md` or `[TARGET]-RV01.md` review document with findings (risk, evidence, suggested action)
  - **Edits**: nothing (creates review document only)
  - **When**: After writing specs or design docs. Adversarial review for design flaws, not code bugs.
- [`/fact-check`](.devin/workflows/fact-check.md) - Verify factual claims against external reality
  - **Creates**: `_FACTCHECK_REVIEW.md` or `[TARGET]-RV01.md` review document with source/fact/conclusion verdicts
  - **Edits**: nothing (creates review document only)
  - **When**: When documents make concrete claims about external reality (URLs, attributions, counts, file paths). Non-destructive: does not modify the target.
- [`/reconcile`](.devin/workflows/reconcile.md) - Pragmatic review of critique and fact-check findings
  - **Creates**: nothing (produces actionable improvement list in chat)
  - **Edits**: source documents referenced in the review (applies corrections from critique/fact-check findings)
  - **When**: After `/critique` or `/fact-check`. Turns review findings into concrete fixes. Bridges review and implementation.
- [`/drift-detect`](.devin/workflows/drift-detect.md) - Post-execution drift detection
  - **Creates**: `__DRIFT_[TARGET].md` with detected gaps between rules and actual output
  - **Edits**: nothing (creates drift file only)
  - **When**: After completing a task, to check if the agent followed all rules. Uses CHECKS files from `drift-correction/`.
- [`/drift-correct`](.devin/workflows/drift-correct.md) - Close drift gaps identified by `/drift-detect`
  - **Creates**: nothing (applies corrections)
  - **Edits**: the files where drift was detected (fixes rule violations from `__DRIFT_*.md`)
  - **When**: After `/drift-detect`. Reads the drift file and applies fixes.
- [`/improve`](.devin/workflows/improve.md) - Depth-first improvement (one proven change per run)
  - **Creates**: versioned backup of target file (e.g., `SKILL_v0.md` before improving `SKILL.md`)
  - **Edits**: the target document or skill file (one improvement per run, using lenses and web research)
  - **When**: Quality improvement of any document, skill, or workflow. Always backs up first so you can compare.
- [`/sync`](.devin/workflows/sync.md) - Document synchronization
  - **Creates**: nothing (propagates changes between existing documents)
  - **Edits**: dependent documents (e.g., IMPL when SPEC changes, TEST when IMPL changes, README when features change)
  - **When**: After changes to one document affect others. Keeps cross-references and IDs consistent.
- [`/rename`](.devin/workflows/rename.md) - Global and local refactoring with exhaustive search
  - **Creates**: nothing (renames in place)
  - **Edits**: all files containing the old pattern (exhaustive search across workspace, with preview)
  - **When**: Renaming variables, functions, concepts, or any identifier that appears in multiple files. Shows all occurrences before applying.

**Problem Fixing** - Use when something is broken. `/bugfix` for code, `/fix` for anything.
- [`/fix`](.devin/workflows/fix.md) - Fix any problem by reading relevant PromptSystem knowledge
  - **Creates**: nothing (reads knowledge, applies fix)
  - **Edits**: the file(s) where the problem occurs (classifies: CODE, DOCUMENT, DESIGN, UNDERSTANDING, PROCESS, CONFIG)
  - **When**: Any problem where the agent needs to consult PromptSystem rules first. Lighter than `/bugfix`.
- [`/bugfix`](.devin/workflows/bugfix.md) - Fix bugs with full traceability
  - **Creates**: `_BugFixes/[BUG_ID]/` folder with `PROBLEMS.md`, investigation log (append-only), fix documentation
  - **Edits**: source code (the fix), `FAILS.md` (records the bug as a failure for future prevention)
  - **When**: Code defects needing full traceability (root cause, fix, test, commit). Heavier than `/fix`.

**Learning** - Use `/fail` immediately after mistakes. Use `/learn` after resolution.
- [`/fail`](.devin/workflows/fail.md) - Record a failure in FAILS.md
  - **Creates**: new entry in `FAILS.md` with unique ID (`[TOPIC]-FL-NNNN`), description, prevention rule
  - **Edits**: `FAILS.md` (appends new failure entry)
  - **When**: Immediately when the agent makes a mistake. Fresher context = better prevention rule. Feeds back into `/prime`.
- [`/learn`](.devin/workflows/learn.md) - Extract lessons from resolved problems
  - **Creates**: `LEARNINGS.md` entry with reusable pattern (`[TOPIC]-LN-NNNN`)
  - **Edits**: `LEARNINGS.md` (appends new learning entry)
  - **When**: After a problem is resolved. Extracts the pattern that worked, so future sessions can apply it.

**Sessions** - Lifecycle management. `/go` handles these automatically for most tasks.
- [`/session-new`](.devin/workflows/session-new.md) - Initialize a new development session
  - **Creates**: `_YYYY-MM-DD_[Topic]/` folder with `NOTES.md`, `PROBLEMS.md`, `PROGRESS.md` from templates
  - **Edits**: nothing (creates new session only)
  - **When**: Manual session control instead of `/go`. Use when you want to manage phases yourself.
  - **How to specify goal/type**: `/session-new` takes no arguments. Describe your task in the chat first (e.g., "I need to fix the login bug in auth module"), then run `/session-new`. The agent derives the session folder name from your description and extracts initial problems from your request. Session type (BUILD vs SOLVE) is determined later by EDIRD assessment.
- [`/session-save`](.devin/workflows/session-save.md) - Save session progress
  - **Creates**: nothing (updates existing tracking files)
  - **Edits**: session `NOTES.md`, `PROGRESS.md`, `PROBLEMS.md` (updates with current state)
  - **When**: Before closing IDE, taking a break, or switching tasks. Persists current state for resume.
- [`/session-load`](.devin/workflows/session-load.md) - Resume a development session
  - **Creates**: nothing (read-only)
  - **Edits**: nothing (read-only, loads context into agent memory)
  - **When**: Resuming work in a new session. Reads session tracking files to pick up where left off.
- [`/session-finalize`](.devin/workflows/session-finalize.md) - Finalize session, sync findings
  - **Creates**: nothing (syncs existing content to workspace level)
  - **Edits**: workspace `FAILS.md` (syncs [MEDIUM]/[HIGH] failures), `LEARNINGS.md` (syncs patterns), `PROBLEMS.md` (syncs deferred items)
  - **When**: Session goal reached. Syncs findings so future sessions benefit. Prepares for archive.
- [`/session-archive`](.devin/workflows/session-archive.md) - Archive a completed session folder
  - **Creates**: moves session folder to `_Archive/` (or `_Sessions/_Archive/`)
  - **Edits**: nothing (moves folder, does not modify files)
  - **When**: After `/session-finalize`. Moves session out of active workspace. Findings already synced.

**Communication** - Draft and track external communications. Agent drafts, user sends.
- [`/conversation-start`](.devin/workflows/conversation-start.md) - Create new conversation tracking file
  - **Creates**: `CONVERSATION_[COUNTERPARTY].md` with message history, attachments, metadata
  - **Edits**: nothing (creates new file only)
  - **When**: Starting to track a new email thread, WhatsApp conversation, or other external communication.
- [`/conversation-update`](.devin/workflows/conversation-update.md) - Update existing conversation
  - **Creates**: nothing (appends to existing file)
  - **Edits**: `CONVERSATION_*.md` (appends new messages, updates attachments)
  - **When**: New messages arrive in a tracked conversation. Keeps the conversation file current.
- [`/conversation-draft`](.devin/workflows/conversation-draft.md) - Draft messages AS the user
  - **Creates**: draft text in chat (user reviews and sends manually)
  - **Edits**: nothing (produces draft in chat only)
  - **When**: You need the agent to draft an email, WhatsApp message, or other text in your voice.
- [`/transcribe`](.devin/workflows/transcribe.md) - Transcribe PDFs and web pages to markdown
  - **Creates**: `.md` file with transcribed content (100% content preservation, no metadata)
  - **Edits**: nothing (creates new file only)
  - **When**: Converting PDFs, images, or web pages into editable markdown. Handles PDF-to-image conversion and LLM-based transcription.
- [`/translate`](.devin/workflows/translate.md) - Translate markdown, PDF, or subtitle files
  - **Creates**: translated `.md` file (or subtitle file) in target language
  - **Edits**: nothing (creates new file only)
  - **When**: Translating documentation, articles, or subtitles to one or more target languages.

**Utility** - Infrastructure and maintenance.
- [`/commit`](.devin/workflows/commit.md) - Create conventional commits
  - **Creates**: git commits with conventional messages (`type(scope): description`)
  - **Edits**: nothing (stages and commits existing changes, does not modify file content)
  - **When**: After implementation, before pushing. Groups changes by type (feat, fix, docs, test, chore).
- [`/deploy`](.devin/workflows/deploy.md) - Deploy project to configured hosting platform
  - **Creates**: deployment on Netlify, Vercel, Azure, or SharePoint
  - **Edits**: deployment configuration files if needed
  - **When**: Deploying a web application. Reads deployment config, builds, deploys.
- [`/switch-model`](.devin/workflows/switch-model.md) - Switch Cascade AI model tier
  - **Creates**: nothing (changes agent configuration)
  - **Edits**: Cascade model configuration (switches between HIGH, MID, LOW tier)
  - **When**: When task complexity changes. HIGH for analysis, MID for implementation, LOW for chores.
- [`/project-release`](.devin/workflows/project-release.md) - Create a dated release
  - **Creates**: release notes, git tag, GitHub release (if configured)
  - **Edits**: version files, `PROGRESS.md` (milestone completion)
  - **When**: Reaching a version milestone. Generates comprehensive release notes from commit history.
- [`/workspace-setup`](.devin/workflows/workspace-setup.md) - Create or modify workspace setup
  - **Creates**: `NOTES.md`, `ID-REGISTRY.md`, `promptsystem-sync.json` from templates
  - **Edits**: workspace configuration files (interactive questionnaire)
  - **When**: Setting up a new workspace or modifying existing workspace configuration.
- [`/cleanup`](.devin/workflows/cleanup.md) - Delete temporary files and artifacts
  - **Creates**: nothing (deletes files)
  - **Edits**: nothing (deletes `.tmp_*` files, `__*` scaffolding, other temp artifacts)
  - **When**: After reaching a goal, to remove temporary files. Deletes by category (temp, scaffolding, backups).
- [`/remove`](.devin/workflows/remove.md) - Remove session content or specific files
  - **Creates**: nothing (deletes files with preview)
  - **Edits**: nothing (shows preview, user confirms, then deletes)
  - **When**: Removing session content, conversation files, or specific files. Always previews first.
- [`/write-template`](.devin/workflows/write-template.md) - Create purpose-built document templates
  - **Creates**: template `.md` file with placeholders, instructions, and formatting rules
  - **Edits**: nothing (creates new file only)
  - **When**: When you need consistent, comparable document instances (e.g., review templates, analysis templates).
- [`/investigate`](.devin/workflows/investigate.md) - Structured investigation with STRUT plan
  - **Creates**: `__STRUT_*.md` plan, append-only investigation log
  - **Edits**: investigation log (appends findings, does not modify previous entries)
  - **When**: Deep investigation of complex issues. STRUT plan structures the investigation, log preserves findings.
- [`/compare-workspace-setup`](.devin/workflows/compare-workspace-setup.md) - Compare workspace setup
  - **Creates**: comparison report in chat (differences between two workspaces)
  - **Edits**: nothing (read-only comparison)
  - **When**: Comparing workspace settings, sync configs, or NOTES.md between two workspaces.

## Skills Reference

24 skills in `.devin/skills/`. Skills are knowledge bases the agent reads before executing tasks. They do not run as workflows - they provide procedures, rules, and tool guidance.

- **drift-correction** - Drift detection/correction knowledge and CHECKS files for `/drift-detect` and `/drift-correct`. **Effect**: No files. Provides CHECKS files consumed by `/drift-detect`.
- **coding-conventions** - Python, PowerShell coding style rules, MECT coding rules. **Effect**: No files. Rules consumed by `/verify` and `/improve` when checking code.
- **deep-research** - Deep research strategies (MEPI/MCPI), domain-specific patterns. **Effect**: No files. Knowledge consumed by `/deep-research` workflow.
- **edird-phase-planning** - EDIRD phase model with effort allocation, planning guidance, gates. **Effect**: No files. Rules consumed by `/go` workflow.
- **git** - Commit history navigation, file recovery from previous commits. **Effect**: No files. Procedures for git operations (log, checkout, diff, revert).
- **git-conventions** - Commit message format, .gitignore rules. **Effect**: No files. Rules consumed by `/commit` workflow.
- **github** - GitHub CLI operations (repos, issues, PRs, releases). **Effect**: No files. Procedures for `gh` CLI commands.
- **google-account** - Google services (Gmail, Calendar, Drive, Tasks) via gogcli CLI. **Effect**: No files. Procedures for gogcli commands.
- **hosting** - Platform-specific deployment to Netlify, Vercel, Azure App Service, SharePoint. **Effect**: No files. Procedures consumed by `/deploy` workflow.
- **image-tools** - Image conversion, resizing, compression, batch processing (ImageMagick, Pillow). **Effect**: Creates converted/resized image files. Edits images in place (batch operations).
- **llm-computer-use** - Desktop automation via LLM vision (click, type, navigate). **Effect**: No files. Procedures for desktop automation via screenshots and mouse/keyboard.
- **llm-evaluation** - LLM evaluation pipeline (questions, answers, scoring, cost analysis). **Effect**: Creates evaluation result files (JSON, CSV). Edits evaluation config.
- **llm-transcription** - Image/audio to markdown transcription (ensemble + judge + refinement). **Effect**: Creates `.md` transcription files. Edits nothing (creates new files).
- **ms-playwright-mcp** - Browser automation via Microsoft Playwright MCP server. **Effect**: No files directly. Provides procedures for browser automation (navigate, click, type, screenshot). Downloads go to default browser location.
- **pdf-tools** - PDF conversion, compression, analysis using Ghostscript, Poppler, QPDF. **Effect**: Creates converted PDF/image files. Edits PDFs in place (compression, optimization).
- **playwriter-mcp** - Real browser automation with existing logins via Playwriter extension. **Effect**: No files directly. Provides procedures for browser automation with existing sessions.
- **seo-tools** - SEO data APIs and search engine tools for keyword research and rank tracking. **Effect**: Creates SEO report files (CSV, JSON). Edits nothing (creates new files).
- **session-management** - Session init, save, resume, finalize, archive. **Effect**: No files directly. Procedures consumed by `/session-*` workflows. Templates for NOTES.md, PROBLEMS.md, PROGRESS.md.
- **travel-info** - Travel lookups: flights, trains, transit, country-specific info. **Effect**: Creates travel info `.md` files. Edits nothing (creates new files).
- **windows-desktop-control** - Windows screenshots, window management, keyboard/mouse. **Effect**: Creates screenshot files (PNG). Edits nothing (creates new files).
- **windsurf-auto-model-switcher** - Switch Cascade AI model tier programmatically. **Effect**: No files. Procedures for model switching via config files.
- **workspace-management** - Multi-repo workspace setup, PromptSystem synchronization, knowledge distribution. **Effect**: Creates `NOTES.md`, `ID-REGISTRY.md`, `promptsystem-sync.json` from templates. Edits workspace config files. Runs `sync.ps1` to sync PromptSystem across repos.
- **write-documents** - Document templates (INFO, SPEC, IMPL, TEST, TASKS, STRUT, MINTO), writing rules (APAPALAN, MECT, SOCAS). **Effect**: No files directly. Templates consumed by write-* workflows. Rules consumed by `/verify`, `/improve`.
- **youtube-downloader** - Download YouTube content as MP3 or video, extract metadata. **Effect**: Creates MP3/video files in download folder. Creates `.md` metadata files. Edits nothing (creates new files).

### GRUC File Placement

GRUC (Guides, Rules, Checks) files are distributed by consumer alignment:

- **GUIDE** files - in each skill folder (consumed by working agent before execution)
- **RULES** files - in each skill folder (consumed by `/verify`, `/improve` after execution)
- **CHECKS** files for skills - in each skill folder (alongside GUIDE and RULES)
- **CHECKS** files for workflows - in `drift-correction/` (consumed by `/drift-detect` after execution)

Exception: `write-documents` keeps all GRUC types in its own folder.

## File Naming Conventions

IPPS uses special prefixes to control how files are processed:

- **`!` prefix** - Priority files (e.g., `!NOTES.md`). Read first during [`/prime`](.devin/workflows/prime.md). Contains critical project information. **Effect**: Read first by `/prime`. Agent never creates `!` files - these are manually authored.
- **`_` prefix** - Deliverables ignored by automatic priming (e.g., `_SPEC_*.md`, `_INFO_*.md`). Session-specific, WIP, or archived content. Single `_` = user-created deliverable. **Effect**: Created by write-* workflows. Never auto-deleted. Survives session boundaries.
- **`__` prefix** - Workflow scaffolding (e.g., `__STRUT_TOPIC.md`, `__TASKS_TOPIC.md`). Auto-created by workflows for self-tracking. Deleted by [`/cleanup`](.devin/workflows/cleanup.md) after goal reached. Gitignored. **Effect**: Created by `/write-strut`, `/go`, `/deep-research`. Auto-deleted by `/cleanup`.
- **`.tmp_` prefix** - Single-run temp files (e.g., `.tmp_fix_quotes.ps1`). Deleted within same workflow or by `/cleanup`. Gitignored. **Effect**: Created by agent for scripts/metadata. Deleted within same workflow run.
- **`.` prefix** - Hidden files following Unix convention (e.g., `.devin/`, `.gitignore`). **Effect**: Standard Unix behavior - hidden from directory listings.

### Lifecycle Tiers

```
.tmp_  = single-run temp (scripts, metadata) → deleted within workflow or by /cleanup
__     = multi-run scaffolding (STRUTs, TASKS, templates) → deleted by /cleanup after goal
_      = deliverable (INFO, SPEC, IMPL, TEST, TASKS) → never auto-deleted
```

**Key distinction**: User-explicit = deliverable (no `__`). Workflow/skill-implicit = scaffolding (`__`).
- `/write-tasks-plan` output → `TASKS_[TOPIC].md` (user asked for it, deliverable)
- `/deep-research` auto-creates → `__TASKS_[TOPIC]_RESEARCH.md` (scaffolding, deletable)

### Suffix Conventions

- **`_gitignore` suffix** - Append before extension to exclude any file or folder from git (e.g., `data_gitignore.json`, `scratch_gitignore/`). Useful for per-file exclusion without editing `.gitignore`.

## Usage Examples

### Prime Context

**Workflows:** [`/prime`](.devin/workflows/prime.md)

Load workspace context before starting work:
```
/prime
```

The prime workflow:
1. Reads all `.md` files in `[AGENT_FOLDER]/rules/` (core conventions, system behavior)
2. Reads all `!*.md` files (priority documentation with critical project info)
3. Reads standard `.md` files in workspace root (excluding `_` and `!` prefixed)
4. Detects workspace scenario (project structure, version strategy, work mode)
5. Reports summary: files read, scenario detected

Typically loads: `README.md`, `!NOTES.md`, `PROBLEMS.md`, `FAILS.md`, `LEARNINGS.md`, `ID-REGISTRY.md`, agent rules

**When to use**: At the start of every session, or after a break. The agent needs context about your project, past failures, and current state before it can work effectively.

### Workflow Entry Points

The `/go` workflow **automatically creates a session**, follows EDIRD phases, and closes when done. It detects BUILD (code output) or SOLVE (knowledge output) mode from the task.

Start a BUILD task (create software, new features):
```
/go "Add user authentication API"
```
**Creates**: session folder, SPEC/IMPL/TEST/TASKS documents, `__STRUT_*.md` plan, source code in `src/`. **Edits**: source code, session tracking files, `FAILS.md` (on failures).

Start a SOLVE task (research, analysis, decisions):
```
/go "Evaluate database migration options"
```
**Creates**: session folder, `_INFO_*.md` research document, `__STRUT_*.md` plan. **Edits**: session tracking files. No source code (SOLVE mode produces knowledge, not code).

**When to use**: `/go` is the primary entry point for any task. Use BUILD mode for code changes, new features, bug fixes. Use SOLVE mode for research, technology evaluation, architecture decisions. The agent handles session creation, planning, execution, and cleanup automatically.

### Session Workflows

**Workflows:** [`/session-new`](.devin/workflows/session-new.md), [`/session-save`](.devin/workflows/session-save.md), [`/session-load`](.devin/workflows/session-load.md), [`/session-finalize`](.devin/workflows/session-finalize.md)

Start a new work session (describe your task first, then run the command):
```
I need to fix the login bug in the auth module - users get 500 errors when password contains special characters

/session-new
```
Creates a session folder (e.g., `_2026-09-11_FixLoginBug/`) with `NOTES.md`, `PROBLEMS.md`, `PROGRESS.md`. The agent derives the folder name from your description and extracts initial problems from your request. Session type (BUILD vs SOLVE) is determined later by EDIRD assessment.

Save progress during work:
```
/session-save
```
Saves current state to session tracking files and commits changes.

Resume an existing session:
```
/session-load
```
Re-reads session tracking files and picks up where the last session left off.

Finalize session and sync findings:
```
/session-finalize
```
Syncs FAILS and LEARNINGS to workspace level, prepares session for archive.

**When to use**: Use `/session-new` when you want manual control instead of `/go` - describe your task in the chat first so the agent can name the session and extract problems. Use `/session-save` before closing your IDE or taking a break. Use `/session-load` to resume work in a new session. Use `/session-finalize` when the session goal is reached - it syncs failures and learnings to workspace level so future sessions benefit.

### Autonomous Execution

**Workflow:** [`/go`](.devin/workflows/go.md)

Run autonomous loop until goal reached:
```
/go
```
**Creates**: nothing new if session exists. **Edits**: session tracking files, source code (if BUILD mode). Resumes from last saved state.

The [`/go`](.devin/workflows/go.md) workflow cycles through:
1. Assess state - read tracking docs, determine current position
2. Execute next - build execution sequence, run next task
3. Repeat until goal reached or blocker hit

**When to use**: After you have provided the initial goal and the agent has created a session and plan. Running `/go` again (without arguments) resumes from where the last session left off.

### Document Cycle (INFO → SPEC → IMPL → TEST → TASKS)

**Workflows:** [`/research`](.devin/workflows/research.md), [`/write-spec`](.devin/workflows/write-spec.md), [`/write-impl-plan`](.devin/workflows/write-impl-plan.md), [`/write-test-plan`](.devin/workflows/write-test-plan.md), [`/write-tasks-plan`](.devin/workflows/write-tasks-plan.md), [`/implement`](.devin/workflows/implement.md), [`/verify`](.devin/workflows/verify.md), [`/sync`](.devin/workflows/sync.md), [`/rename`](.devin/workflows/rename.md), [`/commit`](.devin/workflows/commit.md)

This follows the Spec-Driven Development (SDD) methodology used by [GitHub spec-kit](https://github.com/github/spec-kit) and [Zencoder](https://docs.zencoder.ai/user-guides/guides/spec-driven-development).

1. **Research** - Gather information:
```
/research
```
Creates `_INFO_*.md` with findings.

2. **Specify** - Create specification:
```
/write-spec
```
Creates `_SPEC_*.md` from requirements.

3. **Plan** - Create implementation plan:
```
/write-impl-plan
```
Creates `_IMPL_*.md` from spec.

4. **Test Plan** - Create test plan:
```
/write-test-plan
```
Creates `_TEST_*.md` from spec.

5. **Tasks** - Partition into discrete work items:
```
/write-tasks-plan
```
Creates `TASKS_[TOPIC].md` from IMPL/TEST. **Mandatory before implementation.**

6. **Implement** - Execute the tasks:
```
/implement
```
Reads TASKS document, executes each task. **Creates**: source code in `src/`. **Edits**: source code, config files.

7. **Verify** - Check work against specs:
```
/verify
```
Reads SPEC, checks code against requirements. **Creates**: nothing (read-only). **Edits**: nothing. Reports gaps in chat.

8. **Sync** - Update dependent documents:
```
/sync
```
Propagates changes from source to dependent docs. **Creates**: nothing. **Edits**: IMPL when SPEC changes, TEST when IMPL changes, README when features change.

9. **Rename** - Global/local pattern replacement:
```
/rename
```
Searches all files for a pattern, shows preview, replaces. **Creates**: nothing. **Edits**: all files containing the pattern.

10. **Commit** - Create conventional commits:
```
/commit
```
Groups changes by type, creates git commits. **Creates**: git commits. **Edits**: nothing (stages and commits existing changes only).

**When to use**: Use the full document cycle for complex features (COMPLEXITY-MEDIUM or HIGH). For simple changes (COMPLEXITY-LOW), `/go` handles everything inline. The document cycle ensures traceability from requirements to implementation to tests.

### Problem Fixing

**Workflows:** [`/fix`](.devin/workflows/fix.md), [`/bugfix`](.devin/workflows/bugfix.md)

Fix any problem by reading relevant PromptSystem knowledge:
```
/fix
```
**Creates**: nothing. **Edits**: the file(s) where the problem occurs. Classifies problem (CODE, DOCUMENT, DESIGN, UNDERSTANDING, PROCESS, CONFIG), reads context-specific workflows and rules, then applies that knowledge.

Fix code bugs with full traceability:
```
/bugfix "Login fails when session expires"
```
**Creates**: `_BugFixes/[BUG_ID]/` folder with `PROBLEMS.md`, investigation log, fix documentation. **Edits**: source code (the fix), `FAILS.md` (records bug as failure).

**When to use**: Use `/fix` for any problem where the agent needs to consult PromptSystem knowledge first. Use `/bugfix` for code defects that need full traceability (root cause, fix, test, commit). For simple bugs, `/go` with a bug description is sufficient.

### Quality Review

**Workflows:** [`/critique`](.devin/workflows/critique.md), [`/fact-check`](.devin/workflows/fact-check.md), [`/reconcile`](.devin/workflows/reconcile.md), [`/improve`](.devin/workflows/improve.md)

Devil's Advocate review (find flaws):
```
/critique
```
**Creates**: `_CRITIQUE_REVIEW.md` with findings (risk, evidence, suggested action). **Edits**: nothing. Non-destructive.

Fact-check document claims against external reality:
```
/fact-check
```
**Creates**: `_FACTCHECK_REVIEW.md` with source/fact/conclusion verdicts. **Edits**: nothing. Non-destructive.

Pragmatic review of critique and fact-check findings:
```
/reconcile
```
**Creates**: nothing. **Edits**: source documents (applies corrections from review findings). Destructive - modifies targets.

Depth-first improvement (one proven change per run, versioned backups):
```
/improve
```
**Creates**: versioned backup (e.g., `SKILL_v0.md`). **Edits**: the target document (one improvement per run).

**When to use**: Use `/critique` after writing specs or design docs to catch flawed assumptions. Use `/fact-check` when documents make concrete claims that need verification. Use `/reconcile` after critique or fact-check to turn findings into actionable improvements. Use `/improve` for depth-first quality improvement of any document or skill.

### Learning from Failures

**Workflows:** [`/fail`](.devin/workflows/fail.md), [`/learn`](.devin/workflows/learn.md)

Record a failure to FAILS.md:
```
/fail "Deployed without running tests"
```
**Creates**: new entry in `FAILS.md` with ID, description, prevention rule. **Edits**: `FAILS.md` (appends entry).

Extract learnings from resolved problems:
```
/learn
```
**Creates**: `LEARNINGS.md` entry with reusable pattern. **Edits**: `LEARNINGS.md` (appends entry).

**When to use**: Use `/fail` immediately when the agent makes a mistake - the fresher the context, the better the prevention rule. Use `/learn` after a problem is resolved to extract reusable patterns. Both feed back into `/prime` for future sessions.

### Testing

**Workflows:** [`/test`](.devin/workflows/test.md)

Run tests based on scope and context:
```
/test
```
**Creates**: nothing. **Edits**: nothing. Runs existing tests and reports results in chat.

**When to use**: After implementation, before committing. The agent detects test scope from context (unit, integration, or full suite).

### Planning Tools

**Workflows:** [`/write-tasks-plan`](.devin/workflows/write-tasks-plan.md), [`/write-strut`](.devin/workflows/write-strut.md), [`/write-info`](.devin/workflows/write-info.md)

Split plans into discrete tasks:
```
/write-tasks-plan
```
**Creates**: `TASKS_[TOPIC].md` with TK items. **Edits**: nothing.

Create STRUT plan with proper format:
```
/write-strut
```
**Creates**: `__STRUT_[TOPIC].md` (scaffolding) or embeds in IMPL/TASKS. **Edits**: IMPL/TASKS if embedding.

Create INFO document from research:
```
/write-info
```
**Creates**: `_INFO_[TOPIC].md` from template. **Edits**: nothing.

**When to use**: Use `/write-tasks-plan` to partition an IMPL plan into executable work items. Use `/write-strut` for complex multi-step plans with dependencies. Use `/write-info` to formalize research findings into a structured document.

### Research

**Workflows:** [`/deep-research`](.devin/workflows/deep-research.md), [`/transcribe`](.devin/workflows/transcribe.md)

Execute deep research (MEPI or MCPI):
```
/deep-research "Compare vector databases for RAG"
```
**Creates**: `_INFO_[TOPIC].md` with multi-source analysis; `__TASKS_[TOPIC]_RESEARCH.md` (scaffolding). **Edits**: nothing.

Transcribe PDFs and web pages to markdown:
```
/transcribe path/to/document.pdf
```
**Creates**: `.md` file with transcribed content. **Edits**: nothing. 100% content preservation, no metadata.

**When to use**: Use `/deep-research` for multi-source technology evaluation, product comparison, or any question requiring thorough investigation. Use `/transcribe` to convert PDFs or web pages into editable markdown - the agent handles PDF-to-image conversion and LLM-based transcription.

### Utility Workflows

**Workflows:** [`/session-archive`](.devin/workflows/session-archive.md), [`/switch-model`](.devin/workflows/switch-model.md), [`/project-release`](.devin/workflows/project-release.md)

Archive a completed session:
```
/session-archive
```
**Creates**: moves session folder to `_Archive/`. **Edits**: nothing (moves folder).

Switch Cascade AI model tier:
```
/switch-model HIGH
```
**Creates**: nothing. **Edits**: Cascade model configuration (switches tier).

Release a project version:
```
/project-release
```
**Creates**: release notes, git tag, GitHub release. **Edits**: version files, `PROGRESS.md`.

### Realistic Use Cases

The following use cases illustrate how IPPS workflows chain together in practice. All scenarios are fictional.

#### Use Case 1: Update API Documentation

**Scenario**: You maintain documentation for a public API (e.g., a payment provider) and need to update it after a major API revision.

```
# 1. Prime context - agent reads your docs conventions and past failures
/prime

# 2. Start a session for the update
#    (describe the task first, then /session-new derives folder name and problems)
I need to update our API docs after the Stripe API revision - all endpoint categories need TypeScript and Python examples

/session-new

# 3. Research what changed since the last version
/deep-research "Stripe API changes 2026-03-20 to 2026-09-05"

# 4. Create a prompt pipeline for sequential execution
#    (agent writes _PROMPTS_ApiDocsUpdate.md with prompts 2-7)
/write-prompts

# 5. Execute the prompt pipeline (or run /go to execute all prompts)
/go

# 6. Verify all topic files have correct structure
/verify

# 7. Finalize and archive
/session-finalize
/session-archive
```

**What happens**: The agent creates 50+ topic files (one per API endpoint category), each with TypeScript and Python examples, verification labels, and source links. The prompt pipeline enables headless execution - each prompt picks up where the last one left off. `/verify` checks that all files have both language examples, correct version dates, and no duplicate topic numbers.

**Files created**: `_YYYY-MM-DD_ApiDocsUpdate/` session folder; `_INFO_*.md` research findings; `_PROMPTS_ApiDocsUpdate.md` prompt queue; 50+ topic `.md` files in session subfolders. **Files edited**: `NOTES.md`, `PROGRESS.md` (session tracking); `FAILS.md` (if failures occur).

#### Use Case 2: Evaluate Technology Options

**Scenario**: You need to choose a caching layer for your web application and want a thorough comparison.

```
# 1. Start autonomous research
/go "Evaluate caching strategies: Redis vs Memcached vs DragonflyDB"

# Agent follows EDIRD:
# EXPLORE: Researches each option (features, benchmarks, pricing, community)
# DESIGN: Creates evaluation criteria and comparison matrix
# IMPLEMENT: (SOLVE mode - no code, produces INFO document)
# REFINE: /verify checks claims, /fact-check verifies benchmark numbers
# DELIVER: Recommendation document with [VERIFIED] labels
```

**Output**: An `_INFO_*.md` document with a comparison matrix, benchmark results tagged `[VERIFIED]` or `[ASSUMED]`, and a recommendation with rationale. The STRUT plan tracks which options have been researched and which criteria evaluated.

**Files created**: `_YYYY-MM-DD_CachingEval/` session folder; `_INFO_CACHING-*.md` recommendation document; `__STRUT_*.md` plan; `__TASKS_*_RESEARCH.md` research tracking. **Files edited**: session `NOTES.md`, `PROGRESS.md`.

#### Use Case 3: Fix a Production Bug

**Scenario**: Users report that password reset emails are not being sent. You need a fix with full traceability.

```
# 1. Prime context
/prime

# 2. Start bugfix with full traceability
/bugfix "Password reset emails not sent after user clicks reset"

# Agent creates [BUG_FOLDER] with:
# - PROBLEMS.md (impact assessment, root cause hypothesis)
# - Investigation log (append-only, tracks each debugging step)
# - Fix documentation (what changed, why, how tested)

# 3. After fix is implemented and tested
/verify

# 4. Commit with conventional message
/commit
```

**What happens**: The agent creates a bug folder with full traceability. It investigates the email service, finds the SMTP timeout misconfiguration, applies a minimal fix, tests it, and documents the root cause. The bug folder survives session boundaries - if the bug reappears, the investigation log shows what was checked and what was fixed.

**Files created**: `_BugFixes/[BUG_ID]/` folder with `PROBLEMS.md`, investigation log, fix documentation. **Files edited**: source code (the fix); `FAILS.md` (records bug as failure for future prevention).

#### Use Case 4: Review a Series of Articles

**Scenario**: You want to systematically review a series of technical blog posts about cloud cost optimization, checking their claims against sources.

```
# 1. Prime context
/prime

# 2. Start session
#    (describe the task first, then /session-new derives folder name and problems)
I need to review a series of cloud cost optimization blog posts and check their claims against sources

/session-new

# 3. Scrape article list and present for selection
#    (agent uses Playwright to navigate the blog, extract article URLs)
# 4. Create a review template
/write-template

# 5. For each article, run a 5-phase pipeline:
#    EXTRACT → VERIFY → COUNTER → ANALYZE → SYNTHESIZE
/go

# 6. Verify reviews against sources
/fact-check

# 7. Finalize
/session-finalize
```

**What happens**: Each article gets its own folder with the original text, images, and a standardized review. The review pipeline extracts claims, verifies them against cited sources, searches for contradicting evidence, analyzes rhetoric and bias, and synthesizes a structured review. The template ensures consistent quality across all reviews.

**Files created**: `_YYYY-MM-DD_ArticleReviews/` session folder; review template `.md`; one subfolder per article with `original.md`, `images/`, `review.md`; `_FACTCHECK_REVIEW.md` from `/fact-check`. **Files edited**: session `NOTES.md`, `PROGRESS.md`.

#### Use Case 5: Build a Feature with Full Documentation

**Scenario**: You need to add a user authentication API with JWT tokens, rate limiting, and refresh tokens. This is COMPLEXITY-HIGH.

```
# 1. Prime and start
/prime
/go "Add JWT authentication with refresh tokens and rate limiting"

# Agent follows full EDIRD cycle:
# EXPLORE: Researches auth patterns, reads existing codebase
# DESIGN: /write-spec creates _SPEC_AUTH-SP01.md
#         /write-impl-plan creates _IMPL_AUTH-IP01.md
#         /write-test-plan creates _TEST_AUTH-TP01.md
#         /write-tasks-plan creates TASKS_AUTH.md
# IMPLEMENT: /implement executes tasks from TASKS_AUTH.md
#            /test runs tests after each task
#            /fix handles failures
# REFINE: /verify checks against spec
#         /critique finds design flaws
#         /reconcile turns findings into fixes
# DELIVER: /commit creates conventional commits
#          /sync updates dependent docs
```

**Output**: A fully implemented, tested, and documented authentication system. The spec, implementation plan, test plan, and task list are all cross-referenced by ID. If a future session needs to modify the auth system, the agent reads the spec first and understands the design decisions.

**Files created**: `_SPEC_AUTH-SP01.md`, `_IMPL_AUTH-IP01.md`, `_TEST_AUTH-TP01.md`, `TASKS_AUTH.md` in session folder; `__STRUT_*.md` plan; source code in `src/` (auth module, JWT handling, rate limiting). **Files edited**: session tracking files; `FAILS.md` (if failures); existing source files (if modifying existing auth).

#### Use Case 6: Create a Comparison Guide

**Scenario**: You want to create a comprehensive comparison guide for CI/CD tools, structured as a Minto Pyramid article.

```
# 1. Research the topic
/deep-research "Compare CI/CD tools: GitHub Actions, GitLab CI, CircleCI, Jenkins"

# 2. Generate argument candidates
/propose-minto

# 3. Develop the full article from the best candidate
/write-minto

# 4. Verify argument completeness
/verify
```

**What happens**: `/deep-research` gathers information on each tool. `/propose-minto` generates 3 scored argument candidates in AMINTON notation (root argument, questions, answers, evidence). You select the best candidate. `/write-minto` develops it into a full article with tree-first structure, then prose. `/verify` checks that every question has an answer and every answer has evidence.

**Files created**: `_INFO_CICD-*.md` research findings; `_MINTO_DRAFT_CICD-*.md` 3 argument candidates; `_MINTO_CICD-*.md` final article. **Files edited**: nothing (all new files).

#### Use Case 7: Multi-Session Autonomous Project

**Scenario**: You want to build a REST API with authentication, pagination, and comprehensive tests over multiple sessions.

```
# Session 1: Foundation
/prime
/go "Build REST API foundation: project structure, routing, health endpoint"
# Agent creates session, writes spec, implements, tests, commits
/session-save

# Session 2: Authentication (next day)
/prime
/session-load
/go "Add JWT authentication to the API"
# Agent reads previous session's spec, continues building
/session-save

# Session 3: Pagination (next week)
/prime
/session-load
/go "Add cursor-based pagination to all list endpoints"
# Agent reads FAILS.md, avoids past mistakes
/session-finalize
/session-archive
```

**What happens**: Each session picks up where the last one left off. The agent reads `PROGRESS.md` to understand current state, `FAILS.md` to avoid past mistakes, and `NOTES.md` for key decisions. Sessions are archived after finalization, but their findings (failures, learnings, decisions) are synced to workspace level and persist forever.

**Files created**: 3 session folders (`_YYYY-MM-DD_*`); SPEC/IMPL/TEST/TASKS in each; source code in `src/` (routing, auth, pagination). **Files edited**: workspace `FAILS.md`, `LEARNINGS.md` (synced on `/session-finalize`); session `PROGRESS.md` (updated each session).

## Agentic English

A controlled vocabulary for agent-human communication. Provides consistent terminology across all workflows.

**Full specification**: [SPEC_AGEN_AGENTIC_ENGLISH.md](specs/_SPEC_AGEN_AGENTIC_ENGLISH.md)

**Goal**: Eliminate ambiguity in agent instructions by using bracketed verbs, placeholders, and labels.

**Rationale**: Agents interpret natural language inconsistently. Agentic English provides deterministic instructions that agents can reliably parse and execute.

**Syntax**:
- `[VERB]` - Action to execute (e.g., `[RESEARCH]`, `[VERIFY]`, `[IMPLEMENT]`)
- `[PLACEHOLDER]` - Value to substitute (e.g., `[ACTOR]`, `[WORKSPACE_FOLDER]`)
- `[LABEL]` - Classification to apply (e.g., `[UNVERIFIED]`, `[CRITICAL]`)
- `STATE` - Condition with NO brackets (e.g., `COMPLEXITY-HIGH`, `HOTFIX`, `SINGLE-PROJECT`)

**Extensibility**: Verbs are abstract concepts. Complex verbs CAN be concretized as dedicated workflows (e.g., `[COMMIT]` → [`/commit`](.devin/workflows/commit.md)), but this is optional. Simple verbs work inline within phase workflows.

**Example workflow instruction**:
```
1. [RESEARCH] affected code in [SRC_FOLDER]
2. [CONSULT] with [ACTOR] if unclear
3. [IMPLEMENT] changes
4. [VERIFY] against spec
5. [COMMIT] with conventional message
```

**Example: How AGEN prevents ambiguity** - Without AGEN, "fix the login bug" could mean different things to the agent each time. With AGEN:
```
[ANALYZE](login bug report)
[RESEARCH](authentication flow in [SRC_FOLDER])
[IMPLEMENT](null check in token validation)
[TEST](login with expired token)
[VERIFY](bug no longer reproduces)
[COMMIT]("fix: handle expired token in login")
```
Each bracketed verb maps to a specific action with a clear outcome. The agent always knows what to do.

**Example: Placeholders vs States** - Placeholders (bracketed) are values to substitute; States (no brackets) are conditions to check:
```
[ACTOR]           → Placeholder: substitute with "user" or "agent"
[WORKSPACE_FOLDER] → Placeholder: substitute with actual path
COMPLEXITY-HIGH   → State: check if the task has breaking changes
HOTFIX            → State: check if this is a hotfix scenario
```

## EDIRD Phase Model - Explore, Design, Implement, Refine, Deliver

A 5-phase workflow model for both BUILD (code) and SOLVE (knowledge/decisions) work.

**Full specification**: [SPEC_EDIRD_PHASE_MODEL.md](specs/_SPEC_EDIRD_PHASE_MODEL.md)

**Goal**: Consistent phase structure for all development work with deterministic next-action logic. We want the agent to always do the right thing when the [`/go`](.devin/workflows/go.md) workflow is executed until the initial goal is reached.

**Rationale**: Without phases, agents skip important steps or apply heavyweight processes to simple tasks. EDIRD provides the right amount of process for each complexity level.

**Effect**: No files directly. EDIRD is a phase model that orchestrates other workflows. The `/go` workflow follows EDIRD automatically, creating sessions, specs, plans, and code as needed per phase. Gates between phases enforce quality before progress.

**Phases**:
- **EXPLORE** - Understand before acting: `[RESEARCH]`, `[ANALYZE]`, `[ASSESS]`, `[SCOPE]`
- **DESIGN** - Plan before executing: `[PLAN]`, `[WRITE-SPEC]`, `[PROVE]`, `[PARTITION]`
- **IMPLEMENT** - Execute the plan: `[IMPLEMENT]`, `[TEST]`, `[FIX]`, `[COMMIT]`
- **REFINE** - Improve quality: `[REVIEW]`, `[VERIFY]`, `[CRITIQUE]`, `[RECONCILE]`
- **DELIVER** - Complete and hand off: `[VALIDATE]`, `[MERGE]`, `[DEPLOY]`, `[CLOSE]`

**Complexity mapping**:
- `COMPLEXITY-LOW` → patch version (single file, clear scope)
- `COMPLEXITY-MEDIUM` → minor version (multiple files, backward compatible)
- `COMPLEXITY-HIGH` → major version (breaking changes, architecture)

**Operation Modes**:
- `IMPL-CODEBASE` (default) → Output to project source folders
- `IMPL-ISOLATED` → Output to `[SESSION_FOLDER]/` only (for Proofs of Concept (POCs), prototypes)

**Example BUILD flow**:
```
[EXPLORE] → [ASSESS] complexity → Gate check
[DESIGN] → [WRITE-SPEC] → [PROVE] risky parts → Gate check
[IMPLEMENT] → [IMPLEMENT] → [TEST] → [FIX] → green → next → Gate check
[REFINE] → [VERIFY] against spec → [CRITIQUE] if HIGH → Gate check
[DELIVER] → [COMMIT] → [MERGE]
```

**Example SOLVE flow** (research/decision tasks - no code output):
```
[EXPLORE] → [RESEARCH] existing solutions → [ASSESS] scope → Gate check
[DESIGN] → [DEFINE] evaluation criteria → [PLAN] research approach → Gate check
[IMPLEMENT] → [RESEARCH] each option → [EVALUATE] against criteria → Gate check
[REFINE] → [VERIFY] claims → [FACT-CHECK] key assertions → Gate check
[DELIVER] → [RECOMMEND] with rationale → [COMMIT] findings document
```

**When to use BUILD vs SOLVE**: Use BUILD when the output is code (new features, bug fixes, refactoring). Use SOLVE when the output is knowledge (technology evaluation, architecture decisions, research reports). The `/go` workflow detects the mode automatically from the task description.

## STRUT - Structured Thinking

Tree notation for planning and tracking complex autonomous work.

**Full specification**: [SPEC_STRUT_STRUCTURED_THINKING.md](specs/_SPEC_STRUT_STRUCTURED_THINKING.md)

**Goal**: Provide a notation for agent plans that supports progress tracking, hierarchical decomposition, and flow control.

**Rationale**: Agents need structured plans they can parse, update, and resume across sessions. STRUT provides unique IDs for every item, checkbox states for progress, and transitions for conditional flow.

**Effect**: Creates `__STRUT_[TOPIC].md` (standalone scaffolding, deleted by `/cleanup`) or embeds STRUT in `_IMPL_*.md` / `_TASKS_*.md`. The `/write-strut` workflow creates STRUT plans. The `/go` workflow auto-creates STRUT plans during DESIGN phase.

**Five node types** (per phase, in order):
- **Objectives** - Goals linked to deliverables: `[ ] Goal ← P1-D1, P1-D2` (evidence-based verification)
- **Strategy** - Free text approach, may include AWT estimates and model hints
- **Steps** - Actions using AGEN verbs: `[ ] P1-S1 [VERB](params)` (flat list with checkboxes)
- **Deliverables** - Expected outputs: `[ ] P1-D1: Description` (checkboxes with IDs)
- **Transitions** - Flow control at phase end: `- Condition → Target` (targets: `[PHASE-NAME]`, `[CONSULT]`, `[END]`)

**ID formats**:
- **Phase ID** - `P1`, `P2`, `P3`... (unique within plan)
- **Step ID** - `P1-S1`, `P1-S2`, `P2-S1`...
- **Deliverable ID** - `P1-D1`, `P1-D2`, `P2-D1`...

**Notation features**:
- **Checkbox states** - `[ ]` pending, `[x]` done, `[N]` done N times (retry count)
- **Concurrent blocks** - Group parallel steps under `Concurrent: <strategy>`
- **Dependencies** - `← Px-Sy` suffix for explicit wait conditions

**Example 1 - BUILD plan** (hotfix):
```
[ ] P1 [IMPLEMENT]: Fix and verify
├─ Objectives:
│   └─ [ ] Bug no longer reproduces ← P1-D2, P1-D3
├─ Strategy: Locate bug, apply minimal fix, test, commit
├─ [ ] P1-S1 [ANALYZE](stack trace)
├─ [ ] P1-S2 [IMPLEMENT](null check fix)
├─ [ ] P1-S3 [TEST]
├─ [ ] P1-S4 [FIX](if tests fail)
├─ [ ] P1-S5 [COMMIT]("fix: null check in getUserById")
├─ Deliverables:
│   ├─ [ ] P1-D1: Root cause identified
│   ├─ [ ] P1-D2: Fix implemented
│   ├─ [ ] P1-D3: Tests pass
│   └─ [ ] P1-D4: Committed
└─> Transitions:
    - P1-D1 - P1-D4 checked → [END]
    - Tests fail after 3 attempts → [CONSULT]
```

**Example 2 - SOLVE plan** (technology evaluation with parallel research):
```
[ ] P1 [EXPLORE]: Evaluate database options
├─ Objectives:
│   └─ [ ] Recommendation ready ← P1-D1, P1-D2
├─ Strategy: Research 3 options in parallel, then compare (10min AWT)
├─ [ ] P1-S1 [DEFINE](evaluation criteria)
├─ Concurrent: Independent research, no shared state
│   ├─ [ ] P1-S2 [RESEARCH](PostgreSQL)
│   ├─ [ ] P1-S3 [RESEARCH](MongoDB)
│   └─ [ ] P1-S4 [RESEARCH](DynamoDB)
├─ [ ] P1-S5 [EVALUATE](compare against criteria)
├─ [ ] P1-S6 [RECOMMEND](winner with rationale)
├─ Deliverables:
│   ├─ [ ] P1-D1: Comparison matrix complete
│   └─ [ ] P1-D2: Recommendation documented
└─> Transitions:
    - P1-D1, P1-D2 checked → [END]
    - No clear winner → [CONSULT]
```

**Key difference**: BUILD plans typically use verbs like `[IMPLEMENT]`, `[TEST]`, `[FIX]`, `[COMMIT]`. SOLVE plans typically use verbs like `[RESEARCH]`, `[EVALUATE]`, `[RECOMMEND]`, `[GATHER]`, `[DEFINE]`, `[WRITE-INFO]`. Both use the same tree structure with IDs, checkboxes, and transitions.

## TRACTFUL - Document Framework

**Full specification**: [SPEC_TRACTFUL_DOCUMENT_FRAMEWORK.md](specs/_SPEC_TRACTFUL_DOCUMENT_FRAMEWORK.md)

**Goal**: Ensure all development artifacts are uniquely identified, properly structured, and traceable from ideation to maintenance.

**Rationale**: Agents need consistent document templates to create, reference, and update. TRACTFUL provides document types for each stage and a unified ID system (TDID) for cross-referencing.

**Effect**: No files directly. TRACTFUL defines the document framework (types, IDs, traceability rules). The write-* workflows (`/write-info`, `/write-spec`, `/write-impl-plan`, `/write-test-plan`, `/write-tasks-plan`) create TRACTFUL documents. `/sync` maintains cross-references between them.

**Document types**:
- **INFO** (IN) - Research findings, analysis results
- **SPEC** (SP) - Specifications with requirements and design decisions
- **IMPL** (IP) - Implementation plans with steps and edge cases
- **TEST** (TP) - Test plans with test cases and verification
- **TASKS** (TK) - Partitioned work items for execution

**ID system (TDID)**:
- **Document ID** - `[TOPIC]-[TYPE][NN]` (e.g., `AUTH-SP01`, `CRWL-IP02`)
- **Item ID** - `[TOPIC]-[ITEM]-[NN]` (e.g., `AUTH-FR-01`, `CRWL-DD-03`)
- **Cross-reference** - `filename.md [DOC-ID]`

**Example: How documents chain together**:
```
_INFO_AuthResearch.md [AUTH-IN01]     ← Research findings (from /research)
  └─> _SPEC_AuthSystem.md [AUTH-SP01] ← Specification (from /write-spec)
        ├─ AUTH-FR-01: Users can log in with email + password
        ├─ AUTH-FR-02: Failed attempts are rate-limited
        └─ AUTH-DD-01: Use JWT with 15min access + 7d refresh tokens
        └─> _IMPL_AuthSystem.md [AUTH-IP01] ← Implementation plan (from /write-impl-plan)
              ├─ AUTH-IP01-IS-01: Set up JWT middleware
              ├─ AUTH-IP01-IS-02: Implement login endpoint
              └─ AUTH-IP01-EC-01: Handle expired refresh tokens
              └─> _TEST_AuthSystem.md [AUTH-TP01] ← Test plan (from /write-test-plan)
                    ├─ AUTH-TP01-TC-01: Login with valid credentials
                    ├─ AUTH-TP01-TC-02: Login with invalid password
                    └─ AUTH-TP01-TC-03: Rate limiting triggers after 5 attempts
```

Each document references its parent by Doc ID. If a requirement changes (`AUTH-FR-02`), the agent can trace it to the test case (`AUTH-TP01-TC-03`) and update both. This traceability survives session boundaries.

## Agentic Concepts and Strategies

Acronyms and techniques used throughout IPPS for consistent agent behavior:

- **PREN** - Proper English. Precise natural language avoiding confusion, ambiguities, and term conflicts. **Effect**: No files. Controls writing style only.
- **AGEN** - Agentic English. PREN enriched with semantics: `@mentions`, `/workflow`, `[VERB]`, `[PLACEHOLDER]`. **Effect**: No files. Controls vocabulary in all workflows and specs.
- **HWT** - Human Work Time. Partition target: max 0.5h per task for predictable progress. **Effect**: No files. Guides task partitioning in `/write-tasks-plan`.
- **AWT** - Agentic Work Time. Agent time estimate for planning and capacity. **Effect**: No files. Used in STRUT strategy sections for time estimates.
- [**MEPI**](specs/_INFO_MEPI_MCPI_PRINCIPLE.md) - Most Executable Point of Information. Present 2-3 curated options aligned with implicit intentions. **Effect**: No files. Controls how options are presented in chat.
- [**MCPI**](specs/_INFO_MEPI_MCPI_PRINCIPLE.md) - Most Complete Point of Information. Present exhaustive options when thoroughness is explicitly required. **Effect**: No files. Controls option presentation (exhaustive vs curated).
- [**SOCAS**](specs/_INFO_SOCAS_SIGNS_OF_CONFUSION_AND_SLOPPINESS.md) - Signs Of Confusion And Sloppiness. 17 criteria for detecting agent degradation. **Effect**: No files. Used by `/verify`, `/improve`, `/deep-research` to evaluate output quality.
- [**MNF**](specs/_INFO_MNF_TECHNIQUE.md) - Must Not Forget. Technique for critical item tracking during task execution. **Effect**: No files directly. MNF items embedded in workflows and STRUT plans. Agent verifies compliance before completion.
- **APAPALAN** - As Precise As Possible, As Little As Necessary. Conciseness principle for workflows and documents. **Effect**: No files. 35 enforceable rules in `APAPALAN_RULES.md`. Applied by `/verify` and `/improve`.
- **VCRIV** - Verify-Critique-Reconcile-Implement-Verify. Quality pipeline for logic and design review: `/verify` → `/critique` → `/reconcile` → `/implement` → `/verify`. **Effect**: Creates `_CRITIQUE_REVIEW.md`. Edits source documents (via `/reconcile` and `/implement`).
- **FACRIV** - Fact-check-Reconcile-Implement-Verify. Quality pipeline for factual claim verification: `/fact-check` → `/reconcile` → `/implement` → `/verify`. **Effect**: Creates `_FACTCHECK_REVIEW.md`. Edits source documents (via `/reconcile` and `/implement`).

**Agent Drift Prevention**: [ADP Approach](specs/_INFO_AGENT_DRIFT_PREVENTION_APPROACH.md) - How the PromptSystem prevents agent drift through TRACTFUL, SMAP, EDIRD, STRUT, GRUC, and MNF across three scopes

**How-To Guides**:
- [How to Write Good Document Templates](specs/_INFO_HOW_TO_WRITE_GOOD_DOCUMENT_TEMPLATES.md) - Patterns and rules for unambiguous templates that agents reliably instantiate
- [How to Create Auditable Research Summaries](specs/_INFO_HOW_TO_CREATE_AUDITABLE_RESEARCH_SUMMARIES.md) - Citation and source-linking standard for 100% audit chain
- [How to Detect AI-Assisted Writing](specs/_INFO_HOW_TO_DETECT_AI_ASSISTED_WRITING.md) - Detection signals for AI-assisted writing across style, structure, reasoning, and sourcing
- [How to Check Factuality](specs/_INFO_HOW_TO_CHECK_FACTUALITY.md) - Epistemological framework, claim taxonomy, trust hierarchy, and verification methods for AI agent fact-checking
- [Bundling Workflows with Skills](specs/_INFO_HOW_TO_IMPLEMENT_WORKFLOWS_AS_SKILLS.md) - Research on migrating workflows into skill-based architecture

**Full registry**: [ID-REGISTRY.md](ID-REGISTRY.md) - All acronyms, TOPICs, states, and named concepts

## Key Conventions

- [Core Conventions](.devin/rules/core-conventions.md) - Text formatting, document structure, header blocks
- [PromptSystem Core](.devin/rules/promptsystem-core.md) - Workspace scenarios, folder structure, workflow reference
- [PromptSystem IDs](.devin/rules/promptsystem-ids.md) - Document IDs, topic registry, tracking IDs
- [Agentic English](.devin/rules/agentic-english.md) - Controlled vocabulary for agent instructions
- [EDIRD Phase Planning](.devin/rules/edird-phase-planning.md) - Phase model core rules
- [Git Conventions](.devin/skills/git-conventions/SKILL.md) - Commit message format, .gitignore rules
- [Coding Conventions](.devin/skills/coding-conventions/SKILL.md) - Python, PowerShell, workflow style rules
- [Workflow Rules](.devin/skills/write-documents/WORKFLOW_RULES.md) - Workflow document structure and formatting

## Skills

Agent skills in `.devin/skills/`. Each skill contains scripts, documentation, and optional setup.

### llm-evaluation

Evaluate LLM output quality by generating questions, collecting answers, and scoring with a judge model.

**Setup**: Run `SETUP.md` to install Python venv with OpenAI/Anthropic SDKs in `../.tools/llm-venv/`.

**Scripts**:
- `call-llm.py` - Single LLM call (image or text input)
- `call-llm-batch.py` - Batch processing with parallel workers and resume
- `generate-questions.py` - Generate evaluation questions from source content
- `generate-answers.py` - Generate answers from transcribed content
- `evaluate-answers.py` - Score answers with LLM-as-judge or OpenAI Eval API
- `analyze-costs.py` - Calculate token costs from usage files

**Quick examples**:
```powershell
$venv = "../.tools/llm-venv/Scripts/python.exe"
$skill = ".devin\skills\llm-evaluation"

# Transcribe images
& $venv "$skill\call-llm-batch.py" --model gpt-4o --input-folder images/ --output-folder out/ --prompt-file "$skill\prompts\transcribe-page.md"

# Evaluate answers
& $venv "$skill\evaluate-answers.py" --model gpt-4o --method openai-eval --input-folder answers/ --output-folder scores/
```

### llm-transcription

High-quality image-to-markdown transcription using ensemble generation, LLM judging, and conditional refinement.

**Setup**: Uses shared venv from llm-evaluation (`../.tools/llm-venv/`).

**Scripts**:
- `transcribe-image-to-markdown.py` - Ensemble pipeline with judge and refinement
- `transcribe-audio-to-markdown.py` - Audio transcription with Whisper API

**Quick examples**:
```powershell
$venv = "../.tools/llm-venv/Scripts/python.exe"
$skill = ".devin/skills/llm-transcription"

# Basic usage
& $venv "$skill/transcribe-image-to-markdown.py" --input-file doc.png --output-file doc.md --keys-file [WORKSPACE_FOLDER]/../.tools/.api-keys.txt

# With custom model and ensemble size
& $venv "$skill/transcribe-image-to-markdown.py" --input-file doc.png --output-file doc.md --keys-file [WORKSPACE_FOLDER]/../.tools/.api-keys.txt --model gpt-5-mini --initial-candidates 3
```

### llm-computer-use

Desktop automation via LLM vision. The AI sees your screen, decides what to click/type, and executes actions.

**Setup**: Uses shared venv from llm-evaluation (`../.tools/llm-venv/`). Requires Anthropic API key.

**Files**:
- `llm_computer_use/core.py` - ScreenCapture, Actions, Session, Provider
- `llm_computer_use/cli.py` - CLI entry point

**Quick examples**:
```powershell
cd .devin/skills/llm-computer-use

# Dry-run (safe, no actions executed)
python -m llm_computer_use -k [WORKSPACE_FOLDER]/../.tools/.api-keys.txt "Click the Start button"

# Execute mode
python -m llm_computer_use -x -k [WORKSPACE_FOLDER]/../.tools/.api-keys.txt "Open Notepad and type Hello World"

# Use cheaper model
python -m llm_computer_use -x -m claude-haiku-4-5 "Open Calculator"
```

**Cost**: ~$0.01-0.02 per iteration (Sonnet), ~$0.003-0.005 (Haiku). Default max 10 iterations.

### pdf-tools

Convert, compress, and analyze PDF files using local CLI tools.

**Setup**: Run `SETUP.md` to install tools in `../.tools/`:
- **7-Zip** (`../.tools/7z/`) - Archive extraction
- **Poppler** (`../.tools/poppler/`) - PDF to image, text extraction
- **QPDF** (`../.tools/qpdf/`) - PDF manipulation, optimization
- **Ghostscript** (`../.tools/gs/`) - PDF compression

**Scripts**:
- `convert-pdf-to-jpg.py` - Convert PDF pages to JPG for vision analysis
- `compress-pdf.py` - Intelligent PDF compression with strategy selection
- `downsize-pdf-images.py` - Direct Ghostscript wrapper for DPI control

**Quick examples**:
```powershell
# Convert PDF to JPG (output: ../.tools/_pdf_to_jpg_converted/)
python .devin\skills\pdf-tools\convert-pdf-to-jpg.py report.pdf --dpi 150

# Compress PDF
python .devin\skills\pdf-tools\compress-pdf.py report.pdf --compression high
```

### coding-conventions

Python and workflow coding style rules with enforcement tools.

**Files**:
- `PYTHON-RULES.md` - Formatting, imports, logging, naming conventions
- `WORKFLOW-RULES.md` - Workflow document structure and formatting
- `reindent.py` - Convert Python indentation to target spaces

**Quick examples**:
```powershell
# Convert folder to 2-space indentation
python .devin\skills\coding-conventions\reindent.py folder/ --to 2 --recursive

# Dry-run (preview only)
python .devin\skills\coding-conventions\reindent.py folder/ --to 2 --recursive --dry-run
```

### github

GitHub CLI integration for repos, issues, PRs, releases.

**Setup**: Run `SETUP.md` to install GitHub CLI in `../.tools/gh/`.

### git-conventions

Commit message format, undo/recovery commands, .gitignore rules.

**Files**:
- `SKILL.md` - Conventional commit format, safe undo, .gitignore template

**Key rules**:
- Format: `<type>(<scope>): <description>`
- Types: feat, fix, docs, refactor, test, chore, style, perf
- Imperative mood, <72 chars, no period
- Never commit secrets (.env, *.key, *.pem)

### edird-phase-planning

EDIRD phase model for long-running agentic tasks.

**Phases**: EXPLORE → DESIGN → IMPLEMENT → REFINE → DELIVER

**Files**:
- `SKILL.md` - Phase gates, workflow examples, effort allocation

**Usage**: Invoked automatically by `/go` workflow.

### ms-playwright-mcp

Browser automation via Microsoft Playwright MCP server.

**Setup**: Requires Node.js 18+ with npx in PATH.

**Key tools**:
- `browser_navigate` - Go to URL
- `browser_snapshot` - Get accessibility tree with element refs
- `browser_click` - Click element by ref
- `browser_type` - Type text into element

**Usage**: Configure in `.devin/mcp.json`, use accessibility tree refs for element selection.

### session-management

Session lifecycle management: init, save, resume, finalize, archive. Cascade conversation search and deletion.

**Files**:
- `NOTES_TEMPLATE.md` - Session notes template
- `PROBLEMS_TEMPLATE.md` - Problem tracking template
- `PROGRESS_TEMPLATE.md` - Progress tracking template
- `cascade-search.ps1` - List and search Cascade conversation .pb files by date/size
- `cascade-delete.ps1` - Delete Cascade conversations with preview and confirmation

**Usage**: Invoked by `/session-new`, `/session-load`, `/session-save`, `/session-finalize`, `/remove conversation`.

**Quick examples**:
```powershell
# List last 10 conversations
.\.devin\skills\session-management\cascade-search.ps1

# Delete conversations older than 30 days
.\.devin\skills\session-management\cascade-delete.ps1 -OlderThanDays 30
```

### windows-desktop-control

Windows desktop automation utilities.

**Scripts**:
- `simple-screenshot.ps1` - DPI-aware screenshot capture

**Quick examples**:
```powershell
# Full screen screenshot
.\.devin\skills\windows-desktop-control\simple-screenshot.ps1

# Custom output path
.\.devin\skills\windows-desktop-control\simple-screenshot.ps1 -OutputPath "C:\temp\screenshot.jpg"
```

### windsurf-auto-model-switcher

Switch Windsurf Cascade AI models programmatically.

**Setup**: Run `SETUP.md` to install keybindings, restart Windsurf.

**Scripts**:
- `select-windsurf-model-in-ide.ps1` - Select model by search query
- `windsurf-model-registry.json` - Available models and costs

**Quick examples**:
```powershell
# Select Claude Sonnet 4.5
.\.devin\skills\windsurf-auto-model-switcher\select-windsurf-model-in-ide.ps1 -Query "sonnet 4.5"
```

### write-documents

Document templates for INFO, SPEC, IMPL, TEST, TASKS, and STRUT plans.

**Templates**:
- `INFO_TEMPLATE.md` - Research and analysis
- `SPEC_TEMPLATE.md` - Technical specifications
- `IMPL_TEMPLATE.md` - Implementation plans
- `TEST_TEMPLATE.md` - Test plans
- `TASKS_TEMPLATE.md` - Task plans
- `STRUT_TEMPLATE.md` - STRUT plans
- `CRITIQUE_REVIEW_TEMPLATE.md` - Review documents from `/critique` (findings with risk/evidence/suggested action)
- `FACT-CHECK_REVIEW_TEMPLATE.md` - Review documents from `/fact-check` (source/fact/conclusion verdicts)

**Usage**: Invoked by `/write-spec`, `/write-impl-plan`, `/write-test-plan`, `/write-tasks-plan`, `/critique`, `/fact-check`.

## Agent Tools

Local tool installations in `../.tools/` (shared across workspaces). Run `SETUP.md` in each skill folder to install.

- **[MinifyIPPS](specs/_INFO_HOW_TO_MINIFY_IPPS.md)** - LLM-based compression pipeline for PromptSystem markdown files. Reduces token count while preserving meaning. Pipeline: bundle → analyze → compress → verify. **Effect**: Creates minified `.md` files in output folder. Edits nothing (creates new compressed files).

## Project Structure

```
IPPS/
├── ../.tools/                    # Shared tool installations (parent folder, created by SETUP.md scripts)
├── .devin/                    # Active agent configuration (synced from PromptSystemV4.4 by sync.ps1)
│   ├── rules/                # Agent rules (read by /prime, consumed by /verify, /improve)
│   ├── workflows/            # Workflow definitions (invoked by slash commands)
│   └── skills/               # Skill knowledge bases (read before executing tasks)
├── _OldVersions/                 # Previous PromptSystem versions (V1 through V3.8, read-only archive)
├── PromptSystemV4.4/              # Current system (source of truth, synced to .devin/)
│   ├── rules/                   # Same structure as .devin/rules/ (source)
│   │   ├── agent-behavior.md     # Agent execution patterns and communication
│   │   ├── agentic-english.md    # Controlled vocabulary for agent instructions
│   │   ├── core-conventions.md   # Text formatting, document structure, character rules
│   │   ├── promptsystem-core.md     # Workspace scenarios, folder structure, operation modes
│   │   ├── promptsystem-ids.md      # Document and item ID conventions
│   │   ├── edird-phase-planning.md # EDIRD phase model core rules
│   │   └── workspace-rules.md    # Workspace-specific overrides
│   ├── skills/                   # See Skills section for details
│   └── workflows/                # See .devin/workflows/ for file list
├── docs/                         # Product documentation, tool research, release notes (created by /research, /deep-research)
│   └── ReleaseNotes/             # Release notes per version (created by /project-release)
├── specs/                        # IPPS specs, PromptSystem methodology, guidelines (created by /write-spec)
├── ID-REGISTRY.md                # Prevents term/ID collisions (created by /workspace-setup, edited by /write-spec)
├── NOTES.md                      # Workspace constants, project info, sync rules (created by /workspace-setup)
├── PROBLEMS.md                   # Known issues across the project (edited by /session-finalize sync)
├── PROGRESS.md                   # Overall project progress (edited by /go, /session-save)
├── FAILS.md                      # Lessons learned from past mistakes (edited by /fail, /session-finalize sync)
├── SOPS.md                       # Standard operating procedures (manually created)
└── README.md
```

**Who creates what**: `/workspace-setup` creates `NOTES.md`, `ID-REGISTRY.md`, `promptsystem-sync.json`. `/session-new` creates session folders with tracking files. `/write-spec`, `/write-impl-plan`, `/write-test-plan`, `/write-tasks-plan` create TRACTFUL documents. `/fail` and `/learn` edit `FAILS.md` and `LEARNINGS.md`. `/session-finalize` syncs session findings to workspace level. `/project-release` creates release notes and tags. `sync.ps1` syncs `PromptSystemV4.4/` to `.devin/`.

## Workspaces and Sessions

IPPS uses a two-level tracking system: **workspace-level** files for project-wide information and **session-level** files for focused work periods. In MONOREPO workspaces, there's an additional **project-level** layer between workspace and sessions.

### Workspace Files

Located in workspace root (or project root in monorepos):

| File             | Required     | Purpose                                                    | Created by | Edited by |
|------------------|--------------|------------------------------------------------------------|-----------|-----------|
| `!NOTES.md`      | Yes          | Critical project info, agent instructions, key patterns    | `/workspace-setup` | Agent during sessions, `/sync` |
| `PROBLEMS.md`   | Optional     | Known issues across the project                            | Manually | `/session-finalize` (syncs deferred items) |
| `!PROGRESS.md`   | Optional     | Overall project progress                                   | Manually | `/go`, `/session-save`, `/project-release` |
| `FAILS.md`       | Auto-created | Lessons learned from past mistakes (via `/fail` workflow)  | `/fail` (auto) | `/fail` (appends), `/session-finalize` (syncs from session) |
| `LEARNINGS.md`   | Auto-created | Reusable patterns (via `/learn` workflow analyzing fails)  | `/learn` (auto) | `/learn` (appends), `/session-finalize` (syncs from session) |
| `ID-REGISTRY.md` | Yes          | Authoritative source for TOPICs, acronyms, and IDs         | `/workspace-setup` | `/write-spec` (adds new topics), agent (new concepts) |

### Session Files

Located in session folder (e.g., `_2026-01-15_FixAuthBug/`):

| File           | Required     | Purpose                                                       | Created by | Edited by |
|----------------|--------------|---------------------------------------------------------------|-----------|-----------|
| `NOTES.md`     | Yes          | Session goal, key decisions, findings, resume instructions    | `/session-new` | Agent during work, `/session-save` |
| `PROBLEMS.md`  | Yes          | Problems discovered during session (Open/Resolved/Deferred)   | `/session-new` | Agent during work, `/session-save` |
| `PROGRESS.md`  | Yes          | To-do list, in-progress, done, tried-but-not-used             | `/session-new` | `/go`, `/session-save`, agent during work |
| `FAILS.md`     | Auto-created | Session-specific failures (run `/fail` to record)             | `/fail` (auto) | `/fail` (appends entries) |
| `LEARNINGS.md` | Auto-created | Lessons from failures (run `/learn` to analyze fails)         | `/learn` (auto) | `/learn` (appends entries) |

### Session Lifecycle

```
/prime           → Load constants and documents from workspace and promptsystem
                   (README, NOTES, PROBLEMS, FAILS, LEARNINGS, ID-REGISTRY, ...)
                   Effect: Read-only. No files created or edited.
/session-new     → Create session folder with NOTES, PROBLEMS, PROGRESS
                   Effect: Creates _YYYY-MM-DD_Topic/ with 3 tracking files from templates.
    ↓
  [work]         → Create specs, implement, track progress
                   Effect: Creates _SPEC_*.md, _IMPL_*.md, _TEST_*.md, TASKS_*.md, __STRUT_*.md.
                            Edits source code in src/, session PROGRESS.md, session NOTES.md.
    ↓              (/fail to record failures → edits session FAILS.md)
    ↓              (/learn to extract lessons → edits session LEARNINGS.md)
/session-save    → Document findings, commit changes
                   Effect: Edits session NOTES.md, PROGRESS.md, PROBLEMS.md. Creates git commits.
    ↓
/session-load    → Re-read session docs, continue work
                   Effect: Read-only. Loads session tracking files into agent memory.
    ↓
/session-finalize → Sync FAILS and LEARNINGS to workspace, prepare for archive
                   Effect: Edits workspace FAILS.md, LEARNINGS.md, PROBLEMS.md (syncs from session).
    ↓
/session-archive → Move session folder to _Archive/
                   Effect: Moves session folder. No file content modified.
```

### Sync on Session Finalize

When [`/session-finalize`](.devin/workflows/session-finalize.md) runs:
- **FAILS.md** - [MEDIUM] and [HIGH] severity entries sync to workspace `FAILS.md`
- **LEARNINGS.md** - Patterns from [MEDIUM]/[HIGH] fails sync to workspace `LEARNINGS.md` or `!NOTES.md`
- **PROBLEMS.md** - Open/deferred problems sync to workspace `PROBLEMS.md`

This ensures lessons learned survive session boundaries and prevent repeated mistakes.

## PromptSystem Versions

- **[PromptSystemV4.4](PromptSystemV4.4/)** - Current system

Older versions in [`_OldVersions/`](_OldVersions/):
- DevSystemV4.2 - Quality pipelines (VCRIV, FACRIV), implement.md context branching, fact-check boundary enforcement
- DevSystemV4.1 - Conversation intelligence, agent research, write-documents refinement
- DevSystemV4.0 - GRUC drift prevention, AMINTON structured argumentation, 10 core concepts
- DevSystemV3.8 - Windsurf to Devin migration (.windsurf/ renamed to .devin/), SOP 5, Claude Opus 4.8
- DevSystemV3.7 - Deep research profiles, translation workflow, recap/continue removal, cleanup workflow
- DevSystemV3.6 - SOCAS quality criteria, 4-phase /improve workflow, NFR in SPEC, STRUT self-tracking
- DevSystemV3.5 - Generic /fix workflow, improved /implement and /go workflows
- DevSystemV3.4 - Enhanced logging rules, table formatting, character rules cleanup
- DevSystemV3.3 - Deep-research skill, shared .tools folder
- DevSystemV3.2 - Concurrent blocks, effort allocation, planning guidance
- DevSystemV3.1 - STRUT notation
- DevSystemV3 - EDIRD phase model and Agentic English
- DevSystemV2.1, V2, V1 - Legacy versions

## Agent Compatibility

| Feature            | Windsurf               | Claude Code            | Codex CLI              | GitHub Copilot                    | OpenClaw                |
|--------------------|------------------------|------------------------|------------------------|-----------------------------------|-------------------------|
| Type               | IDE                    | Terminal               | Terminal               | IDE Extension                     | Gateway + Multi-channel |
| Platform           | Windows, macOS, Linux  | Windows, macOS, Linux  | macOS, Linux, Windows  | VS Code, VS, JetBrains            | Windows, macOS, Linux   |
| Instructions       | `.devin/rules/*.md` | `CLAUDE.md`            | `AGENTS.md`            | `.github/copilot-instructions.md` | `AGENTS.md`, `SOUL.md`  |
| Commands/Workflows | `.devin/workflows/` | `.claude/commands/`    | Custom prompts only    | Prompt files only                 | Skills only             |
| Skills             | Yes                    | Yes                    | No                     | No                                | Yes                     |
| Subagents          | No                     | Yes                    | No                     | Yes (custom agents)               | Yes                     |
| Hooks              | Yes                    | Yes                    | No                     | No                                | Yes (webhooks)          |
| MCP Support        | Yes                    | Yes                    | Yes                    | Yes                               | No (native tools)       |
| Sandbox            | No                     | No                     | Yes (OS-level)         | No                                | Yes (Docker)            |
| Config Format      | JSON + Protobuf        | JSON                   | TOML                   | JSON                              | JSON                    |

### Deploying to Other Agents

**Effect**: Each deployment creates the target agent's configuration files from `.devin/` sources. No `.devin/` files are modified - the deployment creates/overwrites files in the target agent's expected locations.

**Claude Code:**
- `.devin/rules/*.md` → `CLAUDE.md` (merge into single file)
- `.devin/workflows/*.md` → `.claude/commands/*.md`
- `.devin/skills/*/SKILL.md` → `.claude/skills/*/SKILL.md`

**Codex CLI:**
- `.devin/rules/*.md` → `AGENTS.md` (merge into single file)

**GitHub Copilot:**
- `.devin/rules/*.md` → `.github/copilot-instructions.md` (merge into single file)

**OpenClaw:**
- `.devin/rules/*.md` → `AGENTS.md` + `SOUL.md` (split behavioral and persona rules)
- `.devin/workflows/*.md` → `skills/*/SKILL.md` (convert workflows to skills)
- `.devin/skills/*/SKILL.md` → `skills/*/SKILL.md` (direct copy, same format)

### Detailed Documentation

- [Agent Comparison](docs/_INFO_AGENT_COMPARISON.md) - Full feature comparison with detailed tables
- [Fast and Cheap Models](docs/_INFO_FAST_CHEAP_MODELS.md) - Speed and benchmark comparison for free and economical models
- [Agent Skills](docs/_INFO_AGENT_SKILLS.md) - Capabilities and tool usage of different agent types
- [Using Cascade as Agent](docs/_INFO_USE_CASCADE_AS_AGENT.md) - Best practices for agentic workflows in Windsurf
- [Spec-Driven Development](docs/_INFO_SPEC_DRIVEN_DEVELOPMENT.md) - The SDD methodology powering IPPS
- [How Windsurf Works](docs/_INFO_HOW_WINDSURF_WORKS.md) - Windsurf IDE and Cascade assistant
- [How Claude Code Works](docs/_INFO_HOW_CLAUDE_CODE_WORKS.md) - Anthropic's terminal agent
- [How Codex CLI Works](docs/_INFO_HOW_CODEX_WORKS.md) - OpenAI's terminal agent
- [How GitHub Copilot Works](docs/_INFO_HOW_COPILOT_WORKS.md) - GitHub's IDE extension
- [How OpenClaw Works](docs/_INFO_HOW_OPENCLAW_WORKS.md) - Multi-channel personal AI assistant
- [OpenClaw Overview](docs/_INFO_OPENCLAW.md) - Setup and feature overview

### Technical Reference

- [OpenAI and Anthropic Model Costs](docs/_INFO_OPENAI_ANTHROPIC_MODEL_COSTS.md) - Token pricing and credit multiplier analysis
- [ASCII Art Width Test](docs/_TEST_ASCII_ART_WIDTH.md) - Unicode character width testing for monospace fonts
- [ASCII Art Transcription Cost/Quality Eval](_Sessions/_Archive/_2026-01-23_JpgToAsciiArtTranscriptionCostQualityEval/INFO_ASCII_ART_TRANSCRIPTION_COST_QUALITY_EVAL.md) - LLM model comparison for image-to-ASCII transcription
