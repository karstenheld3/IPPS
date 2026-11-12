# Release Notes: v3.7 (2026-05-27)

## Summary

This release covers development from DevSystemV3.6 (2026-05-01) through V3.7, spanning 47 commits and 3 active sessions. Major themes: deep-research skill overhaul with profile templates and domain restructuring, translation workflow, workflow simplification (recap/continue removal), and LLM evaluation improvements.

## Highlights

- **Deep Research Profiles** - New domain for personal, company, organization, and network profile research with dedicated templates and cross-cutting quality rules
- **Deep Research Restructuring** - Domain files moved into subfolders, unified file naming (`_INFO_[TOPIC]-[NN]_[Name].md`), mandatory Google search via Playwright, `RESEARCH_RULES.md` for `/verify` and `/improve` integration
- **Translation Workflow** - `/translate` workflow with `TRANSLATION_RULES.md` for translating markdown, PDF, or subtitle files to target languages
- **Workflow Simplification** - Removed `recap.md` and `continue.md` as standalone workflows; logic inlined into `/go` (Step 2: Assess State, Step 4: Execute Next). `[RECAP]` and `[CONTINUE]` remain as abstract AGEN verbs
- **Topic Folder Support** - `T##_*` subfolders within sessions for multi-topic work with workflow integration
- **Cleanup Workflow** - `/cleanup` for temp files, Python cache, improve artifacts, MCP backups, INFO markers
- **LLM Evaluation** - Anthropic adaptive thinking with streaming support, long-context pricing, config-driven effort mapping
- **Agent Communication Rules** - 5 new communication rules in `agent-behavior.md` (progress feedback, goal first, self-contained messages, cognitive load limit, important first)

## DevSystem Version Changes

**V3.7**:
- SOCAS rules restructured into standalone `SOCAS_RULES.md` referenced by `/verify` and `/improve`
- 4-phase `/improve` restructured with depth-first improvement and versioned backups
- `/cleanup` workflow (6 categories: temp files, Python cache, improve artifacts, MCP backups, INFO markers, scaffolding files)
- `__` scaffolding prefix and `_gitignore` suffix conventions with lifecycle tiers
- Topic Folder support (`T##_*`) in session management
- `/translate` workflow with comprehensive `TRANSLATION_RULES.md`
- Deep-research profiles domain (personal, company, organization, network)
- Deep-research `RESEARCH_RULES.md` with 6-step verification procedure (RS, SC, SM, TF, ST, QA rules)
- Mandatory Google search via Playwright for all deep research
- Removed `/recap` and `/continue` workflows (inlined into `/go`)
- Updated model tiers and pricing in LLM evaluation and transcription skills

## Sessions Overview

### 1. MdToPdfRenderer (2026-05-01)

**Goal**: Implement a markdown-to-PDF renderer in Python with theme.json and settings.json support

**Outcome**: Python tool for rendering markdown files to PDF with configurable themes, paper dimensions, and XML tag handling

### 2. DeepResearchProfileTemplates (2026-05-25)

**Goal**: Integrate personal, company, organization, and network profile research templates into deep-research skill

**Outcome**: New `profiles/` domain with 4 profile types, dedicated rules files, cross-cutting quality rules, and shared module architecture

### 3. CascadeMetapromptExtraction (2026-05-27)

**Goal**: Intercept Windsurf Cascade LLM communication to extract and analyze metaprompts

**Outcome**: In progress - research into HTTPS interception mechanisms for LLM prompt extraction

## New Workflows

- `/translate` - Translate markdown, PDF, or subtitle files to target languages
- `/cleanup` - Delete temporary files and artifacts left by workflows and skills

## Removed Workflows

- `/recap` - Logic inlined into `/go` Step 2 (Assess State)
- `/continue` - Logic inlined into `/go` Step 4 (Execute Next)

## New Skills / Skill Changes

- **deep-research** - Domain subfolder restructuring, profiles domain, `RESEARCH_RULES.md`, mandatory Google search, output folder isolation
- **llm-evaluation** - Anthropic adaptive thinking, long-context pricing, updated model registry
- **llm-transcription** - Updated model pricing to batch tier, refreshed registry
- **write-documents** - `TRANSLATION_RULES.md` added, `SOCAS_RULES.md` restructured

## Workspace Files

- `FAILS.md` - Added GLOB-FL-029 through GLOB-FL-032
- `ID-REGISTRY.md` - Added topics: MDPDF, XLATE, REPRT, WSWN, DOCWRITEFW, MECE, SUMQR, DRPRF, CSMP, NTICP
- `README.md` - Updated workflow count (40 → 38), simplified Autonomous Execution section
- `deploy-to-all-repos.md` - Added `recap.md` and `continue.md` to deprecated workflows list

## Statistics

- **Commits since v3.6**: 47
- **Active sessions**: 3
- **New topics registered**: 10
- **Workflows added**: 2
- **Workflows removed**: 2 (net: 38 total)

## Document History

**[2026-05-27 14:20]**
- Initial release notes created
