# TEST: LLM Evaluation Skill - Comprehensive Coverage

**Doc ID**: LLMEV-TP03
**Feature**: llm-evaluation-skill
**Goal**: 100% test coverage of all LLM evaluation scripts with all models and settings combinations
**Timeline**: Created 2026-01-24, Updated 0 times

**Target files**:
- `.windsurf/skills/llm-evaluation/call-llm.py`
- `.windsurf/skills/llm-evaluation/call-llm-batch.py`
- `.windsurf/skills/llm-evaluation/generate-questions.py`
- `.windsurf/skills/llm-evaluation/generate-answers.py`
- `.windsurf/skills/llm-evaluation/evaluate-answers.py`
- `.windsurf/skills/llm-evaluation/analyze-costs.py`
- `.windsurf/skills/llm-evaluation/compare-transcription-runs.py`

**Depends on:**
- `SPEC_LLM_EVALUATION_SKILL.md` [LLMEV-SP01] for requirements
- `IMPL_LLM_EVALUATION_SKILL.md` [LLMEV-IP01] for implementation details
- `_SPEC_LLM_EVALUATION_SKILL_ENHANCEMENTS.md` [LLMEV-SP02] for hybrid comparison

## MUST-NOT-FORGET

- Test ALL model types: gpt-3.5, gpt-4o, gpt-4.1, gpt-5-mini, o1, o3, claude-3.5, claude-opus-4, claude-sonnet-4.5
- Test ALL effort levels: none, minimal, low, medium, high, xhigh
- Test ALL file types: .jpg, .png, .gif, .webp, .txt, .md, .json, .py, .html, .xml, .csv
- Test ALL comparison methods: levenshtein, semantic, hybrid
- Test ALL worker counts: 1, 4, 8, 16
- Test ALL error conditions: missing keys, rate limits, invalid files, network errors
- Test incremental save behavior (crash recovery)
- Test atomic writes (.tmp rename pattern)
- Verify JSON output schema for all scripts

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

Comprehensive test suite covering all LLM evaluation skill scripts with exhaustive combinations of:
- Models (9 types across OpenAI and Anthropic)
- Effort levels (6 levels)
- File types (11 types)
- Comparison methods (3 methods)
- Worker configurations (4 counts)
- Error scenarios (8 categories)

Total test cases: 287 (covering all critical paths and edge cases)

## 2. Scenario

**Problem:** LLM evaluation scripts must work reliably across all supported models, file types, and configurations without data loss or incorrect results.

**Solution:** Systematic testing of all combinations using test fixtures, mocked API responses, and real API calls (where safe).

**What we don't want:**
- Skipping edge cases or rare model combinations
- Testing only "happy path" scenarios
- Ignoring error recovery and retry logic
- Missing file type detection edge cases
- Overlooking concurrency issues

## 3. Test Strategy

**Approach**: Hybrid (unit + integration + end-to-end)

**Test Layers:**
1. **Unit Tests** - Individual functions (file detection, parameter building, JSON parsing)
2. **Integration Tests** - Script execution with mocked APIs
3. **End-to-End Tests** - Real API calls with small test datasets

**Mocking Strategy:**
- Mock OpenAI/Anthropic API responses for deterministic testing
- Use VCR.py for recording/replaying API interactions
- Real API calls only for smoke tests (1-2 per model type)

**Coverage Measurement:**
- pytest-cov for code coverage (target: 95%+)
- Manual verification of all CLI parameter combinations
- Error injection testing for retry logic

## 4. Test Priority Matrix

### MUST TEST (Critical Business Logic)

- **`call_llm.py` - Single LLM call**
  - Testability: **EASY**, Effort: Low
  - File type detection (11 types)
  - Model parameter building (9 models × 6 effort levels = 54 combinations)
  - API error handling (8 error types)
  - JSON metadata output

- **`call_llm_batch.py` - Batch processing**
  - Testability: **MEDIUM**, Effort: Medium
  - Concurrent execution (4 worker counts)
  - Incremental save behavior
  - Atomic writes (.tmp rename)
  - Skip existing files logic
  - Clear folder behavior

- **`generate_questions.py` - Question generation**
  - Testability: **MEDIUM**, Effort: Medium
  - Schema validation
  - Question uniqueness
  - Category distribution
  - File type handling

- **`generate_answers.py` - Answer generation**
  - Testability: **MEDIUM**, Effort: Medium
  - Questions file parsing
  - Context extraction from transcriptions
  - Answer formatting

- **`evaluate_answers.py` - LLM-as-judge scoring**
  - Testability: **MEDIUM**, Effort: Medium
  - Score normalization (0-100)
  - Rubric application
  - Batch evaluation

- **`analyze_costs.py` - Cost analysis**
  - Testability: **EASY**, Effort: Low
  - Token counting
  - Price calculation
  - Multiple pricing tiers

