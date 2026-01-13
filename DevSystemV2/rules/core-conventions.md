---
trigger: always_on
---

# Core Conventions

Universal formatting and writing conventions for all documents.

## Text Style

- Use ASCII "double quotes" or 'single quotes', not "typographic quotes"
- No emojis in documentation (exception: UI may use limited set)
- Avoid Markdown tables; use unnumbered lists with indented properties
- Use Unicode box-drawing characters (├── └── │) for tree structures
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

## ID System

Use consistent IDs for traceability. All documents and items must have unique IDs.

**Topic:** 2-4 uppercase letters describing component (e.g., `CRWL` for Crawler, `AUTH` for Authentication)

### Document IDs

Every document MUST have an ID in its header block.

**Format:** `[TOPIC]-[DOC][NN]`

**Document Types:**
- `IN` - INFO document
- `SP` - SPEC document
- `IP` - Implementation Plan
- `TP` - Test Plan

**Examples:**
- `AUTH-IN01` - Authentication Info doc 1
- `CRWL-SP01` - Crawler Spec 1
- `V2CR-IP01` - V2 Crawler Implementation Plan 1
- `V2CR-TP01` - V2 Crawler Test Plan 1

### Spec-Level Item IDs (FR, IG, DD)

Defined in SPECs, referenced across IMPL and TEST plans.

**Format:** `[TOPIC]-[TYPE]-[NUMBER]`

**Types:**
- `FR` - Functional Requirement
- `IG` - Implementation Guarantee
- `DD` - Design Decision

**Examples:**
- `CRWL-FR-01` - Crawler Functional Requirement 1
- `CRWL-DD-03` - Crawler Design Decision 3
- `AUTH-IG-02` - Authentication Implementation Guarantee 2

### Plan-Level Item IDs (EC, IS, VC, TC)

Local to IMPL and TEST plans. Do NOT use in SPECs.

**Format:** `[TOPIC]-[DOC][NN]-[TYPE]-[NUMBER]`

**Types:**
- `EC` - Edge Case
- `IS` - Implementation Step
- `VC` - Verification Checklist item
- `TC` - Test Case

**Examples:**
- `CRWL-IP01-EC-01` - Crawler Plan 01, Edge Case 1
- `CRWL-IP01-IS-05` - Crawler Plan 01, Implementation Step 5
- `AUTH-TP01-TC-03` - Authentication Test Plan 01, Test Case 3
- `AUTH-IP01-VC-02` - Authentication Plan 01, Verification Checklist 2

### Source IDs (INFO documents)

All sources in INFO documents MUST have unique IDs for traceability.

**Format:** `[TOPIC]-[DOC]-SC-[SOURCE_ID]-[SOURCE_REF]`

**Components:**
- `SC` - Source type marker
- `SOURCE_ID` - Website/source mnemonic (2-6 chars)
- `SOURCE_REF` - Page/section identifier (2-10 chars, human readable, omit vowels)

**Examples:**
- `AGSK-IN01-SC-ASIO-HOME` - agentskills.io/home
- `AGSK-IN01-SC-ASIO-WAS` - agentskills.io/what-are-skills
- `AGSK-IN01-SC-ASIO-SPEC` - agentskills.io/specification
- `AGSK-IN01-SC-ASIO-INTSK` - agentskills.io/integrate-skills
- `AGSK-IN01-SC-CLAUD-SKLBP` - platform.claude.com/.../best-practices
- `CRWL-IN01-SC-MSDN-GRPHAPI` - Microsoft Graph API docs

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
