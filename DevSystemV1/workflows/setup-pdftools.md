---
description: Setup development tools (Python, Poppler, uv)
auto_execution_mode: 1
---

# Setup Development Tools

Run this workflow once to prepare the development environment.

## 1. Set Workspace Folder

```powershell
$workspaceFolder = (Get-Location).Path  # or set explicitly: $workspaceFolder = "E:\Dev\MyProject"
$toolsDir = "$workspaceFolder\.tools"
```

## 2. Verify Python Installation

```powershell
python --version
```

Expected: Python 3.10+ installed and in PATH.
If not installed: Ask user to install Python from https://python.org

## 3. Install Poppler Locally

Poppler provides `pdftoppm` for converting PDF pages to images.

### Check if already installed:
```powershell
Test-Path "$toolsDir\poppler\Library\bin\pdftoppm.exe"
```

### If not installed, download and extract:
```powershell
$popplerDir = "$toolsDir\poppler"

# Create .tools folder if needed
if (-not (Test-Path $toolsDir)) { New-Item -ItemType Directory -Path $toolsDir }

# Download latest Poppler for Windows
$popplerUrl = "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip"
$zipPath = "$toolsDir\poppler.zip"

Invoke-WebRequest -Uri $popplerUrl -OutFile $zipPath
Expand-Archive -Path $zipPath -DestinationPath $toolsDir -Force

# Find extracted folder (poppler-*) and rename to poppler
$extractedFolder = Get-ChildItem $toolsDir -Directory | Where-Object { $_.Name -like "poppler-*" } | Select-Object -First 1
if ($extractedFolder) { Move-Item $extractedFolder.FullName $popplerDir -ErrorAction SilentlyContinue }

Remove-Item $zipPath -ErrorAction SilentlyContinue
```

### Verify installation:
```powershell
& "$toolsDir\poppler\Library\bin\pdftoppm.exe" -v
```

### Create output folder (tracked in git):
```powershell
$jpgDir = "$toolsDir\poppler_pdf_jpgs"
if (-not (Test-Path $jpgDir)) { New-Item -ItemType Directory -Path $jpgDir }
if (-not (Test-Path "$jpgDir\.gitkeep")) { New-Item -ItemType File -Path "$jpgDir\.gitkeep" }
```

## 4. Install uv/uvx (Python Package Runner)

uvx runs Python packages without installing them globally. Required for MCP servers.

### Check if already installed:
```powershell
uvx --version
```

### If not installed:
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Installs to `%USERPROFILE%\.local\bin\` (uv.exe, uvx.exe).

### Verify PATH:
After installation, restart terminal or run:
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","User") + ";" + [System.Environment]::GetEnvironmentVariable("Path","Machine")
uvx --version
```

## 5. Install Python Dependencies

```powershell
pip install pdf2image Pillow
```

## 6. Final Verification

Test Poppler conversion:
```powershell
& "$toolsDir\poppler\Library\bin\pdftoppm.exe" -jpeg -r 150 "input.pdf" "$toolsDir\poppler_pdf_jpgs\output"
```

## Completion

All tools ready:
- **Python**: Script execution
- **Poppler**: PDF to image conversion (`[WORKSPACE_FOLDER]/.tools/poppler/`)
- **uv/uvx**: Python package runner for MCP servers
- **Output folder**: `[WORKSPACE_FOLDER]/.tools/poppler_pdf_jpgs/` (tracked via .gitkeep)
