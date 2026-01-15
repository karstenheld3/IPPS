# IPPS - Insanely Productive Programming System

A development system for AI-assisted coding workflows, optimized for Windsurf IDE on Windows x64.

## Table of Contents

- [Overview](#overview)
- [How to Add to Your Project](#how-to-add-to-your-project)
- [DevSystem Versions](#devsystem-versions)
- [Key Conventions](#key-conventions)
- [Agent Tools](#agent-tools-installed-automatically-by-skill)
- [Project Structure](#project-structure)
- [Skills](#skills)
- [File Naming Conventions](#file-naming-conventions)
- [Usage Examples](#usage-examples)
- [Agent Compatibility](#agent-compatibility)

## Overview

IPP provides structured rules, workflows, and skills for AI agents to follow consistent conventions during pair programming sessions. The system manages sessions, documents, commits, and tool installations.

## How to Add to Your Project

Copy the `.windsurf/` folder to your VS Code or Windsurf workspace root:
```
your-project/
└── .windsurf/
    ├── rules/
    ├── workflows/
    └── skills/
```

## DevSystem Versions

- **[DevSystemV1](DevSystemV1/)** - Legacy system using rules and workflows
- **[DevSystemV2](DevSystemV2/)** - Current system with modular skills and workflows

## Key Conventions

- [Core Conventions](DevSystemV2/rules/core-conventions.md) - Text formatting, document structure, header blocks
- [DevSystem Core](DevSystemV2/rules/devsystem-core.md) - Workspace scenarios, folder structure, workflow reference
- [DevSystem IDs](DevSystemV2/rules/devsystem-ids.md) - Document IDs, topic registry, tracking IDs
- [Git Conventions](DevSystemV2/skills/git-conventions/SKILL.md) - Commit message format, .gitignore rules
- [Coding Conventions](DevSystemV2/skills/coding-conventions/SKILL.md) - Python, PowerShell style rules

## Agent Tools (installed automatically by skill)

Local tool installations in `.tools/` (gitignored). Run `SETUP.md` in each skill folder to install.

**pdf-tools** ([SETUP](DevSystemV2/skills/pdf-tools/SETUP.md)) - Enables agent to read entire PDFs by converting pages to JPG images for vision analysis:
- **7-Zip** (`.tools/7z/`) - Archive extraction, NSIS installer unpacking
- **Poppler** (`.tools/poppler/`) - PDF to image, text extraction, split/merge
- **QPDF** (`.tools/qpdf/`) - PDF manipulation, optimization, repair
- **Ghostscript** (`.tools/gs/`) - PDF compression, image downsampling

**github** ([SETUP](DevSystemV2/skills/github/SETUP.md)):
- **GitHub CLI** (`.tools/gh/`) - Repos, issues, PRs, releases

Run `SETUP.md` in each skill folder to install required tools locally to `.tools/`.

## Project Structure

```
IPP/
├── .tools/                       # Local tool installations (gitignored)
│   ├── poppler/                  # PDF to image conversion
│   ├── qpdf/                     # PDF manipulation
│   ├── gs/                       # Ghostscript PDF compression
│   ├── 7z/                       # Archive extraction
│   └── gh/                       # GitHub CLI
├── .windsurf/                    # Windsurf agent configuration (active)
│   ├── rules/                    # Rules (copied from DevSystemVX for testing)
│   ├── workflows/                # Workflows (copied from DevSystemVX)
│   └── skills/                   # Skills (copied from DevSystemVX)
├── DevSystemV1/                  # Legacy system (deprecated)
│   ├── rules/
│   │   ├── devsystem-rules.md
│   │   ├── document-rules.md
│   │   ├── git-rules.md
│   │   ├── proper-english-rules.md
│   │   ├── python-rules.md
│   │   ├── tools-rules.md
│   │   └── workspace-rules.md
│   └── workflows/
│       ├── commit.md
│       ├── go-autonomous.md
│       ├── go-research.md
│       ├── implement.md
│       ├── prime.md
│       ├── session-archive.md
│       ├── session-close.md
│       ├── session-init.md
│       ├── session-resume.md
│       ├── session-save.md
│       ├── setup-pdftools.md
│       ├── verify.md
│       ├── write-impl-plan.md
│       ├── write-spec.md
│       └── write-test-plan.md
├── DevSystemV2/                  # Current system
│   ├── rules/
│   │   ├── core-conventions.md   # Text formatting, document structure
│   │   ├── devsystem-core.md     # Workspace scenarios, folder structure
│   │   ├── devsystem-ids.md      # Document and item ID conventions
│   │   └── workspace-rules.md    # Project-specific rules
│   ├── skills/
│   │   ├── coding-conventions/   # Python, PowerShell style rules
│   │   ├── git-conventions/      # Commit message format
│   │   ├── github/               # GitHub CLI (SETUP.md, SKILL.md)
│   │   ├── pdf-tools/            # PDF scripts and tools
│   │   ├── session-management/   # Session templates
│   │   └── write-documents/      # Spec, impl, test templates
│   └── workflows/
│       ├── commit.md             # Git commit workflow
│       ├── go-autonomous.md      # Autonomous implementation
│       ├── go-research.md        # Structured research
│       ├── implement.md          # Implementation workflow
│       ├── prime.md              # Context loading workflow
│       ├── session-archive.md    # Archive session folder
│       ├── session-close.md      # Close and sync session
│       ├── session-init.md       # Initialize new session
│       ├── session-resume.md     # Resume existing session
│       ├── session-save.md       # Save session progress
│       ├── setup-pdftools.md     # PDF tools installation
│       ├── sync.md               # Document synchronization (NEW)
│       ├── verify.md             # Verification workflow
│       ├── write-impl-plan.md    # Create implementation plan
│       ├── write-spec.md         # Create specification
│       └── write-test-plan.md    # Create test plan
└── README.md
```

## Skills

- **pdf-tools** - PDF conversion, compression, analysis using Ghostscript, Poppler, QPDF
- **github** - GitHub CLI operations (repos, issues, PRs)
- **session-management** - Session init, save, resume, close workflows
- **write-documents** - Spec, impl, test, info document templates

## File Naming Conventions

IPPS uses special prefixes to control how files are processed:

- **`!` prefix** - Priority files (e.g., `!NOTES.md`). Read first during `/prime`. Contains critical project information.
- **`_` prefix** - Ignored by automatic workflows (e.g., `_SPEC_*.md`, `_PrivateSessions/`). Used for session-specific, WIP, or archived content.
- **`.` prefix** - Hidden files following Unix convention (e.g., `.windsurf/`, `.gitignore`).

## Usage Examples

### Prime Context

Load workspace context before starting work:
```
/prime
```

The prime workflow:
1. Finds and reads all `!*.md` files (priority documentation)
2. Finds and reads standard `.md` files (excluding `_` and `!` prefixed)
3. Detects workspace scenario (project structure, version strategy, work mode)
4. Reports summary: files read, scenario detected

### Session Workflows

Start a new work session:
```
/session-init
```
Creates a session folder with NOTES.md, PROBLEMS.md, PROGRESS.md.

Save progress during work:
```
/session-save
```

Resume an existing session:
```
/session-resume
```

Close session and sync findings:
```
/session-close
```

### Document Cycle (INFO -> SPEC -> IMPL -> TEST)

1. **Research** - Gather information:
```
/go-research
```
Creates `_INFO_*.md` with findings.

2. **Specify** - Create specification:
```
/write-spec
```
Creates `_SPEC_*.md` from requirements.

3. **Plan** - Create implementation plan:
```
/write-impl-plan
```
Creates `_IMPL_*.md` from spec.

4. **Test Plan** - Create test plan:
```
/write-test-plan
```
Creates `_TEST_*.md` from spec.

5. **Implement** - Execute the plan:
```
/implement
```

6. **Verify** - Check work against specs:
```
/verify
```

7. **Sync** - Update dependent documents:
```
/sync
```

8. **Commit** - Create conventional commits:
```
/commit
```

## Agent Compatibility

IPPS concepts map to other AI coding agents with different folder structures:

### Claude Code

- **Rules**: `CLAUDE.md` in repo root (or `~/.claude/CLAUDE.md` for global)
- **Commands**: `.claude/commands/*.md` (invoked as `/project:command-name`)
- **Skills**: `.claude/skills/<name>/SKILL.md`
- **MCP Config**: `.mcp.json` in repo root

```
your-project/
├── CLAUDE.md              # Rules (auto-loaded)
├── .claude/
│   ├── commands/          # Slash commands
│   │   └── fix-issue.md   # -> /project:fix-issue
│   └── skills/
│       └── my-skill/
│           └── SKILL.md   # Agent skill
└── .mcp.json              # MCP servers
```

### OpenAI Codex CLI

- **Rules**: `AGENTS.md` in repo root (or `~/.codex/AGENTS.md` for global)
- **Override**: `AGENTS.override.md` takes precedence over `AGENTS.md`
- **Commands**: Not supported (use inline prompts)
- **Skills**: Not supported natively

```
your-project/
├── AGENTS.md              # Project instructions
├── services/
│   └── payments/
│       └── AGENTS.override.md   # Directory-specific override
```

### GitHub Copilot

- **Rules**: `.github/copilot-instructions.md` (repository-wide)
- **Path-specific**: `.github/instructions/*.instructions.md` with `applyTo` glob
- **Prompt files**: `.github/prompts/*.prompt.md` (reusable prompts)
- **Commands/Skills**: Not supported

```
your-project/
├── .github/
│   ├── copilot-instructions.md        # Repository-wide rules
│   ├── instructions/
│   │   ├── python.instructions.md     # applyTo: "**/*.py"
│   │   └── tests.instructions.md      # applyTo: "**/test_*.py"
│   └── prompts/
│       └── review.prompt.md           # Reusable prompt
```

### Feature Comparison

- **Windsurf**: Rules + Workflows + Skills + MCP
- **Claude Code**: CLAUDE.md + Commands + Skills + MCP
- **Codex CLI**: AGENTS.md only (hierarchical, directory-scoped)
- **Copilot**: Instructions + Path patterns + Prompt files

### Deploying DevSystem Files

To use IPPS with other agents, copy relevant content:

- **Claude Code**: Copy `.windsurf/rules/` content to `CLAUDE.md`, workflows to `.claude/commands/`
- **Codex CLI**: Merge rules into `AGENTS.md` (no workflow/skill support)
- **Copilot**: Copy rules to `.github/copilot-instructions.md` (no workflow/skill support)
