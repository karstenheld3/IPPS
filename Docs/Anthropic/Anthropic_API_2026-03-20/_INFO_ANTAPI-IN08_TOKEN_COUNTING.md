# Token Counting

**Doc ID**: ANTAPI-IN08
**Goal**: Document POST /v1/messages/count_tokens endpoint for pre-request token estimation
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` for Messages API request schema

## Summary

The Token Counting API (`POST /v1/messages/count_tokens`) estimates the number of input tokens a Messages API request will consume before actually sending it. This enables cost estimation, context window budgeting, and rate limit management. The request body mirrors the Messages API request, and the response returns the total input token count.

## Key Facts

- **Endpoint**: `POST /v1/messages/count_tokens`
- **Auth**: `x-api-key` header
- **SDK Method**: `client.messages.count_tokens()`
- **Returns**: `MessageTokensCount` with `input_tokens` field
- **Status**: GA

## Request

The request body accepts the same parameters as POST /v1/messages (model, messages, system, tools, etc.) to accurately count tokens including all content types.

**Required Parameters:**

- **model** (`string`) - Model ID to count tokens for
- **messages** (`array[MessageParam]`) - Input messages to count

**Optional Parameters (affect token count):**

- **system** (`string | array`) - System prompt tokens
- **tools** (`array[ToolUnion]`) - Tool definition tokens
- **thinking** (`ThinkingConfigParam`) - Thinking configuration

## Response

```json
{
  "input_tokens": 2095
}
```

**Response Fields:**

- **input_tokens** (`integer`) - Total input tokens the request would consume

## Python Examples

### Basic Token Count

```python
import anthropic

client = anthropic.Anthropic()

result = client.messages.count_tokens(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "What is the meaning of life?"}],
)
print(f"Input tokens: {result.input_tokens}")
```

### With System Prompt and Tools

```python
import anthropic

client = anthropic.Anthropic()

result = client.messages.count_tokens(
    model="claude-sonnet-4-20250514",
    system="You are a helpful weather assistant.",
    tools=[
        {
            "name": "get_weather",
            "description": "Get weather for a location.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"],
            },
        }
    ],
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
)
print(f"Input tokens (with tools): {result.input_tokens}")
```

### Cost Estimation Before Sending

```python
import anthropic

client = anthropic.Anthropic()

# Pricing per million tokens (example rates)
INPUT_COST_PER_MTOK = 3.00  # $3 per million input tokens for Sonnet

messages = [{"role": "user", "content": "Write a comprehensive analysis..."}]

# Count tokens first
count = client.messages.count_tokens(
    model="claude-sonnet-4-20250514",
    messages=messages,
)

estimated_cost = (count.input_tokens / 1_000_000) * INPUT_COST_PER_MTOK
print(f"Estimated input cost: ${estimated_cost:.4f}")

# Proceed if within budget
if estimated_cost < 0.10:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=messages,
    )
```

## Use Cases

- **Cost estimation** - Calculate expected cost before sending expensive requests
- **Context window budgeting** - Verify messages fit within model context window
- **Rate limit management** - Check token count against TPM limits before sending
- **Dynamic content trimming** - Iteratively remove content until request fits budget

## Gotchas and Quirks

- Token counts include system prompt, tool definitions, and all message content
- The count is for input tokens only; output tokens depend on model generation
- Tool definitions can consume significant tokens; count them to avoid surprises
- The endpoint uses the same auth and version headers as POST /v1/messages

## Related Endpoints

- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` - Messages API (same request structure)
- `_INFO_ANTAPI-IN12_PRICING.md [ANTAPI-IN12]` - Token pricing per model
- `_INFO_ANTAPI-IN19_CONTEXT_MANAGEMENT.md [ANTAPI-IN19]` - Context window management

## Sources

- ANTAPI-SC-ANTH-MSGCNT - https://platform.claude.com/docs/en/api/messages/count_tokens - Endpoint reference
- ANTAPI-SC-ANTH-TOKCNT - https://platform.claude.com/docs/en/build-with-claude/token-counting - Token counting guide

## Document History

**[2026-03-20 02:38]**
- Initial documentation created
