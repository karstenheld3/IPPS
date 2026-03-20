# TEST: MinimalIPPS Compression Pipeline

**Doc ID (TDID)**: MIPPS-TP01
**Feature**: MIPPS-PIPELINE
**Goal**: Verify all MinimalIPPS pipeline modules against SPEC requirements using mocked APIs
**Timeline**: Created 2026-03-20, Updated 3 times
**Target file**: `tests/` directory (11 test files)

**Depends on:**
- `_SPEC_IPPS_MINIFICATION_MOTHER_MODEL.md [MIPPS-SP01]` for requirements
- `_IMPL_IPPS_MINIFICATION_MOTHER_MODEL.md [MIPPS-IP01]` for implementation details and 28 baseline TCs
- `_TASKS_IPPS_MINIFICATION_MOTHER_MODEL.md [MIPPS-TK01]` for task-level test grouping

## MUST-NOT-FORGET

- All tests use mocked API responses - no real Anthropic or OpenAI calls
- All file operations use pytest `tmp_path` fixture - never write to real directories
- IMPL defines 28 Test Cases (TCs) (MIPPS-IP01-TC-01 to TC-28); this plan adds 24 more for full coverage
- Cost tracker, analyzer, checker, prompt builder, and refiner have no IMPL TCs - covered here
- Mock responses must include realistic usage fields (token counts, cache status, request IDs)
- Integration test must verify state tracking across all pipeline steps

## Table of Contents

