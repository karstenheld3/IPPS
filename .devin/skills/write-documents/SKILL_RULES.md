# Skill Document Rules

Rules for writing skill folders and SKILL.md files.

**Writing quality:** Apply `APAPALAN_RULES.md` to all skill content. Key rules for skills: AP-PR-07 (be specific), AP-BR-02 (sacrifice grammar for brevity), AP-NM-01 (one name per concept).

## Rule Index

Header (HD)
- SK-HD-01: YAML frontmatter with `name` and `description` required
- SK-HD-02: `description` must state when to apply (trigger conditions)
- SK-HD-03: Include `compatibility` field if tool has runtime requirements

Structure (ST)
- SK-ST-01: SKILL.md is the entry point - must be self-contained for common use cases
- SK-ST-02: Include MUST-NOT-FORGET section (3-10 items, ordered by impact)
- SK-ST-03: Include Intent Lookup when skill covers multiple use cases
- SK-ST-04: Procedures use numbered steps with tool invocations
- SK-ST-05: SETUP.md must include pre-installation verification section with checklist
- SK-ST-06: SETUP.md installation must be idempotent with backup-before-modify
- SK-ST-07: UNINSTALL.md must include pre-uninstall verification section

Files (FL)
- SK-FL-01: Flat layout - no subdirectories for fewer than 12 files
- SK-FL-02: Standard files keep standard names: `SETUP.md`, `UNINSTALL.md`
- SK-FL-03: Skill-specific files use skill prefix: `PLAYWRIGHT_TOOLS.md`, `GIT_HOOKS.md`
- SK-FL-04: Config example files use lowercase: `playwright_config_examples.json`
- SK-FL-05: All files referenced from SKILL.md References section
- SK-FL-06: 12+ files for a specific topic justifies a subfolder (e.g., `examples/`)
- SK-FL-07: Template files use `_TEMPLATE` suffix: `_TEMPLATE.md` for documents, `_template.ext` for scripts/code

Content (CT)
- SK-CT-01: SKILL.md provides procedures and decision logic, not tool parameter docs
- SK-CT-02: Tool parameters come from MCP handshake or `--help` - do not duplicate
- SK-CT-03: Gotchas section for non-obvious behavior, deprecated APIs, common mistakes
- SK-CT-04: Quick Config section with minimal copy-paste examples
- SK-CT-05: No visual-only formatting in LLM-consumed reference files (no bold, no filler phrases)
- SK-CT-06: No Document History section in skill documents (SKILL.md, _RULES, _GUIDE, _CHECKS)

Architecture (AR)
- SK-AR-01: Composite skill SKILL.md is a router only - routing table, shared rules, quick commands; no function-specific procedures
- SK-AR-02: Composite skill function documents have NO YAML frontmatter (they are not separate skills)
- SK-AR-03: Composite skill function documents use UPPERCASE naming (e.g., EVALUATION.md)
- SK-AR-04: Shared scripts and configs live at composite skill root, not in function subfolders
- SK-AR-05: Subfolder scripts resolve shared configs via Path(__file__).resolve().parent.parent
- SK-AR-06: Composite skill routing table uses one line per function: `- **[Goal]** → [path]`
- SK-AR-07: Composite skill requires 3+ distinct functions sharing infrastructure

## SK-HD-01: Frontmatter

**BAD:**
```yaml
---
name: playwright
---
```

**GOOD:**
```yaml
---
name: ms-playwright-mcp
description: Automates browser interactions via Microsoft Playwright MCP server. Use when navigating websites, filling forms, or testing web UI.
compatibility: Requires Node.js 18+ and @playwright/mcp package via npx
---
```

## SK-ST-01: Self-Contained SKILL.md

SKILL.md must answer the most common questions without loading reference files. Reference files are for deep dives.

**BAD:** SKILL.md says "See TOOLS.md for available tools" with no tool summary.

**GOOD:** SKILL.md has quick reference of core tools, links to TOOLS.md for full catalog.

## SK-FL-01: Flat Layout

**BAD:**
```
my-skill/
  SKILL.md
  references/
    AUTH.md
  assets/
    config.json
```

**GOOD:**
```
my-skill/
  SKILL.md
  MYSKILL_AUTH.md
  myskill_config.json
```

## SK-FL-02: Standard File Names

Files that exist across multiple skills keep unprefixed names for consistency.

**Standard names:** `SETUP.md`, `UNINSTALL.md`

