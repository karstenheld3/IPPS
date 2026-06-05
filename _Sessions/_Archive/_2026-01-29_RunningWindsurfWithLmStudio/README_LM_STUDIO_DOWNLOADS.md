# LM Studio Integration Downloads

## Prerequisites

- **Node.js 20+** - Required for Agent-Cascade build

## Downloaded Files

- **Agent-Cascade-main.zip** - MCP server to bridge Cascade to local LLMs
- **Windsurf.LM-Studio-IDE-Plugin.7z** - IDE plugin for LM Studio integration (alternative: download VSIX from GitHub releases)

## Manual Download Required: LM Studio

LM Studio requires browser-based download (dynamic page with JavaScript).

**Download URL:** https://lmstudio.ai/download

**Steps:**
1. Visit https://lmstudio.ai/download
2. Select "Windows" platform
3. Download the `.exe` installer
4. Save to this folder

## Installation Instructions

### 1. LM Studio

1. Run the downloaded `.exe` installer
2. Follow installation wizard
3. Launch LM Studio
4. Go to Search tab, download a model (e.g., `qwen2.5-coder`)

### 2. Agent-Cascade MCP Server

```powershell
# Extract
Expand-Archive -Path "Agent-Cascade-main.zip" -DestinationPath "."

# Install
cd Agent-Cascade-main/tools/agent-cascade
npm install
npm run build
```

Then configure in `%USERPROFILE%\.codeium\mcp_config.json` (see INFO document for details).

### 3. LM-Studio-IDE-Plugin (Windsurf)

**Option A: VSIX Installation (Recommended)**

1. Download VSIX from https://github.com/BlinkZer0/LM-Studio-IDE-Plugin/releases
2. In Windsurf: Extensions view (Ctrl+Shift+X)
3. Click "..." menu > "Install from VSIX..."
4. Select the downloaded `.vsix` file

**Option B: Manual Extraction**

```powershell
# Extract using workspace 7z
& "E:\Dev\IPPS\.tools\7z\7z.exe" x "Windsurf.LM-Studio-IDE-Plugin.7z" -o"$env:USERPROFILE\.windsurf\extensions\"
```

Or manually extract and drag the folder to `%USERPROFILE%\.windsurf\extensions\`

## Related Documentation

See: `E:\Dev\IPPS\Docs\FurtherResearch\_INFO_RUN_WINDSURF_CASCADE_WITH_LM_STUDIO.md`
