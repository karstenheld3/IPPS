# Fact-Check Review: README.md

**Doc ID**: README-RV01
**Target**: `README.md`
**Date**: 2026-09-11
**Reviewer**: Agent (fact-check workflow)

## Sources Extracted

| ID | Type | Reference | Status |
|----|------|-----------|--------|
| S01 | file | `.devin/workflows/*.md` (48 files) | verified |
| S02 | file | `.devin/skills/` (24 directories) | verified |
| S03 | file | `specs/_SPEC_AGEN_AGENTIC_ENGLISH.md` | verified |
| S04 | file | `specs/_SPEC_EDIRD_PHASE_MODEL.md` | verified |
| S05 | file | `specs/_SPEC_STRUT_STRUCTURED_THINKING.md` | verified |
| S06 | file | `specs/_SPEC_TRACTFUL_DOCUMENT_FRAMEWORK.md` | verified |
| S07 | file | `specs/_INFO_MNF_TECHNIQUE.md` | verified |
| S08 | file | `specs/_INFO_APAPALAN_PRINCIPLE.md` | verified |
| S09 | file | `specs/_INFO_MECT_PHILOHY.md` | verified |
| S10 | file | `specs/_INFO_SOCAS_SIGNS_OF_CONFUSION_AND_SLOPPINESS.md` | verified |
| S11 | file | `specs/_INFO_GRUC_GUIDES_RULES_CHECKS.md` | verified |
| S12 | file | `specs/_INFO_AGENTIC_MINTO_ARTICLES.md` | verified |
| S13 | file | `specs/_INFO_MEPI_MCPI_PRINCIPLE.md` | verified |
| S14 | file | `.devin/skills/write-documents/APAPALAN_RULES.md` | verified |
| S15 | file | `.devin/skills/write-documents/SOCAS_RULES.md` | verified |
| S16 | file | `.devin/skills/write-documents/MECT_WRITING_RULES.md` | verified |
| S17 | file | `.devin/skills/coding-conventions/MECT_CODING_RULES.md` | verified |
| S18 | file | `.devin/skills/workspace-management/DEV_REPO_NOTES_TEMPLATE.md` | verified |
| S19 | file | `.devin/skills/workspace-management/ID-REGISTRY_TEMPLATE.md` | verified |
| S20 | file | `.devin/rules/core-conventions.md` | verified |
| S21 | file | `.devin/rules/promptsystem-core.md` | verified |
| S22 | file | `.devin/rules/promptsystem-ids.md` | verified |
| S23 | file | `.devin/rules/agentic-english.md` | verified |
| S24 | file | `.devin/rules/edird-phase-planning.md` | verified |
| S25 | file | `.devin/skills/git-conventions/SKILL.md` | verified |
| S26 | file | `.devin/skills/coding-conventions/SKILL.md` | verified |
| S27 | file | `.devin/skills/write-documents/WORKFLOW_RULES.md` | verified |
| S28 | file | `ID-REGISTRY.md` | verified |
| S29 | file | `docs/_INFO_AGENT_COMPARISON.md` | verified |
| S30 | file | `docs/_INFO_FAST_CHEAP_MODELS.md` | verified |
| S31 | file | `docs/_INFO_AGENT_SKILLS.md` | verified |
| S32 | file | `docs/_INFO_USE_CASCADE_AS_AGENT.md` | verified |
| S33 | file | `docs/_INFO_SPEC_DRIVEN_DEVELOPMENT.md` | verified |
| S34 | file | `docs/INFO_HOW_WINDSURF_WORKS.md` | **missing** |
| S35 | file | `docs/_INFO_HOW_CLAUDE_CODE_WORKS.md` | verified |
| S36 | file | `docs/_INFO_HOW_CODEX_WORKS.md` | verified |
| S37 | file | `docs/_INFO_HOW_COPILOT_WORKS.md` | verified |
| S38 | file | `docs/_INFO_HOW_OPENCLAW_WORKS.md` | verified |
| S39 | file | `docs/_INFO_OPENCLAW.md` | verified |
| S40 | file | `docs/_INFO_OPENAI_ANTHROPIC_MODEL_COSTS.md` | verified |
| S41 | file | `docs/_TEST_ASCII_ART_WIDTH.md` | verified |
| S42 | file | `DevSystemV4.3/` directory | **missing** |
| S43 | file | `_OldDevSystemVersions/` directory | **missing** |
| S44 | file | `PromptSystemV4.4/` directory | verified (actual name) |
| S45 | file | `_OldVersions/` directory | verified (actual name) |
| S46 | url | `https://github.com/github/spec-kit` | verified |
| S47 | url | `https://docs.zencoder.ai/user-guides/guides/spec-driven-development` | verified |
| S48 | web | Claude Opus 4.8 model (Anthropic, released 2026-05-28) | verified |
| S49 | web | Douglas Engelbart "Augmenting Human Intellect" (1962) | verified |
| S50 | web | Frederick Brooks "surgical team" concept ("The Mythical Man-Month", 1975) | verified |

