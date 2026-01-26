# Windsurf Auto Model Switcher - List all available models and their costs
# Uses keyboard navigation to explore the model selector UI

param(
    [string]$WindowTitle = "*Windsurf*",
    [int]$ScrollGroupSize = 17,  # Number of DOWN presses to reach next section
    [switch]$SaveToFile
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

$models = @()
$currentSection = ""
$sectionCount = 0
$modelCount = 0

# Keep scrolling until we see a model we've already seen (indicates we're at the end)
$seenModels = @{}
$duplicateFound = $false

while (-not $duplicateFound) {
    # Read current line from clipboard
    [System.Windows.Forms.SendKeys]::SendWait("^c")
    Start-Sleep -Milliseconds 100
    $line = [System.Windows.Forms.Clipboard]::GetText()
    
    if ($line -match "^=== (.+) ===$") {
        $currentSection = $matches[1]
        $sectionCount++
    }
    elseif ($line -match "^(.+?)\s+(\d+(?:\.\d+)?x|Free)$") {
        $modelName = $matches[1].Trim()
        $cost = $matches[2]
        
        if ($seenModels.ContainsKey($modelName)) {
            $duplicateFound = $true
            break
        }
        
        $seenModels[$modelName] = $true
        $models += [PSCustomObject]@{
            Section = $currentSection
            Name = $modelName
            Cost = $cost
        }
        $modelCount++
    }
    
    # Scroll down (by group size after each section)
    if ($modelCount % $ScrollGroupSize -eq 0) {
        for ($i = 0; $i -lt $ScrollGroupSize; $i++) {
            [Win32]::SendKey([Win32]::VK_DOWN)
        }
        Start-Sleep -Milliseconds 200
    }
    else {
        [Win32]::SendKey([Win32]::VK_DOWN)
        Start-Sleep -Milliseconds 50
    }
}

# Close selector
[Win32]::SendKey([Win32]::VK_ESCAPE)

# Format output
$output = "# Windsurf Available Models`n`n"
$currentSection = ""

foreach ($model in $models) {
    if ($model.Section -ne $currentSection) {
        $output += "`n## $($model.Section)`n`n"
        $currentSection = $model.Section
    }
    $output += "- $($model.Name) - $($model.Cost)`n"
}

$output += "`n**Total**: $modelCount models in $sectionCount sections`n"

if ($SaveToFile) {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $outputPath = "available-models_$timestamp.md"
    $output | Out-File $outputPath -Encoding UTF8
    Write-Host "Models saved to: $outputPath"
}
else {
    Write-Host $output
}
