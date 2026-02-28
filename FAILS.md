# Failure Log

## 2026-02-28 - MNF Compliance Implementation

### [MEDIUM] `MNF-FL-001` Added incorrect MNF item to session-finalize.md

- **When**: 2026-02-28 13:15 UTC+01:00
- **Where**: `DevSystemV3.3/workflows/session-finalize.md:15`
- **What**: Added "Run `/session-archive` after finalization complete" to MNF section, but workflow explicitly states "Prepares for archiving but does NOT archive" (line 18) and only suggests user run archive (line 64).
- **Why it went wrong**:
  - IMPL plan IS-08 content was drafted without re-reading the actual workflow
  - Assumed the workflow calls `/session-archive` based on workflow name
  - Did not verify MNF content against actual workflow instructions
- **Evidence**: Line 18: "Prepares for archiving but does NOT archive"

**Prevention rules**:
1. Before adding MNF items, re-read the target workflow completely
2. MNF items must match ACTUAL workflow instructions, not assumptions
3. Verify each MNF item against the workflow text before adding

## 2026-02-28 - Deep Research Skill Improvement

### [MEDIUM] `GLOB-FL-018` Implemented instead of proposing when user said "propose"

- **When**: 2026-02-28 12:40 UTC+01:00
- **Where**: Conversation about improving deep-research skill
- **What**: User said "propose 2 modifications" but agent started executing `multi_edit` tool to implement changes immediately
- **Why it went wrong**:
  - Agent defaulted to action mode despite explicit "propose" verb
  - Did not distinguish between "propose" (output plan) vs "implement" (execute changes)
  - Existing rules say "implement rather than suggest" but don't handle explicit proposal requests
- **Evidence**: User correction: "hey I said propose, not implement"

**Prevention rules**:
1. When user uses verbs like "propose", "suggest", "draft", "outline" - OUTPUT TEXT, do not execute tools
2. Distinguish: "propose" = describe what you would do; "implement" = do it
3. Only use edit tools when user says "do", "make", "implement", "fix", "change", "update"

## 2026-02-07 - Model Pricing Update Workflow

### [MEDIUM] `LLMEV-FL-017` Workflow missing stitching step - individual page transcriptions instead of combined markdowns

- **When**: 2026-02-07 13:50 UTC+01:00
- **Where**: `DevSystemV3.2/skills/llm-evaluation/UPDATE_MODEL_PRICING.md` Step 2
- **What**: Original requirement specified single stitched markdown files per provider (`YYYY-MM-DD_Anthropic-ModelPricing.md`, `YYYY-MM-DD_OpenAI-ModelPricing-Standard.md`). When page splitting was added for screenshots, the workflow was updated to transcribe each page chunk individually via `--input-folder`, but no step was added to concatenate the individual page .md files into the required single combined markdown per provider. Result: 13+9 individual page .md files instead of 2 combined files.
- **Why it went wrong**:
  - Focus was on making `--input-folder` work with subfolders, overlooking that the transcription tool produces per-image outputs
  - Original requirement for single combined .md files was not carried forward when restructuring for page splitting
  - No MNF list was created referencing the original output format requirements
- **Evidence**: User asked "where have you put the stitched-together markdowns?" - combined files did not exist until manually concatenated after the fact

**Prevention rules**:
1. When adding intermediate steps (page splitting), trace through to final output format and verify it still matches requirements
2. If a tool produces per-file output but requirement is a combined file, add an explicit concatenation/stitching step
3. Create MNF list referencing original output format when modifying workflow steps

## 2026-02-06 - LLM Transcription Perf Optimization Session

### [HIGH] `LLMTR-FL-016` Edited sync target instead of DevSystem source

- **When**: 2026-02-06 06:30 UTC+01:00
- **Where**: `.windsurf/skills/llm-transcription/transcribe-image-to-markdown.py`
- **What**: Applied v2 persistent client optimizations directly to the `.windsurf` sync target instead of the DevSystem source at `DevSystemV3.2/skills/llm-transcription/transcribe-image-to-markdown.py`. Then committed and pushed, leaving source and target out of sync.
- **Why it went wrong**:
  - Agent had the rule loaded from `!NOTES.md`: "DevSystem is the source, `.windsurf` is the sync target"
  - Despite knowing the rule, agent edited the sync target directly because the previous session checkpoint referenced the `.windsurf` path as the production script
  - Did not verify source vs target before editing
