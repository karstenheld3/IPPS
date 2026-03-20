---
name: llm-evaluation
description: Apply when evaluating LLM performance through structured testing pipelines
---

# LLM Evaluation Skill

## When to Use

**Apply when:** Testing LLM transcription accuracy, comparing LLM outputs, LLM-as-judge scoring, API cost analysis, finding optimal concurrency limits, batch evaluations with parallel workers.

**Do NOT apply when:** Single ad-hoc LLM calls (use API directly), testing non-LLM systems, simple file processing without LLM involvement.

## Quick Start

1. Run `SETUP.md` once
2. Choose workflow: `call-llm.py` (single), `call-llm-batch.py` (batch), full pipeline, `find-workers-limit.py` (concurrency), `analyze-costs.py` (costs)

## Scripts

**Core:** `call-llm.py` (single call), `call-llm-batch.py` (batch + parallel), `find-workers-limit.py` (max workers)

**Pipeline:** `generate-questions.py`, `generate-answers.py`, `evaluate-answers.py`, `compare-transcription-runs.py` (Levenshtein/semantic)

**Analysis:** `analyze-costs.py`, `llm-evaluation-selftest.py`

**Details:** See `LLM_EVALUATION_SCRIPTS.md`

## Key Findings

- **Judge model:** `gpt-5-mini` recommended (best calibration)
- **Claude model IDs:** Use exact release dates (e.g., `claude-opus-4-5-20251101`). See `LLM_EVALUATION_CLAUDE_MODELS.md`.
- **Tested models:** 16+ validated. See `LLM_EVALUATION_TESTED_MODELS.md`.