# INFO: OpenAI API - New Tools (Shell, Computer Use, MCP, Skills)

**Doc ID**: OAIAPI-IN65
**Goal**: Document new tool types added to the OpenAI API: Shell, Computer Use, MCP/Connectors, Skills, Tool Search
**Version scope**: API v1, Documentation date 2026-03-12

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The OpenAI API now supports several new tool types beyond function calling and hosted tools. Shell enables command execution in sandboxed environments. Computer Use allows GUI interaction via screenshots and mouse/keyboard control. MCP (Model Context Protocol) and Connectors provide standardized integration with external services. Skills are reusable tool packages. Tool Search enables dynamic tool discovery from large tool registries.

## Key Facts

- **Shell**: Execute commands in sandboxed environment [VERIFIED]
- **Computer Use**: GUI automation via screenshots [VERIFIED]
- **MCP/Connectors**: Standardized external integrations [VERIFIED]
- **Skills**: Reusable tool packages [VERIFIED]
- **Tool Search**: Dynamic tool discovery [VERIFIED]

## Tool Types Overview

### Shell Tool

Execute shell commands in a sandboxed environment.

**Use cases**:
- Code execution
- File operations
- System queries

**Documentation**: https://developers.openai.com/api/docs/guides/tools-shell

### Computer Use Tool

Control a computer interface via screenshots and input simulation.

**Use cases**:
- GUI automation
- Web browsing
- Application control

**Documentation**: https://developers.openai.com/api/docs/guides/tools-computer-use

### MCP and Connectors

Model Context Protocol provides standardized integration with external services and data sources.

**Use cases**:
- Database connections
- API integrations
- File system access
- Third-party service connections

**Documentation**: https://developers.openai.com/api/docs/guides/tools-connectors-mcp

### Skills

Reusable tool packages that bundle related functionality.

**Use cases**:
- Pre-built capability sets
- Domain-specific toolkits
- Shared tool configurations

**Documentation**: https://developers.openai.com/api/docs/guides/tools-skills

### Tool Search

Dynamic discovery of tools from large registries.

**Use cases**:
- Large tool collections
- Dynamic tool selection
- Context-aware tool matching

**Documentation**: https://developers.openai.com/api/docs/guides/tools-tool-search

## Quick Reference

### Available Tool Types

From the API sidebar navigation:

- Using tools (overview)
- Web search (hosted)
- MCP and Connectors
- Skills
- Shell
- Computer use
- File search and retrieval
- Tool search

### Tool Configuration Pattern

```json
{
  "model": "gpt-5.4",
  "input": "...",
  "tools": [
    {
      "type": "shell",
      "config": {}
    },
    {
      "type": "computer_use",
      "config": {}
    },
    {
      "type": "mcp",
      "server": "..."
    }
  ]
}
```

## Gotchas and Quirks

- Shell execution is sandboxed with limited permissions
- Computer Use requires appropriate display/capture setup
- MCP servers must be configured with proper authentication
- Tool Search works best with well-described tools

## Related Endpoints

- `_INFO_OAIAPI_GPT54.md` - GPT-5.4 model (best for tool use)
- `_INFO_OAIAPI_RESPONSES.md` - Responses API tool configuration

## Sources

- `OAIAPI-IN01-SC-DEV-GPT54` - https://developers.openai.com/api/docs/guides/latest-model (sidebar navigation) [2026-03-12]

## Document History

**[2026-03-12 21:18]**
- Initial documentation created from new Tools section in API docs
