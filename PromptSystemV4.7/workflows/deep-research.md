---
description: Execute deep research (MEPI or MCPI) with domain-specific patterns and quality pipeline
---

# Deep Research Workflow

**Goal**: Multi-source research output with verified claims for a topic.

**Why**: Shallow research produces unverified claims that propagate into specs and decisions.

## Required Skills

- @skills:research-methods for research strategies, domain profiles, source processing
- @skills:session-management for Topic Folder creation and session detection

## MUST-NOT-FORGET

- **Cascade: `gesetze-im-internet.de` Playwright only** - `search_web` / `read_url_content` crash the conversation

## Execution

1. Read @skills:research-methods SKILL.md for core principles and phase model
2. **Detect Work Mode and create output folder** (SKILL.md "Output Folder" section)
3. **Register Topic ID** in ID-REGISTRY.md per Topic Registry rules in promptsystem-ids.md
4. Read the appropriate strategy file (MCPI or MEPI) based on user intent
5. Execute Phases 1-4 per strategy file instructions

## Agent-Created Folders

- `_agentwork/` - role: agentwork; parent: working folder (`T##_` topic folder); creator: Step 2; content: `__STRUT_*`, `_PROMPTS_*`, `__TASKS_*`
- Research source folders (`_download_gitignore/`, `.tmp_jpgs/`, `_sources/`): registered in @skills:research-methods SKILL.md
