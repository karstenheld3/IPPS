# SPEC: LLM Evaluation Skill

**Doc ID**: LLMEV-SP01
**Goal**: Generic skill for LLM evaluation pipelines - works with images, text documents, or any content
**Timeline**: Created 2026-01-22, Updated 0 times

**Target folder**: `.windsurf/skills/llm-evaluation/`

## MUST-NOT-FORGET

- **INCREMENTAL SAVE**: ALL scripts MUST write results after EACH item processed, not just at end. Better to write JSON 1000 times than lose everything on crash.
- **CONCURRENCY**: ALL scripts processing multiple items MUST support `--workers N` for parallel execution (default: 4)
- Model IDs MUST match original API model IDs exactly (e.g., `gpt-4o`, `claude-opus-4-20250514`)
- Keys file supports both `.env` and `key=value` formats
- All input/output paths MUST be parameters with sensible defaults
- JSON output for all scripts (machine-readable)
- No hardcoded paths - use `--keys-file`, `--input-file`, `--input-folder`, `--output-file`, `--output-folder` parameters

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Design Decisions](#5-design-decisions)
6. [Implementation Guarantees](#6-implementation-guarantees)
7. [Key Mechanisms](#7-key-mechanisms)
8. [Action Flow](#8-action-flow)
9. [Data Structures](#9-data-structures)
10. [Implementation Details](#10-implementation-details)
11. [Document History](#11-document-history)

## Skill Summary

**File Type Detection:**
- Auto-detect by suffix only (no override to prevent mismatches)
- Image: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- Text: `.txt`, `.md`, `.json`, `.py`, `.html`, `.xml`, `.csv`
- Unknown suffix: script exits with error, user must rename file

**Scripts:**

- `call-llm.py` - Single LLM call (auto-detects image or text input)
  - `--model` - API model ID (required)
  - `--input-file` - Input file: image (.jpg, .png) or text (.txt, .md)
  - `--prompt-file` - Prompt file (.md)
  - `--output-file` - Output file (default: stdout)
  - `--keys-file` - API keys file (default: .env)
  - `--write-json-metadata` - Write JSON with token usage to separate file
  - Examples:
    ```
    python call-llm.py --model gpt-4o --input-file photo.jpg --prompt-file transcribe.md
    python call-llm.py --model claude-opus-4-20250514 --input-file document.md --prompt-file summarize.md
    python call-llm.py --model gpt-5-mini --prompt-file question.md --write-json-metadata
    ```

- `call-llm-batch.py` - Batch LLM calls on folder (auto-detects image or text)
  - `--model` - API model ID (required)
  - `--input-folder` - Folder with input files (.jpg, .png, .md, .txt)
  - `--output-folder` - Folder for output .md files + _token_usage__.json
  - `--prompt-file` - Prompt file (.md)
  - `--runs` - Number of runs per file (default: 1)
  - `--workers` - Parallel workers (default: 4)
  - `--keys-file` - API keys file (default: .env)
  - Examples:
    ```
    python call-llm-batch.py --model claude-opus-4-20250514 --input-folder images/ --output-folder transcriptions/ --prompt-file transcribe.md --runs 3
    python call-llm-batch.py --model gpt-4o --input-folder docs/ --output-folder summaries/ --prompt-file summarize.md
    python call-llm-batch.py --model gpt-5-mini --input-folder screenshots/ --output-folder processed/ --workers 8
    ```

- `generate-questions.py` - Generate evaluation questions from source files
  - `--model` - API model ID (required)
  - `--input-folder` - Folder with source files (.jpg, .png, .md, .txt)
  - `--output-file` - Output .json file with questions
  - `--schema-file` - Question schema JSON file (categories, counts)
  - `--workers` - Parallel workers (default: 4)
  - `--keys-file` - API keys file (default: .env)
  - Examples:
    ```
    python generate-questions.py --model claude-opus-4-20250514 --input-folder images/ --output-file questions.json
    python generate-questions.py --model gpt-4o --input-folder docs/ --output-file questions.json --schema-file custom.json
    python generate-questions.py --model gpt-5-mini --input-folder images/ --output-file q.json --workers 8
    ```
  - **Dependency Note:** Output file (`--output-file`) is used as input for `generate-answers.py` (`--questions-file`)

- `generate-answers.py` - Generate answers from processed text files
  - `--model` - API model ID (required)
  - `--input-folder` - Folder with .md files (output of `call-llm-batch.py`)
  - `--output-folder` - Folder for .json answer files
  - `--questions-file` - .json file (output of `generate-questions.py`)
  - `--workers` - Parallel workers (default: 4)
  - `--prompt-file` - Custom answering prompt file
  - `--keys-file` - API keys file (default: .env)
  - Examples:
    ```
    python generate-answers.py --model gpt-5-mini --input-folder transcriptions/ --output-folder answers/ --questions-file questions.json
    python generate-answers.py --model claude-3-5-haiku-20241022 --input-folder summaries/ --output-folder answers/ --questions-file q.json --workers 8
    python generate-answers.py --model gpt-4o --input-folder processed/ --output-folder answers/ --questions-file q.json --prompt-file custom.md
    ```

- `evaluate-answers.py` - Score answers with LLM-as-judge
  - `--model` - API model ID for judge (required)
  - `--input-folder` - Folder with .json answer files (output of `generate-answers.py`)
  - `--output-folder` - Folder for .json score files
  - `--method` - `llm` or `openai-eval` (default: llm)
  - `--judge-prompt` - Custom judge prompt file
  - `--pass-threshold` - Pass threshold score (default: 4)
  - `--workers` - Parallel workers (default: 4)
  - `--keys-file` - API keys file (default: .env)
  - Examples:
    ```
    python evaluate-answers.py --model gpt-5 --input-folder answers/ --output-folder scores/
    python evaluate-answers.py --model gpt-4o --input-folder answers/ --output-folder scores/ --method openai-eval
    python evaluate-answers.py --model claude-opus-4-20250514 --input-folder answers/ --output-folder scores/ --judge-prompt strict.md --pass-threshold 3
    ```

- `analyze-costs.py` - Token cost analysis from usage logs
  - `--input-folder` - Folder with _token_usage__{model}.json files (output of `call-llm-batch.py`)
  - `--output-file` - Output .json file for cost analysis
  - `--pricing` - Custom pricing JSON file
  - Examples:
    ```
    python analyze-costs.py --input-folder transcriptions/ --output-file cost_analysis.json
    python analyze-costs.py --input-folder llm-eval/my-eval/ --output-file costs.json --pricing custom-pricing.json
    python analyze-costs.py --input-folder . --output-file summary.json
    ```

**Configuration:**
- `model-registry.json` - Available models with providers and status
- `model-pricing.json` - Token costs per model for cost analysis

**Prompts:**
- `prompts/transcribe-page.md` - Default for image transcription
- `prompts/summarize-text.md` - Default for text summarization
- `prompts/answer-from-text.md` - Default for `generate-answers.py`
- `prompts/judge-answer.md` - Default for `evaluate-answers.py`

**Schemas:**
- `schemas/default-questions.json` - Default question schema

## 1. Scenario

**Problem:** Evaluating LLM output quality requires multiple steps: processing, question generation, answer generation, and scoring. Current scripts are hardcoded to specific input types (images only) and session folders.

**Solution:**
- Create input-agnostic scripts that work with images or text files
- Auto-detect file type by suffix (no override parameter)
- Use original API model IDs (no custom naming)
- Support `.env` format for API keys
- Include model registry and pricing configs as part of skill

**Use cases:**
- Evaluate image transcription quality (original use case)
- Evaluate text summarization quality
- Evaluate document understanding depth
- Evaluate code explanation quality
- Any LLM task where you can generate questions and verify answers

**What we don't want:**
- Hardcoded paths to session folders
- Scripts locked to specific input types
- Custom model naming schemes that differ from API model IDs
- Loss of data on script failure (must save incrementally)

## 2. Context

### Pipeline Overview

The LLM evaluation pipeline consists of 5 independent stages:

```
[INPUT] images, text, PDFs, any file
    │
    ▼
[PROCESS] call-llm-batch.py
    │     (transcribe, summarize, analyze)
    ▼
[GENERATE] generate-questions.py
    │       (create Q&A pairs from source)
    ▼
[ANSWER] generate-answers.py
    │     (answer from processed text)
    ▼
[EVALUATE] evaluate-answers.py
          (score with LLM-as-judge)
```

### Design Principles

- **Stateless scripts**: Each script reads input, produces output, no shared state
- **Composable**: Run any subset of the pipeline, skip stages as needed
- **Input-agnostic**: Same scripts work with images, text, PDFs, code
- **Provider-agnostic**: Works with OpenAI, Anthropic, or any compatible API
- **Crash-resilient**: Incremental saves after each item, resume from partial results

## 3. Domain Objects

### ModelRegistry

A **ModelRegistry** defines available LLM models with their API identifiers and providers.

**Storage:** `model-registry.json` in skill folder
**Purpose:** Map model IDs to providers, track availability

**Key properties:**
- `model_id` - Original API model ID (e.g., `gpt-4o`, `claude-opus-4-20250514`)
- `provider` - API provider (`openai`, `anthropic`)
- `name` - Human-readable display name
- `enabled` - Whether model is available for use
- `status` - Availability status (`available`, `unavailable`, `deprecated`, `retired`)
- `max_tokens_override` - Optional max tokens limit for specific models

### ModelPricing

A **ModelPricing** defines token costs per model for cost analysis.

**Storage:** `model-pricing.json` in skill folder
**Purpose:** Calculate API costs from token usage

**Key properties:**
- `input_per_1m` - USD cost per 1 million input tokens
- `output_per_1m` - USD cost per 1 million output tokens
- `currency` - Always `USD`

### EvalQuestions

An **EvalQuestions** file contains evaluation questions for a set of images.

**Storage:** User-specified JSON file
**Purpose:** Store questions with reference answers for evaluation

**Schema:**
```json
{
  "generated": "2026-01-22T17:14:37.993246",
  "model": "claude-opus-4-1-20250805",
  "images": {
    "image_name": {
      "filename": "image_name.jpg",
      "questions": [
        {"id": 1, "category": "easy", "question": "...", "reference_answer": "...", "answerable": true}
      ]
    }
  }
}
```

### AnswerResults

An **AnswerResults** file contains model answers for evaluation questions.

**Storage:** `{image_name}_answers.json` in output folder
**Purpose:** Store answers from transcription-based QA

**Schema:**
```json
{
  "image_name": "image_name",
  "model_id": "gpt-5-mini",
  "generated": "2026-01-22T17:31:24.603639+00:00",
  "runs": [
    {
      "run": "01",
      "transcription_file": "image_name_run01.md",
      "questions_and_answers": [
        {"id": 1, "category": "easy", "question": "...", "reference_answer": "...", "model_answer": "..."}
      ]
    }
  ]
}
```

### QuestionSchema

A **QuestionSchema** defines custom question generation requirements.

**Storage:** User-provided JSON file via `--schema PATH`
**Purpose:** Define categories, counts, and prompts for question generation

**Schema:**
```json
{
  "categories": [
    {"name": "easy", "count": 2, "description": "Simple facts - single numbers, names, titles"},
    {"name": "medium_facts", "count": 2, "description": "Combined facts requiring synthesis of 2-3 pieces"},
    {"name": "hard_inference", "count": 3, "description": "Questions requiring logical inference"},
    {"name": "custom_category", "count": 3, "description": "Your custom category description"}
  ],
  "prompt_template": "Optional custom prompt. Use {categories_json} placeholder for category injection.",
  "output_format": {
    "require_reference_answer": true,
    "require_answerable_flag": true
  }
}
```

**Default schema** (used when no `--schema` provided):
```json
{
  "categories": [
    {"name": "easy", "count": 2, "description": "Simple facts - single numbers, names, titles"},
    {"name": "medium_facts", "count": 2, "description": "Combined facts requiring synthesis"},
    {"name": "medium_graphics", "count": 2, "description": "Graphical element semantics"},
    {"name": "hard_semantics", "count": 2, "description": "Deep understanding, sequences, dependencies"},
    {"name": "hard_graphics", "count": 2, "description": "Specific graphical details, colors, counts"}
  ]
}
```

### EvalScores

An **EvalScores** file contains LLM-as-judge scores for answers.

**Storage:** `{timestamp}_scores.json` in output folder
**Purpose:** Store evaluation scores with rationale

**Schema:**
```json
{
  "timestamp": "2026-01-22_19-33",
  "total_items": 1250,
  "average_score": 3.67,
  "pass_rate": 52.9,
  "score_distribution": {"0": 0, "1": 21, "2": 384, "3": 184, "4": 63, "5": 598},
  "category_averages": {"easy": 4.58, "medium_facts": 4.02, "hard_graphics": 3.18}
}
```

## 4. Functional Requirements

**LLMEV-FR-01: API Key Loading**
- Support `.env` format: `KEY_NAME=value`
- Support `key=value` format (same syntax, different file extension)
- Ignore lines starting with `#` (comments)
- Ignore empty lines
- Default location: `.env` in current working directory
- Override with `--keys PATH` parameter

**LLMEV-FR-02: Model ID Handling**
- Use original API model IDs exactly as provided by OpenAI/Anthropic
- No custom naming transformation (e.g., keep `gpt-4o` not `GPT-4o`)
- Validate model ID against `model-registry.json` if available
- Auto-detect provider from model ID prefix when possible

**LLMEV-FR-03: Single LLM Call (call-llm.py)**
- Support text-only input via `--prompt-file`
- Support image+text input via `--input-file` (image) and `--prompt-file`
- Auto-detect file type by suffix
- Support image formats: `.jpg, .jpeg, .png, .gif, .webp`
- Output to stdout by default, or file via `--output-file`
- Return token usage in JSON format via `--write-json-metadata` flag

**LLMEV-FR-04: Batch Process (call-llm-batch.py)**
- Process all files in `--input-folder` with configurable `--prompt-file`
- Auto-detect file type by suffix (no `--input-type` override)
- Support multiple runs per file via `--runs N`
- Support parallel processing via `--workers N` (default: 4)
- Skip existing outputs (resume capability)
- Save each output immediately after generation
- Output naming: `{source}__processed__{model}__run{NN}.md`
- Token usage: `_token_usage__{model}.json` (updated incrementally)
- Use cases: transcription, summarization, analysis, extraction

**LLMEV-FR-05: Question Generation (generate-questions.py)**
- Generate questions from ANY input type (image or text file)
- Auto-detect file type by suffix (no `--input-type` override)
- Support `--schema-file PATH` for custom question requirements (JSON file)
- Support parallel processing via `--workers N` (default: 4)
- Save incrementally after each item (thread-safe)
- Output JSON with questions and reference answers
- Default schema: 2 questions each for easy, medium_facts, medium_inference, hard_reasoning, hard_details

**LLMEV-FR-06: Answer Generation (generate-answers.py)**
- Answer questions from processed text (transcriptions, summaries, analyses)
- Process all runs for each source item
- Support parallel processing via `--workers N`
- Save incrementally after each item
- Output one JSON per source item with all runs

**LLMEV-FR-07: Evaluation Scoring (evaluate-answers.py)**
- Support LLM-as-judge evaluation via `--method llm`
- Support OpenAI Eval API via `--method openai-eval`
- Support parallel processing via `--workers N` (default: 4) for LLM method
- Score range 0-5 for both methods
- Calculate pass rate (score >= 4)
- Calculate category averages
- Save after EACH scored item (thread-safe)
- Save raw outputs before parsing (resilience)

**LLMEV-FR-08: Cost Analysis (analyze-costs.py)**
- Extract token counts from transcription files
- Calculate costs using `model-pricing.json`
- Output per-model summary with totals and averages
- Support custom pricing file via `--pricing PATH`

## 5. Design Decisions

**LLMEV-DD-01:** Use original API model IDs. Rationale: Avoids confusion, enables direct copy-paste from API docs, no translation layer needed.

**LLMEV-DD-02:** Keys file uses same format as `.env`. Rationale: Industry standard, works with existing tooling, easy to switch between formats.

**LLMEV-DD-03:** Incremental saving after EVERY item. Rationale: Prevents total data loss on crash, allows progress monitoring. File I/O cost is negligible compared to API latency.

**LLMEV-DD-04:** JSON output for all scripts. Rationale: Machine-readable, enables pipeline composition, easy to parse.

**LLMEV-DD-05:** Token usage stored in separate `_token_usage.json` files. Rationale: Keeps output files clean, structured JSON is easier to analyze, updated incrementally for crash resilience.

**LLMEV-DD-06:** Provider auto-detection from model ID prefix. Rationale: `claude-*` = anthropic, `gpt-*` = openai, `o1-*` = openai. Simplifies usage.

**LLMEV-DD-07:** Parallel processing as default for all batch operations. Rationale: API calls are I/O bound, parallelism dramatically improves throughput. Default 4 workers, configurable via `--workers N`.

**LLMEV-DD-08:** Thread-safe incremental saving with file locks. Rationale: Parallel workers must not corrupt output files when saving concurrently.

## 6. Implementation Guarantees

**LLMEV-IG-01:** Scripts MUST NOT modify input files.

**LLMEV-IG-02:** Scripts MUST save state after EACH completed item, before processing the next item.

**LLMEV-IG-03:** Scripts MUST handle API errors gracefully and continue processing remaining items.

**LLMEV-IG-04:** Scripts MUST validate model ID exists in registry before making API calls (if registry available).

**LLMEV-IG-05:** Scripts MUST respect `--output` path and not write elsewhere.

**LLMEV-IG-06:** Scripts MUST work without model-registry.json (use provider auto-detection).

## 7. Key Mechanisms

### API Key Loading

```python
def load_api_keys(keys_file: Path) -> dict:
    """Load API keys from .env or key=value file."""
    keys = {}
    with open(keys_file, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                keys[key.strip()] = value.strip()
    return keys
```

### Provider Auto-Detection

```python
def detect_provider(model_id: str) -> str:
    """Detect provider from model ID prefix."""
    if model_id.startswith('claude-'):
        return 'anthropic'
    elif model_id.startswith(('gpt-', 'o1-', 'o3-')):
        return 'openai'
    else:
        raise ValueError(f"Cannot detect provider for model: {model_id}")
```

### Incremental Saving Pattern (Sequential)

```python
for idx, item in enumerate(items):
    result = process_item(item)
    results.append(result)
    # Save after EACH item - file I/O is cheap, data loss is expensive
    save_json(output_file, {"processed": idx + 1, "results": results})
```

### Incremental Saving Pattern (Parallel)

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

results = []
file_lock = Lock()

def save_result(result):
    with file_lock:
        results.append(result)
        save_json(output_file, {"processed": len(results), "results": results})

with ThreadPoolExecutor(max_workers=workers) as executor:
    futures = {executor.submit(process_item, item): item for item in items}
    for future in as_completed(futures):
        result = future.result()
        save_result(result)  # Thread-safe incremental save
```

## 8. Action Flow

### Full Evaluation Pipeline

```
User has images to evaluate
├─> call-llm-batch.py --model MODEL --input-folder images/ --output-folder transcriptions/ --prompt-file transcribe.md
│   ├─> For each image:
│   │   ├─> Encode image to base64
│   │   ├─> Call LLM API with prompt
│   │   ├─> Save transcription_run{NN}.md
│   │   └─> Update _token_usage__{model}.json
│   └─> Save _summary.json
│
├─> generate-questions.py --model MODEL --input-folder images/ --output-file questions.json
│   ├─> For each image:
│   │   ├─> Call LLM API with question generation prompt
│   │   ├─> Parse JSON response
│   │   └─> Save incrementally
│   └─> Output: questions.json
│
├─> generate-answers.py --model MODEL --input-folder transcriptions/ --questions-file questions.json --output-folder answers/
│   ├─> For each image:
│   │   ├─> Find all transcription runs
│   │   ├─> For each run:
│   │   │   ├─> Read transcription text
│   │   │   ├─> Call LLM API with questions
│   │   │   └─> Parse answers
│   │   └─> Save {image}_answers.json
│   └─> Save _summary.json
│
├─> evaluate-answers.py --method llm --model JUDGE_MODEL --input-folder answers/ --output-folder scores/
│   ├─> Collect all question-answer pairs
│   ├─> For each pair:
│   │   ├─> Call judge LLM with scoring prompt
│   │   ├─> Extract score and rationale
│   │   └─> Save incrementally
│   └─> Output: scores.json, summary.json
│
└─> analyze-costs.py --input-folder transcriptions/ --pricing model-pricing.json
    ├─> Extract token counts from files
    ├─> Calculate costs per model
    └─> Output: cost_analysis.json
```

## 9. Data Structures

### Keys File (.env format)

```
OPENAI_API_KEY=sk-proj-...
OPENAI_ORGANIZATION=org-...
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### Model Registry (model-registry.json)

```json
{
  "models": [
    {"provider": "openai", "model_id": "gpt-4o", "name": "GPT-4o", "enabled": true, "status": "available"},
    {"provider": "openai", "model_id": "gpt-5-mini", "name": "GPT-5 Mini", "enabled": true, "status": "available"},
    {"provider": "anthropic", "model_id": "claude-opus-4-20250514", "name": "Claude Opus 4", "enabled": true, "status": "available"},
    {"provider": "anthropic", "model_id": "claude-3-5-haiku-20241022", "name": "Claude Haiku 3.5", "enabled": true, "status": "available"}
  ],
  "metadata": {"updated": "2026-01-22"}
}
```

### Model Pricing (model-pricing.json)

```json
{
  "pricing": {
    "openai": {
      "gpt-4o": {"input_per_1m": 2.50, "output_per_1m": 10.00, "currency": "USD"},
      "gpt-5-mini": {"input_per_1m": 1.00, "output_per_1m": 4.00, "currency": "USD"}
    },
    "anthropic": {
      "claude-opus-4-20250514": {"input_per_1m": 15.00, "output_per_1m": 75.00, "currency": "USD"},
      "claude-3-5-haiku-20241022": {"input_per_1m": 0.80, "output_per_1m": 4.00, "currency": "USD"}
    }
  }
}
```

### Processed Output (*.md)

```markdown
# Document Transcription

[Content here - clean output, no metadata embedded]
```

### Token Usage (_token_usage.json)

Stored separately from output files, updated incrementally after each item.

```json
{
  "model_id": "claude-opus-4-20250514",
  "generated": "2026-01-22T17:31:24+00:00",
  "total_input_tokens": 54500,
  "total_output_tokens": 26225,
  "items": [
    {"file": "image1_run01.md", "input_tokens": 2180, "output_tokens": 1049, "timestamp": "2026-01-22T17:30:15+00:00"},
    {"file": "image1_run02.md", "input_tokens": 2180, "output_tokens": 982, "timestamp": "2026-01-22T17:30:45+00:00"}
  ]
}
```

## 10. Implementation Details

### Default Output Folder Structure

When user runs evaluation pipeline, results are stored in a structured folder:

```
{project_root}/llm-eval/{eval_name}/
│
├── _config__{eval_name}.json
│
├── processed/
│   ├── {source}__processed__{model}__run01.md
│   ├── {source}__processed__{model}__run02.md
│   └── _token_usage__{model}.json
│
├── questions/
│   └── questions__from__{input_type}__{model}__{timestamp}.json
│
├── answers/
│   ├── {source}__answers__{process_model}__{answer_model}.json
│   └── _summary__answers__{process_model}__{answer_model}.json
│
├── scores/
│   ├── scores__{process_model}__{answer_model}__judged__{judge_model}__{timestamp}.json
│   └── _summary__scores__{judge_model}__{timestamp}.json
│
└── analysis/
    └── cost_analysis__{timestamp}.json
```

### Filename Convention

**Pattern:** `{what}__{context}__{model}__{qualifier}.{ext}`

**Separator:** Double underscore `__` separates semantic parts (single `_` allowed within parts)

**Examples:**
- `image001__processed__claude-opus-4-20250514__run01.md`
- `questions__from__image__gpt-4o__2026-01-22T20-15.json`
- `doc005__answers__claude-opus-4__gpt-5-mini.json`
- `scores__claude-opus-4__gpt-5-mini__judged__gpt-5__2026-01-22T20-30.json`

**Principles:**
- Filename alone tells you: what it is, what model(s), what source, when
- No information loss - can reconstruct context from filename
- Sortable - related files group together alphabetically
- Parseable - split on `__` to extract components

### Skill Folder Structure

```
.windsurf/skills/llm-evaluation/
├── SKILL.md                  # Skill documentation
├── call-llm.py               # Single LLM call
├── call-llm-batch.py         # Batch LLM calls
├── generate-questions.py     # Generate eval questions
├── generate-answers.py       # Generate answers from text
├── evaluate-answers.py       # Score with LLM-as-judge
├── analyze-costs.py          # Token cost analysis
├── model-registry.json       # Model IDs and providers
├── model-pricing.json        # Token pricing
├── prompts/
│   ├── transcribe-page.md   # Default prompt for image transcription
│   ├── summarize-text.md     # Default prompt for text summarization
│   ├── answer-from-text.md   # Default for generate-answers.py
│   └── judge-answer.md       # Default for evaluate-answers.py
└── schemas/
    └── default-questions.json # Default question schema
```

### CLI Interface Pattern

All scripts follow consistent CLI pattern:

```
python script.py --model MODEL_ID [--keys-file KEYS_FILE] [--input-folder PATH] [--output-folder PATH] [options]

Common flags:
  --model MODEL_ID      Required. API model ID (e.g., gpt-4o, claude-opus-4-20250514)
  --keys-file PATH      API keys file. Default: .env in cwd
  --workers N           Parallel workers (default: 4)
  --help                Show help
```

**Script-specific flags:**

**call-llm-batch.py:**
- `--input-folder PATH` - Folder with input files
- `--output-folder PATH` - Folder for output files
- `--prompt-file PATH` - Prompt file (.md)
- `--runs N` - Number of runs per file (default: 1)

**generate-questions.py:**
- `--input-folder PATH` - Folder with source files
- `--output-file PATH` - Output .json file
- `--schema-file PATH` - Question requirements schema (JSON file)

**generate-answers.py:**
- `--input-folder PATH` - Folder with .md files (output of call-llm-batch.py)
- `--output-folder PATH` - Folder for .json answer files
- `--questions-file PATH` - Questions .json file (output of generate-questions.py)
- `--prompt-file PATH` - Custom answering prompt

**evaluate-answers.py:**
- `--input-folder PATH` - Folder with .json answer files
- `--output-folder PATH` - Folder for .json score files
- `--method METHOD` - Evaluation method: `llm` or `openai-eval`
- `--judge-prompt PATH` - Custom judge prompt for scoring
- `--pass-threshold N` - Pass threshold score (default: 4)

**analyze-costs.py:**
- `--input-folder PATH` - Folder with _token_usage__.json files
- `--output-file PATH` - Output .json file
- `--pricing PATH` - Custom pricing JSON file

### Dependencies

```
openai>=1.0.0
anthropic>=0.18.0
```

## 11. Document History

**[2026-01-22 21:03]**
- Fixed: Script names updated throughout (call-llm.py, call-llm-batch.py, generate-answers.py)
- Fixed: Parameter names made explicit (--keys-file, --input-folder, --output-folder, --prompt-file)
- Fixed: Removed --input-type override (auto-detect only)
- Fixed: Removed --questions-per-item (use --schema-file)
- Added: File type annotations to all input/output parameters
- Added: Pipeline dependency notes to parameters

**[2026-01-22 20:19]**
- Added: Concurrency (`--workers N`) as standard feature for all batch scripts
- Changed: Strengthened incremental save policy - MUST save after EACH item
- Added: Thread-safe incremental saving pattern for parallel execution
- Added: LLMEV-DD-08 for thread-safe file operations

**[2026-01-22 20:16]**
- Initial specification created
- Analyzed 7 source scripts from _ModelComparisonTest
- Defined 8 functional requirements
- Defined 7 design decisions
- Defined 6 implementation guarantees
