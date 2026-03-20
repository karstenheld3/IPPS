# GitHub CLI Setup

Install GitHub CLI locally in `[WORKSPACE_FOLDER]/../.tools/`.

## 1. Set Workspace Folder

```powershell
$workspaceFolder = (Get-Location).Path
$toolsDir = "$workspaceFolder\..\.tools"
$installerDir = "$toolsDir\_installer"
if (-not (Test-Path $toolsDir)) { New-Item -ItemType Directory -Path $toolsDir }
if (-not (Test-Path $installerDir)) { New-Item -ItemType Directory -Path $installerDir }
```

## 2. Install GitHub CLI

```powershell
# Check existing
Test-Path "$toolsDir\gh\bin\gh.exe"

# Download and extract
$ghDir = "$toolsDir\gh"
$ghUrl = "https://github.com/cli/cli/releases/download/v2.63.2/gh_2.63.2_windows_amd64.zip"
Invoke-WebRequest -Uri $ghUrl -OutFile "$installerDir\gh.zip"
New-Item -ItemType Directory -Path $ghDir -Force | Out-Null
Expand-Archive -Path "$installerDir\gh.zip" -DestinationPath $ghDir -Force

# Verify
& "$toolsDir\gh\bin\gh.exe" --version
```

## 3. Authenticate

```powershell
& "$toolsDir\gh\bin\gh.exe" auth status
& "$toolsDir\gh\bin\gh.exe" auth login
```

## 4. Configure Git (Optional)

```powershell
& "$toolsDir\gh\bin\gh.exe" auth setup-git
```