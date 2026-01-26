# IMPL: Find Workers Limit Script

**Doc ID (TDID)**: LLMEV-IP03
**Feature**: find-workers-limit
**Goal**: Implement script to discover maximum concurrent workers for LLM API calls
**Timeline**: Created 2026-01-26, Updated 0 times

**Target files**:
- `DevSystemV3.2/skills/llm-evaluation/find-workers-limit.py` (NEW ~350 lines)
- Then sync to `.windsurf/skills/llm-evaluation/`

**Depends on:**
- `_SPEC_FIND_WORKERS_LIMIT.md [LLMEV-SP03]` for requirements and design decisions

## MUST-NOT-FORGET

- Reuse helper functions from `call-llm-batch.py`: `load_api_keys`, `detect_provider`, `create_openai_client`, `create_anthropic_client`
- Rate limit detection must catch both HTTP 429 and SDK RateLimitError
- Never recommend a worker count that triggered rate limiting
- Built-in prompt must generate 500+ tokens output

## Table of Contents

1. [File Structure](#1-file-structure)
2. [Edge Cases](#2-edge-cases)
3. [Implementation Steps](#3-implementation-steps)
4. [Test Cases](#4-test-cases)
5. [Verification Checklist](#5-verification-checklist)
6. [Document History](#6-document-history)

## 1. File Structure

```
DevSystemV3.2/skills/llm-evaluation/
├── find-workers-limit.py   # Rate limit discovery script (~350 lines) [NEW]
├── call-llm-batch.py       # Existing - reuse helpers [NO CHANGE]
├── model-registry.json     # Existing - reuse for provider detection [NO CHANGE]
└── model-pricing.json      # Existing [NO CHANGE]
```

**Note**: Per `!NOTES.md`, create in `DevSystemV3.2/` first, then sync to `.windsurf/`.

## 2. Edge Cases

**LLMEV-IP03-EC-01**: Rate limited at 3 workers initially -> Scale back to 2, then 1
**LLMEV-IP03-EC-02**: Rate limited at 1 worker -> Exit with error message, recommend_workers=0
**LLMEV-IP03-EC-03**: Network error (not rate limit) -> Retry 3x, count as failure, don't trigger scale-back
**LLMEV-IP03-EC-04**: Max workers reached without rate limit -> Stop, recommend max_workers
**LLMEV-IP03-EC-05**: Scale-back lands on previously passed count -> Skip test, recommend that count
**LLMEV-IP03-EC-06**: Invalid model ID -> Exit with error before any API calls
**LLMEV-IP03-EC-07**: Missing API key -> Exit with error before any API calls

## 3. Implementation Steps

### LLMEV-IP03-IS-01: Create script skeleton with imports and argparse

**Location**: `find-workers-limit.py` (new file)

**Action**: Add imports, constants, and argument parser

**Code**:
```python
#!/usr/bin/env python3
"""find-workers-limit.py - Discover maximum concurrent workers for LLM API."""

import os, sys, json, time, argparse
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

DEFAULT_PROMPT = """Write a detailed 500-word essay about the history of computing, 
covering the evolution from mechanical calculators to modern AI systems."""

def parse_args(): ...
def main(): ...
```

### LLMEV-IP03-IS-02: Implement is_rate_limit_error() function

**Location**: `find-workers-limit.py` > after imports

**Action**: Add rate limit detection function per LLMEV-FR-21

**Code**:
```python
def is_rate_limit_error(e: Exception) -> bool:
    """Check if exception is a rate limit error (FR-21)."""
    error_str = str(e).lower()
    if '429' in error_str or 'rate' in error_str:
        return True
    if hasattr(e, 'status_code') and e.status_code == 429:
        return True
    return type(e).__name__ in ('RateLimitError', 'APIStatusError')
```

### LLMEV-IP03-IS-03: Implement next_worker_count() function

**Location**: `find-workers-limit.py` > after is_rate_limit_error

**Action**: Add scaling sequence function per LLMEV-FR-20

**Code**:
```python
def next_worker_count(current: int, max_workers: int) -> int:
    """Calculate next worker count in scaling sequence (FR-20)."""
    if current == 3:
        return min(6, max_workers)
    if current == 6:
        return min(12, max_workers)
    # After 12, multiply by 1.5
    next_count = int(current * 1.5)
    return min(next_count, max_workers)
```

### LLMEV-IP03-IS-04: Implement scale_back_count() function

**Location**: `find-workers-limit.py` > after next_worker_count

**Action**: Add scale-back calculation per LLMEV-FR-22

**Code**:
```python
def scale_back_count(current: int) -> int:
    """Calculate scaled-back worker count (FR-22)."""
    return max(1, int(current * 0.8))
```

### LLMEV-IP03-IS-05: Import helpers from call-llm-batch.py

**Location**: `find-workers-limit.py` > after scale_back_count

**Action**: Import shared utilities (or copy inline for standalone operation)

**Code**:
```python
def get_script_dir() -> Path:
    return Path(__file__).parent

def load_api_keys(keys_file: Path) -> dict:
    # Copy from call-llm-batch.py
    ...

def detect_provider(model_id: str) -> str:
    # Copy from call-llm-batch.py
    ...

def create_openai_client(keys: dict):
    # Copy from call-llm-batch.py
    ...

def create_anthropic_client(keys: dict):
    # Copy from call-llm-batch.py
    ...
```

**Note**: Copy functions inline rather than importing to keep script standalone.

### LLMEV-IP03-IS-06: Implement single_call() function

**Location**: `find-workers-limit.py` > after client creators

**Action**: Add single LLM call with rate limit detection

**Code**:
```python
def single_call(client, model: str, prompt: str, provider: str, 
                min_tokens: int, timeout: int = 120) -> tuple[bool, bool, dict]:
    """
    Make single LLM call. Returns (success, is_rate_limited, usage).
    Uses retry_with_backoff for non-rate-limit errors (FR-27).
    Timeout: 120 seconds per call (Fix RV-013).
    """
    # Build call params with max_tokens = min_tokens
    # Try up to 3 times for non-rate-limit errors
    # Return immediately on rate limit error
    # Use timeout parameter for API call
    ...
```

### LLMEV-IP03-IS-07: Implement run_test() function

**Location**: `find-workers-limit.py` > after single_call

**Action**: Add test run at specific worker count per LLMEV-FR-25

**Code**:
```python
def run_test(client, model: str, prompt: str, provider: str,
             worker_count: int, min_tokens: int, verbose: bool) -> dict:
    """
    Run test with worker_count concurrent workers (FR-25).
    Sends (worker_count * 2) prompts, minimum 6.
    Returns WorkerRun dict with workers, prompts, success, rate_limited, status, duration_ms.
    """
    num_prompts = max(6, worker_count * 2)
    if verbose:
        print(f"Testing {worker_count} workers with {num_prompts} prompts...", file=sys.stderr)
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = [executor.submit(single_call, client, model, prompt, provider, min_tokens)
                   for _ in range(num_prompts)]
        # Collect results, log progress if verbose
        ...
    
    duration_ms = int((time.time() - start_time) * 1000)
    if verbose:
        status_str = "PASSED" if rate_limit_count == 0 else f"RATE LIMITED ({rate_limit_count})"
        print(f"  -> {status_str} in {duration_ms}ms", file=sys.stderr)
    return {
        "workers": worker_count,
        "prompts": num_prompts,
        "success": success_count,
        "rate_limited": rate_limit_count,
        "status": "passed" if rate_limit_count == 0 else "rate_limited",
        "duration_ms": duration_ms
    }
```

### LLMEV-IP03-IS-08: Implement find_limit() main algorithm

**Location**: `find-workers-limit.py` > after run_test

**Action**: Add main discovery loop per LLMEV-FR-20, FR-22, FR-23

**Code**:
```python
def find_limit(client, model: str, prompt: str, provider: str,
               max_workers: int, min_tokens: int, verbose: bool) -> dict:
    """
    Discover maximum safe worker count (FR-20, FR-22, FR-23).
    Returns TestResult dict.
    """
    tested_counts = {}  # worker_count -> "passed" | "rate_limited"
    runs = []
    current = 3
    
    # Phase 1: Scale up until rate limit or max_workers
    while current <= max_workers:
        result = run_test(client, model, prompt, provider, current, min_tokens, verbose)
        runs.append(result)
        tested_counts[current] = result["status"]
        
        if result["status"] == "rate_limited":
            break
        if current >= max_workers:
            return {"recommended_workers": current, "runs": runs, ...}
        current = next_worker_count(current, max_workers)
    
    # Phase 2: Scale back to find safe limit (FR-22)
    while current > 1:
        target = scale_back_count(current)
        if target == current:  # Fix RV-011: prevent infinite loop at 1 worker
            break
        if target in tested_counts and tested_counts[target] == "passed":
            return {"recommended_workers": target, "runs": runs, ...}
        
        result = run_test(client, model, prompt, provider, target, min_tokens, verbose)
        runs.append(result)
        tested_counts[target] = result["status"]
        
        if result["status"] == "passed":
            return {"recommended_workers": target, "runs": runs, ...}
        current = target
    
    # Reached 1 worker and still rate limited (FR-26, IG-23)
    return {"recommended_workers": 0, "max_tested": max(tested_counts.keys()), 
            "error": "Rate limited even at 1 worker", "runs": runs}
```

**Note**: All return statements include `max_tested = max(tested_counts.keys())` per spec output JSON.

### LLMEV-IP03-IS-09: Implement main() with CLI handling

**Location**: `find-workers-limit.py` > after find_limit

**Action**: Add main function with argument parsing and output

**Code**:
```python
def main():
    args = parse_args()
    
    # Validate output_file early (Fix RV-017)
    if args.output_file:
        try:
            args.output_file.touch()
        except (OSError, PermissionError) as e:
            print(f"Error: Cannot write to {args.output_file}: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Load keys and create client
    keys = load_api_keys(args.keys_file)
    provider = detect_provider(args.model)
    client = create_openai_client(keys) if provider == 'openai' else create_anthropic_client(keys)
    
    # Load prompt
    prompt = args.prompt_file.read_text() if args.prompt_file else DEFAULT_PROMPT
    
    # Run discovery
    result = find_limit(client, args.model, prompt, provider,
                        args.max_workers, args.min_output_tokens, args.verbose)
    result["model"] = args.model
    result["timestamp"] = datetime.now(timezone.utc).isoformat()
    
    # Output
    print(result["recommended_workers"])  # stdout: just the number
    if args.output_file:
        args.output_file.write_text(json.dumps(result, indent=2))
        print(f"Results saved to: {args.output_file}", file=sys.stderr)
```

### LLMEV-IP03-IS-10: Implement parse_args() function

**Location**: `find-workers-limit.py` > before main

**Action**: Add argument parser per LLMEV-SP03 CLI Interface

**Code**:
```python
def parse_args():
    parser = argparse.ArgumentParser(
        description='Discover maximum concurrent workers for LLM API calls.')
    parser.add_argument('--model', required=True, help='API model ID')
    parser.add_argument('--keys-file', type=Path, default=Path('.env'))
    parser.add_argument('--max-workers', type=int, default=100)
    parser.add_argument('--prompt-file', type=Path, default=None)
    parser.add_argument('--output-file', type=Path, default=None)
    parser.add_argument('--min-output-tokens', type=int, default=500)
    parser.add_argument('--verbose', action='store_true')
    return parser.parse_args()
```

## 4. Test Cases

### Category 1: Normal Operation (4 tests)

- **LLMEV-IP03-TC-01**: Model with high rate limit -> ok=true, recommended_workers >= 12
- **LLMEV-IP03-TC-02**: Model with low rate limit -> ok=true, recommended_workers < 12
- **LLMEV-IP03-TC-03**: Max workers reached -> ok=true, recommended_workers == max_workers
- **LLMEV-IP03-TC-04**: Custom prompt file -> ok=true, uses custom prompt

### Category 2: Rate Limit Handling (4 tests)

- **LLMEV-IP03-TC-05**: Rate limit at 27 workers, 18 passed -> ok=true, recommended_workers in [18..21]
- **LLMEV-IP03-TC-06**: Rate limit at 3 workers -> ok=true, tests 2 and 1
- **LLMEV-IP03-TC-07**: Rate limit at 1 worker -> ok=false, recommended_workers=0, error message
- **LLMEV-IP03-TC-08**: Scale-back lands on passed count -> ok=true, no redundant test

### Category 3: Error Handling (3 tests)

- **LLMEV-IP03-TC-09**: Invalid model ID -> ok=false, exit before API call
- **LLMEV-IP03-TC-10**: Missing API key -> ok=false, clear error message
- **LLMEV-IP03-TC-11**: Network error (not rate limit) -> ok=true, retries, no scale-back

### Category 4: Output (2 tests)

- **LLMEV-IP03-TC-12**: JSON output file -> ok=true, valid JSON with all fields
- **LLMEV-IP03-TC-13**: stdout output -> ok=true, single number only

## 5. Verification Checklist

### Prerequisites
- [ ] **LLMEV-IP03-VC-01**: Spec LLMEV-SP03 read and understood
- [ ] **LLMEV-IP03-VC-02**: call-llm-batch.py helper functions identified

### Implementation
- [ ] **LLMEV-IP03-VC-03**: IS-01 script skeleton complete
- [ ] **LLMEV-IP03-VC-04**: IS-02 is_rate_limit_error() works for both providers
- [ ] **LLMEV-IP03-VC-05**: IS-03 next_worker_count() sequence correct
- [ ] **LLMEV-IP03-VC-06**: IS-04 scale_back_count() factor 0.8
- [ ] **LLMEV-IP03-VC-07**: IS-05 helper functions copied
- [ ] **LLMEV-IP03-VC-08**: IS-06 single_call() with retry logic
- [ ] **LLMEV-IP03-VC-09**: IS-07 run_test() with ThreadPoolExecutor
- [ ] **LLMEV-IP03-VC-10**: IS-08 find_limit() main algorithm
- [ ] **LLMEV-IP03-VC-11**: IS-09 main() with output handling
- [ ] **LLMEV-IP03-VC-12**: IS-10 parse_args() with all CLI options

### Validation
- [ ] **LLMEV-IP03-VC-20**: Script runs with --help
- [ ] **LLMEV-IP03-VC-21**: Test with low max_workers (5) passes
- [ ] **LLMEV-IP03-VC-22**: JSON output contains all required fields
- [ ] **LLMEV-IP03-VC-23**: Rate limit detection works (mock or real)

## 6. Document History

**[2026-01-26 19:20]**
- Fixed: Infinite loop risk (RV-011) - add break when target == current
- Fixed: API call timeout 120s (RV-013)
- Fixed: Validate output_file at start (RV-017)

**[2026-01-26 18:59]**
- Fixed: Target file location to DevSystemV3.2 (per !NOTES.md sync rules)

**[2026-01-26 18:57]**
- Added: max_tested field in output JSON per spec
- Added: verbose logging detail in IS-07

**[2026-01-26 18:55]**
- Initial implementation plan created
