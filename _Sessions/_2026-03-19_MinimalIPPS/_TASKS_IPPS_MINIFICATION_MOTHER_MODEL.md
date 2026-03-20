# TASKS: MinimalIPPS Compression Pipeline Tasks Plan

**Doc ID (TDID)**: MIPPS-TK01
**Feature**: MIPPS-PIPELINE
**Goal**: Partitioned tasks for MinimalIPPS pipeline implementation with interleaved test tasks
**Source**: `_IMPL_IPPS_MINIFICATION_MOTHER_MODEL.md [MIPPS-IP01]`, `_SPEC_IPPS_MINIFICATION_MOTHER_MODEL.md [MIPPS-SP01]`
**Strategy**: PARTITION-DEPENDENCY

## Task Overview

- Total tasks: 26
- Estimated total: 14.5 HHW
- Parallelizable: 10 tasks (marked [P])

## Task 0 - Baseline (MANDATORY)

Run before starting any implementation:
- [ ] Run existing tests, record pass/fail baseline
- [ ] Note pre-existing failures (not caused by this feature)
- [ ] Verify Python 3.11+ available
- [ ] Verify `anthropic`, `openai`, `tiktoken` packages installed
- [ ] Verify `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` env vars set

## Tasks

### Phase 1: Project Setup

- [ ] **MIPPS-TK-001** - Create project skeleton and configuration
  - Files: `mipps_pipeline.py` (stub), `lib/__init__.py`, `pipeline_config.json`, `tests/__init__.py`, `tests/conftest.py`
  - Done when: Directory structure exists, `pipeline_config.json` matches SPEC section 9, `conftest.py` has shared fixtures (tmp dirs, sample config, mock API responses)
  - Verify: `python -c "import json; json.load(open('pipeline_config.json'))"`
  - Guardrails: Config must match SPEC section 9 exactly
  - Source: IS-01, IS-02
  - Est: 0.5 HHW

### Phase 2: Core Modules (No API Dependency)

- [ ] **MIPPS-TK-002** - Implement lib/pipeline_state.py
  - Files: `lib/pipeline_state.py`
  - Done when: `load_state`, `save_state`, `init_state`, `update_step`, `add_completed_file`, `update_cost` all implemented. Atomic write via tmp+rename. Handles corrupted JSON (EC-08)
  - Verify: `python -c "from lib.pipeline_state import init_state; print(init_state())"`
  - Guardrails: Never write state without atomic pattern
  - Depends: TK-001
  - Parallel: [P] with TK-004
  - Source: IS-03
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-003** - Write tests for pipeline_state.py
  - Files: `tests/test_pipeline_state.py`
  - Done when: 4 tests pass (TC-06 to TC-09): load valid state, load corrupted state with backup, update step, add completed file
  - Verify: `python -m pytest tests/test_pipeline_state.py -v`
  - Depends: TK-002
  - Parallel: [P] with TK-005
  - Source: TC-06, TC-07, TC-08, TC-09
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-004** - Implement lib/api_cost_tracker.py
  - Files: `lib/api_cost_tracker.py`
  - Done when: `PRICING` dict matches NOTES.md rates, `calculate_cost` handles both providers (cache_read/write for Anthropic, standard for OpenAI), `check_budget` returns warning at 80% and halt at 100%
  - Verify: `python -c "from lib.api_cost_tracker import calculate_cost; print(calculate_cost('gpt-5-mini', 1000, 100))"`
  - Guardrails: Pricing rates must match NOTES.md Anthropic Pricing Reference
  - Depends: TK-001
  - Parallel: [P] with TK-002
  - Source: IS-04
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-005** - Write tests for api_cost_tracker.py
  - Files: `tests/test_api_cost_tracker.py`
  - Done when: Tests pass for: calculate_cost with Anthropic (input, cached_read, cached_write, output), calculate_cost with OpenAI, check_budget warning at 80%, check_budget halt at 100%, unknown model raises error
  - Verify: `python -m pytest tests/test_api_cost_tracker.py -v`
  - Depends: TK-004
  - Parallel: [P] with TK-003
  - Source: IS-04
  - Est: 0.5 HHW

