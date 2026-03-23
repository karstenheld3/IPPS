# Model Context Protocol (MCP)

**Doc ID**: OAIAPI-IN66
**Goal**: Document MCP integration in OpenAI APIs - remote tool servers, Realtime MCP events, configuration
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

Model Context Protocol (MCP) enables OpenAI models to connect to remote tool servers that expose tools, resources, and prompts via a standardized protocol. MCP tools can be used in the Responses API and Realtime API. Configure MCP servers in the tools array with `type: "mcp"` and provide the server URL, transport type (sse or streamable_http), and optional headers/allowed tools. The model discovers available tools from the MCP server, calls them during generation, and incorporates results. In the Realtime API, MCP events track tool listing and execution: `mcp_list_tools.in_progress/completed/failed`, `response.mcp_call_arguments.delta/done`, `response.mcp_call.in_progress/completed/failed`. MCP servers must implement the MCP specification (developed by Anthropic, adopted as open standard). OpenAI acts as the MCP client; external services act as MCP servers. Supports authentication via headers. Tool filtering via `allowed_tools` restricts which server tools the model can use. [VERIFIED] (OAIAPI-SC-OAI-GMCP, OAIAPI-SC-OAI-RTSREV)

## Key Facts

- **Protocol**: Model Context Protocol (open standard) [VERIFIED] (OAIAPI-SC-OAI-GMCP)
- **Tool type**: `mcp` in tools array [VERIFIED] (OAIAPI-SC-OAI-GMCP)
- **Transport**: SSE or streamable_http [VERIFIED] (OAIAPI-SC-OAI-GMCP)
- **APIs**: Supported in Responses API and Realtime API [VERIFIED] (OAIAPI-SC-OAI-GMCP)
- **Discovery**: Model auto-discovers tools from server [VERIFIED] (OAIAPI-SC-OAI-GMCP)
- **Filtering**: `allowed_tools` limits which tools model can use [VERIFIED] (OAIAPI-SC-OAI-GMCP)
- **Auth**: Headers for server authentication [VERIFIED] (OAIAPI-SC-OAI-GMCP)

## Use Cases

- **External tool access**: Connect models to databases, APIs, CRMs via MCP servers
- **Enterprise integration**: Expose internal tools to AI without custom function definitions
- **Standardized tooling**: Use the same MCP server with multiple AI providers
- **Dynamic tool discovery**: Tools can change on the server without updating client config
- **Realtime voice agents**: Voice agents that call external tools via MCP

## Quick Reference

### Responses API

```json
{
  "model": "gpt-5.4",
  "tools": [
    {
      "type": "mcp",
      "server_label": "my_server",
      "server_url": "https://mcp.example.com/sse",
      "transport": "sse",
      "headers": {
        "Authorization": "Bearer token123"
      },
      "allowed_tools": ["search_docs", "create_ticket"]
    }
  ],
  "input": "Search our knowledge base for Python best practices"
}
```

### Realtime API (Session Config)

```json
{
  "type": "session.update",
  "session": {
    "tools": [
      {
        "type": "mcp",
        "server_label": "support_tools",
        "server_url": "https://mcp.example.com/sse",
        "transport": "sse"
      }
    ]
  }
}
```

## MCP Tool Configuration

### Parameters

- **type** (required): `"mcp"`
- **server_label** (required): Identifier for the server (used in events and responses)
- **server_url** (required): URL of the MCP server endpoint
- **transport** (required): `"sse"` or `"streamable_http"`
- **headers** (optional): Authentication and custom headers
- **allowed_tools** (optional): Array of tool names the model can use. If omitted, all tools are available
- **require_approval** (optional): Require user approval before tool execution

### Transport Types

- **sse**: Server-Sent Events transport. Server streams tool results via SSE
- **streamable_http**: HTTP-based transport with streaming support

## Realtime MCP Events

### Tool Discovery

- **mcp_list_tools.in_progress**: Server tool listing started
- **mcp_list_tools.completed**: Tool list received from server
- **mcp_list_tools.failed**: Tool listing failed

### Tool Execution

- **response.mcp_call_arguments.delta**: MCP call arguments streaming
- **response.mcp_call_arguments.done**: MCP call arguments complete
- **response.mcp_call.in_progress**: MCP tool executing on server
- **response.mcp_call.completed**: MCP tool returned result
- **response.mcp_call.failed**: MCP tool execution failed

## SDK Examples (Python)

