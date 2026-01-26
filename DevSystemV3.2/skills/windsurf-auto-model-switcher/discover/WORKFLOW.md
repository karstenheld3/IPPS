# Discover Windsurf Models Workflow

Simplified workflow: fullscreen capture for all sections (no cropping needed).

## Why Fullscreen?

Cropping requires accurate pixel coordinates, but:
- LLM sees scaled-down images, can't map to actual screen pixels
- Popup position changes when window moves or resolution changes
- Cropping adds complexity with minimal benefit

Fullscreen JPEG at default quality is ~150KB per image. 10 sections = ~1.5MB total.

## Workflow Steps

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

## Output Format

```json
{
  "_version": "1.3",
  "_updated": "2026-01-26",
  "_source": "discovered from Windsurf model selector UI",
  "models": [
    { "name": "Claude 3.5 Sonnet", "cost": "2x" }
  ]
}
```
