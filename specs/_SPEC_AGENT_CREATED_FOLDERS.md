# SPEC: Agent-Created Folders

**Doc ID**: AGNTFOLDERS-SP01
**Feature**: agent-created-folders
**Goal**: Define one extendable standard for names, git status, lifecycle, and placement of every subfolder the agent creates, so that modules can add folders without changing the meaning of existing names or the logic of existing workflows
**Timeline**: Created 2026-11-10, Updated 7 times (2026-11-10)
**Target file(s)**:
- `[PROMPTSYSTEM_FOLDER]/rules/agent-behavior.md` (central definition, section File Placement)
- `[PROMPTSYSTEM_FOLDER]/rules/promptsystem-core.md` (folder structure, naming tiers)
- `[PROMPTSYSTEM_FOLDER]/workflows/cleanup.md`, `prime.md`, `session-archive.md` (generic consumers); `archive.md` deferred (DD-12)
- Workflows, skills, and scripts listed in `AGNTFOLDERS-IN01` section 10 (registrations and defaults)
- `[PROMPTSYSTEM_FOLDER]/workflows/bugfix.md`, `conversation-start.md`, `conversation-update.md`, `skills/write-documents/CONVERSATION_RULES.md`, `skills/session-management/SKILL.md` (attachments, bugfixes, poc, backup, test folders)
- `[PROMPTSYSTEM_FOLDER]/skills/workspace-management/` templates and checks: `DEV_REPO_NOTES_TEMPLATE.md`, `COMPANY_REPO_NOTES_TEMPLATE.md`, `WORKSPACE_SETUP_QUESTIONNAIRE.md`, `WORKSPACE_SETUP_REPORT_TEMPLATE.md`, `WORKSPACE-RULES.md` (new workspaces get the standard folders and their `.gitignore` entries)
- Workspace `.gitignore`

**Depends on:**
- `_INFO_WHICH_AGENT_SUBFOLDERS_ARE_CREATED_CURRENTLY.md [AGNTFOLDERS-IN01]` (private session document in `[SESSIONS_FOLDER]/_2026-11-09_StandardizeAgentSubfolders/`) for catalog, conflicts C-01 to C-16, defining files
- `specs/_SPEC_IPPS_SKILLS.md [IPPSSKLS-SP01]` for skill structure that hosts module folder registrations
- `PROBLEMS.md` (workspace) item "archive" for the generic `/archive` workflow (`/archive <input_or_source> <goal_or_target> <options>`); its own SPEC follows. This SPEC fixes only the folder contract `/archive` relies on (FR-15)

**Does not depend on:**
- `specs/_SPEC_WORKSPACE_SETUP_SCHEMA.md` (defines workspace configuration values; this SPEC only consumes `[SESSIONS_FOLDER]` as a configured value)

## MUST-NOT-FORGET

