# Renderings Skill Setup

One-time setup for `render.py`. No pip installs are needed when the shared venv already contains `playwright` (it does in the standard `.tools/llm-venv`).

## Pre-Installation Verification

Complete all checks before installing. Read-only; nothing is modified.

1. Venv Python exists: step 1 prints `True`
2. Playwright importable: step 2 prints a version
3. Existing browser state: `Get-ChildItem "$env:LOCALAPPDATA\ms-playwright" -Directory` lists installed builds (an empty list or a missing folder means step 3 downloads one)
4. Render check with an existing build: `render.py --list-templates` prints template names (does not start a browser)

Pre-Installation Checklist:
- [ ] Venv Python found
- [ ] Playwright imports
- [ ] Installed browser builds listed
- [ ] `--list-templates` prints 4 template names

The install in step 3 is idempotent: running it again keeps existing builds and downloads only a missing one. No configuration file is modified, so no backup is needed.

## 1. Set Paths

```powershell
$venvPython = "[SKILL_TOOLS_FOLDER]\llm-venv\Scripts\python.exe"
Test-Path $venvPython
```

## 2. Check Python Packages

```powershell
& $venvPython -c "import playwright; print('playwright', playwright.__version__)"
```

Missing → `& "[SKILL_TOOLS_FOLDER]\llm-venv\Scripts\pip.exe" install playwright` (only if the venv was created without it).

Optional for page counts in the report: `pymupdf` (already in the standard venv). Without it the report shows PDF size only.

## 3. Install the Pinned Chromium Build

```powershell
& $venvPython -m playwright install chromium-headless-shell
```

Downloads the headless shell that matches the installed Playwright version into `%LOCALAPPDATA%\ms-playwright`. Repeat after upgrading the `playwright` package (each version pins its own build).

Without this step `render.py` still works when another Chromium build exists in `%LOCALAPPDATA%\ms-playwright` (for example from the Node Playwright MCP) or when Google Chrome is installed; the report line then shows `(fallback: ...)`.

## 4. Verify

```powershell
& $venvPython -c "from playwright.sync_api import sync_playwright as s; p = s().start(); b = p.chromium.launch(); print('OK', b.version); b.close(); p.stop()"
```

Expected: `OK 1xx.0.xxxx.xx`

Smoke test with any Markdown file:

```powershell
& $venvPython "[AGENT_FOLDER]\skills\renderings\render.py" README.md --output-dir "$env:TEMP\render-test" --overwrite
```

Expected: one report line with `html ... | pdf N pages ...` and `DONE: 1 ok, 0 failed, 0 skipped`.

Smoke test with an HTML file (PDF only, layout detected):

```powershell
& $venvPython "[AGENT_FOLDER]\skills\renderings\render.py" "$env:TEMP\render-test\README.html" --overwrite
```

Expected: report line with `pdf N pages ... | layout portrait` and `DONE: 1 ok, 0 failed, 0 skipped`.

## 5. Fonts

No font installation is needed. The templates embed Inter, JetBrains Mono, and Open Sans Condensed (woff2, folder `fonts/` next to `render.py`), so output looks the same on Windows, macOS, and Linux. Only these fall back to installed fonts:
- Emoji: Segoe UI Emoji (Windows), Apple Color Emoji (macOS), Noto Color Emoji (Linux)
- Characters missing in the embedded fonts (for example arrows in Open Sans Condensed): Segoe UI, Menlo, DejaVu Sans Mono, Liberation Mono, Noto

Embedded static fonts become TrueType subsets in the PDF; variable fonts embed as Type3 outlines, so none is used.
