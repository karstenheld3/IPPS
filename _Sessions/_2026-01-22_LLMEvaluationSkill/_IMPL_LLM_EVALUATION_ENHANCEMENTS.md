# IMPL: LLM Evaluation Skill Enhancements

**Doc ID**: LLMEV-IP01
**Feature**: LLM_PARAM_CONTROL
**Goal**: Add three-param CLI control (--temperature, --reasoning-effort, --output-length) and compare-outputs.py
**Timeline**: Created 2026-01-24

**Target files**:
- `call-llm.py` (MODIFY)
- `call-llm-batch.py` (MODIFY)
- `compare-outputs.py` (NEW)

**Depends on:**
- `_SPEC_LLM_EVALUATION_SKILL_ENHANCEMENTS.md` [LLMEV-SP01] for requirements

## MUST-NOT-FORGET

- Temperature ranges differ: OpenAI 0-2, Anthropic 0-1
- Reasoning models (o1, o3, o4, gpt-5) do NOT support temperature - use reasoning_effort
- All new params are optional with default "medium"
- Seed default is null (disabled)
- Backward compatibility: existing CLI must work unchanged

## Table of Contents

1. [File Structure](#1-file-structure)
2. [Edge Cases](#2-edge-cases)
3. [Implementation Steps](#3-implementation-steps)
4. [Test Cases](#4-test-cases)
5. [Verification Checklist](#5-verification-checklist)
6. [Document History](#6-document-history)

## 1. File Structure

```
DevSystemV3.2/skills/llm-evaluation/
├── call-llm.py           # [MODIFY] Add params, load configs, build API params
├── call-llm-batch.py     # [MODIFY] Add params, save used_settings_{model}.json
├── compare-outputs.py    # [NEW] ~120 lines - Levenshtein comparison script
├── model-parameter-mapping.json  # [EXISTS] Effort-to-factor mapping
└── model-registry.json   # [EXISTS] Model properties
```

## 2. Edge Cases

- **LLMEV-IP01-EC-01**: Unknown model prefix -> Error with list of known prefixes
- **LLMEV-IP01-EC-02**: Seed on Anthropic -> Warning, ignore seed
- **LLMEV-IP01-EC-03**: Invalid effort level -> Error with valid options
- **LLMEV-IP01-EC-04**: Missing config files -> Error with path
- **LLMEV-IP01-EC-05**: Empty input folder for compare-outputs.py -> Error
- **LLMEV-IP01-EC-06**: Both --input-folder and --files -> Error (mutually exclusive)

## 3. Implementation Steps

### LLMEV-IP01-IS-01: Add shared config loading functions

**Location**: `call-llm.py` > after imports

**Action**: Add functions to load configs and build API params

**Code**:
```python
def load_configs(script_dir: Path) -> tuple[dict, dict]:
    """Load model-parameter-mapping.json and model-registry.json."""
    ...

def get_model_config(model: str, registry: dict) -> dict:
    """Return model config from registry using prefix matching."""
    ...

def build_api_params(model: str, mapping: dict, registry: dict,
                     temperature: str, reasoning_effort: str, 
                     output_length: str, seed: int = None) -> dict:
    """Build API parameters using effort levels."""
    ...
```

### LLMEV-IP01-IS-02: Add CLI arguments

**Location**: `call-llm.py` > `parse_args()`

**Action**: Add new arguments

**Code**:
```python
parser.add_argument('--temperature', choices=['none','minimal','low','medium','high','xhigh'], default='medium')
parser.add_argument('--reasoning-effort', choices=['none','minimal','low','medium','high','xhigh'], default='medium')
parser.add_argument('--output-length', choices=['none','minimal','low','medium','high','xhigh'], default='medium')
parser.add_argument('--seed', type=int, default=None)
parser.add_argument('--response-format', choices=['text','json'], default='text')
```

### LLMEV-IP01-IS-03: Update call_openai() signature

**Location**: `call-llm.py` > `call_openai()`

**Action**: Add api_params parameter, use it for API call

### LLMEV-IP01-IS-04: Update call_anthropic() signature

**Location**: `call-llm.py` > `call_anthropic()`

**Action**: Add api_params parameter, use it for API call

### LLMEV-IP01-IS-05: Update main() to use new params

**Location**: `call-llm.py` > `main()`

**Action**: Load configs, build params, pass to API calls

### LLMEV-IP01-IS-06: Mirror changes in call-llm-batch.py

**Location**: `call-llm-batch.py`

**Action**: Same changes as IS-01 through IS-05

### LLMEV-IP01-IS-07: Add used_settings save

**Location**: `call-llm-batch.py` > `main()` after client creation

**Action**: Save used_settings_{model}.json at batch start

**Code**:
```python
def save_used_settings(output_folder: Path, model: str, cli_params: dict, api_params: dict): ...
```

### LLMEV-IP01-IS-08: Create compare-outputs.py

**Location**: `compare-outputs.py` (NEW)

**Action**: Create script with Levenshtein distance comparison

**Code**:
```python
# CLI: --input-folder OR --files, --output-file, --group-by-input, --baseline
# Functions: levenshtein_distance(), normalized_distance(), similarity()
# Output: JSON report with summary and comparisons
```

## 4. Test Cases

### Category 1: Parameter Mapping (6 tests)

- **LLMEV-IP01-TC-01**: --temperature none on gpt-4o -> temperature=0.0 in API call
- **LLMEV-IP01-TC-02**: --reasoning-effort high on gpt-5-mini -> reasoning_effort="high" in API
- **LLMEV-IP01-TC-03**: --output-length medium on claude-sonnet-4 -> max_tokens=6144 (0.75 * 8192)
- **LLMEV-IP01-TC-04**: --reasoning-effort high on claude-sonnet-4 -> thinking.budget_tokens=32000
- **LLMEV-IP01-TC-05**: --seed 42 on gpt-4o -> seed=42 in API call
- **LLMEV-IP01-TC-06**: --seed 42 on claude-sonnet-4 -> warning, no seed in API call

### Category 2: Backward Compatibility (2 tests)

- **LLMEV-IP01-TC-07**: No new params -> defaults to medium, works like before
- **LLMEV-IP01-TC-08**: Existing --model --input-file --prompt-file -> still works

### Category 3: compare-outputs.py (4 tests)

- **LLMEV-IP01-TC-09**: Two identical files -> similarity=1.0, exact_match=true
- **LLMEV-IP01-TC-10**: Two different files -> 0 < similarity < 1.0
- **LLMEV-IP01-TC-11**: Empty folder -> error message
- **LLMEV-IP01-TC-12**: --group-by-input -> groups by source filename

## 5. Verification Checklist

### Prerequisites
- [x] **LLMEV-IP01-VC-01**: SPEC read and understood
- [x] **LLMEV-IP01-VC-02**: model-parameter-mapping.json exists
- [x] **LLMEV-IP01-VC-03**: model-registry.json exists

### Implementation
- [x] **LLMEV-IP01-VC-04**: IS-01 config loading added
- [x] **LLMEV-IP01-VC-05**: IS-02 CLI arguments added
- [x] **LLMEV-IP01-VC-06**: IS-03/04 API call functions updated
- [x] **LLMEV-IP01-VC-07**: IS-05 main() updated
- [x] **LLMEV-IP01-VC-08**: IS-06 batch script updated
- [x] **LLMEV-IP01-VC-09**: IS-07 used_settings save added
- [x] **LLMEV-IP01-VC-10**: IS-08 compare-outputs.py created

### Validation
- [x] **LLMEV-IP01-VC-11**: Unit tests pass (24/24 param mapping tests)
- [x] **LLMEV-IP01-VC-12**: OpenAI integration tests pass (gpt-4o with temp, seed)
- [x] **LLMEV-IP01-VC-13**: compare-outputs.py works (96.43% similarity for 1-char diff)
- [x] **LLMEV-IP01-VC-14**: Synced to .windsurf/skills/llm-evaluation/
- [ ] **LLMEV-IP01-VC-15**: Anthropic tests (blocked: missing ANTHROPIC_API_KEY)

## 6. Document History

**[2026-01-24 20:30]**
- Implementation complete
- Unit tests: 24/24 pass (param mapping, seed handling, output length)
- Integration tests: OpenAI pass, Anthropic blocked (no API key)
- compare-outputs.py verified

**[2026-01-24 20:05]**
- Initial implementation plan created
