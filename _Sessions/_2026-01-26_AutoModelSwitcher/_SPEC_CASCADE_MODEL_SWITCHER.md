# SPEC: Cascade Auto Model Switcher

**Doc ID**: CAMS-SP01
**Goal**: Proactively switch Cascade models during plan execution to optimize cost while maintaining quality

**Depends on:**
- `windsurf-auto-model-switcher` skill [AMSW] for model switching mechanics
- `devsystem-core.md` for workflow integration points

## MUST-NOT-FORGET

- Always return to DEFAULT model after completing a sequence
- Model switches add latency (~2s each) - batch similar activities
- User can override with `[MODEL:tier]` annotation in plans
- Never downgrade during critical paths (gate checks, error handling)

## Table of Contents

1. [Model Tiers](#model-tiers)
2. [Activity Mapping](#activity-mapping)
3. [Integration Points](#integration-points)
4. [Plan Annotation Syntax](#plan-annotation-syntax)
5. [Cost Estimation](#cost-estimation)
6. [Implementation Strategy](#implementation-strategy)

## Model Tiers

### Tier Definitions

- **CASCADE-MODEL-HIGH** (Default)
  - Model: Claude Opus 4.5 (Thinking)
  - Cost: 5x
  - Use: Complex reasoning, architecture, spec writing

- **CASCADE-MODEL-MID**
  - Model: Claude Sonnet 4.5
  - Cost: 2x
  - Use: Code verification, bug fixes, standard tasks

- **CASCADE-MODEL-LOW**
  - Model: Claude Haiku 4.5
  - Cost: 1x
  - Use: Simple edits, formatting, quick lookups

- **CASCADE-MODEL-CHORES**
  - Model: SWE-1.5 Fast
  - Cost: 0.5x
  - Use: Script execution, file operations, monitoring

- **CASCADE-MODEL-IMAGE**
  - Model: GPT-4.1
  - Cost: 1x
  - Use: Screenshot analysis, UI verification, visual tasks

### Tier Selection Priority

When multiple activities overlap, use highest tier:
```
HIGH > MID > IMAGE > LOW > CHORES
```

## Activity Mapping

### Activity to Tier Matrix

**HIGH (5x) - Complex Reasoning**
- Writing documents (SPEC, IMPL, TEST, INFO)
- Verifying documents
- Writing new code (not edits)
- Analyzing complex problems
- Architecture decisions
- Gate evaluations
- `/critique`, `/reconcile`

**MID (2x) - Standard Tasks**
- Verifying existing code
- Fixing bugs (after root cause identified)
- Code refactoring
- `/verify` (code context)
- Standard `/implement` steps

**LOW (1x) - Simple Tasks**
- Formatting changes
- Comment updates
- Simple renames
- File moves
- Quick lookups

**CHORES (0.5x) - Automation**
- Running planned scripts
- Monitoring execution output
- File system operations
- Git operations (commit, status)
- `/session-archive`, `/session-close` (mechanical steps)

**IMAGE (1x) - Visual Tasks**
- Screenshot analysis
- UI element detection
- Visual verification
- Image-based workflows

### Workflow to Tier Mapping

| Workflow | Default Tier | Notes |
|----------|--------------|-------|
| `/prime` | CHORES | Reading files, building context |
| `/recap` | MID | Analysis but not creation |
| `/continue` | varies | Depends on task type |
| `/go` | varies | Orchestration is CHORES, tasks vary |
| `/build` | HIGH | Complex code creation |
| `/solve` | HIGH | Research and analysis |
| `/implement` | MID→HIGH | Depends on step complexity |
| `/verify` | MID | Checking, not creating |
| `/critique` | HIGH | Deep analysis |
| `/reconcile` | HIGH | Decision making |
| `/commit` | CHORES | Mechanical git operations |
| `/transcribe` | MID | Text extraction |
| `/test` | MID | Running and analyzing tests |

## Integration Points

### 1. Plan Generation (`/continue`, `/go`)

When building execution sequence, annotate each step with model tier:

```markdown
## Execution Sequence

1. [CHORES] Read session files
2. [HIGH] Analyze problem from PROBLEMS.md
3. [MID] Implement fix in auth.py
4. [CHORES] Run tests
5. [MID] Verify test results
6. [CHORES] Commit changes
7. [HIGH] → DEFAULT (restore)
```

### 2. STRUT Plans

Add `[MODEL:tier]` annotation to steps:

```markdown
## P1: EXPLORE

### Steps
- [ ] P1-S1 [CHORES] [READ] session NOTES.md, PROBLEMS.md
- [ ] P1-S2 [HIGH] [ANALYZE] root cause of authentication failure
- [ ] P1-S3 [MID] [RESEARCH] OAuth 2.0 token refresh patterns

### Transition
- IF all deliverables checked → [MODEL:DEFAULT] [DESIGN]
```

### 3. Step Execution

Before executing each step:
1. Check current model tier
2. If step requires different tier, switch model
3. Execute step
4. If next step needs different tier OR sequence complete, prepare switch

### 4. Batch Optimization

Group consecutive same-tier steps to minimize switches:

```markdown
## Optimized Sequence

[SWITCH → CHORES]
1. Read session files
2. Run git status
3. List directory

[SWITCH → HIGH]
4. Analyze problem
5. Write spec section

[SWITCH → MID]
6. Implement fix
7. Verify fix

[SWITCH → DEFAULT]
```

## Plan Annotation Syntax

### Step-Level Annotation

```markdown
- [ ] P1-S1 [MODEL:CHORES] [READ] files
- [ ] P1-S2 [MODEL:HIGH] [ANALYZE] problem
```

### Block-Level Annotation

```markdown
## [MODEL:CHORES] File Operations Block
- [ ] Read NOTES.md
- [ ] Read PROBLEMS.md
- [ ] Check git status
## [MODEL:DEFAULT]
```

### Override Annotation

User can force a tier:
```markdown
- [ ] P1-S1 [MODEL:HIGH!] [READ] files  # Force HIGH even though READ is normally CHORES
```

## Cost Estimation

### Example Session Cost Comparison

**Without auto-switching (all HIGH):**
```
10 steps x 5x = 50 credits
```

**With auto-switching:**
```
3 CHORES steps x 0.5x = 1.5 credits
2 HIGH steps x 5x = 10 credits
4 MID steps x 2x = 8 credits
1 IMAGE step x 1x = 1 credit
Total: 20.5 credits (59% savings)
```

### Switch Overhead

Each model switch:
- Time: ~2 seconds
- No credit cost (switching is free)
- Risk: Context may be slightly different between models

**Recommendation**: Batch at least 3 same-tier operations before switching.

## Implementation Strategy

### Phase 1: Manual Annotation (No Code)

1. Update workflow docs to include tier recommendations
2. Agent manually adds `[MODEL:tier]` annotations to plans
3. User runs `select-windsurf-model-in-ide.ps1` when seeing annotation

### Phase 2: Semi-Automatic

1. Agent outputs switch command as part of execution sequence
2. Agent pauses for user to execute switch
3. Agent continues after switch confirmed

### Phase 3: Fully Automatic (Requires Hook)

1. Agent detects tier change needed
2. Agent calls model switch script
3. Script switches model
4. Agent continues in new model

**Blocker for Phase 3**: Cascade hooks don't trigger reliably (see AMSW-PR-006)

## Design Decisions

### DD-01: Default to HIGH

Rationale: Quality over cost. User explicitly opts into cost savings.

### DD-02: Always restore DEFAULT after sequence

Rationale: Predictable state. User always knows what model they're using.

### DD-03: No auto-switch during error handling

Rationale: Errors need full reasoning capability. Never downgrade when things go wrong.

### DD-04: Batch optimization is advisory

Rationale: Agent suggests batching but executes step-by-step. Premature optimization adds complexity.

## Document History

**[2026-01-26 12:15]**
- Initial specification created
