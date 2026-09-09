# Google Account Skill Uninstall (gogcli)

Remove gogcli and associated configuration.

## Removal Options

- Option 1 (Minimal): Config only - WSL `~/.config/gogcli/`, Windows `%AppData%\gogcli\`
- Option 2 (Standard): Option 1 + gogcli binary (Homebrew or manual)
- Option 3 (Full): Option 2 + OAuth client secret files (`client_secret*.json`)
- Option 4 (Complete): Option 3 + WSL distributions (extra confirmation required)

WARNING: Option 4 removes WSL which may be used by Docker Desktop, VS Code Remote, other Linux tools.

## Detection and Paths

Key variables and locations the uninstall checks:

- WSL installed: `wsl --list --quiet`
- gogcli installed: `wsl bash -c 'command -v gog'`
- WSL config: `wsl bash -c 'test -d ~/.config/gogcli && echo "exists"'`
- Windows config: `$env:APPDATA\gogcli`
- Credential files (checked in order):
  - `[WORKSPACE]/../.tools/gogcli-client-secret.json` (.tools sibling to workspace)
  - `$env:USERPROFILE\client_secret.json`
  - `$env:USERPROFILE\.client_secret.json`
  - `$env:USERPROFILE\Downloads\client_secret*.json`

## Removal Commands

### Config (Options 1-4)

```bash
# WSL config
rm -rf ~/.config/gogcli
```

```powershell
# Windows config
Remove-Item "$env:APPDATA\gogcli" -Recurse -Force
```

### gogcli Binary (Options 2-4)

```bash
# Try Homebrew first
brew uninstall gogcli
# If Homebrew fails, remove manually
rm -f ~/gogcli/bin/gog ~/go/bin/gog /usr/local/bin/gog
rm -rf ~/gogcli
```

### Credentials (Options 3-4)

Delete all `client_secret*.json` from paths listed in Detection section above.

### WSL (Option 4 only)

Requires typing `REMOVE WSL` to confirm.

```powershell
# Unregister all distributions
$distros = wsl --list --quiet
foreach ($distro in $distros) { wsl --unregister $distro.Trim() }
# To fully remove WSL feature (Admin PowerShell):
dism.exe /online /disable-feature /featurename:Microsoft-Windows-Subsystem-Linux
```

### Environment Variables

Remove from `~/.bashrc` or `~/.profile`:

```bash
export GOG_ACCOUNT='...'
export GOG_KEYRING_BACKEND='...'
export GOG_KEYRING_PASSWORD='...'
export GOG_ENABLE_COMMANDS='...'
```

### Revoke OAuth Access (Optional)

1. Go to https://myaccount.google.com/permissions
2. Find gogcli app, click "Remove Access"

## Troubleshooting

### "Homebrew uninstall failed"

```bash
rm -f $(which gog)
```

### "WSL removal failed"

Run PowerShell as Administrator:
```powershell
wsl --shutdown
wsl --unregister Ubuntu  # or your distro name
```

## Recovery Notes

- Config files, gogcli binary, credential files: can be recreated/reinstalled
- OAuth tokens: must re-authorize after removal
- WSL data: cannot recover unless backed up