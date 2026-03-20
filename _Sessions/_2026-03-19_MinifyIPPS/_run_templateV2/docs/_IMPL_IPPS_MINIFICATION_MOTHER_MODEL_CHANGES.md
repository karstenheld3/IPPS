# IMPL: MinifyIPPS V2 Architecture Changes

**Doc ID**: MIPPS-IP02
**Feature**: MIPPS-V2-ARCHITECTURE
**Goal**: Implement run-based isolation, unified Large Language Model (LLM) client, and config-based model settings in V2 template
**Timeline**: Created 2026-03-20, Updated 2 times

**Target files**:
- `pipeline_config.json` (MODIFY)
- `lib/llm_client.py` (MODIFY: fix config path, add call_with_cache, extend calculate_cost)
- `lib/run_manager.py` (NEW ~80 lines)
- `lib/cost_tracker.py` (NEW ~100 lines)
- `lib/pipeline_state.py` (MODIFY)
- `lib/mother_analyzer.py` (MODIFY: LLMClient + run_dir)
- `lib/mother_output_checker.py` (MODIFY: LLMClient)
- `lib/compression_prompt_builder.py` (MODIFY: LLMClient + run_dir)
- `lib/file_compressor.py` (MODIFY: LLMClient + cost tracking + run_dir)
- `lib/compression_report_builder.py` (MODIFY: LLMClient + run_dir)
- `lib/compression_refiner.py` (MODIFY: LLMClient)
- `mipps_pipeline.py` (MODIFY: run creation, --run-label, config snapshot, summary)
- `compare_runs.py` (NEW ~80 lines)
- `generate_report.py` (NEW ~60 lines, optional)
- `lib/llm_clients.py` (DELETE)
- `lib/api_cost_tracker.py` (DELETE)

**Depends on:**
- `_SPEC_IPPS_MINIFICATION_MOTHER_MODEL_CHANGES.md [MIPPS-SP02]` for all V2 requirements
- `_IMPL_IPPS_MINIFICATION_MOTHER_MODEL.md [MIPPS-IP01]` for V1 baseline behavior

## MUST-NOT-FORGET

- `llm_client.py` loads configs from `_SCRIPT_DIR` (= `lib/`) but JSONs are in `configs/` - fix path to `_SCRIPT_DIR / ".." / "configs"`
- `calculate_cost()` must handle `cached_per_1m` from pricing JSON (currently ignored)
- `call_with_cache()` is NEW method: system prompt with `cache_control: {"type": "ephemeral"}` - does not exist in vendored llm_client.py
- `_call_anthropic()` must support system prompt blocks (currently only uses messages)
- All 7 lib modules that use AnthropicClient/OpenAIClient must switch to LLMClient
- All output paths must use `run_dir` parameter, never write to session root
- `run_costs.json` updated atomically after each API call (IG-08)
- V1 files `llm_clients.py` and `api_cost_tracker.py` must be deleted after migration
- Budget check uses `cost_tracker.check_budget()`, not old `api_cost_tracker.check_budget()`
- Pricing tier: vendored `model-pricing.json` has `_pricing_tier: "batch"` (50% of standard). Pipeline uses synchronous API, not Batch API. Per DD-19, update JSON to standard rates before first run.
- `load_state(run_dir)` now takes directory path (V1 took file path) - all callers must update
- Opus 4.6 adaptive thinking: `build_api_params()` has no code path for `thinking: {"type": "adaptive"}` + `output_config: {"effort": ...}`. Manual `type: "enabled"` deprecated on Opus 4.6 (per DD-18, ANTAPI-IN13). Must add handling in IS-03.
- Minimum cacheable prefix size varies by model (per ANTAPI-IN18). If bundle below threshold, caching silently skipped - no error, just no cache benefit.
- `--resume <run-id>` deferred to future version; not in MIPPS-SP02 scope
- Subsequent steps locate run via `--run-id <id>` flag or auto-detect latest run in `runs/`
- `output_dir` in pipeline_config.json is deprecated; output always goes to `run_dir / "output"`

## Table of Contents

