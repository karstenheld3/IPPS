---
trigger: always_on
---

# Core Conventions

Universal formatting and writing conventions for all documents.

## Text Style (Exception: transcribed or external documents)

- Use ASCII "double quotes" or 'single quotes'. Never use Non-ASCII quotes unless explicitly asked.
- No emojis in documentation (see Document Rule Exceptions below)
- Avoid Markdown tables; use unnumbered lists with indented properties (see Document Rule Exceptions below)
- Unicode box-drawing characters for structures:
  - Trees and flows: `├─>` `└─>` `│` (2-space indentation compatible)
  - Boxes and diagrams (non-UI): `┌─` `├─` `└─` `│` `─` `┐` `┤` `┘`
  - UI diagrams and designs: Keep ASCII `+` `-` `|` for compatibility and easy manual editing
- Never use `▼` (U+25BC); use `v` instead
- Fit single statements/decisions/objects on a single line
- Workflow references as inline code: `/verify`, `/go`, `/recap`

## Date and Time Format

- **In documents**: `YYYY-MM-DD HH:MM`
- **In logging**: `YYYY-MM-DD HH:MM:SS`
- **In filenames**: `YYYY-MM-DD` prefix - e.g. `2026-03-19_ServerMigration.md`
- **In session folders**: `YYYY-MM-DD` prefix - e.g. `_2026-03-19_FixAuthBug/`
- **In Document History**: `[YYYY-MM-DD HH:MM]` - e.g. `**[2026-03-19 14:30]**`

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

- Doc ID required for all documents
- Reference other docs by filename AND Doc ID: `_SPEC_CRAWLER.md [CRWL-SP01]`
- Omit optional fields if not applicable: Target file, Depends on, Does not depend on

## Document History Section

Always at document end, reverse chronological order:

```
## Document History

**[2026-01-12 14:30]**
- Added: "Scenario" section with Problem/Solution/What we don't want
- Changed: Placeholder standardized to `{itemId}` (camelCase)
- Fixed: Modal OK button signature

**[2026-01-12 10:00]**
- Initial specification created
```

**Action prefixes:** Added, Changed, Fixed, Removed, Moved

## Document Rule Exceptions

Opt-in via DevSystem tag as **first line** (before title):

```html
<DevSystem MarkdownTablesAllowed=true EmojisAllowed=true />
```

- `MarkdownTablesAllowed=true` - Allow Markdown tables
- `EmojisAllowed=true` - Allow emojis

**Table formatting rule:** Aligned columns using spaces. No bold/italic/formatting inside cells.
- BAD: `|Model|Workers|TPM|` (no spacing)
- BAD: `| **Model** | Workers |` (bold in cells)

**Allowed emojis (when enabled):** ✅ Yes/pass, ❌ No/fail, ⚠️ Warning/partial, ★ Filled star, ☆ Outlined star, ⯪ Half star

**Usage pattern:** Emoji first, then textual equivalent: `- **MCP** - ✅ Yes`

**When to use:** Comparison documents, feature matrices, status dashboards.

## Skill References

Format: `@skills:skill-name` (must match folder in `[AGENT_FOLDER]/skills/`)

**BAD:** `(write-documents skill)`, `the writing skill`
**GOOD:** `@skills:write-documents`

## APAPALAN Writing Principle

**APAPALAN** = As Precise As Possible (Priority 1), As Little As Necessary (Priority 2)

Applies to all written output. Full rules in `APAPALAN_RULES.md` (@skills:write-documents).

**Minimal subset (always apply):**
- **AP-PR-07**: Be specific - no "handles errors appropriately", say "retry 3 times with exponential backoff"
- **AP-PR-09**: Consistent patterns - same concept = same format everywhere
- **AP-BR-02**: Sacrifice grammar for brevity - drop articles, filler, verbose constructions
- **AP-NM-01**: One name per concept - no synonyms, no polysemy
- **AP-NM-05**: Use standard terms - don't invent new names for known concepts
- **AP-ST-01**: Goal first - reader knows WHY before HOW

## Temporary Files (.tmp prefix)

Files starting with `.tmp` are temporary helper scripts. Delete after use.

## Transcription Output

Transcribed content MUST contain only the original document's content. No processing metadata, agent annotations, or workflow artifacts.

**Text Style rules do NOT apply to transcribed content.** Transcriptions preserve the original exactly - including curly quotes, typos, unusual punctuation. Only markdown structural elements (headers, lists, emphasis) are agent-created.

**Prohibited in transcription output:** source filename/path/URL, page/figure counts, transcription timestamps, verification status, agent notes.

**Store metadata separately:** companion `[FILENAME]_meta.json` or session NOTES.md.