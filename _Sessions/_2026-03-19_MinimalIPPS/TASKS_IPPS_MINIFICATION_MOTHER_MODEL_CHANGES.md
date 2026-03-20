# TASKS: MinimalIPPS V2 Architecture Changes

**Doc ID (TDID)**: MIPPS-TK01
**Feature**: MIPPS-V2-ARCHITECTURE
**Goal**: Partitioned tasks for V2 run isolation, unified Large Language Model (LLM) client, and config-based model settings
**Source**: `_IMPL_IPPS_MINIFICATION_MOTHER_MODEL_CHANGES.md [MIPPS-IP02]`
**Strategy**: PARTITION-DEPENDENCY

**Depends on:**
- `_SPEC_IPPS_MINIFICATION_MOTHER_MODEL_CHANGES.md [MIPPS-SP02]` for requirements
- `_IMPL_IPPS_MINIFICATION_MOTHER_MODEL_CHANGES.md [MIPPS-IP02]` for implementation steps

## MUST-NOT-FORGET

- Each task must be verified before moving to next dependent task
- Test files created in `tests/` directory within `_run_templateV2/`
- All tests use pytest; mocks for API calls (no real LLM calls)
- Run `python -m pytest tests/ -v` from `_run_templateV2/` to run all tests
- Never commit a task that breaks previously passing tests

## Task Overview

- Total tasks: 16
- Estimated total: 6.25 HHW
- Parallelizable: 9 tasks (marked [P])

## Task 0 - Baseline (MANDATORY)

Run before starting any implementation:
- [ ] Verify `_run_templateV2/` folder exists with `configs/`, `lib/`, `prompts/`
- [ ] Verify `configs/model-pricing.json`, `configs/model-registry.json`, `configs/model-parameter-mapping.json` exist
- [ ] Verify `lib/llm_client.py` loads without error: `python -c "import sys; sys.path.insert(0,'lib'); exec(open('lib/llm_client.py').read())"` (expect FileNotFoundError from config path - this IS the known bug)
- [ ] Record which V1 modules exist: `lib/llm_clients.py`, `lib/api_cost_tracker.py`
- [ ] Create `tests/__init__.py` and `tests/conftest.py` with shared fixtures:
  - `tmp_run_dir` - creates temp run folder with standard subdirs, cleans up after test
  - `mock_anthropic_client` - patched Anthropic client returning configurable mock responses
  - `mock_openai_client` - patched OpenAI client returning configurable mock responses
  - `sample_config` - returns valid V2 pipeline_config dict
  - `sample_usage` - returns Anthropic usage dict with cache fields
  - `sample_pricing` - returns model-pricing.json dict with standard rates

## Tasks

### Phase 1: Config and LLM Client Foundation

- [ ] **MIPPS-TK-001** - Update pipeline_config.json to V2 format
  - IS: IS-01
  - Files: `pipeline_config.json`
  - Done when: JSON has model ID strings (not objects), `reasoning_effort`/`output_length` fields, no `output_dir`, `budget.warning_threshold` (0.0-1.0)
  - Verify: `python -c "import json; c=json.load(open('pipeline_config.json')); assert isinstance(c['models']['mother'], str); assert 'output_dir' not in c; print('OK')"`
  - Guardrails: Must not change `source_dir`, `thresholds`, `include_patterns`, `skip_patterns`, `never_compress`
  - Test req: Write `tests/test_config.py::test_pipeline_config_v2_schema` - validate all required fields present, model values are strings, no deprecated fields
  - Depends: none
  - Est: 0.25 HHW

