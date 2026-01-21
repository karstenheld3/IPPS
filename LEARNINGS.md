# Learnings Log

## 2026-01-21 - MCP Server Compatibility

### `MCPS-LN-001` MCP servers must be verified compatible with specific AI clients

- **Source**: `MCPS-FL-008` - computer-use-mcp broke Cascade
- **Problem type**: BUILD / COMPLEXITY-MEDIUM (MCP integration)

**Context at decision time:**
- SETUP.md had pre-installation verification steps
- GitHub repo listed Claude Desktop, Cursor, Cline as compatible
- Windsurf was NOT listed but assumed to work

**Assumptions made:**
- `[CONTRADICTS]` All MCP servers work with all MCP clients
- `[CONTRADICTS]` Testing `npx package --help` validates MCP compatibility
- `[UNVERIFIED]` Windsurf handles any valid MCP tool definition
- `[VERIFIED]` Package installs and runs on Windows

**What happened:**
- Package runs fine: "Computer Use MCP server running on stdio"
- Adding to mcp_config.json caused ALL Cascade requests to fail
- Error: "Invalid argument: an internal error occurred"
- Removing the server restored Cascade functionality

**Dependency tree:**
```
[Root: Assumed MCP protocol compatibility without verification]
├─> [GitHub compatibility list didn't include Windsurf - ignored]
│   └─> [Added untested MCP server to config]
│       └─> [MCP handshake/tool schema failed]
│           └─> [Cascade blocked on broken server]
└─> [Pre-install test (--help) doesn't test MCP protocol]
    └─> [False confidence that package works]
```

**Root cause**: MCP servers are NOT universally compatible. Each client (Windsurf, Claude Desktop, Cursor, Cline) may have different MCP protocol implementations or tool schema requirements.

**Counterfactual**: If we had checked the GitHub compatibility list and seen Windsurf was missing, we would have researched why before adding to config.

**Prevention**:
1. Check MCP server's compatibility list BEFORE attempting integration
2. If target client not listed, assume incompatible until proven otherwise
3. `--help` tests CLI, not MCP protocol - don't use as compatibility proof
4. Always have rollback plan (backup config) before adding MCP servers
5. Test MCP servers in expendable environment first if possible
