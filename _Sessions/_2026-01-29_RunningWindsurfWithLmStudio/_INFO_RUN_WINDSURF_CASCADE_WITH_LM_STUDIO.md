# INFO: Running Windsurf Cascade with Local LLMs via LM Studio

**Doc ID**: LMWS-IN01
**Goal**: Document methods to use local LLMs in LM Studio with Windsurf Cascade agent
**Timeline**: Created 2026-01-29

## Summary

- **Windsurf Cascade does NOT natively support local LLM backends** - it uses Codeium's cloud models exclusively [VERIFIED]
- **MCP bridge approach works** - Agent-Cascade MCP server routes prompts to local LLM, but Cascade still uses cloud model as orchestrator [VERIFIED]
- **LM-Studio-IDE-Plugin provides alternative** - Separate extension with chat panel and completions, NOT replacing Cascade [VERIFIED]
- **BYOK limited to cloud providers** - Only Claude models supported via API keys, no local endpoints [VERIFIED]
- **Best local coding models**: Qwen2.5-Coder, DeepSeek-Coder, CodeLlama [VERIFIED]

## Table of Contents

1. [The Core Limitation](#1-the-core-limitation)
2. [Available Approaches](#2-available-approaches)
3. [LM Studio Setup](#3-lm-studio-setup)
4. [Agent-Cascade MCP Server](#4-agent-cascade-mcp-server)
5. [LM-Studio-IDE-Plugin](#5-lm-studio-ide-plugin)
6. [Recommended Models](#6-recommended-models)
7. [Sources](#7-sources)
8. [Next Steps](#8-next-steps)
9. [Document History](#9-document-history)

## 1. The Core Limitation

**Windsurf Cascade cannot be configured to use local LLMs as its primary model.**

Key findings:
- Cascade is tightly integrated with Codeium's cloud infrastructure
- The model selection dropdown only shows Codeium-hosted models (SWE-1.5, Claude, GPT)
- BYOK (Bring Your Own Key) only supports cloud API providers (Anthropic Claude models)
- No configuration option exists to point Cascade at a local OpenAI-compatible endpoint
- This is by design - Codeium's business model relies on cloud model usage

**Why this matters:**
- Code sent to Cascade goes through Codeium's servers
- No true "air-gapped" or fully offline Cascade operation is possible
- Privacy-sensitive codebases cannot use Cascade without cloud exposure

## 2. Available Approaches

### 2.1 Approach A: MCP Bridge (Agent-Cascade)

**What it does:** Adds a `local_chat` MCP tool that Cascade can call to query a local LLM.

**How it works:**
1. Cascade (cloud model) remains the orchestrator
2. Cascade can invoke the `local_chat` tool when appropriate
3. The tool forwards prompts to LM Studio's OpenAI-compatible endpoint
4. Response returns to Cascade for integration

**Limitations:**
- Cascade cloud model still sees all context
- User cannot force Cascade to use local model exclusively
- Adds latency (two LLM calls: cloud + local)
- Useful for "second opinion" or specialized tasks only

### 2.2 Approach B: LM-Studio-IDE-Plugin

**What it does:** Provides a completely separate AI assistant in Windsurf/VS Code using local LLMs.

**Features:**
- Inline code completions (ghost text)
- Dedicated chat panel (separate from Cascade)
- Command palette actions (explain, refactor, write tests)
- MCP tools integration

**Limitations:**
- Does NOT replace or modify Cascade
- Two separate AI systems in the IDE
- No agentic file editing capabilities like Cascade
- Manual context management (@file, @selection directives)

### 2.3 Approach C: Alternative IDEs

For true local-only operation, consider:
- **Continue.dev** - Open-source AI assistant, supports local models
- **Aider** - CLI-based AI pair programmer
- **Cursor with Ollama** - Some community configurations exist
- **VS Code + CodeGPT extension** - Supports local endpoints

## 3. LM Studio Setup

### 3.1 Download and Install

**Download URL:** https://lmstudio.ai/download

**System Requirements (Windows):**
- CPU: AVX2 instruction set support (x64) or ARM64 (Snapdragon X Elite)
- RAM: 16GB+ recommended
- GPU: 4GB+ dedicated VRAM recommended
- OS: Windows 10/11

### 3.2 Start the API Server

1. Open LM Studio
2. Go to **Developer** tab (left sidebar)
3. Toggle **Start server** switch
4. Default endpoint: `http://localhost:1234/v1`

**CLI alternative:**
```powershell
lms server start
```

### 3.3 Load a Model

1. Go to **Search** tab
2. Search for model (e.g., "qwen2.5-coder")
3. Download preferred quantization (Q4_K_M recommended for balance)
4. Go to **Developer** tab
5. Select model from dropdown
6. Model auto-loads when server starts

### 3.4 Verify Server

```powershell
curl http://localhost:1234/v1/models
```

Should return JSON with loaded model info.

## 4. Agent-Cascade MCP Server

**Repository:** https://github.com/BlinkZer0/Agent-Cascade

### 4.1 Installation

```powershell
# Clone repository
git clone https://github.com/BlinkZer0/Agent-Cascade.git
cd Agent-Cascade/tools/agent-cascade

# Install and build
npm install
npm run build
```

### 4.2 Windsurf Configuration

Edit `%USERPROFILE%\.codeium\mcp_config.json`:

```json
{
  "mcpServers": {
    "agent-cascade": {
      "command": "node",
      "args": ["C:/path/to/Agent-Cascade/tools/agent-cascade/dist/server.js"],
      "env": {
        "LM_BASE_URL": "http://localhost:1234/v1",
        "DEFAULT_MODEL": "qwen2.5-coder"
      },
      "disabled": false,
      "disabledTools": []
    }
  }
}
```

### 4.3 Usage

After configuration:
1. Open Cascade panel
2. Go to Plugins > Manage
3. Verify "agent-cascade" appears
4. Refresh Cascade window
5. Cascade can now call `local_chat` tool

**Example prompt to Cascade:**
> "Use the local_chat tool to ask the local model to review this function for security issues."

### 4.4 Troubleshooting

- **Timeouts**: Increase `timeout_ms` in tool call
- **Model not found**: Verify `DEFAULT_MODEL` matches loaded model in LM Studio
- **HTTP errors**: Check LM Studio server is running on correct port

## 5. LM-Studio-IDE-Plugin

**Repository:** https://github.com/BlinkZer0/LM-Studio-IDE-Plugin

### 5.1 Installation

**Option 1: VSIX (Recommended)**
1. Download `.vsix` from GitHub Releases
2. In Windsurf: Extensions view (Ctrl+Shift+X)
3. Click "..." menu > "Install from VSIX..."
4. Select downloaded file

**Option 2: Lazy Install**
Extract to `C:\Users\USERNAME\.windsurf\extensions\`

### 5.2 Configuration

Settings (Ctrl+,):

```json
{
  "lmstudio.baseUrl": "http://localhost:1234/v1",
  "lmstudio.model": "qwen2.5-coder",
  "lmstudio.embeddingsModel": "nomic-embed-text"
}
```

### 5.3 Features

- **Inline completions**: Type and see ghost text suggestions, Tab to accept
- **Chat panel**: Click LM Studio icon in Activity Bar
- **Commands** (Ctrl+Shift+P):
  - LM Studio: Explain Selection
  - LM Studio: Write Tests
  - LM Studio: Refactor Function
  - LM Studio: Check Connection

### 5.4 Chat Directives

- `@file` - Include current file content
- `@selection` - Include selected text
- `@workspace` - Include workspace structure

## 6. Recommended Models

### 6.1 For Coding Tasks

- **Qwen2.5-Coder-7B-Q4_K_M** - Size: ~5GB, VRAM: 6GB+, best balance for consumer GPUs
- **Qwen2.5-Coder-14B-Q4_K_M** - Size: ~9GB, VRAM: 12GB+, better quality, needs more VRAM
- **DeepSeek-Coder-V2-Lite-Q4_K_M** - Size: ~9GB, VRAM: 12GB+, good instruction following
- **CodeLlama-7B-Q4_K_M** - Size: ~4GB, VRAM: 5GB+, fast, decent quality

### 6.2 Quantization Guide

- **Q8_0**: Highest quality, largest size
- **Q6_K**: Very high quality, ~25% smaller than Q8
- **Q5_K_M**: Good quality, recommended for most uses
- **Q4_K_M**: Balanced quality/size, **recommended default**
- **Q3_K_M**: Smaller but noticeable quality loss
- **Q2_K**: Smallest, significant quality degradation

### 6.3 Model Search in LM Studio

Search terms:
- `qwen2.5-coder gguf` - Qwen coder models
- `deepseek-coder gguf` - DeepSeek coder
- `codellama gguf` - Meta's CodeLlama

## 7. Sources

**Primary Sources:**
- `LMWS-IN01-SC-GTHB-AGCSC`: https://github.com/BlinkZer0/Agent-Cascade - Agent-Cascade MCP server documentation [VERIFIED]
- `LMWS-IN01-SC-GTHB-LMSPL`: https://github.com/BlinkZer0/LM-Studio-IDE-Plugin - LM Studio IDE Plugin documentation [VERIFIED]
- `LMWS-IN01-SC-LMST-DOCS`: https://lmstudio.ai/docs/developer/core/server - LM Studio server documentation [VERIFIED]
- `LMWS-IN01-SC-LMST-OAPI`: https://lmstudio.ai/docs/developer/openai-compat - OpenAI compatibility endpoints [VERIFIED]
- `LMWS-IN01-SC-WDSR-MCP`: https://docs.windsurf.com/windsurf/cascade/mcp - Windsurf MCP configuration [VERIFIED]
- `LMWS-IN01-SC-WDSR-MODL`: https://docs.windsurf.com/windsurf/models - Windsurf models and BYOK [VERIFIED]
- `LMWS-IN01-SC-RDDT-CDEM`: https://www.reddit.com/r/Codeium/comments/1h4jo15/ - Community discussion on local LLM limitations [VERIFIED]

## 8. Next Steps

1. **If privacy is critical**: Use LM-Studio-IDE-Plugin as standalone assistant, disable Cascade
2. **If Cascade features needed**: Accept cloud usage, optionally add Agent-Cascade for local secondary queries
3. **For experimentation**: Install both approaches, evaluate which workflow suits your needs
4. **Monitor Windsurf roadmap**: Local model support may be added in future versions

## 9. Document History

**[2026-01-29 10:30]**
- Initial research document created
- Documented core limitation: Cascade requires cloud models
- Documented two workaround approaches (MCP bridge, IDE plugin)
- Added LM Studio setup instructions
- Added model recommendations