### Phase 3: API Clients

- [ ] **MIPPS-TK-006** - Implement lib/llm_clients.py
  - Files: `lib/llm_clients.py`
  - Done when: `AnthropicClient` with `call_with_cache(bundle, prompt, ttl)` and `OpenAIClient` with `call(prompt, max_tokens)` implemented. Custom retry with exponential backoff + jitter. `max_retries=0` on SDK constructors. Logs `response._request_id` for OpenAI. Maps provider-specific usage fields to cost_tracker parameters
  - Verify: `python -c "from lib.llm_clients import AnthropicClient, OpenAIClient; print('imports ok')"`
  - Guardrails: Set `max_retries=0` on both SDKs to avoid double-retry. Distinguish retryable (429, 5xx) from non-retryable (4xx) OpenAI errors
  - Depends: TK-004
  - Source: IS-05, EC-09, EC-10, EC-11
  - Est: 0.75 HHW

- [ ] **MIPPS-TK-007** - Write tests for llm_clients.py (mocked)
  - Files: `tests/test_llm_clients.py`
  - Done when: 5 tests pass (TC-10 to TC-14): Anthropic cache hit, Anthropic timeout retry, Anthropic rate limit, OpenAI success, API failure after 3 retries. All tests use mocked SDK responses (no real API calls)
  - Verify: `python -m pytest tests/test_llm_clients.py -v`
  - Guardrails: Must not make real API calls in tests
  - Depends: TK-006
  - Source: TC-10, TC-11, TC-12, TC-13, TC-14
  - Est: 0.75 HHW

### Phase 4: Bundle and File Scanning

- [ ] **MIPPS-TK-008** - Implement lib/file_bundle_builder.py
  - Files: `lib/file_bundle_builder.py`
  - Done when: `scan_source_dir` categorizes files per FileInventory, `generate_bundle` concatenates with `## [path]` headers and metadata, `count_tokens` uses tiktoken. Handles EC-01 (empty dir), EC-03 (binary files). Applies `include_patterns` and `skip_patterns`
  - Verify: `python -c "from lib.file_bundle_builder import scan_source_dir; print('imports ok')"`
  - Guardrails: Only .md files in compressible output. Never modify source directory
  - Depends: TK-001
  - Parallel: [P] with TK-006
  - Source: IS-06, EC-01, EC-03
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-009** - Write tests for file_bundle_builder.py
  - Files: `tests/test_file_bundle_builder.py`
  - Done when: 5 tests pass (TC-01 to TC-05): scan mixed files, scan empty dir, skip *.py files, generate bundle with headers, token count within 10% of tiktoken. Tests use tmp_path fixture with sample directory structure
  - Verify: `python -m pytest tests/test_file_bundle_builder.py -v`
  - Depends: TK-008
  - Parallel: [P] with TK-007
  - Source: TC-01, TC-02, TC-03, TC-04, TC-05
  - Est: 0.5 HHW

### Phase 5: Mother Analysis

