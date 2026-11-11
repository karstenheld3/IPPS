# Prompts Robustness Guide

Read BEFORE writing `_PROMPTS_[NN]-[Topic].md` files. Pairs with `PROMPTS_GUIDES.md` and `PROMPTS_RULES.md` (PRMT-HS-* and PRMT-RB-* rules). Mechanism depth, safe command patterns, and robustness card templates live in @skills:terminal-robustness; this guide carries the prompt-integration layer (clause, findings card, verification depth).

## 1. Why Robustness Matters

Prompt sequences run unattended across multiple turns. Each prompt depends on the state left by prior prompts. A single failure — a hung command, a skipped prerequisite, an unrecorded glitch — propagates through every later prompt. The execution engine cannot skip a failed prompt; it either hangs, produces broken output, or silently proceeds with corrupted state.

Robustness has five pillars:

1. **Hang-prevention**: no command blocks the sequence indefinitely (terminal robustness: what runs in the terminal)
2. **Agent tool limits**: no tool call stalls on payload size (agent-tool robustness: what runs via agent tools; Section 2a)
3. **Fails card**: every failure and hang is recorded at once and checked before each later command, so no prompt repeats it (Section 2b)
4. **Findings-card mechanism**: content glitches and working solutions are recorded in a findings card between prompts so later prompts can learn from earlier ones
5. **Verification depth**: verification sections catch real defects, not just "tests pass"

A well-structured prompt sequence with precise objectives, clean state flow, and verified idempotency is worthless if the agent issues a single hanging command in prompt 3 of 5, or if a test regression from prompt 2 survives until prompt 5 because nobody recorded it.

**Sources**: Harness rewrite session (2026-09-07), 5 prompt files, 25+ prompts. One hang failure (pipe deadlock) stopped the entire sequence. A dedicated findings card recorded 16 issues across 5 prompts, enabling later prompts to avoid repeating mistakes.

## 2. The Hang-Safety Clause

Every implementation prompt (any prompt that runs commands) MUST include a hang-safety clause in the Constraints section. The clause is one line that points to the two sources; it never restates them. Generic rules (whitelist, supervised runner, monitoring, hang verdict, hard bans) live in `agent-behavior.md` Terminal Hang Prevention; project bans and expected runtimes live in the robustness card. No command gets a time limit: a command that shows progress runs to its end, and the agent ends a command only on a hang verdict. The prompt carries no limit and no kill text.

### Clause Template

```
Hang safety: commands per `agent-behavior.md` Terminal Hang Prevention (supervised runner); bans and expected runtimes per `_agentwork/__CARD_[TOPIC]-Robustness.md`.
```

### Where to Place the Clause

The hang-safety clause goes in the Constraints section of each implementation prompt, after domain-specific constraints and before the idempotency constraint. It is a negative constraint (PRMT-CT-02): it states what the agent must NOT do.

### When to Include the Clause

- **Implementation prompts** (modify files, run tests, execute builds): ALWAYS include
- **Research/analysis prompts** (read files, write findings): include if the prompt runs any commands beyond file reads
- **Pure generation prompts** (write a document from scratch, no command execution): exempt, but include if the prompt might trigger commands indirectly (e.g., `/verify` workflow call)

## 2a. Agent Tool Limits (PRMT-HS-11)

Agent tools (file write, edit, multi-edit) stall or drop calls whose arguments exceed the agent's payload limit. The writing agent is assumed to be the executing agent.

- Single source: the writing agent's agent-specific rule file, section Tool-Call Payload Limit; if absent, `tools-and-skills.md` Large File Writes
- Copy that section verbatim into the robustness card `## Agent tool limits` when creating or refreshing the card
- Every prompt that writes or edits files adds the constraint: `Agent tool limits: see _agentwork/__CARD_[TOPIC]-Robustness.md section "Agent tool limits"; one section per tool call`
- Prompts never restate a token number

**Cascade site ban**: prompts that may touch German law add to Constraints: `gesetze-im-internet.de: Playwright only, no search_web / read_url_content (crashes conversation).`

