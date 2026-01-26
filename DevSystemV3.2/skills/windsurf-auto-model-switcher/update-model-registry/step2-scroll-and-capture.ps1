# Step 2: Scroll down N times and take screenshot
# Called by Cascade after analyzing previous screenshot

param(
    [int]$ScrollCount = 5,
    [string]$OutputPath = "screenshot.png"
)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
    public const byte VK_DOWN = 0x28;
    public const uint KEYEVENTF_KEYUP = 0x0002;

    public static void SendDown() {
        keybd_event(VK_DOWN, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(30);
        keybd_event(VK_DOWN, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        System.Threading.Thread.Sleep(50);
    }
}
"@

# Scroll down
for ($i = 0; $i -lt $ScrollCount; $i++) {
    [Win32]::SendDown()
}
Start-Sleep -Milliseconds 200

# Take screenshot
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen(0, 0, 0, 0, $screen.Size)
$bitmap.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose()
$bitmap.Dispose()

Write-Host "Scrolled $ScrollCount times, screenshot saved to: $OutputPath"
