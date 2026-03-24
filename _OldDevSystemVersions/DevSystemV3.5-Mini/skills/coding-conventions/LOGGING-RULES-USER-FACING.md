# User-Facing Logging Rules

Rules for end-user visible output via console or Server-Sent Events (SSE) stream.

## Philosophy

Goal: Users must always know what is happening.

- Numbered steps `[ x / n ]` reveal workflow structure
- Progress indication via iteration counters and running totals
- Feedback every ~10 seconds for long operations
- Plain language non-technical users can follow
- Full Disclosure: Every log section self-contained - include filenames, URLs, identifiers

MUST NOT use log levels: Never use `INFO`, `DEBUG`, `WARN` prefixes. User-facing logs use plain language with status keywords: `OK`, `FAIL`, `PARTIAL FAIL`, `SKIP`/`SKIPPED`, `ERROR:`, `WARNING:`, `HINT:`.

## Related Documents

- `LOGGING-RULES.md` - General rules (LOG-GN-01 to LOG-GN-11)
- `LOGGING-RULES-APP-LEVEL.md` - App-level rules (LOG-AP-01 to LOG-AP-05)
- `LOGGING-RULES-SCRIPT-LEVEL.md` - Script-level rules (LOG-SC-01 to LOG-SC-07)

## Rules

### LOG-UF-01: Timestamp Format

Use `[YYYY-MM-DD HH:MM:SS]`. Always include date AND time. No process ID, no milliseconds.

```
[2026-03-04 10:15:23] Starting scan...
[2026-03-04 10:15:24] Connecting to site...
[2026-03-04 10:15:25]   3 libraries found.
```

### LOG-UF-02: Progress Indicators

Iteration: `[ x / n ]` with spaces, at line start.

```
[ 1 / 5 ] Processing 'Document A'...
[ 2 / 5 ] Processing 'Document B'...
```

Retry: `( x / n )` inline or indented subitem.

```
Uploading file 'report.pdf'...
  ( 1 / 3 ) Connection timeout, retrying...
  ( 2 / 3 ) Connection timeout, retrying...
  ( 3 / 3 ) Upload successful.
```

Running count: `( x / n )` for long retrievals.

```
( 100 / 342 ) items retrieved...
( 200 / 342 ) items retrieved...
342 files retrieved.
```

Waiting: Show delay reason and attempt count.

```
( 1 / 3 ) Waiting 30 seconds for rate limit...
( 2 / 3 ) Waiting 30 seconds for rate limit...
Resuming upload...
```

### LOG-UF-03: Messages and Results

Plain language. No technical jargon.

```
Scan complete: 156 users found.
Could not save user -> A user with this email already exists.
Request queued -> Server busy, retrying in 30 seconds.
```

Actionable errors: Two-level format - defensive summary + exact error.

```
Could not connect to server -> Connection refused
File not found -> ENOENT - No such file or directory
Access denied to resource -> (403) Forbidden
```

Skipping: Always explain why.

```
SKIP: 12 files not embeddable.
SKIP: 1 file exceeds size limit (>100MB).
```

File operations: Show what is being written.

```
Writing 152 lines to '01_SiteContents.csv'...
  OK: File '01_SiteContents.csv' written.
```

Summary: Always end with counts using activity-level status keywords.

```
OK. 3 libraries processed. 56 added, 3 changed.
PARTIAL FAIL: 2 libraries processed, 1 failed.
FAIL: Could not complete export -> Connection lost.
```

Destructive operations: Multi-line warning with details.

```
IMPORTANT: This script will permanently DELETE all versions
- except for the newest version
- except if the time to the next version is more than 15 minutes
Press any key to continue...
```

### LOG-UF-04: Feedback Timing

Emit progress at least every ~10 seconds for long operations. Users must never wonder if system is stuck.

*BAD*: 2 minutes silence between start and complete.

*GOOD*:
```
[2026-03-04 10:15:23] Starting large file download...
[2026-03-04 10:15:33]   10% downloaded (12MB / 120MB)...
[2026-03-04 10:15:43]   20% downloaded (24MB / 120MB)...
...
[2026-03-04 10:17:45] Download complete. 120MB in 2 mins 22 secs.
```