### Basic MCP Usage

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.4",
    tools=[
        {
            "type": "mcp",
            "server_label": "docs_server",
            "server_url": "https://mcp.mycompany.com/sse",
            "transport": "sse",
            "headers": {
                "Authorization": "Bearer my-token"
            },
            "allowed_tools": ["search_docs", "get_doc_by_id"]
        }
    ],
    input="Find documentation about our authentication system"
)

print(response.output_text)

# Inspect MCP calls made
for item in response.output:
    if item.type == "mcp_call":
        print(f"MCP: {item.server_label}/{item.tool_name}")
        print(f"  Args: {item.arguments}")
        print(f"  Result: {item.result}")
```

### Multiple MCP Servers

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.4",
    tools=[
        {
            "type": "mcp",
            "server_label": "jira",
            "server_url": "https://mcp-jira.example.com/sse",
            "transport": "sse",
            "headers": {"Authorization": "Bearer jira-token"}
        },
        {
            "type": "mcp",
            "server_label": "confluence",
            "server_url": "https://mcp-confluence.example.com/sse",
            "transport": "sse",
            "headers": {"Authorization": "Bearer confluence-token"}
        }
    ],
    input="Create a Jira ticket for the bug described in Confluence page AUTH-123"
)

print(response.output_text)
```

### MCP with Approval Required - Production Ready

```python
from openai import OpenAI

client = OpenAI()

def run_with_approval(user_input: str, mcp_config: list):
    """Run agent with MCP tools requiring approval for write operations"""
    response = client.responses.create(
        model="gpt-5.4",
        tools=mcp_config,
        input=user_input
    )
    
    # Check for pending approvals
    for item in response.output:
        if item.type == "mcp_approval_request":
            print(f"Approval needed: {item.server_label}/{item.tool_name}")
            print(f"  Args: {item.arguments}")
            
            approved = input("Approve? (y/n): ").strip().lower() == "y"
            
            if approved:
                response = client.responses.create(
                    model="gpt-5.4",
                    tools=mcp_config,
                    previous_response_id=response.id,
                    input=[{
                        "type": "mcp_approval_response",
                        "approval_request_id": item.id,
                        "approved": True
                    }]
                )
            else:
                print("Tool call rejected")
                return None
    
    return response.output_text

mcp_tools = [{
    "type": "mcp",
    "server_label": "database",
    "server_url": "https://mcp-db.example.com/sse",
    "transport": "sse",
    "require_approval": True,
    "allowed_tools": ["query_db", "update_record"]
}]

result = run_with_approval("Update the customer's email to new@example.com", mcp_tools)
if result:
    print(result)
```

## Error Responses

- **400 Bad Request** - Invalid MCP server configuration
- **502 Bad Gateway** - MCP server unreachable or returned error
- **504 Gateway Timeout** - MCP server did not respond in time

## Differences from Other APIs

- **vs Anthropic**: Anthropic originated MCP specification. Claude supports MCP natively with similar configuration
- **vs Gemini**: Gemini does not support MCP natively; requires custom function calling wrapper
- **vs Grok**: Grok does not support MCP
- **vs direct function calling**: MCP provides standardized discovery and protocol; function calling requires manual tool definitions

## Limitations and Known Issues

- **Server availability**: MCP server must be reachable from OpenAI infrastructure [VERIFIED] (OAIAPI-SC-OAI-GMCP)
- **Latency**: MCP calls add network round-trip time [VERIFIED] (OAIAPI-SC-OAI-GMCP)
- **Tool count**: Large number of tools from server may increase token usage for tool descriptions [ASSUMED]
- **SSE transport**: Some firewalls may block SSE connections [ASSUMED]

## Gotchas and Quirks

- **server_label uniqueness**: Each MCP server must have a unique label in the tools array [VERIFIED] (OAIAPI-SC-OAI-GMCP)
- **allowed_tools filtering**: Without allowed_tools, model can use ALL tools from server [VERIFIED] (OAIAPI-SC-OAI-GMCP)
- **Headers for auth**: Always use headers for authentication, not URL params [VERIFIED] (OAIAPI-SC-OAI-GMCP)
- **Transport compatibility**: Not all MCP servers support both transports; check server docs [ASSUMED]

## Sources

- OAIAPI-SC-OAI-GMCP - MCP Integration Guide
- OAIAPI-SC-OAI-RTSREV - Realtime Server Events (MCP events)

## Document History

**[2026-03-20 18:38]**
- Initial documentation created
