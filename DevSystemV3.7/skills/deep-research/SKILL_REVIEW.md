# Problems Found - Devil's Advocate Review

**Reviewed**: 2026-05-25 20:00
**Context**: Full critique of deep-research skill (SKILL.md, strategy files, domain files, profile rules, tools)
**Scope**: Assumptions, logic errors, conflicts, unnecessary complexity, quality-reducing instructions

## MUST-NOT-FORGET

- Source ID format must be consistent across all files
- Profile domain must have clear exemptions from heavyweight process
- Strategy files must not contradict SKILL.md
- No redundant files that will drift out of sync

## MUST-RESEARCH

1. Source ID naming conventions - Are there industry standards for citation IDs?
2. Research scaffolding overhead - When does process help vs hurt output quality?
3. Strategy pattern duplication - How do other skill systems handle domain-specific variants?
4. Lightweight research modes - How to define clear boundaries for when to skip formal process?
5. VCRIV applicability - Does quality pipeline make sense for all research sizes?

## Critical Issues

### RF-01: Source ID format conflict (3 contradicting definitions)

**Category**: CONTRADICTION
**Severity**: CRITICAL
**Impact**: Agent produces inconsistent source IDs depending on which file it reads first

| Location | Format |
|----------|--------|
| SKILL.md:243 | `[TOPIC]-SC-[SOURCE]-[DOCNAME]` |
| RESEARCH_STRATEGY_TECH_MCPI.md:54 | `[TOPIC]-IN01-SC-[SOURCE]-[DOCNAME]` |
| devsystem-ids.md (rules) | `[TOPIC]-[DOC]-SC-[SOURCE_ID]-[SOURCE_REF]` |

SKILL.md uses `[TOPIC]-SC-...`, TECH_MCPI embeds a Doc ID reference (`-IN01-`), and the rules file uses `[TOPIC]-[DOC]-SC-...`. These cannot all be correct simultaneously.

**Recommendation**: Adopt one format in SKILL.md, update all strategy files to reference it.

### RF-02: TECH_MCPI is a redundant strategy file that will drift

**Category**: COMPLEXITY
**Severity**: CRITICAL
**Impact**: Edits to MCPI will not propagate to TECH_MCPI, creating silent inconsistencies

`RESEARCH_STRATEGY_TECH_MCPI.md` duplicates ~80% of `RESEARCH_STRATEGY_MCPI.md`. Unique additions:
- Credit tracking (could be in SKILL.md or tools)
- Version scope documentation (could be in `software/DOMAIN_SOFTWARE.md`)
- SDK-specific template sections (could be domain template additions)

Two files that describe the same process = guaranteed drift.

**Recommendation**: Merge TECH_MCPI unique bits into `software/DOMAIN_SOFTWARE.md` (template additions, version scope) and SKILL.md (credit tracking). Delete TECH_MCPI.

### RF-03: Profile domain has no explicit exemption from STRUT/VCRIV

**Category**: ASSUMPTION
**Severity**: CRITICAL
**Impact**: Single-profile research (1-2 hours) wastes 30-45 minutes on scaffolding that adds no quality

SKILL.md mandates:
- STRUT for ALL research
- 3-4 VCRIV checkpoints
- Summary file + Sources file + TASKS plan

DOMAIN_PROFILES.md says "No Summary or Sources files" but does NOT explicitly exempt profiles from STRUT or VCRIV. Agent either:
1. Creates full scaffolding for a 1-hour profile (overhead dominates)
2. Skips scaffolding and violates SKILL.md rules

**Recommendation**: Add explicit "Lightweight Mode" criteria in SKILL.md: single-file output, <2 hours estimated effort = no STRUT, no TASKS, single VCRIV pass at end.

## High Priority

### RF-04: VCRIV granularity undefined for profiles

**Category**: GAP
**Severity**: HIGH
**Impact**: Agent doesn't know when to run quality pipeline on profile output

