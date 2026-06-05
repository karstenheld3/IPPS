# Session Notes

**Doc ID**: 2026-01-29_RunningWindsurfWithLmStudio-NOTES

## Session Info

- **Started**: 2026-01-29
- **Goal**: Set up and test running Windsurf Cascade with local LLMs via LM Studio
- **Operation Mode**: IMPL-ISOLATED
- **Output Location**: [SESSION_FOLDER]/

## Current Phase

**Phase**: IMPLEMENT
**Workflow**: Setup complete, integration verified
**Assessment**: Agent-Cascade MCP working with LM Studio

## Agent Instructions

- LM Studio installer requires manual browser download from https://lmstudio.ai/download
- Use VSIX installation method for LM-Studio-IDE-Plugin (more reliable)
- Node.js 20+ required for Agent-Cascade build
- TOPIC for this session: `LMWS` (registered in ID-REGISTRY.md)

## Available Skills

Skills that may be useful for this session:

- **@windsurf-auto-model-switcher** - Automate Windsurf model selection via UI
- **@windows-desktop-control** - Windows desktop automation (mouse, keyboard)
- **@llm-computer-use** - LLM-driven computer use capabilities

## Key Decisions

- **LMWS-DD-01**: Windsurf Cascade cannot use local LLMs as primary model - this is by design (Codeium cloud integration)
- **LMWS-DD-02**: Two workaround approaches available: MCP bridge (Agent-Cascade) or separate IDE plugin

## Important Findings

- Cascade cloud model always remains the orchestrator, even with MCP bridge [VERIFIED]
- LM-Studio-IDE-Plugin provides separate AI assistant, does NOT replace Cascade [VERIFIED]
- BYOK only supports cloud API providers (Anthropic Claude), not local endpoints [VERIFIED]
- Agent-Cascade `local_chat` tool works with LM Studio API [TESTED]
- MCP config path is `%USERPROFILE%\.codeium\windsurf\mcp_config.json` [TESTED]
- Model name must match API response exactly (e.g., `mistralai/ministral-3-3b`) [TESTED]
- llm-computer-use skill struggles with window focus (~$0.57 spent, failed) [TESTED]

## Topic Registry

- `LMWS` - LM Studio + Windsurf integration research

## Related Documents

- `Docs/FurtherResearch/_INFO_RUN_WINDSURF_CASCADE_WITH_LM_STUDIO.md` [LMWS-IN01]
- `.tools/_installer/README_LM_STUDIO_DOWNLOADS.md`
