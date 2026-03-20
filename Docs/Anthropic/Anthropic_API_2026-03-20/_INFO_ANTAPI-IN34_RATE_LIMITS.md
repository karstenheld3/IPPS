# Rate Limits

**Doc ID**: ANTAPI-IN34
**Goal**: Document rate limit types, tiers, headers, and handling strategies
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN01_INTRODUCTION.md [ANTAPI-IN01]` for base URL, auth headers

## Summary

Anthropic enforces rate limits at three levels: requests per minute (RPM), input tokens per minute (input TPM), and output tokens per minute (output TPM). Limits are set per-model and per-workspace, with higher tiers unlocking greater capacity. Rate limit information is returned in response headers. When limits are exceeded, the API returns HTTP 429 with a `rate_limit_error`. The Message Batches API has separate rate limits for HTTP requests and queued batch requests.

## Key Facts

- **Limit Types**: RPM, input TPM, output TPM
- **Scope**: Per-model, per-workspace
- **HTTP Status**: 429 Too Many Requests
- **Error Type**: `rate_limit_error`
- **Headers**: `anthropic-ratelimit-*` in every response
- **Tiers**: Usage-based tiers with increasing limits
- **Status**: GA

## Rate Limit Headers

Every API response includes rate limit headers:

- **anthropic-ratelimit-requests-limit** - Max RPM for this model
- **anthropic-ratelimit-requests-remaining** - Remaining requests in current window
- **anthropic-ratelimit-requests-reset** - ISO 8601 time when request limit resets
- **anthropic-ratelimit-input-tokens-limit** - Max input TPM
- **anthropic-ratelimit-input-tokens-remaining** - Remaining input tokens
- **anthropic-ratelimit-input-tokens-reset** - Input token limit reset time
- **anthropic-ratelimit-output-tokens-limit** - Max output TPM
- **anthropic-ratelimit-output-tokens-remaining** - Remaining output tokens
- **anthropic-ratelimit-output-tokens-reset** - Output token limit reset time
- **retry-after** - Seconds to wait before retrying (on 429 responses)

## Handling Rate Limits

### Basic Retry with Backoff

```python
import anthropic
import time

client = anthropic.Anthropic()

def make_request_with_retry(messages, max_retries=5):
    for attempt in range(max_retries):
        try:
            return client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=messages,
            )
        except anthropic.RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            retry_after = int(e.response.headers.get("retry-after", 30))
            print(f"Rate limited. Retrying in {retry_after}s...")
            time.sleep(retry_after)
```

### SDK Built-in Retry

The Python SDK automatically retries on 429 errors with exponential backoff:

```python
import anthropic

# SDK retries rate limit errors automatically (default: 2 retries)
client = anthropic.Anthropic(max_retries=3)

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
)
```

### Checking Remaining Capacity

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.with_raw_response.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
)

headers = response.headers
print(f"RPM remaining: {headers.get('anthropic-ratelimit-requests-remaining')}")
print(f"Input TPM remaining: {headers.get('anthropic-ratelimit-input-tokens-remaining')}")
print(f"Output TPM remaining: {headers.get('anthropic-ratelimit-output-tokens-remaining')}")

message = response.parse()
```

## Batch API Rate Limits

Message Batches API has separate limits:

- **HTTP request rate limits** - For batch CRUD operations
- **Queued request limits** - For total requests waiting to be processed across all batches
- Processing may be slowed during high demand, causing more request expirations

## Gotchas and Quirks

- Rate limits are per-model AND per-workspace (not per-API-key)
- The SDK auto-retries on 429 with exponential backoff by default
- `retry-after` header gives the recommended wait time in seconds
- Token limits apply to both input and output separately
- Batch API can slightly exceed workspace spend limits due to concurrent processing
- Rate limit tiers increase based on account usage and spending history
- Server tool usage (web search) may have additional per-tool rate limits

## Related Endpoints

- `_INFO_ANTAPI-IN04_ERRORS.md [ANTAPI-IN04]` - Error types including rate_limit_error
- `_INFO_ANTAPI-IN10_BATCHES.md [ANTAPI-IN10]` - Batch API rate limits
- `_INFO_ANTAPI-IN12_PRICING.md [ANTAPI-IN12]` - Tier-based pricing and limits

## Sources

- ANTAPI-SC-ANTH-RTLMT - https://platform.claude.com/docs/en/api/rate-limits - Rate limit documentation

## Document History

**[2026-03-20 04:25]**
- Initial documentation created from rate limits guide
