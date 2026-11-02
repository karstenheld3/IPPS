# LLM Tools Skill Setup

One setup for all `llm-tools` functions (shared call scripts, evaluation, transcription, computer-use). Run once to install Python dependencies in `[WORKSPACE_FOLDER]/../.tools/llm-venv/`.

## Prerequisites

- Python 3.10+
- OpenAI API key (GPT vision models, Whisper for audio)
- Anthropic API key (Claude models; required for computer-use)
- Windows (computer-use only)

## 1. Set Workspace Folder

```powershell
$workspaceFolder = (Get-Location).Path  # or set explicitly: $workspaceFolder = "C:\Projects\MyProject"
$toolsDir = "$workspaceFolder\..\.tools"
$venvDir = "$toolsDir\llm-venv"

# Create .tools folder if needed
if (-not (Test-Path $toolsDir)) { New-Item -ItemType Directory -Path $toolsDir }
```

## 2. Verify Python Installation

```powershell
python --version
```

Expected: Python 3.10+ installed and in PATH.
If not installed: Download from https://python.org

## 3. Create Virtual Environment

**Check if already exists:**
```powershell
Test-Path "$venvDir\Scripts\python.exe"
```

**If not exists, create:**
```powershell
python -m venv $venvDir
```

**Verify creation:**
```powershell
& "$venvDir\Scripts\python.exe" --version
```

## 4. Install Dependencies

**Core (all functions):**
```powershell
& "$venvDir\Scripts\pip.exe" install "openai==2.8.0" "anthropic>=0.18.0,<1.0.0" httpx
```

**Computer-use (optional, Windows):**
```powershell
& "$venvDir\Scripts\pip.exe" install mss pillow pyautogui
```

**Audio transcription (optional):** `ffmpeg` for format conversion
```powershell
winget install ffmpeg
```

**Verify packages:**
```powershell
& "$venvDir\Scripts\pip.exe" list | Select-String "openai|anthropic|httpx|mss|pillow|pyautogui"
```

## 5. Configure API Keys

**Standard location**: `[WORKSPACE_FOLDER]\..\.tools\.api-keys.txt` (shared across projects). Pass it to every script via `--keys-file`. Format, one key per line:
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

**Alternative**: `.env` file in your working directory (scripts default to `.env` when `--keys-file` is omitted):

```powershell
$envFile = Join-Path (Get-Location).Path ".env"
if (-not (Test-Path $envFile)) {
    $envContent = @"
# LLM API Keys
OPENAI_API_KEY=sk-proj-your-key-here
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

"@
    [System.IO.File]::WriteAllText($envFile, $envContent, (New-Object System.Text.UTF8Encoding $false))   # UTF-8 without BOM, as the Python scripts read it
    Write-Host "Created $envFile - edit with your API keys" -ForegroundColor Yellow
} else {
    Write-Host "$envFile already exists" -ForegroundColor Green
}
```

**IMPORTANT:** Add `.env` to `.gitignore`:
```powershell
$gitignore = Join-Path (Get-Location).Path ".gitignore"
if (Test-Path $gitignore) {
    $content = Get-Content -LiteralPath $gitignore -Raw -Encoding UTF8
    if ($content -notmatch "\.env") {
        [System.IO.File]::AppendAllText($gitignore, "`n# API Keys`n.env`n", (New-Object System.Text.UTF8Encoding $false))
        Write-Host "Added .env to .gitignore" -ForegroundColor Green
    }
}
```

## 6. Test API Connection

**Test OpenAI:**
```powershell
& "$venvDir\Scripts\python.exe" -c @"
import os
from openai import OpenAI
key = os.environ.get('OPENAI_API_KEY')
if not key:
    print('[FAIL] OPENAI_API_KEY not set - create .env file or set environment variable')
    exit(1)
client = OpenAI(api_key=key)
print('[OK] OpenAI client created successfully')
"@
```

**Test Anthropic:**
```powershell
& "$venvDir\Scripts\python.exe" -c @"
import os
from anthropic import Anthropic
key = os.environ.get('ANTHROPIC_API_KEY')
if not key:
    print('[FAIL] ANTHROPIC_API_KEY not set - create .env file or set environment variable')
    exit(1)
