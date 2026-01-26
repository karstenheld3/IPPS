# IMPL: LLM Image Transcription Pipeline

**Doc ID**: LLMTR-IP01
**Feature**: llm-transcription-pipeline
**Goal**: Implement ensemble+judge+refinement pipeline for high-quality image-to-markdown transcription
**Timeline**: Created 2026-01-27

**Target files**:
- `DevSystemV3.2/skills/llm-transcription/transcribe-image-to-markdown-advanced.py` (REWRITE ~600 lines)

**Depends on:**
- `_SPEC_LLM_TRANSCRIPTION_IMAGES.md [LLMTR-SP01]` for requirements and design decisions

## MUST-NOT-FORGET

- **INCREMENTAL SAVE**: Write results after EACH image processed
- **STRUCTURED LOGGING**: `[ worker N ] [ x / total ] message` format to stderr
- **RETRY WITH BACKOFF**: 3x with exponential backoff (1s, 2s, 4s) for API errors
- **TEMP FILES**: `.tmp_YYYY-MM-DD_HH-MM-SS-xxx_` prefix, delete after success
- Use `model-parameter-mapping.json` for effort levels
- Use `model-registry.json` for provider detection and model config
- Use `model-pricing.json` for cost calculation (optional)
- Prompts from `prompts/transcription.md` and `prompts/judge.md`

## Table of Contents