- **`compare_transcription_runs.py` - Hybrid comparison**
  - Testability: **MEDIUM**, Effort: Medium
  - Levenshtein distance
  - LLM judge integration
  - Section parsing (<transcription_image> tags)
  - Effort level wiring

### SHOULD TEST (Important Workflows)

- **Model registry loading**
  - Testability: EASY, Effort: Low
  - Prefix matching
  - Default fallback

- **API key loading**
  - Testability: EASY, Effort: Low
  - .env format
  - key=value format
  - Missing key handling

- **Progress logging**
  - Testability: MEDIUM, Effort: Low
  - Worker ID formatting
  - Progress counters

### DROP (Not Worth Testing)

- **CLI help text** - Reason: argparse built-in, trivial
- **File system operations** - Reason: OS-dependent, covered by integration tests
- **Network timeouts** - Reason: External dependency, covered by retry tests

## 5. Test Data

### Required Fixtures

**Images:**
- `test_fixtures/images/photo_small.jpg` - 100KB JPEG
- `test_fixtures/images/photo_large.png` - 5MB PNG
- `test_fixtures/images/diagram.gif` - Animated GIF
- `test_fixtures/images/screenshot.webp` - WebP format

**Text Files:**
- `test_fixtures/text/document.txt` - Plain text
- `test_fixtures/text/markdown.md` - Markdown with headers
- `test_fixtures/text/data.json` - JSON data
- `test_fixtures/text/script.py` - Python code
- `test_fixtures/text/page.html` - HTML content
- `test_fixtures/text/config.xml` - XML config
- `test_fixtures/text/table.csv` - CSV data

**Prompts:**
- `test_fixtures/prompts/transcribe.md` - Image transcription prompt
- `test_fixtures/prompts/summarize.md` - Text summarization prompt
- `test_fixtures/prompts/answer.md` - Q&A prompt
- `test_fixtures/prompts/judge.md` - Scoring prompt

**Expected Outputs:**
- `test_fixtures/expected/` - Golden outputs for comparison

**Mock API Responses:**
- `test_fixtures/mocks/openai_responses.json` - OpenAI API mocks
- `test_fixtures/mocks/anthropic_responses.json` - Anthropic API mocks

### Setup

```python
import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

@pytest.fixture
def test_fixtures():
    """Load all test fixtures"""
    base = Path(__file__).parent / "test_fixtures"
    return {
        "images": list((base / "images").glob("*")),
        "text": list((base / "text").glob("*")),
        "prompts": list((base / "prompts").glob("*.md")),
        "expected": base / "expected"
    }

@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client with realistic responses"""
    with patch('openai.OpenAI') as mock:
        client = MagicMock()
        # Configure mock responses
        yield client

@pytest.fixture
def mock_anthropic_client():
    """Mock Anthropic client with realistic responses"""
    with patch('anthropic.Anthropic') as mock:
        client = MagicMock()
        # Configure mock responses
        yield client
```

### Teardown

```python
def teardown_module():
    """Clean up test outputs"""
    import shutil
    test_output = Path("test_output")
    if test_output.exists():
        shutil.rmtree(test_output)
```

## 6. Test Cases

### Category 1: File Type Detection (11 tests)

- **LLMEV-TP03-TC-001**: `.jpg` file -> ok=true, detected as image
- **LLMEV-TP03-TC-002**: `.jpeg` file -> ok=true, detected as image
- **LLMEV-TP03-TC-003**: `.png` file -> ok=true, detected as image
- **LLMEV-TP03-TC-004**: `.gif` file -> ok=true, detected as image
- **LLMEV-TP03-TC-005**: `.webp` file -> ok=true, detected as image
- **LLMEV-TP03-TC-006**: `.txt` file -> ok=true, detected as text
- **LLMEV-TP03-TC-007**: `.md` file -> ok=true, detected as text
- **LLMEV-TP03-TC-008**: `.json` file -> ok=true, detected as text
- **LLMEV-TP03-TC-009**: `.py` file -> ok=true, detected as text
- **LLMEV-TP03-TC-010**: `.html` file -> ok=true, detected as text
- **LLMEV-TP03-TC-011**: `.unknown` file -> ok=false, error "Unknown file type"

### Category 2: Model Parameter Building (54 tests)

**OpenAI Temperature Models (gpt-3.5, gpt-4o, gpt-4.1):**
- **LLMEV-TP03-TC-012**: gpt-4o + temperature=none -> ok=true, temp=0.0
- **LLMEV-TP03-TC-013**: gpt-4o + temperature=minimal -> ok=true, temp=0.125
- **LLMEV-TP03-TC-014**: gpt-4o + temperature=low -> ok=true, temp=0.25
- **LLMEV-TP03-TC-015**: gpt-4o + temperature=medium -> ok=true, temp=0.5
- **LLMEV-TP03-TC-016**: gpt-4o + temperature=high -> ok=true, temp=1.0
- **LLMEV-TP03-TC-017**: gpt-4o + temperature=xhigh -> ok=true, temp=2.0
- **LLMEV-TP03-TC-018**: gpt-3.5 + all effort levels (6 tests)
- **LLMEV-TP03-TC-024**: gpt-4.1 + all effort levels (6 tests)

