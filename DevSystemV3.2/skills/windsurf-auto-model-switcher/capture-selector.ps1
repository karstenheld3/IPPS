# Windsurf Auto Model Switcher - Capture model selector screenshots
# Opens selector UI and captures screenshots while scrolling through sections

param(
    [string]$WindowTitle = "*Windsurf*",
    [string]$OutputFolder = "selector-screenshots",
    [int]$SectionsToCapture = 10,  # Number of sections to scroll through
    [int]$DownKeysPerSection = 17  # Keys to press to reach next section
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

# Navigate to first model: UP > TAB > SPACE > DOWN
Write-Host "Navigating to first model..."
[Win32]::SendKey([Win32]::VK_UP)
Start-Sleep -Milliseconds 100
[Win32]::SendKey([Win32]::VK_TAB)
Start-Sleep -Milliseconds 100
[Win32]::SendKey([Win32]::VK_SPACE)
Start-Sleep -Milliseconds 100
[Win32]::SendKey([Win32]::VK_DOWN)
Start-Sleep -Milliseconds 200

Write-Host "Capturing $SectionsToCapture sections..."

for ($section = 1; $section -le $SectionsToCapture; $section++) {
    # Take screenshot
    $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen(0, 0, 0, 0, $screen.Size)
    
    $filename = Join-Path $OutputFolder ("section_{0:D2}.png" -f $section)
    $bitmap.Save($filename, [System.Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose()
    $bitmap.Dispose()
    
    Write-Host "Captured section $section/$SectionsToCapture"
    
    # Scroll down to next section
    for ($i = 0; $i -lt $DownKeysPerSection; $i++) {
        [Win32]::SendKey([Win32]::VK_DOWN)
        Start-Sleep -Milliseconds 50
    }
    Start-Sleep -Milliseconds 200
}

# Close selector
[Win32]::SendKey([Win32]::VK_ESCAPE)

Write-Host "`nDone! Screenshots saved to: $OutputFolder"
Write-Host "Use Cascade to analyze screenshots and extract model names + costs."
