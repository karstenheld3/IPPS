---
name: write-documents
description: Apply when creating or editing INFO, SPEC, IMPL, TEST, FIX documents, or STRUT plans
---

# Document Writing Guide

All documents MUST follow `APAPALAN_RULES.md` (precision, brevity, structure, naming) and `MECT_WRITING_RULES.md` (voice, word choice, terminology, headings, lists). Read both before writing.

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

- Read `APAPALAN_RULES.md` and `MECT_WRITING_RULES.md` before writing
- Lists, not Markdown tables. No emojis. No `---` between sections
- Header block: Doc ID (required), Goal (required), Target file, Depends on (omit if N/A)
- Every document MUST have unique ID. Reference docs by filename AND Doc ID: `_SPEC_CRAWLER.md [CRWL-SP01]`
- Be exhaustive: list ALL domain objects, actions, functions
- Document History at end, reverse chronological. Box-drawing chars (├── └── │) for trees
- SPEC, IMPL, TEST MUST have MUST-NOT-FORGET section (after header, before TOC)

## Document Types

**Research:** INFO (`_INFO_[TOPIC].md`), REVIEW (`_REVIEW_[TOPIC].md`)
**Planning:** SPEC (`_SPEC_[COMPONENT].md`), IMPL (`_IMPL_[COMPONENT].md`), TEST (`_TEST_[COMPONENT].md`), TASKS (`TASKS_[TOPIC].md`)
**Tracking:** STRUT (embedded), FIXES (`_IMPL_[COMPONENT]_FIXES.md`), FAILS (`FAILS.md`)
**Session** (@skills:session-management): NOTES.md, PROBLEMS.md, PROGRESS.md
**Workflow** (`.md` in workflows/): use `WORKFLOW_TEMPLATE.md` + `WORKFLOW_RULES.md`

## Dependency Chain

```
INFO (research) → SPEC (what) → IMPL (how) → TASKS (work items)
                      │                             │
                      └──> TEST (verify) ───────────┘
```

## Usage

1. Read this SKILL.md, then `APAPALAN_RULES.md`, then `MECT_WRITING_RULES.md`
2. Read template for document type (required)
3. SPEC: also read `SPEC_RULES.md`. WORKFLOW: also read `WORKFLOW_RULES.md`
4. Follow template structure exactly unless user requests exceptions

## Writing Rules

- Enumerations: comma-separated (`.pdf, .docx, .ppt`), NOT slash-separated
- Ambiguous modifiers: split into separate sentences
  - BAD: "Files starting with '!' signify high relevance that must be treated with extra attention."
  - GOOD: "Files starting with '!' indicate high relevance. This information must be treated with extra attention."

## File Naming

`_INFO_[TOPIC].md`, `_SPEC_[COMPONENT].md`, `_SPEC_[COMPONENT]_UI.md`, `_IMPL_[COMPONENT].md`, `_IMPL_[COMPONENT]_FIXES.md`, `SPEC_[COMPONENT]_TEST.md`, `IMPL_[COMPONENT]_TEST.md`, `TASKS_[TOPIC].md`. `!` prefix = priority.

## Agent Behavior

- APAPALAN + MECT: precision first, cut unnecessary words
- Never ask for continuations when following plans
- Propose 2-3 alternatives before assumptions. List assumptions at spec start.
- Optimize for simplicity. Re-use existing code (DRY). Research APIs from primary sources.
- Document user decisions in "Key Mechanisms" and "What we don't want"

## ID System

See `[AGENT_FOLDER]/rules/devsystem-ids.md` for complete system.

- Document: `[TOPIC]-[DOC][NN]` — `CRWL-SP01`, `AUTH-IP01`
- Spec-Level: `[TOPIC]-[TYPE]-[NN]` — `CRWL-FR-01`, `AUTH-DD-03`
- Plan-Level: `[TOPIC]-[DOC][NN]-[TYPE]-[NN]` — `CRWL-IP01-EC-01`, `AUTH-TP01-TC-05`