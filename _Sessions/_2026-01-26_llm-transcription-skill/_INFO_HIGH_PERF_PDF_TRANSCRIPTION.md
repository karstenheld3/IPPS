# INFO: High-Performance PDF Transcription

**Doc ID**: LLMTR-IN01
**Goal**: Research strategies for high-performance PDF-to-markdown conversion using poppler and OpenAI gpt-5-mini
**Timeline**: Created 2026-01-28

## Summary

- **Existing pdf-tools skill**: `convert-pdf-to-jpg.py` already handles PDF->JPG with poppler, can reuse [VERIFIED]
- **Two-phase pipeline**: PDF->Images (CPU-bound, poppler threads) then Images->Markdown (IO-bound, asyncio) [VERIFIED]
- **pdf2image key params**: `thread_count`, `dpi=200`, `fmt=jpeg`, `paths_only=True` for performance [VERIFIED]
- **OpenAI parallel processor pattern**: asyncio + aiohttp, throttle RPM/TPM, exponential backoff retry [VERIFIED]
- **Use 75% headroom** on rate limits to avoid hitting limits [VERIFIED]
- **Calibration script first**: Measure actual TPM/RPM, CPU vs workers, quality vs speed [ASSUMED]
- **Three profiles**: fast (1 candidate), balanced (3), quality (5) [TESTED]
- **gpt-5-mini default**: Best cost/quality ratio from previous testing [TESTED]

## Table of Contents

