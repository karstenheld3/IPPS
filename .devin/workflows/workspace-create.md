---
description: Create a new workspace with interactive questionnaire
auto_execution_mode: 3
---

# Workspace Create Workflow

Create a new single-repo or multi-repo workspace using an interactive questionnaire with defaults and impact descriptions.

**Goal**: A fully initialized workspace with all required files, constants, and folder structure

**Why**: Eliminates manual setup errors and ensures new workspaces conform to DevSystem structure rules from the start

Scope: Workspace creation only. Use `/verify workspace` for integrity checks on existing workspaces.

## Required Skills

- @skills:workspace-management for WORKSPACE_CREATION_QUESTIONNAIRE.md questionnaire and templates

## MUST-NOT-FORGET

- Load WORKSPACE_CREATION_QUESTIONNAIRE.md before presenting any questions
- Do not replicate questionnaire content in this workflow - reference the guide
- Each question must show default value and impact description from the guide
- Conditional sections depend on Section 1 answer (SINGLE-PROJECT vs WORKSPACE)
- No confirmation gates - workspace creation is non-destructive per WF-EX-01
- Run `/verify workspace` after file generation to confirm integrity

## Prerequisites

- Target folder exists or can be created → proceed
- Target folder already contains NOTES.md or !NOTES.md → abort, workspace already initialized

## GLOBAL-RULES

Apply before any context-specific steps:

1. Load WORKSPACE_CREATION_QUESTIONNAIRE.md before presenting any questions
2. Do not replicate questionnaire content in this workflow - reference the guide
3. Each question must show default value and impact description from the guide
4. No confirmation gates - workspace creation is non-destructive per WF-EX-01

# CONTEXT-SPECIFIC

## SINGLE-PROJECT

Sections: 1 (Workspace Mode), 3 (Dev Repo), 4 (Version Strategy), 6 (Release Configuration)

1. Load WORKSPACE_CREATION_QUESTIONNAIRE.md from `[AGENT_FOLDER]/skills/workspace-management/`
2. Present Section 1 (Workspace Mode) to user. Accept default or user value
3. Present remaining applicable sections one at a time. Collect answers with defaults
4. Generate workspace files from templates:
   - Read DEV_REPO_NOTES_TEMPLATE.md from `[AGENT_FOLDER]/skills/workspace-management/`
   - Substitute collected answers into template placeholders
   - Create NOTES.md at workspace root
   - Create PROBLEMS.md, PROGRESS.md, ID-REGISTRY.md, SOPS.md, FAILS.md
   - Copy WORKSPACE_CREATION_QUESTIONNAIRE.md from `[AGENT_FOLDER]/skills/workspace-management/` to workspace root as `_WORKSPACE_CREATION_QUESTIONNAIRE.md`
   - Create empty folders: [AGENT_FOLDER], _sessions, _sessions/_archive, Docs/ReleaseNotes (if release configured)
5. Sync DevSystem files from source to [AGENT_FOLDER] using @skills:workspace-management Procedure 2
6. Run `/verify workspace` to confirm all required files and constants are present

## WORKSPACE

Sections: 1 (Workspace Mode), 2 (Product Repo), 3 (Dev Repo), 4 (Version Strategy), 5 (Sync Sources), 6 (Release Configuration), 7 (Skill Categories)

1. Load WORKSPACE_CREATION_QUESTIONNAIRE.md from `[AGENT_FOLDER]/skills/workspace-management/`
2. Present Section 1 (Workspace Mode) to user. Accept default or user value
3. Present remaining applicable sections one at a time. Collect answers with defaults
4. Generate workspace files from templates:
   - Read DEV_REPO_NOTES_TEMPLATE.md from `[AGENT_FOLDER]/skills/workspace-management/`
   - Read PRODUCT_REPO_README_TEMPLATE.md
   - Substitute collected answers into template placeholders
   - Create !NOTES.md at workspace root
   - Create PROBLEMS.md, PROGRESS.md, ID-REGISTRY.md, SOPS.md, FAILS.md
   - Create main.code-workspace referencing product repo
   - Create README.md in product repo
   - Copy WORKSPACE_CREATION_QUESTIONNAIRE.md from `[AGENT_FOLDER]/skills/workspace-management/` to workspace root as `_WORKSPACE_CREATION_QUESTIONNAIRE.md`
   - Create empty folders: [AGENT_FOLDER], _sessions, _sessions/_archive, knowledge/, rules/
5. Sync DevSystem files from source to [AGENT_FOLDER] using @skills:workspace-management Procedure 2
6. Run `/verify workspace` to confirm all required files and constants are present

## No Context Match

1. If Section 1 answer is neither SINGLE-PROJECT nor WORKSPACE, ask user to choose between the two options

## Output

`Created: [file] | Mode: [SINGLE-PROJECT|WORKSPACE] | Files: [N] | Folders: [N]`

## Quality Gate

- [ ] WORKSPACE_CREATION_QUESTIONNAIRE.md loaded before presenting questions
- [ ] All applicable sections presented with defaults and impact descriptions
- [ ] Files generated from templates (not hardcoded content)
- [ ] All required tracking files created (NOTES.md, PROBLEMS.md, PROGRESS.md, ID-REGISTRY.md, SOPS.md, FAILS.md)
- [ ] DevSystem synced to [AGENT_FOLDER]
- [ ] `/verify workspace` passed
