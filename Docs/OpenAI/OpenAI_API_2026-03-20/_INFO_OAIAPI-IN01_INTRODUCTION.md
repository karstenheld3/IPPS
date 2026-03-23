# Introduction

**Doc ID**: OAIAPI-IN01
**Goal**: Document OpenAI API overview, base URL, versioning, authentication basics, and backwards compatibility
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

The OpenAI API is a RESTful API (v1) providing programmatic access to OpenAI's language models (GPT-5.4, GPT-5, o4-mini, o3-pro), image generation (gpt-image-1.5, DALL-E), video generation (Sora), audio (Whisper, TTS), embedding, and moderation models. The base URL is `https://api.openai.com/v1/`. Authentication uses `Authorization: Bearer` header with API keys. Optional headers include `OpenAI-Organization` and `OpenAI-Project` for multi-org/project routing. The API version is currently `2020-10-01` (returned in `openai-version` response header). OpenAI maintains backwards compatibility within major versions by avoiding breaking changes - new endpoints, optional parameters, and response properties are added without version bumps. Clients can supply custom request IDs via `X-Client-Request-Id` header for tracking. API responses include debug headers: `x-request-id` (unique request identifier), `openai-processing-ms` (processing time), rate limit headers, and organization info. [VERIFIED] (OAIAPI-SC-OAI-OVERVIEW)

## Key Facts

- **Base URL**: `https://api.openai.com/v1/` [VERIFIED] (OAIAPI-SC-OAI-OVERVIEW)
- **Current API version**: `v1` (returned as `2020-10-01` in `openai-version` header) [VERIFIED] (OAIAPI-SC-OAI-OVERVIEW)
- **Authentication**: Bearer token in `Authorization` header [VERIFIED] (OAIAPI-SC-OAI-OVERVIEW)
- **Multi-org support**: `OpenAI-Organization` and `OpenAI-Project` headers [VERIFIED] (OAIAPI-SC-OAI-OVERVIEW)
- **Custom request IDs**: `X-Client-Request-Id` header (max 512 ASCII chars) [VERIFIED] (OAIAPI-SC-OAI-OVERVIEW)
- **Debug headers**: `x-request-id`, `openai-processing-ms`, rate limit headers [VERIFIED] (OAIAPI-SC-OAI-OVERVIEW)

## Use Cases

- **API integration**: Building applications that use OpenAI models
- **Multi-org routing**: Managing API usage across multiple organizations and projects
- **Request tracking**: Logging request IDs for production troubleshooting
- **Rate limit monitoring**: Tracking usage via response headers

## Quick Reference

```
Base URL: https://api.openai.com/v1/
Headers:
  Authorization: Bearer $OPENAI_API_KEY
  OpenAI-Organization: $ORGANIZATION_ID (optional)
  OpenAI-Project: $PROJECT_ID (optional)
  X-Client-Request-Id: <custom-id> (optional, max 512 chars)
```

## API Overview

### Base URL and Versioning

All API requests use base URL `https://api.openai.com/v1/`. The current API version is `v1`, with internal version `2020-10-01` returned in the `openai-version` response header.

### Request Structure

API requests are RESTful HTTP requests with JSON payloads. Most endpoints use POST method with JSON request bodies.

## Authentication

### Bearer Token Authentication

All requests require authentication via `Authorization` header:

```
Authorization: Bearer OPENAI_API_KEY
```

### Multi-Organization and Project Routing

For users belonging to multiple organizations or using legacy user API keys, specify organization and project via headers:

```
OpenAI-Organization: $ORGANIZATION_ID
OpenAI-Project: $PROJECT_ID
```

- Organization IDs: Found on organization settings page
- Project IDs: Found on general settings page by selecting specific project
- Usage from these requests counts toward the specified organization and project

## Debugging Requests

### Response Headers

API responses include debug headers for troubleshooting:

**API Meta Information:**
- `openai-organization`: Organization associated with request
- `openai-processing-ms`: Processing time for API request
- `openai-version`: REST API version (`2020-10-01`)
- `x-request-id`: Unique identifier for request (use in troubleshooting)

**Rate Limiting Information:**
- `x-ratelimit-limit-requests`: Request limit
- `x-ratelimit-limit-tokens`: Token limit
- `x-ratelimit-remaining-requests`: Remaining requests
- `x-ratelimit-remaining-tokens`: Remaining tokens
- `x-ratelimit-reset-requests`: Time until request limit resets
- `x-ratelimit-reset-tokens`: Time until token limit resets

