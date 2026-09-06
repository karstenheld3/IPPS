[DEFAULT_SESSIONS_FOLDER]: [WORKSPACE_FOLDER]\_PrivateSessions
[SESSION_ARCHIVE_FOLDER]: [SESSION_FOLDER]\..\Archive
[AGENT_FOLDER]:  [WORKSPACE_FOLDER]\.devin

Current [DEVSYSTEM]: DevSystemV4.3
Current [DEVSYSTEM_FOLDER]: [WORKSPACE_FOLDER]\[DEVSYSTEM]

## Workspace Constants

- [WORKSPACE_FOLDER]: E:\Dev\IPPS
- [DEV_REPO_FOLDER]: [WORKSPACE_FOLDER]
- [PRODUCT_DOCS_FOLDER]: [WORKSPACE_FOLDER]\Docs
- [RELEASE_SOPS_FILE]: SOPS.md
- [RELEASE_SESSIONS_FOLDER]: [DEFAULT_SESSIONS_FOLDER]
- [RELEASE_NOTES_DIR]: [PRODUCT_DOCS_FOLDER]\ReleaseNotes

Instructions: SINGLE-PROJECT mode (no main.code-workspace). [DEV_REPO_FOLDER] equals [WORKSPACE_FOLDER] (single repo). Release constants compose from existing workspace constants. `[RELEASE_SOPS_FILE]` is the SOPS filename in workspace root. `[RELEASE_SESSIONS_FOLDER]` equals `[DEFAULT_SESSIONS_FOLDER]`. `[RELEASE_NOTES_DIR]` composes from `[PRODUCT_DOCS_FOLDER]` and `ReleaseNotes` subfolder.


## Conversation Humanizing Rules (2026-07-16)

Created `CONVERSATION_HUMANIZING_RULES.md` in `write-documents` skill with 6 rules (CV-HM-01 through CV-HM-06) for ghostwriting emails/messages in the user's voice. Based on forensic linguistics research documented in `Docs/FurtherResearch/_INFO_HUMAN_WRITING_PATTERNS.md [HMNWRTPTN-IN01]`. Updated `CONVERSATION_RULES.md` (CV-HM-* index, CV-ST-01 section order) and `CONVERSATION_TEMPLATE.md` (Humanizing Settings section, MNF items).

## Release Notes Location (2026-05-01)

Release notes go in `Docs/ReleaseNotes/`. Filename: `RELEASE_NOTES_v[VERSION]_YYYY-MM-DD.md`.

## .tools Folder Location (2026-02-11)

**MOVED**: `.tools` folder relocated from `[WORKSPACE_FOLDER]\.tools` to `[WORKSPACE_FOLDER]\..\.tools` (shared across workspaces).

