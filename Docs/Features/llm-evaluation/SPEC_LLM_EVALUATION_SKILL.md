# SPEC: LLM Evaluation Skill

**Doc ID**: LLMEV-SP01
**Goal**: Generic skill for LLM evaluation pipelines - works with images, text documents, or any content
**Timeline**: Created 2026-01-22, Updated 2026-01-26

**Target folder**: `.windsurf/skills/llm-evaluation/`

## MUST-NOT-FORGET

- **INCREMENTAL SAVE**: ALL scripts MUST write results after EACH item processed, not just at end
- **CONCURRENCY**: ALL scripts processing multiple items MUST support `--workers N` for parallel execution (default: 4)
- **RETRY WITH BACKOFF**: Use simple retry pattern (3x with exponential backoff) for transient API errors
- Model IDs MUST match original API model IDs exactly (e.g., `gpt-4o`, `claude-opus-4-20250514`)
- Keys file supports both `.env` and `key=value` formats
- All input/output paths MUST be parameters with sensible defaults
- JSON output for all scripts (machine-readable)
- No hardcoded paths - use `--keys-file`, `--input-file`, `--input-folder`, `--output-file`, `--output-folder` parameters
- Temperature=0 reduces but does NOT guarantee determinism (MoE routing, floating-point precision)
- Seed parameter is provider-specific (OpenAI has it, Anthropic does not)
- Reasoning models (o1, o3, o4, gpt-5) do NOT support temperature/top_p - use reasoning_effort instead
- Anthropic temperature range is 0.0-1.0 (not 0-2 like OpenAI legacy)
- Backward compatibility: existing CLI must continue to work

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Design Decisions](#5-design-decisions)
6. [Implementation Guarantees](#6-implementation-guarantees)
7. [Key Mechanisms](#7-key-mechanisms)
8. [Scripts Reference](#8-scripts-reference)
9. [Configuration Files](#9-configuration-files)
10. [Data Structures](#10-data-structures)
11. [Edge Cases](#11-edge-cases)
12. [Document History](#12-document-history)

## Skill Summary

**File Type Detection:**
- Auto-detect by suffix only (no override to prevent mismatches)
- Image: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- Text: `.txt`, `.md`, `.json`, `.py`, `.html`, `.xml`, `.csv`
- Unknown suffix: script exits with error, user must rename file

**Scripts:**

- `call-llm.py` - Single LLM call (auto-detects image or text input)
- `call-llm-batch.py` - Batch LLM calls with parallel processing
- `generate-questions.py` - Generate evaluation questions from source files
- `generate-answers.py` - Generate answers from processed text files
- `evaluate-answers.py` - Score answers with LLM-as-judge
- `analyze-costs.py` - Token cost analysis from usage logs
- `compare-transcription-runs.py` - Compare outputs with Levenshtein/LLM-judge
- `find-workers-limit.py` - Discover optimal worker count for rate limits

**Configuration:**
- `model-registry.json` - Model properties (provider, method, max_output, temp_max, thinking_max)
- `model-pricing.json` - Token costs per model for cost analysis
- `model-parameter-mapping.json` - Effort level to API parameter mapping

**Prompts:**
- `prompts/transcribe-page.md` - Default for image transcription
- `prompts/summarize-text.md` - Default for text summarization
- `prompts/answer-from-text.md` - Default for `generate-answers.py`
- `prompts/judge-answer.md` - Default for `evaluate-answers.py`
- `prompts/compare-image-transcription.md` - Default for hybrid comparison

## 1. Scenario

**Problem:** Evaluating LLM output quality requires multiple steps: processing, question generation, answer generation, and scoring. Scripts need fine-grained control over model parameters and output variability.

**Solution:**
- Create input-agnostic scripts that work with images or text files
- Auto-detect file type by suffix (no override parameter)
- Use original API model IDs (no custom naming)
- Add three CLI parameters using same keywords (none/minimal/low/medium/high/xhigh):
  - `--temperature` for legacy models
  - `--reasoning-effort` for reasoning models
  - `--output-length` for output token control
- Add `--seed` for reproducibility (OpenAI only)
- Add `--use-prompt-caching` for cost reduction with large prompts
- Add `--response-format` for structured output mode
- Save all parameters in output metadata for reproducibility

**Use cases:**
- Evaluate image transcription quality
- Evaluate text summarization quality
- Evaluate document understanding depth
- Compare outputs across multiple runs
- Any LLM task where you can generate questions and verify answers

**What we don't want:**
- Hardcoded paths to session folders
- Scripts locked to specific input types
- Custom model naming schemes that differ from API model IDs
- Loss of data on script failure (must save incrementally)
- Provider-specific flags (keep it generic, handle internally)

## 2. Context

### Pipeline Overview

```
[INPUT] images, text, PDFs, any file
    |
    v
[PROCESS] call-llm-batch.py
    |     (transcribe, summarize, analyze)
    v
[GENERATE] generate-questions.py
    |       (create Q&A pairs from source)
    v
[ANSWER] generate-answers.py
    |     (answer from processed text)
    v
[EVALUATE] evaluate-answers.py
          (score with LLM-as-judge)
```

### Design Principles

- **Stateless scripts**: Each script reads input, produces output, no shared state
- **Composable**: Run any subset of the pipeline, skip stages as needed
- **Input-agnostic**: Same scripts work with images, text, PDFs, code
- **Provider-agnostic**: Works with OpenAI, Anthropic, or any compatible API
- **Crash-resilient**: Incremental saves after each item, resume from partial results

### Key Insight on Determinism

Even with temperature=0 and seed, outputs are NOT fully deterministic due to:
- Mixture-of-Experts (MoE) routing decisions
- Floating-point precision across hardware
- Batch composition effects
- API infrastructure variability

Therefore: Goal is to REDUCE variability, not eliminate it.

## 3. Domain Objects

### ModelRegistry

Defines available LLM models with their API identifiers, providers, and parameter constraints.

**Storage:** `model-registry.json` in skill folder

**Key properties:**
- `model_id` - Original API model ID (e.g., `gpt-4o`, `claude-opus-4-20250514`)
- `provider` - API provider (`openai`, `anthropic`)
- `method` - Parameter method (`temperature`, `reasoning_effort`, `thinking`, `effort`)
- `max_output` - Maximum output tokens
- `temp_max` - Maximum temperature (for temperature method)
- `thinking_max` - Maximum thinking budget (for thinking method)
- `seed` - Whether seed parameter is supported

### ModelPricing

Defines token costs per model for cost analysis.

**Storage:** `model-pricing.json` in skill folder

**Key properties:**
- `input_per_1m` - USD cost per 1 million input tokens
- `output_per_1m` - USD cost per 1 million output tokens
- `cache_read_per_1m` - USD cost per 1M cached read tokens (Anthropic)
- `cache_write_per_1m` - USD cost per 1M cached write tokens (Anthropic)

### ModelParameterMapping

Maps effort levels to API parameters.

**Storage:** `model-parameter-mapping.json` in skill folder

**Effort levels:** `none`, `minimal`, `low`, `medium`, `high`, `xhigh`

**Mapping factors:**
- `temperature_factor` - Multiplied by model's `temp_max`
- `openai_reasoning_effort` - Direct value for OpenAI reasoning models
- `anthropic_thinking_factor` - Multiplied by model's `thinking_max`
- `output_length_factor` - Multiplied by model's `max_output`

## 4. Functional Requirements

**LLMEV-FR-01: API Key Loading**
- Support `.env` format: `KEY_NAME=value`
- Ignore lines starting with `#` (comments)
- Default location: `.env` in current working directory
- Override with `--keys-file PATH` parameter

**LLMEV-FR-02: Model ID Handling**
- Use original API model IDs exactly as provided by OpenAI/Anthropic
- Validate model ID against `model-registry.json` using prefix matching
- Auto-detect provider from model ID prefix

**LLMEV-FR-03: Three Separate Control Parameters**

```
--temperature {none, minimal, low, medium, high, xhigh}
--reasoning-effort {none, minimal, low, medium, high, xhigh}
--output-length {none, minimal, low, medium, high, xhigh}
```

**Default**: `medium` for all three parameters

**LLMEV-FR-04: Seed Parameter**
- Add `--seed` (int, optional, OpenAI only)
- Warn if used with Anthropic (not supported)
- Default: null (disabled unless specified)

**LLMEV-FR-05: Structured Output Mode**
- Add `--response-format` with values: `text` (default), `json`
- For OpenAI: use `response_format={"type": "json_object"}`
- For Anthropic: add JSON instruction to prompt

**LLMEV-FR-06: Prompt Caching**
- Add `--use-prompt-caching` flag
- OpenAI: Automatic caching for prompts >1024 tokens (50% discount)
- Anthropic: Explicit `cache_control` on system blocks (90% read discount, 25% write premium)
- Track cache metrics in metadata: `cached_tokens` (OpenAI), `cache_write_tokens`/`cache_read_tokens` (Anthropic)
- Batch cache warm-up: First file processes synchronously to populate cache before parallel workers

**LLMEV-FR-07: Parameter Recording**
- Save all API parameters in `used_settings_{model}.json`
- Include: effort levels, seed, actual API params sent
- Include: `system_fingerprint` from OpenAI responses

**LLMEV-FR-08: Output Comparison**
- Script `compare-transcription-runs.py` for text similarity
- Methods: `levenshtein` (default), `semantic`, `hybrid`
- Hybrid: Levenshtein for text, LLM-judge for `<transcription_image>` sections
- Output: JSON report with per-file and aggregate metrics

**LLMEV-FR-09: Backward Compatibility**
- All new parameters are optional
- Existing CLI invocations work unchanged
- Default behavior matches original behavior

## 5. Design Decisions

**LLMEV-DD-01:** Use original API model IDs. Rationale: Avoids confusion, enables direct copy-paste from API docs.

**LLMEV-DD-02:** Keys file uses same format as `.env`. Rationale: Industry standard, works with existing tooling.

**LLMEV-DD-03:** Incremental saving after EVERY item. Rationale: Prevents total data loss on crash, allows progress monitoring.

**LLMEV-DD-04:** JSON output for all scripts. Rationale: Machine-readable, enables pipeline composition.

**LLMEV-DD-05:** Token usage stored in `_token_usage_{model}.json`, batch metadata in `_batch_metadata_{model}.json`. Rationale: Keeps output files clean, updated incrementally.

**LLMEV-DD-06:** Provider auto-detection from model ID prefix. Rationale: `claude-*` = anthropic, `gpt-*` = openai, `o1-*` = openai.

**LLMEV-DD-07:** Parallel processing as default (4 workers). Rationale: API calls are I/O bound, parallelism improves throughput.

**LLMEV-DD-08:** Use `ThreadPoolExecutor` with `threading.Lock` for thread-safe incremental saving.

**LLMEV-DD-09:** Atomic file writes via temp file pattern (`.tmp` -> rename). Rationale: Prevents corrupt files on crash.

**LLMEV-DD-10:** Structured logging with worker ID: `[ worker_id ] [ x / n ] action...`

**LLMEV-DD-11:** Use None/null for unset parameters, let provider use defaults.

**LLMEV-DD-12:** Warn but don't error on unsupported provider parameters (e.g., seed on Anthropic).

**LLMEV-DD-13:** Levenshtein distance for text comparison (simple, no tokenization needed).

**LLMEV-DD-14:** Store parameters in `used_settings_{model}.json`, not per-file metadata.

## 6. Implementation Guarantees

**LLMEV-IG-01:** Scripts MUST NOT modify input files.

**LLMEV-IG-02:** Scripts MUST save state after EACH completed item.

**LLMEV-IG-03:** Scripts MUST handle API errors: retry 3x with exponential backoff (1s, 2s, 4s), then skip item. Strip markdown fences before JSON parse.

**LLMEV-IG-04:** Scripts MUST validate model ID against registry (if available).

**LLMEV-IG-05:** Scripts MUST respect `--output` path and not write elsewhere.

**LLMEV-IG-06:** Scripts MUST work without model-registry.json (use provider auto-detection).

**LLMEV-IG-07:** Setting `--temperature none` passes temperature=0.0 to API, not "use default".

**LLMEV-IG-08:** Seed parameter only sent to OpenAI. Anthropic calls ignore it with warning.

**LLMEV-IG-09:** `used_settings_{model}.json` created at batch start, not per file.

**LLMEV-IG-10:** Prompt caching warm-up: First Anthropic request completes before parallel workers start (batch only).

## 7. Key Mechanisms

### API Key Loading

```python
def load_api_keys(keys_file: Path) -> dict:
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
    if model_id.startswith('claude-'):
        return 'anthropic'
    elif model_id.startswith(('gpt-', 'o1-', 'o3-', 'o4-')):
        return 'openai'
    else:
        raise ValueError(f"Cannot detect provider for model: {model_id}")
```

### Parameter Building

```python
def build_api_params(model: str, mapping: dict, registry: dict,
                     temperature: str, reasoning_effort: str,
                     output_length: str, seed: int = None) -> dict:
    model_config = get_model_config(model, registry)
    effort_map = mapping["effort_mapping"]
    params = {}
    
    method = model_config.get("method", "temperature")
    
    if method == "temperature":
        factor = effort_map[temperature]["temperature_factor"]
        params["temperature"] = factor * model_config.get("temp_max", 2.0)
    elif method == "reasoning_effort":
        params["reasoning_effort"] = effort_map[reasoning_effort]["openai_reasoning_effort"]
    elif method == "thinking":
        factor = effort_map[reasoning_effort]["anthropic_thinking_factor"]
        budget = int(factor * model_config.get("thinking_max", 100000))
        if budget > 0:
            params["thinking"] = {"type": "enabled", "budget_tokens": budget}
    
    output_factor = effort_map[output_length]["output_length_factor"]
    params["max_tokens"] = int(output_factor * model_config.get("max_output", 16384))
    
    if seed and model_config.get("seed", False):
        params["seed"] = seed
    
    return params
```

### Prompt Caching (Anthropic)

```python
def call_anthropic(client, model, prompt, api_params, use_prompt_caching=False):
    if use_prompt_caching:
        system_content = [{
            "type": "text",
            "text": prompt,
            "cache_control": {"type": "ephemeral"}
        }]
        call_params = {
            'model': model,
            'max_tokens': api_params.get('max_tokens', 4096),
            'system': system_content,
            'messages': [{"role": "user", "content": [{"type": "text", "text": "Process the content above."}]}]
        }
    else:
        # Standard call without caching
        ...
    
    response = client.messages.create(**call_params)
    
    usage = {"input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens}
    if hasattr(response.usage, 'cache_creation_input_tokens'):
        usage["cache_write_tokens"] = response.usage.cache_creation_input_tokens
    if hasattr(response.usage, 'cache_read_input_tokens'):
        usage["cache_read_tokens"] = response.usage.cache_read_input_tokens
    
    return {"text": ..., "usage": usage, "model": response.model}
```

### Batch Cache Warm-up

```python
# For Anthropic caching: process first file synchronously to warm up cache
if use_caching and provider == 'anthropic' and len(input_files) > 1:
    print("[INFO] Cache warm-up: processing first file before parallel workers...")
    process_file(0, 1, total_files, input_files[0], ...)
    remaining_files = input_files[1:]

# Then process remaining files in parallel
with ThreadPoolExecutor(max_workers=workers) as executor:
    ...
```

## 8. Scripts Reference

### call-llm.py - Single LLM Call

```powershell
python call-llm.py --model gpt-4o --input-file photo.jpg --prompt-file prompts/transcribe-page.md
python call-llm.py --model claude-sonnet-4-20250514 --prompt-file prompts/summarize.md --use-prompt-caching
```

**Parameters:**
- `--model` - API model ID (required)
- `--input-file` - Input file: image or text
- `--prompt-file` - Prompt file (.md)
- `--output-file` - Output file (default: stdout)
- `--keys-file` - API keys file (default: .env)
- `--write-json-metadata` - Write token usage to separate JSON file
- `--temperature` - Temperature effort level (default: medium)
- `--reasoning-effort` - Reasoning effort level (default: medium)
- `--output-length` - Output length effort level (default: medium)
- `--seed` - Random seed (OpenAI only)
- `--response-format` - Output format: text, json (default: text)
- `--use-prompt-caching` - Enable prompt caching

### call-llm-batch.py - Batch Processing

```powershell
python call-llm-batch.py --model gpt-4o --input-folder images/ --output-folder out/ --prompt-file prompts/transcribe.md --runs 3 --workers 4
python call-llm-batch.py --model claude-sonnet-4-20250514 --input-folder docs/ --output-folder out/ --prompt-file prompts/analyze.md --use-prompt-caching
```

**Parameters:**
- `--model` - API model ID (required)
- `--input-folder` - Folder with input files
- `--output-folder` - Folder for output files
- `--prompt-file` - Prompt file (.md)
- `--runs` - Runs per file (default: 1)
- `--workers` - Parallel workers (default: 4)
- `--keys-file` - API keys file (default: .env)
- `--force` - Force reprocess existing files
- `--clear-folder` - Clear output folder before processing
- `--temperature` - Temperature effort level (default: medium)
- `--reasoning-effort` - Reasoning effort level (default: medium)
- `--output-length` - Output length effort level (default: medium)
- `--seed` - Random seed (OpenAI only)
- `--response-format` - Output format: text, json (default: text)
- `--use-prompt-caching` - Enable prompt caching (with auto warm-up for Anthropic)

**Features:**
- Parallel processing with configurable workers
- Resume capability (skips existing outputs)
- Incremental save after each item
- Token usage tracking per model
- Cache warm-up: first file processed before parallel workers (Anthropic only)

### compare-transcription-runs.py - Output Comparison

```powershell
python compare-transcription-runs.py --input-folder runs/ --output-file report.json
python compare-transcription-runs.py --input-folder runs/ --output-file report.json --method hybrid --judge-model gpt-5-mini
```

**Parameters:**
- `--input-folder` - Folder with output files
- `--files` - Explicit list of files (alternative to --input-folder)
- `--output-file` - JSON report output (required)
- `--method` - Comparison method: levenshtein (default), semantic, hybrid
- `--judge-model` - Model for semantic/hybrid comparison
- `--judge-prompt` - Custom judge prompt file
- `--keys-file` - API keys file (default: .env)
- `--baseline` - File to use as baseline
- `--grouped` - Group files by source name

**Hybrid Comparison:**
1. Parse sections by `<transcription_image>` tags
2. Text sections: Compare with Levenshtein distance
3. Image sections: Compare with LLM-as-a-judge
4. Output separate and combined scores

### Other Scripts

- `generate-questions.py` - Generate evaluation questions from source files
- `generate-answers.py` - Generate answers from processed text files
- `evaluate-answers.py` - Score answers with LLM-as-judge
- `analyze-costs.py` - Token cost analysis from usage logs
- `find-workers-limit.py` - Discover optimal worker count for rate limits

## 9. Configuration Files

### model-registry.json

```json
{
  "model_id_startswith": [
    {"prefix": "gpt-4o", "provider": "openai", "method": "temperature", "max_output": 16384, "temp_max": 2.0, "seed": true},
    {"prefix": "gpt-5", "provider": "openai", "method": "reasoning_effort", "max_output": 32768, "seed": false},
    {"prefix": "claude-sonnet-4", "provider": "anthropic", "method": "thinking", "max_output": 8192, "thinking_max": 100000},
    {"prefix": "claude-3.5", "provider": "anthropic", "method": "temperature", "max_output": 8192, "temp_max": 1.0}
  ]
}
```

### model-parameter-mapping.json

```json
{
  "effort_mapping": {
    "none": {"temperature_factor": 0.0, "openai_reasoning_effort": "low", "anthropic_thinking_factor": 0.0, "output_length_factor": 0.125},
    "minimal": {"temperature_factor": 0.05, "openai_reasoning_effort": "low", "anthropic_thinking_factor": 0.05, "output_length_factor": 0.25},
    "low": {"temperature_factor": 0.175, "openai_reasoning_effort": "low", "anthropic_thinking_factor": 0.1, "output_length_factor": 0.375},
    "medium": {"temperature_factor": 0.35, "openai_reasoning_effort": "medium", "anthropic_thinking_factor": 0.1, "output_length_factor": 0.375},
    "high": {"temperature_factor": 0.7, "openai_reasoning_effort": "high", "anthropic_thinking_factor": 0.5, "output_length_factor": 0.5},
    "xhigh": {"temperature_factor": 1.0, "openai_reasoning_effort": "high", "anthropic_thinking_factor": 1.0, "output_length_factor": 1.0}
  }
}
```

### model-pricing.json

```json
{
  "gpt-4o": {"input_per_1m": 2.50, "cached_input_per_1m": 1.25, "output_per_1m": 10.00},
  "claude-sonnet-4-20250514": {"input_per_1m": 3.00, "cache_write_per_1m": 3.75, "cache_read_per_1m": 0.30, "output_per_1m": 15.00}
}
```

## 10. Data Structures

### used_settings_{model}.json

```json
{
  "model": "gpt-5-mini",
  "cli_parameters": {
    "temperature": "medium",
    "reasoning_effort": "high",
    "output_length": "medium",
    "use_prompt_caching": true
  },
  "api_parameters": {
    "reasoning_effort": "high",
    "max_tokens": 24576
  },
  "prompt_file": "prompts/transcribe-page.md",
  "batch_started": "2026-01-24T19:00:00Z"
}
```

### Token Usage with Cache Metrics

```json
{
  "model": "claude-sonnet-4-20250514",
  "total_input_tokens": 54500,
  "total_output_tokens": 26225,
  "total_cache_write_tokens": 2048,
  "total_cache_read_tokens": 52452,
  "calls": 25
}
```

### Batch Metadata Entry

```json
{
  "output_file": "image1_processed_claude-sonnet-4_run01.md",
  "source_file": "images/image1.jpg",
  "model": "claude-sonnet-4-20250514",
  "run": 1,
  "usage": {
    "input_tokens": 2180,
    "output_tokens": 1049,
    "cache_write_tokens": 0,
    "cache_read_tokens": 2048
  },
  "timestamp": "2026-01-26T21:30:15+00:00"
}
```

## 11. Edge Cases

**LLMEV-EC-01:** Effort level not supported by model -> Use fallback from mapping, print info message

**LLMEV-EC-02:** Both `--input-folder` and `--files` provided -> Error, mutually exclusive

**LLMEV-EC-03:** Seed provided for non-OpenAI model -> Warning printed, parameter ignored

**LLMEV-EC-04:** Empty input folder -> Error with clear message

**LLMEV-EC-05:** Non-text files in comparison folder -> Skip with warning

**LLMEV-EC-06:** Unknown model (not in registry) -> Error listing known patterns

**LLMEV-EC-07:** `--method hybrid` without `--judge-model` -> Error with clear message

**LLMEV-EC-08:** No `<transcription_image>` tags with hybrid method -> Fall back to levenshtein with warning

**LLMEV-EC-09:** Prompt caching with prompt <1024 tokens -> Cache metrics will be 0 (below minimum)

**LLMEV-EC-10:** Anthropic thinking budget > max_tokens -> Auto-adjust max_tokens with warning

## 12. Document History

**[2026-01-26 23:45]**
- Merged: LLMEV-SP02 (Enhancements) into main SPEC
- Added: `--use-prompt-caching` flag with cache warm-up logic
- Added: Cache metrics tracking (cached_tokens, cache_write_tokens, cache_read_tokens)
- Added: Batch cache warm-up mechanism for Anthropic
- Added: Edge cases EC-09, EC-10 for caching

**[2026-01-24 19:50]**
- Added: Three separate CLI params (`--temperature`, `--reasoning-effort`, `--output-length`)
- Added: `model-parameter-mapping.json` for effort-to-factor mapping
- Added: `model-registry.json` with `model_id_startswith` pattern matching
- Added: `compare-transcription-runs.py` script with hybrid comparison
- Added: `used_settings_{model}.json` for parameter recording

**[2026-01-23 10:36]**
- Changed: Default schema categories to generic types
- Added: `--clear-folder` to generate-answers.py and evaluate-answers.py

**[2026-01-22 21:23]**
- Changed: LLMEV-IG-03 added image encoding/embedding retry (3x)

**[2026-01-22 21:21]**
- Added: Atomic file writes (temp file pattern)
- Added: Structured logging with worker ID
- Added: Prerequisites section

**[2026-01-22 20:19]**
- Added: Concurrency (`--workers N`) as standard feature
- Added: Thread-safe incremental saving pattern

**[2026-01-22 20:16]**
- Initial specification created
