# SPEC: Windsurf Auto Model Switcher

**Doc ID**: AMSW-SP01
**Goal**: Document the model switching system for Windsurf Cascade
**Timeline**: Created 2026-01-26, updated 3x

## MUST-NOT-FORGET

- Model switch takes effect on user's NEXT message (not current)
- Tier definitions live in `!NOTES.md` and `switch-model.md` (not hardcoded here)
- German keyboards: Use F-keys (Ctrl+Shift+F9/F10), not Ctrl+Alt (AltGr conflict)
- Default to MODEL-HIGH when uncertain - quality over cost

## Table of Contents

1. [Components](#components)
2. [Skill: windsurf-auto-model-switcher](#skill-windsurf-auto-model-switcher)
3. [Workflow: switch-model](#workflow-switch-model)
4. [Rule: cascade-model-switching](#rule-cascade-model-switching)
5. [DevSystem Integration](#devsystem-integration)
6. [Cost Estimation](#cost-estimation)
7. [Implementation Status](#implementation-status)

## Components

The model switching system consists of three DevSystem pieces:

- **Skill** (`windsurf-auto-model-switcher`) - Scripts and registry for model switching mechanics
- **Workflow** (`switch-model.md`) - User-facing workflow for manual tier switching
- **Rule** (`cascade-model-switching.md`) - Guidelines for autonomous agent switching

## Skill: windsurf-auto-model-switcher

**Source**: `DevSystemV3.2/skills/windsurf-auto-model-switcher/`
**Deployed**: `.windsurf/skills/windsurf-auto-model-switcher/`

### Files

- `SKILL.md` - Skill documentation and usage
- `SETUP.md` - Keybinding installation (Ctrl+Shift+F9/F10)
- `UNINSTALL.md` - Removal instructions
- `select-windsurf-model-in-ide.ps1` - Main script for model selection
- `windsurf-model-registry.json` - 68 models with costs
- `update-model-registry/` - Workflow to refresh registry from UI

### Script: select-windsurf-model-in-ide.ps1

**Parameters:**
- `-Query` (required) - Model name or partial match
- `-DryRun` (optional) - Preview selection without execution
- `-WindowTitle` (optional) - Target window pattern (default: "*Windsurf*")

**Features:**
- Fuzzy matching with cost prioritization (prefers cheaper when tied)
- Default fallback to Claude Sonnet 4 if no match
- Bulletproof refocus via `Ctrl+Shift+A`
- German keyboard compatible (uses F-keys, not Ctrl+Alt)

**Usage:**
```powershell
# Select by partial name
.\select-windsurf-model-in-ide.ps1 -Query "opus 4.5 thinking"
.\select-windsurf-model-in-ide.ps1 -Query "sonnet 4.5"
.\select-windsurf-model-in-ide.ps1 -Query "gemini 3 flash medium"

# Preview without executing
.\select-windsurf-model-in-ide.ps1 -Query "haiku" -DryRun
```

### Prerequisites

1. Run `SETUP.md` to install keybindings
2. Restart Windsurf after setup
3. Verify with `Ctrl+Shift+F9` (model selector should appear)

## Workflow: switch-model

**Source**: `DevSystemV3.2/workflows/switch-model.md`
**Deployed**: `.windsurf/workflows/switch-model.md`

### Configuration (in workflow file)

```
MODEL-HIGH = "Claude Opus 4.5 (Thinking)"  [5x]
MODEL-MID  = "Claude Sonnet 4.5"           [2x]
MODEL-LOW  = "Gemini 3 Flash Medium"       [1x]
```

### Usage

```
/switch-model high   # or 'h' or 'MODEL-HIGH'
/switch-model mid    # or 'm' or 'MODEL-MID'
/switch-model low    # or 'l' or 'MODEL-LOW'
```

### Behavior

1. Maps tier argument to configured model query
2. Calls `select-windsurf-model-in-ide.ps1 -Query "[MODEL-*-QUERY]"`
3. Reports: "Switched to [MODEL-*]. Takes effect on next message."

## Rule: cascade-model-switching

**Source**: `DevSystemV3.2/rules/cascade-model-switching.md`
**Deployed**: `.windsurf/rules/cascade-model-switching.md`

### Purpose

Guidelines for autonomous agent model switching (not user-triggered).

### Safety Conditions (ALL required for auto-switch)

1. Windsurf instance in foreground
2. Our conversation open in Cascade
3. User NOT doing anything else (no typing, selecting, scrolling)
4. Cascade chat input is empty

**If ANY condition fails: Skip switch silently.**

### Switch-Back Pattern

After completing a task with different model, always switch back:
```
Start: Opus (planning) -> Switch: Sonnet (implementation) -> Switch back: Opus
```

### Model Hints in STRUT

Strategy sections may include hints:
```
|- Strategy: Analyze requirements, design solution
|   - Opus for analysis, Sonnet for implementation
```

Hints are recommendations - agent decides based on actual task.

## DevSystem Integration

### Tier Definitions (from !NOTES.md)

- **MODEL-HIGH** - Claude Opus 4.5 (Thinking) [5x] - Complex reasoning, specs, architecture
- **MODEL-MID** - Claude Sonnet 4.5 [2x] - Code verification, bug fixes, refactoring
- **MODEL-LOW** - Gemini 3 Flash Medium [1x] - Scripts, git, file ops (372 TPS, 78% SWE-Bench)

### Workflow to Tier Mapping

- `/prime`, `/commit`, `/session-*` - LOW (mechanical operations)
- `/recap`, `/verify`, `/test`, `/implement` - MID (standard tasks)
- `/build`, `/solve`, `/critique`, `/reconcile` - HIGH (complex reasoning)
- `/continue`, `/go` - varies (depends on task type)

### Integration Points

1. **User invokes** `/switch-model` workflow -> calls skill script -> model changes
2. **Agent follows** `cascade-model-switching.md` rule -> safety check -> calls script
3. **STRUT plans** may include model hints in Strategy section
4. **!NOTES.md** defines tier-to-model mapping (single source of truth)

## Cost Estimation

### Example Session Cost Comparison

**Without switching (all HIGH):** 10 steps x 5x = 50 credits

**With tier switching:**
- 3 LOW steps x 1x = 3 credits
- 2 HIGH steps x 5x = 10 credits
- 5 MID steps x 2x = 10 credits
- Total: 23 credits (54% savings)

### Switch Overhead

- Time: ~2 seconds per switch
- Cost: Free (switching has no credit cost)
- Risk: Context may differ slightly between models
- Recommendation: Batch at least 3 same-tier operations before switching

## Implementation Status

### Implemented [TESTED]

- Skill: `windsurf-auto-model-switcher` with fuzzy matching and dry-run
- Workflow: `/switch-model` with HIGH/MID/LOW tiers
- Rule: `cascade-model-switching.md` with safety conditions
- Registry: `windsurf-model-registry.json` with 68 models and costs
- Keybindings: `Ctrl+Shift+F9` (selector), `Ctrl+Shift+F10` (cycle)
- Refocus: `Ctrl+Shift+A` (bulletproof method)

### Not Implemented

- Automatic switching based on activity detection (safety concerns)
- Cascade hooks (unreliable - see AMSW-PR-006)

## Design Decisions

- **AMSW-DD-01**: Default to HIGH - Quality over cost. User explicitly opts into savings.
- **AMSW-DD-02**: Three-tier system - Simplified from 5 tiers. Easier to remember.
- **AMSW-DD-03**: No auto-switch during errors - Errors need full reasoning capability.
- **AMSW-DD-04**: Gemini 3 Flash for LOW - Best speed (372 TPS) and quality (78% SWE-Bench) at 1x.
- **AMSW-DD-05**: Fuzzy matching + cost priority - Partial names work, prefer cheaper on tie.

## Document History

**[2026-01-26 16:43]**
- Fixed: Locations now show Source (DevSystemV3.2) vs Deployed (.windsurf)

**[2026-01-26 16:41]**
- Renamed: `_SPEC_WINDSURF_AUTO_MODEL_SWITCHER.md`
- Added: MUST-NOT-FORGET section, Timeline field
- Fixed: Design Decision IDs to use AMSW-DD-XX format

**[2026-01-26 16:39]**
- Restructured to document skill, workflow, rule, and DevSystem integration
- Added component overview and file listings
- Documented all integration points

**[2026-01-26 16:36]**
- Updated to match actual implementation
- Simplified to 3 tiers (HIGH/MID/LOW)

**[2026-01-26 12:15]**
- Initial specification created
