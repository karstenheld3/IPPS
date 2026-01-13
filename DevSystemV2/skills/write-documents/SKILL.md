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

## ID System

All documents and items must have unique IDs for traceability.

**Topic:** 2-5 uppercase letters describing component (e.g., `CRWL` for Crawler, `AUTH` for Authentication)

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

### Source IDs (INFO documents)

All sources in INFO documents MUST have unique IDs.

**Format:** `[TOPIC]-[DOC]-SC-[SOURCE_ID]-[SOURCE_REF]`

**Components:**
- `SC` - Source type marker
- `SOURCE_ID` - Website/source mnemonic (2-6 chars)
- `SOURCE_REF` - Page/section identifier (2-12 chars, omit vowels)

**Examples:**
- `AGSK-IN01-SC-ASIO-HOME` - agentskills.io/home
- `AGSK-IN01-SC-CLAUD-SKLBP` - platform.claude.com/.../best-practices

## Available Templates

Read the appropriate template for the document type you are creating:
- `INFO_TEMPLATE.md` - Research and analysis documents
- `SPEC_TEMPLATE.md` - Technical specifications
- `SPEC_RULES.md` - SPEC writing rules with GOOD/BAD examples
- `IMPL_TEMPLATE.md` - Implementation plans
- `TEST_TEMPLATE.md` - Test plans
- `FIXES_TEMPLATE.md` - Fix tracking documents

## INFO Document Patterns

INFO documents vary by purpose. Common patterns:

**Knowledge Reference** (most common)
- Summary with copy/paste-ready findings
- Topical sections organized by subject
- Sources at end

**Approach Evaluation** (when choosing between options)
Add these sections when evaluating alternatives:
```
## Approaches
### Option A: [Name]
**Description**: [Brief explanation]
**Pros**: [list]
**Cons**: [list]

## Approach Comparison
- **Speed**: A > B > C
- **Complexity**: A < B < C

## Recommended Approach
**[Option X]** because [rationale].
```

**Quick Reference** (cheat sheets)
- Copy/paste-ready section at top
- Minimal prose, maximum examples

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
