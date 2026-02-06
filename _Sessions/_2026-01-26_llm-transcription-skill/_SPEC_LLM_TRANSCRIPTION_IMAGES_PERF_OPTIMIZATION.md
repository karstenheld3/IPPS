# SPEC: Image Transcription Performance Optimization

**Doc ID (TDID)**: LLMTR-SP02
**Feature**: image-transcription-perf-optimization
**Goal**: Specify performance optimizations for transcribe-image-to-markdown.py, each testable in isolation
**Timeline**: Created 2026-02-06
**Target file**: `.windsurf/skills/llm-transcription/transcribe-image-to-markdown.py`

**Depends on:**
- `_SPEC_LLM_TRANSCRIPTION_IMAGES.md [LLMTR-SP01]` for base script architecture

## MUST-NOT-FORGET

- Each optimization must be testable in isolation as a standalone script variant
- Only optimizations showing >10% wall-clock improvement survive to combined version
- All variants must produce identical output quality (avg score must not regress >0.1)
- Test params: 20 workers, gpt-5-mini, 2 candidates per image
- Source: DevSystemV3.2 is source, .windsurf is sync target
- gpt-5 models require `max_completion_tokens` not `max_tokens`
- Prompt files: `_Sessions/_2026-01-26_llm-transcription-skill/_input/llm-image-to-markdown-transcription-v1b.md` and `llm-image-to-markdown-judge-v1d.md`

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Design Decisions](#5-design-decisions)
6. [Implementation Guarantees](#6-implementation-guarantees)
7. [Key Mechanisms](#7-key-mechanisms)
8. [Optimization Variants](#8-optimization-variants)
9. [Data Structures](#9-data-structures)
10. [Document History](#10-document-history)

## 1. Scenario

**Problem:** The current `transcribe-image-to-markdown.py` uses synchronous HTTP calls wrapped in asyncio executors, creates a new TCP+TLS connection per API call, and runs a separate event loop per image. For batch processing of 159 images with 20 workers and 2 candidates each, these overheads accumulate significantly.

**Solution:**
- Identify 5 independent optimization axes
- Create one script variant per optimization, each changing exactly one thing
- Benchmark all variants against unmodified baseline
- Merge only optimizations with >10% proven wall-clock improvement

**What we don't want:**
- Changing multiple things in one variant (confounds measurement)
- Optimizations that degrade transcription quality
- Premature combination without isolated proof
- Hardcoded test parameters (variants must remain general-purpose scripts)

## 2. Context

The script processes images through an ensemble pipeline: N transcriptions -> N judge evaluations -> select best -> optional refinement. For each image with 2 candidates, that is 4+ API calls (2 transcribe + 2 judge + potential refinement). With 159 images and 20 workers, the batch makes 636+ API calls.

Current architecture bottlenecks:
- `call_openai_vision()` / `call_anthropic_vision()` create a new `httpx.Client` per call (new TCP+TLS handshake each time)
- `generate_transcription_async()` uses `loop.run_in_executor()` wrapping sync HTTP (thread overhead)
- `process_single_image()` calls `asyncio.run()` per image (event loop creation overhead)
- No HTTP/2 multiplexing (each request waits for its own connection)
- No prompt caching structure (same image+prompt sent N times without cache benefit)

## 3. Domain Objects

### ScriptVariant

A **ScriptVariant** is a standalone Python script that modifies exactly one aspect of the baseline.

**Key properties:**
- `variant_id` - Identifier (v0_baseline, v1_async_http, etc.)
- `optimization` - Description of the single change
- `dependencies` - Which previous variant's changes are prerequisites (for layered optimizations)

### PerformanceResult

A **PerformanceResult** captures one variant's test run.

**Key properties:**
- `variant_id` - Which variant was tested
- `wall_clock_seconds` - Total elapsed time for entire batch
- `avg_seconds_per_image` - Mean per-image processing time
- `total_input_tokens` - Sum of all input tokens across all API calls
- `total_output_tokens` - Sum of all output tokens
- `total_cost_usd` - Total API cost
- `avg_score` - Mean transcription quality score
- `images_processed` - Count of successfully processed images
- `images_failed` - Count of failures

## 4. Functional Requirements

**LLMTR-FR-10: Variant Isolation**
- Each variant script is self-contained and runnable independently
- Each variant changes exactly one optimization axis from its base
- All variants accept identical CLI parameters as the baseline

**LLMTR-FR-11: Config Dir Parameter**
- All variants accept `--config-dir` to locate model-registry.json, model-parameter-mapping.json, model-pricing.json
- Default: script's own directory (backward compatible)

**LLMTR-FR-12: Performance Measurement**
- Each variant outputs a `_run_results.json` in its output folder containing PerformanceResult fields
- Wall-clock time measured from first image start to last image complete
- Per-image timing preserved in individual result entries

**LLMTR-FR-13: Quality Preservation**
- All variants must produce transcription output with avg score within 0.1 of baseline
- Judge scoring uses identical prompts and parameters across all variants

**LLMTR-FR-14: Backward Compatibility**
- Combined final script must maintain all existing CLI parameters
- No behavioral changes for single-file mode
- Batch mode gains performance without API changes

## 5. Design Decisions

**LLMTR-DD-10:** Layered variant chain. Variants v1-v4 build on previous changes because async HTTP is prerequisite for persistent client, single loop, and HTTP/2. Individual contribution measured by comparing adjacent variants. Rationale: Some optimizations cannot exist without others (e.g., persistent async client requires async HTTP).

**LLMTR-DD-11:** Use 20 test images (pages 1-20) for fast iteration, full 159 images for final validation. Rationale: Reduces cost and time during development while full set validates production behavior.

**LLMTR-DD-12:** v5 (prompt caching) is orthogonal to v1-v4 chain. It modifies message structure on the baseline without requiring async changes. Rationale: Prompt caching is an API-level optimization independent of HTTP transport.

**LLMTR-DD-13:** Test runner executes variants sequentially by default with `--parallel N` option for concurrent execution. Rationale: Sequential avoids rate limit interference between variants; parallel option available when rate limits permit.

**LLMTR-DD-14:** `h2` package required for HTTP/2 support. Must be installed in the shared venv (`.tools/llm-venv/`). Rationale: httpx requires the `h2` extra for HTTP/2 (`pip install httpx[http2]`).

## 6. Implementation Guarantees

**LLMTR-IG-10:** No variant modifies the transcription prompt, judge prompt, or scoring logic.

**LLMTR-IG-11:** All variants produce output files with identical naming conventions.

**LLMTR-IG-12:** The combined final script preserves all existing CLI parameters and default behaviors.

**LLMTR-IG-13:** Retry logic (retry_with_backoff) preserved in all variants.

## 7. Key Mechanisms

### Variant Chain (v1-v4)

```
v0_baseline (sync httpx, new client/call, per-image loop, HTTP/1.1)
├─> v1_async_http (async httpx.AsyncClient, new client/call, per-image loop, HTTP/1.1)
│   ├─> v2_persistent_client (async, shared client, per-image loop, HTTP/1.1)
│   │   ├─> v3_single_loop (async, shared client, single loop + semaphore, HTTP/1.1)
│   │   └─> v4_http2 (async, shared client, single loop + semaphore, HTTP/2)
v0_baseline
└─> v5_prompt_cache (sync httpx, prompt caching structure, per-image loop, HTTP/1.1)
```

### Measurement Methodology

Each variant is compared against v0_baseline for total improvement. Incremental contribution:
- v1 vs v0 = async HTTP overhead reduction
- v2 vs v1 = connection reuse gain
- v3 vs v2 = event loop overhead reduction
- v4 vs v2 = HTTP/2 multiplexing gain
- v5 vs v0 = prompt caching gain (orthogonal axis)

### >10% Threshold Rule

A variant "wins" if: `(v0_wall_clock - vN_wall_clock) / v0_wall_clock >= 0.10`

Winners are merged into v_combined.py. If winners come from both chains (v1-v4 and v5), both optimizations are merged.

### Statistical Note

API latency varies by 2-5x depending on server load. For borderline results (8-12% improvement), run the variant a second time to confirm. Single runs are sufficient for clear winners (>15%) or clear losers (<5%).

## 8. Optimization Variants

### v0_baseline

Unmodified current script with two additions:
- `--config-dir` parameter for JSON config file location
- `_run_results.json` output with PerformanceResult data

### v1_async_http

**Change:** Replace `httpx.Client` (sync) with `httpx.AsyncClient` in `call_openai_vision()` and `call_anthropic_vision()`. Create a new AsyncClient per call.

**Expected impact:** Eliminates thread pool overhead from `run_in_executor()`. Direct async I/O.

**Implementation:**
- `call_openai_vision()` becomes `async` with `async with httpx.AsyncClient()`
- `call_anthropic_vision()` becomes `async` with `async with httpx.AsyncClient()`
- Remove `run_in_executor()` wrapper in `generate_transcription_async()`
- Still uses `asyncio.run()` per image in `process_single_image()`

### v2_persistent_client

**Change:** Create one `httpx.AsyncClient` at batch start, pass to all API calls, close at end.

**Expected impact:** Eliminates TCP+TLS handshake per call. Connection reuse for all requests to same host.

**Implementation:**
- Create `httpx.AsyncClient(timeout=180.0, limits=httpx.Limits(max_connections=100, max_keepalive_connections=50))` in main
- Pass client through call chain: `process_image_ensemble()` -> `call_vision_api()` -> `call_openai_vision()` / `call_anthropic_vision()`
- Close client after batch completes

### v3_single_loop

**Change:** Replace per-image `asyncio.run()` with single `asyncio.run()` for entire batch. Use `asyncio.Semaphore(workers)` for concurrency control.

**Expected impact:** Eliminates event loop creation per image. All images share one loop.

**Implementation:**
- `main()` calls `asyncio.run(async_main(args))` once
- `async_main()` creates semaphore, client, processes all images concurrently
- `process_single_image()` becomes `async process_single_image_async()` (remove inner `asyncio.run()` call - nested event loops are forbidden)
- Replace `ThreadPoolExecutor` with `asyncio.gather()` + semaphore
- All downstream functions must be fully async (no `asyncio.run()` inside async context)

### v4_http2

**Change:** Enable HTTP/2 on persistent AsyncClient with single event loop (builds on v3, not v2).

**Expected impact:** HTTP/2 multiplexing allows multiple requests over a single connection without head-of-line blocking. Combined with single event loop for maximum concurrent multiplexing.

**Implementation:**
- `httpx.AsyncClient(http2=True, ...)` (requires `httpx[http2]` which installs `h2`)
- Uses single event loop + semaphore (same as v3)
- Otherwise identical to v3_single_loop

### v5_prompt_cache

**Change:** Restructure OpenAI API messages to maximize automatic prompt caching hits.

**Expected impact:** When same image is sent for N candidates, OpenAI caches the prompt prefix (requires >= 1024 tokens in prefix). Subsequent calls get 50% input token discount and lower latency.

**Prerequisite:** Verify transcription prompt is >= 1024 tokens. If shorter, prompt caching will not activate.

**Implementation:**
- Move transcription prompt to `system` message (cached across calls)
- Keep image in `user` message (same image = same prefix = cache hit for all candidates)
- For Anthropic: add `cache_control: {"type": "ephemeral"}` to image source block, add `anthropic-beta: prompt-caching-2024-07-31` header
- No transport changes (stays sync)

**OpenAI message structure:**
```json
{
  "messages": [
    {"role": "system", "content": "<transcription_prompt>"},
    {"role": "user", "content": [
      {"type": "image_url", "image_url": {"url": "data:..."}},
      {"type": "text", "text": "Transcribe this image to markdown."}
    ]}
  ]
}
```

**Anthropic message structure:**
```json
{
  "system": "<transcription_prompt>",
  "messages": [
    {"role": "user", "content": [
      {"type": "image", "source": {...}, "cache_control": {"type": "ephemeral"}},
      {"type": "text", "text": "Transcribe this image to markdown."}
    ]}
  ]
}
```

## 9. Data Structures

### _run_results.json

```json
{
  "variant_id": "v0_baseline",
  "timestamp": "2026-02-06T02:00:00Z",
  "params": {
    "model": "gpt-5-mini",
    "judge_model": "gpt-5-mini",
    "workers": 20,
    "initial_candidates": 2,
    "min_score": 3.5,
    "images_count": 159
  },
  "results": {
    "wall_clock_seconds": 245.3,
    "avg_seconds_per_image": 12.1,
    "total_input_tokens": 1250000,
    "total_output_tokens": 380000,
    "total_cost_usd": 3.45,
    "avg_score": 4.12,
    "images_processed": 157,
    "images_failed": 2,
    "refinements_applied": 12
  },
  "per_image_results": [...]
}
```

### _performance_results.json (comparison)

```json
{
  "test_date": "2026-02-06",
  "test_params": {"model": "gpt-5-mini", "workers": 20, "candidates": 2, "images": 159},
  "variants": [
    {
      "variant_id": "v0_baseline",
      "wall_clock_seconds": 245.3,
      "avg_score": 4.12,
      "total_cost_usd": 3.45,
      "improvement_pct": 0.0,
      "winner": false
    },
    {
      "variant_id": "v1_async_http",
      "wall_clock_seconds": 210.1,
      "avg_score": 4.11,
      "total_cost_usd": 3.44,
      "improvement_pct": 14.3,
      "winner": true
    }
  ],
  "winners": ["v1_async_http"],
  "combined_improvement_pct": null
}
```

## 10. Document History

**[2026-02-06 03:05]**
- Reconciled: v4 now builds on v3 (single loop) for maximum HTTP/2 benefit
- Added: Prompt cache 1024-token minimum prerequisite
- Added: Anthropic beta header for prompt caching
- Added: Statistical note for borderline results
- Clarified: v3 must remove inner asyncio.run() to avoid nesting
- Fixed: h2 install via `httpx[http2]`

**[2026-02-06 02:55]**
- Initial specification created
