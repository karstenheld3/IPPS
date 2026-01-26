# Discover Windsurf Models Workflow

Interactive workflow where Cascade dynamically detects popup position each time.

## CRITICAL: No Hardcoded Coordinates

Popup position changes when:
- Screen resolution changes
- Window moves
- Different monitor

**Always run Phase 1 to detect current popup position.**

## Prerequisites

- Windsurf running with Cascade panel visible
- Custom keybinding `Ctrl+Shift+F9` installed (see ../SETUP.md)

## Workflow Steps

### Phase 1: Detect Popup Position (ALWAYS RUN)

```powershell
.\capture-with-crop.ps1 -Phase1Only
```

1. Takes fullscreen screenshot
2. Cascade analyzes screenshot
3. Cascade returns popup coordinates as JSON:
   ```json
   { "x": 1570, "y": 1070, "width": 320, "height": 210 }
   ```

### Phase 2: Capture with Dynamic Coordinates

```powershell
.\capture-with-crop.ps1 -CropX [x] -CropY [y] -CropWidth [w] -CropHeight [h] -MaxSections 12
```

Use coordinates from Phase 1 analysis.

### Phase 3: Extract Models

1. Cascade reads each cropped screenshot
2. Extracts model names and costs
3. Stops when list wraps around (duplicate models seen)
4. Updates `windsurf-model-registry.json`

## Debugging Blank Screenshots

If cropped screenshots are blank:
1. Query screen resolution: `[System.Windows.Forms.Screen]::PrimaryScreen.Bounds`
2. Zoom out: capture large area (500x300) at estimated position
3. Shift x/y to move toward popup
4. Refine width/height

## Output Format

```json
{
  "_version": "1.3",
  "_updated": "2026-01-26",
  "_source": "discovered from Windsurf model selector UI via capture-with-crop.ps1",
  "models": [
    { "name": "Claude 3.5 Sonnet", "cost": "2x" }
  ]
}
```

No hardcoded coordinates in output - they are session-specific.
