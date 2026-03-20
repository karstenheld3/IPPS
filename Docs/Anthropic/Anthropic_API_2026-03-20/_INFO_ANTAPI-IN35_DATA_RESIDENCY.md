# Data Residency and Region Configuration

**Doc ID**: ANTAPI-IN35
**Goal**: Document inference_geo parameter, regional routing, and data residency options
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` for Messages API request schema

## Summary

Data residency controls where API inference is processed geographically. The `inference_geo` parameter on the Messages API request restricts processing to specific regions. Currently, `"us"` forces US-only inference with a 1.1x pricing multiplier (Opus 4.6+ models). Global routing (default) dynamically routes for optimal availability. Third-party platforms (Bedrock, Vertex AI) offer their own regional vs global endpoint distinctions with a 10% regional premium starting with Sonnet 4.5/Haiku 4.5.

## Key Facts

- **Parameter**: `inference_geo` on Messages API request
- **Values**: `"us"` (US-only), default (global routing)
- **Pricing**: 1.1x multiplier for US-only (Opus 4.6+ models)
- **Workspace Default**: `default_inference_geo` setting
- **Third-Party Regional**: 10% premium on Bedrock/Vertex regional endpoints
- **Status**: GA

## Usage

```python
import anthropic

client = anthropic.Anthropic()

# US-only inference (1.1x pricing multiplier)
message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    inference_geo="us",
    messages=[{"role": "user", "content": "Analyze this sensitive data..."}],
)

# Global routing (default, standard pricing)
message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
)
```

## Workspace Default

Workspaces can set a `default_inference_geo` that applies to all requests unless overridden per-request:

```python
# Per-request override takes precedence over workspace default
message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    inference_geo="us",  # Overrides workspace default
    messages=[{"role": "user", "content": "Process this"}],
)
```

## Third-Party Platforms

Starting with Claude Sonnet 4.5 and Haiku 4.5:

- **Global endpoints** - Dynamic routing across regions, standard pricing
- **Regional endpoints** - Guaranteed geographic routing, 10% premium

Applies to AWS Bedrock and Google Vertex AI. Claude API (1P) is global-only with optional `inference_geo` for US restriction.

## Gotchas and Quirks

- `inference_geo` pricing only affects Opus 4.6+ models; earlier models unaffected
- The 1.1x multiplier stacks with other pricing modifiers (cache, batch, fast mode)
- Global routing is the default and offers best availability
- Workspace `default_inference_geo` can be overridden per-request
- Usage reports group by `inference_geo` when that dimension is specified
- For models that don't support `inference_geo`, the value is `"not_available"` in reports

## Related Endpoints

- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` - Messages API (inference_geo parameter)
- `_INFO_ANTAPI-IN12_PRICING.md [ANTAPI-IN12]` - Data residency pricing multiplier
- `_INFO_ANTAPI-IN33_USAGE_API.md [ANTAPI-IN33]` - Usage reports with geo grouping

## Sources

- ANTAPI-SC-ANTH-DATARES - https://platform.claude.com/docs/en/build-with-claude/data-residency - Data residency guide
- ANTAPI-SC-ANTH-PRICING - https://platform.claude.com/docs/en/about-claude/pricing - Regional pricing

## Document History

**[2026-03-20 04:28]**
- Initial documentation created from data residency and pricing guides
