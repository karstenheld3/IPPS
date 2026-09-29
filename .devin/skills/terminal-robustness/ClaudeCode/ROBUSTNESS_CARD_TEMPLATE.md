# Robustness Card Template (ClaudeCode)

Re-usable card for Claude Code agents. Copy to project root as `__CARD_[TOPIC]-Robustness.md` and extend with project-specific entries. Generic defaults only - replace bracketed placeholders.

```markdown
# Robustness Card: [TOPIC]

## Banned commands

- `2>&1` on stderr-heavy commands (npm, pip, compilers) - shell merge point can hang or crash; redirect to file instead - generic merge rule
- `git log` / `git diff` / `git show` without `--no-pager` - launches pager, waits on stdin - generic pager rule
- `npm install` without `--yes` - prompts for confirmation on stdin - generic stdin rule
- `npx <tool>` without `--yes` - prompts to install package - generic stdin rule
- `Read-Host`, `pause`, `Get-Credential` - wait for stdin - generic stdin rule
- Any `--watch` flag, `npm run dev`, `bun --watch` - never terminates - generic unbounded-child rule
- `Wait-Process` without `-Timeout` - waits forever - generic unbounded-child rule
- `Get-Content -Wait`, `tail -f` - stream indefinitely - generic stream rule
- `Get-ChildItem -Recurse` / `Select-String -Recurse` on large trees - enumerates everything before returning; use rg.exe - generic enumeration rule
- [project-specific: build.bat / ship.bat containing pause; CLI tools without non-interactive flags]

## Time caps

- Single test file: 3-minute cap
- Full test suite: 10-minute cap
- Build scripts: 15-minute cap
- Git operations: 30-second cap
- [project-specific caps]

## Always rules

- Test suites run with non-interactive flags, non-blocking, under cap
- Git commands use `--no-pager`
- `npx`/`npm` commands use `--yes`
- Stderr redirected to file, never merged with `2>&1`
- File and content search uses rg.exe instead of recursive shell enumeration
- Stray processes stopped after every command execution
- Verbose output (>few KB) goes through script + redirect + file-read

## On-cap behavior

1. Kill the process tree (children and grandchildren), not just the parent
2. Record the command and cap in session PROBLEMS.md
3. Continue with the next step - never re-run the same command unbounded

## Kill procedure

Recursive Stop-ProcessTree: enumerate children by ParentProcessId, recurse, force-kill. After the kill, sweep for orphans by command-line pattern (their parent PID no longer maps to a running process).

## Findings feed

(extend with one entry per hang or near-hang: what, why, prevention)
```
