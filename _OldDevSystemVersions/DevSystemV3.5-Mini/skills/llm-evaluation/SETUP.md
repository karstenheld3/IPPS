# LLM Evaluation Skill Setup

Install Python dependencies in `[WORKSPACE_FOLDER]/../.tools/llm-venv/`.

## 1. Set Workspace Folder

```powershell
$workspaceFolder = (Get-Location).Path
$toolsDir = "$workspaceFolder\..\.tools"
$venvDir = "$toolsDir\llm-venv"
if (-not (Test-Path $toolsDir)) { New-Item -ItemType Directory -Path $toolsDir }
```

## 2. Create Virtual Environment

Requires Python 3.10+.

```powershell
python -m venv $venvDir
```

## 3. Install Dependencies

```powershell
& "$venvDir\Scripts\pip.exe" install "openai==2.8.0" "anthropic>=0.18.0,<1.0.0"
```

## 4. Configure API Keys

Create `.env` in working directory (or use `--keys-file` parameter):

```
OPENAI_API_KEY=sk-proj-your-key-here
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

IMPORTANT: Add `.env` to `.gitignore`.

## 5. Running Scripts

```powershell
& "$venvDir\Scripts\python.exe" call-llm.py --model gpt-4o --input-file image.jpg --prompt-file prompt.md
```

## 6. Verify Setup

```powershell
& "$venvDir\Scripts\python.exe" --version
& "$venvDir\Scripts\pip.exe" list | Select-String "openai|anthropic"
Test-Path ".env"
```

## 7. Cleanup (Optional)

```powershell
Remove-Item $venvDir -Recurse -Force
```

## Troubleshooting

### Activation fails: "running scripts is disabled"

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### pip SSL error

```powershell
& "$venvDir\Scripts\pip.exe" install --trusted-host pypi.org --trusted-host pypi.python.org openai anthropic
```

### API key not found

Ensure `.env` is in current working directory, or set env vars directly:
```powershell
$env:OPENAI_API_KEY = "sk-proj-your-key"
$env:ANTHROPIC_API_KEY = "sk-ant-api03-your-key"
```