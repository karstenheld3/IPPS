# SPEC: MinifyIPPS V2 Architecture Changes

**Doc ID**: MIPPS-SP02
**Feature**: MIPPS-V2-ARCHITECTURE
**Goal**: Specify run-based isolation, unified Large Language Model (LLM) client, and standardized model configs for MinifyIPPS V2
**Timeline**: Created 2026-03-20

**Depends on:**
- `_SPEC_IPPS_MINIFICATION_MOTHER_MODEL.md [MIPPS-SP01]` for base pipeline behavior

**Does not depend on:**
- V1 implementation details (this spec supersedes architecture choices)

## MUST-NOT-FORGET

- Each minification run creates isolated subfolder under `runs/`
- Replace `llm_clients.py` (AnthropicClient + OpenAIClient) with unified `LLMClient` from `lib/llm_client.py`
- Model configs loaded from JSON files in `configs/`, not hardcoded
- Cost tracking via `calculate_cost()` with pricing from `model-pricing.json`
- Per-file cost tracking with cache hit/miss status in `run_costs.json`
- Run summary (`run_summary.md`) generated per run
- New modules: `run_manager.py` (run folder creation), `cost_tracker.py` (replaces api_cost_tracker.py)
- All non-.md files copied to output (except `__pycache__`) per MIPPS-SP01 FR-09

## Table of Contents