client = Anthropic(api_key=key)
print('[OK] Anthropic client created successfully')
"@
```

## 7. Running Scripts

Always use the venv Python:

```powershell
$skill = "[AGENT_FOLDER]\skills\llm-tools"
$keys = "$toolsDir\.api-keys.txt"

# Single call (shared)
& "$venvDir\Scripts\python.exe" "$skill\call-llm.py" --model gpt-4o --input-file image.jpg --prompt-file prompt.md --keys-file $keys

# Batch processing (shared)
& "$venvDir\Scripts\python.exe" "$skill\call-llm-batch.py" --model claude-opus-4-20250514 --input-folder images/ --output-folder out/ --prompt-file prompt.md --keys-file $keys

# Transcription
& "$venvDir\Scripts\python.exe" "$skill\transcription\transcribe-image-to-markdown.py" --input-file image.png --keys-file $keys
& "$venvDir\Scripts\python.exe" "$skill\transcription\transcribe-audio-to-markdown.py" --input recording.mp3 --output transcript.md --keys-file $keys

# Computer use (dry-run)
& "$venvDir\Scripts\python.exe" "$skill\computer-use\cli.py" -k $keys "Click the Start button"

# Self-test (no API calls)
& "$venvDir\Scripts\python.exe" "$skill\llm-tools-selftest.py" --skip-api-calls
```

## 8. Final Verification

```powershell
Write-Host "=== LLM Tools Setup Verification ===" -ForegroundColor Cyan

# Check venv
if (Test-Path "$venvDir\Scripts\python.exe") {
    Write-Host "[OK] Virtual environment: $venvDir" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Virtual environment not found" -ForegroundColor Red
}

# Check packages
$packages = & "$venvDir\Scripts\pip.exe" list 2>$null
if ($packages -match "openai") {
    Write-Host "[OK] openai package installed" -ForegroundColor Green
} else {
    Write-Host "[FAIL] openai package missing" -ForegroundColor Red
}
if ($packages -match "anthropic") {
    Write-Host "[OK] anthropic package installed" -ForegroundColor Green
} else {
    Write-Host "[FAIL] anthropic package missing" -ForegroundColor Red
}

# Check .env
if (Test-Path ".env") {
    Write-Host "[OK] .env file exists" -ForegroundColor Green
} else {
    Write-Host "[WARN] .env file not found - create with API keys" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setup complete. Run scripts with:" -ForegroundColor White
Write-Host "  & `"$venvDir\Scripts\python.exe`" <script.py> [args]" -ForegroundColor Gray
```

## 9. Cleanup (Optional)

Remove virtual environment to reinstall:
```powershell
Remove-Item $venvDir -Recurse -Force
```

## 10. Troubleshooting

### Virtual environment activation fails

**Error:** "running scripts is disabled on this system"

**Fix:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### pip install fails with SSL error

**Fix:** Use trusted host:
```powershell
& "$venvDir\Scripts\pip.exe" install --trusted-host pypi.org --trusted-host pypi.python.org openai anthropic
```

### API key not found

Pass `--keys-file` with the standard keys file, ensure `.env` is in the current working directory, or set environment variables:
```powershell
$env:OPENAI_API_KEY = "sk-proj-your-key"
$env:ANTHROPIC_API_KEY = "sk-ant-api03-your-key"
```

### Unsupported file format

Check supported formats in `transcription/TRANSCRIPTION.md`. For audio, ensure ffmpeg is installed.

### Rate limit exceeded

Wait and retry, or lower `--workers`. Use `find-workers-limit.py` to probe the provider limit.

## Completion

Setup complete:
- **Virtual environment**: `[WORKSPACE_FOLDER]/../.tools/llm-venv/` (shared by all llm-tools functions)
- **Python packages**: openai, anthropic, httpx (+ mss, pillow, pyautogui for computer-use)
- **API keys**: `[WORKSPACE_FOLDER]/../.tools/.api-keys.txt` or `.env` (user-created)