- [ ] **MIPPS-TK-002** - Fix config loading path and update pricing to standard tier
  - IS: IS-02 + DD-19
  - Files: `lib/llm_client.py`, `configs/model-pricing.json`
  - Done when: `_load_json_config` reads from `configs/` (not `lib/`); `model-pricing.json` has `_pricing_tier: "standard"` with doubled rates
  - Verify: `python -c "from lib.llm_client import MODEL_REGISTRY, MODEL_PRICING; print(len(MODEL_REGISTRY['model_id_startswith']), 'models'); print(MODEL_PRICING['anthropic']['claude-opus-4-6-20260204']['input_per_1m'], 'USD/MTok')"`
  - Guardrails: Must not change any function signatures or class interfaces
  - Test req: Write `tests/test_config.py::test_config_loading_from_configs_dir` (TC-01) - verify 3 JSON files load; `test_config_missing_dir` (TC-24) - verify FileNotFoundError with path; `test_pricing_standard_tier` - verify `_pricing_tier == "standard"` and opus-4-6 input >= $10/MTok
  - Depends: TK-001
  - Est: 0.25 HHW

- [ ] **MIPPS-TK-003** - Extend calculate_cost for cache tokens
  - IS: IS-04
  - Files: `lib/llm_client.py`
  - Done when: `calculate_cost()` handles `cache_read_input_tokens`, `cache_creation_input_tokens`; returns `cache_read_cost`, `cache_write_cost` fields
  - Verify: `python -c "from lib.llm_client import calculate_cost; r=calculate_cost({'input_tokens':1000,'output_tokens':500,'cache_read_input_tokens':800,'cache_creation_input_tokens':0},'claude-opus-4-6-20260204'); print(r)"`
  - Test req: Write `tests/test_llm_client.py::test_calculate_cost_with_cache_read` (TC-03) - verify cache_read_cost = cache_read_tokens/1M * cached_per_1m; `test_calculate_cost_with_cache_write` - verify cache_write_cost = tokens/1M * input_per_1m * 1.25; `test_calculate_cost_missing_pricing` (TC-04) - pricing_found=false, costs=0.0; `test_calculate_cost_no_cached_per_1m` (EC-04) - cache costs default to 0.0; `test_calculate_cost_missing_cache_fields` (TC-28, EC-09) - default to 0 when fields absent
  - Depends: TK-002
  - Parallel: [P] with TK-004, TK-005
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-004** - Add call_with_cache method to LLMClient
  - IS: IS-03
  - Files: `lib/llm_client.py`
  - Done when: `LLMClient.call_with_cache(bundle, prompt)` exists; `_call_anthropic_with_cache` passes system as array of content blocks with `cache_control: {"type": "ephemeral"}`; text extraction joins ALL text blocks (not just first); raises `ValueError` for non-Anthropic
  - Verify: `python -m pytest tests/test_llm_client.py -k "call_with_cache" -v`
  - Test req: Write `tests/test_llm_client.py::test_call_with_cache_system_prompt_structure` (TC-02) - mock Anthropic, verify system param is array with cache_control block; `test_call_with_cache_non_anthropic_raises` (TC-05) - ValueError for OpenAI model; `test_call_with_cache_joins_text_blocks` - mock response with multiple text blocks, verify all joined; `test_call_with_cache_skips_thinking_blocks` - mock response with thinking+text blocks, verify only text returned; `test_call_with_cache_cache_minimum_warning` (TC-33, EC-11) - log warning when cache_creation_input_tokens==0 on first call
  - Depends: TK-002
  - Parallel: [P] with TK-003, TK-005
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-005** - Add adaptive thinking support for Opus 4.6
  - IS: IS-03 (Opus 4.6 thinking note), DD-18
  - Files: `lib/llm_client.py`
  - Done when: `build_api_params()` detects Opus 4.6 and uses `thinking: {"type": "adaptive"}` + `output_config: {"effort": ...}` instead of deprecated `type: "enabled"` with `budget_tokens`
  - Verify: `python -c "from lib.llm_client import build_api_params; p,m,pr = build_api_params('claude-opus-4-6-20260204','high'); print(p.get('thinking',{}))"`
  - Guardrails: Must not break existing thinking config for non-Opus-4.6 models (claude-sonnet, etc.)
  - Test req: Write `tests/test_llm_client.py::test_build_api_params_opus46_adaptive` - verify `thinking.type == "adaptive"` and `output_config.effort` present; `test_build_api_params_sonnet_manual_thinking` - verify older models still use `type: "enabled"` with `budget_tokens`; `test_build_api_params_unknown_model` (TC-25, EC-02) - ValueError listing known prefixes
  - Depends: TK-002
  - Parallel: [P] with TK-003, TK-004
  - Est: 0.5 HHW