## Facts Extracted and Verdicts

### Quantitative Claims

| ID | Line | Claim | Verdict | Evidence |
|----|------|-------|---------|---------|
| F01 | 172 | "46 workflows in `.devin/workflows/`" | **FAIL** | S01: Actual count is 48 workflow files. `Get-ChildItem` returns 48 `.md` files. |
| F02 | 237 | "24 skills in `.devin/skills/`" | **PASS** | S02: Actual count is 24 skill directories. |
| F03 | 52 | "35 enforceable rules" (APAPALAN) | **PASS** | S14: `APAPALAN_RULES.md` contains exactly 35 `### AP-*` rules (PR:13, BR:7, ST:7, CM:3, NM:5). |
| F04 | 39 | "15 criteria" (SOCAS) | **FAIL** | S15: `SOCAS_RULES.md` line 46 states "## The 17 Criteria". SOCAS-01 through SOCAS-17 = 17 criteria. |
| F05 | 54 | "15 criteria detecting confusion and sloppiness" | **FAIL** | Same as F04. Actual count is 17. |
| F06 | 960 | "15 criteria for detecting agent degradation" | **FAIL** | Same as F04. Actual count is 17. |

### Existence Claims - File Paths

| ID | Line | Claim | Verdict | Evidence |
|----|------|-------|---------|---------|
| F07 | 1233 | `.devin/` "synced from DevSystemV4.3" | **FAIL** | S42: `DevSystemV4.3/` does not exist. Actual source folder is `PromptSystemV4.4/` (S44). |
| F08 | 1238 | `DevSystemV4.3/` "Current system (source of truth)" | **FAIL** | S42: Directory does not exist. Actual: `PromptSystemV4.4/`. |
| F09 | 1320 | `[DevSystemV4.3](DevSystemV4.3/)` link | **FAIL** | Broken link. Target directory does not exist. |
| F10 | 1237 | `_OldDevSystemVersions/` directory | **FAIL** | S43: Does not exist. Actual: `_OldVersions/` (S45). |
| F11 | 1322 | `[_OldDevSystemVersions/](_OldDevSystemVersions/)` link | **FAIL** | Broken link. Target directory does not exist. |
| F12 | 1377 | `[How Windsurf Works](docs/INFO_HOW_WINDSURF_WORKS.md)` | **FAIL** | S34: File does not exist at this path. Actual: `docs/_INFO_HOW_WINDSURF_WORKS.md` (missing underscore prefix). |
| F13 | 107 | "current version (V4.3)" | **FAIL** | Current version folder is `PromptSystemV4.4`, indicating V4.4 is current, not V4.3. |
| F14 | 1233 | `.devin/rules/` contains rules | **PASS** | Verified. All referenced rule files exist (S20-S24). |
| F15 | 139 | `DEV_REPO_NOTES_TEMPLATE.md` link | **PASS** | S18: File exists. |
| F16 | 140 | `ID-REGISTRY_TEMPLATE.md` link | **PASS** | S19: File exists. |
| F17 | 975 | `ID-REGISTRY.md` link | **PASS** | S28: File exists. |
| F18 | 1377 | `[How Claude Code Works](docs/_INFO_HOW_CLAUDE_CODE_WORKS.md)` | **PASS** | S35: File exists. |
| F19 | 1378 | `[How Codex CLI Works](docs/_INFO_HOW_CODEX_WORKS.md)` | **PASS** | S36: File exists. |
| F20 | 1380 | `[How OpenClaw Works](docs/_INFO_HOW_OPENCLAW_WORKS.md)` | **PASS** | S38: File exists. |

