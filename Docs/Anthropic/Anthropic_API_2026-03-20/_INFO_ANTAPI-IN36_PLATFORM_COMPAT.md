# Platform Compatibility (Bedrock, Vertex AI, Foundry)

**Doc ID**: ANTAPI-IN36
**Goal**: Document Claude availability on AWS Bedrock, Google Vertex AI, and Microsoft Foundry
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN01_INTRODUCTION.md [ANTAPI-IN01]` for direct API baseline

## Summary

Claude models are available on three third-party cloud platforms in addition to the direct Anthropic API: AWS Bedrock, Google Vertex AI, and Microsoft Azure AI Foundry. Each platform provides its own authentication, endpoints, SDKs, and pricing. The Anthropic Python SDK supports all three via platform-specific client classes (`AnthropicBedrock`, `AnthropicVertex`). Feature availability may differ from the direct API; not all beta features are available on all platforms.

## Key Facts

- **AWS Bedrock**: `AnthropicBedrock` client, AWS IAM auth
- **Google Vertex AI**: `AnthropicVertex` client, Google Cloud auth
- **Microsoft Foundry**: Azure authentication
- **SDK Install**: `pip install anthropic[bedrock]` or `anthropic[vertex]`
- **Model IDs**: Platform-specific model identifiers
- **Pricing**: Platform-specific (10% regional premium on Bedrock/Vertex for 4.5+ models)
- **Status**: GA

## AWS Bedrock

### Installation and Setup

```python
# Install with Bedrock support
# pip install anthropic[bedrock]

import anthropic

client = anthropic.AnthropicBedrock(
    aws_region="us-east-1",
    # Uses AWS credentials from environment (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    # or IAM role, AWS profile, etc.
)

message = client.messages.create(
    model="us.anthropic.claude-sonnet-4-20250514-v1:0",  # Bedrock model ID
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello from Bedrock!"}],
)
print(message.content[0].text)
```

### Bedrock Specifics

- Model IDs differ from direct API (e.g., `us.anthropic.claude-sonnet-4-20250514-v1:0`)
- Authentication via AWS IAM (credentials, roles, profiles)
- Global vs regional endpoints available (4.5+ models)
- Cross-region inference support

## Google Vertex AI

### Installation and Setup

```python
# Install with Vertex support
# pip install anthropic[vertex]

import anthropic

client = anthropic.AnthropicVertex(
    project_id="my-gcp-project",
    region="us-east5",
    # Uses Google Cloud credentials from environment or application default credentials
)

message = client.messages.create(
    model="claude-sonnet-4@20250514",  # Vertex model ID
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello from Vertex AI!"}],
)
print(message.content[0].text)
```

### Vertex AI Specifics

- Model IDs use `@` format (e.g., `claude-sonnet-4@20250514`)
- Authentication via Google Cloud Application Default Credentials
- Global vs regional endpoints available (4.5+ models)
- Project and region must be specified

## Microsoft Azure AI Foundry

- Claude available via Azure AI Foundry
- Azure authentication mechanisms
- See Microsoft Foundry pricing documentation for details

## Feature Availability

Not all features available on direct API are available on third-party platforms. Check platform-specific documentation for:

- Beta features (may not be available)
- Streaming support
- Tool use capabilities
- Extended thinking
- Batch processing
- Files API

## Gotchas and Quirks

- Model IDs differ across platforms; use platform-specific identifiers
- Auth mechanisms are platform-native (AWS IAM, Google Cloud, Azure AD)
- Regional endpoints on Bedrock/Vertex have a 10% price premium (Sonnet 4.5+ models)
- Beta features may lag behind the direct API
- Rate limits are set by the platform, not Anthropic
- The Anthropic SDK wraps platform-specific APIs for consistent interface
- Some Admin API features are not available on third-party platforms

## Related Endpoints

- `_INFO_ANTAPI-IN01_INTRODUCTION.md [ANTAPI-IN01]` - Direct API baseline
- `_INFO_ANTAPI-IN05_SDKS.md [ANTAPI-IN05]` - SDK platform-specific clients
- `_INFO_ANTAPI-IN12_PRICING.md [ANTAPI-IN12]` - Third-party platform pricing

## Sources

- ANTAPI-SC-ANTH-BEDROCK - https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock - Bedrock guide
- ANTAPI-SC-ANTH-VERTEX - https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai - Vertex AI guide
- ANTAPI-SC-ANTH-FOUNDRY - https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry - Foundry guide

## Document History

**[2026-03-20 04:30]**
- Initial documentation created from platform integration guides
