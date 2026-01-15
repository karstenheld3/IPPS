# Devil's Advocate Review: _INFO_AGENTIC_ENGLISH.md

**Reviewed**: 2026-01-15 16:57
**Context**: Review of Agentic English vocabulary document [AGEN-IN01]

## Critical Issues

None found.

## High Priority

None found.

## Medium Priority

### `AGEN-PR-001` Missing Table of Contents

- **Where**: Document structure
- **What**: No TOC section despite 200+ line document
- **Why it's wrong**: Core conventions require TOC after header block for navigability
- **Suggested fix**: Add TOC after header block

### `AGEN-PR-002` Duplicate Placeholder Definitions

- **Where**: Lines 78-103 (Placeholders section)
- **What**: `[ACTOR]` and folder paths defined here AND in `devsystem-core.md`
- **Why it's wrong**: Violates single source of truth - definitions could drift
- **Suggested fix**: Reference `devsystem-core.md` for core placeholders, only add AGEN-specific ones here

## Low Priority

### `AGEN-PR-003` Inconsistent Bracket Usage in Syntax Section

- **Where**: Lines 70-76 (Syntax section)
- **What**: `[VERB]` uses brackets but `STATE-NAME` does not
- **Why it's wrong**: Could cause confusion about when to use brackets
- **Suggested fix**: Add note explaining states don't use brackets because they're not action markers

### `AGEN-PR-004` Missing Cross-Reference to Phase Document

- **Where**: Document header
- **What**: No "See also" reference to `INFO_PROJECT_PHASES_OPTIONS.md [PHSE-IN01]`
- **Why it's wrong**: Verbs are used in phase hierarchies defined elsewhere
- **Suggested fix**: Add reference in header block

### `AGEN-PR-005` File Naming Convention

- **Where**: File name `_INFO_AGENTIC_ENGLISH.md`
- **What**: File uses two words in name
- **Why it's wrong**: Per @write-documents skill, INFO docs should be `_INFO_[TOPIC].md`
- **Suggested fix**: Keep as-is for readability, or consider `_INFO_AGENTEN.md`

## Style Issues

### `AGEN-PR-006` Examples Could Be More Concrete

- **Where**: Lines 49-54 (Documents section example)
- **What**: Generic examples like `[CONFIGURE] database connection`
- **Why it's wrong**: Real examples from existing docs would be more useful
- **Suggested fix**: Use actual examples from project SPEC/IMPL docs if available

## Questions That Need Answers

1. Should Agentic English be a **rule** (always-on) instead of INFO doc?
2. Should verbs be registered in a central registry like TOPICs?
3. What happens when a verb is deprecated or renamed?
4. Is there a process for adding new verbs?

## Devil's Advocate Summary

**Reviewed**: `_INFO_AGENTIC_ENGLISH.md [AGEN-IN01]`
**Time spent**: ~5 minutes

**Findings**:
- CRITICAL: 0
- HIGH: 0
- MEDIUM: 2
- LOW: 3
- STYLE: 1

**Top 3 Risks**:
1. Missing TOC makes 200+ line document hard to navigate
2. Duplicate placeholder definitions could drift from devsystem-core.md
3. Inconsistent bracket syntax could confuse users

**Files Created/Updated**:
- `_INFO_AGENTIC_ENGLISH_DA.md` - This file

**Recommendation**: PROCEED WITH CAUTION - Add TOC, clarify placeholder ownership
