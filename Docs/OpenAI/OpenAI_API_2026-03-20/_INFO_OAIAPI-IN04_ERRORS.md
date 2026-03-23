# Errors and Error Handling

**Doc ID**: OAIAPI-IN04
**Goal**: Document OpenAI API error codes, response format, debugging with x-request-id
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

OpenAI API returns standard HTTP status codes with JSON error responses containing error type, code, message, and optional param/request_id fields. Common errors: 400 (invalid_request_error - bad parameters), 401 (authentication_error - invalid API key), 403 (permission_error - insufficient permissions), 404 (not_found_error - resource not found), 429 (rate_limit_error - quota exceeded), 500/503 (api_error/overloaded_error - server issues). Each response includes `x-request-id` header for troubleshooting - clients should log this value in production. Error response format: `{"error": {"type": "...", "code": "...", "message": "...", "param": null}}`. Retry strategy: exponential backoff for 429/500/503, no retry for 400/401/403/404. Official SDKs throw typed exceptions matching error types. [VERIFIED] (OAIAPI-SC-OAI-OVERVIEW, OAIAPI-SC-OAI-GERROR)

## Key Facts

- **Error format**: JSON with type, code, message fields [VERIFIED] (OAIAPI-SC-OAI-GERROR)
- **Request tracking**: `x-request-id` header in all responses [VERIFIED] (OAIAPI-SC-OAI-OVERVIEW)
- **HTTP status codes**: 400 (client error), 401/403 (auth), 429 (rate limit), 500/503 (server) [VERIFIED] (OAIAPI-SC-OAI-GERROR)
- **Retry-safe**: 429, 500, 503 should retry with exponential backoff [VERIFIED] (OAIAPI-SC-OAI-GERROR)
- **Non-retry**: 400, 401, 403, 404 indicate client issues [VERIFIED] (OAIAPI-SC-OAI-GERROR)

## Use Cases

- **Production logging**: Capturing x-request-id for support tickets
- **Error handling**: Implementing retry logic based on error type
- **Debugging**: Using request IDs to troubleshoot with OpenAI support
- **Monitoring**: Tracking error rates by type/code

## Quick Reference

```json
{
  "error": {
    "type": "invalid_request_error",
    "code": "parameter_invalid",
    "message": "Invalid value for 'temperature': must be between 0 and 2",
    "param": "temperature",
    "request_id": "req_abc123"
  }
}
```

## HTTP Status Codes

### 400 Bad Request
- **Error type**: `invalid_request_error`
- **Meaning**: Malformed request or invalid parameters
- **Action**: Fix request parameters, do not retry
- **Common causes**: Invalid JSON, missing required fields, out-of-range values

### 401 Unauthorized
- **Error type**: `authentication_error`
- **Meaning**: Missing, invalid, or expired API key
- **Action**: Check API key, do not retry with same key
- **Common causes**: No Authorization header, invalid Bearer token, expired key

### 403 Forbidden
- **Error type**: `permission_error`
- **Meaning**: API key lacks permissions for requested resource
- **Action**: Check account permissions, do not retry
- **Common causes**: Model access restricted, organization access denied, feature not enabled

### 404 Not Found
- **Error type**: `not_found_error`
- **Meaning**: Requested resource does not exist
- **Action**: Verify resource ID, do not retry
- **Common causes**: Invalid model ID, deleted resource, wrong endpoint

### 429 Too Many Requests
- **Error type**: `rate_limit_error`
- **Meaning**: Rate limit exceeded (RPM or TPM)
- **Action**: Retry with exponential backoff
- **Headers**: Check `x-ratelimit-reset-*` for reset time
- **Common causes**: Too many concurrent requests, token limit exceeded

### 500 Internal Server Error
- **Error type**: `api_error`
- **Meaning**: OpenAI server error
- **Action**: Retry with exponential backoff
- **Common causes**: Temporary server issue, service degradation

### 503 Service Unavailable
- **Error type**: `overloaded_error`
- **Meaning**: Servers temporarily overloaded
- **Action**: Retry with exponential backoff
- **Common causes**: High traffic, temporary capacity issues

## Error Response Format

### Standard Error Structure

```json
{
  "error": {
    "type": "string",
    "code": "string",
    "message": "string",
    "param": "string | null",
    "request_id": "string"
  }
}
```

### Error Fields

- **type**: Error category (invalid_request_error, authentication_error, etc.)
- **code**: Specific error code (parameter_invalid, insufficient_quota, etc.)
- **message**: Human-readable error description
- **param**: Name of invalid parameter (if applicable)
- **request_id**: Unique request identifier (also in x-request-id header)

## Error Types

### invalid_request_error
- **Causes**: Malformed JSON, invalid parameters, missing required fields
- **Example codes**: `parameter_invalid`, `parameter_missing`, `invalid_value`
- **Resolution**: Fix request format and parameters

### authentication_error
- **Causes**: Missing or invalid API key
- **Example codes**: `invalid_api_key`, `missing_api_key`
- **Resolution**: Provide valid API key in Authorization header

