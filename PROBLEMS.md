# Workspace Problems

Tracks problems, feature requests, and issues across the IPPS workspace.

Track problems using ID format: `[TOPIC]-PR-[NNNN]`

## Open

**PREL-PR-0001: project-release.md should support 2 release conventions**
- **History**: Added 2026-03-24 15:37
- **Description**: Currently only one release convention. Should support both semantic versioning (X.Y.Z) and date-based (YYYY-MM-DD) releases
- **Impact**: Projects using date-based releases cannot use the workflow as-is
- **Next Steps**: Update `project-release.md` to detect or ask which convention, adapt tag format and release notes accordingly

**DVSYS-FT-0001: DevSystem V5.0 Requirements**
- **History**: Added 2026-08-03 16:31
- **Target**: DevSystem V5.0

1. **Migrate ALL workflows to skills**
   - Find out how to implement write-info, write-strut, write-prompts as skills
   - 1 short file per workflow with multiple branching files for each context
   - Reduce number
   - Add predefined PowerShell scripts where useful to reduce command-line handling time and add stability

2. **Additional workflows or commands**
   - **write-prompts** - Writes 1 or many prompts into a `_PROMPTS_[TopicsOrTask].md` file
   - **execute** - Execute defined workflow, tasks, prompts as sequence with self-reflection
   - **propose** - Propose options in chat
   - **draft** - Create annotated drafts (templates, conversations, specs, info, etc.). How to draft skeletons first and then fill sections later.
   - **investigate** - Meta-prompt for investigating a behavior, assumption, reported bug. Always produces special templated `_INFO_` document. Remedy for superficial, misleading, low-token-budget investigations that are unsound and waste time.
   - **factcheck** - Identifies: 1) factual statements, 2) derivative statements. Checks both against the noted sources. Ensures that sources are inlined in the documents (URLs, source names, dates, verbatim citations with page numbers) and that derivative statements are sound and stand up against critical analysis.
   - **write-skill** - Create agent skills based on rules and templates
   - **write-code** - Language-independent rules with language-specific rules as extensions (subfolders)
   - **write-workflow** - Standardized part of skill, replaces current Cascade workflows and old Claude Code commands
   - **compare** - Branching comparison workflow: 1) different versions of same file: use classic diff, 2) different files: use LLM compare with document-type-aware prompts and focuses, 3) folders, projects, office files: use extra tools and branching to create useful outputs. Must produce standardized file that is then used with sync.md to check dependent files for change propagation.
   - **migrate** - Cross-project and cross-workspace migration: 1) migrate code from one project to another (extract, adapt imports/paths, verify), 2) migrate documents and folders from one workspace to another (preserve IDs, update references, handle naming conflicts)

3. **Generic self-reflection using MNF**
   - How to add self-reflection to have better output consistency in the first generative run?
   - Examples: Markdown rules, used chars, Umlaute, LLM "literally translated English" mistakes and other frequent topics that we have to verify and improve later

4. **Question "agentic-English" and other rules**
   - Which rules are global?
   - How can they be tweaked or changed while the prompt library is running?
   - Where do they apply, how are exceptions or overwrites handled?

5. **How to implement GRUC for each document writing skill?**
   - More and better `_TEMPLATE.md` files - standardized output across documents, better drift-correction
   - More and better `_GUIDES.md` files - explain cognitive concepts, goals, processes and approaches to agent
   - More and better `_RULES.md` files - better low-level instruction following by explaining each rule with GOOD and BAD examples
   - More and better `_CHECKS.md` files - better output quality control after generation that is consistent with `_GUIDES.md` files

6. **Retire global EDIRD rules and references**
   - This can be done via skill that writes STRUT, TASKS and other planning documents

7. **Workspace management skill**
   - Initialize workspaces with DevSystem files and workspace-level files using templates and opinionated workspace definitions (how to configure IPPS DevSystem)
   - Update DevSystem from main IPPS repo
   - Manage and migrate deprecated DevSystem stuff
   - Must cover the following areas:
     - **WORKSPACE**: How to update workspace settings and defaults from a central source and how to change and migrate them if DevSystem and interaction with workspace and session files changes
     - **DEVSYSTEM**: How to update the agentic DevSystem (skills, rules, definitions, instructions, etc.) from a central source
     - **KNOWLEDGE**: How to update crucial documentation (API docs, domain knowledge, company rules and instructions, etc.) from a central source
   - All 3 we should be able to:
     1) Compare against central source
     2) Update from central source with additional content migration if we have breaking changes
     3) Roll back to previous version (last checked in version in repo or another version in central storage)
     4) Check integrity (all set up correctly and completely as specified in workspace NOTES.md)

8. **Review thin/unused workflows during migration**
   - **`/build`** and **`/solve`** are near-identical 40-line orchestrators that only chain `/session-new` → `@edird-phase-planning` → `/session-finalize`. Consider merging into one or inlining into `edird-phase-planning` skill
   - **`/partition`** has zero cross-references in active DevSystem. Evaluate if `write-tasks-plan` fully replaces it
   - **`/session-finalize`** is heavily referenced (8 files) - KEEP, not unused
   - Decision: merge, retire, or simplify during skill migration

9. **STORYTELLING rules in write-documents skill**
   - In addition to MINTO (logical, business oriented) we also need STORYTELLING rules