### Phase 2: Run Management Infrastructure

- [ ] **MIPPS-TK-006** - Create lib/run_manager.py
  - IS: IS-05
  - Files: `lib/run_manager.py` (NEW)
  - Done when: `create_run(base_dir, label)` creates run folder with all subdirs (analysis, context, prompts/step, prompts/transform, prompts/eval, verification, output); `snapshot_config(config, run_dir, run_id)` writes `run_config.json`; `generate_run_summary(run_dir, state, costs)` writes `run_summary.md`
  - Test req: Write `tests/test_run_manager.py::test_create_run_folder_structure` (TC-06) - all 8 subdirs exist; `test_create_run_id_collision` (TC-07) - appends `-2` suffix; `test_create_run_missing_runs_dir` (TC-10, EC-05) - creates parent; `test_create_run_read_only_dir` (TC-26, EC-07) - aborts with error; `test_snapshot_config_fields` (TC-08) - run_id, started_at present; `test_generate_run_summary` (TC-09) - compression ratio and cost sections in output
  - Depends: TK-001
  - Parallel: [P] with TK-003, TK-004, TK-005
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-007** - Create lib/cost_tracker.py
  - IS: IS-06
  - Files: `lib/cost_tracker.py` (NEW)
  - Done when: `init_costs()` returns RunCosts schema; `track_call(costs, step, file_path, usage, model, cache_hit)` accumulates totals; `save_costs(costs, run_dir)` writes atomically (.tmp + rename); `load_costs(run_dir)` reads; `check_budget(costs, config)` returns (ok, message) tuple
  - Test req: Write `tests/test_cost_tracker.py::test_track_call_accumulates` (TC-11) - total increases; `test_track_call_per_file` (TC-12) - entry in per_file list; `test_track_call_cache_hit` (TC-13) - cache_hit=true recorded; `test_save_costs_atomic` (TC-14) - file exists, no partial writes; `test_check_budget_warning` (TC-15) - warning at 80% threshold; `test_save_costs_write_failure` (TC-27, EC-08) - logs error, continues; `test_cache_miss_logs_warning` (TC-29, EC-10) - warning with cost delta on non-first call cache miss
  - Depends: TK-003 (uses calculate_cost with cache support)
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-008** - Modify pipeline_state.py for per-run state
  - IS: IS-07
  - Files: `lib/pipeline_state.py`
  - Done when: `load_state(run_dir)` and `save_state(run_dir, state)` accept directory Path (not file path); internally resolve `run_dir / "pipeline_state.json"`
  - Verify: `python -m pytest tests/test_pipeline_state.py -v`
  - Guardrails: No schema changes to state dict; preserve atomic write pattern
  - Test req: Write `tests/test_pipeline_state.py::test_load_save_with_run_dir` - round-trip with temp dir; `test_load_state_missing_file` - returns init state; `test_save_state_creates_file` - file appears in run_dir
  - Depends: none (API signature change only; tests use temp dir)
  - Parallel: [P] with TK-003, TK-004, TK-005, TK-006, TK-007
  - Est: 0.25 HHW

### Phase 3: Module Migration

Migration pattern for all modules:
1. Replace `AnthropicClient`/`OpenAIClient` param types with `LLMClient`
2. Replace `client.call_with_cache(bundle, prompt)` or `client.call(prompt)` calls
3. Add `run_dir: Path` parameter where output paths change
4. Add `costs: dict` parameter where cost tracking needed
5. Update output paths from `BASE_DIR / "_0N_..."` to `run_dir / "subdir/..."`
6. Return usage dict from each API call for cost tracking

