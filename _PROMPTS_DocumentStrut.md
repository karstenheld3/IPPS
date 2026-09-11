---
intended_model: claude-sonnet-4-5
context_window_size: 200k
reasoning_settings: high
prompt_system: IPPS
---

## Prompt 1 - Read all STRUT source files

<!-- Agent reads every authoritative STRUT source before any documentation work. -->

```
Read the following files completely and report key findings for each. Do not modify any files.

1. specs/_SPEC_STRUT_STRUCTURED_THINKING.md - the STRUT specification (authority)
2. .devin/skills/write-documents/STRUT_TEMPLATE.md - the template agents follow
3. .devin/workflows/write-strut.md - the workflow that creates STRUT plans
4. README.md - the current STRUT section (find by heading "## STRUT - Structured Thinking")
5. .devin/rules/core-conventions.md - formatting and document structure rules

For each file, report:
- File path
- Key concepts, rules, or notation elements defined
- Any examples present

Constraints:
- Do not modify any files
- Do not summarize - report the actual rules, IDs, formats, and notation elements verbatim
- Do not skip any file - all 5 must be read and reported

Verify: All 5 files read. Findings report contains actual notation elements (Phase ID, Step ID, Deliverable ID, Objectives, Strategy, Transitions, Concurrent blocks, checkbox states) from the spec, not paraphrases.
```

---

## Prompt 2 - Update README STRUT section from spec findings

<!-- Agent updates README.md STRUT section using findings from prompt 1. -->

```
Using the findings from the previous step, update the STRUT section in README.md (find by heading "## STRUT - Structured Thinking" through the next `##` heading) so it accurately reflects the specification.

The README STRUT section must cover all five STRUT node types from the spec:
- Phase (P1, P2) with header format
- Objectives with deliverable links (Goal ← P1-D1)
- Strategy (free text, AWT, model hints)
- Steps with AGEN verbs ([ ] P1-S1 [VERB](params))
- Deliverables ([ ] P1-D1: Description)
- Transitions (- Condition → Target)

Also cover: checkbox states ([ ], [x], [N]), concurrent blocks (Concurrent: strategy), dependencies (← Px-Sy), and the Effect line (what files STRUT creates/edits).

Both examples (BUILD hotfix and SOLVE evaluation) must match the spec notation exactly: box-drawing characters, indentation, ID formats.

Constraints:
- Do not modify any file except README.md
- Do not change examples to be different from the spec - they must match spec notation
- Do not remove the Effect line or the Key difference paragraph
- Do not add tables or emojis (README exception allows them, but STRUT section uses lists)
- Use Phase ID not Plan ID (spec says Phase ID)

Verify: README.md STRUT section contains all 5 node types, both examples match spec notation, Phase ID used (not Plan ID), Effect line present.
```

---

## Prompt 3 - Verify README STRUT section against spec

<!-- Agent runs cross-document verification of README vs spec. -->

```
Verify the README.md STRUT section against the authoritative spec.

Read both files:
- specs/_SPEC_STRUT_STRUCTURED_THINKING.md (authority)
- README.md STRUT section (derivative, find by heading "## STRUT - Structured Thinking" through the next `##` heading)

Check every notation element in the spec appears correctly in README:
- Phase ID format (P1, P2)
- Step ID format (P1-S1 with AGEN verbs)
- Deliverable ID format (P1-D1)
- Objectives link to deliverables (← P1-D1, P1-D2)
- Strategy free text with AWT and model hints
- Transitions format (- Condition → Target, targets: [PHASE-NAME], [CONSULT], [END])
- Checkbox states ([ ] pending, [x] done, [N] done N times)
- Concurrent blocks (Concurrent: strategy, ← Px-Sy dependencies)
- Both examples match spec character-for-character

Report any discrepancies as findings with [MEDIUM] or [LOW] severity labels. Fix any [MEDIUM] or [CRITICAL] findings immediately in README.md.

/verify README.md STRUT section against specs/_SPEC_STRUT_STRUCTURED_THINKING.md

Constraints:
- Do not modify the spec file - README is the derivative, spec is authority
- Do not add content not present in the spec
- Do not skip any notation element

Verify: All spec notation elements present in README. Any [MEDIUM]+ findings fixed. No [CRITICAL] findings remain.
```
