# Windsurf Auto Model Switcher - Capture model screenshots for cost discovery
# Cycles through models and takes screenshots of each

param(
    [string]$WindowTitle = "*Windsurf*",
    [string]$OutputFolder = "model-screenshots",
    [int]$CycleCount = 85,  # Number of models to capture (slightly more than 81 to be safe)
    [int]$DelayMs = 800     # Delay between cycles for UI to update
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
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
    
    public struct RECT {
        public int Left;
        public int Top;
        public int Right;
        public int Bottom;
    }

    public const byte VK_CONTROL = 0x11;
    public const byte VK_SHIFT = 0x10;
    public const byte VK_F10 = 0x79;
    public const uint KEYEVENTF_KEYUP = 0x0002;

    public static void SendCtrlShiftF10() {
        keybd_event(VK_CONTROL, 0, 0, UIntPtr.Zero);
        keybd_event(VK_SHIFT, 0, 0, UIntPtr.Zero);
        keybd_event(VK_F10, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(50);
        keybd_event(VK_F10, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
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

Write-Host "Capturing $CycleCount models to: $OutputFolder"
Write-Host "Press Ctrl+C to stop early"

for ($i = 1; $i -le $CycleCount; $i++) {
    # Cycle to next model first
    [Win32]::SendCtrlShiftF10()
    Start-Sleep -Milliseconds $DelayMs
    
    # Take full screen screenshot
    $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen(0, 0, 0, 0, $screen.Size)
    
    $filename = Join-Path $OutputFolder ("model_{0:D3}.png" -f $i)
    $bitmap.Save($filename, [System.Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose()
    $bitmap.Dispose()
    
    Write-Host "`rCaptured $i/$CycleCount" -NoNewline
}

Write-Host "`n`nDone! Screenshots saved to: $OutputFolder"
Write-Host "Analyze screenshots to extract model names and costs."
