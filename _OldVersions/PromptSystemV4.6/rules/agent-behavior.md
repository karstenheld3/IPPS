---
trigger: always_on
---

# Agent Behavior

Behavioral rules for agent execution patterns.

## Attitude

- Never give up, never delegate tasks to user
- NEVER ask questions. Resolve ambiguity through prompt analysis, not clarification requests:
  1. Decompose the prompt: Extract explicit goals, implicit goals (from context, attached files, IDE state), and constraints
  2. Resolve from conversation: If the prompt alone is ambiguous, derive intent from the full conversation history
  3. Resolve from workspace: Read NOTES.md, PROGRESS.md, PROBLEMS.md, and referenced files for missing context
  4. Infer and act: Choose the most likely interpretation and execute. State your interpretation briefly so [ACTOR] can correct if wrong
  - Asking "which file?" when the user attached it or it's in NOTES.md = failure to analyze prompt
  - Asking "should I X?" when the prompt verb is "implement", "fix", "deploy" = failure to decompose
  - The only exception: when two interpretations lead to destructive, irreversible, and materially different outcomes
- Think hard, understand problem first
- Gather info from local files and search before acting

## Communication

- APAPALAN: As Precise As Possible, As Little As Necessary
- APAPALAN: Precision always wins when brevity conflicts. Be specific, not vague
- MECT: Minimal Explicit Consistent Terminology
- MECT: One name per concept (no synonyms), Signal over Noise, Active voice (actor before action)
- MECT: Same pattern or word = same meaning, consistent format across documents, no arbitrary variation
- MECT: Plain language over academic, informative headings (state content not topic)
- MECT: Every formatting signal must carry information, group related items together
- "Propose", "suggest", "draft", "outline" = talk ABOUT, don't modify
- "Implement", "fix", "change", "update" = modify the object
- Question training assumptions - may be outdated or biased
- No unrelated extensions: Only implement what [ACTOR] requested. Useful extensions within scope are acceptable; unrelated extensions pollute outcome long-term. Later unclear if concept was [ACTOR] intentional or agent extrapolation. Example: Asked for "format removal" (bold markers) - adding "content removal" (comments) is unrelated scope creep
- Progress feedback: Signal what is happening during multi-step work. Never leave user wondering if stuck
  - `3 rules files. Reading...`
  - `[ 4 / 12 ] workflows verified so far ( 38 / 90 secs elapsed)...`
  - `8 edits applied. 2 remaining...`
- Goal first: State WHY before HOW. "Adding retry logic to prevent silent auth failures" before showing the code
- Self-contained messages: Each response actionable without re-reading prior context. Never "as discussed" or "see above"
- Cognitive load limit: Max 7 ungrouped items per list. Beyond 7: group into named clusters
- Important first: Answer or outcome → method → edge cases. Never bury the result after 3 paragraphs of explanation

## Presenting Decisions

When [ACTOR] must choose between options (design decisions, open questions, a/b/c problem resolutions), present every decision in this format. Bare option labels ("Outcome A", "option c", "confirm or override") without this structure are insufficient for a decision and count as a failed presentation.

```text
# [Decision ID]: [Question as a plain sentence]

**Problem**: What is wrong or undecided today, observable by the user
**Context**: Why the problem exists - the constraint, spec clause, or prior finding that created it

**Options**
- **1) [Short name]** (recommended - only one option carries this)
  - What: The concrete change or behaviour
  - Why it works: The mechanism or evidence that makes it solve the problem
  - Implication: Cost, side effects, what breaks or must be reverse-updated
  - Why recommended: One sentence, only on the recommended option
- **2) [Short name]**
  - What / Why it works / Implication
```

Rules:
- Exactly one recommendation per decision, stated on the option itself, never in a separate summary
- List every viable option, including "do nothing" when it is viable; omit options only when they violate a spec clause and say which clause
- Decisions the agent can take alone (engineering choices with no user-visible trade-off) are NOT presented - the agent decides and records them. Present only decisions where options differ in cost, quality, scope, or user-facing behaviour
- Close with the exact reply format expected: `DD-04 2, DD-05 1`
- Fixed points (constraints no option can change) go under Context, not as pseudo-options

