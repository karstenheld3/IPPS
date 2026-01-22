# Session Problems

**Session ID**: 2026-01-22_LLMEvaluationSkill

## Open

(none)

## Resolved

**LLMEV-PR-001**: `generate-answers.py` missing `--prompt-file` parameter
- SPEC line 96 specifies `--prompt-file` for custom answering prompt
- **Fixed**: Added `--prompt-file` parameter with `{question}` and `{text_content}` placeholders
- Commit: `797e89f`

**LLMEV-PR-002**: `evaluate-answers.py` missing `--method` parameter
- SPEC line 109 specifies `--method llm|openai-eval`
- **Fixed**: Added `--method` parameter with choices `llm` (default) and `openai-eval`
- Note: `openai-eval` returns "not yet implemented" message
- Commit: `d5c8d04`

**LLMEV-PR-003**: Default question schema categories mismatch
- SPEC (line 301-310): `easy`, `medium_facts`, `medium_graphics`, `hard_semantics`, `hard_graphics`
- **Fixed**: Aligned IMPL to match SPEC categories with detailed descriptions
- Commit: `aaba110`

## Deferred

(none)
