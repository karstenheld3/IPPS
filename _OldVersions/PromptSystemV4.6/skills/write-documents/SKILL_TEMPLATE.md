# Skill Template

Template for writing skill documents.

## SKILL.md Structure

```markdown
---
name: [skill-name]
description: [When to apply this skill. One to three sentences covering trigger conditions and what the skill enables.]
compatibility: [Runtime requirements, e.g., "Requires Node.js 18+"]
---

# [Skill Title]

[One-liner: what this skill provides and how it relates to the underlying tool/concept.]

**References** (loaded on demand):
- [SKILLPREFIX_TOPIC.md](SKILLPREFIX_TOPIC.md) - [What it covers]

## MUST-NOT-FORGET

1. [Critical rule - most common mistake]
2. [Critical rule - data loss or security risk]
3. [Critical rule - API gotcha]

## Intent Lookup

**User wants to...**
- **[Goal A]** → [Procedure or section reference]
- **[Goal B]** → [Procedure or section reference]

## Core Procedures

### 1. [Procedure Name]

` ` `
1. [Step]
2. [Step]
` ` `

[Brief explanation of when/why to use this procedure.]

### 2. [Procedure Name]

` ` `
1. [Step]
2. [Step]
` ` `

## Gotchas

- **[Short label]** - [Explanation and fix]

## Quick Config

[Minimal copy-paste configuration to get started.]
```

## Optional Sections

Include based on skill complexity:

- **References** - Skill has supporting files
- **MUST-NOT-FORGET** - Always (even 2-3 items)
- **Intent Lookup** - Skill covers multiple use cases
- **Core Procedures** - Skill has step-by-step workflows
- **Gotchas** - Tool has non-obvious behavior
- **Quick Config** - Tool requires configuration

## Complexity Tiers

**Tier 1: Simple** (50-100 lines, 1-2 files)
- Frontmatter, title, MNF, procedures

**Tier 2: Standard** (100-200 lines, 3-5 files)
- Add Intent Lookup, Gotchas, Quick Config, supporting references

**Tier 3: Comprehensive** (200+ lines, 5-8 files)
- All sections, multiple reference files, config examples

## Composite Skill Template

When a skill has 3+ distinct functions sharing scripts, configs, or data, use the composite pattern. SKILL.md becomes a router; each function gets its own subfolder guide.

### Composite SKILL.md Structure

```markdown
---
name: [skill-name]
description: [When to apply. Cover all functions and shared infrastructure in 1-3 sentences.]
---

# [Skill Title]

One skill for [domain]. Root holds shared parts; function subfolders hold specialized workflows.

## Routing

Read this file, then jump to exactly one target:

- **[Goal A]** → `[subfolder-a]/[DOCUMENT_A].md`
- **[Goal B]** → `[subfolder-b]/[DOCUMENT_B].md`
- **[Goal C]** → `[subfolder-c]/[DOCUMENT_C].md`
- **Look up shared data** → `[SHARED_DATA.md]` or `[shared-config.json]`
- **Install or remove** → `SETUP.md`, `UNINSTALL.md`
- **Verify the skill works** → `[selftest-script]`

## Do NOT Apply When

- [Related but separate concern - point to the correct skill]

## Folder Layout

```
[skill-name]/
├── SKILL.md                      this file (routing)
├── SETUP.md, UNINSTALL.md        shared setup
├── [shared-script.py]            shared scripts at root
├── [shared-config.json]          shared data at root
├── [subfolder-a]/                function A
│   └── [DOCUMENT_A].md           function guide (no frontmatter)
├── [subfolder-b]/                function B
│   └── [DOCUMENT_B].md           function guide
└── [subfolder-c]/                function C
    └── [DOCUMENT_C].md           function guide
```

## Shared Rules

- All scripts resolve shared configs from the `[skill-name]/` root. Scripts in subfolders use `Path(__file__).resolve().parent.parent`
- [Domain-specific shared rules]
- [Tool-specific shared rules]

## Quick Commands

```powershell
[Minimal copy-paste commands for each function]
```
```

### Function Document Structure (in subfolders)

```markdown
# [Function Name] Guide

[One-liner: what this function does within the composite skill.]

## Procedures

### 1. [Procedure Name]
[Steps]

### 2. [Procedure Name]
[Steps]

## Gotchas

- **[Short label]** - [Explanation and fix]
```

No YAML frontmatter. No MUST-NOT-FORGET (that lives in the root SKILL.md). No References section (the root SKILL.md handles discovery).
