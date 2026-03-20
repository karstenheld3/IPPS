# Update Model Registry Workflow

Update `windsurf-model-registry.json` with current models and costs.

## Data Sources (Priority Order)

1. **Windsurf Docs** (preferred) - https://docs.windsurf.com/windsurf/models
2. **UI Screenshot Capture** (fallback) - when docs outdated or unavailable
3. **Playwright MCP** (last resort) - if docs blocked and UI capture fails

## Method A: Windsurf Docs (Recommended)

1. Fetch https://docs.windsurf.com/windsurf/models
2. Parse model names and credit costs
3. Update `windsurf-model-registry.json`

## Method B: UI Screenshot Capture (Fallback)

**IMPORTANT:** Use `capture-model-selector.ps1` for registry updates ONLY. For general screenshots, use `windows-desktop-control/simple-screenshot.ps1`.

1. Capture: `.\capture-model-selector.ps1 -MaxSections 10` (opens model selector, scrolls via keystrokes, DPI-aware fullscreen)
2. Cascade reads each screenshot from `../.tools/_screenshots/`, extracts model names and costs
3. Stop when duplicate models appear (list wrapped)
4. Update `windsurf-model-registry.json`
5. **Only after successful update**, cleanup: `Remove-Item -Path "[WORKSPACE]/../.tools/_screenshots/*.jpg" -Force` (keep on failure for debugging)

## Method C: Playwright (Last Resort)

1. Navigate to https://docs.windsurf.com/windsurf/models via Playwright MCP
2. Extract model table data
3. Update registry

## Output Format

```json
{
  "_version": "1.4",
  "_updated": "2026-01-26",
  "_source": "docs.windsurf.com/windsurf/models",
  "models": [
    { "name": "Claude 3.5 Sonnet", "cost": "2x" }
  ]
}
```