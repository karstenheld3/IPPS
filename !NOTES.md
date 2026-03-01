[DEFAULT_SESSIONS_FOLDER]: [WORKSPACE_FOLDER]\_PrivateSessions
[SESSION_ARCHIVE_FOLDER]: [SESSION_FOLDER]\..\Archive

Current [DEVSYSTEM]: DevSystemV3.3
Current [DEVSYSTEM_FOLDER]: [WORKSPACE_FOLDER]\[DEVSYSTEM]

## Cascade Model Switching

**Tier Definitions:**
- **MODEL-HIGH** = Claude Opus 4.5 (Thinking) [5x] - Complex reasoning, specs, architecture
- **MODEL-MID** = Claude Sonnet 4.5 [2x] - Code verification, bug fixes, refactoring
- **MODEL-LOW** = Gemini 3 Flash Medium [1x] - Scripts, git, file ops, monitoring (78% SWE-Bench, 372 TPS)

**Activity Mapping:**
- MODEL-HIGH: Writing docs, analyzing problems, architecture, gates
- MODEL-MID: Code verification, bug fixes, refactoring, implementation
- MODEL-LOW: Running scripts, git commit, file reads, session archive

**Default:** MODEL-HIGH (when uncertain)

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

## Model Switching Findings (2026-01-26)

- **Bulletproof Refocus**: Use `Ctrl+Shift+A` to reliably focus the Cascade chat panel in VS Code/Windsurf.
- **German Keyboards**: Avoid `Ctrl+Alt` shortcuts; they conflict with `AltGr`. Use `Ctrl+Shift+F9/F10` for reliable model selection automation.
- **Fast & Cheap Models**: Gemini 3 Flash Medium (372 TPS, 78% SWE-Bench) is the current best performer for MODEL-LOW tasks. Grok Code Fast 1 (236 TPS, 70.8% SWE-Bench) is the best free option in Windsurf for speed.

**ID-REGISTRY.md** - Prevents term and ID collisions. Contains DevSystem constants and project TOPIC registry.

## Karsten's Model Rate Limits (2026-01-26)

- **gpt-5-nano**: 120+ workers. 120k tokens in 17.9s. TPM: ~402,000.
- **gpt-5-mini**: 120+ workers. 120k tokens in 43.7s. TPM: ~164,000.
- **claude-4-5-haiku**: 60+ workers. 60k tokens in 8s. TPM: ~450,000.
- **claude-4-5-sonnet**: 60+ workers. 60k tokens in 7.7s. TPM: ~467,000.
- **claude-4-5-opus**: 60+ workers. 60k tokens in 7.6s. TPM: ~473,000.

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

Automatically push commits to GitHub.

**2026-01-21**: Workflow Reference in devsystem-core.md was outdated (`GLOB-FL-006`). Updated to flat list of all 28 workflows.

## Special Workflows (Workspace Root)

**`deploy-to-all-repos.md`** - Deploys DevSystem files to all linked repos. Located in workspace root (not `.windsurf/workflows/`) to prevent it from being copied to other repos. Run manually by reading the file and following the instructions.

**CRITICAL: NEVER auto-deploy to [LINKED_REPOS]**. Always ask user before deploying to linked repos. Deployment to linked repos is a separate, explicit action.

**[LINKED_REPOS]**:
- e:\Dev\KarstensWorkspace
  - Overwrite everything
  - Delete deprecated or renamed files from older DevSystem versions
  - Don't delete unreleated existing files
- e:\Dev\OpenAI-BackendTools
  - Overwrite everything
  - Delete deprecated or renamed files from older DevSystem versions
  - Don't delete unreleated existing files
- e:\Dev\PRXL\src
  - Overwrite everything
  - Delete deprecated or renamed files from older DevSystem versions
  - Don't delete unreleated existing files
- e:\Dev\SharePoint-GPT-Middleware
  - Overwrite everything
  - Delete deprecated or renamed files from older DevSystem versions
  - Don't delete unreleated existing files
-  e:\dev\USTVA
  - Overwrite everything
  - Delete deprecated or renamed files from older DevSystem versions
  - Don't delete unreleated existing files
- e:\Dev\openclaw\workspace
  - Overwrite: rules/, workflows/, skills/ folders
  - Create: WORKFLOWS.md, _Sessions/ (if not exists)
  - Never overwrite: AGENTS.md, HEARTBEAT.md, memory/, MEMORY.md
  - Special: Copy _OPENCLAW-AGENTS.md to AGENTS.md (one-time), copy _OPENCLAW_WORKFLOWS.md to WORKFLOWS.md
  - **Sync _OPENCLAW_WORKFLOWS.md** every time workflows are added/removed in DevSystem