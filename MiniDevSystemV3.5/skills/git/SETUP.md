# Git Setup Guide

Install and configure Git for Windows.

Prerequisites: Windows 10/11, PowerShell 5.1+, Administrator access (system-wide install)

## Check if Installed

```powershell
git --version
```

If version returned, skip to Configuration.

## Installation

**Winget (Recommended):**
```powershell
winget install --id Git.Git -e --source winget
```

Refresh PATH after install:
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

**Chocolatey:** `choco install git -y`

**Manual:** https://git-scm.com/download/win - run installer with defaults, restart terminal.

## Configuration

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main
git config --global core.autocrlf true
git config --global core.editor "code --wait"
git config --global credential.helper manager
```

Verify: `git config --global --list`

## Troubleshooting

**Permission denied:** Run PowerShell as Administrator.

**SSL certificate problems:**
```powershell
git config --global http.sslBackend schannel
```