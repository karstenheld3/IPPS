---
name: git
description: Apply when working with Git repositories, commit history, or recovering files from previous commits
---

# Git Skill

## MUST-NOT-FORGET

- Always verify repository root before operations: `git rev-parse --show-toplevel`
- Use `--name-status` to see A/M/D (Added/Modified/Deleted) per commit
- To recover deleted file: checkout from commit BEFORE deletion (use `^` suffix)
- Reflog survives even after reset/rebase - use it for recovery

## Setup

See `SETUP.md` in this skill folder.

## Commit History Navigation

```powershell
git log --oneline -10                              # Recent commits
git log --oneline --name-status -10                # With file changes
git log --format="%h %ad %an: %s" --date=short -10 # With date/author

git show --name-status <commit>                    # Files changed in commit
git show --name-only <commit>                      # File list only
git show <commit>                                  # Full diff

git log --oneline HEAD~N -1                        # N commits back
git diff <commit1> <commit2> --name-status         # Compare two commits
```

## File Recovery

### Find Deletion

```powershell
git log --diff-filter=D --summary                          # All deleted files
git log --diff-filter=D --summary -- "/filename.ext"     # Specific file
git log --diff-filter=D -1 -- path/to/file.ext             # Exact commit
git log --all -- path/to/deleted/file.ext                  # Last commit file existed
```

### Recover Deleted File

```powershell
git checkout <deletion_commit>^ -- path/to/file.ext        # From parent of deletion
git checkout <good_commit> -- path/to/file.ext              # From known good commit
git show <commit>:path/to/file.ext > recovered_file.ext     # Via show + redirect
git checkout HEAD@{n} -- path/to/file.ext                   # From reflog
```

Note:** If file was renamed (not deleted), use `git log --follow -- oldname` to track renames.

### Batch Recovery

```powershell
git log --diff-filter=D --name-only --format="" -n 20 | Where-Object { $_ -ne "" } | Sort-Object -Unique
git checkout <commit>^ -- file1.ext file2.ext file3.ext     # Multiple files
git checkout <commit>^ -- path/to/directory/                 # Entire directory
```

## Comparing Versions

```powershell
git diff <commit1> <commit2> -- path/to/file    # Between commits
git diff <commit> -- path/to/file               # Commit vs working dir
git diff --cached <commit> -- path/to/file       # Commit vs staged
git show <commit>:path/to/file                   # File content at commit
```

## Undo Operations

```powershell
git reset --soft HEAD^          # Undo commit, keep staged
git reset --hard HEAD^          # Undo commit, discard changes
git checkout HEAD -- path/to/file  # Restore to last committed
git reset HEAD -- path/to/file     # Unstage file
```

## Status and Inspection

```powershell
git status --short              # Brief status
git diff --cached --name-status # Staged changes
git diff --name-status          # Unstaged changes
```