### Existence Claims - External URLs

| ID | Line | Claim | Verdict | Evidence |
|----|------|-------|---------|---------|
| F21 | 386 | GitHub spec-kit URL `https://github.com/github/spec-kit` | **PASS** | S46: URL resolves. GitHub repository exists with SDD toolkit. |
| F22 | 386 | Zencoder URL `https://docs.zencoder.ai/...` | **PASS** | S47: URL resolves. Page about Spec-Driven Development exists. |

### Attribution Claims

| ID | Line | Claim | Verdict | Evidence |
|----|------|-------|---------|---------|
| F23 | 5 | "Inspired by Douglas Engelbart's intelligence augmentation" | **PASS** | S49: Engelbart's 1962 report "Augmenting Human Intellect" is real and foundational. |
| F24 | 5 | "Frederick Brooks' 'surgical team' concept" | **PASS** | S50: Brooks described the surgical team concept in "The Mythical Man-Month" (1975). Well-known concept. |
| F25 | 1326 | "Claude Opus 4.8" model reference | **PASS** | S48: Claude Opus 4.8 is a real Anthropic model released 2026-05-28. |

### Naming Claims

| ID | Line | Claim | Verdict | Evidence |
|----|------|-------|---------|---------|
| F26 | 386 | "Specification-Driven Development (SDD) methodology" | **PARTIAL** | Both sources (S46, S47) call it "Spec-Driven Development", not "Specification-Driven Development". The linked doc (S33) is named `_INFO_SPEC_DRIVEN_DEVELOPMENT.md` (not SPECIFICATION). Naming inconsistency, but acronym SDD works for both. |

### Workflow Listing Completeness

| ID | Line | Claim | Verdict | Evidence |
|----|------|-------|---------|---------|
| F27 | 172-233 | Workflow reference lists all workflows | **FAIL** | 3 workflows missing from listing: `/write-prompts`, `/investigate`, `/compare-workspace-setup`. All 3 exist as files in `.devin/workflows/`. Listed count: 45. Actual count: 48. |

## Conclusions

| ID | Conclusion | Supporting Facts | Verdict |
|----|-----------|-----------------|---------|
| C01 | README's quantitative claims are unreliable | F01 (workflow count), F04-F06 (SOCAS criteria count) | **FAIL** - 4 quantitative errors found |
| C02 | README's project structure section is stale | F07-F11, F13 (DevSystemV4.3 references, _OldDevSystemVersions, version number) | **FAIL** - 6 stale references to renamed/removed directories |
| C03 | README's external attributions are accurate | F21-F25 (URLs, Engelbart, Brooks, Claude Opus 4.8) | **PASS** |
| C04 | README's file link inventory has 1 broken link | F12 (Windsurf doc) | **FAIL** - 1 broken path |
| C05 | README's workflow listing is incomplete | F27 (3 missing workflows) | **FAIL** |

## Summary

**Total facts checked**: 27
**PASS**: 15
**FAIL**: 11
**PARTIAL**: 1

**Verdict: FAIL** - 11 factual errors found.

### Critical Findings (fix before publication)

1. **Workflow count**: "46" → "48" (line 172). Add missing workflows: `/write-prompts`, `/investigate`, `/compare-workspace-setup` to the reference listing.

2. **SOCAS criteria count**: "15" → "17" (lines 39, 54, 960). The SOCAS_RULES.md explicitly states "## The 17 Criteria" and lists SOCAS-01 through SOCAS-17.

3. **Version and directory names**: All references to `DevSystemV4.3` → `PromptSystemV4.4` (lines 107, 1233, 1238, 1320). All references to `_OldDevSystemVersions` → `_OldVersions` (lines 1237, 1322). Version "V4.3" → "V4.4" (line 107).

4. **Broken file link**: `docs/INFO_HOW_WINDSURF_WORKS.md` → `docs/_INFO_HOW_WINDSURF_WORKS.md` (line 1377). Missing underscore prefix.

5. **SDD naming**: "Specification-Driven Development" → "Spec-Driven Development" (line 386) to match both sources and the linked doc name.
