# TASKS: LLM Evaluation Skill Tasks Plan

**Doc ID**: LLMEV-TK01
**Feature**: llm-evaluation-skill
**Goal**: Partitioned tasks for LLM Evaluation Skill implementation
**Source**: `IMPL_LLM_EVALUATION_SKILL.md [LLMEV-IP01]`, `TEST_LLM_EVALUATION_SKILL.md [LLMEV-TP01]`
**Strategy**: PARTITION-DEPENDENCY

## Task Overview

- Total tasks: 16
- Estimated total: 9.5 HHW
- Parallelizable: 6 tasks (scripts can be built in parallel after infrastructure)

## Task 0 - Baseline (MANDATORY)

Run before starting any implementation:
- [ ] Verify skill folder does not exist yet
- [ ] Note any existing tests in workspace

## Tasks

### Phase 1: Infrastructure

- [ ] **LLMEV-TK-001** - Create skill folder structure and requirements.txt
  - Files: `.windsurf/skills/llm-evaluation/`, `requirements.txt`
  - Done when: Folder exists, requirements.txt has openai and anthropic
  - Verify: `ls .windsurf/skills/llm-evaluation/`
  - Est: 0.25 HHW

- [ ] **LLMEV-TK-002** - Create model-registry.json
  - Files: `model-registry.json`
  - Done when: JSON valid, contains gpt-4o, gpt-5-mini, claude-opus-4, claude-haiku
  - Verify: `python -c "import json; json.load(open('model-registry.json'))"`
  - Depends: TK-001
  - Parallel: [P]
  - Est: 0.25 HHW

- [ ] **LLMEV-TK-003** - Create model-pricing.json
  - Files: `model-pricing.json`
  - Done when: JSON valid, contains pricing per model with currency
  - Verify: `python -c "import json; json.load(open('model-pricing.json'))"`
  - Depends: TK-001
  - Parallel: [P]
  - Est: 0.25 HHW

- [ ] **LLMEV-TK-004** - Create default prompts
  - Files: `prompts/transcribe-page.md`, `prompts/summarize-text.md`, `prompts/answer-from-text.md`, `prompts/judge-answer.md`
  - Done when: All 4 prompt files exist with content
  - Verify: `ls prompts/`
  - Depends: TK-001
  - Parallel: [P]
  - Est: 0.5 HHW

- [ ] **LLMEV-TK-005** - Create default question schema
  - Files: `schemas/default-questions.json`
  - Done when: JSON valid, contains 5 categories
  - Verify: `python -c "import json; json.load(open('schemas/default-questions.json'))"`
  - Depends: TK-001
  - Parallel: [P]
  - Est: 0.25 HHW

### Phase 2: Core Scripts

- [ ] **LLMEV-TK-006** - Implement call-llm.py
  - Files: `call-llm.py`
  - Done when: Single LLM call works with image and text input
  - Verify: `python call-llm.py --help`
  - Guardrails: Must include load_api_keys, detect_provider, retry_with_backoff
  - Depends: TK-001
  - Est: 1.0 HHW

- [ ] **LLMEV-TK-007** - Implement call-llm-batch.py
  - Files: `call-llm-batch.py`
  - Done when: Batch processing with --workers, resume, incremental save works
  - Verify: `python call-llm-batch.py --help`
  - Guardrails: Must use ThreadPoolExecutor, atomic_write_json, threading.Lock
  - Depends: TK-006
  - Est: 1.5 HHW

- [ ] **LLMEV-TK-008** - Implement generate-questions.py
  - Files: `generate-questions.py`
  - Done when: Question generation with schema support works
  - Verify: `python generate-questions.py --help`
  - Depends: TK-006
  - Parallel: [P]
  - Est: 1.0 HHW

- [ ] **LLMEV-TK-009** - Implement generate-answers.py
  - Files: `generate-answers.py`
  - Done when: Answer generation from transcriptions works
  - Verify: `python generate-answers.py --help`
  - Depends: TK-006
  - Parallel: [P]
  - Est: 1.0 HHW

