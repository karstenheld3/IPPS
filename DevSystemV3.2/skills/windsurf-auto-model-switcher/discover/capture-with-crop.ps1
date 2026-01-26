# Two-phase model discovery:
# Phase 1: Fullscreen screenshot to detect popup position (Cascade analyzes)
# Phase 2: Cropped screenshots of popup area only

param(
    [string]$WindowTitle = "*Windsurf*",
    [string]$OutputFolder = "",    # Default: [WORKSPACE]/.tools/_screenshots/YYYY-MM-DD_HH-MM-SS
    [switch]$Phase1Only,           # Only take initial fullscreen shot
    [int]$CropX = 0,               # Popup X position (from Phase 1 analysis)
    [int]$CropY = 0,               # Popup Y position
    [int]$CropWidth = 0,           # Popup width
    [int]$CropHeight = 0,          # Popup height
    [int]$FirstScrollCount = 16,
    [int]$SubsequentScrollCount = 7,
    [int]$MaxSections = 10
)

# Default output folder if not specified
if (-not $OutputFolder) {
    $workspaceRoot = (Get-Item $PSScriptRoot).Parent.Parent.Parent.Parent.FullName
    $OutputFolder = Join-Path $workspaceRoot ".tools\_screenshots"
}

# Timestamp prefix for filenames
$filePrefix = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
    public const byte VK_CONTROL = 0x11;
    public const byte VK_SHIFT = 0x10;
    public const byte VK_F9 = 0x78;
    public const byte VK_UP = 0x26;
    public const byte VK_DOWN = 0x28;
    public const byte VK_TAB = 0x09;
    public const byte VK_SPACE = 0x20;
    public const byte VK_ESCAPE = 0x1B;
    public const uint KEYEVENTF_KEYUP = 0x0002;

    public static void SendKey(byte key) {
        keybd_event(key, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(30);
        keybd_event(key, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        System.Threading.Thread.Sleep(30);
    }
    public static void SendCtrlShiftF9() {
        keybd_event(VK_CONTROL, 0, 0, UIntPtr.Zero);
        keybd_event(VK_SHIFT, 0, 0, UIntPtr.Zero);
        keybd_event(VK_F9, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(50);
        keybd_event(VK_F9, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        keybd_event(VK_SHIFT, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    }
}
"@

if (-not (Test-Path $OutputFolder)) {
    New-Item -ItemType Directory -Path $OutputFolder | Out-Null
}

$proc = Get-Process -Name "Windsurf" -ErrorAction SilentlyContinue |
    Where-Object { $_.MainWindowTitle -like $WindowTitle -and $_.MainWindowTitle -ne "" } |
    Select-Object -First 1

if (-not $proc) { Write-Error "No Windsurf window found"; exit 1 }

[Win32]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 500

# Open model selector
[Win32]::SendCtrlShiftF9()
Start-Sleep -Milliseconds 400

# Navigate to model list
[Win32]::SendKey([Win32]::VK_UP)
Start-Sleep -Milliseconds 100
[Win32]::SendKey([Win32]::VK_TAB)
Start-Sleep -Milliseconds 100
[Win32]::SendKey([Win32]::VK_SPACE)
Start-Sleep -Milliseconds 100
[Win32]::SendKey([Win32]::VK_DOWN)
Start-Sleep -Milliseconds 300

$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds

if ($Phase1Only) {
    # PHASE 1: Fullscreen screenshot for Cascade to analyze
    $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen(0, 0, 0, 0, $screen.Size)
    $filename = Join-Path $OutputFolder "${filePrefix}_phase1_fullscreen.jpg"
    $bitmap.Save($filename, [System.Drawing.Imaging.ImageFormat]::Jpeg)
    $graphics.Dispose()
    $bitmap.Dispose()
    
    [Win32]::SendKey([Win32]::VK_ESCAPE)
    
    Write-Host "Phase 1 complete: $filename"
    Write-Host ""
    Write-Host "Cascade: Analyze this screenshot and return popup coordinates:"
    Write-Host '  { "x": NNN, "y": NNN, "width": NNN, "height": NNN }'
    Write-Host ""
    Write-Host "Then run Phase 2:"
    Write-Host '  .\capture-with-crop.ps1 -CropX NNN -CropY NNN -CropWidth NNN -CropHeight NNN'
    exit 0
}

# PHASE 2: Cropped screenshots
if ($CropWidth -eq 0 -or $CropHeight -eq 0) {
    Write-Error "Phase 2 requires -CropX, -CropY, -CropWidth, -CropHeight from Phase 1 analysis"
    [Win32]::SendKey([Win32]::VK_ESCAPE)
    exit 1
}

Write-Host "Capturing $MaxSections sections, cropped to ${CropWidth}x${CropHeight} at ($CropX, $CropY)"

for ($section = 1; $section -le $MaxSections; $section++) {
    # Capture cropped area only
    $bitmap = New-Object System.Drawing.Bitmap($CropWidth, $CropHeight)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen($CropX, $CropY, 0, 0, (New-Object System.Drawing.Size($CropWidth, $CropHeight)))
    $filename = Join-Path $OutputFolder ("${filePrefix}_section_{0:D2}.jpg" -f $section)
    $bitmap.Save($filename, [System.Drawing.Imaging.ImageFormat]::Jpeg)
    $graphics.Dispose()
    $bitmap.Dispose()
    
    Write-Host "Captured section $section"
    
    # Scroll
    $scrollCount = if ($section -eq 1) { $FirstScrollCount } else { $SubsequentScrollCount }
    for ($i = 0; $i -lt $scrollCount; $i++) {
        [Win32]::SendKey([Win32]::VK_DOWN)
    }
    Start-Sleep -Milliseconds 150
}

[Win32]::SendKey([Win32]::VK_ESCAPE)
Write-Host "`nDone! Screenshots saved to: $OutputFolder"
Write-Host "Cascade: Read screenshots, extract models, then delete folder."
