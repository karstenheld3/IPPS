---
name: google-account
description: Apply when interacting with Google services (Gmail, Calendar, Drive, Tasks) via gogcli CLI
---

# Google Account Skill (gogcli)

## Prerequisites Check (RUN FIRST)

```powershell
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; gog --version"
```

If `gog` not found: Follow [SETUP.md](SETUP.md) completely. Do NOT improvise.
If auth fails: Follow [Token Expiry Re-Auth Flow](#token-expiry-re-auth-flow).

## MUST-NOT-FORGET

- Tool is `gog` (from gogcli package), NOT `gop`
- WSL PATH is broken by default - Always include full PATH export (see command template below)
- If `gog` not installed: Follow SETUP.md, do NOT improvise installation
- If token expired: Follow [Token Expiry Re-Auth Flow](#token-expiry-re-auth-flow)
- Use `--json` flag for all commands to enable parsing
- Set `GOG_ACCOUNT` environment variable for non-interactive use
- Use `GOG_KEYRING_PASSWORD` with file backend for automation
- Google Meet links cannot be created via CLI (API limitation)
- Attachments download to specified `--out-dir`, default is current directory

### Command Template (ALWAYS USE)

```powershell
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; export GOG_KEYRING_PASSWORD='<PASSWORD>'; export GOG_ACCOUNT='<EMAIL>'; gog <command>"
```

Get config from `[WORKSPACE_FOLDER]/!NOTES.md` - Look for "gogcli" section with account and keyring password.

## Intent Lookup

- Check unread emails -> `gog gmail search 'is:unread' --max 20`
- Read specific email -> `gog gmail thread get <threadId>`
- Download attachments -> `gog gmail thread get <threadId> --download --out-dir ./attachments`
- Send email -> `gog gmail send --to <email> --subject "..." --body "..."`
- Create draft -> `gog gmail drafts create --to <email> --subject "..." --body "..."`
- See today's calendar -> `gog calendar events primary --today`
- Create calendar event -> `gog calendar create primary --summary "..." --from <datetime> --to <datetime>`
- Add attendees -> Include `--attendees "email1,email2" --send-updates all`
- Check availability -> `gog calendar freebusy --calendars "primary" --from <start> --to <end>`
- List tasks -> `gog tasks lists` then `gog tasks list <tasklistId>`
- Add task -> `gog tasks add <tasklistId> --title "..." --due <date>`
- Mark task done -> `gog tasks done <tasklistId> <taskId>`
- Download from Drive -> `gog drive download <fileId> --out ./file.bin`
- Search Drive -> `gog drive search "query" --max 20`

## Tool: gogcli

Command structure: `gog [--json] [--account <email>] <service> <command> [options]`

Services: Gmail (search, read, send, drafts, labels, attachments, filters), Calendar (CRUD, free/busy, reminders, recurrence), Drive (upload, download, organize, share), Tasks (CRUD, due dates, recurring), Contacts, Sheets/Docs/Slides, Forms, Apps Script, People, Chat/Groups (Workspace-only)

## Gmail Operations

```bash
gog --json gmail search 'is:unread' --max 20
gog --json gmail thread get <threadId>
gog gmail thread get <threadId> --download --out-dir [TOOLS_FOLDER]/_downloaded_attachments
gog gmail attachment <messageId> <attachmentId> --out ./file.bin
gog gmail send --to recipient@example.com --subject "Subject" --body "Body text"
gog gmail send --to recipient@example.com --subject "Subject" --body-html "<p>HTML</p>"
gog gmail send --reply-to-message-id <messageId> --quote --to recipient@example.com --subject "Re: ..." --body "Reply"
gog gmail drafts create --to recipient@example.com --subject "Draft" --body "Content"
gog gmail drafts list
gog gmail drafts send <draftId>
gog gmail labels list
gog gmail thread modify <threadId> --add STARRED --remove INBOX
```

## Calendar Operations

```bash
gog --json calendar events primary --today
gog --json calendar events primary --week
gog --json calendar events primary --days 7
gog --json calendar events primary --from 2025-01-15T00:00:00Z --to 2025-01-22T00:00:00Z
gog calendar create primary --summary "Meeting" --from 2025-01-15T10:00:00Z --to 2025-01-15T11:00:00Z
gog calendar create primary --summary "Team Sync" --from 2025-01-15T14:00:00Z --to 2025-01-15T15:00:00Z --attendees "alice@example.com,bob@example.com" --send-updates all
gog calendar create primary --summary "Weekly Standup" --from 2025-01-15T09:00:00Z --to 2025-01-15T09:30:00Z --rrule "RRULE:FREQ=WEEKLY;BYDAY=MO"
gog calendar create primary --summary "Payment" --from 2025-02-11T09:00:00Z --to 2025-02-11T09:15:00Z --reminder "email:1d" --reminder "popup:30m"
gog calendar update primary <eventId> --summary "Updated Title"
gog calendar delete primary <eventId>
gog --json calendar freebusy --calendars "primary" --from 2025-01-15T00:00:00Z --to 2025-01-16T00:00:00Z
```

## Tasks Operations

```bash
gog --json tasks lists
gog --json tasks list <tasklistId>
gog tasks add <tasklistId> --title "Task title" --due 2025-02-01
gog tasks add <tasklistId> --title "Daily review" --due 2025-02-01 --repeat daily
gog tasks done <tasklistId> <taskId>
gog tasks undo <tasklistId> <taskId>
```

## Drive Operations

```bash
gog --json drive ls --max 20
gog --json drive search "invoice" --max 20
gog drive download <fileId> --out ./downloaded-file.bin
gog drive upload ./path/to/file --parent <folderId>
```

## Configuration

```bash
export GOG_ACCOUNT='you@gmail.com'
export GOG_KEYRING_BACKEND='file'
export GOG_KEYRING_PASSWORD='secure-password'
export GOG_ENABLE_COMMANDS='gmail,calendar,tasks,drive'  # Optional sandboxing
```

Config locations: Linux/WSL `~/.config/gogcli/config.json` | Windows `%AppData%\gogcli\config.json` | macOS `~/Library/Application Support/gogcli/config.json`

## Limitations

1. Google Meet links cannot be created via CLI (API limitation)
2. Chat, Keep, Groups require Google Workspace
3. Initial OAuth requires browser (use `--manual` for headless)
4. Tokens auto-refresh but initial auth needs browser

## Token Expiry Re-Auth Flow

When `"invalid_grant" "Token has been expired or revoked"`:

Step 1: Start auth, capture OAuth URL:
```powershell
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; export GOG_KEYRING_PASSWORD='<PASSWORD>'; gog auth add <EMAIL> --manual --force" 2>&1 | Select-String -Pattern 'state=' | ForEach-Object { $_.Line }
```

Step 2: Navigate to OAuth URL with Playwright MCP

Step 3: Click through consent (account > "Continue" if unverified app > "Continue" on consent > localhost redirect with ERR_CONNECTION_REFUSED is expected)

Step 4: Capture redirect URL via `mcp1_browser_network_requests({ includeStatic: false })` - look for `http://127.0.0.1:<PORT>/oauth2/callback?state=...&code=...`

Step 5: Complete auth:
```powershell
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; export GOG_KEYRING_PASSWORD='<PASSWORD>'; echo '<REDIRECT_URL>' | gog auth add <EMAIL> --manual --force"
```

Step 6: Verify with `gog --json gmail search 'is:unread' --max 3`

## Common Mistakes

1. WSL PATH Not Set (`gog: command not found`): Always use full PATH export
2. State Mismatch: Redirect URL `state=` must match current auth session. Start fresh if mismatched.
3. Invalid Client ID (`Error 401: invalid_client`): Get correct client_id from client secret file:
   ```powershell
   Get-Content "<CLIENT_SECRET_PATH>" | ConvertFrom-Json | Select-Object -ExpandProperty installed | Select-Object client_id
   ```
   Client secret path in `[WORKSPACE_FOLDER]/!NOTES.md` under "gogcli" section.
4. Terminal Truncates OAuth URL: Use Playwright MCP to navigate directly with client_id from JSON.
5. Port Mismatch: gogcli uses random port each session. Always capture redirect URL from same auth session via `mcp1_browser_network_requests`.