## 2b. Runtime Check and Fails Card

Every implementation prompt carries exactly one runtime-check line next to the hang-safety clause. It also loads and uses the Fails card (`_agentwork/__CARD_[TOPIC]-Fails.md`, structure and rules: @skills:terminal-robustness `ROBUSTNESS_CARD_SKELETON.md`), the failure memory of the working folder: `/write-prompts` reuses it or creates it; chat tasks in the same folder use the same card:

```
Runtime check: before each command state the expected seconds and check the "Never again" list in `_agentwork/__CARD_[TOPIC]-Fails.md`; while it runs read the `ALIVE` lines in the runner log and end it only on a hang verdict, never for its runtime; after it compare with `elapsed=`; on KILLED, ERROR, unexpected exit, or elapsed above both 3x expected and expected + 30 s, write a Fails card entry at once, fix the root cause, continue (a finished slow command is never re-run); same failure twice in this prompt: stop with a PROBLEMS.md entry naming the Fails entry ID.
```

Why one line instead of a protocol block: prompt bullets lose focus under workflow load (observed: clause ignored as bullet 5 of 7); the runner writes `ALIVE` lines and `elapsed=` itself, so the agent reads the liveness values while waiting and compares one number at the end.

Fails card vs findings card vs PROBLEMS.md:
- **Fails card**: every command failure and hang (classes: card skeleton); read before every command
- **Findings card**: content glitches (spec-code mismatches, test drift, naming); no hangs
- **PROBLEMS.md**: prompts stopped by a repeated failure (entry names the Fails entry ID), and deferred problems

The final checkpoint prompt of each prompts file promotes "Never again" lines to the robustness card banned list (PRMT-SQ-04).

## 3. The Findings-Card Directive

Every prompt sequence that risks encountering problems MUST designate a findings card — a card file loaded and updated by every prompt that needs it. The card records glitches, spec-code mismatches, and unexpected findings between prompts. This is the findings-card directive.

### 3.1 Why a Findings Card Matters

Without a findings card:
- Glitches fixed in-prompt are invisible to later prompts — the same mistake repeats
- Test regressions survive multiple prompts because nobody recorded the mismatch
- Spec-code inconsistencies accumulate silently until a late prompt discovers them all at once
- The ex-post analysis is impossible — there is no record of what went wrong and how it was fixed

With a findings card:
- Each prompt records glitches it encounters and how it fixed them
- Later prompts load the findings card at startup and avoid repeating the same mistakes
- The final prompt has a complete record for ex-post analysis
- The agent builds institutional memory within the sequence

### 3.2 The Findings-Card Directive

Each prompt includes a `Findings card:` directive in the prompt body, after the hang-safety clause and before the closing protocol:

```
Findings card: Load and update `__CARD_[TOPIC]-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts.
```

The directive tells the agent which card to load and update. The card is shared across all prompts in the sequence. Every prompt loads it at startup and appends to it at end-of-prompt; no prompt creates a new findings card.

### 3.3 The Findings Card Format

The findings card follows a structured format. Each entry records one glitch:

```
### [N]. [Glitch Title]

**Severity**: HIGH | MEDIUM | LOW

**Expected state** (from prompt [step ID], line [N]): "[what the prompt expected]"

**Actual state**: "[what actually happened]"

**Root cause**: "[why it happened]"

**Resolution**: "[how it was fixed]" or "[not fixed — see PROBLEMS.md entry]"

