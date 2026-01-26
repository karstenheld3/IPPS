# Discover Windsurf Models Workflow

This workflow runs in Cascade to discover all available models and their costs.

## Prerequisites

- Windsurf running with Cascade panel visible
- Custom keybinding `Ctrl+Shift+F9` installed (see ../SETUP.md)

## Workflow Steps

### Phase 1: Initial Screenshot

1. Run `step1-open-selector.ps1` to open model selector and take screenshot
2. Analyze screenshot to determine:
   - How many models are visible in the popup (typically 4-6)
   - Extract model names and costs from visible list
3. Record models seen so far

### Phase 2: Scroll and Capture Loop

4. Run `step2-scroll-and-capture.ps1 -ScrollCount N` where N = visible model count
5. Analyze new screenshot to extract model names and costs
6. If we see a model we already recorded -> STOP (reached end)
7. Otherwise, record new models and go to step 4

### Phase 3: Build Output

8. Run `step3-close-selector.ps1` to close selector
9. Build `windsurf-model-registry.json` with all discovered models

## Output Format

Output must follow JSON-RULES.md:
- 2-space indentation
- snake_case field names
- One model per line for readability

```json
{
  "_version": "1.0",
  "_updated": "2026-01-26",
  "_source": "discovered from Windsurf model selector UI",
  "models": [
    { "name": "Claude 3.5 Sonnet",           "cost": "2x"   },
    { "name": "Claude 3.7 Sonnet",           "cost": "3x"   },
    { "name": "Claude 3.7 Sonnet (Thinking)", "cost": "3x"   }
  ]
}
```

## Cascade Instructions

When running this workflow:

1. Use `run_command` to execute PowerShell scripts
2. Use `read_file` to view screenshots
3. Visually analyze each screenshot to extract model names and costs
4. Keep track of all models seen to detect duplicates
5. Output final JSON when complete
