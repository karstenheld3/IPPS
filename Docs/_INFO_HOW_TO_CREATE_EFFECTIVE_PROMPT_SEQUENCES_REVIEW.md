# _INFO_HOW_TO_CREATE_EFFECTIVE_PROMPT_SEQUENCES_REVIEW.md

**Doc ID**: PRMTSCN-IN02-RV01
**Goal**: Document potential issues, risks, and suggestions for improvement
**Timeline**: Created 2026-09-12, Updated 0 times (2026-09-12 - 2026-09-12)
**Reviewed**: 2026-09-12 14:45
**Context**: Critique of `_INFO_HOW_TO_CREATE_EFFECTIVE_PROMPT_SEQUENCES.md` (PRMTSCN-IN02) — how-to guide for self-contained prompt sequences

## Table of Contents

1. [Critical Issues](#critical-issues)
2. [High Priority](#high-priority)
3. [Medium Priority](#medium-priority)
4. [Low Priority](#low-priority)
5. [Industry Research Findings](#industry-research-findings)
6. [Recommendations](#recommendations)
7. [Document History](#document-history)

## Critical Issues

### `PRMTSCN-RV-001` Token budget claims are model-dependent and presented as universal

- **Location**: Section 7.1, line 196
- **What**: The document states "Optimal context per prompt: 2,000-8,000 tokens" and "Monolithic prompts at 30,000-50,000 tokens cause models to lose track of what matters" as universal facts. These ranges are model-dependent. Frontier models with 200K+ context windows handle 30K tokens differently than models with 8K windows. The lost-in-the-middle effect (Liu et al., TACL 2024) is about information position within context, not total context size. The document conflates two distinct phenomena: context window overflow (hard limit) and attention degradation (positional bias).
- **Risk**: Readers may over-split tasks that a single prompt could handle on a frontier model, adding coordination overhead and failure surfaces without quality benefit. Conversely, readers using small-context models may treat 8,000 tokens as safe when attention degradation starts earlier on those models.
- **Evidence**: Research from Liu et al. (ACL Anthology, TACL 2024) documents a U-shaped accuracy curve across context position, not total size. Anthropic's platform documentation recommends reserving 15-20% of context budget for response and safety margin, implying the budget is relative to window size, not a fixed range.
- **Suggested action**: Qualify the token ranges with model context window size. Replace fixed ranges with percentage-of-window guidance (e.g., "target 10-30% of context window per prompt"). Cite the positional degradation research separately from total-size limits.

### `PRMTSCN-RV-002` Idempotency rule 2 assumes deterministic LLM outputs

- **Location**: Section 9.3, rule 2, line 258
- **What**: "Check for output artifacts before creating them: if the file exists and matches expected content, skip; if it exists but is incomplete, overwrite; if it does not exist, create." The rule assumes the agent can determine whether a file "matches expected content." LLM outputs are non-deterministic (Section 2.3 acknowledges this). The agent cannot compare its output against a golden standard because the output IS the generation. There is no reference to compare against.
- **Risk**: An agent re-running a prompt may see an existing file, attempt to verify it "matches expected content," and either: (a) always skip because the file looks plausible (false positive — unverified output treated as valid), or (b) always overwrite because the content doesn't match the agent's new generation (defeating idempotency entirely). Both outcomes violate the idempotency goal.
- **Evidence**: Research on semantic rollback attacks (ACRFence, arXiv 2603.20625) shows that even at temperature=0, floating-point rounding in GPU kernels produces different token sequences across runs. The agent's re-generated output will differ from the original, making content comparison unreliable.
- **Suggested action**: Replace "matches expected content" with a structural check: file exists AND passes a validation predicate (e.g., valid JSON schema, required sections present, non-empty). The agent checks structural integrity, not semantic equivalence. If structure is valid, skip. If structure is invalid, the file was from an interrupted run — overwrite.

### `PRMTSCN-RV-003` Write-then-verify rule creates an idempotency gap

- **Location**: Section 9.3, rule 6, line 262
- **What**: "Write output to a file first, then verify it. If verification fails, the file exists for inspection." Combined with rule 2 (skip if file exists and matches expected content), this creates a gap: if the prompt is interrupted after writing but before verifying, the file exists with unverified content. The next run sees the file, checks it (rule 2), and if the structural check passes, skips — treating unverified output as valid.
- **Risk**: Unverified output from an interrupted prompt is promoted to "done" status without passing verification criteria. This is the exact failure the end-of-prompt protocol (Section 5) is designed to prevent, but the idempotency rules bypass it.
- **Evidence**: The ACRFence paper identifies this as "Action Replay" — a checkpoint-restore cycle that produces unverified side effects. The agent writes, crashes, resumes, sees the file, and treats it as complete.
- **Suggested action**: Distinguish "written" from "verified" states. Use a two-file pattern: write to `output.tmp`, verify, then atomically rename to `output.md`. The next run checks for `output.md` (verified), not `output.tmp` (unverified). If only `output.tmp` exists, the previous run was interrupted — re-run the prompt.

## High Priority

### `PRMTSCN-RV-004` No guidance on maximum chain length

- **Location**: Section 1, lines 33-49
- **What**: The document provides guidance on when to split into a sequence and when to keep as a single prompt, but never addresses maximum sequence length. Research shows error rates compound across steps: a 5% per-step error rate over 10 steps yields a 40% end-to-end failure rate. Industry consensus identifies 5-6 sequential steps as a practical ceiling before error compounding makes chains unreliable.
- **Risk**: A reader designs a 15-prompt sequence following all the document's patterns. Each prompt is well-structured, self-contained, and idempotent. But the chain as a whole has a 54% failure rate (1 - 0.95^15), making it unreliable for production use. The document gives no warning.
- **Evidence**: FutureAGI research identifies "length ceiling: 5 to 6 sequential steps. Past that, split into sub-chains or parallel branches." Nesyona notes that "many prompts that operators reflexively chain would perform equally well as a single, well-structured prompt."
- **Suggested action**: Add a subsection on chain length limits. Recommend: (a) keep sequences under 6 steps, (b) for longer workflows, split into sub-chains with checkpoints between them, (c) calculate expected end-to-end reliability from per-step error rates.

### `PRMTSCN-RV-005` Model version drift between prompt executions

- **Location**: Not addressed anywhere in the document
- **What**: The document assumes the same model behavior across all prompts in a sequence. In production, model providers update checkpoints between executions. A sequence started with Model A v1 may resume with Model A v2, which interprets prompts differently. This is a documented production failure mode called "version drift."
- **Risk**: A prompt sequence that passed all verification criteria during development fails silently after a model update because the new model version interprets the prompt differently. The start-of-prompt protocol detects step completion, not model compatibility.
- **Evidence**: Research from Vinay 2025 (arXiv) catalogs version drift as a distinct failure mode. The LangChain 0.3 production outage (johal.in, 2026) was caused by a framework version change that silently dropped context — the same class of failure as model version drift.
- **Suggested action**: Add a subsection on version drift. Recommend: (a) pin model versions in the prompt sequence metadata, (b) include a model version check in the start-of-prompt protocol, (c) re-test the full sequence when the model version changes, (d) document which model version each prompt was validated against.

### `PRMTSCN-RV-006` Card update race condition on interruption

- **Location**: Section 3.4, lines 103-105
- **What**: "Each prompt reads AND updates the cards it needs. When a prompt discovers new information, corrects a card error, or completes a unit, it updates the relevant card in the same prompt." If a prompt is interrupted between reading a card and updating it, the card may contain stale state. If the prompt is interrupted mid-update (partial write), the card is in a broken state.
- **Risk**: The next prompt reads a card that was partially updated or not updated at all. It makes decisions based on stale or corrupt card state. The idempotency rules (Section 9.3) address file artifacts but not card files specifically.
- **Evidence**: The filesystem-as-context pattern (Agent Patterns Catalog) identifies "stale or contradictory files accumulate unless the agent prunes them" as a known consequence.
- **Suggested action**: Apply the write-to-temp-then-rename pattern (Section 9.3, rule 3) to card updates. Write the updated card to `__CARD_XX.tmp`, verify, then atomically rename. Add a card integrity check to the start-of-prompt protocol: if any card file is malformed, report and stop.

## Medium Priority

### `PRMTSCN-RV-007` Authority hierarchy places "suggested changes" above "spec"

- **Location**: Section 3.3, line 100
- **What**: "source document > suggested changes > spec > clause map > existing specs > product code." "Suggested changes" (unreviewed, generated by a prompt) ranks above "spec" (reviewed, approved). This means a prompt's suggestion overrides an approved specification.
- **Risk**: A prompt generates a suggestion that contradicts the spec. The next prompt follows the suggestion instead of the spec, introducing an unreviewed design change. The spec is the reviewed authority; treating unreviewed suggestions as higher authority undermines the review process.
- **Evidence**: SOCAS-10 (gaps in reasoning) — the hierarchy assumes suggestions are always correct, which is an unverified assumption.
- **Suggested action**: Move "suggested changes" below "spec" in the hierarchy: source document > spec > clause map > existing specs > suggested changes > product code. Suggestions require human review before overriding specs.

### `PRMTSCN-RV-008` "Treat earlier conversation as compacted" is ambiguous

- **Location**: Section 2.1, line 57; Section 2.2, line 64
- **What**: The phrase "Treat earlier conversation as compacted" is used as a directive but never defined. "Compacted" could mean: (a) summarized and available in a file, (b) dropped entirely, (c) available but not in context. The agent's interpretation determines whether it searches for prior conversation artifacts or assumes they don't exist.
- **Risk**: An agent interpreting "compacted" as "summarized and available" may search for a summary file that doesn't exist, wasting tokens. An agent interpreting it as "dropped" may skip checking progress files, defeating the resume protocol.
- **Evidence**: SOCAS-02 (ambiguous naming and wording) — key directive term without clear definition.
- **Suggested action**: Define "compacted" explicitly on first use: "Treat earlier conversation as compacted (prior conversation is not in context; reconstruct state from files, not from memory)."

### `PRMTSCN-RV-009` No per-step testing strategy before chain assembly

- **Location**: Section 10 (Prompt Structure Template), lines 283-302
- **What**: The document provides a template for individual prompts and verification criteria, but doesn't address how to test individual prompts in isolation before assembling them into a chain. Industry practice (STEP framework, FAPO) emphasizes per-step evaluation: test each prompt against 3-5 inputs, score structural quality, and validate output format before chaining.
- **Risk**: A flaw in prompt 3 is only discovered after prompts 1 and 2 execute successfully. The chain fails at step 3, requiring re-running from the beginning (or fixing prompt 3 and re-running 1-2 to test it). Per-step testing catches the flaw before chain assembly.
- **Evidence**: PromptEval's STEP framework: "Run the prompt live against 3-5 specific inputs" before deployment. FAPO: "records the inputs, outputs, and logs of each step in the pipeline" for per-step attribution.
- **Suggested action**: Add a subsection on per-step testing. Recommend: (a) test each prompt in isolation with 3-5 representative inputs before chaining, (b) validate output format against the Chain Handoff Spec, (c) only assemble the chain after all prompts pass individual testing.

### `PRMTSCN-RV-010` Cost guard rule doesn't account for cache invalidation

- **Location**: Section 9.3, rule 4, line 260
- **What**: "Cache results to files so a re-run reads the cache instead of re-calling the API." This works for deterministic APIs but not for LLM calls where the output may need to change based on updated context. If prompt 1's output is cached and prompt 2 updates a card that prompt 1 read, the cached output is now stale.
- **Risk**: A re-run uses a cached LLM output that was based on card state that has since changed. The cached output is inconsistent with the current card state, introducing a silent inconsistency.
- **Evidence**: The filesystem-as-context pattern notes "stale or contradictory files accumulate unless the agent prunes them."
- **Suggested action**: Add cache invalidation criteria: (a) cache only results that don't depend on card state, (b) if the result depends on card state, include a card content hash in the cache key, (c) invalidate the cache when the card is updated.

## Low Priority

### `PRMTSCN-RV-011` Timeline field not updated after idempotency addition

- **Location**: Line 5
- **What**: Timeline says "Updated 0 times" but Document History shows two entries (14:38 and 14:40). The idempotency addition was an update.
- **Suggested action**: Update Timeline to "Updated 1 time (2026-09-12 - 2026-09-12)".

### `PRMTSCN-RV-012` Sources list includes background sources not cited in content

- **Location**: Section 12, lines 333-343
- **What**: Sources `PRMTSCN-IN02-SC-CCG-SMM`, `PRMTSCN-IN02-SC-JBN-SMM`, and `PRMTSCN-IN02-SC-APC-IRT` are listed but no content section discusses their findings. They were background research, not directly cited.
- **Suggested action**: Either cite each source's findings in a content section or mark them as "Background research" in the Sources section.

### `PRMTSCN-RV-013` ICM GitHub URL has typo in repository name

- **Location**: Section 3, line 72; Section 12, line 334
- **What**: The URL `https://github.com/jkilzi/Interpreted-Context-Methdology` contains "Methdology" (missing 'o' — should be "Methodology"). If this is the actual repo name, it's fine, but if it's a typo in the URL, the link is broken.
- **Suggested action**: Verify the URL resolves. If the repo name is intentionally "Methdology", no action needed. If it's a typo, fix the URL.

## Industry Research Findings

### Prompt Chaining Failure Modes

- **Pattern found**: Four boundary failures account for most production chain breaks: format drift, error propagation, context bleed, and silent truncation. Error rates compound: 5% per-step error over 4 steps = 18.5% end-to-end failure. 5-6 steps is the practical ceiling before sub-chain splitting is needed.
- **How it applies**: The document addresses format drift (Chain Handoff Spec, Section 8) and error propagation (safety layer, Section 8.1) but misses chain length limits (RV-004) and version drift (RV-005).
- **Source**: https://nesyona.com/articles/prompt-chaining-workflows, https://futureagi.com/blog/llm-tool-chaining-cascading-failures-production/, https://www.bestaiweb.ai/error-propagation-and-context-limits-the-technical-failure-modes-of-prompt-chaining/

### Idempotency for LLM Agents

- **Pattern found**: Idempotency must be owned by the orchestrator/runtime, not the model. The key must be derived from structural context `(agent_run_id, step_id, tool_name, business_scope)`, not from model arguments (which drift on re-generation). Even at temperature=0, GPU floating-point rounding produces different token sequences. ACRFence identifies "semantic rollback attacks" where checkpoint-restore produces different requests that servers accept as new.
- **How it applies**: The document's idempotency rules (Section 9.3) are prompt-level, not orchestrator-level. Rule 2's content comparison (RV-002) fails because LLM outputs are non-deterministic. The document needs to distinguish structural validation from semantic comparison.
- **Source**: https://tianpan.co/blog/2026/04/23/agent-idempotency-orchestration-contract, https://arxiv.org/pdf/2603.20625, https://blog.senseof.tech/2026/08/17/reliability-of-long-running-agents/

### File-Based State Management Alternatives

- **Pattern found**: Multiple approaches exist beyond the card system: Agent-Context-Card (passive projection, no model calls), InfiAgent (file-centric state with bounded reasoning context), filesystem-as-context (Agent Patterns Catalog). Key insight: filesystem memory degrades without active governance — duplicates, contradictions, and stale facts accumulate. Organization buys search economy but erodes for all but the strongest management agents.
- **How it applies**: The card system (Section 3) is one approach. The document presents it as THE approach without acknowledging alternatives or the governance burden. Card update conflicts (RV-006) are a specific instance of the general filesystem memory degradation problem.
- **Source**: https://github.com/chkrishna2001/Agent-Context-Card, https://arxiv.org/html/2607.26637, https://www.agentpatternscatalog.org/patterns/filesystem-as-context/, https://aclanthology.org/2026.findings-acl.1787.pdf

### Testing Strategies for Prompt Sequences

- **Pattern found**: STEP framework (Structural evaluation, Playground testing, Experimentation, Production iteration) — test each prompt with 3-5 inputs before chaining. FAPO optimizes multi-step pipelines by attributing failures to specific steps. Per-step evaluation catches flaws before chain assembly. Trajectory testing validates multi-step reasoning paths.
- **How it applies**: The document has no per-step testing guidance (RV-009). Verification criteria (Section 10 template) are per-prompt but don't address how to test before assembly.
- **Source**: https://prompt-eval.com/en/blog/how-to-test-and-iterate-ai-prompts, https://arxiv.org/html/2606.19605, https://www.openlayer.com/blog/agent-testing-complete-guide-validating-ai-systems

### Alternatives Considered

- **Agent-Context-Card (passive projection)**: No model calls for context management, deterministic projection, automatic task isolation. Pros: simpler than card system, no model overhead. Cons: requires host integration, not portable across agents.
- **InfiAgent (file-centric state)**: Strict separation of persistent state and bounded reasoning context. Pros: theoretically grounded, scales to infinite horizons. Cons: requires framework adoption, more complex than cards.
- **Filesystem-as-context (pattern)**: General pattern, not a specific implementation. Pros: framework-agnostic. Cons: no governance built in, stale files accumulate.

## Recommendations

### Must Do

- [ ] Fix idempotency rule 2 (RV-002): replace "matches expected content" with structural validation predicate
- [ ] Fix write-then-verify gap (RV-003): use two-file pattern (`.tmp` then rename) to distinguish written from verified
- [ ] Add chain length limit guidance (RV-004): recommend max 6 steps, sub-chain splitting for longer workflows
- [ ] Fix authority hierarchy (RV-007): move "suggested changes" below "spec"

### Should Do

- [ ] Add version drift section (RV-005): model version pinning, compatibility check in start-of-prompt protocol
- [ ] Add card update race condition handling (RV-006): apply write-to-temp-then-rename to card updates
- [ ] Define "compacted" on first use (RV-008): explicit definition, not ambiguous term
- [ ] Add per-step testing guidance (RV-009): test prompts in isolation before chain assembly
- [ ] Qualify token budget ranges with model context window size (RV-001)

### Could Do

- [ ] Add cache invalidation criteria (RV-010): card content hash in cache key
- [ ] Update Timeline field (RV-011)
- [ ] Cite or mark background sources (RV-012)
- [ ] Verify ICM GitHub URL spelling (RV-013)

## Reference

**Categories and Labels**: See FAILS_TEMPLATE.md for severity categories and assumption labels.

**File Naming**: Document review: `_INFO_HOW_TO_CREATE_EFFECTIVE_PROMPT_SEQUENCES_REVIEW.md`

**Management**: Create fresh each review. Can be discarded after issues addressed.

## Document History

**[2026-09-12 14:45]**
- Initial review created. 13 findings: 3 critical, 3 high, 4 medium, 3 low. Research covered prompt chaining failure modes, idempotency patterns, file-based state management alternatives, and testing strategies.
