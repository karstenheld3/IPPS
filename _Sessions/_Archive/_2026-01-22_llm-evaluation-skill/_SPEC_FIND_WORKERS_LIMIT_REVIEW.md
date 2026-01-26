# _SPEC_FIND_WORKERS_LIMIT_REVIEW.md

**Doc ID**: LLMEV-SP03-RV01
**Goal**: Identify flawed assumptions, logic errors, and hidden risks in the rate limit discovery specification
**Reviewed**: 2026-01-26 19:05
**Context**: Devil's Advocate review of LLMEV-SP03 (find-workers-limit.py spec)

## Table of Contents

1. [Critical Issues](#critical-issues)
2. [High Priority](#high-priority)
3. [Medium Priority](#medium-priority)
4. [Low Priority](#low-priority)
5. [Industry Research Findings](#industry-research-findings)
6. [Recommendations](#recommendations)
7. [Document History](#document-history)

## Critical Issues

### `LLMEV-RV-001` Spec conflates concurrent workers with rate limits

- **Location**: LLMEV-FR-20, FR-21, entire spec premise
- **What**: The spec assumes "concurrent workers" directly maps to "rate limit capacity". This is fundamentally flawed. API rate limits are typically:
  - **RPM** (Requests Per Minute) - total requests over time window
  - **TPM** (Tokens Per Minute) - total tokens over time window
  - **Concurrent connections** - rarely the limiting factor
- **Risk**: Script may find a "safe" concurrent worker count that still triggers rate limits because the *actual* limit is RPM/TPM, not concurrency. A burst of 12 concurrent requests completing in 2 seconds uses 12 RPM capacity instantly, leaving 48 seconds with near-zero capacity.
- **Evidence**: OpenAI docs state limits are "requests per minute" and "tokens per minute", not "concurrent requests"
- **Suggested action**: 
  1. Rename script to `find-request-rate.py` or clarify scope
  2. Add RPM pacing: spread requests over time, not just concurrent bursts
  3. Consider testing sustained throughput (60 requests over 60 seconds) vs burst capacity

### `LLMEV-RV-002` Rate limits are per-organization, not per-model

- **Location**: LLMEV-FR-20, CLI Interface (--model required)
- **What**: OpenAI rate limits are shared across the organization. Testing model A consumes quota that affects model B. Testing gpt-4o may exhaust quota needed for gpt-4o-mini.
- **Risk**: Running this script with one model could disrupt production workloads using other models on the same API key.
- **Evidence**: OpenAI docs: "limits are applied per organization and not per user"
- **Suggested action**: 
  1. Add warning in output about organization-wide impact
  2. Consider --dry-run mode that only reads current limits from headers
  3. Document this risk prominently in SKILL.md

## High Priority

### `LLMEV-RV-003` No use of retry-after header

- **Location**: LLMEV-FR-21 (Rate Limit Detection), Key Mechanisms
- **What**: Both OpenAI and Anthropic return `retry-after` headers indicating how long to wait. The spec ignores this, using arbitrary 0.8 scale-back factor instead.
- **Risk**: Inefficient discovery - script may scale back too aggressively or not enough. Provider tells us exactly when to retry; we're ignoring it.
- **Evidence**: Anthropic docs: "429 error... along with a retry-after header indicating how long to wait"
- **Suggested action**: Parse and log retry-after header, use it to inform scale-back timing

### `LLMEV-RV-004` Rate limits fluctuate based on server load

- **Location**: Entire spec assumes static, discoverable limits
- **What**: Rate limits are not static. OpenAI docs mention "429 Capacity" error that occurs when "your traffic has significantly increased, overloading the model". Same request count may succeed or fail based on server conditions.
- **Risk**: Script returns 18 workers today, but tomorrow same account gets rate-limited at 12 due to server load. Users may rely on stale results.
- **Evidence**: OpenAI error code 529 - temporary throttling based on traffic patterns
- **Suggested action**: 
  1. Add timestamp and "valid for approximately X hours" disclaimer
  2. Consider multiple test runs to establish confidence interval

### `LLMEV-RV-005` Tokens-per-minute limit not tested

- **Location**: LLMEV-FR-24 (Labour-Intensive Prompt)
- **What**: Spec uses 500-token output to "ensure meaningful load", but doesn't consider that TPM limits may be the bottleneck, not RPM. 12 workers * 500 output tokens = 6000 tokens per burst, which could hit TPM limits on lower tiers.
- **Risk**: Script may find RPM-based limit while missing TPM-based limit. Production workload with longer outputs will still get rate-limited.
- **Suggested action**: Test with varying output lengths, or document that results apply only to ~500 token responses

## Medium Priority

### `LLMEV-RV-006` Scale-back math doesn't handle small numbers well

- **Location**: LLMEV-FR-22, LLMEV-DD-22
- **What**: Scale-back factor 0.8 with floor() produces: 3 -> 2 -> 1 -> 0 (clamped to 1). But for initial scaling, 3 * 0.8 = 2.4 -> 2, which is only 1 worker difference. May need many iterations.
- **Risk**: Slow convergence at low worker counts. If rate-limited at 3, we test 2, then 1. But we could have started at 1 directly if 3 failed immediately.
- **Suggested action**: For initial rate limit at 3 workers, jump directly to 1 instead of 2

### `LLMEV-RV-007` No distinction between rate limit types

- **Location**: LLMEV-FR-21
- **What**: Rate limit errors can be for different reasons: RPM exceeded, TPM exceeded, daily limit, spending limit, capacity throttling. Spec treats all as equivalent.
- **Risk**: Script may scale back for a daily limit (which won't help) or spending limit (also won't help).
- **Suggested action**: Parse error message to distinguish rate limit types, handle differently

### `LLMEV-RV-008` Test prompts consume real API quota

- **Location**: LLMEV-FR-24, FR-25
- **What**: At max scale (100 workers * 2 prompts * 500 tokens = 100,000 tokens), testing costs real money and consumes daily/monthly quota.
- **Risk**: Users may run script multiple times, consuming significant quota before doing real work.
- **Suggested action**: 
  1. Add cost estimate before running (using model-pricing.json)
  2. Add --max-cost flag to abort if estimated cost exceeds threshold
  3. Consider using cheapest model variant for testing

## Low Priority

### `LLMEV-RV-009` Assumes single API key per provider

- **Location**: Implicit in design
- **What**: Some organizations have multiple API keys with different rate limits (dev vs prod keys, project-specific keys).
- **Suggested action**: Document that results are specific to the API key used

### `LLMEV-RV-010` No warm-up period consideration

- **Location**: LLMEV-FR-20
- **What**: Some rate limiters use sliding windows or token buckets that refill over time. Starting with burst of 6 prompts may not represent steady-state behavior.
- **Suggested action**: Consider adding --warm-up flag to send gradual requests before testing

## Industry Research Findings

### Rate Limit Response Headers

- **Pattern found**: Both OpenAI and Anthropic return detailed rate limit headers
  - Anthropic: `anthropic-ratelimit-requests-limit`, `anthropic-ratelimit-requests-remaining`, `anthropic-ratelimit-requests-reset`
  - OpenAI: Similar headers with `x-ratelimit-*` prefix
- **How it applies**: Script could read these headers on first successful request to know exact limits without trial-and-error
- **Source**: https://docs.anthropic.com/en/api/rate-limits

### Request Rate vs Concurrency

- **Pattern found**: Industry benchmarking tools (Databricks, NVIDIA NIM) focus on throughput over time, not max concurrency
- **How it applies**: Our approach tests burst capacity, not sustainable throughput. Real workloads need sustained rates.
- **Source**: Databricks LLM benchmarking documentation

### Alternatives Considered

- **Read headers directly**: Query rate limit headers on single request to learn limits without stress testing. Pros: Zero quota consumption, instant results. Cons: Doesn't test actual behavior under load.
- **Binary search**: Instead of linear scale-up, use binary search between 1 and max_workers. Pros: Faster convergence. Cons: May miss gradual degradation patterns.
- **Time-based pacing**: Instead of max concurrency, test "requests per second" rate. Pros: More realistic. Cons: Takes longer to run.

## Recommendations

### Must Do

- [ ] Add prominent warning about organization-wide rate limit impact (RV-002)
- [ ] Document that results are for burst capacity, not sustained throughput (RV-001)
- [ ] Add cost estimate before running (RV-008)

### Should Do

- [ ] Parse and log retry-after header value (RV-003)
- [ ] Add "results valid for ~X hours" disclaimer with timestamp (RV-004)
- [ ] Distinguish between rate limit types in error handling (RV-007)

### Could Do

- [ ] Add --read-headers mode to query limits without stress testing
- [ ] Add --paced mode to test sustained throughput over 60 seconds
- [ ] Add --max-cost flag to limit test spending

## Document History

**[2026-01-26 19:05]**
- Initial Devil's Advocate review created
