# Cascade Model Switching

Automatically switch model tier at the end of each response to optimize costs.

## Tier Definitions

Read from workspace `!NOTES.md` under `## Cascade Model Tiers`:
- **HIGH** = Claude Opus 4.5 (Thinking) - Complex reasoning, specs, architecture
- **MID** = Claude Sonnet 4.5 - Code verification, bug fixes, refactoring
- **CHORES** = Claude Haiku 4.5 - Scripts, git, file ops, monitoring

## Activity Mapping

- **HIGH**: Writing documents, analyzing complex problems, architecture, gate evaluations
- **MID**: Code verification, bug fixes, refactoring, standard implementation
- **CHORES**: Running scripts, git commit, file reads, session archive

## Required Behavior

At the END of every response:

1. Assess what the NEXT user request will likely need
2. Map to appropriate tier (HIGH/MID/CHORES)
3. Call the model switcher script:

```powershell
& "[WORKSPACE]/DevSystemV3.2/skills/windsurf-auto-model-switcher/select-windsurf-model-in-ide.ps1" -Query "<model>"
```

**Model queries by tier:**
- HIGH: `"opus 4.5 thinking"`
- MID: `"sonnet 4.5"`
- CHORES: `"haiku 4.5"`

**If uncertain, default to HIGH.**

## Example

After completing a git commit (CHORES task), if the next task looks like code review:

```powershell
& "E:\Dev\IPPS\DevSystemV3.2\skills\windsurf-auto-model-switcher\select-windsurf-model-in-ide.ps1" -Query "sonnet 4.5"
```