**Prevention**: "[how to prevent this in future prompts]"
```

### 3.4 What to File

File every glitch, not just blockers. The findings card is separate from session PROBLEMS.md:
- **Test failures** that required code changes to fix (record the test file and the mismatch)
- **Spec-code mismatches** where the spec said one thing and the code did another
- **Naming convention violations** caught by `tsc` or lint
- **STRUT sequencing violations** where a step was executed out of order
- **Test expectation drift** where a test was written before the implementation and needed updating
- **Unexpected findings** that are not defects but affect later prompts (e.g., a file is larger than expected, a dependency is missing)

### 3.5 Findings Card vs Session PROBLEMS.md

The findings card and session PROBLEMS.md serve different purposes:

- **Findings card** (`__CARD_[TOPIC]-Findings.md`): Captures ALL glitches (including those fixed in-prompt), root causes, resolutions, prevention notes. Loaded and updated by every prompt. This is a card, not a session file.
- **Session PROBLEMS.md**: Records problems encountered during prompt execution that must be approached later — blockers that stopped a prompt, deferred issues that could not be fixed in-prompt, timeouts that require investigation. PROBLEMS.md is for problems needing later attention, not detailed glitch logs.

### 3.6 How Later Prompts Use the Findings Card

Each prompt loads the findings card at startup, after reading the session cards. The agent checks:

1. Are there unresolved glitches from prior prompts that affect this prompt's work?
2. Are there prevention notes that apply to this prompt's commands or verifications?
3. Are there naming conventions or test patterns that this prompt must follow?

The read is lightweight — scan titles and prevention notes, not full entries. Full entries are read only when a title matches the current prompt's scope.

### 3.7 Integration with the Card System

When a prompt sequence uses a card system (compact context documents read at the start of each prompt), the findings card is one of the cards loaded at startup:

**Card 00 Section 3 (resume detection)** already reads PROGRESS.md to check if a step is done. Add a step: load the findings card for unresolved entries from prior prompts.

**Card 00 Section 4 (end-of-prompt protocol)** already commits and records blockers in PROBLEMS.md. Add a step: file glitches and findings in the findings card before the commit. PROBLEMS.md records blockers that stopped the prompt; the findings card captures everything notable that happened.

The card system reference:

```
## 3. Start-of-prompt protocol (resume detection)

1. Verify the Session Anchor: confirm the `Session:` and `Working folder:` paths in this prompt match the current working directory. If they do not match, navigate to the declared working folder before proceeding (PRMT-SC-08)
2. Read this card and the cards the prompt names
3. Read session PROGRESS.md "Done" section. If the prompt's STRUT step ID is already listed as done: verify its artifacts exist, report "step already done", and stop. If the step is not listed as done, verify that artifacts from the prior step exist on disk before starting new work. Checkbox state alone is insufficient — deleted or missing artifacts mean the step must be redone.
4. Read the STRUT step line and unit block; read the clause-map rows
5. Load `__CARD_[TOPIC]-Findings.md` for unresolved entries and the "Never again" list of `__CARD_[TOPIC]-Fails.md`
6. Run git status --short in both repos; uncommitted work from a previous, interrupted prompt is finished or reverted before new work starts
7. This prompt has execution authority (PRMT-EX-03). Do not ask for confirmation before executing. Execute within the Constraints section boundaries.

## 4. End-of-prompt protocol

1. Verification named in the prompt passed
2. File glitches and findings in `__CARD_[TOPIC]-Findings.md`
3. Mark the STRUT step [ ] -> [x] in __STRUT_[TOPIC].md
4. Append one line to session PROGRESS.md "Done"
5. Record blockers in session PROBLEMS.md
6. Commit both repos where changed
```

### 3.8 Findings-Card Directive Examples

**Minimal** (simple sequence, no build tools):
```
Findings card: Load and update `__CARD_[TOPIC]-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts.
```

**Full** (complex sequence with cards):
```
Findings card: Load and update `__CARD_[TOPIC]-Findings.md`. File every test failure that required a code fix, every spec-code mismatch, every naming convention violation, and every STRUT sequencing issue. Read the card at prompt startup for unresolved entries from prior prompts.
```

## 4. Command-Specific Hang Risks

Before using @skills:terminal-robustness content, determine the executing agent and load the matching variant subfolder (see SKILL.md Agent Dispatch): `ClaudeCode/` (minimum - generic patterns, no tool-internals claims) or `DevinCascade/` (full empirical findings, tested patterns). The variant's `ROBUSTNESS_CARD_TEMPLATE.md` is the copy source for the project card; the variant guide carries the agent-specific execution patterns.

