# Models API

**Doc ID**: ANTAPI-IN11
**Goal**: Document GET /v1/models endpoints for model discovery and capability information
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN01_INTRODUCTION.md [ANTAPI-IN01]` for base URL, auth headers

## Summary

The Models API provides two endpoints for discovering available Claude models and their capabilities. `GET /v1/models` lists all models (most recent first) with pagination support. `GET /v1/models/{model_id}` retrieves detailed information including `max_input_tokens`, `max_tokens` (output limit), and a `capabilities` object covering thinking, vision, PDF, citations, batch, code execution, structured output, and effort levels. As of March 2026, capability fields are returned directly on the model response.

## Key Facts

- **List Endpoint**: `GET /v1/models`
- **Get Endpoint**: `GET /v1/models/{model_id}`
- **SDK Methods**: `client.models.list()`, `client.models.retrieve(model_id)`
- **Pagination**: Cursor-based (after_id, before_id, limit)
- **Default Limit**: 20 items per page (range: 1-1000)
- **Sort Order**: Most recently released first
- **Status**: GA

## Endpoints

### GET /v1/models - List Models

**Query Parameters:**

- **after_id** (`string`, optional) - Cursor for forward pagination
- **before_id** (`string`, optional) - Cursor for backward pagination
- **limit** (`integer`, default: `20`, range: 1-1000) - Items per page

```python
import anthropic

client = anthropic.Anthropic()

# List all models
models = client.models.list()
for model in models:
    print(f"{model.id}: {model.display_name}")
    print(f"  Context: {model.max_input_tokens} tokens")
    print(f"  Max output: {model.max_output_tokens} tokens")
```

### GET /v1/models/{model_id} - Get Model

```python
import anthropic

client = anthropic.Anthropic()

model = client.models.retrieve("claude-opus-4-7")
print(f"Name: {model.display_name}")
print(f"Context window: {model.max_input_tokens}")
print(f"Max output: {model.max_output_tokens}")
print(f"Released: {model.created_at}")

# Check capabilities
caps = model.capabilities
print(f"Thinking: {caps.thinking.supported}")
print(f"Vision: {caps.vision.supported}")
print(f"PDF: {caps.pdf.supported}")
print(f"Citations: {caps.citations.supported}")
print(f"Batch: {caps.batch.supported}")
print(f"Code execution: {caps.code_execution.supported}")
print(f"Structured output: {caps.structured_output.supported}")
```

## ModelInfo Response

- **id** (`string`) - Model identifier (e.g., `"claude-opus-4-7"`)
- **type** (`string`) - Object type
- **display_name** (`string`) - Human-readable name
- **created_at** (`string`) - RFC 3339 release datetime
- **max_input_tokens** (`integer`) - Maximum input context window in tokens
- **max_output_tokens** (`integer`) - Maximum value for `max_tokens` parameter
- **capabilities** (`ModelCapabilities`) - Model capability information:
  - **batch** (`CapabilitySupport`) - Batch API support
  - **citations** (`CapabilitySupport`) - Citation generation support
  - **code_execution** (`CapabilitySupport`) - Code execution tool support
  - **context_management** (`ContextManagementCapability`) - Compaction/editing strategies
  - **vision** (`CapabilitySupport`) - Image content block support
  - **pdf** (`CapabilitySupport`) - PDF content block support
  - **structured_output** (`CapabilitySupport`) - JSON mode / strict schemas
  - **thinking** (`ThinkingCapability`) - Extended thinking support
    - **types** (`ThinkingTypes`) - Supported configs (adaptive, enabled)
  - **effort** (`EffortCapability`) - Effort levels (low, medium, high, max)

## Available Models (as of 2026-05-22)

**Active:**
- **claude-opus-4-7** - Most capable GA model, step-change in agentic coding, new tokenizer (up to 35% more tokens)
- **claude-opus-4-6** - Previous top-tier model, 1M context GA
- **claude-sonnet-4-6** - Best speed/intelligence ratio, 1M context GA
- **claude-haiku-4-5-20251001** - Fastest model with near-frontier intelligence

**Deprecated (retiring June 15, 2026):**
- **claude-sonnet-4-20250514** - Deprecated, migrate to claude-sonnet-4-6
- **claude-opus-4-20250514** - Deprecated, migrate to claude-opus-4-7

**Retired:**
- **claude-3-haiku-20240307** - Retired April 20, 2026

**Special:**
- **Claude Mythos Preview** - Gated research preview for defensive cybersecurity (Project Glasswing, invitation-only)

**1M Context Window:** GA on Opus 4.7, Opus 4.6, and Sonnet 4.6. Retired for Sonnet 4.5 and Sonnet 4 (April 30, 2026).

**300k Output Tokens:** On Batch API for Opus 4.7, Opus 4.6, and Sonnet 4.6 via `output-300k-2026-03-24` beta header.

## Gotchas and Quirks

- Model IDs include version dates (e.g., `claude-opus-4-7`); use the full ID in API calls
- The `created_at` field may be set to epoch value if release date is unknown
- Capability `supported` field is a boolean indicating feature availability for that model
- Models are listed most recent first; use pagination for older models
- Beta models are available via `client.beta.models.list()` with additional beta-specific capabilities

## Related Endpoints

- `_INFO_ANTAPI-IN12_PRICING.md [ANTAPI-IN12]` - Token pricing per model
- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` - Messages API (model parameter)

## Sources

- ANTAPI-SC-ANTH-MODLST - https://platform.claude.com/docs/en/api/models/list - List models endpoint
- ANTAPI-SC-ANTH-MODGET - https://platform.claude.com/docs/en/api/models/retrieve - Get model endpoint
- ANTAPI-SC-ANTH-MODOVW - https://platform.claude.com/docs/en/about-claude/models/overview - Models overview

## SDK Verification

Examples updated for `anthropic` SDK 0.104.0. Pending re-verification in Prompt 3.

## Document History

**[2026-05-22]**
- Updated from Anthropic_API_2026-03-20
- Changed: Available models list updated (Opus 4.7 as top, Mythos Preview, deprecations)
- Added: 300k output tokens on Batch API, 1M context GA status
- Added: Capability fields returned directly on model response (March 2026 update)

**[2026-03-20 06:50]**
- Added: SDK verification section (anthropic 0.104.0, all 2 examples valid)

**[2026-03-20 02:55]**
- Initial documentation created from Models API reference
