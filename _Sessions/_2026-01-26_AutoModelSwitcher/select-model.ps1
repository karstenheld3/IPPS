# AutoModelSwitcher - Select specific model by query
# Opens model selector (Ctrl+/), types query, presses Enter

param(
    [Parameter(Mandatory = $true)]
    [string]$Query,

    [string]$WindowTitle = "*IPPS*",

    [int]$OpenDelayMs = 400,
    [int]$TypeDelayMs = 30,
    [int]$AfterEnterDelayMs = 300
)

Add-Type -AssemblyName System.Windows.Forms

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
    public const byte VK_RETURN = 0x0D;
    public const byte VK_ESCAPE = 0x1B;
    public const byte VK_DOWN = 0x28;
    public const uint KEYEVENTF_KEYUP = 0x0002;

    public static void SendCtrlShiftF9() {
        keybd_event(VK_CONTROL, 0, 0, UIntPtr.Zero);
        keybd_event(VK_SHIFT, 0, 0, UIntPtr.Zero);
        keybd_event(VK_F9, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(50);
        keybd_event(VK_F9, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        keybd_event(VK_SHIFT, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    }

    public static void SendDown() {
        keybd_event(VK_DOWN, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(30);
        keybd_event(VK_DOWN, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    }

    public static void SendEnter() {
        keybd_event(VK_RETURN, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(30);
        keybd_event(VK_RETURN, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    }

    public static void SendEscape() {
        keybd_event(VK_ESCAPE, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(30);
        keybd_event(VK_ESCAPE, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
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
Start-Sleep -Milliseconds 400

# NOTE: We intentionally do NOT try to focus Cascade via Ctrl+Shift+I.
# In Windsurf this triggers `windsurf.triggerCascade` and can open a new Cascade conversation/window.
# Ensure the Cascade panel is already focused before running this script.

# Close any open selector/menu first (best-effort)
[Win32]::SendEscape()
Start-Sleep -Milliseconds 120

# Open model selector (Ctrl+Shift+F9)
[Win32]::SendCtrlShiftF9()
Start-Sleep -Milliseconds $OpenDelayMs

# Type query (assumes selector focuses a textbox)
[System.Windows.Forms.SendKeys]::SendWait('^a')
Start-Sleep -Milliseconds 50
[System.Windows.Forms.SendKeys]::SendWait($Query)
Start-Sleep -Milliseconds 150

# Choose first match
[Win32]::SendDown()
Start-Sleep -Milliseconds 80
[Win32]::SendEnter()
Start-Sleep -Milliseconds $AfterEnterDelayMs

Write-Host "Done. Verify model indicator in Cascade UI."