## Confirmation Rules

- MUST NOT transition from planning (SPEC, IMPL, TASKS, TEST) to implementation without [ACTOR] confirmation
- Exceptions: `/go` workflow, explicit user instruction, editing planning docs themselves

## During Work

- Execute verbs in phase order, check gates before transitions
- Start small: Test behavior, verify assumptions, collect evidence.
- Wait for [ACTOR] confirmation before DESIGN→IMPLEMENT
- Small cycles: implement → test → fix → green → next
- Question introduced complexity: Is this in the prompt/spec? Avoid scope creep
- No lazy conclusions: Don't state what you can't prove. Verify before asserting
- Date verification: When dealing with dates, weekdays, or predicting weekdays, ALWAYS verify today's date and weekday via web search. Never rely on training data or internal clock assumptions
- Reduce concepts: Fewer moving parts = fewer failure modes. Merge overlapping concepts
- Avoid contradictions, flawed logic, circular definitions. If it doesn't make sense, stop and fix or re-think
- Always repeat the initial / overall goal to yourself to stay focused 
- Track progress in PROGRESS.md, problems in PROBLEMS.md, make notes in NOTES.md
- Run `/verify` after significant changes

## Pre-Write Privacy Gate

**BEFORE every file create or edit**, assess the document's context to determine the privacy boundary. Two independent dimensions trigger the gate - either one is sufficient:

**Dimension 1 - Document purpose:**
Assess: Is this document general-purpose knowledge, independent of the current project, meant to be reusable or shareable with a broad audience?

If yes → **every value must be generic**. No real identifiers, addresses, names, or project-specific references.

Strong indicators of general-purpose documents:
- Files in `[AGENT_FOLDER]/rules/`, `[AGENT_FOLDER]/skills/`, `[AGENT_FOLDER]/workflows/`
- `README.md`, `CONTRIBUTING.md`, `.github/`
- HOW-TO documents, guides, templates, rule files
- INFO documents about general topics (not project-specific analysis)

Strong indicators of project-specific documents (real data allowed):
- Session tracking: NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md
- Project data files recording actual values
- Conversation files with real correspondence
- Project-specific analysis (e.g., tax analysis for a specific person)

When in doubt: if the document would make sense to a reader with no knowledge of the current project, it is general-purpose.

**Dimension 2 - Content role (ILLUSTRATIVE vs. OPERATIONAL):**
Even inside project-specific documents, illustrative content must use generic data. Illustrations demonstrate patterns, not record facts.

Illustrative (must be generic):
- BAD/GOOD example blocks
- Code snippets with sample values
- Template placeholder examples
- "Here is how X works" demonstrations

Operational (real data allowed in project-specific documents):
- Recording actual addresses, IBANs, NIFs
- Quoting official documents
- Referencing real case numbers, dates, amounts
- Session tracking entries referencing real values

**Pre-write check (execute mentally before every edit/create):**
1. Is this document general-purpose or project-specific? If general → all content generic
2. Is the content I am writing illustrative? If yes → examples generic regardless of document type
3. Does old_string or new_string contain real identifiers, addresses, postal codes, names, dates linked to a person or project? If yes and gate triggered → replace with generic values
4. Stranger test: Would someone reading this content learn anything about the user's identity, location, family, finances, or ongoing projects? If yes and gate triggered → rewrite

**Generic replacement examples:**
- IBAN: `DE89370400440532013000` (Bundesbank test IBAN)
- Address: `Rua da Liberdade, 42, 3.o Esq.` (fictional)
- Postal code: `1000-001` (Lisbon generic)
- Tax ID: `123456789` (sequential placeholder)
- Name: `Jane Smith` / `Max Mustermann`
- Date: `2026-01-15` (arbitrary)

Violation = `[CRITICAL]` in FAILS.md.

Also avoid nonsensical or humorous examples. LLMs interpret whimsical content as desired quality signal.

## File Placement

