# Release Notes: v4.6 (2026-11-10)

## Summary

This release covers work from 2026-11-03 to 2026-11-10, spanning 7 commits across PromptSystemV4.6. Major themes: standardized agent-created utility folders (naming anatomy, core roles, and specification `_SPEC_AGENT_CREATED_FOLDERS.md`), new `AI_WRITING_RULES.md` for publishing document types (article, report, ebook), Signs of Confusion and Sloppiness (SOCAS) redesign research, and a verification pass over `write-documents` and all workflows (Goal/Why, MUST-NOT-FORGET, No Context Match fallback, `@skills:` reference format).

## Changes Since v4.5

### New Rules and Specs

- **`AI_WRITING_RULES.md`** (`write-documents`) - 20 enforceable `AW-*` rules in five categories for suppressing and catching AI writing artifacts in publishing document types; consumed by `/draft-*`, `/write-*`, `/verify`, `/critique`, `/improve`
- **`specs/_SPEC_AGENT_CREATED_FOLDERS.md`** - Single specification for agent-created utility folders: name anatomy (lifecycle prefix, base name, qualifier, git suffix), closed set of core roles, `.tmp_` deletion semantics
- **`specs/AI_WRITING_DETECTION_RULES.md`** - Reworked detection rule set backing `AI_WRITING_RULES.md`

### Agent-Created Folders Standard

- `agent-behavior.md` defines every utility folder (`_agentwork/`, `_archive_gitignore/`, `_sources/`, `.tmp_jpgs/`, `.tmp_extracted/`, and others) in one place; other files reference it
- Skills and scripts aligned with the standard: `renderings`, `llm-tools`, `pdf-tools`, `research-methods`, `analysis-methods`, `session-management`, `workspace-management`
- `/session-archive` runs `/cleanup` first when `_agentwork/` or `.tmp_*` folders remain
- Drift gaps closed and spec numbering corrected (FR-15)

### Workflow and Skill Verification Pass

- **Goal and Why** added to 22 workflows that lacked them (`WF-HD-02`)
- **MUST-NOT-FORGET** added to `prime`, `rename`, `session-archive`, `session-new`, `session-save`, `switch-model`, and to the `write-documents` `SKILL.md`
- **No Context Match** fallback added to `remove`, `research`, `sync`, `test`
- **Skill reference format** unified to `@skills:[name]` in all workflows and `write-documents` files; `WORKFLOW_RULES.md` GOOD example corrected
- References to project documents (`docs/`, `specs/`) removed from skill files (`WF-CT-09`)
- Writing rules, personas, techniques, document types, and workflow files in `write-documents` updated for consistency

### Research and INFO Documentation

- `docs/_INFO_SOCAS_SIGNS_OF_CONFUSION_AND_SLOPPINESS.md` - Redesign of SOCAS into general, writing, communication, and coding rule sets with priorities (proposal; `SOCAS_RULES.md` unchanged in this release)
- `docs/_INFO_SOCAS_DISCARDED_RULE_CANDIDATES.md` - Discard, merge, and defer reasoning for SOCAS candidates
- `docs/_INFO_HOW_TO_DETECT_AI_ASSISTED_WRITING.md`, `docs/_INFO_APAPALAN_PRINCIPLE.md`, `docs/_INFO_HOW_TO_CHECK_FACTUALITY.md`, `docs/_INFO_MECT_PHILOSOPHY.md`, `docs/_INFO_GRUC_GUIDES_RULES_CHECKS.md` updated
- `README.md` synced with V4.6 and the AI writing rules

## Statistics

- **Commits since v4.5**: 7
- **PromptSystem files changed (V4.5 → V4.6)**: 154 (1528 insertions, 783 deletions)
- **Specs and documentation files changed**: 32
- **New rule files**: 1 (`AI_WRITING_RULES.md`)
- **New specs**: 1 (`_SPEC_AGENT_CREATED_FOLDERS.md`)
- **Workflows changed**: 50
- **Total active workflows**: 62
- **Total active skills**: 25
- **Date range**: 2026-11-03 to 2026-11-10