- [ ] **MIPPS-TK-009** - Migrate call_with_cache modules (mother_analyzer, compression_prompt_builder, compression_refiner)
  - IS: IS-08, IS-10, IS-13
  - Files: `lib/mother_analyzer.py`, `lib/compression_prompt_builder.py`, `lib/compression_refiner.py`
  - Done when: All 3 modules use `LLMClient.call_with_cache(bundle, prompt)`; output paths use `run_dir` parameter; no imports of `llm_clients`
  - Test req: Write `tests/test_module_migration.py::test_mother_analyzer_uses_llmclient` (TC-16) - mock LLMClient, verify call_with_cache called, output in run_dir/analysis/; `test_compression_prompt_builder_saves_to_run_dir` - prompts saved to run_dir/prompts/; `test_compression_refiner_uses_call_with_cache` - verify call_with_cache, strategy path in run_dir/analysis/
  - Verify: `grep -r "from lib.llm_clients\|import llm_clients" lib/mother_analyzer.py lib/compression_prompt_builder.py lib/compression_refiner.py` returns 0 matches
  - Depends: TK-004 (needs call_with_cache)
  - Parallel: [P] with TK-010
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-010** - Migrate call() modules (mother_output_checker, compression_report_builder)
  - IS: IS-09, IS-12
  - Files: `lib/mother_output_checker.py`, `lib/compression_report_builder.py`
  - Done when: Both modules use `LLMClient.call(prompt)`; compression_report_builder outputs to `run_dir/verification/`; no imports of `llm_clients`
  - Test req: Write `tests/test_module_migration.py::test_mother_output_checker_uses_llmclient` - mock LLMClient, verify call() used (not call_with_cache); `test_compression_report_builder_output_path` (TC-18) - report at run_dir/verification/_04_FILE_COMPRESSION_REPORT.md
  - Verify: `grep -r "from lib.llm_clients\|import llm_clients" lib/mother_output_checker.py lib/compression_report_builder.py` returns 0 matches
  - Depends: TK-002 (needs working LLMClient)
  - Parallel: [P] with TK-009
  - Est: 0.25 HHW

- [ ] **MIPPS-TK-011** - Migrate file_compressor.py (both clients + cost tracking)
  - IS: IS-11
  - Files: `lib/file_compressor.py`
  - Done when: Uses `mother: LLMClient` with `call_with_cache()` for compression; uses `verifier: LLMClient` with `call()` for verification; calls `cost_tracker.track_call()` after each API call; outputs to `run_dir / "output"`; copies non-.md files to output
  - Test req: Write `tests/test_module_migration.py::test_file_compressor_tracks_costs` (TC-17) - mock both clients, verify per_file entries in run_costs; `test_file_compressor_output_to_run_dir` - compressed files at run_dir/output/
  - Depends: TK-004 (call_with_cache), TK-007 (cost_tracker)
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-012** - Delete V1 files and verify no stale imports
  - IS: IS-14
  - Files: `lib/llm_clients.py` (DELETE), `lib/api_cost_tracker.py` (DELETE)
  - Done when: Both files deleted; zero grep matches for old imports across all .py files
  - Verify: `grep -r "from lib.llm_clients\|from lib.api_cost_tracker\|import llm_clients\|import api_cost_tracker" lib/ mipps_pipeline.py` returns 0 matches
  - Test req: Write `tests/test_module_migration.py::test_no_v1_imports` (TC-19) - scan all .py files for old import patterns
  - Depends: TK-009, TK-010, TK-011 (all migrations complete)
  - Est: 0.25 HHW

### Phase 4: Pipeline Integration and Tools