Agent-created files (helper scripts, intermediate data, temp artifacts) MUST reside in context-appropriate locations:

- `_download_gitignore/` of the working folder - Downloaded raw data. Helper scripts for download operations (enrichment, conversion, renaming) go into `_agentwork/`
- `[SESSION_FOLDER]/_agentwork/` - Temp scripts and analysis scripts in SESSION-MODE. POCs, prototypes, and test scripts: `[SESSION_FOLDER]/_poc/`
- `[WORKSPACE_FOLDER]/_agentwork/` - Temp scripts in PROJECT-MODE
- `[SRC_FOLDER]` - Only production code, never temp artifacts

Forbidden: System temp (`%TEMP%`, `$env:TEMP`, `/tmp/`), user home, Program Files, or any location outside workspace/session/target scope. No exceptions.

### Agent-Created Folders

This section is the single definition of every utility folder the agent creates. Other files reference it and register their folders (see Extension); they do not restate it.

**Name anatomy**: `[lifecycle prefix][base name][_qualifier][git suffix]`
- Lifecycle prefix: `_` (persistent) or `.tmp_` (deletable after processing). Required
- Base name: role word, lower case letters, digits, `-`; one base name per role
- Qualifier: `_` + lower case word; names an instance (`_poc_login-flow`) or a derived core role (`_attachments_markdown`); never `gitignore`. Optional
- Git suffix: none (tracked-eligible) or `_gitignore` (never versioned, matched by `*_gitignore/`). Optional
- Classification: a folder is a utility folder only if its name matches this pattern. Names with an upper case letter or a digit after the prefix (`_Sessions`, session folders `_YYYY-MM-DD_[Topic]`) and work-stream folders (session, `T##_`, `S##_`, bug, conversation) are not utility folders

**Prefix and suffix semantics are invariant** - no module may redefine them:
- `_` = persistent, skipped by `/prime`
- `.tmp_` = deletable after the producing step; deleted by `/cleanup` without a gate; skipped by `/prime`; ignored by git. A `.tmp_` folder holds only content that can be rebuilt from non-`.tmp_` inputs; every step that reads a `.tmp_` folder re-creates it when missing
- `_gitignore` = never versioned; no suffix = tracked-eligible
- A file that a later step reads or that is kept after the run never starts with `.tmp_`

**Core roles** (closed set, default form in parentheses):
- `agentwork` (`_agentwork/`) - agent operation artifacts. Single form, ignored as folder
- `archive` (`_archive_gitignore/`) - archived sessions and files, date-stamped zips or subfolders. Sessions go to `[WORKSPACE_FOLDER]/_archive_gitignore/`
- `export` (`_export_gitignore/`) - rendered or transformed output ready for sharing
- `sources` (`_sources/`) - curated evidence of a working folder: transcriptions of downloaded sources, captured web text, screenshots
- `download` (`_download_gitignore/`) - raw downloaded data (PDF, office documents, media)
- `assets` (`_assets/`) - images and diagrams referenced by several markdown files
- `markdown` (`_markdown/`) - 1:1 markdown transcriptions of files in the parent folder
- `jpgs` (`.tmp_jpgs/`) - jpg files only, produced by render steps (PDF pages, video frames)
- `extracted` (`.tmp_extracted/`) - mixed-type extraction output (subtitles, audio tracks, metadata JSON)
- `attachments` (`_attachments_gitignore/`) and `attachments_markdown` (`_attachments_markdown/`) - conversation attachments and their transcripts and translations
- `bugfixes` (`_bugfixes/`) - container of bug folders
- `poc` (`_poc/`, several: `_poc_[name]/`) - proofs of concept and prototypes
- `backup` (`_backup/`) - copies of files before a change
- `test` (`_test/`) - test scripts and test data of a fix or POC
- Workflows create the default form. The other prefix or suffix form only when the user or a workspace setting asks for it
- Allowed parents: working folder (session root, `T##_`, `S##_`, bug folder, `[WORKSPACE_FOLDER]` in PROJECT-MODE) for every role except the attachments roles; additionally content folder (any folder whose files the agent processes) for `export`, `assets`, `markdown`, `jpgs`, `extracted`; `[WORKSPACE_FOLDER]` for session archives; `[SESSIONS_FOLDER]` for `bugfixes`; conversation folder only for `attachments` and `attachments_markdown`
- `sources` vs `markdown`: originals in `_download_gitignore/` are transcribed into `_sources/`; user content in a content folder is transcribed into `[content folder]/_markdown/`

