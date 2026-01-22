# TEST: LLM Evaluation Skill

**Doc ID**: LLMEV-TP01
**Feature**: llm-evaluation-skill
**Goal**: Verify all scripts work correctly with proper error handling, resume capability, and incremental saving
**Timeline**: Created 2026-01-22, Updated 0 times
**Target file**: `.windsurf/skills/llm-evaluation/tests/` (test scripts)

**Depends on:**
- `SPEC_LLM_EVALUATION_SKILL.md` [LLMEV-SP01] for requirements
- `IMPL_LLM_EVALUATION_SKILL.md` [LLMEV-IP01] for implementation details

## MUST-NOT-FORGET

- **NO REAL API CALLS**: All tests use mocked API responses
- **CLEANUP**: Remove all test artifacts after each test
- **ISOLATED**: Each test must be independent, no shared state
- Test incremental save by simulating crash mid-process
- Test resume by verifying skipped files and reprocessed .tmp files

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

This test plan verifies the LLM Evaluation Skill scripts:
- `call-llm.py` - Single LLM call
- `call-llm-batch.py` - Batch processing with parallelism
- `generate-questions.py` - Question generation
- `generate-answers.py` - Answer generation
- `evaluate-answers.py` - LLM-as-judge scoring
- `analyze-costs.py` - Token cost analysis

Focus areas: API key loading, file type detection, retry logic, resume capability, incremental saving, JSON parsing.

## 2. Scenario

**Problem:** LLM evaluation pipelines can fail due to API errors, network issues, or crashes. We need to verify scripts handle these gracefully.

**Solution:** Test each failure mode with mocked responses, verify correct behavior including:
- Retry with backoff on transient errors
- Resume capability (skip completed, reprocess .tmp)
- Incremental save after each item
- Atomic writes via temp file pattern

**What we don't want:**
- Tests that make real API calls (expensive, slow, flaky)
- Tests that depend on execution order
- Tests that leave artifacts behind

## 3. Test Strategy

**Approach**: Unit tests with mocked API responses

**Mocking Strategy:**
1. Mock `openai.OpenAI` and `anthropic.Anthropic` clients
2. Return predefined responses or raise exceptions
3. Verify correct retry behavior
4. Verify file outputs match expectations

**Test Execution:**
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific category
python -m pytest tests/ -v -k "test_retry"

# Run with coverage
python -m pytest tests/ -v --cov=. --cov-report=term-missing
```

## 4. Test Priority Matrix

### MUST TEST (Critical Business Logic)

- **`load_api_keys()`** - All scripts
  - Testability: **EASY**, Effort: Low
  - Parse .env format, handle missing keys

- **`detect_provider()`** - All scripts
  - Testability: **EASY**, Effort: Low
  - Map model ID prefix to provider

- **`retry_with_backoff()`** - All scripts
  - Testability: **EASY**, Effort: Low
  - Verify retry count, backoff timing

- **`atomic_write_json()`** - All batch scripts
  - Testability: **EASY**, Effort: Low
  - Verify temp file pattern, thread safety

- **Resume logic** - call-llm-batch.py
  - Testability: **MEDIUM**, Effort: Medium
  - Skip existing outputs, reprocess .tmp files

- **Incremental save** - All batch scripts
  - Testability: **MEDIUM**, Effort: Medium
  - Verify save after each item

### SHOULD TEST (Important Workflows)

- **`detect_file_type()`** - call-llm.py, call-llm-batch.py
  - Testability: Medium, Effort: Low
  - Map suffix to image/text type

- **`parse_json_response()`** - generate-questions.py, generate-answers.py
  - Testability: **EASY**, Effort: Low
  - Strip markdown fences, handle malformed JSON

- **`calculate_cost()`** - analyze-costs.py
  - Testability: **EASY**, Effort: Low
  - Math verification with known inputs

- **End-to-end pipeline** - All scripts
  - Testability: Medium, Effort: High
  - Full workflow with mocked responses

### DROP (Not Worth Testing)

- **CLI argument parsing** - Reason: argparse is well-tested
- **File I/O primitives** - Reason: Python stdlib is reliable
- **Actual API responses** - Reason: External dependency, use mocks

## 5. Test Data

**Required Fixtures:**

- **`test_images/`** - Small test images (1x1 pixel PNG, JPG)
- **`test_docs/`** - Small test documents (.md, .txt)
- **`test_keys.env`** - Fake API keys for testing
- **`mock_responses/`** - JSON files with mock API responses

**Sample test_keys.env:**
```
OPENAI_API_KEY=sk-test-fake-key-12345
ANTHROPIC_API_KEY=sk-ant-test-fake-key-67890
```

**Sample mock_responses/transcription.json:**
```json
{
  "content": "This is a test transcription.",
  "usage": {"input_tokens": 100, "output_tokens": 50}
}
```

**Setup:**
```python
@pytest.fixture
def test_env(tmp_path):
    # Create test directory structure
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    
    # Create test files
    (input_dir / "test.jpg").write_bytes(MINIMAL_JPG)
    (input_dir / "test.md").write_text("Test content")
    
    # Create keys file
    keys_file = tmp_path / ".env"
    keys_file.write_text("OPENAI_API_KEY=sk-test\nANTHROPIC_API_KEY=sk-ant-test")
    
    return {"input": input_dir, "output": output_dir, "keys": keys_file}