### permission_error
- **Causes**: Insufficient permissions for requested action
- **Example codes**: `insufficient_permissions`, `model_access_denied`
- **Resolution**: Check account tier, model access, organization settings

### not_found_error
- **Causes**: Resource does not exist
- **Example codes**: `resource_not_found`, `model_not_found`
- **Resolution**: Verify resource ID, check if resource was deleted

### rate_limit_error
- **Causes**: Exceeded RPM or TPM limits
- **Example codes**: `rate_limit_exceeded`, `insufficient_quota`
- **Resolution**: Implement exponential backoff, upgrade tier if needed

### api_error
- **Causes**: OpenAI server error
- **Resolution**: Retry with backoff, contact support if persistent

### overloaded_error
- **Causes**: Servers at capacity
- **Resolution**: Retry with backoff

## Request Tracking

### x-request-id Header

Every API response includes `x-request-id` header containing unique request identifier:
```
x-request-id: req_1234567890abcdef
```

**Purpose:**
- Troubleshooting with OpenAI support
- Correlating logs with API requests
- Debugging production issues

**Best practice:** Log x-request-id for all requests in production

### X-Client-Request-Id Header

Optionally provide custom request ID:
```
X-Client-Request-Id: my-trace-id-12345
```

**Benefits:**
- Use own ID format (UUID, trace ID, etc.)
- Track requests when x-request-id unavailable (timeouts)
- Correlate with internal systems

## SDK Examples (Python)

### Basic Error Handling

```python
from openai import OpenAI
from openai import APIError, RateLimitError, AuthenticationError

client = OpenAI()

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}]
    )
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    # Check API key
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
    # Implement backoff
except APIError as e:
    print(f"API error: {e}")
    # Retry with backoff
```

### Production Error Handling with Logging

```python
from openai import OpenAI
from openai import APIError, RateLimitError
import logging
import time

client = OpenAI()
logger = logging.getLogger(__name__)

def call_api_with_retry(max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": "Hello"}]
            )
            
            # Log request ID for troubleshooting
            logger.info(f"Request successful: {response.id}")
            return response
            
        except RateLimitError as e:
            wait_time = 2 ** attempt  # Exponential backoff
            logger.warning(f"Rate limit hit, retrying in {wait_time}s")
            time.sleep(wait_time)
            
        except APIError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.error(f"API error, retrying in {wait_time}s: {e}")
                time.sleep(wait_time)
            else:
                logger.error(f"Max retries reached: {e}")
                raise
                
    raise Exception("Max retries exceeded")
```

### Capturing Request ID

```python
from openai import OpenAI
import logging

client = OpenAI()
logger = logging.getLogger(__name__)

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}]
    )
    
    # Access request ID from response metadata
    request_id = response.id  # or from response headers
    logger.info(f"Request ID: {request_id}")
    
except Exception as e:
    # Log error with any available request ID
    logger.error(f"Request failed: {e}")
```

### Custom Request ID

```python
from openai import OpenAI
import uuid

client = OpenAI()

custom_id = str(uuid.uuid4())

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    extra_headers={
        "X-Client-Request-Id": custom_id
    }
)

print(f"Custom request ID: {custom_id}")
```

## Error Responses

- **400 Bad Request** - Invalid request parameters, fix request
- **401 Unauthorized** - Invalid API key, check authentication
- **403 Forbidden** - Insufficient permissions, check account access
- **404 Not Found** - Resource not found, verify resource ID
- **429 Too Many Requests** - Rate limit exceeded, implement backoff
- **500 Internal Server Error** - Server error, retry with backoff
- **503 Service Unavailable** - Service overloaded, retry with backoff

## Rate Limiting / Throttling

Rate limit errors (429) should trigger exponential backoff:
- First retry: 1-2 seconds
- Second retry: 2-4 seconds
- Third retry: 4-8 seconds
- Check `x-ratelimit-reset-*` headers for reset time

## Differences from Other APIs

- **vs Anthropic**: Similar error structure, different error type names
- **vs Gemini**: Uses Google Cloud error format (different structure)
- **vs Grok**: OpenAI-compatible error format

## Limitations and Known Issues

- **Request ID not in error body**: Some errors may not include request_id in JSON (always in header) [COMMUNITY] (OAIAPI-SC-SO-REQID)
- **Error messages may change**: Message text not guaranteed stable across versions [VERIFIED] (OAIAPI-SC-OAI-GERROR)

## Gotchas and Quirks

- **429 can mean quota or rate**: Rate limit error covers both RPM/TPM limits AND quota exhaustion [VERIFIED] (OAIAPI-SC-OAI-GERROR)
- **param field optional**: Not all errors include param field [VERIFIED] (OAIAPI-SC-OAI-GERROR)
- **Error codes undocumented**: Full list of error codes not publicly documented [COMMUNITY] (OAIAPI-SC-SO-ERRCODES)

## Sources

- OAIAPI-SC-OAI-OVERVIEW - API Overview (Debugging section)
- OAIAPI-SC-OAI-GERROR - Error codes guide
- OAIAPI-SC-GH-SDKPY - Python SDK error handling

## Document History

**[2026-03-20 14:58]**
- Initial documentation created
