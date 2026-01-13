---
name: write-documents
description: Apply when creating or editing INFO, SPEC, IMPL, TEST, or FIX documents
---

# Document Writing Guide

This skill contains document templates and formatting rules.

## MUST-NOT-FORGET

- Use lists, not Markdown tables
- No emojis - ASCII only, no `---` markers between sections
- Header block: Doc ID, Goal, Target file, Depends on
- Every document MUST have a unique ID
- Reference other docs by filename AND Doc ID: `_SPEC_CRAWLER.md [CRWL-SP01]`
- Be exhaustive: list ALL domain objects, actions, functions
- Spec Changes at end, reverse chronological
- Use box-drawing characters (├── └── │) for trees

## Available Templates

Read the appropriate template for the document type you are creating:
- `INFO_TEMPLATE.md` - Research and analysis documents
- `SPEC_TEMPLATE.md` - Technical specifications
- `SPEC_RULES.md` - SPEC writing rules with GOOD/BAD examples
- `IMPL_TEMPLATE.md` - Implementation plans
- `TEST_TEMPLATE.md` - Test plans
- `FIXES_TEMPLATE.md` - Fix tracking documents

## Usage

1. Read this SKILL.md for core rules
2. Read the appropriate template for your document type
3. Follow the template structure

## File Naming

- `_INFO_[TOPIC].md` - Research, analysis, preparation documents
- `_SPEC_[COMPONENT].md` - Technical specifications
- `_SPEC_[COMPONENT]_UI.md` - UI specifications
- `_IMPL_[COMPONENT].md` - Implementation plans
- `_IMPL_[COMPONENT]_FIXES.md` - Fix tracking during implementation
- `SPEC_[COMPONENT]_TEST.md` - Test plan for specification
- `IMPL_[COMPONENT]_TEST.md` - Test plan for implementation
- `!` prefix for priority docs that must be read first

## Agent Behavior

- Be extremely concise. Sacrifice grammar for concision.
- NEVER ask for continuations when following plans.
- Before assumptions, propose 2-3 implementation alternatives.
- List assumptions at spec start for user verification.
- Optimize for simplicity.
- Re-use existing code by default (DRY principle).
- Research APIs before suggesting; rely on primary sources only.
- Document user decisions in "Key Mechanisms" and "What we don't want" sections.

## ID System

All documents and items must have unique IDs for traceability.

### Topic Registry

**Topic:** 2-5 uppercase letters describing component (e.g., `CRWL` for Crawler, `AUTH` for Authentication)

**REQUIREMENT:** Workspace/project-level NOTES.md MUST maintain a complete list of registered TOPIC IDs.

Before using a new TOPIC ID:
1. Check workspace/project NOTES.md for existing TOPIC IDs
2. If new, add to NOTES.md Topic Registry section
3. Use consistent TOPIC across all related documents

**Example: SINGLE-PROJECT**
```
## Topic Registry
- `PRXL` - Project-wide (main spec, architecture)
- `SAP` - SAP Integration (import, temp files)
- `SCHD` - Schaden/Damage (damage records)
- `UI` - User Interface (forms, dialogs)
```

**Example: MONOREPO** (first 2 letters = repo prefix)
```
## Topic Registry
- `CRCORE` - CR: Crawler Core (shared libraries)
- `CRAPI` - CR: Crawler API (REST endpoints)
- `CRUI` - CR: Crawler UI (frontend)
- `IXCORE` - IX: Indexer Core (indexing engine)
- `IXSCHED` - IX: Indexer Scheduler (job scheduling)
```

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

### INFO document IDs

All sources in INFO documents MUST have unique IDs.

**Format:** `[TOPIC]-[DOC]-SC-[SOURCE_ID]-[SOURCE_REF]`

**Components:**
- `SC` - Source type marker
- `SOURCE_ID` - Website/source mnemonic (2-6 chars)
- `SOURCE_REF` - Page/section identifier (2-12 chars, omit vowels)

**Examples:**
- `AGSK-IN01-SC-ASIO-HOME` - agentskills.io/home
- `AGSK-IN01-SC-CLAUD-SKLBP` - platform.claude.com/.../best-practices

### Tracking IDs (PR, FX)

For session and project tracking in PROBLEMS.md and FIXES documents.

**Format:** `[TOPIC]-[TYPE]-[NUMBER]`

**Types:**
- `PR` - Problem (tracked in PROBLEMS.md)
- `FX` - Fix (tracked in IMPL_*_FIXES.md)

**Examples:**
- `SAP-PR-01` - SAP-related problem 1
- `SCHD-FX-01` - Damage module fix 1
- `PRXL-PR-03` - Project-wide problem 3