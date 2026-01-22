# Devil's Advocate Review: SPEC_LLM_EVALUATION_SKILL.md

**Reviewed**: 2026-01-22 21:15
**Document**: `SPEC_LLM_EVALUATION_SKILL.md [LLMEV-SP01]`
**Reviewer**: Devil's Advocate workflow

## Industry Research Findings

### Rate Limiting (OpenAI Cookbook)
- **Exponential backoff with jitter** is the recommended pattern
- Use `tenacity` library with `wait_random_exponential(min=1, max=60)`
- OpenAI provides parallel processing script: `api_request_parallel_processor.py`
- Key features needed: throttle both requests AND tokens, stream from file, retry failed requests

### LLM Evaluation Frameworks
- OpenAI Evals exists as established framework
- Spec doesn't mention why custom over existing tools
- Missing: comparison with existing frameworks, justification for custom approach

## Critical Issues

### LLMEV-RV-001: No Rate Limiting Strategy

**Severity**: [CRITICAL]
**Location**: FR-04, FR-05, FR-06, FR-07 (all batch scripts)

**Problem**: Spec allows `--workers 4` (or 8) with no rate limiting. 4 workers hitting OpenAI API simultaneously will trigger 429 errors within seconds for most tier levels.

**Evidence**: OpenAI Cookbook explicitly recommends throttling both requests AND tokens.

**What could go wrong**:
- First 10 requests succeed, next 100 fail with 429
- All workers block on rate limit simultaneously
- No token counting before sending = exceed TPM limit

**Suggested fix**: Add LLMEV-FR-09 for rate limiting:
```
- Track requests per minute (RPM) and tokens per minute (TPM)
- Implement token bucket or sliding window
- Read rate limit headers from API responses
- Add --rpm-limit and --tpm-limit parameters
```

### LLMEV-RV-002: No Retry Policy Specified

**Severity**: [HIGH]
**Location**: IG-03 says "handle errors gracefully" but no specifics

**Problem**: "Handle gracefully" is not a specification. Implementation will guess.

**What could go wrong**:
- Dev implements no retry = every transient error loses data
- Dev implements infinite retry = script hangs forever
- No backoff = hammers API, makes rate limiting worse

**Suggested fix**: Add explicit retry policy:
```
LLMEV-EC-01: API timeout (30s) -> Retry 3x with exponential backoff (1s, 2s, 4s + jitter)
LLMEV-EC-02: Rate limit (429) -> Read retry-after header, wait, retry
LLMEV-EC-03: Server error (5xx) -> Retry 3x with backoff
LLMEV-EC-04: Invalid response -> Retry 2x, then save raw + error flag
LLMEV-EC-05: Network error -> Retry 3x, then skip item with error logged
```

### LLMEV-RV-003: Resume Capability Underspecified

**Severity**: [HIGH]
**Location**: FR-04 says "skip existing outputs"

**Problem**: How does script know output is complete vs corrupted partial?

**What could go wrong**:
- Script crashed mid-write, output file exists but is truncated JSON
- Resume skips it, final results have missing data
- User doesn't notice until analysis phase

**Suggested fix**: Add completion marker:
```
- Write to temp file first: {output}.tmp
- On success, rename to final: {output}.json
- Resume checks for .tmp files = incomplete, reprocess
- Add --force flag to reprocess all
```

## High Priority Issues

### LLMEV-RV-004: No Response Validation

**Severity**: [HIGH]
**Location**: generate-questions.py, generate-answers.py

**Problem**: LLMs return malformed JSON surprisingly often. No validation specified.

**What could go wrong**:
- LLM returns markdown-wrapped JSON: ```json {...} ```
- LLM returns partial JSON (token limit hit)
- LLM returns valid JSON but wrong schema
- Script crashes or saves garbage

**Suggested fix**: Add LLMEV-IG-07:
```
Scripts MUST validate LLM JSON responses against expected schema.
On parse failure: strip markdown wrappers, retry request once.
On schema failure: log warning, save with error flag.
```

### LLMEV-RV-005: No Token Limit Handling

**Severity**: [HIGH]
**Location**: call-llm-batch.py with images

**Problem**: Large images + long prompts can exceed context window. Not addressed.

**What could go wrong**:
- 5MB image = ~85K tokens (estimated)
- gpt-4o context = 128K tokens
- Add prompt + expected output = exceeds limit
- API returns error or truncates

**Suggested fix**: Add pre-flight token estimation:
```
- Estimate image tokens (width * height / 750)
- Estimate text tokens (chars / 4)
- If total > 80% context limit, warn and skip or resize
```

### LLMEV-RV-006: No Setup/Installation Documentation

**Severity**: [MEDIUM]
**Location**: Missing from spec

**Problem**: User cannot run scripts without knowing dependencies.

**Missing**:
- Python version requirement
- `requirements.txt` contents
- API key setup instructions
- First-run verification steps

**Suggested fix**: Add Prerequisites section or separate SETUP.md:
```
## Prerequisites

- Python 3.10+
- pip install openai>=1.0.0 anthropic>=0.18.0 tenacity>=8.0.0
- Create .env with OPENAI_API_KEY and ANTHROPIC_API_KEY
```

## Medium Priority Issues

### LLMEV-RV-007: No Progress Reporting

**Severity**: [MEDIUM]
**Location**: All batch scripts

**Problem**: User has no idea if script is 10% or 90% done.

**Suggested fix**: Add `--progress` flag or default progress output:
```
[  5/100] Processing image_005.jpg... OK (2.3s)
[  6/100] Processing image_006.jpg... OK (1.8s)
```

### LLMEV-RV-008: Thread Safety Assumption

**Severity**: [MEDIUM]
**Location**: DD-08, Key Mechanisms - Parallel pattern

**Problem**: `threading.Lock` for file writes is correct, but what about the `results` list append?

**What could go wrong**:
- List append is atomic in CPython but not guaranteed
- If using multiprocessing instead of threading, Lock won't work

**Suggested fix**: Clarify threading vs multiprocessing:
```
DD-08: Use threading (not multiprocessing) for parallel API calls.
Thread-safe incremental saving with threading.Lock for file I/O.
```

### LLMEV-RV-009: No Logging Specification

**Severity**: [MEDIUM]
**Location**: Missing

**Problem**: Where do errors go? What verbosity levels?

**Suggested fix**: Add logging spec:
```
- Default: errors and warnings to stderr
- --verbose: info messages (progress, timing)
- --debug: full request/response logging
- Log format: [TIMESTAMP] [LEVEL] [SCRIPT] message
```

## Questions That Need Answers

1. **Why custom framework vs OpenAI Evals?** The spec doesn't justify why existing tools are insufficient.

2. **What happens with very large evaluations (10K+ items)?** Memory usage, file handle limits?

3. **Is there a way to pause/resume mid-batch?** Not just crash recovery, but intentional pause.

4. **How are API costs tracked in real-time?** User might want to abort if costs exceed budget.

5. **What about Anthropic rate limits?** Different from OpenAI, different headers.

## Summary

| Severity | Count | Status |
|----------|-------|--------|
| CRITICAL | 1 | Rate limiting missing |
| HIGH | 4 | Retry, resume, validation, token limits |
| MEDIUM | 4 | Setup, progress, threading, logging |

**Recommendation**: Address CRITICAL and HIGH issues before implementation. The spec is ~80% complete but missing operational concerns that will cause production failures.

## Document History

**[2026-01-22 21:15]**
- Initial Devil's Advocate review
- Research: OpenAI rate limiting, LLM evaluation frameworks

