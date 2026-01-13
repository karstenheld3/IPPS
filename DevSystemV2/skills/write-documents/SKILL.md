---
name: write-documents
description: Apply when creating or editing INFO, SPEC, IMPL, TEST, or FIX documents
---

# Document Writing Guide

This skill contains document templates and formatting rules.

## MUST-NOT-FORGET

- Use lists, not Markdown tables
- No emojis - ASCII only, no `---` markers between sections
- Header block: Goal, Target file, Depends on
- ID-System: `**XXXX-FR-01:**`, `**XXXX-DD-01:**`
- Be exhaustive: list ALL domain objects, actions, functions
- Spec Changes at end, reverse chronological
- Use box-drawing characters (├── └── │) for trees

## Available Templates

Read the appropriate template for the document type you are creating:
- `INFO_TEMPLATE.md` - Research and analysis documents
- `SPEC_TEMPLATE.md` - Technical specifications
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