- [ ] **MIPPS-TK-010** - Create analysis step prompts (Steps 2-4)
  - Files: `prompts/step/s2_call_tree.md`, `prompts/step/s3_complexity_map.md`, `prompts/step/s4_compression_strategy.md`
  - Done when: 3 prompt files exist, each references corresponding SPEC FR (FR-02, FR-03, FR-04), specifies expected output format, includes exclusion criteria instructions
  - Verify: `python -c "import pathlib; assert all((pathlib.Path('prompts/step') / f).exists() for f in ['s2_call_tree.md', 's3_complexity_map.md', 's4_compression_strategy.md'])"`
  - Parallel: [P] with TK-006, TK-008
  - Source: IS-10 (partial)
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-011** - Implement mother_analyzer.py - Step 2 (call tree)
  - Files: `lib/mother_analyzer.py`
  - Done when: `analyze_call_tree` calls AnthropicClient with cached bundle, writes `_01_FILE_CALL_TREE.md`. `parse_load_frequencies` extracts per-file reference counts from call tree output
  - Verify: `python -c "from lib.mother_analyzer import analyze_call_tree, parse_load_frequencies; print('imports ok')"`
  - Depends: TK-006, TK-010
  - Parallel: [P] with TK-013
  - Source: IS-07
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-012** - Implement mother_analyzer.py - Steps 3-4 (complexity + strategy)
  - Files: `lib/mother_analyzer.py` (extend)
  - Done when: `analyze_complexity` writes `_02_FILE_COMPLEXITY_MAP.md`, `identify_excluded_files` applies exclusion criteria (< 100 lines AND <= 2 refs), `generate_strategy` writes `_03_FILE_COMPRESSION_STRATEGY.md` with Primary/Secondary/Drop lists excluding flagged files
  - Verify: `python -c "from lib.mother_analyzer import analyze_complexity, identify_excluded_files, generate_strategy; print('imports ok')"`
  - Depends: TK-011
  - Source: IS-08, IS-09
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-013** - Implement mother_output_checker.py
  - Files: `lib/mother_output_checker.py`
  - Done when: `spot_check_document` picks 10-20 random files, uses OpenAIClient to verify claims against source, `report_issues` formats findings. Per FR-11
  - Verify: `python -c "from lib.mother_output_checker import spot_check_document, report_issues; print('imports ok')"`
  - Depends: TK-006
  - Parallel: [P] with TK-011
  - Source: IS-13
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-014** - Write tests for mother_analyzer.py and mother_output_checker.py
  - Files: `tests/test_mother_analyzer.py`, `tests/test_mother_output_checker.py`
  - Done when: Tests pass with mocked LLM responses: call tree produces output file, parse_load_frequencies returns dict, identify_excluded_files filters correctly, spot_check_document samples correct count, report_issues formats output
  - Verify: `python -m pytest tests/test_mother_analyzer.py tests/test_mother_output_checker.py -v`
  - Guardrails: Must not make real API calls
  - Depends: TK-012, TK-013
  - Source: IS-07, IS-08, IS-09, IS-13
  - Est: 0.75 HHW

### Phase 6: Compression Pipeline

- [ ] **MIPPS-TK-015** - Create compression and evaluation step prompts (Steps 5-7)
  - Files: `prompts/step/s5_generate_prompts.md`, `prompts/step/s6_compress_file.md`, `prompts/step/s7_verify_file.md`
  - Done when: 3 prompt files exist, s5 references file_type_map and strategy, s6 includes compression instructions with Primary/Secondary/Drop awareness, s7 specifies 5-line report format per FR-07
  - Verify: `python -c "import pathlib; assert all((pathlib.Path('prompts/step') / f).exists() for f in ['s5_generate_prompts.md', 's6_compress_file.md', 's7_verify_file.md'])"`
  - Parallel: [P] with TK-011 through TK-013
  - Source: IS-10 (partial)
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-016** - Implement compression_prompt_builder.py
  - Files: `lib/compression_prompt_builder.py`
  - Done when: `generate_compression_prompts` calls Mother with strategy and file_type_map, produces one prompt per type + compress_other fallback. `save_prompts` writes to `prompts/transform/*.md` and `prompts/eval/*.md`
  - Verify: `python -c "from lib.compression_prompt_builder import generate_compression_prompts, save_prompts; print('imports ok')"`
  - Depends: TK-006
  - Source: IS-11
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-017** - Write tests for compression_prompt_builder.py
  - Files: `tests/test_compression_prompt_builder.py`
  - Done when: Tests pass with mocked LLM: generates prompts for each file type, saves to correct directories, includes compress_other fallback
  - Verify: `python -m pytest tests/test_compression_prompt_builder.py -v`
  - Depends: TK-016
  - Source: IS-11
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-018** - Implement file_compressor.py
  - Files: `lib/file_compressor.py`
  - Done when: `compress_file` sends file + prompt + strategy to Mother, judges with OpenAI (score 1-5), refines once if < 3.5, flags for manual review if still < 3.5. `run_compression_step` loops all non-excluded files, tracks files_completed for resume, copies excluded .md files as-is. Handles EC-06 (resume cleanup), EC-13 (truncated output), EC-14 (invalid score), EC-16 (token increase). Logs "Compressing file N/M: [path]"
  - Verify: `python -c "from lib.file_compressor import compress_file, run_compression_step; print('imports ok')"`
  - Guardrails: Never modify source files. Track per-file completion for resume
  - Depends: TK-006, TK-016
  - Source: IS-12, EC-06, EC-13, EC-14, EC-16
  - Est: 0.75 HHW

