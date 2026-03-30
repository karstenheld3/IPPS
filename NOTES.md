[DEFAULT_SESSIONS_FOLDER]: [WORKSPACE_FOLDER]\_PrivateSessions
[SESSION_ARCHIVE_FOLDER]: [SESSION_FOLDER]\..\Archive

Current [DEVSYSTEM]: DevSystemV3.6
Current [DEVSYSTEM_FOLDER]: [WORKSPACE_FOLDER]\[DEVSYSTEM]


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

**CRITICAL: [DEVSYSTEM_FOLDER] is the SOURCE. .windsurf is the SYNC TARGET.**

- **Creating new rules, workflows, skills** -> Create in [DEVSYSTEM_FOLDER] first, then sync
- **Editing existing content** -> Edit in [DEVSYSTEM_FOLDER] first, then sync
- **NEVER create or edit directly in `.windsurf/`** (except for temp testing)

**Sync direction:**
```
[DEVSYSTEM_FOLDER] ---(sync to)---> .windsurf/
```

**Exception:** If user edits .windsurf directly, sync BACK to [DEVSYSTEM_FOLDER] first.

**README.md Link Convention (2026-03-19):**
- **ALWAYS use `.windsurf/` paths in README.md** - Never reference `DevSystemV3.6/` or any version folder
- Example: `.windsurf/skills/write-documents/APAPALAN_RULES.md` (GOOD)
- Example: `DevSystemV3.6/skills/write-documents/APAPALAN_RULES.md` (BAD)
- Reason: README is user-facing, users interact with `.windsurf/`, not version folders

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

**Windows:** No symlinks. `.windsurf/` is a copy of `[DEVSYSTEM_FOLDER]`, not a symlink.

**Sync command** (run after editing [DEVSYSTEM_FOLDER]):
```powershell
Copy-Item -Path "[DEVSYSTEM_FOLDER]\*" -Destination ".windsurf\" -Recurse -Force
```

**"deploy" keyword:** When user says "deploy", sync [DEVSYSTEM_FOLDER] to `.windsurf/` using the command above.

Automatically push commits to GitHub.

**2026-01-21**: Workflow Reference in devsystem-core.md was outdated (`GLOB-FL-006`). Updated to flat list of all 28 workflows.

## Special Workflows (Workspace Root)

**`deploy-to-all-repos.md`** - Deploys DevSystem files to all linked repos. Located in workspace root (not `.windsurf/workflows/`) to prevent it from being copied to other repos. Run manually by reading the file and following the instructions.

**CRITICAL: NEVER auto-deploy to [LINKED_REPOS]**. Always ask user before deploying to linked repos. Deployment to linked repos is a separate, explicit action.

**[SKILL_CATEGORIES]**:
- **Development**: coding-conventions, deep-research, edird-phase-planning, git-conventions, github, llm-computer-use, llm-evaluation, llm-transcription, ms-playwright-mcp, pdf-tools, session-management, windows-desktop-control, windsurf-auto-model-switcher, write-documents, youtube-downloader
- **Personal**: google-account, travel-info
- **All**: Development + Personal (all skills)

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