### LOG-UF-05: Context Display

Show hierarchy so users understand position in operation.

```
Site: 'https://contoso.sharepoint.com/sites/ProjectA'
  Library: 'Shared Documents'
    Folder: 'Reports/2026'
      Processing 42 files...
```

With iteration:
```
Job [ 1 / 5 ] 'https://contoso.sharepoint.com/sites/ProjectA'
  Connecting to site...
  Loading subsites...
  3 subsites found.
    ( 1 / 3 ) Subsite 'https://contoso.sharepoint.com/sites/ProjectA/TeamB'
      4 lists found.
```

### LOG-UF-06: Activity Boundaries

All user-facing output and standalone scripts MUST use 100-character START/END headers and footers.

```
============================== START: SHAREPOINT PERMISSION SCANNER ==============================
2026-03-04 14:30:00

[... script output ...]

================================ END: SHAREPOINT PERMISSION SCANNER ================================
2026-03-04 14:35:23 (5 mins 23 secs)
```

Simple operations within scripts use indentation and status keywords, no additional markers.

Note: App-Level logging uses simple `START:` / `END:` markers per LOG-AP-04.

## Complete Examples

### Example 1: SharePoint Scan

```
[2026-03-04 14:30:00] Crawling site 'https://contoso.sharepoint.com/sites/ProjectA'...
[2026-03-04 14:30:01]   3 libraries found.
[2026-03-04 14:30:01] [ 1 / 3 ] Processing 'Documents'...
[2026-03-04 14:30:02]   ( 100 / 342 ) items retrieved...
[2026-03-04 14:30:03]   ( 200 / 342 ) items retrieved...
[2026-03-04 14:30:04]   342 files retrieved.
[2026-03-04 14:30:04]   12 added, 3 changed, 0 removed.
[2026-03-04 14:30:04]   OK.
[2026-03-04 14:30:05] [ 2 / 3 ] Processing 'Reports'...
[2026-03-04 14:30:06]   45 files retrieved.
[2026-03-04 14:30:06]   OK.
[2026-03-04 14:30:07] [ 3 / 3 ] Processing 'Archive'...
[2026-03-04 14:30:07]   SKIP: Library empty.
[2026-03-04 14:30:08] OK. 2 libraries processed. 57 added, 3 changed.
[2026-03-04 14:30:08] Crawl complete in 8.0 secs.
```

### Example 2: File Upload with Retry

```
[2026-03-04 10:00:00] Uploading 5 files to 'Documents'...
[2026-03-04 10:00:01] [ 1 / 5 ] Uploading 'report.pdf'...
[2026-03-04 10:00:02]   ( 1 / 3 ) Connection timeout, retrying...
[2026-03-04 10:00:05]   ( 2 / 3 ) Connection timeout, retrying...
[2026-03-04 10:00:08]   ( 3 / 3 ) Upload successful.
[2026-03-04 10:00:08] [ 2 / 5 ] Uploading 'data.xlsx'...
[2026-03-04 10:00:09]   OK.
[2026-03-04 10:00:12] [ 4 / 5 ] Uploading 'archive.zip'...
[2026-03-04 10:00:13]   SKIP: File too large (>100MB).
[2026-03-04 10:00:15]   OK.
[2026-03-04 10:00:15] 4 files uploaded, 1 skipped.
```

### Example 3: Permission Scanner

```
Job [ 1 / 5 ] 'https://contoso.sharepoint.com/sites/ProjectA'
  Connecting to 'https://contoso.sharepoint.com/sites/ProjectA'...
  Loading subsites...
  3 subsites found.
  Loading site groups...
  8 groups found in site collection.
    4 lists found.
    5420 items found, 127 with broken permissions.
      ( 50 / 127 ) Processing broken items...
      ( 100 / 127 ) Processing broken items...
    152 lines written to: '01_SiteContents.csv'
  OK: File '02_SiteGroups.csv' written.
Job [ 2 / 5 ] 'https://contoso.sharepoint.com/sites/ProjectB'
  Connecting to 'https://contoso.sharepoint.com/sites/ProjectB'...
  FAIL: (401) Unauthorized
```