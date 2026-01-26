# SPEC: Cascade Auto Model Switcher

**Doc ID**: AMSW-SP01
**Goal**: Switch Cascade models via `/switch-model` workflow to optimize cost while maintaining quality

**Depends on:**
- `windsurf-auto-model-switcher` skill for model switching mechanics
- `switch-model.md` workflow for tier-based switching

## MUST-NOT-FORGET

- Model switch takes effect on user's NEXT message (not current)
- Model switches add latency (~2s each) - batch similar activities
- Default to MODEL-HIGH when uncertain
- Never downgrade during critical paths (gate checks, error handling)
- Tier definitions live in `!NOTES.md` and `switch-model.md` (not hardcoded here)

## Table of Contents

1. [Model Tiers](#model-tiers)
2. [Activity Mapping](#activity-mapping)
3. [Integration Points](#integration-points)
4. [Cost Estimation](#cost-estimation)
5. [Implementation Status](#implementation-status)

## Model Tiers

### Tier Definitions (from !NOTES.md)

- **MODEL-HIGH** (Default)
  - Model: Claude Opus 4.5 (Thinking)
  - Cost: 5x
  - Use: Complex reasoning, specs, architecture, gate evaluations

- **MODEL-MID**
  - Model: Claude Sonnet 4.5
  - Cost: 2x
  - Use: Code verification, bug fixes, refactoring, implementation

- **MODEL-LOW**
  - Model: Gemini 3 Flash Medium
  - Cost: 1x
  - Speed: 372 TPS, 78% SWE-Bench
  - Use: Scripts, git operations, file reads, session archive

### Tier Selection Priority

When multiple activities overlap, use highest tier:
```
HIGH > MID > LOW
```

## Activity Mapping

### Activity to Tier Matrix

**HIGH (5x) - Complex Reasoning**
- Writing documents (SPEC, IMPL, TEST, INFO)
- Analyzing complex problems
- Architecture decisions
- Gate evaluations
- `/critique`, `/reconcile`, `/build`, `/solve`

**MID (2x) - Standard Tasks**
- Verifying existing code
- Fixing bugs (after root cause identified)
- Code refactoring
- Standard `/implement` steps
- `/verify`, `/test`

**LOW (1x) - Fast Tasks**
- Running scripts
- Git operations (commit, status)
- File reads/writes
- Session management
- `/prime`, `/commit`, `/session-archive`, `/session-close`

### Workflow to Tier Mapping

- `/prime` - LOW (reading files, building context)
- `/recap` - MID (analysis but not creation)
- `/continue` - varies (depends on task type)
- `/go` - varies (orchestration is LOW, tasks vary)
- `/build` - HIGH (complex code creation)
- `/solve` - HIGH (research and analysis)
- `/implement` - MID (standard implementation)
- `/verify` - MID (checking, not creating)
- `/critique` - HIGH (deep analysis)
- `/reconcile` - HIGH (decision making)
- `/commit` - LOW (mechanical git operations)
- `/test` - MID (running and analyzing tests)
- `/session-*` - LOW (session management)

## Integration Points

### 1. Manual Switching via Workflow

User or agent invokes `/switch-model` workflow:

```
/switch-model high   # Switch to Claude Opus 4.5 (Thinking)
/switch-model mid    # Switch to Claude Sonnet 4.5
/switch-model low    # Switch to Gemini 3 Flash Medium
```

Aliases: `h`, `m`, `l` or `MODEL-HIGH`, `MODEL-MID`, `MODEL-LOW`

### 2. Script Execution

The workflow calls `select-windsurf-model-in-ide.ps1`:

```powershell
# With fuzzy matching
.\select-windsurf-model-in-ide.ps1 -Query "opus 4.5 thinking"

# Dry-run mode (preview only)
.\select-windsurf-model-in-ide.ps1 -Query "sonnet" -DryRun
```

**Script features:**
- Fuzzy matching with cost prioritization
- `-DryRun` mode for safe preview
- Default fallback to Claude Sonnet 4 if no match
- Bulletproof refocus via `Ctrl+Shift+A`

### 3. Batch Optimization (Advisory)

Group consecutive same-tier steps to minimize switches:

```markdown
## Optimized Sequence

/switch-model low
1. Read session files
2. Run git status
3. List directory

/switch-model high
4. Analyze problem
5. Write spec section

/switch-model mid
6. Implement fix
7. Verify fix
```

**Recommendation**: Batch at least 3 same-tier operations before switching.

## Cost Estimation

### Example Session Cost Comparison

**Without switching (all HIGH):**
```
10 steps x 5x = 50 credits
```

**With tier switching:**
```
3 LOW steps x 1x = 3 credits
2 HIGH steps x 5x = 10 credits
5 MID steps x 2x = 10 credits
Total: 23 credits (54% savings)
```

### Switch Overhead

Each model switch:
- Time: ~2 seconds
- No credit cost (switching is free)
- Risk: Context may be slightly different between models

## Implementation Status

### Implemented [TESTED]

- `/switch-model` workflow with HIGH/MID/LOW tiers
- `select-windsurf-model-in-ide.ps1` with fuzzy matching and dry-run
- `windsurf-model-registry.json` with 68 models and costs
- Bulletproof refocus via `Ctrl+Shift+A`
- German keyboard compatible keybindings (`Ctrl+Shift+F9/F10`)

### Not Implemented

- Automatic switching based on activity detection
- STRUT plan annotations with `[MODEL:tier]`
- Cascade hooks (unreliable - see AMSW-PR-006)

## Design Decisions

### DD-01: Default to HIGH

Rationale: Quality over cost. User explicitly opts into cost savings.

### DD-02: Three-tier system (HIGH/MID/LOW)

Rationale: Simplified from 5 tiers. CHORES and IMAGE merged into LOW. Easier to remember and use.

### DD-03: No auto-switch during error handling

Rationale: Errors need full reasoning capability. Never downgrade when things go wrong.

### DD-04: Gemini 3 Flash Medium for LOW tier

Rationale: Best balance of speed (372 TPS) and quality (78% SWE-Bench) at 1x cost.

### DD-05: Fuzzy matching with cost prioritization

Rationale: User can type partial model names. When multiple matches, prefer cheaper option.

## Document History

**[2026-01-26 16:36]**
- Updated to match actual implementation
- Simplified to 3 tiers (HIGH/MID/LOW)
- Removed unimplemented features (CHORES, IMAGE, auto-annotations)
- Added implementation status section
- Updated DD-02, DD-04, DD-05

**[2026-01-26 12:15]**
- Initial specification created
