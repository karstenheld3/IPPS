# Logging Rules

Language-agnostic output rules for Python, PowerShell, and future languages.

## Overview

Four logging types serve distinct audiences:
- **General (GN)** - Rules applying to all output types
- **User-Facing (UF)** - End users via console or SSE stream
- **App-Level (AP)** - Technical staff debugging via server logs
- **Script-Level (SC)** - QA verifying correctness via selftest output

## Related Documents

- `LOGGING-RULES-USER-FACING.md` - LOG-UF-01 to LOG-UF-06
- `LOGGING-RULES-APP-LEVEL.md` - LOG-AP-01 to LOG-AP-05
- `LOGGING-RULES-SCRIPT-LEVEL.md` - LOG-SC-01 to LOG-SC-07

## Logging Philosophy

### APAPALAN Principle

**As precise as possible, as little as necessary.** Maximum information, minimum words. Never ambiguous.

- BAD: `P=1`, `F1=1`
- GOOD: `Precision=1.00`, `F1-Score=1.00`

### Principle of Least Surprise

Logging must be predictable across all solutions. Same patterns, formats, structure everywhere.

### Principle of Full Disclosure

Each log line must be understandable without context. Include what is being processed, what action, and enough detail to assess complexity.

- BAD: `[ 1 / 2 ] LLM extraction run 1...`
- GOOD: `[ 1 / 2 ] Calling gpt-5-mini to extract 5 records from 20 rows...`

### Principle of Visible Structure

Break operations into numbered steps `[ x / n ]` so readers can assess progress, understand structure, and learn workflow by observation.

### Principle of Announce > Track > Report

Every activity follows three phases:
1. **Announce** - State what will happen with full disclosure
2. **Track** - Log progress with intermediate results as nested lines
3. **Report** - State final status and results

**Item-level status** (individual operations):
- `OK.` or `OK: <details>` | `SKIP: <why>` | `ERROR: <what> -> <system error>` | `WARNING: <problem>`

**Activity-level status** (whole activity):
- `OK.` or `OK: <results>` | `SKIP: <why>` | `FAIL: <summary>` | `PARTIAL FAIL: <summary>` | `WARNING: <problem>` | `HINT: <advice>`

**Final line rule:** Last line of any activity MUST contain a status keyword (`OK.`, `FAIL:`, `PARTIAL FAIL:`, `SKIP:`).

**Parallel execution rule:** Report lines MUST carry the same identifier as their Announce line.
- GOOD: `[ 1 / 2 ] OK. Extracted 5 correct...`

**Worker/process prefix rule:** Multiple workers/processes MUST prefix all lines with identity.
- Workers: `[ worker 1 ] [ 1 / 5 ] Processing 'file.pdf'...`
- Processes: `[timestamp,process 12345,request 1] START: function_name...`

**Not used for status:** `DONE`, `FINISHED`, `INFO`, `DEBUG`.

```
Connecting to 'https://contoso.sharepoint.com/sites/ProjectA'...
  OK. Connected in 1.2 secs.
Processing 3 libraries...
  [ 1 / 3 ] Processing library 'Documents'...
    342 files retrieved.
    OK.
  [ 2 / 3 ] Processing library 'Reports'...
    ERROR: Access denied -> (403) Forbidden
  [ 3 / 3 ] Processing library 'Archive'...
    SKIP: Library empty.
  FAIL: 2 libraries processed, 1 failed.
```

### Principle of Two-Level Errors (User-Facing)

**Format:** `<what failed> -> <system error>`

"What failed" is neutral (no blame). "System error" is exact from system.

```
Could not save user -> A user with this email already exists.
Could not connect to site -> (401) Unauthorized
```

### Arrow Convention

` -> ` is the universal separator for error chains, two-level errors, and transformations. Never use `-`, `:`, or other separators.

### Script-Level Goal

All failure information must be in the logs alone. Drives: no timestamps, comparison markers `[equal]`/`[different]`, complete error context, summary with counts.

### App-Level Goal

Human-readable AND machine-parseable. Drives: extended timestamps with PID, START/END markers, nested indentation, `key='value'` format, error chains.

### User-Facing Goal

Users must always know what is happening. Drives: simple timestamps, `[ x / n ]` progress, running counts, 100-char headers/footers, plain language.

## Philosophy-to-Rules Mapping

