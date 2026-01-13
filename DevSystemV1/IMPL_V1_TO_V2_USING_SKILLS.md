# Implementation Plan: DevSystem V1 to V2 Migration Using Skills

**Plan ID**: MIG-IP01
**Goal**: Migrate DevSystem from rules-only to Skills-based architecture while preserving all functionality.

**Target files**:
- `[WORKSPACE_FOLDER]/DevSystemV2/rules/devsystem-core.md` (NEW)
- `[WORKSPACE_FOLDER]/DevSystemV2/rules/core-conventions.md` (NEW)
- `[WORKSPACE_FOLDER]/DevSystemV2/rules/workspace-rules.md` (NEW)
- `[WORKSPACE_FOLDER]/DevSystemV2/skills/python-coding/SKILL.md` (NEW)
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
│   ├── python-coding/
│   │   └── SKILL.md                          # (~17KB) [NEW] - Full python-rules.md
│   ├── write-documents/
│   │   └── SKILL.md                          # (~20KB) [NEW] - document-rules.md §2-6
│   ├── git-conventions/
│   │   └── SKILL.md                          # (~2KB) [NEW] - Full git-rules.md
│   ├── pdf-tools/
│   │   └── SKILL.md                          # (~4KB) [NEW] - Full tools-rules.md
│   └── session-management/
│       └── SKILL.md                          # (~2KB) [NEW] - devsystem-rules.md §6
│
└── workflows/                                # Copy from V1, add skill invocations
    ├── prime.md                              # [MODIFY] - Update for V2
    ├── go-autonomous.md                      # [MODIFY] - Add @python-coding
    ├── go-research.md                        # [MODIFY] - Add @write-documents
    ├── session-init.md                       # [MODIFY] - Add @session-management
    ├── session-save.md                       # [MODIFY] - Add @session-management, @git-conventions
    ├── session-resume.md                     # [MODIFY] - Add @session-management
    ├── session-close.md                      # [MODIFY] - Add @session-management, @git-conventions
    ├── session-archive.md                    # [MODIFY] - Add @session-management
    ├── write-spec.md                         # [MODIFY] - Add @write-documents
    ├── write-impl-plan.md                    # [MODIFY] - Add @write-documents
    ├── write-test-plan.md                    # [MODIFY] - Add @write-documents
    ├── implement.md                          # [MODIFY] - Add @python-coding, @write-documents
    ├── verify.md                             # [MODIFY] - Add @write-documents, @python-coding
    ├── commit.md                             # [MODIFY] - Add @git-conventions
    └── setup-pdftools.md                     # [MODIFY] - Add @pdf-tools
```

## 2. Skill Content Previews

### 2.1 python-coding/SKILL.md

```markdown
---
name: python-coding
description: Apply when writing, editing, reviewing, or debugging Python code
---

# Python Coding Conventions

## MUST-NOT-FORGET

- TAB = 2 spaces, MAX_LINE = 220 chars
- Single-line statements when ≤ MAX_LINE
- All imports at top, grouped: stdlib → third-party → internal
- Core imports on single line: `import asyncio, datetime, json`
- No emojis, no lambda/map/filter for control flow
- No docstrings for small functions - use single comment above
- Log action BEFORE executing, status (OK/ERROR/FAIL/WARNING) on indented line
- Surround paths/IDs with single quotes in logs
- Iteration: `[ x / n ]` at line start; Retry: `( x / n )` inline
- Use `UNKNOWN = '[UNKNOWN]'` for missing API values

## 1. Formatting Rules (FT)

[Full content from python-rules.md §Formatting]

## 2. Import Rules (IM)

[Full content from python-rules.md §Imports]

## 3. Code Generation Rules (CG)

[Full content from python-rules.md §Code Generation]

## 4. Naming Rules (NM)

[Full content from python-rules.md §Naming]

## 5. Comment Rules (CM)

[Full content from python-rules.md §Comments]

## 6. Logging Rules (LG)

[Full content from python-rules.md §Logging - most detailed section]
```

### 2.2 write-documents/SKILL.md

```markdown
---
name: write-documents
description: Apply when creating or editing INFO, SPEC, IMPL, TEST, or FIX documents
---