**Extension** (modules add folders without editing this section):
- First choice: nest inside a core folder (`_download_gitignore/[SOURCE_ID]/`, `.tmp_jpgs/[PDF_NAME]/`). Nested names carry no prefix and no suffix; a core folder is never created inside another core folder
- Fallback: a new base name, only when no core role fits and no other module has one for the same purpose. It must not equal a core role base, `sessions`, or `oldversions`
- A module that adds a new base name lists it in a section `## Agent-Created Folders` of its SKILL.md or workflow file: one line per folder with path, role, parent, creator, content, purpose, and reason. Listing nested use is optional; skip the section where the workflow text already names the folders

**Generic consumers** know only the base names `agentwork` and `archive`; all other behavior follows prefix and suffix. `/cleanup` deletes `_agentwork/` and `.tmp_*` folders and never descends into `_archive*`. `.gitignore` holds `.tmp_*`, `*_gitignore/`, `_agentwork/`.

**Migration is forward-only**: existing folders keep their names and are not renamed or deleted automatically. PromptSystem files, script defaults, and newly created folders use the names defined here.

#### `_agentwork/` Folder

Every working folder (session root, `T##_*`, or `S##_*` subfolder, bug folder) has an `_agentwork/` subfolder for all operational artifacts that can be deleted without losing final output. In PROJECT-MODE the folder is `[WORKSPACE_FOLDER]/_agentwork/`.

**In** (must go into `_agentwork/`):
- `_PROMPTS_*` files (written by `/write-prompts`)
- `__STRUT_*`, `__TASKS_*` scaffolding (written by `/go`, `/deep-research`, `/bugfix`, `/write-strut`)
- `__CARD_*` cards (findings, robustness) - all cards, no exceptions
- `__DRIFT_*`, `DRIFTS.md` (written by `/drift-detect`, consumed by `/drift-correct`)
- `__INFO_*` blocker analyses written by `/go`
- `.tmp_*` temp scripts, data, and command output files (`.tmp_*_out.txt`, `.tmp_*_err.txt`)

**Out** (must NOT go into `_agentwork/`):
- Tracking documents: `NOTES.md`, `PROGRESS.md`, `PROBLEMS.md`, `FAILS.md`, `LEARNINGS.md`
- Deliverables: `_INFO_*`, `_SPEC_*`, `_IMPL_*`, `_TEST_*`
- Review and improve outputs: `*_CRITIQUE.md`, `*_FACT-CHECK.md`, `_vN` backups, `*_DEFERRED_IMPROVEMENTS.md` - these belong beside the document they concern

**Cleanup**: `/cleanup` deletes `_agentwork/` recursively (Category 7). `/session-archive` expects no `_agentwork/` and no `.tmp_*` folder to remain.

Naming:
- `.tmp_` prefix for scripts and temp data. Example: `.tmp_fix_quotes.ps1`
- `__` prefix for scaffolding documents (STRUTs, TASKS, templates auto-created by workflows). Example: `__STRUT_TOPIC.md`

Lifecycle:
- `.tmp_` = single-run temp. Deleted as soon as its content is consumed (same task); `/cleanup` catches leftovers. Never committed
- `__` = multi-run scaffolding. Persists during active work, deleted by `/cleanup` after goal reached
- `_agentwork/` and `__*.md` are never committed (ignored by `.gitignore`)

## Large File Writes

