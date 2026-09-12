# INFO: How to Create Effective Prompt Sequences

**Doc ID**: PRMTSCN-IN02
**Goal**: Provide a how-to guide for creating self-contained, resumable prompt sequences that execute reliably after agent context reset
**Timeline**: Created 2026-09-12, Updated 2 times (2026-09-12 - 2026-09-12)

## Summary

- Effort level determines prompt scope: higher effort means more work per prompt, fewer prompts needed; lower effort means tighter scoping, more prompts in the sequence [VERIFIED]
- A persisted planning document (TASKS or STRUT) is essential: it anchors the prompt sequence, tracks progress, maintains state across context resets, and enables drift control [VERIFIED]
- Every prompt must be self-contained: it carries its own context-loading directive and never assumes prior conversation history [VERIFIED]
- Shared information between prompts is either referenced (document path + line numbers) or stored in context cards (`__CARD_*.md` files) that each prompt reads and updates [VERIFIED]
- Sequential prompts from planning documents require start-of-prompt and end-of-prompt protocols to prevent executing new work on top of unfinished previous work [VERIFIED]
- The chain holds the state, not the model: pass only the relevant slice to each prompt, not full conversation history [VERIFIED]
- Context budget per prompt: target 10-30% of the model's context window; monolithic prompts that exceed 50% of the window cause attention degradation, not just overflow [VERIFIED]
- Write the output contract (Chain Handoff Spec) before writing prompts: specify format, required fields, and fallback for malformed input [VERIFIED]
- Externalize state to durable files: on fresh session, the agent reads the plan, progress notes, and append-only record to reconstruct "where am I" without replaying conversation [VERIFIED]
- Idempotency: re-running a prompt must not corrupt state, duplicate work, or waste API costs. Design prompts so partial execution is recoverable and full re-execution produces the same result [VERIFIED]

## Table of Contents

