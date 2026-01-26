# Update Model Registry Workflow

Update `windsurf-model-registry.json` with current models and costs.

## Data Sources (Priority Order)

1. **Windsurf Docs** (preferred) - https://docs.windsurf.com/windsurf/models
2. **UI Screenshot Capture** (fallback) - when docs are outdated or unavailable

## Method A: Windsurf Docs (Recommended)

### Step 1: Fetch Model Data

Use web search or read URL:
```
https://docs.windsurf.com/windsurf/models
```

### Step 2: Extract Models and Costs

Parse the page for model names and credit costs.

### Step 3: Update Registry

Update `windsurf-model-registry.json` with extracted data.

## Method B: UI Screenshot Capture (Fallback)

Use when docs are outdated or don't match UI.

### Step 1: Capture All Sections

```powershell
.\capture-with-crop.ps1 -CropX 0 -CropY 0 -CropWidth 2048 -CropHeight 1280 -MaxSections 10
```

Replace 2048x1280 with your screen resolution.

### Step 2: Cascade Reads Screenshots

Cascade reads each fullscreen screenshot from `.tools/_screenshots/`.
Extracts model names and costs from the popup visible in each image.

### Step 3: Stop When List Wraps

When Cascade sees duplicate models (list wrapped around), extraction is complete.

### Step 4: Update Registry

Update `windsurf-model-registry.json` with discovered models and costs.

### Step 5: Cleanup

```powershell
Remove-Item -Path "[WORKSPACE]/.tools/_screenshots/*.jpg" -Force
```

## Method C: Playwright (Last Resort)

If docs blocked or UI capture fails, use Playwright MCP to navigate:
1. Open https://docs.windsurf.com/windsurf/models
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
