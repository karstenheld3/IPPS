# INFO: CLI Screenshot and Image Resize Tools

**Doc ID**: CLITL-IN01
**Goal**: MCPI research on freeware command-line tools for screenshot capture and image resizing on Windows
**Timeline**: Created 2026-01-27, Updated 1 time (2026-01-27)

**Depends on:**
- `_SPEC_LLM_COMPUTER_USE.md [LLMCU-SP01]` for tool selection requirements

## Summary (Copy/Paste Ready)

### Screenshot Tools

- **NirCmd** - Freeware, Native CLI, DPI unknown, Region Yes, Delay No, PNG/JPG/BMP
- **Flameshot** - GPLv3, Native CLI, DPI Yes, Region Yes, Delay Yes, PNG
- **ShareX** - GPLv3, CLI + Hotkeys, DPI Yes, Region Yes, Delay Yes, PNG/JPG/GIF
- **FFmpeg gdigrab** - LGPLv2.1, Native CLI, DPI Yes, Region Yes, Delay No, Any format
- **IrfanView** - Freeware, CLI, DPI Yes, Region Yes, Delay No, Many formats
- **PowerShell** - Built-in, Script, DPI varies, Region Yes, Delay No, PNG/JPG/BMP

### Image Resize Tools

- **ImageMagick** - Apache 2.0, Native CLI, Batch Yes, Quality Yes, 200+ formats
- **PowerToys ImageResizer** - MIT, Native CLI, Batch Yes, Quality Yes, Common formats
- **imgp** - GPLv3, Native CLI, Batch Yes, Quality Yes, JPEG/PNG
- **IrfanView** - Freeware, CLI, Batch Yes, Quality Yes, Many formats
- **FFmpeg** - LGPLv2.1, Native CLI, Batch Yes, Quality Yes, Video/image

### Recommendations for LLM Computer Use

- **Screenshot**: NirCmd (simplest) or PowerShell (no dependencies) [VERIFIED]
- **Resize**: ImageMagick (most powerful) or PowerToys (Windows-native) [VERIFIED]
- **Existing**: Current `simple-screenshot.ps1` already handles DPI correctly [PROVEN]

## Table of Contents

