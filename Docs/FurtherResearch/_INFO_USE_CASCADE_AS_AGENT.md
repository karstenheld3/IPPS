# Using Windsurf Cascade as an Autonomous Development Agent

**Goal**: Research and document best practices for using Windsurf Cascade for autonomous development work.

## Summary (TL;DR)

**Key enablers for autonomous Cascade work:**
- Enable **Auto-Continue** setting to automatically continue when tool call limit (20) is hit
- Enable **Turbo Mode** for auto-executing terminal commands (configure allow/deny lists)
- Use **Workflows** (`/workflow-name`) for repeatable multi-step processes
- Use **Rules** (always-on, glob-based, or manual) to embed coding standards
- Add **MCP servers** for extended capabilities (Playwright for browser, GitHub for repos)
- Use **Cascade Hooks** for custom automation (logging, formatters, validation)
- Use **AGENTS.md** files for directory-scoped instructions

**Spec-Driven Development pattern (4 phases):**
1. **Specify**: Create `requirements.md` with user stories and acceptance criteria
2. **Plan**: Generate `plan.md` with technical approach and architecture
3. **Tasks**: Break down into `tasks.md` with checkboxes and phases
4. **Implement**: Execute tasks one phase at a time, verify after each

**Code quality patterns:**
- Write tests BEFORE code (TDD approach) - agent iterates until tests pass
- Use checklists/scratchpads in markdown files for complex tasks
- Have one agent write code, another agent verify (multi-agent pattern)
- Use small, focused task scopes - avoid "do everything" prompts
- Always verify with independent sessions (use /clear or separate Cascade panels) for complex implementations

## Table of Contents

1. Avoiding the "Continue Response" Problem
2. Adding Capabilities for Autonomous Work
3. Spec Driven Development with Cascade
4. Maximizing Code Quality and Bugfree Implementations
5. Sources and References

## 1. Avoiding the "Continue Response" Problem

### The Problem

Cascade has a **20 tool calls per prompt** limit. When the trajectory stops, you must click "Continue" to resume. Each continue counts as a new prompt credit. This interrupts autonomous work.

### Solution 1: Auto-Continue Setting [VERIFIED]

Windsurf has an **Auto-Continue** setting that automatically continues when the limit is hit.

**How to enable:**
- Settings > Cascade > Auto-Continue
- Consumes prompt credits corresponding to the model you are using

### Solution 2: Turbo Mode [VERIFIED]

Turbo Mode auto-executes terminal commands without asking for permission.

**How to enable:**
- Windsurf Settings panel (bottom right corner of editor)
- Toggle "Turbo Mode" on

**Configure safety with Allow/Deny lists:**
- **Allow list**: Commands that always auto-execute (e.g., `git`, `npm test`)
  - Setting: `windsurf.cascadeCommandsAllowList`
- **Deny list**: Commands that never auto-execute (e.g., `rm`, `sudo`)
  - Setting: `windsurf.cascadeCommandsDenyList`

### Solution 3: Workflow-Based Continuation [VERIFIED]

Design workflows that use checkpoints and resume patterns:
- Break work into phases with explicit checkpoints
- Use markdown files to track state (`tasks.md`, `progress.md`)
- Agent can read state files and continue from where it left off

### Limitation: No True "Fully Autonomous" Mode [CONFIRMED]

As of current Windsurf version, there is no way to make Cascade run completely unattended like Gemini CLI. The Auto-Continue helps but still requires occasional user presence for:
- Permission prompts for file edits
- Error handling decisions
- Large context decisions

## 2. Adding Capabilities for Autonomous Work

### 2.1 MCP Servers (Model Context Protocol)

MCP extends Cascade with custom tools. Configure in `~/.codeium/windsurf/mcp_config.json`.

**Key MCP Servers for Autonomous Work:**

**Playwright MCP (Browser Automation)** [VERIFIED - Microsoft Official]
- Repository: `github.com/microsoft/playwright-mcp`
- Features: Click, navigate, fill forms, take screenshots, get console logs
- Uses accessibility tree (no vision models needed)
- Installation:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