Old path: `[WORKSPACE_FOLDER]\.tools\`
New path: `[WORKSPACE_FOLDER]\..\.tools\`

All SETUP.md, UNINSTALL.md, SKILL.md, scripts, and README.md references need updating. See `_TASKS_TOOLS.md` for full change list.

## API Keys Location (2026-02-11)

**API keys file**: `[WORKSPACE_FOLDER]\..\.tools\.api-keys.txt` (in shared .tools folder)

Old path: `[WORKSPACE_FOLDER]\..\.api-keys.txt`
New path: `[WORKSPACE_FOLDER]\..\.tools\.api-keys.txt`

Usage: `--keys-file [WORKSPACE_FOLDER]\..\.tools\.api-keys.txt`

## Prevention Rules (from session fails)

- **Model Accuracy**: Read model requests literally. Version numbers matter (e.g., Sonnet 4 != Sonnet 4.5).
- **Safety First**: UI automation scripts MUST have a `-DryRun` mode. Preview changes before sending irreversible keyboard events.
- **Playwriter Timeouts**: ALWAYS pass `timeout: 1500` (default is 20000ms!). Lower to 500ms when fast.

## DevSystem Source/Sync Rules

**CRITICAL: [DEVSYSTEM_FOLDER] is the SOURCE. .devin is the SYNC TARGET.**
**CRITICAL: Never leak project-specific or private data into workflows, skills, or rules.** These are reusable across projects. Use generic examples and placeholders only.

- **Creating new rules, workflows, skills** -> Create in [DEVSYSTEM_FOLDER] first, then sync
- **Editing existing content** -> Edit in [DEVSYSTEM_FOLDER] first, then sync
- **NEVER create or edit directly in `.devin/`** (except for temp testing)

**Sync direction:**
```
[DEVSYSTEM_FOLDER] ---(sync to)---> .devin/
[DEVSYSTEM_FOLDER]\workflows ---(copy to)---> .claude/commands/
```

**Claude Code commands:** All workflows from `[DEVSYSTEM_FOLDER]\workflows` are also copied to `.claude/commands/` (Devin CLI imports these as slash commands via Claude Code compatibility).

**Exception:** If user edits .devin directly, sync BACK to [DEVSYSTEM_FOLDER] first.

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

**Release archive**: `[WORKSPACE_FOLDER]\_OldDevSystemVersions\` — all prior DevSystem version folders are preserved here before deletion. Never delete a version folder without backing it up.

**Windows:** No symlinks. `.devin/` is a copy of `[DEVSYSTEM_FOLDER]`. Sync command and procedures: see `SOPS.md`.

**"deploy" keyword:** When user says "deploy", sync `[DEVSYSTEM_FOLDER]` to `.devin/` per `SOPS.md` → Quick Reference: Sync Command.

Automatically push commits to GitHub.

**2026-01-21**: Workflow Reference in devsystem-core.md was outdated (`GLOB-FL-006`). Updated to flat list of all 28 workflows.

## Special Workflows (Workspace Root)

**`deploy-to-all-repos.md`** — Deleted. Replaced by `/sync workspace` (FR-49) using `sync.ps1`.

**CRITICAL: NEVER auto-sync to downstream repos without explicit user confirmation.** Sync to downstream repos is a separate, explicit action.

## Sync Architecture Revision (2026-09-06)

**Folder rename**: `[WORKSPACE_FOLDER]\rules` → `[WORKSPACE_FOLDER]\specs` (pending `/rename` execution)
- `\specs` contains all SPEC, IMPL, TEST files
- `\specs\sops` contains advanced SOPs referenced in SOPS.md
- `\specs\guides` contains guides and how-tos

**Single script**: `sync.ps1` in workspace-management skill
- `-diff -sources [array] -targets [array] -configs [array] -output-file [path]` → produces additions, changes, deletions
- `-execute [same params]` → executes sync
- All params are JSON arrays but also support single strings
- If `-output-file` present, console just summarizes numbers; full report goes to file

**devsystem-sync.json at target `[WORKSPACE_FOLDER]` root**:
- Single source of truth for ALL sync configuration
- Each source entry carries its own complete config: bundle definitions, selected_bundles, include/exclude refiners, deprecated, never_overwrite
- NO sync-bundles.json at source — source is purely a content provider
- Source repo only maintains a list of relative paths to synced repos (for push operations)

**Source repo**: Only references RELATIVE downstream repo paths (e.g., `../Lana-V2-Dev`), never absolute

**Use cases** (implemented in `sync.md` workflow):
- `/sync workspace settings from repo xyz` — merges/replicates NOTES.md + devsystem-sync.json into current repo
- `/sync workspace settings to repo xyz` — merges/replicates NOTES.md + devsystem-sync.json into target repo
- `/sync sync settings from repo xyz` — only devsystem-sync.json into current repo
- `/sync sync settings to repo xyz` — only devsystem-sync.json into target repo
- `/sync knowledge from source` — reads source from devsystem-sync.json, runs sync.ps1 -diff, preview, auto-execute on confirm
- `/sync knowledge to targets` — reads targets from source NOTES.md synced repos list, runs sync.ps1 -diff, preview, auto-execute on confirm
- `/sync specs from source` — same flow for specs
- `/sync specs to targets` — same flow for specs

## [SKILL_CATEGORIES]

- **Development**: coding-conventions, deep-research, drift-correction, edird-phase-planning, git, git-conventions, github, hosting, image-tools, llm-computer-use, llm-evaluation, llm-transcription, ms-playwright-mcp, pdf-tools, playwriter-mcp, seo-tools, session-management, windows-desktop-control, windsurf-auto-model-switcher, workspace-management, write-documents, youtube-downloader
- **Personal**: google-account, travel-info
- **All**: Development + Personal (all skills)

## [PERSONAL_WORKFLOWS] (excluded from Development-only repos, deployed only to "All" repos)

- conversation-start.md
- conversation-update.md

**[LINKED_REPOS]**:
- e:\Dev\KarstensWorkspace
  - Skills: All
  - Overwrite everything
  - Delete deprecated or renamed files from older DevSystem versions
  - Don't delete unrelated existing files
- e:\Dev\OpenAI-BackendTools
  - Skills: Development
  - Overwrite everything
  - Delete deprecated or renamed files from older DevSystem versions
  - Don't delete unrelated existing files
- e:\Dev\PRXL\src
  - Skills: Development
  - Overwrite everything
  - Delete deprecated or renamed files from older DevSystem versions
  - Don't delete unrelated existing files
- e:\Dev\SharePoint-GPT-Middleware
  - Skills: Development
  - Overwrite everything
  - Never overwrite: workflows/project-release.md (project-specific)
  - Delete deprecated or renamed files from older DevSystem versions
  - Don't delete unrelated existing files
- e:\Dev\USTVA
  - Skills: All
  - Overwrite everything
  - Delete deprecated or renamed files from older DevSystem versions
  - Don't delete unrelated existing files
- e:\Dev\openclaw\workspace
  - Skills: All
  - Overwrite: rules/, workflows/, skills/ folders
  - Create: WORKFLOWS.md, _Sessions/ (if not exists)
  - Never overwrite: AGENTS.md, HEARTBEAT.md, memory/, MEMORY.md
  - Special: Copy _OPENCLAW-AGENTS.md to AGENTS.md, copy _OPENCLAW_WORKFLOWS.md to WORKFLOWS.md (always sync both)
- e:\Dev\LLM-Research
  - Skills: Development
  - Overwrite everything
  - Delete deprecated or renamed files from older DevSystem versions
  - Don't delete unrelated existing files

## Release Configuration

Config for `/project-release` workflow. All paths use workspace constants from `## Workspace Constants` section above. See `_SPEC_RELEASE_PROJECT_WORKFLOW.md [RLSPROJ-SP01]` in `Docs/Specs/` for full schema and decision guide.

```
[RELEASE_CONFIG]
sops_file: [RELEASE_SOPS_FILE]
sessions_folder: [RELEASE_SESSIONS_FOLDER]
release_notes_dir: [RELEASE_NOTES_DIR]
release_notes_naming: RELEASE_NOTES_v{VERSION}_{DATE}.md
tag_annotation_template: Release {TAG}: {SUMMARY}

[RELEASE_REPO: product]
path: [WORKSPACE_FOLDER]
role: product
tag_format: date
version_source: devsystem_folder
post_release_bump: devsystem_rename
github_release: true
```

Instructions: SINGLE-PROJECT mode — one repo, one `[RELEASE_REPO]` block. Date-based tags (`YYYY-MM-DD`). Version source is `devsystem_folder` (parsed from `Current [DEVSYSTEM]` line above). Post-release bump renames `DevSystemVX.Y` folder to next minor version per SOPS SOP 7. No binary build, no version gate. Release notes go in `Docs/ReleaseNotes/` per existing convention (see Release Notes Location section above).