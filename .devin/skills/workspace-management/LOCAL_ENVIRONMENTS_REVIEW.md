# Fact-Check Review: Local Environments Documents

**Reviewed files**:
- `LOCAL_ENVIRONMENTS.md` (workspace-management skill)
- `_INFO_LOCAL_ENVIRONMENTS.md` (research document)

**Date**: 2026-09-05 19:10

## Summary

- 13 factual claims checked
- 10 VERIFIED (correct)
- 2 STALE (outdated claims)
- 1 INACCURATE (wrong detail)

## Findings

### F01: Deno "has no node_modules" - STALE

**Claim** (LOCAL_ENVIRONMENTS.md line 44): "Deno has no `node_modules`. Dependencies are URL-imported and cached globally per project."

**Verdict**: STALE

**Evidence**: Deno 2.0+ supports `npm:` specifiers, `package.json`, and `jsr:` specifiers. With `package.json` present, Deno defaults to creating a local `node_modules` directory (manual mode). `nodeModulesDir` option in `deno.json` controls this: "none" (default, no node_modules), "auto" (creates on each run), "manual" (requires `deno install`).

Source: https://docs.deno.com/runtime/fundamentals/node/ (last updated 2026-06-25) - "By default, Deno instead resolves npm packages from a central global cache and does not create a `node_modules` directory" BUT "Projects with a `package.json` default to the manual `node_modules` mode".

**Fix needed**: Reword to "By default, Deno uses a global cache instead of `node_modules`. When using `package.json`, Deno creates a local `node_modules` directory (configurable via `nodeModulesDir` in `deno.json`)."

### F02: Deno ".deno/ cache" gitignore - INACCURATE

**Claim** (LOCAL_ENVIRONMENTS.md line 48): "Add `.gitignore` entry for `.deno/` cache if present"

**Verdict**: INACCURATE

**Evidence**: Deno's cache directory is `DENO_DIR`, which defaults to `$HOME/.cache/deno` (Linux/Mac) or `%LOCALAPPDATA%\deno` (Windows). This is a global cache, not a per-project `.deno/` directory. No `.deno/` folder is created in the project directory.

Source: https://docs.deno.com/runtime/getting_started/installation/ (last updated 2026-07-09)

**Fix needed**: Remove the `.deno/` gitignore line. Deno projects typically don't need a cache gitignore entry since the cache is global, not per-project.

### F03: uv "10-100x faster" - PARTIALLY ACCURATE

**Claim** (LOCAL_ENVIRONMENTS.md line 69, INFO line 52): "uv is a Rust-based Python package manager that creates venvs and installs packages 10-100x faster."

**Verdict**: PARTIALLY ACCURATE

**Evidence**: The "10-100x" figure comes from Astral's marketing and Xebia blog. Real benchmarks show:
- Warm cache: uv 0.0s vs pip 6.3s (effectively infinite x, but 78x vs conda in OpenTeams benchmark)
- Cold cache: uv 1.7s vs pip 8.5s (5x, not 10x)
- With matching bytecode compilation settings: uv 2.4s vs pip 8.5s cold (3.5x)

Sources:
- https://pythonspeed.com/articles/faster-pip-installs/ - independent benchmark showing 5x for cold cache
- https://openteams.com/benchmark-python-package-managers/ - 78x vs conda for warm install
- https://xebia.com/blog/uv-the-engineering-secrets-behind-pythons-speed-king/ - claims 10-100x

**Fix needed**: Change to "10-100x faster for warm cache, 5-10x faster for cold cache" or simplify to "significantly faster (often 10x or more for cached installs)".

### F04: Bun install URL - VERIFIED

**Claim** (LOCAL_ENVIRONMENTS.md line 39): `powershell -c "irm bun.sh/install.ps1 | iex"`

**Verdict**: VERIFIED

**Evidence**: Official Bun docs at https://bun.sh/docs/installation show exact same command. Note: `bun.com` domain has 308 redirect issues, but `bun.sh` works correctly.

### F05: Deno install URL - VERIFIED

