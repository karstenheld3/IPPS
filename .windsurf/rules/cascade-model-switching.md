# Cascade Model Switching

Automatically switch AI models based on task type and STRUT hints.

## Model Hints

STRUT Strategy sections may include model hints:
```
├─ Strategy: Analyze requirements, design solution
│   - Opus for analysis, Sonnet for implementation
```

Hints are recommendations - agent decides based on actual task.

## Default Model Selection

When no STRUT hint exists, use task-based selection:
- **Planning/Analysis**: Claude Opus 4.5 (Thinking)
- **Implementation/Bugfix**: Claude Sonnet 4.5
- **Chores (git, files)**: Claude Haiku 4.5

## Safety Conditions (ALL required)

Before auto-switching, verify via screenshot:
1. Windsurf window is foreground
2. Cascade panel visible with our conversation
3. User not actively typing in editor
4. Cascade chat input is empty

**If any condition fails: Skip switch silently.**

## Switching Procedure

1. Take screenshot using `@windows-desktop-control` skill
2. Analyze screenshot for safety conditions
3. If safe: Run `select-windsurf-model-in-ide.ps1 -Query "<model>"`
4. If unsafe: Do not switch (user is busy)
