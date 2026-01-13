# IPP - Intelligent Pair Programming

A development system for AI-assisted coding workflows, optimized for Windsurf IDE.

## Overview

IPP provides structured rules, workflows, and skills for AI agents to follow consistent conventions during pair programming sessions. The system manages sessions, documents, commits, and tool installations.

## DevSystem Versions

- **DevSystemV1** - Legacy workflows in `.windsurf/` (being migrated)
- **DevSystemV2** - Current system with modular skills and workflows

## Project Structure

```
IPP/
├── .windsurf/                    # Windsurf agent configuration (active)
│   ├── rules/                    # Rules (copied from DevSystemVX for testing)
│   ├── workflows/                # Workflows (copied from DevSystemVX)
│   └── skills/                   # Skills (copied from DevSystemVX)
├── DevSystemV1/                  # Legacy system (deprecated)
│   ├── rules/
│   └── workflows/
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
│       ├── session-*.md          # Session management workflows
│       ├── write-*.md            # Document creation workflows
│       ├── commit.md             # Git commit workflow
│       ├── verify.md             # Verification workflow
│       └── prime.md              # Context loading workflow
├── .tools/                       # Local tool installations (gitignored)
│   ├── poppler/                  # PDF to image conversion
│   ├── qpdf/                     # PDF manipulation
│   ├── gs/                       # Ghostscript PDF compression
│   ├── 7z/                       # Archive extraction
│   └── gh/                       # GitHub CLI
└── README.md
```

## Skills

- **pdf-tools** - PDF conversion, compression, analysis using Ghostscript, Poppler, QPDF
- **github** - GitHub CLI operations (repos, issues, PRs)
- **session-management** - Session init, save, resume, close workflows
- **write-documents** - Spec, impl, test, info document templates

## Setup

Run `SETUP.md` in each skill folder to install required tools locally to `.tools/`.