### Request ID Logging

OpenAI recommends logging `x-request-id` values in production deployments for efficient troubleshooting with support team. Official SDKs provide a property on response objects containing this value.

### Custom Request IDs (X-Client-Request-Id)

Clients can supply their own unique identifier via `X-Client-Request-Id` request header:

**Requirements:**
- Must contain only ASCII characters
- Maximum 512 characters
- Strongly recommended to be unique per request

**Benefits:**
- Control ID format (UUID, internal trace ID, etc.)
- OpenAI logs value in internal logs for supported endpoints
- Can share with support team during timeouts/network issues when `x-request-id` unavailable

**Supported endpoints:** chat/completions, embeddings, responses, and more

## Backwards Compatibility

### Compatibility Commitment

OpenAI avoids breaking changes in major API versions whenever reasonably possible. This applies to:
- REST API (currently `v1`)
- First-party SDKs (follow semantic versioning)
- Model families (like `gpt-4o`, `o4-mini`)

### Model Behavior Changes

**Important:** Model prompting behavior between snapshots is subject to change. Model outputs are variable by nature - expect changes between snapshots (e.g., `gpt-4o-2024-05-13` to `gpt-4o-2024-08-06`). Best practices:
- Use pinned model versions for consistent behavior
- Implement evals for applications

### Backwards-Compatible Changes

These changes do NOT constitute breaking changes:
- Adding new resources (URLs) to REST API and SDKs
- Adding new optional API parameters
- Adding new properties to JSON response objects or event data
- Changing order of properties in JSON response object
- Changing length or format of opaque strings (resource IDs, UUIDs)
- Adding new event types (streaming or Realtime API)

## SDK Examples (Python)

### Basic Request

```python
from openai import OpenAI

client = OpenAI()

# API key automatically loaded from OPENAI_API_KEY environment variable
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response)
```

### Multi-Organization Request

```python
from openai import OpenAI

client = OpenAI(
    organization="org-123456",
    project="proj-abc123"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Request ID Logging (Production)

```python
from openai import OpenAI
import logging

client = OpenAI()
logger = logging.getLogger(__name__)

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    # Log request ID for troubleshooting
    logger.info(f"Request completed: {response.id}")
except Exception as e:
    logger.error(f"Request failed: {e}")
```

## Error Responses

- **400 Bad Request** - Invalid request format or parameters
- **401 Unauthorized** - Missing or invalid API key
- **403 Forbidden** - API key lacks required permissions
- **429 Too Many Requests** - Rate limit exceeded, retry with backoff
- **500 Internal Server Error** - OpenAI server error, retry with exponential backoff

## Rate Limiting / Throttling

- **Applicable rate limits**: All endpoints have RPM (requests per minute) and TPM (tokens per minute) limits
- **Headers**: See Debugging Requests section for full list
- **Retry strategy**: Implement exponential backoff on 429 responses

## Differences from Other APIs

- **vs Anthropic**: Anthropic uses `x-api-key` header instead of `Authorization: Bearer`; no multi-org routing headers
- **vs Gemini**: Gemini uses `x-goog-api-key` header; no organization/project routing
- **vs Grok**: Grok is OpenAI-compatible (uses same authentication and base URL pattern)

## Limitations and Known Issues

- **Custom request IDs limited**: Max 512 ASCII characters, request fails with 400 if exceeded [VERIFIED] (OAIAPI-SC-OAI-OVERVIEW)
- **Model behavior variability**: Model outputs change between snapshots even with identical prompts [VERIFIED] (OAIAPI-SC-OAI-OVERVIEW)

## Gotchas and Quirks

- **Organization/Project headers optional**: Only needed for multi-org access or legacy user API keys [VERIFIED] (OAIAPI-SC-OAI-OVERVIEW)
- **API version in header**: The `openai-version` header returns `2020-10-01`, not `v1` [VERIFIED] (OAIAPI-SC-OAI-OVERVIEW)

## Sources

- OAIAPI-SC-OAI-OVERVIEW - API Overview (Introduction, Authentication, Debugging, Backwards compatibility)
- OAIAPI-SC-OAI-GOVRVW - Official guides overview

## Document History

**[2026-03-20 14:50]**
- Initial documentation created from developers.openai.com/api/reference/overview
