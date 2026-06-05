# INFO: Mutagen Sync from Windows to Azure Windows 11 VM

**Doc ID**: MUTAG-IN01
**Goal**: Complete setup guide for syncing E:\Dev folder to Azure Windows 11 VM using Mutagen
**Created**: 2026-02-28
**Updated**: 2026-02-28 (1 revision)
**Strategy**: MEPI (curated, actionable setup guide)
**Domain**: SOFTWARE

## Summary (Copy/Paste Ready)

**Critical requirement**: Use Bitvise SSH Server on Windows VM (NOT OpenSSH) [VERIFIED]

**Quick setup steps**:
1. Create Azure Windows 11 VM (Standard_D2s_v3, 8 GB RAM)
2. Install Bitvise SSH Server on VM (free for personal use)
3. Configure Bitvise with Windows account + SSH key
4. Install Mutagen on laptop: `winget install mutagen-io.mutagen`
5. Create sync session: `mutagen sync create --name=dev-sync E:\Dev dev-vm:C:\Dev`

**Key commands**:
- Monitor: `mutagen sync monitor dev-sync`
- Pause: `mutagen sync pause dev-sync`
- Resume: `mutagen sync resume dev-sync`

**Estimated setup time**: 45-60 minutes

## CRITICAL: SSH Server Choice

**Mutagen only reliably works with Bitvise SSH Server on Windows** [VERIFIED - official Mutagen docs]

- **Bitvise SSH Server** - Recommended, only officially supported Windows SSH server
- **Windows OpenSSH Server** - Not recommended, performance issues and stalled data streams [VERIFIED]
- **Cygwin OpenSSH** - Untested, may work but not officially supported

**Source**: https://mutagen.io/documentation/transports/ssh/ - "Mutagen is currently only known to work reliably with Bitvise SSH Server on Windows."

## Table of Contents

1. Executive Summary
2. Architecture Overview
3. Prerequisites
4. Phase 1: Azure Windows 11 VM Setup
5. Phase 2: Bitvise SSH Server Installation (on VM)
6. Phase 3: Windows Mutagen Installation (on Laptop)
7. Phase 4: SSH Configuration
8. Phase 5: Mutagen Sync Session
9. Phase 6: Optimization for Large Dev Folders
10. Maintenance and Troubleshooting
11. Sources

## 1. Executive Summary

**Goal**: Sync entire `E:\Dev` folder from Windows laptop to Azure Windows 11 VM.

**Solution**: Mutagen real-time sync over SSH (using Bitvise SSH Server)

**Architecture**:
```
Windows Laptop (E:\Dev)  <--Mutagen SSH-->  Azure Windows 11 VM (C:\Dev)
         |                                            |
    Local work                               Remote dev environment
```

**Key Benefits**:
- Real-time bidirectional sync (changes in <1 second)
- Three-way merge prevents spurious conflicts
- No conflict copies with `two-way-resolved` mode
- Works over any SSH connection (Tailscale recommended for always-on)

**Critical Requirement**: Bitvise SSH Server on Windows VM (NOT OpenSSH)

**Estimated Setup Time**: 45-60 minutes

## 2. Architecture Overview

### Sync Flow

```
E:\Dev (Windows Laptop)
    |
    v
[Mutagen Daemon] -- SSH (Bitvise) --> [Azure Windows 11 VM: C:\Dev]
    |                                          |
    +-- Scans changes                          +-- Remote dev work
    +-- Transfers deltas                       +-- Git operations
    +-- Resolves conflicts                     +-- Build/test
```

### Why Mutagen for This Use Case

- **Large folder (E:\Dev)** - Efficient scanning, rsync delta algorithm
- **Multiple repos** - Per-repo or whole-folder sync
- **No conflict copies** - `two-way-resolved` mode (laptop wins, see warning below)
- **Custom folder location** - Any path on both sides
- **Physical files** - Full files synced (not symlinks)
- **Real-time** - Filesystem watching, <1s propagation

### Windows-to-Windows Sync Considerations

**Why Bitvise SSH Server is required** [VERIFIED - Mutagen docs]:
- Windows OpenSSH Server has performance issues and stalled data streams
- Bitvise is the only Windows SSH server officially known to work reliably with Mutagen
- Bitvise is free for personal use, $99.50/year for commercial use

**Path handling**:
- Laptop uses `E:\Dev`, VM uses `C:\Dev` (Mutagen syncs content, paths can differ)
- Azure VMs have C: and D: drives by default (no E: drive without additional disk)
- Mutagen handles Windows path separators automatically
- Both sides use NTFS (consistent permissions)

