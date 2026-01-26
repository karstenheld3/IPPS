# Step 3: Close the model selector
# Called when discovery is complete

Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
    public const byte VK_ESCAPE = 0x1B;
    public const uint KEYEVENTF_KEYUP = 0x0002;

    public static void SendEscape() {
        keybd_event(VK_ESCAPE, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(30);
        keybd_event(VK_ESCAPE, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    }
}
"@

[Win32]::SendEscape()
Write-Host "Model selector closed"
