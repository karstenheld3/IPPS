# Release Notes: v3.6 (2026-05-01)

## Summary

This release covers development from DevSystemV3.4 through V3.6, spanning 116 commits and 8 active sessions. Major themes: writing quality frameworks (APAPALAN, MECT, SOCAS), autonomous agent execution, MinifyIPPS compression pipeline, conversation management, and comprehensive README overhaul.

## Highlights

- **SOCAS** - Signs of Confusion and Sloppiness: 15 criteria for detecting agent degradation in documents, code, and workflows
- **APAPALAN** - As Precise As Possible, As Little As Necessary: 26 enforceable writing rules
- **MECT** - Minimal Explicit Consistent Terminology: Writing and coding rules for consistent terminology
- **4-phase `/improve` workflow** - Pre-flight scan, fix violations, focused improvement, quality polish with versioned backups
- **Autonomous `/go` workflow** - Fully autonomous execution with [ACTOR]=agent, multi-layer completion check, safety protocol
- **MinifyIPPS** - LLM-based compression pipeline for DevSystem markdown files (bundle, analyze, compress, verify)
- **Conversation management** - `/conversation-start` and `/conversation-update` workflows
- **Complete README** - Full workflows reference (38), skills reference (19), 8 core concepts including SOCAS

## DevSystem Version Changes

**V3.5** (intermediate, included in this release):
- Generic `/fix` workflow for any problem type
- Improved `/implement` and `/go` workflows
- MNF sections with auto-apply rule in verify, improve, implement, partition

**V3.6** (current):
- SOCAS quality criteria (15 detection rules)
- 4-phase `/improve` workflow with depth-first improvement and versioned backups
- NFR section in SPEC template
- STRUT self-tracking in workflows
- Updated model tiers (Opus 4.6, Sonnet 4.6, Gemini 3 Flash)

## Sessions Overview

### 1. llm-transcription-skill (2026-01-26)

**Outcome**: LLM transcription skill updates and model config sync

### 2. llm-computer-use (2026-01-27)

**Outcome**: LLM computer use skill refinements

### 3. RunningWindsurfWithLmStudio (2026-01-29)

**Outcome**: Exploration of running Windsurf with LM Studio local models

### 4. AgentExcelSkill (2026-02-27)

**Goal**: Explore possibilities for creating an Agent Excel skill

**Outcome**: Research and exploration phase

### 5. OpenClawExploration (2026-02-27)

**Outcome**: OpenClaw multi-channel agent research and documentation

### 6. GoogleAccountSkill (2026-03-04)

**Goal**: Create a Cascade skill for Google account interaction via gogcli CLI

**Outcome**: google-account skill added

### 7. TravelInfoSkill (2026-03-04)

**Outcome**: travel-info skill added

### 8. MinifyIPPS (2026-03-19)

**Outcome**: Full MinifyIPPS V2 pipeline with spec-driven development (SPEC, IMPL, TEST, TASKS), 57 passing tests

## New Workflows

- `/conversation-start` - Create conversation tracking files from chat context
- `/conversation-update` - Update existing conversations with new messages

## New Rules and Templates

- `APAPALAN_RULES.md` - 26 enforceable precision and brevity rules
- `MECT_WRITING_RULES.md` - Voice, word choice, terminology, headings, lists
- `MECT_CODING_RULES.md` - Naming, functions, comments, logs, errors
- `SOCAS_RULES.md` - 15 criteria for agent degradation detection
- `WORKFLOW_RULES.md` - Workflow document structure and formatting
- `SKILL_RULES.md` - Skill document standards
- `SKILL_TEMPLATE.md` - Template for new skills
- `CONVERSATION_RULES.md` - Conversation document standards
- `CONVERSATION_TEMPLATE.md` - Template for conversation tracking
- `LOGGING-RULES-TEST-LEVEL.md` - Test-level logging standards

## Workspace File Changes

- `README.md` - Complete rewrite with 8 core concepts, full workflow/skill reference, agent compatibility matrix
- `!PROBLEMS.md` - Added for workspace-level problem tracking
- `FAILS.md` - Updated with new failure entries (GLOB-FL-020 through GLOB-FL-028)
- `ID-REGISTRY.md` - New topics: FLCOR, REPRT, WS2DV, WSWN, DOCWRITEFW, and others
- `NOTES.md` - Updated with encoding rules, DevSystem sync rules, README link conventions

## Statistics

- **Total Commits**: 116
- **Total Files Changed**: 1972
- **Active Sessions**: 8
- **Archived Sessions**: 7 (pre-existing)
- **New Workflows**: 2
- **New Rule/Template Files**: 10
- **Core Concepts**: 8 (added SOCAS)

## Document History

**[2026-05-01 16:50]**
- Initial release notes created
