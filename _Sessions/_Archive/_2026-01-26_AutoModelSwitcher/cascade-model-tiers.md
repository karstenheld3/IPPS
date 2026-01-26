# Cascade Model Tiers Rule

**Goal**: Define model tiers and activity mappings for cost-optimized Cascade usage

## Model Tier Definitions

```
CASCADE-MODEL-HIGH    = Claude Opus 4.5 (Thinking)  [5x]  - Complex reasoning
CASCADE-MODEL-MID     = Claude Sonnet 4.5           [2x]  - Standard tasks
CASCADE-MODEL-LOW     = Claude Haiku 4.5            [1x]  - Simple tasks
CASCADE-MODEL-CHORES  = SWE-1.5 Fast                [0.5x] - Automation
CASCADE-MODEL-IMAGE   = GPT-4.1                     [1x]  - Visual tasks
CASCADE-MODEL-DEFAULT = CASCADE-MODEL-HIGH
```

## Activity to Tier Mapping

### HIGH (5x) - Use for:
- Writing documents (SPEC, IMPL, TEST, INFO)
- Verifying documents against specs
- Writing new code (architecture, new features)
- Analyzing complex problems
- Gate evaluations and phase transitions
- `/critique`, `/reconcile`, `/build`, `/solve`

### MID (2x) - Use for:
- Code verification and review
- Bug fixes (after diagnosis)
- Refactoring existing code
- `/verify` (code), `/implement`, `/test`
- Standard edits and updates

### LOW (1x) - Use for:
- Formatting and style fixes
- Comment updates
- Simple renames and moves
- Quick lookups

### CHORES (0.5x) - Use for:
- Running scripts and commands
- Monitoring output
- File operations
- Git operations
- `/prime`, `/commit`, `/session-archive`

### IMAGE (1x) - Use for:
- Screenshot analysis
- UI element detection
- Visual verification

## Plan Annotation

When creating execution sequences, annotate steps:

```markdown
## Execution Sequence

1. [CHORES] Read session files
2. [HIGH] Analyze problem
3. [MID] Implement fix
4. [CHORES] Run tests
5. [MID] Verify results
6. [CHORES] Commit
```

## Switch Protocol

1. **Before step**: Check if tier change needed
2. **Switch**: Output `[SWITCH → TIER]` and run: `.\select-windsurf-model-in-ide.ps1 -Query "[model name]"`
3. **After sequence**: Always restore DEFAULT

## Rules

- Default tier is HIGH (quality over cost)
- Never downgrade during error handling
- Batch 3+ same-tier operations before switching
- User can override with `[MODEL:TIER!]` annotation
