# Tools Overview

**Doc ID**: OAIAPI-IN12
**Goal**: Document tool types, built-in tools vs function calling, tool_choice parameter
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN06_RESPONSES_API.md [OAIAPI-IN06]` for Responses API context

## Summary

OpenAI API supports two categories of tools: built-in tools provided by OpenAI (file_search, web_search, code_interpreter, tool_search, computer_use) and custom function calling where developers define functions for the model to invoke. Tools extend model capabilities beyond text generation, enabling RAG with vector stores, real-time web access, Python code execution, skill discovery, and computer interface interaction. The tool_choice parameter controls tool usage: "auto" (model decides), "required" (must use tools), "none" (no tools), or specific tool selection. Models can execute parallel tool calls in single response. Tools specified in Responses API tools array with type field. Built-in tools have preset configurations, functions require schema definition. Tool results must be provided back to model for response continuation. [VERIFIED] (OAIAPI-SC-OAI-GTOOLS, OAIAPI-SC-OAI-GFNCAL)

## Key Facts

- **Built-in tools**: file_search, web_search, code_interpreter, tool_search, computer_use [VERIFIED] (OAIAPI-SC-OAI-GTOOLS)
- **Function calling**: Custom developer-defined functions [VERIFIED] (OAIAPI-SC-OAI-GFNCAL)
- **tool_choice**: Controls when/which tools used (auto, required, none, specific) [VERIFIED] (OAIAPI-SC-OAI-GTOOLS)
- **Parallel calls**: Model can invoke multiple tools simultaneously [VERIFIED] (OAIAPI-SC-OAI-GFNCAL)
- **Tool loop**: Call tool → Execute → Return result → Model continues [VERIFIED] (OAIAPI-SC-OAI-GTOOLS)

## Use Cases

- **RAG applications**: file_search for document retrieval
- **Web-enabled chat**: web_search for current information
- **Code execution**: code_interpreter for data analysis
- **External APIs**: Function calling for databases, services
- **Skill discovery**: tool_search for finding available skills

## Quick Reference

```python
# Built-in tool
tools=[
    {"type": "web_search"}
]

# Custom function
tools=[
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather",
            "parameters": {...}
        }
    }
]

# Tool choice
tool_choice="auto"  # or "required", "none", {"type": "function", "function": {"name": "..."}}
```

## Tool Types

### Built-in Tools

#### file_search
- **Purpose**: Search uploaded files in vector stores
- **Use case**: RAG, document Q&A
- **Configuration**: vector_store_ids, max_num_results
- **Returns**: Relevant document chunks with citations

#### web_search
- **Purpose**: Real-time web search
- **Use case**: Current events, latest information
- **Configuration**: max_results, search parameters
- **Returns**: Web search results and summaries

#### code_interpreter
- **Purpose**: Execute Python code in sandboxed environment
- **Use case**: Data analysis, calculations, chart generation
- **Configuration**: Automatic
- **Returns**: Code execution results, generated files

#### tool_search
- **Purpose**: Discover and use skills from Skills API
- **Use case**: Dynamic tool discovery, skill utilization
- **Configuration**: Automatic
- **Returns**: Skill invocation results

#### computer_use
- **Purpose**: Interact with computer interfaces
- **Use case**: UI automation, testing, screenshots
- **Configuration**: Requires computer-use-preview model
- **Returns**: Screenshot, UI state, interaction results

### Function Calling

Developer-defined functions:
- Define function schema (name, description, parameters)
- Model decides when to call
- Execute function in your code
- Return results to model
- Model uses results in response

## tool_choice Parameter

### Options

**auto** (default)
- Model decides whether to use tools
- Most flexible option
- May or may not call tools

**required**
- Model must use at least one tool
- Forces tool usage
- Useful when tool call expected

**none**
- Disable all tools
- Model generates text-only response
- Override tools array

**Specific tool**
- Force specific tool usage
- Example: `{"type": "function", "function": {"name": "get_weather"}}`
- Model must call that tool

## Parallel Tool Calls

Model can invoke multiple tools simultaneously:

```python
# Model might call:
# 1. get_weather("Paris")
# 2. get_weather("London")
# 3. get_weather("Tokyo")
# All in single response
```

Process all tool calls and return results together.

## Tool Execution Flow

1. **Model decides**: Based on input, decides which tools to call
2. **Tool call returned**: Response includes tool_calls array
3. **Execute tools**: Developer executes requested functions
4. **Return results**: Submit tool results back to API
5. **Model continues**: Uses tool results to generate final response

## SDK Examples (Python)

### Using Built-in Tools

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "user", "content": "Search the web for latest AI news"}
    ],
    tools=[
        {"type": "web_search"}
    ]
)

print(response.output[0].content[0].text)
```

