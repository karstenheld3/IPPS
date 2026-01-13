# IPP - Intelligent Pair Programming

A development system for AI-assisted coding workflows.

## DevSystem Versions

- **DevSystemV1** - Legacy workflows and rules (deprecated)
- **DevSystemV2** - Current system with modular skills

## Structure

```
.windsurf/
  rules/          # Agent rules (conventions, IDs)
  workflows/      # Agent workflows (session, commit, etc.)
  skills/         # Agent skills (pdf-tools, github, etc.)
DevSystemV2/
  skills/         # Skill implementations with scripts
.tools/           # Local tool installations (gitignored)
```

## Skills

- **pdf-tools** - PDF conversion, compression, analysis
- **github** - GitHub CLI operations

## Setup

Run `SETUP.md` in each skill folder to install required tools locally.
