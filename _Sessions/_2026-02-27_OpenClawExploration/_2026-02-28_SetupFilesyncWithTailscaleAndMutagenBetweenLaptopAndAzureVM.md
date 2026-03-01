# INFO: File Sync Setup Record - Laptop to Azure VM

**Doc ID**: FSYNC-IN01
**Goal**: Document the setup of real-time file sync between laptop and Azure VM
**Created**: 2026-02-28
**Status**: [COMPLETED] - Sync operational

## Configuration Summary

### Network

- **Laptop Tailscale IP**: 100.97.242.28
- **VM Tailscale IP**: 100.98.20.25
- **VM Windows Username**: User

### Laptop Paths

- **Sync folder**: `E:\Dev`
- **Mutagen executable**: `%LOCALAPPDATA%\mutagen\mutagen.exe`
- **SSH private key**: `%USERPROFILE%\.ssh\id_ed25519_mutagen`
- **SSH public key**: `%USERPROFILE%\.ssh\id_ed25519_mutagen.pub`
- **SSH config**: `%USERPROFILE%\.ssh\config`
- **Tailscale**: `C:\Program Files\Tailscale\`
- **Batch files**: `E:\Dev\*-vm-sync.bat`

### VM Paths

- **Sync folder**: `E:\Dev`
- **Bitvise SSH Server**: `C:\Program Files\Bitvise SSH Server\`
- **Bitvise settings**: Bitvise Control Panel → Easy settings
- **Public key imported in**: Bitvise → Windows accounts → User → Public keys
- **Tailscale**: `C:\Program Files\Tailscale\`
- **Key transfer location**: `E:\Karsten\Dropbox\TransferAzureVM\laptop_key_new.pub`

### Mutagen Session

- **Session name**: dev-sync
- **Session ID**: `sync_NzmB17ebMvnVNF2PioMd3wk0oPbHPjAJk5BLYwurVso`
- **Sync mode**: Two Way Safe (bidirectional)
- **Alpha (source)**: Laptop `E:\Dev`
- **Beta (target)**: VM `User@100.98.20.25:E:\Dev`

## Summary

Established real-time bidirectional file synchronization between Windows laptop and Azure Windows 11 VM.

**Stack:** Tailscale (mesh network) + Bitvise SSH Server + Mutagen (file sync)

**Result:** `E:\Dev` on laptop syncs with `E:\Dev` on VM in real-time.

## Install Procedure

### Part 1: Setup on the Azure VM

#### Step 1: Install Bitvise SSH Server

```powershell
Invoke-WebRequest -Uri "https://dl.bitvise.com/BvSshServer-Inst.exe" -OutFile "$env:TEMP\BvSshServer-Inst.exe"
Start-Process -FilePath "$env:TEMP\BvSshServer-Inst.exe"
```

In the installer:
- Check "I agree to accept all the terms"
- Select "Personal Edition" (free for personal use)
- Fill in your name
- Click "Install"

#### Step 2: Configure Bitvise

1. In the Bitvise Control Panel, click **"Start Server"**
2. Click **"Open easy settings"**
3. Go to **"2. Windows accounts"** tab
4. Your Windows user should already be listed with "Login allowed" checked
5. Click **"Save changes"**

#### Step 3: Install Tailscale on VM

```powershell
winget install tailscale.tailscale --accept-package-agreements --accept-source-agreements
& 'C:\Program Files\Tailscale\tailscale.exe' up
```

Sign in with your Google/Microsoft/GitHub account when prompted.

#### Step 4: Create the Sync Folder

```powershell
New-Item -ItemType Directory -Path "E:\Dev" -Force
```

### Part 2: Setup on Your Laptop

#### Step 5: Install Tailscale on Laptop

```powershell
winget install tailscale.tailscale
```

Open Tailscale from Start Menu and sign in with the same account as the VM.

#### Step 6: Generate SSH Key (No Password)

```powershell
ssh-keygen -t ed25519 -C "laptop-mutagen" -N '""' -f "$env:USERPROFILE\.ssh\id_ed25519_mutagen"
```

#### Step 7: Copy Public Key to VM

```powershell
Copy-Item "$env:USERPROFILE\.ssh\id_ed25519_mutagen.pub" "<YOUR_SHARED_FOLDER>\laptop_key.pub"
```

#### Step 8: Configure SSH to Use the New Key

```powershell
Add-Content -Path "$env:USERPROFILE\.ssh\config" -Value "`nHost 100.98.20.25`n    IdentityFile ~/.ssh/id_ed25519_mutagen`n    User User"
```

### Part 3: Connect the Key on the VM

#### Step 9: Import Laptop Key into Bitvise

1. On the VM, open **Bitvise SSH Server Control Panel**
2. Click **"Open easy settings"**
3. Go to **"2. Windows accounts"** tab
4. Click on your user, then **"Edit"**
5. Click **"Public keys"**
6. Click **"Import"** > **"Import from file"**
7. Select the key file from your shared folder (laptop_key.pub)
8. Click **"Close"** > **"OK"** > **"Save changes"**

### Part 4: Test and Start Syncing

#### Step 10: Test SSH Connection (on Laptop)

```powershell
ssh -o BatchMode=yes User@100.98.20.25 "echo SSH_KEY_AUTH_SUCCESS"
```

#### Step 11: Install Mutagen (on Laptop)

Mutagen is not available via winget. Download and extract manually:

```powershell
Invoke-WebRequest -Uri "https://github.com/mutagen-io/mutagen/releases/download/v0.18.1/mutagen_windows_amd64_v0.18.1.zip" -OutFile "$env:TEMP\mutagen.zip"
Expand-Archive -Path "$env:TEMP\mutagen.zip" -DestinationPath "$env:LOCALAPPDATA\mutagen" -Force
$env:Path += ";$env:LOCALAPPDATA\mutagen"
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$env:LOCALAPPDATA\mutagen", "User")
& "$env:LOCALAPPDATA\mutagen\mutagen.exe" daemon start
```

#### Step 12: Create Sync Session (on Laptop)

```powershell
& "$env:LOCALAPPDATA\mutagen\mutagen.exe" sync create --name=dev-sync E:\Dev User@100.98.20.25:E:\Dev
```

#### Step 13: Monitor Sync

```powershell
& "$env:LOCALAPPDATA\mutagen\mutagen.exe" sync monitor dev-sync
```

## Session Created

Session ID: `sync_NzmB17ebMvnVNF2PioMd3wk0oPbHPjAJk5BLYwurVso`

## Batch Files Created

Located in `E:\Dev\`:

- **start-vm-sync.bat** - Start Tailscale + Mutagen, create/resume sync
- **stop-vm-sync.bat** - Pause sync (session preserved)
- **monitor-vm-sync.bat** - Live progress monitoring
- **conflicts-vm-sync.bat** - Check and resolve conflicts
- **rescan-vm-sync.bat** - Force rescan both sides
- **flush-vm-sync.bat** - Push pending changes immediately
- **reset-vm-sync.bat** - Delete and recreate session from scratch

## Sync Behavior

- **Two Way Safe mode**: Changes on either side sync to the other
- **Deletions propagate**: Delete on laptop → deleted on VM (and vice versa)
- **Conflicts**: Same file modified on both sides → flagged for manual resolution
- **Identical files**: Compared by SHA-1 hash, skipped if same

## Issues Encountered

1. **Mutagen not in winget** - Had to download from GitHub directly
2. **SSH key auth failed initially** - Windows OpenSSH permissions issue; switched to Bitvise which handles keys via GUI import
3. **High latency** - Tailscale connection ~1100ms (Azure location), but sync still works

## OpenClaw Remote Access Configuration

Added 2026-03-01. OpenClaw gateway on VM accessible from laptop via Tailscale Serve.

### OpenClaw Paths (VM)

- **OPENCLAW_HOME**: `E:\Dev\openclaw`
- **OPENCLAW_STATE_DIR**: `E:\Dev\openclaw\.openclaw`
- **OPENCLAW_CONFIG_PATH**: `E:\Dev\openclaw\.openclaw\openclaw.json`
- **Workspace**: `E:\Dev\openclaw\workspace`
- **Gateway port**: 18789

### Tailscale Serve

- **Access URL**: `https://wa-vm-01.tailaed0cc.ts.net/`
- **Local gateway**: `ws://127.0.0.1:18789`

