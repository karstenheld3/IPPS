# gogcli Sources

**Doc ID**: GOAC-SOURCES-01
**Accessed**: 2026-03-04

## Primary Sources (Tier 1-2)

### GOAC-SC-GH-README

- **URL**: https://github.com/steipete/gogcli
- **Type**: Official GitHub repository
- **Tier**: 1 (primary)
- **Content**: Full README with installation, authentication, all commands
- **Status**: Accessed

### GOAC-SC-SITE-HOME

- **URL**: https://gogcli.sh/
- **Type**: Official website
- **Tier**: 1 (primary)
- **Content**: Quick start, feature overview
- **Status**: Accessed

## Key Findings from Sources

### Installation

- **Homebrew**: `brew install steipete/tap/gogcli`
- **Arch**: `yay -S gogcli`
- **Build from source**: `git clone` + `make`
- **Windows**: Build from source (Go binary)

### Authentication Flow

1. Create OAuth2 Desktop app credentials in Google Cloud Console
2. Enable required APIs (Gmail, Calendar, Drive, Tasks, etc.)
3. Store credentials: `gog auth credentials ~/Downloads/client_secret_....json`
4. Add account: `gog auth add you@gmail.com`
5. Browser opens for OAuth consent
6. Headless/remote: Use `--manual` or `--remote` flag for server auth

### Credential Storage

- **macOS**: Keychain Access
- **Linux**: Secret Service (GNOME Keyring, KWallet)
- **Windows**: Credential Manager
- **Fallback**: Encrypted file backend with `GOG_KEYRING_PASSWORD`
- **Config path (Linux)**: `~/.config/gogcli/config.json`
- **Config path (Windows)**: `%AppData%\gogcli\config.json`

### Gmail Commands (Key)

- Search: `gog gmail search 'newer_than:7d' --max 10`
- Read thread: `gog gmail thread get <threadId>`
- Download attachments: `gog gmail thread get <threadId> --download --out-dir ./attachments`
- Send: `gog gmail send --to a@b.com --subject "Hi" --body "Text"`
- Drafts: `gog gmail drafts create/update/send`
- Labels: `gog gmail labels list/create/modify`

### Calendar Commands (Key)

- List events: `gog calendar events primary --today`
- Create event: `gog calendar create primary --summary "Meeting" --from ... --to ... --attendees "..."`
- Update: `gog calendar update <calendarId> <eventId> --summary "..."`
- Google Meet: Not directly supported via CLI (API limitation for conferenceData)
- Free/busy: `gog calendar freebusy --calendars "primary" --from ... --to ...`

### Tasks Commands

- List tasklists: `gog tasks lists`
- List tasks: `gog tasks list <tasklistId>`
- Add task: `gog tasks add <tasklistId> --title "..." --due 2025-02-01`
- Complete: `gog tasks done <tasklistId> <taskId>`

### Drive Commands (for attachments)

- Download: `gog drive download <fileId> --out ./file.bin`
- List: `gog drive ls --max 20`
- Search: `gog drive search "query"`

### Agent Automation Notes

- Environment variable for account: `GOG_ACCOUNT=you@gmail.com`
- Non-interactive runs: Set `GOG_KEYRING_PASSWORD` for file backend
- JSON output: `gog --json gmail search ...`
- Command allowlist (sandboxing): `GOG_ENABLE_COMMANDS=gmail,calendar`

### WSL Integration Notes

- gogcli is a Go binary, can be built for Windows natively
- For WSL approach: Install via Homebrew in WSL, call via `wsl gog ...`
- Keyring in WSL: No OS keychain, use file backend with `GOG_KEYRING_BACKEND=file`
- Password management: `GOG_KEYRING_PASSWORD` environment variable

## Missing Information

- **Google Meet link creation**: Not directly supported in CLI, requires Google Calendar API conferenceData
- **Workspace-only features**: Chat, Keep, Groups require Google Workspace (not personal Gmail)
