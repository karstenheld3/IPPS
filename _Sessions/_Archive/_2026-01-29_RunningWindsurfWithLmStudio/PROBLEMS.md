# Session Problems

**Doc ID**: 2026-01-29_RunningWindsurfWithLmStudio-PROBLEMS

## Open

**LMWS-PR-001: LM Studio installer requires manual download**
- **History**: Added 2026-01-29 10:37
- **Description**: LM Studio download page uses JavaScript, cannot be automated via curl/wget
- **Impact**: User must manually download installer from browser
- **Next Steps**: Visit https://lmstudio.ai/download and download Windows installer

## Resolved

**LMWS-PR-002: Verify Agent-Cascade MCP server works with Windsurf**
- **History**: Added 2026-01-29 10:37, Resolved 2026-01-29 11:16
- **Description**: Agent-Cascade repo documentation shows it works, but not tested on this system
- **Resolution**: Successfully tested - local_chat tool responds with Ministral model
- **Next Steps**: Install LM Studio, load model, build Agent-Cascade, test with Windsurf

**LMWS-PR-003: Verify LM-Studio-IDE-Plugin works with current Windsurf version**
- **History**: Added 2026-01-29 10:37
- **Description**: Plugin is third-party, may have compatibility issues
- **Impact**: Unknown if inline completions and chat panel will function
- **Next Steps**: Install via VSIX, configure, test functionality

## Resolved

## Deferred

## Problems Changes

**[2026-01-29 10:37]**
- Added: LMWS-PR-001 (manual download required)
- Added: LMWS-PR-002 (Agent-Cascade verification pending)
- Added: LMWS-PR-003 (IDE plugin verification pending)
