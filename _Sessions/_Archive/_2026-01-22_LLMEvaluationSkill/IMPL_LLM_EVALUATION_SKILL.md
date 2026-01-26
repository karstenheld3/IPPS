# IMPL: LLM Evaluation Skill

**Doc ID**: LLMEV-IP01
**Feature**: llm-evaluation-skill
**Goal**: Implement generic LLM evaluation pipeline scripts for the llm-evaluation skill
**Timeline**: Created 2026-01-22, Updated 0 times

**Target files**:
- `.windsurf/skills/llm-evaluation/SKILL.md` (NEW)
- `.windsurf/skills/llm-evaluation/call-llm.py` (NEW ~150 lines)
- `.windsurf/skills/llm-evaluation/call-llm-batch.py` (NEW ~250 lines)
- `.windsurf/skills/llm-evaluation/generate-questions.py` (NEW ~200 lines)
- `.windsurf/skills/llm-evaluation/generate-answers.py` (NEW ~200 lines)
- `.windsurf/skills/llm-evaluation/evaluate-answers.py` (NEW ~250 lines)
- `.windsurf/skills/llm-evaluation/analyze-costs.py` (NEW ~100 lines)
- `.windsurf/skills/llm-evaluation/model-registry.json` (NEW)
- `.windsurf/skills/llm-evaluation/model-pricing.json` (NEW)
- `.windsurf/skills/llm-evaluation/prompts/*.md` (NEW, 4 files)
- `.windsurf/skills/llm-evaluation/schemas/default-questions.json` (NEW)
- `.windsurf/skills/llm-evaluation/requirements.txt` (NEW)

**Depends on:**
- `SPEC_LLM_EVALUATION_SKILL.md` [LLMEV-SP01] for all requirements

## MUST-NOT-FORGET

- **INCREMENTAL SAVE**: Write results after EACH item, not at end
- **RETRY**: 3x with exponential backoff (1s, 2s, 4s) for transient errors
- **ATOMIC WRITES**: Write to `.tmp`, rename on success
- **LOGGING**: Format `[ worker N ] [ x / n ] action...` (1-indexed worker IDs)
- **CONCURRENCY**: Use `concurrent.futures.ThreadPoolExecutor` + `threading.Lock`
- Reference: `E:\Dev\OpenAI-BackendTools\src\openai_backendtools.py` for patterns

## Table of Contents

