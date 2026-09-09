# Create TOC Workflow

Global workflow for creating Table of Contents in deep research. Used by all research strategies.

## Prerequisites

- `__[SUBJECT]_SOURCES.md` exists with all sources collected and IDs assigned
- [SUBJECT] identifier defined (2-6 uppercase chars, e.g., `MSGRAPH`)
- Full subject name defined (e.g., "Microsoft Graph API")

## Workflow

1. Copy `RESEARCH_TOC_TEMPLATE.md` as base
2. Replace placeholders: `[TOPIC]` → topic ID, `[SUBJECT]` → full name, `[VERSION]` → version/date
3. Create categories: Group topics logically from sources
4. List topic files: One entry per topic - Format: `[\`_INFO_[TOPIC]-IN[XX]_[SUBTOPIC].md\`](./_INFO_[TOPIC]-IN[XX]_[SUBTOPIC].md) [TOPIC-IN[XX]]` (XX = sequential, files sort alphabetically)
5. Add Topic Count section: Total and per-category counts
6. Write Topic Details: Scope, Contents, Sources for each topic
7. Add Related: Related/competing technologies with URLs
8. Write Summary: 5-15 sentences covering all key facts
9. Delete template instructions (HTML comment block)
10. Run quality pipeline: verify → critique → reconcile → implement → verify

## File Naming

Output: `__[SUBJECT]_TOC.md` (double underscore = master document)
Doc ID: `[SUBJECT]-TOC` (not numbered)

## Structure Rules

- Topic Files section: Links only, no checkboxes
- Topic Details section: Scope + Contents + Sources for each topic
- NO Progress Tracking: Progress goes in STRUT or TASKS, not TOC
- Research stats: Added in final phase, not during TOC creation

## Quality Gates

- All sources from `__[SUBJECT]_SOURCES.md` covered
- Doc ID is `[SUBJECT]-TOC` (not numbered)
- Summary is 5-15 sentences
- All topic links follow format above
- Topic Count section present with per-category breakdown
- Related technologies section complete
- `/verify` passes