# INFO: DevSystem V3 Migration Analysis

**Doc ID**: DSVS-IN01
**Goal**: Analyze challenges when migrating DevSystemV2.1 to V3 with EDIRD phase model and Agentic English
**Timeline**: Created 2026-01-15

**Depends on:**
- `_SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP01]` for vocabulary
- `_SPEC_EDIRD_PHASE_MODEL_2.md [EDIRD-SP04]` for phase model

## Summary

**Key findings:**
- DevSystemV2.1 has 4 rules, 20 workflows, 7 skills
- Current workflows use informal verbs, not standardized Agentic English
- No phase structure exists - workflows are task-specific, not phase-mapped
- Session management aligns well with EDIRD (already has EXPLORE/DESIGN/IMPLEMENT patterns)
- Major challenge: retrofitting existing workflows to EDIRD phases without breaking functionality

**Migration scope:**
- LOW complexity: Rules (mostly terminology updates)
- MEDIUM complexity: Skills (add verb mappings, update placeholders)
- HIGH complexity: Workflows (restructure around EDIRD phases)

## Current DevSystemV2.1 Structure

### Rules (4 files)

- `core-conventions.md` - Text formatting, document structure, header blocks
- `devsystem-core.md` - Core definitions, folder structure, placeholders, workflow reference
- `devsystem-ids.md` - ID system for documents and tracking items
- `workspace-rules.md` - Empty placeholder

**Challenge:** Rules define concepts but don't use Agentic English syntax consistently.

### Workflows (20 files)

**Context workflows:**
- `prime.md` - Load workspace context

**Autonomous action workflows:**
- `go-autonomous.md` - Generic autonomous loop
- `go-research.md` - Structured research

**Session workflows:**
- `session-init.md`, `session-save.md`, `session-resume.md`, `session-close.md`, `session-archive.md`

**Process workflows:**
- `write-spec.md`, `write-impl-plan.md`, `write-test-plan.md`
- `implement.md` - Autonomous implementation
- `verify.md` - Verification against specs/rules
- `commit.md` - Git commits

**Review workflows:**
- `review-devilsadvocate.md` - Critical review
- `review-pragmaticprogrammer.md` - Pragmatic review

**Utility workflows:**
- `next.md` - Universal entry point with planning
- `rename.md` - Refactoring
- `sync.md` - Sync files between locations
- `setup-pdftools.md` - Tool setup

**Challenge:** Workflows don't map to EDIRD phases. No [VERB] syntax used.

### Skills (7 folders)

- `coding-conventions/` - Python, PowerShell rules
- `git-conventions/` - Commit message rules
- `github/` - GitHub setup and usage
- `ms-playwright-mcp/` - Browser automation
- `pdf-tools/` - PDF processing
- `session-management/` - Session lifecycle
- `write-documents/` - Document templates

**Challenge:** Skills provide detailed guidance but don't use [PLACEHOLDER] syntax consistently.

## Gap Analysis

### What EDIRD-SP04 Requires

1. **Phase-based workflow structure**: EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER
2. **Verb outcomes**: [VERB]-OK, [VERB]-FAIL, [VERB]-SKIP
3. **Gate checks**: Prerequisites before phase transitions
4. **Workflow type detection**: BUILD vs SOLVE
5. **Complexity/problem-type assessment**: [ASSESS] in EXPLORE phase
6. **Deterministic next-action**: Agent always knows next step

### What DevSystemV2.1 Has

1. **Task-specific workflows**: No phase structure
2. **Informal language**: "Do research", not [RESEARCH]
3. **No gates**: Transitions based on completion, not checklists
4. **No workflow type**: All workflows implicit BUILD
5. **Complexity mentioned**: But not assessed systematically
6. **Human-guided flow**: Workflows expect user interaction

### Migration Challenges

#### CH-01: Workflow Restructuring

**Problem:** Current workflows are linear task lists, not phase-mapped verb sequences.

**Example - `implement.md` current:**
```
Implement what the user wants. Do it completely autonomously.
- Be conservative about your assumptions
- Don't leave clutter
```

**Example - `implement.md` with EDIRD:**
```
## Phase: IMPLEMENT
[IMPLEMENT] code changes per IMPL plan
[TEST] after each change
[FIX] if tests fail
[COMMIT] small, frequent
Gate check: Tests pass, no TODO/FIXME
```

**Impact:** All 20 workflows need restructuring.

#### CH-02: Verb Standardization

**Problem:** Workflows use informal verbs, not [VERB] syntax.

**Current:** "Ask clarifying questions", "Check exhaustiveness"
**AGEN:** [QUESTION], [VERIFY]

**Impact:** Every instruction sentence needs verb extraction.

#### CH-03: Gate Definition

**Problem:** No gate checklists exist. Workflows rely on implicit completion.

**Needed:**
- Define gates for each workflow
- Map gate items to verbs
- Add stuck detection (3 cycles, [CONSULT])

**Impact:** New content required for all process workflows.

#### CH-04: Workflow Type Detection

**Problem:** No BUILD/SOLVE distinction. All workflows assume code output.

**Examples needing SOLVE:**
- `go-research.md` - SOLVE: RESEARCH
- `review-devilsadvocate.md` - SOLVE: ANALYSIS
- `write-spec.md` - SOLVE: WRITING (outputs document, not code)

**Impact:** Add [ASSESS] step to entry workflows (`next.md`, `go-autonomous.md`).

#### CH-05: Placeholder Consistency

**Problem:** Placeholders used inconsistently.