SKILL.md granularity rules:
- NARROW: VCRIV per topic file
- FOCUSED/EXPLORATORY: VCRIV per dimension

Profile research has no "dimensions" or numbered topic files. A single profile is what scope? What triggers VCRIV?

**Recommendation**: Add profile-specific VCRIV rule: "Profile research: VCRIV once per standalone profile document."

### RF-05: Checkpoint count conflict (3 vs 4)

**Category**: CONTRADICTION
**Severity**: HIGH
**Impact**: Agent uncertain whether to run 3 or 4 quality checkpoints

- SKILL.md line 173: "Four mandatory checkpoints" (lists 4)
- MCPI strategy line 25: "STRUT enforces 3 VCRIV checkpoints as deliverables"

**Recommendation**: Align to 4 in SKILL.md (authoritative), update strategy files.

### RF-06: RESEARCH_CREATE_TOC.md purpose unclear

**Category**: COMPLEXITY
**Severity**: HIGH
**Impact**: Two workflows create master index files, agent doesn't know which to use

- `RESEARCH_CREATE_SUMMARY.md` -> outputs `_INFO_[TOPIC]-01_Summary.md`
- `RESEARCH_CREATE_TOC.md` -> outputs `__[SUBJECT]_TOC.md`

Strategy files only reference the Summary workflow. The TOC workflow uses `__` prefix (scaffolding) and different naming. When does TOC apply? If it's a legacy artifact, remove it.

**Recommendation**: Clarify relationship or merge. If TOC is a working document superseded by Summary, document this explicitly.

### RF-07: Output Folder step depends on unread skill

**Category**: ASSUMPTION
**Severity**: HIGH
**Impact**: Agent may fail to create correct output folder if session-management skill not loaded

SKILL.md Step 1.2 references "@skills:session-management Topic Folder Creation procedure" without defining the procedure inline. If agent hasn't read that skill (reading order not enforced), it will improvise folder naming.

**Recommendation**: Either inline the folder naming rules or add explicit "Read @skills:session-management first" prerequisite.

## Medium Priority

### RF-08: profiles/ self-referential description

**Category**: STALE
**Severity**: MEDIUM
**Impact**: Confusing text for agent reading the file

DOMAIN_PROFILES.md line 43: "The `profiles/` subfolder is a shared module..."
But DOMAIN_PROFILES.md IS now in `profiles/`. Should say "This folder" or "These templates".

### RF-09: Domain enum vs folder name mismatch

**Category**: INCONSISTENCY
**Severity**: MEDIUM
**Impact**: Potential path resolution confusion

- PromptDecomposition enum: `PROFILE` (singular)
- Folder name: `profiles/` (plural)
- PromptDecomposition enum: `MARKET_INTEL` (underscore)
- Folder name: `market-intel/` (hyphen)

### RF-10: Effort Validation only in DEFAULT domain

**Category**: GAP
**Severity**: MEDIUM
**Impact**: Non-DEFAULT research has no budget sanity check

`default/DOMAIN_DEFAULT.md` has "Effort Validation" section: "If actual time < 50% of estimate, justify or expand." This useful guardrail exists nowhere else. Either promote to SKILL.md or add to all domains.

### RF-11: deep-research-config.json has hardcoded model names

**Category**: ASSUMPTION
**Severity**: MEDIUM
**Impact**: Config becomes stale when models are updated

```json
"default_model": "gpt-5-mini",
"default_model_informal": "gpt-5-nano"
```

These model names will become outdated. No process ensures they stay current.

**Recommendation**: Reference a registry file or add a comment noting when last verified.

## Questions That Need Answers

1. Is TECH_MCPI still needed now that SOFTWARE domain exists?
2. Should single-profile research ever require STRUT?
3. What is the canonical source ID format?
4. Is RESEARCH_CREATE_TOC.md still used? By whom?
5. Should credit tracking be a global SKILL.md feature or domain-specific?

## Industry Research Findings

Not executed (inline critique session). Recommend executing research phase if findings above are addressed and further validation needed.
