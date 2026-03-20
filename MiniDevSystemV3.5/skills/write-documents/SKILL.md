---
name: write-documents
description: Apply when creating or editing INFO, SPEC, IMPL, TEST, FIX documents, or STRUT plans
---

# Document Writing Guide

**Writing quality standard:** All documents MUST follow:
- `APAPALAN_RULES.md` - Precision formatting, brevity, document structure, naming conventions
- `MECT_WRITING_RULES.md` - Voice, word choice, terminology design, heading/list construction, description types

Read both before writing any document.

## Verb Mapping

- [WRITE-INFO] → `INFO_TEMPLATE.md`
- [WRITE-SPEC] → `SPEC_TEMPLATE.md` + `SPEC_RULES.md`
- [WRITE-IMPL-PLAN] → `IMPL_TEMPLATE.md`
- [WRITE-TEST-PLAN] → `TEST_TEMPLATE.md`
- [WRITE-FIX] → `FIXES_TEMPLATE.md`
- [WRITE-FAIL] → `FAILS_TEMPLATE.md`
- [WRITE-REVIEW] → `REVIEW_TEMPLATE.md`
- [WRITE-TASKS-PLAN] → `TASKS_TEMPLATE.md`
- [WRITE-STRUT] → `STRUT_TEMPLATE.md`

## MUST-NOT-FORGET

- Read `APAPALAN_RULES.md` before writing - precision first, then brevity
- Read `MECT_WRITING_RULES.md` before writing - voice, word choice, terminology design
- Use lists, not Markdown tables
- No emojis - ASCII only, no `---` markers between sections
- Header block: Doc ID (required), Goal (required), Target file, Depends on (omit if N/A)
- Every document MUST have a unique ID
- Reference other docs by filename AND Doc ID: `_SPEC_CRAWLER.md [CRWL-SP01]`
- Be exhaustive: list ALL domain objects, actions, functions
- Document History section at end, reverse chronological
- Use box-drawing characters (├── └── │) for trees
- SPEC, IMPL, TEST documents MUST have MUST-NOT-FORGET section (after header block, before TOC)

## Document Types and When to Use

**Research and Knowledge:**
- **INFO** (`_INFO_[TOPIC].md`) - Research, analysis, option evaluation. Use when gathering information before making decisions.
- **REVIEW** (`_REVIEW_[TOPIC].md`) - Structured review of existing documents. Use for `/critique` and `/reconcile` outputs.

**Planning:**
- **SPEC** (`_SPEC_[COMPONENT].md`) - Technical specifications. Define WHAT to build before building it. Rules: `SPEC_RULES.md`
- **IMPL** (`_IMPL_[COMPONENT].md`) - Implementation plans. Define HOW to build what SPEC describes.
- **TEST** (`_TEST_[COMPONENT].md`) - Test plans. Define how to VERIFY what SPEC requires.
- **TASKS** (`TASKS_[TOPIC].md`) - Partitioned task lists from IMPL/TEST plans. Break plans into discrete work items.

**Execution Tracking:**
- **STRUT** (embedded in any document) - Structured execution plans with checkboxes for phased work with verification gates.
- **FIXES** (`_IMPL_[COMPONENT]_FIXES.md`) - Fix tracking during implementation.
- **FAILS** (`FAILS.md`) - Failure log, lessons learned to prevent repetition.

**Session Tracking** (templates from @skills:session-management): NOTES.md, PROBLEMS.md, PROGRESS.md

**Workflow Documents:** `.md` in workflows/. Rules: `WORKFLOW_RULES.md`

## Document Dependency Chain

```
INFO (research) → SPEC (what) → IMPL (how) → TASKS (work items)
                      │                             │
                      └──> TEST (verify) ───────────┘
```

## Usage

1. Read this SKILL.md, then `APAPALAN_RULES.md`, then `MECT_WRITING_RULES.md`
2. Read the template for your document type (required)
3. For SPEC: also read `SPEC_RULES.md`. For WORKFLOW: also read `WORKFLOW_RULES.md`
4. Follow template structure exactly, except when user requests exceptions

## Document Writing Rules

- Enumerations: comma-separated (`.pdf, .docx, .ppt`), NOT slash-separated
- Ambiguous modifiers: split into separate sentences
  - BAD: "Files starting with '!' signify high relevance that must be treated with extra attention."
  - GOOD: "Files starting with '!' indicate high relevance. This information must be treated with extra attention."

## File Naming

`_INFO_[TOPIC].md`, `_SPEC_[COMPONENT].md`, `_SPEC_[COMPONENT]_UI.md`, `_IMPL_[COMPONENT].md`, `_IMPL_[COMPONENT]_FIXES.md`, `SPEC_[COMPONENT]_TEST.md`, `IMPL_[COMPONENT]_TEST.md`, `TASKS_[TOPIC].md`. `!` prefix for priority docs.

## Agent Behavior

- Follow APAPALAN + MECT: precision first, then cut every unnecessary word
- NEVER ask for continuations when following plans
- Before assumptions, propose 2-3 implementation alternatives
- List assumptions at spec start for user verification
- Optimize for simplicity; re-use existing code (DRY)
- Research APIs before suggesting; rely on primary sources only
- Document user decisions in "Key Mechanisms" and "What we don't want" sections

## ID System

See `[AGENT_FOLDER]/rules/devsystem-ids.md` for complete system.

- Document: `[TOPIC]-[DOC][NN]` — Example: `CRWL-SP01`, `AUTH-IP01`
- Spec-Level: `[TOPIC]-[TYPE]-[NN]` (FR, IG, DD) — Example: `CRWL-FR-01`, `AUTH-DD-03`
- Plan-Level: `[TOPIC]-[DOC][NN]-[TYPE]-[NN]` (EC, IS, VC, TC) — Example: `CRWL-IP01-EC-01`, `AUTH-TP01-TC-05`