1. [Screenshot Tools](#1-screenshot-tools)
2. [Image Resize Tools](#2-image-resize-tools)
3. [Combined Tools](#3-combined-tools)
4. [Built-in Windows Options](#4-built-in-windows-options)
5. [Comparison Matrix](#5-comparison-matrix)
6. [Integration Considerations](#6-integration-considerations)
7. [Sources](#7-sources)
8. [Document History](#8-document-history)

## 1. Screenshot Tools

### NirCmd

**License**: Freeware (closed source, free for personal/commercial use)
**Platform**: Windows only
**Size**: ~100KB

**CLI Commands**:
```cmd
# Full screen screenshot
nircmd.exe savescreenshot "c:\screenshots\shot.png"

# Region capture (x, y, width, height)
nircmd.exe savescreenshot "c:\screenshots\shot.png" 50 50 300 200

# Full screen (all monitors as one image)
nircmd.exe savescreenshotfull "c:\screenshots\shot.png"

# Specific window
nircmd.exe savescreenshotwin "c:\screenshots\shot.png" stitle "Calculator"

# To clipboard
nircmd.exe savescreenshot *clipboard* 150 150 400 400
```

**Pros**:
- Extremely small and portable
- No installation required
- Very fast execution
- Supports region, window, and full screen

**Cons**:
- Closed source
- No delay option
- DPI awareness undocumented

**Status**: [VERIFIED]

### Flameshot

**License**: GPLv3 (open source)
**Platform**: Windows, Linux, macOS
**Size**: ~40MB installed

**CLI Commands**:
```cmd
# Full screen capture (silent, save to path)
flameshot full -p "C:\screenshots" -c

# Region capture with GUI
flameshot gui -p "C:\screenshots"

# Delayed capture (2000ms)
flameshot gui -d 2000

# Specific screen
flameshot screen -n 1 -c

# Raw output (bytes to stdout)
flameshot screen -r
```

**Pros**:
- Open source, actively maintained
- Built-in annotation tools
- Delay support
- Multi-monitor aware

**Cons**:
- Larger installation
- Windows CLI wrapper needed for console output (`flameshot-cli.exe`)
- PNG only output

**Status**: [VERIFIED]

### ShareX

**License**: GPLv3 (open source)
**Platform**: Windows only
**Size**: ~20MB installed

**CLI Commands**:
```cmd
# Full screen capture
ShareX.exe -PrintScreen

# Rectangle region
ShareX.exe -RectangleRegion

# Active window
ShareX.exe -ActiveWindow

# Active monitor
ShareX.exe -ActiveMonitor

# Silent mode + auto-close
ShareX.exe -s -PrintScreen -autoclose

# Custom workflow
ShareX.exe -workflow "Capture rectangle region & annotate"
```

**Pros**:
- Feature-rich
- Highly configurable workflows
- Built-in upload to many services
- Open source

**Cons**:
- GUI-focused, CLI is secondary
- Requires installation
- Silent mode still shows tray icon

**Status**: [VERIFIED]

### FFmpeg (gdigrab)

**License**: LGPLv2.1 / GPLv2 (open source)
**Platform**: Windows, Linux, macOS
**Size**: ~80MB

**CLI Commands**:
```cmd
# Single frame screenshot
ffmpeg -f gdigrab -framerate 1 -i desktop -frames:v 1 screenshot.png

# Region capture
ffmpeg -f gdigrab -offset_x 100 -offset_y 100 -video_size 800x600 -framerate 1 -i desktop -frames:v 1 region.png

# Specific window by title
ffmpeg -f gdigrab -framerate 1 -i title=Calculator -frames:v 1 calc.png

# JPEG output with quality
ffmpeg -f gdigrab -framerate 1 -i desktop -frames:v 1 -q:v 2 screenshot.jpg
```

**Pros**:
- Extremely powerful and flexible
- Already widely installed
- Supports any output format
- Can capture video too

**Cons**:
- Complex command syntax
- Large dependency
- Slower startup than dedicated tools

**Status**: [VERIFIED]

### IrfanView

**License**: Freeware (free for personal use)
**Platform**: Windows only
**Size**: ~3MB

**CLI Commands**:
```cmd
# Full screen capture
i_view64.exe /capture=0 /convert=screenshot.jpg

# Active window
i_view64.exe /capture=1 /convert=window.jpg

# Client area of active window
i_view64.exe /capture=2 /convert=client.jpg

# Rectangle selection
i_view64.exe /capture=3 /convert=region.jpg

# Specific object/window
i_view64.exe /capture=4 /convert=object.jpg
```

**Capture modes**:
- 0 = Full screen
- 1 = Active window
- 2 = Client area of active window
- 3 = Rectangle selection (manual)
- 4 = Object/window selection

**Pros**:
- Fast, lightweight
- Combined screenshot + image processing
- Extensive format support
- Long track record

**Cons**:
- Commercial use requires registration
- Some capture modes require GUI interaction

**Status**: [VERIFIED]

## 2. Image Resize Tools

### ImageMagick

**License**: Apache 2.0 (open source)
**Platform**: Windows, Linux, macOS
**Size**: ~50MB

**CLI Commands**:
```cmd
# Simple resize
magick input.jpg -resize 1568x1568 output.jpg

# Resize with aspect ratio preservation
magick input.jpg -resize 1568x1568> output.jpg

# Resize by percentage
magick input.jpg -resize 50% output.jpg

# Resize with quality control
magick input.jpg -resize 1568x1568 -quality 85 output.jpg

# Batch resize (all JPGs in folder)
magick mogrify -resize 1568x1568 -quality 85 *.jpg

# Convert format + resize
magick input.png -resize 1024x768 output.jpg
```

**Pros**:
- Industry standard
- 200+ format support
- Extremely flexible
- Excellent documentation

**Cons**:
- Large installation
- Complex options can be overwhelming

**Status**: [VERIFIED]

### PowerToys Image Resizer

**License**: MIT (open source, Microsoft)
**Platform**: Windows only
**Size**: Part of PowerToys (~50MB total)

**CLI Commands**:
```cmd
# Resize with explicit dimensions
PowerToys.ImageResizerCLI.exe --width 800 --height 600 image.png

# Resize to output folder
PowerToys.ImageResizerCLI.exe --width 800 --height 600 -d "C:\Output" image.png

# Show current config
PowerToys.ImageResizerCLI.exe --show-config

# Use preset size
PowerToys.ImageResizerCLI.exe --size 0 -d "C:\Output" photo.png

# Preserve date modified
PowerToys.ImageResizerCLI.exe --width 800 --height 600 --keep-date-modified -d "C:\Output" image.png

# Set quality
PowerToys.ImageResizerCLI.exe --width 800 --height 600 --quality 85 image.png
```

**Pros**:
- Microsoft-supported
- Clean CLI interface
- Integrates with Windows shell
- Preset sizes

**Cons**:
- Requires full PowerToys installation
- Limited format support vs ImageMagick

**Status**: [VERIFIED]

### imgp

**License**: GPLv3 (open source)
**Platform**: Windows, Linux, macOS (Python)
**Size**: ~50KB + Pillow dependency

**CLI Commands**:
```bash
# Resize to specific resolution
imgp -x 1568x1568 input.jpg

# Resize by percentage
imgp -x 50% input.jpg

# Resize with quality
imgp -x 1568x1568 -q 85 input.jpg

# Batch resize recursively
imgp -x 1568x1568 -r /path/to/images/

# Optimize output
imgp -x 1568x1568 -O input.jpg

# Overwrite originals
imgp -x 1568x1568 -w input.jpg

# Convert PNG to JPEG
imgp -c input.png

# Erase EXIF metadata
imgp -e input.jpg
```

**Pros**:
- Very fast (Pillow-based)
- Adaptive resize mode
- Lightweight
- Good CLI ergonomics

**Cons**:
- Requires Python + Pillow
- JPEG/PNG only
- Less known than ImageMagick

**Status**: [VERIFIED]

### IrfanView (Resize)

**License**: Freeware
**Platform**: Windows only

**CLI Commands**:
```cmd
# Resize single file
i_view64.exe input.jpg /resize=(800,600) /convert=output.jpg

# Resize with aspect ratio
i_view64.exe input.jpg /resize=(800,600) /aspectratio /convert=output.jpg

# Resize with resampling (better quality)
i_view64.exe input.jpg /resize=(800,600) /aspectratio /resample /convert=output.jpg

# Resize long side
i_view64.exe input.jpg /resize_long=1568 /convert=output.jpg

# Batch resize
i_view64.exe c:\*.jpg /resize=(800,600) /aspectratio /resample /convert=c:\output\*.jpg

# Set JPEG quality
i_view64.exe input.jpg /resize=(800,600) /jpgq=85 /convert=output.jpg
```

**Pros**:
- Combined viewer/editor/converter
- Fast batch processing
- Many format options
- Silent mode available

**Cons**:
- Commercial use requires license
- Windows only

**Status**: [VERIFIED]

## 3. Combined Tools

### FFmpeg (Screenshot + Resize)

Can do both in one command:

```cmd
# Screenshot + resize in one step
ffmpeg -f gdigrab -framerate 1 -i desktop -frames:v 1 -vf "scale=1568:-1" output.jpg

# With quality control
ffmpeg -f gdigrab -framerate 1 -i desktop -frames:v 1 -vf "scale=1568:-1" -q:v 2 output.jpg
```

### IrfanView (Screenshot + Resize)

```cmd
# Capture + resize + save
i_view64.exe /capture=0 /resize=(1568,1568) /aspectratio /resample /convert=screenshot.jpg
```

## 4. Built-in Windows Options

### PowerShell (No External Dependencies)

**Screenshot** (already in use via `simple-screenshot.ps1`):
```powershell
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$screen = [System.Windows.Forms.Screen]::PrimaryScreen
$bitmap = New-Object System.Drawing.Bitmap($screen.Bounds.Width, $screen.Bounds.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screen.Bounds.Location, [System.Drawing.Point]::Empty, $screen.Bounds.Size)
$bitmap.Save("screenshot.png")
```

**Resize** (using .NET):
```powershell
Add-Type -AssemblyName System.Drawing

$img = [System.Drawing.Image]::FromFile("input.jpg")
$newWidth = 1568
$newHeight = [int]($img.Height * ($newWidth / $img.Width))
$bitmap = New-Object System.Drawing.Bitmap($newWidth, $newHeight)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$graphics.DrawImage($img, 0, 0, $newWidth, $newHeight)
$bitmap.Save("output.jpg", [System.Drawing.Imaging.ImageFormat]::Jpeg)
```

**Pros**:
- No external dependencies
- Full control over DPI handling
- Already proven in `simple-screenshot.ps1`

**Cons**:
- More verbose
- Slower than native tools
- Quality settings require more code

**Status**: [PROVEN] - already in use

## 5. Comparison Matrix

### Screenshot Tools

```
Tool          Size     Speed    DPI     Silent   Delay    Formats
-----------------------------------------------------------------
NirCmd        100KB    Fast     ?       Yes      No       PNG/JPG/BMP
Flameshot     40MB     Medium   Yes     Yes      Yes      PNG
ShareX        20MB     Medium   Yes     Partial  Yes      Many
FFmpeg        80MB     Medium   Yes     Yes      No       Any
IrfanView     3MB      Fast     Yes     Yes      No       Many
PowerShell    0        Medium   Yes     Yes      No       PNG/JPG/BMP
```

### Resize Tools

```
Tool              Size     Speed    Quality    Formats    Batch
---------------------------------------------------------------
ImageMagick       50MB     Fast     Excellent  200+       Yes
PowerToys         50MB     Medium   Good       Common     Yes
imgp              50KB+    Fast     Good       JPEG/PNG   Yes
IrfanView         3MB      Fast     Good       Many       Yes
FFmpeg            80MB     Medium   Good       Any        Yes
PowerShell        0        Slow     Good       Common     Script
```

## 6. Integration Considerations

### For LLM Computer Use Skill

**Current State**:
- `simple-screenshot.ps1` already handles DPI correctly using Win32 GetDeviceCaps
- JPEG output at physical resolution
- Works without external dependencies

**Recommended Additions**:

1. **Resize capability**: Add to existing PowerShell script using .NET
   - No new dependencies
   - Resize to max 1568px before API call
   - Control JPEG quality (85 recommended)

2. **Alternative for speed-critical use**: ImageMagick
   - Pre-installed on many dev machines
   - Single command: `magick input.jpg -resize 1568x1568> -quality 85 output.jpg`

3. **Portable option**: NirCmd + ImageMagick portable
   - ~100KB + ~50MB
   - No installation required

### Integration Pattern

```powershell
# Combined screenshot + resize for LLM Computer Use

# 1. Capture at full resolution
.\simple-screenshot.ps1 -OutputPath "temp_full.jpg"

# 2. Resize if needed (using ImageMagick if available, else .NET)
if (Get-Command magick -ErrorAction SilentlyContinue) {
    magick temp_full.jpg -resize "1568x1568>" -quality 85 screenshot.jpg
} else {
    # Fallback to .NET resize
    .\resize-image.ps1 -Input "temp_full.jpg" -MaxSize 1568 -Output "screenshot.jpg"
}
```

## 7. Sources

**Screenshot Tools**:
- https://nircmd.nirsoft.net/savescreenshot.html [NirCmd documentation]
- https://github.com/flameshot-org/flameshot [Flameshot GitHub]
- https://getsharex.com/docs/command-line-arguments [ShareX CLI docs]
- https://stackoverflow.com/questions/6766333/capture-windows-screen-with-ffmpeg [FFmpeg gdigrab]
- https://www.etcwiki.org/wiki/IrfanView_Command_Line_Options [IrfanView CLI]

**Resize Tools**:
- https://imagemagick.org/script/convert.php [ImageMagick convert]
- https://learn.microsoft.com/en-us/windows/powertoys/image-resizer [PowerToys Image Resizer]
- https://github.com/jarun/imgp [imgp GitHub]
- https://superuser.com/questions/315885/fast-batch-image-resizer [IrfanView batch resize]

**General**:
- https://recorder.easeus.com/screen-recording-tips/open-source-screenshot-tool.html [Open source overview]
- https://sourceforge.net/directory/screen-capture/ [SourceForge directory]

## 8. Document History

**[2026-01-27 19:35]**
- Fixed: Converted Markdown tables to lists per GLOBAL-RULES

**[2026-01-27 19:30]**
- Initial MCPI research completed
- Documented: 5 screenshot tools, 5 resize tools, 2 combined approaches
- Added integration recommendations for LLM Computer Use skill
