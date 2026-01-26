# Capture all model selector sections in one run
# Keeps selector open, scrolls and captures multiple screenshots

param(
    [string]$WindowTitle = "*Windsurf*",
    [string]$OutputFolder = "shots",
    [int]$FirstScrollCount = 4,      # DOWN keys for first scroll (visible model count)
    [int]$SubsequentScrollCount = 3, # DOWN keys for subsequent scrolls (visible - 1 for overlap detection)
    [int]$MaxSections = 25
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
if (Test-Path $OutputFolder) {
    Remove-Item "$OutputFolder/*" -Force -ErrorAction SilentlyContinue
} else {
    New-Item -ItemType Directory -Path $OutputFolder | Out-Null
}

$proc = Get-Process -Name "Windsurf" -ErrorAction SilentlyContinue |
    Where-Object { $_.MainWindowTitle -like $WindowTitle -and $_.MainWindowTitle -ne "" } |
    Select-Object -First 1

if (-not $proc) {
    Write-Error "No Windsurf window found"
    exit 1
}

[Win32]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 500

# Open model selector
[Win32]::SendCtrlShiftF9()
Start-Sleep -Milliseconds 400

# Navigate to show model list
[Win32]::SendKey([Win32]::VK_UP)
Start-Sleep -Milliseconds 100
[Win32]::SendKey([Win32]::VK_TAB)
Start-Sleep -Milliseconds 100
[Win32]::SendKey([Win32]::VK_SPACE)
Start-Sleep -Milliseconds 100
[Win32]::SendKey([Win32]::VK_DOWN)
Start-Sleep -Milliseconds 300

$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds

for ($section = 1; $section -le $MaxSections; $section++) {
    # Take screenshot
    $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen(0, 0, 0, 0, $screen.Size)
    $filename = Join-Path $OutputFolder ("section_{0:D2}.jpg" -f $section)
    $bitmap.Save($filename, [System.Drawing.Imaging.ImageFormat]::Jpeg)
    $graphics.Dispose()
    $bitmap.Dispose()
    
    Write-Host "Captured section $section"
    
    # Scroll down (first scroll uses FirstScrollCount, subsequent use SubsequentScrollCount)
    $scrollCount = if ($section -eq 1) { $FirstScrollCount } else { $SubsequentScrollCount }
    for ($i = 0; $i -lt $scrollCount; $i++) {
        [Win32]::SendKey([Win32]::VK_DOWN)
    }
    Start-Sleep -Milliseconds 150
}

# Close selector
[Win32]::SendKey([Win32]::VK_ESCAPE)

Write-Host "`nDone! Captured $MaxSections sections to: $OutputFolder"
Write-Host "Cascade will analyze screenshots to extract model names and costs."