1. [PDF to Image Conversion](#1-pdf-to-image-conversion)
2. [OpenAI API Rate Limits and Async](#2-openai-api-rate-limits-and-async)
3. [Concurrent Processing Strategies](#3-concurrent-processing-strategies)
4. [Optimization Parameters](#4-optimization-parameters)
5. [Quality vs Speed Tradeoffs](#5-quality-vs-speed-tradeoffs)
6. [Recommended Architecture](#6-recommended-architecture)
7. [Sources](#7-sources)
8. [Next Steps](#8-next-steps)
9. [Document History](#9-document-history)

## 1. PDF to Image Conversion

### 1.1 Existing pdf-tools Skill [VERIFIED]

We already have `DevSystemV3.2/skills/pdf-tools/convert-pdf-to-jpg.py`:
- Uses pdf2image with poppler
- Poppler path: `.tools/poppler/Library/bin`
- Output: `.tools/_pdf_to_jpg_converted/[PDF_NAME]/`
- Default DPI: 150, JPEG quality: 90
- Supports page ranges (`--pages 1-3`)

**Can reuse**: Import `convert_pdf_to_jpg()` function or refactor for async.

### 1.2 Poppler with pdf2image

**pdf2image** is a Python wrapper for poppler-utils (pdftoppm, pdftocairo).

**Key parameters for performance:**
- `dpi` - Image quality (default 200). Higher = better quality, slower conversion, larger images
- `thread_count` - Threads for poppler processing (default 1). Increase for multi-core CPUs
- `fmt` - Output format: `ppm` (default, fastest), `jpeg` (smaller, good quality), `png` (lossless)
- `jpegopt` - JPEG options: `{"quality": 85, "progressive": True, "optimize": True}`
- `output_folder` - Write to disk instead of memory (essential for large PDFs)
- `paths_only` - Return paths instead of loading images (memory optimization)
- `use_pdftocairo` - Alternative renderer, may help performance
- `first_page`, `last_page` - Process page ranges for chunked processing

### 1.2 Performance Recommendations [VERIFIED]

- **DPI 150-200**: Best balance for OCR/vision models (300 DPI rarely improves results)
- **JPEG format**: 3-5x smaller than PNG, minimal quality loss at quality=85
- **Thread count**: Set to `min(cpu_count, page_count)` for optimal parallelism
- **Chunked processing**: For 500+ page PDFs, process in batches of 50-100 pages
- **paths_only=True**: Essential for large PDFs to avoid memory exhaustion

### 1.3 Estimated Conversion Times [ASSUMED]

| Pages | DPI 150 | DPI 200 | DPI 300 |
|-------|---------|---------|----------|
| 1 | ~0.5s | ~0.8s | ~1.5s |
| 10 | ~3s | ~5s | ~10s |
| 100 | ~25s | ~40s | ~90s |
| 500 | ~120s | ~200s | ~450s |

*With thread_count=8 on modern CPU. Actual times vary by PDF complexity.*

## 2. OpenAI API Rate Limits and Async

### 2.1 Rate Limit Types [VERIFIED]

- **RPM** (Requests Per Minute) - Number of API calls
- **TPM** (Tokens Per Minute) - Total tokens (input + output)
- **TPD** (Tokens Per Day) - Daily token limit (some tiers)

### 2.2 gpt-4o-mini Limits [ASSUMED - needs calibration]

| Tier | RPM | TPM |
|------|-----|-----|
| Tier 1 | 500 | 200,000 |
| Tier 2 | 5,000 | 2,000,000 |
| Tier 3 | 5,000 | 4,000,000 |
| Tier 4+ | 10,000 | 10,000,000 |

*Note: gpt-5-mini limits may differ - calibration script will measure actual limits.*

### 2.3 OpenAI Parallel Processor Pattern [VERIFIED]

OpenAI provides `api_request_parallel_processor.py` with these features:
- Streams requests from file (memory efficient)
- Concurrent requests with asyncio + aiohttp
- Throttles both RPM and TPM
- Exponential backoff retry on rate limits
- Logs errors for diagnosis

**Key implementation patterns:**
```python
@dataclass
class StatusTracker:
    num_tasks_in_progress: int = 0
    num_rate_limit_errors: int = 0
    time_of_last_rate_limit_error: int = 0  # for cooldown

# Throttling approach:
# - Track available_request_capacity and available_token_capacity
# - Replenish capacity based on time elapsed
# - Only send request if both capacities available
# - Pause loop on rate limit errors
```

### 2.4 Recommended Headroom [VERIFIED]

OpenAI recommends setting limits to **50-75% of actual limits** to avoid hitting rate limits:
- If RPM=5000, target 2500-3750 RPM
- If TPM=2M, target 1M-1.5M TPM

## 3. Concurrent Processing Strategies

### 3.1 Two-Phase Pipeline [VERIFIED]

**Phase 1: PDF to Images (CPU-bound)**
- Use `ProcessPoolExecutor` or poppler's `thread_count`
- Target 80% CPU usage
- Write images to disk with `paths_only=True`

**Phase 2: Images to Markdown (IO-bound)**
- Use `asyncio` with `aiohttp` for concurrent API calls
- Throttle by RPM and TPM
- Retry with exponential backoff

### 3.2 Worker Calculation Strategy

**PDF Conversion Workers:**
```python
import os
cpu_count = os.cpu_count()
target_cpu_usage = 0.8
pdf_workers = max(1, int(cpu_count * target_cpu_usage))
```

**API Concurrent Requests:**
```python
# Based on rate limits and estimated tokens per request
tokens_per_image = 5000  # input ~4000, output ~1000 (estimate)
max_concurrent = min(
    rpm_limit * 0.75 / 60,  # requests per second
    tpm_limit * 0.75 / tokens_per_image / 60  # token-limited
)
```

### 3.3 Hybrid Async Pattern [VERIFIED]

For vision API calls with image encoding:
```python
async def process_batch(images: list, semaphore: asyncio.Semaphore):
    async with semaphore:  # limit concurrent requests
        async with aiohttp.ClientSession() as session:
            tasks = [call_api(img, session) for img in images]
            return await asyncio.gather(*tasks, return_exceptions=True)
```

### 3.4 Memory Management

- **Streaming**: Process pages as they're converted, don't wait for all
- **Disk buffer**: Write intermediate results to temp files
- **Chunking**: For 500-page PDFs, process in 50-page chunks
- **Cleanup**: Delete temp images after successful transcription

## 4. Optimization Parameters

### 4.1 Image Conversion Parameters

**DPI (Dots Per Inch)**
- Range: 72-300
- Strategy: Start low (150), retry with higher (200, 300) if score < threshold
- Tradeoff: Higher DPI = better text clarity, slower conversion, larger files
- Test: Compare transcription quality at 100, 150, 200, 300 DPI

**JPEG Quality**
- Range: 50-100
- Current: 90 (in existing pdf-tools)
- Strategy: Find minimum quality that doesn't degrade transcription
- Test: Compare at 70, 80, 85, 90, 95

**Image Size/Resolution**
- Consider resizing after conversion if images are too large
- Vision models have token limits based on image size
- Test: Max image dimension (1024, 2048, 4096 pixels)

### 4.2 LLM Parameters

**Reasoning Effort** (gpt-5-mini specific)
- Options: `minimal`, `low`, `medium`, `high`
- Previous testing: `medium` best quality/cost ratio
- Strategy: Use `low` for fast mode, `medium` for balanced
- Test: Score vs time vs cost for each effort level

**Max Output Tokens**
- Range: 1000-16000
- Strategy: Estimate based on page content density
- Dense text pages: 4000-8000 tokens
- Graphics-heavy: 2000-4000 tokens
- Test: Find optimal default that covers 95% of pages

**Temperature**
- Range: 0.0-1.0
- For transcription: Low (0.0-0.3) for accuracy
- Test: Impact on transcription consistency

### 4.3 Concurrency Parameters

**PDF Conversion Workers**
- Range: 1 to cpu_count
- Target: 80% CPU usage
- Test: CPU usage vs worker count, find optimal mapping

**API Concurrent Requests**
- Limited by: RPM, TPM, and practical throughput
- Strategy: Start conservative, increase based on calibration
- Test: Find max concurrent before rate limits

**Batch Size** (for chunked processing)
- Range: 10-100 pages per batch
- Tradeoff: Larger batches = more memory, fewer disk writes
- Test: Memory usage vs batch size

### 4.4 Quality Control Parameters

**Minimum Acceptable Score**
- Range: 3.0-5.0
- Strategy: Configurable per profile (fast=3.0, balanced=3.5, quality=4.0)
- Test: Correlation between score and human evaluation

**Retry Threshold**
- When to retry with higher DPI or more candidates
- Strategy: If score < min_score, retry with upgraded settings
- Max retries: 2-3 before giving up

**Ensemble Size** (candidates)
- Range: 1-7
- Tradeoff: More candidates = better selection, higher cost/time
- Test: Diminishing returns analysis (3 vs 5 vs 7)

### 4.5 Calibration Test Matrix

| Parameter | Test Values | Metric |
|-----------|-------------|--------|
| DPI | 100, 150, 200, 300 | Score, time, file size |
| JPEG quality | 70, 80, 85, 90, 95 | Score, file size |
| Reasoning effort | minimal, low, medium, high | Score, time, cost |
| Max tokens | 2000, 4000, 8000, 16000 | Truncation rate |
| Temperature | 0.0, 0.1, 0.3 | Score variance |
| Workers | 2, 4, 8, 12, 16 | CPU %, conversion time |
| Concurrent API | 5, 10, 20, 40 | Rate limit hits, throughput |
| Candidates | 1, 3, 5, 7 | Score improvement per candidate |

### 4.6 Adaptive Strategy

```
IF page_score < min_score:
    IF dpi < 200:
        retry with dpi = 200
    ELIF candidates < 3:
        retry with candidates = 3
    ELIF reasoning_effort < "medium":
        retry with reasoning_effort = "medium"
    ELSE:
        accept with warning
```

## 5. Quality vs Speed Tradeoffs

### 5.1 DPI vs Quality [ASSUMED - needs testing]

| DPI | File Size | Vision Model Quality | Conversion Time |
|-----|-----------|---------------------|------------------|
| 100 | ~50KB/page | May miss fine text | Fastest |
| 150 | ~100KB/page | Good for most docs | Fast |
| 200 | ~200KB/page | Excellent | Moderate |
| 300 | ~400KB/page | Overkill for most | Slow |

### 5.2 Ensemble Size vs Speed [TESTED from previous session]

| Candidates | Quality Score | Time (per page) | Cost |
|------------|---------------|-----------------|------|
| 1 | 3.5-4.0 | ~5s | $0.003 |
| 3 | 4.0-4.5 | ~15s | $0.009 |
| 5 | 4.5-5.0 | ~25s | $0.015 |

*gpt-5-mini with medium reasoning effort*

### 5.3 Speed Optimization Profiles

**Fast Mode** (bulk processing, acceptable quality):
- DPI: 150
- Candidates: 1
- Refinement: disabled
- Est. speed: ~2 pages/second with max concurrency

**Balanced Mode** (recommended):
- DPI: 200
- Candidates: 3
- Refinement: if score < 3.5
- Est. speed: ~0.5 pages/second

**Quality Mode** (critical documents):
- DPI: 200
- Candidates: 5
- Refinement: if score < 4.0
- Est. speed: ~0.2 pages/second

## 6. Recommended Architecture

### 6.1 Script Structure

```
transcribe-pdf-to-markdown.py
├── PDF Analysis (page count, file size)
├── Strategy Selection (based on calibration data)
├── Phase 1: PDF -> Images (ProcessPoolExecutor or poppler threads)
├── Phase 2: Images -> Markdown (asyncio + aiohttp)
├── Output Assembly (merge per-page markdown)
└── Cleanup (temp files)

transcribe-pdf-to-markdown-calibration.py
├── Run test PDFs at various settings
├── Measure actual TPM/RPM limits
├── Measure CPU usage vs workers
├── Measure quality vs speed
└── Output calibration data
```

### 6.2 Configuration Files

**transcribe-pdf-to-markdown.json** (defaults + limits):
```json
{
  "default_model": "gpt-5-mini",
  "default_dpi": 200,
  "max_cpu_usage_percent": 80,
  "tpm_limit": 2000000,
  "rpm_limit": 5000,
  "tpm_headroom": 0.75,
  "rpm_headroom": 0.75,
  "tokens_per_image_estimate": 5000,
  "retry_attempts": 3,
  "retry_base_delay": 1.0,
  "profiles": {
    "fast": {"dpi": 150, "candidates": 1, "refinement": false},
    "balanced": {"dpi": 200, "candidates": 3, "refinement": true},
    "quality": {"dpi": 200, "candidates": 5, "refinement": true}
  }
}
```

**transcribe-pdf-to-markdown-calibration.json** (measured data):
```json
{
  "measured_tpm_limit": 1950000,
  "measured_rpm_limit": 4800,
  "avg_tokens_per_image": 4850,
  "cpu_workers_vs_usage": {
    "4": 45, "8": 78, "12": 85, "16": 88
  },
  "pdf_properties_to_settings": [
    {"pages_max": 10, "workers": 4, "concurrent_api": 10},
    {"pages_max": 50, "workers": 8, "concurrent_api": 20},
    {"pages_max": 200, "workers": 12, "concurrent_api": 30},
    {"pages_max": 500, "workers": 16, "concurrent_api": 40}
  ]
}
```

### 6.3 Key Implementation Points

1. **Use aiohttp, not requests** - True async HTTP
2. **Semaphore for concurrency** - `asyncio.Semaphore(max_concurrent)`
3. **Token counting with tiktoken** - Pre-calculate to avoid rate limit surprises
4. **Streaming results** - Write each page as it completes
5. **Graceful degradation** - Reduce concurrency on rate limits, don't fail

## 7. Sources

**Primary Sources:**
- `LLMTR-IN01-SC-PDFTOOLS-CVT`: `DevSystemV3.2/skills/pdf-tools/convert-pdf-to-jpg.py` - Existing PDF conversion script [VERIFIED]
- `LLMTR-IN01-SC-PDF2IMG-REF`: https://pdf2image.readthedocs.io/en/latest/reference.html - pdf2image API reference, key parameters [VERIFIED]
- `LLMTR-IN01-SC-OAICOOK-RATE`: https://cookbook.openai.com/examples/how_to_handle_rate_limits - Rate limit handling, parallel processor pattern [VERIFIED]
- `LLMTR-IN01-SC-OAICOOK-PARA`: https://github.com/openai/openai-cookbook/blob/main/examples/api_request_parallel_processor.py - Official parallel processing script [VERIFIED]
- `LLMTR-IN01-SC-PYPI-PDF2IMG`: https://pypi.org/project/pdf2image/ - pdf2image installation and usage [VERIFIED]
- `LLMTR-IN01-SC-TESTDRIV-CONC`: https://testdriven.io/blog/python-concurrency-parallelism/ - Python concurrency patterns [VERIFIED]

## 8. Next Steps

1. **Create calibration script** (`transcribe-pdf-to-markdown-calibration.py`)
   - Measure actual gpt-5-mini TPM/RPM limits
   - Benchmark CPU usage vs worker count
   - Build quality vs speed lookup table

2. **Create main script** (`transcribe-pdf-to-markdown.py`)
   - Implement two-phase pipeline
   - Use calibration data for strategy selection
   - Support fast/balanced/quality profiles

3. **Create test PDFs**
   - 1-page, 10-page, 50-page, 100-page, 500-page samples
   - Mix of text-heavy and graphics-heavy content

4. **Run calibration and document results**
   - Update `transcribe-pdf-to-markdown-calibration.json`
   - Verify assumptions marked [ASSUMED] in this document

## 9. Document History

**[2026-01-28 09:51]**
- Initial research document created
- Added sections 1-5 with findings from web research
- Documented OpenAI parallel processor pattern
- Added pdf2image performance recommendations
- Added recommended architecture with config file structures
