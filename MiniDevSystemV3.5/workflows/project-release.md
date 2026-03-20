# Project Release Workflow

Create dated release with comprehensive release notes.

## Prerequisites

- All work committed and pushed
- GitHub CLI (`gh`) installed and authenticated
- No uncommitted changes

## Steps

### 1. Determine Release Scope

```powershell
git tag --sort=-creatordate | Select-Object -First 1
```

- List commits: `git log [LAST_TAG]..HEAD --oneline`
- List changed files: `git diff --name-status [LAST_TAG]..HEAD`

### 2. Inventory Sessions

```powershell
Get-ChildItem "_Sessions" -Directory | Where-Object { $_.Name -notlike "_Archive*" }
```

Per session collect: name, date, Goal (NOTES.md), Status (PROGRESS.md), artifacts (`_INFO_*.md`, `_SPEC_*.md`, `_IMPL_*.md`, `_STRUT_*.md`), key findings.

### 3. Generate Release Notes

Create `RELEASE_NOTES_[YYYY-MM-DD].md`:

```markdown
# Release Notes: [YYYY-MM-DD]

## Summary
This release covers [N] sessions from [date range], focusing on [themes].

## Sessions Overview
### [N]. [Session_Name]
**Goal**: [from NOTES.md]
**Outcome**: [summary]
**Artifacts:**
- `[filename]` - [description]
**Key Findings:** (if any)
- [finding]
---
[Repeat for each session]

## New Skills Deployed
## New Workflows
## Workspace Files
## Statistics
- **Total Sessions**: [N]
- **Total Documents Created**: [N]

## Document History
**[YYYY-MM-DD HH:MM]**
- Initial release notes created
```

### 4. Commit Release Notes

```powershell
git add "RELEASE_NOTES_[YYYY-MM-DD].md"
git commit -m "docs: add release notes for [YYYY-MM-DD]"
```

### 5. Create Tag

```powershell
git tag -a "[YYYY-MM-DD]" -m "Release [YYYY-MM-DD]: [brief summary]"
git push origin "[YYYY-MM-DD]"
git push
```

### 6. User Confirmation

Present: session count, key artifacts, tag name. Ask: "Create GitHub release with these notes? (y/n)"

### 7. Create GitHub Release

```powershell
gh release create "[YYYY-MM-DD]" --title "Release [YYYY-MM-DD]" --notes-file "RELEASE_NOTES_[YYYY-MM-DD].md"
```

Report release URL to user.

## Notes

- Use today's date for tag unless user specifies otherwise
- Include ALL sessions since last release, mark in-progress ones clearly
- If `gh` not installed, provide manual release URL