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

## Test Configuration

### Paths

- **API Keys**: `.tools/.api-keys.txt`
- **Virtual Environment**: `.tools/llm-eval-venv/`
- **Test Input**: `test/input/` (16 images + 1 text)
- **Test Transcriptions**: `test/transcriptions/`
- **Test Prompts**: `test/prompts/` (custom prompts for this test)
- **Test Schemas**: `test/schemas/` (custom schemas for this test)

### Models

- **Transcription**: `claude-opus-4-1-20250805` (Anthropic)
- **Generate questions**: `gpt-5-mini` (OpenAI)
- **Generate answers**: `gpt-5-mini` (OpenAI)
- **Judge**: `gpt-5` (OpenAI)

### Default Settings

- **Workers**: 4 parallel
- **Runs**: 2 per file
- **Pass Threshold**: 4 (out of 5)
- **Clear folders on re-run**: Use `--clear-folder` flag

### Custom Prompts (test/prompts/)

- `transcribe-page-v2.md` - Full transcription with ASCII art protocol (from `/transcribe` workflow)
- `judge-with-reference.md` - Scoring with reference answers (from EvalPrompt-01)

### Custom Schema (test/schemas/)

- `eval-questions-v2.json` - Categorized questions: 2 easy, 2 medium_facts, 2 medium_graphics, 2 hard_semantics, 2 hard_graphics

### Output Format

- Content: `.md` files (plain markdown)
- Metadata: `.meta.json` files (token usage, model, timestamp)
- Filename pattern: `{stem}_processed_{model}_run{NN}.md`

## Workflows to Run on Resume

1. Read NOTES.md, PROGRESS.md, PROBLEMS.md
2. Read SPEC_LLM_EVALUATION_SKILL.md
3. Continue with implementation phase
