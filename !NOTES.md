[SESSIONS_FOLDER]: [WORKSPACE_FOLDER]\_PrivateSessions
[SESSIONS_ARCHIVE]: [SESSIONS_FOLDER]\_Archive

Current [DEVSYSTEM]: DevSystemV2.1
Current [DEVSYSTEM_FOLDER]: [WORKSPACE_FOLDER]\[DEVSYSTEM]

If you update workflows in .windsurf\workflows, sync changes back to the current [DEVSYSTEM_FOLDER].
DONT auto-sync changes to  .windsurf\workflows if you update workflows in the [DEVSYSTEM_FOLDER].

## Platform Notes

**Windows:** No symlinks. `.windsurf/` is a copy of `[DEVSYSTEM_FOLDER]`, not a symlink. Use PowerShell to sync:
```powershell
Copy-Item -Path "[DEVSYSTEM_FOLDER]\*" -Destination ".windsurf\" -Recurse -Force
```

Automatically push commits to GitHub.

## Special Workflows (Workspace Root)

**`deploy-to-all-repos.md`** - Deploys DevSystem files to all linked repos. Located in workspace root (not `.windsurf/workflows/`) to prevent it from being copied to other repos. Run manually by reading the file and following the instructions.

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
/
