# INFO: LLM (Large Language Model) Evaluation Test Results

**Doc ID**: LLMEV-IN01
**Goal**: Document test results for LLM Evaluation Skill API testing
**Timeline**: 2026-01-22 (2 updates)

## Summary

**Key Findings:**
- All 6 scripts work correctly with real API calls [PROVEN]
- End-to-end pipeline executes successfully [PROVEN]
- 81.1% pass rate (129/159) with claude-opus-4-1 transcription [TESTED]
- Average score: 4.14/5 [TESTED]
- Total cost: $4.82 USD for transcription (130K tokens) [VERIFIED]
- 4 issues found and resolved (FL-007, FL-008, FL-009, max_tokens fix) [PROVEN]

## Table of Contents

1. [Test Objective](#test-objective)
2. [Test Strategy](#test-strategy)
3. [Test Setup](#test-setup)
4. [Test Configuration](#test-configuration)
5. [Test Execution](#test-execution)
6. [Test Results](#test-results)
7. [Issues Found](#issues-found)
8. [Document History](#document-history)

## Test Objective

Validate that all 6 core scripts of the LLM Evaluation Skill function correctly:

- **call-llm.py** - Single LLM call with image/text input
- **call-llm-batch.py** - Batch processing with parallel workers
- **generate-questions.py** - Question generation from source content
- **generate-answers.py** - Answer generation using transcriptions
- **evaluate-answers.py** - LLM-as-judge scoring
- **analyze-costs.py** - Token usage and cost analysis

## Test Strategy

### Approach

- **Integration testing** with real API calls (OpenAI gpt-4o-mini)
- **End-to-end pipeline** execution from input to final evaluation
- **Incremental validation** - verify each script output before proceeding

### Test Flow

```
Input Files (16 images + 1 text)
    │
    ├─> [call-llm-batch.py] -> Transcriptions (.md + .meta.json)
    │
    ├─> [generate-questions.py] -> questions.json (156 questions)
    │
    ├─> [generate-answers.py] -> answers_gpt-4o-mini.json
    │
    ├─> [evaluate-answers.py] -> scores_gpt-4o-mini.json
    │
    └─> [analyze-costs.py] -> cost_analysis.json
```

### Success Criteria

- All scripts execute without errors
- Output files are created in expected format
- Token usage is tracked correctly
- Cost analysis produces valid results

## Test Setup

### Environment

- **OS**: Windows
- **Python**: Virtual environment at `.tools/llm-eval-venv/`
- **API Keys**: `.api-keys.txt` (OpenAI + Anthropic)

### Dependencies

- openai==2.8.0
- anthropic>=0.18.0,<1.0.0

### Virtual Environment Activation

```powershell
.tools\llm-eval-venv\Scripts\Activate.ps1
```

## Test Configuration

### Models

- **Transcription**: `claude-opus-4-1-20250805` (Anthropic) - $15/$75 per 1M tokens
- **Generate questions**: `gpt-5-mini` (OpenAI) - $0.25/$2 per 1M tokens
- **Generate answers**: `gpt-5-mini` (OpenAI) - $0.25/$2 per 1M tokens
- **Judge**: `gpt-5` (OpenAI) - $1.25/$10 per 1M tokens
- **Workers**: 4 parallel

### Input Data

**Location**: `_Sessions/_2026-01-22_LLMEvaluationSkill/test/input/`

**Files (16 total):**

- BP-ESG-Datasheet-2023_page010.jpg
- Edison-Financial-Report-2023-FY2023-Results_page004.jpg
- Microsoft_10WaysToUseCopilotForManagers.jpg
- Microsoft_OutlookImage.jpg
- Microsoft_PowerPointImage.jpg
- Microsoft_WordImage.jpg
- sample_document.txt (text file)
- SSE-Annual-Report-2024-Group-Risk-Report_page004.jpg
- SSE-Annual-Report-2024-Group-Risk-Report_page005.jpg
- Vestas-Annual-Report-2023-Investor-Presentation_page006.jpg
- Vestas-Annual-Report-2023-Investor-Presentation_page013.jpg
- VisualCapitalist_RentPricesAroundTheWorld.jpg
- VisualCapitalist_TopEconomies.jpg
- Werner_2016_Stem_Cells_Good_Bad_Ugly_page006.jpg
- Werner_2018_Cancer_Cell_Suicide_Protocol_page003.jpg
- Werner_2018_Cancer_Cell_Suicide_Protocol_page004.jpg

### Output Folders

- **Transcriptions**: `test/transcriptions/`
- **Questions**: `test/questions.json`
- **Answers**: `test/answers/`
- **Scores**: `test/scores/`
- **Cost Analysis**: `test/cost_analysis.json`

## Test Execution

### Step 1: Batch Transcription

```powershell
python call-llm-batch.py --model gpt-4o-mini --input-folder test/input --output-folder test/transcriptions --prompt-file prompts/summarize-text.md --keys-file .api-keys.txt --workers 2
```

**Result**: 16 files processed (15 new + 1 skipped from previous run)

### Step 2: Generate Questions

```powershell
python generate-questions.py --model gpt-4o-mini --input-folder test/input --output-file test/questions.json --keys-file .api-keys.txt --workers 2
```

**Result**: 156 questions generated

### Step 3: Generate Answers

```powershell
python generate-answers.py --model gpt-4o-mini --questions-file test/questions.json --input-folder test/transcriptions --output-folder test/answers --keys-file .api-keys.txt --workers 4
```

**Result**: 156 answers generated

### Step 4: Evaluate Answers

```powershell
python evaluate-answers.py --model gpt-4o-mini --input-folder test/answers --output-folder test/scores --keys-file .api-keys.txt --workers 4
```

**Result**: 156 evaluations completed

### Step 5: Analyze Costs

```powershell
python analyze-costs.py --input-folder test --output-file test/cost_analysis.json
```

**Result**: Cost analysis generated

## Test Results

### Results Summary

- **Files Processed** - 16 images + 1 text
- **Transcription Runs** - 32 (2 runs per file)
- **Questions Generated** - 160
- **Answers Generated** - 160
- **Evaluations** - 159 (1 blocked by OpenAI safety filter)
- **Pass Rate** - 81.1% (129/159)
- **Average Score** - 4.14/5
- **Transcription Tokens** - 83,020 in + 47,648 out = 130,668
- **Transcription Cost** - $4.82 USD

### Pass Rate Analysis

The 81.1% pass rate with claude-opus-4-1 transcription is good:

1. **Full transcription**: Used `transcribe-page-v2.md` prompt with ASCII art protocol for figures
2. **High-quality source**: Claude Opus 4.1 captures visual elements well
3. **Challenging questions**: Some questions require inference beyond literal text

**Note**: 1 evaluation blocked by OpenAI safety filter (biology-related content from Werner papers).

### Token Usage Breakdown (Transcription)

- **Input tokens**: 83,020
- **Output tokens**: 47,648
- **Model**: claude-opus-4-1-20250805

### Cost Breakdown

- **Transcription (call-llm-batch)**: $4.82 USD
  - Input: 83,020 / 1M * $15 = $1.25
  - Output: 47,648 / 1M * $75 = $3.57
- **Questions (generate-questions)**: gpt-5-mini (minimal cost)
- **Answers (generate-answers)**: gpt-5-mini (minimal cost)
- **Evaluation (evaluate-answers)**: gpt-5 (minimal cost)

## Issues Found

### Resolved During Testing

**LLMEV-FL-007**: Transcription matching loaded empty .meta.json files
- **Severity**: MEDIUM
- **Cause**: No filtering for `_*` files, `.meta.*` files, or empty content
- **Fix**: Added filters in `generate-answers.py` lines 213-222
- **Status**: RESOLVED

**LLMEV-FL-008**: Skill created in wrong location
- **Severity**: HIGH
- **Cause**: Created in `.windsurf/` instead of `DevSystemV3.2/`
- **Fix**: Copied to correct location
- **Status**: RESOLVED

**LLMEV-FL-009**: Agent ignored documented settings in NOTES.md
- **Severity**: MEDIUM
- **Cause**: Used --workers 2 instead of --workers 4 (documented in NOTES.md)
- **Fix**: Always read NOTES.md Test Configuration before executing commands
- **Status**: RESOLVED

**max_tokens fix**: gpt-5/o1/o3 models require max_completion_tokens
- **Severity**: HIGH
- **Cause**: OpenAI newer models don't support `max_tokens` parameter
- **Fix**: Added detection for gpt-5/o1/o3 models to use `max_completion_tokens`
- **Commit**: 3aac6ea
- **Status**: RESOLVED

### No Open Issues

All scripts executed successfully after bug fixes.

## Verification Checklist

- [x] `call-llm.py` - Single file processing works
- [x] `call-llm-batch.py` - Batch processing with resume works
- [x] `generate-questions.py` - Question generation works
- [x] `generate-answers.py` - Answer generation with transcription matching works
- [x] `evaluate-answers.py` - LLM-as-judge scoring works
- [x] `analyze-costs.py` - Cost calculation works
- [x] Token usage tracking works
- [x] Atomic writes work (no corrupted files)
- [x] Parallel processing works (2-4 workers)
- [x] Resume capability works (skips existing files)

## Document History

**[2026-01-22 23:30]**
- Updated with full pipeline test results using claude-opus-4-1 + gpt-5-mini + gpt-5
- 81.1% pass rate (129/159), avg score 4.14/5
- Added FL-009 and max_tokens fix issues
- Updated cost analysis ($4.82 for transcription)

**[2026-01-22 22:30]**
- Initial test results documented
- All 6 scripts verified working
- 2 bugs found and resolved (FL-007, FL-008)
