# Curated Research Strategy (MEPI Approach)

Research **[SUBJECT]** using the MEPI (Most Executable Point of Information) approach - curated 2-3 best options per topic.

**Before starting**: Create `STRUT_[TOPIC].md` using `/write-strut` with Time Log section and quality pipeline steps.

**When to use MEPI instead of MCPI:**
- Reversible decisions (can change later)
- Time-constrained (user needs answer quickly)
- Action-oriented (user will do something, not archive)
- Low-to-medium stakes (not legal/financial/medical critical)

**Domain identification** (during Phase 0 or Phase 1a):
1. Determine research domain from prompt context
2. Read corresponding `DOMAIN_*.md` profile (if available, otherwise use DOMAIN_DEFAULT.md)
3. Incorporate domain-specific rules into STRUT plan

## Phases

**Phase 0: STRUT Plan Creation (MANDATORY)**
- Same as MCPI - create STRUT before any research
- Include quality pipeline steps and time log
- Run `/verify` on STRUT plan

**Phase 1: Preflight - Decomposition & Source Collection**

**Phase 1a: Prompt Decomposition (MANDATORY)**
Same as MCPI - answer 6 questions:
1. Q1 - Goal: What is the user's intent?
2. Q2 - Scope: NARROW, FOCUSED, or EXPLORATORY?
3. Q3 - Dimensions: Which apply?
4. Q4 - Topics: 3-5 per dimension
5. Q5 - Strategy: Confirm MEPI (or switch to MCPI if high-stakes)
6. Q6 - Domain: Which profile?

**Phase 1b: Source Collection (Curated)**
- Collect 5-10 sources per dimension (vs MCPI 15+)
- Focus on top-tier sources first
- Skip exhaustive community source collection
- **Done when**: 5-10 quality sources per dimension collected

**Phase 2: TOC Creation**
- Same as MCPI - create `__[TOPIC]_TOC.md`
- Summary can be shorter (5-10 sentences vs MCPI 5-15)
- **Quality gate**: Run quality pipeline

**Phase 3: Template Creation**
- Same structure as MCPI
- **Quality gate**: Run quality pipeline

**Phase 4: TASKS Plan**
- Same as MCPI - partition into discrete tasks
- Effort estimates typically lower (2-4 hours total vs MCPI 4-16)

**Phase 5: File-by-File Research**
- Focus on top 2-3 options per topic (vs MCPI exhaustive)
- Include clear recommendation with rationale
- **Quality gate**: Run quality pipeline per VCRIV granularity rules
- **Done when**: All tasks completed with 2-3 curated recommendations each

**Phase 6: Final Verification and Sync**
- Same as MCPI including dimension coverage check
- **Quality gate**: Run quality pipeline on complete set
- **Done when**: All requirements met, recommendations actionable

## Key Differences from MCPI

- **Sources per dimension**: MEPI 5-10, MCPI 15-30
- **Output per topic**: MEPI 2-3 curated options, MCPI exhaustive coverage
- **Effort estimate**: MEPI 2-4 hours, MCPI 4-16 hours
- **VCRIV cycles**: MEPI single minimum, MCPI multi-cycle
- **Community sources**: MEPI limited, MCPI exhaustive

## Quality Pipeline

Same as MCPI: `verify → critique → reconcile → implement → verify`

**VCRIV Granularity (Scope-Based):**
- NARROW (1 dimension): VCRIV per topic file
- FOCUSED/EXPLORATORY (2+ dimensions): VCRIV per dimension
- Final VCRIV on synthesis document

**Termination criteria**: Max 2 cycles per checkpoint. Escalate via [CONSULT] if issues persist.

## Output Format

MEPI outputs an INFO document with:
1. **Research Question** - What we investigated
2. **Key Findings** - 2-3 curated recommendations with rationale
3. **Comparison** - Brief comparison of options (pros/cons)
4. **Recommendation** - Clear "do this" guidance
5. **Limitations** - What we didn't cover, caveats
6. **Sources** - Quality sources with IDs

## Anti-patterns to Avoid

- Treating MEPI as "skip quality" - VCRIV still runs
- Missing decomposition phase - still mandatory
- No recommendation - MEPI must recommend, not just list
- Shallow research - curated != minimal effort
