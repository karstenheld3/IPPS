---
context_window_size: 200k
effort: high
prompt_system: IPPS
---

## Prompt 1 - Preflight: inventory and clean target

<!-- Records source counts in the findings card and resets the two deployment subtrees for a full rebuild. -->

```
Update Claude [ 01 / 07 ] - Preflight: inventory and clean target

Read `__CARD_UpdateClaude-Findings.md` in the repository root (create it in this prompt if missing) and `_PROMPTS_UpdateClaude.md` for sequence context. Treat earlier conversation as compacted. Step 1 of 7 of the Claude Code deployment. Working directory: repository root (the folder containing `PromptSystemV4.4\` and `NOTES.md`).

Objective: source inventory recorded and the deployment target reset so the migration prompts (2, 3, and 5) rebuild `.claude\` from a clean state.

Count with the find_by_name tool: markdown files in `PromptSystemV4.4\rules\` (expected 9), markdown files in `PromptSystemV4.4\workflows\` (expected 49), skill folders in `PromptSystemV4.4\skills\` (expected 24). Record the three actual counts and any deviation from the expected counts in `__CARD_UpdateClaude-Findings.md`. Delete `.claude\rules\` and `.claude\skills\` if they exist (full rebuild semantics).

Constraints:
- Do not modify anything under `PromptSystemV4.4\` - it is the read-only source of truth
- Do not delete any `.claude\` content other than the `rules\` and `skills\` subtrees (leave `settings.json` and any other content untouched)
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: Read-Host, pause, Get-Credential, Get-Content -Wait, 2>&1 with Blocking:true. File search and reads use agent tools (find_by_name, read_file, grep_search), not Get-ChildItem -Recurse or Select-String -Recurse. 1-minute cap per command. On cap: stop the process, record command and cap in PROBLEMS.md, continue.

Findings card: Load and update `__CARD_UpdateClaude-Findings.md`. Record the source inventory counts and deviations. Read at prompt startup for unresolved entries from prior prompts.

Verify: `__CARD_UpdateClaude-Findings.md` exists and lists actual counts for rules, workflows, and skills. Neither `.claude\rules\` nor `.claude\skills\` exists. Other `.claude\` content (if any) is unchanged.
```

---

## Prompt 2 - Migrate rules

<!-- Expected state: counts recorded, target subtrees absent. Deploys 8 of 9 rule files unchanged. -->

```
Update Claude [ 02 / 07 ] - Migrate rules

Read `__CARD_UpdateClaude-Findings.md` and confirm the rule inventory count is recorded (prior-step verification). Treat earlier conversation as compacted. Step 2 of 7. Authority: `_PROMPTS_UpdateClaude.md` Prompt 2 design (source: CLAUDEIPPS-IN02 section 3.1).

Objective: `.claude\rules\` contains exact copies of every agent-agnostic rule file from `PromptSystemV4.4\rules\`; `devin.md` is not deployed.

Copy each rule file from `PromptSystemV4.4\rules\` to `.claude\rules\` except `devin.md` (Devin/Cascade-specific tool constraints, meaningless for Claude Code). No content transform - the deployed rules are agent-agnostic by design and the `[AGENT_FOLDER]` placeholder resolves per agent.

Constraints:
- Do not modify the source files
- Do not deploy `devin.md`
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost (overwrite, never append)
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: Read-Host, pause, Get-Credential, Get-Content -Wait, 2>&1 with Blocking:true. File operations use agent tools. 1-minute cap per command. On cap: stop the process, record command and cap in PROBLEMS.md, continue.

Findings card: Load and update `__CARD_UpdateClaude-Findings.md`. File glitches and unexpected findings. Read at prompt startup for unresolved entries from prior prompts.

Verify: `.claude\rules\` contains 8 files (rule inventory count minus 1). Get-FileHash of each deployed file matches its source file. No `devin.md` in `.claude\rules\`.
```

---

## Prompt 3 - Migrate workflows

<!-- Expected state: 8 rule files deployed. Creates 49 user-only workflow skills with the frontmatter transform and both collision renames. -->

````
Update Claude [ 03 / 07 ] - Migrate workflows

