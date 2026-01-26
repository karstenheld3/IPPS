# Learnings Log

## 2026-01-26 - UI Automation and Discovery Scripts

### `AMSW-LN-001` Listen first, implement second - user requirements are specific for a reason

**Linked failures**: `AMSW-FL-001` through `AMSW-FL-006`
**Problem type**: BUILD / COMPLEXITY-MEDIUM (UI automation skill)

**Context at decision time:**
- User wanted to discover Windsurf models and costs programmatically
- User specified two-phase approach: fullscreen first, then crop
- User mentioned coordinates change each time

**Assumptions made:**
- `[CONTRADICTS]` Hardcoding model data is acceptable for "discovery"
- `[CONTRADICTS]` Clipboard reading is reliable for UI scraping
- `[CONTRADICTS]` LLM can accurately map scaled images to screen pixels
- `[CONTRADICTS]` Crop coordinates can be stored and reused
- `[UNVERIFIED]` Generic file names are acceptable
- `[VERIFIED]` Keyboard simulation works for model selection

**Actual outcome:**
- 6 failures recorded in one session
- Multiple rewrites of capture scripts
- Final solution: simplified fullscreen capture (opposite of optimization attempt)

**Problem dependency tree:**
```
[Root: Not pausing to fully understand user's specific requirements]
├─> [Ignored "coordinates change each time"]
│   ├─> [Hardcoded coordinates] -> FL-004
│   └─> [Tried cropping optimization] -> FL-003
├─> [Misunderstood "discovery" goal]
│   ├─> [Hardcoded model mapping] -> FL-002
│   └─> [Clipboard anti-pattern] -> FL-001
└─> [Did not consider broader context]
    ├─> [Committed temp files] -> FL-005
    └─> [Generic file names] -> FL-006
```

**Root cause**: Rushing to implement before fully understanding WHY the user specified particular requirements. Each user constraint exists for a reason.

**Counterfactual**: If we had asked "why do coordinates change each time?" we would have understood the window position issue immediately and never attempted to store fixed coordinates.

**Prevention**:
1. When user gives specific instructions, ask "why" if unclear before implementing
2. User constraints are data - they exist because user encountered the problem before
3. Simpler solutions often beat optimized ones (fullscreen > cropping)
4. Consider reusability: will this work in different contexts?
5. Generic names signal incomplete thinking about the file's purpose

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