Banned lists, mechanisms, and per-tool behavior are maintained in the skill (agent variants as above). Build the project banned list into the robustness card (that skill's guide, Section 4.3), then reference the card from the hang-safety clause - do not inline command-by-command risk lists into prompts.

## 5. Safe Command Patterns

Safe command patterns (non-blocking execution with monitoring, process cleanup, git flags, non-interactive builds, stderr redirection, ripgrep usage) are maintained in @skills:terminal-robustness `TERMINAL_ROBUSTNESS_GUIDES.md` and the agent card templates. Reference them from the robustness card; prompts never repeat the full pattern text.

### 5.1 Agent Tools Over Shell Commands for File Operations

Prompts must direct the agent to use built-in tools (grep_search, read_file, find_by_name, code_search) for file search, read, and list operations (PRMT-CT-12). Shell commands for file operations are a hang source and bypass the agent's file access layer.

**Why this is a robustness concern**: Shell commands like `Get-ChildItem -Recurse`, `Select-String -Recurse`, and `Get-Content` were primary hang sources in a Lana-V2-Dev session. `Get-ChildItem -Recurse` on large trees enumerates every file before returning. `Select-String -Recurse` has the same problem. `Get-Content -Wait` streams indefinitely. Agent built-in tools are non-hanging by design.

**Rule**: Shell commands (Select-String, Get-ChildItem, Get-Content, cat, grep, find, rg.exe) must not appear in prompt bodies for file exploration or reading. Verify sections use `grep_search` for residual sweeps too; only when `grep_search` cannot reach the folder (outside the workspace), `rg.exe` runs inside a tmp script through the supervised runner, never inline.

**Prompt body — use agent tool directives**:
```
Search for 'validateToken' in src/ using the grep_search tool.
Read `src/auth/validator.ts`.
Find all .ts files in src/ using the find_by_name tool.
```

**Verify section — residual sweep with the agent tool**:
```
Verify: grep_search for 'guard_request' in src/ returns zero matches.
```

## 6. Expected Runtimes and Hang Verdict

### 6.1 Expected Runtimes

Every command that runs a process gets an expected runtime, not a limit. Starting values per command type live in the agent robustness card templates (@skills:terminal-robustness); the project card carries the measured values and notes known silent phases.

**Why no time limit**: a limit ends work that would have finished. A test suite that needs 9 minutes under an 8-minute limit is ended at minute 8 and run again: 17 minutes instead of 9, and the same can happen again. The expected runtime only tells the agent when to start reading the liveness signals.

### 6.2 Hang Verdict

The supervised runner has no deadline. It logs `ALIVE` lines (CPU time, output size); the agent ends a command only when the evidence shows a hang (`agent-behavior.md` Terminal Hang Prevention step 5) by creating the stop file, and the runner then kills the whole process tree and writes `KILLED`. The runtime-check line (Section 2b) records the failure in the Fails card and stops the prompt on a repeat. Prompts carry no separate hang or kill text.

### 6.3 Per-Test Timeouts

Tests that spawn processes must set explicit per-test timeouts and kill their process tree in `afterEach`:

```
New tests that spawn processes set an explicit per-test timeout and kill their process tree in afterEach. A spawning test without both is a defect to fix in the same prompt.
```

### 6.4 Targeted Test Scope

Verification sections must run specific test files, not the full test suite, during implementation steps (PRMT-HS-09). Full test suite runs are reserved for final verification steps only.

**Why targeted scope matters**: A Lana-V2-Dev session documented the full `bun test` suite hanging indefinitely, while targeted test files completed in seconds. The full suite includes long-running integration tests, timing-dependent tests, and process-spawning tests that may not terminate cleanly. Another session documented a flaky test that failed in the full suite but passed in isolation due to timing pressure from other tests in the same run.

**Implementation prompts — run specific test files**:
```
Verify: Run `bun test tests/unit/auth.test.ts tests/unit/token_validator.test.ts`. All tests pass.
```

**Final verification — full suite acceptable**:
```
Verify: Run `bun test --timeout 20000` (per-test timeout; expected runtime of the full suite from the robustness card). All tests pass.
```

**Rule**: Bare `bun test` or `npm test` (full suite) in implementation prompt verification is a PRMT-HS-09 violation. Always scope to specific test files during implementation. Full suite only in the final verification step of a sequence.

## 7. Verification Gap Prevention

Beyond hangs and problem filing, verification gaps silently pass as "done." Include these in prompt verification sections to prevent false "done" claims:

### 7.1 Test Coverage Depth

Do not accept "tests pass" when the prompt required specific test scenarios. Verify that the specific scenarios exist, not just that the suite is green:

```
Verify: tests/integration/harness.test.ts contains test cases for [specific scenario A], [specific scenario B]. All tests pass.
```

### 7.2 Spec-Code Consistency

When a prompt amends specs and implements code, verify both directions:

```
Verify: spec FR-03 text matches code implementation. Run `bun tsc --noEmit` — no type errors.
```

### 7.3 Residual Sweeps

When a prompt removes concepts (old protocol, old naming), include a residual sweep:

```
Verify: grep_search for 'old_term' returns zero matches in src/ and outside Document History in specs.
```

### 7.4 Naming Convention Checks

When a prompt introduces new naming conventions, verify consistency:

```
Verify: no camelCase variants of [snake_case_field] exist in src/. Run `bun tsc --noEmit` — no type errors.
```

### 7.5 Prior-Step Confirmation

When a prompt depends on a prior step, verify the prior step is done:

```
Verify: Confirm STRUT step [prior step ID] is `[x]` in [STRUT filename].
```

### 7.6 Interleaved Verification Prompts as Drift Prevention

Insert a verification prompt after every checkpoint interval (Items 8: 3 implementation prompts, Items 6: 2, Items 5 or less: 1) plus a final checkpoint per file (PRMT-SQ-04, `PROMPTS_GUIDES.md` Section 3a). These are verification-only prompts that run `/verify` against the planning document and `/fix` to address gaps — not implementation prompts with verification sections.

**Why this is a robustness concern**: Without interleaved checkpoints, spec-code drift accumulates silently. An observed security remediation sequence had 5 sub-chains where drift was only caught at the end, requiring rework across the full sequence. Interleaved verification limits blast radius to one checkpoint interval.

**Verification prompt template**:
```
[NN]-[Topic] [ NN / NN ] - Verification Checkpoint [N]

Session: `[SESSION_FOLDER]`
Working folder: `[WORKING_FOLDER]`

Read `__CARD_00-Rules.md` and `__STRUT_[Topic].md`. Treat earlier conversation as compacted. Verification checkpoint after prompts [N]-[M].

/verify

current state against `__STRUT_[Topic].md` for prompts executed so far.

/fix

all gaps and remaining work.
```

**Key properties**:
- Prompt Marker (PRMT-FT-10), Session Anchor (PRMT-SC-08), self-contained opening reads rules card and planning document (PRMT-SC-01)
- `/verify` and `/fix` are standalone workflow calls (PRMT-CT-08)
- No implementation content — no code, tests, or builds
- Does NOT count toward the 10 implementation prompts per file (PRMT-SC-04)
- Heading: `## Verification Checkpoint N` (not `## Prompt N`)

## 8. Project-Specific Banned Lists

The banned list lives in the project robustness card, not in the prompt. `/write-prompts` Step 1 creates or loads the card via @skills:terminal-robustness (copy the agent's `ROBUSTNESS_CARD_TEMPLATE.md`, extend with project entries, follow the card's build procedure). The hang-safety clause references the card by filename; prompts never inline the full list.

## 9. Lessons from a Harness Rewrite Session

A harness rewrite session (2026-09-07) used 5 prompt files with 25+ prompts. One hang failure and several verification gaps occurred despite the hang-safety system. A dedicated findings card recorded 16 issues across 5 prompts.

### 9.1 The `2>&1` Hang (Pipe Deadlock)

**What**: `bun test --timeout 20000 tests/unit/prompt_assemble.test.ts 2>&1` with `Blocking: true` caused an indefinite hang. The same command without `2>&1` completed in 182ms.

**Root cause**: confirmed empirically - the pwsh merge-point mechanism (backpressure hang or OutOfMemoryException with corrupted exit code). Mechanism and evidence: @skills:terminal-robustness `DevinCascade/TERMINAL_ROBUSTNESS_GUIDES.md`.

**Prevention**: The banned list must include `2>&1` with `Blocking: true`. For capturing stderr, redirect to a file.

### 9.2 STRUT Sequencing Violation

**What**: P3-S4 (spec amendments) was skipped, P3-S5 (implementation) was executed without spec backing. The STRUT showed P3-S4 as `[ ]` and P3-S5 as `[x]`.

**Root cause**: The prompt sequence did not enforce a gate between P3-S4 and P3-S5. The agent proceeded to implementation without the spec prerequisite.

**Prevention**: Prompts that depend on prior steps must verify the prior step is done. Include in the Verify section: "Confirm STRUT step [prior step ID] is `[x]` in [STRUT filename]."

### 9.3 Test Regression Survived 3 Prompts

**What**: P3-S3 changed prompt text in source code. The corresponding test was not updated. The failure was not caught until P3-S6 — three prompts later.

**Root cause**: P3-S3's verification said "bun test green" but did not name the specific test file that would be affected by the text change.

**Prevention**: When a prompt changes code that has associated tests, name the test file in the Verify section: "Run `bun test tests/unit/prompt_assemble.test.ts`. All tests pass."

### 9.4 Spec-Code Type Mismatch

**What**: Spec 14 example showed `origin_refs` as `[{kind, ref}]` (objects) but code implements `string[]`. The spec example was written before the FR was refined.

**Root cause**: The spec example was not updated when the FR text was refined in a later prompt.

**Prevention**: When a prompt refines a spec FR, include in the Verify section: "Spec examples at [section] match the refined FR text."

### 9.5 Property Naming Convention Mismatch

**What**: Code used `runCtx` (camelCase) but the spec and Gate class use `run_ctx` (snake_case). `tsc` caught it immediately.

**Root cause**: TypeScript convention (camelCase) conflicted with the harness naming convention (snake_case). The agent defaulted to TypeScript convention.

**Prevention**: When a prompt introduces naming conventions, include the convention in the Constraints section: "Use snake_case for all harness field names, not TypeScript camelCase."

### 9.6 What the Findings Card Caught

The findings card recorded all 16 issues above. Later prompts loaded it and:

- Avoided the `2>&1` pattern (banned in card 00 Section 12 after the first hang)
- Caught spec-code mismatches earlier by checking the findings card before verification
- Followed the naming convention after reading the mismatch entry
- Backfilled the skipped STRUT step after reading the sequencing violation entry

Without the card, these issues would have been discovered only at the final validation — too late to fix without re-running earlier prompts.

## 10. Robustness Clause Examples

### 10.1 Implementation Prompt (Standard)

```
- Hang safety: commands per `agent-behavior.md` Terminal Hang Prevention (supervised runner); bans and expected runtimes per `_agentwork/__CARD_[TOPIC]-Robustness.md`.
- Runtime check: before each command state the expected seconds and check the "Never again" list in `_agentwork/__CARD_[TOPIC]-Fails.md`; while it runs read the `ALIVE` lines in the runner log and end it only on a hang verdict, never for its runtime; after it compare with `elapsed=`; on KILLED, ERROR, unexpected exit, or elapsed above both 3x expected and expected + 30 s, write a Fails card entry at once, fix the root cause, continue (a finished slow command is never re-run); same failure twice in this prompt: stop with a PROBLEMS.md entry naming the Fails entry ID.

Findings card: Load and update `__CARD_[TOPIC]-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts.
```

### 10.2 Research Prompt (No Builds)

Same two Constraints lines if the prompt runs any command; prompts that only read files with agent tools are exempt (Section 2).

## 11. Timeout Execution

The supervised runner `run-supervised.ps1` (@skills:terminal-robustness) is the only supervision mechanism (containment, liveness log, kill on a hang verdict; no deadline); its call line lives in `agent-behavior.md` Terminal Hang Prevention. Prompts never contain a timeout pattern, a kill procedure, or a runner call line.

## 12. Review Checklist

Before considering a prompt file complete, verify robustness:

**Hang-safety**:
- [ ] Every implementation prompt includes the one-line hang-safety clause referencing `agent-behavior.md` and the robustness card (PRMT-HS-01, PRMT-HS-02)
- [ ] Expected runtimes live in the robustness card, not in prompts; prompts with an unusual command name its expected seconds; no prompt sets a time limit for a command (PRMT-HS-03)
- [ ] No prompt restates hang-verdict, kill, or cleanup procedures (PRMT-HS-04, PRMT-HS-05)
- [ ] No prompt contains `2>&1`, `git log`, `git diff`, `git show` without `--no-pager` (PRMT-HS-06)
- [ ] Every implementation prompt includes exactly one runtime-check line pointing to the Fails card; the Fails card exists in `_agentwork/` (PRMT-RB-08)
- [ ] No shell commands for file search/read in prompt bodies — agent tools only (PRMT-CT-12)
- [ ] Card `## Agent tool limits` equals the writing agent's rule; file-writing prompts reference it; no token numbers in prompts (PRMT-HS-11)
- [ ] Cascade: prompts touching German law carry the `gesetze-im-internet.de` site ban (Section 2)
- [ ] Document History timestamps use request metadata, not extrapolated times (PRMT-CT-13)
- [ ] Banned-term sweep recordings describe pattern shape, do not spell banned literals (PRMT-CT-14)
- [ ] Verification runs specific test files, not full suite, during implementation steps (PRMT-HS-09)
- [ ] Verify section checks spec-code consistency when prompt changes code with associated spec (PRMT-HS-10)
- [ ] Verification checkpoints after every checkpoint interval plus a final checkpoint per file (PRMT-SQ-04)
- [ ] Every implementation prompt includes "Execute without asking for confirmation" in Constraints (PRMT-EX-03)

**Verification depth**:
- [ ] Verification sections name specific test files when code changes affect tests (PRMT-HS-07)
- [ ] Verification sections include residual sweeps when concepts are removed (PRMT-HS-07)
- [ ] Prompts that depend on prior steps verify the prior step is done (PRMT-HS-08)

**Findings card**:
- [ ] The prompt sequence designates a findings card (PRMT-RB-01)
- [ ] Every implementation prompt includes a Findings card directive pointing to the card (PRMT-RB-02)
- [ ] The findings card is loaded at prompt startup for unresolved entries from prior prompts (PRMT-RB-03)
- [ ] Glitches are filed in the findings card before the end-of-prompt commit (PRMT-RB-04)
- [ ] Each glitch entry records: what, expected, actual, root cause, resolution, prevention (PRMT-RB-05)
- [ ] The card system end-of-prompt protocol includes a findings-card update step (PRMT-RB-06)
- [ ] Session PROBLEMS.md records deferred problems, not detailed glitch logs (PRMT-RB-07)

## 13. Example Files

Worked examples for card types referenced in this guide:

- Robustness card and Fails card structure: @skills:terminal-robustness `ROBUSTNESS_CARD_SKELETON.md` + agent `ROBUSTNESS_CARD_TEMPLATE.md`
- `PROMPTS_EXAMPLE_03-FindingsCard.md` — complete `__CARD_[TOPIC]-Findings.md` with resolved glitches, unresolved blocker, six-field entry format

Load these when authoring cards for a new prompt sequence. The examples are not mandatory reads — load them when unfamiliar with card structure or when a sequence has complex robustness requirements.
