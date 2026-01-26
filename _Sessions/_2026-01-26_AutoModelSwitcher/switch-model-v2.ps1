# AutoModelSwitcher v2 - Using keybd_event instead of SendKeys
# More reliable for Electron apps

param(
    [string]$WindowTitle = "*Windsurf*",
    [int]$CycleCount = 1
)

Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")]
    public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
    
    public const byte VK_CONTROL = 0x11;
    public const byte VK_SHIFT = 0x10;
    public const byte VK_OEM_2 = 0xBF;  // / key
    public const byte VK_L = 0x4C;
    public const uint KEYEVENTF_KEYUP = 0x0002;
    
    public static void SendCtrlL() {
        keybd_event(VK_CONTROL, 0, 0, UIntPtr.Zero);
        keybd_event(VK_L, 0, 0, UIntPtr.Zero);
        keybd_event(VK_L, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    }
    
    public static void SendCtrlShiftSlash() {
        keybd_event(VK_CONTROL, 0, 0, UIntPtr.Zero);
        keybd_event(VK_SHIFT, 0, 0, UIntPtr.Zero);
        keybd_event(VK_OEM_2, 0, 0, UIntPtr.Zero);
        keybd_event(VK_OEM_2, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        keybd_event(VK_SHIFT, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    }
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

# Focus Windsurf
[Win32]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 300

# Focus Cascade panel with Ctrl+L
[Win32]::SendCtrlL()
Write-Host "Sent Ctrl+L to focus Cascade"
Start-Sleep -Milliseconds 500

for ($i = 0; $i -lt $CycleCount; $i++) {
    # Ctrl+Shift+/ = Switch to next model
    [Win32]::SendCtrlShiftSlash()
    Write-Host "Sent Ctrl+Shift+/ ($($i + 1)/$CycleCount)"
    Start-Sleep -Milliseconds 500
}

# Restore original window focus
if ($originalWindow -ne [IntPtr]::Zero) {
    Start-Sleep -Milliseconds 200
    [Win32]::SetForegroundWindow($originalWindow) | Out-Null
}

Write-Host "Done."