**Conflict warning** (`two-way-resolved` mode):
- Laptop (alpha) ALWAYS wins conflicts
- If you edit a file on VM, then edit the same file on laptop before sync completes, **VM changes are silently lost**
- Best practice: Edit on one machine at a time, wait for sync to complete before switching

## 3. Prerequisites

### Windows Side

- [ ] **Git for Windows** installed (provides OpenSSH client that Mutagen uses)
  - Download: https://git-scm.com/download/win
  - Mutagen automatically finds Git's SSH at `C:\Program Files\Git\usr\bin\ssh.exe`

- [ ] **Mutagen** installed
  ```powershell
  # Option 1: winget (recommended)
  winget install mutagen-io.mutagen
  
  # Option 2: Scoop
  scoop install mutagen
  
  # Option 3: Direct download
  # https://github.com/mutagen-io/mutagen/releases
  ```

- [ ] **SSH key pair** generated
  ```powershell
  # If you don't have one already
  ssh-keygen -t ed25519 -C "mutagen-azure"
  # Keys stored in: %USERPROFILE%\.ssh\id_ed25519
  ```

- [ ] **(Optional) Long paths enabled** - Required if you have deep `node_modules` folders
  ```powershell
  # Run as admin, requires reboot
  Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1
  ```

### Azure Side (Windows 11 VM)

- [ ] **Azure Windows 11 VM**
  - Size: Standard_D2s_v3 minimum (2 vCPU, 8 GB RAM) - Windows needs more RAM than Linux
  - Disk: Premium SSD recommended for large repos
  - OS: Windows 11 Pro or Enterprise

- [ ] **NSG Rule** for SSH (port 22) or custom port
  - Source: Your IP or Tailscale network
  - Destination: VM
  - Port: 22 (or custom Bitvise port)

- [ ] **Bitvise SSH Server** (will be installed in Phase 2)
  - Free for personal use
  - Download: https://bitvise.com/ssh-server-download

## 4. Phase 1: Azure Windows 11 VM Setup

### 4.1 Create Azure Windows 11 VM

```powershell
# Azure CLI (run from Windows laptop)
az login

# Create Windows 11 VM
az vm create `
  --resource-group YOUR_RG `
  --name dev-vm `
  --image MicrosoftWindowsDesktop:windows-11:win11-23h2-pro:latest `
  --size Standard_D2s_v3 `
  --admin-username User `
  --admin-password 'YOUR_SECURE_PASSWORD' `
  --public-ip-sku Standard
```

### 4.2 Configure NSG for SSH

```powershell
# Allow SSH from your IP only (recommended)
az network nsg rule create `
  --resource-group YOUR_RG `
  --nsg-name dev-vmNSG `
  --name AllowSSH `
  --priority 1000 `
  --source-address-prefixes YOUR_IP `
  --destination-port-ranges 22 `
  --access Allow `
  --protocol Tcp
```

### 4.3 Connect to VM via RDP (Initial Setup)

```powershell
# Get VM public IP
az vm show -g YOUR_RG -n dev-vm --show-details --query publicIps -o tsv

# Connect via Remote Desktop
mstsc /v:YOUR_VM_IP
```

### 4.4 Create Target Directory on VM

```powershell
# On Azure Windows 11 VM (via RDP)
New-Item -ItemType Directory -Path C:\Dev -Force
```

### 4.5 (Recommended) Install Tailscale for Always-On Access

```powershell
# On Azure Windows 11 VM
winget install tailscale
tailscale up

