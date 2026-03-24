---
description: Switch Cascade AI model tier (HIGH, MID, LOW)
---

# Switch Model Workflow

Switch AI model tier. Direct execution - no file reads.

## Configuration

```
MODEL-HIGH = "Claude Opus 4.5 (Thinking)" / QUERY = "opus 4.5 thinking"
MODEL-MID  = "Claude Sonnet 4.5"          / QUERY = "sonnet 4.5"
MODEL-LOW  = "Gemini 3 Flash Medium"      / QUERY = "gemini 3 flash medium"
```

## Required Skills

- `@skills:windsurf-auto-model-switcher` for model switching

## Usage

```
/switch-model high|h | mid|m | low|l
```

## Execute

Map tier argument to query, run from `.windsurf/skills/windsurf-auto-model-switcher/`:

```powershell
.\select-windsurf-model-in-ide.ps1 -Query "[QUERY]"
```

Report: "Switched to [MODEL-*]. Takes effect on next message."

## Notes

- Takes effect on user's NEXT message
- Edit this workflow to change tier→model mapping
- Safety checks only for autonomous switching (see `cascade-model-switching.md`)