- **Evidence**: Commit `8c6dc9a` modifies `.windsurf/skills/llm-transcription/transcribe-image-to-markdown.py` while `DevSystemV3.2/skills/llm-transcription/transcribe-image-to-markdown.py` remains unchanged. `fc.exe` comparison confirms files differ.
- **Suggested fix**: Apply same changes to DevSystem source, then sync to `.windsurf` to restore correct flow

**Prevention rules**:
1. ALWAYS check `!NOTES.md` source/sync rules before editing any file under `.windsurf/skills/`
2. For skill files: edit `DevSystemV3.2/` first, then sync to `.windsurf/`
3. Never trust checkpoint paths as authoritative - verify source location before editing

## 2026-01-26 - LLM Evaluation Skill Session

### [MEDIUM] `LLMEV-FL-014` Deleted content before creating reference files

- **When**: 2026-01-26 21:00 UTC+01:00
- **Where**: `DevSystemV3.2/skills/llm-evaluation/SKILL.md`
- **What**: User asked for "progressive disclosure" in SKILL.md. Agent deleted 600 lines of detail BEFORE creating the reference files (SCRIPTS.md, CLAUDE_MODELS.md, TESTED_MODELS.md) that would hold those details.
- **Why it went wrong**:
  - Misunderstood "progressive disclosure" as "remove details" instead of "reorganize details"
  - Committed the deletion before creating replacement files
  - User had to correct: "all details are gone. Progressive disclosure means we make details available as the llm uses the skill. not delete all details"
- **Evidence**: Commit `cf48ea9` deleted 600 lines; reference files created in separate commit `9175d66` only after user correction

**Prevention rules**:
1. Progressive disclosure = reorganize, NOT delete
2. When moving content to reference files: CREATE reference files FIRST, THEN update main file to reference them
3. Never commit content deletion without the replacement ready
4. If restructuring, do it in ONE commit with both changes

## 2026-01-26 - Auto Model Switcher Session

### [MEDIUM] `AMSW-FL-015` Session TOPIC not registered in ID-REGISTRY.md

- **When**: 2026-01-26 09:28 UTC+01:00 (session creation)
- **Where**: `ID-REGISTRY.md` Project Topics section
- **What**: Session created with TOPIC `AMSW` but never added it to ID-REGISTRY.md.
- **Why it went wrong**:
  - `/session-new` workflow does not explicitly require TOPIC registration
  - Agent knew the ID system rules but did not follow them during session init
  - No checklist item for "Add TOPIC to ID-REGISTRY.md"
- **Evidence**: `AMSW-NOTES`, `AMSW-FL-*`, `AMSW-PR-*` all used throughout session without registry entry
- **Prevention rules**:
  1. `/session-new` workflow MUST include step: "Add session TOPIC to ID-REGISTRY.md"
  2. Before using any new TOPIC, verify it exists in ID-REGISTRY.md
  3. Session NOTES.md header should include: "TOPIC: [X] (registered in ID-REGISTRY.md)"

### [HIGH] `AMSW-FL-014` Confused Claude Sonnet 4 with Claude Sonnet 4.5

- **When**: 2026-01-26 16:14 UTC+01:00
- **Where**: `select-windsurf-model-in-ide.ps1:22-27, 57-58`
- **What**: Used "Claude Sonnet 4.5" as default despite user explicitly wanting "Claude Sonnet 4".
- **Why it went wrong**: Assumed "sonnet 4" meant "latest sonnet" (4.5) instead of the specific older version.
- **Evidence**: User correction: "are you stupid? Sonnet 4 is NOT sonnet 4.5"
- **Prevention rules**:
  1. Read user model requests literally - version numbers matter.
  2. Verify available models in registry before defaulting.

### [HIGH] `AMSW-FL-013` No dry-run mode to preview model selection