# On Windows laptop
winget install tailscale
tailscale up
```

With Tailscale, you get:
- Always-on connection (no need for public IP)
- Encrypted tunnel
- Works through NAT/firewalls
- Stable hostname: `dev-vm.tailnet-xxxx.ts.net`

## 5. Phase 2: Bitvise SSH Server Installation (on VM)

**CRITICAL**: Use Bitvise SSH Server, NOT Windows OpenSSH Server [VERIFIED - Mutagen docs]

### 5.1 Download and Install Bitvise

```powershell
# On Azure Windows 11 VM (via RDP or Tailscale)
# Download from: https://bitvise.com/ssh-server-download
# Or use direct link:
Invoke-WebRequest -Uri "https://dl.bitvise.com/BvSshServer-Inst.exe" -OutFile "$env:TEMP\BvSshServer-Inst.exe"
Start-Process -FilePath "$env:TEMP\BvSshServer-Inst.exe" -Wait
```

### 5.2 Configure Bitvise SSH Server

1. **Open Bitvise SSH Server Control Panel** (Start Menu > Bitvise SSH Server)

2. **Easy Settings > Server Settings**:
   - Enable "Open Windows Firewall" (auto-creates rule for port 22)
   - Set interface to listen on: All interfaces

3. **Easy Settings > Windows Accounts**:
   - Click "Add"
   - Select your Windows user (e.g., `User`)
   - Enable "Allow login"
   - Enable "Allow terminal shell"
   - Enable "Allow file transfer (SFTP, SCP)"

4. **Easy Settings > Virtual Accounts** (alternative):
   - Create a virtual account for Mutagen
   - Set shell access: PowerShell or CMD
   - Set initial directory: `C:\Dev`

### 5.3 Configure SSH Key Authentication

1. **On Windows laptop**, copy your public key:
   ```powershell
   Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | Set-Clipboard
   ```

2. **On Azure VM**, add to Bitvise:
   - Open Bitvise SSH Server Control Panel
   - Go to "Easy Settings" > "Windows Accounts" or "Virtual Accounts"
   - Select your account > Edit
   - Go to "Public keys" section
   - Click "Import" > paste your public key
   - Save and apply

### 5.4 Start Bitvise SSH Server

```powershell
# Start the service
net start BvSshServer

# Verify it's running
Get-Service BvSshServer
```

### 5.5 Test SSH Connection from Laptop

```powershell
# From Windows laptop
ssh User@YOUR_VM_IP
# OR with Tailscale
ssh User@dev-vm

# Should connect without password (key-based auth)
```

## 6. Phase 3: Windows Mutagen Installation (on Laptop)

### 6.1 Install Mutagen

```powershell
# Recommended: winget
winget install mutagen-io.mutagen

# Verify installation
mutagen version
# Expected: mutagen version 0.17.x or higher
```

### 6.2 Verify SSH Works with Bitvise

```powershell
# Test SSH connection to Windows 11 VM with Bitvise
ssh azureuser@dev-vm  # Tailscale
# OR
ssh azureuser@YOUR_VM_IP   # Public IP

# Should connect without password (key-based auth)
# You should see a Windows command prompt or PowerShell
```

### 6.3 Register Daemon for Auto-Start

```powershell
# Start daemon and register for auto-start on Windows login
mutagen daemon register
mutagen daemon start
```

## 7. Phase 4: SSH Configuration

### 7.1 Create SSH Config (Recommended)

Create/edit `%USERPROFILE%\.ssh\config`:

```
Host dev-vm
    HostName dev-vm.tailnet-xxxx.ts.net  # Tailscale
    # OR: HostName YOUR_VM_PUBLIC_IP
    User User
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes
```

### 7.2 Test SSH Alias

```powershell
ssh dev-vm
# Should connect immediately and show Windows prompt
```

## 8. Phase 5: Mutagen Sync Session

### 8.1 Create Global Configuration

Create `%USERPROFILE%\.mutagen.yml`:

```yaml
sync:
  defaults:
    # Use two-way-resolved to prevent conflict copies (alpha wins)
    mode: "two-way-resolved"
    
    # Ignore VCS directories (recommended)
    ignore:
      vcs: true
      paths:
        # Common ignores for dev folders
        - "node_modules"
        - "__pycache__"
        - "*.pyc"
        - ".pytest_cache"
        - "dist"
        - "build"
        - ".venv"
        - "venv"
        - "*.egg-info"
        - ".tox"
        - ".mypy_cache"
        - ".ruff_cache"
        - "coverage"
        - ".coverage"
        - "*.log"
        - ".DS_Store"
        - "Thumbs.db"
        # Large binary folders
        - "*.iso"
        - "*.zip"
        - "*.tar.gz"
    
    # Watch settings for large folders
    watch:
      mode: "force-poll"
      pollingInterval: 10
```

### 8.2 Create Sync Session

```powershell
# Create the sync session (Windows to Windows)
mutagen sync create `
  --name=dev-sync `
  --sync-mode=two-way-resolved `
  --ignore-vcs `
  E:\Dev `
  dev-vm:C:\Dev

# Expected output:
# Created session sync_xxxxxxxxxx
```

**Note**: Laptop uses `E:\Dev`, VM uses `C:\Dev`. Mutagen syncs content regardless of path names.

### 8.3 Verify Sync Status

```powershell
# List sessions
mutagen sync list

# Monitor real-time status
mutagen sync monitor dev-sync

# Expected: "Watching for changes"
```

### 8.4 Initial Sync

The first sync will transfer all files. For a large E:\Dev folder:

- **10 GB**: ~5-10 minutes (LAN) / ~30-60 minutes (WAN 100 Mbps)
- **50 GB**: ~30-60 minutes (LAN) / ~3-5 hours (WAN 100 Mbps)
- **100 GB**: ~1-2 hours (LAN) / ~8-10 hours (WAN 100 Mbps)

Monitor progress:
```powershell
mutagen sync monitor dev-sync
```

### 8.5 If Initial Sync Fails or Interrupts

```powershell
# 1. Check status
mutagen sync list

# 2. If "Halted" or "Error": resume
mutagen sync resume dev-sync

# 3. If still failing: reset (rescans both sides)
mutagen sync reset dev-sync

# 4. If corrupted: terminate and recreate
mutagen sync terminate dev-sync
# Then recreate session with mutagen sync create...
```

## 9. Phase 6: Optimization for Large Dev Folders

### 9.1 Ignore Heavy Folders

For `E:\Dev` with many repos, add per-session ignores for large folders:

```powershell
# Add ignores to existing session (must recreate session)
mutagen sync terminate dev-sync

mutagen sync create `
  --name=dev-sync `
  --sync-mode=two-way-resolved `
  --ignore-vcs `
  --ignore="node_modules" `
  --ignore="__pycache__" `
  --ignore=".venv" `
  --ignore="venv" `
  --ignore="dist" `
  --ignore="build" `
  --ignore="*.pyc" `
  --ignore=".pytest_cache" `
  --ignore=".mypy_cache" `
  --ignore=".git"  `
  E:\Dev `
  dev-vm:C:\Dev
```

### 9.2 Why Ignore .git Directories

Mutagen documentation strongly recommends ignoring `.git` directories [VERIFIED]:

1. **Git index contains local metadata** (inode numbers, device IDs) - resyncing causes full rehash
2. **Object store is not homogenous** - loose objects vs pack files differ per copy
3. **Git expects exclusive access** - concurrent modifications cause corruption

**Recommended workflow**:
- Keep `.git` on Windows only
- Sync working tree to VM
- Run Git commands on Windows
- Changes propagate to VM automatically

### 9.3 Force Poll Mode for Very Large Folders

For folders with 100k+ files, use polling instead of filesystem watching:

```yaml
# In ~/.mutagen.yml
sync:
  defaults:
    watch:
      mode: "force-poll"
      pollingInterval: 30  # seconds (higher = less CPU, more delay)
```

### 9.4 Staging Configuration for Large Files

```yaml
# In ~/.mutagen.yml
sync:
  defaults:
    maxStagingFileSize: "100MB"  # Skip files larger than this
```

## 10. Maintenance and Troubleshooting

### 10.1 Common Commands

```powershell
# Check session status
mutagen sync list

# Monitor in real-time
mutagen sync monitor dev-sync

# Pause sync (e.g., before large Git operations)
mutagen sync pause dev-sync

# Resume sync
mutagen sync resume dev-sync

# Force rescan (after external changes)
mutagen sync flush dev-sync

# Reset session (clears state, rescans both sides)
mutagen sync reset dev-sync

# Terminate session
mutagen sync terminate dev-sync
```

### 10.2 Troubleshooting

#### SSH Connection Issues

```powershell
# Test SSH directly to Bitvise
ssh -v dev-vm

# Check if Mutagen can find SSH
$env:MUTAGEN_SSH_PATH = "C:\Program Files\Git\usr\bin"
mutagen sync list

# Verify Bitvise is running on VM
# (via RDP or another SSH session)
Get-Service BvSshServer
```

#### Sync Stuck or Slow

```powershell
# Check daemon status
mutagen daemon status

# Restart daemon
mutagen daemon stop
mutagen daemon start

# Reset session
mutagen sync reset dev-sync
```

#### Conflicts (Rare with two-way-resolved)

```powershell
# List any conflicts
mutagen sync list --long

# Conflicts auto-resolve (alpha wins), but if stuck:
mutagen sync reset dev-sync
```

#### High CPU Usage

```yaml
# In ~/.mutagen.yml - increase poll interval
sync:
  defaults:
    watch:
      pollingInterval: 60  # seconds
```

### 10.3 Logs and Debugging

```powershell
# Enable verbose logging
$env:MUTAGEN_LOG_LEVEL = "debug"
mutagen daemon stop
mutagen daemon start

