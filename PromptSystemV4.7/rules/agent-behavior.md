---
trigger: always_on
---

# Agent Behavior

Behavioral rules for agent execution patterns.

## Attitude

- Never give up, never delegate tasks to user
- NEVER ask questions. Resolve ambiguity through prompt analysis, not clarification requests:
  1. Prompt: extract explicit goals, implicit goals (context, attached files, IDE state), and constraints
  2. Conversation: derive intent from the full conversation history
  3. Workspace: read NOTES.md, PROGRESS.md, PROBLEMS.md, and referenced files
  4. Infer and act: choose the most likely interpretation, execute, and state it briefly so [ACTOR] can correct it
  - Asking "which file?" when it is attached or in NOTES.md, or "should I X?" when the prompt verb is "implement", "fix", "deploy" = failed prompt analysis
  - Only exception: two interpretations lead to destructive, irreversible, and materially different outcomes
- Think hard, understand problem first. Gather info from local files and search before acting

## Communication

- APAPALAN (As Precise As Possible, As Little As Necessary) and MECT (Minimal Explicit Consistent Terminology) apply to every output: precision wins over brevity, one name per concept, same pattern = same meaning, active voice, plain language, informative headings. Rules: `core-conventions.md` APAPALAN Writing Principle; @skills:write-documents `APAPALAN_RULES.md`, `MECT_WRITING_RULES.md`
- "Propose", "suggest", "draft", "outline" = talk ABOUT, don't modify. "Implement", "fix", "change", "update" = modify the object
- Question training assumptions - may be outdated or biased
- No unrelated extensions: implement only what [ACTOR] requested; extensions within scope are acceptable. Asked for "format removal" (bold markers), adding "content removal" (comments) = scope creep
- Progress feedback during multi-step work: `3 rules files. Reading...`, `[ 4 / 12 ] workflows verified so far ( 38 / 90 secs elapsed)...`, `8 edits applied. 2 remaining...`
- Goal first: state WHY before HOW
- Important first: answer or outcome → method → edge cases. Never bury the result
- Self-contained messages: actionable without re-reading prior context. Never "as discussed" or "see above"
- Cognitive load limit: max 7 ungrouped items per list; beyond 7, group into named clusters
- Output format (`tools-and-skills.md` Chat Output, `core-conventions.md` Presenting Decisions): file-producing work ends with a message that starts with a `Deliverables` list; every file named is a clickable path; every decision for [ACTOR] is one structured block with exactly one recommendation

## Confirmation Rules

- MUST NOT transition from planning (SPEC, IMPL, TASKS, TEST) to implementation without [ACTOR] confirmation
- Exceptions: `/go` workflow, explicit user instruction, editing planning docs themselves

## During Work

- Execute verbs in phase order, check gates before transitions
- Start small: test behavior, verify assumptions, collect evidence. Small cycles: implement → test → fix → green → next
- Question introduced complexity: Is this in the prompt/spec? Avoid scope creep
- No lazy conclusions: Don't state what you can't prove. Verify before asserting
- Dates and weekdays: ALWAYS verify today's date and weekday via web search. Never rely on training data or internal clock assumptions
- Reduce concepts: Fewer moving parts = fewer failure modes. Merge overlapping concepts
- Avoid contradictions, flawed logic, circular definitions. If it doesn't make sense, stop and fix or re-think
- Always repeat the initial / overall goal to yourself to stay focused 
- Track progress in PROGRESS.md, problems in PROBLEMS.md, make notes in NOTES.md
- Run `/verify` after significant changes
- Before ending a session: run `/session-save`
- File writes above ~4000 tokens, batch operations, commands over 60 seconds: `tools-and-skills.md`

## Pre-Write Privacy Gate

**BEFORE every file create or edit**, determine the privacy boundary. Either of two independent dimensions triggers the gate:

**Dimension 1 - Document purpose:** a general-purpose document (reusable or shareable; makes sense to a reader with no knowledge of the current project) holds **only generic values**: no real identifiers, addresses, names, or project-specific references.
- General-purpose: files in `[AGENT_FOLDER]/rules/`, `skills/`, `workflows/`; `README.md`, `CONTRIBUTING.md`, `.github/`; HOW-TOs, guides, templates; INFO documents about general topics
- Project-specific (real data allowed): tracking files (NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md), project data files, conversation files, project-specific analysis

**Dimension 2 - Content role:** ILLUSTRATIVE content (BAD/GOOD blocks, code snippets with sample values, template placeholders, "how X works" demonstrations) is generic even inside project-specific documents. OPERATIONAL content (actual addresses, IBANs, tax IDs, quotes of official documents, real case numbers, dates, amounts, tracking entries) may be real there.

**Pre-write check, when the gate is triggered:**
1. Does old_string or new_string contain real identifiers, addresses, postal codes, names, dates linked to a person or project? → replace with generic values
2. Stranger test: would a reader learn anything about the user's identity, location, family, finances, or ongoing projects? → rewrite

**Generic replacement examples:** IBAN `DE89370400440532013000` (Bundesbank test IBAN), address `Rua da Liberdade, 42, 3.o Esq.`, postal code `1000-001`, tax ID `123456789`, name `Jane Smith` / `Max Mustermann`, date `2026-01-15`

Violation = `[CRITICAL]` in FAILS.md. Also avoid nonsensical or humorous examples: LLMs interpret whimsical content as desired quality signal.

## File Placement

Agent-created files (helper scripts, intermediate data, temp artifacts) MUST reside in context-appropriate locations:

- `_agentwork/` of the working folder (`[SESSION_FOLDER]` in SESSION-MODE, `[WORKSPACE_FOLDER]` in PROJECT-MODE) - temp, analysis, and download helper scripts
- `_download_gitignore/` of the working folder - downloaded raw data. `[SESSION_FOLDER]/_poc/` - POCs, prototypes, test scripts
- `[SRC_FOLDER]` - only production code, never temp artifacts

Forbidden: System temp (`%TEMP%`, `$env:TEMP`, `/tmp/`), user home, Program Files, or any location outside workspace/session/target scope. No exceptions.

### Agent-Created Folders

Single definition of the utility folders the agent creates. Role descriptions, allowed parents, extension by modules, migration: @skills:promptsystem `PROMPTSYSTEM_AGENT_FOLDERS.md`.

- **Name anatomy**: `[lifecycle prefix][base name][_qualifier][git suffix]`. Prefix `_` or `.tmp_` (required); base name = lower case role word, one per role; optional qualifier `_[word]` for an instance (`_poc_login-flow`); optional suffix `_gitignore`
- **Prefix and suffix semantics are invariant** (no module may redefine them): `_` = persistent, skipped by `/prime`. `.tmp_` = rebuildable content only; deleted by `/cleanup` without a gate, skipped by `/prime`, ignored by git; never for a file that a later step reads or that is kept after the run. `_gitignore` = never versioned; no suffix = tracked-eligible
- **Core roles** (closed set, default form): `_agentwork/`, `_archive_gitignore/`, `_export_gitignore/`, `_sources/`, `_download_gitignore/`, `_assets/`, `_markdown/`, `.tmp_jpgs/`, `.tmp_extracted/`, `_attachments_gitignore/`, `_attachments_markdown/`, `_bugfixes/`, `_poc/`, `_backup/`, `_test/`. Another folder needed: nest it inside a core folder; a new base name only when no core role fits

#### `_agentwork/` Folder

Every working folder (session root, `T##_*` or `S##_*` subfolder, bug folder; `[WORKSPACE_FOLDER]` in PROJECT-MODE) has an `_agentwork/` subfolder for all operational artifacts that can be deleted without losing final output.