**Claim** (LOCAL_ENVIRONMENTS.md line 48): `irm https://deno.land/install.ps1 | iex`

**Verdict**: VERIFIED

**Evidence**: Official Deno docs at https://docs.deno.com/runtime/getting_started/installation/ show exact same command. GitHub repo denoland/deno_install confirms.

### F06: Python venv ships with Python 3.3+ - VERIFIED

**Claim** (LOCAL_ENVIRONMENTS.md line 57): "venv ships with Python 3.3+"

**Verdict**: VERIFIED

**Evidence**: Well-established. The `venv` module was added to Python 3.3 standard library. Recommended over `virtualenv` since Python 3.5.

### F07: fnm is Rust binary, cross-platform - VERIFIED

**Claim** (LOCAL_ENVIRONMENTS.md line 18): "fnm - All platforms (Win/Mac/Linux). Fast Rust binary"

**Verdict**: VERIFIED

**Evidence**: GitHub README at https://github.com/schniz/fnm confirms "built in Rust" and "Cross-platform support (macOS, Windows, Linux)".

### F08: Volta pins in package.json "volta" key - VERIFIED

**Claim** (LOCAL_ENVIRONMENTS.md line 19): "Pins in `package.json` `"volta"` key. Also pins npm/Yarn"

**Verdict**: VERIFIED

**Evidence**: Volta documentation confirms it pins Node, npm, and Yarn versions in `package.json` `"volta"` field.

### F09: rust-toolchain.toml format - VERIFIED

**Claim** (LOCAL_ENVIRONMENTS.md lines 90-94): `[toolchain]` section with `channel` and `components` fields

**Verdict**: VERIFIED

**Evidence**: rustup documentation at https://rust-lang.github.io/rustup/overrides.html confirms the `rust-toolchain.toml` format with `[toolchain]` table, `channel` field, and `components` field.

### F10: nvm is Mac/Linux only, nvm-windows is separate - VERIFIED

**Claim** (LOCAL_ENVIRONMENTS.md lines 20-23): "nvm - Mac/Linux only" and "nvm-windows - Windows only. Separate project from nvm"

**Verdict**: VERIFIED

**Evidence**: https://github.com/nvm-sh/nvm/ is bash script for Mac/Linux. https://github.com/coreybutler/nvm-windows is a separate project for Windows.

### F11: zvm detects from build.zig.zon - VERIFIED

**Claim** (LOCAL_ENVIRONMENTS.md line 109): "zvm - Auto-detects from `build.zig.zon` `minimum_zig_version`"

**Verdict**: VERIFIED

**Evidence**: GitHub README at https://github.com/hendriknielaender/zvm/ confirms project-aware shims that detect `minimum_zig_version` from `build.zig.zon`.

### F12: zv uses .zigversion - VERIFIED

**Claim** (LOCAL_ENVIRONMENTS.md line 110): "zv - Auto-detects `.zigversion` file"

**Verdict**: VERIFIED

**Evidence**: GitHub README at https://github.com/weezy20/zv/ confirms `.zigversion` file support and inline `+version` syntax.

### F13: Deno "URL-imported" description - STALE

**Claim** (LOCAL_ENVIRONMENTS.md line 44): "Dependencies are URL-imported and cached globally per project"

**Verdict**: STALE

**Evidence**: Since Deno 2.0, `npm:` specifiers are recommended over HTTP URL imports. Deno blog: "we recommend using `npm:` specifiers directly" instead of esm.sh/unpkg.com HTTP imports. `jsr:` specifiers are also now available.

Source: https://deno.com/blog/not-using-npm-specifiers-doing-it-wrong

**Fix needed**: Reword to "Dependencies are imported via `npm:`, `jsr:`, or URL specifiers and cached globally by default."

## Fixes Required

1. **F01 + F13**: Reword Deno section to reflect Deno 2+ behavior (npm: specifiers, optional node_modules)
2. **F02**: Remove inaccurate `.deno/` gitignore claim
3. **F03**: Qualify uv speed claim with realistic ranges
