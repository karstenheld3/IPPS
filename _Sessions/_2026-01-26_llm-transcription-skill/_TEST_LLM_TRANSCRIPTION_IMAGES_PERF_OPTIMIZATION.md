# TEST: Image Transcription Performance Optimization

**Doc ID (TDID)**: LLMTR-TP02
**Feature**: image-transcription-perf-optimization
**Goal**: Define test plan for measuring performance impact of each optimization variant
**Timeline**: Created 2026-02-06
**Target file**: `_PrivateSessions/_2026-01-31_MarkdownTestTranscriptions/05_PerformanceTesting/`

**Depends on:**
- `_SPEC_LLM_TRANSCRIPTION_IMAGES_PERF_OPTIMIZATION.md [LLMTR-SP02]` for variant definitions and success criteria

## MUST-NOT-FORGET

- All variants use identical test parameters: 20 workers, gpt-5-mini, 2 candidates, min-score 3.5
- Prompt files: `_Sessions/_2026-01-26_llm-transcription-skill/_input/llm-image-to-markdown-transcription-v1b.md` and `llm-image-to-markdown-judge-v1d.md`
- API keys: `E:\Dev\IPPS\..\.api-keys.txt`
- Config dir: `.windsurf/skills/llm-transcription/` (model-registry.json, model-parameter-mapping.json, model-pricing.json)
- >10% wall-clock improvement threshold for "winner" status
- Quality must not regress: avg score delta must be < 0.1 vs baseline
- Each variant outputs to its own numbered subfolder
- `h2` package must be installed for v4_http2 variant

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

Performance benchmark of 6 script variants (1 baseline + 5 optimizations) processing 159 images from the Axpo Annual Report 2023. Each variant is run with identical parameters and the wall-clock time, token usage, cost, and quality scores are compared.

## 2. Scenario

**Problem:** Need to measure whether each proposed optimization actually improves performance, and by how much, before merging into production script.

**Solution:** Run each variant on the same image set with identical parameters, capture structured results, compare automatically.

**What we don't want:**
- Running variants concurrently so they interfere with each other's rate limits
- Comparing runs with different parameters or image sets
- Accepting performance gains that degrade transcription quality
- Manual timing (everything captured in JSON)

## 3. Test Strategy

**Approach**: Automated benchmark via `run_perf_tests.py` test runner

**Execution modes:**
- **Sequential** (default): Run variants one at a time. Cleanest measurement, no rate limit interference.
- **Parallel** (`--parallel N`): Run N variants simultaneously. Faster but may skew results due to shared rate limits.

**Measurement methodology:**
- Wall-clock time: Python `time.perf_counter()` around entire batch
- Per-image time: Already tracked by script (`elapsed_seconds` per result)
- Tokens: Sum from API responses
- Cost: Calculated from model-pricing.json
- Quality: Average `final_score` across all images

**Success criteria per variant:**
- `(baseline_wall_clock - variant_wall_clock) / baseline_wall_clock >= 0.10` (>10% faster)
- `abs(baseline_avg_score - variant_avg_score) < 0.1` (quality preserved)

## 4. Test Priority Matrix

### MUST TEST (Critical)

- **v0_baseline.py** - Establishes reference point for all comparisons
  - Testability: **EASY**, Effort: Low
  - Must complete successfully to validate test infrastructure

- **v3_single_loop.py** - Highest expected impact (eliminates per-image loop + thread pool)
  - Testability: **EASY**, Effort: Low
  - Most architectural change, most likely to show >10%

- **v5_prompt_cache.py** - Orthogonal optimization, reduces API latency directly
  - Testability: **EASY**, Effort: Low
  - Tests API-level caching, independent of transport

### SHOULD TEST (Important)

- **v1_async_http.py** - Foundation for v2-v4 chain
  - Testability: **EASY**, Effort: Low

- **v2_persistent_client.py** - Connection reuse measurement
  - Testability: **EASY**, Effort: Low

- **v4_http2.py** - HTTP/2 multiplexing measurement
  - Testability: **MEDIUM**, Effort: Low (requires h2 package)

### DROP (Not Worth Testing Separately)

- None. All 6 variants are tested.

## 5. Test Data

**Source images:**
- Location: `_PrivateSessions/_2026-01-31_MarkdownTestTranscriptions/05_PerformanceTesting/01_source_images/`
- Count: 159 JPG images (Axpo-Annual-Report-2023-Financial-Report pages 1-159)
- Size range: ~74KB to ~470KB per image

**Prompt files:**
- Transcription: `E:\Dev\IPPS\_Sessions\_2026-01-26_llm-transcription-skill\_input\llm-image-to-markdown-transcription-v1b.md`
- Judge: `E:\Dev\IPPS\_Sessions\_2026-01-26_llm-transcription-skill\_input\llm-image-to-markdown-judge-v1d.md`

**API keys:**
- File: `E:\Dev\IPPS\..\.api-keys.txt`

