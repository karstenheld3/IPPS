---
name: git-conventions
description: Apply when committing code, writing commit messages, or configuring .gitignore
---

# Git Conventions

Implements: [COMMIT], [MERGE] | Phases: IMPLEMENT, DELIVER

## MUST-NOT-FORGET

- Use Conventional Commits: `<type>(<scope>): <description>`
- Types: feat, fix, docs, refactor, test, chore, style, perf
- Imperative mood, <72 chars, no period
- NEVER commit secrets: .env, *.cer, *.pfx, *.pem, *.key

## Commit Format

`<type>(<scope>): <description>` - imperative mood, scope matches module/folder name.

Types: feat (feature), fix (bug), docs (docs only), refactor (no fix/feat), test, chore (deps/build), style (formatting), perf

```
feat(crawler): add incremental crawl mode
fix(auth): handle expired tokens
docs: update README installation steps
```

## Safe Undo Commit

```bash
git reset --soft HEAD~1   # Undo commit, keep STAGED
git reset HEAD~1          # Undo commit, keep UNSTAGED
git reset --hard HEAD~1   # DESTRUCTIVE - undo commit AND DELETE changes
```

**WARNING**: `--hard` deletes uncommitted files permanently.

Recovery from reflog: `git reflog` then `git checkout <hash> -- path/to/file`
Recovery from remote: `git fetch origin` then `git checkout origin/master -- path/to/file`
Amend (not pushed): `git commit --amend -m "new message"`
Force push: `git push --force-with-lease` (fails if remote changed)

## .gitignore Rules

1. **NEVER commit secrets**: .env, certificates, API keys
2. Exclude reinstallable binaries (node_modules, .venv/)
3. Exclude build artifacts (dist/, __pycache__/)
4. Track shared config (.vscode/)
5. Use `!` negation to keep specific files
6. Comment non-obvious exclusions

```gitignore
# Secrets (NEVER commit)
*.env
.env.*
*.cer
*.pfx
*.pem
*.key

# Python
.venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/

# Node.js
node_modules/
dist/
lib/
*.log

# IDE (keep .vscode/)
.vs/
bin/
obj/

# OS
.DS_Store

# Tools (reinstallable)
../.tools/poppler/

# Temporary
*.tmp
.tmp_*
*.bak
```