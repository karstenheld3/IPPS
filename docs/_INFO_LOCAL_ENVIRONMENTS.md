# INFO: Local Runtime Environments for JavaScript, Python, Rust, and Zig

**Doc ID**: LOCALENV-IN01
**Goal**: Document how local environments work for JS, Python, Rust, Zig and how to set them up from day 1

## Summary

- **JavaScript/Node.js**: Use `fnm` (recommended) or `Volta` (teams). Pin version in `.nvmrc`. Isolate deps in `node_modules/` (gitignored). Bun and Deno have their own runtimes.
- **Python**: Use built-in `venv` module. Create `.venv/` per project. Pin packages in `requirements.txt`. `uv` is a faster alternative.
- **Rust**: Use `rustup` with `rust-toolchain.toml` for per-project toolchain pinning. `target/` is disposable. No activation step needed.
- **Zig**: Use `zvm` (reads `build.zig.zon`) or `zv` (reads `.zigversion`). `zig-cache/` and `zig-out/` are disposable. No activation step.
- **Universal pattern**: Version file committed, environment dir gitignored, lock file committed, setup automated by deploy/build workflows.

## JavaScript / Node.js

### Version Managers [VERIFIED]

- **fnm** [VERIFIED]: Fast Rust binary, cross-platform (Win/Mac/Linux), reads `.nvmrc` and `.node-version`, auto-switches on `cd` with `--use-on-cd` flag. Recommended default for personal machines.
- **Volta** [VERIFIED]: Rust binary, cross-platform, pins Node AND package manager (npm/Yarn) in `package.json` `"volta"` key. Transparent switching (no shell hook). Best for team reproducibility.
- **nvm** [VERIFIED]: Classic bash script, Mac/Linux only. Slow shell startup. Windows uses separate `nvm-windows` project. Still widely used but not recommended for new setups in 2026.
- **nvm-windows** [VERIFIED]: Separate project from nvm, Windows only. No auto-switching.

### Setup from Day 1

1. Create `.nvmrc` with Node version (e.g., `22` or `22.17.0`)
2. `npm init -y`
3. `npm install`
4. Gitignore `node_modules/`
5. Commit `.nvmrc`, `package.json`, `package-lock.json`

### Bun [VERIFIED]

Bun is its own runtime (not Node.js). Installs via `bun.sh/install.ps1`. Uses `bun.lockb` lockfile. `node_modules/` still used for npm compatibility.

### Deno [VERIFIED]

Deno has no `node_modules`. Dependencies are URL-imported and cached. Uses `deno.json` for config. `deno cache main.ts` pre-fetches deps.

## Python

### venv (Built-in) [VERIFIED]

- Ships with Python 3.3+, no external tools needed
- `python -m venv .venv` creates isolated environment
- Activate: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)
- `pip freeze > requirements.txt` captures exact versions
- `pip install -r requirements.txt` restores environment
- `.venv/` is gitignored, `requirements.txt` is committed

### uv [VERIFIED]

Rust-based package manager, 10-100x faster than pip. `uv venv` creates environment, `uv pip install` installs packages. Can use `pyproject.toml` with `uv sync` for automatic venv management.

### Version Pinning [VERIFIED]

- `.python-version` file: used by pyenv/pyenv-win to pin Python interpreter version
- `requirements.txt`: pin package versions
- `pyproject.toml`: modern alternative with build system metadata

## Rust

### rustup [VERIFIED]

Official Rust toolchain manager. Manages stable/beta/nightly channels and components (clippy, rustfmt).

Per-project pinning via `rust-toolchain.toml` [VERIFIED]:

```toml
[toolchain]
channel = "stable"
components = ["rustfmt", "clippy"]
```

rustup auto-detects this file and uses the pinned toolchain when running `cargo` or `rustc` in that directory. The file is committed to git for reproducible builds.

Key properties:
- `target/` directory is disposable (rebuilt by `cargo build`)
- No separate "activate" step - rustup handles toolchain selection automatically
- `CARGO_HOME` and `RUSTUP_HOME` can be customized for isolated installations
- `Cargo.lock` committed for reproducible builds

## Zig

### Version Managers [VERIFIED]

- **zvm** [VERIFIED]: Native CLI, project-aware shims detect `minimum_zig_version` from `build.zig.zon`. Auto-installs correct version. JSON/plain output for automation.
- **zv** [VERIFIED]: Rust binary, uses `.zigversion` file or inline `+version` syntax. Cross-platform. Also provisions ZLS (Zig Language Server).
- **zix** [VERIFIED]: Lightweight, parallel downloads, auto-detects `.zigversion` files.

### Setup from Day 1

1. Install zvm (or zv/zix)
2. Create `build.zig.zon` with `minimum_zig_version` field
3. Version manager auto-installs and switches to correct Zig version
4. Gitignore `zig-cache/` and `zig-out/`
5. Commit `build.zig.zon`

Key properties:
- No separate "activate" step - version managers handle switching
- `build.zig.zon` is the project manifest (committed to git)
- `zig-cache/` and `zig-out/` are disposable build artifacts

## Sources

- https://github.com/schniz/fnm - fnm GitHub repository
- https://ortamarco.me/en/blog/nvm-vs-fnm-vs-volta-node-version-managers/ - nvm vs fnm vs Volta comparison
- https://techearl.com/nvm-vs-fnm-vs-volta - 2026 comparison of Node version managers
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Extension/Server-side/Express_Nodejs/development_environment - MDN Node setup guide
- https://github.com/nvm-sh/nvm/ - nvm GitHub repository
- https://docs.python.org/3/tutorial/venv.html - Python venv tutorial
- https://docs.python.org/3/library/venv.html - Python venv module docs
- https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/ - pip + venv guide
- https://generalistprogrammer.com/tutorials/python-virtual-environment-complete-guide - Complete venv guide 2026
- https://realpython.com/python-virtual-environments-a-primer/ - Real Python venv primer
- https://rust-lang.github.io/rustup/overrides.html - rustup overrides documentation
- https://rust-lang.github.io/rustup/installation/index.html - rustup installation
- https://doc.rust-lang.org/book/ch01-01-installation.html - Rust installation guide
- https://github.com/hendriknielaender/zvm/ - zvm GitHub repository
- https://github.com/weezy20/zv/ - zv GitHub repository
- https://zig.sh/ - ZVM website
- https://codeberg.org/erffy/zix - zix Codeberg repository

## Document History

**[2026-09-05 19:00]**
- Initial research document created
