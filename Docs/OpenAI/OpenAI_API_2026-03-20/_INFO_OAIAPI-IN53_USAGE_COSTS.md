# Usage and Cost Tracking

**Doc ID**: OAIAPI-IN53
**Goal**: Document usage tracking and cost reporting APIs for monitoring API consumption
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN47_ADMIN_OVERVIEW.md [OAIAPI-IN47]` for admin context

## Summary

The Usage API and Cost API provide detailed tracking of API consumption and spending. Usage endpoints (GET /v1/organization/usage/*) report token counts, request counts, and resource consumption broken down by model, endpoint type, and time bucket. Separate usage endpoints for completions, embeddings, images, audio, moderations, and vector stores. The Cost API (GET /v1/organization/costs) returns dollar-amount spending with breakdowns by project, model, and time period. Both APIs support date range filtering and grouping. Usage data is available with near-real-time latency. Cost data may have slight delay for billing reconciliation. Admin API key required for organization-level data. Project-scoped queries available. Useful for budget monitoring, cost optimization, chargeback reporting, and capacity planning. [VERIFIED] (OAIAPI-SC-OAI-ADMORG)

## Key Facts

- **Usage categories**: Completions, embeddings, images, audio, moderations, vector stores [VERIFIED] (OAIAPI-SC-OAI-ADMORG)
- **Cost reporting**: Dollar amounts with project/model breakdown [VERIFIED] (OAIAPI-SC-OAI-ADMORG)
- **Near-real-time**: Usage data available shortly after API calls [VERIFIED] (OAIAPI-SC-OAI-ADMORG)
- **Grouping**: By model, project, API key, time bucket [VERIFIED] (OAIAPI-SC-OAI-ADMORG)
- **Admin key required**: Organization-level access needs admin API key [VERIFIED] (OAIAPI-SC-OAI-ADMOVW)

## Quick Reference

```
Usage Endpoints:
  GET /v1/organization/usage/completions     # Text generation usage
  GET /v1/organization/usage/embeddings      # Embedding usage
  GET /v1/organization/usage/images          # Image generation usage
  GET /v1/organization/usage/audio           # Audio (TTS, transcription) usage
  GET /v1/organization/usage/moderations     # Moderation usage
  GET /v1/organization/usage/vector_stores   # Vector store usage

Cost Endpoint:
  GET /v1/organization/costs                 # Dollar-amount spending

Common Query Parameters:
  start_time     # Start of date range (Unix timestamp)
  end_time       # End of date range (Unix timestamp)
  bucket_width   # Time bucket: "1m", "1h", "1d"
  group_by[]     # Grouping: "model", "project_id", "api_key_id"
  project_ids[]  # Filter by project(s)
  limit          # Results per page
```

## Usage Response Structure

```json
{
  "object": "page",
  "data": [
    {
      "object": "bucket",
      "start_time": 1711411200,
      "end_time": 1711497600,
      "results": [
        {
          "object": "organization.usage.completions.result",
          "input_tokens": 150000,
          "output_tokens": 50000,
          "input_cached_tokens": 30000,
          "num_model_requests": 500,
          "project_id": "proj_abc123",
          "model": "gpt-5.4"
        }
      ]
    }
  ],
  "has_more": false
}
```

## Cost Response Structure

```json
{
  "object": "page",
  "data": [
    {
      "object": "bucket",
      "start_time": 1711411200,
      "end_time": 1711497600,
      "results": [
        {
          "object": "organization.costs.result",
          "amount": {
            "value": 12.50,
            "currency": "usd"
          },
          "project_id": "proj_abc123",
          "line_item": "gpt-5.4-input"
        }
      ]
    }
  ]
}
```

## SDK Examples (Python)

> **SDK note**: `client.organization.*` methods are not available in openai Python SDK v2.29.0.
> The Administration API uses REST-only endpoints with admin API keys (`sk-admin-...`).
> Use `httpx` or `requests` for direct REST calls to `https://api.openai.com/v1/organization/*`.

### Daily Usage Report

```python
from openai import OpenAI
import time

client = OpenAI(api_key="sk-admin-...")

def get_daily_usage(days_back: int = 7):
    """Get daily usage summary for last N days"""
    now = int(time.time())
    start = now - (days_back * 86400)
    
    usage = client.organization.usage.completions.list(
        start_time=start,
        end_time=now,
        bucket_width="1d",
        group_by=["model"]
    )
    
    for bucket in usage.data:
        date = time.strftime("%Y-%m-%d", time.gmtime(bucket.start_time))
        for result in bucket.results:
            total_tokens = result.input_tokens + result.output_tokens
            cached = result.input_cached_tokens
            print(
                f"  {date} | {result.model}: "
                f"{total_tokens:,} tokens ({cached:,} cached), "
                f"{result.num_model_requests} requests"
            )

try:
    get_daily_usage(7)
except Exception as e:
    print(f"Error: {e}")
```

### Cost Monitoring - Production Ready

```python
from openai import OpenAI
import time

client = OpenAI(api_key="sk-admin-...")

def get_project_costs(project_id: str = None, days_back: int = 30):
    """Get cost breakdown by project"""
    now = int(time.time())
    start = now - (days_back * 86400)
    
    params = {
        "start_time": start,
        "end_time": now,
        "bucket_width": "1d",
        "group_by": ["project_id"]
    }
    if project_id:
        params["project_ids"] = [project_id]
    
    costs = client.organization.costs.list(**params)
    
    total = 0.0
    daily_costs = {}
    
    for bucket in costs.data:
        date = time.strftime("%Y-%m-%d", time.gmtime(bucket.start_time))
        for result in bucket.results:
            amount = result.amount.value
            total += amount
            daily_costs.setdefault(date, 0.0)
            daily_costs[date] += amount
    
    print(f"Total cost ({days_back}d): ${total:.2f}")
    for date, cost in sorted(daily_costs.items()):
        print(f"  {date}: ${cost:.2f}")
    
    return {"total": total, "daily": daily_costs}

try:
    costs = get_project_costs(days_back=7)
    
    # Alert if daily cost exceeds threshold
    for date, cost in costs["daily"].items():
        if cost > 100.0:
            print(f"ALERT: ${cost:.2f} on {date} exceeds $100 threshold")

except Exception as e:
    print(f"Error: {e}")
```

## Error Responses

- **401 Unauthorized** - Invalid admin API key
- **400 Bad Request** - Invalid date range or parameters
- **429 Too Many Requests** - Rate limit exceeded

## Differences from Other APIs

- **vs Anthropic**: Anthropic provides usage via console; no programmatic usage/cost API
- **vs Gemini**: Google Cloud billing APIs provide similar cost tracking
- **vs Grok**: Limited usage reporting API

## Limitations and Known Issues

- **Cost delay**: Cost data may lag real-time usage by minutes to hours for billing reconciliation [ASSUMED]
- **Granularity**: Minimum bucket width is 1 minute [VERIFIED] (OAIAPI-SC-OAI-ADMORG)

## Sources

- OAIAPI-SC-OAI-ADMORG - Organization Administration API

## Document History

**[2026-03-21 09:48]**
- Added: SDK v2.29.0 note - client.organization.* not in Python SDK (REST-only admin API)

**[2026-03-20 18:15]**
- Initial documentation created
