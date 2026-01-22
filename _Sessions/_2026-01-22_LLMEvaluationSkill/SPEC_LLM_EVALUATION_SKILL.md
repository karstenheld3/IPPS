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
- No hardcoded paths - use `--keys`, `--input`, `--output` parameters

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

## 1. Scenario

**Problem:** Evaluating LLM output quality requires multiple steps: processing, question generation, answer generation, and scoring. Current scripts are hardcoded to specific input types (images only) and session folders.

**Solution:**
- Create input-agnostic scripts that work with images, text files, PDFs, or any content
- Use `--input-type` parameter to specify: `image`, `text`, `auto` (detect from extension)
- Use original API model IDs (no custom naming)
- Support both `.env` and `key=value` API key formats
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

This skill extracts and generalizes scripts created during the ASCII Art Transcription optimization session. The original scripts in `_ModelComparisonTest/` folder implemented a full evaluation pipeline but were tied to session-specific paths.

**Source scripts analyzed:**
- `transcribe-image.py` - Single image transcription
- `parallel-runner.py` - Batch transcription with runs
- `generate-eval-questions.py` - Question generation from images
- `answer-from-transcription.py` - Answer questions from text
- `evaluate-with-openai-eval.py` - OpenAI Eval API scoring
- `validate-eval-questions.py` - Question validation with LLM-as-judge
- `collect-token-data.py` - Token cost analysis

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

**LLMEV-FR-03: Single LLM Call (llm-call.py)**
- Support text-only input via `--input` or stdin
- Support image+text input via `--image` and `--input`
- Support file input via `--file PATH` (reads file content as input)
- Support image formats: `.jpg, .jpeg, .png, .gif, .webp`
- Output to stdout by default, or file via `--output`
- Return token usage in JSON format via `--json` flag

**LLMEV-FR-04: Batch Process (batch-process.py)**
- Process all files in input folder with configurable prompt
- Support `--input-type` parameter: `image`, `text`, `auto` (detect from extension)
- Support multiple runs per file via `--runs N`
- Support parallel processing via `--workers N` (default: 4)
- Skip existing outputs (resume capability)
- Save each output immediately after generation
- Output naming: `{file_stem}_run{NN}.md` (clean output, no metadata)
- Token usage stored separately in `_token_usage.json` (updated incrementally)
- Use cases: transcription, summarization, analysis, extraction

**LLMEV-FR-05: Question Generation (generate-questions.py)**
- Generate questions from ANY input type (image or text file)
- Support `--input-type` parameter: `image`, `text`, `auto`
- Support `--schema PATH` for custom question requirements (JSON file)
- Support `--questions-per-item N` as simple override (default 10)
- Support parallel processing via `--workers N` (default: 4)
- Save incrementally after each item (thread-safe)
- Output JSON with questions and reference answers
- Default schema: 2 questions each for easy, medium_facts, medium_inference, hard_reasoning, hard_details

**LLMEV-FR-06: Answer Generation (answer-questions.py)**
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
├─> batch-transcribe.py --model MODEL --input images/ --output transcriptions/
│   ├─> For each image:
│   │   ├─> Encode image to base64
│   │   ├─> Call LLM API with prompt
│   │   ├─> Save transcription_run{NN}.md
│   │   └─> Embed token usage as comment
│   └─> Save _summary.json
│
├─> generate-questions.py --model MODEL --input images/ --output questions.json
│   ├─> For each image:
│   │   ├─> Call LLM API with question generation prompt
│   │   ├─> Parse JSON response
│   │   └─> Save incrementally
│   └─> Output: questions.json
│
├─> answer-questions.py --model MODEL --input transcriptions/ --questions questions.json --output answers/
│   ├─> For each image:
│   │   ├─> Find all transcription runs
│   │   ├─> For each run:
│   │   │   ├─> Read transcription text
│   │   │   ├─> Call LLM API with questions
│   │   │   └─> Parse answers
│   │   └─> Save {image}_answers.json
│   └─> Save _summary.json
│
├─> evaluate-answers.py --method llm --model JUDGE_MODEL --input answers/ --output scores/
│   ├─> Collect all question-answer pairs
│   ├─> For each pair:
│   │   ├─> Call judge LLM with scoring prompt
│   │   ├─> Extract score and rationale
│   │   └─> Save incrementally
│   └─> Output: scores.json, summary.json
│
└─> analyze-costs.py --input transcriptions/ --pricing model-pricing.json
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

