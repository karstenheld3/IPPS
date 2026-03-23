# Production Best Practices

**Doc ID**: OAIAPI-IN61
**Goal**: Document production best practices for deploying OpenAI API applications - security, reliability, monitoring
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

Production best practices cover security, reliability, cost management, and safety for OpenAI API deployments. Key areas: API key management (use project-scoped keys, rotate regularly, never expose in client code), rate limit handling (implement exponential backoff with jitter), error handling (handle 429, 500, 503 with retries), input sanitization (validate and sanitize user inputs), output validation (check for refusals, content filter triggers), monitoring (track token usage, latency, error rates), cost control (set spending limits, use prompt caching, consider flex processing for latency-insensitive workloads), safety (follow safety best practices, implement content moderation, restrict output scope). The API returns rate limit headers (`x-ratelimit-limit-*`, `x-ratelimit-remaining-*`, `x-ratelimit-reset-*`) for proactive throttling. Use the Moderation API for content screening. Set `max_completion_tokens` to control output length and cost. Use `store: false` to disable response storage when not needed. Implement timeouts and circuit breakers for production resilience. [VERIFIED] (OAIAPI-SC-OAI-GBPRD)

## Key Facts

- **API key security**: Project-scoped keys, never in client code [VERIFIED] (OAIAPI-SC-OAI-GBPRD)
- **Rate limits**: Exponential backoff with jitter on 429 responses [VERIFIED] (OAIAPI-SC-OAI-GBPRD)
- **Error handling**: Retry on 429, 500, 503; don't retry 400, 401 [VERIFIED] (OAIAPI-SC-OAI-GBPRD)
- **Cost control**: max_completion_tokens, prompt caching, flex processing [VERIFIED] (OAIAPI-SC-OAI-GBPRD)
- **Safety**: Moderation API, input validation, output scope restriction [VERIFIED] (OAIAPI-SC-OAI-GBPRD)
- **Monitoring**: Track tokens, latency, errors, cost per request [VERIFIED] (OAIAPI-SC-OAI-GBPRD)

## Security Best Practices

- **Never expose API keys in client-side code** - use server-side proxy
- **Use project-scoped keys** - limit blast radius of key compromise
- **Rotate keys regularly** - create new, deploy, delete old
- **Use service accounts for automation** - not personal keys
- **Environment variables** - never hardcode keys in source code
- **mTLS** - enable for enterprise security requirements
- **Audit logs** - monitor key usage and administrative actions

## Reliability Patterns

### Exponential Backoff

```python
from openai import OpenAI, RateLimitError, APIError
import time
import random

client = OpenAI()

def call_with_retry(fn, max_retries=5, base_delay=1.0):
    """Call API with exponential backoff and jitter"""
    for attempt in range(max_retries):
        try:
            return fn()
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            retry_after = e.response.headers.get("retry-after")
            if retry_after:
                delay = max(delay, float(retry_after))
            print(f"Rate limited. Retrying in {delay:.1f}s...")
            time.sleep(delay)
        except APIError as e:
            if e.status_code in (500, 503) and attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
            else:
                raise

# Usage
response = call_with_retry(
    lambda: client.chat.completions.create(
        model="gpt-5.4",
        messages=[{"role": "user", "content": "Hello"}]
    )
)
```

### Rate Limit Headers

```python
def check_rate_limits(response):
    """Extract rate limit info from response headers"""
    headers = response.headers if hasattr(response, 'headers') else {}
    return {
        "requests_limit": headers.get("x-ratelimit-limit-requests"),
        "requests_remaining": headers.get("x-ratelimit-remaining-requests"),
        "tokens_limit": headers.get("x-ratelimit-limit-tokens"),
        "tokens_remaining": headers.get("x-ratelimit-remaining-tokens"),
        "reset": headers.get("x-ratelimit-reset-requests")
    }
```

## Cost Management

- **max_completion_tokens**: Always set to prevent runaway generation
- **Prompt caching**: Automatic 50-90% discount on repeated prompt prefixes
- **Flex processing**: 50% discount for latency-insensitive workloads (`service_tier: "flex"`)
- **Batch API**: 50% discount for async batch processing
- **Model selection**: Use smaller models (gpt-4.1-mini, gpt-4.1-nano) for simpler tasks
- **Usage API**: Monitor costs per project via admin endpoints

## Safety Practices

- **Moderation API**: Screen user inputs and model outputs
- **Input validation**: Sanitize, length-limit, and validate all user inputs
- **Output scope**: Use structured outputs to constrain response format
- **Content filtering**: Handle `finish_reason: "content_filter"` gracefully
- **Refusal handling**: Check `message.refusal` field for safety refusals
- **User identification**: Pass `user` parameter for abuse tracking

### Moderation Check

```python
from openai import OpenAI

client = OpenAI()

def moderate_input(text: str) -> bool:
    """Returns True if content is safe"""
    result = client.moderations.create(input=text)
    return not result.results[0].flagged

def safe_completion(user_input: str):
    if not moderate_input(user_input):
        return "I cannot process this request."
    
    response = client.chat.completions.create(
        model="gpt-5.4",
        messages=[{"role": "user", "content": user_input}],
        max_completion_tokens=500
    )
    
    output = response.choices[0].message.content
    
    if not moderate_input(output):
        return "The response was filtered for safety."
    
    return output
```

## Monitoring Checklist

- **Token usage**: Track prompt_tokens, completion_tokens per request
- **Cached tokens**: Monitor prompt_tokens_details.cached_tokens for caching efficiency
- **Latency**: P50, P95, P99 response times
- **Error rates**: 4xx and 5xx error percentages
- **Cost per request**: Track spending via Usage/Cost API
- **Model performance**: Quality metrics specific to your use case
- **Rate limit proximity**: Alert when remaining requests/tokens < threshold

## Error Responses and Handling

- **400** - Bad request. Fix request parameters. Do not retry
- **401** - Invalid API key. Check key. Do not retry
- **403** - Forbidden. Check permissions. Do not retry
- **404** - Not found. Check resource ID. Do not retry
- **422** - Invalid schema (structured outputs). Fix schema. Do not retry
- **429** - Rate limited. Retry with exponential backoff
- **500** - Server error. Retry with backoff
- **503** - Service unavailable. Retry with backoff

## Differences from Other APIs

- **vs Anthropic**: Similar best practices. Anthropic has `anthropic-ratelimit-*` headers
- **vs Gemini**: Google Cloud quotas and IAM for access control
- **vs Grok**: Uses OpenAI-compatible API; same patterns apply

## Sources

- OAIAPI-SC-OAI-GBPRD - Production Best Practices Guide
- OAIAPI-SC-OAI-GSAFE - Safety Best Practices Guide
- OAIAPI-SC-OAI-GRLIM - Rate Limits Guide

## Document History

**[2026-03-20 18:48]**
- Initial documentation created
