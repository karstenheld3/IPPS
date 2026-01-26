---
trigger: always_on
---

# Cascade Model Switching

Automatically recommend model tier for the next response to optimize costs.

## Configuration Location

Model tier definitions are in **workspace `!NOTES.md`** or **session `NOTES.md`**.
Look for the `## Cascade Model Tiers` section.

If no configuration found, use defaults:
- HIGH = Claude Opus 4.5 (Thinking)
- MID = Claude Sonnet 4.5
- CHORES = SWE-1.5 Fast

## Activity to Tier Mapping

**HIGH**: Writing documents, analyzing complex problems, architecture, gate evaluations
**MID**: Code verification, bug fixes, refactoring, standard implementation
**CHORES**: Running scripts, git commit, file reads, session archive

## Required Behavior

At the END of every response, you MUST:

1. Assess what the NEXT user request will likely need
2. Write ONLY the tier name to file: `.windsurf/next-model.txt`
3. Use this exact PowerShell command:
   ```
   Set-Content -Path ".windsurf/next-model.txt" -Value "TIER" -NoNewline
   ```
   Replace TIER with the tier name from NOTES.md config.

**If uncertain, default to HIGH.**
