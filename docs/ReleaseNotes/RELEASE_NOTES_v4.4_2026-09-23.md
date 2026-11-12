# Release Notes: v4.4 (2026-09-23)

## Summary

This release covers work from 2026-09-10 to 2026-09-23, spanning 90 commits across PromptSystemV4.4. Major themes: Claude Code as fully supported agent (generated `.claude/` deployment), DevSystem → PromptSystem rename, GRUC formalization with ASCII diagram workflow, workspace document placement rules, and prompt sequence robustness rules.

## Changes Since v4.3

### New Workflows

- **ascii-diagram** - ASCII/Unicode diagram creation and fixing with guides, checks, and helper script

### Claude Code Support (Major)

- **`_PROMPTS_UpdateClaude.md`** - 7-prompt idempotent deployment sequence generating the full `.claude/` deployment
- **`.claude/rules/`** - 7 agent-agnostic rule files (8 source rules minus Devin-specific `devin.md`)
- **`.claude/skills/`** - 71 skills: 48 workflow skills (user-only, `disable-model-invocation: true`, zero context cost) + 23 domain skills (model-invocable)
- **`verify` → `ipps-verify`** - avoids collision with the bundled Claude Code `/verify` skill
- **Devin-specific items excluded** - `switch-model` workflow, `devin-auto-model-switcher` skill (Claude Code has native `/model`)
- **Agent-agnostic content** - `[AGENT_FOLDER]` placeholder across rules, workflows, skills; MCP setup instructions branch per agent (Devin JSON config, Claude Code `claude mcp add` / `.mcp.json`)
- **`ClaudeCode.bat`** - launcher script
- **Documentation** - `Docs/_INFO_HOW_CLAUDE_CODE_WORKS.md` (CLCD-IN01) refreshed with archived predecessor; `Docs/_INFO_HOW_TO_USE_IPPS_WITH_CLAUDE_CODE.md` (CLCD-IN02) added; README "Supported Agents" section

### Renames

- **DevSystem → PromptSystem** across the entire codebase
- **deep-research skill → research-methods** (the `/deep-research` workflow keeps its name)
- **drift-correction → drift-control**
- **windsurf-auto-model-switcher → devin-auto-model-switcher**
- **critique and fact-check** review output files renamed

### GRUC Formalization

- **write-documents**: GRUC structure (GUIDE, RULES, CHECKS) with separation preventing self-gaming
- **ASCII art guides** - diagram rules for trees, flows, boxes, UI mockups
- **write-prompts**: effort parameters, position markers, hang-safety

### Prompt Sequence Robustness

- New rules: PRMT-CT-12/13/14, PRMT-HS-09/10, PRMT-SQ-04 (interleaved verification), PRMT-FT-10 (plan summary), PRMT-EX-03, PRMT-NM-03 (numbered prompt filenames)
- Prompt Markers required for all prompt counts

### Workspace Management

- **Document placement rules WS-DP-01 through WS-DP-06** - two-tier folder enforcement, `docs/` folder added to workspace structure
- **18 INFO documents migrated** from `specs/` to `docs/` per WS-DP-02
- **promptsystem-sync.json targets-based schema** - per-target include/exclude/never_overwrite, `sync.ps1` rewritten
- FR-76/77/78 document placement rules

### Rules

- **devin.md** - agent-specific rules extracted from `tools-and-skills.md` (model switching, terminal limits, skill registry)
- **agent-behavior.md** - `ask_user_question` prohibition, batch operation rules, workspace file placement
- **coding-conventions** - test rules restructured into dedicated files
- **core-conventions** - document rule exceptions (opt-in Markdown tables, emoji whitelist)

### LLM Evaluation

- **find-workers-limit.py**: Z.AI provider support (`glm-` prefix), `--start-workers`, prompt caching (Anthropic explicit `cache_control`, OpenAI/Z.AI automatic `cached_tokens`), 4 pre-existing bugs fixed
- Burst capacity results documented: OpenAI/Anthropic safe at 100 workers, Z.AI stable at 72

### Specs

- `_SPEC_ASCII_DIAGRAM_WORKFLOW.md` - ASCII diagram workflow specification
- `_SPEC_IPPS_KNOWLEDGE_BUNDLE_FORMAT` - knowledge bundle format (IPPSKBNDL topic)
- `_SPEC_RELEASE_PROJECT_WORKFLOW.md` - `github_release_confirm` config key

### Infrastructure

- **`check_workflow_refs.ps1`** - broken workflow reference detection (mandatory pre-release gate)
- **IDE launcher scripts** - standardized workspace file naming
- **IPPS gap analysis** - reusable gap analysis template

## Sessions

### _2026-09-12_GRUCFormalize

**Goal**: GRUC formalization, write-prompts effort parameters, ASCII art diagram workflow

### _2026-09-12_IPPSGapAnalysis

**Goal**: IPPS gap analysis with preflight analysis, STRUT plan, prompt files, and reusable template

## Statistics

- **Commits since v4.3**: 90
- **Files changed**: 3771 (includes deployment mirrors and version archives)
- **Lines added**: 289956
- **Lines deleted**: 3688
- **New workflows**: 1 (ascii-diagram)
- **Renamed skills**: 3 (research-methods, drift-control, devin-auto-model-switcher)
- **Deployment targets**: 2 (`.devin/` robocopy mirror, `.claude/` prompt-generated)
- **Date range**: 2026-09-10 to 2026-09-23

## Document History

**[2026-09-23 17:00]**
- Initial release notes created