**OpenAI Reasoning Models (o1, o3, gpt-5-mini, gpt-5):**
- **LLMEV-TP03-TC-030**: o1 + reasoning_effort=low -> ok=true, effort=low
- **LLMEV-TP03-TC-031**: o1 + reasoning_effort=medium -> ok=true, effort=medium
- **LLMEV-TP03-TC-032**: o1 + reasoning_effort=high -> ok=true, effort=high
- **LLMEV-TP03-TC-033**: gpt-5-mini + all effort levels (6 tests)
- **LLMEV-TP03-TC-039**: gpt-5 + all effort levels (6 tests)
- **LLMEV-TP03-TC-045**: o3 + all effort levels (6 tests)

**Anthropic Models (claude-3.5, claude-opus-4, claude-sonnet-4.5):**
- **LLMEV-TP03-TC-051**: claude-3.5 + temperature=medium -> ok=true, temp=0.5
- **LLMEV-TP03-TC-052**: claude-opus-4 + thinking budget -> ok=true, budget set
- **LLMEV-TP03-TC-053**: claude-sonnet-4.5 + thinking budget -> ok=true, max_tokens > budget
- **LLMEV-TP03-TC-054**: claude-opus-4 + all effort levels (6 tests)
- **LLMEV-TP03-TC-060**: claude-sonnet-4.5 + all effort levels (6 tests)

### Category 3: API Error Handling (8 tests)

- **LLMEV-TP03-TC-066**: Rate limit 429 -> ok=true, retries 3x with backoff, then skips
- **LLMEV-TP03-TC-067**: Server error 500 -> ok=true, retries 3x, then skips
- **LLMEV-TP03-TC-068**: Network timeout -> ok=true, retries 3x, then skips
- **LLMEV-TP03-TC-069**: Invalid API key -> ok=false, error "Invalid API key"
- **LLMEV-TP03-TC-070**: Missing API key -> ok=false, error "Missing OPENAI_API_KEY"
- **LLMEV-TP03-TC-071**: Invalid JSON response -> ok=true, logs warning, saves raw
- **LLMEV-TP03-TC-072**: Empty response -> ok=true, logs warning, saves empty
- **LLMEV-TP03-TC-073**: Malformed response -> ok=true, logs warning, saves raw

### Category 4: Batch Processing (16 tests)

- **LLMEV-TP03-TC-074**: workers=1 -> ok=true, sequential processing
- **LLMEV-TP03-TC-075**: workers=4 -> ok=true, parallel processing
- **LLMEV-TP03-TC-076**: workers=8 -> ok=true, parallel processing
- **LLMEV-TP03-TC-077**: workers=16 -> ok=true, parallel processing
- **LLMEV-TP03-TC-078**: Incremental save after each item -> ok=true, JSON updated
- **LLMEV-TP03-TC-079**: Atomic write (.tmp rename) -> ok=true, no partial files
- **LLMEV-TP03-TC-080**: Skip existing files -> ok=true, existing not reprocessed
- **LLMEV-TP03-TC-081**: Force reprocess -> ok=true, existing overwritten
- **LLMEV-TP03-TC-082**: Clear folder before processing -> ok=true, folder emptied
- **LLMEV-TP03-TC-083**: Multiple runs per file -> ok=true, run1, run2, run3 created
- **LLMEV-TP03-TC-084**: Empty input folder -> ok=false, error "No files found"
- **LLMEV-TP03-TC-085**: Mixed file types in folder -> ok=true, processes all supported
- **LLMEV-TP03-TC-086**: Crash recovery (partial JSON) -> ok=true, resumes from last saved
- **LLMEV-TP03-TC-087**: Progress logging format -> ok=true, "[ worker N ] [ x / n ]"
- **LLMEV-TP03-TC-088**: Worker ID assignment -> ok=true, 1-indexed IDs
- **LLMEV-TP03-TC-089**: Thread safety (concurrent writes) -> ok=true, no race conditions

### Category 5: Question Generation (12 tests)