**BAD:** `PLAYWRIGHT_SETUP.md`, `GIT_UNINSTALL.md`

**GOOD:** `SETUP.md`, `UNINSTALL.md`

## SK-FL-03: Skill-Specific Prefix

Files unique to a skill use an uppercase prefix derived from the skill's domain.

**BAD:** `TOOLS.md` (ambiguous across skills)

**GOOD:** `PLAYWRIGHT_TOOLS.md` (clearly scoped)

## SK-FL-07: Template File Naming

Files intended as templates (copied and adapted per project) MUST use the `_TEMPLATE` suffix to distinguish them from operational files.

- Documents: `_TEMPLATE.md` (uppercase, matches document convention)
- Scripts and code: `_template.ext` (lowercase extension matches code convention)

**BAD:**
```
hosting/netlify/
  deploy.bat            # Looks like a runnable script
  deploy.ps1            # Ambiguous: template or operational?
```

**GOOD:**
```
hosting/netlify/
  deploy_template.bat  # Clearly a template to copy and adapt
  deploy_template.ps1  # Clearly a template to copy and adapt
```

**BAD:** `CONVERSATION.md` used as a template (no suffix)

**GOOD:** `CONVERSATION_TEMPLATE.md` (existing convention, already correct)

## SK-CT-01: Procedures Over Parameters

Skills teach *how* and *when*, not *what parameters exist*.

**BAD:** "`browser_click` accepts `ref` (string), `element` (string), `button` (enum: left, right, middle)"

**GOOD:** "After navigation or click, always re-snapshot before clicking - refs are ephemeral"

## SK-AR-01: Router-Only SKILL.md for Composite Skills

Composite skill SKILL.md contains a routing table, shared rules, and quick commands. Function-specific procedures live in subfolder documents.

**BAD:** Composite SKILL.md contains full procedures for evaluation, transcription, and computer-use (300+ lines).

**GOOD:** Composite SKILL.md has a routing table (10 lines), shared rules (5 lines), quick commands (5 lines). Each function's procedures are in `evaluation/EVALUATION.md`, `transcription/TRANSCRIPTION.md`, `computer-use/COMPUTER_USE.md`.

## SK-AR-02: No Frontmatter on Function Documents

Function subfolder documents are guides within the composite skill, not separate skills. They must not have YAML frontmatter.

**BAD:**
```yaml
---
name: evaluation
description: LLM evaluation pipelines
---
# Evaluation Guide
```

**GOOD:**
```markdown
# Evaluation Guide

This function covers LLM-as-judge evaluation pipelines...
```

## SK-AR-03: Uppercase Function Document Names

Function documents use UPPERCASE naming to distinguish from skill entry points (always `SKILL.md`).

**BAD:** `evaluation/skill.md`, `transcription/guide.md`

**GOOD:** `evaluation/EVALUATION.md`, `transcription/TRANSCRIPTION.md`, `computer-use/COMPUTER_USE.md`

## SK-AR-04: Shared Resources at Root

Scripts, configs, and data files shared across functions live at the composite skill root. Function subfolders contain only function-specific scripts and documents.

**BAD:** `evaluation/model-pricing.json` (duplicated from root)

**GOOD:** `model-pricing.json` at root, `evaluation/generate-questions.py` in subfolder

## SK-AR-05: Subfolder Config Resolution

Scripts in function subfolders resolve shared config files by navigating to the skill root: `Path(__file__).resolve().parent.parent`.

**BAD:** `Path(__file__).parent / "model-pricing.json"` (looks in subfolder)

**GOOD:** `Path(__file__).resolve().parent.parent / "model-pricing.json"` (looks at skill root)

## SK-AR-06: Routing Table Format

Composite skill SKILL.md contains a routing table with one line per function.

**BAD:** Paragraph describing each function with inline links.

**GOOD:**
```markdown
## Routing

- **Evaluate LLM output** → `evaluation/EVALUATION.md`
- **Transcribe images or audio** → `transcription/TRANSCRIPTION.md`
- **Automate the desktop** → `computer-use/COMPUTER_USE.md`
```

## SK-AR-07: Minimum Three Functions

Composite skill structure requires 3+ distinct functions sharing infrastructure. Fewer than 3 functions should use a flat SKILL.md with Intent Lookup.

**BAD:** Composite skill with 2 subfolders (use Intent Lookup instead).

**GOOD:** Composite skill with 3+ subfolders, each with its own workflow and shared root resources.
