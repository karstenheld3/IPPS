# Robustness Card Template (ClaudeCode)

Re-usable card for Claude Code agents. Copy to `_agentwork/__CARD_[TOPIC]-Robustness.md` of the current working folder and extend with project-specific entries. Generic defaults only - replace bracketed placeholders. Generic rules (whitelist, supervised runner, hang verdict, hard bans) stay in `agent-behavior.md` Terminal Hang Prevention and are not copied here.

```markdown
# Robustness Card: [TOPIC]

## Banned commands

- Inline command with `;`, `|`, a loop, or nested quotes - unterminated string can leave pwsh at the `>>` continuation prompt - evidence: HANGBENCH HC-10
- `git log` / `git diff` / `git show` without `--no-pager` - launches pager, waits on stdin - generic pager rule
- `npm install` without `--yes` - prompts for confirmation on stdin - generic stdin rule
- `npx <tool>` without `--yes` - prompts to install package - generic stdin rule
- `npm create <tool> ... -- <flags> --yes` - `--yes` after `--` reaches the scaffold tool, not the runner's install prompt - generic stdin rule
- `Get-Credential` - waits for interactive input - generic stdin rule
- `Wait-Process` without `-Timeout` - waits forever - generic unbounded-child rule
- `Get-Content -Wait`, `tail -f` - stream indefinitely - generic stream rule
- `Get-ChildItem -Recurse` / `Select-String -Recurse` on large trees - enumerates everything before returning; use rg.exe - generic enumeration rule
- [project-specific: build.bat / ship.bat containing pause; CLI tools without non-interactive flags]

## Expected runtimes

Typical seconds per command class, passed as `-Expected` to `run-supervised.ps1`. They start the liveness check and feed the runtime check; no command is ended for exceeding them. Starting values - replace with measured project values:
- Single test file: 60 s; none
- Full test suite: 200 s; none
- Build scripts: 300 s; none
- Git operations: 10 s; none
- [project-specific class]: [N] s; [known silent phase or none]

## Always rules

- Test suites run with non-interactive flags (no watch mode)
- Git commands use `--no-pager`
- `npx`/`npm` commands use `--yes`, placed before `--` in two-layer commands (`npm create`, `npx`)
- File and content search uses rg.exe inside the tmp script instead of recursive shell enumeration
- [project-specific safe alternatives]

## Agent tool limits

[copy verbatim the bullet list of `tools-and-skills.md` section "Large File Writes"; do not edit values in the card]
```

Failures of a run go to the Fails card (`ROBUSTNESS_CARD_SKELETON.md` Fails block), not into this card; its "Never again" lines are promoted into "Banned commands" per the Fails card rules (final checkpoint prompt, or more than about 15 lines).
