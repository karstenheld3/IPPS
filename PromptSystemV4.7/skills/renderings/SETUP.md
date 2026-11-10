# Renderings Skill Setup

One-time setup for `render.py`. No pip installs are needed when the shared venv already contains `playwright` (it does in the standard `.tools/llm-venv`).

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

## 5. Fonts

The templates use installed system fonts only:
- Sans: Inter if installed, otherwise Segoe UI, Noto Sans, Arial
- Monospace: Consolas (present on every Windows), then JetBrains Mono, DejaVu Sans Mono, Cascadia Mono
- Emoji: Segoe UI Emoji (Windows), Noto Color Emoji (Linux)

Static fonts embed as TrueType subsets in the PDF; variable fonts (Cascadia) embed as Type3 outlines, which is why they are last in the stack.
