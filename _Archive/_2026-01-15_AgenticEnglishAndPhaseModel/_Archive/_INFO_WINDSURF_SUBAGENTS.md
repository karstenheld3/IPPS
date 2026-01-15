# INFO: Windsurf Cascade Sub-Agent Capabilities

**Doc ID**: WSAG-IN01
**Goal**: Document how Windsurf Cascade can spawn sub-agents and alternatives for multi-agent workflows
**Timeline**: Created 2026-01-15

## Summary

- **Windsurf has NO native sub-agent delegation** like Claude Code's Task tool [VERIFIED]
- **Fast Context** is the only built-in subagent - specialized for codebase search using SWE-grep models [VERIFIED]
- **Simultaneous Cascades** (Wave 8+) allow multiple independent Cascade sessions, NOT programmatic sub-agents [VERIFIED]
- **Parallel Agents** (Wave 13) enable multiple Cascades working on separate branches via Git worktrees [VERIFIED]
- **sub-agents-mcp** is an MCP server that brings Claude Code-style sub-agents to Windsurf [VERIFIED]
- **Workaround**: Use MCP + external CLI (claude, cursor-agent, gemini, codex) as execution backend [VERIFIED]

## Table of Contents

1. [Native Windsurf Capabilities](#1-native-windsurf-capabilities)
2. [Comparison with Claude Code Sub-Agents](#2-comparison-with-claude-code-sub-agents)
3. [MCP-Based Sub-Agent Solution](#3-mcp-based-sub-agent-solution)
4. [Practical Alternatives](#4-practical-alternatives)
5. [Sources](#5-sources)
6. [Next Steps](#6-next-steps)
7. [Document History](#7-document-history)

## 1. Native Windsurf Capabilities

### 1.1 Fast Context Subagent (Built-in)

Windsurf has ONE built-in subagent: **Fast Context**, a specialized retrieval subagent for codebase search.

**Purpose**: Retrieve relevant code from codebase up to 20x faster than traditional agentic search.

**How it works**:
- Powered by SWE-grep and SWE-grep-mini models (trained via reinforcement learning)
- Executes up to 8 parallel tool calls per turn, max 4 turns
- Uses restricted tool set: grep, read, glob (cross-platform)
- Activates automatically on code search queries
- Force activation: `Cmd+Enter` (Mac) or `Ctrl+Enter` (Win/Linux)

**Key difference from Claude Code**: Fast Context is automatic and invisible - you cannot define custom subagents or delegate arbitrary tasks to it.

### 1.2 Simultaneous Cascades (Wave 8+)

Multiple independent Cascade sessions can run simultaneously.

**What it is**:
- Navigate between sessions via dropdown (top left of Cascade panel)
- Each Cascade has its own conversation context
- User-initiated (click "+" to create new Cascade)

**What it is NOT**:
- NOT programmatic sub-agent spawning
- NOT automatic task delegation
- Cascades cannot spawn other Cascades

**Warning**: If two Cascades edit the same file simultaneously, edits can race and fail.

### 1.3 Parallel Agents (Wave 13)

First-class support for running multiple Cascade agents on separate branches.

**Features**:
- Git worktrees integration - each agent works on different branch in separate directory
- Multi-pane interface for side-by-side monitoring
- Dedicated zsh terminal for reliable execution
- Up to 5 agents working on 5 bugs simultaneously

**Limitation**: Still user-initiated. Cascade cannot programmatically spawn another Cascade to delegate a subtask.

## 2. Comparison with Claude Code Sub-Agents

### 2.1 Claude Code Native Sub-Agents

Claude Code has built-in sub-agent support with the **Task tool**:

**Built-in subagents**:
- **Explore**: Fast file discovery using Haiku, read-only tools
- **Plan**: Codebase research for planning, read-only tools
- **General-purpose**: Complex research, all tools available

**Key capabilities Windsurf lacks**:
- `Task` tool for programmatic delegation
- Custom subagent definitions in `.claude/agents/`
- Model selection per subagent (route to cheaper/faster models)
- Tool restrictions per subagent
- Automatic delegation based on task type

### 2.2 Feature Comparison

**Claude Code**:
- Can spawn 10+ sub-agents in parallel via Task tool
- Sub-agents get fresh context (no leakage)
- Sub-agents cannot spawn other sub-agents (prevents infinite nesting)
- Custom agents defined in markdown files
- Foreground or background execution

**Windsurf**:
- No programmatic sub-agent spawning
- Fast Context is the only automatic subagent (retrieval-only)
- Multiple Cascades require user initiation
- No Task tool equivalent
- No custom agent definitions (native)

## 3. MCP-Based Sub-Agent Solution

### 3.1 sub-agents-mcp Server

**Repository**: https://github.com/shinpr/sub-agents-mcp

An MCP server that brings Claude Code-style sub-agents to any MCP-compatible tool, including Windsurf.

**How it works**:
1. Define agents as markdown files in a folder
2. Configure MCP server with execution backend (cursor-agent, claude, gemini, codex CLI)
3. MCP server exposes agents as callable tools
4. Main agent delegates tasks by calling the MCP tool

### 3.2 Configuration for Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "sub-agents": {
      "command": "npx",
      "args": ["-y", "sub-agents-mcp"],
      "env": {
        "AGENTS_DIR": "C:\\Users\\YourUser\\agents",
        "AGENT_TYPE": "claude"
      }
    }
  }
}
```

**Execution backends** (choose one):
- `cursor` - Uses cursor-agent CLI
- `claude` - Uses Claude Code CLI
- `gemini` - Uses Gemini CLI
- `codex` - Uses Codex CLI

### 3.3 Creating a Sub-Agent

Create `code-reviewer.md` in your AGENTS_DIR:

```markdown
# Code Reviewer
Review code for quality and maintainability issues.

## Task
- Find bugs and potential issues
- Suggest improvements
- Check code style consistency

## Done When
- All target files reviewed
- Issues listed with explanations
```

### 3.4 Design Philosophy

Each sub-agent starts with **fresh context**:
- No context leakage between runs
- Sub-agents specialize in single goal
- Large tasks safely split into smaller sub-tasks
- Main agent coordinates without hitting context limits

**Trade-off**: Startup overhead for each call, but ensures accuracy and reliability.

## 4. Practical Alternatives

### 4.1 Workflows as Pseudo-Subagents

Use Windsurf workflows (`.windsurf/workflows/*.md`) as structured task execution:
- Define step-by-step instructions
- Invoke with `/workflow-name`
- Cascade follows instructions sequentially

**Limitation**: Single Cascade, no parallel execution, no fresh context isolation.

### 4.2 Skills for Reusable Behavior

Use Windsurf skills (`.windsurf/skills/*/SKILL.md`):
- Define specialized knowledge and instructions
- Invoke with `@skill-name`
- Auto-invoked based on description match

**Limitation**: Modifies behavior of current Cascade, not separate execution context.

### 4.3 Manual Multi-Cascade Pattern

1. Open multiple Cascade panels (Simultaneous Cascades)
2. Assign each Cascade a specific task
3. Use Git worktrees for branch isolation
4. Monitor side-by-side

**Limitation**: Manual orchestration required, no programmatic delegation.

## 5. Sources

**Primary Sources**:
- `WSAG-IN01-SC-WSRF-DOCS`: https://docs.windsurf.com/windsurf/cascade/cascade - Official Cascade documentation [VERIFIED]
- `WSAG-IN01-SC-WSRF-FCTX`: https://docs.windsurf.com/context-awareness/fast-context - Fast Context subagent documentation [VERIFIED]
- `WSAG-IN01-SC-BYTE-WV13`: https://byteiota.com/windsurf-wave-13-free-swe-1-5-parallel-agents-escalate-ai-ide-war/ - Wave 13 parallel agents announcement [VERIFIED]
- `WSAG-IN01-SC-SHPR-SAMCP`: https://github.com/shinpr/sub-agents-mcp - Sub-agents MCP server for Windsurf [VERIFIED]
- `WSAG-IN01-SC-CLCD-SUBAG`: https://code.claude.com/docs/en/sub-agents - Claude Code sub-agent documentation (comparison) [VERIFIED]
- `WSAG-IN01-SC-COGN-SWGRP`: https://cognition.ai/blog/swe-grep - SWE-grep model powering Fast Context [VERIFIED]
- `WSAG-IN01-SC-LNKD-FCTX`: https://www.linkedin.com/posts/windsurf_introducing-the-new-fast-context-subagent-activity-7384664960938758145-Z29u - Fast Context announcement [VERIFIED]

## 6. Next Steps

1. **For immediate sub-agent needs**: Install sub-agents-mcp and configure with claude or cursor-agent CLI backend
2. **For simpler delegation**: Use workflows to structure multi-step tasks
3. **For parallel work**: Use Simultaneous Cascades with Git worktrees (Wave 13 style)
4. **Watch for updates**: Native sub-agent support may come in future Windsurf releases

## 7. Document History

**[2026-01-15 20:15]**
- Initial research document created
- Documented Fast Context as only built-in subagent
- Documented Simultaneous Cascades vs true sub-agents
- Added sub-agents-mcp as workaround solution
- Compared with Claude Code native sub-agent capabilities
- Listed practical alternatives (workflows, skills, manual multi-Cascade)
