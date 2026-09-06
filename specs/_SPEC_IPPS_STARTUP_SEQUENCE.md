# SPEC: IPPS Startup Sequence

**Doc ID**: IPPSSTART-SP01
**Feature**: ipps-startup-sequence
**Goal**: Specify the agent startup sequence, the orthogonality between IPPS and AGENTS.md, and the lazy activation model that governs all IPPS behavior
**Timeline**: Created 2026-09-04, Updated 0 times (2026-09-04 - 2026-09-04)
**Target file(s)**:
- `DevSystemV4.3/workflows/prime.md` (startup sequence formalization)
- `DevSystemV4.3/rules/devsystem-core.md` (startup sequence section, operation modes)
- `DevSystemV4.3/skills/workspace-management/WORKSPACE-GUIDES.md` (startup guidance)

**Depends on:**
- `Docs/Specs/_SPEC_SKILL_WORKFLOW-MANAGEMENT.md [WSKMGMT-SP01]` for 4 workspace dimensions, workspace constants, sync relationship (including Dimension 4: FR-32..39, DD-11..15)
- `DevSystemV4.3/skills/session-management/SKILL.md` for session lifecycle and folder structure
- `DevSystemV4.3/rules/devsystem-core.md` for operation modes, workspace scenarios, document types

**Does not depend on:**
- Any agent-specific documentation (AGENTS.md is explicitly out of scope)

## MUST-NOT-FORGET

