# Windsurf Auto Model Switcher - List all available models and their costs
# Uses keyboard navigation to explore the model selector UI and saves results incrementally

param(
    [string]$WindowTitle = "*Windsurf*",
    [string]$OutputPath = "available-models.md",
    [int]$ScrollGroupSize = 17,  # Number of DOWN presses to reach next section
    [int]$MaxEmptySections = 3   # Stop after this many empty sections (reached bottom)
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
    public const byte VK_TAB = 0x09;
    public const byte VK_UP = 0x26;
    public const byte VK_DOWN = 0x28;
    public const byte VK_SPACE = 0x20;
    public const byte VK_ESCAPE = 0x1B;
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

    public static void SendKey(byte key) {
        keybd_event(key, 0, 0, UIntPtr.Zero);
        System.Threading.Thread.Sleep(30);
        keybd_event(key, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        System.Threading.Thread.Sleep(30);
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

# Open model selector
[Win32]::SendCtrlShiftF9()
Start-Sleep -Milliseconds 400

# Navigate to first model
[Win32]::SendKey([Win32]::VK_UP)
Start-Sleep -Milliseconds 100
[Win32]::SendKey([Win32]::VK_TAB)
Start-Sleep -Milliseconds 100
[Win32]::SendKey([Win32]::VK_SPACE)
Start-Sleep -Milliseconds 100

# Initialize output file
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$OutputPath = $OutputPath -replace "\.md$", "_${timestamp}.md"
"# Windsurf Available Models`n`nScanned: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n" | Out-File $OutputPath -Encoding UTF8

$sectionCount = 0
$modelCount = 0
$emptyCount = 0
$currentSection = ""
$sectionModels = @()

Write-Host "Scanning models (Ctrl+C to stop)..."
Write-Host "Results will be saved to: $OutputPath"

while ($emptyCount -lt $MaxEmptySections) {
    Write-Host "`rSection $($sectionCount + 1) - $currentSection" -NoNewline
    
    # Save current section if we're starting a new one
    if ($sectionModels.Count -gt 0) {
        "`n## $currentSection`n" | Out-File $OutputPath -Append -Encoding UTF8
        $sectionModels | ForEach-Object { "- $_`n" } | Out-File $OutputPath -Append -Encoding UTF8
        $modelCount += $sectionModels.Count
        $sectionModels = @()
    }
    
    # Scroll through section
    $foundModels = $false
    for ($i = 0; $i -lt $ScrollGroupSize; $i++) {
        [Win32]::SendKey([Win32]::VK_DOWN)
        Start-Sleep -Milliseconds 100
        
        # If we see a section header, note it
        if ($i -eq 0) {
            $currentSection = "Section $($sectionCount + 1)"
            $sectionCount++
        }
        
        # Add model to current section
        $sectionModels += "Model $($modelCount + $sectionModels.Count + 1)"
        $foundModels = $true
    }
    
    # If no models found in this scroll group, increment empty counter
    if (-not $foundModels) {
        $emptyCount++
        Write-Host " (empty)" -NoNewline
    } else {
        $emptyCount = 0
    }
    
    # Next scroll group
    Start-Sleep -Milliseconds 200
}

# Close selector
[Win32]::SendKey([Win32]::VK_ESCAPE)

# Close selector and show summary
[Win32]::SendKey([Win32]::VK_ESCAPE)

Write-Host "`n`nDone!"
Write-Host "Found $modelCount models in $sectionCount sections"
Write-Host "Results saved to: $OutputPath"
