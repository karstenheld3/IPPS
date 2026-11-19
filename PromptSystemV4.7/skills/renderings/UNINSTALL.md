# Renderings Skill Uninstall

Removes what the renderings skill installed. The skill installs no pip packages (it reuses `playwright` and `pymupdf` of the shared venv) and modifies no configuration file. Only the Playwright browser build is skill-specific.

## Pre-Uninstall Verification

Read-only checks; nothing is removed.

1. Installed browser builds:

```powershell
Get-ChildItem "$env:LOCALAPPDATA\ms-playwright" -Directory | Select-Object Name
```

Expected: `chromium_headless_shell-NNNN` (installed by SETUP.md step 3). A build with the same number may also be used by the Node Playwright MCP: remove it only when no other tool needs it (check 2). `chromium-NNNN`, `ffmpeg-*`, and `winldd-*` folders are not created by this skill.

2. Other users of the browser build:

```powershell
Select-String -Path "[AGENT_FOLDER]\skills\*\*.py" -Pattern "playwright" -List | Select-Object -ExpandProperty Path
```

Expected: every listed script (other than `renderings\render.py`) also depends on the same browser build; keep the build when any of them is used.

3. Outputs to keep: rendered `.html` and `.pdf` files stay where they are; this procedure never deletes them.

Pre-Uninstall Checklist:
- [ ] Installed browser builds listed
- [ ] Other scripts that use Playwright identified
- [ ] Rendered outputs kept

If all checks pass, proceed.

## 1. Remove the Browser Build

```powershell
Remove-Item "$env:LOCALAPPDATA\ms-playwright\chromium_headless_shell-*" -Recurse -Force
```

Only run this when check 2 found no other user of the build and the Node Playwright MCP is not in use. Do not remove `chromium-*`, `ffmpeg-*`, or `winldd-*` folders.

## 2. Remove the Skill Files

Delete `[AGENT_FOLDER]\skills\renderings\` and `[AGENT_FOLDER]\workflows\render.md`. In a PromptSystem workspace, delete them in `[PROMPTSYSTEM_FOLDER]` first (source of truth), then mirror to `[AGENT_FOLDER]`.

## Post-Uninstall Verification

```powershell
Test-Path "[AGENT_FOLDER]\skills\renderings"
Test-Path "[AGENT_FOLDER]\workflows\render.md"
Get-ChildItem "$env:LOCALAPPDATA\ms-playwright" -Directory | Select-Object Name
```

Expected: `False`, `False`, and no `chromium_headless_shell-*` folder.

Manual cleanup: none. The venv packages `playwright` and `pymupdf` stay (shared with other skills).
