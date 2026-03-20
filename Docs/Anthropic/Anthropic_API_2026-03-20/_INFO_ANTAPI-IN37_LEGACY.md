# Legacy APIs and Model Deprecations

**Doc ID**: ANTAPI-IN37
**Goal**: Document deprecated models, legacy API patterns, and migration guidance
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN03_VERSIONING.md [ANTAPI-IN03]` for API versioning
- `_INFO_ANTAPI-IN11_MODELS.md [ANTAPI-IN11]` for current model list

## Summary

Anthropic follows a structured model deprecation policy. Models are marked as deprecated with advance notice, then eventually removed from service. The legacy Text Completions API (`POST /v1/complete`) is fully deprecated in favor of the Messages API. Model deprecation dates and migration paths are published on the deprecations page. Users should migrate to current models and the Messages API for continued support.

## Key Facts

- **Deprecation Notice**: Published in advance on deprecations page
- **Legacy API**: Text Completions (`POST /v1/complete`) - fully deprecated
- **Current API**: Messages (`POST /v1/messages`)
- **Deprecated Models**: Claude 3.x series being phased out
- **Migration**: Update model ID in API calls; Messages API is the only supported interface
- **Status**: Ongoing deprecation cycle

## Deprecated Models (as of 2026-03-20)

- **claude-3-7-sonnet-20250219** - Deprecated; migrate to claude-sonnet-4-20250514
- **claude-3-5-sonnet-20241022** - Deprecated; migrate to claude-sonnet-4-20250514
- **claude-3-5-sonnet-20240620** - Deprecated
- **claude-3-5-haiku-20241022** - Deprecated; migrate to claude-haiku-4-5-20251001
- **claude-3-opus-20240229** - Deprecated; migrate to claude-opus-4-20250514
- **claude-3-sonnet-20240229** - Deprecated
- **claude-3-haiku-20240307** - Deprecated (some features still supported)

## Legacy Text Completions API

The Text Completions API (`POST /v1/complete`) is fully deprecated. All users should migrate to the Messages API:

### Migration Example

```python
import anthropic

client = anthropic.Anthropic()

# LEGACY (deprecated) - Text Completions
# response = client.completions.create(
#     model="claude-2",
#     max_tokens_to_sample=1024,
#     prompt="\n\nHuman: Hello\n\nAssistant:",
# )

# CURRENT - Messages API
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
)
print(response.content[0].text)
```

### Key Differences from Text Completions

- **Structured messages** instead of raw prompt string
- **Content blocks** in response instead of flat text
- **Role-based** conversation (user, assistant) instead of Human/Assistant format
- **Stop reasons** instead of stop_reason field
- **Token usage** reported in response body
- **Streaming** via SSE events instead of raw text chunks
- **Tool use** natively supported (no prompt engineering needed)

## Deprecation Timeline Pattern

1. **Active** - Model fully supported, recommended for use
2. **Deprecated** - Model still works but deprecated notice published, migration recommended
3. **End of Life** - Model removed from service, API returns error

## API Version Compatibility

- Current GA version: `2023-06-01`
- Beta features accessed via `anthropic-beta` header
- Older API versions may lose support; always use current version
- New features may require newer model versions

## Gotchas and Quirks

- Deprecated models still function until their end-of-life date
- Model IDs change between versions; do not hardcode without checking deprecation page
- The Messages API is the only active API; Text Completions is fully deprecated
- Some deprecated models retain limited support for specific use cases
- Beta features on deprecated models may stop working before the model EOL
- Check `client.models.list()` for currently available models

## Related Endpoints

- `_INFO_ANTAPI-IN03_VERSIONING.md [ANTAPI-IN03]` - API version management
- `_INFO_ANTAPI-IN11_MODELS.md [ANTAPI-IN11]` - Current model capabilities
- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` - Current Messages API (replacement for Text Completions)

## Sources

- ANTAPI-SC-ANTH-DEPR - https://platform.claude.com/docs/en/about-claude/model-deprecations - Deprecation schedule
- ANTAPI-SC-ANTH-LEGACY - https://platform.claude.com/docs/en/api/complete - Legacy Text Completions reference

## Document History

**[2026-03-20 04:33]**
- Initial documentation created from deprecation schedule and legacy API reference
