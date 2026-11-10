# LLM Tools - Evaluation

Function of `@skills:llm-tools`. Evaluate LLM performance through structured testing pipelines.

Shared scripts (`call-llm.py`, `call-llm-batch.py`, `find-workers-limit.py`) and model JSONs live one level up in `llm-tools/`. Pipeline scripts and prompts live here.

## When to Use This Function

**Apply when:**
- Testing LLM transcription accuracy (images → text)
- Comparing multiple LLM outputs for quality
- Measuring model performance with LLM-as-judge
- Analyzing API costs across models
- Finding optimal concurrency limits for API calls
- Running batch evaluations with parallel workers

**Do NOT apply when:**
- Making single ad-hoc LLM calls (use API directly)
- Testing non-LLM systems
- Simple file processing without LLM involvement

## Quick Start

1. Run `../SETUP.md` once to install dependencies
2. Choose your workflow:
   - **Single call**: `../call-llm.py` for one-off tests
   - **Batch processing**: `../call-llm-batch.py` for multiple files
   - **Full pipeline**: Transcribe → Questions → Answers → Evaluate
   - **Worker limits**: `../find-workers-limit.py` to find max concurrency
   - **Cost analysis**: `analyze-costs.py` for token usage reports

## Available Scripts

**Shared scripts (in `llm-tools/` root):**
- `call-llm.py` - Single LLM API call
- `call-llm-batch.py` - Batch processing with parallel workers
- `find-workers-limit.py` - Discover max concurrent workers
- `test-call-llm.py` - API matrix test across models and efforts
- `llm-tools-selftest.py` - Validate all scripts and JSONs work

**Evaluation Pipeline (here):**
- `generate-questions.py` - Create test questions from source
- `generate-answers.py` - Generate answers from processed text
- `evaluate-answers.py` - Score answers with LLM judge
- `compare-transcription-runs.py` - Compare outputs (Levenshtein/semantic)

**Analysis:**
- `analyze-costs.py` - Calculate token costs (`--pricing ../model-pricing.json`)

**Details:** See `LLM_EVALUATION_SCRIPTS.md` for parameters and examples

## Key Findings

**Judge model recommendation:** Use `gpt-5-mini` for LLM-as-judge tasks (best calibration on similarity tests)

**Worker limits (2026-01-26):**
- OpenAI models: 120+ concurrent workers
- Anthropic models: 60+ concurrent workers

**Claude model IDs:** Use exact release dates (e.g., `claude-opus-4-5-20251101` not `20250514`). See `LLM_EVALUATION_CLAUDE_MODELS.md` for verified IDs.

**Tested models:** 16+ models validated via `../llm-tools-selftest.py`. See `LLM_EVALUATION_TESTED_MODELS.md` for full list.