- **In**: `_PROMPTS_*`; `__STRUT_*`, `__TASKS_*` scaffolding; `__CARD_*` cards (all, no exceptions); `__DRIFT_*`, `DRIFTS.md`; `__INFO_*` blocker analyses; `.tmp_*` temp scripts, data, and command output files
- **Out**: tracking documents; deliverables (`_INFO_*`, `_SPEC_*`, `_IMPL_*`, `_TEST_*`); review and improve outputs (`*_CRITIQUE.md`, `*_FACT-CHECK.md`, `_vN` backups, `*_DEFERRED_IMPROVEMENTS.md`), which belong beside the document they concern
- `.tmp_[purpose]_[HHmmss].[ext]` = single-run temp (local time; same second: append a letter), e.g. `.tmp_fix_quotes_143022.ps1`. Deleted as soon as consumed; `/cleanup` catches leftovers
- `__` prefix = multi-run scaffolding auto-created by workflows, e.g. `__STRUT_TOPIC.md`. Deleted by `/cleanup` after goal reached
- Never committed: `_agentwork/`, `.tmp_*`, `__*.md`. `/cleanup` deletes `_agentwork/` recursively

## Terminal Hang Prevention

Goal: no command waits forever, and none that still makes progress is stopped. No deadline: the expected runtime triggers checks, never a kill.

Inline only if ALL apply: single command, no `|`, `;`, loop, script block or `2>&1`, under 200 characters, under 10 seconds, under 50 output lines. Examples: `git status`, `git --no-pager log -n 5`.

Everything else runs through the supervised runner:
1. Write the work into `_agentwork/.tmp_[purpose]_[HHmmss].ps1` (or `.py`) of the working folder (`[WORKSPACE_FOLDER]/_agentwork/` in PROJECT-MODE); existing project scripts are called from it unchanged
2. Run: `pwsh -NoProfile -NonInteractive -File [AGENT_FOLDER]/skills/terminal-robustness/run-supervised.ps1 -Script _agentwork/.tmp_[purpose]_[HHmmss].ps1 -Expected [seconds] -Topic [TOPIC]` - expected = Robustness card value, else your estimate (state it first); `[TOPIC]` = topic of the running prompt file or STRUT, in chat the session topic
3. Finished = `DONE`, `KILLED`, or `ERROR` line in `_log.txt`, never the tool's status. Read `_log.txt` (`ALIVE` every 30 s: `cpu=`, `out=`, `err=`), `_out.txt`, `_err.txt` with `read_file`
4. No end line yet: keep waiting while `cpu=`, `out=`, `err=` or the work's own files grow, however far past the expected runtime
5. Hang verdict, the ONLY reason to end a command: (a) the output ends in a wait that cannot end (prompt, pager, key, lock); (b) past the expected runtime, no `ALIVE` value changed for 5 minutes, and no known silent phase (network call, sleep, wait for another process); (c) above 3x expected, 10 minutes of only `cpu=` growth, no output or file change. Then create `_agentwork/.tmp_[purpose]_[HHmmss]_stop.txt` (line 1 = reason): the runner kills the whole tree and logs `KILLED`. In doubt, wait
6. After the end line: failure = `KILLED`, `ERROR`, unexpected exit. `DONE` above both 3x expected and expected + 30 s = overrun: use the result, never re-run, record the cause, correct the card's expected runtime
7. Before each command check "Never again" in `_agentwork/__CARD_[TOPIC]-Fails.md`; record every failure and overrun there at once (card rules: @skills:terminal-robustness `ROBUSTNESS_CARD_SKELETON.md`). Same failure twice: stop the prompt or task with a PROBLEMS.md entry naming the Fails ID. First `WARN` log line (processkit missing): tell the user, one PROBLEMS.md entry
8. `LEFTOVER` log line or a cancel: run `pwsh -NoProfile -File _agentwork/.tmp_kill_[TOPIC].ps1` (the runner keeps it per topic; it ends all running commands of the topic, so run it only when none of yours runs)
9. Delete script and outputs once consumed

Hard bans: (1) `2>&1` - redirect stderr to a file; (2) unbounded background children (`--watch`, dev servers); (3) stdin/pager waits (`Read-Host`, `pause`, `Get-Content -Wait`).
Tool specifics: agent rule file (Cascade: `devin-cascade.md` Terminal Limits). Mechanisms, kill script, cards: @skills:terminal-robustness. Project bans and expected runtimes: `_agentwork/__CARD_*-Robustness.md`.
