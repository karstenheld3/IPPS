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
- TERMROBUSTNESS-EX-01: Output to files, read with file tool
- TERMROBUSTNESS-EX-02: Expected runtime stated, no runtime kill
- TERMROBUSTNESS-EX-03: Whole-tree kill by the supervised runner
- TERMROBUSTNESS-EX-04: Inline whitelist, everything else via `_agentwork/.tmp_` script and the supervised runner
- TERMROBUSTNESS-EX-05: Delete temp script and output files after consumption

Card Definition (CD)
- TERMROBUSTNESS-CD-01: Card created from agent template, never from scratch
- TERMROBUSTNESS-CD-02: Card contains all skeleton sections and no generic rules
- TERMROBUSTNESS-CD-03: Every entry traceable to evidence or generic rule
- TERMROBUSTNESS-CD-04: Fails card entry written at once on every failure

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
npm run build (through run-supervised.ps1; a dev server only on explicit user request, stopped after use, no orphans left)
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

## TERMROBUSTNESS-EX-01: Output to files, read with file tool

**BAD:** Long inline pipeline whose output returns through the terminal tool.

**GOOD:** Write a `_agentwork/.tmp_*.ps1`/`.py` script, run it through `run-supervised.ps1`, then `read_file` its `_log.txt`, `_out.txt`, `_err.txt`.

## TERMROBUSTNESS-EX-02: Expected runtime stated, no runtime kill

**BAD:**
```text
Run the test suite with a 10-minute limit and stop it when the limit is reached.
```
A suite that needs 11 minutes is ended at minute 10 and runs again: 21 minutes instead of 11.

**GOOD:**
```text
Run the test suite through run-supervised.ps1 with -Expected 200. Read the ALIVE lines while it runs; end it only on a hang verdict.
```

## TERMROBUSTNESS-EX-03: Whole-tree kill by the supervised runner

**BAD:** `Stop-Process -Id $pid -Force` or a recursive ParentProcessId walk (misses grandchildren that hold the pipe and orphans whose parent exited; HANGBENCH 24/27).

**GOOD:** `run-supervised.ps1` with processkit: the whole tree lives in one Job Object and ends when the script exits or when the agent creates the stop file after a hang verdict (HANGBENCH 26/27; open: a cancelled runner leaves its tree alive, HC-27).

## TERMROBUSTNESS-EX-04: Inline whitelist, everything else via `_agentwork/.tmp_` script and the supervised runner

Whitelist: `agent-behavior.md` Terminal Hang Prevention (single source, not repeated here).

**BAD:**
```powershell
Get-ChildItem -Recurse -Filter *.md | Where-Object { $_.Length -gt 10000 } | Select-Object FullName, Length
```

**GOOD:**
```powershell
pwsh -NoProfile -NonInteractive -File [AGENT_FOLDER]/skills/terminal-robustness/run-supervised.ps1 -Script _agentwork/.tmp_large_md.ps1 -Expected 10
```
Then `read_file` the `_log.txt` and `_out.txt` files.

## TERMROBUSTNESS-EX-05: Delete temp script and output files after consumption

**BAD:** `.tmp_large_md.ps1` and its `_out.txt` / `_err.txt` remain after the results were read and used.

**GOOD:** Delete the script and its output files in the same task once their content is consumed; `/cleanup` only catches leftovers.

## TERMROBUSTNESS-CD-01: Card created from agent template, never from scratch

**BAD:** A hand-written `__CARD_*-Robustness.md` with ad-hoc section names.

**GOOD:** A copy of `ClaudeCode/ROBUSTNESS_CARD_TEMPLATE.md` or `DevinCascade/ROBUSTNESS_CARD_TEMPLATE.md`, extended with project-specific entries.

## TERMROBUSTNESS-CD-02: Card contains all skeleton sections and no generic rules

**BAD:** A card with only a banned list, or a card that restates the whitelist, the runner call, or the hang verdict; a card that turns an expected runtime into a kill limit.

**GOOD:** Robustness card: Banned commands, Expected runtimes, Always rules, Agent tool limits. Fails card: Never again, Entries. Both matching `ROBUSTNESS_CARD_SKELETON.md`.

## TERMROBUSTNESS-CD-03: Every entry traceable to evidence or generic rule

**BAD:** `Banned: npm (hangs sometimes)`.

**GOOD:** `Banned: npm install without --yes (prompts on stdin) - generic stdin rule` or `- evidence: investigation log @I001.015`.

## TERMROBUSTNESS-CD-04: Fails card entry written at once on every failure

**BAD:** A `KILLED` run recorded only in chat memory, or written at the end of the prompt after a crash already lost it.

**GOOD:** Fails card entry and "Never again" line written right after the failure, in the Fails card of the working folder (created at the first failure); every later command, in chat tasks and prompts, is checked against the line.
