# INFO: gogcli Google Account Integration

**Doc ID**: GOAC-IN01
**Goal**: Document gogcli CLI capabilities for Cascade skill creation enabling Google account interaction
**Strategy**: MEPI (curated, action-oriented)
**Domain**: SOFTWARE
**Version Scope**: gogcli v1.x (2026-03-04)

## Research Question

How to create a Cascade skill that enables Google account interaction (Gmail, Calendar, Drive, Tasks) using gogcli CLI, with focus on WSL integration for Windows and agent automation requirements?

## Key Corrections

**IMPORTANT**: The user referred to "gop CLI" - the correct tool is **`gogcli`** (command: `gog`).

## Key Findings

### 1. Tool Overview

`gogcli` is a unified CLI for Google services:
- **Gmail**: Search, read, send, drafts, labels, attachments, filters
- **Calendar**: Events CRUD, free/busy, reminders, recurrence
- **Drive**: Upload, download, organize, share
- **Tasks**: Tasklists, tasks CRUD, due dates, recurring
- **Contacts**: Personal contacts, directory search
- **Sheets/Docs/Slides**: Read, write, export
- **Additional**: Forms, Apps Script, People, Chat (Workspace-only), Groups (Workspace-only)

[VERIFIED] (GOAC-SC-GH-README | https://github.com/steipete/gogcli)

### 2. Installation Options

**Option A: Native Windows (Recommended for simplicity)**
```powershell
# Build from source (requires Go)
git clone https://github.com/steipete/gogcli.git
cd gogcli
go build -o bin/gog.exe ./cmd/gog
```

**Option B: WSL (Original user intent)**
```bash
# In WSL (Ubuntu)
brew install steipete/tap/gogcli

# Or build from source
git clone https://github.com/steipete/gogcli.git
cd gogcli
make
```

**Recommendation**: WSL approach is viable but adds complexity. Native Windows build is simpler if Go is available.

[VERIFIED] (GOAC-SC-GH-README | https://github.com/steipete/gogcli)

### 3. Authentication Flow

**Prerequisites (User must complete manually)**:
1. Create Google Cloud Project: https://console.cloud.google.com/projectcreate
2. Enable APIs:
   - Gmail API: https://console.cloud.google.com/apis/api/gmail.googleapis.com
   - Calendar API: https://console.cloud.google.com/apis/api/calendar-json.googleapis.com
   - Drive API: https://console.cloud.google.com/apis/api/drive.googleapis.com
   - Tasks API: https://console.cloud.google.com/apis/api/tasks.googleapis.com
   - People API: https://console.cloud.google.com/apis/api/people.googleapis.com
3. Configure OAuth consent screen: https://console.cloud.google.com/auth/branding
4. Create OAuth Desktop app client: https://console.cloud.google.com/auth/clients
5. Download `client_secret_*.json`

**Agent Authentication Setup**:
```bash
# Store credentials (one-time)
gog auth credentials ~/path/to/client_secret_....json

# Add account (opens browser for consent)
gog auth add you@gmail.com

# For headless/WSL (no browser on server)
gog auth add you@gmail.com --services user --manual
# Copy URL to browser, paste redirect URL back
```

[VERIFIED] (GOAC-SC-GH-README | https://github.com/steipete/gogcli)

### 4. Credential Storage for Agent Automation

**Problem**: Default keyring requires interactive password or OS keychain access.

**Solution for WSL/Agent use**:
```bash
# Use file backend instead of OS keychain
gog auth keyring file

# Set password via environment variable (non-interactive)
export GOG_KEYRING_PASSWORD='your-secure-password'
export GOG_ACCOUNT='you@gmail.com'
```

**Config location (WSL)**: `~/.config/gogcli/config.json`

[VERIFIED] (GOAC-SC-GH-README | https://github.com/steipete/gogcli)

### 5. Gmail Operations

**Search and Read**:
```bash
# Search recent emails
gog gmail search 'newer_than:7d' --max 10

# Search unread
gog gmail search 'is:unread' --max 20

# Get thread details
gog gmail thread get <threadId>

# Get with JSON output (for parsing)
gog --json gmail thread get <threadId>
```

**Download Attachments**:
```bash
# Download to specific directory
gog gmail thread get <threadId> --download --out-dir /path/to/attachments

# Single attachment
gog gmail attachment <messageId> <attachmentId> --out ./file.bin
```

**Send Emails**:
```bash
# Simple send
gog gmail send --to recipient@example.com --subject "Subject" --body "Body text"

# With HTML body
gog gmail send --to recipient@example.com --subject "Subject" --body-html "<p>HTML content</p>"

# Reply with quote
gog gmail send --reply-to-message-id <messageId> --quote --to recipient@example.com --subject "Re: ..." --body "Reply"
```

**Drafts**:
```bash
# Create draft
gog gmail drafts create --to recipient@example.com --subject "Draft" --body "Content"

# List drafts
gog gmail drafts list

# Send draft
gog gmail drafts send <draftId>
```

**Labels**:
```bash
# List labels
gog gmail labels list

# Modify thread labels
gog gmail thread modify <threadId> --add STARRED --remove INBOX
```

[VERIFIED] (GOAC-SC-GH-README | https://github.com/steipete/gogcli)

### 6. Calendar Operations

**List Events**:
```bash
# Today's events
gog calendar events primary --today

# This week
gog calendar events primary --week

# Next N days
gog calendar events primary --days 7

# Date range
gog calendar events primary --from 2025-01-15T00:00:00Z --to 2025-01-22T00:00:00Z
```

**Create Events**:
```bash
# Basic event
gog calendar create primary \
  --summary "Meeting" \
  --from 2025-01-15T10:00:00Z \
  --to 2025-01-15T11:00:00Z

# With attendees
gog calendar create primary \
  --summary "Team Sync" \
  --from 2025-01-15T14:00:00Z \
  --to 2025-01-15T15:00:00Z \
  --attendees "alice@example.com,bob@example.com" \
  --send-updates all

# Recurring event
gog calendar create primary \
  --summary "Weekly Standup" \
  --from 2025-01-15T09:00:00Z \
  --to 2025-01-15T09:30:00Z \
  --rrule "RRULE:FREQ=WEEKLY;BYDAY=MO"
```

**Update and Delete**:
```bash
# Update event
gog calendar update primary <eventId> --summary "Updated Title"

# Delete event
gog calendar delete primary <eventId>
```

**Free/Busy Check**:
```bash
gog calendar freebusy --calendars "primary" \
  --from 2025-01-15T00:00:00Z \
  --to 2025-01-16T00:00:00Z
```

**Google Meet Links**: [LIMITATION] Cannot be created directly via gogcli. The Google Calendar API requires `conferenceDataVersion` and `conferenceData` fields which gogcli does not currently expose. Workaround: Create event in Google Calendar web UI or use Google Meet API separately.

[VERIFIED] (GOAC-SC-GH-README | https://github.com/steipete/gogcli)

### 7. Tasks Operations

```bash
# List tasklists
gog tasks lists

# List tasks in a list
gog tasks list <tasklistId>

# Add task
gog tasks add <tasklistId> --title "Task title" --due 2025-02-01

# Add recurring task
gog tasks add <tasklistId> --title "Daily review" --due 2025-02-01 --repeat daily

# Mark complete
gog tasks done <tasklistId> <taskId>

# Undo completion
gog tasks undo <tasklistId> <taskId>
```

[VERIFIED] (GOAC-SC-GH-README | https://github.com/steipete/gogcli)

### 8. Drive Operations (for attachments)

```bash
# Download file
gog drive download <fileId> --out ./downloaded-file.bin

# List files
gog drive ls --max 20

# Search files
gog drive search "invoice" --max 20

# Upload file
gog drive upload ./path/to/file --parent <folderId>
```

[VERIFIED] (GOAC-SC-GH-README | https://github.com/steipete/gogcli)

### 9. Agent Automation Configuration

**Environment Variables**:
```bash
# Required for non-interactive use
export GOG_ACCOUNT='you@gmail.com'
export GOG_KEYRING_BACKEND='file'
export GOG_KEYRING_PASSWORD='secure-password'

# Optional: Restrict commands (sandboxing)
export GOG_ENABLE_COMMANDS='gmail,calendar,tasks,drive'
```

**JSON Output** (for parsing):
```bash
gog --json gmail search 'is:unread' --max 10 | jq '.threads[].id'
```

[VERIFIED] (GOAC-SC-GH-README | https://github.com/steipete/gogcli)

### 10. WSL Integration Pattern

**Calling from Windows PowerShell**:
```powershell
# Set environment and call
wsl bash -c 'export GOG_ACCOUNT="you@gmail.com" && export GOG_KEYRING_PASSWORD="pass" && gog gmail search "is:unread" --max 5'

# Or with persistent environment in .bashrc
wsl gog gmail search 'is:unread' --max 5
```

**Passwordless sudo** (user requirement): Not needed for gogcli itself. The tool runs in userspace and doesn't require sudo.

[VERIFIED] (GOAC-SC-GH-README | https://github.com/steipete/gogcli)

## Comparison: Native Windows vs WSL

**Native Windows Build**:
- Pros: Simpler invocation, no WSL overhead, direct file paths
- Cons: Requires Go toolchain installation, credential manager integration

**WSL Approach**:
- Pros: Linux environment, Homebrew available, matches dev workflows
- Cons: Path translation needed, extra layer, environment variable management

**Recommendation**: For agent automation, **native Windows build** is simpler. WSL adds unnecessary complexity unless other Linux tools are needed.

## Limitations and Known Issues

1. **Google Meet links**: Cannot be created via CLI (API limitation)
2. **Workspace-only features**: Chat, Keep, Groups require Google Workspace, not personal Gmail
3. **OAuth consent**: User must manually complete initial OAuth flow in browser
4. **Token refresh**: Tokens auto-refresh, but initial auth requires browser
5. **Headless auth**: `--manual` flag required for servers without browser

## Recommendations for Skill Creation

1. **Use native Windows build** unless other WSL dependencies exist
2. **Use file keyring backend** with `GOG_KEYRING_PASSWORD` for automation
3. **Store credentials** in user's home directory, not workspace
4. **Use JSON output** (`--json`) for all commands to enable parsing
5. **Document OAuth setup** thoroughly in SETUP.md (manual user step)
6. **Sandbox commands** with `GOG_ENABLE_COMMANDS` for security
7. **For Google Meet**: Note limitation, suggest using Calendar web UI or separate workflow

## Sources

- **GOAC-SC-GH-README**: https://github.com/steipete/gogcli (Accessed: 2026-03-04)
- **GOAC-SC-SITE-HOME**: https://gogcli.sh/ (Accessed: 2026-03-04)

## Document History

**[2026-03-04 15:55]**
- Initial INFO document created from MEPI research
- Corrected tool name from "gop" to "gogcli"
- Documented all major commands and limitations