# Document Writing Guide

## MUST-NOT-FORGET

- Use lists, not Markdown tables
- No emojis - ASCII only, no `---` markers between sections
- Use box-drawing characters (├── └── │) for trees
- Header block: Goal, Target file, Depends on
- ID-System: `**XXXX-FR-01:**`, `**XXXX-DD-01:**`
- Be exhaustive: list ALL domain objects, actions, functions
- Include "What we don't want" in Scenario section
- Spec Changes at end, reverse chronological

## 1. INFO Documents

[Full content from document-rules.md §2]

## 2. SPEC Documents

[Full content from document-rules.md §3]

## 3. IMPL Documents

[Full content from document-rules.md §4]

## 4. TEST Documents

[Full content from document-rules.md §5]

## 5. FIX Documents

[Full content from document-rules.md §6]
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

**@python-coding:**
- `/go-autonomous` - Autonomous implementation loop
- `/implement` - Also needs @write-documents
- `/verify` - Also needs @write-documents

**@write-documents:**
- `/go-research` - Creates INFO documents
- `/write-spec` - Creates SPEC documents
- `/write-impl-plan` - Creates IMPL documents
- `/write-test-plan` - Creates TEST documents
- `/implement` - Also needs @python-coding
- `/verify` - Also needs @python-coding

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
mkdir DevSystemV2/skills/python-coding
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

### MIG-IP01-IS-04: Create python-coding skill

**Action**: Create `skills/python-coding/SKILL.md`

**Content**: Full python-rules.md with:
- Skill frontmatter (name, description)
- MUST-NOT-FORGET section (top 10 rules)
- All sections: FT, IM, CG, NM, CM, LG

### MIG-IP01-IS-05: Create write-documents skill

**Action**: Create `skills/write-documents/SKILL.md`

**Content**: document-rules.md §2-6 with:
- Skill frontmatter
- MUST-NOT-FORGET section
- All sections: INFO, SPEC, IMPL, TEST, FIX

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
- [ ] **MIG-IP01-VC-11**: python-coding/SKILL.md created with frontmatter
- [ ] **MIG-IP01-VC-12**: write-documents/SKILL.md created with frontmatter
- [ ] **MIG-IP01-VC-13**: git-conventions/SKILL.md created with frontmatter
- [ ] **MIG-IP01-VC-14**: pdf-tools/SKILL.md created with frontmatter
- [ ] **MIG-IP01-VC-15**: session-management/SKILL.md created with frontmatter
- [ ] **MIG-IP01-VC-16**: Each skill has MUST-NOT-FORGET section

### Workflows (IS-09, IS-10)
- [ ] **MIG-IP01-VC-17**: All 15 workflows copied to V2
- [ ] **MIG-IP01-VC-18**: Each workflow has "Required Skills" section
- [ ] **MIG-IP01-VC-19**: /prime updated for V2

### Content Preservation (IS-11)
- [ ] **MIG-IP01-VC-20**: python-rules.md content in python-coding skill
- [ ] **MIG-IP01-VC-21**: document-rules.md §1 in core-conventions
- [ ] **MIG-IP01-VC-22**: document-rules.md §2-6 in write-documents skill
- [ ] **MIG-IP01-VC-23**: git-rules.md content in git-conventions skill
- [ ] **MIG-IP01-VC-24**: tools-rules.md content in pdf-tools skill
- [ ] **MIG-IP01-VC-25**: devsystem-rules.md §6 in session-management skill
- [ ] **MIG-IP01-VC-26**: proper-english-rules.md in core-conventions

### Validation
- [ ] **MIG-IP01-VC-27**: Test /write-spec with @write-documents
- [ ] **MIG-IP01-VC-28**: Test /commit with @git-conventions
- [ ] **MIG-IP01-VC-29**: Test /go-autonomous with @python-coding
- [ ] **MIG-IP01-VC-30**: Progressive disclosure triggers correctly

### Cleanup (IS-12)
- [ ] **MIG-IP01-VC-31**: DevSystemV1 folder deleted
- [ ] **MIG-IP01-VC-32**: !NOTES.md updated to reference DevSystemV2
