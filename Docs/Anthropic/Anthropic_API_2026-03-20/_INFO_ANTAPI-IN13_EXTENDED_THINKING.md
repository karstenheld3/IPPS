# Extended Thinking

**Doc ID**: ANTAPI-IN13
**Goal**: Document extended thinking configuration, thinking blocks, adaptive thinking, and effort control
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` for Messages API request/response schema

## Summary

Extended thinking enables Claude to show its internal reasoning process before generating a final response. When enabled via the `thinking` parameter, responses include `thinking` content blocks with Claude's step-by-step analysis, followed by `text` blocks with the final answer. Two modes exist: manual (`type: "enabled"` with `budget_tokens`) and adaptive (`type: "adaptive"` with effort levels). Claude Opus 4.6 uses adaptive thinking only; earlier models support both. Thinking tokens count toward `max_tokens` and are billed as output tokens.

## Key Facts

- **Parameter**: `thinking` object in request body
- **Manual Mode**: `{"type": "enabled", "budget_tokens": N}` (deprecated on Opus 4.6)
- **Adaptive Mode**: `{"type": "adaptive"}` with effort parameter
- **Response Blocks**: `thinking` (reasoning) + `text` (final answer)
- **Thinking Signature**: Each thinking block includes a `signature` for integrity verification
- **Max Output**: Opus 4.6 supports 128K output tokens; earlier models 64K
- **Budget Constraint**: `budget_tokens` must be less than `max_tokens`
- **Status**: GA

## Supported Models

- **claude-opus-4-6** - Adaptive thinking only; manual mode deprecated
- **claude-sonnet-4-6** - Both manual and adaptive thinking, plus interleaved mode
- **claude-opus-4-5-20251101** - Manual and adaptive
- **claude-opus-4-1-20250805** - Manual and adaptive
- **claude-opus-4-20250514** - Manual and adaptive
- **claude-sonnet-4-5-20250929** - Manual and adaptive
- **claude-sonnet-4-20250514** - Manual and adaptive
- **claude-haiku-4-5-20251001** - Manual and adaptive

## Configuration

### Manual Mode (type: "enabled")

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000,
    },
    messages=[
        {"role": "user", "content": "Prove there are infinitely many primes p where p mod 4 = 3"}
    ],
)

for block in message.content:
    if block.type == "thinking":
        print(f"Thinking: {block.thinking[:200]}...")
    elif block.type == "text":
        print(f"Answer: {block.text}")
```

### Adaptive Mode (type: "adaptive")

```python
import anthropic

client = anthropic.Anthropic()

# Adaptive thinking with effort control
message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    messages=[
        {"role": "user", "content": "What is 2 + 2?"}
    ],
)
```

### Controlling Effort Level

```python
# Low effort for simple tasks
message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    thinking={"type": "adaptive"},
    output_config={"effort": "low"},
    messages=[{"role": "user", "content": "Classify this sentiment: Great product!"}],
)

# High effort for complex reasoning
message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=32000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    messages=[{"role": "user", "content": "Design an optimal database schema for..."}],
)
```

## Response Format

```json
{
  "content": [
    {
      "type": "thinking",
      "thinking": "Let me analyze this step by step...",
      "signature": "WaUjzkypQ2mUEVM36O2TxuC06KN8xyfbJwyem2dw3URve..."
    },
    {
      "type": "text",
      "text": "Based on my analysis..."
    }
  ]
}
```

### Response Content Blocks

- **thinking** - Claude's internal reasoning (may be summarized in Claude 4+ models)
  - `thinking` (`string`) - Reasoning text
  - `signature` (`string`) - Integrity verification signature
- **redacted_thinking** - Thinking that was redacted for safety reasons
  - `data` (`string`) - Encrypted data
- **text** - Final response text

## Controlling Thinking Display

- **Default**: Full thinking content returned
- **`display: "omitted"`**: Thinking blocks open and close with only a signature; no thinking text streamed. Useful for production where thinking is not displayed to users but you want the quality benefit

## Extended Thinking with Tool Use

When using tools with extended thinking, Claude can think before each tool call and after receiving results. In interleaved thinking mode (Sonnet 4.6), thinking blocks appear between tool use and tool result blocks.

### Preserving Thinking Blocks

In multi-turn conversations with thinking enabled, pass thinking and redacted_thinking blocks back in assistant messages to maintain context:

