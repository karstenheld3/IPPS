# INFO: How to Write Good Prompts for Headless Agent Execution

**Doc ID**: WRTPRMPT-IN01
**Goal**: Define what makes prompts effective for sequential headless execution in `_PROMPTS_[Topic].md` files, and derive GUIDE/RULES split for the write-documents skill
**Timeline**: Created 2026-08-31, Updated 0 times

## Summary

- Effective prompts for headless execution follow a 4-part structure: Objective, Context, Constraints, Verification [VERIFIED]
- One prompt = one concern. Mixing roles (plan + execute + validate) degrades output quality because the model has no signal which mode it is in [VERIFIED]
- Constraints (what NOT to do) prevent more failures than detailed instructions (what to do). Agents optimize for what you literally asked; unstated boundaries get crossed [VERIFIED]
- Verification criteria must be machine-checkable or observable, not subjective ("works correctly"). Without explicit done-criteria, the agent decides when to stop [VERIFIED]
- Context must be selective: name specific files and relevant facts instead of dumping everything. Context window fill degrades retrieval quality [VERIFIED]
- Sequential prompts in one session accumulate state. Later prompts can reference earlier results without restating them, but must not contradict earlier constraints [VERIFIED]
- Maximum 5-8 high-priority rules per prompt. Beyond that, lost-in-the-middle effect causes the model to skip rules late in long lists [VERIFIED]
- Stop criteria and failure handling must be explicit. Without them, agents loop on failures indefinitely or silently suppress errors [VERIFIED]
- GUIDES/RULES split: GUIDES cover strategic decisions (when to decompose, how to structure, what context to include). RULES cover verifiable output standards (every prompt has objective, constraints checkable from artifact) [ASSUMED]

## Table of Contents

