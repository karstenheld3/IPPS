# Workspace Problems

Tracks problems, feature requests, and issues across the IPPS workspace.

Track problems using ID format: `[TOPIC]-PR-[NNNN]`

## Open

**PRMTHANGFIX-PR-0001: Prompt sequences still issue hanging terminal commands**
- **History**: Added 2026-11-11 13:42 (session `_2026-11-11_PromptSequenceHangPrevention`)
- **Description**: Agents in prompt sequences run long inline multi-statement PowerShell commands that hang (observed: update sequence prompt 08/14)
- **Status**: Fix implemented and mirrored to `.devin/` (supervised runner without deadline, hang verdict by the agent, kill script, Fails card, runtime-check line); bench `runner5` 27/27, contract tests 14/14
- **Next Steps**: Live acceptance test `_PROMPTS_99-HangAcceptance.md` in Cascade; then `.claude/` rebuild (`_PROMPTS_UpdateClaude.md`), downstream `/sync`

**PRMTHANGFIX-PR-0004: Repeated hangs need constant human intervention**
- **History**: Added 2026-11-11 13:42
- **Status**: Fix implemented (Fails card "Never again" list checked before every command, hang verdict + stop file)
- **Next Steps**: Live acceptance test, prompt 4 must reuse the replacement; resolve after it passes

**PRMTHANGFIX-PR-0006: Hang verdict by the agent is untested in live runs**
- **History**: Added 2026-11-11 20:25
- **Description**: After the time cap was removed (PRMTHANGFIX-FL-0001) a real hang ends only when the agent applies the hang verdict (`agent-behavior.md` Terminal Hang Prevention step 5). The bench plays the agent with a fixed 5 s stop; thresholds 5 and 10 minutes are not tested live
- **Impact**: A hang without a telling output line may wait longer than needed; slow work may be ended by a wrong verdict
- **Next Steps**: Add a real-hang prompt to `_PROMPTS_99-HangAcceptance.md`, run it in Cascade

