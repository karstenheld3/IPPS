# AutoModelSwitcher - Proof of Concept
# Switches to next model in Windsurf Cascade using keyboard simulation

param(
    [string]$WindowTitle = "*Windsurf*",
    [int]$CycleCount = 1
)

Add-Type -AssemblyName System.Windows.Forms

Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
}
"@

# Find Windsurf window
$proc = Get-Process -Name "Windsurf" -ErrorAction SilentlyContinue | 
    Where-Object { $_.MainWindowTitle -like $WindowTitle -and $_.MainWindowTitle -ne "" } | 
    Select-Object -First 1

if (-not $proc) {
    Write-Error "No Windsurf window found matching: $WindowTitle"
    exit 1
}

Write-Host "Found: $($proc.MainWindowTitle) (PID: $($proc.Id))"

# Save current foreground window
$originalWindow = [Win32]::GetForegroundWindow()

# Focus Windsurf and send keystrokes
[Win32]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 300

# First, focus Cascade panel with Ctrl+L
[System.Windows.Forms.SendKeys]::SendWait("^l")
Write-Host "Sent Ctrl+L to focus Cascade"
Start-Sleep -Milliseconds 500

for ($i = 0; $i -lt $CycleCount; $i++) {
    # Ctrl+Shift+/ = Switch to next model
    [System.Windows.Forms.SendKeys]::SendWait("^+/")
    Write-Host "Sent model switch command ($($i + 1)/$CycleCount)"
    Start-Sleep -Milliseconds 500
}

# Restore original window focus
if ($originalWindow -ne [IntPtr]::Zero) {
    [Win32]::SetForegroundWindow($originalWindow) | Out-Null
}

Write-Host "Done. Model should have cycled $CycleCount time(s)."
