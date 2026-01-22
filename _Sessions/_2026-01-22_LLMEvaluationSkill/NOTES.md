# Session Notes

**Session ID**: 2026-01-22_LLMEvaluationSkill
**Started**: 2026-01-22
**Goal**: Create generic LLM evaluation skill with parameterized scripts for any input type

## Current Phase

**Phase**: DESIGN
**Workflow**: /build
**Assessment**: SPEC complete, ready for implementation

## Key Decisions

- **LLMEV-DD-01**: Use original API model IDs (no custom naming)
- **LLMEV-DD-03**: Incremental save after EVERY item processed
- **LLMEV-DD-05**: Token usage in separate `_token_usage.json` files
- **LLMEV-DD-07**: Parallel processing (`--workers N`) for all batch operations

## Important Findings

- Scripts must be input-agnostic (images, text, PDFs)
- Question generation uses schema with categories + prompt_template
- All prompts have explicit parameter names (`--process-prompt`, `--judge-prompt`, etc.)

## Topic Registry

- `LLMEV` - LLM Evaluation Skill

## IMPORTANT: Cascade Agent Instructions

### From devsystem-core.md
- Session documents: NOTES.md, PROGRESS.md, PROBLEMS.md
- Document types: INFO (IN), SPEC (SP), IMPL (IP), TEST (TP)
- Incremental saving for crash resilience
- Use box-drawing characters for trees

### From core-conventions.md
- No emojis in documentation
- Use lists, not Markdown tables
- ASCII quotes only

### Session-Specific
- TOPIC ID: `LLMEV`
- Target folder: `.windsurf/skills/llm-evaluation/`
- SPEC document: `SPEC_LLM_EVALUATION_SKILL.md [LLMEV-SP01]`

## Workflows to Run on Resume

1. Read NOTES.md, PROGRESS.md, PROBLEMS.md
2. Read SPEC_LLM_EVALUATION_SKILL.md
3. Continue with implementation phase