- **LLMEV-TP03-TC-090**: Default schema -> ok=true, 3 categories, 10 questions each
- **LLMEV-TP03-TC-091**: Custom schema -> ok=true, follows custom categories
- **LLMEV-TP03-TC-092**: Question uniqueness -> ok=true, no duplicate questions
- **LLMEV-TP03-TC-093**: Category distribution -> ok=true, matches schema counts
- **LLMEV-TP03-TC-094**: Image input -> ok=true, generates visual questions
- **LLMEV-TP03-TC-095**: Text input -> ok=true, generates content questions
- **LLMEV-TP03-TC-096**: Mixed inputs -> ok=true, generates appropriate questions
- **LLMEV-TP03-TC-097**: Empty input folder -> ok=false, error "No files found"
- **LLMEV-TP03-TC-098**: Invalid schema JSON -> ok=false, error "Invalid schema"
- **LLMEV-TP03-TC-099**: Output JSON format -> ok=true, matches expected schema
- **LLMEV-TP03-TC-100**: Parallel question generation -> ok=true, workers=4
- **LLMEV-TP03-TC-101**: Question ID uniqueness -> ok=true, sequential IDs

### Category 6: Answer Generation (10 tests)

- **LLMEV-TP03-TC-102**: Questions file parsing -> ok=true, loads all questions
- **LLMEV-TP03-TC-103**: Context extraction -> ok=true, finds relevant text
- **LLMEV-TP03-TC-104**: Answer formatting -> ok=true, JSON with question_id, answer
- **LLMEV-TP03-TC-105**: Missing questions file -> ok=false, error "File not found"
- **LLMEV-TP03-TC-106**: Invalid questions JSON -> ok=false, error "Invalid JSON"
- **LLMEV-TP03-TC-107**: Empty transcriptions folder -> ok=false, error "No files"
- **LLMEV-TP03-TC-108**: Custom prompt override -> ok=true, uses custom prompt
- **LLMEV-TP03-TC-109**: Parallel answer generation -> ok=true, workers=4
- **LLMEV-TP03-TC-110**: Clear output folder -> ok=true, folder emptied
- **LLMEV-TP03-TC-111**: Output JSON schema -> ok=true, matches expected

### Category 7: LLM-as-Judge Evaluation (14 tests)

- **LLMEV-TP03-TC-112**: Score normalization (0-100) -> ok=true, scores in range
- **LLMEV-TP03-TC-113**: Rubric application -> ok=true, follows scoring criteria
- **LLMEV-TP03-TC-114**: Batch evaluation -> ok=true, processes all answers
- **LLMEV-TP03-TC-115**: Missing reference answers -> ok=false, error "No reference"
- **LLMEV-TP03-TC-116**: Invalid rubric -> ok=false, error "Invalid rubric"
- **LLMEV-TP03-TC-117**: Output JSON format -> ok=true, includes scores, feedback
- **LLMEV-TP03-TC-118**: Parallel evaluation -> ok=true, workers=4
- **LLMEV-TP03-TC-119**: Judge model selection -> ok=true, uses specified model
- **LLMEV-TP03-TC-120**: Custom judge prompt -> ok=true, uses custom prompt
- **LLMEV-TP03-TC-121**: Score aggregation -> ok=true, calculates avg, min, max
- **LLMEV-TP03-TC-122**: Feedback extraction -> ok=true, extracts judge comments
- **LLMEV-TP03-TC-123**: Empty answers folder -> ok=false, error "No files"
- **LLMEV-TP03-TC-124**: Incremental save -> ok=true, saves after each evaluation
- **LLMEV-TP03-TC-125**: Token usage tracking -> ok=true, logs input/output tokens

### Category 8: Cost Analysis (8 tests)

- **LLMEV-TP03-TC-126**: Token counting -> ok=true, accurate token counts
- **LLMEV-TP03-TC-127**: Price calculation -> ok=true, correct cost per model
- **LLMEV-TP03-TC-128**: Multiple pricing tiers -> ok=true, handles batch discounts
- **LLMEV-TP03-TC-129**: Prompt caching costs -> ok=true, includes cache rates
- **LLMEV-TP03-TC-130**: Extended thinking costs -> ok=true, includes thinking tokens
- **LLMEV-TP03-TC-131**: Vision processing fees -> ok=true, includes image costs
- **LLMEV-TP03-TC-132**: Output JSON format -> ok=true, includes breakdown
- **LLMEV-TP03-TC-133**: Missing pricing data -> ok=true, uses default rates

### Category 9: Hybrid Comparison (20 tests)