1. [Overview](#1-overview)
2. [Scenario](#2-scenario)
3. [Test Strategy](#3-test-strategy)
4. [Test Priority Matrix](#4-test-priority-matrix)
5. [Test Data](#5-test-data)
6. [Test Cases](#6-test-cases)
7. [Test Phases](#7-test-phases)
8. [Helper Functions](#8-helper-functions)
9. [Cleanup](#9-cleanup)
10. [Verification Checklist](#10-verification-checklist)
11. [Document History](#11-document-history)

## 1. Overview

This test plan covers 52 test cases across 12 categories for the MinimalIPPS compression pipeline. It extends the 28 baseline test cases defined in `_IMPL_IPPS_MINIFICATION_MOTHER_MODEL.md [MIPPS-IP01]` with 24 additional test cases covering modules that had no IMPL-level TCs: api_cost_tracker, mother_analyzer, mother_output_checker, compression_prompt_builder, compression_refiner, and integration.

All tests run with mocked Large Language Model (LLM) APIs. No real API calls. No file writes outside `tmp_path`.

## 2. Scenario

**Problem:** The pipeline has 11 modules with cross-dependencies. Each module must work correctly in isolation and together. Real API calls are expensive ($15-75/M tokens for Mother) and non-deterministic.

**Solution:** Unit tests per module with mocked SDK responses. Integration test verifies full pipeline flow with mocked APIs. All tests use pytest with `tmp_path` fixtures.

**What we don't want:**
- Tests that require real API keys or make real API calls
- Tests that write files outside `tmp_path`
- Tests that depend on execution order within a category
- Tests that validate LLM output quality (non-deterministic, untestable)
- Flaky tests from timing-dependent assertions

## 3. Test Strategy

**Approach**: Unit tests per module + integration test with mocked APIs

**Mocking strategy:**
- Anthropic SDK: `unittest.mock.patch` on `anthropic.Anthropic` constructor. Mock `messages.create()` to return canned responses with realistic `usage` fields (input_tokens, output_tokens, cache_creation_input_tokens, cache_read_input_tokens)
- OpenAI SDK: `unittest.mock.patch` on `openai.OpenAI` constructor. Mock `chat.completions.create()` to return canned responses with `usage` (prompt_tokens, completion_tokens) and `_request_id`
- File system: pytest `tmp_path` fixture for all read/write operations

**Test runner:** `python -m pytest tests/ -v`

**Coverage target:** All public functions in all 11 modules. 52 test cases total.

## 4. Test Priority Matrix

### MUST TEST (Critical Business Logic)

- **`load_state()`, `save_state()`, `init_state()`, `update_step()`, `add_completed_file()`** - pipeline_state.py
  - Testability: **EASY**, Effort: Low
  - Resume capability depends on correct state. Corrupted state recovery critical (EC-08)

- **`calculate_cost()`, `check_budget()`** - api_cost_tracker.py
  - Testability: **EASY**, Effort: Low
  - Budget guard prevents runaway costs. Wrong rates = wrong budget decisions

- **`scan_source_dir()`, `generate_bundle()`, `count_tokens()`** - file_bundle_builder.py
  - Testability: **EASY**, Effort: Low
  - Bundle is input to all Mother calls. Wrong scan = missing files in context

- **`compress_file()`, `run_compression_step()`** - file_compressor.py
  - Testability: **MEDIUM**, Effort: Medium
  - Core compression loop with judge scoring, refinement, and resume. 6 distinct paths

- **`verify_file()`, `check_cross_references()`, `generate_report()`** - compression_report_builder.py
  - Testability: **MEDIUM**, Effort: Medium
  - Quality gate: broken references or wrong report format = incorrect iteration decisions

### SHOULD TEST (Important Workflows)

- **`AnthropicClient.call_with_cache()`, `OpenAIClient.call()`** - llm_clients.py
  - Testability: **MEDIUM**, Effort: Medium
  - Retry logic, cache handling, error classification. All external I/O

- **`analyze_call_tree()`, `parse_load_frequencies()`, `identify_excluded_files()`, `generate_strategy()`** - mother_analyzer.py
  - Testability: **MEDIUM**, Effort: Medium
  - Orchestrates Mother calls for Steps 2-4. Exclusion logic critical

- **`spot_check_document()`, `report_issues()`** - mother_output_checker.py
  - Testability: **EASY**, Effort: Low
  - Sampling logic and issue formatting

- **`generate_compression_prompts()`, `save_prompts()`** - compression_prompt_builder.py
  - Testability: **EASY**, Effort: Low
  - Prompt generation and file output structure

- **`review_report()`, `update_strategy()`, `get_files_to_recompress()`** - compression_refiner.py
  - Testability: **EASY**, Effort: Low
  - Iteration logic, error handling for missing report

- **CLI subcommands** - mipps_pipeline.py
  - Testability: **MEDIUM**, Effort: Medium
  - Prerequisite checking, state updates per command

### DROP (Not Worth Testing)

- **`lib/__init__.py`** - Empty package init, no logic
- **Prompt content quality** - LLM-dependent, non-deterministic output. Evaluated by judge at runtime
- **Actual compression ratio** - Requires real API calls, measured in production runs
- **Cache TTL behavior** - Anthropic infrastructure concern, not testable locally

## 5. Test Data

### Required Fixtures (in `tests/conftest.py`)

- **`sample_config`** - Valid `pipeline_config.json` dict matching SPEC section 9
- **`sample_state`** - Valid `pipeline_state.json` dict with realistic field values
- **`corrupted_state_file`** - File with invalid JSON content for EC-08 testing
- **`mock_source_dir`** - `tmp_path` with mixed files (.md, .py, .json, binary)
- **`sample_bundle`** - Concatenated .md content with `## [path]` headers
- **`mock_anthropic_response`** - Factory for Anthropic SDK response objects with configurable cache status
- **`mock_openai_response`** - Factory for OpenAI SDK response objects with configurable score
- **`mock_compressed_file`** - Sample compressed .md content
- **`mock_strategy`** - Sample `_03_FILE_COMPRESSION_STRATEGY.md` content with Primary/Secondary/Drop lists
- **`mock_report`** - Sample `_04_FILE_COMPRESSION_REPORT.md` content

### Setup

```python
@pytest.fixture
def sample_config(tmp_path):
    config = {
        "source_dir": str(tmp_path / "source"),
        "output_dir": str(tmp_path / "output"),
        "models": {
            "mother": {"provider": "anthropic", "model": "claude-opus-4-6",
                       "max_context": 1000000, "thinking": True},
            "verification": {"provider": "openai", "model": "gpt-5-mini",
                            "max_context": 128000}
        },
        "thresholds": {
            "judge_min_score": 3.5, "max_refinement_attempts": 1,
            "exclusion_max_lines": 100, "exclusion_max_references": 2,
            "target_compression_percent": 40, "max_manual_review_files": 5
        },
        "cache": {"ttl": "1h"},
        "budget": {"max_total_usd": 100.0, "warn_at_percent": 80},
        "file_type_map": {"rules/*.md": "compress_rules", "*": "compress_other"},
        "include_patterns": ["*.md"],
        "skip_patterns": ["pricing-sources/*"],
        "api_timeout_seconds": 120
    }
    return config

@pytest.fixture
def mock_source_dir(tmp_path):
    source = tmp_path / "source"
    (source / "rules").mkdir(parents=True)
    (source / "workflows").mkdir()
    (source / "skills" / "coding" ).mkdir(parents=True)
    # .md files (compressible)
    (source / "rules" / "core.md").write_text("# Core Rules\n" * 50)
    (source / "workflows" / "build.md").write_text("# Build\n" * 30)
    (source / "skills" / "coding" / "SKILL.md").write_text("# Skill\n" * 10)
    # Non-.md files (excluded from output)
    (source / "skills" / "coding" / "script.py").write_text("print('hello')")
    (source / "skills" / "coding" / "config.json").write_text("{}")
    # Binary file
    (source / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    return source
```

### Teardown

pytest `tmp_path` fixture handles cleanup automatically. No manual teardown needed.

## 6. Test Cases

### Category 1: File Bundle Builder (5 tests)

- **MIPPS-TP01-TC-01**: Scan source dir with mixed files -> ok=true, returns categorized dict, .md files in categories, .py/.json excluded. Maps to MIPPS-IP01-TC-01
- **MIPPS-TP01-TC-02**: Scan empty directory -> ok=false, raises EmptySourceError with directory path in message. Maps to MIPPS-IP01-TC-02
- **MIPPS-TP01-TC-03**: Skip files matching skip_patterns -> ok=true, matched files absent from result. Maps to MIPPS-IP01-TC-03
- **MIPPS-TP01-TC-04**: Generate bundle with headers -> ok=true, each file prefixed with `## [relative/path]`, metadata line with line count and token estimate. Maps to MIPPS-IP01-TC-04
- **MIPPS-TP01-TC-05**: Token count estimation -> ok=true, result within 10% of tiktoken `cl100k_base` encoding. Maps to MIPPS-IP01-TC-05

### Category 2: Pipeline State (4 tests)

- **MIPPS-TP01-TC-06**: Load valid state file -> ok=true, returns dict with all PipelineState fields. Maps to MIPPS-IP01-TC-06
- **MIPPS-TP01-TC-07**: Load corrupted state file -> ok=true, creates `.bak` backup, returns fresh `init_state()`. Maps to MIPPS-IP01-TC-07
- **MIPPS-TP01-TC-08**: update_step sets current_step -> ok=true, state["current_step"] equals new value. Maps to MIPPS-IP01-TC-08
- **MIPPS-TP01-TC-09**: add_completed_file appends to list -> ok=true, file path in state["files_completed"]. Maps to MIPPS-IP01-TC-09

### Category 3: API Cost Tracker (5 tests)

- **MIPPS-TP01-TC-10**: calculate_cost for Anthropic with all token types (input, cached_read, cached_write, output) -> ok=true, result matches manual calculation using PRICING dict rates ($15.00/$1.50/$30.00/$75.00 per 1M tokens)
- **MIPPS-TP01-TC-11**: calculate_cost for OpenAI -> ok=true, result matches manual calculation using PRICING dict rates ($0.25/$2.00 per 1M tokens)
- **MIPPS-TP01-TC-12**: check_budget at 80% -> ok=true, returns (False, "warning: 80% of budget...") tuple
- **MIPPS-TP01-TC-13**: check_budget at 100% -> ok=true, returns (True, "halt: budget exceeded...") tuple
- **MIPPS-TP01-TC-14**: calculate_cost with unknown model -> ok=false, raises KeyError or ValueError with model name in message

### Category 4: LLM Clients (6 tests)

- **MIPPS-TP01-TC-15**: Anthropic call_with_cache returns cache hit -> ok=true, usage includes cache_read_input_tokens > 0. Maps to MIPPS-IP01-TC-10
- **MIPPS-TP01-TC-16**: Anthropic timeout -> ok=true, retries 3x with backoff, succeeds on 3rd attempt. Maps to MIPPS-IP01-TC-11
- **MIPPS-TP01-TC-17**: Anthropic rate limit (429) -> ok=true, waits and retries per Retry-After. Maps to MIPPS-IP01-TC-12
- **MIPPS-TP01-TC-18**: OpenAI call success -> ok=true, returns response text and usage dict with prompt_tokens/completion_tokens. Maps to MIPPS-IP01-TC-13
- **MIPPS-TP01-TC-19**: API failure after 3 retries -> ok=false, raises APIError with retry count and last error. Maps to MIPPS-IP01-TC-14
- **MIPPS-TP01-TC-52**: Anthropic call with cache miss (expired Time To Live (TTL)) -> ok=true, usage shows cache_creation_input_tokens > 0 and cache_read_input_tokens = 0, cost_tracker records cache write cost. Verifies IG-05

### Category 5: Mother Analyzer (5 tests)

- **MIPPS-TP01-TC-20**: analyze_call_tree writes `_01_FILE_CALL_TREE.md` -> ok=true, file exists with content from mocked Mother response
- **MIPPS-TP01-TC-21**: parse_load_frequencies extracts per-file counts -> ok=true, returns dict mapping file paths to integer reference counts
- **MIPPS-TP01-TC-22**: analyze_complexity writes `_02_FILE_COMPLEXITY_MAP.md` -> ok=true, file exists
- **MIPPS-TP01-TC-23**: identify_excluded_files applies both criteria -> ok=true, files with < 100 lines AND <= 2 refs are excluded; files meeting only one criterion are NOT excluded
- **MIPPS-TP01-TC-24**: generate_strategy writes `_03_FILE_COMPRESSION_STRATEGY.md` -> ok=true, excluded files not in compression scope

### Category 6: Mother Output Checker (2 tests)

- **MIPPS-TP01-TC-25**: spot_check_document samples correct count -> ok=true, calls OpenAI client exactly `sample_size` times (default 15), returns dict with issues list
- **MIPPS-TP01-TC-26**: report_issues formats findings -> ok=true, output contains file path, claim, and verification result per issue

### Category 7: Compression Prompt Builder (3 tests)

- **MIPPS-TP01-TC-27**: generate_compression_prompts produces per-type dict -> ok=true, keys match file_type_map values (compress_rules, compress_workflows, compress_skill_docs, compress_skill_prompts, compress_templates, compress_other)
- **MIPPS-TP01-TC-28**: save_prompts writes to transform/ and eval/ dirs -> ok=true, `prompts/transform/compress_rules.md` and `prompts/eval/compress_rules.md` exist for each type
- **MIPPS-TP01-TC-29**: compress_other fallback always included -> ok=true, even when file_type_map has no `*` entry, compress_other prompt is generated

### Category 8: File Compressor (6 tests)

- **MIPPS-TP01-TC-30**: compress_file score >= 3.5 -> ok=true, saves to output/ without refinement. Maps to MIPPS-IP01-TC-15
- **MIPPS-TP01-TC-31**: compress_file score < 3.5, refine succeeds (score >= 3.5 on retry) -> ok=true, refined version saved. Maps to MIPPS-IP01-TC-16
- **MIPPS-TP01-TC-32**: compress_file fails after refinement -> ok=true, file appended to `_05_MANUAL_REVIEW_QUEUE.md` with path, scores, and feedback. Maps to MIPPS-IP01-TC-17
- **MIPPS-TP01-TC-33**: run_compression_step resumes from files_completed -> ok=true, skips files already in state["files_completed"]. Maps to MIPPS-IP01-TC-18
- **MIPPS-TP01-TC-34**: Compression increases token count -> ok=false, file flagged as failed, added to manual review. Maps to MIPPS-IP01-TC-19
- **MIPPS-TP01-TC-35**: Budget exceeded during compression -> ok=false, halts with budget message, does not process remaining files. Maps to MIPPS-IP01-TC-20

### Category 9: Compression Report Builder (4 tests)

- **MIPPS-TP01-TC-36**: verify_file produces exactly 5-line report -> ok=true, lines match format: structural, removed, simplified, sacrificed, impact. Maps to MIPPS-IP01-TC-21
- **MIPPS-TP01-TC-37**: check_cross_references finds broken ref -> ok=true, broken_references count incremented, ref details in report. Maps to MIPPS-IP01-TC-22
- **MIPPS-TP01-TC-38**: All references resolve -> ok=true, broken_references = 0. Maps to MIPPS-IP01-TC-23
- **MIPPS-TP01-TC-39**: generate_report includes summary -> ok=true, summary contains pass rate, compression ratio, broken references count. Maps to MIPPS-IP01-TC-24

### Category 10: Compression Refiner (4 tests)

- **MIPPS-TP01-TC-40**: review_report returns strategy updates -> ok=true, dict contains specific file-level guidance changes
- **MIPPS-TP01-TC-41**: update_strategy modifies strategy content -> ok=true, at least one file's compression guidance changed in strategy file
- **MIPPS-TP01-TC-42**: get_files_to_recompress parses flagged files -> ok=true, returns list of file paths from report's flagged entries
- **MIPPS-TP01-TC-43**: No report exists -> ok=false, raises FileNotFoundError with report path in message (EC-07)

### Category 11: Command-Line Interface (4 tests)

- **MIPPS-TP01-TC-44**: `bundle --source-dir [path]` -> ok=true, creates bundle file and initializes state. Maps to MIPPS-IP01-TC-25
- **MIPPS-TP01-TC-45**: `status` with existing state -> ok=true, stdout shows current_step, files_compressed, total cost. Maps to MIPPS-IP01-TC-26
- **MIPPS-TP01-TC-46**: `compress` without prior bundle -> ok=false, exits with error "Run 'bundle' first". Maps to MIPPS-IP01-TC-27
- **MIPPS-TP01-TC-47**: `iterate` without report -> ok=false, exits with error "Run 'verify' first" or auto-runs verify. Maps to MIPPS-IP01-TC-28

### Category 12: Integration (4 tests)

- **MIPPS-TP01-TC-48**: Full pipeline run (bundle -> analyze -> check -> generate -> compress -> verify) completes -> ok=true, state["current_step"] == 7 and all 7 steps recorded
- **MIPPS-TP01-TC-49**: State tracks all steps correctly -> ok=true, state["current_step"] == 7 after full run, files_compressed matches expected count
- **MIPPS-TP01-TC-50**: Output directory contains compressed files -> ok=true, output/ has files matching non-excluded .md files from source
- **MIPPS-TP01-TC-51**: Cost stays within budget -> ok=true, state["cost"]["total"] < config["budget"]["max_total_usd"]

## 7. Test Phases

Ordered execution sequence:

1. **Phase 1: Pure Unit Tests** (no mocked API)
   - Categories: 1 (Bundle Builder), 2 (Pipeline State), 3 (Cost Tracker)
   - Tests: TC-01 to TC-14
   - Dependencies: None
   - Run: `python -m pytest tests/test_file_bundle_builder.py tests/test_pipeline_state.py tests/test_api_cost_tracker.py -v`

2. **Phase 2: API Client Tests** (mocked SDK)
   - Categories: 4 (LLM Clients)
   - Tests: TC-15 to TC-19, TC-52
   - Dependencies: Phase 1 passes
   - Run: `python -m pytest tests/test_llm_clients.py -v`

3. **Phase 3: Module Tests** (mocked clients)
   - Categories: 5 (Analyzer), 6 (Checker), 7 (Prompt Builder), 8 (Compressor), 9 (Report Builder), 10 (Refiner)
   - Tests: TC-20 to TC-43
   - Dependencies: Phase 2 passes
   - Run: `python -m pytest tests/test_mother_analyzer.py tests/test_mother_output_checker.py tests/test_compression_prompt_builder.py tests/test_file_compressor.py tests/test_compression_report_builder.py tests/test_compression_refiner.py -v`

4. **Phase 4: CLI Tests** (mocked modules)
   - Categories: 11 (CLI)
   - Tests: TC-44 to TC-47
   - Dependencies: Phase 3 passes
   - Run: `python -m pytest tests/test_cli.py -v`

5. **Phase 5: Integration Test** (mocked APIs, full pipeline)
   - Categories: 12 (Integration)
   - Tests: TC-48 to TC-51
   - Dependencies: Phase 4 passes
   - Run: `python -m pytest tests/test_integration.py -v --timeout=60`

## 8. Helper Functions

```python
# tests/conftest.py - Shared fixtures and helpers

def create_mock_anthropic_response(content: str, cache_hit: bool = False) -> Mock:
    """Create mock Anthropic messages.create() response.
    
    Args:
        content: Text content of response
        cache_hit: If True, usage shows cache_read_input_tokens > 0
    """
    response = Mock()
    response.content = [Mock(text=content)]
    response.usage = Mock(
        input_tokens=1000 if not cache_hit else 100,
        output_tokens=500,
        cache_creation_input_tokens=300000 if not cache_hit else 0,
        cache_read_input_tokens=300000 if cache_hit else 0,
    )
    response.model = "claude-opus-4-6"
    return response

def create_mock_openai_response(content: str, score: float = 4.0) -> Mock:
    """Create mock OpenAI chat.completions.create() response.
    
    Args:
        content: Text content of response (or use score to auto-generate judge response)
        score: Judge score to embed in content if content not provided
    """
    response = Mock()
    response.choices = [Mock(message=Mock(content=content or f"Score: {score}/5\nGood compression."))]
    response.usage = Mock(prompt_tokens=500, completion_tokens=100)
    response._request_id = "req_test_12345"
    response.model = "gpt-5-mini"
    return response

def create_sample_state(step: int = 0, files_completed: list = None) -> dict:
    """Create valid pipeline_state.json dict."""
    return {
        "current_step": step,
        "iteration": 1,
        "files_total": 10,
        "files_compressible": 8,
        "files_excluded": 2,
        "files_compressed": 0,
        "files_passed": 0,
        "files_failed": 0,
        "files_excluded_md": 2,
        "files_completed": files_completed or [],
        "broken_references": 0,
        "cost": {
            "mother_input": 0.0, "mother_output": 0.0,
            "verification_input": 0.0, "verification_output": 0.0,
            "total": 0.0
        }
    }

def assert_file_contains(path, expected_substring: str):
    """Assert file exists and contains expected substring."""
    assert path.exists(), f"File not found: {path}"
    content = path.read_text(encoding="utf-8")
    assert expected_substring in content, (
        f"Expected '{expected_substring}' in {path.name}, "
        f"got first 200 chars: {content[:200]}"
    )
```

## 9. Cleanup

- pytest `tmp_path` auto-cleans all temporary directories
- No persistent state between test runs
- No mock patches leak between tests (use `with patch(...)` or `@patch` decorator scoped to each test function)
- No environment variables modified (API keys not needed for mocked tests)

## 10. Verification Checklist

### Requirements Coverage

- [ ] **MIPPS-TP01-VC-01**: FR-01 (Bundle Generation) covered by TC-01 to TC-05
- [ ] **MIPPS-TP01-VC-02**: FR-02 (Call Tree Analysis) covered by TC-20, TC-21
- [ ] **MIPPS-TP01-VC-03**: FR-03 (Complexity Map) covered by TC-22, TC-23
- [ ] **MIPPS-TP01-VC-04**: FR-04 (Compression Strategy) covered by TC-24
- [ ] **MIPPS-TP01-VC-05**: FR-05 (Prompt Generation) covered by TC-27 to TC-29
- [ ] **MIPPS-TP01-VC-06**: FR-06 (Compression Execution) covered by TC-30 to TC-35
- [ ] **MIPPS-TP01-VC-07**: FR-07 (Verification Report) covered by TC-36 to TC-39
- [ ] **MIPPS-TP01-VC-08**: FR-08 (Iteration) covered by TC-40 to TC-43, TC-47
- [ ] **MIPPS-TP01-VC-09**: FR-09 (Excluded File Handling) covered by TC-03, TC-23, TC-33
- [ ] **MIPPS-TP01-VC-10**: FR-10 (Pipeline State) covered by TC-06 to TC-09, TC-49
- [ ] **MIPPS-TP01-VC-11**: FR-11 (Verification of Mother Outputs) covered by TC-25, TC-26

### Implementation Guarantees

- [ ] **MIPPS-TP01-VC-12**: IG-01 (Independent verification) verified by TC-30 to TC-32 (verifier is separate client)
- [ ] **MIPPS-TP01-VC-13**: IG-02 (No source modification) verified by TC-48 (integration checks source untouched)
- [ ] **MIPPS-TP01-VC-14**: IG-03 (Resume without data loss) verified by TC-07, TC-33
- [ ] **MIPPS-TP01-VC-15**: IG-04 (Excluded files identical) verified by TC-50 (output matches source for excluded)
- [ ] **MIPPS-TP01-VC-16**: IG-05 (Cache re-send on expiry) verified by TC-52
- [ ] **MIPPS-TP01-VC-17**: IG-06 (Budget guard) verified by TC-12, TC-13, TC-35, TC-51
- [ ] **MIPPS-TP01-VC-18**: IG-07 (Excluded files never sent to Mother) verified by TC-23, TC-33

### Edge Cases

- [ ] **MIPPS-TP01-VC-19**: EC-01 (Empty dir) covered by TC-02
- [ ] **MIPPS-TP01-VC-20**: EC-04 (Missing config) covered by TC-46 (prerequisite check)
- [ ] **MIPPS-TP01-VC-21**: EC-06 (Resume partial) covered by TC-33
- [ ] **MIPPS-TP01-VC-22**: EC-07 (No report) covered by TC-43
- [ ] **MIPPS-TP01-VC-23**: EC-08 (Corrupted state) covered by TC-07
- [ ] **MIPPS-TP01-VC-24**: EC-09 (Anthropic timeout) covered by TC-16
- [ ] **MIPPS-TP01-VC-25**: EC-10 (Rate limit) covered by TC-17
- [ ] **MIPPS-TP01-VC-26**: EC-11 (OpenAI failure) covered by TC-19
- [ ] **MIPPS-TP01-VC-27**: EC-12 (Cache expired) covered by TC-52
- [ ] **MIPPS-TP01-VC-28**: EC-13 (Truncated output) covered by TC-34 (token increase as proxy)
- [ ] **MIPPS-TP01-VC-29**: EC-14 (Invalid score) covered by TC-34
- [ ] **MIPPS-TP01-VC-30**: EC-16 (Token increase) covered by TC-34

### Test Execution

- [ ] **MIPPS-TP01-VC-31**: All 52 test cases pass
- [ ] **MIPPS-TP01-VC-32**: No test makes real API calls
- [ ] **MIPPS-TP01-VC-33**: No test writes outside tmp_path
- [ ] **MIPPS-TP01-VC-34**: All 28 IMPL TCs (MIPPS-IP01-TC-01 to TC-28) have corresponding TP01 TCs
- [ ] **MIPPS-TP01-VC-35**: All 11 FRs have at least one test case
- [ ] **MIPPS-TP01-VC-36**: All 7 IGs have at least one verification test (IG-01 to IG-07)

### IMPL TC Traceability

- [ ] **MIPPS-TP01-VC-37**: IP01-TC-01 -> TP01-TC-01
- [ ] **MIPPS-TP01-VC-38**: IP01-TC-02 -> TP01-TC-02
- [ ] **MIPPS-TP01-VC-39**: IP01-TC-03 -> TP01-TC-03
- [ ] **MIPPS-TP01-VC-40**: IP01-TC-04 -> TP01-TC-04
- [ ] **MIPPS-TP01-VC-41**: IP01-TC-05 -> TP01-TC-05
- [ ] **MIPPS-TP01-VC-42**: IP01-TC-06 -> TP01-TC-06
- [ ] **MIPPS-TP01-VC-43**: IP01-TC-07 -> TP01-TC-07
- [ ] **MIPPS-TP01-VC-44**: IP01-TC-08 -> TP01-TC-08
- [ ] **MIPPS-TP01-VC-45**: IP01-TC-09 -> TP01-TC-09
- [ ] **MIPPS-TP01-VC-46**: IP01-TC-10 -> TP01-TC-15
- [ ] **MIPPS-TP01-VC-47**: IP01-TC-11 -> TP01-TC-16
- [ ] **MIPPS-TP01-VC-48**: IP01-TC-12 -> TP01-TC-17
- [ ] **MIPPS-TP01-VC-49**: IP01-TC-13 -> TP01-TC-18
- [ ] **MIPPS-TP01-VC-50**: IP01-TC-14 -> TP01-TC-19
- [ ] **MIPPS-TP01-VC-51**: IP01-TC-15 -> TP01-TC-30
- [ ] **MIPPS-TP01-VC-52**: IP01-TC-16 -> TP01-TC-31
- [ ] **MIPPS-TP01-VC-53**: IP01-TC-17 -> TP01-TC-32
- [ ] **MIPPS-TP01-VC-54**: IP01-TC-18 -> TP01-TC-33
- [ ] **MIPPS-TP01-VC-55**: IP01-TC-19 -> TP01-TC-34
- [ ] **MIPPS-TP01-VC-56**: IP01-TC-20 -> TP01-TC-35
- [ ] **MIPPS-TP01-VC-57**: IP01-TC-21 -> TP01-TC-36
- [ ] **MIPPS-TP01-VC-58**: IP01-TC-22 -> TP01-TC-37
- [ ] **MIPPS-TP01-VC-59**: IP01-TC-23 -> TP01-TC-38
- [ ] **MIPPS-TP01-VC-60**: IP01-TC-24 -> TP01-TC-39
- [ ] **MIPPS-TP01-VC-61**: IP01-TC-25 -> TP01-TC-44
- [ ] **MIPPS-TP01-VC-62**: IP01-TC-26 -> TP01-TC-45
- [ ] **MIPPS-TP01-VC-63**: IP01-TC-27 -> TP01-TC-46
- [ ] **MIPPS-TP01-VC-64**: IP01-TC-28 -> TP01-TC-47

## 11. Document History

**[2026-03-20 05:05]**
- Fixed: TTL expanded to "Time To Live (TTL)" on first use in TC-52 (AP-PR-06)
- Fixed: PROGRESS.md test case counts corrected from 51/23 to 52/24

**[2026-03-20 05:00]**
- Fixed: Category 4 heading "5 tests" corrected to "6 tests" (TC-52 was added but count not updated)
- Fixed: IG ordering in VC section - IG-05 before IG-06 (was reversed)
- Fixed: LLM expanded to "Large Language Model (LLM)" on first use (AP-PR-06)
- Fixed: TC-41 and TC-48 descriptions made more specific (AP-PR-07)
- Fixed: Timeline "Updated 0 times" corrected to "Updated 2 times"

**[2026-03-20 04:50]**
- Fixed: Added TC-52 for IG-05 (cache miss/re-send) - was missing from initial plan
- Fixed: "TCs" expanded to "Test Cases (TCs)" on first use (AP-PR-06)
- Fixed: VC renumbered after inserting IG-05 coverage (VC-17)
- Added: EC-12 (cache expired) to edge case VCs

**[2026-03-20 04:45]**
- Initial test plan created from MIPPS-SP01, MIPPS-IP01, and MIPPS-TK01
- 52 test cases across 12 categories (28 from IMPL + 24 new)
- 5 test phases with dependency ordering
- 64 verification checklist items with full IMPL TC traceability
