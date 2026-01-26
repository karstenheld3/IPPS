# Windsurf Auto Model Switcher - Optimized selector capture
# 1. Opens selector and takes initial screenshot to locate popup
# 2. Crops to model list area only
# 3. Scrolls and captures cropped screenshots

param(
    [string]$WindowTitle = "*Windsurf*",
    [string]$OutputFolder = "selector-optimized",
    [int]$SectionsToCapture = 10
)

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

# Create output folder
if (-not (Test-Path $OutputFolder)) {
    New-Item -ItemType Directory -Path $OutputFolder | Out-Null
}

# Find Windsurf window
$proc = Get-Process -Name "Windsurf" -ErrorAction SilentlyContinue |
    Where-Object { $_.MainWindowTitle -like $WindowTitle -and $_.MainWindowTitle -ne "" } |
    Select-Object -First 1

if (-not $proc) {
    Write-Error "No Windsurf window found matching: $WindowTitle"
    exit 1
}

Write-Host "Focusing: $($proc.MainWindowTitle)"
[Win32]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 500

# Open model selector
Write-Host "Opening model selector..."
[Win32]::SendCtrlShiftF9()
Start-Sleep -Milliseconds 400

# Navigate to first model
Write-Host "Navigating to first model..."
[Win32]::SendKey([Win32]::VK_UP)
Start-Sleep -Milliseconds 100
[Win32]::SendKey([Win32]::VK_TAB)
Start-Sleep -Milliseconds 100
[Win32]::SendKey([Win32]::VK_SPACE)
Start-Sleep -Milliseconds 100
[Win32]::SendKey([Win32]::VK_DOWN)
Start-Sleep -Milliseconds 200

# Take initial full screenshot to locate popup
Write-Host "Taking initial screenshot to locate popup..."
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$fullBitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
$graphics = [System.Drawing.Graphics]::FromImage($fullBitmap)
$graphics.CopyFromScreen(0, 0, 0, 0, $screen.Size)
$fullBitmap.Save((Join-Path $OutputFolder "initial_full.png"), [System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose()
$fullBitmap.Dispose()

Write-Host "Saved initial_full.png - analyze this to determine popup position"
Write-Host ""
Write-Host "MANUAL STEP REQUIRED:"
Write-Host "1. Open initial_full.png"
Write-Host "2. Note the X, Y, Width, Height of the model selector popup"
Write-Host "3. Update this script with those values"
Write-Host "4. Re-run to capture cropped screenshots"
Write-Host ""
Write-Host "Example crop values (adjust based on your screen):"
Write-Host '  $cropX = 700'
Write-Host '  $cropY = 100'
Write-Host '  $cropWidth = 300'
Write-Host '  $cropHeight = 500'

# Close selector
[Win32]::SendKey([Win32]::VK_ESCAPE)

Write-Host "`nInitial screenshot saved to: $OutputFolder/initial_full.png"
