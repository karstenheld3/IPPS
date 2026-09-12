---
intended_model: claude-sonnet-4-5
context_window_size: 200k
effort: high
prompt_system: IPPS
---

<!-- Planning document: __STRUT_PRMTGRUC.md, phases P1-P9
Each prompt implements one phase of the STRUT plan.
Read the STRUT plan and referenced files before starting each prompt. -->

## Prompt 1 - Add PRMT-SC rules to PROMPTS_RULES.md

<!-- P1 [RULES]: Add 6 self-contained prompt rules with BAD/GOOD pairs to PROMPTS_RULES.md -->

```
Read `__STRUT_PRMTGRUC.md` phase P1 and `docs/_INFO_HOW_TO_CREATE_EFFECTIVE_PROMPT_SEQUENCES.md` sections 1.1-1.4, 2, 9 for principles. Treat earlier conversation as compacted. Step P1.
Planning document: `__STRUT_PRMTGRUC.md`, step P1.

Add 6 new rules to `PromptSystemV4.4/skills/write-documents/PROMPTS_RULES.md`:
- PRMT-SC-01: Self-contained opening — every prompt starts with context-loading directive, "treat earlier conversation as compacted", step identifier
- PRMT-SC-02: No conversation dependency — no "the previous step" or "as discussed above" without naming where output lives in a file
- PRMT-SC-03: Idempotency constraint — implementation prompts must include "re-running must not corrupt state or waste cost"
- PRMT-SC-04: Chain length limit — sequences under 6 steps; longer workflows split into sub-chains with checkpoints
- PRMT-SC-05: Effort and model specification — frontmatter must specify intended_model, context_window_size, effort level; prompts scoped to effort budget
- PRMT-SC-06: Planning document reference — prompt sequences from planning documents must reference the document by filename and step ID

Add "Self-Contained (SC)" category to the Rule Index. Write BAD/GOOD pairs for each rule following the existing format in the file.

Constraints:
- Do not modify existing PRMT-* rules
- Follow existing BAD/GOOD pair format exactly
- All examples must use generic content (no real project data)
- Each rule must be verifiable from the prompt file artifact alone
- Re-running this prompt must not corrupt state or waste cost

Verify: Rule Index contains PRMT-SC-01 through PRMT-SC-06. Each rule has BAD/GOOD pair. All rules verifiable from artifact alone.
```

---

## Prompt 2 - Update PROMPTS_GUIDES.md

<!-- P2 [GUIDES]: Fix Section 4 contradiction, add effort partitioning, planning anchor, chain limits, self-contained pattern, idempotency -->

```
Read `__STRUT_PRMTGRUC.md` phase P2 for detailed requirements. Treat earlier conversation as compacted. Step P2.
Planning document: `__STRUT_PRMTGRUC.md`, step P2.

Update `PromptSystemV4.4/skills/write-documents/PROMPTS_GUIDES.md`:

1. FIX Section 4 "Plan State Flow": remove "Later prompts see all earlier conversation" — replace with: each prompt names dependencies by file path, not by conversation reference
2. ADD Section 1c "Effort-Based Partitioning" after Section 1b: effort level determines prompt scope, connect to frontmatter effort and context_window_size
3. ADD Section 1d "Planning Document Anchor" after Section 1c: TASKS or STRUT essential for progress, state, drift control
4. ADD Section 1e "Chain Length Limits" after Section 1d: error compounding data, sub-chain pattern, keep under 6 steps
5. ADD Section 6a "Self-Contained Prompt Pattern" after Section 6: context-loading directive, "treat earlier conversation as compacted", step identifier, context cards
6. ADD Section 6b "Idempotency in Prompts" after Section 6a: pre-execution check, partial execution recovery, write-to-temp-then-rename, cost guard
7. UPDATE Section 12 Review Checklist: add self-containment, effort partitioning, planning document, idempotency, chain length checks
8. ADD placeholder reference "see PROMPTS_EXAMPLE_01" in Section 6a

Constraints:
- Keep GUIDE tone (strategic, not enforceable) — no BAD/GOOD pairs, no rule IDs
- Do not duplicate content from PROMPTS_RULES.md — reference by ID
- Follow existing section numbering pattern
- Do not change existing Sections 1-3, 5-11 content beyond Section 4 fix
- Re-running this prompt must not corrupt state or waste cost

Verify: Section 4 no longer says "Later prompts see all earlier conversation". Sections 1c, 1d, 1e, 6a, 6b exist. Review Checklist includes 5 new checks. Placeholder reference in Section 6a.
```

---

## Prompt 3 - Update PROMPTS_TEMPLATE.md

<!-- P3 [TEMPLATE]: Add effort to frontmatter, self-contained opening, idempotency constraint, planning document reference -->

