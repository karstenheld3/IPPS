# API Versioning and Beta Headers

**Doc ID**: ANTAPI-IN03
**Goal**: Document API version management, version history, and beta feature access
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN01_INTRODUCTION.md [ANTAPI-IN01]` for base URL and general overview

## Summary

The Anthropic API uses the `anthropic-version` header for version control. The current (and only GA) version is `2023-06-01`. Within a version, Anthropic may add optional inputs, additional output values, new enum variants, and change error conditions, but will not break existing documented usage. Beta features are accessed via the `anthropic-beta` header with feature-specific identifiers following the `feature-name-YYYY-MM-DD` naming convention.

## Key Facts

- **Version Header**: `anthropic-version: 2023-06-01`
- **Current Version**: `2023-06-01`
- **Previous Version**: `2023-01-01` (deprecated)
- **Beta Header**: `anthropic-beta: feature-name-YYYY-MM-DD`
- **Multiple Betas**: Comma-separated in a single header
- **SDK Handling**: SDKs set version header automatically

## Stability Guarantees (within a version)

For any given API version, Anthropic preserves:

- Existing input parameters
- Existing output parameters

Anthropic may:

- Add additional optional inputs
- Add additional values to the output
- Change conditions for specific error types
- Add new variants to enum-like output values (e.g., streaming event types)

## Version History

### 2023-06-01 (current)

- New format for streaming SSE: completions are incremental (deltas, not cumulative)
- All events are named events (not data-only events)
- Removed `data: [DONE]` event
- Removed legacy `exception` and `truncated` values in responses

### 2023-01-01 (deprecated)

- Initial release

## Beta Headers

### Usage

Include the `anthropic-beta` header to access experimental features:

```python
import anthropic

client = anthropic.Anthropic()

# Using beta namespace in SDK
response = client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
    betas=["files-api-2025-04-14"],
)
```

### Raw HTTP

```
POST /v1/messages HTTP/1.1
Content-Type: application/json
X-API-Key: YOUR_API_KEY
anthropic-beta: files-api-2025-04-14
```

### Multiple Beta Features

Comma-separated in a single header:

```
anthropic-beta: feature1,feature2,feature3
```

### Version Naming Convention

Beta feature names follow `feature-name-YYYY-MM-DD` where the date indicates when the beta version was released. Always use the exact name as documented.

### Beta Feature Characteristics

Beta features are experimental and may:

- Have breaking changes with notice
- Be deprecated or removed
- Have different rate limits or pricing
- Not be available in all regions

## Error Codes

- **400** `invalid_request_error` - Invalid or unsupported beta header value (e.g., `"Unsupported beta header: invalid-beta-name"`)

## Gotchas and Quirks

- The `anthropic-version` value has been `2023-06-01` since June 2023; new features use beta headers instead of new API versions
- Always use the latest API version; previous versions are deprecated and may be unavailable for new users
- Beta features accessed via the `beta` namespace in SDKs (`client.beta.messages.create()`)
- Streaming changed significantly between 2023-01-01 and 2023-06-01: deltas became incremental rather than cumulative

## Related Endpoints

- `_INFO_ANTAPI-IN01_INTRODUCTION.md [ANTAPI-IN01]` - API overview
- `_INFO_ANTAPI-IN04_ERRORS.md [ANTAPI-IN04]` - Error handling for invalid beta headers
- `_INFO_ANTAPI-IN28_FILES_API.md [ANTAPI-IN28]` - Files API (beta feature)
- `_INFO_ANTAPI-IN29_SKILLS_API.md [ANTAPI-IN29]` - Skills API (beta feature)

## Sources

- ANTAPI-SC-ANTH-VERSION - https://platform.claude.com/docs/en/api/versioning - Version history, stability guarantees
- ANTAPI-SC-ANTH-BETAHDR - https://platform.claude.com/docs/en/api/beta-headers - Beta header usage, naming, errors

## Document History

**[2026-03-20 02:18]**
- Initial documentation created from versioning and beta headers pages
