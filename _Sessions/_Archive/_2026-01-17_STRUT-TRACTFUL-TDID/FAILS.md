# Session Failure Log

## Active Issues

### [LOW] `EDIRD-FL-001` File sync issue - go.md showed stale content in IDE

**Learning**: `EDIRD-LN-003` - IDE Buffer Sync After Major Rewrites

- **When**: 2026-01-20 20:11 UTC+01:00
- **Where**: `DevSystemV3.1/workflows/go.md`
- **What**: After rewriting go.md to remove EDIRD references, user's IDE still showed old content with EDIRD references. File on disk was correct but IDE buffer was stale.
- **Why it went wrong**:
  - Agent's edit succeeded on disk
  - IDE did not auto-reload the changed file
  - Agent did not warn user to reload file after major rewrite
- **Evidence**: User said "hey we said NO EDIRD dependencies here!" showing old content, while `Get-Content` showed correct new content

**Prevention rules**:
1. After major file rewrites, suggest user reload file: "File rewritten - reload in IDE if showing old content"
2. When user reports stale content, verify disk vs IDE with `Get-Content`

### [LOW] `EDIRD-FL-002` Used AGEN verbs in workflow when plain English requested

**Learning**: `EDIRD-LN-002` - Plain English in Workflows

- **When**: 2026-01-20 20:18 UTC+01:00
- **Where**: `DevSystemV3.1/workflows/test.md`
- **What**: Initial test.md update used AGEN verbs like [GATHER], [TEST], [VERIFY] when user wanted plain English in workflows
- **Why it went wrong**:
  - Agent followed existing pattern from verify.md
  - User's constraint about workflow style wasn't applied consistently
  - Workflows should be readable without AGEN knowledge
- **Evidence**: User said "hey replace AGEN verbs with normal english"

**Prevention rules**:
1. Workflows should use plain English, not AGEN verbs
2. AGEN verbs belong in rules and skills, not workflow instructions
3. When simplifying workflows, also simplify the language

### [MEDIUM] `EDIRD-FL-003` Duplicated content between skill and workflows

**Learning**: `EDIRD-LN-001` - Workflow-Skill Separation Principle

- **When**: 2026-01-20 20:12 UTC+01:00
- **Where**: `DevSystemV3.1/workflows/build.md`, `solve.md`
- **What**: build.md and solve.md contained detailed phase steps, gates, and verb sequences that duplicated content in @edird-phase-planning skill
- **Why it went wrong**:
  - Original workflow design included full phase details
  - Skill was added but workflows weren't simplified
  - Violated DRY principle
- **Evidence**: User said "Simplify. Dont replicate stuff that is in the skill."

**Prevention rules**:
1. Workflows that invoke skills should NOT duplicate skill content
2. Workflow = entry point + skill reference + workflow-specific rules only
3. After adding skills, review and simplify referencing workflows

## Resolved Issues

(none yet)
