[DEFAULT_SESSIONS_FOLDER]: [WORKSPACE_FOLDER]\_PrivateSessions
[SESSION_ARCHIVE_FOLDER]: [SESSION_FOLDER]\..\Archive

Current [DEVSYSTEM]: DevSystemV3.2
Current [DEVSYSTEM_FOLDER]: [WORKSPACE_FOLDER]\[DEVSYSTEM]

## Cascade Model Tiers

**Tier Definitions:**
- **HIGH** = Claude Opus 4.5 (Thinking) [5x] - Complex reasoning, specs, architecture
- **MID** = Claude Sonnet 4.5 [2x] - Code verification, bug fixes, refactoring
- **CHORES** = Claude Haiku 4.5 [1x] - Scripts, git, file ops, monitoring

**Activity Mapping:**
- HIGH: Writing docs, analyzing problems, architecture, gates
- MID: Code verification, bug fixes, refactoring, implementation
- CHORES: Running scripts, git commit, file reads, session archive

**Default:** HIGH (when uncertain)

**ID-REGISTRY.md** - Prevents term and ID collisions. Contains DevSystem constants and project TOPIC registry.

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