```
Read `__STRUT_PRMTGRUC.md` phase P3 for detailed requirements. Treat earlier conversation as compacted. Step P3.
Planning document: `__STRUT_PRMTGRUC.md`, step P3.

Update `PromptSystemV4.4/skills/write-documents/PROMPTS_TEMPLATE.md`:

1. UPDATE frontmatter: rename `reasoning_settings` to `effort`, add `low` to values: `effort: [low | medium | high | extra-high]`
2. UPDATE prompt skeleton: add self-contained opening line with context-loading directive, "treat earlier conversation as compacted" statement, and step identifier
3. UPDATE constraints section: add idempotency constraint placeholder: "re-running this prompt must not corrupt state or waste cost"
4. ADD planning document reference placeholder: "Planning document: [TASKS or STRUT filename], step [ID]"
5. UPDATE Full Example at end: reflect self-contained opening, effort in frontmatter, idempotency constraint, planning document reference

Constraints:
- Template must still pass PRMT-FT-01 through PRMT-FT-09 after changes
- Keep XML comment annotations for instructions
- Do not add rules or guidance — template contains only skeleton and placeholders
- Follow existing template structure
- Re-running this prompt must not corrupt state or waste cost

Verify: Frontmatter uses `effort` not `reasoning_settings`. Prompt skeleton includes self-contained opening. Constraints include idempotency. Planning document reference present. Full Example updated.
```

---

## Prompt 4 - Create PROMPTS_CHECKS.md

<!-- P4 [CHECKS]: Create PD + QI checks for prompt writing process and quality -->

```
Read `__STRUT_PRMTGRUC.md` phase P4 and `specs/_SPEC_GRUC_STANDARD.md` GRUC-FR-17 for CHECKS file structure. Treat earlier conversation as compacted. Step P4.
Planning document: `__STRUT_PRMTGRUC.md`, step P4.

Create `PromptSystemV4.4/skills/write-documents/PROMPTS_CHECKS.md` with:

Process Discipline (PD) items — 5 items, each with action + evidence + failure indicator + references:
- PRMT-PD-01: Agent read PROMPTS_GUIDES.md before writing prompts (References: PRMT-CT-11)
- PRMT-PD-02: Agent scanned existing workflows before designing prompts (References: PRMT-CT-11)
- PRMT-PD-03: Agent checked effort budget when partitioning prompts (References: PRMT-SC-05)
- PRMT-PD-04: Agent referenced planning document in prompt sequence (References: PRMT-SC-06)
- PRMT-PD-05: Agent verified prompt file against PRMT-* rules after writing (References: PRMT-ST-01 through ST-05)

Quality Improvement (QI) items — 5 items, each with quality question + improvement tip:
- PRMT-QI-01: Is each prompt self-contained? Could it execute after context reset?
- PRMT-QI-02: Does the sequence stay under 6 steps? Are sub-chains used if longer?
- PRMT-QI-03: Are prompts scoped to the effort budget?
- PRMT-QI-04: Do implementation prompts include idempotency constraints?
- PRMT-QI-05: Does the sequence use context cards for shared state?

Include Check Index at top listing all PD and QI items.

Constraints:
- PD items must be evidence-based (action traces, not output alone)
- QI items must be judgment-based (not binary pass/fail)
- Reference rule IDs, do not replicate rule content
- Follow GRUC-FR-17 structure exactly
- CHECKS must not be referenced in any workflow step the working agent executes
- Re-running this prompt must not corrupt state or waste cost

Verify: File has PD section with 5 items. File has QI section with 5 items. Check Index at top. Each PD item has action + evidence + failure indicator + references. Each QI item has question + improvement tip. No binary pass/fail QI items.
```

---

## Prompt 5 - Create PROMPTS_EXAMPLE_01 and link from GUIDES

<!-- P5 [EXAMPLE]: Create example self-contained prompt sequence, link from GUIDES -->

```
Read `__STRUT_PRMTGRUC.md` phase P5 and `specs/_SPEC_GRUC_STANDARD.md` GRUC-FR-08 for EXAMPLE file rules. Treat earlier conversation as compacted. Step P5.
Planning document: `__STRUT_PRMTGRUC.md`, step P5.

Create `PromptSystemV4.4/skills/write-documents/PROMPTS_EXAMPLE_01-SelfContainedSequence.md`:

A 3-prompt sequence for a generic task (e.g., "SetupProject" or "MigrateAuthModule") demonstrating:
- Frontmatter with intended_model, context_window_size, effort, prompt_system
- Self-contained opening in each prompt (context-loading directive, "treat earlier conversation as compacted", step identifier)
- Idempotency constraints in implementation prompts
- Planning document reference
- Context cards for shared state
- `---` separators between prompts
- Proper fence depths

Structure: Context section (what use case this demonstrates), Document section (the complete prompt file), Key Decisions section (what decisions were made and why).

Then update `PromptSystemV4.4/skills/write-documents/PROMPTS_GUIDES.md` Section 6a: replace the placeholder reference from prompt 2 with an actual link to `PROMPTS_EXAMPLE_01-SelfContainedSequence.md`.

Constraints:
- All content must be generic — no real project data, names, or identifiers (privacy gate)
- Example must pass all PRMT-SC and PRMT-FT rules
- Follow GRUC-FR-08 content rules: no BAD examples, complete or substantial GOOD document
- File naming: `PROMPTS_EXAMPLE_01-SelfContainedSequence.md` per GRUC-FR-07
- Re-running this prompt must not corrupt state or waste cost

Verify: Example file exists with 3 prompts. Each prompt has self-contained opening. Frontmatter includes effort. Implementation prompts have idempotency constraints. No real project data. GUIDES Section 6a links to the example. Example passes PRMT-FT and PRMT-SC rules.
```

