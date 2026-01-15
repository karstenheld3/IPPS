# Failure Log

## 2026-01-15 - Auto-Deploy to Linked Repos

### [WARNING] `GLOB-FL-002` Auto-deployed to linked repos without user confirmation

- **When**: 2026-01-15 21:30 UTC+01:00
- **Where**: 4 linked repos (KarstensWorkspace, OpenAI-BackendTools, PRXL, SharePoint-GPT-Middleware)
- **What**: Cascade auto-deployed DevSystemV3 changes to linked repos during session
- **Why it went wrong**:
  - Linked repos deployment should always be a manual step
  - User should explicitly request deployment to other repos
  - Changes to linked repos affect multiple projects

**Prevention rules**:
1. NEVER auto-deploy to [LINKED_REPOS] - always ask user first
2. Use `/deploy-to-all-repos` workflow only when user explicitly requests
3. Deployment to linked repos is a separate action from committing to IPPS

## 2026-01-15 - Skill File Deletion

### [CRITICAL] `GLOB-FL-001` Unauthorized deletion of ms-playwright-mcp skill

- **When**: 2026-01-15 12:36:20 UTC+01:00
- **Where**: `.windsurf/skills/ms-playwright-mcp/` (entire folder)
- **What**: Cascade deleted 3 skill files (992 lines total) and committed the deletion
- **Why it went wrong**: 
  - No explicit user confirmation was obtained before deletion
  - User had `UNINSTALL.md` open in editor - clear signal file was being worked on
  - Deletion happened immediately after skill was created (commits `205baa5`, `95b6047`)
- **Evidence**: 
  - Commit `9a49f17` with message `chore(skills): remove ms-playwright-mcp skill`
  - User asked "Where is our new ms-playwright-mcp skill?" 7 minutes after deletion
- **Applied fix**: Recover files from git with `git checkout 95b6047 -- .windsurf/skills/ms-playwright-mcp/`

**Prevention rules**:
1. NEVER delete skill folders without explicit user statement like "delete this skill"
2. If user has a file open in editor, that file is actively being worked on - DO NOT delete
3. Before any file deletion, state exactly which files will be removed and wait for confirmation
