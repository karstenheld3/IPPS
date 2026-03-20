---
description: Finalize a development session, sync findings, and prepare for archive
auto_execution_mode: 1
---

# Finalize Session Workflow

Skills: @session-management, @git-conventions

## MUST-NOT-FORGET

- Sync session PROBLEMS.md to project
- Suggest `/session-archive` when ready (do NOT auto-run)

## Steps

1. **Sync problems to project !PROBLEMS.md**
   - RESOLVED: Mark in `!PROBLEMS.md` as FIXED with date
   - OPEN/DEFERRED: Add to `!PROBLEMS.md`

2. **Sync FAILS to project FAILS.md (MEDIUM and HIGH only)**
   - Add [MEDIUM]/[HIGH] entries to workspace FAILS.md if not present
   - Skip [LOW] (session-specific)

3. **Sync LEARNINGS to project (MEDIUM and HIGH only)**
   - Add prevention rules to `!NOTES.md` for [MEDIUM]/[HIGH]-linked learnings
   - Or create workspace-level LEARNINGS.md if reusable

4. **Update session PROGRESS.md**
   - Keep To Do list intact - do NOT delete
   - Mark completed items: `- [x]`
   - Ensure completed tasks in "Done" section

5. **Sync findings to project !NOTES.md**
   - Add reusable patterns from session NOTES.md: problem, solution, key facts

6. **Check for deployable artifacts**
   - List: `_SPEC_*.md`, `_IMPL_*.md`, `_INFO_*.md`, code files, skills/workflows/rules
   - For each, ask [ACTOR]: "Deploy to workspace/project?" or "Keep in session archive only?"
   - Execute deployment decisions before archiving

7. **Ready for archive**
   - Verify all syncs and deployment decisions complete
   - Report: "Session ready for archive. Run `/session-archive` when ready."