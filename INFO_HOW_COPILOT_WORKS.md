# INFO: How GitHub Copilot Works

**Doc ID**: CPLT-IN01
**Goal**: Document GitHub Copilot features, configuration, and integration for cross-agent compatibility reference

## Summary

Key findings for cross-agent compatibility:
- GitHub Copilot uses `.github/copilot-instructions.md` for repository-wide instructions [VERIFIED]
- Path-specific instructions in `.github/instructions/*.instructions.md` with `applyTo` glob [VERIFIED]
- Custom agents in `.github/agents/*.agent.md` (similar to Claude Code subagents) [VERIFIED]
- Model Context Protocol (MCP) servers configured in `.vscode/mcp.json` [VERIFIED]
- Supports `AGENTS.md` for multi-agent compatibility (same as Codex CLI) [VERIFIED]
- No slash commands or skills - uses prompt files (`.github/prompts/*.prompt.md`) instead [VERIFIED]

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Directory Structure](#directory-structure)
4. [Settings and Configuration](#settings-and-configuration)
5. [AI Assistant Features](#ai-assistant-features)
6. [Memory and Instructions](#memory-and-instructions)
7. [Custom Agents](#custom-agents)
8. [MCP Integration](#mcp-integration)
9. [Prompt Files](#prompt-files)
10. [Key Files Reference](#key-files-reference)
11. [Sources](#sources)

## Overview

GitHub Copilot is an AI-powered coding assistant integrated into Visual Studio Code (and other IDEs). It provides code suggestions, explanations, and automated implementations based on natural language prompts and existing code context.

**Key characteristics:**
- IDE-integrated (VS Code, Visual Studio, JetBrains, Xcode, Eclipse)
- Inline code suggestions as you type
- Chat interface for questions and code changes
- Autonomous agent mode for complex tasks
- MCP support for external tool integration

**Copilot Products:**
- **Copilot Free** - Limited features
- **Copilot Pro/Pro+** - Individual subscription
- **Copilot Business** - Organization subscription
- **Copilot Enterprise** - Enterprise features with policy management

## Installation

**VS Code:**
1. Install the GitHub Copilot extension from the Marketplace
2. Sign in with your GitHub account
3. Copilot icon appears in the activity bar

**Other IDEs:**
- Visual Studio: Install via Extensions menu
- JetBrains IDEs: Install from Marketplace
- Xcode: Install Copilot for Xcode app
- Eclipse: Install from Eclipse Marketplace

**CLI (Public Preview):**
```bash
# Install GitHub CLI first, then:
gh extension install github/gh-copilot
```

## Directory Structure

```
your-project/
├── .github/
│   ├── copilot-instructions.md       # Repository-wide instructions
│   ├── instructions/                  # Path-specific instructions
│   │   ├── python.instructions.md     # applyTo: "**/*.py"
│   │   ├── tests.instructions.md      # applyTo: "**/test_*.py"
│   │   └── api.instructions.md        # applyTo: "src/api/**/*.ts"
│   ├── agents/                        # Custom agents
│   │   ├── planner.agent.md
│   │   └── reviewer.agent.md
│   └── prompts/                       # Reusable prompts
│       ├── review.prompt.md
│       └── refactor.prompt.md
├── .vscode/
│   └── mcp.json                       # MCP server configuration
└── AGENTS.md                          # Multi-agent instructions (optional)
```

**User-level files (VS Code profile):**
- User instructions files synced via Settings Sync
- Custom agents in VS Code profile folder

## Settings and Configuration

### VS Code Settings

Key Copilot settings in `settings.json`:

```json
{
  "github.copilot.chat.codeGeneration.useInstructionFiles": true,
  "github.copilot.chat.reviewSelection.instructions": [
    { "file": "guidance/review-guidelines.md" }
  ],
  "github.copilot.chat.commitMessageGeneration.instructions": [
    { "text": "Use conventional commits format" }
  ],
  "chat.useAgentsMdFile": true
}
```

**Instruction settings (deprecated in VS Code 1.102+):**
- `github.copilot.chat.codeGeneration.instructions` - Use instruction files instead
- `github.copilot.chat.testGeneration.instructions` - Use instruction files instead

**Active settings:**
- `reviewSelection.instructions` - Code review guidelines
- `commitMessageGeneration.instructions` - Commit message format
- `pullRequestDescriptionGeneration.instructions` - PR description format

### Enabling Features

- **Instruction files**: `github.copilot.chat.codeGeneration.useInstructionFiles: true`
- **AGENTS.md support**: `chat.useAgentsMdFile: true`
- **MCP servers**: Enabled by default (policy-controlled for Business/Enterprise)

## AI Assistant Features

### Core Capabilities

- **Inline suggestions** - Autocomplete as you type
- **Next edit suggestions** - Predict next logical code change (VS Code, Xcode, Eclipse)
- **Chat** - Natural language Q&A about code
- **Copilot Edits** - Multi-file changes from single prompt
- **Agent mode** - Autonomous task execution
- **Code review** - AI-generated review suggestions
- **Pull request (PR) summaries** - Auto-generate PR descriptions

### Chat Modes

- **Ask** - Questions and explanations (read-only)
- **Edit** - Granular control over file edits
- **Agent** - Autonomous mode with terminal commands and MCP tools

### Smart Actions

Built-in AI-enhanced actions:
- Generate commit messages (sparkle icon)
- Fix errors in editor
- Rename symbols with AI assistance
- Semantic search for files

### Keyboard Shortcuts (VS Code)

- `Ctrl+I` - Open inline chat
- `Ctrl+Shift+I` - Open Copilot Chat panel
- `Tab` - Accept inline suggestion
- `Esc` - Dismiss suggestion
- `Alt+]` / `Alt+[` - Cycle through suggestions

## Memory and Instructions

### copilot-instructions.md

Repository-wide instructions that apply to all chat requests.

**Location:** `.github/copilot-instructions.md`

**Example:**
```markdown
# Project Coding Standards

- Use TypeScript for all new code
- Follow existing ESLint configuration
- Write tests for all new functions using Jest
- Use functional components with hooks in React
- Follow the Repository pattern for data access
```

### Path-Specific Instructions (.instructions.md)

Apply instructions conditionally based on file patterns.

**Location:** `.github/instructions/*.instructions.md`

**Format:**
```yaml
---
applyTo: "**/*.py"
description: Python coding standards
---

# Python Guidelines
- Follow PEP 8 style guide
- Use type hints for all functions
- Write docstrings for public functions
```

**Glob patterns:**
- `**/*.py` - All Python files recursively
- `src/**/*.ts` - TypeScript files in src/
- `**/test_*.py` - All test files
- `**/*.{ts,tsx}` - TypeScript and TSX files

### AGENTS.md

Multi-agent compatible instructions file (also used by OpenAI Codex CLI).

**Location:** Project root or subfolders

**Enable:** `chat.useAgentsMdFile: true` in VS Code settings

Instructions in AGENTS.md apply to all chat requests in the workspace.

### Instruction Priority

When multiple instruction sources exist, VS Code combines them (no guaranteed order):
1. `.github/copilot-instructions.md`
2. `.instructions.md` files matching current file
3. `AGENTS.md` files
4. Settings-based instructions

## Custom Agents

Custom agents provide specialized AI configurations for different tasks.

### Agent File Structure

**Location:** `.github/agents/*.agent.md` or VS Code profile folder

**Format:**
```yaml
---
name: Planner
description: Generate implementation plans without making code changes
tools: ['fetch', 'githubRepo', 'search', 'usages']
model: Claude Sonnet 4
handoffs:
  - label: Start Implementation
    agent: implementation
    prompt: Implement the plan outlined above.
    send: false
---

# Planning Instructions

You are in planning mode. Generate an implementation plan without making code edits.

Include these sections:
- Overview
- Requirements
- Implementation Steps
- Testing
```

**Frontmatter fields:**
- `name` - Display name in agent dropdown
- `description` - When to use this agent
- `tools` - Available tools (array)
- `model` - AI model to use
- `handoffs` - Sequential workflow transitions
- `target` - `vscode` or `github-copilot`
- `mcp-servers` - MCP servers to enable

### Built-in Agents

- **Ask** - Questions and explanations
- **Edit** - Controlled file editing
- **Agent** - Autonomous coding

### Agent Commands

- Configure Custom Agents from agent dropdown
- `Chat: New Custom Agent` command
- Select agent from dropdown in Chat view

## MCP Integration

Model Context Protocol enables Copilot to access external tools and data sources.

### Configuration

**Location:** `.vscode/mcp.json`

**Format:**
```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "github-token",
      "description": "GitHub Personal Access Token",
      "password": true
    }
  ],
  "servers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${input:github-token}"
      }
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

### Server Types

**stdio servers:**
```json
{
  "servers": {
    "local-server": {
      "command": "node",
      "args": ["server.js"],
      "env": { "API_KEY": "${input:api-key}" }
    }
  }
}
```

**HTTP servers:**
```json
{
  "servers": {
    "remote-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${input:token}"
      }
    }
  }
}
```

### MCP Commands

- Tools button in Chat view to toggle tools
- `#tool:toolName` to reference tools in prompts
- Add Context button to attach MCP resources

### Finding MCP Servers

- GitHub MCP server registry: https://github.com/mcp
- Official server repository: https://github.com/modelcontextprotocol/servers
- VS Code Marketplace extensions

## Prompt Files

Reusable prompt templates for common tasks.

**Location:** `.github/prompts/*.prompt.md`

**Format:**
```yaml
---
description: Code review checklist
tools: ['search', 'fetch']
agent: reviewer
---

Review the following code for:
1. Security vulnerabilities
2. Performance issues
3. Code style violations
4. Missing error handling

Provide specific, actionable feedback.
```

**Usage:**
- Add Context > Prompts in Chat view
- Reference with Markdown links in other files

## Key Files Reference

**Repository Config:**
- `.github/copilot-instructions.md` - Repository-wide instructions
- `.github/instructions/*.instructions.md` - Path-specific instructions
- `.github/agents/*.agent.md` - Custom agents
- `.github/prompts/*.prompt.md` - Reusable prompts
- `.vscode/mcp.json` - MCP server configuration
- `AGENTS.md` - Multi-agent instructions

**User Config (VS Code):**
- User instructions files (synced via Settings Sync)
- Custom agents in VS Code profile folder
- `settings.json` - Copilot settings

**Settings Keys:**
- `github.copilot.chat.codeGeneration.useInstructionFiles`
- `github.copilot.chat.reviewSelection.instructions`
- `github.copilot.chat.commitMessageGeneration.instructions`
- `chat.useAgentsMdFile`

## Sources

**Official Documentation:** [VERIFIED 2026-01-15]
- https://code.visualstudio.com/docs/copilot/overview - VS Code Copilot overview
- https://code.visualstudio.com/docs/copilot/customization/custom-instructions - Custom instructions
- https://code.visualstudio.com/docs/copilot/customization/custom-agents - Custom agents
- https://code.visualstudio.com/docs/copilot/customization/mcp-servers - MCP servers
- https://docs.github.com/en/copilot/get-started/features - Copilot features
- https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot - GitHub Docs instructions

**Additional Resources:**
- https://github.com/github/awesome-copilot - Community examples

## Document History

**[2026-01-15 08:40]**
- Initial document created from official GitHub Copilot documentation
- Researched: overview, custom instructions, agents, MCP, prompt files
- Sources verified against code.visualstudio.com and docs.github.com