1. [File Structure](#1-file-structure)
2. [Edge Cases](#2-edge-cases)
3. [Implementation Steps](#3-implementation-steps)
4. [Test Cases](#4-test-cases)
5. [Verification Checklist](#5-verification-checklist)
6. [Document History](#6-document-history)

## 1. File Structure

```
.windsurf/skills/llm-evaluation/
├── SKILL.md                      # Skill documentation (~50 lines) [NEW]
├── requirements.txt              # Dependencies [NEW]
├── call-llm.py                   # Single LLM call (~150 lines) [NEW]
├── call-llm-batch.py             # Batch LLM calls (~250 lines) [NEW]
├── generate-questions.py         # Question generation (~200 lines) [NEW]
├── generate-answers.py           # Answer generation (~200 lines) [NEW]
├── evaluate-answers.py           # LLM-as-judge scoring (~250 lines) [NEW]
├── analyze-costs.py              # Token cost analysis (~100 lines) [NEW]
├── model-registry.json           # Model definitions [NEW]
├── model-pricing.json            # Token pricing [NEW]
├── prompts/
│   ├── transcribe-page.md        # Image transcription prompt [NEW]
│   ├── summarize-text.md         # Text summarization prompt [NEW]
│   ├── answer-from-text.md       # Q&A prompt [NEW]
│   └── judge-answer.md           # Scoring prompt [NEW]
└── schemas/
    └── default-questions.json    # Default question schema [NEW]
```

## 2. Edge Cases

### Input Validation
- **LLMEV-IP01-EC-01**: Empty input folder -> Exit with error "No files found in {folder}"
- **LLMEV-IP01-EC-02**: Unknown file suffix -> Exit with error "Unknown file type: {suffix}"
- **LLMEV-IP01-EC-03**: Missing API key -> Exit with error "Missing {PROVIDER}_API_KEY in keys file"
- **LLMEV-IP01-EC-04**: Invalid model ID -> Exit with error "Cannot detect provider for model: {id}"

### API Errors
- **LLMEV-IP01-EC-05**: Rate limit (429) -> Retry 3x with backoff, then skip item
- **LLMEV-IP01-EC-06**: Server error (5xx) -> Retry 3x with backoff, then skip item
- **LLMEV-IP01-EC-07**: Network timeout -> Retry 3x with backoff, then skip item
- **LLMEV-IP01-EC-08**: Invalid API response -> Log warning, save raw response

### File Operations
- **LLMEV-IP01-EC-09**: Output file exists -> Skip (resume mode) unless --force
- **LLMEV-IP01-EC-10**: Temp file exists (.tmp) -> Reprocess (incomplete from crash)
- **LLMEV-IP01-EC-11**: Image encoding failure -> Retry 3x, then skip with error logged

### Response Parsing
- **LLMEV-IP01-EC-12**: Malformed JSON response -> Strip markdown fences, retry parse
- **LLMEV-IP01-EC-13**: Missing expected fields -> Log warning, use defaults
- **LLMEV-IP01-EC-14**: Workers set to 0 -> Default to 1 with warning

## 3. Implementation Steps

### Phase 1: Core Infrastructure

#### LLMEV-IP01-IS-01: Create requirements.txt

**Location**: `.windsurf/skills/llm-evaluation/requirements.txt`

**Action**: Add - Python dependencies

**Code**:
```
openai>=1.0.0
anthropic>=0.18.0
```

#### LLMEV-IP01-IS-02: Create shared utilities module pattern

**Location**: Each script (inline, no shared module to keep scripts self-contained)

**Action**: Add - Common functions to each script

**Code**:
```python
# Standard pattern for all scripts
import os, sys, json, time, argparse, base64
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

UNKNOWN = '[UNKNOWN]'

def load_api_keys(keys_file: Path) -> dict: ...
def detect_provider(model_id: str) -> str: ...
def retry_with_backoff(fn, retries=3, backoff=(1,2,4)): ...
def atomic_write_json(path: Path, data: dict, lock: Lock): ...
def log(worker_id: int, current: int, total: int, msg: str): ...  # outputs [ worker {id+1} ]
```

### Phase 2: Single Call Script

#### LLMEV-IP01-IS-03: Implement call-llm.py

**Location**: `.windsurf/skills/llm-evaluation/call-llm.py`

**Action**: Add - Single LLM call with image/text auto-detection

**Code**:
```python
# CLI: python call-llm.py --model MODEL --input-file FILE --prompt-file PROMPT
def main():
  args = parse_args()
  keys = load_api_keys(args.keys_file)
  provider = detect_provider(args.model)
  client = create_client(provider, keys)
  
  # Auto-detect input type
  input_type = detect_file_type(args.input_file)
  
  # Build request
  if input_type == 'image':
    content = encode_image_with_retry(args.input_file)
  else:
    content = read_text_file(args.input_file)
  
  # Call API with retry
  response = retry_with_backoff(lambda: call_api(client, args.model, content, prompt))
  
  # Output
  if args.output_file:
    write_output(args.output_file, response)
  else:
    print(response.text)
```

### Phase 3: Batch Processing Script

#### LLMEV-IP01-IS-04: Implement call-llm-batch.py

**Location**: `.windsurf/skills/llm-evaluation/call-llm-batch.py`

**Action**: Add - Batch processing with parallel workers

**Code**:
```python
# CLI: python call-llm-batch.py --model MODEL --input-folder IN --output-folder OUT --prompt-file PROMPT
def process_file(worker_id, file_path, args, client, results_lock, token_usage_lock):
  # Check resume (skip if output exists and not .tmp)
  output_path = get_output_path(file_path, args)
  if output_path.exists() and not output_path.with_suffix('.tmp').exists():
    log(worker_id, "Skipping (exists)")
    return
  
  # Process with retry
  for run in range(args.runs):
    result = retry_with_backoff(lambda: call_api(...))
    
    # Atomic write
    atomic_write_json(output_path, result, results_lock)
    
    # Update token usage
    update_token_usage(args.output_folder, args.model, result.usage, token_usage_lock)

def main():
  # ThreadPoolExecutor for parallel processing
  with ThreadPoolExecutor(max_workers=args.workers) as executor:
    futures = {executor.submit(process_file, i, f, ...): f for i, f in enumerate(files)}
    for future in as_completed(futures):
      future.result()  # Propagate exceptions
```

### Phase 4: Question Generation Script

#### LLMEV-IP01-IS-05: Implement generate-questions.py

**Location**: `.windsurf/skills/llm-evaluation/generate-questions.py`

**Action**: Add - Generate evaluation questions from source files

**Code**:
```python
# CLI: python generate-questions.py --model MODEL --input-folder IN --output-file OUT
def generate_questions_for_file(worker_id, file_path, schema, client, args):
  # Build prompt with schema
  prompt = build_question_prompt(file_path, schema)
  
  # Call API
  response = retry_with_backoff(lambda: call_api(client, args.model, prompt))
  
  # Parse JSON (strip markdown fences)
  questions = parse_json_response(response.text)
  return questions

def main():
  schema = load_schema(args.schema_file)
  results = {"generated": now_iso(), "model": args.model, "images": {}}
  
  with ThreadPoolExecutor(max_workers=args.workers) as executor:
    # Process files in parallel, save incrementally
    ...
```

### Phase 5: Answer Generation Script

#### LLMEV-IP01-IS-06: Implement generate-answers.py

**Location**: `.windsurf/skills/llm-evaluation/generate-answers.py`

**Action**: Add - Generate answers from processed text

**Code**:
```python
# CLI: python generate-answers.py --model MODEL --input-folder IN --output-folder OUT --questions-file Q
def generate_answers_for_item(worker_id, item_name, transcription_files, questions, client, args):
  results = {"image_name": item_name, "model_id": args.model, "runs": []}
  
  for run_file in transcription_files:
    text = read_file(run_file)
    answers = []
    
    for q in questions:
      prompt = build_answer_prompt(text, q)
      response = retry_with_backoff(lambda: call_api(...))
      answers.append({"id": q["id"], "question": q["question"], "model_answer": response.text})
    
    results["runs"].append({"run": run_file.stem, "questions_and_answers": answers})
  
  return results
```

### Phase 6: Evaluation Script

#### LLMEV-IP01-IS-07: Implement evaluate-answers.py (LLM method)

**Location**: `.windsurf/skills/llm-evaluation/evaluate-answers.py`

**Action**: Add - LLM-as-judge scoring with `--method llm`

**Code**:
```python
# CLI: python evaluate-answers.py --model MODEL --input-folder IN --output-folder OUT --method llm
def score_answer(worker_id, qa_pair, judge_prompt, client, args):
  prompt = build_judge_prompt(qa_pair, judge_prompt)
  response = retry_with_backoff(lambda: call_api(...))
  
  # Parse score (0-5)
  score = parse_score(response.text)
  return {"score": score, "rationale": response.text}

def main():
  # Aggregate scores, calculate pass rate
  ...
```

#### LLMEV-IP01-IS-07b: Implement evaluate-answers.py (OpenAI Eval API method)

**Location**: `.windsurf/skills/llm-evaluation/evaluate-answers.py`

**Action**: Add - OpenAI Eval API scoring with `--method openai-eval`

**Reference**: `https://github.com/karstenheld3/OpenAI-BackendTools/blob/main/src/test_eval_operations.py`

**Code**:
```python
# CLI: python evaluate-answers.py --model MODEL --input-folder IN --output-folder OUT --method openai-eval
def score_answers_using_openai_eval(client, items, eval_model, pass_threshold):
  # 1. Create eval config with score_model grader
  eval_cfg = client.evals.create(
    name=eval_name,
    data_source_config={"type": "custom", "item_schema": {...}},
    testing_criteria=[{
      "type": "score_model", "model": eval_model,
      "input": [{"role": "system", "content": prompt_template}],
      "range": [0, 5], "pass_threshold": pass_threshold
    }]
  )
  
  # 2. Create and run evaluation
  eval_run = client.evals.runs.create(
    eval_id=eval_cfg.id,
    data_source={"type": "jsonl", "source": {"type": "file_content", "content": items}}
  )
  
  # 3. Poll for completion
  while status != "completed":
    status = client.evals.runs.retrieve(eval_run.id, eval_id=eval_cfg.id).status
    time.sleep(10)
  
  # 4. Get output items and extract scores
  output_items = get_all_eval_run_output_items(client, run_id=eval_run.id, eval_id=eval_cfg.id)
  for item in output_items:
    score = item.results[0].score
    rationale = item.results[0].rationale
```

**Item schema**: `{input: str, reference: str, output_text: str}`

**Status**: IMPLEMENTED (2026-01-23) - tested with gpt-4o, 3/3 passed

### Phase 7: Cost Analysis Script

#### LLMEV-IP01-IS-08: Implement analyze-costs.py

**Location**: `.windsurf/skills/llm-evaluation/analyze-costs.py`

**Action**: Add - Token cost analysis

**Code**:
```python
# CLI: python analyze-costs.py --input-folder IN --output-file OUT
def main():
  # Find all _token_usage_*.json files
  usage_files = list(args.input_folder.glob("_token_usage_*.json"))
  
  # Load pricing
  pricing = load_pricing(args.pricing)
  
  # Calculate costs per model
  for usage_file in usage_files:
    model = extract_model_from_filename(usage_file)
    data = json.load(usage_file.open())
    cost = calculate_cost(data, pricing[model])
    ...
```

### Phase 8: Configuration Files

#### LLMEV-IP01-IS-09: Create model-registry.json

**Location**: `.windsurf/skills/llm-evaluation/model-registry.json`

**Action**: Add - Model definitions

**Code**:
```json
{
  "models": [
    {"provider": "openai", "model_id": "gpt-4o", "name": "GPT-4o", "enabled": true, "status": "available"},
    {"provider": "openai", "model_id": "gpt-5-mini", "name": "GPT-5 Mini", "enabled": true, "status": "available"},
    {"provider": "anthropic", "model_id": "claude-opus-4-20250514", "name": "Claude Opus 4", "enabled": true, "status": "available"},
    {"provider": "anthropic", "model_id": "claude-3-5-haiku-20241022", "name": "Claude Haiku 3.5", "enabled": true, "status": "available"}
  ]
}
```

#### LLMEV-IP01-IS-10: Create model-pricing.json

**Location**: `.windsurf/skills/llm-evaluation/model-pricing.json`

**Action**: Add - Token pricing

**Code**:
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

### Phase 9: Prompt Files

#### LLMEV-IP01-IS-11: Create default prompts

**Location**: `.windsurf/skills/llm-evaluation/prompts/`

**Action**: Add - 4 prompt files

**Files**:
- `transcribe-page.md` - "Transcribe this page exactly as shown..."
- `summarize-text.md` - "Summarize the following text..."
- `answer-from-text.md` - "Based on the text, answer: {question}"
- `judge-answer.md` - "Score 0-5 how well the answer matches..."

#### LLMEV-IP01-IS-12: Create default question schema

**Location**: `.windsurf/skills/llm-evaluation/schemas/default-questions.json`

**Action**: Add - Default question categories

**Code**:
```json
{
  "categories": [
    {"name": "easy", "count": 2, "description": "Simple facts"},
    {"name": "medium_facts", "count": 2, "description": "Combined facts"},
    {"name": "medium_inference", "count": 2, "description": "Simple inference"},
    {"name": "hard_reasoning", "count": 2, "description": "Complex reasoning"},
    {"name": "hard_details", "count": 2, "description": "Specific details"}
  ]
}
```

### Phase 10: Skill Documentation

#### LLMEV-IP01-IS-13: Create SKILL.md

**Location**: `.windsurf/skills/llm-evaluation/SKILL.md`

**Action**: Add - Skill documentation

**Content**: Copy Skill Summary section from SPEC

## 4. Test Cases

### Category 1: API Key Loading (3 tests)

- **LLMEV-IP01-TC-01**: Load .env format -> ok=true, keys dict populated
- **LLMEV-IP01-TC-02**: Missing key file -> ok=false, "Keys file not found"
- **LLMEV-IP01-TC-03**: Invalid format -> ok=false, "Invalid keys format"

### Category 2: File Type Detection (4 tests)

- **LLMEV-IP01-TC-04**: .jpg file -> ok=true, type="image"
- **LLMEV-IP01-TC-05**: .md file -> ok=true, type="text"
- **LLMEV-IP01-TC-06**: .xyz file -> ok=false, "Unknown file type"
- **LLMEV-IP01-TC-07**: No extension -> ok=false, "Unknown file type"

### Category 3: Retry Logic (3 tests)

- **LLMEV-IP01-TC-08**: Success on first try -> ok=true, 1 attempt
- **LLMEV-IP01-TC-09**: Success on retry -> ok=true, 2-3 attempts
- **LLMEV-IP01-TC-10**: All retries fail -> ok=false, item skipped

### Category 4: Resume Capability (3 tests)

- **LLMEV-IP01-TC-11**: Output exists -> ok=true, skipped
- **LLMEV-IP01-TC-12**: .tmp exists -> ok=true, reprocessed
- **LLMEV-IP01-TC-13**: Neither exists -> ok=true, processed

### Category 5: JSON Parsing (3 tests)

- **LLMEV-IP01-TC-14**: Clean JSON -> ok=true, parsed
- **LLMEV-IP01-TC-15**: Markdown-wrapped JSON -> ok=true, fences stripped
- **LLMEV-IP01-TC-16**: Invalid JSON -> ok=false, error logged

## 5. Verification Checklist

### Prerequisites
- [ ] **LLMEV-IP01-VC-01**: SPEC_LLM_EVALUATION_SKILL.md [LLMEV-SP01] read
- [ ] **LLMEV-IP01-VC-02**: openai_backendtools.py patterns reviewed

### Phase 1: Infrastructure
- [ ] **LLMEV-IP01-VC-03**: requirements.txt created
- [ ] **LLMEV-IP01-VC-04**: Shared utility functions implemented in scripts

### Phase 2-7: Scripts
- [ ] **LLMEV-IP01-VC-05**: call-llm.py works (single image, single text)
- [ ] **LLMEV-IP01-VC-06**: call-llm-batch.py works (parallel, resume, incremental save)
- [ ] **LLMEV-IP01-VC-07**: generate-questions.py works (schema support)
- [ ] **LLMEV-IP01-VC-08**: generate-answers.py works (multi-run support)
- [ ] **LLMEV-IP01-VC-09**: evaluate-answers.py works (LLM judge)
- [ ] **LLMEV-IP01-VC-10**: analyze-costs.py works (pricing calculation)

### Phase 8-10: Configuration
- [ ] **LLMEV-IP01-VC-11**: model-registry.json valid
- [ ] **LLMEV-IP01-VC-12**: model-pricing.json valid
- [ ] **LLMEV-IP01-VC-13**: All prompts created
- [ ] **LLMEV-IP01-VC-14**: SKILL.md created

### Validation
- [ ] **LLMEV-IP01-VC-15**: All TC-* test cases pass
- [ ] **LLMEV-IP01-VC-16**: End-to-end pipeline test (image -> score)
- [ ] **LLMEV-IP01-VC-17**: Resume after simulated crash works

## 6. Document History

**[2026-01-23 10:40]**
- Added: LLMEV-IP01-IS-07b for OpenAI Eval API method
- Reference: test_eval_operations.py from OpenAI-BackendTools
- Status: NOT YET IMPLEMENTED (stub returns error)

**[2026-01-22 21:25]**
- Fixed: Added `status` field to model-registry.json per SPEC
- Fixed: Added `currency` field to model-pricing.json per SPEC
- Added: EC-14 for --workers 0 edge case

**[2026-01-22 21:24]**
- Initial implementation plan created
- 13 implementation steps across 10 phases
- 16 test cases across 5 categories
- 17 verification checklist items