1. [File Structure](#1-file-structure)
2. [Edge Cases](#2-edge-cases)
3. [Implementation Steps](#3-implementation-steps)
4. [Test Cases](#4-test-cases)
5. [Verification Checklist](#5-verification-checklist)
6. [Document History](#6-document-history)

## 1. File Structure

```
DevSystemV3.2/skills/llm-transcription/
├── transcribe-image-to-markdown-advanced.py  # Main pipeline script (~600 lines) [REWRITE]
├── model-registry.json           # Model properties [EXISTS]
├── model-parameter-mapping.json  # Effort levels [EXISTS]
├── model-pricing.json            # Cost per 1M tokens [EXISTS]
└── prompts/
    ├── transcription.md          # Transcription prompt [EXISTS]
    └── judge.md                  # Judge prompt [EXISTS]
```

## 2. Edge Cases

**Input Validation:**
- **LLMTR-IP01-EC-01**: No input file or folder specified -> Error with usage
- **LLMTR-IP01-EC-02**: Input file not found -> Error with path
- **LLMTR-IP01-EC-03**: Unsupported image format -> Error listing `.jpg, .jpeg, .png, .gif, .webp`
- **LLMTR-IP01-EC-04**: Empty input folder -> Error "No images found"
- **LLMTR-IP01-EC-05**: Prompt file not found -> Error with instructions

**API Failures:**
- **LLMTR-IP01-EC-06**: API rate limit -> Retry with backoff, eventually skip image
- **LLMTR-IP01-EC-07**: API timeout -> Retry 3x, then mark failed
- **LLMTR-IP01-EC-08**: Invalid API key -> Error immediately, don't retry
- **LLMTR-IP01-EC-09**: All ensemble attempts fail -> Mark image failed, continue batch

**Parsing:**
- **LLMTR-IP01-EC-10**: Judge returns non-JSON -> Assign default score 3.0, log warning
- **LLMTR-IP01-EC-11**: Judge JSON missing weighted_score -> Calculate from dimensions
- **LLMTR-IP01-EC-12**: JSON wrapped in markdown fences -> Strip fences, extract JSON

**Refinement:**
- **LLMTR-IP01-EC-13**: Refinement doesn't improve score -> Keep original, note in metadata
- **LLMTR-IP01-EC-14**: Refinement fails -> Keep original

## 3. Implementation Steps

### LLMTR-IP01-IS-01: Script Structure and Imports

**Location**: `transcribe-image-to-markdown-advanced.py` > top of file

**Action**: Add imports and constants

**Code**:
```python
#!/usr/bin/env python3
"""Ensemble transcription pipeline with judge and refinement."""
import os, sys, json, time, base64, argparse, asyncio
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

EFFORT_LEVELS = ['none', 'minimal', 'low', 'medium', 'high', 'xhigh']
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
```

### LLMTR-IP01-IS-02: Configuration Loading

**Location**: `transcribe-image-to-markdown-advanced.py` > after imports

**Action**: Add config loading functions

**Code**:
```python
def get_script_dir() -> Path: ...
def load_configs(script_dir: Path) -> tuple[dict, dict, dict | None]: ...  # registry, mapping, pricing
def get_model_config(model: str, registry: dict) -> dict: ...
def build_api_params(model, mapping, registry, temperature, reasoning_effort, output_length) -> dict: ...
```

**Note**: Copy patterns from `call-llm-batch.py`

### LLMTR-IP01-IS-02b: Cost Calculation

**Location**: `transcribe-image-to-markdown-advanced.py` > after config loading

**Action**: Add cost calculation function

**Code**:
```python
def calculate_cost(model: str, input_tokens: int, output_tokens: int, pricing: dict | None) -> float | None:
    if not pricing:
        return None
    provider = detect_provider(model)
    if provider not in pricing.get('pricing', {}):
        return None
    model_pricing = pricing['pricing'][provider].get(model)
    if not model_pricing:
        return None
    input_cost = (input_tokens / 1_000_000) * model_pricing['input_per_1m']
    output_cost = (output_tokens / 1_000_000) * model_pricing['output_per_1m']
    return input_cost + output_cost
```

### LLMTR-IP01-IS-03: API Key Loading

**Location**: `transcribe-image-to-markdown-advanced.py` > after config loading

**Action**: Add API key loading

**Code**:
```python
def load_api_keys(keys_file: Path) -> dict: ...
def detect_provider(model_id: str) -> str: ...
def get_client(provider: str, api_keys: dict): ...
```

### LLMTR-IP01-IS-04: Image Encoding

**Location**: `transcribe-image-to-markdown-advanced.py` > after API functions

**Action**: Add image encoding

**Code**:
```python
def encode_image_to_base64(image_path: Path) -> str: ...
def get_image_media_type(image_path: Path) -> str: ...
```

### LLMTR-IP01-IS-05: Structured Logging

**Location**: `transcribe-image-to-markdown-advanced.py` > after image functions

**Action**: Add logging function

**Code**:
```python
def log(worker_id: int, current: int, total: int, msg: str):
    print(f"[ worker {worker_id + 1} ] [ {current} / {total} ] {msg}", file=sys.stderr)
```

### LLMTR-IP01-IS-06: Temp File Management

**Location**: `transcribe-image-to-markdown-advanced.py` > after logging

**Action**: Add temp file functions

**Code**:
```python
def get_temp_dir(workspace: Path = None) -> Path: ...
def make_temp_prefix() -> str: ...
def save_temp_file(temp_dir: Path, prefix: str, suffix: str, content: str) -> Path: ...
def cleanup_temp_files(temp_dir: Path, prefix: str): ...
```

### LLMTR-IP01-IS-07: Retry with Backoff

**Location**: `transcribe-image-to-markdown-advanced.py` > after temp file functions

**Action**: Add retry decorator/function

**Code**:
```python
def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
```

### LLMTR-IP01-IS-08: API Call Functions

**Location**: `transcribe-image-to-markdown-advanced.py` > after retry

**Action**: Add OpenAI and Anthropic call functions

**Code**:
```python
def call_openai(client, model, prompt, api_params, image_data, image_media_type) -> dict: ...
def call_anthropic(client, model, prompt, api_params, method, image_data, image_media_type) -> dict: ...
```

**Note**: Return `{"text": ..., "usage": {...}, "model": ...}`

### LLMTR-IP01-IS-09: Async Transcription Generation

**Location**: `transcribe-image-to-markdown-advanced.py` > after API calls

**Action**: Add async transcription function

**Code**:
```python
async def generate_transcription_async(image_data, media_type, prompt, model, 
                                        client, provider, method, api_params) -> dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: call_api(...))
```

### LLMTR-IP01-IS-10: Async Judge Function

**Location**: `transcribe-image-to-markdown-advanced.py` > after transcription

**Action**: Add async judge function

**Code**:
```python
async def judge_transcription_async(image_data, media_type, transcription, 
                                     judge_prompt, judge_model, client, 
                                     provider, method, api_params) -> dict:
    # Build combined prompt: image + transcription + judge prompt
    # Call API
    # Parse JSON response
    # Calculate weighted_score if missing
```

### LLMTR-IP01-IS-11: Score Parsing

**Location**: `transcribe-image-to-markdown-advanced.py` > after judge

**Action**: Add JSON parsing with fence handling

**Code**:
```python
def parse_judge_response(content: str) -> dict:
    content = content.strip()
    if content.startswith('```'):
        content = content.split('\n', 1)[1]
        content = content.rsplit('```', 1)[0]
    start = content.find('{')
    end = content.rfind('}') + 1
    return json.loads(content[start:end])

def calculate_weighted_score(judge_result: dict) -> float:
    # weights: text=0.25, structure=0.35, graphics=0.40
```

### LLMTR-IP01-IS-12: Ensemble + Judge + Select

**Location**: `transcribe-image-to-markdown-advanced.py` > after score parsing

**Action**: Add main pipeline function

**Code**:
```python
async def process_image_ensemble(image_path, image_data, media_type,
                                  transcribe_prompt, judge_prompt,
                                  model, judge_model, initial_candidates,
                                  clients, api_params, temp_dir, temp_prefix):
    # Step 1: Generate N transcriptions concurrently
    transcriptions = await asyncio.gather(*[...])
    
    # Step 2: Judge all N concurrently
    judge_results = await asyncio.gather(*[...])
    
    # Step 3: Select best
    best_idx = max(range(len(judge_results)), key=lambda i: judge_results[i]['weighted_score'])
    return transcriptions[best_idx], judge_results[best_idx], all_scores
```

### LLMTR-IP01-IS-13: Conditional Refinement

**Location**: `transcribe-image-to-markdown-advanced.py` > after ensemble

**Action**: Add refinement function

**Code**:
```python
async def maybe_refine(best_transcription, best_judge, image_data, media_type,
                       transcribe_prompt, model, judge_model, judge_prompt,
                       min_score, client, provider, method, api_params):
    if best_judge['weighted_score'] >= min_score:
        return best_transcription, best_judge, False
    
    # Build refinement prompt with complete judge JSON
    refinement_prompt = f"""{transcribe_prompt}
---
Previous transcription (score: {best_judge['weighted_score']:.2f}/5.0):
{best_transcription['text']}
---
Judge feedback (improve based on this):
```json
{json.dumps(best_judge, indent=2)}
```
Please improve the transcription based on the judge feedback above.
"""
    
    # Generate refined transcription
    # Re-judge
    # Return better one
```

### LLMTR-IP01-IS-14: Single Image Processing

**Location**: `transcribe-image-to-markdown-advanced.py` > after refinement

**Action**: Add complete single image processor

**Code**:
```python
def process_single_image(worker_id, file_idx, total_files, image_path, args,
                         clients, api_params, transcribe_prompt, judge_prompt,
                         temp_dir, results_lock):
    log(worker_id, file_idx, total_files, f"Processing: {image_path.name}")
    start_time = time.time()
    temp_prefix = make_temp_prefix()
    
    # Encode image
    # Run ensemble + judge + select
    # Maybe refine
    # Save output
    # Cleanup temp files
    # Update metadata
```

### LLMTR-IP01-IS-15: Batch Processing with Workers

**Location**: `transcribe-image-to-markdown-advanced.py` > after single image

**Action**: Add batch processor with ThreadPoolExecutor

**Code**:
```python
def process_batch(args, clients, api_params, transcribe_prompt, judge_prompt):
    images = list(args.input_folder.glob('*'))
    images = [f for f in images if f.suffix.lower() in IMAGE_EXTENSIONS]
    
    temp_dir = get_temp_dir(args.temp_folder)
    results_lock = Lock()
    
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(process_single_image, i % args.workers, i + 1, 
                           len(images), img, args, ...): img
            for i, img in enumerate(images)
        }
        for future in as_completed(futures):
            ...
```

### LLMTR-IP01-IS-16: Output Writing

**Location**: `transcribe-image-to-markdown-advanced.py` > after batch

**Action**: Add output functions

**Code**:
```python
def write_output(output_path: Path, content: str, metadata: dict): ...
def write_batch_summary(output_folder: Path, results: list): ...
```

### LLMTR-IP01-IS-17: Argument Parser

**Location**: `transcribe-image-to-markdown-advanced.py` > after output

**Action**: Add argparse setup

**Code**:
```python
def parse_args():
    parser = argparse.ArgumentParser(description='Ensemble image transcription pipeline')
    parser.add_argument('--input-file', type=Path, help='Single input image')
    parser.add_argument('--output-file', type=Path, help='Output markdown file')
    parser.add_argument('--input-folder', type=Path, help='Batch input folder')
    parser.add_argument('--output-folder', type=Path, help='Batch output folder')
    parser.add_argument('--model', default='gpt-5-mini', help='Transcription model')
    parser.add_argument('--judge-model', default='gpt-5-mini', help='Judge model')
    parser.add_argument('--transcribe-prompt-file', type=Path)
    parser.add_argument('--judge-prompt-file', type=Path)
    parser.add_argument('--initial-candidates', type=int, default=3)
    parser.add_argument('--min-score', type=float, default=3.5)
    parser.add_argument('--max-refinements', type=int, default=1)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--keys-file', type=Path, default=Path('.env'))
    parser.add_argument('--temperature', default='medium', choices=EFFORT_LEVELS)
    parser.add_argument('--reasoning-effort', default='medium', choices=EFFORT_LEVELS)
    parser.add_argument('--output-length', default='medium', choices=EFFORT_LEVELS)
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--keep-temp', action='store_true')
    parser.add_argument('--temp-folder', type=Path)
    return parser.parse_args()
```

### LLMTR-IP01-IS-18: Main Entry Point

**Location**: `transcribe-image-to-markdown-advanced.py` > end of file

**Action**: Add main function

**Code**:
```python
def main():
    args = parse_args()
    script_dir = get_script_dir()
    
    # Validate inputs
    # Load configs
    # Load API keys
    # Load prompts
    # Initialize clients
    # Build API params
    
    if args.input_file:
        # Single file mode
        process_single_image(...)
    else:
        # Batch mode
        process_batch(...)

if __name__ == '__main__':
    main()
```

## 4. Test Cases

### Category 1: Input Validation (5 tests)

- **LLMTR-IP01-TC-01**: No input specified -> exit 1, "Must specify --input-file or --input-folder"
- **LLMTR-IP01-TC-02**: File not found -> exit 1, "File not found: [path]"
- **LLMTR-IP01-TC-03**: Unsupported format (.pdf) -> exit 1, "Unsupported format. Use: .jpg, .jpeg, .png, .gif, .webp"
- **LLMTR-IP01-TC-04**: Empty folder -> exit 1, "No images found in [path]"
- **LLMTR-IP01-TC-05**: Valid image -> exit 0, output file created

### Category 2: Ensemble Generation (3 tests)

- **LLMTR-IP01-TC-06**: Default candidates (3) -> 3 transcriptions generated
- **LLMTR-IP01-TC-07**: Custom candidates (5) -> 5 transcriptions generated
- **LLMTR-IP01-TC-08**: All attempts fail -> exit 0, image marked failed

### Category 3: Judging (3 tests)

- **LLMTR-IP01-TC-09**: Valid JSON response -> weighted_score calculated correctly
- **LLMTR-IP01-TC-10**: JSON in markdown fences -> fences stripped, score parsed
- **LLMTR-IP01-TC-11**: Non-JSON response -> default score 3.0 assigned

### Category 4: Refinement (3 tests)

- **LLMTR-IP01-TC-12**: Score >= min_score -> no refinement triggered
- **LLMTR-IP01-TC-13**: Score < min_score, refined better -> refined version used
- **LLMTR-IP01-TC-14**: Score < min_score, refined worse -> original kept

### Category 5: Batch Processing (3 tests)

- **LLMTR-IP01-TC-15**: 3 images, 2 workers -> all processed, order may vary
- **LLMTR-IP01-TC-16**: Existing output, no --force -> skipped
- **LLMTR-IP01-TC-17**: Existing output, --force -> reprocessed

## 5. Verification Checklist

### Prerequisites
- [ ] **LLMTR-IP01-VC-01**: SPEC LLMTR-SP01 read and understood
- [ ] **LLMTR-IP01-VC-02**: Prompts exist in prompts/ folder
- [ ] **LLMTR-IP01-VC-03**: Config files exist (model-registry.json, model-parameter-mapping.json)

### Implementation
- [ ] **LLMTR-IP01-VC-04**: IS-01 to IS-04 completed (imports, config, API keys, image encoding)
- [ ] **LLMTR-IP01-VC-05**: IS-05 to IS-08 completed (logging, temp files, retry, API calls)
- [ ] **LLMTR-IP01-VC-06**: IS-09 to IS-11 completed (async transcription, judge, score parsing)
- [ ] **LLMTR-IP01-VC-07**: IS-12 to IS-13 completed (ensemble, refinement)
- [ ] **LLMTR-IP01-VC-08**: IS-14 to IS-16 completed (single image, batch, output)
- [ ] **LLMTR-IP01-VC-09**: IS-17 to IS-18 completed (argparse, main)

### Validation
- [ ] **LLMTR-IP01-VC-10**: Single image test passes (TC-05)
- [ ] **LLMTR-IP01-VC-11**: Ensemble test passes (TC-06)
- [ ] **LLMTR-IP01-VC-12**: Judge parsing tests pass (TC-09 to TC-11)
- [ ] **LLMTR-IP01-VC-13**: Refinement tests pass (TC-12 to TC-14)
- [ ] **LLMTR-IP01-VC-14**: Batch test passes (TC-15)
- [ ] **LLMTR-IP01-VC-15**: Logging format matches spec ([ worker N ] [ x / total ])

## 6. Document History

**[2026-01-27 00:32]**
- Initial implementation plan created from LLMTR-SP01
