---
intended_model: claude-sonnet-4-5
context_window_size: 200k
reasoning_settings: high
prompt_system: IPPS
---

## Prompt 1 - Update SKILL_GUIDES.md with TEMPLATE

<!-- Update the GRUC file set section in SKILL_GUIDES.md to include TEMPLATE as a fifth file type. -->

```
Update `PromptSystemV4.4/skills/write-documents/SKILL_GUIDES.md` section 8 (GRUC File Set) to include TEMPLATE as a fifth GRUC file type.

Changes needed:
- Add section 8.5 (or renumber) for SKILL_TEMPLATE.md: optional, provides skeleton structure for documents created with this skill, consumed by `/verify` alongside SKILL_RULES.md
- Update section 8.6 (GRUC Separation Rules) to add: TEMPLATE files contain only structural skeleton and placeholders, no rules, no guidance, no audit items
- Update the References example in section 8.5 to include SKILL_TEMPLATE.md
- Update the Review Checklist to add: "If skill has a template: SKILL_TEMPLATE.md exists with _TEMPLATE suffix"

Constraints:
- Do not change existing sections 8.1-8.4 content, only add TEMPLATE content
- Reference GRUC standard by ID (GRUC-FR-01, GRUC-FR-19) instead of re-defining
- Follow existing formatting (numbered subsections, bold labels)

Verify: Section 8 contains a TEMPLATE subsection. GRUC Separation Rules mention TEMPLATE. References example includes SKILL_TEMPLATE.md. Review Checklist has TEMPLATE item.
```

---

## Prompt 2 - Update WORKFLOW_GUIDES.md with TEMPLATE

<!-- WORKFLOW_GUIDES.md needs TEMPLATE integration for workflow creation guidance. -->

```
Update `PromptSystemV4.4/skills/write-documents/WORKFLOW_GUIDES.md` to integrate TEMPLATE as a fifth GRUC file type for workflow creation.

Changes needed:
- Add guidance for WORKFLOW_TEMPLATE.md: optional skeleton structure for new workflow documents, consumed by `/verify` alongside WORKFLOW_RULES.md
- Update any GRUC file set listing to include TEMPLATE
- Add guidance: "If the workflow has a template, `/verify` checks instantiated workflows against both WORKFLOW_RULES.md and WORKFLOW_TEMPLATE.md"

Constraints:
- Do not re-define GRUC types, reference `specs/_SPEC_GRUC_STANDARD.md [GRUC-SP01]` by ID
- Follow existing formatting and section structure
- Do not duplicate content from SKILL_GUIDES.md

Verify: WORKFLOW_GUIDES.md mentions WORKFLOW_TEMPLATE.md. GRUC file set listing includes TEMPLATE. No content duplicated from SKILL_GUIDES.md.
```

---

## Prompt 3 - Update INFO doc with TEMPLATE as fifth file type

<!-- The explanatory INFO companion document must reflect the five-type GRUC model. -->

```
Update `docs/_INFO_GRUC_GUIDES_RULES_CHECKS.md [GRUC-IN01]` to mention TEMPLATE as the fifth GRUC file type alongside GUIDE, RULES, CHECKS, and EXAMPLE.

Changes needed:
- Update any "four file types" or "four GRUC types" references to "five file types"
- Add TEMPLATE to the file type listing with description: skeleton structure for document creation, consumed by `/verify` alongside RULES
- Update the consumer mapping section to show TEMPLATE -> `/verify` (if template exists)
- Update the lifecycle diagram to show RULES + TEMPLATE consumed by `/verify`

Constraints:
- This is an INFO document (explanatory), not a SPEC (enforceable) - keep the tone explanatory
- Do not copy SPEC content, explain the WHY and HOW
- Reference `specs/_SPEC_GRUC_STANDARD.md [GRUC-SP01]` for the enforceable standard

Verify: No "four file types" or "four GRUC types" text remains. TEMPLATE appears in file type listing. Consumer mapping shows TEMPLATE -> `/verify`. Lifecycle diagram shows RULES + TEMPLATE.
```

---

## Prompt 4 - Sync .devin/ from PromptSystemV4.4/

<!-- The new TEMPLATE_CHECKS.md and updated GRUC files need to be synced to .devin/. -->

```
Sync all changes from `PromptSystemV4.4/` to `.devin/` so both agent folders are identical.

New file to copy:
- `PromptSystemV4.4/skills/write-documents/TEMPLATE_CHECKS.md` -> `.devin/skills/write-documents/TEMPLATE_CHECKS.md`

Files modified in PromptSystemV4.4/ that need sync to .devin/:
- `skills/write-documents/SKILL_GUIDES.md` (updated in prompt 1)
- `skills/write-documents/WORKFLOW_GUIDES.md` (updated in prompt 2)

Sync PromptSystemV4.4/ to .devin/ following the sync workflow's GLOBAL-RULES and Workspace Sync section:

/sync
PromptSystemV4.4/ to .devin/

Verify after sync:
- `TEMPLATE_CHECKS.md` exists in `.devin/skills/write-documents/`
- File contents match between `PromptSystemV4.4/` and `.devin/` copies

Constraints:
- Do not modify any file content during sync, only copy
- Do not sync `.git/` or session folders
```

---

## Prompt 5 - Verify all GRUC SPECs

<!-- Final verification of all updated and new SPEC documents against GRUC standard and project rules. -->

```
Verify the following SPEC files for structural compliance, consistency, and GRUC alignment:

- `specs/_SPEC_GRUC_STANDARD.md [GRUC-SP01]`
- `specs/_SPEC_IPPS_TEMPLATES.md [IPPSTMPL-SP01]`
- `specs/_SPEC_IPPS_SKILLS.md [IPPSSKLS-SP01]`
- `specs/_SPEC_IPPS_WORKFLOWS.md [IPPSWFLW-SP01]`

Verification checks:
- All five GRUC file types (GUIDE, RULES, CHECKS, EXAMPLE, TEMPLATE) are consistently referenced across all SPECs
- `/verify` consumer mapping shows RULES + TEMPLATE consumption in all SPECs
- No content replication between GRUC file type definitions across SPECs
- All cross-references use Doc IDs, not file paths alone
- Acceptance criteria include TEMPLATE where applicable
- No "four file types" remnants - all say "five"

Fix any issues found immediately.

Constraints:
- Do not modify SPEC content beyond fixing GRUC consistency issues
- Do not add new FRs or DDs, only fix existing ones for consistency

Verify: All SPECs reference five file types. All consumer mappings show RULES + TEMPLATE for `/verify`. No "four file types" remnants. No content replication between GRUC definitions.

/verify
against specs/_SPEC_GRUC_STANDARD.md, specs/_SPEC_IPPS_TEMPLATES.md, specs/_SPEC_IPPS_SKILLS.md, specs/_SPEC_IPPS_WORKFLOWS.md
```
