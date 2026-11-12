# INFO: Quota Consumption Increase with Opus Models

**Doc ID**: QTACONSMM-IN01
**Goal**: Explain why users experience drastic quota consumption increases when using Opus models on Devin Desktop, and identify mitigations
**Version scope**: Devin Desktop 3.10.67+ / Opus 5.5 (Sep 22, 2026) / Opus 5 (Jul 24, 2026)
**Timeline**: Created 2026-10-20

**Depends on:**
- `_INFO_HOW_DEVIN_WORKS.md [DVDT-IN01]` for Devin Desktop architecture, model catalog, and pricing

## Summary

- **Opus 5.5 is cheaper per token than Opus 5** (20% less input/output, 60% less cache reads), but can consume **more quota at max effort** because it thinks more per turn [VERIFIED]
- **Credits → Quotas transition** (March 2026) changed the billing model from per-message to per-token. Long agent loops with growing context now cost more than fixed-credit messages did [VERIFIED]
- **Opus 5.5 at max effort** can exhaust its entire 128K output token budget on simple tasks, costing 1.2x more than Opus 5 at max effort [VERIFIED]
- **Fusion (Opus 5.5 lead + SWE-2 sidekick)** reduces quota consumption by 31-46% vs Opus 5.5 alone, with similar quality [VERIFIED]
- **Cache reads are the dominant cost** in agentic sessions. Opus 5.5 cache reads cost $0.20/M (60% less than Opus 5's $0.50/M), but sessions with 40+ turns still accumulate millions of cached tokens [VERIFIED]
- **SWE-2 free period ended Oct 15, 2026**. Post-free pricing: $3/$15/$0.30 per MTok (75% off through Dec 31, 2026). Still far cheaper than Opus 5.5 ($4/$20/$0.20) [VERIFIED]
- **Practical mitigations**: Use Fusion, lower effort to medium, use `/compact` and `/clear`, add `.devinignore`, keep rules short, link ChatGPT plan for GPT usage [VERIFIED]

## 1. Root Cause: Credits → Quotas Transition

The credits-to-quotas transition (March 2026) is the primary structural cause of perceived consumption increase. [VERIFIED]

**Old system (credits):**
- 1 prompt credit = 1 message, regardless of token count
- Model multipliers applied (e.g., Opus = 2 credits)
- Agent could take 50 tool calls in one message and it still cost 1 credit
- Monthly reset, no rollover

**New system (quotas):**
- Token-based daily/weekly budget
- Every tool call, every turn re-sends the full conversation context
- A 40-turn session with 70K average context = ~2.8M input tokens
- Cost scales with context size, session length, and model token price

A task that cost 1 credit under the old system can consume 200K+ tokens under quotas. The Devin docs provide a worked example: a single "Refactor @my_function" task with analysis, planning, and two file edits totals ~200K tokens. [VERIFIED]

Source: `https://docs.devin.ai/desktop/accounts/quota`

## 2. Opus 5.5 vs Opus 5: Token Efficiency

### 2.1 Per-Token Pricing

| Model | Input | Output | Cache Read | Cache Write |
| --- | --- | --- | --- | --- |
| Opus 5 | $5/M | $25/M | $0.50/M | $6.25/M |
| Opus 5.5 | $4/M | $20/M | $0.20/M | $5/M |
| Change | -20% | -20% | -60% | -20% |

Source: `https://platform.claude.com/docs/en/about-claude/pricing` [VERIFIED]

### 2.2 Per-Task Cost (Real Measurements)

Independent testing (Claude Code Camp, 12 tasks x 3 runs each):

| Model | Cost per task | Output tokens per task |
| --- | --- | --- |
| Opus 5 | $0.173 | 2,227 |
| Opus 5.5 | $0.088 | 1,434 |
| GPT-5.6 Sol | $0.225 | 2,521 |
| GPT-6 Sol | $0.118 | 2,178 |

Opus 5.5 wrote 36% fewer tokens per task. Combined with the 20% price cut, per-task cost dropped ~49%. [VERIFIED]

Source: `https://www.claudecodecamp.com/p/why-new-models-get-cheaper`

### 2.3 The Max Effort Trap

At max effort, Opus 5.5 costs **more** than Opus 5:

| Effort | Opus 5 | Opus 5.5 | Ratio |
| --- | --- | --- | --- |
| Medium | $2,732 | $1,627 | 0.60x |
| High | $4,332 | $2,172 | 0.50x |
| Max | $7,275 | $8,708 | 1.20x |

At max effort, Opus 5.5 thinks much longer. Simon Willison reported it exhausted the entire 128K output token budget on a simple SVG drawing task without answering. [VERIFIED]

Source: Artificial Analysis via `https://www.claudecodecamp.com/p/why-new-models-get-cheaper`

### 2.4 Thinking Cannot Be Disabled

Opus 5.5 removed the ability to disable thinking. On Opus 5, `thinking: {"type": "disabled"}` was accepted. On Opus 5.5, it returns a 400 error. Thinking is always on, controlled only by the `effort` parameter. [VERIFIED]

Source: `https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5`

### 2.5 Default Effort Changed

Opus 5 defaulted to `high` effort. Opus 5.5 defaults to `medium`. If a user or harness carries over the `high` or `max` setting from Opus 5, Opus 5.5 thinks more per turn at that level than Opus 5 did. [VERIFIED]

Source: `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5`

## 3. Why Agentic Sessions Are Expensive

### 3.1 The Resend Problem

Every turn in an agent loop re-sends the full conversation context. A session that grows from 20K to 120K tokens over 40 turns processes ~2.8M input tokens total. At 90% cache hit rate, that costs ~$1.62 in input alone (Opus 5.5 prices). At 0% cache hit, it costs $11.20. [VERIFIED]

Source: `https://claude.dev/blog/what-a-task-costs-on-opus-5-5/`

### 3.2 Cache Hit Rate Dominates Cost

| Cache hit rate | Input cost (2.8M tokens, Opus 5.5) |
| --- | --- |
| 0% | $11.20 |
| 90% | $1.62 |
| 96% | $0.99 |

No other setting moves input cost this much. Breaking the cache (switching models, changing effort mid-session) forces cache rewrites at full input price. [VERIFIED]

Source: `https://claude.dev/blog/what-a-task-costs-on-opus-5-5/`

### 3.3 Output Tokens Dominate Total Cost

On Opus 5.5, an output token costs 100x a cache read. A typical 60K output token task costs $1.20 in output, equivalent to reading 6M tokens from cache. Thinking is billed as output. Higher effort = more thinking = more cost. [VERIFIED]

Source: `https://claude.dev/blog/what-a-task-costs-on-opus-5-5/`

### 3.4 Rules and Context Add Fixed Cost

- Always-on rules load on every request (fixed cost per turn)
- A 2,000-character testing guide at always-on = ~500 tokens added to every turn
- Over 40 turns, that's 20K extra tokens (mostly cache reads, but still billed)
- Retrieved memories and codebase index hits add input tokens per turn
- `.devinignore` excludes paths from indexing, reducing retrieval cost [VERIFIED]

Source: `https://tokenade.net/en/articles/reduce-devin-desktop-token-usage`

## 4. Fusion as Primary Mitigation

### 4.1 How Fusion Reduces Consumption

Fusion pairs a frontier lead (planning/review) with a cost-effective sidekick (execution). The lead does less typing, the sidekick does the bulk work at lower token cost. [VERIFIED]

### 4.2 Benchmark Savings

| Benchmark | Lead alone | Fusion (lead + SWE-2) | Savings |
| --- | --- | --- | --- |
| FrontierCode 1.1 Ext | Fable 5.1: $2.68 | $1.67 | -38% |
| FrontierCode 1.1 Ext | Astra: $2.62 | $2.34 | -11% |
| DeepSWE 1.1 | Fable 5.1: $14.63 | $7.88 | -46% |
| DeepSWE 1.1 | Astra: $7.88 | $4.69 | -40% |
| Terminal-Bench 4 | Fable 5.1: $17.46 | $13.37 | -23% |
| Vals Code Migration | Fable 5.1: $70.97 | $42.00 | -41% |

Source: `https://cognition.com/blog/local-fusion` [VERIFIED]

### 4.3 Real-World Reports

- User "ilikekillnerds" (Oct 14, 2026): Opus 5.5 + SWE-2 Fusion barely moves weekly quota. "I'll get to Thursday and I've used a sliver of the allowance." [VERIFIED]
- User "CtrlAltDwayne" (Oct 3, 2026): SWE-2 + Opus 5.5 combo "barely uses 10% of weekly quota" [VERIFIED]
- User on X (Oct 10, 2026): "Opus 5.5 (high) as lead, SWE-2 (medium) for execution. Hours of quality work, only 15% of my weekly quota used." [VERIFIED]
- Cognition's own data: Fusion runs ~36% cheaper than same lead model alone in Claude Code [VERIFIED]

### 4.4 SWE-2 Free Period Ended

SWE-2 was free for self-serve through Oct 15, 2026. Post-free pricing:
- 75% off list price through Dec 31, 2026: $0.75/$3.75/$0.075 per MTok
- List price from Jan 1, 2027: $3/$15/$0.30 per MTok
- Still far cheaper than Opus 5.5 ($4/$20/$0.20) for execution work [VERIFIED]

Note: Some of the "barely uses quota" reports were during the free SWE-2 period. Post-Oct 15, SWE-2 consumes quota, but at a fraction of Opus cost. [VERIFIED]

Source: `https://docs.devin.ai/desktop/models`

## 5. Practical Mitigations

### 5.1 Model and Mode Selection

- **Use Fusion** (Opus 5.5 lead + SWE-2 sidekick) for everyday tasks. 31-46% quota savings vs Opus alone [VERIFIED]
- **Lower effort to medium** (Opus 5.5 default). Medium matches or exceeds Opus 5 at high on coding tasks [VERIFIED]
- **Reserve max effort** for tasks where you've measured a quality gain. Max can cost 1.2x more than Opus 5 at max [VERIFIED]
- **Use SWE-2 or SWE-1.7 standalone** for routine tasks. Free or low-cost [VERIFIED]
- **Use Plan mode** (`/plan`) for research. Read-only, no edit-retry loops [VERIFIED]
- **Use Ask mode** (`/ask`) for one-off questions. Short exchange instead of agent run [VERIFIED]

### 5.2 Session Management

- **Use `/compact`** to force conversation compaction when sessions grow long. Replaces history with summary [VERIFIED]
- **Use `/clear` or `/new`** to start fresh. Next turn starts from base prompt, not accumulated context [VERIFIED]
- **Avoid unnecessarily long sessions**. Each turn re-sends full context [VERIFIED]
- **Split big projects into sub-tasks** across parallel sessions. Shorter context per session [VERIFIED]
- **Delegate clearly scoped tasks** with well-defined end goals [VERIFIED]

### 5.3 Context and Rules

- **Add `.devinignore`** for generated, vendored, or bulky paths. Excludes from indexing and retrieval [VERIFIED]
- **Move rules off always-on**. Use glob or model-decision triggers for rules that only apply to specific files [VERIFIED]
- **Keep rules short**. 12K character cap per file. Every always-on rule adds tokens to every request [VERIFIED]
- **Prune stale memories**. Retrieved memories occupy context even if creating them is free [VERIFIED]
- **Be precise with prompts**. Remove unnecessary context. Shorter prompts = fewer tokens per turn [VERIFIED]

### 5.4 Billing Optimization

- **Link ChatGPT plan** (Go/Plus/Pro). GPT model usage billed to ChatGPT, not Devin quota. Pro/Max/Teams only [VERIFIED]
- **Stay on single model per task**. Switching models breaks cache, forcing full-price re-reads [VERIFIED]
- **Avoid fast/priority variants**. SWE-1.5 Fast and fast Opus variants cost more [VERIFIED]
- **Use mini models** (Haiku, GPT 5.2 Mini, Kimi K2.5) for simple tasks [VERIFIED]

## 6. Exclusions

- This document does not cover Enterprise ACU billing mechanics in detail (see `https://docs.devin.ai/admin/billing/usage`)
- Does not cover Devin Cloud session pricing (VM time, cloud agent costs)
- Does not cover voice mode quota impact in detail (see `https://docs.devin.ai/work-with-devin/voice-mode`)
- Does not cover Cascade-specific billing (legacy, same pricing model as Devin Local per FAQ)
- Per-token prices are current as of 2026-10-20 and subject to change. Check `https://devin.ai/pricing` for current rates

## Sources

- `QTACONSMM-IN01-SC-DVNDC-QTA`: https://docs.devin.ai/desktop/accounts/quota - Quota-based usage docs with token pricing example [VERIFIED]
- `QTACONSMM-IN01-SC-DVNDC-USG`: https://docs.devin.ai/desktop/accounts/usage - Plans and usage docs [VERIFIED]
- `QTACONSMM-IN01-SC-DVNDC-MDL`: https://docs.devin.ai/desktop/models - AI Models docs with per-model pricing [VERIFIED]
- `QTACONSMM-IN01-SC-DVNDC-UTL`: https://docs.devin.ai/admin/billing/usage - Usage metering docs (what counts toward consumption) [VERIFIED]
- `QTACONSMM-IN01-SC-DVNAI-PRC`: https://devin.ai/pricing - Current pricing page [VERIFIED]
- `QTACONSMM-IN01-SC-CLAUDE-OP55`: https://platform.claude.com/docs/en/about-claude/pricing - Claude model pricing table [VERIFIED]
- `QTACONSMM-IN01-SC-CLAUDE-WN55`: https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5 - Opus 5.5 what's new (thinking always on, effort changes) [VERIFIED]
- `QTACONSMM-IN01-SC-CLAUDE-PMP55`: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5 - Prompting Opus 5.5 (effort calibration, max_tokens guidance) [VERIFIED]
- `QTACONSMM-IN01-SC-CLAUDE-STC`: https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost - Thinking steering and cost control [VERIFIED]
- `QTACONSMM-IN01-SC-CLAUDE-OPT`: https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence - Cost optimization with max_tokens caps and effort levels [VERIFIED]
- `QTACONSMM-IN01-SC-CLDEV-WTC`: https://claude.dev/blog/what-a-task-costs-on-opus-5-5/ - What a task costs on Opus 5.5 (turns, cache reads, output tokens) [VERIFIED]
- `QTACONSMM-IN01-SC-CCCMP-WNM`: https://www.claudecodecamp.com/p/why-new-models-get-cheaper - Why new models get cheaper (per-task cost comparison) [VERIFIED]
- `QTACONSMM-IN01-SC-CGNTN-FUS`: https://cognition.com/blog/local-fusion - Devin Fusion announcement with benchmark savings [VERIFIED]
- `QTACONSMM-IN01-SC-CGNTN-EFF`: https://devin.ai/blog/more-efficient-devin - Devin 30-40% more cost-efficient announcement [VERIFIED]
- `QTACONSMM-IN01-SC-DVNAI-OP55`: https://devin.ai/blog/claude-opus-5-5 - Opus 5.5 in Devin announcement [VERIFIED]
- `QTACONSMM-IN01-SC-ILKN-SWE2`: https://ilikekillnerds.com/2026/10/14/devin-swe-2-is-my-daily-driver/ - Real-world Fusion usage report [VERIFIED]
- `QTACONSMM-IN01-SC-AGIH-BV`: https://agihunt.info/en/p/1a101e31c61aafa35f4435d94e6 - Devin best-value subscription report [VERIFIED]
- `QTACONSMM-IN01-SC-TKNDE-RED`: https://tokenade.net/en/articles/reduce-devin-desktop-token-usage - Token reduction guide (.devinignore, rules, modes) [VERIFIED]
- `QTACONSMM-IN01-SC-ENGF-CHG`: https://engineerfoodie.in/blog/devin-desktop-formerly-windsurf/ - Credits to quotas transition explanation [VERIFIED]
- `QTACONSMM-IN01-SC-BLDR-CMP`: https://www.benchleader.com/compare/claude-opus-5-vs-claude-opus-5-5 - Opus 5 vs 5.5 price and speed comparison [VERIFIED]
- `QTACONSMM-IN01-SC-MINDP-MAX`: https://mindpattern.ai/f/26733 - Opus 5.5 max effort 128K budget exhaustion report [VERIFIED]
- `QTACONSMM-IN01-SC-FBBNCH-DEV`: https://www.feedbackbench.com/agents/devin.md - Devin user feedback aggregation (Fusion quota reports) [VERIFIED]

## Document History

**[2026-10-20 10:20]**
- Initial research document created
