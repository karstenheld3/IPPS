# SPEC: LLM Evaluation Skill Enhancements

**Doc ID**: LLMEV-SP01
**Goal**: Add model control parameters and quality metrics to llm-evaluation skill scripts
**Timeline**: Created 2026-01-24
**Target files**: `call-llm.py`, `call-llm-batch.py`, new `compare-outputs.py`, new `model-parameter-mapping.json`, new `model-registry.json`

**Depends on:**
- `_INFO_TRANSCRIPTION_VARIABILITY.md [LLMEV-IN01]` for identified gaps

## MUST-NOT-FORGET

- Temperature=0 reduces but does NOT guarantee determinism (MoE routing, floating-point precision)
- Seed parameter is provider-specific (OpenAI has it, Anthropic does not)
- Reasoning models (o1, o3, o4, gpt-5) do NOT support temperature/top_p - use reasoning_effort instead
- Anthropic temperature range is 0.0-1.0 (not 0-2 like OpenAI legacy)
- Backward compatibility: existing CLI must continue to work
- No breaking changes to output format

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Current State Analysis](#3-current-state-analysis)
4. [Functional Requirements](#4-functional-requirements)
5. [Design Decisions](#5-design-decisions)
6. [Implementation Guarantees](#6-implementation-guarantees)
7. [Key Mechanisms](#7-key-mechanisms)
8. [CLI Changes](#8-cli-changes)
9. [New Script: compare-outputs.py](#9-new-script-compare-outputspy)
10. [Edge Cases](#10-edge-cases)
11. [Implementation Verification Checklist](#11-implementation-verification-checklist)
12. [Document History](#12-document-history)

## 1. Scenario

**Problem:** Current scripts use default API parameters, giving no control over output variability. We discovered:
- No way to set temperature or seed
- No way to control reasoning effort for modern models
- No way to compare outputs across runs (only file size)
- No structured output mode for consistent formatting
- Hardcoded max_tokens=4096

**Solution:**
- Add three CLI parameters using same keywords (none/minimal/low/medium/high/xhigh):
  - `--temperature` for legacy models
  - `--reasoning-effort` for reasoning models
  - `--output-length` for output token control
- Add `--seed` for reproducibility (OpenAI only)
- Create `compare-outputs.py` for text similarity metrics
- Add `--response-format` for structured output mode
- Save all parameters in output metadata for reproducibility

**What we don't want:**
- Breaking existing CLI usage
- Provider-specific flags (keep it generic, handle internally)
- Complex configuration files (CLI-first)

## 2. Context

The llm-evaluation skill provides batch LLM calling for evaluation pipelines. Variability testing revealed we need finer control over model outputs and better metrics for comparing results.

Key insight from research: Even with temperature=0 and seed, outputs are NOT fully deterministic due to:
- Mixture-of-Experts (MoE) routing decisions
- Floating-point precision across hardware
- Batch composition effects
- API infrastructure variability

Therefore: Goal is to REDUCE variability, not eliminate it.

## 3. Current State Analysis

### What `call-llm.py` and `call-llm-batch.py` currently support

**Supported:**
- `--model` - Model ID
- `--input-file` / `--input-folder` - Input files
- `--prompt-file` - Prompt template
- `--output-file` / `--output-folder` - Output location
- `--runs` - Multiple runs per input (batch only)
- `--workers` - Parallel processing (batch only)
- `--keys-file` - API key location
- `--force` - Reprocess existing (batch only)

**NOT Supported (Gap):**
- `--temperature` - Not exposed (legacy models only)
- `--seed` - Not exposed
- `--reasoning-effort` - Not exposed (reasoning models)
- `--max-tokens` - Hardcoded to 4096
- `--response-format` - Not supported
- Output comparison - Not available

### Current API Call Flow

```
call_openai() / call_anthropic()
├─> Hardcoded: max_tokens=4096
├─> Missing: temperature, seed (legacy models)
├─> Missing: reasoning_effort (reasoning models)
└─> Missing: response_format
```

## 4. Functional Requirements

**LLMEV-FR-01: Three Separate Control Parameters**

Three CLI parameters, each using the same keywords:

```
--temperature {none, minimal, low, medium, high, xhigh}
--reasoning-effort {none, minimal, low, medium, high, xhigh}
--output-length {none, minimal, low, medium, high, xhigh}
```

**Mapping Table** (from `model-parameter-mapping.json`):

- **temperature_factor**: Multiplied by model's `temp_max` from registry
- **openai_reasoning_effort**: Direct value for OpenAI reasoning models
- **anthropic_thinking_factor**: Multiplied by model's `thinking_max` from registry
- **output_length_factor**: Multiplied by model's `max_output` from registry

**Default**: `medium` for all three parameters

**LLMEV-FR-01a: Seed Parameter**
- Add `--seed` (int, optional, OpenAI only - warn if used with Anthropic)
- Default: null (disabled unless specified)

**LLMEV-FR-01b: Model Registry**
- Use `model-registry.json` for model properties (max_output, temp_max, thinking_max)
- Pattern matching via `model_id_startswith` determines model config

**LLMEV-FR-02: Structured Output Mode**
- Add `--response-format` with values: `text` (default), `json`
- For OpenAI: use `response_format={"type": "json_object"}` when `json`
- For Anthropic: add JSON instruction to prompt (no native support)

**LLMEV-FR-03: Parameter Recording**
- Save all API parameters in `used_settings_{model}.json`
- Include: effort level, seed, actual API params sent (temperature or reasoning_effort)
- Include: model version (if available from response)
- Include: `system_fingerprint` from OpenAI responses (for tracking backend changes)

**LLMEV-FR-06: Configuration Files**
- `model-parameter-mapping.json` - Effort-to-parameter mapping (factors)
- `model-registry.json` - Model properties and boundaries
- Pattern matching via `model_id_startswith` for model detection

**LLMEV-FR-04: Output Comparison Script**
- New script `compare-outputs.py`
- Compare multiple output files for same input
- Metrics: exact match, Levenshtein distance, line-by-line diff count
- Output: JSON report with per-file and aggregate metrics

**LLMEV-FR-05: Backward Compatibility**
- All new parameters are optional
- Existing CLI invocations work unchanged
- Default behavior matches current behavior

## 5. Design Decisions

**LLMEV-DD-01:** Use None/null for unset parameters, let provider use defaults. Rationale: Explicit about what we control vs provider defaults. `[ASSUMED]`

**LLMEV-DD-02:** Warn but don't error on unsupported provider parameters (e.g., seed on Anthropic). Rationale: Allow same CLI for multi-provider testing. `[ASSUMED]`

**LLMEV-DD-03:** Levenshtein distance for text comparison, not BLEU/ROUGE. Rationale: Simpler, no tokenization needed, sufficient for variability measurement. `[VERIFIED]`

**LLMEV-DD-04:** Store parameters in separate `used_settings_{model}.json`, not per-file metadata. Rationale: Reduces duplication, single source of truth per batch run. `[ASSUMED]`

## 6. Implementation Guarantees

**LLMEV-IG-01:** Setting `--temperature none` passes temperature=0.0 to API, not "use default".

**LLMEV-IG-02:** Seed parameter only sent to OpenAI. Anthropic calls ignore it with warning.

**LLMEV-IG-03:** `used_settings_{model}.json` created/updated at batch start, not per file.

**LLMEV-IG-04:** compare-outputs.py works on any text files, not just LLM outputs.

## 7. Key Mechanisms

### Parameter Passthrough Pattern

```python
import json

def load_config():
    with open("model-parameter-mapping.json") as f:
        mapping = json.load(f)
    with open("model-registry.json") as f:
        registry = json.load(f)
    return mapping, registry

def get_model_config(model: str, registry: dict) -> dict:
    """Return model config from registry using prefix matching."""
    for entry in registry["model_id_startswith"]:
        if model.startswith(entry["prefix"]):
            return entry
    raise ValueError(f"Unknown model: {model}")

def build_api_params(
    model: str,
    temperature: str = "medium",
    reasoning_effort: str = "medium",
    output_length: str = "medium",
    seed: int = None
) -> dict:
    """Build API parameters using three separate effort-level params."""
    mapping, registry = load_config()
    model_config = get_model_config(model, registry)
    effort_map = mapping["effort_mapping"]
    params = {}
    
    method = model_config.get("method", "temperature")
    
    if method == "temperature":
        factor = effort_map[temperature]["temperature_factor"]
        params["temperature"] = factor * model_config.get("temp_max", 2.0)
    elif method == "reasoning_effort":
        params["reasoning_effort"] = effort_map[reasoning_effort]["openai_reasoning_effort"]
    elif method == "effort":  # Anthropic effort (claude-opus-4.5)
        params["effort"] = effort_map[reasoning_effort]["openai_reasoning_effort"]  # uses same values
    elif method == "thinking":
        factor = effort_map[reasoning_effort]["anthropic_thinking_factor"]
        params["thinking"] = {"budget_tokens": int(factor * model_config.get("thinking_max", 100000))}
    
    # Output length
    output_factor = effort_map[output_length]["output_length_factor"]
    max_output = model_config.get("max_output", 16384)
    params["max_tokens"] = int(output_factor * max_output)
    
    # Seed (OpenAI only)
    if seed and model_config.get("seed", False):
        params["seed"] = seed
    elif seed:
        print(f"[WARN] --seed ignored for {model} (not supported)", file=sys.stderr)
    
    return params
```

### Levenshtein Distance (Inline - No Dependencies)

Pure Python implementation using Wagner-Fischer algorithm with O(min(m,n)) space:

```python
def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate minimum edits to transform s1 into s2."""
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    if not s2:
        return len(s1)
    
    prev_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            cost = 0 if c1 == c2 else 1
            curr_row.append(min(
                curr_row[j] + 1,      # insert
                prev_row[j + 1] + 1,  # delete
                prev_row[j] + cost    # substitute
            ))
        prev_row = curr_row
    return prev_row[-1]

def normalized_distance(a: str, b: str) -> float:
    """Return 0.0 (identical) to 1.0 (completely different)."""
    if not a and not b:
        return 0.0
    max_len = max(len(a), len(b))
    return levenshtein_distance(a, b) / max_len

def similarity(a: str, b: str) -> float:
    """Return 1.0 (identical) to 0.0 (completely different)."""
    return 1.0 - normalized_distance(a, b)
```

## 8. CLI Changes

### call-llm.py

```bash
# Deterministic output (legacy model)
python call-llm.py --model gpt-4o --input-file image.jpg --prompt-file prompt.md \
    --temperature none --output-length medium --seed 42

# Reasoning model with high effort
python call-llm.py --model gpt-5-mini --input-file image.jpg --prompt-file prompt.md \
    --reasoning-effort high --output-length high

# Anthropic with extended thinking
python call-llm.py --model claude-sonnet-4 --input-file image.jpg --prompt-file prompt.md \
    --reasoning-effort high --output-length medium

# Defaults to medium for all if not specified
python call-llm.py --model gpt-4o --input-file image.jpg --prompt-file prompt.md
```

**New parameters:**
- `--temperature {none,minimal,low,medium,high,xhigh}` - Temperature control for legacy models (default: medium)
- `--reasoning-effort {none,minimal,low,medium,high,xhigh}` - Reasoning control for modern models (default: medium)
- `--output-length {none,minimal,low,medium,high,xhigh}` - Output length control (default: medium)
- `--seed INT` - Random seed for reproducibility (OpenAI only, beta)
- `--response-format {text,json}` - Output format (default: text)

### call-llm-batch.py

Same new parameters, plus recorded in `used_settings_{model}.json`:

```json
{
  "model": "gpt-5-mini",
  "cli_parameters": {
    "temperature": "medium",
    "reasoning_effort": "high",
    "output_length": "medium"
  },
  "api_parameters": {
    "reasoning_effort": "high",
    "max_completion_tokens": 24576
  },
  "openai_metadata": {
    "system_fingerprint": "fp_abc123"
  },
  "batch_started": "2026-01-24T19:00:00Z",
  "prompt_file": "prompts/transcribe-page.md"
}
```

## 9. New Script: compare-outputs.py

### Usage

```powershell
python compare-outputs.py --input-folder outputs/ --output-file comparison.json
python compare-outputs.py --files output1.md output2.md output3.md --output-file comparison.json
```

### Parameters

- `--input-folder` - Folder with output files to compare
- `--files` - Explicit list of files to compare
- `--output-file` - JSON report output
- `--group-by-input` - Group by source input file (extract from filename)
- `--baseline` - File to use as baseline for comparison

### Output Schema

```json
{
  "summary": {
    "total_files": 10,
    "exact_matches": 0,
    "avg_similarity": 0.87,
    "max_distance": 0.23
  },
  "comparisons": [
    {
      "group": "image1.jpg",
      "files": ["image1_run01.md", "image1_run02.md", "image1_run03.md"],
      "exact_match": false,
      "pairwise": [
        {"a": "run01", "b": "run02", "distance": 0.08, "diff_lines": 3},
        {"a": "run01", "b": "run03", "distance": 0.12, "diff_lines": 5}
      ],
      "avg_similarity": 0.90
    }
  ]
}
```

### Metrics

- **exact_match** - Boolean: all files identical
- **distance** - Normalized Levenshtein (0.0 = identical, 1.0 = completely different)
- **similarity** - 1.0 - distance
- **diff_lines** - Count of lines that differ (simplified diff)

## 10. Edge Cases

**LLMEV-EC-01:** Effort level not supported by model -> Use fallback from mapping, print info message

**LLMEV-EC-02:** Both `--input-folder` and `--files` provided to compare-outputs.py -> Error, mutually exclusive

**LLMEV-EC-03:** Seed provided for non-OpenAI or reasoning model -> Warning printed, parameter ignored

**LLMEV-EC-04:** Empty output folder for compare-outputs.py -> Error with clear message

**LLMEV-EC-05:** Non-text files in comparison folder -> Skip with warning

**LLMEV-EC-06:** Unknown model (not in mapping) -> Error with clear message listing known patterns

## 11. Implementation Verification Checklist

- [ ] `model-parameter-mapping.json` created in skill folder
- [ ] `model-registry.json` created in skill folder
- [ ] `call-llm.py` accepts `--temperature`, `--reasoning-effort`, `--output-length`, `--seed`, `--response-format`
- [ ] `call-llm-batch.py` accepts same parameters
- [ ] Model detection from registry works (model_id_startswith)
- [ ] Parameters map to correct API values using factors from mapping
- [ ] `system_fingerprint` captured in OpenAI metadata
- [ ] `used_settings_{model}.json` created with all parameters
- [ ] `compare-outputs.py` created and functional
- [ ] Levenshtein distance calculation correct
- [ ] Existing CLI usage unchanged (backward compatibility)
- [ ] Edge cases handled

## 12. Document History

**[2026-01-24 19:50]**
- Changed: Three separate CLI params (`--temperature`, `--reasoning-effort`, `--output-length`) using same keywords
- Added: `model-parameter-mapping.json` for effort-to-factor mapping
- Added: `model-registry.json` for model properties (max_output, temp_max, thinking_max)
- Changed: All values are factors (0.0-1.0) applied to model limits from registry
- Updated: Code example to reflect new two-file design

**[2026-01-24 19:45]**
- Removed: `--top-p` parameter (deprecated for reasoning models)
- Added: `--reasoning-effort` parameter for reasoning models (none/minimal/low/medium/high)
- Changed: Temperature range now provider-specific (OpenAI 0-2, Anthropic 0-1)
- Added: Note about max_tokens translation to internal param by model type
- Added: `system_fingerprint` capture in OpenAI metadata
- Added: Edge cases EC-06, EC-07 for reasoning model parameter handling
- Updated: MUST-NOT-FORGET with reasoning model constraints

**[2026-01-24 19:15]**
- Added: Verification labels to design decisions
- Added: Edge cases (LLMEV-EC-01 through EC-05)
- Added: Implementation verification checklist

**[2026-01-24 19:10]**
- Initial specification created
- Based on gaps identified in LLMEV-IN01 and _REVIEW findings
