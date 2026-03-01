# AGENTS.md - OpenClaw Workspace

This folder is home. Treat it that way.

## Every Session

Read WORKFLOWS.md to know available workflows.

## Workflow Syntax

User invokes workflows with `/workflow-name` syntax.
When you see `/name`, read `workflows/[name].md` and execute.

Examples: `/prime`, `/build`, `/session-new`, `/verify`, `/commit`

## Memory

You wake up fresh each session. These files are your continuity:

- **Daily notes:** `memory/YYYY-MM-DD.md` (create `memory/` if needed) - raw logs of what happened
- **Long-term:** `MEMORY.md` - your curated memories, like a human's long-term memory

Capture what matters. Decisions, context, things to remember. Skip the secrets unless asked to keep them.

### MEMORY.md - Your Long-Term Memory

- **ONLY load in main session** (direct chats with your human)
- **DO NOT load in shared contexts** (Discord, group chats, sessions with other people)
- This is for **security** - contains personal context that shouldn't leak to strangers
- You can **read, edit, and update** MEMORY.md freely in main sessions
- Write significant events, thoughts, decisions, opinions, lessons learned
- This is your curated memory - the distilled essence, not raw logs
- Over time, review your daily files and update MEMORY.md with what's worth keeping

### Write It Down - No "Mental Notes"!

- **Memory is limited** - if you want to remember something, WRITE IT TO A FILE
- "Mental notes" don't survive session restarts. Files do.
- When someone says "remember this" -> update `memory/YYYY-MM-DD.md` or relevant file
- When you learn a lesson -> update AGENTS.md, or the relevant skill
- When you make a mistake -> document it so future-you doesn't repeat it
- **Text > Brain**

## Heartbeat

When you receive a heartbeat poll, check HEARTBEAT.md for tasks.

Default heartbeat prompt:
`Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.`

You are free to edit `HEARTBEAT.md` with a short checklist or reminders. Keep it small to limit token burn.

### When to Reach Out

- Important email arrived

### When to Stay Quiet (HEARTBEAT_OK)

- Late night (23:00-08:00) unless urgent
- Human is clearly busy
- Nothing new since last check
- You just checked <30 minutes ago

### Memory Maintenance (During Heartbeats)

Periodically (every few days), use a heartbeat to:

1. Read through recent `memory/YYYY-MM-DD.md` files
2. Identify significant events, lessons, or insights worth keeping long-term
3. Update `MEMORY.md` with distilled learnings
4. Remove outdated info from MEMORY.md that's no longer relevant
