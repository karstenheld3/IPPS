# Screenshot Scripts

## For General Screenshots

Use `windows-desktop-control` skill:
```powershell
.\simple-screenshot.ps1
```

## capture-model-selector.ps1

Purpose: Model registry update workflow. OPENS model selector popup, sends keystrokes, navigates list, takes screenshots.

WARNING: Actively manipulates UI. Do NOT use for general screenshots.

Use when: Updating windsurf-model-registry.json per UPDATE_WINDSURF_MODEL_REGISTRY.md workflow.

```powershell
.\capture-with-crop.ps1 -CropX 0 -CropY 0 -CropWidth 2048 -CropHeight 1280 -MaxSections 10
```

## Quick Reference

- Test/verify model switcher, general screenshots: `simple-screenshot.ps1`
- Update model registry: `capture-with-crop.ps1`