```python
# First turn
response1 = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[{"role": "user", "content": "Analyze this data..."}],
)

# Second turn - include thinking blocks from first response
messages = [
    {"role": "user", "content": "Analyze this data..."},
    {"role": "assistant", "content": response1.content},  # includes thinking blocks
    {"role": "user", "content": "Now compare with this..."},
]

response2 = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=messages,
)
```

## Streaming with Thinking

Thinking content streams via `thinking_delta` events, followed by `signature_delta` before `content_block_stop`:

```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[{"role": "user", "content": "Solve this complex problem..."}],
) as stream:
    for event in stream:
        if hasattr(event, "type"):
            if event.type == "content_block_start":
                if event.content_block.type == "thinking":
                    print("[THINKING]")
                elif event.content_block.type == "text":
                    print("\n[ANSWER]")
            elif event.type == "content_block_delta":
                if event.delta.type == "thinking_delta":
                    print(event.delta.thinking, end="")
                elif event.delta.type == "text_delta":
                    print(event.delta.text, end="")
```

## Token Management

- `budget_tokens` sets the max thinking tokens (must be < `max_tokens`)
- `max_tokens` covers both thinking and response tokens
- Claude may not use the entire budget, especially above 32K
- With interleaved thinking + tools, the token limit becomes the entire context window
- Thinking tokens are billed as output tokens

## Pricing

Thinking tokens are billed at the same rate as output tokens for the model used.

## Feature Compatibility Restrictions

- **Not compatible with**: `temperature` modifications, `top_k` modifications, forced tool use (`tool_choice: {type: "tool", name: "..."}`))
- **top_p**: Limited to values between 0.95 and 1.0 when thinking is enabled
- **No pre-fill**: Cannot use assistant pre-fill when thinking is enabled
- **Caching**: Changes to thinking budget invalidate cached prompt prefixes that include messages (cached system prompts and tool definitions still work)

## Performance Constraints

- **Minimum budget**: 1,024 tokens
- **Streaming required**: SDKs require streaming when `max_tokens` > 21,333 to avoid HTTP timeouts (client-side validation, not API restriction). Use `.stream()` with `.get_final_message()` for non-incremental processing
- **Large budgets (>32K)**: Use batch processing to avoid networking issues; long-running requests can hit system timeouts and open connection limits
- **max_tokens strictly enforced**: On Claude 3.7+ and 4 models, `prompt_tokens + max_tokens` must not exceed context window (returns validation error, no longer silently adjusted)
- **Latency**: Set `display: "omitted"` on thinking config to reduce time-to-first-text-token when your app does not display thinking content

## Gotchas and Quirks

- On Opus 4.6, `type: "enabled"` with `budget_tokens` is deprecated; use `type: "adaptive"` instead
- Thinking blocks include a `signature` field for integrity verification; do not modify thinking content
- `redacted_thinking` blocks appear when safety classifiers flag reasoning content
- In Claude 4+ models, `budget_tokens` applies to full thinking, not summarized output
- Summarized thinking: Claude 4+ models internally produce full reasoning but may return a summarized version
- Cannot disable thinking mid-conversation if it was enabled in earlier turns (Opus 4.5+)
- Thinking blocks from earlier turns should be passed back in multi-turn conversations
- Previous thinking blocks are automatically ignored and not counted toward context usage
- Thinking budget is a target, not a strict limit; actual usage may vary

## Related Endpoints

- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` - Messages API (thinking parameter)
- `_INFO_ANTAPI-IN07_STREAMING.md [ANTAPI-IN07]` - Streaming thinking deltas
- `_INFO_ANTAPI-IN21_TOOL_USE.md [ANTAPI-IN21]` - Thinking with tool use

## Sources

- ANTAPI-SC-ANTH-THINK - https://platform.claude.com/docs/en/build-with-claude/extended-thinking - Full thinking guide
- ANTAPI-SC-ANTH-ADAPT - https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking - Adaptive thinking
- ANTAPI-SC-ANTH-EFFORT - https://platform.claude.com/docs/en/build-with-claude/effort - Effort control

## Document History

**[2026-03-20 05:00]**
- Added: Feature compatibility restrictions (no temperature, top_k, forced tool use, pre-fill)
- Added: Performance constraints (min 1,024 budget, streaming >21,333, batch >32K, strict max_tokens)
- Added: display "omitted" option, caching invalidation behavior

**[2026-03-20 03:10]**
- Initial documentation created from extended thinking guide