- **LLMEV-TP03-TC-134**: Levenshtein distance -> ok=true, accurate similarity
- **LLMEV-TP03-TC-135**: LLM judge integration -> ok=true, calls judge model
- **LLMEV-TP03-TC-136**: Section parsing -> ok=true, splits by <transcription_image>
- **LLMEV-TP03-TC-137**: Text section comparison -> ok=true, uses Levenshtein
- **LLMEV-TP03-TC-138**: Image section comparison -> ok=true, uses LLM judge
- **LLMEV-TP03-TC-139**: Combined score calculation -> ok=true, weighted average
- **LLMEV-TP03-TC-140**: Effort level wiring (gpt-4o) -> ok=true, temperature set
- **LLMEV-TP03-TC-141**: Effort level wiring (gpt-5-mini) -> ok=true, reasoning_effort set
- **LLMEV-TP03-TC-142**: Effort level wiring (claude-sonnet-4.5) -> ok=true, thinking budget set
- **LLMEV-TP03-TC-143**: max_tokens vs max_completion_tokens -> ok=true, correct param
- **LLMEV-TP03-TC-144**: Claude thinking budget constraint -> ok=true, max_tokens > budget
- **LLMEV-TP03-TC-145**: Grouped comparison -> ok=true, groups by source
- **LLMEV-TP03-TC-146**: Non-grouped comparison -> ok=true, pairwise comparison
- **LLMEV-TP03-TC-147**: Baseline comparison -> ok=true, compares to baseline file
- **LLMEV-TP03-TC-148**: Judge usage tracking -> ok=true, logs tokens, calls
- **LLMEV-TP03-TC-149**: Input files list -> ok=true, includes paths, sizes
- **LLMEV-TP03-TC-150**: Output JSON schema -> ok=true, matches spec
- **LLMEV-TP03-TC-151**: No images found -> ok=true, falls back to Levenshtein
- **LLMEV-TP03-TC-152**: Judge parse error -> ok=true, defaults to score=50
- **LLMEV-TP03-TC-153**: Custom judge prompt -> ok=true, uses custom prompt

### Category 10: Integration Tests (20 tests)

- **LLMEV-TP03-TC-154**: End-to-end: call-llm.py (image) -> ok=true, transcription saved
- **LLMEV-TP03-TC-155**: End-to-end: call-llm.py (text) -> ok=true, summary saved
- **LLMEV-TP03-TC-156**: End-to-end: call-llm-batch.py -> ok=true, all files processed
- **LLMEV-TP03-TC-157**: End-to-end: generate-questions.py -> ok=true, questions.json created
- **LLMEV-TP03-TC-158**: End-to-end: generate-answers.py -> ok=true, answers created
- **LLMEV-TP03-TC-159**: End-to-end: evaluate-answers.py -> ok=true, scores calculated
- **LLMEV-TP03-TC-160**: End-to-end: analyze-costs.py -> ok=true, costs calculated
- **LLMEV-TP03-TC-161**: End-to-end: compare-transcription-runs.py -> ok=true, comparison done
- **LLMEV-TP03-TC-162**: Pipeline: batch -> questions -> answers -> evaluate -> ok=true, full pipeline
- **LLMEV-TP03-TC-163**: Pipeline: batch (3 runs) -> compare -> ok=true, consistency check
- **LLMEV-TP03-TC-164**: Real API: gpt-4o smoke test -> ok=true, actual API call
- **LLMEV-TP03-TC-165**: Real API: gpt-5-mini smoke test -> ok=true, actual API call
- **LLMEV-TP03-TC-166**: Real API: claude-sonnet-4.5 smoke test -> ok=true, actual API call
- **LLMEV-TP03-TC-167**: Error recovery: crash during batch -> ok=true, resumes correctly
- **LLMEV-TP03-TC-168**: Error recovery: partial JSON -> ok=true, loads and continues
- **LLMEV-TP03-TC-169**: Concurrency: 8 workers, 100 files -> ok=true, no race conditions
- **LLMEV-TP03-TC-170**: Concurrency: thread safety -> ok=true, lock works
- **LLMEV-TP03-TC-171**: Performance: batch 100 images -> ok=true, completes in reasonable time
- **LLMEV-TP03-TC-172**: Performance: compare 100 files -> ok=true, completes in reasonable time
- **LLMEV-TP03-TC-173**: Memory: large files (10MB+) -> ok=true, no memory errors

### Category 11: CLI Parameter Validation (20 tests)

- **LLMEV-TP03-TC-174**: Missing required --model -> ok=false, error message
- **LLMEV-TP03-TC-175**: Missing required --input-file -> ok=false, error message
- **LLMEV-TP03-TC-176**: Invalid --workers value -> ok=false, error "must be positive"
- **LLMEV-TP03-TC-177**: Invalid --runs value -> ok=false, error "must be positive"
- **LLMEV-TP03-TC-178**: Invalid --temperature value -> ok=false, error "invalid effort level"
- **LLMEV-TP03-TC-179**: Invalid --reasoning-effort value -> ok=false, error "invalid effort level"
- **LLMEV-TP03-TC-180**: Invalid --output-length value -> ok=false, error "invalid effort level"
- **LLMEV-TP03-TC-181**: Invalid --method value -> ok=false, error "must be levenshtein, semantic, or hybrid"
- **LLMEV-TP03-TC-182**: Conflicting --input-folder and --files -> ok=false, error "use one or the other"
- **LLMEV-TP03-TC-183**: --judge-model required for hybrid -> ok=false, error message
- **LLMEV-TP03-TC-184**: --questions-file not found -> ok=false, error "file not found"
- **LLMEV-TP03-TC-185**: --schema-file not found -> ok=false, error "file not found"
- **LLMEV-TP03-TC-186**: --prompt-file not found -> ok=false, error "file not found"
- **LLMEV-TP03-TC-187**: --keys-file not found -> ok=false, error "file not found"
- **LLMEV-TP03-TC-188**: --output-file parent dir doesn't exist -> ok=true, creates dirs
- **LLMEV-TP03-TC-189**: --output-folder doesn't exist -> ok=true, creates folder
- **LLMEV-TP03-TC-190**: --clear-folder without confirmation -> ok=false, requires --force or prompt
- **LLMEV-TP03-TC-191**: Help text --help -> ok=true, displays usage
- **LLMEV-TP03-TC-192**: Version --version -> ok=true, displays version
- **LLMEV-TP03-TC-193**: All parameters combined -> ok=true, accepts all valid params