1. [File Structure](#1-file-structure)
2. [Edge Cases](#2-edge-cases)
3. [Implementation Steps](#3-implementation-steps)
4. [Test Cases](#4-test-cases)
5. [Verification Checklist](#5-verification-checklist)
6. [Document History](#6-document-history)

## 1. File Structure

```
_run_templateV2/
├── mipps_pipeline.py                  (MODIFY: run creation, --run-label, config snapshot)
├── pipeline_config.json               (MODIFY: model IDs, reasoning_effort, output_length)
├── compare_runs.py                    (NEW: run comparison tool)
├── generate_report.py                 (NEW: optional HTML report)
├── configs/
│   ├── model-registry.json            (unchanged, copied from llm-evaluation)
│   ├── model-pricing.json             (unchanged, copied from llm-evaluation)
│   └── model-parameter-mapping.json   (unchanged, copied from llm-evaluation)
├── lib/
│   ├── __init__.py                    (unchanged)
│   ├── llm_client.py                  (MODIFY: config path, call_with_cache, cache cost)
│   ├── run_manager.py                 (NEW: run folder, config snapshot, summary)
│   ├── cost_tracker.py                (NEW: RunCosts tracking, replaces api_cost_tracker.py)
│   ├── pipeline_state.py              (MODIFY: per-run state path)
│   ├── file_bundle_builder.py         (unchanged)
│   ├── mother_analyzer.py             (MODIFY: LLMClient + run_dir)
│   ├── mother_output_checker.py       (MODIFY: LLMClient)
│   ├── compression_prompt_builder.py  (MODIFY: LLMClient + run_dir)
│   ├── file_compressor.py             (MODIFY: LLMClient + cost tracking + run_dir)
│   ├── compression_report_builder.py  (MODIFY: LLMClient + run_dir)
│   └── compression_refiner.py         (MODIFY: LLMClient)
├── prompts/
│   └── step/                          (unchanged)
├── tests/                             (NEW: V2-specific tests)
└── runs/                              (created at runtime)
    └── <run-id>/                      (per-run artifacts)
```

**Deleted files** (after migration):
- `lib/llm_clients.py` (V1 AnthropicClient + OpenAIClient)
- `lib/api_cost_tracker.py` (V1 hardcoded PRICING dict)

## 2. Edge Cases

### Config & Client

- **MIPPS-IP02-EC-01**: `configs/` directory missing at import -> `FileNotFoundError` with clear path in message
- **MIPPS-IP02-EC-02**: Model ID not in `model-registry.json` -> `ValueError` listing known prefixes (existing behavior)
- **MIPPS-IP02-EC-03**: Model not in `model-pricing.json` -> cost set to 0.0, `pricing_found: false`, warning logged (IG-09)
- **MIPPS-IP02-EC-04**: `cached_per_1m` missing from pricing entry -> treat cache cost as 0.0 (some models lack cache pricing)

### Run Management

- **MIPPS-IP02-EC-05**: `runs/` directory does not exist -> create it (mkdir parents=True)
- **MIPPS-IP02-EC-06**: Run ID collision (same timestamp, same label) -> append `-2`, `-3` suffix
- **MIPPS-IP02-EC-07**: Run folder creation fails (permissions, disk full) -> abort before any API calls (IG-06)
- **MIPPS-IP02-EC-08**: `run_costs.json` write fails mid-pipeline -> log error, continue (cost data is supplementary)

### Cache Tracking

- **MIPPS-IP02-EC-09**: Anthropic response missing `cache_creation_input_tokens` field -> default to 0 (older API versions)
- **MIPPS-IP02-EC-10**: Cache expired mid-step (`cache_read_input_tokens == 0` on non-first call) -> log cost delta warning, track as cache miss
- **MIPPS-IP02-EC-11**: Bundle below minimum cacheable prefix size -> caching silently skipped by API, no error; log warning if `cache_creation_input_tokens == 0` on first call with cache

## 3. Implementation Steps

### Phase 1: Config & LLM Client (IS-01 to IS-04)

#### MIPPS-IP02-IS-01: Update pipeline_config.json to V2 format

**Location**: `pipeline_config.json`

**Action**: Modify config to use model ID strings instead of objects

**Code**:
```json
{
  "source_dir": ".windsurf/",
  "models": {
    "mother": "claude-opus-4-6-20260204",
    "verifier": "gpt-5-mini"
  },
  "reasoning_effort": "high",
  "output_length": "high",
  "thresholds": { ... },
  "budget": {
    "max_total_usd": 100.0,
    "warning_threshold": 0.8
  },
  ...
}
```

**Note**: Key changes: `models.mother` from `{"provider": ..., "model": ..., "thinking": true}` to plain string `"claude-opus-4-6-20260204"`. `models.verification` renamed to `models.verifier`. `budget.warn_at_percent` renamed to `budget.warning_threshold` (0.0-1.0 ratio). Remove `cache.ttl` (cache is always ephemeral per Anthropic API). Remove `output_dir` (output now always `run_dir / "output"`).

#### MIPPS-IP02-IS-02: Fix llm_client.py config loading path

**Location**: `lib/llm_client.py` > module-level config loading

**Action**: Modify `_SCRIPT_DIR` resolution to find `configs/` directory

**Code**:
```python
_SCRIPT_DIR = Path(__file__).parent
_CONFIGS_DIR = _SCRIPT_DIR.parent / "configs"

def _load_json_config(filename: str) -> dict:
    config_path = _CONFIGS_DIR / filename
    ...
```

**Note**: Current code loads from `_SCRIPT_DIR` (= `lib/`), but JSONs are in `configs/` (sibling of `lib/`). Must resolve to `lib/../configs/`.

#### MIPPS-IP02-IS-03: Add call_with_cache method to LLMClient

**Location**: `lib/llm_client.py` > `LLMClient` class and `_call_anthropic` function

**Action**: Add `call_with_cache(bundle, prompt)` method and extend `_call_anthropic` to support system prompt with `cache_control`

**Code**:
```python
# In LLMClient class:
def call_with_cache(self, bundle: str, prompt: str) -> dict:
    """Call with cached system prompt (Anthropic only)."""
    ...

# New function:
def _call_anthropic_with_cache(client, model: str, bundle: str, prompt: str, api_params: dict) -> dict:
    """Call Anthropic with bundle as cached system prompt."""
    ...
```

**Note**: `_call_anthropic_with_cache` must pass `system` as array of content blocks (not string):
```python
system=[
    {"type": "text", "text": bundle, "cache_control": {"type": "ephemeral"}}  # 5m TTL per DD-17
]
```
Response includes `cache_creation_input_tokens` and `cache_read_input_tokens` in usage (per ANTAPI-IN06). Text extraction must join ALL `text` type blocks (current `_call_anthropic` only gets first via `break`); skip `thinking` type blocks (have `thinking` attr, not `text`). Method raises `ValueError` if provider is not anthropic.

**Opus 4.6 thinking**: If model is claude-opus-4-6, `build_api_params` must use `thinking: {"type": "adaptive"}` + `output_config: {"effort": ...}` instead of deprecated `type: "enabled"` with `budget_tokens` (per DD-18, ANTAPI-IN13). Source `build_api_params()` lacks this code path - add `method: 'adaptive_thinking'` handling or update existing `'thinking'` path to detect Opus 4.6.

#### MIPPS-IP02-IS-04: Extend calculate_cost for cache tokens

**Location**: `lib/llm_client.py` > `calculate_cost()` function

**Action**: Modify to handle `cached_per_1m` pricing and cache token fields in usage

**Code**:
```python
def calculate_cost(usage: dict, model: str, provider: str = None) -> dict:
    # Existing: input_tokens, output_tokens
    # Add: cache_read_input_tokens, cache_creation_input_tokens
    # Use: cached_per_1m from pricing, cache_write = input_per_1m * 1.25
    ...
```

**Note**: Anthropic usage dict contains 4 token fields. Cost decomposition (5m TTL per DD-17):
```
non_cached_input = input_tokens - cache_read_input_tokens - cache_creation_input_tokens
input_cost       = non_cached_input / 1M * input_per_1m
cache_read_cost  = cache_read_input_tokens / 1M * cached_per_1m           (0.1x base)
cache_write_cost = cache_creation_input_tokens / 1M * input_per_1m * 1.25 (1.25x base, 5m TTL)
output_cost      = output_tokens / 1M * output_per_1m
```
Return dict adds `cache_read_cost`, `cache_write_cost` fields. Handle EC-04: if `cached_per_1m` missing, set both cache costs to 0.0. Thinking tokens (extended thinking) are included in `output_tokens` by the API and billed at output rate - no special handling needed, but high thinking budgets significantly increase output cost. **Pricing tier**: vendored model-pricing.json has `_pricing_tier: "batch"` (50% of standard). Per DD-19, must be updated to standard rates before first run since pipeline uses synchronous API.

### Phase 2: Run Management & Cost Tracking (IS-05 to IS-07)

#### MIPPS-IP02-IS-05: Create lib/run_manager.py

**Location**: `lib/run_manager.py` (NEW)

**Action**: Create module for run folder creation, config snapshot, and summary generation

**Code**:
```python
def create_run(base_dir: Path, label: str = "auto") -> tuple[str, Path]: ...
def snapshot_config(config: dict, run_dir: Path, run_id: str) -> None: ...
def generate_run_summary(run_dir: Path, state: dict, costs: dict) -> None: ...
```

**Note**: `create_run` generates run ID as `<YYYYMMDD>-<HHMM>-<label>`, creates subdirectory structure (analysis, context, prompts/step, prompts/transform, prompts/eval, verification, output). Handle EC-05 (missing runs/), EC-06 (ID collision), EC-07 (creation failure). `snapshot_config` writes `run_config.json` with fields: `run_id`, `started_at`, `source_dir`, `models` (resolved IDs), `thresholds`, `budget` - must be written before first API call (IG-07). `generate_run_summary` computes: compression ratio = `1 - (compressed_tokens / original_tokens)`, cache hit rate = `cache_hits / total_mother_calls`, cost saved = `cache_hits * (input_per_1m - cached_per_1m) * avg_bundle_tokens / 1M`.

#### MIPPS-IP02-IS-06: Create lib/cost_tracker.py

**Location**: `lib/cost_tracker.py` (NEW)

**Action**: Create module for RunCosts accumulation with per-file, per-step tracking

**Code**:
```python
def init_costs() -> dict: ...
def track_call(costs: dict, step: str, file_path: str, usage: dict, model: str, cache_hit: bool) -> None: ...
def save_costs(costs: dict, run_dir: Path) -> None: ...
def load_costs(run_dir: Path) -> dict: ...
def check_budget(costs: dict, config: dict) -> tuple[bool, str]: ...
```

**Note**: `track_call` uses `llm_client.calculate_cost()` for cost computation, accumulates in RunCosts dict per MIPPS-SP02 schema. `save_costs` uses atomic write pattern (write .tmp, rename). Called after each API call (IG-08). Handle EC-08 (write failure). `check_budget` replaces `api_cost_tracker.check_budget()` with `warning_threshold` (0.0-1.0 ratio) instead of `warn_at_percent`.

#### MIPPS-IP02-IS-07: Modify lib/pipeline_state.py for per-run state

**Location**: `lib/pipeline_state.py`

**Action**: Modify state functions to accept `run_dir` (directory) instead of file path

**Code**:
```python
def load_state(run_dir: Path) -> dict: ...
def save_state(run_dir: Path, state: dict) -> None: ...
```

**Note**: **Breaking API change**: V1 signature was `load_state(path: Path)` where path = full file path. V2 signature is `load_state(run_dir: Path)` where run_dir = directory. Functions internally resolve `run_dir / "pipeline_state.json"`. All callers in `mipps_pipeline.py` must update. Existing atomic write pattern preserved. No schema changes.

### Phase 3: Module Migration (IS-08 to IS-14)

Each module change follows the same pattern:
1. Replace `AnthropicClient`/`OpenAIClient` parameter types with `LLMClient`
2. Replace `client.call_with_cache(bundle, prompt)` or `client.call(prompt)` calls
3. Add `run_dir: Path` parameter where output paths change
4. Add `costs: dict` parameter where cost tracking needed
5. Update output file paths from `BASE_DIR / "_0N_..."` to `run_dir / "subdir/..."`
6. Return usage dict from each API call for cost tracking via `cost_tracker.track_call()`

#### MIPPS-IP02-IS-08: Modify mother_analyzer.py

**Location**: `lib/mother_analyzer.py`

**Action**: Replace AnthropicClient with LLMClient, output to `run_dir/analysis/`

**Code**:
```python
def analyze_call_tree(client: LLMClient, bundle: str, prompt: str, run_dir: Path) -> str: ...
def analyze_complexity(client: LLMClient, bundle: str, prompt: str, run_dir: Path) -> str: ...
def generate_strategy(client: LLMClient, bundle: str, prompt: str, excluded: list, run_dir: Path) -> str: ...
```

**Note**: V1 used `AnthropicClient.call_with_cache()`; V2 uses `LLMClient.call_with_cache()` (same method name, different class). Output paths: `run_dir / "analysis" / "_01_FILE_CALL_TREE.md"`, etc.

#### MIPPS-IP02-IS-09: Modify mother_output_checker.py

**Location**: `lib/mother_output_checker.py`

**Action**: Replace OpenAIClient with LLMClient

**Code**:
```python
def spot_check_document(client: LLMClient, document: str, source_files: list, sample_size: int = 15) -> dict: ...
```

**Note**: Uses `client.call(prompt)` (not `call_with_cache` - no bundle needed for spot checks). Return usage for cost tracking.

#### MIPPS-IP02-IS-10: Modify compression_prompt_builder.py

**Location**: `lib/compression_prompt_builder.py`

**Action**: Replace AnthropicClient with LLMClient, save prompts to run_dir

**Code**:
```python
def generate_compression_prompts(client: LLMClient, bundle: str, strategy: str, file_types: list) -> dict: ...
def save_prompts(prompts: dict, run_dir: Path) -> None: ...
```

**Note**: `save_prompts` writes to `run_dir / "prompts" / "transform"` and `run_dir / "prompts" / "eval"`. Uses `client.call_with_cache(bundle, prompt)`.

#### MIPPS-IP02-IS-11: Modify file_compressor.py

**Location**: `lib/file_compressor.py`

**Action**: Replace both clients with LLMClient, add cost tracking, output to run_dir

**Code**:
```python
def compress_file(mother: LLMClient, verifier: LLMClient, file_path: Path,
                  bundle: str, prompt: str, eval_prompt: str, config: dict,
                  costs: dict) -> dict: ...
def run_compression_step(mother: LLMClient, verifier: LLMClient, bundle: str,
                         source_dir: Path, run_dir: Path, config: dict, state: dict,
                         costs: dict) -> dict: ...
```

**Note**: Most complex migration. Compression uses `mother.call_with_cache(bundle, prompt)`, verification uses `verifier.call(prompt)`. After each call, invoke `cost_tracker.track_call()`. Output compressed files to `run_dir / "output"`. Copy non-.md files to `run_dir / "output"` (unchanged logic from V1 IS-12).

#### MIPPS-IP02-IS-12: Modify compression_report_builder.py

**Location**: `lib/compression_report_builder.py`

**Action**: Replace OpenAIClient with LLMClient, output to run_dir/verification

**Code**:
```python
def verify_file(client: LLMClient, original: str, compressed: str, prompt: str) -> dict: ...
def generate_report(results: list, cross_ref_issues: list, run_dir: Path) -> str: ...
```

**Note**: Report written to `run_dir / "verification" / "_04_FILE_COMPRESSION_REPORT.md"`. Manual review queue to `run_dir / "verification" / "_05_MANUAL_REVIEW_QUEUE.md"`.

#### MIPPS-IP02-IS-13: Modify compression_refiner.py

**Location**: `lib/compression_refiner.py`

**Action**: Replace AnthropicClient with LLMClient

**Code**:
```python
def review_report(client: LLMClient, bundle: str, report: str) -> dict: ...
```

**Note**: Uses `client.call_with_cache(bundle, prompt)`. Strategy file path now `run_dir / "analysis" / "_03_FILE_COMPRESSION_STRATEGY.md"`.

#### MIPPS-IP02-IS-14: Delete V1 client files

**Location**: `lib/llm_clients.py`, `lib/api_cost_tracker.py`

**Action**: Delete both files after all modules migrated to LLMClient + cost_tracker

**Note**: Verify no remaining imports of `llm_clients` or `api_cost_tracker` in any module. Run: `grep -r "from lib.llm_clients\|from lib.api_cost_tracker\|import llm_clients\|import api_cost_tracker" lib/ mipps_pipeline.py`

### Phase 4: Pipeline Command-Line Interface (CLI) & Tools (IS-15 to IS-18)

#### MIPPS-IP02-IS-15: Modify mipps_pipeline.py for run management

**Location**: `mipps_pipeline.py`

**Action**: Add `--run-label` and `--run-id` flags, create run folder at start, pass `run_dir` to all steps

**Code**:
```python
# Global arguments added to all subcommands:
parser.add_argument("--run-label", default="auto", help="Label for this run")
parser.add_argument("--run-id", default=None, help="Resume existing run by ID")

# In each cmd_* function:
def cmd_bundle(args):
    if args.run_id:
        run_dir = BASE_DIR / "runs" / args.run_id
    else:
        run_id, run_dir = create_run(BASE_DIR, args.run_label)
        snapshot_config(config, run_dir, run_id)
    costs = load_costs(run_dir) if args.run_id else init_costs()
    ...
    save_costs(costs, run_dir)
```

**Note**: Replace all `BASE_DIR` output paths with `run_dir`. Replace `AnthropicClient(config)` / `OpenAIClient(config)` with `LLMClient(model=config["models"]["mother"], reasoning_effort=config["reasoning_effort"])` / `LLMClient(model=config["models"]["verifier"], reasoning_effort="medium")`. Remove `_state_path()` function, use `run_dir` directly. When `--run-id` not provided and no `--run-label`, auto-detect latest run folder by sorting `runs/` entries. If `runs/` empty, create new run.

#### MIPPS-IP02-IS-16: Add run summary generation

**Location**: `mipps_pipeline.py` > `cmd_verify()`

**Action**: Generate `run_summary.md` after verification step completes

**Code**:
```python
def cmd_verify(args):
    ...
    # After report generation:
    generate_run_summary(run_dir, state, costs)
    save_costs(costs, run_dir)
```

**Note**: Summary format per MIPPS-SP02 section 8 (run_summary.md template). Includes compression ratio, verification results, cost breakdown, cache efficiency.

#### MIPPS-IP02-IS-17: Create compare_runs.py

**Location**: `compare_runs.py` (NEW)

**Action**: Create run comparison tool

**Code**:
```python
def load_run_data(run_dir: Path) -> dict: ...
def compare_runs(run_dirs: list[Path]) -> str: ...
def main(): ...  # CLI: compare_runs.py --runs <id1> <id2>
```

**Note**: Loads `pipeline_state.json` and `run_costs.json` from each run. Compares compression ratio, cost, files passed/failed. Identifies regressions (files with worse scores). Per MIPPS-DD-16, this is optional tooling, not a pipeline step.

#### MIPPS-IP02-IS-18: Create generate_report.py (optional)

**Location**: `generate_report.py` (NEW)

**Action**: Create optional Hypertext Markup Language (HTML) report generator

**Code**:
```python
def generate_html_report(run_dir: Path, output_path: Path = None) -> None: ...
def main(): ...  # CLI: generate_report.py --run <id>
```

**Note**: Low priority. Generates HTML dashboard from run data. Per MIPPS-DD-16, optional tooling.

## 4. Test Cases

### Category 1: LLM Client Changes (5 tests)

- **MIPPS-IP02-TC-01**: Config loading from `configs/` directory -> ok=true, loads all 3 JSON files
- **MIPPS-IP02-TC-02**: `call_with_cache` with mock Anthropic -> ok=true, system prompt has `cache_control` block
- **MIPPS-IP02-TC-03**: `calculate_cost` with cache tokens -> ok=true, includes `cache_read_cost` and `cache_write_cost`
- **MIPPS-IP02-TC-04**: `calculate_cost` with model missing from pricing -> ok=true, returns `pricing_found: false`, costs 0.0
- **MIPPS-IP02-TC-05**: `call_with_cache` on non-Anthropic model -> ok=false, raises `ValueError`

### Category 2: Run Management (5 tests)

- **MIPPS-IP02-TC-06**: `create_run` creates folder structure -> ok=true, all subdirs exist
- **MIPPS-IP02-TC-07**: `create_run` with collision -> ok=true, appends `-2` suffix
- **MIPPS-IP02-TC-08**: `snapshot_config` writes `run_config.json` -> ok=true, contains run_id and started_at
- **MIPPS-IP02-TC-09**: `generate_run_summary` produces markdown -> ok=true, contains compression ratio and cost sections
- **MIPPS-IP02-TC-10**: `create_run` with missing `runs/` dir -> ok=true, creates `runs/` parent

### Category 3: Cost Tracking (5 tests)

- **MIPPS-IP02-TC-11**: `track_call` accumulates total_usd -> ok=true, total increases
- **MIPPS-IP02-TC-12**: `track_call` records per-file cost -> ok=true, file entry in `per_file` list
- **MIPPS-IP02-TC-13**: `track_call` records cache_hit status -> ok=true, `cache_hit: true` when `cache_read_input_tokens > 0`
- **MIPPS-IP02-TC-14**: `save_costs` atomic write -> ok=true, file exists after save, no partial writes
- **MIPPS-IP02-TC-15**: `check_budget` at 80% threshold -> ok=false (no halt), returns warning message

### Category 4: Module Migration (4 tests)

- **MIPPS-IP02-TC-16**: `mother_analyzer` uses LLMClient.call_with_cache -> ok=true, outputs to `run_dir/analysis/`
- **MIPPS-IP02-TC-17**: `file_compressor` tracks costs per file -> ok=true, `run_costs.json` has per_file entries
- **MIPPS-IP02-TC-18**: `compression_report_builder` outputs to `run_dir/verification/` -> ok=true, report file at expected path
- **MIPPS-IP02-TC-19**: No remaining imports of `llm_clients` or `api_cost_tracker` -> ok=true, grep returns 0 matches

### Category 5: Pipeline CLI (4 tests)

- **MIPPS-IP02-TC-20**: `bundle --run-label test` creates `runs/YYYYMMDD-HHMM-test/` -> ok=true
- **MIPPS-IP02-TC-21**: `status` reads state from run folder -> ok=true, displays run-specific progress
- **MIPPS-IP02-TC-22**: Pipeline creates `run_config.json` before first API call -> ok=true, file exists before bundle step calls API
- **MIPPS-IP02-TC-23**: `verify` generates `run_summary.md` -> ok=true, summary file in run folder

### Category 6: Error Handling (6 tests)

- **MIPPS-IP02-TC-24**: Config loading with missing `configs/` dir -> ok=false, `FileNotFoundError` with path (EC-01)
- **MIPPS-IP02-TC-25**: Unknown model ID in registry -> ok=false, `ValueError` listing known prefixes (EC-02)
- **MIPPS-IP02-TC-26**: Run folder creation fails (read-only dir) -> ok=false, aborts before API calls (EC-07)
- **MIPPS-IP02-TC-27**: `save_costs` write failure -> ok=true, logs error but continues (EC-08)
- **MIPPS-IP02-TC-28**: Anthropic response without `cache_creation_input_tokens` -> ok=true, defaults to 0 (EC-09)
- **MIPPS-IP02-TC-29**: Cache miss on non-first call -> ok=true, logs warning with cost delta (EC-10)
- **MIPPS-IP02-TC-33**: Bundle below cache minimum on first call -> ok=true, logs warning when `cache_creation_input_tokens == 0` (EC-11)

### Category 7: Comparison Tool (3 tests)

- **MIPPS-IP02-TC-30**: `compare_runs` with 2 valid runs -> ok=true, outputs diff table
- **MIPPS-IP02-TC-31**: `compare_runs` with nonexistent run -> ok=false, clear error message
- **MIPPS-IP02-TC-32**: `compare_runs` identifies regression -> ok=true, lists files with worse scores

## 5. Verification Checklist

### Prerequisites

- [ ] **MIPPS-IP02-VC-01**: MIPPS-SP02 read and understood
- [ ] **MIPPS-IP02-VC-02**: MIPPS-IP01 read for V1 baseline behavior
- [ ] **MIPPS-IP02-VC-03**: V2 template folder exists with configs/ populated

### Phase 1: Config & LLM Client

- [ ] **MIPPS-IP02-VC-04**: IS-01 completed (pipeline_config.json V2 format)
- [ ] **MIPPS-IP02-VC-05**: IS-02 completed (config loading path fixed)
- [ ] **MIPPS-IP02-VC-06**: IS-03 completed (call_with_cache added)
- [ ] **MIPPS-IP02-VC-07**: IS-04 completed (calculate_cost handles cache)
- [ ] **MIPPS-IP02-VC-08**: TC-01 through TC-05 pass (LLM client changes)

### Phase 2: Run Management & Cost

- [ ] **MIPPS-IP02-VC-09**: IS-05 completed (run_manager.py)
- [ ] **MIPPS-IP02-VC-10**: IS-06 completed (cost_tracker.py)
- [ ] **MIPPS-IP02-VC-11**: IS-07 completed (pipeline_state.py per-run)
- [ ] **MIPPS-IP02-VC-12**: TC-06 through TC-15 pass (run management + cost tracking)

### Phase 3: Module Migration

- [ ] **MIPPS-IP02-VC-13**: IS-08 through IS-13 completed (all modules migrated)
- [ ] **MIPPS-IP02-VC-14**: IS-14 completed (V1 files deleted)
- [ ] **MIPPS-IP02-VC-15**: TC-16 through TC-19 pass (module migration)
- [ ] **MIPPS-IP02-VC-16**: No remaining imports of `llm_clients` or `api_cost_tracker`

### Phase 4: Pipeline & Tools

- [ ] **MIPPS-IP02-VC-17**: IS-15 completed (mipps_pipeline.py V2)
- [ ] **MIPPS-IP02-VC-18**: IS-16 completed (run summary generation)
- [ ] **MIPPS-IP02-VC-19**: IS-17 completed (compare_runs.py)
- [ ] **MIPPS-IP02-VC-20**: IS-18 completed (generate_report.py, optional)
- [ ] **MIPPS-IP02-VC-21**: TC-20 through TC-23 pass (CLI)

### Phase 5: Error Handling & Tools

- [ ] **MIPPS-IP02-VC-22**: TC-24 through TC-29 and TC-33 pass (error handling)
- [ ] **MIPPS-IP02-VC-23**: TC-30 through TC-32 pass (comparison tool)

### Validation

- [ ] **MIPPS-IP02-VC-24**: All 33 test cases pass
- [ ] **MIPPS-IP02-VC-25**: Full pipeline run creates isolated run folder with all artifacts
- [ ] **MIPPS-IP02-VC-26**: `run_costs.json` contains accurate per-file costs
- [ ] **MIPPS-IP02-VC-27**: `run_summary.md` generated with correct metrics
- [ ] **MIPPS-IP02-VC-28**: V1 compression behavior unchanged (same results, different file locations)

## 6. Document History

**[2026-03-20 15:15]**
- Fixed: IS-03 Action/Code signature mismatch - removed `ttl` param from Action (5m default per DD-17)
- Fixed: IS-04 cache write cost formula - explicit decomposition with 4 token fields and TTL-specific multiplier
- Fixed: MNF pricing tier entry - clarified batch vs standard, added DD-19 reference
- Added: IS-03 Note - system prompt must be array of content blocks (not string), shown with code example
- Added: IS-03 Note - Opus 4.6 adaptive thinking gap (`build_api_params` lacks `type: "adaptive"` path per DD-18)
- Added: IS-03 Note - text extraction must join ALL text blocks (source only gets first via `break`)
- Added: IS-04 Note - thinking tokens billed as output (no special handling, but cost impact noted)
- Added: MNF entry for Opus 4.6 adaptive thinking gap
- Added: MNF entry for minimum cacheable prefix size (ANTAPI-IN18)
- Added: EC-11 - bundle below minimum cacheable prefix size
- Added: TC-33 - cache minimum prefix test
- Changed: Test count 32 -> 33 (EC-11 coverage)

**[2026-03-20 15:05]**
- Fixed: Run identification gap - added `--run-id` flag and auto-detect latest run for subsequent steps (CRITICAL)
- Fixed: EC-TC coverage gap - added 6 error handling tests (TC-24 to TC-29) covering EC-01, EC-02, EC-07, EC-08, EC-09, EC-10
- Fixed: `output_dir` ambiguity - removed from pipeline_config.json, output always `run_dir / "output"`
- Fixed: LLM acronym expanded on first use in Goal line (AP-PR-06)
- Fixed: CLI expanded to "Command-Line Interface (CLI)" in Phase 4 heading
- Fixed: HTML expanded to "Hypertext Markup Language (HTML)" in IS-18
- Changed: Test count 26 -> 32 (6 error handling tests added)
- Changed: VC count 26 -> 28 (added Phase 5 error handling + tools sections)
- Changed: Comparison tool tests renumbered TC-30 to TC-32

**[2026-03-20 14:58]**
- Fixed: Phase ordering - IS-08 (delete V1 files) moved from Phase 2 to end of Phase 3 (depends on module migration)
- Fixed: IS-09 Note - clarified V1 AnthropicClient vs V2 LLMClient distinction
- Fixed: IS-07 Note - documented breaking API change (file path -> directory path)
- Fixed: IS-04 Note - explicit cache write cost formula, pricing tier discrepancy noted
- Fixed: IS-05 Note - added run_config.json fields and cache efficiency formulas
- Fixed: IS-15 Note - added reasoning_effort params to LLMClient constructor calls
- Added: MNF entries for pricing tier change, load_state API break, --resume deferral
- Added: Pattern step 6 (return usage dict) to Phase 3 migration pattern
- Removed: --resume flag from IS-15 (not in MIPPS-SP02 scope)
- Changed: IS renumbered (Phase 2: IS-05 to IS-07, Phase 3: IS-08 to IS-14)

**[2026-03-20 14:55]**
- Initial implementation plan for MinifyIPPS V2 architecture changes
- 18 implementation steps across 4 phases
- 10 edge cases identified
- 26 test cases defined
- 26 verification checklist items
- Key finding: llm_client.py config path mismatch, missing call_with_cache, missing cache cost calculation
