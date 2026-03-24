---
trigger: always_on
---

# Core Conventions

Universal formatting and writing conventions for all documents.

## Text Style (Exception: transcribed or external documents)

- Use ASCII "double quotes" or 'single quotes'. Never Non-ASCII quotes unless explicitly asked.
- No emojis in documentation (see Document Rule Exceptions)
- Avoid Markdown tables; use unnumbered lists with indented properties (see Document Rule Exceptions)
- Unicode box-drawing for structures:
  - Trees/flows: `├─>` `└─>` `│` (2-space indentation compatible)
  - Boxes/diagrams (non-UI): `┌─` `├─` `└─` `│` `─` `┐` `┤` `┘`
  - UI diagrams: ASCII `+` `-` `|` for compatibility
- Never use `▼` (U+25BC); use `v` instead
- Fit single statements/decisions/objects on one line
- Workflow references as inline code: `/verify`, `/go`, `/recap`

## Date and Time Format

- **Documents**: `YYYY-MM-DD HH:MM` - `2026-03-19 14:30`
- **Logging**: `YYYY-MM-DD HH:MM:SS` - `2026-03-19 14:30:23`
- **Filenames**: `YYYY-MM-DD` prefix - `2026-03-19_ServerMigration.md`
- **Session folders**: `YYYY-MM-DD` prefix - `_2026-03-19_FixAuthBug/`
- **Document History**: `[YYYY-MM-DD HH:MM]` - `**[2026-03-19 14:30]**`

Never use locale-dependent formats (`03/19/2026`, `19.03.2026`, `March 19, 2026`).

## Document Structure

- TOC after header block (or after MUST-NOT-FORGET if present)
- No `---` markers between sections
- One empty line between sections
- Most recent changes at top in changelog sections

## Header Block

```
# [Document Type]: [Title]

**Doc ID**: [TOPIC]-[TYPE][NN]
**Goal**: Single sentence describing purpose
**Target file**: `/path/to/file.py` (or list for multiple)

**Depends on:**
- `_SPEC_[X].md [TOPIC-SP01]` for [what it provides]

**Does not depend on:**
- `_SPEC_[Y].md [TOPIC-SP02]` (explicitly exclude if might seem related)
```

Doc ID required. Reference docs by filename AND Doc ID: `_SPEC_CRAWLER.md [CRWL-SP01]`. Omit optional fields if N/A.

## Document History Section

Always at document end, reverse chronological. Action prefixes: Added, Changed, Fixed, Removed, Moved

```
## Document History

**[2026-01-12 14:30]**
- Added: "Scenario" section with Problem/Solution/What we don't want
- Changed: Placeholder standardized to `{itemId}` (camelCase)
```

## Document Rule Exceptions

Opt-in via first line (before title): `<DevSystem MarkdownTablesAllowed=true EmojisAllowed=true />`

**Tables (when allowed):** Aligned columns, spaces for readability. No bold/italic in cells.
- BAD: `|Model|Workers|` (no spacing) or `| **Model** |` (bold in cells)

**Allowed emojis (when enabled):** ✅ Yes/pass, ❌ No/fail, ⚠️ Warning/partial, ★ Filled star, ☆ Outlined star, ⯪ Half star. Pattern: emoji first, then text equivalent.

Use exceptions for: comparison docs, feature matrices, status dashboards.

## Skill References

Format: `@skills:skill-name` (must match folder in `[AGENT_FOLDER]/skills/`).
- BAD: `(write-documents skill)`, `the writing skill`
- GOOD: `@skills:write-documents`

## APAPALAN Writing Principle

All output follows `APAPALAN_RULES.md` (@skills:write-documents): precision first, then brevity.

## Temporary Files (.tmp prefix)

Files starting with `.tmp` are temporary helper scripts. Delete after use. Example: `.tmp_fix_quotes.ps1`

## Transcription Output

Transcribed content MUST contain only original document content. Text Style rules do NOT apply - preserve original exactly (curly quotes, typos, formatting).

**Prohibited in transcription output:**
- Source filename, path, or URL
- Page counts, figure counts, or statistics
- Transcription date or processing timestamps
- Verification status or progress markers
- Agent notes or processing comments

Store metadata separately: companion `[FILENAME]_meta.json` or session NOTES.md.