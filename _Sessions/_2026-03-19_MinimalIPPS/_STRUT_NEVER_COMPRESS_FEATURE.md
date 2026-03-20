# STRUT: Implement never_compress Feature

**Doc ID**: MIPPS-STRUT-01
**Goal**: Add `never_compress` config to copy specialized files as-is without compression
**Target files**: `lib/file_bundle_builder.py`, `lib/mother_analyzer.py`, `lib/file_compressor.py`, `mipps_pipeline.py`, `tests/*.py`

## Dependency Analysis

**Files that need changes:**
- `lib/file_bundle_builder.py` - Add `is_never_compress()` helper
- `lib/mother_analyzer.py` - Add `get_never_compress_files()` helper
- `lib/file_compressor.py` - Modify `run_compression_step()` to handle never_compress
- `mipps_pipeline.py` - Pass never_compress through pipeline commands
- `tests/conftest.py` - Update fixtures with never_compress config
- `tests/test_file_bundle_builder.py` - Add tests for is_never_compress
- `tests/test_mother_analyzer.py` - Add tests for get_never_compress_files
- `tests/test_file_compressor.py` - Add test for never_compress copy behavior
- `tests/test_integration.py` - Add integration test for never_compress flow

**Regression Risks:**
- `scan_source_dir()` - signature unchanged, safe
- `identify_excluded_files()` - must still work for files NOT in never_compress
- `run_compression_step()` - must still compress non-excluded, non-never_compress files
- State tracking - `files_excluded_md` count must include never_compress files

**Zero Regression Strategy:**
1. Run all 57 existing tests BEFORE any code changes (baseline)
2. Add new tests FIRST (TDD approach)
3. Implement feature to make new tests pass
4. Run ALL tests (57 old + new) to verify zero regression
5. Integration test validates end-to-end flow

## Plan

[x] P1 [PREPARE]: Establish baseline and add test infrastructure
├─ Objectives:
│   ├─ [x] All 57 existing tests pass ← P1-D1
│   └─ [x] Test fixtures updated for never_compress ← P1-D2
├─ Strategy: Run existing tests, update conftest.py with never_compress fixtures
├─ [x] P1-S1 [RUN](pytest tests/ -v) - verify all 57 tests pass
├─ [x] P1-S2 [UPDATE](tests/conftest.py) - add never_compress to sample_config fixture
├─ [x] P1-S3 [UPDATE](tests/conftest.py) - add mock_source_dir_with_prompts fixture
├─ Deliverables:
│   ├─ [x] P1-D1: 57/57 tests pass (baseline)
│   └─ [x] P1-D2: conftest.py updated with never_compress fixtures
└─> Transitions:
    - P1-D1, P1-D2 checked → P2 [IMPLEMENT-BUNDLE]
    - Tests fail → [CONSULT]

[x] P2 [IMPLEMENT-BUNDLE]: Add is_never_compress to file_bundle_builder
├─ Objectives:
│   └─ [x] is_never_compress function works ← P2-D1, P2-D2
├─ Strategy: TDD - write test first, then implement
├─ [x] P2-S1 [WRITE](test_file_bundle_builder.py) - test_is_never_compress_matches_pattern
├─ [x] P2-S2 [WRITE](test_file_bundle_builder.py) - test_is_never_compress_no_match
├─ [x] P2-S3 [IMPLEMENT](lib/file_bundle_builder.py) - add is_never_compress() function
├─ [x] P2-S4 [RUN](pytest tests/test_file_bundle_builder.py -v) - verify new tests pass
├─ Deliverables:
│   ├─ [x] P2-D1: is_never_compress() implemented
│   └─ [x] P2-D2: 2 new tests pass
└─> Transitions:
    - P2-D1, P2-D2 checked → P3 [IMPLEMENT-ANALYZER]

[x] P3 [IMPLEMENT-ANALYZER]: Add get_never_compress_files to mother_analyzer
├─ Objectives:
│   └─ [x] get_never_compress_files returns matching file paths ← P3-D1
├─ Strategy: TDD - write test, implement helper function
├─ [x] P3-S1 [WRITE](test_mother_analyzer.py) - test_get_never_compress_files
├─ [x] P3-S2 [IMPLEMENT](lib/mother_analyzer.py) - add get_never_compress_files()
├─ [x] P3-S3 [RUN](pytest tests/test_mother_analyzer.py -v) - verify test passes
├─ Deliverables:
│   └─ [x] P3-D1: get_never_compress_files() implemented and tested
└─> Transitions:
    - P3-D1 checked → P4 [IMPLEMENT-COMPRESSOR]

