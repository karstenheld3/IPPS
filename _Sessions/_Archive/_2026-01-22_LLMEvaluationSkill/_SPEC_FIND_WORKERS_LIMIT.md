# SPEC: Find Workers Limit Script

**Doc ID (TDID)**: LLMEV-SP03
**Feature**: find-workers-limit
**Goal**: Discover the maximum concurrent workers for a given LLM model by progressively scaling until rate limits are hit, then scaling back to find a stable limit.
**Timeline**: Created 2026-01-26, Updated 0 times
**Target file**: `.windsurf/skills/llm-evaluation/find-workers-limit.py`

**Depends on:**
- `SPEC_LLM_EVALUATION_SKILL.md [LLMEV-SP01]` for worker pattern and API abstraction

## MUST-NOT-FORGET

- Use ThreadPoolExecutor pattern from `call-llm-batch.py`
- Detect rate limit errors from both OpenAI and Anthropic APIs
- Minimum 500 tokens output per prompt to ensure meaningful load
- Never suggest a worker count that caused rate limiting

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Design Decisions](#5-design-decisions)
6. [Implementation Guarantees](#6-implementation-guarantees)
7. [Key Mechanisms](#7-key-mechanisms)
8. [Action Flow](#8-action-flow)
9. [Data Structures](#9-data-structures)
10. [CLI Interface](#10-cli-interface)
11. [Document History](#11-document-history)

## 1. Scenario

**Problem:** When running batch LLM operations, users don't know the maximum concurrent workers their API account can handle. Too few workers = slow processing. Too many = rate limit errors and wasted retries.

**Solution:**
- Start with 3 concurrent workers
- Double workers twice (3 -> 6 -> 12)
- Then multiply by 1.5 for each subsequent run (12 -> 18 -> 27 -> ...)
- When rate limit detected: scale back by multiplying with 0.8
- Stop when a stable worker count is found (no rate limits at current level)

**What we don't want:**
- Manually guessing worker counts through trial and error
- Silent failures that don't report the discovered limit
- Excessive API costs from running too many test prompts

## 2. Context

Part of the LLM Evaluation Skill (`LLMEV`). Uses the same worker system as `call-llm-batch.py` (ThreadPoolExecutor, retry_with_backoff). Supports both OpenAI and Anthropic providers.

## 3. Domain Objects

### WorkerRun

A **WorkerRun** represents one test iteration at a specific worker count.

**Key properties:**
- `worker_count` - Number of concurrent workers tested
- `success_count` - Prompts that completed successfully
- `rate_limit_count` - Prompts that hit rate limits
- `duration_ms` - Total duration of this run
- `status` - "passed" (no rate limits), "rate_limited" (at least one rate limit)

### TestResult

A **TestResult** represents the final output of the script.

**Key properties:**
- `model` - Model ID tested
- `recommended_workers` - Safe worker count (highest that passed)
- `max_tested` - Highest worker count tested
- `runs` - List of WorkerRun objects
- `timestamp` - When test completed
- `error` - (optional) Error message if rate limited at 1 worker

## 4. Functional Requirements

**LLMEV-FR-20: Progressive Worker Scaling**
- Start at 3 concurrent workers
- Double twice: 3 -> 6 -> 12
- Then multiply by 1.5 and round to nearest integer: 12 -> 18 -> 27 -> 40 -> 60 -> ...
- Cap at --max-workers (default: 100)

**LLMEV-FR-21: Rate Limit Detection**
- Detect OpenAI rate limit errors (429, RateLimitError)
- Detect Anthropic rate limit errors (429, RateLimitError)
- Count rate limit occurrences per run
- A run "fails" if ANY prompt hits a rate limit

**LLMEV-FR-22: Scale-Back Algorithm**
- On rate limit: multiply current workers by 0.8 (round down)
- If scaled-back count already tested and passed: stop, recommend that count
- If scaled-back count not tested: test it
- If scaled-back count also fails: continue scaling back by 0.8

**LLMEV-FR-23: Stable Limit Discovery**
- Stop when: (a) scaled-back count was already tested and passed, OR (b) scaled-back count passes on test
- Report the highest worker count that completed without rate limits

**LLMEV-FR-24: Labour-Intensive Prompt**
- Use built-in prompt that generates minimum 500 tokens output
- Prompt: "Write a detailed 500-word essay about the history of computing"
- Or allow custom prompt via --prompt-file

**LLMEV-FR-25: Prompts Per Run**
- Each run sends (worker_count * 2) prompts to ensure all workers are utilized
- Minimum 6 prompts per run

**LLMEV-FR-26: Initial Rate Limit Handling**
- If rate limited at initial 3 workers: scale back to 2, then 1
- If rate limited at 1 worker: report error "Model rate limited even with 1 worker"

**LLMEV-FR-27: Non-Rate-Limit Error Handling**
- Network errors and other transient errors: retry up to 3 times with exponential backoff
- After 3 retries: treat as failure for that prompt, continue with others
- Non-rate-limit failures do NOT trigger scale-back (only rate limits do)

## 5. Design Decisions

**LLMEV-DD-20:** Use same ThreadPoolExecutor pattern as call-llm-batch.py. Rationale: Consistent behavior across scripts, proven reliable.

**LLMEV-DD-21:** Scaling sequence 3->6->12 then *1.5 instead of always *2. Rationale: Doubling at high counts (e.g., 24->48) is too aggressive; 1.5x provides finer granularity after initial ramp-up.

**LLMEV-DD-22:** Scale-back factor 0.8 instead of halving. Rationale: Halving loses too much discovered capacity; 0.8 finds a closer safe limit.

**LLMEV-DD-23:** Stop immediately when a previously-passing count is reached during scale-back. Rationale: Avoids redundant testing.

**LLMEV-DD-24:** During scale-back, if the scaled-back count falls between two tested counts, use the higher passing count. Example: tested 18 (pass), 27 (fail), scale back gives 21 -> since 21 > 18, test 21. If 21 passes, recommend 21 (higher than 18). Rationale: Find the highest safe limit.

## 6. Implementation Guarantees

**LLMEV-IG-20:** Script will never recommend a worker count that caused rate limits during testing.

**LLMEV-IG-21:** Script will always output a recommended_workers value (minimum 1).

**LLMEV-IG-22:** Rate limit detection covers both HTTP 429 and SDK-specific RateLimitError exceptions.

**LLMEV-IG-23:** Script will report clear error if rate limited even at 1 worker.

## 7. Key Mechanisms

### Worker Scaling Sequence

```
Phase 1 (doubling): 3 -> 6 -> 12
Phase 2 (1.5x):     12 -> 18 -> 27 -> 40 -> 60 -> 90 -> ...
Cap:                Stop at --max-workers (default 100)
```

### Scale-Back Logic

```
On rate limit at N workers:
├─> Calculate target = floor(N * 0.8)
├─> If target was tested and passed:
│   └─> Stop, recommend target
└─> Else test target:
    ├─> If passes: recommend target
    └─> If fails: scale back again from target
```

### Rate Limit Detection

```python
def is_rate_limit_error(e: Exception) -> bool:
    """Check if exception is a rate limit error."""
    error_str = str(e).lower()
    if '429' in error_str or 'rate' in error_str:
        return True
    if hasattr(e, 'status_code') and e.status_code == 429:
        return True
    return type(e).__name__ in ('RateLimitError', 'APIStatusError')
```

## 8. Action Flow

```
User runs find-workers-limit.py --model gpt-4o
├─> Load API keys and model registry
├─> Initialize: workers=3, tested_counts={}
├─> Loop (scaling up):
│   ├─> Run test at current workers
│   │   ├─> Send (workers * 2) prompts concurrently
│   │   └─> Count successes and rate limits
│   ├─> If no rate limits:
│   │   ├─> tested_counts[workers] = "passed"
│   │   ├─> If workers >= max_workers: Stop, recommend workers
│   │   └─> Scale up: workers = next_worker_count(workers)
│   └─> If rate limit detected:
│       ├─> tested_counts[workers] = "rate_limited"
│       └─> Enter scale-back phase
├─> Loop (scaling back):
│   ├─> target = floor(workers * 0.8)
│   ├─> If tested_counts[target] == "passed":
│   │   └─> Stop, recommend target
│   ├─> Run test at target
│   │   ├─> If passes: Stop, recommend target
│   │   └─> If fails: workers = target, continue
│   └─> If target <= 1: Stop, recommend 1
└─> Output results JSON
```

## 9. Data Structures

### Output JSON

```json
{
  "model": "gpt-4o",
  "recommended_workers": 18,
  "max_tested": 27,
  "runs": [
    {"workers": 3, "prompts": 6, "success": 6, "rate_limited": 0, "status": "passed", "duration_ms": 2340},
    {"workers": 6, "prompts": 12, "success": 12, "rate_limited": 0, "status": "passed", "duration_ms": 3120},
    {"workers": 12, "prompts": 24, "success": 24, "rate_limited": 0, "status": "passed", "duration_ms": 4560},
    {"workers": 18, "prompts": 36, "success": 36, "rate_limited": 0, "status": "passed", "duration_ms": 6780},
    {"workers": 27, "prompts": 54, "success": 48, "rate_limited": 6, "status": "rate_limited", "duration_ms": 8900},
    {"workers": 21, "prompts": 42, "success": 42, "rate_limited": 0, "status": "passed", "duration_ms": 7200}
  ],
  "timestamp": "2026-01-26T18:45:00Z"
}
```

## 10. CLI Interface

```bash
python find-workers-limit.py --model MODEL [options]

Required:
  --model MODEL           API model ID (e.g., gpt-4o, claude-3-5-sonnet-20241022)

Optional:
  --keys-file PATH        API keys file (default: .env)
  --max-workers N         Maximum workers to test (default: 100)
  --prompt-file PATH      Custom prompt file (default: built-in 500-word essay prompt)
  --output-file PATH      Save results JSON to file
  --min-output-tokens N   Minimum output tokens per prompt (default: 500)
  --verbose               Print detailed progress

Output:
  Prints recommended_workers to stdout
  Prints progress to stderr
  JSON results to --output-file if specified
```

### Example Usage

```bash
# Basic usage
python find-workers-limit.py --model gpt-4o --keys-file .api-keys.txt

# With output file
python find-workers-limit.py --model claude-3-5-sonnet-20241022 \
    --keys-file .api-keys.txt --output-file limits.json --verbose

# Custom prompt
python find-workers-limit.py --model gpt-4o --prompt-file my-prompt.md
```

## 11. Document History

**[2026-01-26 18:58]**
- Fixed: Added max_tested and error to TestResult domain object

**[2026-01-26 18:49]**
- Added: LLMEV-FR-26 (initial rate limit handling at 3/2/1 workers)
- Added: LLMEV-FR-27 (non-rate-limit error handling with retries)
- Added: LLMEV-DD-24 (scale-back finds highest passing count)
- Added: LLMEV-IG-23 (error report if rate limited at 1 worker)

**[2026-01-26 18:45]**
- Initial specification created