### Category 12: Edge Cases (20 tests)

- **LLMEV-TP03-TC-194**: Empty input file -> ok=true, logs warning, skips
- **LLMEV-TP03-TC-195**: Very large input file (100MB+) -> ok=true, processes or errors gracefully
- **LLMEV-TP03-TC-196**: Unicode filenames -> ok=true, handles correctly
- **LLMEV-TP03-TC-197**: Special characters in filenames -> ok=true, handles correctly
- **LLMEV-TP03-TC-198**: Symlinks in input folder -> ok=true, follows or skips
- **LLMEV-TP03-TC-199**: Hidden files (. prefix) -> ok=true, skips
- **LLMEV-TP03-TC-200**: Nested folders in input -> ok=false, error "use flat folder"
- **LLMEV-TP03-TC-201**: Duplicate filenames (different paths) -> ok=true, handles uniquely
- **LLMEV-TP03-TC-202**: Output file already exists -> ok=true, overwrites or errors based on --force
- **LLMEV-TP03-TC-203**: Disk full during write -> ok=false, error "disk full"
- **LLMEV-TP03-TC-204**: Permission denied on output -> ok=false, error "permission denied"
- **LLMEV-TP03-TC-205**: Corrupted JSON input -> ok=false, error "invalid JSON"
- **LLMEV-TP03-TC-206**: Malformed prompt file -> ok=true, uses as-is or errors
- **LLMEV-TP03-TC-207**: Empty prompt file -> ok=true, sends empty prompt or errors
- **LLMEV-TP03-TC-208**: Very long prompt (100K+ chars) -> ok=true, processes or errors
- **LLMEV-TP03-TC-209**: Binary file with text extension -> ok=true, errors or processes
- **LLMEV-TP03-TC-210**: Text file with image extension -> ok=false, error "invalid image"
- **LLMEV-TP03-TC-211**: Zero-byte file -> ok=true, logs warning, skips
- **LLMEV-TP03-TC-212**: File deleted during processing -> ok=true, logs error, continues
- **LLMEV-TP03-TC-213**: File modified during processing -> ok=true, uses original or errors

### Category 13: Output Schema Validation (20 tests)

- **LLMEV-TP03-TC-214**: call-llm.py JSON metadata -> ok=true, matches schema
- **LLMEV-TP03-TC-215**: call-llm-batch.py summary JSON -> ok=true, matches schema
- **LLMEV-TP03-TC-216**: generate-questions.py output -> ok=true, matches schema
- **LLMEV-TP03-TC-217**: generate-answers.py output -> ok=true, matches schema
- **LLMEV-TP03-TC-218**: evaluate-answers.py output -> ok=true, matches schema
- **LLMEV-TP03-TC-219**: analyze-costs.py output -> ok=true, matches schema
- **LLMEV-TP03-TC-220**: compare-transcription-runs.py output -> ok=true, matches schema
- **LLMEV-TP03-TC-221**: Hybrid comparison output -> ok=true, includes text/images breakdown
- **LLMEV-TP03-TC-222**: Judge usage tracking -> ok=true, includes tokens, calls, model
- **LLMEV-TP03-TC-223**: Input files list -> ok=true, includes path, size
- **LLMEV-TP03-TC-224**: Timestamp format -> ok=true, ISO 8601
- **LLMEV-TP03-TC-225**: Model ID in output -> ok=true, exact API model ID
- **LLMEV-TP03-TC-226**: Token usage in output -> ok=true, input/output tokens
- **LLMEV-TP03-TC-227**: Error messages in output -> ok=true, includes error field
- **LLMEV-TP03-TC-228**: Progress in output -> ok=true, includes completed/total
- **LLMEV-TP03-TC-229**: Worker ID in logs -> ok=true, 1-indexed
- **LLMEV-TP03-TC-230**: File paths in output -> ok=true, relative or absolute
- **LLMEV-TP03-TC-231**: Similarity scores -> ok=true, 0.0-1.0 range
- **LLMEV-TP03-TC-232**: Distance scores -> ok=true, non-negative
- **LLMEV-TP03-TC-233**: JSON pretty-printing -> ok=true, indented