- [ ] **MIPPS-TK-019** - Write tests for file_compressor.py
  - Files: `tests/test_file_compressor.py`
  - Done when: 6 tests pass (TC-15 to TC-20): score >= 3.5 accepts, score < 3.5 refine succeeds, refine fails -> manual review, resume skips completed, token increase flagged, budget exceeded halts
  - Verify: `python -m pytest tests/test_file_compressor.py -v`
  - Guardrails: Must not make real API calls
  - Depends: TK-018
  - Source: TC-15, TC-16, TC-17, TC-18, TC-19, TC-20
  - Est: 0.75 HHW

### Phase 7: Verification and Iteration

- [ ] **MIPPS-TK-020** - Implement compression_report_builder.py
  - Files: `lib/compression_report_builder.py`
  - Done when: `verify_file` produces exactly 5 lines per file (structural, removed, simplified, sacrificed, impact). `check_cross_references` scans all compressed + excluded files for broken refs (EC-15). `generate_report` writes `_04_FILE_COMPRESSION_REPORT.md` with summary (pass rate, compression ratio, broken refs)
  - Verify: `python -c "from lib.compression_report_builder import verify_file, check_cross_references, generate_report; print('imports ok')"`
  - Depends: TK-006
  - Source: IS-14, EC-15
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-021** - Write tests for compression_report_builder.py
  - Files: `tests/test_compression_report_builder.py`
  - Done when: 4 tests pass (TC-21 to TC-24): 5-line report format, broken ref detected, all refs resolve, summary with pass rate
  - Verify: `python -m pytest tests/test_compression_report_builder.py -v`
  - Depends: TK-020
  - Source: TC-21, TC-22, TC-23, TC-24
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-022** - Implement compression_refiner.py
  - Files: `lib/compression_refiner.py`
  - Done when: `review_report` sends report to Mother with cached context, `update_strategy` modifies strategy based on findings, `get_files_to_recompress` parses report for flagged files. Handles EC-07 (no report)
  - Verify: `python -c "from lib.compression_refiner import review_report, update_strategy, get_files_to_recompress; print('imports ok')"`
  - Depends: TK-006
  - Source: IS-15, EC-07
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-023** - Write tests for compression_refiner.py
  - Files: `tests/test_compression_refiner.py`
  - Done when: Tests pass with mocked LLM: review produces updates, strategy file updated, files_to_recompress parsed correctly, missing report raises error
  - Verify: `python -m pytest tests/test_compression_refiner.py -v`
  - Depends: TK-022
  - Source: IS-15
  - Est: 0.5 HHW

### Phase 8: CLI and Integration

- [ ] **MIPPS-TK-024** - Implement mipps_pipeline.py CLI
  - Files: `mipps_pipeline.py`
  - Done when: 8 subcommands work (bundle, analyze, check, generate, compress, verify, iterate, status). Handles EC-04 (missing config), EC-05 (resume prerequisites). Each command loads config, state, calls appropriate module, updates state
  - Verify: `python mipps_pipeline.py --help`
  - Depends: TK-002, TK-004, TK-006, TK-008, TK-012, TK-013, TK-016, TK-018, TK-020, TK-022
  - Source: IS-16, EC-04, EC-05
  - Est: 0.75 HHW

