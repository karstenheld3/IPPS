# Agentic English (AGEN)

High-level vocabulary for problem-solving strategy and planning. It defines how agents reason about and decompose problems. Full vocabulary (all placeholders, verbs, labels, states): @skills:promptsystem `PROMPTSYSTEM_AGENTIC_ENGLISH.md`.

## Scope

- Used in: STRUT plans (formal step notation `[ ] P1-S1 [VERB](params)`), EDIRD phase planning (phase transitions, gate evaluations), skill verb mappings (routing actions to the right skill), document planning
- NOT used in: workflow step instructions (plain English or `/workflow` refs), agent skills (except when explicitly referencing AGEN), code comments or implementation details, user-facing documentation
- The formal `[VERB](params)` notation is reserved for STRUT plans and planning documents

## Syntax

- **Instructions `[BRACKETS]`** - tokens the agent reads and DOES: `[VERB]` action to execute (`[RESEARCH]`, `[VERIFY]`, `[IMPLEMENT]`), `[PLACEHOLDER]` value to substitute (`[ACTOR]`, `[WORKSPACE_FOLDER]`), `[LABEL]` classification to apply (`[UNVERIFIED]`, `[CRITICAL]`)
- **Verb modifiers**: `[VERB]-OK` successful outcome, proceed to next step; `[VERB]-FAIL` failed outcome, re-iterate or escalate; `[VERB]-SKIP` intentionally skipped (complexity doesn't require it)
- **States `NO-BRACKETS`** - tokens the agent checks for branching: `PREFIX-VALUE` format (`SINGLE-PROJECT`, `COMPLEXITY-HIGH`, `HOTFIX`), used in conditional headers (`## For COMPLEXITY-HIGH`), never substituted or executed - only checked
- **[ACTOR]** - decision-making entity. Default: user. `/go` sets `[ACTOR] = agent`: all Communication verbs (`[CONSULT]`, `[CONFIRMS]`, `[QUESTION]`, `[PROPOSE]`) target the agent itself, which self-resolves, logs the decision, and proceeds without user interaction

## Vocabulary Groups

- **Verbs**: information gathering (`[RESEARCH]`, `[ANALYZE]`), thinking and planning (`[SCOPE]`, `[PLAN]`, `[PARTITION]`, `[ASSESS]`), validation and proof (`[PROVE]`, `[VERIFY]`, `[TEST]`, `[CRITIQUE]`, `[RECONCILE]`), documentation (`[WRITE-SPEC]`, `[WRITE-IMPL-PLAN]`), implementation (`[IMPLEMENT]`, `[FIX]`), communication (`[CONSULT]`, `[PROPOSE]`, `[RECOMMEND]`), completion (`[COMMIT]`, `[DEPLOY]`, `[CLOSE]`, `[ARCHIVE]`)
- **Labels**: assumption labels (`[UNVERIFIED]`, `[CONTRADICTS]`, `[OUTDATED]`, `[INCOMPLETE]`), status labels (`[RESOLVED]`, `[WONT-FIX]`, `[NEEDS-DISCUSSION]`)
- **States**: workspace context (`SINGLE-PROJECT`, `SESSION-MODE`), complexity (`COMPLEXITY-LOW`, `COMPLEXITY-MEDIUM`, `COMPLEXITY-HIGH`), SOLVE problem type (`RESEARCH`, `ANALYSIS`, `EVALUATION`, `WRITING`, `DECISION`, `HOTFIX`, `BUGFIX`)