# Check logs
# Windows: %USERPROFILE%\.mutagen\daemon.log
```

## 11. Quick Start Checklist

```
[ ] Azure Windows 11 VM created
[ ] Connected to VM via RDP for initial setup
[ ] Bitvise SSH Server installed on VM
[ ] Bitvise configured with Windows account + SSH key
[ ] Bitvise service running (BvSshServer)
[ ] C:\Dev folder created on VM
[ ] Git for Windows installed on laptop
[ ] Mutagen installed on laptop (winget install mutagen-io.mutagen)
[ ] SSH config created (~/.ssh/config with dev-vm alias)
[ ] SSH connection tested (ssh dev-vm shows Windows prompt)
[ ] ~/.mutagen.yml created with ignores
[ ] Sync session created (mutagen sync create ... dev-vm:C:\Dev)
[ ] Initial sync completed (mutagen sync monitor)
[ ] (Optional) Tailscale installed on both machines for always-on connection
```

## 12. Sources

### Official Documentation

- **MUTAG-SC-DOCS-START**: https://mutagen.io/documentation/introduction/getting-started/ (Accessed: 2026-02-28) [VERIFIED]
- **MUTAG-SC-DOCS-SYNC**: https://mutagen.io/documentation/synchronization/ (Accessed: 2026-02-28) [VERIFIED]
- **MUTAG-SC-DOCS-IGN**: https://mutagen.io/documentation/synchronization/ignores/ (Accessed: 2026-02-28) [VERIFIED]
- **MUTAG-SC-DOCS-VCS**: https://mutagen.io/documentation/synchronization/version-control-systems/ (Accessed: 2026-02-28) [VERIFIED]
- **MUTAG-SC-DOCS-SSH**: https://mutagen.io/documentation/transports/ssh/ (Accessed: 2026-02-28) [VERIFIED]
- **MUTAG-SC-DOCS-DAEMON**: https://mutagen.io/documentation/introduction/daemon/ (Accessed: 2026-02-28) [VERIFIED]
- **MUTAG-SC-GH**: https://github.com/mutagen-io/mutagen (Accessed: 2026-02-28) [VERIFIED]

### Azure Documentation

- **AZURE-SC-WIN-SSH**: https://learn.microsoft.com/en-us/azure/virtual-machines/windows/connect-ssh (Accessed: 2026-02-28) [VERIFIED]
- **AZURE-SC-WIN-OPENSSH**: https://learn.microsoft.com/en-us/samples/azure/azure-quickstart-templates/vm-windows-ssh/ (Accessed: 2026-02-28) [VERIFIED]

### Bitvise Documentation

- **BITVISE-SC-INSTALL**: https://bitvise.com/ssh-server-guide-installing (Accessed: 2026-02-28) [VERIFIED]
- **BITVISE-SC-ACCOUNTS**: https://bitvise.com/ssh-server-guide-accounts (Accessed: 2026-02-28) [VERIFIED]
- **BITVISE-SC-DOWNLOAD**: https://bitvise.com/ssh-server-download (Accessed: 2026-02-28) [VERIFIED]

### Community Sources

- **MUTAG-SC-DDEV**: https://ddev.com/blog/mutagen-functionality-issues-debugging/ (Accessed: 2026-02-28) [COMMUNITY]
- **MUTAG-SC-PHOTOROOM**: https://www.photoroom.com/inside-photoroom/mutagen-tutorial (Accessed: 2026-02-28) [COMMUNITY]

## Document History

**[2026-02-28 16:30]**
- Fixed: VM path changed to C:\Dev (Azure VMs don't have E: drive by default)
- Added: Section 8.5 - Sync recovery commands for interrupted initial sync
- Added: Conflict warning in Architecture section (laptop wins, VM changes lost)
- Added: Optional long paths prerequisite for deep node_modules folders

**[2026-02-28 16:20]**
- Changed: Target path from C:\Dev to E:\Dev (same as source)
- Changed: Username from azureuser to User (same on both machines)

**[2026-02-28 16:15]**
- Fixed: Converted Markdown tables to lists (GLOBAL-RULES compliance)
- Added: Summary section with copy/paste ready key findings
- Added: Timeline fields (Created, Updated)

**[2026-02-28 16:10]**
- Changed: Target VM from Linux to Windows 11
- Added: Critical warning about SSH server choice (Bitvise required)
- Added: Phase 2 - Bitvise SSH Server installation and configuration
- Changed: All paths from Linux (~/dev) to Windows (C:\Dev)
- Removed: OpenClaw integration section (Linux-specific)
- Added: Bitvise documentation sources
- Changed: Quick Start Checklist for Windows 11 VM

**[2026-02-28 15:45]**
- Initial document created
- Complete setup guide from Windows to Azure Linux VM
- Includes optimization for large dev folders
