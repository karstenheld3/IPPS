# Release Notes: v3.8 (2026-06-05)

## Summary

This release covers development from DevSystemV3.7 (2026-05-27) through V3.8, spanning 8 commits. Major theme: migration from Windsurf to Devin after the IDE software was renamed, plus model registry updates and documentation enrichment.

## Highlights

- **Windsurf to Devin Migration** - The IDE software was renamed from "Windsurf" to "Devin". All `.windsurf/` folder references migrated to `.devin/` across 50+ files (rules, workflows, skills, SOPs, README, Docs, deploy scripts). Historical records preserved as-is.
- **Devin Desktop Launcher** - `Devin.bat` launcher script added for opening workspace in Devin IDE
- **Claude Opus 4.8 Support** - New model added to LLM evaluation skill with `max` effort level
- **SOP 5: Model Registry Deployment** - New standard operating procedure for syncing model registry JSON files across repos
- **Architecture Documentation** - Windsurf/Devin internals documented from proxy interception testing

## DevSystem Version Changes

**V3.8**:
- `.windsurf/` renamed to `.devin/` throughout all DevSystem files
- Agent folder definition updated: `Windsurf: .windsurf/` changed to `Devin: .devin/`
- All skill scripts, workflow references, and path navigation comments updated
- `deploy-to-all-repos.md` target repo paths updated from `.windsurf` to `.devin`
- `SOPS.md` all sync commands and verification scripts updated
- `__pycache__` bytecode pollution cleaned from skills folders
- SOP 5 added for model registry JSON file deployment across repos

## Sessions Overview

No formal sessions created during this release period. All work performed in PROJECT-MODE.

## New Workflows

None.

## Removed Workflows

None.

## New Skills / Skill Changes

- **llm-evaluation** - Added Claude Opus 4.8 model, introduced `max` effort level

## Workspace Files

- `FAILS.md` - Added GLOB-FL-033 (unnecessary clarification question)
- `ID-REGISTRY.md` - Added topics: DVDT (Devin Desktop), LLMCG (LLM Code Generation)
- `NOTES.md` - All `.windsurf` references migrated to `.devin`
- `SOPS.md` - All `.windsurf` references migrated to `.devin`, SOP 5 added
- `README.md` - All `.windsurf` path references migrated to `.devin`
- `deploy-to-all-repos.md` - All target paths updated from `.windsurf` to `.devin`
- `Devin.bat` - New launcher script

## Docs

- `INFO_HOW_DEVIN_WORKS.md` - New reference document for Devin Desktop IDE
- `INFO_HOW_WINDSURF_WORKS.md` - Restructured and enriched from deep research, architecture internals added
- `Docs/` folder - All `.windsurf` path references migrated to `.devin` (14 files)

## Statistics

- **Commits since v3.7**: 8
- **Active sessions**: 0 (PROJECT-MODE work)
- **New topics registered**: 2 (DVDT, LLMCG)
- **Files migrated**: 50+ (`.windsurf` to `.devin`)
- **Workflows added/removed**: 0/0 (net: 38 total)

## Document History

**[2026-06-05 15:04]**
- Initial release notes created