[x] P4 [IMPLEMENT-COMPRESSOR]: Update file_compressor to copy never_compress files as-is
├─ Objectives:
│   ├─ [x] never_compress files copied without compression ← P4-D1
│   ├─ [x] Mother not called for never_compress files ← P4-D2
│   └─ [x] Evaluation order: skip → never_compress → exclusion → compress ← P4-D3
├─ Strategy: TDD - write tests, modify run_compression_step, verify order
├─ [x] P4-S1 [WRITE](test_file_compressor.py) - test_never_compress_copied_as_is
├─ [x] P4-S2 [WRITE](test_file_compressor.py) - test_never_compress_not_sent_to_mother
├─ [x] P4-S3 [WRITE](test_file_compressor.py) - test_never_compress_before_exclusion_criteria
├─ [x] P4-S4 [UPDATE](lib/file_compressor.py) - handle never_compress in run_compression_step
├─ [x] P4-S5 [RUN](pytest tests/test_file_compressor.py -v) - verify tests pass
├─ Deliverables:
│   ├─ [x] P4-D1: never_compress files copied to output unchanged
│   ├─ [x] P4-D2: Mother API not called for never_compress files
│   └─ [x] P4-D3: Evaluation order enforced (3 new tests pass)
└─> Transitions:
    - P4-D1, P4-D2, P4-D3 checked → P5 [IMPLEMENT-CLI]

[x] P5 [IMPLEMENT-CLI]: Update mipps_pipeline.py to pass never_compress through pipeline
├─ Objectives:
│   └─ [x] CLI passes never_compress config to all relevant functions ← P5-D1
├─ Strategy: Update cmd_analyze and cmd_compress to handle never_compress
├─ [x] P5-S1 [UPDATE](mipps_pipeline.py) - cmd_analyze passes never_compress to state
├─ [x] P5-S2 [UPDATE](mipps_pipeline.py) - cmd_compress reads never_compress from config
├─ [x] P5-S3 [UPDATE](mipps_pipeline.py) - _load_config default includes never_compress
├─ Deliverables:
│   └─ [x] P5-D1: CLI handles never_compress config
└─> Transitions:
    - P5-D1 checked → P6 [INTEGRATION]

[x] P6 [INTEGRATION]: Integration test and full regression check
├─ Objectives:
│   ├─ [x] Integration test validates end-to-end never_compress flow ← P6-D1
│   ├─ [x] All 57 original tests still pass (zero regression) ← P6-D2
│   └─ [x] All new tests pass ← P6-D3
├─ Strategy: Write integration test, run full test suite
├─ [x] P6-S1 [WRITE](test_integration.py) - test_never_compress_files_copied_not_compressed
├─ [x] P6-S2 [RUN](pytest tests/ -v) - run ALL tests
├─ [x] P6-S3 [VERIFY] - count tests: 57 original + 7 new = 64 total
├─ Deliverables:
│   ├─ [x] P6-D1: Integration test passes
│   ├─ [x] P6-D2: 57 original tests pass (zero regression)
│   └─ [x] P6-D3: 7 new tests pass
└─> Transitions:
    - P6-D1, P6-D2, P6-D3 checked → [END]
    - Any regression → P6-S2 (fix and retest)

## Test Summary

**New tests to add (8 total):**
1. `test_is_never_compress_matches_pattern` - glob pattern matching works
2. `test_is_never_compress_no_match` - non-matching paths return False
3. `test_get_never_compress_files` - returns files matching patterns
4. `test_never_compress_copied_as_is` - file content preserved in output
5. `test_never_compress_not_sent_to_mother` - Mother API call count = 0 for these files
6. `test_never_compress_before_exclusion_criteria` - evaluation order enforced
7. `test_never_compress_files_copied_not_compressed` (integration)
8. Update `test_full_pipeline_run` - add never_compress file to integration env

**Regression guarantee:**
- All 57 existing tests must pass after implementation
- New tests are additive, not modifications of existing tests
- Integration test validates full pipeline with never_compress

## Document History

**[2026-03-20 10:04]**
- Initial STRUT plan created for never_compress feature

**[2026-03-20 10:10]**
- Fixed: P3 simplified (evaluation order belongs in P4, not analyzer)
- Fixed: P4 expanded with evaluation order test and 3 deliverables
- Fixed: Test count corrected to 8 (added evaluation order test)

**[2026-03-20 10:20]**
- All phases completed: 64/64 tests pass (57 original + 7 new)
- Test #8 (update test_full_pipeline_run) skipped to avoid modifying existing tests
