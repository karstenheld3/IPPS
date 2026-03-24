---
description: Create conventional commits
auto_execution_mode: 1
---

# Commit Workflow

## Required Skills

- @git-conventions for commit message format

## Steps

1. Analyze changes since last commit
2. If multiple activities with different files, plan multiple commits
3. Order chronologically by file modification times
4. Separate by type: docs (research/specs/plans), feat/fix, test, docs
5. Follow @git-conventions for message format
6. Execute commits until all changes committed

Format: `<type>(<scope>): <description>`

Types: feat, fix, docs, refactor, test, chore, style, perf