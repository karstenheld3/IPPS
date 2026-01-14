# Implementation Plan: DevSystem V1 to V2 Migration Using Skills

**Plan ID**: MIG-IP01
**Goal**: Migrate DevSystem from rules-only to Skills-based architecture while preserving all functionality.

**Target files**:
- `[WORKSPACE_FOLDER]/DevSystemV2/rules/devsystem-core.md` (NEW)
- `[WORKSPACE_FOLDER]/DevSystemV2/rules/core-conventions.md` (NEW)
- `[WORKSPACE_FOLDER]/DevSystemV2/rules/workspace-rules.md` (NEW)
- `[WORKSPACE_FOLDER]/DevSystemV2/skills/coding-conventions/SKILL.md` (NEW)
- `[WORKSPACE_FOLDER]/DevSystemV2/skills/write-documents/SKILL.md` (NEW)
- `[WORKSPACE_FOLDER]/DevSystemV2/skills/git-conventions/SKILL.md` (NEW)
- `[WORKSPACE_FOLDER]/DevSystemV2/skills/pdf-tools/SKILL.md` (NEW)
- `[WORKSPACE_FOLDER]/DevSystemV2/skills/session-management/SKILL.md` (NEW)
- `[WORKSPACE_FOLDER]/DevSystemV2/workflows/*.md` (NEW - copy and modify from V1)

**Depends on:**
- `SPEC_V1_TO_V2_USING_SKILLS.md` for migration mapping and requirements

## Table of Contents

