---
name: github
description: Apply when working with GitHub repositories, issues, PRs, or authentication
---

# GitHub CLI Guide

GitHub CLI at `../.tools/gh/bin/gh.exe`. Alias `$gh` below.

## MUST-NOT-FORGET

- Authenticate before first use: `gh auth login`
- Use `--repo` flag when not in a git directory
- Check auth status if commands fail: `gh auth status`

## Authentication

```powershell
& "../.tools/gh/bin/gh.exe" auth login
& "../.tools/gh/bin/gh.exe" auth status
& "../.tools/gh/bin/gh.exe" auth setup-git
```

## Repository Operations

```powershell
& "../.tools/gh/bin/gh.exe" repo create <name> --private --source=. --remote=origin --push
& "../.tools/gh/bin/gh.exe" repo clone <owner>/<repo>
& "../.tools/gh/bin/gh.exe" repo view [<owner>/<repo>]
& "../.tools/gh/bin/gh.exe" repo list [--limit 50]
& "../.tools/gh/bin/gh.exe" repo fork <owner>/<repo> --clone
& "../.tools/gh/bin/gh.exe" repo view --web
```

## Issues

```powershell
& "../.tools/gh/bin/gh.exe" issue create --title "Bug: something broke" --body "Description"
& "../.tools/gh/bin/gh.exe" issue list [--state open] [--label "bug"]
& "../.tools/gh/bin/gh.exe" issue view <number>
& "../.tools/gh/bin/gh.exe" issue close <number>
```

## Pull Requests

```powershell
& "../.tools/gh/bin/gh.exe" pr create --title "Add feature" --body "Description"
& "../.tools/gh/bin/gh.exe" pr create --fill
& "../.tools/gh/bin/gh.exe" pr list [--state open]
& "../.tools/gh/bin/gh.exe" pr view <number> [--web]
& "../.tools/gh/bin/gh.exe" pr merge <number> [--squash]
& "../.tools/gh/bin/gh.exe" pr checkout <number>
```

## Releases

```powershell
& "../.tools/gh/bin/gh.exe" release create v1.0.0 --title "Version 1.0.0" --notes "Release notes"
& "../.tools/gh/bin/gh.exe" release list
& "../.tools/gh/bin/gh.exe" release download v1.0.0
```

## Gists

```powershell
& "../.tools/gh/bin/gh.exe" gist create file.txt --public
& "../.tools/gh/bin/gh.exe" gist create file1.txt file2.txt --desc "My gist"
& "../.tools/gh/bin/gh.exe" gist list
```

## Workflow / Actions

```powershell
& "../.tools/gh/bin/gh.exe" workflow list
& "../.tools/gh/bin/gh.exe" run list
& "../.tools/gh/bin/gh.exe" run view <run-id>
& "../.tools/gh/bin/gh.exe" workflow run <workflow-name>
```

## Setup

See `SETUP.md` in this skill folder.