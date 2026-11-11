# Robustness Card Skeleton

Canonical structure of the two command cards. Copy an agent `ROBUSTNESS_CARD_TEMPLATE.md` for the Robustness card and the Fails block below for the Fails card; `/verify` checks card instances against this structure.

Cards hold only project- and run-specific content. Generic rules (inline whitelist, supervised runner, monitoring, hang verdict, runtime check, hard bans) live in `agent-behavior.md` Terminal Hang Prevention and are never copied into a card.

## Robustness card (per working folder, kept until `/cleanup`)

```markdown
# Robustness Card: [TOPIC]

## Banned commands

- [command pattern] - [why it hangs: stdin wait / pager / unbounded child / merge operator / recursive enumeration] - [source: generic rule, project probe, evidence entry, or promoted Fails entry FL-NN]

## Expected runtimes

- [command class, e.g. single test file]: [N] s; [known silent phase, e.g. "no output until the summary", or none] (passed as `-Expected` to `run-supervised.ps1`; starts the liveness check and feeds the runtime check, never a kill limit)

## Always rules

- [project-specific safe alternative for each banned class, e.g. test suites run with --ci]

## Agent tool limits

[verbatim copy of the writing agent's (= executing agent's) agent-specific rule file, section Tool-Call Payload Limit; if absent, `tools-and-skills.md` Large File Writes - never edited in the card]
```

## Fails card (per working folder, kept until `/cleanup`; created by `/write-prompts` or by the agent at the first failure)

```markdown
# Fails Card: [TOPIC]

## Never again

- [command shape + trigger] -> [complete replacement the agent can run as written] (FL-[NN])

## Entries

### FL-[NN]: [short title]
- **Prompt**: [NN] of [sequence file]
- **Command**: [exact command or tmp script name]
- **Class**: process hang / completion miss / error exit / runtime overrun / runner error / parse error / tool-call drop / repeat after failure
- **Expected / actual**: [N] s / [N] s (`elapsed=` from the runner log)
- **Hang evidence** (class process hang only): [the wait shown in the last output lines, or the unchanged `ALIVE` values and their time span]
- **Root cause**: [mechanism] [VERIFIED or ASSUMED]
- **Fix**: [what was changed to continue]
- **Never again**: [pattern] -> [replacement]
```

Fails card rules:
- Write the entry and its "Never again" line immediately after the failure, before any other step; chat tasks and prompt sequences of the working folder use the same card
- Pattern = command shape + trigger, not one exact command; replacement = complete alternative that runs as written (tool, call form, where completion is read)
- One line per root cause: a second failure with the same root cause extends the existing line
- Command shapes only: replace secret values (tokens, keys, passwords) with `[SECRET]`
- A command is never ended for its runtime. Class process hang requires hang evidence; ending a command that still showed progress is itself a failure (class process hang, root cause "false hang verdict")
- Runtime overrun (`DONE`, elapsed far above expected): the result is used, never re-run; the entry records the cause, and the Robustness card gets the corrected expected runtime
- Same failure twice in one prompt or chat task: stop it with a PROBLEMS.md entry naming the Fails entry ID
- Promotion to the Robustness card banned list: in the final checkpoint prompt of each prompts file, and when the list exceeds about 15 lines
- `/cleanup` deletes both cards; before that, lines that recur or apply beyond the project are carried out, generalized (no paths, names, values): in IPPS into the agent `ROBUSTNESS_CARD_TEMPLATE.md`, in other workspaces into workspace `FAILS.md`