**Config files:**
- Directory: `E:\Dev\IPPS\.windsurf\skills\llm-transcription\`
- Files: `model-registry.json`, `model-parameter-mapping.json`, `model-pricing.json`

**Output structure:**
```
05_PerformanceTesting/
├── 01_source_images/              # 159 source images
├── 02_v0_baseline/                # Baseline output + _run_results.json
├── 03_v1_async_http/              # v1 output + _run_results.json
├── 04_v2_persistent_client/       # v2 output + _run_results.json
├── 05_v3_single_loop/             # v3 output + _run_results.json
├── 06_v4_http2/                   # v4 output + _run_results.json
├── 07_v5_prompt_cache/            # v5 output + _run_results.json
├── 08_v_combined/                 # Combined winner output + _run_results.json
├── scripts/                       # All variant scripts + test runner
│   ├── v0_baseline.py
│   ├── v1_async_http.py
│   ├── v2_persistent_client.py
│   ├── v3_single_loop.py
│   ├── v4_http2.py
│   ├── v5_prompt_cache.py
│   ├── v_combined.py
│   └── run_perf_tests.py
└── _performance_results.json      # Final comparison
```

**Setup:**
```
pip install httpx h2
```

## 6. Test Cases

### Category 1: Infrastructure Validation (3 tests)

- **LLMTR-TC-20**: All 6 variant scripts run with `--help` without errors -> ok=true, exit code 0
- **LLMTR-TC-21**: v0_baseline processes 1 image successfully -> ok=true, output .md file created, _run_results.json contains valid PerformanceResult
- **LLMTR-TC-22**: run_perf_tests.py `--help` shows usage -> ok=true, lists all variants
- **LLMTR-TC-22b**: `import h2` succeeds in venv -> ok=true, required for v4_http2 (skip v4 if fails)

### Category 2: Baseline Benchmark (2 tests)

- **LLMTR-TC-23**: v0_baseline processes all 159 images with 20 workers, 2 candidates -> ok=true, _run_results.json written with wall_clock_seconds, avg_score, images_processed=159 (or close)
- **LLMTR-TC-24**: v0_baseline avg_score >= 3.5 -> ok=true, confirms quality baseline is reasonable

### Category 3: Variant Benchmarks (5 tests)

- **LLMTR-TC-25**: v1_async_http processes all 159 images, _run_results.json valid -> ok=true
- **LLMTR-TC-26**: v2_persistent_client processes all 159 images, _run_results.json valid -> ok=true
- **LLMTR-TC-27**: v3_single_loop processes all 159 images, _run_results.json valid -> ok=true
- **LLMTR-TC-28**: v4_http2 processes all 159 images, _run_results.json valid -> ok=true
- **LLMTR-TC-29**: v5_prompt_cache processes all 159 images, _run_results.json valid -> ok=true

### Category 4: Performance Analysis (3 tests)

- **LLMTR-TC-30**: At least one variant shows >10% wall-clock improvement vs baseline -> ok=true
- **LLMTR-TC-31**: No variant has avg_score regression >0.1 vs baseline -> ok=true, _performance_results.json includes `quality_regression: true/false` per variant
- **LLMTR-TC-32**: _performance_results.json created with comparison table and winners list -> ok=true

### Category 5: Combined Script (2 tests)

- **LLMTR-TC-33**: v_combined processes all 159 images, _run_results.json valid -> ok=true
- **LLMTR-TC-34**: v_combined shows >10% improvement vs baseline AND avg_score within 0.1 of baseline -> ok=true

## 7. Test Phases

1. **Phase 1: Setup** - Install h2 package, verify prompt/config files exist, create output folders
2. **Phase 2: Infrastructure** - Run TC-20 through TC-22 (--help checks, single image test)
3. **Phase 3: Baseline** - Run TC-23, TC-24 (full baseline benchmark)
4. **Phase 4: Variants** - Run TC-25 through TC-29 (all 5 optimization benchmarks)
5. **Phase 5: Analysis** - Run TC-30 through TC-32 (compare results, identify winners)
6. **Phase 6: Combined** - Run TC-33, TC-34 (build and test combined winner)
7. **Phase 7: Cleanup** - Archive results, no temp file cleanup (all results preserved)

## 8. Helper Functions

```python
def load_run_results(variant_dir: Path) -> dict:
    """Load _run_results.json from variant output directory."""

def compare_variants(baseline: dict, variant: dict) -> dict:
    """Compare variant vs baseline, return improvement_pct and quality_delta."""

def is_winner(comparison: dict) -> bool:
    """Return True if improvement_pct >= 10.0 and quality_delta < 0.1."""

def build_comparison_table(results: list[dict]) -> dict:
    """Build _performance_results.json from all variant results."""
```

## 9. Cleanup

- All output folders and results are preserved (performance data is the deliverable)
- No temp files to clean up (scripts handle their own temp cleanup)
- Scripts in `scripts/` folder are preserved as artifacts

## 10. Verification Checklist

- [ ] All 6 variant scripts pass --help check (TC-20)
- [ ] Baseline completes successfully (TC-23, TC-24)
- [ ] All 5 optimization variants complete (TC-25 through TC-29)
- [ ] Performance comparison generated (TC-30, TC-31, TC-32)
- [ ] Combined script tested if winners exist (TC-33, TC-34)
- [ ] All results preserved in output folders
- [ ] _performance_results.json contains complete comparison

## 11. Document History

**[2026-02-06 03:10]**
- Reconciled: Added TC-22b for h2 import pre-check
- Reconciled: TC-31 now specifies quality_regression field in output
- Reconciled: TC-34 clarified quality check

**[2026-02-06 02:55]**
- Initial test plan created
