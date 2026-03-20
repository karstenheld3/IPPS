# Windows Desktop Control

Windows desktop automation: screenshots, window management, keyboard/mouse simulation.

Prerequisites: Windows OS, PowerShell 5.1+

## simple-screenshot.ps1

Passive screenshot, no UI interaction. DPI-aware via Win32 `GetDeviceCaps(DESKTOPHORZRES/DESKTOPVERTRES)`.

```powershell
.\simple-screenshot.ps1 [-OutputPath "C:\temp\screenshot.jpg"] [-Width 1920] [-Height 1080] [-X 0] [-Y 0]
```

Parameters:
- `-OutputPath` - Output file (default: `../.tools/_screenshots/YYYY-MM-DD_HH-mm-ss_screenshot.jpg`)
- `-Width` / `-Height` - Capture dimensions (default: full screen physical resolution)
- `-X` / `-Y` - Capture offset (default: 0)

Output: JPEG. Default folder auto-created. No keyboard/mouse input sent.