- [ ] **MIPPS-TK-013** - Modify mipps_pipeline.py for run management
  - IS: IS-15
  - Files: `mipps_pipeline.py`
  - Done when: `--run-label` and `--run-id` global args added; `cmd_bundle` creates run folder via `create_run()` and snapshots config; subsequent commands use `--run-id` or auto-detect latest run; all `AnthropicClient`/`OpenAIClient` replaced with `LLMClient`; all output paths use `run_dir`
  - Test req: Write `tests/test_pipeline_cli.py::test_bundle_creates_run_folder` (TC-20) - verify run folder created with label; `test_config_snapshot_before_api` (TC-22) - run_config.json exists before first API call; `test_status_reads_from_run` (TC-21) - status command reads run-specific state; `test_auto_detect_latest_run` - when no --run-id, finds most recent run
  - Guardrails: Pipeline step logic (1-7) must not change; only infrastructure around it changes
  - Depends: TK-006, TK-007, TK-008, TK-012
  - Note: Critical path bottleneck - all Phase 1-3 tasks must complete before this task
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-014** - Add run summary generation to verify command
  - IS: IS-16
  - Files: `mipps_pipeline.py`
  - Done when: `cmd_verify()` calls `generate_run_summary(run_dir, state, costs)` after report generation; summary file contains compression ratio, cost breakdown, cache efficiency
  - Test req: Write `tests/test_pipeline_cli.py::test_verify_generates_summary` (TC-23) - run_summary.md exists in run folder after verify
  - Depends: TK-013
  - Est: 0.25 HHW

- [ ] **MIPPS-TK-015** - Create compare_runs.py
  - IS: IS-17
  - Files: `compare_runs.py` (NEW)
  - Done when: CLI `compare_runs.py --runs <id1> <id2>` loads pipeline_state.json + run_costs.json from each run; outputs diff table; identifies regressions
  - Test req: Write `tests/test_compare_runs.py::test_compare_two_runs` (TC-30) - mock run data, verify diff output; `test_compare_nonexistent_run` (TC-31) - clear error; `test_compare_identifies_regression` (TC-32) - files with worse scores listed
  - Depends: TK-006 (run folder structure)
  - Parallel: [P] with TK-013
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-016** - Create generate_report.py (optional)
  - IS: IS-18
  - Files: `generate_report.py` (NEW)
  - Done when: CLI `generate_report.py --run <id>` generates HTML dashboard from run data
  - Test req: Write `tests/test_generate_report.py::test_html_report_generated` - verify HTML file created with cost and compression sections
  - Depends: TK-006
  - Parallel: [P] with TK-015
  - Est: 0.25 HHW

## Task N - Final Verification (MANDATORY)

Run after all tasks complete:
- [ ] Run full test suite: `python -m pytest tests/ -v` - all 33 TCs pass (per MIPPS-IP02 VC-24)
- [ ] Compare test results to Task 0 baseline - no regressions
- [ ] Verify run folder isolation: `bundle --run-label test` creates `runs/YYYYMMDD-HHMM-test/` with all subdirs
- [ ] Verify `run_costs.json` written after API call mock
- [ ] Verify `run_summary.md` generated with correct sections
- [ ] Verify no remaining imports of `llm_clients` or `api_cost_tracker`
- [ ] Run `/verify` workflow against MIPPS-SP02 and MIPPS-IP02
- [ ] Update PROGRESS.md - mark complete

## Test File Structure

```
tests/
├── __init__.py
├── conftest.py                  (shared fixtures: mock clients, temp dirs, sample configs)
├── test_config.py               (TK-001, TK-002: config schema, loading, pricing tier)
├── test_llm_client.py          (TK-003, TK-004, TK-005: cost calc, call_with_cache, adaptive thinking)
├── test_run_manager.py          (TK-006: folder creation, config snapshot, summary)
├── test_cost_tracker.py         (TK-007: tracking, atomic save, budget check)
├── test_pipeline_state.py       (TK-008: per-run state load/save)
├── test_module_migration.py     (TK-009 to TK-012: LLMClient usage, output paths, no V1 imports)
├── test_pipeline_cli.py         (TK-013, TK-014: CLI args, run creation, summary)
├── test_compare_runs.py         (TK-015: run comparison)
└── test_generate_report.py      (TK-016: HTML report)
```

