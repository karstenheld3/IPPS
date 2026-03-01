# WORKFLOWS.md - Available Workflows

Invoke with `/workflow-name`. Definitions in `workflows/` folder.

## Core Workflows

- `/prime` - Load workspace context (reads rules/)
- `/build` - BUILD workflow for code output
- `/solve` - SOLVE workflow for knowledge output
- `/go` - Autonomous loop (recap + continue until done)
- `/recap` - Analyze context, identify current status
- `/continue` - Execute next items on plan

## Session Workflows

- `/session-new` - Initialize new session
- `/session-load` - Resume existing session
- `/session-save` - Save session progress
- `/session-finalize` - Finalize session, sync findings
- `/session-archive` - Archive session folder

## Document Workflows

- `/write-spec` - Create specification from requirements
- `/write-impl-plan` - Create implementation plan from spec
- `/write-test-plan` - Create test plan from spec
- `/write-tasks-plan` - Create tasks plan from IMPL/TEST
- `/write-strut` - Create STRUT plans with proper format
- `/write-info` - Create INFO document from research

## Verification Workflows

- `/verify` - Verify against specs and rules
- `/critique` - Devil's Advocate review
- `/reconcile` - Pragmatic review of critique findings
- `/implement` - Execute implementation from plan
- `/test` - Run tests based on scope

## Other Workflows

- `/commit` - Create conventional commits
- `/rename` - Global/local refactoring with verification
- `/sync` - Document synchronization
- `/fail` - Record failures to FAILS.md
- `/learn` - Extract learnings from resolved problems
- `/partition` - Split plans into discrete tasks
- `/transcribe` - PDF/web to markdown transcription
- `/switch-model` - Switch Cascade AI model tier
- `/deep-research` - Execute deep research with domain-specific patterns
