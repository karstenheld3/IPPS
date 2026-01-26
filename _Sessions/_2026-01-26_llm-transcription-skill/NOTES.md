# Session Notes

**Doc ID**: 2026-01-26_llm-transcription-skill-NOTES
**TOPIC**: LLMTR (registered in ID-REGISTRY.md)

## Session Info

- **Started**: 2026-01-26
- **Goal**: Create llm-transcription skill with universal transcription tools using optimized prompts
- **Operation Mode**: IMPL-CODEBASE
- **Output Location**: DevSystemV3.2/skills/llm-transcription/

## Current Phase

**Phase**: EXPLORE
**Workflow**: /build (BUILD workflow - creating new skill)
**Assessment**: COMPLEXITY-MEDIUM (new skill with 2 scripts, prompt engineering)

## Initial Request

User wants to add a new skill "llm-transcription" as a universal transcription tool with optimized prompts for each purpose. Initial features:
1. `transcribe-image-to-markdown.py` - Convert images to markdown
2. `transcribe-image-to-markdown-advanced.py` - Convert images to markdown with refinement
3. `transcribe-audio-to-markdown.py` - Convert audio to markdown

## IMPORTANT: Cascade Agent Instructions

1. **Source Location**: Create all files in `DevSystemV3.2/skills/llm-transcription/` first, then sync to `.windsurf/`
2. **Sync Command**: After editing DevSystemV3.2, run: `Copy-Item -Path "DevSystemV3.2\*" -Destination ".windsurf\" -Recurse -Force`
3. **Progressive Disclosure**: Reference files hold details, SKILL.md provides overview

## Key Decisions

- **API Keys**: Use `--keys-file .tools/.api-keys.txt` for all LLM scripts
- **Default models**: gpt-5-mini for both transcription and judge

## Important Findings

(To be filled during EXPLORE phase)

## Topic Registry

- `LLMTR` - LLM Transcription skill (image-to-markdown, audio-to-markdown)