### Category 14: Model-Specific Tests (20 tests)

- **LLMEV-TP03-TC-234**: gpt-3.5-turbo -> ok=true, correct params
- **LLMEV-TP03-TC-235**: gpt-4o -> ok=true, correct params
- **LLMEV-TP03-TC-236**: gpt-4.1 -> ok=true, correct params
- **LLMEV-TP03-TC-237**: gpt-5-mini -> ok=true, max_completion_tokens
- **LLMEV-TP03-TC-238**: gpt-5-pro -> ok=true, reasoning_effort=high only
- **LLMEV-TP03-TC-239**: o1-mini -> ok=true, reasoning_effort
- **LLMEV-TP03-TC-240**: o1-preview -> ok=true, reasoning_effort
- **LLMEV-TP03-TC-241**: o3-mini -> ok=true, reasoning_effort
- **LLMEV-TP03-TC-242**: claude-3.5-sonnet -> ok=true, temperature
- **LLMEV-TP03-TC-243**: claude-opus-4 -> ok=true, thinking budget
- **LLMEV-TP03-TC-244**: claude-sonnet-4.5 -> ok=true, thinking budget, max_tokens > budget
- **LLMEV-TP03-TC-245**: Unknown model ID -> ok=false, error "cannot detect provider"
- **LLMEV-TP03-TC-246**: Model with vision support -> ok=true, accepts image input
- **LLMEV-TP03-TC-247**: Model without vision support -> ok=false, error "no vision support"
- **LLMEV-TP03-TC-248**: Model with extended context -> ok=true, handles long prompts
- **LLMEV-TP03-TC-249**: Model with prompt caching -> ok=true, uses cache
- **LLMEV-TP03-TC-250**: Model with seed support -> ok=true, sets seed
- **LLMEV-TP03-TC-251**: Model without seed support -> ok=true, ignores seed param
- **LLMEV-TP03-TC-252**: Model pricing lookup -> ok=true, finds correct pricing
- **LLMEV-TP03-TC-253**: Model with batch API -> ok=true, uses batch pricing

### Category 15: Regression Tests (20 tests)

- **LLMEV-TP03-TC-254**: Judge prompt calibration (gpt-4o) -> ok=true, 75% case within tolerance
- **LLMEV-TP03-TC-255**: Judge prompt calibration (gpt-5-mini) -> ok=true, all cases within tolerance
- **LLMEV-TP03-TC-256**: Judge prompt calibration (claude-sonnet-4.5) -> ok=false, parse error (known issue)
- **LLMEV-TP03-TC-257**: Hybrid comparison (text identical, images different) -> ok=true, correct scores
- **LLMEV-TP03-TC-258**: Hybrid comparison (text different, images identical) -> ok=true, correct scores
- **LLMEV-TP03-TC-259**: Hybrid comparison (both identical) -> ok=true, exact_match=true
- **LLMEV-TP03-TC-260**: Hybrid comparison (both different) -> ok=true, low similarity
- **LLMEV-TP03-TC-261**: Effort level wiring (temperature models) -> ok=true, correct temp
- **LLMEV-TP03-TC-262**: Effort level wiring (reasoning models) -> ok=true, correct effort
- **LLMEV-TP03-TC-263**: Effort level wiring (thinking models) -> ok=true, correct budget
- **LLMEV-TP03-TC-264**: max_tokens vs max_completion_tokens fix -> ok=true, no 400 errors
- **LLMEV-TP03-TC-265**: Claude thinking budget constraint fix -> ok=true, no 400 errors
- **LLMEV-TP03-TC-266**: JSON parsing (extended thinking output) -> ok=false, parse error (known issue)
- **LLMEV-TP03-TC-267**: Grouped comparison mode -> ok=true, groups by source
- **LLMEV-TP03-TC-268**: Non-grouped comparison mode -> ok=true, pairwise
- **LLMEV-TP03-TC-269**: Section parsing (<transcription_image>) -> ok=true, correct split
- **LLMEV-TP03-TC-270**: Transcription notes in judge prompt -> ok=true, included
- **LLMEV-TP03-TC-271**: Config loading (model-registry.json) -> ok=true, loads correctly
- **LLMEV-TP03-TC-272**: Config loading (model-parameter-mapping.json) -> ok=true, loads correctly
- **LLMEV-TP03-TC-273**: Prefix matching (model registry) -> ok=true, finds correct entry

### Category 16: Performance Tests (14 tests)

