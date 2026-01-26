# _IMPL_FIND_WORKERS_LIMIT_REVIEW.md

**Doc ID**: LLMEV-IP03-RV01
**Goal**: Identify implementation risks and logic errors in the find-workers-limit implementation plan
**Reviewed**: 2026-01-26 19:10
**Context**: Devil's Advocate review of LLMEV-IP03 (find-workers-limit.py implementation plan)

## Table of Contents

1. [Critical Issues](#critical-issues)
2. [High Priority](#high-priority)
3. [Medium Priority](#medium-priority)
4. [Low Priority](#low-priority)
5. [Recommendations](#recommendations)
6. [Document History](#document-history)

## Critical Issues

### `LLMEV-RV-011` find_limit() algorithm has infinite loop risk

- **Location**: IS-08 find_limit() pseudocode, lines 247-258
- **What**: The scale-back loop condition is `while current > 1` but the loop body sets `current = target` where `target = scale_back_count(current)`. If `scale_back_count(1)` returns 1 (due to `max(1, int(1 * 0.8))` = 1), the loop never terminates.
- **Risk**: Script hangs indefinitely at 1 worker, retesting forever.
- **Evidence**: `scale_back_count(1) = max(1, int(0.8)) = max(1, 0) = 1`
- **Suggested action**: Add explicit break when target equals current: `if target == current: break`

### `LLMEV-RV-012` single_call() return type inconsistent with usage

- **Location**: IS-06 single_call() signature, IS-07 run_test() usage
- **What**: IS-06 defines return as `tuple[bool, bool, dict]` (success, is_rate_limited, usage), but IS-07 doesn't show how to collect and aggregate these results from futures.
- **Risk**: Implementation may mishandle the tuple unpacking, especially when counting rate_limit_count.
- **Suggested action**: Add explicit result collection code in IS-07 showing how to aggregate success_count and rate_limit_count from futures

## High Priority

### `LLMEV-RV-013` No timeout on individual API calls

- **Location**: IS-06 single_call(), IS-07 run_test()
- **What**: ThreadPoolExecutor.submit() has no timeout. If an API call hangs (network issue, server issue), the entire test hangs.
- **Risk**: Script appears frozen with no error. User has to Ctrl+C.
- **Suggested action**: Use `future.result(timeout=60)` or add --timeout CLI flag

### `LLMEV-RV-014` Race condition in rate limit detection

- **Location**: IS-07 run_test() concurrent execution
- **What**: When rate limit occurs, multiple concurrent calls may all receive 429 simultaneously. Script counts each as a separate rate limit event, but they're really the same underlying limit.
- **Risk**: Inflated rate_limit_count may trigger premature scale-back. 6 concurrent 429s counted as 6 events when it's really 1 event affecting 6 calls.
- **Suggested action**: Consider "at least one rate limit = fail" logic (already specified), but clarify that count is informational only

### `LLMEV-RV-015` Helper functions copied inline creates maintenance burden

- **Location**: IS-05 "Copy functions inline rather than importing"
- **What**: Copying load_api_keys, detect_provider, create_*_client from call-llm-batch.py means any bug fixes or updates must be applied to both files.
- **Risk**: Functions diverge over time. Bug fixed in one file not fixed in other.
- **Suggested action**: Consider extracting shared utilities to `_llm_utils.py` that both scripts import

## Medium Priority

### `LLMEV-RV-016` No validation of --model before expensive operations

- **Location**: IS-09 main(), IS-10 parse_args()
- **What**: main() loads API keys, creates client, then runs discovery. If model ID is invalid for the provider, error occurs after setup.
- **Risk**: Confusing error messages, wasted time loading configs.
- **Suggested action**: Validate model format early: check known prefixes (gpt-, claude-) before creating client

### `LLMEV-RV-017` output_file.write_text() may fail silently

- **Location**: IS-09 main() line 295
- **What**: `args.output_file.write_text(json.dumps(result, indent=2))` - if output_file path is invalid or permission denied, script crashes after all testing is complete.
- **Risk**: All test results lost after expensive API calls completed.
- **Suggested action**: Validate output_file is writable at start, or use try/except with fallback to stdout

### `LLMEV-RV-018` DEFAULT_PROMPT may not reliably produce 500+ tokens

- **Location**: IS-01 DEFAULT_PROMPT constant
- **What**: Prompt asks for "500-word essay" but output token count depends on model behavior. Some models may produce shorter responses, especially with rate limiting pressure.
- **Risk**: Prompts produce <500 tokens, not achieving "labour-intensive" goal per FR-24.
- **Suggested action**: Add min_tokens as max_tokens parameter to API call to encourage longer output

## Low Priority

### `LLMEV-RV-019` Lock not used in implementation

- **Location**: IS-01 imports include `from threading import Lock`
- **What**: Lock is imported but never used in the implementation steps. Unlike call-llm-batch.py which uses locks for file writing, this script only aggregates in-memory results.
- **Risk**: Unused import, minor code smell.
- **Suggested action**: Remove Lock import if not needed

### `LLMEV-RV-020` Test cases don't cover all edge cases

- **Location**: Section 4 Test Cases
- **What**: TC-06 says "Rate limit at 3 workers -> ok=true, tests 2 and 1" but LLMEV-IP03-EC-01 says "Scale back to 2, then 1". The infinite loop risk (RV-011) at 1 worker isn't tested.
- **Risk**: Bug in scale-back loop not caught by tests.
- **Suggested action**: Add TC for scale-back loop termination at 1 worker

## Recommendations

### Must Do

- [ ] Fix infinite loop risk in find_limit() - add break when target == current (RV-011)
- [ ] Add timeout to API calls (RV-013)
- [ ] Validate output_file is writable before running tests (RV-017)

### Should Do

- [ ] Show explicit result collection code in IS-07 (RV-012)
- [ ] Extract shared utilities to common module (RV-015)
- [ ] Validate model format early in main() (RV-016)

### Could Do

- [ ] Remove unused Lock import (RV-019)
- [ ] Add test case for scale-back loop termination (RV-020)

## Document History

**[2026-01-26 19:10]**
- Initial Devil's Advocate review created