## TC Coverage Map

- TC-01: TK-002 (config loading)
- TC-02: TK-004 (call_with_cache structure)
- TC-03: TK-003 (cache cost calc)
- TC-04: TK-003 (missing pricing)
- TC-05: TK-004 (non-Anthropic raises)
- TC-06: TK-006 (folder structure)
- TC-07: TK-006 (ID collision)
- TC-08: TK-006 (config snapshot)
- TC-09: TK-006 (run summary)
- TC-10: TK-006 (missing runs/ dir)
- TC-11: TK-007 (accumulates total)
- TC-12: TK-007 (per-file cost)
- TC-13: TK-007 (cache hit status)
- TC-14: TK-007 (atomic save)
- TC-15: TK-007 (budget warning)
- TC-16: TK-009 (mother_analyzer)
- TC-17: TK-011 (file_compressor costs)
- TC-18: TK-010 (report output path)
- TC-19: TK-012 (no V1 imports)
- TC-20: TK-013 (bundle creates run)
- TC-21: TK-013 (status from run)
- TC-22: TK-013 (config before API)
- TC-23: TK-014 (verify generates summary)
- TC-24: TK-002 (missing configs/ dir)
- TC-25: TK-005 (unknown model)
- TC-26: TK-006 (creation fails)
- TC-27: TK-007 (save failure)
- TC-28: TK-003 (missing cache fields)
- TC-29: TK-007 (cache miss warning)
- TC-30: TK-015 (compare 2 runs)
- TC-31: TK-015 (nonexistent run)
- TC-32: TK-015 (regression detection)
- TC-33: TK-004 (cache minimum prefix)

## Dependency Graph

```
Phase 1 (foundation):
TK-001 ─> TK-002 ─┬─> TK-003 [P]
                   ├─> TK-004 [P]
                   └─> TK-005 [P]

Phase 2 (infrastructure, parallel with Phase 1 after TK-001):
TK-001 ────────> TK-006 [P]
TK-003 ────────> TK-007
TK-008 [P] (no dependencies)

Phase 3 (migration):
TK-004 ──────────> TK-009 [P]
TK-002 ──────────> TK-010 [P]
TK-004 + TK-007 ─> TK-011
TK-009 + TK-010 + TK-011 ─> TK-012

Phase 4 (integration):
TK-006 + TK-007 + TK-008 + TK-012 ─> TK-013 ─> TK-014
TK-006 ─> TK-015 [P]
TK-006 ─> TK-016 [P]
```

## Document History

**[2026-03-20 15:25]**
- Fixed: LLM expanded on first use in Goal (AP-PR-06)
- Fixed: TK-008 dependency removed (was TK-006, now none - API signature change needs only temp dir)
- Fixed: TK-009 missing [P] marker added (parallel with TK-010)
- Fixed: TK-004 and TK-008 Verify fields changed from vague text to runnable pytest commands
- Fixed: Dependency graph restructured by phase for clarity; TK-005 and TK-008 now visible
- Fixed: Test file renamed `test_llm_client_cache.py` to `test_llm_client.py` (covers non-cache changes too)
- Added: conftest.py fixture list (6 fixtures: tmp_run_dir, mock clients, sample data)
- Added: TK-013 note about critical path bottleneck

**[2026-03-20 15:20]**
- Initial tasks plan created from `_IMPL_IPPS_MINIFICATION_MOTHER_MODEL_CHANGES.md [MIPPS-IP02]`
- 16 tasks across 4 phases, PARTITION-DEPENDENCY strategy
- Each task includes test requirements mapping to 33 TCs from MIPPS-IP02
- Test file structure defined for incremental verification
- Full TC coverage map and dependency graph included