```bash
{project_root}/llm-eval/
├── {eval_name}/                          # Named evaluation run (e.g., "ascii-transcription-2026-01")
│   ├── config.json                       # Evaluation configuration snapshot
│   ├── input/                            # Symlink or copy of source files
│   │
│   ├── processed/                        # Output from batch-process.py
│   │   ├── {model_id}/                   # One folder per model
│   │   │   ├── {file_stem}_run01.md
│   │   │   ├── {file_stem}_run02.md
│   │   │   └── _token_usage.json
│   │   └── {another_model_id}/
│   │
│   ├── questions/                        # Output from generate-questions.py
│   │   └── questions.json
│   │
│   ├── answers/                          # Output from answer-questions.py
│   │   ├── {transcription_model}_{answer_model}/
│   │   │   ├── {file_stem}_answers.json
│   │   │   └── _summary.json
│   │   └── {another_combination}/
│   │
│   ├── scores/                           # Output from evaluate-answers.py
│   │   ├── {timestamp}_scores.json
│   │   └── {timestamp}_summary.json
│   │
│   └── analysis/                         # Output from analyze-costs.py
│       └── cost_analysis.json
```

**Conventions:**
- `{model_id}` uses original API model ID (e.g., `claude-opus-4-20250514`)
- `{eval_name}` is user-provided or auto-generated from timestamp
- `config.json` captures all parameters used for reproducibility
- Each script defaults to appropriate subfolder but can be overridden with `--output`

### Skill Folder Structure

```
.windsurf/skills/llm-evaluation/
├── SKILL.md                  # Skill documentation
├── llm-call.py               # Single LLM API call (text or image)
├── batch-process.py          # Batch process any input (images, text, PDFs)
├── generate-questions.py     # Generate eval questions from any input
├── answer-questions.py       # Answer questions from processed text
├── evaluate-answers.py       # Score answers with LLM
├── analyze-costs.py          # Token cost analysis
├── model-registry.json       # Model IDs and providers
├── model-pricing.json        # Token pricing
├── prompts/
│   ├── process-image-prompt.md     # Default for image processing (transcription)
│   ├── process-text-prompt.md      # Default for text processing (summarization)
│   ├── answering-prompt.md         # Default for --answering-prompt
│   └── judge-prompt.md             # Default for --judge-prompt
└── schemas/
    └── default-question-schema.json # Default schema with categories + prompt
```

### CLI Interface Pattern

All scripts follow consistent CLI pattern:

```
python script.py --model MODEL_ID [--keys KEYS_FILE] [--input PATH] [--output PATH] [options]

Common flags:
  --model MODEL_ID    Required. API model ID (e.g., gpt-4o, claude-opus-4-20250514)
  --keys PATH         API keys file. Default: .env in cwd
  --input PATH        Input file or folder
  --output PATH       Output file or folder
  --json              Output JSON to stdout
  --verbose           Verbose logging
  --help              Show help
```

### Script-Specific Parameters

**llm-call.py:**
- `--image PATH` - Image file for multimodal call
- `--system-prompt PATH` - System prompt file
- `--user-prompt PATH` - User prompt file (overrides --input for prompt text)

**batch-process.py:**
- `--input-type TYPE` - Input type: `image`, `text`, `auto` (default: auto)
- `--runs N` - Number of runs per file (default: 5)
- `--workers N` - Parallel workers (default: 4)
- `--process-prompt PATH` - Custom processing prompt (transcription, summarization, etc.)
- `--max-tokens N` - Max output tokens (default: 8192)

**generate-questions.py:**
- `--input-type TYPE` - Input type: `image`, `text`, `auto` (default: auto)
- `--schema PATH` - Question requirements schema (JSON file, includes categories + optional prompt_template)
- `--questions-per-item N` - Simple override: total questions (uses default prompt, ignores schema)
- `--workers N` - Parallel workers (default: 4)

**answer-questions.py:**
- `--questions PATH` - Eval questions JSON file (required)
- `--workers N` - Parallel workers (default: 4)
- `--answering-prompt PATH` - Custom answering prompt (how to answer from transcription)

**evaluate-answers.py:**
- `--method METHOD` - Evaluation method: `llm` or `openai-eval`
- `--judge-model MODEL` - Judge model ID (for --method llm)
- `--judge-prompt PATH` - Custom judge prompt for scoring
- `--pass-threshold N` - Pass threshold score (default: 4)

**analyze-costs.py:**
- `--pricing PATH` - Custom pricing JSON file

### Dependencies

```
openai>=1.0.0
anthropic>=0.18.0
```

## 11. Document History

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