11. **Evolve GRUC principle: add Templates, rename, generic discovery**
    - Add instructive Templates (with inline instructions) to GRUC principle. Maybe rename the whole principle.
    - Better implementation of GRUC philosophy: Guides, Rules, Checks should each be creatable and updateable with 1 single workflow.
    - Instructive Templates must be a part of the whole idea.
    - Figure out how write-document and write-code skill workflows + the generic `verify.md`, `improve.md`, `critique.md` workflows can find and use these files in a generic way.
    - Ideally other skills can re-use everything to create ad-hoc templates + GRUC files to repeat outputs and ensure consistency over multiple runs and files.
    - Reference: `_INFO_GRUC_GUIDES_RULES_CHECKS.md [GRUC-IN01]`

10. **Session folder structure: separate agent files from output**
    - Currently agent workflow and temporary files are in same folder as output
    - Need clearer separation:
      - **`_AGENT_PROMPTS_WORKFLOWS`** - To store prompts, callable workflows, local `*_TEMPLATE.md`, `*_RULES.md`, `*_GUIDE.md`, `*_CHECKS.md` files
      - **`_AGENT_WORKSTREAM`** - Everything that is covered by `cleanup.md` and can be removed later. Like drift files, document versions, deferred improvements file, reviews etc. These will be checked in for audit reasons as long as they are needed.
    - Review each agent artifact:
      1) Is it temporary? Either: 1. prefix with `__` to be caught by `cleanup.md`, or 2. store in workstream
      2) Is it session output? It can remain where it currently is placed.
      - For example TASKS and STRUT are candidates for workstream files
    - Already have:
      - `_TNN_[Topic]_[Date]` folders for subtopics
      - `_SNN_[Topic]_[Date]` folders for steps
      - `_DOWNLOAD_gitignore` folders for downloaded content
      - `_SOURCES` for transcribed content

12. **ASCII art diagrams, UX designs, and markdown formatting in write-documents skill**
   - Guides, rules, templates, and scripts to create and update ASCII art diagrams and UX designs in markdown documents
   - **Workflow**: `ascii-art.md` → creates, edits, transforms ASCII art diagrams and visualizations
   - **Script**: `md.py` → comprehensive markdown formatting and extraction CLI tool
     - Detects frame glitches in ASCII art diagrams and UX designs and fixes them
     - Detects markdown table glitches and fixes them
     - Adds chapter links to table of contents
     - Detects unexpanded acronyms and lists them with contextual information (lines, positions, sentences)
     - Outputs markdown file structure and outline
     - Formatting style extraction for LLMs to insert content with consistent formatting
   - **Goal**: Ensure consistent formatting of markdown files that are easily readable by humans (equal-width formatted columns in tables) and editable by agents (extracted formatting and content)

13. **Deep-research and research update compatibility (re-run over existing output)**
   - Make `deep-research.md` (+ skill) and `research.md` support re-running over existing research output
   - **Copy existing output**: Preserve original output as backup before modifying (versioned copy, e.g., `_INFO_[TOPIC]-IN01_v1_[Date].md`)
   - **Verify all claims using `/fact-check`**: Run fact-check workflow over existing output to find changes on the web - sources that changed, disappeared, or now say something different
   - **Re-research old research questions**: Re-execute original research questions to find updates, new sources, or corrections on the web since last research date
   - **Update output**: Merge verified updates into existing INFO documents, preserving original findings with `[UPDATED YYYY-MM-DD]` markers and adding new findings with access dates
   - **Source diff**: Compare existing `_SOURCES/` transcriptions against current web content to detect staleness
   - **Detection**: Workflow detects existing research output by checking for `_INFO_*.md` files matching the topic in the target folder
   - **Affected files**: `deep-research.md` workflow, `research.md` workflow, `deep-research` skill (SKILL.md, RESEARCH_STRATEGY_MEPI.md, RESEARCH_STRATEGY_MCPI.md), `fact-check.md` workflow (as dependency)

14. **Deep-research reusable templates via write-template workflow**
   - Deep-research should use proper reusable templates created via `write-template.md` workflow (+ guides + rules)
   - **Goal**: Make it easy to create, compare, and update multi-file outputs
   - **Block templates**: Add blocks of INFO files that share the same output structure, tied together by a common template
   - **Template includes**: Hints and instructions inline in the template (instructive templates, not just structural skeletons)
   - **Consistent structure**: All INFO files in a multi-file research set follow the same template sections, enabling:
     - Easy comparison across topic files (same section layout)
     - Easy updates (change template, re-apply across files)
     - Better drift detection (structural deviations stand out)
   - **Affected files**: `deep-research` skill (new template files in skill folder), `write-template.md` workflow (must support research template creation), `RESEARCH_STRATEGY_MEPI.md` and `RESEARCH_STRATEGY_MCPI.md` (reference templates instead of inline structure)

## Resolved

(none)

## Deferred

(none)

## Problems Changes

**[2026-09-05 15:26]**
- Updated: DVSYS-FT-0001 (added item 14 - deep-research reusable templates via write-template workflow)

**[2026-09-05 15:23]**
- Updated: DVSYS-FT-0001 (added item 13 - deep-research and research update compatibility, re-run over existing output with fact-check verification)

**[2026-09-03 19:09]**
- Updated: DVSYS-FT-0001 (added item 12 - ASCII art diagrams, UX designs, and markdown formatting in write-documents skill)

**[2026-08-03 16:31]**
- Added: DVSYS-FT-0001 (DevSystem V5.0 requirements - 5 areas)

**[2026-03-24 15:37]**
- Added: PREL-PR-0001 (project-release.md dual release convention support)