- **When**: 2026-01-26 16:11 UTC+01:00
- **Where**: `select-windsurf-model-in-ide.ps1`
- **What**: Script executed keyboard events immediately without previewing selection.
- **Why it went wrong**: Designed for speed rather than safety/verification.
- **Evidence**: User request: "could you add a dry_run mode and evaluate first before executing this?"
- **Prevention rules**:
  1. UI automation scripts should have a `-DryRun` mode for safe verification.
  2. Always show what will happen before sending irreversible keyboard events.

## 2026-01-24 - MEPI/MCPI Document ID

### [LOW] `GLOB-FL-008` Used wrong TOPIC for MEPI/MCPI INFO document

- **When**: 2026-01-24 18:58 UTC+01:00
- **Where**: `Docs/Concepts/_INFO_MEPI_MCPI_PRINCIPLE.md` line 3
- **What**: Used `GLOB-IN01` as Doc ID, but MEPI/MCPI is a distinct concept that should have its own TOPIC
- **Why it went wrong**:
  - Assumed `GLOB` was appropriate for "global concepts"
  - Did not check ID-REGISTRY.md for existing MEPI/MCPI TOPIC
  - `GLOB` is for project-wide architecture, not for named concepts like MEPI/MCPI
- **Evidence**: Doc ID `GLOB-IN01` on line 3, but MEPI/MCPI are listed as concepts in ID-REGISTRY.md

**Prevention rules**:
1. Named concepts (MEPI, MCPI, EDIRD, STRUT) should have their own TOPIC
2. Check ID-REGISTRY.md before assigning TOPIC
3. `GLOB` is for project-wide items without a specific concept name

**Fix**: Change Doc ID to `MEPI-IN01` and register `MEPI` as TOPIC in ID-REGISTRY.md

## 2026-01-22 - LLM Evaluation Skill Session

### [MEDIUM] `LLMEV-FL-013` Repeatedly misunderstanding user's parameter design intent

- **When**: 2026-01-24 19:41 UTC+01:00
- **Where**: model-parameter-mapping.json design iterations
- **What**: Agent kept trying to create a unified `--effort` parameter when user wanted THREE separate CLI params (`--temperature`, `--reasoning-effort`, `--output-length`) that all use the same keywords

**Prevention rules**:
1. When user says "no" or corrects, STOP and ask for clarification
2. Restate understanding before implementing: "So you want X, Y, Z - is that correct?"
3. Don't assume simplification is always the goal

### [MEDIUM] `LLMEV-FL-012` Repeatedly confusing API parameter ranges between providers

- **When**: 2026-01-24 19:27 UTC+01:00
- **Where**: SPEC document, model-parameter-mapping.json
- **What**: Agent repeatedly wrote incorrect temperature ranges - swapping OpenAI (0-2) and Anthropic (0-1) values

**Prevention rules**:
1. When user reports a bug, assume they are correct and find it
2. Create reference table and verify against it each time
3. **OpenAI legacy: 0-2, Anthropic: 0-1** (memorize this)

### [MEDIUM] `LLMEV-FL-010` Failed to recognize workspace workflow and executed without confirmation

- **When**: 2026-01-23 11:05 UTC+01:00
- **Where**: Agent response to "deploy-to-all" user message
- **What**: User said "deploy-to-all" which maps to `deploy-to-all-repos.md` workflow in workspace root. Agent ignored the workflow and executed sync commands immediately.

**Prevention rules**:
1. When receiving command-like messages, check workspace root for matching `.md` workflow files
2. Read and follow workflow's execution mode (preview vs auto-execute)
3. Never execute batch file operations without explicit confirmation

### [MEDIUM] `LLMEV-FL-009` Ignored documented settings in NOTES.md

- **When**: 2026-01-22 23:03 UTC+01:00
- **Where**: Agent command execution for test runs
- **What**: Agent repeatedly used `--workers 2` instead of `--workers 4` despite NOTES.md clearly specifying "Workers: 4 parallel" in Test Configuration section
- **Why it went wrong**: Agent used hardcoded value from memory instead of reading current NOTES.md settings before executing commands

**Prevention rules**:
1. Before running test commands, always read NOTES.md Test Configuration section
2. Use exact values from session documentation, not memory
3. When in doubt, re-read the config section

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
