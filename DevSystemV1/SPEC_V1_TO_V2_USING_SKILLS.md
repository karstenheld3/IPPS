# Specification: DevSystem V1 to V2 Migration Using Skills

**Goal**: Migrate DevSystem from rules-only architecture to a Skills-based architecture for context-aware loading while preserving all functionality.

**Target files**:
- `DevSystemV2/skills/*/SKILL.md` (NEW)
- `DevSystemV2/rules/*.md` (MODIFY - reduce to core only)
- `DevSystemV2/workflows/*.md` (MODIFY - add skill invocations)

**Depends on:**
- `DevSystemV1/rules/*.md` - Source content to migrate
- `DevSystemV1/workflows/*.md` - Workflows to update
- `INFO_HOW_WINDSURF_WORKS.md` - Skills specification reference

## MUST-NOT-FORGET

- Nothing from V1 rules must be lost - all content migrates somewhere
- Skills use progressive disclosure - good descriptions are critical
- Workflows must explicitly invoke skills via `@skill-name`
- Core rules remain always-on for universal conventions
- Each skill must be self-contained with MUST-NOT-FORGET section

## Table of Contents

1. [Scenario](#1-scenario)
2. [Current State Analysis](#2-current-state-analysis)
3. [Target Architecture](#3-target-architecture)
4. [Domain Objects](#4-domain-objects)
5. [Migration Mapping](#5-migration-mapping)
6. [Functional Requirements](#6-functional-requirements)
7. [Design Decisions](#7-design-decisions)
8. [Workflow Updates](#8-workflow-updates)
9. [Verification Checklist](#9-verification-checklist)
10. [Spec Changes](#10-spec-changes)

## 1. Scenario

**Problem:**
DevSystem V1 uses 6 always-on rule files totaling ~62KB. All rules are loaded into context regardless of task, consuming tokens and potentially overwhelming the agent with irrelevant information.

**Solution:**
- Migrate context-specific rules to Skills (progressive disclosure)
- Keep only universal conventions as always-on rules (~3KB)
- Update workflows to explicitly invoke required skills
- Preserve all content - nothing is deleted, only reorganized

**What we don't want:**
- Lost rules or conventions that worked in V1
- Skills that are too granular (loading overhead)
- Skills that are too broad (defeats purpose)
- Workflows that forget to invoke necessary skills
- Breaking cross-agent compatibility

## 2. Current State Analysis

### 2.1 V1 Rules Inventory

**Total: 7 files, ~62KB, all trigger: always_on** (workspace-rules.md is empty placeholder)

- **devsystem-rules.md** (14.6KB, 375 lines)
  - Core definitions and placeholders
  - Workspace scenarios (SINGLE-PROJECT, MONOREPO, etc.)
  - Folder structure conventions
  - File naming conventions (!, _, .)
  - Session management lifecycle
  - Document type definitions
  - Workflow reference
  - Agent instructions
  - MUST-NOT-FORGET guidance

- **document-rules.md** (23.3KB, 799 lines)
  - Common formatting rules
  - Header block format
  - ID system (FR, DD, IG, EC, IS, VC, TC)
  - INFO document structure and examples
  - SPEC document structure and examples
  - IMPL document structure and examples
  - TEST document structure
  - FIX document structure

- **python-rules.md** (17.5KB, 551 lines)
  - Formatting rules (FT-01 to FT-05)
  - Import rules (IM-01 to IM-05)
  - Code generation rules (CG-01 to CG-09)
  - Naming rules (NM-01 to NM-03)
  - Comment rules (CM-01 to CM-05)
  - Logging rules (LG-01 to LG-12)

- **git-rules.md** (1.9KB, 88 lines)
  - Conventional commits format
  - Commit types and guidelines
  - .gitignore rules and template

- **tools-rules.md** (4.4KB, 138 lines)
  - PDF to JPG conversion script usage
  - Poppler CLI tools
  - QPDF CLI tools
  - Ghostscript CLI tools
  - PDF downsizing workflow

- **proper-english-rules.md** (1KB, 32 lines)
  - Ambiguous grammar rule

- **workspace-rules.md** (32B, empty)
  - Placeholder for workspace-specific rules

### 2.2 V1 Workflows Inventory

**Total: 15 files, ~18KB**

- `/prime` (1.3KB) - Load context. Skills: None (entry point)
- `/go-autonomous` (0.8KB) - Autonomous loop. Skills: python-coding
- `/go-research` (1.1KB) - Research mode. Skills: write-documents
- `/session-init` (1.3KB) - Create session. Skills: session-management
- `/session-save` (0.6KB) - Save session. Skills: session-management, git-conventions
- `/session-resume` (0.3KB) - Resume session. Skills: session-management
- `/session-close` (1.2KB) - Close session. Skills: session-management, git-conventions
- `/session-archive` (0.8KB) - Archive session. Skills: session-management
- `/write-spec` (1.3KB) - Write specification. Skills: write-documents
- `/write-impl-plan` (1.3KB) - Write impl plan. Skills: write-documents
- `/write-test-plan` (1.3KB) - Write test plan. Skills: write-documents
- `/implement` (1.2KB) - Implementation. Skills: python-coding, write-documents
- `/verify` (2KB) - Verification. Skills: write-documents, python-coding
- `/commit` (0.5KB) - Git commit. Skills: git-conventions
- `/setup-pdftools` (5.4KB) - Setup PDF tools. Skills: pdf-tools

## 3. Target Architecture

### 3.1 V2 Folder Structure

```
DevSystemV2/
├── rules/                        # Always-on core rules (~3KB total)
│   ├── core-conventions.md       # Universal formatting, no tables/emojis
│   └── devsystem-core.md         # Definitions, placeholders, folder structure
│
├── skills/                       # Context-triggered skills
│   ├── python-coding/
│   │   └── SKILL.md              # Python coding conventions
│   ├── write-documents/
│   │   └── SKILL.md              # INFO/SPEC/IMPL/TEST/FIX writing
│   ├── git-conventions/
│   │   └── SKILL.md              # Commits, .gitignore
│   ├── pdf-tools/
│   │   └── SKILL.md              # PDF processing tools
│   └── session-management/
│       └── SKILL.md              # Session lifecycle
│
└── workflows/                    # Unchanged structure, updated content
    ├── prime.md
    ├── go-autonomous.md
    ├── go-research.md
    ├── session-init.md
    ├── session-save.md
    ├── session-resume.md
    ├── session-close.md
    ├── session-archive.md
    ├── write-spec.md
    ├── write-impl-plan.md
    ├── write-test-plan.md
    ├── implement.md
    ├── verify.md
    ├── commit.md
    └── setup-pdftools.md
```

### 3.2 Loading Comparison

**V1 (Current):**
```
Agent starts → Load ALL rules (~62KB) → Execute task
```

**V2 (Target):**
```
Agent starts → Load core rules (~3KB) → User invokes workflow → Workflow invokes skill → Load skill (~5-15KB) → Execute task
```

## 4. Domain Objects

### 4.1 Skill

A **Skill** is a folder containing `SKILL.md` and optional supporting files.

**Location:** `[AGENT_FOLDER]/skills/[skill-name]/`

**Key properties:**
- `name` - Skill identifier (kebab-case)
- `description` - Progressive disclosure trigger text
- Content sections with MUST-NOT-FORGET summary

**Invocation:**
- Explicit: `@skill-name` in chat or workflow
- Automatic: Progressive disclosure matches description to task

**Schema (SKILL.md frontmatter):**
```yaml
---
name: skill-name
description: Apply when [trigger conditions]
---
```

### 4.2 Core Rule

A **Core Rule** is an always-on rule file with minimal, universal content.

**Location:** `[AGENT_FOLDER]/rules/`

**Key properties:**
- `trigger: always_on` in frontmatter
- Content applies to ALL tasks regardless of context
- Must be kept small (<2KB per file)

### 4.3 Workflow

A **Workflow** is a step-by-step procedure file.

**Location:** `[AGENT_FOLDER]/workflows/`

**Key properties:**
- `description` for /command discovery
- Steps that may invoke skills via `@skill-name`
- Unchanged structure from V1

## 5. Migration Mapping

### 5.1 Content Distribution

- `devsystem-rules.md` §1-5 (170 lines) → `rules/devsystem-core.md` - Universal definitions
- `devsystem-rules.md` §6 (50 lines) → `skills/session-management/` - Session-specific
- `devsystem-rules.md` §7-10 (100 lines) → `rules/devsystem-core.md` - Reference info
- `document-rules.md` §1 (130 lines) → `rules/core-conventions.md` - Universal formatting
- `document-rules.md` §2-6 (670 lines) → `skills/write-documents/` - Document-specific
- `python-rules.md` (551 lines) → `skills/python-coding/` - Python-specific
- `git-rules.md` (88 lines) → `skills/git-conventions/` - Git-specific
- `tools-rules.md` (138 lines) → `skills/pdf-tools/` - Tool-specific
- `proper-english-rules.md` (32 lines) → `rules/core-conventions.md` - Universal writing
- `workspace-rules.md` (empty) → `rules/workspace-rules.md` - Remains as placeholder

### 5.2 Skill Content Mapping

**Skill: python-coding**
- Source: `python-rules.md` (551 lines)
- Description: "Apply when writing, editing, reviewing, or debugging Python code"
- MUST-NOT-FORGET: Top 10 most-violated rules
- Full content: All FT, IM, CG, NM, CM, LG rules with examples

**Skill: write-documents**
- Source: `document-rules.md` §2-6 (670 lines)
- Description: "Apply when creating or editing INFO, SPEC, IMPL, TEST, or FIX documents"
- MUST-NOT-FORGET: ID system, header block, no tables
- Full content: INFO, SPEC, IMPL, TEST, FIX structures and examples

**Skill: git-conventions**
- Source: `git-rules.md` (88 lines)
- Description: "Apply when committing code, writing commit messages, or configuring .gitignore"
- MUST-NOT-FORGET: Conventional commits format, never commit secrets
- Full content: Types, guidelines, .gitignore template

**Skill: pdf-tools**
- Source: `tools-rules.md` (138 lines)
- Description: "Apply when converting, processing, or analyzing PDF files"
- MUST-NOT-FORGET: Script usage, check existing conversions
- Full content: All tool CLI examples

**Skill: session-management**
- Source: `devsystem-rules.md` §6 (50 lines)
- Description: "Apply when initializing, saving, resuming, or closing a work session"
- MUST-NOT-FORGET: Lifecycle steps, folder naming
- Full content: Session lifecycle, required files

## 6. Functional Requirements

**MIG-FR-01:** Complete Content Preservation
- Every line from V1 rules must exist in V2 (rules or skills)
- No functionality may be lost in migration

**MIG-FR-02:** Skill Progressive Disclosure
- Each skill must have a `description` that triggers on relevant tasks
- Descriptions must be specific enough to avoid false positives

**MIG-FR-03:** Workflow Skill Invocation
- Each workflow must explicitly invoke required skills
- Format: "Invoke @skill-name for [purpose]"

**MIG-FR-04:** Core Rules Minimization
- Core rules must total <5KB combined
- Each file <2KB
- Only universal, task-agnostic content

**MIG-FR-05:** MUST-NOT-FORGET Sections
- Each skill must have a MUST-NOT-FORGET section
- Maximum 15 lines of critical rules

**MIG-FR-06:** Self-Contained Skills
- Each skill must be usable without reading other files
- Include all necessary context within the skill

**MIG-FR-07:** Backward Compatibility
- V1 workflows must work with V2 structure
- No breaking changes to workflow invocation

**MIG-FR-08:** Workflow-Guaranteed Skill Loading
- Progressive disclosure may miss edge cases
- Workflows explicitly invoke required skills to ensure loading
- No V1 fallback - V2 is complete and self-contained

## 7. Design Decisions

**MIG-DD-01:** Skill Granularity
- Create 5 skills matching major rule files
- Rationale: Matches natural task boundaries, avoids fragmentation

**MIG-DD-02:** Core Rules Split
- Two core rule files: `devsystem-core.md` (definitions) and `core-conventions.md` (formatting)
- Rationale: Separation of concerns

**MIG-DD-03:** Skill Invocation Syntax
- Use `@skill-name` in workflows
- Rationale: Matches Windsurf native syntax, enables progressive disclosure

**MIG-DD-04:** No Nested Skills
- Skills do not invoke other skills
- Rationale: Simplicity, predictable loading

**MIG-DD-05:** Workflow Skill Section
- Add "Required Skills" section at top of each workflow
- Rationale: Clear dependencies, self-documenting

**MIG-DD-06:** Complete V1 Replacement
- Delete DevSystemV1 folder after migration
- V2 becomes the single source of truth
- Rationale: No duplication, clean structure

**MIG-DD-07:** Cross-Agent Compatibility
- Skills folder structure follows Agent Skills open format (agentskills.io)
- SKILL.md format portable to Claude Code, Codex, etc.
- Rationale: Future-proofing, multi-agent support

## 8. Workflow Updates

### 8.1 Updated Workflow Format

```markdown
---
description: [description]
auto_execution_mode: 1
---

# [Workflow Name]

## Required Skills

Invoke these skills before proceeding:
- @skill-name-1 for [purpose]
- @skill-name-2 for [purpose]

## Prerequisites
...

## Steps
...
```

### 8.2 Workflow-to-Skill Mapping

- `/prime` → None (loads core rules only)
- `/go-autonomous` → @python-coding
- `/go-research` → @write-documents
- `/session-init` → @session-management
- `/session-save` → @session-management, @git-conventions
- `/session-resume` → @session-management
- `/session-close` → @session-management, @git-conventions
- `/session-archive` → @session-management
- `/write-spec` → @write-documents
- `/write-impl-plan` → @write-documents
- `/write-test-plan` → @write-documents
- `/implement` → @python-coding, @write-documents
- `/verify` → @write-documents, @python-coding
- `/commit` → @git-conventions
- `/setup-pdftools` → @pdf-tools

### 8.3 Example: Updated /write-spec

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
   - Follow @write-documents skill structure:
     - Header block (Goal, Target file, Dependencies)
     - Table of Contents
     - Scenario (Problem, Solution, What we don't want)
     - Domain Objects
     - Functional Requirements (numbered: XXXX-FR-01)
     - Design Decisions (numbered: XXXX-DD-01)
     - Key Mechanisms

4. **For UI Specs** (`_SPEC_[COMPONENT]_UI.md`)
   - Add User Actions section
   - Add UX Design with ASCII diagrams
   - Show ALL buttons and interactive elements

5. **Verify**
   - Run /verify workflow
   - Check exhaustiveness: all domain objects, buttons, functions listed?
```

## 9. Verification Checklist

### Prerequisites
- [ ] **MIG-VC-01**: V1 rules completely analyzed and inventoried
- [ ] **MIG-VC-02**: All V1 content accounted for in mapping

### Structure
- [ ] **MIG-VC-03**: DevSystemV2 folder created
- [ ] **MIG-VC-04**: All 5 skill folders created with SKILL.md
- [ ] **MIG-VC-05**: Core rules created (<5KB total)
- [ ] **MIG-VC-06**: All workflows updated with skill invocations

### Content Preservation
- [ ] **MIG-VC-07**: python-rules.md fully migrated to python-coding skill
- [ ] **MIG-VC-08**: document-rules.md fully migrated (core + write-documents)
- [ ] **MIG-VC-09**: git-rules.md fully migrated to git-conventions skill
- [ ] **MIG-VC-10**: tools-rules.md fully migrated to pdf-tools skill
- [ ] **MIG-VC-11**: devsystem-rules.md fully migrated (core + session-management)
- [ ] **MIG-VC-12**: proper-english-rules.md migrated to core-conventions

### Functionality
- [ ] **MIG-VC-13**: Each skill has MUST-NOT-FORGET section
- [ ] **MIG-VC-14**: Each skill has progressive disclosure description
- [ ] **MIG-VC-15**: Each workflow invokes correct skills
- [ ] **MIG-VC-16**: /prime workflow updated for V2

### Validation
- [ ] **MIG-VC-17**: Test /write-spec with @write-documents
- [ ] **MIG-VC-18**: Test /commit with @git-conventions
- [ ] **MIG-VC-19**: Test /go-autonomous with @python-coding
- [ ] **MIG-VC-20**: Compare V1 vs V2 token usage
- [ ] **MIG-VC-21**: Verify progressive disclosure triggers on skill descriptions
- [ ] **MIG-VC-22**: Delete DevSystemV1 folder after successful validation

## 10. Spec Changes

**[2026-01-13 16:49]**
- Fixed: File count "6 files" → "7 files" (includes empty workspace-rules.md)
- Added: Progressive disclosure descriptions for all 5 skills
- Added: MIG-VC-21 and MIG-VC-22 to verification checklist

**[2026-01-13 16:40]**
- Changed: MIG-FR-08 from V1 fallback to workflow-guaranteed loading
- Changed: MIG-DD-06 from keep V1 as reference to complete V1 replacement

**[2026-01-13 16:35]**
- Fixed: Converted tables to lists (document-rules compliance)
- Fixed: ID format `**MIG-FR-01:**` with colon outside bold
- Fixed: DD format with list items instead of inline
- Added: MIG-FR-08 for fallback behavior
- Added: MIG-DD-07 for cross-agent compatibility
- Added: workspace-rules.md to migration mapping
- Fixed: Core rules size target consistency (<5KB combined, <2KB per file)

**[2026-01-13 16:30]**
- Initial specification created
