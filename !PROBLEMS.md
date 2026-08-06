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

3. **Generic self-reflection using MNF**
   - How to add self-reflection to have better output consistency in the first generative run?
   - Examples: Markdown rules, used chars, Umlaute, LLM "literally translated English" mistakes and other frequent topics that we have to verify and improve later

4. **Question "agentic-English" and other rules**
   - Which rules are global?
   - How can they be tweaked or changed while the prompt library is running?
   - Where do they apply, how are exceptions or overwrites handled?

5. **How to implement GRUC for each document writing skill?**
   - More and better `_TEMPLATE.md` files - standardized output across documents, better drift-correction
   - More and better `_GUIDE.md` files - explain cognitive concepts, goals, processes and approaches to agent
   - More and better `_RULES.md` files - better low-level instruction following by explaining each rule with GOOD and BAD examples
   - More and better `_CHECKS.md` files - better output quality control after generation that is consistent with `_GUIDE.md` files

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

## Resolved

(none)

## Deferred

(none)

## Problems Changes

**[2026-08-03 16:31]**
- Added: DVSYS-FT-0001 (DevSystem V5.0 requirements - 5 areas)

**[2026-03-24 15:37]**
- Added: PREL-PR-0001 (project-release.md dual release convention support)