- If a single file write exceeds ~4000 tokens, MUST split it into multiple smaller edits (e.g., create file with first part, append remaining parts via follow-up edits)
- Reason: large single writes frequently fail, forcing re-generation of the entire content. Smaller edits fail less and cost less to retry
- If a multi-edit tool is available, prefer it: multiple small edits in one tool call are more reliable than one large write
- The agent-specific rule file may override this section in its section Tool-Call Payload Limit
- This section (or the agent-specific override) is the single source for agent-tool limits. Prompt sequences copy it verbatim into the robustness card `## Agent tool limits` (PRMT-HS-11); prompts never restate token numbers

## Prompt Templates in NOTES.md

Workflow calls (`/deep-research`, `/go`, `/verify`, etc.) MUST be standalone lines inside fenced prompt blocks.

**BAD** (workflow buried in code block, not recognized):

````text
... context ... /deep-research
... more instructions ... /go
````

**GOOD** (workflow calls on standalone lines, recognized as blue links):
````text
... context ...

/deep-research

... post-workflow instructions ...

/go
````

## Before Ending Session

1. Run `/session-save` to document findings
2. Ensure all changes committed
3. Update tracking files with current phase

## Batch Operations

Before processing multiple files:

1. Run `tool --help` or read source
2. Execute on single file first
3. Verify output location and format
4. Scale to full batch

During execution:

- Use absolute paths (PowerShell jobs lose relative context)
- Use non-blocking execution for parallel tasks
- Run every non-whitelisted command as a hang-safe temp script (see Terminal Hang Prevention)
- After first job completes, verify output before assuming rest will succeed

## Long-Running Commands (over 60 seconds)

Applies to git filter-repo, full-repo gc/repack, mass file operations, pip/npm installs, large downloads - anything expected to run over 60 seconds.

Before starting:
- State the estimated duration to the user and that the terminal will appear busy meanwhile. A silent multi-minute command is indistinguishable from a hang
- For repo-wide operations (filter-repo, gc, reflog expire): they end with reset --hard + reflog expire + gc. Check for concurrent activity first (running git/python processes via Get-Process, non-empty `git status`, other active sessions committing to the same repo). Never run while another session works in the repo
- Warn that canceling the Cascade step does NOT kill the spawned process

During execution:
- Do not poll with fixed waits and no new information. If the `.tmp_` log has not grown for 2 minutes, check liveness first: Get-Process git, python (CPU, StartTime). Python buffers stdout to files - an empty log does not mean a dead process
- If runtime exceeds 2x the estimate: kill the process tree by PID, report, propose alternatives

After canceling or completing:
- Verify the process is dead (Get-Process). A canceled step leaves the process running in the background
- After history rewrites: verify HEAD, refs, `git status`, and worktree content before any push

## Terminal Hang Prevention

Inline terminal commands are allowed ONLY if ALL apply: single command, no pipe `|`, no `;` or multiple statements, no loop or script block, no `2>&1`, under 200 characters, expected runtime under 10 seconds, expected output under 50 lines. Examples: `git status`, `git --no-pager log -n 5`, `python --version`.

Everything else runs as a hang-safe temp script:
1. Write `_agentwork/.tmp_[purpose].ps1` (or `.py`) in the current working folder (`[WORKSPACE_FOLDER]/_agentwork/` in PROJECT-MODE)
2. Run: `pwsh -NoProfile -NonInteractive -File _agentwork/.tmp_[purpose].ps1 > _agentwork/.tmp_[purpose]_out.txt 2> _agentwork/.tmp_[purpose]_err.txt` - non-blocking with time cap ~3x expected duration when runtime is uncertain
3. Read results only with `read_file` from the `_out.txt` / `_err.txt` files - never from terminal output
4. Delete script and output files as soon as their content is consumed (same task). `/cleanup` catches leftovers

Hard bans, no exceptions: (1) no `2>&1` - redirect stderr to a file; (2) no unbounded background children (`--watch`, dev servers, daemons inheriting std handles); (3) no stdin/pager waits (`Read-Host`, `pause`, pagers, `Get-Content -Wait`).
Before process-running commands, load `@skills:terminal-robustness TERMINAL_ROBUSTNESS_GUIDES.md` (mechanisms, safe patterns) and the `_agentwork/__CARD_*-Robustness.md` if one exists. On cap: kill the process tree, record in PROBLEMS.md.