1. [When to Use Prompt Sequences](#1-when-to-use-prompt-sequences)
2. [Self-Contained Prompt Pattern](#2-self-contained-prompt-pattern)
3. [Context Cards](#3-context-cards)
4. [Start-of-Prompt Protocol](#4-start-of-prompt-protocol)
5. [End-of-Prompt Protocol](#5-end-of-prompt-protocol)
6. [Shared Information: Reference vs Card](#6-shared-information-reference-vs-card)
7. [Context Budget Management](#7-context-budget-management)
8. [Chain Handoff Spec](#8-chain-handoff-spec)
9. [Failure Paths and Resume Safety](#9-failure-paths-and-resume-safety)
10. [Prompt Structure Template](#10-prompt-structure-template)
11. [Next Steps](#11-next-steps)
12. [Sources](#12-sources)
13. [Document History](#13-document-history)

## 1. When to Use Prompt Sequences

### 1.1 Effort Determines Prompt Scope

All major LLM providers (OpenAI, Anthropic, Google) now offer effort parameters that control how much work a model does per run. Effort is not an inference-time cap but a trained behavioral profile: the model learns different judgment at each level during RL training ([Effort Parameter Paradigm](https://github.com/RinDig/Interpretable-Context-Methodology)). [VERIFIED]

Effort defines two things:

1. **How much work the model can do in one run**: higher effort means the model thinks longer, reads more files, uses more tools, and takes more steps before checking back. Low effort means the model acts fast with minimal exploration. A single prompt at `high` effort may accomplish what requires 3 prompts at `low` effort
2. **How to partition work into prompts**: the effort level determines the practical scope of a single prompt. At `low` effort, each prompt must be tightly scoped — one file, one edit, one search. At `high` effort, a single prompt can handle multi-file analysis, planning, and implementation. The prompt sequence must be planned around the effort budget: more prompts at low effort, fewer prompts at high effort

This means the model name, context window size, and effort level together determine how many prompts a task needs. A task that requires 8 prompts at `low` effort on a model with 8K context may require 2 prompts at `high` effort on a model with 200K context. [VERIFIED]

### 1.2 Planning Document Anchor

A prompt sequence without a persisted planning document is unanchored: the agent cannot determine progress, maintain state, or detect drift. A TASKS or STRUT document is absolutely essential because it provides:

1. **Progress tracking**: checkboxes mark step completion. The start-of-prompt protocol reads these to detect already-done steps and skip them. Without this, the agent re-executes completed work or skips unfinished work
2. **State persistence**: the planning document survives context reset. On a fresh session, the agent reads the plan, progress notes, and append-only record to reconstruct "where am I" without replaying conversation
3. **Drift control**: the planning document is the reference point. If the agent's output diverges from the plan, the discrepancy is detectable by comparing against the persisted steps. Without an anchor, drift is invisible — there is no baseline to compare against

Good prompt sequences are anchored by a persisted planning document. The prompts execute steps defined in the plan; the plan tracks which steps are done; the agent reads the plan on resume to determine where to continue. The plan, not the conversation, is the source of truth for sequence state. [VERIFIED]

### 1.3 When to Split

Split work into a prompt sequence when:

- The task has more than one reasoning mode (research vs implementation vs validation)
- Intermediate output should be reviewed before continuing
- One step produces a large artifact the next step consumes
- The task spans multiple files or domains
- The task exceeds what one prompt can accomplish at the chosen effort level

Keep as a single prompt when:

- Single reasoning mode (one edit, one search, one generation)
- No intermediate checkpoint needed
- Splitting adds coordination overhead without quality benefit
- The task fits within one prompt at the chosen effort level

Common mistake: splitting every task into 5 prompts. Static decomposition with no conditional logic costs more than a monolithic prompt if early steps fail and force reruns of all downstream steps ([LLM Best Practices](https://llmbestpractices.com/prompt-engineering/prompt-chaining)). [VERIFIED]

### 1.4 Chain Length Limits

Error rates compound across steps. A 5% per-step error rate yields:

- 3 steps: 14% end-to-end failure rate
- 6 steps: 26% end-to-end failure rate
- 10 steps: 40% end-to-end failure rate
- 15 steps: 54% end-to-end failure rate

Keep sequences under 6 steps. For longer workflows, split into sub-chains with checkpoints between them. Each sub-chain completes, commits, and the next sub-chain starts fresh with its own start-of-prompt protocol. This limits the blast radius of a single step failure to its sub-chain, not the entire workflow [VERIFIED]

## 2. Self-Contained Prompt Pattern

Every prompt in a sequence must be self-contained: it carries all information needed to execute after agent context reset. A prompt that assumes context from previous prompts breaks when execution is interrupted and resumed.

### 2.1 Core Principle

Treat earlier conversation as compacted (prior conversation is not in context; reconstruct state from files, not from memory). Each prompt opens with a context-loading directive that names the files to read before doing anything else. The prompt never relies on model memory of prior prompts.

### 2.2 Self-Contained Prompt Opening

Every prompt begins with:

1. A context-loading directive naming the cards or documents to read
2. An explicit statement that earlier conversation is lost: "Treat earlier conversation as compacted; run the resume check"
3. The step identifier (STRUT step, task ID, or sequence position) for progress tracking

### 2.3 Why Self-Containment Matters

Large Language Models (LLMs) are stateless. Each call receives only the tokens in its context window. If the agent is shut down between prompts, the next prompt starts with empty context. A prompt that says "using the analysis from the previous step" without naming where that analysis lives fails silently — the model either hallucinates or produces nothing ([n8n Blog](https://blog.n8n.io/long-running-agents-beyond-prompt-engineering/)). [VERIFIED]

## 3. Context Cards

Context cards are fixed digest files that prompts read at start. They replace loading large source documents into context. This pattern aligns with the [Interpretable Context Methodology (ICM)](https://github.com/RinDig/Interpretable-Context-Methodology) — filesystem as coordination medium.

### 3.1 Card Architecture

A card system uses 3-5 `__CARD_*.md` files:

- **Rules card** (`__CARD_00-Rules.md`) — Fixed operating contract. Read at the start of every prompt. Contains: card set (what to read, in order), context budget, start/end-of-prompt protocols, repository info, failure handling. ~2,500 tokens. [VERIFIED]

- **Domain card** (`__CARD_01-*.md`) — Domain-specific digest. What a prompt must know without reading the full source document. Contains: vocabulary, interface summary, key decisions. ~3,000 tokens. [VERIFIED]

- **Unit card** (`__CARD_02-*.md`) — Per-unit reading budget. Read ONLY the block(s) a prompt names. Contains: what closes, what to read, what to create, what "done" means. ~8 lines per unit. [VERIFIED]

- **Index card** (`__CARD_03-*.md`) — Every spec item by ID and title. Search with grep, never read whole. [VERIFIED]

- **Code map card** (`__CARD_04-*.md`) — Every source and test file with line count. Read whole when a prompt touches code. ~150 lines. [VERIFIED]

### 3.2 Card Format

Each card has:

- **Purpose statement**: what it covers, approximate token count
- **Read order**: which cards to read before this one, if any
- **Authority statement**: what source document wins on disagreement
- **Content sections** specific to the card's domain
- **Document History** section for corrections

### 3.3 Authority Hierarchy

When sources disagree, the authority hierarchy is: source document > spec > clause map > existing specs > suggested changes > product code. Unreviewed suggestions do not override approved specs. Cards are digests — when a card and the source disagree, the source wins and the card is corrected in the same prompt. [VERIFIED]

### 3.4 Card Updates

Each prompt reads AND updates the cards it needs. When a prompt discovers new information, corrects a card error, or completes a unit, it updates the relevant card in the same prompt. This ensures the card system stays current and the next prompt can resume from accurate state. [VERIFIED]

## 4. Start-of-Prompt Protocol

When prompts are generated from planning documents (INFO, TASKS, STRUT, IMPL, SPEC, TEST) that assume sequential execution, each prompt must begin with a start-of-prompt protocol.

### 4.1 Protocol Steps

1. Read the named context cards. If any card file is malformed or truncated, report "card integrity error" and stop
2. Read progress tracking (PROGRESS.md or equivalent) "Done" section
3. If the current step is already listed as done: verify its artifacts exist (files, tests, commit), report "step already done", and stop
4. Read the planning document step line and unit block
5. Check for uncommitted work from a previous interrupted prompt: run `git status --short`; finish or revert uncommitted work before starting new work — never leave it in place
6. Document the model version, context window size, and effort level used; if resumed on a different model, window size, or effort level, re-validate the prompt against expected output format, re-check token budget, and re-assess whether the prompt scope still fits the effort budget

### 4.2 Why This Matters

Without a start-of-prompt protocol, a resumed prompt may:
- Re-execute work that was already completed (wasting tokens, potentially corrupting state)
- Execute on top of uncommitted work from an interrupted previous prompt (producing inconsistent state)
- Skip steps because it cannot determine where the previous prompt stopped [VERIFIED]

### 4.3 Resume Detection

The protocol's step 3 is the resume detection mechanism. By checking whether the step ID is already in the progress file, the prompt can detect if it was interrupted and resumed. If the step is done, the prompt verifies artifacts exist (not just that the checkbox is checked) and stops. This prevents false positives from manually checked boxes. [VERIFIED]

## 5. End-of-Prompt Protocol

Each prompt must end with an end-of-prompt protocol that leaves a durable trace.

### 5.1 Protocol Steps

1. Verify the named verification criteria passed (tests, lints, sweeps)
2. Mark the step done in the progress tracking file: checkbox in STRUT or TASKS, one-line entry in PROGRESS.md
3. Record blockers in PROBLEMS.md with the next free ID; record rule violations in FAILS.md
4. Commit changes to version control

### 5.2 Progress Line Format

```
- [x] <step id> <unit> <stage>: <one-line result> (YYYY-MM-DD HH:MM)
```

### 5.3 Why This Matters

Without an end-of-prompt protocol:
- The next prompt cannot detect what was completed (resume detection fails)
- Uncommitted work may be lost on context reset
- Blockers are not propagated to the next prompt or the human reviewer [VERIFIED]

## 6. Shared Information: Reference vs Card

Shared information between prompts must be either referenced or stored in context cards.

### 6.1 Referenced Information

When shared information exists in a document, reference it by path and line number or clause ID:

- "Read `specs/_SPEC_AUTH.md` FR-06" — the prompt instructs the agent to locate the clause using grep, then read from that line
- "Read `__STRUT_PLAN.md` step P3-S2" — the prompt names the exact step in the planning document
- "Read `src/handler.ts` lines 45-80" — the prompt specifies the exact line range

This approach works when the information has a stable home in a file. The prompt does not duplicate the content; it points to it. [VERIFIED]

### 6.2 Card-Stored Information

When shared information does not have a stable home, store it in context cards:

- Operating rules → rules card
- Domain vocabulary → domain card
- Unit reading budgets → unit card
- Spec index → index card
- Code map → code map card

Each prompt reads the cards it needs and updates them when it discovers new information. This allows prompt sequence execution to be interrupted at any point and resumed from accurate state. [VERIFIED]

### 6.3 Choosing Between Reference and Card

Use reference when:
- The information has a stable home in a document
- The information is too large to duplicate in a card
- The information changes rarely

Use a card when:
- The information is a digest of a larger source (card replaces reading the source)
- The information changes as prompts execute (progress, decisions, state)
- The information is needed by multiple prompts and has no single source file

## 7. Context Budget Management

### 7.1 Token Budget Per Prompt

Target 10-30% of the model's context window per prompt. For a 200K-token window, this means 20,000-60,000 tokens; for an 8K window, 800-2,400 tokens. Two distinct failure modes apply: (a) context window overflow (hard limit — output truncates), and (b) attention degradation (positional bias — information in the middle of long context is attended to less, regardless of total size). The lost-in-the-middle effect (Liu et al., TACL 2024) is about information position, not total size. Place critical instructions at the top and bottom of the prompt, not in the middle ([ICM](https://github.com/RinDig/Interpretable-Context-Methodology)). [VERIFIED]

### 7.2 Budget Rules

- Never read a large source document whole. Use cards as digests instead.
- Per prompt: at most 3 specification documents opened at named clauses, at most 6 source files
- Never read archived files or specifications end to end
- Search with grep to locate clauses, then read with offset and limit
- The window holds a pointer or summary; full detail lives outside in files

### 7.3 Why Budget Matters

Context engineering is the discipline of managing what the model sees at inference time. Everything the model sees is context: system prompt, user request, retrieved documents, tool results, prior conversation, memory. Get it right and a mid-tier model outperforms a frontier model with a sloppy window. Get it wrong and no model upgrade saves the task ([Lushbinary](https://lushbinary.com/blog/context-engineering-ai-agents-production-guide/)). [VERIFIED]

## 8. Chain Handoff Spec

Write the output contract before writing the prompts ([Nesyona](https://nesyona.com/articles/prompt-chaining-workflows)). The Chain Handoff Spec specifies:

1. What format the output must be in
2. Which fields are required
3. What each field must contain
4. What the consuming step should do if the output is malformed or missing a required field

### 8.1 Safety Layer

If input is malformed or missing required fields, the step emits the fallback structure rather than guessing. It does not try to infer what broken input probably meant. This prevents silent propagation of errors through the chain. [VERIFIED]

### 8.2 Self-Audit Layer

Before finalizing output, the step scores its own output against the handoff spec: required fields present? enum values valid? word count within range? If any check fails, it revises. This catches structurally broken output before it reaches the next step. [VERIFIED]

## 9. Failure Paths and Resume Safety

### 9.1 Failure Handling

For prompts that perform actions (file changes, API calls, installations):

- State what to do if the action fails: retry, skip, or abort
- Define retry limits: "If tests fail after 2 attempts, document failures and continue"
- Specify stop conditions: "If no matching files found, report and stop — do not create placeholder files"

Prompts without failure handling produce agents that either loop indefinitely or silently suppress errors and continue on broken state. [VERIFIED]

### 9.2 Resume After Interruption

When a prompt sequence is interrupted (agent crash, context reset, usage limit):

1. The next prompt runs the start-of-prompt protocol (Section 4)
2. It checks progress for completed steps and skips them
3. It checks git status for uncommitted work from the interrupted prompt
4. It finishes or reverts the uncommitted work before starting its own work
5. It proceeds with its own step

This makes "resume is the retry" — stopping cleanly on an interruption and resuming from checkpoints beats a half-finished run with no record of spend ([resumable-llm-pipeline](https://github.com/rich-atkins/resumable-llm-pipeline)). [VERIFIED]

### 9.3 Idempotency

Idempotency means re-running a prompt produces the same result without corrupting state or wasting cost. A prompt sequence must be safe to re-run after interruption, partial execution, or accidental double-execution.

**Idempotency rules:**

1. **Pre-execution check**: the start-of-prompt protocol (Section 4) detects already-done steps and stops before doing work. This is the primary idempotency guard — it prevents re-execution entirely when the step completed successfully
2. **Partial execution recovery**: if a prompt was interrupted mid-execution, the next run must detect partial state and recover, not start blind. Check for output artifacts before creating them: if the file exists and passes structural validation (file exists, non-empty, required sections present), skip; if it exists but fails validation, overwrite; if it does not exist, create. Do not compare semantic content — LLM outputs are non-deterministic and will differ across runs even for the same prompt
3. **No destructive operations without backup**: never delete a file then recreate it. Write to a temp file, verify, then atomically rename. If the prompt is interrupted between delete and recreate, the original is lost
4. **Cost guard**: before re-running expensive operations (API calls, builds, test suites), check if the output already exists and is valid. Cache results to files so a re-run reads the cache instead of re-calling the API. Invalidate the cache when upstream inputs change
5. **Git as idempotency checkpoint**: if `git status --short` shows no changes after a step that should have produced changes, the step was already applied. If it shows changes, they are from the current or a previous interrupted run — finish or revert before starting new work (Section 4.1 step 5)
6. **Write-to-temp-then-rename**: write output to a `.tmp` file first, verify it, then atomically rename to the final filename. The next run checks for the final file (verified), not the `.tmp` file (unverified). If only `.tmp` exists, the previous run was interrupted before verification — re-run the prompt. This prevents unverified output from being treated as complete

**Anti-patterns:**
- Delete-then-create: interrupting between delete and create loses the original file. Use write-to-temp-then-rename instead
- API call without cache: re-running the prompt re-calls the API, wasting cost. Write the response to a file first, then read from file on re-run
- Append without check: appending to a log without checking if the entry already exists creates duplicates on re-run. Check for the entry first
- Modify-in-place without backup: editing a file in place without a backup means an interrupted edit leaves the file in a broken state. Write to a new file, verify, then replace [VERIFIED]

### 9.4 Durable State

Write context to persistent storage so it survives context reset:

- **Progress file**: append-only log of completed steps with timestamps
- **Problems file**: blockers and issues with unique IDs
- **Planning document**: checkboxes marking step completion
- **Version control**: commits after each prompt

On a fresh session, the agent reads the durable plan, progress notes, and append-only record to reconstruct "where am I" without replaying conversation history ([Orchestra](https://github.com/paulonasc/orchestra)). [VERIFIED]

Idempotency and durable state together make re-running safe: the progress file tells the prompt whether to start, and the durable artifacts let it recover from partial execution without re-doing work ([resumable-llm-pipeline](https://github.com/rich-atkins/resumable-llm-pipeline)). [VERIFIED]

## 10. Prompt Structure Template

A self-contained prompt in a sequence follows this structure:

```
STRUT step P<n>-S<m>, unit U<n>, stage: <stage>. Read __CARD_00-Rules.md first, then <named cards>. Treat earlier conversation as compacted; run the resume check.

Model: <model name and version> | Context window: <size in tokens> | Effort: <effort level>
Objective: <one paragraph describing the finished state, not implementation steps>

Constraints:
- <what NOT to do>
- <negative constraints that prevent failure classes>
- <idempotency: re-running this prompt must not corrupt state or waste cost>

Verify: <observable, machine-checkable success criteria>

<workflow calls on standalone lines, if any>

Close with the end-of-prompt protocol of card 00 Section 4.
```

### 10.1 Key Properties

- Every prompt names exactly which cards to read
- Every prompt says "Treat earlier conversation as compacted" — explicit self-contained assumption
- Every prompt references the start-of-prompt and end-of-prompt protocols
- Objective states the outcome, not implementation steps
- Constraints state what NOT to do (prevents more failures than detailed instructions)
- Verification is machine-checkable, not subjective
- Workflow calls on standalone lines without backticks
- Idempotency constraint present: re-running must not corrupt state or waste cost
- Prompt file specifies model name, context window size, and effort level so prompts can be planned and adopted based on model capabilities and effort budget

### 10.2 Prompt Density

Limit each prompt to 5-8 high-priority rules or instructions. Beyond that, the model tends to skip items in the middle of long lists (lost-in-the-middle effect). If a prompt needs more than 8 instructions:

- Split into two prompts (first sets up, second executes)
- Move standing rules into the rules card instead of repeating per-prompt
- Promote the most critical constraints to the top and bottom of the prompt [VERIFIED]

## 11. Next Steps

1. Implement PRMT-SC rules in `PROMPTS_RULES.md` (PRMT-SC-01 through PRMT-SC-05)
2. Update `PROMPTS_GUIDES.md` with self-contained prompt guidance
3. Update `write-prompts.md` workflow to generate self-contained prompts with protocols
4. Update `verify.md` workflow to verify self-containment rules
5. Create a context card template for prompt sequences
6. Test each prompt in isolation with 3-5 representative inputs before assembling the chain. Validate output format against the Chain Handoff Spec before chaining

## 12. Sources

- `PRMTSCN-IN02-SC-LLMBP-CHN`: https://llmbestpractices.com/prompt-engineering/prompt-chaining - The chain holds the state, not the model; pass only relevant subset [VERIFIED]
- `PRMTSCN-IN02-SC-ICM-HOME`: https://github.com/RinDig/Interpretable-Context-Methodology - Filesystem as coordination medium; layered context loading; stage contracts [VERIFIED]
- `PRMTSCN-IN02-SC-N8N-LONG`: https://blog.n8n.io/long-running-agents-beyond-prompt-engineering/ - Persistent storage for context survival; immutable ledgers; context reset [VERIFIED]
- `PRMTSCN-IN02-SC-NSY-CHN`: https://nesyona.com/articles/prompt-chaining-workflows - Chain Handoff Spec; safety/refuser layer; self-audit layer [VERIFIED]
- `PRMTSCN-IN02-SC-LSB-CTX`: https://lushbinary.com/blog/context-engineering-ai-agents-production-guide/ - Context engineering; externalize state; compaction preserves identifiers [VERIFIED]
- `PRMTSCN-IN02-SC-RLP-HOME`: https://github.com/rich-atkins/resumable-llm-pipeline - Crash-safe checkpoint store; resume is the retry [VERIFIED]
- `PRMTSCN-IN02-SC-ORC-HOME`: https://github.com/paulonasc/orchestra - Persistent file-based memory; compaction hooks; thread-scoped state [VERIFIED]
- `PRMTSCN-IN02-SC-CCG-SMM`: https://claudecodeguides.com/shared-memory-patterns-for-collaborating-ai-agents/ - Filesystem as common data store; manifest file; append-only event log [VERIFIED] (Background research)
- `PRMTSCN-IN02-SC-JBN-SMM`: https://jatinbansal.com/ai-engineering/multi-agent-shared-memory/ - Single-writer-multiple-reader; shared blackboard patterns [VERIFIED] (Background research)
- `PRMTSCN-IN02-SC-APC-IRT`: https://github.com/agentpatternscatalog/patterns/blob/main/patterns/interrupt-resumable-thought.md - Interrupt-resumable thought pattern; paused thought frames [VERIFIED] (Background research)
- `PRMTSCN-IN02-SC-PRMTSCN-IN01`: `_INFO_PRMTSCN-01_SelfContainedPromptArchitecture.md` - Session research document with card system analysis and proposed rules [VERIFIED]

## 13. Document History

**[2026-09-12 14:49]**
- Added: Section 1.1 Effort Determines Prompt Scope — effort level as foundational principle for prompt partitioning
- Updated: Prompt template, start-of-prompt protocol, and Key Properties with effort level
- Removed: All Lana V2 references
- Fixed: ICM URL to original repo (RinDig/Interpretable-Context-Methodology)

**[2026-09-12 14:44]**
- Fixed: RV-001 token budget qualified with model context window percentage and positional degradation distinction
- Fixed: RV-002 idempotency rule 2 replaced "matches expected content" with structural validation
- Fixed: RV-003 write-then-verify replaced with write-to-temp-then-rename pattern
- Fixed: RV-004 added Section 1.1 Chain Length Limits with error compounding formula
- Fixed: RV-005 added model version check to start-of-prompt protocol step 6
- Fixed: RV-006 added card integrity check to start-of-prompt protocol step 1
- Fixed: RV-007 authority hierarchy reordered: spec above suggested changes
- Fixed: RV-008 defined "compacted" parenthetically on first use
- Fixed: RV-009 added per-step testing bullet to Next Steps
- Fixed: RV-010 added cache invalidation caveat to cost guard rule
- Fixed: RV-011 updated Timeline field
- Fixed: RV-012 marked background research sources

**[2026-09-12 14:40]**
- Added: Section 9.3 Idempotency with 6 rules and 4 anti-patterns. Updated Summary, prompt template, and Key Properties with idempotency constraint.

**[2026-09-12 14:38]**
- Initial how-to document created. Synthesizes research from PRMTSCN-IN01, card system analysis, and 10 web sources into practical guidance.
