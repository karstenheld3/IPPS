# Session Notes

**Doc ID**: 2026-01-26_llm-transcription-skill-NOTES
**TOPIC**: LLMTR (registered in ID-REGISTRY.md)

## Session Info

- **Started**: 2026-01-26
- **Goal**: Create llm-transcription skill with universal transcription tools using optimized prompts
- **Operation Mode**: IMPL-CODEBASE
- **Output Location**: DevSystemV3.2/skills/llm-transcription/

## Current Phase

**Phase**: REFINE
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
- **Shared venv**: `.tools/llm-venv/` shared between llm-evaluation and llm-transcription skills

## Important Findings

### gpt-5 and o-series API Parameter [TESTED]

gpt-5 and o-series models require `max_completion_tokens` instead of `max_tokens` in API calls. Without this, API calls fail silently.

```python
uses_completion_tokens = any(x in model for x in ['gpt-5', 'o1-', 'o3-', 'o4-'])
token_param = 'max_completion_tokens' if uses_completion_tokens else 'max_tokens'
```

### gpt-5-mini Effort Levels [TESTED]

gpt-5-mini only supports `["minimal", "low", "medium", "high"]` reasoning effort - NOT "none".

### Cost Comparison [TESTED]

| Settings | Score | Time | Cost |
|----------|-------|------|------|
| gpt-4o (default) | 4.50 | 69s | $0.37 |
| gpt-5-mini (medium) | 4.75 | 163s | $0.02 |
| gpt-5-mini (minimal) | 4.15 | 63s | $0.0085 |

**Best quality/cost**: gpt-5-mini + medium reasoning ($0.02, score 4.75)
**Cheapest**: gpt-5-mini + minimal reasoning ($0.0085, 43x cheaper than gpt-4o)

## Topic Registry

- `LLMTR` - LLM Transcription skill (image-to-markdown, audio-to-markdown)
