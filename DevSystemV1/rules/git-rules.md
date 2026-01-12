# Git Rules

## Rules

1. **NEVER commit secrets**: `.env` files, certificates (*.cer, *.pfx, *.pem, *.key), API keys
2. **Exclude large binaries**: Reinstallable tools (poppler, node_modules) - save repo size
3. **Exclude build artifacts**: Generated files (dist/, __pycache__/, *.pyc)
4. **Track shared config**: `.vscode/`, `Set-*-Env.bat` (environment setup scripts)
5. **Use negation pattern**: Keep specific files with `!` prefix when excluding folders
6. **Add comments**: Document non-obvious exclusions in .gitignore

## Template

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
.tools/poppler/

# Temporary
*.tmp
.tmp_*
*.bak

# Local storage
.localstorage/
```