1. [File Structure](#1-file-structure)
2. [Skill Content Previews](#2-skill-content-previews)
3. [Workflow Updates Preview](#3-workflow-updates-preview)
4. [Implementation Steps](#4-implementation-steps)
5. [Verification Checklist](#5-verification-checklist)

## 1. File Structure

```
[WORKSPACE_FOLDER]/DevSystemV2/
├── rules/                                    # ~3KB total
│   ├── devsystem-core.md                     # (~2KB) [NEW] - Definitions, placeholders, folder structure
│   ├── core-conventions.md                   # (~1KB) [NEW] - No tables, no emojis, ASCII quotes
│   └── workspace-rules.md                    # (empty) [NEW] - Placeholder
│
├── skills/
│   ├── coding-conventions/
│   │   ├── SKILL.md                          # (~1KB) [NEW] - Router for convention files
│   │   └── python-rules.md                   # (~17KB) [NEW] - Full python-rules.md content
│   ├── write-documents/
│   │   ├── SKILL.md                          # (~2KB) [NEW] - Router for templates, core rules
│   │   ├── INFO_TEMPLATE.md                  # (~2KB) [NEW] - INFO document template with examples
│   │   ├── SPEC_TEMPLATE.md                  # (~3KB) [NEW] - SPEC document template with examples
│   │   ├── IMPL_TEMPLATE.md                  # (~2KB) [NEW] - IMPL document template with examples
│   │   ├── TEST_TEMPLATE.md                  # (~2KB) [NEW] - TEST document template with examples
│   │   └── FIXES_TEMPLATE.md                   # (~1KB) [NEW] - FIX document template with examples
│   ├── git-conventions/
│   │   └── SKILL.md                          # (~2KB) [NEW] - Full git-rules.md
│   ├── pdf-tools/
│   │   └── SKILL.md                          # (~4KB) [NEW] - Full tools-rules.md
│   └── session-management/
│       └── SKILL.md                          # (~2KB) [NEW] - devsystem-rules.md §6
│
└── workflows/                                # Copy from V1, add skill invocations
    ├── prime.md                              # [MODIFY] - Update for V2
    ├── go-autonomous.md                      # [MODIFY] - No skill (language-agnostic)
    ├── go-research.md                        # [MODIFY] - Add @write-documents
    ├── session-init.md                       # [MODIFY] - Add @session-management
    ├── session-save.md                       # [MODIFY] - Add @session-management, @git-conventions
    ├── session-resume.md                     # [MODIFY] - Add @session-management
    ├── session-close.md                      # [MODIFY] - Add @session-management, @git-conventions
    ├── session-archive.md                    # [MODIFY] - Add @session-management
    ├── write-spec.md                         # [MODIFY] - Add @write-documents
    ├── write-impl-plan.md                    # [MODIFY] - Add @write-documents
    ├── write-test-plan.md                    # [MODIFY] - Add @write-documents
    ├── implement.md                          # [MODIFY] - Add @coding-conventions, @write-documents
    ├── verify.md                             # [MODIFY] - Add @write-documents, @coding-conventions
    ├── commit.md                             # [MODIFY] - Add @git-conventions
    └── setup-pdftools.md                     # [MODIFY] - Add @pdf-tools
```

## 2. Skill Content Previews

### 2.1 coding-conventions/SKILL.md (Router)

```markdown
---
name: coding-conventions
description: Apply when writing, editing, reviewing, or debugging code (Python, PowerShell, etc.)
---

# Coding Conventions

This skill contains language-specific coding convention files.

## Available Convention Files

- `python-rules.md` - Python coding conventions (formatting, imports, logging, etc.)

## Usage

Read the appropriate convention file for the language you are working with.
For Python code, read `python-rules.md` in this skill folder.
```

### 2.1.1 coding-conventions/python-rules.md

Full content copied from `DevSystemV1/rules/python-rules.md` (without frontmatter).
Contains all FT, IM, CG, NM, CM, LG rules with examples (~17KB, 551 lines).

### 2.2 write-documents/SKILL.md (Router)

```markdown
---
name: write-documents
description: Apply when creating or editing INFO, SPEC, IMPL, TEST, or FIX documents
---

# Document Writing Guide

This skill contains document templates and formatting rules.

## MUST-NOT-FORGET

- Use lists, not Markdown tables
- No emojis - ASCII only, no `---` markers between sections
- Header block: Goal, Target file, Depends on
- ID-System: `**XXXX-FR-01:**`, `**XXXX-DD-01:**`
- Be exhaustive: list ALL domain objects, actions, functions
- Spec Changes at end, reverse chronological

## Available Templates

Read the appropriate template for the document type you are creating:
- `INFO_TEMPLATE.md` - Research and analysis documents
- `SPEC_TEMPLATE.md` - Technical specifications
- `IMPL_TEMPLATE.md` - Implementation plans
- `TEST_TEMPLATE.md` - Test plans
- `FIXES_TEMPLATE.md` - Fix tracking documents

## Usage

1. Read this SKILL.md for core rules
2. Read the appropriate template for your document type
3. Follow the template structure
```

### 2.2.1 INFO_TEMPLATE.md

```markdown
# INFO: [Topic]

**Goal**: [Single sentence describing research purpose]

## Table of Contents

1. [Approaches](#1-approaches)
2. [Approach Comparison](#2-approach-comparison)
3. [Recommended Approach](#3-recommended-approach)
4. [Sources](#4-sources)
5. [Next Steps](#5-next-steps)

## 1. Approaches

### Option A: [Name]

**Description**: [Brief explanation]

**Pros**:
- [Pro 1]
- [Pro 2]

**Cons**:
- [Con 1]

<!-- EXAMPLE: Delete this block after copying -->
### Option A: Direct API Integration

**Description**: Call external API directly from main application.

**Pros**:
- Simple implementation
- No middleware needed

**Cons**:
- Tight coupling
- Hard to test
<!-- END EXAMPLE -->

## 2. Approach Comparison

- **Speed**: [A > B > C]
- **Complexity**: [A < B < C]

## 3. Recommended Approach

**[Option X]** because [rationale].

## 4. Sources

- [URL or file] - [Primary finding]

## 5. Next Steps

1. [Action item]
```

### 2.2.2 SPEC_TEMPLATE.md

```markdown
# SPEC: [Component Name]

**Goal**: [Single sentence describing what to specify]
**Target file**: `[path/to/file.py]`

**Depends on:**
- `[other-spec.md]` for [what it provides]

## MUST-NOT-FORGET

- [Critical rule 1]
- [Critical rule 2]

## Table of Contents

1. [Scenario](#1-scenario)
2. [Domain Objects](#2-domain-objects)
3. [Functional Requirements](#3-functional-requirements)
4. [Design Decisions](#4-design-decisions)
5. [Spec Changes](#5-spec-changes)

## 1. Scenario

**Problem:** [Real-world problem description]

**Solution:**
- [Approach point 1]
- [Approach point 2]

**What we don't want:**
- [Anti-pattern 1]
- [Anti-pattern 2]

## 2. Domain Objects

### [ObjectName]

A **[ObjectName]** represents [description].

**Key properties:**
- `property_1` - [description]
- `property_2` - [description]

<!-- EXAMPLE: Delete this block after copying -->
### CrawlJob

A **CrawlJob** represents a scheduled document crawl operation.

**Key properties:**
- `job_id` - Unique identifier (UUID)
- `status` - Current state: pending | running | completed | failed
- `created_at` - Timestamp of creation
<!-- END EXAMPLE -->

## 3. Functional Requirements

**[PREFIX]-FR-01:** [Requirement Title]
- [Requirement detail 1]
- [Requirement detail 2]

## 4. Design Decisions

**[PREFIX]-DD-01:** [Decision Title]
- [Decision detail]
- Rationale: [Why this decision]

## 5. Changes

**[YYYY-MM-DD HH:MM]**
- Initial specification created
```

### 2.2.3 IMPL_TEMPLATE.md

```markdown
# IMPL: [Feature Name]

**Plan ID**: [PREFIX]-IP01
**Goal**: [Single sentence describing what to implement]

**Target files**:
- `[path/to/file1.py]` (NEW)
- `[path/to/file2.py]` (MODIFY)

**Depends on:**
- `SPEC_[X].md` for [what it provides]

## Table of Contents

1. [File Structure](#1-file-structure)
2. [Implementation Steps](#2-implementation-steps)
3. [Verification Checklist](#3-verification-checklist)

## 1. File Structure

```
[folder]/
├── [file1.py]    # [Description] [NEW]
└── [file2.py]    # [Description] [MODIFY]
```

## 2. Implementation Steps

### [PREFIX]-IP01-IS-01: [Action Description]

**Action**: [Add | Modify | Remove] [description]

**Content**: [What to create or change]

## 3. Verification Checklist

- [ ] **[PREFIX]-IP01-VC-01**: [Prerequisite check]
- [ ] **[PREFIX]-IP01-VC-02**: [Implementation check]
- [ ] **[PREFIX]-IP01-VC-03**: [Validation check]
```

### 2.2.4 TEST_TEMPLATE.md

```markdown
# TEST: [Component Name]

**Goal**: [Single sentence describing test purpose]
**Target file**: `[path/to/test_file.py]`

**Depends on:**
- `SPEC_[X].md` for requirements
- `IMPL_[X].md` for implementation details

## Table of Contents

1. [Test Strategy](#1-test-strategy)
2. [Test Cases](#2-test-cases)
3. [Verification Checklist](#3-verification-checklist)

## 1. Test Strategy

**Approach**: [unit | integration | snapshot-based]

**MUST TEST:**
- [Critical function 1]
- [Critical function 2]

**DROP:**
- [Not worth testing] - Reason: [external dependency / UI-only]

## 2. Test Cases

### Category: [Name]

- **[PREFIX]-TC-01**: [Description] -> ok=true, [expected result]
- **[PREFIX]-TC-02**: [Error case] -> ok=false, [error message]

## 3. Verification Checklist

- [ ] All test cases pass
- [ ] Coverage meets requirements
```

### 2.2.5 FIXES_TEMPLATE.md

```markdown
# FIX: [Issue Description]

**Goal**: [Single sentence describing fix purpose]
**Target files**:
- `[path/to/file.py]`

## Fixes

### Fix 1: [Description]

**Location**: `[filename.py:123]`

**BEFORE:**
```python
[old_code]
```

**AFTER:**
```python
[new_code]
```

**Reason**: [Why this change is needed]

## TODO Checklist

- [ ] Fix 1: [Description]
- [ ] Verify fix works
- [ ] No regressions
```

### 2.3 git-conventions/SKILL.md

```markdown
---
name: git-conventions
description: Apply when committing code, writing commit messages, or configuring .gitignore
---

# Git Conventions

## MUST-NOT-FORGET

- Use Conventional Commits: `<type>(<scope>): <description>`
- Types: feat, fix, docs, refactor, test, chore, style, perf
- Imperative mood, <72 chars, no period
- NEVER commit secrets: .env, *.cer, *.pfx, *.pem, *.key

## Commit Message Format

[Full content from git-rules.md §Commit Message Format]

## .gitignore Rules

[Full content from git-rules.md §.gitignore Rules]

## Template

[Full content from git-rules.md §Template]
```

### 2.4 pdf-tools/SKILL.md

```markdown
---
name: pdf-tools
description: Apply when converting, processing, or analyzing PDF files
---

# PDF Tools Guide

## MUST-NOT-FORGET

- Check existing conversions before converting
- Default output: `.tools/poppler_pdf_jpgs/[PDF_FILENAME]/`
- Use 150 DPI for screen, 300 DPI for OCR
- Two-pass downsizing: Ghostscript (images) then QPDF (structure)

## PDF to JPG Conversion

[Full content from tools-rules.md §PDF to JPG]

## Poppler CLI Tools

[Full content from tools-rules.md §Poppler]

## QPDF CLI Tools

[Full content from tools-rules.md §QPDF]

## Ghostscript CLI Tools

[Full content from tools-rules.md §Ghostscript]
```

### 2.5 session-management/SKILL.md

```markdown
---
name: session-management
description: Apply when initializing, saving, resuming, or closing a work session
---

# Session Management Guide

## MUST-NOT-FORGET

- Session folder naming: `_YYYY-MM-DD_[ProblemDescription]/`
- Required files: NOTES.md, PROBLEMS.md, PROGRESS.md
- Lifecycle: Init → Work → Save → Resume → Close → Archive
- Sync session PROBLEMS.md to project on /session-close

## Session Lifecycle

1. **Init** (`/session-init`): Create session folder with tracking files
2. **Work**: Create specs, plans, implement, track progress
3. **Save** (`/session-save`): Document findings, commit changes
4. **Resume** (`/session-resume`): Re-read session documents, continue work
5. **Close** (`/session-close`): Sync findings to project files, archive

## Session Folder Naming

Format: `_YYYY-MM-DD_[ProblemDescription]/`
Example: `_2026-01-12_FixAuthenticationBug/`

## Required Session Files

- **NOTES.md**: Key information, agent instructions, working patterns
- **PROBLEMS.md**: Problems found and their status (Open/Resolved/Deferred)
- **PROGRESS.md**: To-do list, done items, tried-but-not-used approaches
```

## 3. Workflow Updates Preview

### 3.1 Updated Workflow Template

All workflows add a "Required Skills" section after frontmatter:

```markdown
---
description: [description]
auto_execution_mode: 1
---

# [Workflow Name]

## Required Skills

Invoke these skills before proceeding:
- @skill-name for [purpose]

## [Rest of workflow unchanged]
```

### 3.2 Workflow Updates Summary

**No skill required:**
- `/prime` - Entry point, loads core rules only

**@coding-conventions:**
- `/implement` - Also needs @write-documents
- `/verify` - Also needs @write-documents

**No skill required (language-agnostic):**
- `/go-autonomous` - Autonomous loop, progressive disclosure handles skill loading

**@write-documents:**
- `/go-research` - Creates INFO documents
- `/write-spec` - Creates SPEC documents
- `/write-impl-plan` - Creates IMPL documents
- `/write-test-plan` - Creates TEST documents
- `/implement` - Also needs @coding-conventions
- `/verify` - Also needs @coding-conventions

**@session-management:**
- `/session-init` - Create session
- `/session-save` - Also needs @git-conventions
- `/session-resume` - Resume session
- `/session-close` - Also needs @git-conventions
- `/session-archive` - Archive session

**@git-conventions:**
- `/commit` - Git commit workflow
- `/session-save` - Also needs @session-management
- `/session-close` - Also needs @session-management

**@pdf-tools:**
- `/setup-pdftools` - PDF tools setup

### 3.3 Example: /write-spec.md (V2)

```markdown
---
description: Create specification from requirements
auto_execution_mode: 1
---

# Write Specification Workflow

## Required Skills

Invoke these skills before proceeding:
- @write-documents for document structure and formatting rules

## Prerequisites

- User has described the problem or feature
- Clarify scope and naming before starting

## Steps

1. **Gather Requirements**
   - Ask clarifying questions if scope is unclear
   - Identify domain objects, actions, and constraints
   - Document "What we don't want" (anti-patterns, rejected approaches)

2. **Propose Alternatives** (for complex tasks)
   - Present 2-3 implementation approaches
   - Compare pros/cons
   - Let user choose before proceeding

3. **Create Specification File**
   - Create `_SPEC_[COMPONENT].md` in session folder
   - Follow @write-documents skill structure

4. **For UI Specs** (`_SPEC_[COMPONENT]_UI.md`)
   - Add User Actions section
   - Add UX Design with ASCII diagrams
   - Show ALL buttons and interactive elements

5. **Verify**
   - Run /verify workflow
   - Check exhaustiveness: all domain objects, buttons, functions listed?
```

## 4. Implementation Steps

### MIG-IP01-IS-01: Create DevSystemV2 folder structure

**Action**: Create folder structure for V2

```
mkdir DevSystemV2
mkdir DevSystemV2/rules
mkdir DevSystemV2/skills
mkdir DevSystemV2/skills/coding-conventions
mkdir DevSystemV2/skills/write-documents
mkdir DevSystemV2/skills/git-conventions
mkdir DevSystemV2/skills/pdf-tools
mkdir DevSystemV2/skills/session-management
mkdir DevSystemV2/workflows
```

### MIG-IP01-IS-02: Create core rules

**Action**: Create `devsystem-core.md` from devsystem-rules.md §1-5, §7-10

**Content sources**:
- §1 Definitions (Core Concepts, Configuration, Document Types, Tracking Documents)
- §2 Workspace Scenarios
- §3 Folder Structure
- §4 File Naming Conventions
- §5 Placeholders
- §7 Document Types (reference only)
- §8 Workflow Reference
- §9 Agent Instructions
- §10 MUST-NOT-FORGET List

### MIG-IP01-IS-03: Create core-conventions.md

**Action**: Create `core-conventions.md` from document-rules.md §1 + proper-english-rules.md

**Content sources**:
- §1.1 File Naming
- §1.2 Agent Behavior
- §1.3 Formatting (Text style, Structure)
- §1.4 Header Block
- §1.5 ID System
- §1.6 Spec Changes Section
- proper-english-rules.md (Ambiguous Grammar)

### MIG-IP01-IS-04: Create coding-conventions skill

**Action**: Create `skills/coding-conventions/` folder with 2 files

**Files**:
1. `SKILL.md` - Router with skill frontmatter, lists available convention files
2. `python-rules.md` - Full content from V1 python-rules.md (without frontmatter)

### MIG-IP01-IS-05: Create write-documents skill

**Action**: Create `skills/write-documents/` folder with 6 files

**Files**:
1. `SKILL.md` - Core rules, MUST-NOT-FORGET, template references
2. `INFO_TEMPLATE.md` - INFO document template with example content
3. `SPEC_TEMPLATE.md` - SPEC document template with example content
4. `IMPL_TEMPLATE.md` - IMPL document template with example content
5. `TEST_TEMPLATE.md` - TEST document template with example content
6. `FIXES_TEMPLATE.md` - FIX document template with example content

**Content sources**:
- SKILL.md: document-rules.md §1 (Common Rules)
- Templates: document-rules.md §2-6 converted to copy-paste templates with `<!-- EXAMPLE -->` blocks

### MIG-IP01-IS-06: Create git-conventions skill

**Action**: Create `skills/git-conventions/SKILL.md`

**Content**: Full git-rules.md with skill frontmatter and MUST-NOT-FORGET

### MIG-IP01-IS-07: Create pdf-tools skill

**Action**: Create `skills/pdf-tools/SKILL.md`

**Content**: Full tools-rules.md with skill frontmatter and MUST-NOT-FORGET

### MIG-IP01-IS-08: Create session-management skill

**Action**: Create `skills/session-management/SKILL.md`

**Content**: devsystem-rules.md §6 with skill frontmatter and MUST-NOT-FORGET

### MIG-IP01-IS-09: Copy and update workflows

**Action**: Copy all 15 workflows from V1, add "Required Skills" section

For each workflow:
1. Copy from DevSystemV1/workflows/
2. Add "Required Skills" section after frontmatter
3. Reference correct skills per mapping in §3.2

### MIG-IP01-IS-10: Update /prime workflow for V2

**Action**: Modify prime.md to reference V2 structure

Changes:
- Remove V1 references
- Update to scan DevSystemV2 folders
- Core rules auto-loaded, skills on-demand

### MIG-IP01-IS-11: Verify content preservation

**Action**: Line-by-line verification that all V1 content exists in V2

### MIG-IP01-IS-12: Delete DevSystemV1

**Action**: Remove DevSystemV1 folder after successful validation

## 5. Verification Checklist

### Prerequisites
- [ ] **MIG-IP01-VC-01**: SPEC_V1_TO_V2_USING_SKILLS.md read and understood
- [ ] **MIG-IP01-VC-02**: document-rules.md read for IMPL format

### Structure (IS-01)
- [ ] **MIG-IP01-VC-03**: DevSystemV2 folder created
- [ ] **MIG-IP01-VC-04**: rules/ subfolder created
- [ ] **MIG-IP01-VC-05**: skills/ subfolder with 5 skill folders created
- [ ] **MIG-IP01-VC-06**: workflows/ subfolder created

### Core Rules (IS-02, IS-03)
- [ ] **MIG-IP01-VC-07**: devsystem-core.md created (<2KB)
- [ ] **MIG-IP01-VC-08**: core-conventions.md created (<2KB)
- [ ] **MIG-IP01-VC-09**: workspace-rules.md placeholder created
- [ ] **MIG-IP01-VC-10**: Total core rules <5KB

### Skills (IS-04 to IS-08)
- [ ] **MIG-IP01-VC-11**: coding-conventions/SKILL.md (router) created with frontmatter
- [ ] **MIG-IP01-VC-11a**: coding-conventions/python-rules.md created
- [ ] **MIG-IP01-VC-12**: write-documents/SKILL.md created with frontmatter
- [ ] **MIG-IP01-VC-12a**: write-documents/INFO_TEMPLATE.md created
- [ ] **MIG-IP01-VC-12b**: write-documents/SPEC_TEMPLATE.md created
- [ ] **MIG-IP01-VC-12c**: write-documents/IMPL_TEMPLATE.md created
- [ ] **MIG-IP01-VC-12d**: write-documents/TEST_TEMPLATE.md created
- [ ] **MIG-IP01-VC-12e**: write-documents/FIXES_TEMPLATE.md created
- [ ] **MIG-IP01-VC-13**: git-conventions/SKILL.md created with frontmatter
- [ ] **MIG-IP01-VC-14**: pdf-tools/SKILL.md created with frontmatter
- [ ] **MIG-IP01-VC-15**: session-management/SKILL.md created with frontmatter
- [ ] **MIG-IP01-VC-16**: Each skill has MUST-NOT-FORGET section

### Workflows (IS-09, IS-10)
- [ ] **MIG-IP01-VC-17**: All 15 workflows copied to V2
- [ ] **MIG-IP01-VC-18**: Each workflow has "Required Skills" section
- [ ] **MIG-IP01-VC-19**: /prime updated for V2

### Content Preservation (IS-11)
- [ ] **MIG-IP01-VC-20**: python-rules.md content in coding-conventions skill
- [ ] **MIG-IP01-VC-21**: document-rules.md §1 in core-conventions
- [ ] **MIG-IP01-VC-22**: document-rules.md §2-6 in write-documents skill
- [ ] **MIG-IP01-VC-23**: git-rules.md content in git-conventions skill
- [ ] **MIG-IP01-VC-24**: tools-rules.md content in pdf-tools skill
- [ ] **MIG-IP01-VC-25**: devsystem-rules.md §6 in session-management skill
- [ ] **MIG-IP01-VC-26**: proper-english-rules.md in core-conventions

### Validation
- [ ] **MIG-IP01-VC-27**: Test /write-spec with @write-documents
- [ ] **MIG-IP01-VC-28**: Test /commit with @git-conventions
- [ ] **MIG-IP01-VC-29**: Test /go-autonomous with @coding-conventions
- [ ] **MIG-IP01-VC-30**: Progressive disclosure triggers correctly

### Cleanup (IS-12)
- [ ] **MIG-IP01-VC-31**: DevSystemV1 folder deleted
- [ ] **MIG-IP01-VC-32**: !NOTES.md updated to reference DevSystemV2
