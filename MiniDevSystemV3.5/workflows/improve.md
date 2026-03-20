---
description: Find and fix contradictions, inconsistencies, and improvement opportunities
---

# Improve Workflow

Autonomous self-improvement. Find issues, fix immediately. No user consultation.

**Mandatory reads before improving:**
- `APAPALAN_RULES.md` (@skills:write-documents)
- `MECT_WRITING_RULES.md` (@skills:write-documents)
- `MECT_CODING_RULES.md` (@skills:coding-conventions)

## APAPALAN Quality Check

Apply to ALL written documents and communications in scope:
- **AP-PR-07**: Be specific - concrete, verifiable statements
- **AP-PR-09**: Consistent patterns - same concept = same format everywhere
- **AP-BR-02**: Cut filler - drop articles, verbose constructions
- **AP-NM-01**: One name per concept - fix synonyms and polysemy
- **AP-NM-05**: Use standard terms - no invented jargon
- **AP-ST-01**: Goal first - WHY before HOW

## MECT Writing Quality Check

Apply to written documents in scope:
- **MW-VO-01**: Active voice - actor before action
- **MW-VO-03**: Simplest verb - "review" not "carry out a review"
- **MW-VO-04**: Obligation words - must/must not/should/may, never "shall"
- **MW-WC-01**: Word-level precision - accuracy != precision
- **MW-TD-01**: Naming structure - explicit -> specifiers -> states -> mnemonics
- **MW-HS-01**: Informative headings - state content, not topic
- **MW-DT-01**: Four description lenses - intentional/functional/technical/contextual

## MECT Coding Quality Check

Apply to code in scope:
- **MC-PR-01**: One name per concept across codebase
- **MC-PR-03**: No meta-words without qualifier
- **MC-PR-05**: Error messages state what failed, why, recovery
- **MC-PR-06**: Log messages self-contained
- **MC-BR-04**: Boolean functions use is_/has_/can_, not "check_"
- **MC-CO-01**: Corresponding pairs use same word stem
- **MC-CO-03**: Convergent naming across URL, payload, variable, log, docs
- **MC-ND-06**: Disambiguate by qualifying, not renaming

## Issue Categories

1. Contradictions
2. Inconsistencies
3. Ambiguities
4. Underspecified behavior
5. Broken dependencies
6. Incorrect/unverified assumptions
7. Flawed logic/thinking
8. Unnecessary complexity
9. New solutions for already solved problems
10. Concept overlap
11. Broken rules
12. APAPALAN/MECT violations

## Workflow

1. Scope: file path → that file; folder → all .md/code; none → conversation context
2. Re-read dependencies before assessing:
   - Rules: `[AGENT_FOLDER]/rules/*.md`
   - Writing: `APAPALAN_RULES.md` + `MECT_WRITING_RULES.md` (@skills:write-documents)
   - Code: `MECT_CODING_RULES.md` (@skills:coding-conventions)
   - Workspace: README, NOTES, ID-REGISTRY, FAILS, LEARNINGS
   - Scope-specific: SPEC→INFO, IMPL→SPEC, TEST→SPEC+IMPL, workflow→`WORKFLOW-RULES.md`
   - Session: NOTES, PROBLEMS, PROGRESS (if SESSION-MODE)
3. Build internal issue list with location, severity, fix
4. Create fix plan (CRITICAL first, then HIGH, group related)
5. Execute fixes, update Document History
6. Verify: re-read, check for regressions

## Fix Rules

- Preserve IDs (FR-XX, DD-XX)
- Pick simplest fix when multiple valid options
- Remove broken refs or add missing targets
- Apply APAPALAN + MECT to all text changes
- Apply MECT_CODING_RULES to all code changes