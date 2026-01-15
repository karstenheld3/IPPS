# Failure Log

## 2026-01-16 - EDIRD Gate Check Bypass

### [CRITICAL] `GLOB-FL-004` Skipped DESIGN phase documents, passed gate without meeting criteria

- **When**: 2026-01-16 00:17-00:20 UTC+01:00
- **Where**: `/build` workflow for Space Invaders replica
- **What**: Agent marked DESIGN phase complete and proceeded to IMPLEMENT without creating required documents. Result: broken gameplay (aliens spawned at wrong position, game unplayable).
- **Why it went wrong**:
  - COMPLEXITY-MEDIUM requires `_SPEC_*.md` + `_IMPL_*.md` per `edird-core.md`
  - Zero design documents were created
  - Agent self-reported "DESIGN: Plan game architecture - completed" without evidence
  - Gate check DESIGN→IMPLEMENT was passed dishonestly
  - No `[PROVE]` step for high-risk coordinate system translation
  - 800+ lines implemented monolithically before any visual testing
- **Evidence**:
  - Session PROBLEMS.md documents `SINV-PR-001`
  - User screenshot comparison revealed aliens at 50% screen height vs 15% in original
  - Root cause: misinterpreted rotated-screen coordinates from disassembly

**Prevention rules**:
1. **Gate checks require evidence** - Cannot mark phase complete without deliverables
2. **COMPLEXITY-MEDIUM+ requires documents** - No exceptions, no "inline plan sufficient"
3. **UI/Game work requires visual [PROVE]** - Text research alone is insufficient for visual accuracy
4. **Coordinate systems are high-risk** - Always verify with visual test before full implementation
5. **Incremental [TEST] is mandatory** - Never implement 800+ lines before first visual check
6. **Replica work requires visual reference** - Research must include actual gameplay footage/screenshots, not just code analysis

**Process gap identified**: EDIRD describes *what* to do but agent self-discipline failed at honest gate checking. Consider: mandatory artifact list per phase that agent must produce before proceeding.

## 2026-01-15 - Wrong Folder Location for Isolated Implementation

### [WARNING] `GLOB-FL-003` Created isolated implementation folder in workspace root instead of session folder

- **When**: 2026-01-15 ~22:00 UTC+01:00
- **Where**: `_2026-01-15_SpaceInvadersClone/` (workspace root)
- **What**: `/solve` workflow (was `/new-task`) created a standalone HTML game file in workspace root instead of keeping it within the session folder or `_PrivateSessions/`
- **Why it went wrong**:
  - `/solve` did not distinguish between IMPL-CODEBASE and IMPL-ISOLATED modes
  - Agent treated BUILD output as a separate "project" folder
  - No guidance on where isolated implementations should be placed
- **Evidence**:
  - Folder created at `e:\Dev\IPPS\_2026-01-15_SpaceInvadersClone\`
  - Should have been in `_PrivateSessions/_2026-01-15_SolveSpaceInvadersProblem/` or similar

**Prevention rules**:
1. Workflows MUST specify operation mode: IMPL-CODEBASE or IMPL-ISOLATED
2. **IMPL-CODEBASE** (default): Implement in existing codebase - for SPEC, IMPL, TEST, [IMPLEMENT]
3. **IMPL-ISOLATED**: Implement separately - for [PROVE], POCs, prototypes, self-contained test scripts
   - Place in `[SESSION_FOLDER]/` or dedicated subfolder
   - Existing code, configuration, or runtime MUST NOT be affected
4. Never create top-level folders in workspace root for isolated implementations

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
