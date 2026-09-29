# Robustness Card Skeleton

Canonical structure for robustness cards. Copy an agent `ROBUSTNESS_CARD_TEMPLATE.md` (not this skeleton) when creating a card; `/verify` checks card instances against this structure.

```markdown
# Robustness Card: [TOPIC]

## Banned commands

- [command pattern] - [why it hangs: stdin wait / pager / unbounded child / merge operator / recursive enumeration]
- [source: generic rule, project probe, or evidence entry]

## Time caps

- [command class, e.g. single test file]: [N]-minute cap
- [command class, e.g. full test suite]: [N]-minute cap
- [command class, e.g. build]: [N]-minute cap
- [command class, e.g. git operations]: [N]-second cap

## Always rules

- [safe alternative for each banned class, e.g. test suites run with --ci non-blocking]
- [redirect rule, e.g. stderr redirected to file, never merged]
- [cleanup rule, e.g. stray processes stopped after every run]

## On-cap behavior

1. [kill step]
2. [record step]
3. [continue step]

## Kill procedure

[kill method: process-tree kill, survivor sweep by command-line pattern]

## Findings feed

### [N]. [Title]
- **When**: [date/session]
- **What hung or nearly hung**: [command]
- **Why**: [mechanism]
- **Prevention**: [new banned entry, cap adjustment, or pattern change]
```