1. [Scenario](#1-scenario)
2. [Changes from V1](#2-changes-from-v1)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Design Decisions](#5-design-decisions)
6. [Implementation Guarantees](#6-implementation-guarantees)
7. [Key Mechanisms](#7-key-mechanisms)
8. [Data Structures](#8-data-structures)
9. [Module Structure](#9-module-structure)
10. [Document History](#10-document-history)

## 1. Scenario

**Problem:** V1 MinifyIPPS has architectural limitations:
- Run artifacts overwrite each other (no history, no comparison)
- Cost data lost on state reset (manually rebuilt `pipeline_state.json` shows $0.00)
- Hardcoded model configs scattered across code
- No tooling to compare runs or generate reports

**Solution:**
- Run-based subfolder isolation preserves all artifacts per run
- Unified LLM client with JSON-based model configs
- Automatic cost tracking from standardized pricing files
- Run comparison and report generation tools

**What we don't want:**
- Config file drift (copied JSONs becoming stale vs source)
- Over-engineering (HTML report generator is optional tooling, not core)
- Breaking existing compression logic (Step 1-7 behavior unchanged)

## 2. Changes from V1

### Unchanged (from MIPPS-SP01)

- Pipeline steps 1-7 logic (bundle, analyze, generate, compress, verify, iterate)
- Mother model compression with cached context
- Verification model scoring with 3.5 threshold
- Exclusion criteria (< 100 lines AND <= 2 references)
- `never_compress` pattern matching
- Non-.md file copying (except `__pycache__`)
- Prompt structure (`prompts/step/`, `prompts/transform/`, `prompts/eval/`)

### Changed

- **File layout**: Flat files at session root -> `runs/<run-id>/` subfolder per run
- **LLM clients**: `llm_clients.py` (AnthropicClient + OpenAIClient) -> `llm_client.py` (unified LLMClient)
- **Pricing**: Hardcoded PRICING dict -> `configs/model-pricing.json`
- **Model params**: Hardcoded in code -> `configs/model-registry.json` + `configs/model-parameter-mapping.json`
- **State location**: `pipeline_state.json` at session root -> `runs/<run-id>/pipeline_state.json`
- **Cost tracking**: Manual calculation -> `calculate_cost()` auto-tracking
- **Cache tracking**: None -> Per-call cache hit/miss in `run_costs.json`
- **Run comparison**: None -> `compare_runs.py` tool

### Added

- **MinificationRun**: Isolated run folder with all artifacts
- **RunConfig**: Snapshot of config at run start (`run_config.json`)
- **RunSummary**: Markdown summary of run results (`run_summary.md`)
- **RunCosts**: Detailed per-file cost breakdown (`run_costs.json`)
- **compare_runs.py**: Compare 2+ runs (compression ratio, cost, files)
- **generate_report.py**: Optional HTML report generator

## 3. Domain Objects

### MinificationRun

A **MinificationRun** is an isolated execution of the compression pipeline.

- **Location**: `runs/<run-id>/`
- **Run ID format**: `<YYYYMMDD>-<HHMM>-<label>` (e.g., `20260320-1430-full`)
- **Contents**:
  - `run_config.json` - config snapshot at run start
  - `pipeline_state.json` - final state with metrics
  - `run_summary.md` - human-readable summary
  - `run_costs.json` - detailed cost breakdown
  - `analysis/` - Steps 2-4 outputs (`_01_FILE_CALL_TREE.md`, `_02_FILE_COMPLEXITY_MAP.md`, `_03_FILE_COMPRESSION_STRATEGY.md`)
  - `context/` - Step 1 output (`all_files_bundle.md`)
  - `prompts/` - Step 5 outputs (`step/`, `transform/`, `eval/`)
  - `verification/` - Step 7 outputs (`_04_FILE_COMPRESSION_REPORT.md`, `_05_MANUAL_REVIEW_QUEUE.md`)
  - `output/` - compressed .md files and copied non-.md files

### RunConfig

A **RunConfig** captures the configuration used for a specific run.

- **Storage**: `runs/<run-id>/run_config.json`
- **Contents**: Snapshot of `pipeline_config.json` plus runtime metadata
- **Schema**:
```json
{
  "run_id": "20260320-1430-full",
  "started_at": "2026-03-20 14:30:00",
  "source_dir": "E:/Dev/IPPS/.windsurf",
  "models": {
    "mother": "claude-opus-4-6-20260204",
    "verifier": "gpt-5-mini"
  },
  "thresholds": { "judge_min_score": 3.5 },
  "budget": { "max_total_usd": 100.0 }
}
```

### RunCosts

A **RunCosts** tracks detailed cost breakdown per file and step.

- **Storage**: `runs/<run-id>/run_costs.json`
- **Schema**:
```json
{
  "total_usd": 45.32,
  "mother": {
    "input_usd": 25.10,
    "cached_read_usd": 3.20,
    "cached_write_usd": 5.02,
    "output_usd": 12.00
  },
  "verifier": {
    "input_usd": 1.02,
    "output_usd": 1.00
  },
  "per_step": {
    "analyze": { "calls": 3, "cost_usd": 8.50 },
    "compress": { "calls": 55, "cost_usd": 35.80 },
    "verify": { "calls": 55, "cost_usd": 1.02 }
  },
  "per_file": [
    {
      "path": "rules/core-conventions.md",
      "compress_cost": 0.52,
      "verify_cost": 0.02,
      "cache_hit": true
    }
  ]
}
```

### LLMClient

The **LLMClient** class provides unified LLM access for MinifyIPPS.

- **Source**: `lib/llm_client.py` (adapted from LLM-Research, extended with cache support)
- **Config loading**: `configs/model-registry.json`, `configs/model-pricing.json`, `configs/model-parameter-mapping.json`
- **Key methods**:
  - `call(prompt, max_tokens)` - unified API call (OpenAI or Anthropic)
  - `call_with_cache(bundle, prompt)` - bundle as cached system prompt, Anthropic only (NEW, not in original)
  - `check_context_fit(model, prompt)` - context window check
- **Constraints**: Minimum cacheable prefix size varies by model (per ANTAPI-IN18); caching silently skipped if bundle below threshold
- **Module functions**:
  - `calculate_cost(usage, model)` - compute cost from pricing JSON (handles cache_read/write tokens)
  - `get_model_pricing(model)` - lookup pricing by model ID

## 4. Functional Requirements

**MIPPS-FR-12: Run Isolation**
- Each pipeline execution creates `runs/<run-id>/` subfolder
- Run ID format: `<YYYYMMDD>-<HHMM>-<label>` (e.g., `20260320-1430-full`)
- CLI flag `--run-label <label>` sets label (default: `auto`)
- All outputs written to run folder: analysis, prompts, state, costs, compressed files
- `output/` (compressed files) is `runs/<run-id>/output/`, not top-level `output_dir`

**MIPPS-FR-13: Unified LLM Client**
- Replace `AnthropicClient` and `OpenAIClient` with unified `LLMClient` class
- Model selection by ID (e.g., `claude-opus-4-6-20260204`, `gpt-5-mini`)
- Auto-detect provider from model ID prefix via `model-registry.json`
- Parameter mapping via `model-parameter-mapping.json` (effort levels, thinking budgets)

**MIPPS-FR-14: Config-Based Model Settings**
- `pipeline_config.json` contains model IDs only, not parameters
- Model parameters resolved from `configs/model-registry.json`
- Pricing resolved from `configs/model-pricing.json`
- Effort mapping from `configs/model-parameter-mapping.json`

**MIPPS-FR-15: Automatic Cost Tracking**
- Every API call returns usage dict
- Cost calculated via `llm_client.calculate_cost(usage, model)`
- Per-call cost accumulated in `RunCosts`
- Cache hit/miss tracked per call (`cache_read_input_tokens > 0` = hit)
- Thinking tokens (extended thinking) billed as output tokens; high thinking budgets increase cost proportionally

**MIPPS-FR-16: Run Summary Generation**
- After Step 7, generate `run_summary.md` with:
  - Compression ratio (total, per-category)
  - Cost breakdown (mother, verifier, total)
  - Files passed/failed/manual review
  - Cache efficiency (hit rate, cost saved)

**MIPPS-FR-17: Run Comparison Tool**
- `compare_runs.py --runs <id1> <id2>` compares two runs
- Output: diff table (compression ratio, cost, files changed)
- Identify regressions (files that got worse)

**MIPPS-FR-18: Config Snapshot**
- At run start, copy `pipeline_config.json` to `runs/<run-id>/run_config.json`
- Add runtime metadata (run_id, started_at, resolved model IDs)
- Run is reproducible from its `run_config.json`

## 5. Design Decisions

**MIPPS-DD-12:** Copy config files to `configs/` instead of symlinks. Rationale: independence from `.windsurf/skills/llm-evaluation/` path; version-locked configs per pipeline version.

**MIPPS-DD-13:** Run ID uses timestamp, not UUID. Rationale: human-readable, sortable, identifies when run occurred.

**MIPPS-DD-14:** `llm_client.py` adapted, not imported. Rationale: MinifyIPPS needs `call_with_cache(bundle, prompt)` method for Anthropic prompt caching; vendored copy allows adding this method.

**MIPPS-DD-15:** Per-file cost tracking stored in `run_costs.json`, not `pipeline_state.json`. Rationale: separate concerns; state tracks progress, costs track spending.

**MIPPS-DD-16:** `compare_runs.py` and `generate_report.py` are optional tools, not pipeline steps. Rationale: core pipeline (Steps 1-7) unchanged; tools are post-run analysis.

**MIPPS-DD-17:** Cache TTL uses 5m (default, 1.25x write cost). Rationale: sequential synchronous calls refresh cache on each hit (per ANTAPI-IN18); 5m never expires during normal pipeline operation. 1h TTL (2x write cost) only needed for Batch API where request processing is deferred.

**MIPPS-DD-18:** `build_api_params()` must handle Opus 4.6 adaptive thinking. Claude Opus 4.6 requires `thinking: {"type": "adaptive"}` + `output_config: {"effort": ...}` (per ANTAPI-IN13). Manual `type: "enabled"` with `budget_tokens` is deprecated on Opus 4.6. Source `llm_client.py` lacks this code path.

**MIPPS-DD-19:** `model-pricing.json` must contain standard API rates. Pipeline uses synchronous Messages/Chat Completions API calls, not Batch API. Batch pricing (50% discount) only applies to Batch API endpoint. Vendored JSON has `_pricing_tier: "batch"` - must be updated to standard rates before first run.

## 6. Implementation Guarantees

**MIPPS-IG-06:** Run folder created atomically at pipeline start. If creation fails, pipeline aborts before any API calls.

**MIPPS-IG-07:** `run_config.json` written before first API call. Run is always traceable to its config.

**MIPPS-IG-08:** Cost tracking survives interruption. `run_costs.json` updated after each API call (atomic write).

**MIPPS-IG-09:** Model pricing lookup fails gracefully. If model not in `model-pricing.json`, cost set to 0.0 with warning logged.

## 7. Key Mechanisms

### LLM Client Integration

```python
# V1: Separate clients
mother = AnthropicClient(config)
verifier = OpenAIClient(config)

# V2: Unified client
from lib.llm_client import LLMClient, calculate_cost

mother = LLMClient(model="claude-opus-4-6-20260204", reasoning_effort="high")
verifier = LLMClient(model="gpt-5-mini", reasoning_effort="medium")
```

### Cache-Aware Cost Tracking

```python
def track_call(result: dict, model: str, run_costs: dict):
    usage = result["usage"]
    cost = calculate_cost(usage, model)
    
    # Track cache status
    cache_hit = usage.get("cache_read_input_tokens", 0) > 0
    
    # Accumulate
    run_costs["total_usd"] += cost["total_cost"]
    run_costs["per_file"].append({
        "path": current_file,
        "cost": cost["total_cost"],
        "cache_hit": cache_hit
    })
```

### Run Folder Creation

```python
def create_run(label: str = "auto") -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    run_id = f"{timestamp}-{label}"
    run_dir = BASE_DIR / "runs" / run_id
    
    # Create structure
    (run_dir / "analysis").mkdir(parents=True)
    (run_dir / "context").mkdir()
    (run_dir / "prompts/step").mkdir(parents=True)
    (run_dir / "prompts/transform").mkdir()
    (run_dir / "prompts/eval").mkdir()
    (run_dir / "verification").mkdir()
    (run_dir / "output").mkdir()
    
    return run_dir
```

## 8. Data Structures

### pipeline_config.json (V2)

```json
{
  "source_dir": ".windsurf/",
  "models": {
    "mother": "claude-opus-4-6-20260204",
    "verifier": "gpt-5-mini"
  },
  "reasoning_effort": "high",
  "output_length": "high",
  "thresholds": {
    "judge_min_score": 3.5,
    "exclusion_max_lines": 100,
    "exclusion_max_references": 2
  },
  "budget": {
    "max_total_usd": 100.0,
    "warning_threshold": 0.8
  },
  "include_patterns": ["*.md"],
  "skip_patterns": ["__pycache__/*", "**/__pycache__/*"],
  "never_compress": [
    "skills/llm-evaluation/prompts/*",
    "skills/llm-transcription/prompts/*"
  ],
  "api_timeout_seconds": 600
}
```

**Changes from V1:**
- `models.mother` is model ID string (was: object with `model`, `thinking`, `max_context`)
- `models.verifier` is model ID string (was: object with `model`)
- Added `reasoning_effort`, `output_length` for parameter mapping
- Removed hardcoded API parameters (resolved from registry)
- Removed `output_dir` (output always `run_dir / "output"` per FR-12)

### run_summary.md

```markdown
# Run Summary: 20260320-1430-full

**Started**: 2026-03-20 14:30:00
**Completed**: 2026-03-20 15:45:23
**Duration**: 1h 15m

## Compression Results

- **Files Total**: 154
- **Files Compressed**: 75
- **Files Excluded**: 20 (< 100 lines AND rarely loaded)
- **Files Copied (non-.md)**: 59
- **Compression Ratio**: 42.3%

## Verification

- **Passed**: 68 (90.7%)
- **Failed**: 7 (9.3%)
- **Manual Review**: 5

## Cost

| Model | Input | Cached | Output | Total |
|-------|-------|--------|--------|-------|
| claude-opus-4-6 | $25.10 | $3.20 | $12.00 | $40.30 |
| gpt-5-mini | $1.02 | - | $1.00 | $2.02 |
| **Total** | | | | **$42.32** |

## Cache Efficiency

- **Cache Hits**: 52/75 (69.3%)
- **Cost Saved**: ~$18.40
```

## 9. Module Structure

```
_run_templateV2/
├─> mipps_pipeline.py                  (entry point, CLI - MODIFIED)
├─> pipeline_config.json               (template config - MODIFIED)
├─> configs/
│   ├─> model-registry.json            (COPIED from llm-evaluation)
│   ├─> model-pricing.json             (COPIED from llm-evaluation)
│   └─> model-parameter-mapping.json   (COPIED from llm-evaluation)
├─> lib/
│   ├─> llm_client.py                  (NEW: unified client from LLM-Research)
│   ├─> file_bundle_builder.py         (unchanged)
│   ├─> mother_analyzer.py             (MODIFIED: use LLMClient)
│   ├─> mother_output_checker.py       (MODIFIED: use LLMClient)
│   ├─> compression_prompt_builder.py  (MODIFIED: use LLMClient)
│   ├─> file_compressor.py             (MODIFIED: use LLMClient + cost tracking)
│   ├─> compression_report_builder.py  (MODIFIED: use LLMClient)
│   ├─> compression_refiner.py         (MODIFIED: use LLMClient)
│   ├─> run_manager.py                 (NEW: run folder creation/management)
│   ├─> cost_tracker.py                (NEW: replaces api_cost_tracker.py)
│   └─> pipeline_state.py              (MODIFIED: per-run state path)
├─> prompts/
│   └─> step/                          (unchanged)
├─> compare_runs.py                    (NEW: run comparison tool)
└─> generate_report.py                 (NEW: optional HTML report)
```

## 10. Document History

**[2026-03-20 15:10]**
- Fixed: LLM acronym expanded on first use in Goal line (AP-PR-06)
- Fixed: Removed deprecated `output_dir` from pipeline_config.json V2 schema (contradicted FR-12)
- Fixed: `calculate_cost` description now mentions cache token handling
- Added: DD-17 - Cache TTL uses 5m default (sequential sync calls refresh on hit; 1h only for Batch API)
- Added: DD-18 - Opus 4.6 requires adaptive thinking (`type: "adaptive"` + `output_config.effort`); source lacks code path
- Added: DD-19 - model-pricing.json must use standard API rates (vendored JSON has batch tier, pipeline uses sync API)
- Added: LLMClient constraint - minimum cacheable prefix size varies by model (ANTAPI-IN18)
- Added: FR-15 note - thinking tokens billed as output tokens
- Added: Config schema "Changes from V1" note for `output_dir` removal
- Changed: `call_with_cache` description clarifies "bundle as cached system prompt, Anthropic only"

**[2026-03-20 14:38]**
- Fixed: AP-NM-01 "UnifiedLLMClient" renamed to "LLMClient" for consistency with code
- Fixed: Markdown table in section 2 converted to list (SPEC-CT-01)
- Fixed: DateTime format standardized to `YYYY-MM-DD HH:MM:SS` (AP-PR-01)
- Fixed: FR-12 clarified that `output/` is inside run folder
- Fixed: Domain object contents lists use consistent format
- Added: MNF now lists `run_manager.py` and `cost_tracker.py` new modules
- Added: `call_with_cache` noted as NEW method in LLMClient

**[2026-03-20 14:34]**
- Initial CHANGES specification for MinifyIPPS V2 (Option C)
- Defines run isolation, unified LLM client, config-based model settings
- Added FR-12 through FR-18, DD-12 through DD-16, IG-06 through IG-09
