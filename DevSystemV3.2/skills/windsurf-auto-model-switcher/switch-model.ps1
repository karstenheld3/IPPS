# Windsurf Auto Model Switcher - Cycle to next model
# Sends Ctrl+Shift+F10 (custom keybinding) or Ctrl+Shift+/ (default)

param(
    [string]$WindowTitle = "*Windsurf*",
    [int]$CycleCount = 1,
    [switch]$UseDefault  # Use default Ctrl+Shift+/ instead of custom F10
)

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
    public const byte VK_F10 = 0x79;
    public const byte VK_OEM_2 = 0xBF;  // / key
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

    public static void SendCtrlShiftSlash() {
        keybd_event(VK_CONTROL, 0, 0, UIntPtr.Zero);
        keybd_event(VK_SHIFT, 0, 0, UIntPtr.Zero);
        keybd_event(VK_OEM_2, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(50);
        keybd_event(VK_OEM_2, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        keybd_event(VK_SHIFT, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    }
}
"@

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

for ($i = 0; $i -lt $CycleCount; $i++) {
    if ($UseDefault) {
        [Win32]::SendCtrlShiftSlash()
        Write-Host "Sent Ctrl+Shift+/ ($($i + 1)/$CycleCount)"
    } else {
        [Win32]::SendCtrlShiftF10()
        Write-Host "Sent Ctrl+Shift+F10 ($($i + 1)/$CycleCount)"
    }
    Start-Sleep -Milliseconds 300
}

Write-Host "Done - check model indicator"