**PRMTHANGFIX-PR-0007: Older documents still describe the time-cap design**
- **History**: Added 2026-11-11 20:50
- **Description**: Still mention caps: `specs/_SPEC_TERMINAL_ROBUSTNESS_SKILL.md`, `specs/_SPEC_IPPS_PROMPT_FILE_FORMAT.md` (DD-12, DD-14), `docs/_INFO_HOW_TO_WRITE_ROBUST_PROMPT_SEQUENCES.md`, `docs/_INFO_HOW_TO_PREVENT_AGENTS_FROM_HANGING.md` sections 7.4 and 8.1 to 8.3 (marked superseded); session `_IMPL_AGENT_TERMINAL_ROBUSTNESS.md`; `.claude/` (until rebuilt)
- **Next Steps**: Reverse-update from `AGENTTERMINAL-SP01`

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
    - needs handling of skipped prompts: What has to happen if expected work is not found and the whole prompt sequence cant be run?
    - needs model tiering so work can be partitioned correctly across prompts using target model capability and context window size.
  - **execute** - Execute defined workflow, tasks, prompts as sequence with self-reflection
  - **propose** - Propose options in chat
  - **draft** - Create annotated drafts (templates, conversations, specs, info, etc.). How to draft skeletons first and then fill sections later.
  - **investigate** - Meta-prompt for investigating a behavior, assumption, reported bug. Always produces special templated `_INFO_` document. Remedy for superficial, misleading, low-token-budget investigations that are unsound and waste time.
    - **Status**: Implemented 2026-09-09 in DevSystemV4.3. Deliverables: `specs/_SPEC_INVESTIGATE_WORKFLOW.md [INVESTIGATE-SP01]`, `workflows/investigate.md`, `skills/write-documents/INVESTIGATION_LOG_TEMPLATE.md`, `skills/write-documents/INVESTIGATION_GUIDES.md`, `skills/write-documents/INVESTIGATION_LOG_RULES.md`, `verify.md` updated with Investigation Logs section. Topic `INVESTIGATE` registered in ID-REGISTRY.md. Session: `_PrivateSessions_gitignore/_2026-09-09_InvestigateWorkflow/`.
  - **factcheck** - Identifies: 1) factual statements, 2) derivative statements. Checks both against the noted sources. Ensures that sources are inlined in the documents (URLs, source names, dates, verbatim citations with page numbers) and that derivative statements are sound and stand up against critical analysis.
  - **write-skill** - Create agent skills based on rules and templates
  - **write-code** - Language-independent rules with language-specific rules as extensions (subfolders)
  - **write-workflow** - Standardized part of skill, replaces current Cascade workflows and old Claude Code commands
  - **compare** - Branching comparison workflow: 1) different versions of same file: use classic diff, 2) different files: use LLM compare with document-type-aware prompts and focuses, 3) folders, projects, office files: use extra tools and branching to create useful outputs. Must produce standardized file that is then used with sync.md to check dependent files for change propagation. This is intended to become the major workflow for verified document intelligence features that produce INFO documents and reports
    - Compare 2 or more contracts, summarize each version with a standardized format: Unique parts, major / minor deviations, omissions, common parts.
    - Compare 2 or more specifications
  - **migrate** - Cross-project and cross-workspace migration: 1) migrate code from one project to another (extract, adapt imports/paths, verify), 2) migrate documents and folders from one workspace to another (preserve IDs, update references, handle naming conflicts)
  - **archive** - New generic implementation that can archive
    1) intermediate and less relevant files in a session to _archive_gitignore subfolder
      - like this `/archive 
    2) finilized, abandoned or less relevant sessions to workspace _archive_gitignore subfolder
    3) unneeded, intermediate and less relevant files in the entire workspace or folder (with or without subfolders)
    - How it works: `/archive <input_or_source> <goal_or_target> <options>`
    - Zip current archivable session files to date-stamped archive -> creates _archive_gitignore\2026-11-09_PipelineRuns-From-2026-09-31-To-2026-10-31.zip
      - `/archive zip` or `/archive session zip`-> only from session root folder
      - `/archive zip all` or `/archive all zip` or `/archive session zip all` -> session root folder including all subfolders
    - Archive all TASKS plans and STRUT files -> move all `*STRUT_*.md` and `*TASKS_*.md` files to _archive
      - `/archive all planning files from _agentwork`
    - Sweep through entire workspace and identify all files and sessions that can be archived but do not archive them -> creates a .tmp_archive_files_v01.txt and presents results
      - `/archive preview workspace all` or `/archive propose workspace all`
  - **check** - New generic workflow that performs post-workflow GRUC checks on workflow, STRUT or prompt sequence outputs. Very much like improve.md workflow or critique.md workflow, just by focusing ONLY on existing CHECKS files.
    1. identifies check targets from context or files
    2. identifies *_CHECKS.md files that applies to each target (for example `PROMPTS_CHECKS.md`on `write-prompts` output)
    3. reads checks, produces a review document (with TBD filename scheme aligned with other review documents) with suggestions for improvement
    4. creates backup versions just like improve.md workflow and applies all changes in targets
    5. when run with `inline` option, applies the suggestions directly without creating extra review file and backups


3. **Generic self-reflection using MNF**
  - How to add self-reflection to have better output consistency in the first generative run?
  - Examples: Markdown rules, used chars, Umlaute, LLM "literally translated English" mistakes and other frequent topics that we have to verify and improve later

4. **Question "agentic-English" and other rules**
  - Which rules are global?
  - How can they be tweaked or changed while the prompt library is running?
  - Where do they apply, how are exceptions or overwrites handled?

5. **How to implement GRUC for each document writing skill?**
  - More and better `_TEMPLATE.md` files - standardized output across documents, better drift-control
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
  - **Status**: GRUC files created 2026-09-12. Deliverables: `ASCII_ART_GUIDES.md`, `ASCII_ART_RULES.md`, `ASCII_ART_CHECKS.md`, 4 EXAMPLES files, `SetAsciiBoxStyle.ps1` (with -DryRun), `ascii-diagram.md` workflow, `[ASCII-DIAGRAM]` verb in SKILL.md. Topic `ASCIIART` registered. Session: `_PrivateSessions_gitignore/_2026-09-10_AsciiArtGuidelines/`. Deferred improvements logged in `docs/_DEFERRED_ASCII_ART_IMPROVEMENTS.md`.
  - **Remaining**: `md.py` comprehensive markdown formatting CLI tool (postponed - develop individual PowerShell scripts per problem, consolidate later)

13. **Deep-research and research update compatibility (re-run over existing output)**
  - Make `deep-research.md` (+ skill) and `research.md` support re-running over existing research output
  - **Copy existing output**: Preserve original output as backup before modifying (versioned copy, e.g., `_INFO_[TOPIC]-IN01_v1_[Date].md`)
  - **Verify all claims using `/fact-check`**: Run fact-check workflow over existing output to find changes on the web - sources that changed, disappeared, or now say something different
  - **Re-research old research questions**: Re-execute original research questions to find updates, new sources, or corrections on the web since last research date
  - **Update output**: Merge verified updates into existing INFO documents, preserving original findings with `[UPDATED YYYY-MM-DD]` markers and adding new findings with access dates
  - **Source diff**: Compare existing `_SOURCES/` transcriptions against current web content to detect staleness
  - **Detection**: Workflow detects existing research output by checking for `_INFO_*.md` files matching the topic in the target folder
  - **Affected files**: `deep-research.md` workflow, `research.md` workflow, `research-methods` skill (SKILL.md, RESEARCH_STRATEGY_MEPI.md, RESEARCH_STRATEGY_MCPI.md), `fact-check.md` workflow (as dependency)

14. **Deep-research reusable templates via write-template workflow**
  - Deep-research should use proper reusable templates created via `write-template.md` workflow (+ guides + rules)
  - **Goal**: Make it easy to create, compare, and update multi-file outputs
  - **Block templates**: Add blocks of INFO files that share the same output structure, tied together by a common template
  - **Template includes**: Hints and instructions inline in the template (instructive templates, not just structural skeletons)
  - **Consistent structure**: All INFO files in a multi-file research set follow the same template sections, enabling:
    - Easy comparison across topic files (same section layout)
    - Easy updates (change template, re-apply across files)
    - Better drift detection (structural deviations stand out)
  - **Affected files**: `research-methods` skill (new template files in skill folder), `write-template.md` workflow (must support research template creation), `RESEARCH_STRATEGY_MEPI.md` and `RESEARCH_STRATEGY_MCPI.md` (reference templates instead of inline structure)

## Resolved

**PRMTHANGFIX-PR-0002, PR-0003, PR-0005: failure recording, runtime check, search tool gap** [FIXED 2026-11-11]
- **History**: Added 2026-11-11 13:42 / 13:55 → Fixed 2026-11-11 19:15
- **Fix**: separate `__CARD_[TOPIC]-Fails.md` per working folder (PR-0002); one `Runtime check:` line per implementation prompt (PR-0003); `rg.exe` inside a tmp script through the runner where `grep_search` cannot reach a folder (PR-0005). Spec `specs/_SPEC_AGENT_TERMINAL_ROBUSTNESS.md [AGENTTERMINAL-SP01]`

**SEOFIRST-PR-0001..0014: SEO-First Skill upgrade** [RESOLVED 2026-11-11]
- **History**: Added 2026-11-03 14:40 → Resolved 2026-11-11 (commits `9a2219c`, `ddb53e0`, `ba1b6f9`, `843e0c2`)
- **Summary**: 14 problems found and fixed during the SEO-first skill upgrade session (`_2026-11-03_SEOFirstSkill`): wrong Google Indexing API guidance (PR-0002), wrong DataForSEO MCP package name (PR-0003), outdated cost figures 20%-600% error (PR-0004), hardcoded local paths (PR-0005), untested providers and broken GSC MCP packages (PR-0006), missing free/first-party sources (PR-0007), fragmented trend sourcing (PR-0009), search-volume cost deviation $0.06 vs $0.09 (PR-0010), GSC API not enabled (PR-0011), table truncation (PR-0012), SPEC/IMPL reverse sync (PR-0013), ScrapeCreators skill files inaccurate (PR-0014), skill only retrieves data no SEO-first knowledge (PR-0001), and field-of-application scope (PR-0008)
- **Resolution**: All implemented, tested (52 PASS, 0 FAIL, 14 SKIPPED offline; live tests passed), committed and pushed

## Deferred

(none)

## Problems Changes

**[2026-11-11 20:50]**
- Added: PRMTHANGFIX-PR-0001, PR-0004, PR-0006, PR-0007 (synced from session `_2026-11-11_PromptSequenceHangPrevention`)
- Fixed: PRMTHANGFIX-PR-0002, PR-0003, PR-0005

**[2026-11-11 17:30]**
- Resolved: SEOFIRST-PR-0001..0014 (SEO-First Skill upgrade, all 14 session problems fixed, tested, committed and pushed)

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