- IPPS is agent-agnostic: must work with Cascade, Claude Code, Cursor, or any agent that can read .md files and run workflows
- AGENTS.md and IPPS are completely orthogonal: IPPS must never reference, modify, or depend on AGENTS.md
- Lazy activation: IPPS does nothing until the user explicitly calls a workflow. No background sync, no auto-verify, no proactive suggestions
- The only shared surface between agent and IPPS is the `rules/` folder — both read it, neither writes it during startup
- `/prime` is the IPPS entry point, not the agent entry point. Agent starts independently
- `auto_execution_mode: 3` in prime.md frontmatter means agents MAY auto-run prime on startup — this is agent behavior, not IPPS behavior
- Privacy gate: no real identifiers, agent names, or project-specific data in spec or skill files

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
11. [User Actions](#11-user-actions)
12. [UX Design](#12-ux-design)
13. [Logging Requirements](#13-logging-requirements)
14. [Technical Constraints](#14-technical-constraints)
15. [Document History](#15-document-history)

## 1. Scenario

**Problem:** The DevSystem prompt system (IPPS) has no formal specification of how agents start up, what happens before the first workflow call, and where the boundary between agent behavior and IPPS behavior lies. This causes:
- Confusion about whether `/prime` runs automatically or must be called
- Unclear responsibility for rules loading (agent auto-load vs `/prime` read)
- No explicit contract for what agents must support to use IPPS
- Risk of coupling IPPS to agent-specific behavior (AGENTS.md formats, auto-execution modes)

**Solution:**
- Define a 3-layer startup model: Agent layer, IPPS startup layer (`/prime`), IPPS activity layer (workflows)
- Establish the orthogonality principle: IPPS and AGENTS.md are completely independent
- Define the lazy activation model: IPPS does nothing without explicit workflow invocation
- Document the shared surface (`rules/` folder) and the agent-agnostic contract
- Formalize `/prime` as the IPPS entry point with 4 detection steps

**What we don't want:**
- IPPS referencing or depending on AGENTS.md — agents have different formats and loading behavior
- Auto-execution of workflows without user call — IPPS is user-driven, not proactive
- Coupling to a specific agent — IPPS must work with any agent that can read .md and run commands
- Rules folder modification during startup — both agent and IPPS read it read-only
- IPPS to define how agents configure themselves — that is agent behavior, not IPPS behavior

## 2. Context

The DevSystem prompt system (IPPS) is a collection of rules, workflows, skills, and templates stored in `[DEVSYSTEM_FOLDER]` and mirrored to `[AGENT_FOLDER]` (e.g., `.devin/`). It provides structured development workflows for agentic AI coding assistants.

Different agents interact with IPPS differently (descriptive context only — IPPS does not depend on any specific agent):
- **Cascade** (Windsurf): Auto-loads `rules/` folder content as system prompt. Supports `auto_execution_mode` in workflow frontmatter. May auto-run `/prime` on session start.
- **Claude Code**: Reads `AGENTS.md` for configuration. Loads `.claude/commands/` as slash commands. Does not auto-load rules.
- **Cursor**: Reads `.cursorrules` or `.cursor/rules/` for configuration. Different loading mechanism.

Despite these differences, all agents use the same IPPS workflows, skills, and rules. The key insight is that IPPS content is agent-agnostic — it is the agent that adapts to IPPS, not the other way around.

### 3-Layer Startup Model

```
Layer 1: Agent Startup (agent-specific, NOT IPPS)
├─> Agent reads AGENTS.md (or equivalent: .cursorrules, etc.)
├─> Agent configures itself (model, tools, permissions)
├─> Cascade: auto-loads rules/ folder content as system prompt
├─> Agent is ready for user input
└─> IPPS has no role here

Layer 2: IPPS Startup (/prime — the IPPS entry point)
├─> /prime called (by user or auto-executed by agent)
├─> Step 1: Read rules/ folder (.md files)
├─> Step 2: Read priority docs (! prefix .md files)
├─> Step 3: Read standard docs (.md files, excluding _ and ! prefix)
├─> Step 4: Detect workspace scenario (4 dimensions)
└─> Report: file counts + mode string

Layer 3: IPPS Activity (workflows — user-driven)
├─> Agent waits for user input
├─> User calls workflow (e.g., /verify, /sync, /commit)
├─> Workflow loads required skills on demand
├─> Workflow executes
├─> Agent waits for next user input
└─> No background or proactive behavior
```

### Orthogonality Principle

```
AGENTS.md                    IPPS
├─> Agent configuration      ├─> Rules, workflows, skills, templates
├─> Agent-specific format    ├─> Agent-agnostic .md files
├─> Agent reads it           ├─> Agent reads it (via /prime or auto-load)
├─> IPPS never touches it    ├─> AGENTS.md never references it
└─> Agent owns this layer    └─> IPPS owns workflow/skill layer

Shared surface: rules/ folder
├─> Agent (Cascade): auto-loads as system prompt content
├─> /prime: reads for context reporting
├─> Both consumers read-only
└─> Neither consumer modifies during startup
```

## 3. Domain Objects

### AgentConfiguration

An **AgentConfiguration** is the agent's own startup configuration, stored in AGENTS.md or equivalent agent-specific file. Not part of IPPS.

**Storage:** `AGENTS.md` (or `.cursorrules`, `.cursor/rules/`, agent-specific)
**Key properties:**
- `model` - AI model to use
- `tools` - enabled tools and permissions
- `instructions` - agent-specific behavioral instructions
- `auto_execution_mode` - whether agent auto-runs workflows with certain frontmatter

**IPPS relationship:** None. IPPS does not read, write, or reference AgentConfiguration.

### IPPSContext

An **IPPSContext** is the workspace context assembled by `/prime`. Contains file inventory and workspace scenario detection.

**Storage:** In-memory (reported to user, not persisted)
**Key properties:**
- `rules_read` - count of .md files read from rules/ folder
- `priority_docs` - count of ! prefix .md files read
- `standard_docs` - count of standard .md files read
- `code_files` - count and types of code files detected
- `workspace_mode` - 4 dimensions: Project Structure, Version Strategy, Work Mode, Sync Relationship

### WorkspaceDimensions

Four orthogonal dimensions detected during `/prime` Step 4. Defined in `_SPEC_SKILL_WORKFLOW-MANAGEMENT.md [WSKMGMT-SP01]`.

1. **Project Structure**: SINGLE-PROJECT, MONOREPO, WORKSPACE
2. **Version Strategy**: SINGLE-VERSION, MULTI-VERSION
3. **Work Mode**: SESSION-MODE, PROJECT-MODE
4. **Sync Relationship**: SYNCED, SELF-CONTAINED `[ASSUMED]` (defined in `_SPEC_SKILL_WORKFLOW-MANAGEMENT.md [WSKMGMT-SP01]` FR-32..39, not yet implemented)

```
Workspace Dimension Overview
┌────────────────────────────────────────────────────────────────────────┐
│                    /prime Step 4: Detect 4 Dimensions                  │
├──────────────────┬──────────────────┬──────────────────┬───────────────┤
│  Dim 1           │  Dim 2           │  Dim 3           │  Dim 4        │
│  Project         │  Version         │  Work            │  Sync         │
│  Structure       │  Strategy        │  Mode            │  Relationship │
├──────────────────┼──────────────────┼──────────────────┼───────────────┤
│ SINGLE-PROJECT   │ SINGLE-VERSION   │ SESSION-MODE     │ SYNCED        │
│ MONOREPO         │ MULTI-VERSION    │ PROJECT-MODE     │ SELF-         │
│ WORKSPACE        │                  │                  │  CONTAINED    │
├──────────────────┼──────────────────┼──────────────────┼───────────────┤
│ Detection:       │ Detection:       │ Detection:       │ Detection:    │
│ main.code-       │ Multiple version │ Active session   │ [LINKED_REPOS]│
│ workspace file?  │ folders or       │ folder exists?   │ or            │
│ → WORKSPACE      │ detectors?       │ → SESSION-MODE   │ [*_SOURCE_    │
│ Multi-project    │ → MULTI-VERSION  │ Otherwise        │  FOLDER] or   │
│ subfolders?      │ Otherwise        │ → PROJECT-MODE   │ [PRODUCT_VERSION]   │
│ → MONOREPO       │ → SINGLE-VERSION │                  │ in NOTES.md?  │
│ Otherwise        │                  │                  │ → SYNCED      │
│ → SINGLE-PROJECT │                  │                  │ Otherwise     │
│                  │                  │                  │ → SELF-       │
│                  │                  │                  │  CONTAINED    │
└──────────────────┴──────────────────┴──────────────────┴───────────────┘

Example combinations:
  SINGLE-PROJECT + SINGLE-VERSION + SESSION-MODE + SYNCED
  WORKSPACE + SINGLE-VERSION + PROJECT-MODE + SELF-CONTAINED
  MONOREPO + MULTI-VERSION + SESSION-MODE + SYNCED
```

### WorkspaceConstants

Default variables defined in DevRepo NOTES.md. Defined in `_SPEC_SKILL_WORKFLOW-MANAGEMENT.md [WSKMGMT-SP01]`, section FR-06.

**Always required (5):**
- `[WORKSPACE_FOLDER]`, `[PRODUCT_REPO_FOLDER]`
- `[KNOWLEDGE_FOLDER]`, `[RULES_FOLDER]`, `[PRODUCT_DOCS_FOLDER]`

**Required for SYNCED only (3):**
- `[COMPANY_REPO_FOLDER]`, `[KNOWLEDGE_SOURCE_FOLDER]`, `[RULES_SOURCE_FOLDER]`

### SessionLifecycle

Session management follows the session-management skill (`@skills:session-management`). Sessions are time-limited work contexts with tracking files.

**Lifecycle:** Init → Work → Save → Resume → Finalize → Archive
**Key files:** NOTES.md, PROBLEMS.md, PROGRESS.md (per session)
**Folder pattern:** `_YYYY-MM-DD_[SessionTopicCamelCase]/`

Session creation is an IPPS activity (Layer 3), triggered by user calling `/session-new`. It is not part of startup.

## 4. Functional Requirements

### Startup Sequence

**IPPSSTART-FR-01: Define 3-layer startup model in devsystem-core.md**
- Add "Startup Sequence" section to devsystem-core.md
- Document 3 layers: Agent Startup, IPPS Startup (/prime), IPPS Activity (workflows)
- Document orthogonality principle: IPPS and AGENTS.md are independent
- Document lazy activation: no IPPS action without explicit workflow call
- Document shared surface: rules/ folder is read-only for both agent and IPPS

**IPPSSTART-FR-02: Formalize /prime as IPPS entry point**
- /prime is the first IPPS workflow in the startup sequence
- /prime reads workspace files and detects workspace scenario
- /prime does not modify any files — read-only operation
- /prime reports context to user and agent
- After /prime, agent waits for user input (lazy activation)

**IPPSSTART-FR-03: Document agent-agnostic contract**
- Agent must support: reading .md files, running shell commands, executing workflows
- Agent must not: modify rules/ folder during startup, auto-execute workflows without user call (except /prime if auto_execution_mode allows)
- Agent may: auto-load rules/ folder content as system prompt (Cascade does this)
- Agent may: auto-run /prime on startup (if auto_execution_mode in frontmatter allows)
- IPPS must not: reference AGENTS.md, depend on agent-specific behavior, or assume a specific agent

### Prime Detection

**IPPSSTART-FR-04: /prime Step 4 detects 4 dimensions**
- Dimension 1: Project Structure (SINGLE-PROJECT, MONOREPO, WORKSPACE)
- Dimension 2: Version Strategy (SINGLE-VERSION, MULTI-VERSION)
- Dimension 3: Work Mode (SESSION-MODE, PROJECT-MODE)
- Dimension 4: Sync Relationship (SYNCED, SELF-CONTAINED) — per SYNCREL-SP01
- Detection is read-only: /prime reads NOTES.md and workspace structure, modifies nothing
- Report all 4 dimensions in final output line

**IPPSSTART-FR-05: /prime reads workspace constants from NOTES.md**
- Read DevRepo NOTES.md (or !NOTES.md) for workspace constants
- Constants inform dimension detection (presence of sync markers → SYNCED)
- Missing constants are reported but do not cause /prime to fail
- /prime does not create or modify constants — that is /verify workspace's job

### Lazy Activation

**IPPSSTART-FR-06: No IPPS action without explicit workflow call**
- After /prime completes, agent enters idle state
- No workflow runs without user explicitly calling it
- No background sync, no auto-verify, no proactive suggestions
- Exception: /prime may be auto-executed by agent if frontmatter allows (auto_execution_mode: 3)
- Exception: /go workflow runs an autonomous loop, but only after user explicitly calls /go

**IPPSSTART-FR-07: Workflows load skills on demand**
- Each workflow declares required skills in its frontmatter
- Skills are loaded when the workflow is called, not at startup
- /prime does not load skills — it only reads rules and docs
- This keeps startup fast and context window lean

### Session Integration

**IPPSSTART-FR-08: Session creation is post-startup activity**
- Sessions are created by user calling /session-new (Layer 3 activity)
- /prime does not create sessions
- /prime may detect existing session (SESSION-MODE) but does not initialize one
- Session lifecycle (init → work → save → resume → finalize → archive) is managed by session-management skill, not by startup sequence

## 5. Non-Functional Requirements

**IPPSSTART-NFR-01: Agent agnosticism**
- IPPS must work with any agent that can: read .md files, run shell commands, execute workflows
- No IPPS file may reference agent-specific features (Cascade auto-load, Claude Code commands, Cursor rules)
- Exception: workflow frontmatter (auto_execution_mode) is a hint to agents, not a requirement
- Verification method: grep for agent-specific references in all IPPS files

**IPPSSTART-NFR-02: Startup performance**
- /prime must complete within 5 seconds for workspaces with up to 100 .md files
- /prime must not read files in _ prefix folders (sessions, archives, temp)
- /prime must not load skills or workflows — only rules and docs
- Verification method: timed execution of /prime on a workspace with 100+ .md files

**IPPSSTART-NFR-03: Orthogonality enforcement**
- No IPPS file may import, reference, or depend on AGENTS.md
- No IPPS workflow may modify AGENTS.md
- AGENTS.md may reference IPPS workflows (agent's choice), but IPPS must not require this
- Verification method: grep for "AGENTS.md" in all IPPS files in DevSystemV4.3/

## 6. Design Decisions

**IPPSSTART-DD-01:** 3-layer model, not 2-layer. Separating Agent Startup from IPPS Startup is necessary because agents configure themselves independently of IPPS. Collapsing them would imply IPPS controls agent configuration, which it does not. Rationale: Real-world agents (Cascade, Claude Code, Cursor) have different startup mechanisms. IPPS must not constrain agent startup.

**IPPSSTART-DD-02:** Lazy activation, not proactive. IPPS does nothing between workflow calls. Rationale: Predictability. The user knows exactly when IPPS acts. Proactive behavior (auto-sync, auto-verify) would surprise users and consume context window budget without user consent.

**IPPSSTART-DD-03:** rules/ folder is the only shared surface. Both agent (Cascade) and /prime read rules/ folder content. Neither modifies it. Rationale: The rules/ folder defines core conventions that both the agent's system prompt and IPPS workflows need. Making it the single shared surface avoids coupling while ensuring consistency.

**IPPSSTART-DD-04:** auto_execution_mode in frontmatter is a hint, not a requirement. Agents may choose to auto-run workflows with auto_execution_mode: 3 (like /prime). IPPS defines what the workflow does when called, not whether it is called automatically. Rationale: Auto-execution is agent behavior. Different agents may handle frontmatter differently. IPPS must not assume auto-execution.

**IPPSSTART-DD-05:** /prime is read-only. It reads files and reports context but modifies nothing. Rationale: Startup must be safe. A read-only /prime cannot break workspace state. Fixes and modifications are done by /verify workspace (Layer 3 activity).

**IPPSSTART-DD-06:** Skills are loaded on demand, not at startup. /prime reads rules and docs only. Workflows load their declared skills when called. Rationale: Context window efficiency. Loading all skills at startup would consume context budget for skills the user may never call.

**IPPSSTART-DD-07:** Dimension 4 (Sync Relationship) detection is part of /prime, not a separate workflow. Rationale: /prime already reads NOTES.md for workspace context. Detecting sync markers during /prime is efficient and ensures the agent knows sync relationship before any workflow is called.

## 7. Implementation Guarantees

**IPPSSTART-IG-01:** Existing /prime behavior (steps 1-3) must not change. Adding dimension 4 detection and formalizing the startup model is additive.

**IPPSSTART-IG-02:** Agents that do not support auto_execution_mode must still be able to use IPPS by manually calling /prime.

**IPPSSTART-IG-03:** No existing workflow must break because of the startup sequence formalization. Workflows continue to be called explicitly by users.

**IPPSSTART-IG-04:** The rules/ folder shared surface must remain read-only during startup for both agent and IPPS. No startup step may write to rules/.

## 8. Key Mechanisms

### Startup Sequence

```
Agent process starts
├─> Layer 1: Agent Startup (agent-specific)
│   ├─> Read AGENTS.md (or equivalent)
│   ├─> Configure model, tools, permissions
│   ├─> Cascade: auto-load rules/ folder as system prompt
│   └─> Agent ready for user input
│
├─> Layer 2: IPPS Startup (/prime called or auto-executed)
│   ├─> Step 1: Read rules/ folder .md files
│   ├─> Step 2: Read priority docs (! prefix .md files)
│   ├─> Step 3: Read standard docs (.md files, excluding _ and !)
│   ├─> Step 4: Detect workspace scenario
│   │   ├─> Dimension 1: Project Structure
│   │   ├─> Dimension 2: Version Strategy
│   │   ├─> Dimension 3: Work Mode
│   │   └─> Dimension 4: Sync Relationship
│   └─> Report: "Read [a] .md files ([b] priority), [c] code files. Mode: [d1]+[d2]+[d3]+[d4]"
│
└─> Layer 3: IPPS Activity (user-driven, lazy activation)
    ├─> Agent idle — waiting for user input
    ├─> User calls workflow (e.g., /verify, /sync, /commit)
    ├─> Workflow loads required skills (on demand)
    ├─> Workflow executes
    └─> Agent idle — waiting for next user input
```

### Orthogonality Boundary

```
         AGENTS.md              rules/ folder            IPPS workflows
         ┌──────────┐          ┌──────────────┐          ┌──────────────┐
Agent    │  reads   │          │  reads       │          │  calls       │
         │  owns    │          │  (read-only) │          │  (on demand) │
         └──────────┘          └──────────────┘          └──────────────┘
                                    │
                              shared surface
                              (read-only both sides)

IPPS     ┌──────────┐          ┌──────────────┐          ┌──────────────┐
         │  never   │          │  /prime reads│          │  defines     │
         │  touches │          │  (read-only) │          │  content     │
         └──────────┘          └──────────────┘          └──────────────┘
```

### Workspace Dimension Detection (Step 4)

```
Detect workspace scenario (4 dimensions):
├─> Dimension 1: Project Structure
│   ├─> main.code-workspace exists? → WORKSPACE
│   ├─> Multiple project subfolders? → MONOREPO
│   └─> Otherwise → SINGLE-PROJECT
├─> Dimension 2: Version Strategy
│   ├─> Multiple version folders/detectors? → MULTI-VERSION
│   └─> Otherwise → SINGLE-VERSION
├─> Dimension 3: Work Mode
│   ├─> Active session folder exists? → SESSION-MODE
│   └─> Otherwise → PROJECT-MODE
└─> Dimension 4: Sync Relationship
    ├─> [LINKED_REPOS] or [*_SOURCE_FOLDER] or [PRODUCT_VERSION] in NOTES.md?
    │   ├─ Yes → SYNCED
    │   └─ No → SELF-CONTAINED
```

## 9. Action Flow

### Normal Startup

```
User opens workspace in agent
├─> Agent starts (Layer 1)
│   ├─> Reads AGENTS.md
│   ├─> Configures itself
│   └─> Ready
├─> /prime executed (Layer 2)
│   ├─> Reads rules/ folder
│   ├─> Reads ! prefix docs
│   ├─> Reads standard docs
│   ├─> Detects 4 dimensions
│   └─> Reports: "Read 8 .md files (3 priority), 12 code files. Mode: WORKSPACE + SINGLE-VERSION + SESSION-MODE + SYNCED"
└─> Agent idle (Layer 3)
    └─> Waiting for user to call a workflow
```

### First Workflow Call

```
User calls /verify workspace
├─> /verify workflow activated
│   ├─> Loads required skills (workspace-management)
│   ├─> Reads WORKSPACE-RULES.md
│   ├─> Detects workspace mode (from /prime or re-detects)
│   ├─> Checks rules against workspace state
│   └─> Reports: passes, gaps, incompatibilities
└─> Agent idle — waiting for next workflow call
```

### Session Creation (post-startup)

```
User calls /session-new
├─> session-management skill loaded
├─> Create session folder: _YYYY-MM-DD_TopicName/
├─> Create NOTES.md, PROBLEMS.md, PROGRESS.md
├─> STOP — wait for user review
└─> User confirms goals → work begins
```

## 10. Data Structures

### Prime Output Format

```
Read [a] .md files ([b] priority), [c] code files ([d] .py, [e] ...). Mode: [dim1] + [dim2] + [dim3] + [dim4]
```

Examples:
```
Read 5 .md files (2 priority), 12 code files (10 .py, 2 .html). Mode: SINGLE-PROJECT + SINGLE-VERSION + SESSION-MODE + SYNCED
Read 3 .md files (1 priority), 0 code files. Mode: SINGLE-PROJECT + SINGLE-VERSION + PROJECT-MODE + SELF-CONTAINED
Read 8 .md files (3 priority), 45 code files (30 .py, 15 .js). Mode: WORKSPACE + SINGLE-VERSION + SESSION-MODE + SYNCED
```

### Workspace Dimension Values

```
Dimension 1 (Project Structure): SINGLE-PROJECT | MONOREPO | WORKSPACE
Dimension 2 (Version Strategy):  SINGLE-VERSION | MULTI-VERSION
Dimension 3 (Work Mode):         SESSION-MODE | PROJECT-MODE
Dimension 4 (Sync Relationship): SYNCED | SELF-CONTAINED
```

### Agent-Agnostic Contract

```
Agent must support:
- Reading .md files from filesystem
- Running shell commands (PowerShell, bash)
- Executing workflows (slash commands or equivalent)

Agent may support:
- Auto-loading rules/ folder as system prompt content
- Auto-executing workflows based on frontmatter (auto_execution_mode)
- Custom AGENTS.md or equivalent configuration file

IPPS must not:
- Reference or depend on AGENTS.md
- Assume a specific agent or agent feature
- Require auto-execution of any workflow
- Modify rules/ folder during startup

IPPS must:
- Provide /prime as the entry point workflow
- Define all workflows as user-invoked (lazy activation)
- Keep rules/ folder as the only shared surface with agents
- Work with any agent that meets the agent-agnostic contract
```

## 11. User Actions

N/A: This is a process specification, not a UI specification. User actions are workflow invocations defined in individual workflow files.

## 12. UX Design

N/A: No UI components. All interaction is via CLI/workflow commands and console output.

## 13. Logging Requirements

**Applicable logging types:**
- [x] User-Facing (UF) - prime output, startup reporting
- [ ] App-Level (AP) - N/A: no server/service
- [ ] Script-Level (SC) - N/A: no new scripts

**User-Facing logging:**
- **Audience**: Developer starting a workspace session
- **Goal**: Understand what context was loaded and what mode was detected
- **Key operations**: /prime execution, dimension detection

**Expected output for /prime:**
```
Read 8 .md files (3 priority), 45 code files (30 .py, 15 .js).
Mode: WORKSPACE + SINGLE-VERSION + SESSION-MODE + SYNCED
```

## 14. Technical Constraints

- devsystem-core.md edit adds Startup Sequence section and formalizes 3-layer model
- prime.md edit adds Dimension 4 detection to Step 4 and updates output format
- WORKSPACE-GUIDES.md edit adds startup sequence guidance section
- No new files created in rules/ or workflows/ — this spec formalizes existing behavior
- All changes are additive — existing /prime steps 1-3 must not change
- All spec files must pass privacy gate (no real identifiers, agent names, project-specific data)
- References to _SPEC_SKILL_WORKFLOW-MANAGEMENT.md use Doc ID format: `[WSKMGMT-SP01]`
- References to session-management skill use skill reference format: `@skills:session-management`

## 15. Document History

**[2026-09-04 16:00]**
- Added: 4-Dimension Overview diagram in WorkspaceDimensions section showing all dimensions, states, detection signals, and example combinations in a single visual

**[2026-09-04 15:55]**
- Fixed: SOCAS-01 — added clarifying note that agent descriptions in Context are illustrative, not dependencies
- Fixed: SOCAS-10 — added [ASSUMED] label to Dimension 4 reference (SYNCREL-SP01 not yet implemented)
- Fixed: Synced workspace constant counts with WSKMGMT spec (5 base + 3 SYNCED-only)

**[2026-09-04 15:46]**
- Initial specification created