```

**Teardown:**
```python
# pytest tmp_path fixture auto-cleans after test
# No manual cleanup needed
```

## 6. Test Cases

### Category 1: API Key Loading (4 tests)

- **LLMEV-TP01-TC-01**: Load valid .env file -> ok=true, keys dict has OPENAI_API_KEY and ANTHROPIC_API_KEY
- **LLMEV-TP01-TC-02**: Load file with comments -> ok=true, comments ignored
- **LLMEV-TP01-TC-03**: Missing key file -> ok=false, FileNotFoundError
- **LLMEV-TP01-TC-04**: Empty key file -> ok=true, empty dict

### Category 2: Provider Detection (5 tests)

- **LLMEV-TP01-TC-05**: Model "gpt-4o" -> ok=true, provider="openai"
- **LLMEV-TP01-TC-06**: Model "claude-opus-4-20250514" -> ok=true, provider="anthropic"
- **LLMEV-TP01-TC-07**: Model "o1-preview" -> ok=true, provider="openai"
- **LLMEV-TP01-TC-08**: Model "unknown-model" -> ok=false, ValueError
- **LLMEV-TP01-TC-09**: Model "gpt-5-mini" -> ok=true, provider="openai"

### Category 3: File Type Detection (6 tests)

- **LLMEV-TP01-TC-10**: File "test.jpg" -> ok=true, type="image"
- **LLMEV-TP01-TC-11**: File "test.png" -> ok=true, type="image"
- **LLMEV-TP01-TC-12**: File "test.md" -> ok=true, type="text"
- **LLMEV-TP01-TC-13**: File "test.txt" -> ok=true, type="text"
- **LLMEV-TP01-TC-14**: File "test.xyz" -> ok=false, "Unknown file type"
- **LLMEV-TP01-TC-15**: File with no extension -> ok=false, "Unknown file type"

### Category 4: Retry Logic (5 tests)

- **LLMEV-TP01-TC-16**: Success on first try -> ok=true, 1 attempt
- **LLMEV-TP01-TC-17**: Success on second try (rate limit then ok) -> ok=true, 2 attempts
- **LLMEV-TP01-TC-18**: Success on third try -> ok=true, 3 attempts
- **LLMEV-TP01-TC-19**: All 3 retries fail -> ok=false, item skipped, error logged
- **LLMEV-TP01-TC-20**: Verify backoff timing (1s, 2s, 4s) -> ok=true, delays correct

### Category 5: Atomic Write (4 tests)

- **LLMEV-TP01-TC-21**: Write JSON to new file -> ok=true, file exists, no .tmp
- **LLMEV-TP01-TC-22**: Write JSON with lock (thread safety) -> ok=true, no corruption
- **LLMEV-TP01-TC-23**: Simulated crash mid-write -> ok=true, .tmp exists, final missing
- **LLMEV-TP01-TC-24**: Overwrite existing file -> ok=true, old content replaced

### Category 6: Resume Capability (5 tests)

- **LLMEV-TP01-TC-25**: Output file exists -> ok=true, skipped (no processing)
- **LLMEV-TP01-TC-26**: .tmp file exists -> ok=true, reprocessed
- **LLMEV-TP01-TC-27**: Neither exists -> ok=true, processed normally
- **LLMEV-TP01-TC-28**: Mix of complete and incomplete -> ok=true, only incomplete processed
- **LLMEV-TP01-TC-29**: --force flag -> ok=true, all reprocessed

### Category 7: Incremental Save (3 tests)

- **LLMEV-TP01-TC-30**: Process 3 items -> ok=true, file updated 3 times
- **LLMEV-TP01-TC-31**: Crash after item 2 -> ok=true, items 1-2 saved, item 3 missing
- **LLMEV-TP01-TC-32**: Resume after crash -> ok=true, only item 3 processed

### Category 8: JSON Parsing (4 tests)

- **LLMEV-TP01-TC-33**: Clean JSON response -> ok=true, parsed correctly
- **LLMEV-TP01-TC-34**: Markdown-wrapped JSON (```json...```) -> ok=true, fences stripped
- **LLMEV-TP01-TC-35**: Invalid JSON -> ok=false, error logged, raw saved
- **LLMEV-TP01-TC-36**: JSON with extra whitespace -> ok=true, parsed correctly

### Category 9: Cost Calculation (3 tests)

- **LLMEV-TP01-TC-37**: Calculate cost for known tokens -> ok=true, matches expected
- **LLMEV-TP01-TC-38**: Multiple models in folder -> ok=true, per-model totals correct
- **LLMEV-TP01-TC-39**: Custom pricing file -> ok=true, uses custom prices

### Category 10: Script-Specific (6 tests)

- **LLMEV-TP01-TC-40**: generate-questions.py with schema -> ok=true, questions match schema categories
- **LLMEV-TP01-TC-41**: generate-answers.py with multiple runs -> ok=true, all runs processed
- **LLMEV-TP01-TC-42**: evaluate-answers.py LLM judge -> ok=true, scores 0-5 returned
- **LLMEV-TP01-TC-43**: Empty input folder -> ok=false, "No files found"
- **LLMEV-TP01-TC-44**: Image encoding failure -> ok=false, retried 3x then skipped
- **LLMEV-TP01-TC-45**: Workers set to 0 -> ok=true, defaults to 1 with warning

### Category 11: End-to-End (3 tests)

- **LLMEV-TP01-TC-46**: call-llm.py with image -> ok=true, output contains transcription
- **LLMEV-TP01-TC-47**: call-llm-batch.py with folder -> ok=true, all files processed
- **LLMEV-TP01-TC-48**: Full pipeline (transcribe -> questions -> answers -> score) -> ok=true, scores generated

## 7. Test Phases

Ordered execution sequence:

1. **Phase 1: Unit Tests - Utilities** (TC-01 to TC-24)
   - API key loading
   - Provider detection
   - File type detection
   - Retry logic
   - Atomic write

2. **Phase 2: Unit Tests - Resume & Incremental** (TC-25 to TC-32)
   - Resume capability
   - Incremental save

3. **Phase 3: Unit Tests - Parsing** (TC-33 to TC-39)
   - JSON parsing
   - Cost calculation

4. **Phase 4: Script-Specific Tests** (TC-40 to TC-45)
   - Individual script behavior
   - Edge cases specific to each script

5. **Phase 5: Integration Tests** (TC-46 to TC-48)
   - End-to-end workflows
   - Requires all unit tests to pass first

## 8. Helper Functions

```python
# Minimal valid image bytes for testing
MINIMAL_JPG = bytes([0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46, 0x00, 0x01, 0x01, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0xFF, 0xD9])
MINIMAL_PNG = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])

