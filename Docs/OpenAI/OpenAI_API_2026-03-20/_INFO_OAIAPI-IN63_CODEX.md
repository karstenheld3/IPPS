# Codex

**Doc ID**: OAIAPI-IN63
**Goal**: Document Codex - OpenAI's cloud software engineering agent for code tasks, automations, and repository management
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

Codex is OpenAI's cloud-based software engineering agent that operates in sandboxed environments to complete coding tasks. Available via web app (codex.openai.com) and CLI (`codex-cli`). Codex connects to Git repositories, reads code, writes files, runs commands, executes tests, and creates pull requests. Tasks run in isolated sandbox environments with configurable access levels: read-only, workspace write, or full access. Supports background automations (scheduled/triggered tasks), subagents for parallelization, web search (cached or live), screenshot/design spec input, and code review by separate agents. Sandbox modes control what Codex can do: file modifications, command execution, network access. Approval modes keep humans in the loop for sensitive operations. Codex uses specialized models optimized for software engineering tasks. Supports multiple languages, frameworks, and build systems. The CLI provides local development integration with terminal-based interaction. [VERIFIED] (OAIAPI-SC-OAI-CODEX)

## Key Facts

- **Interfaces**: Web app (codex.openai.com) and CLI (codex-cli) [VERIFIED] (OAIAPI-SC-OAI-CODEX)
- **Sandbox modes**: Read-only, workspace write, full access [VERIFIED] (OAIAPI-SC-OAI-CODEX)
- **Repository integration**: Git repos, PRs, code review [VERIFIED] (OAIAPI-SC-OAI-CODEX)
- **Automations**: Background tasks, scheduled/triggered [VERIFIED] (OAIAPI-SC-OAI-CODEX)
- **Subagents**: Parallel task execution [VERIFIED] (OAIAPI-SC-OAI-CODEX)
- **Web search**: Cached (OpenAI index) or live mode [VERIFIED] (OAIAPI-SC-OAI-CODEX)
- **Visual input**: Screenshots and design specs [VERIFIED] (OAIAPI-SC-OAI-CODEX)

## Use Cases

- **Feature implementation**: Describe a feature, Codex writes the code
- **Bug fixing**: Point Codex at an issue, it investigates and fixes
- **Code review**: Automated review before commit/push
- **Refactoring**: Large-scale code changes across files
- **Test writing**: Generate tests for existing code
- **Documentation**: Auto-generate docs from code
- **Dependency updates**: Update packages and fix breaking changes

## Architecture

```
User (Web/CLI)
  |
  v
Codex Task
  |
  v
Sandboxed Environment
  ├─> Git Repository (clone/read/write)
  ├─> File System (read/write per sandbox mode)
  ├─> Command Execution (per sandbox mode)
  ├─> Web Search (cached or live)
  └─> Network (per sandbox mode)
  |
  v
Output (PR, files, logs)
```

## Sandbox Modes

- **Read-only**: Can read files and run read-only commands. Cannot modify files
- **Workspace write**: Can modify files within workspace. Cannot run arbitrary commands
- **Full access**: Full file system, command execution, and network access. Highest risk

## Automations

Background automations run tasks without manual triggering:
- **Scheduled**: Run at intervals (e.g., daily dependency check)
- **Triggered**: Run on events (e.g., new PR, issue created)
- **Risk note**: Full access sandbox mode with background automations carries elevated risk

## CLI Usage

```bash
# Install
npm install -g codex-cli

# Start task
codex "Add input validation to the user registration form"

# With screenshot input
codex "Match this design" --image design-spec.png

# Code review
codex review --before-push

# Subagents for parallel work
codex "Refactor auth module" --parallel
```

## SDK Examples (Python)

> **SDK note**: `client.codex.*` methods are not available in openai Python SDK v2.29.0.
> Codex is primarily used via web app or CLI. Use `httpx` or `requests` for direct REST API calls.

### Create Codex Task via API

```python
from openai import OpenAI

client = OpenAI()

# Codex tasks are typically created via web app or CLI
# The API provides task management for programmatic integration

task = client.codex.tasks.create(
    description="Add rate limiting middleware to the Express API server",
    repository="https://github.com/myorg/api-server",
    sandbox_mode="workspace_write",
    rules=[
        "Do not modify existing tests",
        "Use express-rate-limit package",
        "Add rate limit of 100 requests per 15 minutes"
    ]
)

print(f"Task ID: {task.id}")
print(f"Status: {task.status}")
```

### Monitor Task Progress

```python
from openai import OpenAI
import time

client = OpenAI()

def wait_for_task(task_id: str, timeout: int = 600):
    """Wait for Codex task completion"""
    start = time.time()
    
    while True:
        task = client.codex.tasks.retrieve(task_id)
        elapsed = time.time() - start
        
        print(f"[{elapsed:.0f}s] Status: {task.status}")
        
        if task.status in ("completed", "failed", "cancelled"):
            return task
        
        if elapsed > timeout:
            raise TimeoutError(f"Task timed out after {timeout}s")
        
        time.sleep(10)

try:
    task = wait_for_task("task_abc123")
    if task.status == "completed":
        print(f"PR: {task.pull_request_url}")
    else:
        print(f"Failed: {task.error}")
except Exception as e:
    print(f"Error: {e}")
```

## Error Responses

- **400 Bad Request** - Invalid task parameters
- **401 Unauthorized** - Invalid API key
- **403 Forbidden** - Repository access denied
- **429 Too Many Requests** - Concurrent task limit exceeded

## Differences from Other APIs

- **vs Anthropic Claude Code**: Similar concept - AI coding agent. Claude Code runs locally via CLI
- **vs Gemini**: No equivalent cloud coding agent
- **vs Grok**: No equivalent coding agent
- **vs GitHub Copilot Workspace**: Similar cloud-based coding environment with AI agent

## Limitations and Known Issues

- **Sandbox constraints**: Some operations require full access mode [VERIFIED] (OAIAPI-SC-OAI-CODEX)
- **Repository size**: Very large repos may have longer setup times [ASSUMED]
- **Language coverage**: Best for popular languages; less effective for niche ones [ASSUMED]
- **Background automation risk**: Full access + background = potential for unintended changes [VERIFIED] (OAIAPI-SC-OAI-CODEX)

## Sources

- OAIAPI-SC-OAI-CODEX - Codex Documentation

## Document History

**[2026-03-21 09:48]**
- Added: SDK v2.29.0 note - client.codex.* not in Python SDK (CLI/web app only)

**[2026-03-20 18:32]**
- Initial documentation created
