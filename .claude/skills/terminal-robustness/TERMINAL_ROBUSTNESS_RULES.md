# Terminal Robustness Rules

Output standards for robustness cards and terminal command patterns. Consumed by `/verify`.

**Writing quality:** Apply `APAPALAN_RULES.md`. Key rules: APAPL-PR-07 specific, APAPL-NM-01 one name per concept, APAPL-PR-09 consistent patterns.

## Rule Index

Hang Guards (HG)
- TERMROBUSTNESS-HG-01: No stream merge on stderr-heavy commands
- TERMROBUSTNESS-HG-02: No stdin, pager, or key waits
- TERMROBUSTNESS-HG-03: No unbounded background children
- TERMROBUSTNESS-HG-04: No recursive shell enumeration on large trees

Execution Patterns (EX)
- TERMROBUSTNESS-EX-01: Redirect verbose output to file, read with file tool
- TERMROBUSTNESS-EX-02: Time cap on every process-running command
- TERMROBUSTNESS-EX-03: Process-tree kill with survivor sweep
- TERMROBUSTNESS-EX-04: Inline whitelist, everything else via `_agentwork/.tmp_` script
- TERMROBUSTNESS-EX-05: Delete temp script and output files after consumption

Card Definition (CD)
- TERMROBUSTNESS-CD-01: Card created from agent template, never from scratch
- TERMROBUSTNESS-CD-02: Card contains all six skeleton sections
- TERMROBUSTNESS-CD-03: Every entry traceable to evidence or generic rule
- TERMROBUSTNESS-CD-04: Findings Feed updated on every hang or near-hang

## TERMROBUSTNESS-HG-01: No stream merge on stderr-heavy commands

**BAD:**
```powershell
npm install 2>&1
```

**GOOD:**
```powershell
npm install 2>"_agentwork/.tmp_install_stderr.txt"
```

## TERMROBUSTNESS-HG-02: No stdin, pager, or key waits

**BAD:**
```powershell
git log
```

**GOOD:**
```powershell
git --no-pager log -n 20
```

**BAD:**
```powershell
npm create astro@latest .tmp_astro_test -- --template minimal --yes
```

**GOOD:**
```powershell
npm create --yes astro@latest .tmp_astro_test -- --template minimal
```

The `--yes` after `--` reaches the scaffold tool, not npm - the runner's own "Ok to proceed?" install prompt still waits on stdin.

## TERMROBUSTNESS-HG-03: No unbounded background children

**BAD:**
```powershell
npm run dev
```

**GOOD:**
```powershell
npm run dev (non-blocking, cap 60s, then kill process tree and verify no orphans)
```

## TERMROBUSTNESS-HG-04: No recursive shell enumeration on large trees

**BAD:**
```powershell
Get-ChildItem -Recurse | Select-String "pattern"
```

**GOOD:**
```powershell
& $rg.FullName "pattern" "src/"
```

## TERMROBUSTNESS-EX-01: Redirect verbose output to file, read with file tool

**BAD:** Long inline pipeline whose output returns through the terminal tool.

**GOOD:** Write a `_agentwork/.tmp_*.ps1`/`.py` script, redirect all output to `_agentwork/.tmp_` files, run it, then `read_file` the results.

## TERMROBUSTNESS-EX-02: Time cap on every process-running command

**BAD:**
```text
Run the test suite.
```

**GOOD:**
```text
Run the test suite non-blocking with a 10-minute cap. On cap: kill the process tree, record command and cap in PROBLEMS.md, continue.
```

## TERMROBUSTNESS-EX-03: Process-tree kill with survivor sweep

**BAD:** `Stop-Process -Id $pid -Force` (kills only the parent; grandchildren keep the pipe open).

**GOOD:** Recursive `Stop-ProcessTree` (children and grandchildren), then sweep by command-line pattern for orphans whose parent PID no longer maps to a running process.

## TERMROBUSTNESS-EX-04: Inline whitelist, everything else via `_agentwork/.tmp_` script

Inline only if ALL apply: single command, no `|`, no `;`, no loop or script block, no `2>&1`, under 200 characters, under 10 seconds, under 50 output lines.

**BAD:**
```powershell
Get-ChildItem -Recurse -Filter *.md | Where-Object { $_.Length -gt 10000 } | Select-Object FullName, Length
```

**GOOD:**
```powershell
pwsh -NoProfile -NonInteractive -File _agentwork/.tmp_large_md.ps1 > _agentwork/.tmp_large_md_out.txt 2> _agentwork/.tmp_large_md_err.txt
```
Then `read_file` both output files.

## TERMROBUSTNESS-EX-05: Delete temp script and output files after consumption

**BAD:** `.tmp_large_md.ps1` and its `_out.txt` / `_err.txt` remain after the results were read and used.

**GOOD:** Delete the script and its output files in the same task once their content is consumed; `/cleanup` only catches leftovers.

## TERMROBUSTNESS-CD-01: Card created from agent template, never from scratch

**BAD:** A hand-written `__CARD_*-Robustness.md` with ad-hoc section names.

**GOOD:** A copy of `ClaudeCode/ROBUSTNESS_CARD_TEMPLATE.md` or `DevinCascade/ROBUSTNESS_CARD_TEMPLATE.md`, extended with project-specific entries.

## TERMROBUSTNESS-CD-02: Card contains all six skeleton sections

**BAD:** A card with only a banned list (no caps, no on-cap behavior).

**GOOD:** Banned Commands, Time Caps, Always Rules, On-Cap Behavior, Kill Procedure, Findings Feed - all present, matching `ROBUSTNESS_CARD_SKELETON.md`.

## TERMROBUSTNESS-CD-03: Every entry traceable to evidence or generic rule

**BAD:** `Banned: npm (hangs sometimes)`.

**GOOD:** `Banned: npm install without --yes (prompts on stdin) - generic stdin rule` or `- evidence: investigation log @I001.015`.

## TERMROBUSTNESS-CD-04: Findings Feed updated on every hang or near-hang

**BAD:** A hang killed and recorded only in chat memory.

**GOOD:** New card entry: what hung, why, prevention - so later sessions load it at startup.