**GitHub MCP (Repository Operations)**
- Automate: push code, create PRs, analyze repositories
- Installation:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
      }
    }
  }
}
```

**Note:** Cascade has a limit of 100 total MCP tools enabled at any time.

### 2.2 Cascade Hooks [VERIFIED]

Hooks are shell commands that run automatically when specific Cascade actions occur.

**Configuration locations (merged in order):**
- System-level: `C:\ProgramData\Windsurf\hooks.json` (Windows)
- User-level: `~/.codeium/windsurf/hooks.json`
- Workspace-level: `.windsurf/hooks.json`

**Hook Events:**
- `pre_read_code` / `post_read_code` - Before/after reading files
- `pre_write_code` / `post_write_code` - Before/after writing files
- `pre_run_command` / `post_run_command` - Before/after terminal commands
- `pre_mcp_tool_use` / `post_mcp_tool_use` - Before/after MCP tool calls
- `pre_user_prompt` / `post_cascade_response` - Before/after prompts

**Use Cases:**
- **Logging**: Track every file read, code change, command executed
- **Security**: Block access to sensitive files or dangerous commands
- **Quality**: Run linters/formatters automatically after code modifications
- **Integration**: Connect to issue trackers, notification systems

**Exit Codes:**
- Exit code `2` in pre-hooks **blocks** the action (useful for validation)

### 2.3 AGENTS.md Files [VERIFIED]

Create `AGENTS.md` (or `agents.md`) for directory-scoped instructions.

**Behavior:**
- **Root directory**: Instructions apply globally (like "always on" rules)
- **Subdirectories**: Instructions apply only to files in that directory tree

**Advantages over Rules:**
- Location-based scoping without configuration
- Version-controlled with your code
- No special frontmatter required

### 2.4 Rules and Workflows [VERIFIED]

**Rules** - Persistent context at prompt level
- Storage: `.windsurf/rules/` directory
- Activation modes: Manual (`@mention`), Always On, Model Decision, Glob-based
- Limit: 12000 characters per rule file

**Workflows** - Structured sequence of steps at trajectory level
- Storage: `.windsurf/workflows/` directory
- Invoke via `/workflow-name` command
- Can call other workflows from within a workflow
- Limit: 12000 characters per workflow file

### 2.5 Built-in Cascade Features

**Real-time Awareness**: Cascade sees your manual edits in real-time

**Plans and Todo Lists**: Built-in planning agent continuously refines long-term plan

**Named Checkpoints**: Create snapshots to revert to specific states

**Queued Messages**: Queue messages while Cascade is working

**Send Problems to Cascade**: Click "Send to Cascade" button in Problems panel

## 3. Spec Driven Development with Cascade

### The Core Idea [VERIFIED]

Instead of "code first, docs later", start with a specification that becomes the source of truth. The spec drives implementation, tests, and validation.

**Why it works better with AI:**
- Vague prompts force AI to guess at thousands of unstated requirements
- Clear specs give the AI deterministic targets to implement against
- Separates stable "what" from flexible "how"

### The 4-Phase Process (GitHub Spec Kit Pattern)

**Phase 1: Specify** - Create `requirements.md`
- Focus on user journeys and experiences, not technical details
- Define: Who uses it? What problem does it solve? What outcomes matter?
- Format: User stories with acceptance criteria
```
As a [user], I want [goal] so that [benefit]
WHEN [condition] THEN the system SHALL [expected behavior]
```

**Phase 2: Plan** - Generate `plan.md`
- Provide: stack, architecture, constraints, compliance requirements
- AI generates detailed technical plan respecting constraints
- Can request multiple plan variations to compare approaches
- Create checkpoint here - save plan before implementation

**Phase 3: Tasks** - Break down into `tasks.md`
- AI generates small, reviewable chunks
- Each task: specific, testable in isolation, linked to requirements
- Format: Enumerated list with checkboxes, grouped into phases
```markdown
## Phase 1: Setup
- [ ] Task 1.1: Create data repository
- [ ] Task 1.2: Set up authentication

