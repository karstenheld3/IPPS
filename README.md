# IPP - Intelligent Pair Programming

A development system for AI-assisted coding workflows, optimized for Windsurf IDE.

## Overview

IPP provides structured rules, workflows, and skills for AI agents to follow consistent conventions during pair programming sessions. The system manages sessions, documents, commits, and tool installations.

## DevSystem Versions

- **DevSystemV1** - Legacy workflows in `.windsurf/` (being migrated)
- **DevSystemV2** - Current system with modular skills and workflows

## Structure

```
.windsurf/
  rules/          # Agent rules (conventions, IDs, core behavior)
  workflows/      # Agent workflows (session, commit, verify, etc.)
  skills/         # Agent skill definitions (SKILL.md files)
DevSystemV2/
  skills/         # Skill implementations with scripts and docs
  workflows/      # Extended workflow definitions
.tools/           # Local tool installations (gitignored)
```

## Skills

- **pdf-tools** - PDF conversion, compression, analysis using Ghostscript, Poppler, QPDF
- **github** - GitHub CLI operations (repos, issues, PRs)
- **session-management** - Session init, save, resume, close workflows
- **write-documents** - Spec, impl, test, info document templates

## Setup

Run `SETUP.md` in each skill folder to install required tools locally to `.tools/`.