**Current:** Some use `[WORKSPACE_FOLDER]`, some use `workspace root`
**AGEN:** All must use `[PLACEHOLDER]` syntax

**Impact:** Search/replace across all files.

#### CH-06: Skill-Workflow Integration

**Problem:** Skills are invoked with `@skill-name` but don't map to verbs.

**AGEN pattern:** Workflows use `[WRITE-SPEC]`, which invokes `@write-documents` skill.

**Impact:** Define which verbs invoke which skills.

#### CH-07: Session Lifecycle Alignment

**Problem:** Session workflows (init/save/resume/close) don't use EDIRD phases.

**Opportunity:** Session lifecycle maps naturally to EDIRD:
- `/session-init` = Start of EXPLORE
- `/session-save` = Checkpoint anywhere
- `/session-resume` = Re-enter at saved phase
- `/session-close` = DELIVER phase complete

**Impact:** Add phase tracking to session files (NOTES.md: "Current Phase: DESIGN").

#### CH-08: Backward Compatibility

**Problem:** Existing repos use DevSystemV2.1. Migration must not break them.

**Strategy:**
- V3 must work in repos that haven't migrated documents
- Graceful degradation if old-style workflows encountered
- Deploy script must handle both versions

**Impact:** Extra validation in deploy workflow.

## Proposed V3 Structure

### Rules

- `core-conventions.md` - Unchanged (formatting only)
- `devsystem-core.md` - Update with EDIRD references, phase tracking
- `devsystem-ids.md` - Unchanged (ID system stable)
- `agentic-english.md` - NEW: Include AGEN-SP01 content as always-on rule

### Workflows (Reorganized by Phase)

**Entry workflows:**
- `next.md` - Universal entry, [ASSESS] workflow type
- `prime.md` - Load context (unchanged)

**EXPLORE phase:**
- `explore.md` - NEW: [RESEARCH], [ANALYZE], [GATHER], [ASSESS], [SCOPE]

**DESIGN phase:**
- `design.md` - NEW: [PLAN], [OUTLINE], [WRITE-SPEC], [WRITE-IMPL], [WRITE-TEST]
- `prove.md` - NEW: POC workflow with [PROVE]

**IMPLEMENT phase:**
- `implement.md` - Restructured with [IMPLEMENT], [TEST], [FIX], [COMMIT]
- `go-autonomous.md` - Becomes full EDIRD cycle wrapper

**REFINE phase:**
- `refine.md` - NEW: [REVIEW], [VERIFY], [CRITIQUE], [RECONCILE]
- `verify.md` - Becomes [VERIFY] verb implementation

**DELIVER phase:**
- `deliver.md` - NEW: [VALIDATE], [MERGE], [DEPLOY], [CLOSE], [ARCHIVE]
- `commit.md` - Becomes [COMMIT] verb implementation

**Session workflows:**
- `session-*.md` - Add phase tracking, otherwise similar

**Review workflows:**
- `review-devilsadvocate.md` - Becomes [CRITIQUE] implementation
- `review-pragmaticprogrammer.md` - Becomes [RECONCILE] implementation

### Skills

- Keep all existing skills
- Add verb-skill mapping table to each SKILL.md
- Update placeholder syntax

## Migration Strategy Options

### Option A: Big Bang

Replace all DevSystemV2.1 content at once.

**Pros:**
- Clean break, no compatibility issues
- Faster for IPPS repo

**Cons:**
- Breaks linked repos until they migrate
- High risk if issues discovered post-migration

### Option B: Incremental

Add V3 content alongside V2.1, deprecate over time.

**Pros:**
- Lower risk
- Linked repos can migrate gradually

**Cons:**
- Dual maintenance burden
- Confusion about which version to use

### Option C: Hybrid (Recommended)

1. Create V3 in DevSystemV3/ folder
2. Deploy to IPPS first, test thoroughly
3. Deploy to linked repos one at a time
4. Archive DevSystemV2.1 after all repos migrated

## Risk Assessment

- **HIGH**: Workflow restructuring breaks agent behavior
- **MEDIUM**: Placeholder inconsistencies cause path errors
- **MEDIUM**: Gate definitions too strict, causing loops
- **LOW**: ID system changes (none planned)
- **LOW**: Skill content changes (additions only)

## Next Steps

1. Create `_IMPL_DEVSYSTEM_V3_MIGRATION.md` with detailed migration plan
2. Start with rules (lowest risk)
3. Migrate one workflow as pilot (suggest: `implement.md`)
4. Iterate based on pilot results
5. Batch migrate remaining workflows
6. Update skills
7. Test in IPPS repo
8. Deploy to linked repos

## Sources

**Primary Sources:**
- `DSVS-IN01-SC-DSV21-RULES`: `DevSystemV2.1/rules/` - 4 rule files analyzed
- `DSVS-IN01-SC-DSV21-WKFLW`: `DevSystemV2.1/workflows/` - 20 workflow files analyzed
- `DSVS-IN01-SC-DSV21-SKILLS`: `DevSystemV2.1/skills/` - 7 skill folders analyzed
- `DSVS-IN01-SC-AGEN-SP01`: `_SPEC_AGEN_AGENTIC_ENGLISH.md` - Verb and placeholder definitions
- `DSVS-IN01-SC-EDIRD-SP04`: `_SPEC_EDIRD_PHASE_MODEL_2.md` - Phase model requirements

## Document History

**[2026-01-15 20:15]**
- Initial analysis created
- Identified 8 migration challenges (CH-01 through CH-08)
- Proposed V3 structure with phase-based workflows
- Recommended hybrid migration strategy