## Phase 2: Core Features
- [ ] Task 2.1: Implement user registration endpoint
```

**Phase 4: Implement** - Execute tasks
- Work in phases, not "do everything at once"
- Mark tasks complete in `tasks.md` as they finish
- Review after each phase before proceeding
- Agent knows WHAT to build (spec), HOW (plan), and WHAT to work on (tasks)

### Best Practices for Execution [VERIFIED]

- **Work in phases**: "Complete tasks 1-2 from tasks.md and mark them as completed"
- **Mark progress**: Require agent to update tasks.md with checkmarks
- **Review after each phase**: Run tests, confirm correctness before next phase
- **Control pacing**: If task reveals complexity, update task list first

### Prompt Template for Spec-Driven Setup

```
Read the contents of requirements.md and create a detailed development plan.
The plan should include:
- A short overview of the goal
- The main steps or phases required
- Any dependencies, risks, or considerations
Do not write or modify any code yet.
Save the plan as plan.md.
```

## 4. Maximizing Code Quality and Bugfree Implementations

### 4.1 The "Explore, Plan, Code, Commit" Workflow [VERIFIED]

1. **Explore**: Ask agent to read relevant files, explicitly tell it NOT to code yet
2. **Plan**: Ask agent to make a plan. Use "think hard" for extended thinking mode
3. **Implement**: Ask agent to implement its solution, verify reasonableness
4. **Commit**: Ask agent to commit and create PR, update docs

**Key insight:** Steps 1-2 are crucial. Without them, AI jumps straight to coding.

### 4.2 Test-Driven Development (TDD) Pattern [VERIFIED]

This is the most effective pattern for verifiable changes:

1. Ask agent to write tests based on expected input/output pairs
2. Tell agent to run tests and confirm they FAIL (no implementation yet)
3. Commit the tests
4. Ask agent to write code that passes tests (don't modify tests)
5. Agent iterates: write code -> run tests -> adjust -> repeat until pass
6. Verify implementation isn't overfitting to tests (use /clear and fresh review)
7. Commit the code

**Why it works:** Agent has a clear target to iterate against. Can make changes, evaluate results, and incrementally improve.

### 4.3 Multi-Agent Verification Pattern [VERIFIED]

Have separate agents for writing and reviewing:

1. Agent A writes code
2. Clear context or start Agent B in another terminal
3. Agent B reviews Agent A's work
4. Agent C (or clear again) reads both code and review, makes edits

**Variations:**
- Agent A writes tests, Agent B writes implementation
- Agents communicate via shared scratchpad files

### 4.4 Checklist and Scratchpad Pattern [VERIFIED]

For large tasks with many steps:

1. Tell agent to run lint/build command and write all errors to a markdown checklist
2. Instruct agent to address each issue one by one
3. Fix and verify each before checking off and moving to next

**Example prompt:**
```
Run the lint command and write all resulting errors (with filenames and line numbers) 
to a Markdown checklist. Then address each issue one by one, fixing and verifying 
before checking it off and moving to the next.
```

### 4.5 Visual Iteration Pattern [VERIFIED]

For UI work:

1. Give agent a way to take browser screenshots (Playwright MCP)
2. Provide visual mock (image file or pasted screenshot)
3. Ask agent to implement design, take screenshots, iterate until matches mock
4. Commit when satisfied

**Key insight:** Like humans, AI outputs improve significantly with iteration. First version might be good, after 2-3 iterations typically much better.

### 4.6 General Best Practices

**Be specific**: Specificity leads to better alignment. "Add a user login page with email/password fields and a forgot password link" vs "add login"

**Course correct early**: Press Escape to interrupt and redirect. Don't wait until agent finishes wrong approach.

**Use /clear frequently**: Reset context between tasks to avoid distraction from irrelevant history.

**Give visual targets**: Tests, mocks, or other output targets improve iteration quality.

**Verify independently**: For complex implementations, use /clear and do a fresh review, or open a separate Cascade panel.

## 5. Sources and References

### Official Documentation
- Windsurf Cascade Overview: https://docs.windsurf.com/windsurf/cascade/cascade
  - Primary findings: 20 tool calls per prompt, Auto-Continue setting, Turbo Mode, queued messages
- MCP Integration: https://docs.windsurf.com/windsurf/cascade/mcp
  - Primary findings: MCP config location, 100 tool limit, stdio/HTTP/SSE transports
- Workflows: https://docs.windsurf.com/windsurf/cascade/workflows
  - Primary findings: 12000 char limit, `/workflow-name` invocation, can nest workflows
- Memories & Rules: https://docs.windsurf.com/windsurf/cascade/memories
  - Primary findings: 4 activation modes, rules auto-discovered from .windsurf/rules/

### MCP Servers
- Playwright MCP (Microsoft): https://github.com/microsoft/playwright-mcp
  - Primary findings: Uses accessibility tree (no vision), supports Windsurf natively
- MCP Server Reference: https://github.com/modelcontextprotocol/servers
- OpenTools Directory: https://opentools.com/

### Spec-Driven Development
- GitHub Spec Kit: https://github.com/github/spec-kit
  - Primary findings: 4-phase process (specify/plan/tasks/implement), CLI tool available
- GitHub Blog - Spec-driven development: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
  - Primary findings: Spec as source of truth, iterative refinement, works across AI tools
- JetBrains Blog - Spec-driven approach: https://blog.jetbrains.com/junie/2025/10/how-to-use-a-spec-driven-approach-for-coding-with-ai/
  - Primary findings: requirements.md -> plan.md -> tasks.md pattern, phase-based execution

### Agentic Coding Best Practices
- Anthropic - Claude Code Best Practices: https://www.anthropic.com/engineering/claude-code-best-practices
  - Primary findings: TDD pattern, multi-agent verification, checklists/scratchpads, explore-plan-code-commit

### Community Discussion
- Reddit r/windsurf - Auto-continue discussion: https://www.reddit.com/r/windsurf/comments/1lul3j5/can_i_make_it_continue_automatically_without_the/
  - Primary findings: No fully autonomous mode like Gemini CLI, Auto-Continue helps but not complete solution