1. [The Problem: Why Headless Prompts Differ from Chat](#1-the-problem-why-headless-prompts-differ-from-chat)
2. [The 4-Part Prompt Structure](#2-the-4-part-prompt-structure)
3. [Decomposition: When to Split Prompts](#3-decomposition-when-to-split-prompts)
4. [State Management Across Sequential Prompts](#4-state-management-across-sequential-prompts)
5. [Common Failure Modes](#5-common-failure-modes)
6. [GUIDES vs RULES Split](#6-guides-vs-rules-split)
7. [Next Steps](#7-next-steps)
8. [Sources](#8-sources)

## 1. The Problem: Why Headless Prompts Differ from Chat

A chat prompt is an instruction for a single answer. An agent prompt is an instruction for a process involving sequential decisions, tool calls, and error conditions. In headless execution (no human in the loop), the cost of a poorly specified prompt is not a mediocre paragraph - it is a failed workflow ([Applied AI Hub](https://appliedaihub.org/blog/prompt-engineering-for-autonomous-ai-agents/)).

Key differences:

- **No correction opportunity** - Chat allows back-and-forth refinement. Headless prompts must be complete on first submission
- **Cascading failures** - A wrong assumption in prompt 2 propagates through prompts 3-N. Each builds on the last
- **State accumulation** - In a `_PROMPTS_[Topic].md` file, all prompts run as turns of ONE session. Later prompts see earlier results
- **No implicit context** - The agent has no IDE state, no cursor position, no open files unless the prompt names them

This means headless prompts must be more precise, more constrained, and more explicit about success criteria than interactive chat prompts.

## 2. The 4-Part Prompt Structure

Every effective agent prompt contains four components ([Field Guide to AI](https://fieldguidetoai.com/guides/prompting-ai-agents), [TECHSY](https://techsy.io/en/blog/prompt-engineering-for-coding), [Musketeers Tech](https://musketeerstech.com/blogs/prompt-engineering-best-practices/)):

### 2.1 Objective (What, Not How)

State the desired outcome. Do not micromanage implementation steps.

- **Weak**: "Open file X, find function Y, add a try-catch around line Z, return error 401"
- **Strong**: "The validateToken middleware crashes on expired JWTs. Fix it so expired tokens return 401 instead of crashing"

The strong prompt describes the problem and desired state. The agent determines the implementation. This matters because the agent may find a better solution than the one you would have prescribed.

### 2.2 Context (Selective, Not Exhaustive)

Name specific files, tech stack, business logic, and conventions the agent needs. Do not dump the entire codebase.

- Name 1-3 relevant files
- State the tech stack and patterns in use
- Include business logic the agent cannot infer from code

Context window fill degrades retrieval quality ([Blck Alpaca](https://blckalpaca.at/en/knowledge-base/ai-agents/prompt-engineering-for-agents/system-prompts-design-patterns)). Treat the context window as a budget, not a dumping ground.

### 2.3 Constraints (What NOT to Do)

Constraints prevent more failures than instructions. Agents optimize for what you literally asked; unstated boundaries get crossed.

- "Do not modify the database schema"
- "No new dependencies"
- "Preserve the existing public API"
- "Do not change files outside src/auth/"

### 2.4 Verification (Machine-Checkable Done Criteria)

Without explicit verification, the agent decides when it is done.

- **Weak**: "Make sure it works correctly"
- **Strong**: "Run `pnpm test`. All tests pass. The endpoint returns 200 for valid tokens and 401 for expired ones"

Every prompt should end with observable success criteria. For prompts in a sequential file, the verification of prompt N becomes implicit context for prompt N+1.

## 3. Decomposition: When to Split Prompts

Not every task needs multiple prompts. The decision depends on three factors ([Nesyona](https://nesyona.com/articles/prompt-chaining-workflows)):

1. **Multiple reasoning modes?** Research, implementation, validation, and formatting are different modes. If the task requires more than one, split
2. **Need to inspect mid-workflow?** If a human or automated check should review intermediate output, you need separate prompts
3. **Different model strengths?** If one step benefits from depth (research) and another from precision (formatting), separate them

One prompt per concern:
- **Prompt 1**: Research and analyze (produce findings)
- **Prompt 2**: Implement based on findings (produce code)
- **Prompt 3**: Test and verify (produce test results)

The [SuperPrompts](https://superprompts.app/blog/agentic-ai-prompt-engineering-best-practices-2026) research confirms: "The most effective structural change you can make is to stop giving a single agent multiple roles."

### 3.1 When NOT to Split

- Task has a single reasoning mode (one file edit, one question)
- No intermediate inspection needed
- Splitting adds coordination overhead without quality benefit

Static decomposition that is fixed at design time with no runtime branching can cost more in retries than not decomposing at all ([Asthana et al.](https://jyoung.dev/blog/task-decomposition-for-ai-coding-agents/)).

## 4. State Management Across Sequential Prompts

In a `_PROMPTS_[Topic].md` file, all prompts execute as turns of one session. This means:

- Later prompts see all earlier results (conversation history accumulates)
- No need to restate facts established by earlier prompts
- Constraints established early remain binding throughout
- Contradicting an earlier constraint causes undefined behavior

### 4.1 Commentary as State Documentation

Commentary sections (between `---` and the next fence) document intent for human readers but are never sent to the model. Use them to:

- Explain why this prompt follows the previous one
- Note what the previous prompt should have produced
- Document assumptions for human review

### 4.2 Explicit References to Prior Output

When a later prompt depends on a specific artifact from an earlier prompt, name it:

- "Using the `calc.py` file created in the previous step, add a `multiply` function"
- "The analysis from step 1 identified three issues. Fix the highest-severity one first"

Do not assume the model will infer which prior output matters.

## 5. Common Failure Modes

### 5.1 Prompt-Level Failures

- **Ambiguous objective** - "Improve the code" has no verifiable done state
- **Missing constraints** - Agent installs packages, changes schemas, modifies unrelated files
- **No verification** - Agent produces plausible output with no way to confirm correctness
- **Role mixing** - One prompt asks agent to research, decide, implement, and test. Quality degrades on all four
- **Excessive instructions** - More than 5-8 rules per prompt triggers lost-in-the-middle. Agent skips rules late in long lists

### 5.2 Sequence-Level Failures

- **Contradicting earlier constraints** - Prompt 3 says "use library X" when prompt 1 said "no new dependencies"
- **Assuming prior output** - Prompt 4 references a file that prompt 2 may not have created (conditional path)
- **No failure handling** - No instruction for what to do if a step fails. Agent either loops or silently continues
- **Context window exhaustion** - Too many verbose prompts fill the window, degrading quality on later steps

### 5.3 Format-Level Failures

- **Wrong fence length** - Inner code block closes the outer fence prematurely
- **Missing separator** - `---` between prompts omitted, causing parser error
- **Content outside fences** - Prompt text placed in commentary area, silently dropped

## 6. GUIDES vs RULES Split

Applying the GRUC content boundary test from `_INFO_GRUC_GUIDES_RULES_CHECKS.md [GRUC-IN01]`:

### 6.1 PROMPTS_GUIDES.md (Strategy - Read BEFORE Writing)

Strategic decisions the agent makes before writing prompts:

- **Classify** the task type (single task, multi-step pipeline, research, implementation, mixed)
- **Decide decomposition** - When to split into multiple prompts vs keep as one
- **Structure each prompt** - Apply the 4-part structure (Objective, Context, Constraints, Verification)
- **Plan state flow** - What each prompt produces that the next one consumes
- **Select context** - Which files, facts, and conventions to include vs omit
- **Choose fence length** - Based on inner code block depth
- **Review checklist** - Final check before considering prompts file complete

### 6.2 PROMPTS_RULES.md (Output Standards - Verifiable from Artifact)

Checkable by reading the `_PROMPTS_[Topic].md` file:

- **Structure rules** - Each prompt contains objective. Constraints present when scope could be ambiguous. Verification present for implementation prompts
- **Format rules** - Fence lengths correct, separators present, no content outside fences
- **Scope rules** - One concern per prompt, no role mixing within a single prompt
- **Clarity rules** - No ambiguous objectives, no subjective done criteria
- **Sequence rules** - No contradictions between prompts, explicit references to prior output when dependent
- **Commentary rules** - Commentary sections explain purpose, not duplicate prompt content

## 7. Next Steps

1. Create `PROMPTS_GUIDES.md` in `@skills:write-documents` - strategic approach guidance
2. Create `PROMPTS_RULES.md` in `@skills:write-documents` - verifiable output rules with BAD/GOOD examples
3. Update `write-prompts.md` workflow to reference PROMPTS_GUIDES.md and PROMPTS_RULES.md
4. Consider creating `PROMPTS_TEMPLATE.md` if prompts files benefit from a skeleton template

## 8. Sources

**Primary Sources:**
- `WRTPRMPT-IN01-SC-FGAI-AGNT`: https://fieldguidetoai.com/guides/prompting-ai-agents - 4-part prompt anatomy (Objective, Context, Constraints, Verification), rules files, task decomposition [VERIFIED]
- `WRTPRMPT-IN01-SC-BLCK-SYSP`: https://blckalpaca.at/en/knowledge-base/ai-agents/prompt-engineering-for-agents/system-prompts-design-patterns - 12 design patterns, 4-layer model, 5-8 rule limit, lost-in-the-middle [VERIFIED]
- `WRTPRMPT-IN01-SC-SPMT-AGNP`: https://superprompts.app/blog/agentic-ai-prompt-engineering-best-practices-2026 - One role per prompt, state passing, failure-mode instructions [VERIFIED]
- `WRTPRMPT-IN01-SC-APAI-AUAG`: https://appliedaihub.org/blog/prompt-engineering-for-autonomous-ai-agents/ - Agent prompt vs chat prompt, tool use, state management, failure modes [VERIFIED]
- `WRTPRMPT-IN01-SC-NESY-CHNW`: https://nesyona.com/articles/prompt-chaining-workflows - Chain Handoff Spec, when-to-chain decision criteria, decomposition trade-offs [VERIFIED]
- `WRTPRMPT-IN01-SC-MUSK-PEBP`: https://musketeerstech.com/blogs/prompt-engineering-best-practices/ - 10 best practices for 2026, operating manual metaphor, context as budget [VERIFIED]
- `WRTPRMPT-IN01-SC-TECH-PECG`: https://techsy.io/en/blog/prompt-engineering-for-coding - 7 coding prompt patterns, plan-first, test-first, config vs task separation [VERIFIED]
- `WRTPRMPT-IN01-SC-KDNG-10RL`: https://www.kdnuggets.com/10-rules-for-getting-better-results-from-ai-coding-agents - 10 rules for AI coding agents, specification quality, feedback loops [VERIFIED]
- `WRTPRMPT-IN01-SC-JYNG-TDGR`: https://jyoung.dev/blog/task-decomposition-for-ai-coding-agents/ - Task graph decomposition, validated handoffs, static decomposition risks [VERIFIED]

**Internal Sources:**
- `WRTPRMPT-IN01-SC-LANA-PFMT`: `e:\Dev\Lana-V1\docs\PROMPT_FILE_FORMAT.md` - Prompt queue file format (fences, separators, commentary) [VERIFIED]
- `WRTPRMPT-IN01-SC-GRUC-IN01`: `Docs/Concepts/_INFO_GRUC_GUIDES_RULES_CHECKS.md` - GRUC content boundaries (GUIDE vs RULES vs CHECKS) [VERIFIED]

## Document History

**[2026-08-31 21:32]**
- Initial research document created
