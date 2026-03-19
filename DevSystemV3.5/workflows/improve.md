---
description: Find and fix contradictions, inconsistencies, and improvement opportunities
---

# Improve Workflow

Autonomous self-improvement. Find issues, fix immediately. No user consultation.

**Mandatory read:** `APAPALAN_RULES.md` (@skills:write-documents) before improving any written content.

## APAPALAN Quality Check

Apply to ALL written documents and communications in scope:
- **AP-PR-07**: Be specific - replace vague statements with concrete, verifiable ones
- **AP-PR-09**: Consistent patterns - same concept = same format, same structure everywhere
- **AP-BR-02**: Cut filler - drop articles, verbose constructions, redundant phrases
- **AP-NM-01**: One name per concept - find and fix synonyms and polysemy
- **AP-NM-05**: Use standard terms - replace invented jargon with established terminology
- **AP-ST-01**: Goal first - ensure reader knows WHY before HOW

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
12. APAPALAN violations (vague writing, synonyms, missing examples, inconsistent patterns)

## Workflow

1. Scope: file path → that file; folder → all .md/code; none → conversation context
2. Re-read dependencies before assessing:
   - Rules: `[AGENT_FOLDER]/rules/*.md`
   - Writing quality: `APAPALAN_RULES.md` (@skills:write-documents)
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
- Apply APAPALAN to all text changes (precision first, then brevity)
