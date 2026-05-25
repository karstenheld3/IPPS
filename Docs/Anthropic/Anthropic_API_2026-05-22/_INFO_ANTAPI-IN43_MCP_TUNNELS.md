# MCP Tunnels

**Doc ID**: ANTAPI-IN43
**Goal**: Document MCP tunnels for connecting Claude to private MCP servers
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN38_MANAGED_AGENTS.md [ANTAPI-IN38]` for Managed Agents context
- `_INFO_ANTAPI-IN03_VERSIONING.md [ANTAPI-IN03]` for beta header usage

## Summary

MCP tunnels (research preview) allow Claude Managed Agents to connect to MCP (Model Context Protocol) servers running on private networks. This enables agents to access internal tools, databases, and services that are not publicly accessible. Tunnels create a secure connection between the managed agent's cloud container and your private infrastructure. Requires the `mcp-tunnels-2026-05-01` beta header and separate research preview access.

## Key Facts

- **Beta Header**: `mcp-tunnels-2026-05-01`
- **Access**: Research preview (requires separate access request)
- **Purpose**: Connect managed agents to private MCP servers
- **Security**: Secure tunnel between cloud container and private network
- **Prerequisite**: Claude Managed Agents
- **Status**: Research Preview (launched May 19, 2026)

## Use Cases

- Connect agents to internal databases via MCP
- Access private APIs and tools from managed agent sessions
- Enterprise workflows requiring access to on-premise systems
- Compliance scenarios where tools must run inside private networks

## Limitations

- Research preview; may change significantly
- Requires separate access request via form
- Only available with Claude Managed Agents
- Not eligible for ZDR or HIPAA BAA (same as Managed Agents)

## Gotchas and Quirks

- MCP tunnels require both the MCP tunnels beta header and Managed Agents beta header
- Tunnel setup adds latency to initial connection
- Private MCP servers must implement the standard MCP protocol

## Related Endpoints

- `_INFO_ANTAPI-IN38_MANAGED_AGENTS.md [ANTAPI-IN38]` - Managed Agents (required for tunnels)
- `_INFO_ANTAPI-IN03_VERSIONING.md [ANTAPI-IN03]` - Beta header configuration

## Sources

- ANTAPI-SC-ANTH-MCPTNL - https://platform.claude.com/docs/en/managed-agents/mcp-tunnels - MCP tunnels documentation
- ANTAPI-SC-ANTH-RLNTS - https://platform.claude.com/docs/en/about-claude/release-notes - Release notes (May 19, 2026)

## Document History

**[2026-05-22]**
- Initial documentation created from release notes and MCP tunnels references