Read `__CARD_UpdateClaude-Findings.md` and confirm `.claude\rules\` holds 8 files (prior-step verification). Treat earlier conversation as compacted. Step 3 of 7. Authority: `_PROMPTS_UpdateClaude.md` Prompt 3 design (source: CLAUDEIPPS-IN02 sections 3.2 and 4).

Objective: every workflow from `PromptSystemV4.4\workflows\` is deployed as a user-invocable skill `.claude\skills\<name>\SKILL.md` with transformed frontmatter, the workflow body unchanged, and both collision renames applied.

Per workflow file: create `.claude\skills\<name>\SKILL.md` containing the transformed frontmatter followed by the original workflow body. Transform: keep `description`; add `name` (the deployed folder name) and `disable-model-invocation: true`; drop `auto_execution_mode`.

Example - `cleanup.md` deploys as:
```yaml
---
name: cleanup
description: Delete temporary files and artifacts left by workflows and skills
disable-model-invocation: true
---
```

Renames (bundled-skill collisions): `verify.md` deploys to `.claude\skills\ipps-verify\` because the bundled Claude Code `/verify` skill writes its recipes to `.claude/skills/verify/`, which would clobber an IPPS copy. `deep-research.md` deploys to `.claude\skills\deep-research-run\` because the `deep-research` folder is reserved for the domain skill deployed in step 5. The `name` field matches the renamed folder (`ipps-verify`, `deep-research-run`).

Constraints:
- Do not modify workflow sources
- Do not change workflow body content - frontmatter transform only
- Do not create a `.claude\commands\` folder (skills are the recommended format; commands are legacy)
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost (folders overwritten)
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: Read-Host, pause, Get-Credential, Get-Content -Wait, 2>&1 with Blocking:true. File operations use agent tools. 1-minute cap per command. On cap: stop the process, record command and cap in PROBLEMS.md, continue.

Findings card: Load and update `__CARD_UpdateClaude-Findings.md`. File glitches and unexpected findings. Read at prompt startup for unresolved entries from prior prompts.

Verify: workflow-derived folder count equals the workflow inventory count from `__CARD_UpdateClaude-Findings.md` (expected 49). `.claude\skills\ipps-verify\` and `.claude\skills\deep-research-run\` exist; `.claude\skills\verify\` does not. A grep_search for `auto_execution_mode` in `.claude\skills\` returns zero matches. Every workflow-derived SKILL.md contains `disable-model-invocation: true`.
````

---

## Verification Checkpoint 1

<!-- Rules and workflow skills deployed; verify state before the skills migration. -->

```
Update Claude [ 04 / 07 ] - Verification checkpoint 1: rules and workflow skills

Read `__CARD_UpdateClaude-Findings.md`. Treat earlier conversation as compacted. Verification checkpoint after prompts 1-3.

/verify

current `.claude\` deployment state (rules and workflow skills) against the Verify criteria of prompts 1-3 in `_PROMPTS_UpdateClaude.md`.

/fix

all gaps and remaining work found.
```

---

## Prompt 5 - Migrate skills

<!-- Workflow skills verified. Deploys 24 skill folders with the invocation classification. -->

