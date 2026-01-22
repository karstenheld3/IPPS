# Gate Output Template

Mandatory output format before any phase transition.

## Usage

Before proceeding from one phase to the next, agent MUST output this block:

```markdown
---
## Gate: [CURRENT_PHASE] → [NEXT_PHASE]

**Trigger analysis:**
- Triggers detected: [list from request]
- Complexity: [LOW/MEDIUM/HIGH]
- Research required: [YES/NO]

**Checklist:**
- [x] Item 1 - Evidence: [specific evidence or artifact]
- [x] Item 2 - Evidence: [specific evidence or artifact]
- [ ] Item 3 - BLOCKED: [what's missing]

**Required artifacts:**
- INFO: [filename] | NOT REQUIRED | MISSING (required)
- SPEC: [filename] | NOT REQUIRED | MISSING (required)
- IMPL: [filename] | NOT REQUIRED | MISSING (required)
- TEST: [filename] | NOT REQUIRED | MISSING (required)

**Research sources cited:**
- [source 1] | NONE (if not required) | MISSING (if required)

**Gate status:** PASS | FAIL | BLOCKED

**If FAIL/BLOCKED:** [What must be done before proceeding]
---
```

## Gate Cannot Pass If

1. Required artifacts are MISSING
2. Research triggers detected but no sources cited
3. Complexity is HIGH but documents skipped
4. Any checklist item is unchecked without justification

## Example: COMPLEXITY-HIGH with Research Trigger

```markdown
---
## Gate: EXPLORE → DESIGN

**Trigger analysis:**
- Triggers detected: "100%", "replica"
- Complexity: HIGH (trigger-forced)
- Research required: YES (replica trigger)

**Checklist:**
- [x] Problem clearly understood - Evidence: User wants exact 1978 Space Invaders
- [x] Workflow type: BUILD confirmed
- [x] Complexity: HIGH (forced by "100%" trigger)
- [x] Scope: Single HTML file, all original features
- [x] No blocking unknowns - Evidence: Original specs available online

**Required artifacts:**
- INFO: _INFO_SPACEINV.md (research complete)
- SPEC: PENDING (next phase)
- IMPL: PENDING (next phase)
- TEST: PENDING (next phase)

**Research sources cited:**
- Original arcade manual
- MAME emulator source code
- Detailed gameplay analysis videos

**Gate status:** PASS
---
```

## Integration Points

Add to these workflows:
- `/build` - After each phase
- `/solve` - After each phase
- `/next` - At completion
- `/explore`, `/design`, `/implement`, `/refine`, `/deliver` - At exit
