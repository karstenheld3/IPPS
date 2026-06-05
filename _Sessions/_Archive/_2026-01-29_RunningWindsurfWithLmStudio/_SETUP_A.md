# SETUP: Agent-Cascade + LM Studio Integration

**Doc ID**: LMWS-IP01
**Goal**: Step-by-step plan to integrate local LLMs with Windsurf via Agent-Cascade MCP server
**Timeline**: Created 2026-01-29
**Approach**: A - MCP Bridge (Cascade calls local model via tool)

## Prerequisites

- Windows 10/11
- Node.js 20+ installed
- 16GB+ RAM recommended
- GPU with 4GB+ VRAM (optional but recommended)

**WARNING**: Agent-Cascade is a third-party MCP server. If Cascade breaks after configuration, remove `agent-cascade` entry from mcp_config.json and restart Windsurf.

## Phase 1: Install LM Studio

### Step 1.1: Download LM Studio

1. Open browser: https://lmstudio.ai/download
2. Select "Windows" platform
3. Download the `.exe` installer
4. Save to `E:\Dev\IPPS\.tools\_installer\`

### Step 1.2: Install and Configure

```powershell
# Run installer (manual step)
# After installation, launch LM Studio
```

1. Launch LM Studio
2. Go to **Search** tab
3. Search for `qwen2.5-coder-7b-instruct gguf`
4. Download Q4_K_M quantization (~5GB)

### Step 1.3: Start API Server

1. Go to **Developer** tab (left sidebar)
2. Verify GPU acceleration is enabled (check "GPU Offload" setting)
3. Select downloaded model from dropdown
4. Toggle **Start server** switch ON
5. Note the port number (default: 1234, configurable)
6. Verify: `http://localhost:1234/v1` is accessible

**Verification - Get Model Name:**
```powershell
# This returns the exact model name to use in MCP config
curl http://localhost:1234/v1/models
```

**IMPORTANT**: Note the `id` field in the response - this is the exact model name to use in Step 3.1. It may differ from the display name in LM Studio UI.

## Phase 2: Build Agent-Cascade

### Step 2.1: Extract Source

```powershell
cd E:\Dev\IPPS\.tools\_installer
Expand-Archive -Path "Agent-Cascade-main.zip" -DestinationPath "." -Force
```

### Step 2.2: Install Dependencies

```powershell
cd Agent-Cascade-main\tools\agent-cascade
npm install
```

### Step 2.3: Build

```powershell
npm run build
```

**Verification:**
```powershell
Test-Path "dist\server.js"
# Should return: True
```

## Phase 3: Configure Windsurf MCP

### Step 3.1: Edit MCP Config

**Find config file** (use Windsurf Settings > Cascade > MCP Servers > "View Raw Config"):
- Path: `%USERPROFILE%\.codeium\windsurf\mcp_config.json`

Add or merge the following (replace `DEFAULT_MODEL` with actual model name from Step 1.3):

```json
{
  "mcpServers": {
    "agent-cascade": {
      "command": "node",
      "args": ["E:/Dev/IPPS/.tools/_installer/Agent-Cascade-main/tools/agent-cascade/dist/server.js"],
      "env": {
        "LM_BASE_URL": "http://localhost:1234/v1",
        "DEFAULT_MODEL": "<MODEL_NAME_FROM_STEP_1.3>"
      },
      "disabled": false,
      "disabledTools": []
    }
  }
}
```

**Note**: Path must use forward slashes. Update path if installation location differs.

### Step 3.2: Reload Windsurf

1. Open Cascade panel
2. Go to **Plugins** > **Manage**
3. Click **Refresh** button
4. Verify "agent-cascade" appears in list
5. **If not visible**: Restart Windsurf completely and check again

## Phase 4: Test Integration

### Step 4.1: Basic Test

In Cascade, type:
```
Use the local_chat tool to say hello
```

**Expected**: Response from local model via `local_chat` tool

### Step 4.2: Code Review Test

In Cascade, type:
```
Use the local_chat tool to review this code for security issues:

function login(user, pass) {
  return db.query(`SELECT * FROM users WHERE user='${user}' AND pass='${pass}'`);
}
```

**Expected**: Local model identifies SQL injection vulnerability

## Troubleshooting

### LM Studio Server Not Responding

1. Verify server is running (green indicator in Developer tab)
2. Check port 1234 is not blocked
3. Try: `curl http://localhost:1234/v1/models`

### Agent-Cascade Build Fails

1. Verify Node.js 20+: `node --version`
2. Clear npm cache: `npm cache clean --force`
3. Delete node_modules and reinstall: `rm -rf node_modules && npm install`

### MCP Server Not Appearing in Cascade

1. Check mcp_config.json syntax (valid JSON)
2. Verify path to `dist/server.js` is correct (use forward slashes)
3. Restart Windsurf completely

### Timeouts on Local Chat

1. Increase `timeout_ms` in tool call
2. Use smaller model or higher quantization
3. Reduce `max_tokens` parameter

## Limitations

- Cascade cloud model remains the orchestrator
- Cannot force Cascade to use local model exclusively
- Local model only accessible via explicit `local_chat` tool call
- All context still goes through Codeium cloud

## Next Steps After Setup

1. Test various prompts with local model
2. Evaluate response quality vs cloud models
3. Consider LM-Studio-IDE-Plugin for inline completions (separate setup)

## Document History

**[2026-01-29 10:45]**
- Fixed: MCP config path (now uses correct windsurf subfolder)
- Added: Third-party warning and rollback instructions
- Added: GPU acceleration check in LM Studio setup
- Added: Model name verification step
- Added: Restart Windsurf fallback if refresh fails
- Added: Note about path customization

**[2026-01-29 10:40]**
- Initial setup plan created
