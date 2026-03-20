---
description: Forward-looking assessment, execute next items on plan
auto_execution_mode: 1
---

# Continue Workflow

Forward-looking execution of next steps in a plan.

## MUST-NOT-FORGET

- Execute queued workflows in sequence
- `/session-finalize`, `/session-archive` require user confirmation
- Remove workflows from sequence after completion

## Step 1: Build Execution Sequence

**Mandatory re-read:**

SESSION-MODE: NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md, LEARNINGS.md (if exists)

PROJECT-MODE: README.md, !NOTES.md or NOTES.md, !PROBLEMS.md or PROBLEMS.md (if exists), !PROGRESS.md or PROGRESS.md (if exists), FAILS.md, LEARNINGS.md (if exists)

Then build sequence:

1. **Conversation context** - Scan for workflow suggestions, successor workflows, explicit user instructions
2. **Session lifecycle** (SESSION-MODE) - Check lifecycle state (Init→Work→Save→Resume→Finalize→Archive), check NOTES.md "Workflows to Run on Resume". Lifecycle workflows require `[CONFIRM]` (see Step 2)
3. **Progress/tasks** - Read PROGRESS.md unchecked items, TASKS doc next unchecked task, else IMPL next step
4. **Merge** - Workflow succession before task execution

**If sequence empty:** Report "No pending work" and STOP.

## Step 2: Execute First Item

**If session lifecycle workflow** (`/session-finalize`, `/session-archive`):
- Output sequence with `[CONFIRM]` - do NOT auto-execute
- Wait for user to confirm with `/continue` or `/go`

**If other workflow** (starts with `/`):
- Execute, remove from sequence when complete

**If task**:
- Execute, update PROGRESS.md / TASKS (mark Done)

## Step 3: Loop or Stop

- **More items?** Return to Step 2
- **Phase gate reached?** Run gate check
- **Sequence empty?** Report completion
- **Blocker?** Report and wait for user

## Output

```markdown
## Execution Sequence

1. `/session-archive` - Session closed, ready to archive
2. Update README.md - From PROGRESS.md To Do
3. Run tests - From TASKS TK-005
```

After each execution:

`Executed: [item] | Result: OK/FAIL | Remaining: [N]`

## Stopping Conditions

- All tasks complete
- Blocker requires user input
- Gate check needed
- User interruption