- **LLMEV-TP03-TC-274**: Batch 10 files, 1 worker -> ok=true, baseline time
- **LLMEV-TP03-TC-275**: Batch 10 files, 4 workers -> ok=true, ~4x faster
- **LLMEV-TP03-TC-276**: Batch 10 files, 8 workers -> ok=true, ~8x faster
- **LLMEV-TP03-TC-277**: Batch 100 files, 16 workers -> ok=true, completes in reasonable time
- **LLMEV-TP03-TC-278**: Memory usage (100 files) -> ok=true, < 1GB RAM
- **LLMEV-TP03-TC-279**: Memory usage (large files) -> ok=true, no memory leaks
- **LLMEV-TP03-TC-280**: Incremental save overhead -> ok=true, minimal impact
- **LLMEV-TP03-TC-281**: Atomic write overhead -> ok=true, minimal impact
- **LLMEV-TP03-TC-282**: Lock contention (16 workers) -> ok=true, no deadlocks
- **LLMEV-TP03-TC-283**: API rate limiting -> ok=true, respects limits
- **LLMEV-TP03-TC-284**: Retry backoff timing -> ok=true, 1s, 2s, 4s delays
- **LLMEV-TP03-TC-285**: Progress logging frequency -> ok=true, not too verbose
- **LLMEV-TP03-TC-286**: JSON parsing performance -> ok=true, fast enough
- **LLMEV-TP03-TC-287**: File I/O performance -> ok=true, fast enough

## 7. Test Phases

Ordered execution sequence:

1. **Phase 1: Setup** - Create test fixtures, mock API clients
2. **Phase 2: Unit Tests** - Test individual functions (TC-001 to TC-065)
3. **Phase 3: Integration Tests** - Test script execution with mocks (TC-066 to TC-153)
4. **Phase 4: End-to-End Tests** - Test full pipelines (TC-154 to TC-173)
5. **Phase 5: Smoke Tests** - Real API calls (TC-164 to TC-166)
6. **Phase 6: Regression Tests** - Verify known issues fixed (TC-254 to TC-273)
7. **Phase 7: Performance Tests** - Measure speed and resource usage (TC-274 to TC-287)
8. **Phase 8: Cleanup** - Remove test outputs, restore state

## 8. Helper Functions

```python
def run_script(script_name, args, cwd=None):
    """Run a script with arguments and return output"""
    import subprocess
    cmd = ["python", script_name] + args
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result

def assert_json_schema(json_data, schema):
    """Validate JSON against schema"""
    import jsonschema
    jsonschema.validate(instance=json_data, schema=schema)

def assert_file_exists(path):
    """Assert file exists"""
    assert Path(path).exists(), f"File not found: {path}"

def assert_json_field(json_data, field, expected):
    """Assert JSON field equals expected value"""
    actual = json_data.get(field)
    assert actual == expected, f"Expected {field}={expected}, got {actual}"

def create_test_image(path, size_kb=100):
    """Create a test image file"""
    from PIL import Image
    import io
    img = Image.new('RGB', (800, 600), color='red')
    img.save(path)

def create_test_text(path, content="Test content"):
    """Create a test text file"""
    Path(path).write_text(content, encoding='utf-8')

def mock_api_response(provider, model, response_text):
    """Create a mock API response"""
    if provider == 'openai':
        return {
            "choices": [{"message": {"content": response_text}}],
            "usage": {"prompt_tokens": 100, "completion_tokens": 50}
        }
    elif provider == 'anthropic':
        return {
            "content": [{"text": response_text}],
            "usage": {"input_tokens": 100, "output_tokens": 50}
        }
```

## 9. Cleanup

- Remove `test_output/` folder
- Remove `test_fixtures/` generated files
- Restore original config files if modified
- Clear any cached API responses

## 10. Verification Checklist

### Coverage Verification
- [ ] All 287 test cases executed
- [ ] All 9 model types tested
- [ ] All 6 effort levels tested
- [ ] All 11 file types tested
- [ ] All 3 comparison methods tested
- [ ] All 4 worker counts tested
- [ ] All 8 error conditions tested
- [ ] Code coverage >= 95%

### Script-Specific Verification
- [ ] call-llm.py: All parameters tested
- [ ] call-llm-batch.py: Concurrency verified
- [ ] generate-questions.py: Schema validation verified
- [ ] generate-answers.py: Context extraction verified
- [ ] evaluate-answers.py: Scoring verified
- [ ] analyze-costs.py: Pricing verified
- [ ] compare-transcription-runs.py: Hybrid mode verified

### Quality Verification
- [ ] No flaky tests (all deterministic)
- [ ] No test data leakage
- [ ] All mocks realistic
- [ ] All edge cases covered
- [ ] All error messages clear
- [ ] All JSON schemas validated
- [ ] All performance benchmarks met
- [ ] All regression tests pass

### Documentation Verification
- [ ] Test plan complete
- [ ] All test cases documented
- [ ] All helper functions documented
- [ ] All fixtures documented
- [ ] All known issues documented

## 11. Document History

**[2026-01-24 22:52]**
- Initial comprehensive test plan created
- 287 test cases covering all combinations
- 16 test categories defined
- 8 test phases outlined
