# Cascade Model Switching

Automatically switch model tier at the end of each response to optimize costs.

## Configuration

Tier definitions and activity mappings are in workspace `!NOTES.md` under `## Cascade Model Tiers`.

## Required Behavior

At the END of every response:

1. Assess what the NEXT user request will likely need
2. Map to appropriate tier (HIGH/MID/CHORES)
3. Call the model switcher script:

```powershell
& "[WORKSPACE]/DevSystemV3.2/skills/windsurf-auto-model-switcher/select-windsurf-model-in-ide.ps1" -Query "<model>"
```
**If uncertain, default to HIGH.**

## Example

After completing a git commit (CHORES task), if the next task looks like code review:

```powershell
& "E:\Dev\IPPS\DevSystemV3.2\skills\windsurf-auto-model-switcher\select-windsurf-model-in-ide.ps1" -Query "sonnet 4.5"
```
