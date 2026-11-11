# Git Conventions

Commit message format and .gitignore rules.

## MUST-NOT-FORGET

- Use Conventional Commits: `<type>(<scope>): <description>`
- Types: feat, fix, docs, refactor, test, chore, style, perf
- Imperative mood, <72 chars, no period
- NEVER commit secrets: .env, *.cer, *.pfx, *.pem, *.key

## Commit Message Format

Use **Conventional Commits**: `<type>(<scope>): <description>`

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependencies, build changes
- **style**: Formatting, whitespace (no code logic change)
- **perf**: Performance improvement

### Guidelines

1. Use imperative mood ("add" not "added" or "adds")
2. Keep description under 72 characters
3. No period at the end
4. Scope should match module/folder name when applicable

### Examples

```
feat(crawler): add incremental crawl mode
fix(auth): handle expired tokens
docs: update README installation steps
refactor(domains): simplify source validation logic
chore: update dependencies to latest versions
```

## .gitignore Rules

**Required in every workspace:**

1. **NEVER commit secrets**: `.env` files, certificates (*.cer, *.pfx, *.pem, *.key), API keys (`.api-keys.txt`)
2. **Keep the PromptSystem standard patterns**: `.tmp_*` (temp files and folders), `*_gitignore.*` and `*_gitignore/` (suffix-based exclusion), `_agentwork/` (agent artifacts), `__*.md` (workflow scaffolding). @skills:workspace-management `WORKSPACE-RULES.md` WS-SF-01 requires `.tmp_*`, `*_gitignore/`, `_agentwork/`; folder semantics: `agent-behavior.md` section Agent-Created Folders
3. **Prefer the `_gitignore` suffix over a new entry**: to exclude one file or folder, append `_gitignore` before the extension (`data_gitignore.json`, `_download_gitignore/`) instead of editing .gitignore
4. **No entries for paths outside the repository**: .gitignore patterns match only paths inside the repository; a pattern starting with `../` never matches. Shared tools live in `[WORKSPACE_FOLDER]/../.tools/` and need no entry. `.tools/` stays as a safety net in case the folder is created inside the workspace

**Per repository:**

5. **Exclude runtime environments, commit version and lock files**: add entries only for the runtimes the repo uses (`.venv/`, `node_modules/`, `target/`). Rule: @skills:workspace-management `WORKSPACE-RULES.md` WS-CT-05; patterns per runtime: `LOCAL_ENVIRONMENTS.md` section ".gitignore Patterns"
6. **Add build output and OS files only when the repo produces them**: `dist/`, `bin/`, `obj/`, `*.log`, `.DS_Store`
7. **Track shared config**: `.vscode/`, `Set-*-Env.bat` (environment setup scripts)
8. **Use negation pattern**: Keep specific files with `!` prefix when excluding folders
9. **Add comments**: Document non-obvious exclusions in .gitignore
10. **Verify after every change**: `git check-ignore -v <path>` prints the matching pattern; no output = not ignored

## .gitignore Template

```gitignore
# Secrets (NEVER commit)
*.env
.env.*
*.cer
*.pfx
*.pem
*.key
.api-keys.txt

# Temporary files
.tmp_*
*.tmp

# Workflow scaffolding and agent artifacts (auto-created, not deliverables)
__*.md
_agentwork/

# Suffix-based exclusion (append _gitignore before the extension of any file or folder)
*_gitignore.*
*_gitignore/

# Shared tools live in ../.tools/ outside the repository: no entry needed
# Safety net in case .tools/ is created inside the workspace
.tools/

# IDE (keep .vscode/ - shared config)
.vs/

# Runtime environments: only the runtimes this repo uses
# (other runtimes: workspace-management LOCAL_ENVIRONMENTS.md)
# Python
.venv/
__pycache__/
*.pyc
```

## Undo, Amend, Recovery

Undo or amend commits, force push, recover files after `git reset --hard`: see `SKILL.md` sections "Undo Operations" and "File Recovery".
