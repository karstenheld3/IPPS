# Local Environments Guide

How to set up and use local runtime environments for project repos. Local environments isolate dependencies per project, preventing version conflicts and ensuring reproducibility.

**Why**: Global installations cause dependency conflicts between projects. Local environments pin runtime versions and dependencies per project, checked into version control for team reproducibility.

## Principles

1. **Every project gets its own environment** - No shared global package installs
2. **Version files are committed** - `.nvmrc`, `rust-toolchain.toml`, `.python-version`, `.zigversion` travel with the repo
3. **Environment directories are gitignored** - `node_modules/`, `.venv/`, `target/`, `zig-cache/` are disposable
4. **Setup is automated** - Deploy/build workflows verify environment exists before building

## JavaScript / Node.js

### Version Managers

| Tool | Platform | Auto-switch | Pins in | Notes |
| --- | --- | --- | --- | --- |
| fnm | All (Win/Mac/Linux) | Yes (`--use-on-cd`) | `.nvmrc` or `.node-version` | Fast Rust binary, recommended default |
| Volta | All | Yes (transparent) | `package.json` `"volta"` | Also pins npm/Yarn, best for teams |
| nvm | Mac/Linux only | Manual (hook needed) | `.nvmrc` | Classic, slow shell startup |
| nvm-windows | Windows only | No | N/A | Separate project from nvm |

**Recommended**: `fnm` for personal machines, `Volta` for team repos needing package manager pinning.

### Setup from Day 1

1. Create `.nvmrc` in project root with Node version (e.g., `22` or `22.17.0`)
2. Add `.gitignore` entry for `node_modules/`
3. Initialize: `npm init -y` (or `pnpm init`, `yarn init`)
4. Install dependencies: `npm install`
5. Verify: `node --version` matches `.nvmrc`

### Bun

Bun installs its own runtime. No version manager needed for single-version projects.

1. Install: `powershell -c "irm bun.sh/install.ps1 | iex"`
2. Initialize: `bun init`
3. Install deps: `bun install`
4. Add `.gitignore` entry for `node_modules/` and `bun.lockb` (keep lockfile, ignore cache)

### Deno

Deno has no `node_modules`. Dependencies are URL-imported and cached globally per project.

1. Install: `irm https://deno.land/install.ps1 | iex` (Windows)
2. Create `deno.json` with config
3. Add `.gitignore` entry for `.deno/` cache if present
4. Cache deps: `deno cache main.ts`

## Python

### venv (Built-in, Recommended Default)

`venv` ships with Python 3.3+. No external tools needed.

1. Create: `python -m venv .venv`
2. Activate (Windows): `.venv\Scripts\activate`
3. Activate (Mac/Linux): `source .venv/bin/activate`
4. Upgrade pip: `python -m pip install --upgrade pip`
5. Install deps: `pip install -r requirements.txt`
6. Freeze: `pip freeze > requirements.txt`
7. Add `.gitignore` entry for `.venv/`

### uv (Fast Alternative)

`uv` is a Rust-based Python package manager that creates venvs and installs packages 10-100x faster.

1. Install: `pip install uv` or `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
2. Create venv + install: `uv venv && uv pip install -r requirements.txt`
3. Or use `uv sync` with `pyproject.toml` (manages venv automatically)

### Version Pinning

- `.python-version` file (used by pyenv, pyenv-win): pin Python interpreter version
- `requirements.txt`: pin package versions for reproducibility
- `pyproject.toml`: modern alternative with build system metadata

## Rust

### rustup (Official Toolchain Manager)

`rustup` manages Rust toolchains (stable, beta, nightly) and components (clippy, rustfmt).

1. Install: `https://rust-lang.org/tools/install` or `winget install Rustlang.Rustup`
2. Per-project pinning: create `rust-toolchain.toml` in project root:

```toml
[toolchain]
channel = "stable"
components = ["rustfmt", "clippy"]
```

3. rustup auto-detects `rust-toolchain.toml` and uses the pinned toolchain
4. Dependencies: managed by `cargo` via `Cargo.toml` and `Cargo.lock`
5. Add `.gitignore` entry for `target/`

### Key Properties

- `rust-toolchain.toml` is committed to git (reproducible builds)
- `target/` directory is disposable (rebuilt by `cargo build`)
- No separate "activate" step - rustup handles toolchain selection automatically
- `CARGO_HOME` can be customized for isolated installations

## Zig

### Version Managers

| Tool | Platform | Auto-detect | Pins in | Notes |
| --- | --- | --- | --- | --- |
| zvm | All | Yes (`build.zig.zon`) | `build.zig.zon` `minimum_zig_version` | Native, project-aware shims |
| zv | All | Yes (`.zigversion`) | `.zigversion` | Rust binary, inline `+version` syntax |
| zix | All | Yes (`.zigversion`) | `.zigversion` | Lightweight, parallel downloads |

**Recommended**: `zvm` for project-aware detection from `build.zig.zon`, `zv` for explicit `.zigversion` files.

### Setup from Day 1

1. Install zvm: see https://zig.sh/
2. Create `build.zig.zon` with `minimum_zig_version` field
3. zvm auto-installs and switches to correct Zig version on `zig build`
4. Add `.gitignore` entry for `zig-cache/` and `zig-out/`

### Key Properties

- `build.zig.zon` is the project manifest (committed to git)
- `minimum_zig_version` field pins the Zig compiler version
- `zig-cache/` and `zig-out/` are disposable build artifacts
- No separate "activate" step - version managers handle switching

## Detection Guide

To detect which runtime environment a project uses:

| Signal | Runtime | Environment Location |
| --- | --- | --- |
| `package.json` + `.nvmrc` | Node.js | `node_modules/` |
| `package.json` + `"volta"` key | Node.js (Volta) | `node_modules/` |
| `bun.lockb` | Bun | `node_modules/` |
| `deno.json` | Deno | global cache |
| `requirements.txt` or `pyproject.toml` | Python | `.venv/` |
| `.python-version` | Python (pyenv) | `.venv/` |
| `Cargo.toml` + `rust-toolchain.toml` | Rust | `target/` |
| `build.zig.zon` | Zig | `zig-cache/` |
| `.zigversion` | Zig (zv/zix) | `zig-cache/` |

## .gitignore Patterns

Each runtime requires specific gitignore entries:

```
# Node.js / Bun
node_modules/

# Python
.venv/
__pycache__/
*.pyc

# Rust
target/

# Zig
zig-cache/
zig-out/
```

## Verification Checklist

When setting up a local environment for a repo:

- [ ] Runtime version file exists (`.nvmrc`, `rust-toolchain.toml`, `.python-version`, `build.zig.zon`)
- [ ] Environment directory is gitignored
- [ ] Lock file exists (`package-lock.json`, `requirements.txt`, `Cargo.lock`, `bun.lockb`)
- [ ] Runtime version matches version file
- [ ] Dependencies installed successfully
- [ ] Project builds without errors