### openclaw.json Gateway Config

```json
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback",
    "auth": {
      "mode": "token",
      "token": "77e4feb0a2ffbf87762944de809b656f897b1a6f9db9b3c8"
    },
    "controlUi": {
      "allowedOrigins": [
        "https://wa-vm-01.tailaed0cc.ts.net"
      ]
    },
    "trustedProxies": ["127.0.0.1", "::1"]
  }
}
```

### Setup Steps Performed

1. Set environment variables for custom OpenClaw paths
2. Moved OpenClaw data from `C:\Users\User\.openclaw` to `E:\Dev\openclaw\.openclaw`
3. Updated `workspace` path in `openclaw.json`
4. Enabled Tailscale Serve: `tailscale serve --bg 18789`
5. Added `controlUi.allowedOrigins` with Tailscale URL
6. Added `trustedProxies` for proxy header handling
7. Approved laptop device pairing: `openclaw devices approve <request-id>`

### Batch Files (VM)

- `E:\Dev\openclaw-start.bat` - Start gateway (local or via SSH from laptop)
- `E:\Dev\openclaw-stop.bat` - Stop gateway
- `E:\Dev\openclaw-status.bat` - Check gateway status

### Device Pairing

Laptop paired and approved for remote dashboard access.

Commands:
```powershell
openclaw devices list
openclaw devices approve <id>
```

## Document History

**[2026-03-01 16:35]**
- Added: OpenClaw Remote Access Configuration section (paths, Tailscale Serve, gateway config, batch files, device pairing)

**[2026-02-28 19:36]**
- Rewrote: Changed from guide format to record of what was done

**[2026-02-28 19:34]**
- Fixed: Mutagen install command (winget not available, use GitHub download)
- Added: Batch files section with 7 helper scripts

**[2026-02-28 19:15]**
- Initial document created from successful setup session
