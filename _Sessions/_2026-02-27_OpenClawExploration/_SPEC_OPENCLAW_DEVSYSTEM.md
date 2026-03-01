# SPEC: OpenClaw DevSystem Integration

**Doc ID**: OCLAW-SP01
**Feature**: openclaw-devsystem-integration
**Goal**: Specify how to integrate IPPS DevSystem into OpenClaw workspaces
**Timeline**: Created 2026-03-01, Updated 1 time (2026-03-01)

**Target file**: `E:\Dev\openclaw\workspace\` (workspace bootstrap files)

**Depends on:**
- `_INFO_HOW_OPENCLAW_WORKS.md [OCLAW-IN03]` for OpenClaw architecture understanding

## MUST-NOT-FORGET

- Keep HEARTBEAT.md and memory system (daily logs + MEMORY.md)
- Drop BOOTSTRAP.md, IDENTITY.md, SOUL.md, TOOLS.md, USER.md (OpenClaw-specific, not needed)
- AGENTS.md only reads WORKFLOWS.md (nothing else)
- Sync rules/, workflows/, skills/ folders from IPPS DevSystem
- OpenClaw workspace uses git for change tracking

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Design Decisions](#5-design-decisions)
6. [Implementation Guarantees](#6-implementation-guarantees)
7. [Key Mechanisms](#7-key-mechanisms)
8. [File Mapping](#8-file-mapping)
9. [Deployment to Linked Repos](#9-deployment-to-linked-repos)
10. [Document History](#10-document-history)

## 1. Scenario

**Problem:** OpenClaw has its own workspace structure (AGENTS.md, SOUL.md, BOOTSTRAP.md, etc.) that differs from IPPS (Insanely Productive Programming System) DevSystem conventions. We want OpenClaw agents to use our DevSystem rules, workflows, and skills while preserving OpenClaw's unique features (heartbeat, memory system, WhatsApp integration).

**Solution:**
- Adapt AGENTS.md to read WORKFLOWS.md (tells agent about available workflows)
- Sync rules/, workflows/, skills/ folders from IPPS DevSystem
- Keep HEARTBEAT.md and memory/ for OpenClaw-specific features
- Use _Sessions folder for session-based work

**What we don't want:**
- Duplicate rule files between IPPS and OpenClaw
- Manual sync of rules/workflows (use deploy-to-all-repos)
- Losing OpenClaw's heartbeat and memory features
- Breaking OpenClaw's bootstrap ritual for new agents

## 2. Context

### OpenClaw Workspace Structure (Current)

```
E:\Dev\openclaw\workspace\
├── .git/                # Git tracking (exists)
├── .openclaw/           # OpenClaw workspace config
├── AGENTS.md            # Operating instructions (7.8 KB)
├── BOOTSTRAP.md         # First-run ritual (1.5 KB)
├── HEARTBEAT.md         # Periodic task checklist
├── IDENTITY.md          # Agent name/vibe/emoji
├── SOUL.md              # Persona and boundaries
├── TOOLS.md             # Local tool notes
├── USER.md              # Human profile
├── memory/              # Daily memory logs
│   └── YYYY-MM-DD.md
├── MEMORY.md            # Curated long-term memory
└── skills/              # Workspace-specific skills
```

### IPPS DevSystem Structure

```
E:\Dev\IPPS\.windsurf\
├── rules/               # Agent rules (.md files)
├── workflows/           # Agent workflows (.md files)
└── skills/              # Agent skills (folders with SKILL.md)
```

### OpenClaw Workspace Structure (Target)

```
E:\Dev\openclaw\workspace\
├── .git/                # Git tracking (preserved)
├── .openclaw/           # OpenClaw workspace config (preserved)
├── _Sessions/           # [LOCAL] OpenClaw session folders (not synced)
│   └── _YYYY-MM-DD_TopicName/
│       ├── NOTES.md
│       ├── PROGRESS.md
│       └── PROBLEMS.md
├── rules/               # [SYNCED] From IPPS .windsurf/rules/
│   ├── core-conventions.md
│   ├── devsystem-core.md
│   ├── devsystem-ids.md
│   ├── agentic-english.md
│   └── edird-phase-planning.md
├── workflows/           # [SYNCED] From IPPS .windsurf/workflows/
│   ├── prime.md
│   ├── build.md
│   ├── solve.md
│   ├── go.md
│   ├── commit.md
│   ├── verify.md
│   └── ...
├── skills/              # [SYNCED] From IPPS .windsurf/skills/
│   ├── write-documents/
│   ├── deep-research/
│   ├── session-management/
│   ├── coding-conventions/
│   ├── git-conventions/
│   └── ...
├── AGENTS.md            # [MODIFIED] Only reads WORKFLOWS.md
├── HEARTBEAT.md         # (preserved)
├── memory/              # (preserved)
│   └── YYYY-MM-DD.md
└── MEMORY.md            # (preserved)
```

### Key Differences

- **OpenClaw**: AGENTS.md only reads WORKFLOWS.md
- **DevSystem**: Same structure - rules/, workflows/, skills/ folders
- **OpenClaw**: HEARTBEAT.md for periodic tasks (unique)
- **OpenClaw**: memory/ folder for daily logs (unique)
- **Both**: _Sessions/ folder for session tracking

## 3. Domain Objects

### AGENTS.md

The **AGENTS.md** file is the main entry point for OpenClaw agents. It only reads WORKFLOWS.md.

**Location:** `workspace/AGENTS.md`
**Role:** Bootstrap instructions - tells agent to read WORKFLOWS.md

**Key sections:**
- `## Every Session` - Read WORKFLOWS.md
- `## Memory` - OpenClaw's memory system (daily logs + MEMORY.md)
- `## Heartbeat` - Periodic task handling


