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

See `devsystem-ids.md` rule (always-on) for complete ID system.

**Quick Reference:**
- Document: `[TOPIC]-[DOC][NN]` (IN, SP, IP, TP)
- Spec-Level: `[TOPIC]-[TYPE]-[NN]` (FR, IG, DD)
- Plan-Level: `[TOPIC]-[DOC][NN]-[TYPE]-[NN]` (EC, IS, VC, TC)
- Source: `[TOPIC]-[DOC]-SC-[SOURCE_ID]-[SOURCE_REF]`
- Tracking: `[TOPIC]-[TYPE]-[NNN]` (BG, FT, PR, FX, TK)