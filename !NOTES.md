[DEFAULT_SESSIONS_FOLDER]: [WORKSPACE_FOLDER]\_PrivateSessions
[SESSION_ARCHIVE_FOLDER]: [SESSION_FOLDER]\..\_Archive

Current [DEVSYSTEM]: DevSystemV3.1
Current [DEVSYSTEM_FOLDER]: [WORKSPACE_FOLDER]\[DEVSYSTEM]

**CONCEPTS.md** - Inventory of named concepts (frameworks, identifiers, strategies, document types). Reference only, specs have details.

If you update workflows in .windsurf\workflows, sync changes back to the current [DEVSYSTEM_FOLDER].
DONT auto-sync changes to  .windsurf\workflows if you update workflows in the [DEVSYSTEM_FOLDER].

## Workflow Design Rules

**CRITICAL: Workflows MUST be phase-model independent.**
- Workflows contain task knowledge (what to do, how to do it, what tools/context needed)
- Workflows MUST NOT reference phase names (EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER)
- Workflows MUST NOT have `phase:` field in frontmatter
- Phase orchestration belongs in the phase model (EDIRD), not in workflows
- This allows swapping EDIRD for alternative phase models without rewriting workflows

## Platform Notes

**Windows:** No symlinks. `.windsurf/` is a copy of `[DEVSYSTEM_FOLDER]`, not a symlink.

**Agent sync method:** Agent cannot directly edit `.windsurf/` files. To update `.windsurf/` after editing DevSystemV3:
```powershell
Copy-Item -Path "DevSystemV3\*" -Destination ".windsurf\" -Recurse -Force
```

Automatically push commits to GitHub.

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