- Folder behavior (git, cleanup, `/prime` skip) is decided by prefix and suffix; consumers know only two base names: `agentwork` and `archive` (FR-10)
- Modules extend by nesting inside core folders first; a new base name only when no core role fits
- Prefix and suffix semantics are invariant; no module may redefine them
- Base names are lower case, one name per role, no synonyms (MECT)
- `.tools` folders outside the repository are out of scope

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Design Decisions](#6-design-decisions)
7. [Implementation Guarantees](#7-implementation-guarantees)
8. [Key Mechanisms](#8-key-mechanisms)
9. [Action Flow](#9-action-flow)
10. [Data Structures](#10-data-structures)
11. [Logging Requirements](#11-logging-requirements)
12. [Technical Constraints](#12-technical-constraints)
13. [Document History](#13-document-history)

## 1. Scenario

**Problem:** Workflows, skills, and scripts pick folder names independently. The inventory `AGNTFOLDERS-IN01` found 36 folder entries, 16 conflicts, and only one centrally defined name (`_agentwork/`). The same purpose has up to 7 names or locations (downloads), case varies (`_SOURCES`, `_Archive`, `_assets`), and `.tmp_` has 6 meanings. Users cannot predict where artifacts land, what git tracks, or what is safe to delete. Every new skill adds another private convention.

**Solution:**
- A folder name is composed of three orthogonal parts: lifecycle prefix, base name (role), git suffix; an optional qualifier names an instance or a derived role
- Generic consumers (`/cleanup`, `/prime`, `.gitignore`, `/archive`) act on prefix and suffix plus the two reserved base names `agentwork` and `archive`, so any new base name inherits correct behavior
- A small set of core roles is defined centrally; modules (skills, workflows) declare additional folders in a registration section of their own file
- Nesting inside a core folder is the preferred extension; new base names are the fallback

**What we don't want:**
- Behavior keyed to specific base names (for example `/cleanup` deleting `_download_gitignore/` by name) - breaks when modules add names
- Synonyms for one role (`transcribed/`, `transcripts/`, `02_transcribed_pages/` for markdown output)
- Modules redefining `.tmp_`, `_gitignore`, or `_` semantics
- A central list that every new module must edit
- Kept inputs named `.tmp_*` (deletable marker on non-deletable content)
- Upper-case base names, or a second base name for a role that already has one

### Architecture Diagram

```text
FOLDER STANDARD - LAYERS
┌──────────────────────────────────────────────────────────────────────────────┐
│ L1 Naming Contract (invariant, rules/agent-behavior.md)                      │
│   [lifecycle prefix] + [base name] + [_qualifier] + [git suffix]             │
│   prefix: _ | .tmp_         suffix: (none) | _gitignore                      │
├──────────────────────────────────────────────────────────────────────────────┤
│ L2 Core Roles (central, closed set)                                          │
│   agentwork  archive  export  sources  download  assets  markdown            │
│   jpgs  extracted  attachments  bugfixes  poc  backup  test                  │
├──────────────────────────────────────────────────────────────────────────────┤
│ L3 Module Registrations (open set, in each module file)                      │
│   1) nested: _download_gitignore/[SOURCE_ID]/  .tmp_jpgs/[PDF_NAME]/         │
│   2) new base name: _[base]/ declared in SKILL.md or workflow                │
├──────────────────────────────────────────────────────────────────────────────┤
│ L4 Generic Consumers (read L1 + base names agentwork, archive)               │
│   .gitignore  /cleanup  /prime  /archive                                     │
└──────────────────────────────────────────────────────────────────────────────┘
Legend: L4 reads L1 plus the base names agentwork and archive, never L3.
```

## 2. Context

- IPPS rules, workflows, and skills live in `[PROMPTSYSTEM_FOLDER]`; `[AGENT_FOLDER]` is a byte-identical mirror
- Existing git patterns already encode two properties by name: `.tmp_*` and `*_gitignore/` are ignored (`AGNTFOLDERS-IN01` section 5)
- `/prime` skips folders starting with `_`; `/cleanup` deletes `_agentwork/` (Category 7) and `.tmp_*` files (Category 1)
- Decisions of 2026-11-10: D1 lower case, D2 tracked and `_gitignore` forms per name, D3 `.tmp_` on folders = deletable after processing, D4 `_agentwork/` ignored as a folder. D5 (sessions folder name) partly resolved: archived sessions go to `[WORKSPACE_FOLDER]/_archive_gitignore/` per the generic `/archive` design; the sessions folder name stays a configured value `[SESSIONS_FOLDER]`
- Work-stream folders (session, topic `T##_`, step `S##_`, bug, conversation) have their own naming rules in `session-management` and `/bugfix`; this SPEC defines only how utility folders inside them are named

## 3. Domain Objects

### Folder Name

A **Folder Name** is the name of an agent-created utility folder, composed of `[lifecycle prefix][base name][_qualifier][git suffix]`.

- `lifecycle prefix` - `_` (persistent) or `.tmp_` (deletable after processing); required
- `base name` - role word, lower case letters and digits, multi-word joined with `-`; required
- `qualifier` - `_` + lower-case letters, digits, `-`; names an instance (`_poc_[name]`) or a derived core role (`_attachments_markdown` = markdown of attachments); never `gitignore`; optional
- `git suffix` - empty (tracked-eligible) or `_gitignore` (never versioned); optional
- Examples: `_sources`, `_download_gitignore`, `.tmp_jpgs`, `.tmp_extracted_gitignore`, `_poc_login-flow`, `_attachments_markdown`

### Lifecycle Prefix

A **Lifecycle Prefix** states how long a folder lives and whether `/prime` reads it.

- `_` - persistent; kept until the user or `/session-archive` moves it; skipped by `/prime`
- `.tmp_` - deletable once the producing step has consumed it; deleted by `/cleanup`; skipped by `/prime`; ignored by git

### Git Suffix

A **Git Suffix** states whether git versions the folder content.

- (none) - tracked-eligible
- `_gitignore` - never versioned, matched by `*_gitignore/`

### Folder Role

A **Folder Role** is the purpose a base name stands for. Core roles are a closed set defined centrally (FR-04). Module roles are an open set declared by modules (FR-08).

- `base` - the base name, unique across core and module roles
- `purpose` - one sentence
- `default form` - the full Folder Name a workflow creates when nothing else is requested
- `allowed parents` - Parent Scopes where the folder may appear

### Parent Scope

A **Parent Scope** is where an agent-created folder may be placed.

- `working folder` - session root, topic folder `T##_*`, step folder `S##_*`, bug folder, or `[WORKSPACE_FOLDER]` in PROJECT-MODE
- `sessions folder` - `[SESSIONS_FOLDER]` (configured value)
- `workspace root` - `[WORKSPACE_FOLDER]`, for workspace-wide folders (archived sessions)
- `content folder` - any folder whose files the agent processes (for example a folder of PDFs being transcribed)
- `bug folder` - `[TOPIC]-BG-NNNN_[IssueDescription]/` or `GLOB-BG-NNNN_[IssueDescription]/` inside `_bugfixes/`
- `conversation folder` - partner folder `[FirstnameLastname]-[Description]/` or session topic subfolder holding `CONVERSATION_*.md`

### Folder Registration

A **Folder Registration** is a declaration in a module file (SKILL.md or workflow) of a folder the module creates, either nested in a core folder or under a new base name.

- `path` - Folder Name plus nested path, with placeholders (for example `.tmp_jpgs/[PDF_NAME]/`)
- `role` - core role or module role base
- `parent` - Parent Scope
- `creator` - workflow, step, or script that creates it
- `content` - what it holds
- `purpose` - only for a new module role

## 4. Functional Requirements

**AGNTFOLDERS-FR-01: Name anatomy**
- Every agent-created utility folder name matches `[lifecycle prefix][base name][_qualifier][git suffix]` (Domain Object Folder Name)
- A qualifier names either an instance of the role (`_poc_[name]`, name in lower case) or a derived core role applied to the base role's content (`_attachments_markdown`); a derived qualifier must be a core role base, and an instance name must not equal a core role base
- Base names start with a lower-case letter and contain only lower-case letters, digits, and `-`; one base name per role
- Classification by name: a folder is a utility folder only if its name matches this pattern. Names with an upper-case letter after the prefix (`_Sessions`, `_BugFixes`, `_PrivateSessions_gitignore`) or a digit after the prefix (session folders `_YYYY-MM-DD_[Topic]`) are not utility folders, and consumers do not apply utility-folder behavior to them
- Work-stream folders (session, topic, step, bug, conversation) keep their own patterns and are not utility folders

**AGNTFOLDERS-FR-02: Prefix semantics are invariant**
- `_` = persistent utility folder, skipped by `/prime`
- `.tmp_` = deletable after the producing step; deleted by `/cleanup`; skipped by `/prime`; ignored by git
- `/cleanup` deletes without a gate and may run while a pipeline is still in progress. Therefore a `.tmp_` folder holds only content that can be rebuilt from non-`.tmp_` inputs, and every step that reads a `.tmp_` folder re-creates it when it is missing instead of failing
- No module may give either prefix another meaning
- Agent-created utility folders without a lifecycle prefix are not allowed

**AGNTFOLDERS-FR-03: Suffix semantics are invariant**
- `_gitignore` = never versioned; no suffix = tracked-eligible
- `.tmp_` folders are ignored regardless of suffix; `.tmp_[base]_gitignore` is allowed and redundant
- No module may give the suffix another meaning

**AGNTFOLDERS-FR-04: Core roles**
- `agentwork` - agent operation artifacts: `_PROMPTS_*`, `__STRUT_*`, `__TASKS_*`, `__CARD_*`, `__DRIFT_*`, `DRIFTS.md`, `.tmp_*` scripts and outputs, intermediate chapter files. Default `_agentwork/`. Parents: working folder
- `archive` - archived sessions, superseded or less relevant files, date-stamped zip files. Default `_archive_gitignore/`. Parents: workspace root (sessions), working folder (files)
- `export` - rendered or transformed output ready for sharing. Default `_export_gitignore/`. Parents: working folder, content folder
- `sources` - curated evidence set of a working folder: transcriptions of downloaded sources, captured web text, screenshots, legislation texts. Default `_sources/`. Parents: working folder
- `download` - raw downloaded data: PDF, office documents, media files. Default `_download_gitignore/`. Parents: working folder
- `assets` - images and diagrams referenced by several markdown files. Default `_assets/`. Parents: working folder, content folder
- `markdown` - 1:1 markdown transcriptions of files that sit in the parent folder. Default `_markdown/`. Parents: content folder, working folder
- Disambiguation `sources` vs `markdown`: originals in `_download_gitignore/` are transcribed into `_sources/`; originals that are user content in a content folder are transcribed into `[content folder]/_markdown/`; conversation attachments are transcribed into `_attachments_markdown/`
- `jpgs` - jpg files only, produced by render steps (PDF pages, video frames). Default `.tmp_jpgs/`. Parents: content folder, working folder
- `extracted` - mixed-type extraction output: subtitles, audio tracks, metadata JSON, database extracts. Default `.tmp_extracted/`. Parents: content folder, working folder
- `attachments` - binary attachments of a conversation (PDF, ZIP, images) in subfolders `YYYY-MM-DD_HH-MM_[Topic]/`. Default `_attachments_gitignore/`. Parents: conversation folder
- `attachments_markdown` (derived) - transcripts `[file].md` and translations `[file]_en.md` of attachments, same subfolders as `attachments`. Default `_attachments_markdown/`. Parents: conversation folder
- `bugfixes` - container of bug folders: `[TOPIC]-BG-NNNN_*` in SESSION-MODE; permanent bug session with `GLOB-BG-NNNN_*` folders in PROJECT-MODE, never archived. Default `_bugfixes/`. Parents: working folder (session root), sessions folder
- `poc` - proofs of concept, prototypes, self-contained test scripts (IMPL-ISOLATED). Default `_poc/`; several POCs side by side: `_poc_[name]/`. Parents: working folder, bug folder
- `backup` - copies of files before a change, used for BEFORE/AFTER comparison. Default `_backup/`. Parents: bug folder, working folder
- `test` - test scripts and test data of a fix or POC. Default `_test/`. Parents: bug folder, working folder

**AGNTFOLDERS-FR-05: Default and alternative forms**
- Workflows create the default form of a role (FR-04)
- The other prefix or suffix form is created only when the user asks for it or a workspace setting requests it (for example `_download/` to version raw downloads, `_jpgs/` to keep page images)
- Exception: `agentwork` has only the form `_agentwork/`; it is ignored as a folder (DD-04)

**AGNTFOLDERS-FR-06: Placement**
- A folder appears only in an allowed Parent Scope of its role
- Every working folder has its own utility folders; a topic folder does not write into the session root `_sources/`
- Archived sessions go to `[WORKSPACE_FOLDER]/_archive_gitignore/`; archived files of a working folder go to that folder's `_archive_gitignore/`

**AGNTFOLDERS-FR-07: Extension by nesting (preferred)**
- A module whose content fits a core role writes into a subfolder of that core folder (for example `_download_gitignore/[SOURCE_ID]/`, `.tmp_jpgs/[PDF_NAME]/`, `_markdown/[DOC_NAME]/`)
- Nested subfolders inherit lifecycle and git status from the core folder
- Nested subfolder names carry no lifecycle prefix and no git suffix
- A core role folder is never created directly inside another core role folder (for example no `_download_gitignore/_markdown/`); nested content inherits the outer folder's git status, which would silently override the inner default. Container roles (`bugfixes`, `archive`) hold work-stream folders (bug folders, sessions), and those may hold core folders
- Nested subfolder names are free-form but use placeholders documented in the Folder Registration

**AGNTFOLDERS-FR-08: Extension by new base name (fallback)**
- Allowed only when no core role fits the purpose; the registration states why
- The module declares the folder in a section `## Agent-Created Folders` of its SKILL.md or workflow file (Folder Registration, section 10)
- The base name follows FR-01, must not equal a core role base, a reserved name (FR-13), or another module's base name
- Prefix and suffix follow FR-02 and FR-03; generic consumers then handle the folder without change (FR-10)
- If two modules need the same purpose, the second reuses the first module's base name instead of adding a synonym; a base name used by 3 or more modules is a candidate for promotion to a core role (DD-06)

**AGNTFOLDERS-FR-09: Registration of nested use**
- A module that writes into a core folder also declares this in its `## Agent-Created Folders` section, with path and creator
- Purpose: a grep over `## Agent-Created Folders` sections lists every folder the system creates

**AGNTFOLDERS-FR-10: Generic consumers act on prefix, suffix, and two reserved base names**
- Consumers know exactly two base names: `agentwork` (deletion target of `/cleanup`) and `archive` (target of `/archive`, never descended); every other behavior comes from prefix and suffix
- `.gitignore` holds `.tmp_*`, `*_gitignore/`, `_agentwork/`; no entry per base name
- `/cleanup` deletes `_agentwork/` and `.tmp_*` folders in its scope; it never deletes a folder because of its base name; it never descends into `_archive*` folders
- `/prime` skips folders starting with `_` or `.tmp_`
- `/archive` selects archivable items by affix (FR-15) and writes into the `archive` role folder of the target scope
- `/session-archive` is `/archive session` with the session folder as source and `[WORKSPACE_FOLDER]/_archive_gitignore/` as target
- Adding a third base name to consumer logic requires a SPEC update

**AGNTFOLDERS-FR-11: Scaffolding placement**
- `_PROMPTS_*`, `__STRUT_*`, `__TASKS_*`, `__CARD_*`, `__DRIFT_*`, `DRIFTS.md`, `__INFO_*` blocker analyses go into `_agentwork/` of the working folder
- No workflow leaves scaffolding location open

**AGNTFOLDERS-FR-12: Kept files never carry `.tmp_`**
- A file read by a later step or kept after the run does not start with `.tmp_`
- Extracted data that a later step reads goes into the `extracted` role folder (for example `.tmp_extracted/[TOPIC]_youtube-metadata.json`); the folder prefix marks it deletable after that later step, the file name carries no `.tmp_`
- Multi-run scaffolding uses the `__` prefix (existing rule)

**AGNTFOLDERS-FR-13: Reserved names and prefixes**
- Reserved base names: the core role bases (FR-04), plus `sessions`, `oldversions`
- Reserved prefixes for other purposes: `__` (scaffolding files), `!` (priority files and permanent sessions)
- Reserved suffix: `_gitignore`

**AGNTFOLDERS-FR-14: Retired names**
- Names listed in section 10 Migration Map are retired; workflows, skills, and script defaults use the new names
- A retired name found in `[PROMPTSYSTEM_FOLDER]` after migration is a defect

**AGNTFOLDERS-FR-15: Archive folder contract (used by `/archive`)**
- Scopes: 1) session files → `[SESSION_FOLDER]/_archive_gitignore/`; 2) sessions → `[WORKSPACE_FOLDER]/_archive_gitignore/`; 3) files of any folder (with or without subfolders) → that folder's `_archive_gitignore/`
- Content forms inside an archive folder: moved items keeping their relative path, date-stamped zip files `YYYY-MM-DD_[Description].zip`, date-stamped subfolders `YYYY-MM-DD_[Description]/`
- Leading date = archive creation date; an optional time range `[Description]-From-YYYY-MM-DD-To-YYYY-MM-DD` uses the earliest and latest last-modified dates of the archived items (valid calendar dates only)
- Zip mode deletes originals only after the zip is verified: entry count and total uncompressed size match the selected items; on mismatch the zip is deleted, originals stay, and the run reports failure
- An existing archive file or folder with the same name is never overwritten; the new name gets a `_v2`, `_v3` suffix
- The tracked form `_archive/` is used only when the user or a workspace setting requests versioned archives (FR-05)
- Never archived: `_archive*` folders themselves (no re-archiving), `.tmp_*` items (deleted by `/cleanup`, not archived)
- Session scope selects only session folders (`_YYYY-MM-DD_*`); utility folders such as `_bugfixes/` (permanent bug session) are never archived as a whole
- Archivable item selection (which files count as intermediate or less relevant) belongs to the `/archive` SPEC; it must use names and affixes only, never module-specific folder lists (FR-10)
- Preview output (`/archive preview ...`, `/archive propose ...`) is a temp file `_agentwork/.tmp_archive_files_vNN.txt` of the working folder; preview never moves or zips
- Modules archive their own content by nesting under the archive folder (FR-07), for example `_archive_gitignore/YYYY-MM-DD_[Description]/`

## 5. Non-Functional Requirements

**AGNTFOLDERS-NFR-01: Maintainability - zero-touch extension**
- Adding a module folder that follows FR-07 or FR-08 requires 0 edits in rules, `/cleanup`, `/prime`, `/archive`, or `.gitignore`
- Verification: add a test registration with a new base name in a scratch skill; `git check-ignore` and the `/cleanup` scan step (scan only, no delete) show the expected behavior without other edits

**AGNTFOLDERS-NFR-02: Predictability - name tells behavior**
- From the folder name alone a reader can tell: deleted by `/cleanup` (yes/no), versioned (yes/no), read by `/prime` (yes/no)
- Verification: the three answers follow from prefix and suffix for every core role and registration

**AGNTFOLDERS-NFR-03: Backward compatibility - existing folders keep working**
- Existing on-disk folders with retired names are not deleted by any consumer and not renamed automatically (DD-13)
- Verification: the `/cleanup` scan step (scan only, no delete) on a workspace with legacy names lists none of them; references in existing documents (for example links to `_SOURCES/...`) still resolve

## 6. Design Decisions

**AGNTFOLDERS-DD-01:** Folder names have three orthogonal parts plus an optional qualifier; behavior comes from prefix and suffix, meaning from the base name; `agentwork` and `archive` are the only base names consumers know (FR-10). Rationale: generic consumers stay unchanged when modules add base names (NFR-01); the existing `.gitignore` patterns already work this way.

**AGNTFOLDERS-DD-02:** All base names lower case (decision D1, 2026-11-10). Rationale: removes the case variants `_SOURCES`, `_Archive`, `_EXPORT_gitignore`, `_DOWNLOADS_gitignore`; matches the most used name `_agentwork`.

**AGNTFOLDERS-DD-03:** Every role has a tracked form and a `_gitignore` form; each core role names one default (decision D2). Rationale: git status is chosen per use without `.gitignore` edits.

**AGNTFOLDERS-DD-04:** `_agentwork/` is ignored as a folder and has a single form (decision D4). Rationale: agent artifacts are never deliverables; today `_PROMPTS_*`, `*.jsonl`, `DRIFTS.md` inside it are tracked-eligible by accident. Consequence: prompt files are no longer versioned.

**AGNTFOLDERS-DD-05:** `.tmp_` on a folder means deletable after processing, and `/cleanup` deletes such folders without a gate (decision D3). Only rebuildable content goes into `.tmp_` folders; consuming steps rebuild a missing `.tmp_` folder (FR-02). Rationale: one meaning for one marker; `/cleanup` has no confirmation step, so safety comes from rebuildability, not from timing.

**AGNTFOLDERS-DD-06:** Core roles are a closed set; module roles are an open set. A module role used by 3 or more modules is promoted to a core role by a SPEC update. Rationale: keeps the core small while letting proven names become standard.

**AGNTFOLDERS-DD-07:** Folder Registrations live in the module's own file, not in a central list. Rationale: adding a module never requires editing a rule file; a grep over all registrations lists every folder and shows collisions.

**AGNTFOLDERS-DD-08:** Folders in `[WORKSPACE_FOLDER]/../.tools/` are out of scope. Rationale: outside the repository, shared across workspaces, protected by `/cleanup`; their own lifecycle is defined by each tool's SETUP guide.

**AGNTFOLDERS-DD-09:** Archived sessions go to `[WORKSPACE_FOLDER]/_archive_gitignore/` and leave the working tree of the repository on purpose; git history keeps their content. The sessions folder name stays a configured value `[SESSIONS_FOLDER]`. Rationale: archived sessions no longer clutter the tracked tree, and history makes them recoverable. The generic `/archive` design (workspace `PROBLEMS.md`) archives sessions to the workspace archive folder; workspaces already use different sessions folder names (`AGNTFOLDERS-IN01` C-02), so only the archive location is fixed.

**AGNTFOLDERS-DD-10:** Conversation partner folders `[FirstnameLastname]-[Description]/`, session topic subfolders, and bug folders `[TOPIC]-BG-NNNN_*` are work-stream folders (FR-01) and keep their names. Rationale: they are named after a counterparty or a tracking ID, not a role (`AGNTFOLDERS-IN01` C-11, C-12).

**AGNTFOLDERS-DD-11:** `/cleanup` and `/archive` never descend into `_archive*` folders. Rationale: archived content is kept as it was, including any `_agentwork/` left by older sessions, and is never archived twice.

**AGNTFOLDERS-DD-12:** One generic `/archive` workflow replaces scope-specific archive logic; `/session-archive` becomes a preset of `/archive`. Rationale: one consumer for the `archive` role keeps archive semantics in one place; default `_archive_gitignore/` follows the `/archive` design and D2. Staging (user, 2026-11-10): `/archive` is built later in session `_2026-11-03_GenericWorkflowSyntax` (AGENSYNTAX) against FR-15. Until then `/session-archive` stays a standalone workflow with the new target `[WORKSPACE_FOLDER]/_archive_gitignore/` and the FR-10 checks.

**AGNTFOLDERS-DD-13:** Migration is forward-only. New names apply to `[PROMPTSYSTEM_FOLDER]` files, script defaults, and folders created after the change; existing session folders, archived sessions, and their documents keep their folder names. Moving existing archives or sessions happens only through an explicit `/archive` run. Rationale: existing INFO documents link to `_SOURCES/...` and similar paths; a retroactive rename breaks those links, and Windows case-only renames need extra git steps per folder.

**AGNTFOLDERS-DD-14:** Attachments, bug containers, POCs, backups, and tests become core roles (`attachments`, `attachments_markdown`, `bugfixes`, `poc`, `backup`, `test`). Rationale: they were the last agent-created folders without a lifecycle prefix; with the prefix, `/prime` skips them and `/cleanup` needs no special protection for `backup/` because affix rules never delete `_backup/`. A qualifier (`_attachments_markdown`, `_poc_[name]`) expresses derived content and multiple instances without new base names.

## 7. Implementation Guarantees

**AGNTFOLDERS-IG-01:** No consumer deletes an agent utility folder (FR-01) unless its name is `_agentwork` or starts with `.tmp_`. Unchanged: `/cleanup` Category 2 tool caches (`__pycache__/` and similar) and explicit `/remove` targets.

**AGNTFOLDERS-IG-02:** Every folder that a workflow, skill, or script default creates is either a core role folder (FR-04), declared in a `## Agent-Created Folders` section, a work-stream folder (FR-01), or exempt by DD-10.

**AGNTFOLDERS-IG-03:** A case-sensitive grep for every retired name in section 10 returns 0 hits in `[PROMPTSYSTEM_FOLDER]`.

**AGNTFOLDERS-IG-04:** `[AGENT_FOLDER]` is byte-identical to `[PROMPTSYSTEM_FOLDER]` after the change (MD5 compare).

**AGNTFOLDERS-IG-05:** `git check-ignore` confirms: `_agentwork/`, `.tmp_[base]/`, `_[base]_gitignore/` ignored; `_[base]/` tracked-eligible, for every core role.

## 8. Key Mechanisms

### Behavior from affixes

Consumers derive behavior from the name, in this order:

- Name does not match the utility pattern (FR-01) → not a utility folder; consumers apply their existing rules
- Name starts with `_archive` → `/cleanup` and `/archive` never descend; git: by suffix; `/prime` reads: no
- Name is `_agentwork` → `/cleanup` deletes: yes; git: ignored; `/prime` reads: no
- Name starts with `.tmp_` → `/cleanup` deletes: yes; git: ignored; `/prime` reads: no
- Name starts with `_` and ends with `_gitignore` → `/cleanup` deletes: no; git: ignored; `/prime` reads: no
- Name starts with `_` → `/cleanup` deletes: no; git: tracked-eligible; `/prime` reads: no

### Extension decision

A module that needs a folder chooses in this order:

1) Content fits a core role → nest in the core folder (FR-07)
2) Another module already registered a base name for the same purpose → reuse it (FR-08)
3) Otherwise → new base name with registration and reason (FR-08)

## 9. Action Flow

```text
Module author needs a folder for new content
├─> Does a core role fit? (FR-04)
│   ├─> Yes: write into [core folder]/[nested]/  (FR-07)
│   │   └─> Add path to "## Agent-Created Folders" in module file (FR-09)
│   └─> No: search all "## Agent-Created Folders" sections for same purpose
│       ├─> Found: reuse that base name (FR-08)
│       └─> Not found: choose base name, lifecycle prefix, git suffix (FR-01 to FR-03)
│           └─> Add registration with purpose and reason (FR-08)
└─> Generic consumers handle the folder, no other edits (NFR-01)

/cleanup [scope]
├─> Find folders named _agentwork or starting with .tmp_ (skip _archive*)
├─> List found folders in chat (information only, no gate)
└─> Delete listed folders immediately (IG-01)

Pipeline step that reads .tmp_jpgs/[PDF_NAME]/
├─> Folder exists → use it
└─> Folder missing (deleted by /cleanup) → re-render from the PDF, then continue (FR-02)

/archive <input_or_source> <goal_or_target> <options>
├─> Resolve scope: session files | session | folder (with or without subfolders)
├─> Select archivable items by name and affix (skip _archive*, .tmp_*) (FR-15)
├─> preview | propose: write _agentwork/.tmp_archive_files_vNN.txt, present, stop
├─> zip: create [target]/_archive_gitignore/YYYY-MM-DD_[Description].zip, remove zipped originals
└─> move: move items to [target]/_archive_gitignore/ keeping relative paths

/session-archive [SESSION_FOLDER]  (preset of /archive)
├─> /cleanup [SESSION_FOLDER]
├─> Check: no _agentwork/ and no .tmp_* folder left
└─> /archive session: move session folder to [WORKSPACE_FOLDER]/_archive_gitignore/, commit removal
```

## 10. Data Structures

### Folder Registration section

Every module that creates folders has this section in its SKILL.md or workflow file. Example for a hypothetical audio skill (generic):

```markdown
## Agent-Created Folders

- `_download_gitignore/[SOURCE_ID]/` - role: download; parent: working folder; creator: Step 2 download script; content: original audio files
- `.tmp_extracted/[SOURCE_ID]/` - role: extracted; parent: working folder; creator: Step 3 split script; content: audio segments, metadata JSON
- `_markdown/` - role: markdown; parent: working folder; creator: Step 4 transcription; content: one transcript per audio file
- `_recordings_gitignore/` - role: recordings (module role); parent: working folder; creator: Step 1 capture script; content: live microphone captures
  - Purpose: raw captures made by the agent, not downloaded
  - Reason: `download` means fetched from a remote source; captures have no source URL
```

Rules for entries: one line per folder; `role` is a core role base or a module role base; module role entries add `Purpose` and `Reason`.

### Directory example

```text
[SESSION_FOLDER]/
├── _agentwork/                      ignored, deleted by /cleanup
├── _sources/                        tracked
├── _download_gitignore/             ignored, kept
│   └── [SOURCE_ID]/                 nested, inherits
├── _export_gitignore/               ignored, kept
├── _assets/                         tracked
├── _archive_gitignore/              ignored, kept; moved files, YYYY-MM-DD_*.zip
├── _poc_[name]/                     tracked
├── _bugfixes/                       tracked, container
│   └── [TOPIC]-BG-0001_[Issue]/     bug folder (work-stream)
│       └── _agentwork/  _backup/  _test/  _poc/
├── [ConversationTopic]/             conversation folder (work-stream)
│   ├── _attachments_gitignore/YYYY-MM-DD_HH-MM_[Topic]/
│   └── _attachments_markdown/YYYY-MM-DD_HH-MM_[Topic]/
├── input-pdfs/                      content folder (user content)
│   ├── _markdown/                   tracked
│   └── .tmp_jpgs/[PDF_NAME]/        ignored, deleted by /cleanup
└── T01_[SUBTOPIC]_[Description]_YYYY-MM-DD/
    ├── _agentwork/
    └── _sources/
```

### Migration Map

Retired names (FR-14) and their targets:

- `_DOWNLOADS_gitignore/` → `_download_gitignore/`
- `[DOWNLOAD_FOLDER]` (undefined placeholder) → `_download_gitignore/`
- `_EXPORT_gitignore/` → `_export_gitignore/`
- `render.py` default "next to each input" → `_export_gitignore/` next to the input
- `_SOURCES/` → `_sources/`
- `_Archive/`, `Archive/`, `_sessions/_archive/`, `[SESSIONS_FOLDER]/_Archive/` → `[WORKSPACE_FOLDER]/_archive_gitignore/`
- `transcribed/`, `02_transcribed_pages/`, `transcripts/` → `_markdown/`
- `pdf_images/` → `.tmp_jpgs/`
- `compressed/` → `_download_gitignore/compressed/` (nested)
- `_agent_work/` (legacy on disk) → `_agentwork/`
- `_agentwork/.tmp_STRUT_IMPROVE_*.md` → `_agentwork/__STRUT_IMPROVE_*.md`
- `_agentwork/.tmp_INFO_[BLOCKER].md` → `_agentwork/__INFO_[BLOCKER].md`
- `.tmp_[TOPIC]_youtube-metadata.json` → `.tmp_extracted/[TOPIC]_youtube-metadata.json`
- `agent-behavior.md` lifecycle line "Commit `__` files along with task or session files" → removed; `__*.md` and `_agentwork/` are never committed (existing `__*.md` ignore pattern, DD-04)
- `__DRIFT_*.md`, `DRIFTS.md` in the working folder → `_agentwork/`
- `__STRUT_*.md`, `__TASKS_*.md`, `__[TOPIC]_TOC.md` outside `_agentwork/` (bug folder, topic folder) → `_agentwork/` of that folder
- `*.jsonl` guard and `partition-observations.jsonl` in `/cleanup` and `agent-behavior.md` → removed (no producer exists, `AGNTFOLDERS-IN01` section 6.3)
- `Attachments_gitignore/` → `_attachments_gitignore/`
- `Attachments/` (transcripts and translations) → `_attachments_markdown/`
- `_BugFixes/` → `_bugfixes/`; `[BUGFIXES_FOLDER]` default `[SESSIONS_FOLDER]/_bugfixes/`
- `poc/` → `_poc/` or `_poc_[name]/`
- bug folder `backup/` → `_backup/`; `test/` → `_test/`
- `/cleanup` Protected Location `*/backup/` inside `_BugFixes/` → removed (affix rules never delete `_backup/`)

Not migrated: `.tools` folders (DD-08); conversation partner folders, session topic subfolders, bug folders (work-stream, DD-10); unregistered user folders found on disk (`_input`, `_output`, `_Discarded`).

## 11. Logging Requirements

N/A: this SPEC defines naming and placement rules for instruction files; no component produces runtime output. Script default changes keep the existing logging of each script.

## 12. Technical Constraints

- `.gitignore` patterns `.tmp_*` and `*_gitignore/` exist and match folders at any depth; `_agentwork/` must be added
- Windows file systems are case-insensitive; an agent asked to create `_archive/` or `_sources/` next to an existing `_Archive/` or `_SOURCES/` writes into the existing folder. Forward-only migration (DD-13) accepts this for existing sessions
- `[AGENT_FOLDER]` is a mirror of `[PROMPTSYSTEM_FOLDER]`; edits go to the source and are copied
- `/prime` file discovery skips names by prefix; `.tmp_` must be added to its skip list
- Script defaults (`render.py`, `transcribe-image-to-markdown.py`, `convert-pdf-to-jpg.py` when called with an explicit output, YouTube download scripts) change behavior for callers that rely on the old default; workflow call sites are updated in the same change set
- Existing archived sessions may hold `_agentwork/` folders; DD-11 keeps them untouched
- Moving a tracked session into `_archive_gitignore/` removes it from the tracked tree on the next commit; git history keeps the content (intended, DD-09). Workspaces that want archived sessions in the tracked tree use `_archive/` (FR-15)
- `/cleanup` has no confirmation step: its listing is printed and deletion follows immediately (`workflows/cleanup.md`)
- Zip creation on Windows uses built-in PowerShell archive commands; no extra tool dependency
- `[BUGFIXES_FOLDER]` is a configured value in `!NOTES.md`; workspaces with an existing `_BugFixes/` permanent session keep it (DD-13) until the user moves it

## 13. Document History

**[2026-11-10 17:50]**
- Removed: former FR-15 (`/verify` collision and conformance check) and all `/verify` references (architecture diagram, DD-07, Action Flow); `WORKSPACE-RULES.md` WS-SF-02 covers the name anatomy
- Changed: former FR-16 (archive folder contract) renumbered to FR-15; history entries below this one keep the old numbers

**[2026-11-10 17:40]**
- Changed: implementation deviations recorded after STRUT execution - research PDF page transcripts go to `_sources/[PDF_NAME]/` (FR-04 disambiguation); `/transcribe` page transcripts go to `_markdown/[DocName]/`; registration sections are required only where a module adds a new base name (nested use optional), removed from `/conversation-start`, `/conversation-update`, and `/verify` on user request
- Added: allowed parent folders per role in `agent-behavior.md` (FR-06)

**[2026-11-10 17:25]**
- Changed: DD-12 staging - `/archive` deferred to session AGENSYNTAX; `/session-archive` keeps standalone logic with new target; `archive.md` removed from this change set
- Added: `workspace-management` templates and checks to target files (session decision AGNTFOLDERS-DD-B)

**[2026-11-10 17:15]**
- Added: FR-02 and DD-05 - `.tmp_` folders hold only rebuildable content; consuming steps rebuild missing `.tmp_` folders, because `/cleanup` deletes without a gate
- Changed: DD-09 - archived sessions leaving the tracked tree is intended; git history keeps them
- Fixed: Action Flow `/cleanup` - listing is information only, no preview gate; added rebuild flow for a pipeline step

**[2026-11-10 17:05]**
- Added: optional qualifier part (`_poc_[name]`, `_attachments_markdown`) in Folder Name, FR-01, diagram
- Added: core roles `attachments`, `attachments_markdown`, `bugfixes`, `poc`, `backup`, `test` (FR-04, DD-14); Parent Scopes `bug folder`, `conversation folder`
- Changed: DD-10 now covers only work-stream folders; FR-07 container roles; FR-13 reserved names; FR-16 session scope never archives `_bugfixes/`
- Added: Migration Map entries for attachments, bug, poc, backup, test folders; `/cleanup` backup protection removed

**[2026-11-10 16:50]**
- Changed: FR-10, MNF, DD-01, diagram - consumers know two base names (`agentwork`, `archive`); the "prefix and suffix only" claim contradicted the `_archive*` skip rule (inline `/critique`)
- Added: FR-01 classification pattern separating utility folders from `_Sessions`, `_BugFixes`, session folders
- Added: `sources` vs `markdown` disambiguation (FR-04); no core folder inside another core folder (FR-07)
- Added: FR-16 zip verification before deleting originals, date-range definition, no overwrite
- Added: DD-13 forward-only migration; NFR-03 and technical constraints aligned
- Changed: YouTube metadata target `_agentwork/` → `.tmp_extracted/` (FR-12, Migration Map); added removal of the "Commit `__` files" rule

**[2026-11-10 16:30]**
- Changed: `archive` role default `_archive/` → `_archive_gitignore/`; sessions archive moved to `[WORKSPACE_FOLDER]/_archive_gitignore/` (generic `/archive` design in workspace `PROBLEMS.md`)
- Added: FR-16 archive folder contract, DD-12 generic `/archive`; `/archive` in consumer layer
- Changed: DD-09, DD-11, FR-06, FR-10, Action Flow, Migration Map, directory example

**[2026-11-10 16:10]**
- Initial specification created from `AGNTFOLDERS-IN01` and decisions D1-D4




