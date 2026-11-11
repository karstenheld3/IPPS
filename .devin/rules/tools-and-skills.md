---
trigger: always_on
---

# Tools and Skills

Tool-specific knowledge and disambiguation.

## Browser Automation

- **Playwright MCP** - Microsoft's MCP server. Spawns fresh browser instance (clean session, no existing logins). `npx @playwright/mcp@latest`. Procedures: @skills:ms-playwright-mcp

## Workflow-First Rule

Before executing any multi-step operation (file processing, deployment, transcription, email):

1. Search `[WORKFLOWS]` for applicable workflow: file type, action verb, or domain
2. Search `[SKILLS]` for applicable skill
3. **If workflow/skill exists**: MUST follow it step-by-step. No improvisation, no shortcuts.
4. **If not found**: Proceed with best judgment

Before installing Python or PowerShell modules: Check existing skills and workflows for established dependencies, venvs, and tool preferences first.

Violation = automatic CRITICAL in FAILS.md. No exceptions.

## Workflow Reference

Workflows are `[AGENT_FOLDER]/workflows/[name].md`, called as `/[name]`. The frontmatter `description` of each file states its purpose; read the file before executing it.

- **Context and session**: `/prime`, `/session-new`, `/session-load`, `/session-save`, `/session-finalize`, `/session-archive`
- **Execution**: `/go`, `/implement`, `/test`, `/fix`, `/bugfix`, `/investigate`
- **Planning documents**: `/write-info`, `/write-spec`, `/write-impl-plan`, `/write-test-plan`, `/write-tasks-plan`, `/write-strut`, `/write-prompts`, `/write-template`
- **Publishing documents**: `/propose-article`, `/draft-article`, `/write-article`, `/propose-report`, `/draft-report`, `/write-report`, `/propose-ebook`, `/draft-ebook`, `/write-ebook`
- **Quality**: `/verify`, `/critique`, `/fact-check`, `/reconcile`, `/improve`, `/drift-detect`, `/drift-correct`
- **Research and analysis**: `/research`, `/deep-research`, `/research-program`, `/analyze`, `/pattern-detect`, `/hypothesize`, `/validate`
- **Content processing**: `/transcribe`, `/translate`, `/render`, `/ascii-diagram`, `/conversation-start`, `/conversation-update`, `/conversation-draft`
- **Repository and workspace**: `/commit`, `/sync`, `/deploy`, `/project-release`, `/rename`, `/remove`, `/cleanup`, `/workspace-setup`, `/compare-workspace-setup`, `/switch-model`
- **Learning**: `/fail`, `/learn`

## Quality Pipelines

**Verify-Critique-Reconcile-Implement-Verify (VCRIV)** - logic and design review:
`/verify` → `/critique` → `/reconcile` → `/implement` → `/verify`

**Fact-check-Reconcile-Implement-Verify (FACRIV)** - factual claim verification:
`/fact-check` → `/reconcile` → `/implement` → `/verify`

**Roles:** `/critique` and `/fact-check` = JUDGE (produce `*_CRITIQUE.md` / `*_FACT-CHECK.md` only, never modify originals). `/reconcile` = TRIAGE (chat output only). `/implement` = EXECUTOR (applies approved corrections to source documents).

**Rules:** Sequential execution. When user says "run VCRIV" or "run FACRIV", execute full pipeline in order.

## Prompt Templates in NOTES.md

Workflow calls (`/deep-research`, `/go`, `/verify`, etc.) MUST be standalone lines inside fenced prompt blocks; a call buried in a sentence (`... context ... /deep-research`) is not recognized. BAD/GOOD examples: @skills:write-documents `PROMPTS_RULES.md` PRMT-CT-08

## Skill Registry

Skills are in `[AGENT_FOLDER]/skills/`. Each has a `SKILL.md` with usage instructions. The agent MUST discover available skills by listing the `[AGENT_FOLDER]/skills/` directory and reading each `SKILL.md` frontmatter `description` field. Do not rely on a hardcoded list - skills may be added, removed, or customized per workspace.

## Tool Locations

Executable tools outside the workspace:

- **Python venv**: `[WORKSPACE_FOLDER]/../.tools/llm-venv/Scripts/python.exe`
- **processkit** (supervisor for `run-supervised.ps1`): `[WORKSPACE_FOLDER]/../.tools/llm-venv/Scripts/processkit.exe` - install: `pip install processkit-py==1.5.0` into the venv (version tested in HANGBENCH)
- **API keys**: `[WORKSPACE_FOLDER]/../.tools/.api-keys.txt` (default; override in session or workspace NOTES.md)
- **Poppler** (PDF): `[WORKSPACE_FOLDER]/../.tools/poppler/Library/bin/`
- **Ghostscript**: `[WORKSPACE_FOLDER]/../.tools/gs/bin/`
- **QPDF**: `[WORKSPACE_FOLDER]/../.tools/qpdf/bin/`
- **7-Zip**: `[WORKSPACE_FOLDER]/../.tools/7z/`
- **ImageMagick**: `[WORKSPACE_FOLDER]/../.tools/magick/`
- **gogcli config**: `[WORKSPACE_FOLDER]/../.tools/gogcli-client-secret.json`

## Chat Output

The Devin / Cascade chat panel renders a backticked workspace-relative path as a clickable chip.

- Deliverables first: when the request produces files (documents, prompts, code, reports), the final message starts with a `Deliverables` list, before method, decisions, and details. One bullet per main output file (the files [ACTOR] asked for or must open next): clickable path + 5-10 word purpose. One `Next step` line follows (e.g. the command or prompt to run). Helper, tracking, and scratch files: one short `Also changed` line, or omitted. Keep the rest short; no long "What I created" inventories
- Clickable paths (EVERY message that names a file, including answers to "where is the file"): one path per bullet, inline single backticks, workspace-relative, forward slashes, e.g. - `docs/guides/_PROMPTS_01-Example.md` - purpose. Never in fenced code blocks, never a bare absolute `[DRIVE]:\` path, never `file:///` links: all render as plain text. File outside the workspace root: state that and give the absolute path in inline backticks. State the file's session or folder in the purpose when it differs from the file the user has open

## Large File Writes

- If a single file write exceeds ~4000 tokens, MUST split it into multiple smaller edits (e.g., create file with first part, append remaining parts via follow-up edits)
- Reason: large single writes frequently fail, forcing re-generation of the entire content. Smaller edits fail less and cost less to retry
- If a multi-edit tool is available, prefer it: multiple small edits in one tool call are more reliable than one large write
- The agent-specific rule file may override this section in its section Tool-Call Payload Limit
- This section (or the agent-specific override) is the single source for agent-tool limits. Prompt sequences copy it verbatim into the robustness card `## Agent tool limits` (PRMT-HS-11); prompts never restate token numbers

## Batch Operations

- Before processing multiple files: run `tool --help` or read source, execute on a single file first, verify output location and format, then scale to full batch
- Use absolute paths (PowerShell jobs lose relative context) and non-blocking execution for parallel tasks
- Run every non-whitelisted command through the supervised runner (`agent-behavior.md` Terminal Hang Prevention)
- After first job completes, verify output before assuming rest will succeed

## Long-Running Commands (over 60 seconds)

Applies to git filter-repo, full-repo gc/repack, mass file operations, pip/npm installs, large downloads - anything expected to run over 60 seconds. Step numbers refer to `agent-behavior.md` Terminal Hang Prevention.

- Before starting: state the estimated duration to the user and that the terminal will appear busy meanwhile. A silent multi-minute command is indistinguishable from a hang
- Repo-wide operations (filter-repo, gc, reflog expire) end with reset --hard + reflog expire + gc: check for concurrent activity first (running git/python processes via Get-Process, non-empty `git status`, other active sessions committing to the same repo). Never run while another session works in the repo
- Run through the supervised runner. The runner sets no time limit: a long run that shows progress is never ended
- During execution: do not poll with fixed waits and no new information. Read the runner `_log.txt` (`ALIVE` lines: CPU time, output size) and `_out.txt` between waits; output is live (the runner sets `PYTHONUNBUFFERED`). End the command only on a hang verdict (step 5)
- After canceling or completing: verify the process is dead. A canceled step leaves the process tree running in the background; its line stays in `_agentwork/.tmp_kill_[TOPIC].ps1` (step 8)
- After history rewrites: verify HEAD, refs, `git status`, and worktree content before any push
