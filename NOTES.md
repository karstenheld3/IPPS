# NOTES

## MUST-NOT-FORGET

- [PROMPTSYSTEM_FOLDER] is the source of truth. Never edit [AGENT_FOLDER] directly
- Sync order: 1) [PROMPTSYSTEM_FOLDER] → [AGENT_FOLDER] (robocopy /MIR), 2) [AGENT_FOLDER] → [LINKED_REPOS] (sync.ps1 -execute). Stage 2 requires stage 1 complete. Stage 3 (linked repo local mirror) is NOT automatic from source repo
- Downstream repos pull from [AGENT_FOLDER], NOT from [PROMPTSYSTEM_FOLDER]. The local mirror is the published source for linked repos
- Use placeholders in all workspace/session files, never ephemeral version strings or repo names

## Table of Contents

- [MUST-NOT-FORGET](#must-not-forget)
- [Project Info](#project-info)
- [Workspace Constants](#workspace-constants)
- [Prevention Rules](#prevention-rules-from-session-fails)
- [PromptSystem Source/Sync Rules](#promptsystem-sourcesync-rules)
- [Workflow Design Rules](#workflow-design-rules)
- [Platform Notes](#platform-notes)
- [Special Workflows](#special-workflows-workspace-root)
- [Sync Architecture](#sync-architecture-2026-09-06-revised-2026-09-12)
- [PromptSystem 5.0 Planning](#promptsystem-50-planning)
- [PERSONAL_WORKFLOWS](#personal_workflows-excluded-from-development-only-repos-deployed-only-to-all-repos)
- [Agentic Problems Notepad](#agentic-problems-notepad)
- [LINKED_REPOS](#linked_repos)
- [Release Configuration](#release-configuration)
- [find-workers-limit.py Changes (2026-09-16)](#find-workers-limitpy-changes-2026-09-16)

## Project Info

- Project name: IPPS
- Project goal: PromptSystem source repository — rules, workflows, skills for agentic development
- Workspace type: SOFTWARE-DEV
- Workspace mode: SINGLE-PROJECT
- Version strategy: SINGLE-VERSION


## Workspace Constants

[WORKSPACE_FOLDER]: `E:\Dev\IPPS`
- Root folder of the workspace. All other paths compose from this.

[PRODUCT_REPO_FOLDER]: `[WORKSPACE_FOLDER]`
- In SINGLE-PROJECT mode, equals [WORKSPACE_FOLDER]. In WORKSPACE mode, points to product repo (may be outside [WORKSPACE_FOLDER]).

[PRODUCT_SOURCE_FOLDER]: `[PRODUCT_REPO_FOLDER]\src`
- Source code folder. Applies to ProductRepo only.

[PRODUCT_DOCS_FOLDER]: `[WORKSPACE_FOLDER]\docs`
- Product documentation folder.

[DEV_KNOWLEDGE_FOLDER]: `E:\Dev\Delphios\knowledge`
- Knowledge bundles folder. External — shared across workspaces via Delphios repo.

[DEV_SPECS_FOLDER]: `[WORKSPACE_FOLDER]\specs`
- Specs folder containing shared specifications, design guidelines, SOPs.

[PRODUCT_VERSION]: `4.4`
- Current PromptSystem version. Update on version changes (SOPS SOP 4/7).

[PROMPTSYSTEM_FOLDER]: `[WORKSPACE_FOLDER]\PromptSystemV4.4`
- Source of truth for all rules, workflows, skills. Never edit `.devin/` directly. Repo-specific — not in template.

[AGENT_FOLDER]: `[WORKSPACE_FOLDER]\.devin`
- Sync target. Copy of [PROMPTSYSTEM_FOLDER] content.

[SESSIONS_FOLDER]: `[WORKSPACE_FOLDER]\_PrivateSessions_gitignore`
- Base folder for session folders.

[SESSION_ARCHIVE_FOLDER]: `[SESSIONS_FOLDER]\..\Archive`
- Archive folder for closed sessions.

[SKILL_TOOLS_FOLDER]: `[WORKSPACE_FOLDER]\..\.tools\`
- Command line tools used by various PromptSystem skills. Shared across workspaces. Not the agent built-in tools.

[API_KEYS_FILE]: `[SKILL_TOOLS_FOLDER]\.api-keys.txt`
- API keys file for skill scripts. Pass via `--keys-file [API_KEYS_FILE]`.

[SOPS_FILE]: `SOPS.md`
- SOPS filename in workspace root.

[RELEASE_NOTES_FOLDER]: `[PRODUCT_DOCS_FOLDER]\ReleaseNotes`
- Release notes directory. Naming: `RELEASE_NOTES_v{VERSION}_{DATE}.md`.


## Prevention Rules (from session fails)

- **Model Accuracy**: Read model requests literally. Version numbers matter (e.g., Sonnet 4 != Sonnet 4.5).
- **Safety First**: UI automation scripts MUST have a `-DryRun` mode. Preview changes before sending irreversible keyboard events.
- **Playwriter Timeouts**: ALWAYS pass `timeout: 1500` (default is 20000ms!). Lower to 500ms when fast.
- **No Ask Tool**: NEVER use the `ask_user_question` tool. Resolve ambiguity through prompt analysis, not interactive prompts. See `agent-behavior.md` Attitude section.

## PromptSystem Source/Sync Rules

**CRITICAL: [PROMPTSYSTEM_FOLDER] is the SOURCE. .devin is the SYNC TARGET.**
**CRITICAL: Never leak project-specific or private data into workflows, skills, or rules.** These are reusable across projects. Use generic examples and placeholders only.

**Sync order (3 stages, each depends on the previous):**
```
1. [PROMPTSYSTEM_FOLDER] → local [AGENT_FOLDER]
   Method: robocopy /MIR (see command below)
   When: after every edit to source

2. [AGENT_FOLDER] → [LINKED_REPOS] .devin/
   Method: sync.ps1 -execute at each target (reads promptsystem-sync.json)
   When: explicit user confirmation only
   Source for targets: ../IPPS/[AGENT_FOLDER] (the local mirror, not [PROMPTSYSTEM_FOLDER])

3. [LINKED_REPOS] .devin/ → agent folder in each linked repo
   Method: robocopy /MIR at each linked repo (same as stage 1, local to that repo)
   When: each linked repo's own procedure (NOT automatic from IPPS)
```

- **Creating new rules, workflows, skills** -> Create in [PROMPTSYSTEM_FOLDER] first, then sync
- **Editing existing content** -> Edit in [PROMPTSYSTEM_FOLDER] first, then sync
- **NEVER create or edit directly in `.devin/`** (except for temp testing)

**Local mirror sync (robocopy /MIR):**
```powershell
robocopy "[PROMPTSYSTEM_FOLDER]" "[AGENT_FOLDER]" /MIR /XD .git
```
`/MIR` = mirror mode (copies new/changed, deletes files at target not in source). `/XD .git` = exclude .git folder. This is the only command for local `[PROMPTSYSTEM_FOLDER]` → `.devin/` sync. Not `sync.ps1` — that is for cross-repo downstream sync only.

**Claude Code deployment:** `.claude/` (rules and skills) is regenerated by running the prompts in `_PROMPTS_UpdateClaude.md` at the workspace root (idempotent full rebuild; `.devin/` continues via robocopy /MIR).

**Exception:** If user edits .devin directly, sync BACK to [PROMPTSYSTEM_FOLDER] first.

**README.md Link Convention (2026-03-19):**
- **ALWAYS use `.devin/` paths in README.md** - Never reference `DevSystemV3.6/` or any version folder
- Example: `.devin/skills/write-documents/APAPALAN_RULES.md` (GOOD)
- Example: `DevSystemV3.6/skills/write-documents/APAPALAN_RULES.md` (BAD)
- Reason: README is user-facing, users interact with `.devin/`, not version folders

## Workflow Design Rules

**CRITICAL: Workflows MUST be phase-model independent.**
- Workflows contain task knowledge (what to do, how to do it, what tools/context needed)
- Workflows MUST NOT reference phase names (EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER)
- Workflows MUST NOT have `phase:` field in frontmatter
- Phase orchestration belongs in the phase model (EDIRD), not in workflows
- This allows swapping EDIRD for alternative phase models without rewriting workflows

**Workflow-Skill Separation (from session 2026-01-17):**
- Workflows are thin: entry point + skill refs + workflow-specific rules only
- Skills hold knowledge: phase logic, gates, detailed procedures
- Plain English in workflows: AGEN verbs for rules/skills only
- DRY check: after adding skills, review referencing workflows for duplication

## Platform Notes

**Release archive**: `[WORKSPACE_FOLDER]\_OldPromptSystemVersions\` — all prior PromptSystem version folders are preserved here before deletion. Never delete a version folder without backing it up.

**Windows:** No symlinks. `.devin/` is a copy of `[PROMPTSYSTEM_FOLDER]`. Local mirror sync: see robocopy command above. SOPS.md procedures reference this command.

**"deploy" keyword:** When user says "deploy", run the robocopy /MIR command above to sync `[PROMPTSYSTEM_FOLDER]` to `.devin/`.

Automatically push commits to GitHub.

**2026-01-21**: Workflow Reference in devsystem-core.md was outdated (`GLOB-FL-006`). Updated to flat list of all 28 workflows.

## Special Workflows (Workspace Root)

**`deploy-to-all-repos.md`** — Deleted. Replaced by `/sync workspace` (FR-49) using `sync.ps1`.

**CRITICAL: NEVER auto-sync to downstream repos without explicit user confirmation.** Sync to downstream repos is a separate, explicit action.

## Sync Architecture (2026-09-06, revised 2026-09-12)

**Folder rename**: `[WORKSPACE_FOLDER]\rules` → `[WORKSPACE_FOLDER]\specs` (completed 2026-09-06)
- `\specs` contains all SPEC, IMPL, TEST, INFO concept files
- `\docs` contains product documentation, tool research, release notes

**Local mirror**: `robocopy /MIR` (see PromptSystem Source/Sync Rules above). Not `sync.ps1`.

**Cross-repo sync**: `sync.ps1` in workspace-management skill
- `-diff -config <path-to-promptsystem-sync.json>` → produces additions, changes, deletions
- `-execute -config <path-to-promptsystem-sync.json>` → executes sync
- `-preview_file <path>` → markdown preview for chat presentation
- `-output_file <path>` → full text report to file

**promptsystem-sync.json at target `[WORKSPACE_FOLDER]` root** (PULL model):
- Single source of truth for ALL cross-repo sync configuration
- `targets` array: each entry is self-contained (path, source, include, exclude, never_overwrite)
- `deprecated`: top-level array (shared across all targets in repo)
- `bundles` and `selected_bundles` removed — include/exclude per target is the single filter layer
- Source is purely a content provider — no config at source
- Source repo maintains `[LINKED_REPOS]` list in NOTES.md (for push operations)

**Source repo**: Only references RELATIVE downstream repo paths (e.g., `../Lana-V2-Dev`), never absolute

## PromptSystem 5.0 Planning

**Investigate workflow** (created 2026-09-09 in DevSystemV4.3, ready for 5.0 inclusion):
- `specs/_SPEC_INVESTIGATE_WORKFLOW.md [INVESTIGATE-SP01]` - Specification
- `DevSystemV4.3/workflows/investigate.md` - Workflow file
- `DevSystemV4.3/skills/write-documents/INVESTIGATION_LOG_TEMPLATE.md` - Log template
- `DevSystemV4.3/skills/write-documents/INVESTIGATION_GUIDES.md` - Entry type guidance
- `DevSystemV4.3/skills/write-documents/INVESTIGATION_LOG_RULES.md` - Verification rules (IL-* rule IDs)
- `DevSystemV4.3/workflows/verify.md` - Updated with Investigation Logs section

Workflow behavior: formulates goal, collects premises, analyzes problem nature, lists known knowns and unknowns, writes STRUT with phased approaches (Phase 1 first), creates append-only investigation log, executes phases with mandatory log checkpoints, updates log with handover state and STRUT with progress after each phase.

## [PERSONAL_WORKFLOWS] (excluded from Development-only repos, deployed only to "All" repos)

- conversation-start.md
- conversation-update.md

## Agentic Problems Notepad

`docs/_INFO_AGENTIC_PROBLEMS.md` is the central notepad for collecting all agentic failure patterns, PromptSystem problems, and shortcomings. Add new categories, failure modes, and instances as they are observed. Do NOT record fix suggestions in this file - only record and categorize the problem.

## [LINKED_REPOS]

Downstream repos that pull from this source. Each repo has its own `promptsystem-sync.json` defining what it pulls.

**[LINKED_REPOS]**:
- ../KarstensWorkspace
- ../OpenAI-BackendTools
- ../PRXL/src
- ../SharePoint-GPT-Middleware
- ../USTVA
- ../LLM-Research
- ../Lana-V1
- ../Lana-V1-Dev
- ../Hera-V1-Dev (agent folder: `.devin`)
- ../Hera-V1 (agent folder: `.agent`)

## Release Configuration

Config for `/project-release` workflow. All paths use workspace constants from `## Workspace Constants` section above. See `_SPEC_RELEASE_PROJECT_WORKFLOW.md [RLSPROJ-SP01]` in `[DEV_SPECS_FOLDER]` for full schema and decision guide.

```
[RELEASE_CONFIG]
sops_file: [SOPS_FILE]
sessions_folder: [SESSIONS_FOLDER]
release_notes_dir: [RELEASE_NOTES_FOLDER]
release_notes_naming: RELEASE_NOTES_v{VERSION}_{DATE}.md
tag_annotation_template: Release {TAG}: {SUMMARY}

[RELEASE_REPO: product]
path: [WORKSPACE_FOLDER]
role: product
tag_format: semver
version_source: promptsystem_folder
post_release_bump: promptsystem_rename
github_release: true
```

Instructions: SINGLE-PROJECT mode — one repo, one `[RELEASE_REPO]` block. Semver tags (`vX.Y`). Version source is `promptsystem_folder` (parsed from `[PRODUCT_VERSION]` line above). Post-release bump renames `PromptSystemVX.Y` folder to next minor version per SOPS SOP 7. No binary build, no version gate. Release notes go in `docs/ReleaseNotes/` per existing convention (see `[RELEASE_NOTES_FOLDER]` constant above).

## find-workers-limit.py Changes (2026-09-16)

**Location**: `[PROMPTSYSTEM_FOLDER]/skills/llm-evaluation/find-workers-limit.py`
**Source session**: KarstensWorkspace `_2026-09-16_TranscriptionSkillRewrite`

### Changes

- **Z.AI provider support**: `detect_provider()` recognizes `glm-` prefix, `create_zai_client()` uses OpenAI SDK with `base_url='https://api.z.ai/api/paas/v4/'` and `ZAI_API_KEY`
- **`--start-workers N`** (default 3): Skip known-safe worker levels to save time and tokens
- **Prompt caching**: System message pattern for cache-friendly prefix; Anthropic explicit `cache_control` on system block; OpenAI/Z.AI automatic caching tracked via `prompt_tokens_details.cached_tokens`
- **`cached_tokens`** tracked in usage aggregation and per-run JSON output; cache hit rate shown in verbose output

### Bug fixes (pre-existing)

- OpenAI/Z.AI branch had no `return (True, False, usage)` after successful call - fell through to retry loop
- `timeout` passed inside request body dict instead of as SDK kwarg - could cause Z.AI 400 errors
- `args.model` printed instead of `args.output_file` in save confirmation message
- Anthropic branch did not pass `timeout` to `messages.create()`
- Usage only aggregated for `success=True` calls - now aggregated for all non-rate-limited completions

### SDK compatibility

- **Anthropic SDK 0.76.0**: Top-level `cache_control` kwarg on `messages.create()` is NOT supported (docs reference SDK 1.3.0). Uses explicit `cache_control` on system content block instead.
- **Anthropic caching minimum**: 2048 tokens for Haiku, 1024 for Opus/Sonnet. Default prompt (~95 tokens) is below minimum. Caching only benefits large `--prompt-file` inputs.
- **Z.AI caching**: Implicit automatic, 50% discount on cached tokens. Observed 22% cache hit on first burst test with `glm-5.3-flash`.

### Live test results (2026-09-16, 3 workers, 10 output tokens)

- **OpenAI** (`gpt-4o-mini`): 33/33 tests passed, 570 input tokens, 0% cache
- **Anthropic** (`claude-haiku-4-5-20251001`): 33/33 tests passed, 588 input tokens, 0% cache
- **Z.AI** (`glm-5.3-flash`): 33/33 tests passed, 576 input tokens, 22% cache

### Burst capacity results (2026-09-16, scaling 3 → 100 workers, 10 output tokens)

- **OpenAI** (`gpt-4o-mini`): 100 workers, 0 rate limits across 9 test rounds (712 calls)
- **Anthropic** (`claude-haiku-4-5-20251001`): 100 workers, 0 rate limits across 9 test rounds (712 calls)
- **Z.AI** (`glm-5.3-flash`): **72 workers stable**. Rate-limited at 90 (20/180 calls got 429). Z.AI automatic caching reached 67% hit rate at 60+ workers.
- **Recommendation**: OpenAI/Anthropic safe at 120 workers. Z.AI cap at 60 (conservative) or 72 (tested limit).