# Rate Limits

**Doc ID**: OAIAPI-IN05
**Goal**: Document OpenAI API rate limiting system, tiers, headers, and monitoring
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

OpenAI API implements rate limiting at project level with RPM (requests per minute) and TPM (tokens per minute) limits varying by usage tier (Free, Tier 1-5) and model. Rate limit info returned in response headers: `x-ratelimit-limit-requests`, `x-ratelimit-limit-tokens`, `x-ratelimit-remaining-requests`, `x-ratelimit-remaining-tokens`, `x-ratelimit-reset-requests`, `x-ratelimit-reset-tokens`. When limits exceeded, API returns 429 status with retry-after info. Tiers determined by cumulative spend: Free ($0), Tier 1 ($5+), Tier 2 ($50+), Tier 3 ($100+), Tier 4 ($250+), Tier 5 ($1000+). Each tier has higher limits. Rate limits are model-specific and project-scoped - different projects have separate limits. Batch API bypasses rate limits but has 50% cost reduction. Best practices: implement exponential backoff on 429, monitor headers proactively, use batch processing for large jobs. [VERIFIED] (OAIAPI-SC-OAI-GRLMT, OAIAPI-SC-OAI-ADMPRJ)

## Key Facts

- **Limit types**: RPM (requests per minute), TPM (tokens per minute) [VERIFIED] (OAIAPI-SC-OAI-GRLMT)
- **Scope**: Project-level, model-specific [VERIFIED] (OAIAPI-SC-OAI-ADMPRJ)
- **Tiers**: Free, Tier 1-5 based on cumulative spend [VERIFIED] (OAIAPI-SC-OAI-GRLMT)
- **Headers**: Six x-ratelimit-* headers in responses [VERIFIED] (OAIAPI-SC-OAI-OVERVIEW)
- **Error**: 429 Too Many Requests when exceeded [VERIFIED] (OAIAPI-SC-OAI-GERROR)

## Use Cases

- **Rate limit monitoring**: Tracking usage via response headers
- **Capacity planning**: Understanding tier limits for scaling
- **Error handling**: Implementing retry logic for 429 responses
- **Batch processing**: Using Batch API to bypass rate limits

## Quick Reference

```
Response headers:
x-ratelimit-limit-requests: 500
x-ratelimit-limit-tokens: 150000
x-ratelimit-remaining-requests: 499
x-ratelimit-remaining-tokens: 149950
x-ratelimit-reset-requests: 60s
x-ratelimit-reset-tokens: 60s
```

## Rate Limit Headers

### Limit Headers

- **x-ratelimit-limit-requests**: Maximum requests allowed per minute
- **x-ratelimit-limit-tokens**: Maximum tokens allowed per minute

### Remaining Headers

- **x-ratelimit-remaining-requests**: Requests remaining in current window
- **x-ratelimit-remaining-tokens**: Tokens remaining in current window

### Reset Headers

- **x-ratelimit-reset-requests**: Time until request limit resets
- **x-ratelimit-reset-tokens**: Time until token limit resets

Format: Duration string (e.g., "60s", "2m30s")

## Usage Tiers

### Free Tier
- **Requirement**: $0 spend
- **Limits**: Lowest RPM/TPM
- **Models**: Limited model access
- **Use case**: Testing, development

### Tier 1
- **Requirement**: $5+ cumulative spend
- **Limits**: Basic production limits
- **Example**: 500 RPM, 150K TPM (model-dependent)

### Tier 2
- **Requirement**: $50+ cumulative spend
- **Limits**: Higher production limits
- **Example**: 5,000 RPM, 1.5M TPM (model-dependent)

### Tier 3
- **Requirement**: $100+ cumulative spend
- **Limits**: Large-scale production

### Tier 4
- **Requirement**: $250+ cumulative spend
- **Limits**: Enterprise-scale

### Tier 5
- **Requirement**: $1,000+ cumulative spend
- **Limits**: Highest available limits

**Note**: Exact limits vary by model. Check platform dashboard for current limits.

## Model-Specific Limits

Different models have different rate limits within same tier:

- **Flagship models** (GPT-5.4): Lower TPM limits due to cost
- **Mini models** (GPT-5.4-mini): Higher TPM limits
- **Nano models** (GPT-5.4-nano): Highest TPM limits
- **Specialized models**: Varies by model type

## Project-Level Rate Limiting

Rate limits are scoped to projects:
- Each project has separate limits
- Multiple projects = multiple sets of limits
- Usage doesn't share across projects
- Manage limits in project settings

## Exceeding Rate Limits

### 429 Response

When rate limit exceeded:
```json
{
  "error": {
    "type": "rate_limit_error",
    "code": "rate_limit_exceeded",
    "message": "Rate limit reached for requests",
    "request_id": "req_abc123"
  }
}
```