### rules/ Folder

The **rules/** folder contains DevSystem rules synced from IPPS.

**Location:** `workspace/rules/`
**Role:** Agent rules loaded by `/prime` workflow
**Sync source:** `E:\Dev\IPPS\.windsurf\rules\`

### workflows/ Folder

The **workflows/** folder contains DevSystem workflows synced from IPPS.

**Location:** `workspace/workflows/`
**Role:** Workflow definitions invoked with `/workflow-name` syntax
**Sync source:** `E:\Dev\IPPS\.windsurf\workflows\`

### Skills Folder

The **skills/** folder contains skill definitions synced from IPPS DevSystem.

**Location:** `workspace/skills/`
**Role:** Provides specialized capabilities (write-documents, deep-research, etc.)
**Sync source:** `E:\Dev\IPPS\.windsurf\skills\`

### Sessions Folder

The **_Sessions/** folder contains session-specific work.

**Location:** `workspace/_Sessions/`
**Role:** Stores NOTES.md, PROGRESS.md, PROBLEMS.md, and session documents

## 4. Functional Requirements

**OCLAW-FR-01: AGENTS.md Reads WORKFLOWS.md**
- AGENTS.md tells agent to read WORKFLOWS.md on every session start
- Agent reads AGENTS.md automatically (OpenClaw injects it)
- User invokes workflows as needed (e.g., `/prime`, `/build`, `/session-new`)

**OCLAW-FR-02: Standard Folder Structure**
- rules/ folder synced from IPPS `.windsurf/rules/`
- workflows/ folder synced from IPPS `.windsurf/workflows/`
- skills/ folder synced from IPPS `.windsurf/skills/`
- User can invoke workflows with `/workflow-name` syntax (e.g., `/build`, `/verify`, `/commit`)
- Agent reads `workflows/[name].md` when user invokes `/name`

**OCLAW-FR-03: Sync via deploy-to-all-repos**
- All three folders (rules/, workflows/, skills/) synced from IPPS
- Sync via deploy-to-all-repos.md workflow
- One-way sync: IPPS → OpenClaw workspace

**OCLAW-FR-04: Session Management**
- Default sessions folder: `_Sessions/`
- Session structure: NOTES.md, PROGRESS.md, PROBLEMS.md
- Session naming: `_YYYY-MM-DD_TopicName/`

**OCLAW-FR-05: Memory System Preservation**
- Keep HEARTBEAT.md for periodic tasks
- Keep memory/ folder for daily logs
- Keep MEMORY.md for curated long-term memory

**OCLAW-FR-06: Git Tracking**
- OpenClaw workspace uses git for change tracking
- Agent can commit and push changes
- Existing .git/ folder preserved
- **Sync direction**: skills/ flows one-way (IPPS → OpenClaw via deploy-to-all-repos)
- **Sync direction**: _Sessions/ is OpenClaw-internal only (not synced to IPPS)

**OCLAW-FR-07: Sub-Agent Session Spawning**
- OpenClaw can spawn sub-agents for independent work
- Each sub-agent works in its own session folder
- **Limitation**: Sub-agents use `promptMode=minimal` which omits Skills and Memory
- For complex DevSystem work, use main agent or pass rules via session NOTES.md

## 5. Design Decisions

**OCLAW-DD-01:** Use same folder structure as Windsurf (rules/, workflows/, skills/). Rationale: Agent reads rules via `/prime` just like in Windsurf; no need to embed rules in AGENTS.md.

**OCLAW-DD-02:** AGENTS.md only reads WORKFLOWS.md. Rationale: Keep AGENTS.md minimal; WORKFLOWS.md contains `/prime` which loads rules.

**OCLAW-DD-03:** Sync all three folders from IPPS. Rationale: Same DevSystem files work in both Windsurf and OpenClaw.

**OCLAW-DD-04:** Keep only HEARTBEAT.md and memory/. Rationale: Drop unused OpenClaw files (BOOTSTRAP, IDENTITY, SOUL, TOOLS, USER); keep heartbeat and memory which are unique.

**OCLAW-DD-05:** Deploy via deploy-to-all-repos.md. Rationale: Reuse existing deployment workflow; add OpenClaw workspace to [LINKED_REPOS].

## 6. Implementation Guarantees

**OCLAW-IG-01:** rules/ folder structure matches IPPS `.windsurf/rules/` exactly

**OCLAW-IG-02:** workflows/ folder structure matches IPPS `.windsurf/workflows/` exactly

**OCLAW-IG-03:** skills/ folder structure matches IPPS `.windsurf/skills/` exactly

**OCLAW-IG-04:** _Sessions/ folder follows DevSystem session conventions

**OCLAW-IG-05:** Git repository remains functional after integration

## 7. Key Mechanisms

### Workflow Invocation

When agent encounters `/workflow-name`:
1. Read `workflows/[workflow-name].md`
2. Execute workflow instructions

### Workflow Execution

User invokes workflows as needed:
1. OpenClaw injects AGENTS.md into system prompt
2. AGENTS.md tells agent to read WORKFLOWS.md
3. User invokes `/workflow-name` when they want
4. Agent reads `workflows/[name].md` and executes

### Skills Loading

Skills work identically to Windsurf:
1. Agent encounters @skill-name reference
2. Reads skills/[skill-name]/SKILL.md
3. Follows skill instructions

### Session Handover (Laptop to VM)

For long-running tasks:
1. Create session on laptop with NOTES.md, PROGRESS.md
2. Commit and push to git
3. OpenClaw on VM pulls changes
4. VM agent continues work using /session-load
5. Results committed and pushed back

## 8. File Mapping

### Files to Create/Modify

**Modify:**
- `AGENTS.md` - Simplify to only read WORKFLOWS.md, preserve Memory and Heartbeat sections

**Create:**
- `_Sessions/` - Sessions folder (empty initially)

**Sync from IPPS `.windsurf/`:**
- `rules/` - All rules
- `workflows/` - All workflows  
- `skills/` - All skills

**Keep unchanged:**
- `HEARTBEAT.md` - Periodic tasks
- `memory/` - Daily memory logs
- `MEMORY.md` - Long-term memory

**Remove:**
- `BOOTSTRAP.md` - Not needed (DevSystem has own onboarding)
- `IDENTITY.md` - Not needed (no persona needed)
- `SOUL.md` - Not needed (persona defined by DevSystem rules)
- `TOOLS.md` - Not needed (tools defined in skills/)
- `USER.md` - Not needed (user context in session NOTES.md)

### AGENTS.md Structure (After Integration)

```markdown
# AGENTS.md - OpenClaw Workspace

## Every Session
Read WORKFLOWS.md to know available workflows.

## Workflow Syntax
User invokes workflows with `/workflow-name` syntax.
When you see `/name`, read `workflows/[name].md` and execute.

Examples: `/prime`, `/build`, `/session-new`, `/verify`, `/commit`

## Memory
[Keep existing memory instructions]

## Heartbeat
[Keep existing heartbeat instructions]

## Safety
[Keep existing safety instructions]
```

### WORKFLOWS.md Purpose

WORKFLOWS.md is a **lookup table** that lists available workflows.
Actual workflow definitions are in `workflows/` folder (synced from IPPS).

```markdown
# WORKFLOWS.md - Available Workflows

Invoke with `/workflow-name`. Definitions in `workflows/` folder.

## Core Workflows
- `/prime` - Load workspace context (reads rules/)
- `/build` - BUILD workflow for code output
- `/solve` - SOLVE workflow for knowledge output
- `/go` - Autonomous loop

## Session Workflows  
- `/session-new` - Initialize new session
- `/session-load` - Resume existing session
- `/session-save` - Save session progress

## Verification Workflows
- `/verify` - Verify against specs and rules
- `/commit` - Create conventional commits
```

## 9. Deployment to Linked Repos

### Adding OpenClaw to Linked Repos

Add to `!NOTES.md` [LINKED_REPOS] section:

```markdown
- e:\Dev\openclaw\workspace
  - Overwrite: rules/, workflows/, skills/ folders
  - Create: WORKFLOWS.md, _Sessions/ (if not exists)
  - Never overwrite: AGENTS.md, HEARTBEAT.md, memory/, MEMORY.md
  - Special: AGENTS.md requires manual update (one-time)
```

### deploy-to-all-repos.md Modifications

Add OpenClaw-specific handling:

```powershell
# OpenClaw workspace - all three folders
$openclawTarget = "E:\Dev\openclaw\workspace"
$openclawRules = @{
    "syncFolders" = @("rules", "workflows", "skills")
    "createIfMissing" = @("WORKFLOWS.md", "_Sessions")
    "neverOverwrite" = @("AGENTS.md", "HEARTBEAT.md", "memory", "MEMORY.md")
}
```

### Deployment Steps

1. Run `deploy-to-all-repos` from IPPS
2. Script syncs rules/, workflows/, skills/ folders to OpenClaw workspace
3. Script creates WORKFLOWS.md if missing
4. Script creates _Sessions/ folder if missing
5. AGENTS.md updated manually (one-time setup)

### Manual AGENTS.md Update (One-Time)

After initial deployment:
1. Open `E:\Dev\openclaw\workspace\AGENTS.md`
2. Add instruction to read WORKFLOWS.md
3. Keep Memory and Heartbeat sections

## 10. Document History

**[2026-03-01 17:30]**
- Fixed: Added WORKFLOWS.md read instruction requirement (OCLAW-RV-001)
- Fixed: Added git sync direction clarification (OCLAW-RV-006)
- Fixed: Added sub-agent limitation note (OCLAW-RV-003)

**[2026-03-01 17:15]**
- Initial specification created
- Defined file mapping and deployment strategy
- Added linked repos deployment section

