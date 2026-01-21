# INFO: Git Skills and MCP Servers

**Doc ID**: GIT-IN01
**Goal**: Research existing git skills/MCP servers to inform design of new git skill
**Timeline**: Created 2026-01-21

## Summary

- Official MCP Git Server exists with basic operations (clone, status, diff, log, commit) [VERIFIED]
- cyanheads/git-mcp-server provides 27 tools including reflog, but no dedicated file recovery workflow [VERIFIED]
- No existing skill specifically focused on file recovery from commit history [VERIFIED]
- Git file recovery uses: `git log --diff-filter=D`, `git checkout <commit>^ -- <file>`, `git reflog` [VERIFIED]
- Skills marketplace (skillzwave.ai, skillsmp.com) has git-worktrees skill, no recovery-focused skill found [VERIFIED]

## Table of Contents

1. [Existing Git MCP Servers](#1-existing-git-mcp-servers)
2. [Existing Git Skills](#2-existing-git-skills)
3. [File Recovery Techniques](#3-file-recovery-techniques)
4. [Gap Analysis](#4-gap-analysis)
5. [Sources](#5-sources)
6. [Next Steps](#6-next-steps)
7. [Document History](#7-document-history)

## 1. Existing Git MCP Servers

### 1.1 Official MCP Git Server

Location: `github.com/modelcontextprotocol/servers/tree/main/src/git`

**Features:**
- Read, search, and manipulate Git repositories
- Part of official MCP reference implementations
- Basic operations only

### 1.2 cyanheads/git-mcp-server

Location: `github.com/cyanheads/git-mcp-server`

**27 Tools in 6 categories:**
- **Repository**: git_init, git_clone, git_status, git_clean
- **Staging/Commit**: git_add, git_commit
- **History**: git_diff, git_log, git_show, git_blame, git_reflog
- **Branching**: git_branch, git_checkout, git_merge, git_rebase, git_cherry_pick
- **Remote**: git_remote, git_fetch, git_pull, git_push
- **Advanced**: git_tag, git_stash, git_reset, git_worktree, git_set_working_dir, git_clear_working_dir, git_wrapup_instructions

**Resources:** `git://working-directory`

**Observations:**
- Most comprehensive git MCP server found
- Has git_reflog tool (useful for recovery)
- No dedicated file recovery workflow/prompt
- TypeScript implementation, STDIO and HTTP transport

## 2. Existing Git Skills

### 2.1 Microsoft Agent Skills

Location: `github.com/microsoft/agent-skills`

**Structure:**
- `.github/skills/` - Modular knowledge packages
- Each skill has `SKILL.md` file
- No git-specific skill included (focus on Azure, FastAPI, React)

**Key Insight:** Skills are designed for selective loading to avoid "context rot"

### 2.2 OpenSkills (Universal Loader)

Location: `github.com/numman-ali/openskills`

**Features:**
- Universal loader for Claude Code, Cursor, Windsurf, Aider, Codex
- Progressive disclosure (load skills only when needed)
- Same SKILL.md format as Claude Code

**No git skill found in their collection**

### 2.3 SkillzWave Marketplace

Location: `skillzwave.ai`

**git-worktrees skill found:**
- Manages Git worktrees for parallel development
- Focus: multiple Claude sessions working simultaneously
- NOT focused on file recovery

## 3. File Recovery Techniques

### 3.1 Find Deleted Files

```powershell
git log --diff-filter=D --summary
```
Output shows `delete mode 100644 path/to/file` for each deletion.

### 3.2 Find When Specific File Was Deleted

```powershell
git log -- path/to/deleted_file.txt
```
Shows commits affecting that file path.

### 3.3 Restore Deleted File

From commit that deleted it (use `^` to get parent):
```powershell
git checkout <commit_hash>^ -- path/to/file
```

From known good commit:
```powershell
git checkout <commit_hash> -- path/to/file
```

### 3.4 Using Reflog for Recovery

```powershell
git reflog
git checkout HEAD@{n} -- path/to/file
```
Reflog tracks ALL changes, including those not in commit history.

### 3.5 List Files Changed in Commit

```powershell
git show --name-status <commit_hash>
```
Shows: A (added), M (modified), D (deleted) for each file.

## 4. Gap Analysis

**What exists:**
- MCP servers with git commands (but no guided workflows)
- Skills for worktrees, Azure, etc. (but not git fundamentals)

**What's missing:**
- Step-by-step file recovery guidance
- Commit navigation with file change summaries
- Setup/installation instructions for git
- Windows-specific considerations (PowerShell commands)

**Our skill should provide:**
- SETUP.md for git installation
- Guided file recovery workflow
- Commit-by-commit navigation
- List added/modified/deleted files per commit
- Recover specific file versions

## 5. Sources

**Primary Sources:**
- `GIT-IN01-SC-MCPIO-EXMPL`: https://modelcontextprotocol.io/examples - Official MCP Git server listed
- `GIT-IN01-SC-CYAN-GMCP`: https://github.com/cyanheads/git-mcp-server - 27 tools, comprehensive
- `GIT-IN01-SC-MSFT-AGSK`: https://github.com/microsoft/agent-skills - Skill structure patterns
- `GIT-IN01-SC-OPSK-MAIN`: https://github.com/numman-ali/openskills - Universal skill loader
- `GIT-IN01-SC-SKLZ-WRTREE`: https://skillzwave.ai - git-worktrees skill (not recovery)
- `GIT-IN01-SC-DLFT-RCVR`: https://www.delftstack.com/howto/git/git-history-of-deleted-file/ - Recovery commands

## 6. Next Steps

1. Create `git` skill folder in `.windsurf/skills/`
2. Write SETUP.md with git installation for Windows
3. Write SKILL.md with focus on file recovery workflows
4. Include commit navigation and file listing commands

## 7. Document History

**[2026-01-21 08:40]**
- Initial research document created
- Analyzed 6 primary sources
- Identified gap: no recovery-focused git skill exists
