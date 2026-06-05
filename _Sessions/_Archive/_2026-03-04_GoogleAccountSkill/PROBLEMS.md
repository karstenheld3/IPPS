# Session Problems

**Doc ID**: GOAC-PROBLEMS

## Open

### GOAC-PR-001: WSL Integration for gop CLI

**Status**: Open
**Description**: `gop` CLI only runs on Linux/WSL. Need to create robust WSL wrapper for Windows usage.
**Requirements**:
- Detect if WSL is installed
- Verify default WSL distro
- Ensure passwordless sudo for automation
- Wrap all gop commands with `wsl` invocation

### GOAC-PR-002: SETUP.md Installation Workflow

**Status**: Open
**Description**: Create comprehensive SETUP.md that guides agent through installation.
**Requirements**:
- WSL installation/verification
- Go installation in WSL
- gop CLI installation
- Google OAuth setup (client credentials)
- Token acquisition workflow
- Passwordless sudo configuration

### GOAC-PR-003: Gmail Feature Coverage

**Status**: Open
**Description**: Implement all Gmail features provided by gop.
**Requirements**:
- Check/read emails
- Write emails and drafts
- Download attachments to `[TOOLS_FOLDER]\_downloaded_attachments`
- Search/filter emails

### GOAC-PR-004: Calendar Feature Coverage

**Status**: Open
**Description**: Implement Calendar features with Google Meet integration.
**Requirements**:
- Read calendar items
- Write/create calendar items
- Add Google Meet links to events
- List upcoming events

### GOAC-PR-005: UNINSTALL.md Conservative Workflow

**Status**: Open
**Description**: Create uninstall workflow following ms-playwright-mcp pattern.
**Requirements**:
- Show current state of all components
- Tiered removal options (config only, credentials, gop, WSL)
- WSL marked as potentially needed by other apps
- Backup important files before removal

## Resolved

## Deferred

## Document History

**[2026-03-04 15:48]**
- Initial problems derived from user request