def create_mock_client(responses: list):
    """Create mock OpenAI/Anthropic client with predefined responses."""
    ...

def assert_file_contains_json(path: Path, expected_keys: list):
    """Assert file exists, is valid JSON, contains expected keys."""
    ...

def simulate_crash_after_n_items(n: int):
    """Decorator to raise exception after n items processed."""
    ...

def count_api_calls(mock_client) -> int:
    """Return number of API calls made to mock client."""
    ...

def verify_backoff_timing(mock_sleep, expected: tuple):
    """Verify sleep was called with expected backoff values."""
    ...
```

## 9. Cleanup

All tests use `pytest.tmp_path` fixture which auto-cleans. No manual cleanup needed.

**If manual cleanup required:**
- Remove `tests/output/` directory
- Remove any `.tmp` files in skill folder
- Reset mock state between tests

## 10. Verification Checklist

### Prerequisites
- [ ] **LLMEV-TP01-VC-01**: pytest installed
- [ ] **LLMEV-TP01-VC-02**: Mock fixtures created

### Phase 1: Utilities
- [ ] **LLMEV-TP01-VC-03**: TC-01 to TC-04 (API keys) pass
- [ ] **LLMEV-TP01-VC-04**: TC-05 to TC-09 (Provider) pass
- [ ] **LLMEV-TP01-VC-05**: TC-10 to TC-15 (File type) pass
- [ ] **LLMEV-TP01-VC-06**: TC-16 to TC-20 (Retry) pass
- [ ] **LLMEV-TP01-VC-07**: TC-21 to TC-24 (Atomic write) pass

### Phase 2: Resume & Incremental
- [ ] **LLMEV-TP01-VC-08**: TC-25 to TC-29 (Resume) pass
- [ ] **LLMEV-TP01-VC-09**: TC-30 to TC-32 (Incremental) pass

### Phase 3: Parsing
- [ ] **LLMEV-TP01-VC-10**: TC-33 to TC-36 (JSON) pass
- [ ] **LLMEV-TP01-VC-11**: TC-37 to TC-39 (Cost) pass

### Phase 4: Script-Specific
- [ ] **LLMEV-TP01-VC-12**: TC-40 to TC-45 (Script tests) pass

### Phase 5: Integration
- [ ] **LLMEV-TP01-VC-13**: TC-46 to TC-48 (E2E) pass

### Coverage
- [ ] **LLMEV-TP01-VC-14**: All FR-* from SPEC have at least one TC
- [ ] **LLMEV-TP01-VC-15**: All EC-* from IMPL have corresponding TC
- [ ] **LLMEV-TP01-VC-16**: Coverage >= 80%

## 11. Document History

**[2026-01-22 21:27]**
- Added: TC-40 to TC-45 for FR-05, FR-06, FR-07 and missing EC coverage
- Added: Category 10 (Script-Specific) and Category 11 (End-to-End)
- Added: Phase 5 for integration tests
- Fixed: Renumbered E2E tests to TC-46 to TC-48

**[2026-01-22 21:26]**
- Initial test plan created
- 42 test cases across 10 categories
- 15 verification checklist items

