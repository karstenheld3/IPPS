# IPP - Insanely Productive Programmer

A development system for AI-assisted coding workflows, optimized for Windsurf IDE on Windows x64.

## Overview

IPP provides structured rules, workflows, and skills for AI agents to follow consistent conventions during pair programming sessions. The system manages sessions, documents, commits, and tool installations.

## DevSystem Versions

- **DevSystemV1** - Legacy workflows in `.windsurf/` (being migrated)
- **DevSystemV2** - Current system with modular skills and workflows

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
│   ├── _SPEC_V1_TO_V2_USING_SKILLS.md
│   ├── _IMPL_V1_TO_V2_USING_SKILLS.md
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

## Setup

Run `SETUP.md` in each skill folder to install required tools locally to `.tools/`.
