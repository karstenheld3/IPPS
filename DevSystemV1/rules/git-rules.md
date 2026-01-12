# Git Rules

Rules and patterns for Git usage in Windsurf projects.

## .gitignore Patterns

### Environment and Secrets (NEVER commit)

```gitignore
# Environment files with secrets
*.env
.env.local
.env.*

# Certificates and keys
*.cer
*.pfx
*.pem
*.key
```

### Python

```gitignore
# Virtual environment
.venv/

# Cache and build artifacts
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
```

### Node.js / JavaScript

```gitignore
# Dependencies
node_modules/

# Build output
dist/
lib/
release/
temp/

# Logs
logs/
*.log
npm-debug.log*
```

### IDE and OS

```gitignore
# Visual Studio
.vs/
.ntvs_analysis.dat
bin/
obj/

# macOS
.DS_Store
```

### Large Binaries and Tools

```gitignore
# Reinstallable tools (save repo size)
.tools/poppler/
_Tools/poppler/

# Deployment artifacts
deploy.zip
*.sppkg
```

### Temporary Files

```gitignore
# Temp files
*.tmp
.tmp_*

# Backup files
*.bak
```

### Project-Specific Sensitive Data

```gitignore
# Example: Exclude folders with personal data
[FOLDER]-*/_Input/
[FOLDER]-*/_Output/

# But keep specific file types
![FOLDER]-*/*.csv
![FOLDER]-*/*.md
```

## Best Practices

1. **Secrets**: NEVER commit `.env` files, certificates, or API keys
2. **Large binaries**: Exclude reinstallable tools (poppler, node_modules)
3. **Build artifacts**: Exclude generated files (dist/, __pycache__/)
4. **Use negation**: Keep specific files with `!` prefix when excluding folders
5. **Document patterns**: Add comments explaining non-obvious exclusions

## Negation Pattern Example

Keep folder structure but exclude contents:
```gitignore
# Ignore contents
src/uploads/*

# But keep the folder (with .gitkeep)
!src/uploads/.gitkeep
```

## Template .gitignore for Windsurf Projects

```gitignore
# Environment and secrets
*.env
.env.*

# Python
.venv/
__pycache__/
*.pyc

# Node.js
node_modules/
dist/

# IDE
.vs/

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
