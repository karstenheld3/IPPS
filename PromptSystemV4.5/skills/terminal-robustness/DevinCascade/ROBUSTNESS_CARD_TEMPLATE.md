# Robustness Card Template (DevinCascade)

Re-usable card for Devin/Cascade agents. Copy to project root as `__CARD_[TOPIC]-Robustness.md` and extend with project-specific entries. Defaults are tested or evidence-cited - replace bracketed placeholders.

```markdown
# Robustness Card: [TOPIC]

## Banned commands

- `2>&1` on stderr-heavy commands (npm, pip, compilers) - pwsh becomes the merge point: OutOfMemoryException with corrupted exit code or backpressure hang - evidence: investigation log @I001.016-017
- `git log` / `git diff` / `git show` / `git blame` without `--no-pager` - launches pager, blocks on stdin - generic pager rule
- `npm install` without `--yes` or `--ci` - prompts on stdin - generic stdin rule
- `npx <tool>` without `--yes` - prompts to install package - generic stdin rule
- `npm create <tool> ... -- <flags> --yes` - `--yes` after `--` reaches the scaffold tool, not the runner; "Ok to proceed?" install prompt still waits on stdin - evidence: @I001.025
- `node` without a script argument - starts REPL, waits on stdin - generic stdin rule
- `Read-Host`, `pause`, `Get-Credential` - wait for stdin - generic stdin rule
- `bun --watch`, `npm run dev`, any `--watch` flag - unbounded child; tool waits for pipe EOF until the child dies - evidence: @I001.012-013
- `Wait-Process` without `-Timeout` - waits forever - generic unbounded-child rule
- `Get-Content -Wait`, `tail -f` - stream indefinitely - generic stream rule
- `Get-ChildItem -Recurse` / `Select-String -Recurse` on large trees - full enumeration before return; use rg.exe - generic enumeration rule
- `Get-Content | Select-Object -First N` on large or locked files - pipeline buffers before stop; use `-TotalCount` - tested
- [project-specific: build.bat / ship.bat containing pause; CLI tools without non-interactive flags; dev servers]

## Time caps

- Single test file: 3-minute cap
- Full test suite: 10-minute cap
- Build scripts: 15-minute cap
- Git operations: 2-minute cap
- Type checking: 5-minute cap
- [project-specific caps]

## Always rules

- Verbose output (>few KB) runs as .tmp_ script + redirect to file + read_file - defeats pipe buffer, drain throttle, merge point, and handle inheritance - evidence: @I001.019
- Test suites run with `--ci` / `--timeout` (non-blocking, no watch mode)
- Git commands use `--no-pager`
- `npx` commands use `--yes`; in two-layer commands (`npm create` / `npx` + `--`) the runner-level `--yes` goes BEFORE `--` - evidence: @I001.025
- Stderr redirected to file, never merged with `2>&1`
- File and content search uses rg.exe instead of recursive shell enumeration
- Stray processes stopped after every command execution
- Hang-risky commands run non-blocking with status polling, not blind blocking
- Long command echo is mangled (duplicated, truncated) - verify via artifacts on disk, never by parsing the echo - evidence: @I001.011

## On-cap behavior

1. Kill the process tree (children and grandchildren), not just the parent
2. Record the command and cap in session PROBLEMS.md
3. Continue with the next step - never re-run the same command unbounded
4. Same command hangs twice: stop the prompt with a PROBLEMS.md entry

## Kill procedure

Recursive Stop-ProcessTree (see DevinCascade guide Section 3) - kills children and grandchildren, dead-PID safe. After the kill, sweep for orphaned grandchildren by command-line pattern: their parent PID no longer maps to a running process.

## Execution pattern

Hang-risky commands execute via Start-Process + WaitForExit with redirect-to-file and process-tree kill on timeout. Full tested pattern: DevinCascade/TERMINAL_ROBUSTNESS_GUIDES.md Section 3.

## Findings feed

(extend with one entry per hang or near-hang: what, why, prevention)
```