---

<!-- CHECKPOINT: Sub-chain 1 complete (P1-P5: content creation). Sub-chain 2 starts below (P6-P9: workflows, sync, verify). Commit and start fresh context. -->

## Prompt 6 - Update write-prompts.md and verify.md workflows

<!-- P6+P7 [WORKFLOW]: Update write-prompts workflow with new principles, update verify workflow with PRMT-SC checks -->

```
Read `__STRUT_PRMTGRUC.md` phases P6 and P7 for detailed requirements. Treat earlier conversation as compacted. Step P6.
Planning document: `__STRUT_PRMTGRUC.md`, step P6.

Update `PromptSystemV4.4/workflows/write-prompts.md`:
1. MUST-NOT-FORGET: add PRMT-SC rules, planning document anchor requirement, effort-based partitioning requirement
2. Step 1: add effort-based partitioning guidance (read frontmatter effort level, scope prompts to effort budget)
3. Step 1: add planning document check (verify TASKS or STRUT exists, reference in prompts)
4. Step 4: add self-contained prompt opening to format overview
5. Step 4: add idempotency constraint to constraints section in format overview
6. Step 5: add PRMT-SC-01 through PRMT-SC-06 to verification checklist
7. Step 5b: add check for self-contained opening in each prompt
8. Quality Gate: add PRMT-SC rules to checklist

Update `PromptSystemV4.4/workflows/verify.md` Prompts Files section:
1. Add PRMT-SC-01 through PRMT-SC-06 to verification checklist
2. Add check for self-contained opening in each prompt
3. Add check for idempotency constraint in implementation prompts
4. Add check for planning document reference in prompt sequences
5. Add check for effort level in frontmatter

Constraints:
- Do not change existing workflow steps beyond the specified additions
- Keep workflow structure and formatting consistent
- Do not duplicate GUIDES content — reference by section
- write-prompts.md and verify.md must not contradict PROMPTS_RULES.md or PROMPTS_GUIDES.md
- Re-running this prompt must not corrupt state or waste cost

Verify: write-prompts.md MUST-NOT-FORGET includes PRMT-SC rules. Step 1 mentions effort partitioning and planning document. Step 4 shows self-contained opening. Step 5 checks PRMT-SC rules. verify.md Prompts section checks PRMT-SC-01 through SC-06.
```

---

## Prompt 7 - Sync and verify all files

<!-- P8+P9 [SYNC+VERIFY]: Sync PromptSystemV4.4/ to .devin/, then verify all files -->

```
Read `__STRUT_PRMTGRUC.md` phases P8 and P9. Treat earlier conversation as compacted. Step P7.
Planning document: `__STRUT_PRMTGRUC.md`, step P8.

Sync all changes from `PromptSystemV4.4/` to `.devin/`:

/sync
PromptSystemV4.4/ to .devin/

Verify after sync:
- `PROMPTS_CHECKS.md` exists in `.devin/skills/write-documents/`
- `PROMPTS_EXAMPLE_01-SelfContainedSequence.md` exists in `.devin/skills/write-documents/`
- All modified files match between `PromptSystemV4.4/` and `.devin/` copies

Then verify all updated files against GRUC standard and PROMPTS rules:

/verify
against `PromptSystemV4.4/skills/write-documents/PROMPTS_RULES.md`, `PromptSystemV4.4/skills/write-documents/PROMPTS_GUIDES.md`, `PromptSystemV4.4/skills/write-documents/PROMPTS_TEMPLATE.md`, `PromptSystemV4.4/skills/write-documents/PROMPTS_CHECKS.md`, `PromptSystemV4.4/skills/write-documents/PROMPTS_EXAMPLE_01-SelfContainedSequence.md`, `PromptSystemV4.4/workflows/write-prompts.md`, `PromptSystemV4.4/workflows/verify.md`

Cross-file consistency checks:
- No content replication between GRUC file types
- Consistent terminology across all files
- Same prefix (PRMT-*) across RULES, CHECKS
- GUIDE references RULES and EXAMPLES
- CHECKS references RULES by ID
- No contradictions between GUIDES, RULES, TEMPLATE, CHECKS, EXAMPLE

Fix any issues found immediately.

Constraints:
- Do not modify tracking documents
- Do not change file content during sync, only copy
- Fix any verification failures immediately
- Re-running this prompt must not corrupt state or waste cost

Verify: All files exist in `.devin/` with matching content. All files pass PRMT-* and PRMT-SC rules. No cross-file inconsistencies.
```
