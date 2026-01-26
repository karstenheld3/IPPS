# SPEC: LLM Image Transcription Pipeline

**Doc ID**: LLMTR-SP01
**Goal**: High-quality image-to-markdown transcription via ensemble generation, LLM judging, and refinement
**Timeline**: Created 2026-01-27
**Target folder**: `DevSystemV3.2/skills/llm-transcription/`

**Depends on:**
- `SPEC_LLM_EVALUATION_SKILL.md [LLMEV-SP01]` for CLI patterns, model registry, parameter mapping
- `_INFO_TRANSCRIPTION_EVALUATION.md [EVAL-IN01]` for model selection (best value, consistency, judge effectiveness)

## MUST-NOT-FORGET

- **INCREMENTAL SAVE**: Write results after EACH image processed
- **CONCURRENCY**: Support `--workers N` for parallel image processing (default: 4)
- **RETRY WITH BACKOFF**: 3x with exponential backoff (1s, 2s, 4s) for API errors
- **TEMP FILES**: Store in `[WORKSPACE]/.tools/_image_to_markdown/`, prefix `.tmp_YYYY-MM-DD_HH-MM-SS-xxx_`, delete after success
- Use original API model IDs exactly (e.g., `gpt-4o`, `claude-sonnet-4-20250514`)
- Reuse `model-registry.json`, `model-parameter-mapping.json`, `model-pricing.json` from @llm-evaluation
- JSON output for machine-readable results
- Prompts stored in `prompts/` folder (transcription.md, judge.md)

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Design Decisions](#5-design-decisions)
6. [Implementation Guarantees](#6-implementation-guarantees)
7. [Key Mechanisms](#7-key-mechanisms)
8. [Pipeline Flow](#8-pipeline-flow)
9. [Scripts Reference](#9-scripts-reference)
10. [Data Structures](#10-data-structures)
11. [Edge Cases](#11-edge-cases)
12. [Document History](#12-document-history)

## 1. Scenario

**Problem:** Single-shot image transcription has variable quality. Some attempts miss graphics, misread text, or produce poor structure. No way to know if output is good without manual review.

**Solution:**
- Generate N transcriptions concurrently (ensemble)
- Judge all N concurrently with scoring prompt
- Select highest-scoring transcription
- If score below threshold, refine best attempt and re-judge
- Output includes final score for quality assurance

**What we don't want:**
- Sequential processing when concurrent is possible
- Hardcoded prompts (must be external files)
- Loss of intermediate results on failure
- Incompatible CLI patterns with @llm-evaluation

## 2. Context

### Pipeline Overview

```
[IMAGE] .jpg, .png, .gif, .webp
    |
    v
[TRANSCRIBE] x N concurrent (ensemble)
    |
    v
[JUDGE] x N concurrent (score each)
    |
    v
[SELECT] highest score
    |
    v (if score < threshold)
[REFINE] feed back with issues
    |
    v
[RE-JUDGE] final score
    |
    v
[OUTPUT] .md + metadata
```

### Compatible Patterns from @llm-evaluation

**Reuse directly:**
- `model-registry.json` - Model properties (provider, method, max_output)
- `model-parameter-mapping.json` - Effort levels (none/minimal/low/medium/high/xhigh)
- `model-pricing.json` - Cost per 1M tokens (optional, for cost tracking)
- API key loading from `.env` file
- Provider auto-detection from model ID prefix
- Retry with exponential backoff pattern
- Atomic file writes (temp file -> rename)
- Structured logging pattern (always on, no --verbose flag)

**Adapt:**
- `--temperature`, `--reasoning-effort`, `--output-length` effort parameters
- `--workers` for outer-loop parallelism (multiple images)
- `--use-prompt-caching` for large prompts

## 3. Domain Objects

### TranscriptionPrompt

Prompt for converting image to markdown.

**Storage:** `prompts/transcription.md`
**Source:** `llm-image-to-markdown-transcription-v1b.md`

**Key sections:**
- Graphics handling (essential vs decorative, ASCII art with labels)
- Structure (semantic hierarchy, multi-column layouts)
- Text accuracy (precision, special characters, tolerances)

### JudgePrompt

Prompt for scoring transcription quality.

**Storage:** `prompts/judge.md`
**Source:** `llm-image-to-markdown-judge-v1d.md`

**Scoring dimensions:**
- `text_accuracy` (1-5) - Character-level correctness
- `page_structure` (1-5) - Semantic hierarchy match
- `graphics_quality` (1-5) - Essential graphics captured

**Weights:** text=0.25, structure=0.35, graphics=0.40

### PipelineResult

Output metadata for each processed image.

**Key properties:**
- `input_file` - Source image path
- `output_file` - Output markdown path
- `final_score` - Weighted score (0-5)
- `candidates` - Number of transcriptions generated
- `refinement_applied` - Whether refinement was used
- `scores` - Array of individual candidate scores
- `total_input_tokens`, `total_output_tokens` - Token tracking
- `total_cost_usd` - Total cost in USD (if model-pricing.json available)
- `elapsed_seconds` - Processing time

## 4. Functional Requirements

**LLMTR-FR-01: Ensemble Generation**
- Generate N transcriptions concurrently for each image
- Default N=3, configurable via `--initial-candidates`
- All use same transcription prompt
- Use asyncio for concurrent API calls

**LLMTR-FR-02: Concurrent Judging**
- Judge all N transcriptions concurrently
- Each judge call receives: image + transcription + judge prompt
- Parse JSON response for scores
- Calculate weighted score per judge prompt weights

**LLMTR-FR-03: Best Selection**
- Select transcription with highest weighted score
- Record all scores in metadata for analysis

**LLMTR-FR-04: Conditional Refinement**
- If best score < `--min-score` (default: 3.5), trigger refinement
- Send to LLM: best transcription + complete judge JSON output + task to improve
- Re-judge refined transcription
- Take refined if score improves, otherwise keep original

**LLMTR-FR-05: Batch Processing**
- Process multiple images with `--input-folder`
- Parallelize at image level with `--workers` (default: 4)
- Incremental save after each image completes
- Skip existing outputs unless `--force`

**LLMTR-FR-06: CLI Compatibility**
- Match @llm-evaluation parameter names exactly
- `--input-file` / `--input-folder` (not --input / --input-dir)
- `--output-file` / `--output-folder` (not --output / --output-dir)
- `--model`, `--judge-model` for models
- `--temperature`, `--reasoning-effort`, `--output-length` effort levels
- `--keys-file` for API keys (default: .env)
- `--workers`, `--force` standard flags

**LLMTR-FR-07: Prompt Files**
- `--transcribe-prompt-file` for custom transcription prompt
- `--judge-prompt-file` for custom judge prompt
- Default: `prompts/transcription.md`, `prompts/judge.md`

**LLMTR-FR-08: Temp File Management**
- Temp folder: `[WORKSPACE]/.tools/_image_to_markdown/`
- Auto-create folder if not exists
- Temp file prefix: `.tmp_YYYY-MM-DD_HH-MM-SS-xxx_` (xxx = milliseconds)
- Store intermediate results (transcriptions, judge responses) as temp files
- Delete all temp files for an image after successful transcription
- On failure: leave temp files for debugging (user can manually clean)
- `--keep-temp` flag to preserve temp files even on success

## 5. Design Decisions

**LLMTR-DD-01:** Ensemble size default is 3. Rationale: Balance between quality and cost. 3 candidates usually sufficient to find good output.

**LLMTR-DD-02:** Both transcription and judge use gpt-5-mini by default. Rationale: Good quality (8.0 fields), cost-effective ($0.017/image), and consistent evaluation scores (3.67/5 matches premium models).

**LLMTR-DD-03:** Min score threshold is 3.5 (out of 5). Rationale: Below 70% indicates significant issues worth attempting to fix.

**LLMTR-DD-04:** Max 1 refinement iteration. Rationale: Diminishing returns, prevents cost explosion.

**LLMTR-DD-05:** Refinement sends complete judge JSON (not extracted issues). Rationale: Simpler implementation, full context for LLM to understand what to fix.

**LLMTR-DD-06:** Reuse @llm-evaluation configs. Rationale: Consistency, avoid duplicate maintenance.

**LLMTR-DD-07:** Inner concurrency (ensemble) uses asyncio. Outer concurrency (images) uses ThreadPoolExecutor. Rationale: asyncio efficient for I/O-bound API calls within single image, threads for image-level parallelism.

**LLMTR-DD-08:** Always log progress to stderr, no --verbose flag. Rationale: Consistent monitoring, matches @llm-evaluation pattern.

## 6. Implementation Guarantees

**LLMTR-IG-01:** Scripts MUST NOT modify input images.

**LLMTR-IG-02:** Scripts MUST save result after EACH image completes (incremental).

**LLMTR-IG-03:** Scripts MUST handle API errors: retry 3x with backoff, then mark image as failed.

**LLMTR-IG-04:** Scripts MUST parse JSON from judge response, handling markdown fences.

**LLMTR-IG-05:** Scripts MUST work without config files (use defaults, auto-detect provider).

**LLMTR-IG-06:** Refinement MUST NOT exceed `--max-refinements` iterations.

**LLMTR-IG-07:** Final output MUST include score for quality filtering.

## 7. Key Mechanisms

### Ensemble + Judge + Select

```python
async def process_image(image_path, transcribe_prompt, judge_prompt, 
                        model, judge_model, ensemble_size):
    image_data, media_type = encode_image(image_path)
    
    # Step 1: Generate N transcriptions concurrently
    transcriptions = await asyncio.gather(*[
        generate_transcription(image_data, media_type, transcribe_prompt, model)
        for _ in range(ensemble_size)
    ])
    
    # Step 2: Judge all N concurrently
    judge_results = await asyncio.gather(*[
        judge_transcription(image_data, media_type, t.content, judge_prompt, judge_model)
        for t in transcriptions
    ])
    
    # Step 3: Select best
    best_idx = max(range(len(judge_results)), key=lambda i: judge_results[i].weighted_score)
    return transcriptions[best_idx], judge_results[best_idx]
```

### Conditional Refinement

```python
async def maybe_refine(best_transcription, best_judge, image_data, media_type,
                       transcribe_prompt, model, judge_model, judge_prompt, min_score):
    if best_judge.weighted_score >= min_score:
        return best_transcription, best_judge, False  # No refinement needed
    
    # Build refinement prompt with complete judge output
    refinement_prompt = f"""{transcribe_prompt}

---

Previous transcription (score: {best_judge.weighted_score:.2f}/5.0):

{best_transcription.content}

---

Judge feedback (improve based on this):

```json
{json.dumps(best_judge.raw_json, indent=2)}
```

Please improve the transcription based on the judge feedback above.
"""
    
    refined = await generate_transcription(image_data, media_type, refinement_prompt, model)
    
    # Re-judge
    refined_judge = await judge_transcription(
        image_data, media_type, refined.content, judge_prompt, judge_model
    )
    
    # Take refined only if better
    if refined_judge.weighted_score > best_judge.weighted_score:
        return refined, refined_judge, True
    return best_transcription, best_judge, False
```

### Temp File Management

```python
import os
from datetime import datetime
from pathlib import Path

def get_temp_dir(workspace: Path = None) -> Path:
    """Get or create temp directory."""
    if workspace is None:
        workspace = Path.cwd()
    temp_dir = workspace / '.tools' / '_image_to_markdown'
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir

def make_temp_prefix() -> str:
    """Generate temp file prefix with timestamp."""
    now = datetime.now()
    return f".tmp_{now.strftime('%Y-%m-%d_%H-%M-%S')}-{now.microsecond // 1000:03d}_"

def save_temp_file(temp_dir: Path, prefix: str, suffix: str, content: str) -> Path:
    """Save content to temp file."""
    temp_path = temp_dir / f"{prefix}{suffix}"
    temp_path.write_text(content, encoding='utf-8')
    return temp_path

def cleanup_temp_files(temp_dir: Path, prefix: str):
    """Delete all temp files with given prefix."""
    for f in temp_dir.glob(f"{prefix}*"):
        f.unlink()
```

### Structured Logging

```python
def log(worker_id: int, current: int, total: int, msg: str):
    """Log with worker ID and progress."""
    print(f"[ worker {worker_id + 1} ] [ {current} / {total} ] {msg}", file=sys.stderr)
```

**Example output:**
```
[ worker 1 ] [ 1 / 10 ] Processing: doc1.png
[ worker 1 ] [ 1 / 10 ] Transcribing (3 candidates)...
[ worker 1 ] [ 1 / 10 ] Judging candidates...
[ worker 1 ] [ 1 / 10 ] Best score: 4.20 (candidate 2)
[ worker 1 ] [ 1 / 10 ] Done: doc1.md (4.20, 15420+8230 tokens, 12.3s)
[ worker 2 ] [ 2 / 10 ] Processing: doc2.png
```

### Score Parsing

```python
def parse_judge_response(content: str) -> dict:
    # Strip markdown fences if present
    content = content.strip()
    if content.startswith('```'):
        content = content.split('\n', 1)[1]
        content = content.rsplit('```', 1)[0]
    
    # Find JSON object
    start = content.find('{')
    end = content.rfind('}') + 1
    if start >= 0 and end > start:
        return json.loads(content[start:end])
    raise ValueError("No JSON found in judge response")
```

## 8. Pipeline Flow

```
User runs: python transcribe-image-to-markdown-advanced.py --input-file doc.png --output-file doc.md

├─> Load API keys from .env or --keys-file
├─> Load prompts from prompts/ or --transcribe-prompt-file / --judge-prompt-file
├─> Encode image to base64
│
├─> [1/3] Generate 3 transcriptions concurrently
│   ├─> call_vision_api(model, image, transcribe_prompt) x3
│   └─> Wait for all to complete
│
├─> [2/3] Judge all 3 concurrently
│   ├─> call_vision_api(judge_model, image + transcription, judge_prompt) x3
│   └─> Parse JSON scores, calculate weighted_score
│       Scores: [3.85, 4.20, 3.95] -> selected #2 (4.20)
│
├─> [3/3] Check if refinement needed
│   ├─> If 4.20 >= 3.5: Skip refinement
│   └─> If 4.20 < 3.5: 
│       ├─> Refine with feedback
│       ├─> Re-judge
│       └─> Take if improved
│
└─> Write doc.md + metadata
    └─> Output: score: 4.20, tokens: 15420+8230, 12.3s
```

## 9. Scripts Reference

### transcribe-image-to-markdown-advanced.py

```powershell
python transcribe-image-to-markdown-advanced.py --input-file doc.png --output-file doc.md
python transcribe-image-to-markdown-advanced.py --input-folder images/ --output-folder out/ --workers 4
python transcribe-image-to-markdown-advanced.py --input-file doc.png --model claude-sonnet-4-20250514 --initial-candidates 5 --min-score 4.0
```

**Parameters:**
- `--input-file` - Single input image file
- `--output-file` - Output markdown file (default: stdout)
- `--input-folder` - Folder with input images (batch mode)
- `--output-folder` - Folder for output files (batch mode)
- `--model` - Transcription model (default: gpt-5-mini)
- `--judge-model` - Judge model (default: gpt-5-mini)
- `--transcribe-prompt-file` - Transcription prompt file (default: prompts/transcription.md)
- `--judge-prompt-file` - Judge prompt file (default: prompts/judge.md)
- `--initial-candidates` - Candidates to generate (default: 3)
- `--min-score` - Threshold for refinement (default: 3.5)
- `--max-refinements` - Max refinement iterations (default: 1)
- `--workers` - Parallel workers (default: 4)
- `--keys-file` - API keys file (default: .env)
- `--temperature` - Temperature effort level (default: medium, via model-parameter-mapping.json)
- `--reasoning-effort` - Reasoning effort level (default: medium, via model-parameter-mapping.json)
- `--output-length` - Output length effort level (default: medium, via model-parameter-mapping.json)
- `--force` - Force reprocess existing files
- `--keep-temp` - Preserve temp files after success
- `--temp-folder` - Custom temp folder (default: .tools/_image_to_markdown/)

### transcribe-image-to-markdown.py (Simple)

Single-shot transcription without ensemble/judge (for quick tests).

```powershell
python transcribe-image-to-markdown.py --input doc.png --output doc.md
```

## 10. Data Structures

### Pipeline Result JSON

```json
{
  "input": "images/doc1.png",
  "output": "out/doc1.md",
  "model": "gpt-5-mini",
  "judge_model": "gpt-5-mini",
  "final_score": 4.20,
  "candidates": 3,
  "candidate_scores": [3.85, 4.20, 3.95],
  "selected_candidate": 2,
  "refinement_applied": false,
  "total_input_tokens": 15420,
  "total_output_tokens": 8230,
  "total_cost_usd": 0.0203,
  "elapsed_seconds": 12.3,
  "timestamp": "2026-01-27T00:15:00+01:00"
}
```

### Judge Response JSON

```json
{
  "text_accuracy": {
    "score": 4,
    "justification": "Two typos found, format variations tolerated",
    "errors_found": ["'$2,540M' should be '$2,450M'"]
  },
  "page_structure": {
    "score": 5,
    "justification": "All 12 outline nodes correctly captured",
    "missing_nodes": [],
    "misleveled_nodes": []
  },
  "graphics_quality": {
    "score": 4,
    "justification": "24 of 25 essential graphics detected",
    "essential_graphics_in_image": 25,
    "essential_graphics_detected": 24,
    "missed_essential_graphics": ["company logo top-right"]
  },
  "weighted_score": 4.20
}
```

### Batch Summary JSON

```json
{
  "total_images": 10,
  "successful": 9,
  "failed": 1,
  "average_score": 4.15,
  "refinements_applied": 2,
  "total_input_tokens": 154200,
  "total_output_tokens": 82300,
  "total_cost_usd": 0.203,
  "total_elapsed_seconds": 145.7
}
```

## 11. Edge Cases

**LLMTR-EC-01:** Judge returns non-JSON -> Assign default score 3.0, log warning

**LLMTR-EC-02:** All ensemble attempts fail -> Mark image as failed, continue batch

**LLMTR-EC-03:** Refinement doesn't improve score -> Keep original, note in metadata

**LLMTR-EC-04:** Image file not found -> Error with clear message

**LLMTR-EC-05:** Unsupported image format -> Error listing supported formats

**LLMTR-EC-06:** No prompts found -> Error with instructions to create prompts/ folder

**LLMTR-EC-07:** API rate limit -> Retry with backoff, eventually skip

**LLMTR-EC-08:** Empty input directory -> Error with clear message

## 12. Document History

**[2026-01-27 00:38]**
- Added: `model-pricing.json` for cost tracking
- Added: `total_cost_usd` to PipelineResult and data structures

**[2026-01-27 00:30]**
- Fixed: Removed stale `--verbose` from FR-06 and Pipeline Flow
- Fixed: `--input-dir` to `--input-folder` in FR-05
- Fixed: `~/.llm-keys` to `.env` in Pipeline Flow
- Fixed: Data structure examples to use `gpt-5-mini` defaults
- Changed: `--ensemble-size` to `--initial-candidates`

**[2026-01-27 00:29]**
- Changed: Refinement now sends complete judge JSON output (not extracted issues)
- Changed: LLMTR-DD-05 and LLMTR-FR-04 updated for simpler refinement workflow

**[2026-01-27 00:26]**
- Removed: `--verbose` flag (always log to stderr, matches @llm-evaluation)
- Added: LLMTR-DD-08 for logging design decision
- Added: Structured Logging key mechanism with format and examples

**[2026-01-27 00:24]**
- Changed: Harmonized params with @llm-evaluation conventions
- Changed: `--input`/`--output` to `--input-file`/`--output-file`
- Changed: `--input-dir`/`--output-dir` to `--input-folder`/`--output-folder`
- Changed: Single `--effort` back to `--temperature`, `--reasoning-effort`, `--output-length`
- Changed: `--keys-file` default to .env (matching llm-evaluation)

**[2026-01-27 00:23]**
- Changed: Renamed `--transcribe-prompt` to `--transcribe-prompt-file`, `--judge-prompt` to `--judge-prompt-file`

**[2026-01-27 00:21]**
- Changed: Single `--effort` param instead of 3 separate params (maps via model-parameter-mapping.json)

**[2026-01-27 00:20]**
- Changed: Default to gpt-5-mini for both transcription and judge (user preference)

**[2026-01-27 00:19]**
- Changed: Default models per EVAL-IN01 research (gpt-4.1 transcription, gpt-5-mini judge)
- Added: Dependency on EVAL-IN01 for model selection rationale

**[2026-01-27 00:15]**
- Added: LLMTR-FR-08 Temp File Management
- Added: `--keep-temp`, `--temp-dir` parameters
- Added: Temp file key mechanism (get_temp_dir, make_temp_prefix, cleanup_temp_files)

**[2026-01-27 00:12]**
- Initial specification created
- Extracted compatible patterns from LLMEV-SP01
- Defined ensemble+judge+refinement pipeline
