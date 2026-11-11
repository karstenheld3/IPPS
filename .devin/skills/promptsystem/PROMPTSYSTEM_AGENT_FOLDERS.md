# Agent-Created Folders Rules

Full utility folder standard. The always-loaded definition is `agent-behavior.md` section Agent-Created Folders (name anatomy, prefix and suffix semantics, default folder names, `_agentwork/` content, in short form). This file holds the complete wording plus core role descriptions, allowed parents, classification, extension, generic consumers, and migration. Read it before adding a folder role, registering a module folder, or verifying folder names (WS-SF-02).

## Name Anatomy

`[lifecycle prefix][base name][_qualifier][git suffix]`
- Lifecycle prefix: `_` (persistent) or `.tmp_` (deletable after processing). Required
- Base name: role word, lower case letters, digits, `-`; one base name per role
- Qualifier: `_` + lower case word; names an instance (`_poc_login-flow`) or a derived core role (`_attachments_markdown`); never `gitignore`. Optional
- Git suffix: none (tracked-eligible) or `_gitignore` (never versioned, matched by `*_gitignore/`). Optional

## Prefix and Suffix Semantics

Invariant - no module may redefine them:
- `_` = persistent, skipped by `/prime`
- `.tmp_` = deletable after the producing step; deleted by `/cleanup` without a gate; skipped by `/prime`; ignored by git
- `_gitignore` = never versioned; no suffix = tracked-eligible
- A file that a later step reads or that is kept after the run never starts with `.tmp_`

## Core Roles

Closed set, default form in parentheses:
- `agentwork` (`_agentwork/`) - agent operation artifacts. Single form, ignored as folder
- `archive` (`_archive_gitignore/`) - archived sessions and files, date-stamped zips or subfolders. Sessions go to `[WORKSPACE_FOLDER]/_archive_gitignore/`
- `export` (`_export_gitignore/`) - rendered or transformed output ready for sharing
- `sources` (`_sources/`) - curated evidence of a working folder: transcriptions of downloaded sources, captured web text, screenshots
- `download` (`_download_gitignore/`) - raw downloaded data (PDF, office documents, media)
- `assets` (`_assets/`) - images and diagrams referenced by several markdown files
- `markdown` (`_markdown/`) - 1:1 markdown transcriptions of files in the parent folder
- `jpgs` (`.tmp_jpgs/`) - jpg files only, produced by render steps (PDF pages, video frames)
- `extracted` (`.tmp_extracted/`) - mixed-type extraction output (subtitles, audio tracks, metadata JSON)
- `attachments` (`_attachments_gitignore/`) and `attachments_markdown` (`_attachments_markdown/`) - conversation attachments and their transcripts and translations
- `bugfixes` (`_bugfixes/`) - container of bug folders
- `poc` (`_poc/`, several: `_poc_[name]/`) - proofs of concept and prototypes
- `backup` (`_backup/`) - copies of files before a change
- `test` (`_test/`) - test scripts and test data of a fix or POC

Workflows create the default form. The other prefix or suffix form only when the user or a workspace setting asks for it.

`sources` vs `markdown`: originals in `_download_gitignore/` are transcribed into `_sources/`; user content in a content folder is transcribed into `[content folder]/_markdown/`.

## Allowed Parents

- Working folder (session root, `T##_`, `S##_`, bug folder, `[WORKSPACE_FOLDER]` in PROJECT-MODE): every role except the attachments roles
- Content folder (any folder whose files the agent processes): additionally `export`, `assets`, `markdown`, `jpgs`, `extracted`
- `[WORKSPACE_FOLDER]`: session archives
- `[SESSIONS_FOLDER]`: `bugfixes`
- Conversation folder: only `attachments` and `attachments_markdown`

## Classification

A folder is a utility folder only if its name matches the name anatomy. Names with an upper case letter or a digit after the prefix (`_Sessions`, session folders `_YYYY-MM-DD_[Topic]`) and work-stream folders (session, `T##_`, `S##_`, bug, conversation) are not utility folders.

A `.tmp_` folder holds only content that can be rebuilt from non-`.tmp_` inputs; every step that reads a `.tmp_` folder re-creates it when missing.

## Extension

Modules add folders without editing the rule section:
- First choice: nest inside a core folder (`_download_gitignore/[SOURCE_ID]/`, `.tmp_jpgs/[PDF_NAME]/`). Nested names carry no prefix and no suffix; a core folder is never created inside another core folder
- Fallback: a new base name, only when no core role fits and no other module has one for the same purpose. It must not equal a core role base, `sessions`, or `oldversions`
- A module that adds a new base name lists it in a section `## Agent-Created Folders` of its SKILL.md or workflow file: one line per folder with path, role, parent, creator, content, purpose, and reason. Listing nested use is optional; skip the section where the workflow text already names the folders

## Generic Consumers

Generic consumers know only the base names `agentwork` and `archive`; all other behavior follows prefix and suffix. `/cleanup` deletes `_agentwork/` and `.tmp_*` folders and never descends into `_archive*`. `.gitignore` holds `.tmp_*`, `*_gitignore/`, `_agentwork/`.

`/cleanup` deletes `_agentwork/` recursively (Category 7). `/session-archive` expects no `_agentwork/` and no `.tmp_*` folder to remain.

## `_agentwork/` Content by Writer

**In** (must go into `_agentwork/`):
- `_PROMPTS_*` files (written by `/write-prompts`)
- `__STRUT_*`, `__TASKS_*` scaffolding (written by `/go`, `/deep-research`, `/bugfix`, `/write-strut`)
- `__CARD_*` cards (findings, robustness) - all cards, no exceptions
- `__DRIFT_*`, `DRIFTS.md` (written by `/drift-detect`, consumed by `/drift-correct`)
- `__INFO_*` blocker analyses written by `/go`
- `.tmp_*` temp scripts, data, and command output files (`.tmp_*_out.txt`, `.tmp_*_err.txt`)

**Out** (must NOT go into `_agentwork/`):
- Tracking documents: `NOTES.md`, `PROGRESS.md`, `PROBLEMS.md`, `FAILS.md`, `LEARNINGS.md`
- Deliverables: `_INFO_*`, `_SPEC_*`, `_IMPL_*`, `_TEST_*`
- Review and improve outputs: `*_CRITIQUE.md`, `*_FACT-CHECK.md`, `_vN` backups, `*_DEFERRED_IMPROVEMENTS.md` - these belong beside the document they concern

## Migration

Migration is forward-only: existing folders keep their names and are not renamed or deleted automatically. PromptSystem files, script defaults, and newly created folders use the names defined in the rule section.
