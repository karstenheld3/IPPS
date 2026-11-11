# Git Setup Guide

Install and configure Git for Windows.

## Prerequisites

- Windows 10/11
- PowerShell 5.1+ or PowerShell Core 7+
- Administrator access (for system-wide install)

## Check if Git is Installed

```powershell
git --version
```

If command returns version number, Git is already installed. Skip to [Configuration](#configuration).

## Installation Methods

### Method 1: Winget (Recommended)

```powershell
winget install --id Git.Git -e --source winget
```

After installation, restart terminal or run:
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

### Method 2: Chocolatey

```powershell
choco install git -y
```

### Method 3: Manual Download

1. Download from https://git-scm.com/download/win
2. Run installer with defaults
3. Restart terminal

## Configuration

### Set Identity (Required)

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Verify Configuration

```powershell
git config --global --list
```

### Recommended Settings

```powershell
# Default branch name
git config --global init.defaultBranch main

# Line ending handling (Windows)
git config --global core.autocrlf true

# Default editor (VSCode)
git config --global core.editor "code --wait"

# Credential helper (Windows)
git config --global credential.helper manager
```

## Verification

```powershell
# Check version
git --version

# Check config
git config --global user.name
git config --global user.email

# Test with a simple operation
git init test-repo
cd test-repo
echo "test" > test.txt
git add .
git commit -m "test commit"
git log --oneline
cd ..
Remove-Item -Recurse -Force test-repo
```

## Troubleshooting

### Git not found after installation

Restart terminal or refresh PATH:
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

### Permission denied errors

Run PowerShell as Administrator for system-wide operations.

### SSL certificate problems

```powershell
git config --global http.sslBackend schannel
```

# GitHub CLI Setup

Run once to install GitHub CLI locally in `[WORKSPACE_FOLDER]/../.tools/`.

## 1. Set Workspace Folder

```powershell
$workspaceFolder = (Get-Location).Path  # or set explicitly: $workspaceFolder = "C:\Dev\MyProject"
$toolsDir = "$workspaceFolder\..\.tools"
$installerDir = "$toolsDir\_installer"

# Create folders if needed
if (-not (Test-Path $toolsDir)) { New-Item -ItemType Directory -Path $toolsDir }
if (-not (Test-Path $installerDir)) { New-Item -ItemType Directory -Path $installerDir }
```

## 2. Install GitHub CLI Locally

**Check if already installed:**
```powershell
Test-Path "$toolsDir\gh\bin\gh.exe"
```

**If not installed, download and extract:**
```powershell
$ghDir = "$toolsDir\gh"

# Download latest GitHub CLI for Windows (64-bit)
$ghUrl = "https://github.com/cli/cli/releases/download/v2.63.2/gh_2.63.2_windows_amd64.zip"
$zipPath = "$installerDir\gh.zip"

Invoke-WebRequest -Uri $ghUrl -OutFile $zipPath

# Extract to gh folder (zip contains bin/ and LICENSE at root)
New-Item -ItemType Directory -Path $ghDir -Force | Out-Null
Expand-Archive -Path $zipPath -DestinationPath $ghDir -Force
```

**Verify installation:**
```powershell
& "$toolsDir\gh\bin\gh.exe" --version
```

## 3. Authenticate with GitHub

**Check authentication status:**
```powershell
& "$toolsDir\gh\bin\gh.exe" auth status
```

**If not authenticated, login:**
```powershell
& "$toolsDir\gh\bin\gh.exe" auth login
```

Follow the prompts to authenticate via browser or token.

## 4. Configure Git (Optional)

Set gh as credential helper for seamless git operations:
```powershell
& "$toolsDir\gh\bin\gh.exe" auth setup-git
```

## Completion

GitHub CLI ready:
- **gh**: GitHub CLI (`[WORKSPACE_FOLDER]/../.tools/gh/bin/`)
- Run `gh auth login` to authenticate with your GitHub account
