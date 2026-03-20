# Tool Infrastructure (Search and Programmatic Tools)

**Doc ID**: ANTAPI-IN26
**Goal**: Document tool search, hidden tools, tool_reference blocks, and programmatic tool patterns
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN21_TOOL_USE.md [ANTAPI-IN21]` for tool use architecture

## Summary

Tool infrastructure features enable scaling to large numbers of tools. Tool search (`tool_search_tool_bm25_20251119`, `tool_search_tool_regex_20251119`) lets Claude dynamically discover tools from a large catalog instead of including all definitions in the system prompt. Hidden tools (`hidden: true`) are excluded from the initial system prompt and only loaded when returned via `tool_reference` blocks from tool search. This reduces token usage for applications with many tools.

## Key Facts

- **Tool Search (BM25)**: `tool_search_tool_bm25_20251119`
- **Tool Search (Regex)**: `tool_search_tool_regex_20251119`
- **Hidden Tools**: `hidden: true` on tool definition
- **Tool Reference**: `tool_reference` content block type
- **Purpose**: Scale to large tool catalogs without token overhead
- **Status**: GA

## Tool Search

```python
import anthropic

client = anthropic.Anthropic()

# Define many tools, most hidden
tools = [
    {
        "type": "tool_search_tool_bm25_20251119",
        "name": "tool_search",
    },
    {
        "name": "get_weather",
        "description": "Get weather for a location",
        "input_schema": {"type": "object", "properties": {"location": {"type": "string"}}, "required": ["location"]},
        "hidden": True,  # Not in system prompt
    },
    {
        "name": "get_stock_price",
        "description": "Get stock price for a ticker",
        "input_schema": {"type": "object", "properties": {"ticker": {"type": "string"}}, "required": ["ticker"]},
        "hidden": True,
    },
    # ... hundreds more hidden tools
]

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
)
# Claude searches for relevant tools, then uses them
```

## Hidden Tools

When `hidden: true` is set on a tool definition:

- Tool is NOT included in the initial system prompt (saves tokens)
- Tool is only loaded when returned via `tool_reference` from tool search
- Reduces context window usage for applications with many tools

## Tool Reference Blocks

`tool_reference` content blocks appear in tool search results, indicating which tools matched the search query. Claude then uses these references to call the appropriate tools.

## Gotchas and Quirks

- Tool search adds a server-side tool that uses the sampling loop
- Hidden tools still count toward the tools array size but not system prompt tokens
- BM25 search is keyword-based; regex search uses pattern matching
- Tool search is most valuable with 50+ tools where including all in system prompt is expensive

## Related Endpoints

- `_INFO_ANTAPI-IN21_TOOL_USE.md [ANTAPI-IN21]` - Tool use architecture
- `_INFO_ANTAPI-IN12_PRICING.md [ANTAPI-IN12]` - Tool use token costs

## Sources

- ANTAPI-SC-GH-SDKAPI - https://github.com/anthropics/anthropic-sdk-python/blob/main/api.md - ToolSearchTool types
- ANTAPI-SC-ANTH-TOOLOVW - https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview - Tool overview

## Document History

**[2026-03-20 03:58]**
- Initial documentation created from SDK types and tool use overview
