---
name: write-documents
description: Single source of truth for all document writing - system and planning documents (INFO, SPEC, IMPL, TEST, TASKS, PROMPTS, STRUT, CONVERSATION), document types (articles, reports, ebooks), writing techniques (MINTO, IMINTO, ABTSTORY, KABOB, STA, PAS, AIDA, DIATAXIS, IMRAD), and writing personas. Apply when planning, drafting, reviewing, or writing any document.
---

# Document Writing Skill

Single skill for planning, creating, reviewing, and packaging documents. Root holds system and planning document standards; function subfolders hold deliverable document types, macro-structure writing techniques, and writing personas.

## Routing

Read this file, then jump to exactly one target:

- **Create or edit INFO documents** (research synthesis, analysis, option evaluation) -> `INFO_GUIDES.md`, `INFO_RULES.md`, `INFO_TEMPLATE.md`
- **Create or edit SPEC documents** (technical specifications, requirements, architecture) -> `SPEC_RULES.md`, `SPEC_TEMPLATE.md`
- **Create or edit IMPL plans** (implementation plans, steps, edge cases) -> `IMPL_TEMPLATE.md`
- **Create or edit TEST plans** (test plans, test cases, verification checklist) -> `TEST_TEMPLATE.md`
- **Create or edit TASKS documents** (partitioned work items, model sizing) -> `TASKS_GUIDES.md`, `TASKS_TEMPLATE.md`, `@skills:llm-tools` `MODEL_INVENTORY.md`
- **Create or edit PROMPTS queue files** (headless execution sequences) -> `PROMPTS_GUIDES.md`, `PROMPTS_RULES.md`, `PROMPTS_TEMPLATE.md`, `PROMPTS_ROBUSTNESS_GUIDES.md`, `@skills:llm-tools` `MODEL_INVENTORY.md`
- **Create or insert STRUT plans** (structured execution plans with gates) -> `STRUT_TEMPLATE.md`
- **Create review documents** (`*_CRITIQUE.md`, `*_FACT-CHECK.md` for `/critique`, `/fact-check`) -> `CRITIQUE_TEMPLATE.md`, `FACT-CHECK_TEMPLATE.md`
- **Track implementation fixes** (`_IMPL_[COMPONENT]_FIXES.md`) -> `FIXES_TEMPLATE.md`
- **Record failures and lessons learned** (`FAILS.md`) -> `FAILS_TEMPLATE.md`
- **Track deferred improvements** (`*_DEFERRED_IMPROVEMENTS.md`) -> `DEFERRED_IMPROVEMENTS_TEMPLATE.md`
- **Create or update CONVERSATION documents** (email, WhatsApp) -> `CONVERSATION_RULES.md`, `CONVERSATION_HUMANIZING_RULES.md`, `CONVERSATION_TEMPLATE.md`
- **Create or update SKILL documents** (`SKILL.md` in skills/[name]/) -> `SKILL_GUIDES.md`, `SKILL_RULES.md`, `SKILL_TEMPLATE.md`
- **Create or update WORKFLOW documents** (`.md` in workflows/) -> `WORKFLOW_GUIDES.md`, `WORKFLOW_RULES.md`, `WORKFLOW_TEMPLATE.md`
- **Create or update TEMPLATE files** -> `TEMPLATE_GUIDES.md`, `TEMPLATE_RULES.md`
- **Create or fix ASCII art diagrams** -> `ASCII_ART_GUIDES.md`, `ASCII_ART_RULES.md`
- **Step-by-step investigation log** (`_INVESTIGATION_[TOPIC].md` for `/investigate`) -> `@skills:analysis-methods` `INVESTIGATION_GUIDES.md`, `INVESTIGATION_LOG_RULES.md`, `INVESTIGATION_LOG_TEMPLATE.md`
- **Write articles, reports, or ebooks** (DD-20 coverage: landing pages are articles, user manuals are ebooks, reference documentation is reports) -> `document_types/ARTICLE_GUIDES.md`, `document_types/REPORT_GUIDES.md`, `document_types/EBOOK_GUIDES.md`
- **Apply a writing technique** (macro-structure: MINTO, IMINTO, ABTSTORY, KABOB, STA, PAS, AIDA, DIATAXIS, IMRAD) -> `writing_techniques/README.md`
- **Apply a writing persona** (voice sliders, traits, zero-bullshit baseline) -> `writing_personas/README.md`