- [ ] **LLMEV-TK-010** - Implement evaluate-answers.py (LLM method)
  - Files: `evaluate-answers.py`
  - Done when: LLM-as-judge scoring 0-5 works with `--method llm`
  - Verify: `python evaluate-answers.py --help`
  - Depends: TK-006
  - Est: 1.0 HHW

- [ ] **LLMEV-TK-010b** - Implement evaluate-answers.py (OpenAI Eval API method)
  - Files: `evaluate-answers.py`
  - Done when: `--method openai-eval` works using OpenAI Eval API
  - Reference: `https://github.com/karstenheld3/OpenAI-BackendTools/blob/main/src/test_eval_operations.py`
  - Implementation notes:
    - Use `client.evals.create()` with score_model grader
    - Use `client.evals.runs.create()` with JSONL data source
    - Poll for completion with timeout
    - Parse output items for scores and rationale
    - Item schema: `{input, reference, output_text}`
    - Score range: 0-5, pass_threshold from --pass-threshold
  - Verify: `python evaluate-answers.py --method openai-eval --model gpt-4o --input-folder answers/ --output-folder scores/`
  - Depends: TK-010
  - Est: 1.5 HHW

- [ ] **LLMEV-TK-011** - Implement analyze-costs.py
  - Files: `analyze-costs.py`
  - Done when: Cost calculation from token usage files works
  - Verify: `python analyze-costs.py --help`
  - Depends: TK-003
  - Parallel: [P]
  - Est: 0.5 HHW

### Phase 3: Documentation

- [ ] **LLMEV-TK-012** - Create SKILL.md
  - Files: `SKILL.md`
  - Done when: Skill documentation complete with usage examples
  - Depends: TK-006 to TK-011
  - Est: 0.5 HHW

### Phase 4: Testing

- [ ] **LLMEV-TK-013** - Create test fixtures and mocks
  - Files: `tests/conftest.py`, `tests/fixtures/`
  - Done when: Mock clients and test data ready
  - Verify: `python -m pytest tests/ --collect-only`
  - Depends: TK-007
  - Est: 0.5 HHW

- [ ] **LLMEV-TK-014** - Implement unit tests (TC-01 to TC-39)
  - Files: `tests/test_utils.py`, `tests/test_resume.py`, `tests/test_parsing.py`
  - Done when: All unit tests pass
  - Verify: `python -m pytest tests/ -v -k "not e2e"`
  - Depends: TK-013
  - Est: 1.0 HHW

- [ ] **LLMEV-TK-015** - Implement integration tests (TC-40 to TC-48)
  - Files: `tests/test_e2e.py`
  - Done when: All E2E tests pass with mocked API
  - Verify: `python -m pytest tests/ -v -k "e2e"`
  - Depends: TK-014
  - Est: 0.5 HHW

## Task N - Final Verification (MANDATORY)

Run after all tasks complete:
- [ ] Run full test suite: `python -m pytest tests/ -v`
- [ ] Compare test results to Task 0 baseline
- [ ] New failures = regressions (must fix)
- [ ] Run `/verify` workflow on all documents
- [ ] Update PROGRESS.md - mark complete
- [ ] Run `/commit` to commit all changes

## Dependency Graph

```
TK-001 ─┬─> TK-002 ─────────────────────────────────────┐
        ├─> TK-003 ───────────────────────> TK-011 ────┤
        ├─> TK-004 ────────────────────────────────────┤
        ├─> TK-005 ────────────────────────────────────┤
        └─> TK-006 ─┬─> TK-007 ─> TK-013 ─> TK-014 ─> TK-015
                    ├─> TK-008 ─────────────────────────┤
                    ├─> TK-009 ─────────────────────────┼─> TK-012
                    └─> TK-010 ─────────────────────────┘
```

## Parallel Execution Groups

**Group A** (after TK-001): TK-002, TK-003, TK-004, TK-005
**Group B** (after TK-006): TK-008, TK-009, TK-011

## Document History

**[2026-01-23 10:40]**
- Added: LLMEV-TK-010b for OpenAI Eval API implementation
- Reference: test_eval_operations.py from OpenAI-BackendTools

**[2026-01-22 21:28]**
- Initial tasks plan created from IMPL/TEST
- 15 tasks across 4 phases
- 6 parallelizable tasks identified