### Combining Multiple Built-in Tools

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "user", "content": "Search my documents and the web for quantum computing"}
    ],
    tools=[
        {
            "type": "file_search",
            "file_search": {
                "vector_store_ids": ["vs_abc123"]
            }
        },
        {"type": "web_search"}
    ]
)

print(response.output[0].content[0].text)
```

### Function Calling with tool_choice

```python
from openai import OpenAI

client = OpenAI()

# Define function
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get current time for timezone",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {"type": "string"}
                },
                "required": ["timezone"]
            }
        }
    }
]

# Force function call
response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "user", "content": "What time is it in Tokyo?"}
    ],
    tools=tools,
    tool_choice="required"  # Must call a tool
)

print(response.output[0].content)
```

### Handling Parallel Tool Calls

```python
from openai import OpenAI
import json

client = OpenAI()

def execute_function(name: str, arguments: str):
    """Execute function based on name"""
    args = json.loads(arguments)
    
    if name == "get_weather":
        # Simulate weather API call
        return f"Weather in {args['location']}: Sunny, 22°C"
    
    return "Unknown function"

# Initial request
response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "user", "content": "What's the weather in Paris, London, and Tokyo?"}
    ],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather for location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"}
                    },
                    "required": ["location"]
                }
            }
        }
    ]
)

# Check for tool calls
tool_calls = response.output[0].tool_calls if hasattr(response.output[0], 'tool_calls') else []

if tool_calls:
    # Execute all tool calls
    tool_results = []
    for call in tool_calls:
        result = execute_function(call.function.name, call.function.arguments)
        tool_results.append({
            "tool_call_id": call.id,
            "output": result
        })
    
    # Submit results and get final response
    final_response = client.responses.create(
        model="gpt-5.4",
        input=[
            {"role": "tool", "tool_call_id": tr["tool_call_id"], "content": tr["output"]}
            for tr in tool_results
        ]
    )
    
    print(final_response.output[0].content[0].text)
```

### Tool Choice Selection

```python
from openai import OpenAI

client = OpenAI()

tools = [
    {"type": "web_search"},
    {
        "type": "function",
        "function": {
            "name": "query_database",
            "description": "Query internal database",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                }
            }
        }
    }
]

# Force specific tool
response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "user", "content": "Find information about user 12345"}
    ],
    tools=tools,
    tool_choice={
        "type": "function",
        "function": {"name": "query_database"}
    }
)
```

## Error Responses

- **400 Bad Request** - Invalid tool definition or tool_choice
- **404 Not Found** - Referenced vector store or skill not found
- **429 Too Many Requests** - Tool usage counts toward rate limits

## Rate Limiting / Throttling

- **Tool calls count**: Each tool invocation counts toward token limits
- **Parallel calls**: Multiple parallel calls count separately
- **Built-in tool quotas**: Some tools have usage limits

## Differences from Other APIs

- **vs Anthropic Tools**: Similar concept, different tool types (no built-in web_search in Anthropic)
- **vs Gemini Tools**: Gemini has function calling, no equivalent to code_interpreter
- **vs Function Calling (legacy)**: tools array replaces functions array

## Limitations and Known Issues

- **Max tools per request**: Limited number of tools in single request [COMMUNITY] (OAIAPI-SC-SO-TOOLMAX)
- **Tool timeout**: Long-running tools may timeout [COMMUNITY] (OAIAPI-SC-SO-TOOLTIMEOUT)
- **computer_use preview**: Only works with specific model [VERIFIED] (OAIAPI-SC-OAI-GCMPTU)

## Gotchas and Quirks

- **tool_choice=required doesn't guarantee tool**: Model still needs valid reason to call tool [COMMUNITY] (OAIAPI-SC-SO-TOOLREQ)
- **Parallel calls optional**: Model decides whether to parallelize [VERIFIED] (OAIAPI-SC-OAI-GFNCAL)
- **Tool result format**: Must match expected structure or model fails [COMMUNITY] (OAIAPI-SC-SO-TOOLFMT)

## Sources

- OAIAPI-SC-OAI-GTOOLS - Using tools guide
- OAIAPI-SC-OAI-GFNCAL - Function calling guide
- OAIAPI-SC-OAI-RESCRT - POST Create a response

## Document History

**[2026-03-20 15:25]**
- Initial documentation created
