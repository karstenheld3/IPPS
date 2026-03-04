# Session Notes

**Doc ID**: GOAC-NOTES
**Started**: 2026-03-04
**Goal**: Create a Cascade skill for Google account interaction (Gmail, Calendar) using `gop` CLI via WSL

## Current Phase

**Phase**: EXPLORE
**Workflow**: (pending assessment)
**Assessment**: (pending)

## User Prompts

### Initial Request (2026-03-04)

I want to create a skill for cascade to interact with my google account. primarily gmail.

Since the gop cli only runs on wsl we need to make it work with WSL on windows. and we need a robust SETUP.md file that helps the agent install everything. the default wsl user should have no password otherwise the agent will not be able to use it.

I want all main features covered in the skill:
- check and read emails
- write emails and drafts
- download attachments to [TOOLS_FOLDER]\_downloaded_attachments
- read and write calendar items, add google meet links
- anything useful that gop provides

we also need an UNINSTALL.md workflow that is conservative and asks the user what to remove. WSL might be needed by other apps for example.

Read to understand strategy: ms-playwright-mcp/UNINSTALL.md

## Key Decisions

- **Tool name corrected**: User said "gop CLI" - actual tool is **`gogcli`** (command: `gog`)
- **Installation approach**: Native Windows build recommended over WSL (simpler)
- **Google Meet limitation**: Cannot create Meet links via CLI (API limitation)

## Important Findings

- **gogcli** supports: Gmail, Calendar, Drive, Tasks, Contacts, Sheets, Docs, Slides, Forms, Apps Script
- **Auth**: Requires user's own OAuth2 Desktop app credentials from Google Cloud Console
- **Agent automation**: Use file keyring backend + `GOG_KEYRING_PASSWORD` environment variable
- **JSON output**: All commands support `--json` for parsing
- **Sandboxing**: `GOG_ENABLE_COMMANDS` restricts available commands

## IMPORTANT: Cascade Agent Instructions

- **WSL Integration**: `gop` CLI runs in WSL only; all commands must be wrapped with `wsl` invocation
- **Passwordless sudo**: Default WSL user must have no password for agent automation
- **SETUP.md**: Must guide agent through complete installation (WSL, gop, OAuth setup)
- **UNINSTALL.md**: Conservative approach - show current state, offer tiered removal options (like ms-playwright-mcp pattern)
- **Attachments**: Download to `[TOOLS_FOLDER]\_downloaded_attachments`
- **Reference**: Use `ms-playwright-mcp` skill structure as template

## Workflows to Run on Resume

1. `/prime` - Load workspace context
2. Review PROBLEMS.md for open items
3. Continue with current phase

## Document History

**[2026-03-04 15:48]**
- Initial session created
- Recorded user prompt verbatim
