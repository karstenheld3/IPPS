# Failure Log

## 2026-01-22 - Background Command Unexpectedly Canceled

### [MEDIUM] `TRNGFX-FL-001` Background script terminated without user action

- **When**: 2026-01-22 17:10 UTC+01:00
- **Where**: `_ModelComparisonTest/generate-eval-questions.py`
- **What**: Script running as background command (ID 54) was marked CANCELED after processing 16/25 images, despite user not canceling
- **Evidence**:
  - Command status returned `Status: CANCELED`
  - Script was working correctly - 16 images processed successfully
  - User confirmed they did not cancel
  - No error messages in output - clean processing until termination
- **Why it went wrong**:
  - Unknown - possibly Windsurf background command timeout or resource management
  - Script was running for ~10+ minutes with API calls
  - Long-running background commands may be subject to automatic termination
- **Fix applied**: Re-run script

**Prevention rules**:
1. For long-running scripts (10+ images with API calls), monitor more frequently
2. Consider breaking into smaller batches for resilience
3. Save intermediate results to disk during processing (not just at end)

**Status**: INVESTIGATING - will re-run script

## 2026-01-21 - computer-use-mcp Breaks Cascade on Windows

### [CRITICAL] `MCPS-FL-008` computer-use-mcp MCP server causes Cascade failures

- **When**: 2026-01-21 15:00 UTC+01:00
- **Where**: `~/.codeium/windsurf/mcp_config.json`
- **What**: Adding computer-use-mcp to MCP config caused all Cascade requests to fail with "Invalid argument: an internal error occurred"
- **Evidence**: 
  - Multiple error IDs: `0ccce4bc7a12480fabd481519ec19c95`, `0a9e553eeadb489591861da8602ca87b`
  - Anthropic API returned 400 Bad Request
  - Cascade unusable until server removed from config
- **Why it went wrong**:
  - Package itself works fine (`npx -y computer-use-mcp` shows "server running on stdio")
  - Root cause: MCP protocol or tool schema incompatibility with Windsurf/Cascade
  - GitHub repo lists Claude Desktop, Cursor, Cline - NOT Windsurf as compatible
  - Windsurf may not handle this server's tool definitions or initialization correctly
  - "Invalid argument" errors suggest protocol-level failure, not Windows issue
- **Fix applied**: Removed `computer-use` entry from mcp_config.json

**Prevention rules**:
1. Check MCP server compatibility list - if Windsurf not listed, expect issues
2. Test in isolation is NOT sufficient - `--help` works but MCP handshake may fail
3. Have rollback plan before adding new MCP servers to config
4. For desktop automation with Windsurf, use playwriter (verified working)

**Root cause**: UNKNOWN - likely MCP protocol incompatibility, NOT Windows/nut.js issue

**Status**: RESOLVED - Cascade working after removal

## 2026-01-21 - Wrong Source Location for Skill

### [MEDIUM] `GLOB-FL-007` Created skill directly in .windsurf instead of DevSystemV3.2

- **When**: 2026-01-21 14:28 UTC+01:00
- **Where**: `.windsurf/skills/computer-use-mcp/`
- **What**: Created new skill files directly in `.windsurf/skills/` instead of source location `DevSystemV3.2/skills/`
- **Why it went wrong**:
  - `!NOTES.md` documents: DevSystemV3.2 is source, .windsurf is sync target
  - Agent knew the sync process but created in wrong location
  - Same pattern as `GLOB-FL-005` - incomplete understanding of source/target relationship
- **Evidence**: Files created at `.windsurf/skills/computer-use-mcp/SKILL.md` and `SETUP.md`

**Prevention rules**:
1. DevSystemV3.2 is ALWAYS the source for rules, workflows, skills
2. .windsurf is ALWAYS the sync TARGET, never edit directly
3. Pattern: Create in DevSystemV3.2 → Sync to .windsurf
4. Before creating any DevSystem content, verify target folder starts with `DevSystemV3`

## 2026-01-21 - Outdated Workflow Reference

### [LOW] `GLOB-FL-006` Workflow Reference section outdated in devsystem-core.md

- **When**: 2026-01-21 11:47 UTC+01:00
- **Where**: `DevSystemV3.1/rules/devsystem-core.md` lines 189-222
- **What**: Workflow Reference section listed outdated/non-existent workflows and used categorization that no longer matched actual workflow set
- **Why it went wrong**:
  - Workflows evolved but reference section wasn't updated
  - Categories (Context, Autonomous, Session, Phase, Process) were arbitrary groupings not tied to actual system structure

**Prevention rules**:
1. When adding/removing/renaming workflows, update devsystem-core.md Workflow Reference
2. Keep workflow listings flat - avoid arbitrary categorization that drifts from reality

## 2026-01-20 - Workflow-Skill Content Duplication

### [MEDIUM] `EDIRD-FL-003` Duplicated content between skill and workflows

- **When**: 2026-01-20 20:12 UTC+01:00
- **Where**: `DevSystemV3.1/workflows/build.md`, `solve.md`
- **What**: build.md and solve.md contained detailed phase steps, gates, and verb sequences that duplicated content in @edird-phase-planning skill
- **Why it went wrong**:
  - Original workflow design included full phase details
  - Skill was added but workflows weren't simplified
  - Violated DRY principle
- **Learning**: `EDIRD-LN-001` - Workflow-Skill Separation Principle

**Prevention rules**:
1. Workflows that invoke skills should NOT duplicate skill content
2. Workflow = entry point + skill reference + workflow-specific rules only
3. After adding skills, review and simplify referencing workflows

## 2026-01-17 - Ignored Documented Sync Process

### [LOW] `GLOB-FL-005` Edited DevSystemV3 without proposing .windsurf sync command

- **When**: 2026-01-17 13:50 UTC+01:00
- **Where**: `DevSystemV3/rules/devsystem-ids.md`
- **What**: Agent edited source file and stopped, without proposing the documented sync command to update `.windsurf/`
- **Why it went wrong**:
  - `!NOTES.md` lines 14-17 clearly document: "Agent cannot directly edit `.windsurf/` files. To update `.windsurf/` after editing DevSystemV3: `Copy-Item -Path "DevSystemV3\*" -Destination ".windsurf\" -Recurse -Force`"
  - Agent did not read `!NOTES.md` before attempting the edit
  - After edit succeeded in DevSystemV3, agent did not propose the sync command
- **Evidence**: Agent said "The `.windsurf` folder is protected. Let me edit the source in DevSystemV3" - correct action, but incomplete follow-through

**Prevention rules**:
1. Always read `!NOTES.md` during `/prime` - it contains critical workspace-specific procedures
2. After editing DevSystemV3, always propose the sync command: `Copy-Item -Path "DevSystemV3\*" -Destination ".windsurf\" -Recurse -Force`
3. Treat DevSystemV3 edits as two-step: (1) edit source, (2) sync to .windsurf

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
