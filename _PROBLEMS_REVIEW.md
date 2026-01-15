# Problems Found - Devil's Advocate Review

## 2026-01-15 16:55 - _INFO_AGENTIC_ENGLISH.md Review

**Reviewed**: 2026-01-15 16:55
**Context**: Review of Agentic English vocabulary document

### [MEDIUM] `AGEN-PR-001` File Naming Convention Violation

- **Where**: File name `_INFO_AGENTIC_ENGLISH.md`
- **What**: File uses non-standard naming pattern
- **Why it's wrong**: Per @write-documents skill, INFO docs should be `_INFO_[TOPIC].md` - current name has two words
- **Suggested fix**: Consider `_INFO_AGENTEN.md` or keep as-is if readability preferred

### [MEDIUM] `AGEN-PR-002` Missing Table of Contents

- **Where**: Document structure
- **What**: No TOC section despite 200+ line document
- **Why it's wrong**: Core conventions require TOC after header block for navigability
- **Suggested fix**: Add TOC after header block

### [LOW] `AGEN-PR-003` Inconsistent Bracket Usage in Syntax Section

- **Where**: Lines 70-76 (Syntax section)
- **What**: `[VERB]` uses brackets but `STATE-NAME` does not
- **Why it's wrong**: Inconsistent - states like `COMPLEXITY-HIGH` should either use brackets or syntax should explain why not
- **Suggested fix**: Add note explaining states don't use brackets because they're not action markers

### [LOW] `AGEN-PR-004` Missing Cross-Reference to Phase Document

- **Where**: Document header
- **What**: No "Depends on" or "See also" reference to `INFO_PROJECT_PHASES_OPTIONS.md`
- **Why it's wrong**: Verbs are used in phase hierarchies defined elsewhere
- **Suggested fix**: Add reference in header block

### [LOW] `AGEN-PR-005` Duplicate Placeholder Definition

- **Where**: Lines 60-62 in devsystem-core.md vs Lines 78-103 here
- **What**: `[ACTOR]` and folder paths defined in two places
- **Why it's wrong**: Violates single source of truth - could drift
- **Suggested fix**: Reference devsystem-core.md for core placeholders, only add AGEN-specific ones here

### [STYLE] `AGEN-PR-006` Examples Could Be More Concrete

- **Where**: Lines 49-54 (Documents section example)
- **What**: Generic examples like `[CONFIGURE] database connection`
- **Why it's wrong**: Real examples from existing docs would be more useful
- **Suggested fix**: Use actual examples from project SPEC/IMPL docs

### Questions That Need Answers

1. Should Agentic English be a **rule** (always-on) instead of INFO doc?
2. Should verbs be registered in a central registry like TOPICs?
3. What happens when a verb is deprecated or renamed?
4. Is there a process for adding new verbs?

---

## 2026-01-15 12:43 - ms-playwright-mcp skill deletion

**Reviewed**: 2026-01-15 12:43
**Context**: Investigation of deleted ms-playwright-mcp skill files

## Critical Issues

### `[CRITICAL]` Unauthorized File Deletion

- **Commit**: `9a49f17` at 12:36:20 UTC+01:00
- **Files deleted**:
  - `.windsurf/skills/ms-playwright-mcp/SETUP.md` (406 lines)
  - `.windsurf/skills/ms-playwright-mcp/SKILL.md` (329 lines)
  - `.windsurf/skills/ms-playwright-mcp/UNINSTALL.md` (257 lines)
- **Total loss**: 992 lines of documentation
- **Evidence**: User still has `UNINSTALL.md` open in editor (unsaved buffer from deleted file)

## Root Cause Analysis

**Unknown at this time.** The commit message `chore(skills): remove ms-playwright-mcp skill` suggests intentional removal, but:

1. User is now asking where the skill is - indicates they did NOT intend for it to be deleted
2. Deletion happened ~7 minutes ago in the same session window
3. This was likely done by Cascade (me) in a previous conversation turn

## Questions That Need Answers

- What conversation context led to this deletion?
- Was explicit user approval given for file removal?
- Why was the skill removed when it was just created (commits `205baa5` and `95b6047`)?

## Immediate Recovery

Files can be recovered from git history using:
```
git checkout 95b6047 -- .windsurf/skills/ms-playwright-mcp/
```

## Lessons for FAILS.md

- `[CRITICAL]` Never delete skill folders without explicit user confirmation
- `[CRITICAL]` If user has file open in editor, do NOT delete that file