### Retry Strategy

Implement exponential backoff:
1. First retry: Wait 1-2 seconds
2. Second retry: Wait 2-4 seconds
3. Third retry: Wait 4-8 seconds
4. Check `x-ratelimit-reset-*` headers for reset time

## Rate Limit Bypass

### Batch API

Batch API bypasses rate limits:
- No RPM/TPM limits
- 50% cost reduction
- 24-hour completion window
- Use for large-scale processing

### Request Batching

Group multiple operations into batch requests where supported.

## SDK Examples (Python)

### Monitoring Rate Limits

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)

# Access response headers (SDK-dependent)
# Note: Python SDK may not expose headers directly
# Use HTTP client for direct header access
```

### Rate Limit Aware Client

```python
from openai import OpenAI, RateLimitError
import time
import logging

logger = logging.getLogger(__name__)

class RateLimitAwareClient:
    def __init__(self):
        self.client = OpenAI()
        self.max_retries = 5
    
    def call_with_backoff(self, **kwargs):
        for attempt in range(self.max_retries):
            try:
                return self.client.chat.completions.create(**kwargs)
            
            except RateLimitError as e:
                if attempt == self.max_retries - 1:
                    raise
                
                wait_time = 2 ** attempt  # Exponential backoff
                logger.warning(f"Rate limit hit, waiting {wait_time}s")
                time.sleep(wait_time)
        
        raise Exception("Max retries exceeded")

# Usage
client = RateLimitAwareClient()
response = client.call_with_backoff(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### Production Setup with Rate Limit Monitoring

```python
from openai import OpenAI, RateLimitError
import time
import logging

logger = logging.getLogger(__name__)

def call_api_with_monitoring(prompt, max_retries=3):
    client = OpenAI()
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            
            logger.info(f"Request successful: {response.id}")
            return response
            
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = min(2 ** attempt, 60)  # Cap at 60s
                logger.warning(
                    f"Rate limit exceeded (attempt {attempt + 1}), "
                    f"waiting {wait_time}s before retry"
                )
                time.sleep(wait_time)
            else:
                logger.error("Max retries reached, rate limit still exceeded")
                raise
    
    raise Exception("Failed after all retries")
```

### Batch API for Rate Limit Bypass

```python
from openai import OpenAI
import json

client = OpenAI()

# Create batch file
batch_requests = []
for i in range(1000):
    batch_requests.append({
        "custom_id": f"request-{i}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": f"Task {i}"}]
        }
    })

# Upload batch file
with open("batch.jsonl", "w") as f:
    for req in batch_requests:
        f.write(json.dumps(req) + "\n")

batch_file = client.files.create(
    file=open("batch.jsonl", "rb"),
    purpose="batch"
)

# Create batch job (bypasses rate limits)
batch = client.batches.create(
    input_file_id=batch_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h"
)

print(f"Batch created: {batch.id}")
```

## Error Responses

- **429 Too Many Requests** - Rate limit exceeded, implement exponential backoff
- **400 Bad Request** - Invalid tier or limit configuration (rare)

## Rate Limiting / Throttling

**This IS the rate limiting documentation.**

Best practices:
- Monitor headers proactively
- Implement exponential backoff
- Use Batch API for large jobs
- Consider tier upgrades for higher limits
- Distribute load across projects if needed

## Differences from Other APIs

- **vs Anthropic**: Similar RPM/TPM system, different tier structure
- **vs Gemini**: Uses QPM (queries per minute) instead of RPM
- **vs Grok**: OpenAI-compatible rate limiting

## Limitations and Known Issues

- **Tier upgrades not instant**: May take time to reflect after spend [COMMUNITY] (OAIAPI-SC-SO-TIERLAG)
- **Model limits vary**: No published table of all model limits [COMMUNITY] (OAIAPI-SC-SO-MODLIM)
- **Burst limits undocumented**: Short burst behavior not fully documented [COMMUNITY] (OAIAPI-SC-SO-BURST)

## Gotchas and Quirks

- **Tokens counted both ways**: Both input AND output tokens count toward TPM [VERIFIED] (OAIAPI-SC-OAI-GRLMT)
- **Reset time approximate**: Reset headers show approximate time, not exact [COMMUNITY] (OAIAPI-SC-SO-RESET)
- **Project limits independent**: Can't pool limits across projects [VERIFIED] (OAIAPI-SC-OAI-ADMPRJ)

## Sources

- OAIAPI-SC-OAI-GRLMT - Rate limits guide
- OAIAPI-SC-OAI-ADMPRJ - Project administration
- OAIAPI-SC-OAI-OVERVIEW - API overview (headers)

## Document History

**[2026-03-20 15:00]**
- Initial documentation created
