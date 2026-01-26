# Screenshot Scripts

Two scripts for different purposes:

## simple-screenshot.ps1

**Purpose:** Passive screenshot capture for testing and verification

**Behavior:** Takes a screenshot WITHOUT any keyboard/mouse input

**Use when:**
- Testing the model switcher
- Verifying UI state
- General documentation screenshots
- Any time you need a clean capture without UI interaction

**Usage:**
```powershell
# Full screen
.\simple-screenshot.ps1

# Custom size/position
.\simple-screenshot.ps1 -Width 1920 -Height 1080 -X 0 -Y 0

# Custom output path
.\simple-screenshot.ps1 -OutputPath "C:\temp\screenshot.jpg"
```

## capture-with-crop.ps1

**Purpose:** Model registry update workflow

**Behavior:** OPENS model selector popup, sends keystrokes, navigates list, takes screenshots

**Use when:**
- Updating windsurf-model-registry.json
- Extracting model names and costs from UI
- Following UPDATE_WINDSURF_MODEL_REGISTRY.md workflow

**WARNING:** This script actively manipulates the UI. Do NOT use for general screenshots.

**Usage:**
```powershell
# Full screen capture with popup navigation
.\capture-with-crop.ps1 -CropX 0 -CropY 0 -CropWidth 2048 -CropHeight 1280 -MaxSections 10
```

## Quick Reference

| Need | Script |
|------|--------|
| Test model switcher | `simple-screenshot.ps1` |
| Verify popup state | `simple-screenshot.ps1` |
| Update model registry | `capture-with-crop.ps1` |
| General screenshots | `simple-screenshot.ps1` |
