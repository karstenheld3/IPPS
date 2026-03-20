# LLM Evaluation Skill Uninstall

Remove LLM Evaluation Skill from your workspace.

## Quick Uninstall

Run this script and answer with a single character:

```powershell
# === LLM Evaluation Skill Uninstall ===

$workspaceFolder = (Get-Location).Path
$venvDir = "$workspaceFolder\..\.tools\llm-venv"
$envFile = "$workspaceFolder\.env"
$toolsDir = "$workspaceFolder\..\.tools"

$hasVenv = Test-Path $venvDir
$hasEnv = Test-Path $envFile
$hasToolsDir = Test-Path $toolsDir

$venvSize = 0
if ($hasVenv) {
    $venvSize = [math]::Round((Get-ChildItem $venvDir -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB, 0)
}

Write-Host "`n=== LLM Evaluation Skill Uninstall ===" -ForegroundColor Cyan
Write-Host "`nWorkspace: $workspaceFolder" -ForegroundColor White
Write-Host "`nCurrent state:" -ForegroundColor White
Write-Host "  [V] Virtual environment: $(if ($hasVenv) { "Found ($venvSize MB)" } else { 'Not found' })" -ForegroundColor $(if ($hasVenv) { 'Yellow' } else { 'Gray' })
Write-Host "  [E] API keys (.env):     $(if ($hasEnv) { 'Found' } else { 'Not found' })" -ForegroundColor $(if ($hasEnv) { 'Yellow' } else { 'Gray' })
Write-Host "`nOptions:" -ForegroundColor White
Write-Host "  1 = Minimal: Virtual environment only" -ForegroundColor White
Write-Host "  2 = Complete: Virtual environment + .env file" -ForegroundColor White
Write-Host "  Q = Quit (no changes)" -ForegroundColor White

$choice = Read-Host "`nWhat to remove? [1/2/Q]"
$validChoices = @('1', '2', 'Q', 'q')
if ($choice -notin $validChoices) {
    Write-Host "Invalid choice: '$choice'. Please enter 1, 2, or Q" -ForegroundColor Red
    return
}
if ($choice -eq 'Q' -or $choice -eq 'q') {
    Write-Host "Cancelled. No changes made." -ForegroundColor Yellow
    return
}

$removeVenv = $choice -in @('1', '2')
$removeEnv = $choice -eq '2'

Write-Host ""

if ($removeVenv -and $hasVenv) {
    try {
        $pythonProcs = Get-Process python*, python -ErrorAction SilentlyContinue | Where-Object {
            $_.Path -like "*$venvDir*"
        }
        if ($pythonProcs) {
            Write-Host "[V] Warning: Python processes running from venv" -ForegroundColor Yellow
            $pythonProcs | ForEach-Object { Write-Host "    PID $($_.Id): $($_.Path)" -ForegroundColor Yellow }
        }
        Remove-Item $venvDir -Recurse -Force -ErrorAction Stop
        Write-Host "[V] Removed virtual environment ($venvSize MB)" -ForegroundColor Green
        if ($hasToolsDir) {
            $remaining = Get-ChildItem $toolsDir -ErrorAction SilentlyContinue
            if (-not $remaining) {
                Remove-Item $toolsDir -Force -ErrorAction SilentlyContinue
                Write-Host "[V] Removed empty .tools folder" -ForegroundColor Green
            }
        }
    } catch {
        Write-Host "[V] Failed: Close any running scripts and delete manually: $venvDir" -ForegroundColor Red
    }
} elseif ($removeVenv) {
    Write-Host "[V] Virtual environment already removed" -ForegroundColor Gray
}

if ($removeEnv -and $hasEnv) {
    try {
        $backupPath = "$envFile.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Copy-Item $envFile $backupPath -ErrorAction Stop
        Remove-Item $envFile -Force -ErrorAction Stop
        Write-Host "[E] Removed .env file (backup: $backupPath)" -ForegroundColor Green
    } catch {
        Write-Host "[E] Failed to remove .env: $_" -ForegroundColor Red
    }
} elseif ($removeEnv) {
    Write-Host "[E] .env file already removed" -ForegroundColor Gray
}

Write-Host "`n=== Done ===" -ForegroundColor Cyan
Write-Host "Note: Skill files in .windsurf/skills/llm-evaluation/ are not removed." -ForegroundColor White
Write-Host "To completely remove the skill, delete that folder manually." -ForegroundColor White
```

## What Gets Removed

- **Option 1 (Minimal)** - Virtual environment only
- **Option 2 (Complete)** - Virtual environment + .env file

**Components:**
- **Virtual environment**: `../.tools/llm-venv/` (~100-200 MB). Contains openai, anthropic. Recreatable via SETUP.md.
- **.env file**: API keys at workspace root (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`). **Warning**: Backup created before removal.

## What Is NOT Removed

- Skill files: `.windsurf/skills/llm-evaluation/`
- Test outputs and `_token_usage__*.json` files

Complete removal after uninstall:
```powershell
Remove-Item ".windsurf\skills\llm-evaluation" -Recurse -Force
```

## Reinstalling

1. Run SETUP.md to create virtual environment
2. Create new .env file with API keys
3. Test: `python call-llm.py --help`