**Script-Level:** LOG-SC-01 (no timestamps), LOG-SC-04 (status markers), LOG-SC-03 (test case IDs), LOG-SC-07 (summary)

**App-Level:** LOG-AP-01 (extended timestamp), LOG-AP-04 (START/END), LOG-GN-02 (`key='value'`), LOG-AP-05 (error chains)

**User-Facing:** LOG-UF-02 (iteration counters), LOG-UF-04 (emit every ~10s), LOG-UF-03 (plain language), LOG-UF-06 (100-char headers)

## General Rules (LOG-GN)

### LOG-GN-01: Indentation

2 spaces per level. `INDENT = "  "`

```
Processing batch...
  Loading configuration...
    OK.
```

### LOG-GN-02: Quote Paths, Names, and IDs

Single quotes around file paths, resource names, identifiers.

```
Processing file 'report.csv'...
User 'admin@company.com' not found.
```

### LOG-GN-03: Numbers and Counters First

Results start with count. Iteration counters at line start.

- Top-level: `[ x / n ]` | Nested: `( x / n )`

```
5 records retrieved.
[ 1 / 5 ] Processing item...
( 50 / 127 ) Processing broken items...
```

**Exception:** Activity announcements describe action first: `Processing 5 items...`

### LOG-GN-04: Duration Format

Report duration for any process >30 seconds.

- Milliseconds: `245 ms` | Seconds: `1.5 secs` | Minutes: `2 mins 30 secs` | Hours: `1 hour 15 mins`

### LOG-GN-05: Singular/Plural

Handle correctly. Never use `(s)`.

```
3 files found.
1 item processed.
```

### LOG-GN-06: Property Format

`key='value'` for strings, `key=value` for numbers. Additional properties in parentheses.

```
Loading domain='AiSearch' from 'E:\domains\config.json'...
Processing library 'Documents' (id='045229b3-57de')...
ERROR: Failed to process 'Documents' (site='ProjectA', id='045229b3') -> Access denied
```

### LOG-GN-07: UNKNOWN Constant

`UNKNOWN = '[UNKNOWN]'` for missing values. Never use `None`, `''`, `?`, or `Unknown`.

### LOG-GN-08: Error Formatting

Concatenate nested errors with ` -> `. Also use for rename/transform. Additional info in parentheses.

```
Failed to upload file 'report.pdf' -> Connection refused -> Server timeout after 30s
Renaming 'site_001' -> 'site_001_archived'...
```

### LOG-GN-09: Log Before Execution

Always log BEFORE starting code that could hang. If it hangs, last log line shows where.

```
Connecting to 'https://sharepoint.com/sites/ProjectA'...
  OK. Connected in 1.2 secs.
```

### LOG-GN-10: Ellipsis Usage

`...` for ongoing actions only. Never on result lines.

- GOOD: `Processing files...` / `5 files found.`
- BAD: `5 files found...`

### LOG-GN-11: Sentence Endings

Activity announcements end with `...`. Results/statements end with `.`

```
Connecting to server...
5 files retrieved.
User 'admin@company.com' not found.
```

### LOG-GN-12: No Acronyms

Always spell out full term first: `Full Term (ACRONYM)`. Applies to env vars and config too.

- BAD: `OBO_ENABLED`, `Authenticating via OBO...`
- GOOD: `ON_BEHALF_OF_ENABLED`, `Authenticating via On Behalf Of (OBO)...`

## Complete Example

```
Connecting to 'https://contoso.sharepoint.com/sites/ProjectA'...
  OK. Connected in 1.2 secs.
Loading libraries...
  3 libraries found.
  OK.
Processing 3 libraries...
  [ 1 / 3 ] Processing library 'Documents'...
    Scanning files...
    ( 100 / 342 ) items retrieved...
    ( 200 / 342 ) items retrieved...
    342 files retrieved.
    12 added, 3 changed, 0 removed.
    OK.
  [ 2 / 3 ] Processing library 'Reports'...
    Scanning files...
    45 files retrieved.
    ERROR: Failed to process file 'budget.xlsx' -> Access denied -> User lacks read permission
  [ 3 / 3 ] Processing library 'Archive'...
    SKIP: Library empty.
  PARTIAL FAIL: 2 libraries processed, 1 failed.
Renaming 'site_backup' -> 'site_backup_2026-03-04'...
  OK.
```