## Folder Layout

```
write-documents/
├── SKILL.md                         this file (router)
├── APAPALAN_RULES.md, MECT_WRITING_RULES.md, SOCAS_RULES.md, TRANSLATION_RULES.md
├── [root system and planning GRUC files: INFO_*, SPEC_*, IMPL_*, TEST_*, TASKS_*, PROMPTS_*, STRUT_*, ...]
├── document_types/                  ARTICLE_*, REPORT_*, EBOOK_* (GUIDES, RULES, CHECKS, TEMPLATE)
├── writing_techniques/              README.md, 9 technique sets (GUIDES, RULES, CHECKS, TEMPLATES, EXAMPLES)
└── writing_personas/                README.md, 20 persona files
```

## Shared Rules

- **Writing quality standards**: All documents follow `APAPALAN_RULES.md` (precision, brevity, document structure) and `MECT_WRITING_RULES.md` (voice, word choice, terminology design). Evaluated via `SOCAS_RULES.md`. Translations follow `TRANSLATION_RULES.md`.
- **User-only selection (DRSYNART-DD-08)**: Only the user selects `using <ID>` and `as <persona>`. Without explicit user keywords, the agent follows document-type defaults. Partial selections are never completed; agent suggests library options only when the user explicitly requests advice on style or technique.
- **Discovery by filename pattern (DRSYNART-FR-05)**: Document types are discovered via `document_types/[TYPE]_GUIDES.md`; techniques via `writing_techniques/[ID]_GUIDES.md`; personas via `writing_personas/[PERSONA].md`. Adding a new file requires no edits to workflows or routing tables.
- **Deliverable file naming (DRSYNART-DD-16)**: Deliverable documents follow three sequential file kinds: options proposal `[ID]-OPTIONS-NN_[Title].md`, working draft `[ID]-DRAFT-NN_[Title].md`, and final publication output `YYYY-MM-DD_[Title].md`.
- **CHECKS isolation (DRSYNART-FR-32, GRUC-IG-03)**: CHECKS files are NEVER loaded during execution by `/propose-*`, `/draft-*`, `/write-*`, or any generated prompt. CHECKS are consumed only post-execution by `/drift-detect` (PD) and `/improve` (QI).
- **Consistency layer stack (DRSYNART-FR-35)**: House style (`[AGENT_FOLDER]/rules/core-conventions.md`, `APAPALAN_RULES.md`, `MECT_WRITING_RULES.md`) > Document-type GRUC (`document_types/`) > Technique GRUC (`writing_techniques/`, overrides macro-structure only) > Persona file (`writing_personas/`, adjusts voice only) > Per-document Style Sheet (DRAFT section) > Edit passes. Lower layers add where higher layers are silent and never contradict higher layers.
- **Formatting discipline**: No Markdown tables, no emojis, ASCII quotes, generic examples only (Pre-Write Privacy Gate).

## Quick Commands

Execute deliverable writing workflows using the standard command grammar (`DRSYNART-FR-04`, Section 8.2):

```text
/<verb>-<type> <input> [using <ID>] [as <PERSONA>] [for <audience>] [tier N] [plan | plan only] [N options] [compare techniques <ID>, <ID>] [inline]
```

Examples:
- `/propose-article _INFO_TOPIC-IN01_Summary.md using ABTSTORY`
- `/draft-report REPORT-OPTIONS-01_InfrastructureConsolidation.md`
- `/write-article DRAFT as FOUNDER-ESSAYIST for practitioners`
- `/write-report for executive leadership tier 2`
- `/propose-ebook compare techniques MINTO, STA, DIATAXIS`
- `/write-ebook EBOOK-DRAFT-01_QueueReliabilityHandbook.md as BOOK-AUTHOR`
