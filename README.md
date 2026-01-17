<DevSystem MarkdownTablesAllowed=true EmojisAllowed=true />

# IPPS - Insanely Productive Programming System

A development system for AI-assisted coding workflows, optimized for Windsurf IDE on Windows x64.

## Table of Contents

- [Overview](#overview)
- [How to Add to Your Project](#how-to-add-to-your-project)
- [DevSystem Versions](#devsystem-versions)
- [Agentic English](#agentic-english)
- [EDIRD Phase Model](#edird-phase-model)
- [Key Conventions](#key-conventions)
- [Agent Tools](#agent-tools-installed-automatically-by-skill)
- [Project Structure](#project-structure)
- [Skills](#skills)
- [File Naming Conventions](#file-naming-conventions)
- [Usage Examples](#usage-examples)
- [Agent Compatibility](#agent-compatibility)

## Overview

IPPS provides structured rules, workflows, and skills for AI agents to follow consistent conventions during pair programming sessions. The current version (V3) introduces the EDIRD phase model and Agentic English vocabulary for deterministic agent behavior.

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
- **[DevSystemV2](DevSystemV2/)** - Previous version with modular skills and workflows
- **[DevSystemV2.1](DevSystemV2.1/)** - Previous version with refined workflows
- **[DevSystemV3](DevSystemV3/)** - Current system with EDIRD phase model and Agentic English

## Agentic English

A controlled vocabulary for agent-human communication. Provides consistent terminology across all workflows.

**Goal**: Eliminate ambiguity in agent instructions by using bracketed verbs, placeholders, and labels.

**Rationale**: Agents interpret natural language inconsistently. Agentic English provides deterministic instructions that agents can reliably parse and execute.

**Syntax**:
- `[VERB]` - Action to execute (e.g., `[RESEARCH]`, `[VERIFY]`, `[IMPLEMENT]`)

**Extensibility**: Verbs are abstract concepts. Complex verbs CAN be concretized as dedicated workflows (e.g., `[COMMIT]` → `/commit`), but this is optional. Simple verbs work inline within phase workflows.
- `[PLACEHOLDER]` - Value to substitute (e.g., `[ACTOR]`, `[WORKSPACE_FOLDER]`)
- `[LABEL]` - Classification to apply (e.g., `[UNVERIFIED]`, `[CRITICAL]`)
- Context states use NO brackets: `COMPLEXITY-HIGH`, `HOTFIX`, `SINGLE-PROJECT`

**Example workflow instruction**:
```
1. [RESEARCH] affected code in [SRC_FOLDER]
2. [CONSULT] with [ACTOR] if unclear
3. [IMPLEMENT] changes
4. [VERIFY] against spec
5. [COMMIT] with conventional message
```

**Full specification**: [SPEC_AGEN_AGENTIC_ENGLISH.md](SPEC_AGEN_AGENTIC_ENGLISH.md)

## EDIRD Phase Model - Explore, Design, Implement, Refine, Deliver

A 5-phase workflow model for both BUILD (code) and SOLVE (knowledge/decisions) work.

**Goal**: Consistent phase structure for all development work with deterministic next-action logic. We want the agent to always do the right thing when the `/next` workflow / command is executed until the initial goal is reached.

**Rationale**: Without phases, agents skip important steps or apply heavyweight processes to simple tasks. EDIRD provides the right amount of process for each complexity level.

**Phases**:
- **EXPLORE** - Understand before acting: `[RESEARCH]`, `[ANALYZE]`, `[ASSESS]`, `[SCOPE]`
- **DESIGN** - Plan before executing: `[PLAN]`, `[WRITE-SPEC]`, `[PROVE]`, `[DECOMPOSE]`
- **IMPLEMENT** - Execute the plan: `[IMPLEMENT]`, `[TEST]`, `[FIX]`, `[COMMIT]`
- **REFINE** - Improve quality: `[REVIEW]`, `[VERIFY]`, `[CRITIQUE]`, `[RECONCILE]`
- **DELIVER** - Complete and hand off: `[VALIDATE]`, `[MERGE]`, `[DEPLOY]`, `[CLOSE]`

**Complexity mapping**:
- `COMPLEXITY-LOW` → patch version (single file, clear scope)
- `COMPLEXITY-MEDIUM` → minor version (multiple files, backward compatible)
- `COMPLEXITY-HIGH` → major version (breaking changes, architecture)

**Operation Modes**:
- `IMPL-CODEBASE` (default) → Output to project source folders
- `IMPL-ISOLATED` → Output to `[SESSION_FOLDER]/` only (for POCs, prototypes)

**Example BUILD flow**:
```
[EXPLORE] → [ASSESS] complexity → Gate check
[DESIGN] → [WRITE-SPEC] → [PROVE] risky parts → Gate check
[IMPLEMENT] → [IMPLEMENT]→[TEST]→[FIX]→green→next → Gate check
[REFINE] → [VERIFY] against spec → [CRITIQUE] if MEDIUM+ → Gate check
[DELIVER] → [COMMIT] → [MERGE]
```

**Full specification**: [SPEC_EDIRD_PHASE_MODEL.md](SPEC_EDIRD_PHASE_MODEL.md)

## Key Conventions

- [Core Conventions](DevSystemV3/rules/core-conventions.md) - Text formatting, document structure, header blocks
- [DevSystem Core](DevSystemV3/rules/devsystem-core.md) - Workspace scenarios, folder structure, workflow reference
- [DevSystem IDs](DevSystemV3/rules/devsystem-ids.md) - Document IDs, topic registry, tracking IDs
- [Agentic English](DevSystemV3/rules/agentic-english.md) - Controlled vocabulary for agent instructions
- [Git Conventions](DevSystemV3/skills/git-conventions/SKILL.md) - Commit message format, .gitignore rules
- [Coding Conventions](DevSystemV3/skills/coding-conventions/SKILL.md) - Python, PowerShell style rules

## Agent Tools (installed automatically by skill)

Local tool installations in `.tools/` (gitignored). Run `SETUP.md` in each skill folder to install.

**pdf-tools** ([SETUP](DevSystemV2.1/skills/pdf-tools/SETUP.md)) - Enables agent to read entire PDFs by converting pages to JPG images for vision analysis:
- **7-Zip** (`.tools/7z/`) - Archive extraction, NSIS installer unpacking
- **Poppler** (`.tools/poppler/`) - PDF to image, text extraction, split/merge
- **QPDF** (`.tools/qpdf/`) - PDF manipulation, optimization, repair
- **Ghostscript** (`.tools/gs/`) - PDF compression, image downsampling

**github** ([SETUP](DevSystemV2.1/skills/github/SETUP.md)):
- **GitHub CLI** (`.tools/gh/`) - Repos, issues, PRs, releases

Run `SETUP.md` in each skill folder to install required tools locally to `.tools/`.

## Project Structure

```
IPPS/
├── .tools/                       # Local tool installations (gitignored)
├── .windsurf/                    # Active agent configuration (copied from DevSystemV3)
│   ├── rules/
│   ├── workflows/
│   └── skills/
├── DevSystemV1/                  # Legacy (deprecated)
├── DevSystemV2/                  # Legacy (deprecated)
├── DevSystemV2.1/                # Legacy (deprecated)
├── DevSystemV3/                  # Current system
│   ├── rules/
│   │   ├── core-conventions.md   # Text formatting, document structure
│   │   ├── devsystem-core.md     # Workspace scenarios, folder structure, operation modes
│   │   ├── devsystem-ids.md      # Document and item ID conventions
│   │   ├── agentic-english.md    # Controlled vocabulary for agent instructions
│   │   └── edird-core.md         # EDIRD phase model core rules
│   ├── skills/
│   │   ├── coding-conventions/   # Python, PowerShell style rules
│   │   ├── edird-phase-model/    # Phase gates, flows, branching
│   │   ├── git-conventions/      # Commit message format
│   │   ├── github/               # GitHub CLI operations
│   │   ├── pdf-tools/            # PDF scripts and tools
│   │   ├── session-management/   # Session templates
│   │   └── write-documents/      # Spec, impl, test templates
│   └── workflows/
│       ├── build.md              # BUILD workflow entry point
│       ├── solve.md              # SOLVE workflow entry point
│       ├── next.md               # Universal task entry with compliance
│       ├── explore.md            # EXPLORE phase
│       ├── design.md             # DESIGN phase
│       ├── implement.md          # IMPLEMENT phase
│       ├── refine.md             # REFINE phase
│       ├── deliver.md            # DELIVER phase
│       ├── critique.md           # Devil's Advocate review
│       ├── reconcile.md          # Pragmatic reconciliation
│       ├── verify.md             # Verification against specs and rules
│       ├── commit.md             # Git conventional commits
│       ├── rename.md             # Global/local refactoring
│       ├── sync.md               # Document synchronization
│       ├── test.md               # Run tests based on scope
│       ├── prime.md              # Load workspace context
│       ├── go-autonomous.md      # Full EDIRD autonomous loop
│       ├── go-research.md        # Structured research
│       ├── write-spec.md         # Create specification
│       ├── write-impl-plan.md    # Create implementation plan
│       ├── write-test-plan.md    # Create test plan
│       ├── session-new.md        # Initialize session
│       ├── session-save.md       # Save session progress
│       ├── session-resume.md     # Resume session
│       ├── session-close.md      # Close and sync session
│       ├── session-archive.md    # Archive session folder
│       └── setup-pdftools.md     # Install PDF tools
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

### Workflow Entry Points

Start a BUILD workflow (create software, features):
```
/build "Add user authentication API"
```

Start a SOLVE workflow (research, analysis, decisions):
```
/solve "Evaluate database migration options"
```

### Session Workflows

Start a new work session:
```
/session-new
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

8. **Rename** - Global/local pattern replacement:
```
/rename
```

9. **Commit** - Create conventional commits:
```
/commit
```

## Agent Compatibility

| Feature | Windsurf | Claude Code | Codex CLI | GitHub Copilot |
|---------|----------|-------------|-----------|----------------|
| **Type** | IDE | Terminal | Terminal | IDE Extension |
| **Platform** | Windows, macOS, Linux | Windows, macOS, Linux | macOS, Linux, Windows (WSL) | VS Code, Visual Studio, JetBrains |
| **Instructions** | `.windsurf/rules/*.md` | `CLAUDE.md` | `AGENTS.md` | `.github/copilot-instructions.md` |
| **Commands/Workflows** | `.windsurf/workflows/*.md` | `.claude/commands/*.md` | Custom prompts only | Prompt files only |
| **Skills** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Subagents** | ❌ No | ✅ Yes | ❌ No | ✅ Yes (custom agents) |
| **Hooks** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **MCP Support** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Sandbox** | ❌ No | ❌ No | ✅ Yes (OS-level) | ❌ No |
| **Config Format** | JSON + Protobuf | JSON | TOML | JSON |

### Deploying to Other Agents

**Claude Code:**
- `.windsurf/rules/*.md` → `CLAUDE.md` (merge into single file)
- `.windsurf/workflows/*.md` → `.claude/commands/*.md`
- `.windsurf/skills/*/SKILL.md` → `.claude/skills/*/SKILL.md`

**Codex CLI:**
- `.windsurf/rules/*.md` → `AGENTS.md` (merge into single file)

**GitHub Copilot:**
- `.windsurf/rules/*.md` → `.github/copilot-instructions.md` (merge into single file)

### Detailed Documentation

- [Agent Comparison](_INFO_AGENT_COMPARISON.md) - Full feature comparison with detailed tables
- [How Windsurf Works](INFO_HOW_WINDSURF_WORKS.md) - Windsurf IDE and Cascade assistant
- [How Claude Code Works](_INFO_HOW_CLAUDE_CODE_WORKS.md) - Anthropic's terminal agent
- [How Codex CLI Works](_INFO_HOW_CODEX_WORKS.md) - OpenAI's terminal agent
- [How GitHub Copilot Works](_INFO_HOW_COPILOT_WORKS.md) - GitHub's IDE extension
