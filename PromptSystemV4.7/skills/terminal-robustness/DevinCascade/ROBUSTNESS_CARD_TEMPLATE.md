# Robustness Card Template (DevinCascade)

Re-usable card for Devin/Cascade agents. Copy to `_agentwork/__CARD_[TOPIC]-Robustness.md` of the current working folder and extend with project-specific entries. Defaults are tested or evidence-cited - replace bracketed placeholders. Generic rules (whitelist, supervised runner, hang verdict, hard bans) stay in `agent-behavior.md` Terminal Hang Prevention and are not copied here.

```markdown
# Robustness Card: [TOPIC]

## Banned commands

- Inline command with `;`, `|`, a loop, or nested quotes (`"...$(...)"`) - unterminated string leaves pwsh at the `>>` continuation prompt forever - evidence: HANGBENCH HC-10
- `git log` / `git diff` / `git show` / `git blame` without `--no-pager` - launches pager, blocks on stdin - generic pager rule
- `npm install` without `--yes` or `--ci` - prompts on stdin - generic stdin rule
- `npx <tool>` without `--yes` - prompts to install package - generic stdin rule
- `npm create <tool> ... -- <flags> --yes` - `--yes` after `--` reaches the scaffold tool, not the runner; "Ok to proceed?" install prompt still waits on stdin - evidence: @I001.025
- `node` without a script argument - starts REPL, waits on stdin - generic stdin rule
- `Get-Credential` - waits for interactive input - generic stdin rule
- `Wait-Process` without `-Timeout` - waits forever - generic unbounded-child rule
- `Get-Content -Wait`, `tail -f` - stream indefinitely - generic stream rule
- `Get-ChildItem -Recurse` / `Select-String -Recurse` on large trees - full enumeration before return; use rg.exe - generic enumeration rule
- `Get-Content | Select-Object -First N` on large or locked files - pipeline buffers before stop; use `-TotalCount` - tested
- Cascade `search_web` / `read_url_content` on `gesetze-im-internet.de` - crashes the conversation; use Playwright
- [project-specific: build.bat / ship.bat containing pause; CLI tools without non-interactive flags; dev servers]

## Expected runtimes

Typical seconds per command class, passed as `-Expected` to `run-supervised.ps1`. They start the liveness check and feed the runtime check; no command is ended for exceeding them. Starting values - replace with measured project values:
- Single test file: 60 s; none
- Full test suite: 200 s; none
- Build scripts: 300 s; none
- Git operations: 10 s; none
- Type checking: 100 s; no output until the end
- [project-specific class]: [N] s; [known silent phase or none]

## Always rules

- Test suites run with `--ci` / `--timeout` (no watch mode)
- Git commands use `--no-pager`
- `npx` commands use `--yes`; in two-layer commands (`npm create` / `npx` + `--`) the runner-level `--yes` goes BEFORE `--` - evidence: @I001.025
- File and content search uses `grep_search`; outside the workspace rg.exe inside the tmp script, never recursive shell enumeration
- [project-specific safe alternatives]

## Agent tool limits

[copy verbatim the bullet list of `devin-cascade.md` section "Tool-Call Payload Limit"; do not edit values in the card]
```

Failures of a run go to the Fails card (`ROBUSTNESS_CARD_SKELETON.md` Fails block), not into this card; its "Never again" lines are promoted into "Banned commands" per the Fails card rules (final checkpoint prompt, or more than about 15 lines).
