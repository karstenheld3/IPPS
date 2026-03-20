# Tool Use Overview

**Doc ID**: ANTAPI-IN21
**Goal**: Document tool use architecture, client vs server tools, tool_choice, and agentic patterns
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` for Messages API tool parameters

## Summary

Claude supports two categories of tools: client tools (executed on your systems) and server tools (executed on Anthropic's servers). Client tools include user-defined custom tools and Anthropic-defined tools like computer use and text editor. Server tools include web search, web fetch, code execution, and memory. Tools are defined in the `tools` parameter with JSON Schema input definitions. Claude returns `tool_use` content blocks when it wants to call a tool; you execute and return results via `tool_result` blocks. The `tool_choice` parameter controls how Claude selects tools.

## Key Facts

- **Tool Types**: Client tools (user-defined, Anthropic-defined) and server tools
- **Definition**: `tools` array with name, description, input_schema
- **Schema Format**: JSON Schema (draft 2020-12)
- **Tool Choice**: `auto` (default), `any`, `none`, `{"type": "tool", "name": "..."}`
- **Stop Reason**: `tool_use` for client tools, `pause_turn` for server tool iteration limit
- **Server Loop**: Up to 10 iterations before `pause_turn`
- **Versioned Types**: Server tools use `tool_type_YYYYMMDD` format
- **Status**: GA

## Client Tools

### Defining Custom Tools

```python
import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and state, e.g. San Francisco, CA",
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit",
                },
            },
            "required": ["location"],
        },
    }
]

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
)
```

### Agentic Tool Loop

```python
import anthropic
import json

client = anthropic.Anthropic()

def run_tool(name, input_data):
    """Execute tool and return result."""
    if name == "get_weather":
        return json.dumps({"temp": "22C", "condition": "sunny", "location": input_data["location"]})
    return json.dumps({"error": f"Unknown tool: {name}"})

tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location.",
        "input_schema": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"],
        },
    }
]

messages = [{"role": "user", "content": "Compare weather in NYC and London"}]

while True:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )

    if response.stop_reason == "end_turn":
        for block in response.content:
            if hasattr(block, "text"):
                print(block.text)
        break

    if response.stop_reason == "tool_use":
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = run_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })
        messages.append({"role": "user", "content": tool_results})
```

## Tool Choice

Controls how Claude selects tools:

```python
# Auto (default) - Claude decides whether to use tools
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "auto"},
    messages=[{"role": "user", "content": "Hello"}],
)

# Any - Claude must use at least one tool
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "any"},
    messages=[{"role": "user", "content": "Get weather"}],
)

# None - Claude cannot use tools
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "none"},
    messages=[{"role": "user", "content": "Hello"}],
)

# Specific tool - Force a particular tool
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "tool", "name": "get_weather"},
    messages=[{"role": "user", "content": "Paris weather"}],
)
```

## Server Tools

Server tools execute on Anthropic's servers. Include in `tools` array with versioned type:

```python
# Web search (server tool)
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[{"type": "web_search_20250305", "name": "web_search"}],
    messages=[{"role": "user", "content": "What's the latest AI news?"}],
)

# Handle pause_turn for server tools
if message.stop_reason == "pause_turn":
    messages = [
        {"role": "user", "content": "What's the latest AI news?"},
        {"role": "assistant", "content": message.content},
    ]
    continuation = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=messages,
    )
```

## Available Server Tools

- **web_search** (`web_search_20250305`) - Real-time web search
- **web_fetch** (`web_fetch_tool_20250910`) - Fetch and process web pages
- **code_execution** (`code_execution_tool_20250522`) - Sandboxed code execution
- **bash** (`bash_20250124`) - Bash shell commands (computer use)
- **text_editor** (`text_editor_20250124`) - File viewing/editing (computer use)
- **memory** (`memory_tool_20250818`) - Persistent memory across conversations
- **tool_search** (`tool_search_tool_bm25_20251119`) - Dynamic tool discovery

## Tool Definition Options

- **name** (`string`, required) - Tool identifier
- **description** (`string`, recommended) - Detailed description for the model
- **input_schema** (`object`, required) - JSON Schema for input
- **cache_control** (`CacheControlEphemeral`, optional) - Prompt caching
- **hidden** (`boolean`, optional) - Not in system prompt; loaded via tool_reference
- **eager_streaming** (`boolean`, optional) - Incremental input streaming
- **strict** (`boolean`, optional) - Guarantee schema validation on inputs

## Gotchas and Quirks

- Tool definitions add hidden system prompt tokens (varies by model and tool_choice)
- Server tools use a sampling loop (up to 10 iterations) before returning `pause_turn`
- Client tools require you to execute and return results; server tools auto-execute
- `tool_use` content blocks include an `id` (format: `toolu_...`) that must match `tool_use_id` in results
- Do not add text blocks alongside `tool_result` blocks in the same user message
- Anthropic-defined tools use versioned type strings for compatibility
- MCP tools can be converted to Claude's tool format

## Related Endpoints

- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` - Messages API (tools parameter)
- `_INFO_ANTAPI-IN22_WEB_TOOLS.md [ANTAPI-IN22]` - Web search and fetch tools
- `_INFO_ANTAPI-IN23_CODE_EXECUTION.md [ANTAPI-IN23]` - Code execution tool
- `_INFO_ANTAPI-IN24_COMPUTER_USE.md [ANTAPI-IN24]` - Computer use tools
- `_INFO_ANTAPI-IN14_STRUCTURED_OUTPUTS.md [ANTAPI-IN14]` - Strict tool schemas

## Sources

- ANTAPI-SC-ANTH-TOOLOVW - https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview - Tool use overview
- ANTAPI-SC-ANTH-TOOLIMPL - https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use - Implementation guide

## Document History

**[2026-03-20 03:40]**
- Initial documentation created from tool use overview and implementation guides
