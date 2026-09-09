---
description: Create INFO document from research
auto_execution_mode: 1
---

# Write INFO Workflow

Create research/analysis documents following INFO_TEMPLATE.md structure.

## Required Skills

- @write-documents for INFO document structure and formatting rules

## MUST-NOT-FORGET

- Run `/verify` after document complete

## Prerequisites

- User has described research topic, question, or analysis goal
- Clarify scope if ambiguous
- Read @write-documents skill and INFO_TEMPLATE.md

## Steps

1. Create INFO File - `_INFO_[TOPIC].md` in session folder. Header: Doc ID (`[TOPIC]-IN[NN]`), Goal, Timeline. Empty Summary (fill last).

2. Make Research Plan - Identify 3-5 key questions. List sources (docs, code, web, APIs). Estimate scope: narrow vs broad.

3. Research Step-by-Step - Add sections incrementally. After each section ask: Need further verification? Duplicates? Unverified/contradicting findings? Actually helpful? Review new sections against existing ones - remove overload, redundancies, ambiguities.

4. Think Outside the Box - No verified solution? Reconsider problem. Missing perspectives? Clever alternatives? Never pollute with non-working solutions.

5. Document Sources - IDs: `[TOPIC]-[DOC]-SC-[SOURCE_ID]-[SOURCE_REF]`. List URL + primary finding. Mark `[VERIFIED]`.

6. Write Summary - Copy/paste ready list at top. Label: `[ASSUMED]`, `[VERIFIED]`, `[TESTED]`, `[PROVEN]`. Most important first.

7. Add Next Steps - Actionable items. Link to follow-up (SPEC, IMPL, decision needed).

8. Verify - Run `/verify`. Check: All questions answered? Sources documented? Summary accurate?

## Document Structure

See `INFO_TEMPLATE.md` in @write-documents skill.

```markdown
# INFO: [Topic]

Doc ID: [TOPIC]-IN[NN]
Goal: [Single sentence]
Timeline: Created YYYY-MM-DD

## Summary
- [Key finding 1] [VERIFIED]
- [Key finding 2] [ASSUMED]

## 1. [Section]
...

## Sources
- `TOPIC-IN01-SC-SITE-PAGE`: [URL] - [Finding]

## Next Steps
1. [Action]

## Document History
[YYYY-MM-DD HH:MM]
- Initial research document created
```