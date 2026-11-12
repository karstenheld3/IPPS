# Release Notes: v4.3 (2026-09-10)

## Summary

This release covers work from 2026-08-30 to 2026-09-10, spanning 55 commits across DevSystemV4.3. Major themes: workspace management skill with sync.ps1, fact-check and investigate workflows, prompt file format support, Z.AI provider integration, and major artifact cleanup (328 images purged, Docs/ restructured).

## Changes Since v4.2

### New Skills

- **workspace-management** - Workspace setup, comparison, and sync with `sync.ps1` script, questionnaire, report template, and workspace guides/rules

### New Workflows

- **fact-check** - Source materialization and factuality verification with critique and fact-check review templates
- **write-prompts** - IPPS prompt file format support with rules, guides, and template
- **workspace-setup** - Interactive workspace creation with schema-aware questionnaire
- **compare-workspace-setup** - Workspace setup comparison between repos
- **investigate** - Structured investigation workflow with log template, guides, and rules
- **cleanup** - Path-scoped and category-scoped cleanup modes

### Deprecated Workflows

- **solve.md** - Replaced by `/go`
- **build.md** - Replaced by `/go` and `/write-tasks-plan`
- **partition.md** - Replaced by `/write-tasks-plan`
- **workspace-create.md** - Replaced by `/workspace-setup`

### Skill and Workflow Updates

- **write-documents**: PROMPTS_GUIDES, PROMPTS_RULES, INVESTIGATION_LOG_TEMPLATE, INVESTIGATION_GUIDES, INVESTIGATION_LOG_RULES
- **deep-research**: RESEARCH_TOOLS updated with DevSystem references
- **llm-evaluation**: Z.AI provider added with unified parameter mapping
- **commit**: Workspace vs workspace-file distinction, restricted to workspace repos only
- **verify**: Cross-document verification, schema-aware mode for workspace setup, minimal fact-check
- **project-release**: Config-driven with multi-repo support, SOPS mandatory read, SOP 7 version bump
- **sync**: sync.ps1 with per-repo version detection, LOCALLY_MODIFIED/BREAKING_CHANGE detection

### Rules

- **agent-behavior.md**: Updated behavioral rules
- **core-conventions.md**: Updated formatting and writing conventions
- **devsystem-core.md**: Updated with workspace-management definitions, sync architecture
- **devsystem-ids.md**: Updated with nested document IDs

### Specs

- **_SPEC_WORKSPACE-MANAGEMENT_SKILL.md**: 1646 lines — workspace management skill specification with FR-41 through FR-75
- **_SPEC_INVESTIGATE_WORKFLOW.md**: Investigate workflow specification
- **_SPEC_IPPS_PROMPT_FILE_FORMAT.md**: Prompt file format specification

### Documentation

- **Docs/ restructured to docs/** with underscore prefix for INFO documents
- **328 tracked images purged** (old version duplicates, ghost files, POC screenshots)
- **Model pricing images transcribed to markdown**
- **README** restructured with V4.3 references
- **ID-REGISTRY** updated with new topics
- **LOCAL_ENVIRONMENTS.md** added with scoped deployment

### Model Registry

- **Z.AI provider** added with unified parameter mapping
- **Lana-V1** added as model JSON distribution target
- **update-model-registry.md** updated with Phase 9.3 multi-target distribution

### Infrastructure

- **check_workflow_refs.ps1** - Broken workflow reference detection tool
- **sync.ps1** - Full sync script with diff/execute modes, bundle support, deprecated patterns
- **devsystem-sync.json** - Sync configuration at workspace root
- **.claude/commands** removed (deprecated)

### Tracking

- **!PROBLEMS.md** renamed to **PROBLEMS.md** with updated references
- **!NOTES.md** convention established for priority files
- **V5.0 planning items** added (deep-research update compat, reusable templates)

## Sessions

### _2026-09-05_ZAIIntegration (Sessions)

**Goal**: Z.AI provider integration with unified parameter mapping

### _2026-09-06_SyncScriptImpl (Sessions)

**Goal**: sync.ps1 implementation with per-repo version detection

## Statistics

- **Commits since v4.2**: 55
- **Files changed**: 1250
- **Lines added**: 23372
- **Lines deleted**: 118507
- **New skills**: 1 (workspace-management)
- **New workflows**: 6 (fact-check, write-prompts, workspace-setup, compare-workspace-setup, investigate, cleanup)
- **Deprecated workflows**: 4 (solve, build, partition, workspace-create)
- **New providers**: 1 (Z.AI)
- **Images purged**: 328
- **Date range**: 2026-08-30 to 2026-09-10

## Document History

**[2026-09-10 00:00]**
- Initial release notes created
