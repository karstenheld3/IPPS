# Session Notes

**Doc ID**: 2026-01-27_llm-computer-use-NOTES

## Initial Request

```
I want to develop a llm-computer-use skill.

The goal is to use this skill in another skill called windows-desktop-control which does screenshots, sends them to an llm model and receives actions to perform (keys, clicks, etc.)

First we have to research Anthropic models, what they offer, how they work, pricing, APIs specs, and best practices.

I want the document _INFO_ANTHROPIC_COMPUTER_USE.md to be a complete and detailed overview of the models, their capabilities, limitations, and how we can make use of them in our use case.

Also research response times and how many screenshots to send, in which quality and so on.

Collect all research topics and questions first, make a TOC and then research each topic individually. All sources allowed.
```

## Session Info

- **Started**: 2026-01-27
- **Goal**: Research Anthropic Computer Use for windows-desktop-control skill development
- **Operation Mode**: IMPL-ISOLATED
- **Output Location**: [SESSION_FOLDER]/

## Agent Instructions

- Exploratory research with MEPI approach (2-3 curated options where applicable)
- Label all findings: [ASSUMED], [VERIFIED], [TESTED], [PROVEN]
- Keep all sources even if findings were minimal
- Build TOC first, then research section by section

## Key Decisions

**[2026-01-27 19:11] POC before SPEC**
- Build POC first to validate research findings
- Use existing `windows-desktop-control` skill as foundation
- Start with Anthropic (recommended for desktop)

**Resources**:
- Screenshot tool: `DevSystemV3.2/skills/windows-desktop-control/simple-screenshot.ps1`
- API keys: `e:\Dev\.api-keys.txt`

## Important Findings

- Existing screenshot tool already handles DPI scaling via Win32 GetDeviceCaps
- Physical resolution captured correctly (DESKTOPHORZRES/DESKTOPVERTRES)
- JPEG output, configurable region capture
- POC should add: Anthropic API integration, action execution, agent loop
- **Windows Defender blocks .NET image compression in PowerShell** - need alternative approach

## Topic Registry

- `ANTCU` - Anthropic Computer Use research
- `OAICU` - OpenAI Computer Use research
- `WINDC` - Windows Desktop Control (existing skill)
- `LLMCU` - LLM Computer Use (new skill being specified)

## Current Phase

**Phase**: IMPLEMENT (completed)
**Workflow**: /go
**Assessment**: Full llm_computer_use module created and tested
**Next**: Test with actual Anthropic API, then move to DevSystemV3.2/skills/