```
Update Claude [ 05 / 07 ] - Migrate skills

Read `__CARD_UpdateClaude-Findings.md` and confirm the workflow-derived skill folders exist in `.claude\skills\` (prior-step verification). Treat earlier conversation as compacted. Step 5 of 7. Authority: `_PROMPTS_UpdateClaude.md` Prompt 5 design (source: CLAUDEIPPS-IN02 sections 3.3 and 5).

Objective: every skill from `PromptSystemV4.4\skills\` is deployed to `.claude\skills\<name>\` with all supporting files and the invocation classification frontmatter applied.

Copy each skill folder from `PromptSystemV4.4\skills\` to `.claude\skills\<name>\` including supporting files (progressive disclosure). Keep existing `name` and `description` frontmatter. Add `disable-model-invocation: true` to the 15 user-only skills; the 9 model-triggered skills stay without it. 6 source skills have no frontmatter at all (5 user-only: travel-info, windows-desktop-control, llm-computer-use, llm-evaluation, llm-transcription; 1 model-triggered: drift-control) - prepend frontmatter to their deployed copies only (name = folder name, description derived from the file's intro line); do not modify the sources.

Model-triggered (9): write-documents, session-management, coding-conventions, deep-research, workspace-management, drift-control, edird-phase-planning, git-conventions, ms-playwright-mcp

User-only (15): travel-info, youtube-downloader, seo-tools, google-account, image-tools, pdf-tools, windows-desktop-control, playwriter-mcp, llm-computer-use, llm-evaluation, llm-transcription, github, git, hosting, devin-auto-model-switcher

Constraints:
- Do not modify skill sources
- Do not rename the `deep-research` skill folder - the workflow-derived `deep-research-run` from step 3 is separate and both coexist
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost (folders overwritten)
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: Read-Host, pause, Get-Credential, Get-Content -Wait, 2>&1 with Blocking:true. File operations use agent tools. 1-minute cap per command. On cap: stop the process, record command and cap in PROBLEMS.md, continue.

Findings card: Load and update `__CARD_UpdateClaude-Findings.md`. File glitches and unexpected findings. Read at prompt startup for unresolved entries from prior prompts.

Verify: deployed skill folder count equals the skill inventory count from `__CARD_UpdateClaude-Findings.md` (expected 24); total `.claude\skills\` folder count equals the card's workflow plus skill counts (expected 73). Each of the 15 user-only SKILL.md files contains `disable-model-invocation: true`; none of the 9 model-triggered SKILL.md files does. Every deployed SKILL.md has valid frontmatter with `name` (matching the folder) and `description` (compare line-by-line, not with `$`-anchored regex - CRLF files break it).
```

---

## Verification Checkpoint 2

<!-- Full deployment in place; verifies complete state including skills before finalization. -->

```
Update Claude [ 06 / 07 ] - Verification checkpoint 2: full deployment state

Read `__CARD_UpdateClaude-Findings.md`. Treat earlier conversation as compacted. Verification checkpoint after prompts 1-5.

/verify

current `.claude\` deployment state (rules, workflow skills, and domain skills) against the Verify criteria of prompts 1-5 in `_PROMPTS_UpdateClaude.md`.

/fix

all gaps and remaining work found.
```

---

## Prompt 7 - Finalize: mechanism note, commit, report

<!-- Deployment verified. Updates the NOTES.md mechanism line, commits, and reports with live-reload guidance. -->

```
Update Claude [ 07 / 07 ] - Finalize: mechanism note, commit, report

Read `__CARD_UpdateClaude-Findings.md` and `NOTES.md` in the repository root. Treat earlier conversation as compacted. Step 7 of 7. Authority: `_PROMPTS_UpdateClaude.md` Prompt 7 design (source: CLAUDEIPPS-IN02 sections 1 and 7).

Objective: the deployment mechanism in NOTES.md references this prompts file, the deployment is committed, and the completion report includes live-reload guidance.

Update the deployment mechanism section in `NOTES.md`: replace the line stating that workflows are also copied to `.claude/commands/` with a line stating that `.claude/` (rules and skills) is regenerated by running the prompts in `_PROMPTS_UpdateClaude.md` (idempotent full rebuild; `.devin/` continues via robocopy /MIR). Then commit the deployment:

/commit

the `.claude\` rules and skills deployment, the NOTES.md mechanism update, and `_PROMPTS_UpdateClaude.md`

Report to the user: deployed counts (rules, skills), the two renames (`ipps-verify`, `deep-research-run`), and that already-running Claude Code sessions pick up regenerated skills only after a restart or `/reload-skills`.

Constraints:
- Do not modify anything under `PromptSystemV4.4\`
- Do not commit `__CARD_UpdateClaude-Findings.md` (runtime scaffolding, removed later by `/cleanup`)
- Do not change NOTES.md beyond the mechanism line
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost
- Hang safety: git commands use --no-pager and commits use -m (no editor). 30-second cap per git command. On cap: stop the process, record command and cap in PROBLEMS.md, continue.

Findings card: final update - record completion state and any unresolved entries.

Verify: `git --no-pager status --short` shows no unstaged changes except `__CARD_UpdateClaude-Findings.md`. NOTES.md contains the `_PROMPTS_UpdateClaude.md` mechanism reference and no `.claude/commands/` line. The latest commit contains `.claude/rules/` and `.claude/skills/`.
```
