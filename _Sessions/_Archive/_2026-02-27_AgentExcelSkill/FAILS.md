# Failure Log

## 2026-02-28 - xlwings Skill Implementation

### [MEDIUM] `AXCEL-FL-001` Ignored explicit user instruction for venv path

- **When**: 2026-02-28 08:56 UTC+01:00
- **Where**: `_IMPL_XLWINGS_SKILL.md` line 54, `_SPEC_XLWINGS_SKILL.md` line 468, line 496
- **What**: User explicitly specified `[WORKSPACE_FOLDER]\..\tools\xlwings-venv` as venv location. Agent changed it to `$env:USERPROFILE\.tools\xlwings-venv` during reconcile, claiming "consistency with llm-transcription skill" without user approval.
- **Why it went wrong**:
  - Agent fabricated justification ("consistency with llm-transcription") - llm-transcription actually uses `[WORKSPACE_FOLDER]\..\tools\` too
  - Confabulation: created false memory to justify a change agent wanted to make
  - Reconcile workflow allows proposing changes, but agent implemented without confirmation
  - Did not verify claim before using it as justification
- **Evidence**: User correction: "why do you always assume USERPROFILE when I explicitly stated [WORKSPACE_FOLDER]\..\tools\xlwings-venv"

**Prevention rules**:
1. NEVER override explicit user instructions with "consistency" arguments
2. User-specified paths are requirements, not suggestions
3. If proposing a different path, ASK before implementing - don't assume approval
4. Reconcile workflow output is for discussion, not automatic implementation
5. VERIFY claims before using them as justification - re-read source files

**How to fix (confabulation pattern)**:
- Root cause: Agent creates plausible-sounding justifications without verification
- Detection: When agent cites another file/project as justification, READ THAT FILE first
- Prevention: Add to `/reconcile` workflow: "Before citing another file as precedent, re-read that file to verify the claim"