- [ ] **MIPPS-TK-025** - Write tests for CLI
  - Files: `tests/test_cli.py`
  - Done when: 4 tests pass (TC-25 to TC-28): bundle creates output, status displays progress, compress without bundle fails, iterate without report fails
  - Verify: `python -m pytest tests/test_cli.py -v`
  - Depends: TK-024
  - Source: TC-25, TC-26, TC-27, TC-28
  - Est: 0.5 HHW

- [ ] **MIPPS-TK-026** - Integration test - end-to-end with mocked APIs
  - Files: `tests/test_integration.py`
  - Done when: Full pipeline run (bundle -> analyze -> check -> generate -> compress -> verify) completes with mocked API responses. State tracks all steps. Output directory contains compressed files. Cost stays within budget
  - Verify: `python -m pytest tests/test_integration.py -v --timeout=60`
  - Guardrails: Must not make real API calls. Must not modify any files outside test tmp dirs
  - Depends: TK-024, TK-025
  - Source: VC-27, VC-28
  - Est: 1.0 HHW

## Task N - Final Verification (MANDATORY)

Run after all tasks complete:
- [ ] Compare test results to Task 0 baseline
- [ ] New failures = regressions (must fix)
- [ ] All 28 IMPL test cases covered (TC-01 through TC-28)
- [ ] Run `python -m pytest tests/ -v` - all pass
- [ ] Run `/verify` workflow against SPEC and IMPL
- [ ] Verify: compression ratio >= 40% (VC-29)
- [ ] Verify: manual review queue <= 5 files (VC-30)
- [ ] Verify: all cross-file references resolve (VC-31)
- [ ] Verify: total cost within budget (VC-32)
- [ ] Update PROGRESS.md - mark complete

## Dependency Graph

```
TK-001 ─> TK-002 ─> TK-003
  │          └───────────────────────────────> TK-024
  ├─> TK-004 ─> TK-005
  │     └─> TK-006 ─> TK-007
  │           ├───────────────────────────────> TK-024
  │           ├─> TK-011 ─> TK-012 ─> TK-014
  │           │     └────────────────────────> TK-024
  │           ├─> TK-013 ───────────> TK-014
  │           │     └────────────────────────> TK-024
  │           ├─> TK-016 ─> TK-017
  │           │     └─> TK-018 ─> TK-019
  │           │           └──────────────────> TK-024
  │           ├─> TK-020 ─> TK-021
  │           │     └────────────────────────> TK-024
  │           └─> TK-022 ─> TK-023
  │                 └────────────────────────> TK-024
  ├─> TK-008 ─> TK-009
  │     └────────────────────────────────────> TK-024
  ├─> TK-010 ─> TK-011
  └─> TK-015 ─> TK-016

TK-024 ─> TK-025 ─> TK-026
```

**Parallel groups:**
- Group A: TK-002, TK-004 (core modules, no cross-dependency)
- Group B: TK-003, TK-005 (tests for core modules)
- Group C: TK-006, TK-008, TK-010, TK-015 (after their deps, independent of each other)
- Group D: TK-011, TK-013 (both need TK-006, independent of each other)
- Group E: TK-016, TK-020, TK-022 (all need TK-006, independent of each other)

## Document History

**[2026-03-20 04:20]**
- Fixed: TK-024 Depends missing TK-004 (api_cost_tracker) and TK-006 (llm_clients)
- Fixed: Dependency graph showed test tasks feeding into TK-024 instead of impl tasks
- Fixed: Dependency graph TK-010/TK-015 now connected to TK-001

**[2026-03-20 04:15]**
- Initial tasks plan created from MIPPS-IP01 and MIPPS-SP01
- 26 implementation + test tasks across 8 phases
- Interleaved test tasks after each module implementation
- All 28 IMPL test cases (TC-01 to TC-28) mapped to specific tasks
