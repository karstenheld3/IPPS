---
trigger: always_on
---

# Core Conventions

Universal formatting and writing conventions for all documents.

## Text Style

- Use ASCII "double quotes" or 'single quotes'. Never use Non-ASCII quotes unless explicitly asked.
- No emojis in documentation (exception: UI may use limited set)
- Avoid Markdown tables; use unnumbered lists with indented properties to avoid unreadable rendering
- Use Unicode box-drawing characters for structures:
  - Trees and flows: `├─>` `└─>` `│` (2-space indentation compatible)
  - Boxes and diagrams (non-UI): `┌─` `├─` `└─` `│` `─` `┐` `┤` `┘`
  - UI diagrams: Keep ASCII `+` `-` `|` for compatibility and easy manual editing
- Try to fit single statements/decisions/objects on a single line

## Document Structure

- Place Table of Contents after header block (or after MUST-NOT-FORGET if present)
- No `---` markers between sections
- One empty line between sections
- Most recent changes at top in changelog sections

## Header Block

All documents start with:

```
# [Document Type]: [Title]

**Goal**: Single sentence describing purpose
**Target file**: `/path/to/file.py` (or list for multiple)

**Depends on:**
- `_SPEC_[X].md` for [what it provides]

**Does not depend on:**
- `_SPEC_[Y].md` (explicitly exclude if might seem related)
```

Only include "Depends on" / "Does not depend on" if they have items.

## Spec Changes Section

Always at document end, reverse chronological order:

```
## Spec Changes

**[2026-01-12 14:30]**
- Added: "Scenario" section with Problem/Solution/What we don't want
- Changed: Placeholder standardized to `{itemId}` (camelCase)
- Fixed: Modal OK button signature

**[2026-01-12 10:00]**
- Initial specification created
```

**Action prefixes:** Added, Changed, Fixed, Removed, Moved

## Proper English

**RULE:** When a modifier (clause or phrase) can attach to multiple nouns, split into separate sentences.

**BAD:**
```
Files starting with '!' signify high relevance that must be treated with extra attention.
```

**GOOD:**
```
Files starting with '!' indicate high relevance. This information must be treated with extra attention.
```
