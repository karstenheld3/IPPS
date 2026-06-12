# INFO: Agent Drift Prevention (ADP) - DevSystem Approach

**Doc ID**: ADP-IN01
**Goal**: Describe how the DevSystem prevents agent drift through structured, modular instruction layers
**Timeline**: Created 2026-06-12

## Summary

- Agent Drift Prevention (ADP) is the core problem the DevSystem solves: agents systematically deviate from instructions
- General approach: structure and modularize instructions to reduce agent freedom and increase agent accountability
- Three scopes: DevSystem, Session (dependent), Workflow/Skill (dependent)
- DevSystem scope: TRACTFUL (when creating artifacts) + global rules (always active)
- Session scope: SMAP (mandatory) + EDIRD and STRUT (modular additions)
- Workflow/Skill scope: GRUC and MNF (defined per workflow/skill)
- GRUC (Guides, Rules, Checks) enables quality assurance pipelines (/verify, /improve, /critique, /reconcile, /follow-instructions)
- Supporting concepts (AGEN, APAPALAN, MECT, SOCAS) provide vocabulary, writing quality, and detection heuristics

## Table of Contents

1. [The Problem: Agent Drift](#1-the-problem-agent-drift)
2. [The Approach: Structure and Modularize](#2-the-approach-structure-and-modularize)
3. [Three Scopes](#3-three-scopes)
4. [DevSystem Scope: TRACTFUL + Global Rules](#4-devsystem-scope-tractful--global-rules)
5. [Session Scope: SMAP, EDIRD, and STRUT](#5-session-scope-smap-edird-and-strut)
6. [Workflow/Skill Scope: GRUC and MNF](#6-workflowskill-scope-gruc-and-mnf)
7. [Supporting Concepts](#7-supporting-concepts)
8. [How Components Interact](#8-how-components-interact)
9. [Document History](#9-document-history)

## 1. The Problem: Agent Drift

Agents are powerful but inconsistent. Without constraints, they:
- Interpret instructions differently each time
- Skip important steps or over-engineer simple tasks
- Lose context across sessions
- Make the same mistakes repeatedly

This is **Agent Drift**: systematic deviation from instructions due to context budget constraints, reasoning shortcuts, and implicit priority tradeoffs.

### 1.1 Three Categories of Drift

- **Output Structure Drift** (~97% compliance): wrong file structure, naming, count, format. High visibility = high compliance.
- **Process Discipline Drift** (~45% compliance): skipped steps, shallow execution, wrong sequence. Low visibility = low compliance.
- **Meta-Criteria Drift** (variable, model-dependent): absent cognitive behaviors (prompt decomposition, self-correction, backtracking). Deeper reasoning models exhibit more of these naturally. Very low visibility.

### 1.2 Root Cause

Agents allocate a finite context budget. Content quality, process compliance, and meta-cognition compete for the same budget. Agents prioritize content because it produces visible output. Process steps are invisible unless audited.

## 2. The Approach: Structure and Modularize

The DevSystem's approach to ADP:

**Reduce agent freedom** by providing structured instructions that leave fewer decisions to the agent. Not "figure out what to do" but "follow this structure."

**Increase agent accountability** by modularizing quality standards into verifiable, enforceable artifacts. Not "do a good job" but "pass these specific checks."

### 2.1 Design Principles

- **Deterministic over creative**: same input should produce same behavior
- **Lookup over derivation**: pre-calculate what's knowable, don't waste tokens re-deriving
- **Explicit over implicit**: write down what "done" means, don't assume the agent knows
- **Layered over monolithic**: separate concerns by time horizon and granularity
- **Modular over coupled**: each layer has its own purpose, consumer, and lifecycle

### 2.2 Three Scopes

Different drift categories require countermeasures at different scopes. No single technique covers all categories.

## 3. Three Scopes

```
DevSystem:
  TRACTFUL     (document framework - active when creating artifacts)
  Global rules (always active)

Session (dependent):
  SMAP     (session persistence - mandatory for every session)
  EDIRD    (phase model - modular, added when multi-phase structure needed)
  STRUT    (progress tracking - modular, added when explicit state tracking needed)

Workflow/Skill (dependent):
  GRUC     (quality infrastructure - defined per skill/workflow)
  MNF      (constraint memory - defined per skill/workflow)
```

SMAP is mandatory for every session. EDIRD and STRUT are modular additions at session or step level - they can be used separately or together. GRUC and MNF can be used separately or together. What a session or workflow uses depends on its complexity and needs.

## 4. DevSystem Scope: TRACTFUL + Global Rules

**Global rules** are always active. **TRACTFUL** is active when artifacts are being created: designing and writing code, writing documents/reports/articles, designing and writing workflows.

### 4.1 TRACTFUL

**TRACTFUL** (Traceable Requirements Artifacts and Coded Templates For Unified Lifecycle) - Maps requirements and decisions from general to specific.

- **Mechanism**: typed documents (INFO, SPEC, IMPL, TEST, TASKS) with unique IDs and cross-references. Central implementation in `@skills:write-documents`.
- **Purpose**: each document type assists reaching a goal on a different abstraction level - from overall requirements to implementation details
- **Lifecycle**: persists across sessions, survives context window boundaries

**Document Chain:**
```
INFO (research) → SPEC (what) → IMPL (how) → TASKS (work items)
                      │                             │
                      └──> TEST (verify) ───────────┘
```

**What TRACTFUL constrains:** The connection between intent and implementation. Without TRACTFUL, agents lose WHY a decision was made, WHAT the constraints are, and HOW they relate to code. Each session starts from scratch.

### 4.2 Global Rules

Always-on rules (in `[AGENT_FOLDER]/rules/`) that apply regardless of session, workflow, or skill. Core conventions, ID system, agent behavior rules.

### 4.3 Drift Category Addressed

All categories across session boundaries:
- Output structure: SPEC defines expected artifacts
- Process discipline: IMPL defines expected steps
- Meta-criteria: INFO preserves reasoning and analysis

## 5. Session Scope: SMAP, EDIRD, and STRUT

**SMAP is mandatory** for every session. EDIRD and STRUT are modular additions dependent on session complexity.

### 5.1 SMAP

**SMAP** (Session Management And Persistence) - Tracks and persists overall session goals, status, and problems.

- **Mechanism**: three tracking documents (NOTES.md, PROGRESS.md, PROBLEMS.md) plus lifecycle workflows (init, save, load, finalize, archive)
- **Purpose**: persist context across conversations, enable resume, propagate learnings
- **Lifecycle**: created at session init, updated throughout, synced to project on finalize
- **Always present**: every session has SMAP. No session without tracking documents.
- **Session structure**: a session can have any combination of phases, steps, and topics

**What SMAP constrains:** Context continuity. Without SMAP, agents start each conversation fresh - no memory of progress, decisions, failures, or open problems. Knowledge dies with the conversation.

**Tracking documents:**
- **NOTES.md** - Context and reference information (goals, decisions, instructions)
- **PROGRESS.md** - Task execution status (to-do, in-progress, done)
- **PROBLEMS.md** - Topics requiring attention (open, resolved, deferred)

**Lifecycle:**
```
/session-new → /session-save → /session-load → /session-finalize → /session-archive
```

### 5.2 EDIRD

**EDIRD** (Explore, Design, Implement, Refine, Deliver) - Helps the agent think in phases and keep long-term relations between smaller steps.

- **Mechanism**: 5 standard phases with gate checklists defining transition conditions
- **Purpose**: defines HOW to reach a goal using a standardized phase model
- **Lifecycle**: active for the duration of a session or task
- **Used when**: work has distinct phases that should not be skipped or reordered

**What EDIRD constrains:** Phase sequence. Without EDIRD, agents jump to implementation before understanding the problem. Gates enforce quality before progress.

### 5.3 STRUT

**STRUT** (STRUctured Thinking) - Helps the agent plan long-running activities using tree-shaped notation.

- **Mechanism**: tree notation defining phases, steps, transitions, deliverables, and evidence-based verification
- **Purpose**: plan and track complex work with explicit state, dependencies, and completion criteria
- **Lifecycle**: created at task start, tracked during execution, verified at phase boundaries
- **Used when**: work has multiple steps where losing track is a risk

**What STRUT constrains:** Execution visibility. Without STRUT, agents lose track of where they are, skip steps, repeat work, or abandon tasks.

**Structure:**
```
[ ] P1 [EXPLORE]: Understand the problem
├── [ ] P1-S1 [ANALYZE](requirements)
├── [ ] P1-S2 [RESEARCH](existing solutions)
├── Deliverables:
│   └── [ ] P1-D1: Problem fully understood
└── Transitions:
    - P1-D1 checked → P2
```

### 5.4 SMAP, EDIRD, STRUT: Layered

- SMAP alone: context persists, but no phase enforcement or structured tracking (sufficient for simple sessions)
- SMAP + EDIRD: phase gates enforced, context persists, but no tree-notation tracking
- SMAP + STRUT: progress tracked with tree notation, but phases are custom (not the standard 5)
- SMAP + EDIRD + STRUT: full infrastructure (most common for complex work)

EDIRD and STRUT are added at session level or step level (within topic/step folders). SMAP is always present.

### 5.5 Drift Category Addressed

- SMAP prevents context loss across conversations (all drift categories across boundaries)
- EDIRD prevents skipped phases (process discipline drift)
- STRUT prevents lost progress (process discipline drift)
- Together they prevent wrong sequence, abandoned work, and repeated mistakes

## 6. Workflow/Skill Scope: GRUC and MNF

**Defined per workflow or skill.** Each workflow/skill can have its own GRUC files and MNF items tailored to its specific requirements.

### 6.1 MNF

**MNF** (Must-Not-Forget) - Single-turn constraint memory.

- **Mechanism**: in-memory checklist (5-15 items)
- **Purpose**: prevent critical oversights within a single action
- **Lifecycle**: created at task start, verified at task end, discarded after
- **Used when**: workflow has critical constraints the agent might forget mid-turn

**What MNF constrains:** The agent's immediate working memory. MNF pins critical items so they survive the context window.

**Example:**
```
MUST-NOT-FORGET:
1. Re-read original instruction BEFORE auditing
2. Each category evaluated independently
3. Score each category 0-100%
4. A "pass" requires all three at 80%+
5. Gaps are FIXED, not just reported
```

### 6.2 GRUC

**GRUC** (Guides, Rules, Checks) - Helps the agent detect and reduce 1) instruction-following drift and 2) content quality problems.

- **Mechanism**: three files per skill/workflow (GUIDE, RULES, CHECKS)
- **Purpose**: enable quality assurance pipelines (/verify, /improve, /critique, /reconcile, /follow-instructions)
- **Lifecycle**: persistent per skill/workflow, accumulates over time from FAILS.md
- **Implementation status**: partially realized. `*_RULES.md` files exist in several skills. `SKILL_GUIDE.md` and `SKILL_CHECKS.md` patterns not yet implemented per-skill. `/follow-instructions` exists but does not consume GRUC files.

### 6.3 The Three GRUC Components

**GUIDE** (`SKILL_GUIDE.md`) - Goal-oriented process guidance.
- Consumer: working agent (before execution)
- Content: how to approach the work, decision frameworks, strategies
- Lifecycle phase: before (planning)

**RULES** (`SKILL_RULES.md`) - Verifiable output quality standards.
- Consumer: `/verify`, `/improve`
- Content: structural requirements, format standards, naming conventions
- Lifecycle phase: whole lifecycle (checkable from output alone)
- Verification: read the output artifacts - no action traces needed

**CHECKS** (`SKILL_CHECKS.md`) - Enforceable process discipline checks.
- Consumer: `/follow-instructions`
- Content: actions that must have been performed, evidence of process followed
- Lifecycle phase: after only (ex-post)
- Verification: requires action evidence (conversation logs, file history)
- NOT visible to agent during execution

### 6.4 What GRUC Enables

GRUC provides the MATERIAL that quality assurance workflows consume:

- **`/verify`** - Consumes: RULES. Purpose: check output correctness
- **`/improve`** - Consumes: RULES. Purpose: fix output quality
- **`/critique`** - Consumes: GUIDE (implicit standards). Purpose: find logic flaws
- **`/reconcile`** - Consumes: RULES + critique findings. Purpose: prioritize fixes
- **`/follow-instructions`** - Consumes: CHECKS + meta-criteria. Purpose: audit process discipline

Without GRUC, these workflows must re-derive quality standards from the full skill/workflow definition each time. GRUC pre-calculates them into purpose-specific, lookup-ready files.

### 6.5 Core Insight

Compliance criteria are **constants**, not **variables**. They are knowable in advance from skill definitions and accumulated failures. Pre-calculate them once, store per workflow, look them up. Don't waste tokens re-deriving.

### 6.6 Why CHECKS Are Ex-Post Only

1. **Token economy**: agent spends budget on work, not on proving compliance
2. **No gaming**: visible checklists produce superficial compliance
3. **Separation of concerns**: execution agent does quality, realignment agent does compliance
4. **Honest signal**: unaware agent produces genuine evidence

### 6.7 MNF and GRUC: Independent

- MNF without GRUC: critical constraints in memory, but no pre-calculated quality standards
- GRUC without MNF: quality standards exist, but no pinned constraints during execution
- Both together: most common for complex skills

### 6.8 Drift Category Addressed

- MNF: process discipline + meta-criteria (reminds agent of steps and cognitive behaviors)
- GRUC.RULES: output structure drift (category 1)
- GRUC.CHECKS: process discipline drift (category 2)
- Meta-criteria drift (category 3): evaluated ad-hoc by `/follow-instructions` based on task context

## 7. Supporting Concepts

The ADP components are supported by concepts that provide vocabulary, writing quality, and detection heuristics:

### 7.1 AGEN (Agentic English)

Controlled vocabulary used across all scopes. Same verb = same action. Eliminates ambiguity in instructions.

Supports ALL components by ensuring instructions are unambiguous.

### 7.2 APAPALAN (As Precise As Possible, As Little As Necessary)

Writing quality principle. 26 enforceable rules for precision, brevity, structure, naming.

Supports GRUC.RULES by providing measurable writing quality standards.

### 7.3 MECT (Minimal Explicit Consistent Terminology)

Terminology design philosophy. One name per concept, consistent usage everywhere.

Supports GRUC.RULES by providing terminology standards. Supports AGEN by ensuring consistent vocabulary.

### 7.4 SOCAS (Signs of Confusion and Sloppiness)

15 criteria for detecting quality degradation.

Supports GRUC.RULES as detection heuristics. Used by `/verify`, `/improve`, `/critique`.

## 8. How Components Interact

### 8.1 Example: Deep Research Task

A complex deep-research session uses most components:

- **TRACTFUL** (DevSystem): _INFO_[TOPIC]-01_Summary.md defines expected output structure
- **SMAP** (Session): NOTES.md, PROGRESS.md, PROBLEMS.md track session state
- **No EDIRD**: deep research uses its own 4-phase model (Preflight, Planning, Research, Final), not the standard EDIRD 5 phases
- **STRUT** (Session): tree notation tracks progress through custom phases
- **GRUC** (Skill): DEEP_RESEARCH_RULES.md checked by /verify after each phase
- **MNF** (Skill): "Google search via Playwright MANDATORY" pinned in memory

### 8.2 Example: Simple Workflow

A simple single-step workflow (e.g., `/commit`) uses minimal components:

- **No TRACTFUL**: no documents being created
- **No SMAP, no EDIRD, no STRUT**: single-step, no session needed
- **GRUC** (Skill): commit message RULES checked by /verify
- **MNF** (Skill): "conventional commit format" pinned

### 8.3 Accountability per Scope

- **TRACTFUL**: "Is the implementation traceable to the spec? Are decisions documented?"
- **SMAP**: "Is context preserved? Can you resume? Are problems tracked?"
- **EDIRD**: "Did you pass gates before transitions?"
- **STRUT**: "Did you complete all steps? Is progress tracked?"
- **GRUC**: "Does output meet quality standards? Did you follow process?"
- **MNF**: "Did you remember this constraint during THIS turn?"

### 8.4 Freedom Reduction per Component

- **TRACTFUL**: removes freedom to disconnect implementation from intent
- **SMAP**: removes freedom to lose context between conversations
- **EDIRD**: removes freedom to skip phases
- **STRUT**: removes freedom to lose track or work out of order
- **GRUC**: removes freedom to define "good enough" subjectively
- **MNF**: removes freedom to forget critical constraints

### 8.5 Failure Modes

- **Without TRACTFUL**: each session starts from scratch, decisions re-debated, knowledge lost
- **Without SMAP**: agent has no memory between conversations, repeats work, loses findings
- **Without EDIRD**: agent jumps to implementation before understanding the problem
- **Without STRUT**: agent loses track in multi-step work, abandons steps
- **Without GRUC**: QA workflows re-derive standards each time, inconsistent detection across runs
- **Without MNF**: agent forgets constraints mid-turn, violates rules it read 2000 tokens ago

## 9. Document History

**[2026-06-12 16:30]**
- Added: SMAP (Session Management And Persistence) as mandatory Session scope component
- Changed: Session scope restructured - SMAP mandatory, EDIRD/STRUT modular additions
- Changed: Section 5 renumbered (5.1 SMAP, 5.2 EDIRD, 5.3 STRUT, 5.4 layered, 5.5 drift)
- Changed: Examples and accountability/freedom/failure sections updated with SMAP

**[2026-06-12 16:16]**
- Fixed: GRUC labeled - not yet implemented as described (only RULES partially exists)
- Fixed: Markdown table in section 6.4 converted to list format
- Fixed: Document type order aligned to canonical TRACTFUL sequence

**[2026-06-12 16:14]**
- Authoritative copy created from session working document
- Removed session-specific content (next steps, iterative history)
- Doc ID changed to ADP-IN01
