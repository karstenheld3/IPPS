# INFO: Devin Fusion Harness

**Doc ID**: DVNFUSION-IN01
**Goal**: Explain what Devin Fusion is, how it works, how it saves tokens, and what techniques it uses

**Depends on:**
- None

**Does not depend on:**
- `_INFO_ANTBLGTRNS-*` (different research scope; Anthropic blog analysis, not Cognition)

## Summary

- **What it is**: Fusion is a multi-model agent harness inside Devin (Desktop and CLI) that runs two parallel agents — a frontier "lead" model and a cheaper "sidekick" model — to maintain frontier-level coding performance at significantly lower cost `[VERIFIED]`
- **Who made it**: Cognition (cognition.com), the company behind Devin, the autonomous AI software engineer `[VERIFIED]`
- **Announcement timeline**: Originally announced June 29, 2026 as "Devin Fusion" for Devin Cloud (date per third-party source eesel.ai); expanded to Devin Desktop and CLI on September 11, 2026 `[VERIFIED]`
- **Cost savings**: Up to 60% lower cost on FrontierCode benchmarks (originally reported 35%, updated to 60% on FrontierCode 1.1 Extended data); up to 39% more efficient compared to other model harnesses across major coding benchmarks `[VERIFIED]`
- **Recommended pairing**: Fable 5.1 (lead) + SWE-2 (sidekick); GPT-6 Astra + SWE-2 also tested `[VERIFIED]`
- **Core technique 1 — Sidekick architecture**: Two parallel agents each maintain their own persistent, cached context. The lead delegates bounded tasks via plain-language briefs; the sidekick executes and reports back. No full conversation context is passed between them `[VERIFIED]`
- **Core technique 2 — Dynamic mid-session routing**: Lightweight classifiers during execution signal when to switch models. Model switches happen during context compaction (which triggers a cache miss anyway), so the switch adds no additional cache penalty beyond what compaction already costs `[VERIFIED]`
- **Key insight — Price per task, not price per token**: More expensive models can make the system cheaper because frontier models are more token-efficient, delegate earlier, and require fewer review rounds `[VERIFIED]`
- **Availability**: Paid Devin plans; CLI 3000.10.20+ and Desktop 3.10.0+; free and trial tiers excluded `[VERIFIED]`

## What Is Fusion

Fusion is a **multi-model agent harness** — the scaffolding around language models that turns them into coding agents (the loop that reads codebases, plans, calls tools, runs tests, decides next steps). Traditional harnesses run this loop on a single model. Fusion runs it across two models simultaneously `[VERIFIED]`.

### Key terminology

- **Harness**: The agent scaffolding — tool loop, context management, planning, execution. Devin has always been Cognition's harness for autonomous software work. Fusion changes how that loop runs: across two models instead of one `[VERIFIED]`
- **Lead** (formerly "main agent"): The frontier model that owns the session. Handles planning, ambiguity interpretation, delegation, and final review. The user always interfaces with the lead `[VERIFIED]`
- **Sidekick**: A cost-effective model paired with the lead. Receives bounded briefs, explores code, implements changes, runs tests, reports results. Has its own persistent context and tools `[VERIFIED]`
- **Fusion**: The overall architecture combining lead + sidekick + dynamic routing. Not a standalone model, editor, or subscription — it is a harness configuration inside Devin `[VERIFIED]`

### What Fusion is NOT

- Not a standalone model `[VERIFIED]`
- Not a separate editor or IDE `[VERIFIED]`
- Not a separate subscription — it is a feature within Devin `[VERIFIED]`
- Not simple model routing (picking one model per task at the start) `[VERIFIED]`

## The Problem Fusion Solves

### Why model routing alone is insufficient

Model routing seems attractive: let cheaper models handle easy tasks, reserve costly models for serious reasoning. But two fundamental problems make naive routing impractical `[VERIFIED]`:

1. **The initial prompt doesn't reveal task difficulty**: "Fix xyz bug" could be a one-line edge case or could require rearchitecting your entire product. You can't know until you've investigated the code `[VERIFIED]`
2. **Switching models mid-task breaks prompt caches**: When you switch models, you incur cache misses, paying full price for frontier model context re-processing. This defeats the purpose of routing `[VERIFIED]`

### The "Smart Friend" / "Advisor" tool problem

Earlier approaches (Cognition's "Smart Friend" tool, Anthropic's similar "Advisor" tool) gave one model a tool to query another model for advice. The catch: upon every call to the other model, the context for the task is not shared in a way that is cached, and you pay a very expensive price every time `[VERIFIED]`.

Fusion sidesteps this by having both agents maintain their own persistent, cached contexts. Delegation doesn't trigger a costly context re-send `[VERIFIED]`.

## The Fusion Architecture

### Two parallel agents with independent contexts

```
┌─────────────────────────────────────────────────────────┐
│                    Devin Session                        │
│                                                         │
│  ┌──────────────────┐       ┌──────────────────────┐    │
│  │   LEAD AGENT     │       │   SIDEKICK AGENT     │    │
│  │   (frontier $)   │       │   (cost-effective $) │    │
│  │                  │       │                      │    │
│  │ - Planning       │ brief │ - Explores code      │    │
│  │ - Ambiguity      │──────>│ - Implements changes │    │
│  │ - Delegation     │       │ - Runs tests         │    │
│  │ - Final review   │<──────│ - Reports results    │    │
│  │ - Commits        │ result│                      │    │
│  │                  │       │                      │    │
│  │ Own persistent   │       │ Own persistent       │    │
│  │ cached context   │       │ cached context       │    │
│  └──────────────────┘       └──────────────────────┘    │
│                                                         │
│  User interacts ONLY with the lead agent                │
└─────────────────────────────────────────────────────────┘
```

### How delegation works

The lead writes a **handoff brief** in plain language — a bounded task with constraints and success criteria. The sidekick carries it out in its own context and reports back. The lead reviews the result and decides what happens next `[VERIFIED]`.

Key design principles:
- The lead should take **minimal actions** and only read what is absolutely necessary. By default it delegates and monitors, while making the significant decisions `[VERIFIED]`
- Instead of passing entire conversations between models, the lead and sidekick only exchange **briefs, results, and feedback** `[VERIFIED]`
- The sidekick doesn't need the lead's entire history to implement a change; the lead doesn't need every intermediate tool result to review the work `[VERIFIED]`
- Each agent builds its own persistent context, taking full advantage of **prompt caching** `[VERIFIED]`

### Why frontier intelligence stays in charge

The Fusion architecture ensures frontier intelligence is always in charge. The system doesn't assign tasks to a cheaper model hoping the routing decision was correct. The lead always reviews the work, identifies problems, and can take control back when the sidekick is out of its depth `[VERIFIED]`.

Since the lead model is in charge of the session, the user always interfaces with frontier intelligence for the best user experience. Many smaller models are becoming more capable but are still less polished as user-facing agents `[VERIFIED]`.

## How Fusion Saves Tokens

### Technique 1: Persistent Cached Contexts (Sidekick Architecture)

Both agents maintain their own persistent, cached contexts. This is the foundational token-saving mechanism:

- **No context re-sending on delegation**: Unlike "Smart Friend"/"Advisor" tools where each cross-model call re-sends full context at full price, Fusion's agents never share context. They exchange only briefs and results `[VERIFIED]`
- **Full prompt caching exploitation**: Each agent's context is independently cached, so repeated calls within each agent's session benefit from cache hits `[VERIFIED]`
- **5-minute cache expiry workaround**: Cognition notes that "most cached inputs only have a 5-minute expiry" and invites readers to think about how they engineered around this (walden@cognition.ai for trade notes) `[VERIFIED]`

### Technique 2: Dynamic Mid-Session Routing

Lightweight classifiers run during task execution to signal when to switch models. The key cache-efficiency trick:

- Model switches happen **during context compaction** — a step that triggers a cache miss anyway `[VERIFIED]`
- Each compaction event is an opportunity to evaluate the situation and switch the model in charge, so the switch adds no additional cache penalty beyond what compaction already costs `[VERIFIED]`
- This means the system can even "upgrade" the sidekick model without going back to the main model, at no extra cache penalty `[VERIFIED]`
- Classifiers can escalate a struggling sidekick task back to the main agent, or swap models entirely `[VERIFIED]`

**Why this matters**: Compaction (summarizing/truncating the conversation to fit context limits) inherently invalidates the cache because the context content changes. This cache miss is unavoidable. If you switched models at a *different* time, you'd trigger a *second* cache miss on top of it. By piggybacking the model switch onto the compaction event, you avoid that second cache miss. The switch is "free" only in the sense of "no marginal additional cache penalty" — not "no cost at all" `[VERIFIED]`.

### Technique 3: Delegation as Cost Avoidance

The most significant token savings come from the lead **avoiding work entirely** by delegating it to the cheaper model:

From the Fable-vs-Opus analysis (3,000 evaluation sessions on FrontierCode 1.1):
- Fable's lead takes **11.5 turns per run** vs Opus's 26.5 turns `[VERIFIED]`
- Fable writes **a third of the output tokens** (6.1k vs 19.0k) `[VERIFIED]`
- Fable consumes **a third of the input tokens** `[VERIFIED]`
- In **81% of Fable-led runs**, the lead never makes a single code edit. For Opus, that's true for only 24% of runs `[VERIFIED]`
- In **13% of Fable-led runs**, the lead never even reads a repo file itself `[VERIFIED]`

### Technique 4: Early Delegation

Fable's first handoff comes early. Opus often delegates late, after a long stretch of solo exploration and implementation — by then, the design decisions are made, the important files are in its context, and the expensive work is done `[VERIFIED]`.

A typical Fable-led run: a few reconnaissance actions on the repo, then one spec-quality brief delegating the entire implement + test + lint loop, then one `git show` to review the diff, and a commit `[VERIFIED]`.

A typical Opus-led run: 20-45 turns of solo exploration, design, and implementation, and one late handoff for the mechanical tail `[VERIFIED]`.

### Technique 5: Constraint-Rich Briefs

Fable's handoffs enumerate constraints, edge cases, and a definition of "done". This saves itself effort while enabling the sidekick to cheaply and correctly complete the implementation `[VERIFIED]`.

Example: A hashing task required O(1) in pointer length. Opus implemented it by hand, never wrote the requirement down, forgot the constraint, and shipped a linear-time implementation (scored 25). Fable delegated using high-level constraints — its brief said "operator() must be O(1) in pointer length: NO full token scan" — and the sidekick implemented it successfully (scored 94) `[VERIFIED]`.

## The Counterintuitive Finding: Expensive Models Can Be Cheaper

### Price per task, not price per token

One of Cognition's key findings: using more expensive models can make the entire system cheaper. This applies to both the lead and the sidekick. Price per token is only part of the equation because frontier models are increasingly more token-efficient and more efficient in how much back-and-forth work the lead and sidekick create for each other `[VERIFIED]`.

### Fable vs Opus as lead

Fable 5 nominally costs 2x more per token than Opus 4.8. In pure (non-Fusion) runs, Fable outscores Opus (60.8 vs 55.4) and costs more — better model, bigger bill `[VERIFIED]`. But with the same sidekick, Fable-led sessions cost **9% less on average** while scoring higher on FrontierCode `[VERIFIED]`.

The cost split analysis:
- Fable spends more on its sidekick ($0.27 more per run) but spends $0.45 less on itself `[VERIFIED]`
- Fable + Sidekick: $1.86/task, score 60.7 `[VERIFIED]`
- Opus + Sidekick: $2.04/task, score 54.6 `[VERIFIED]`
- Fable + Sidekick cuts cost by **54%** vs pure Fable, with score nearly unchanged `[VERIFIED]`

The difference is management style: Opus behaves like a **micromanager with an intern**; Fable is a **manager with a capable engineer** `[VERIFIED]`. Both leads delegate the same number of times — about 3 handoffs per run. What differs is when and what they delegate `[VERIFIED]`.

### Stronger sidekicks are cheaper overall

Using SWE-2 ($0.75/Mtok, +275% more expensive) instead of GPT-5.6 Luna ($0.20/Mtok) doesn't substantially increase overall cost `[VERIFIED]`:

| Sidekick | List price | Astra Fusion score | Astra Fusion cost |
| --- | --- | --- | --- |
| GPT-5.6 Luna (high) | $0.20/Mtok | 62.0 | $2.39 |
| SWE-2 (medium) | $0.75/Mtok (+275%) | 63.4 | $2.34 (-2%) |

Two reasons:
1. **Stronger sidekicks are more turn and token efficient**: A lower price per token is less useful if the model needs more attempts to get the implementation right `[VERIFIED]`
2. **Stronger sidekicks make the lead cheaper**: Every mistake a stronger sidekick avoids saves the frontier model rounds of reasoning. Those savings often offset the higher cost of the sidekick itself `[VERIFIED]`

### Opus's expensive distrust

After delegation, both leads run the same cheap check (2-3 `git diff`/`git show` calls). But Opus doesn't stop there:
- Pulls sidekick's files back into its own context **2x more often** `[VERIFIED]`
- Makes **4x more corrective edits** at lead prices `[VERIFIED]`
- In extreme cases, reverts the sidekick's work and rewrites it by hand `[VERIFIED]`

Opus's distrust doesn't increase correctness. In some eval tasks, Fable's single diff review caught real sidekick bugs and opted for another cheap handoff instead of the lead-level rewrite Opus reaches for `[VERIFIED]`.

## Harness Tuning Per Model Pair

Picking a lead and sidekick is not enough. Instructions that help one pair work efficiently can make another perform worse. Cognition continuously tunes the harness around how models actually work together `[VERIFIED]`.

Three tuning dimensions:

1. **How much detail should the lead provide?**
   - Weaker sidekick: Fable 5.1 needs more prescriptive briefs. More lead tokens upfront, but avoids extra review rounds later `[VERIFIED]`
   - Stronger sidekick (SWE-2): Fable can leave more implementation details for the sidekick to figure out `[VERIFIED]`

2. **Should the sidekick be allowed to push back?**
   - Stronger sidekicks: encouraging pushback can catch mistakes in the lead's plan `[VERIFIED]`
   - Weaker sidekicks: allowing opinionated behavior hurts overall performance and cost `[VERIFIED]`

3. **What exploration should be delegated?**
   - Exploration needed for planning should NOT be delegated to a weaker sidekick — it shapes the lead's plan, and a weaker sidekick may not decide what information matters `[VERIFIED]`
   - Stronger sidekicks are encouraged to support initial exploration `[VERIFIED]`
   - Tuning this boundary remains an active area of research `[VERIFIED]`

## Benchmark Results

### FrontierCode 1.1 Extended

| Lead configuration | Fusion config | Score | Avg cost/task | Cost change |
| --- | --- | --- | --- | --- |
| Fable 5.1 alone | Fable 5.1 + SWE-2 | 63.5 (Fusion) / 63.6 (alone) | $1.67 (Fusion) / $2.68 (alone) | 38% lower |
| GPT-6 Astra alone | GPT-6 Astra + SWE-2 | 63.4 (Fusion) / 63.1 (alone) | $2.34 (Fusion) / $2.62 (alone) | 11% lower |

`[VERIFIED]` via NeoTeo analysis of Cognition's published data.

### Headline efficiency claim

Fusion is up to **39% more efficient** compared to other model harnesses across major coding benchmarks (Artificial Analysis Coding Agent Index v1.5, evaluated in partnership with Artificial Analysis and Vals AI) `[VERIFIED]`.

### Internal production usage

88% of merged PRs from internal Cognition users were driven entirely by the automated Fusion router `[VERIFIED]`.

## When Delegation Doesn't Help

Fusion's delegation strategy is not universally useful. It fails when tasks don't have delegable components `[VERIFIED]`:

- **Short tasks**: Only a handful of lead-model turns with nothing to delegate between deciding and shipping
- **Serial debugging**: Root-cause hunt is one long chain of judgments. The accumulated context IS the work

On these tasks, Fable barely delegates at all. The same judgment that writes a good brief also knows when not to write one. When a task offers nothing worth handing off, delegation has no leverage over cost `[VERIFIED]`.

In production, Fusion handles this at another layer: **delegation** controls what work stays with the expensive model, while **routing** decides whether the expensive model is involved at all `[VERIFIED]`.

## Good and Bad Sidekick Examples

From Cognition's representative FrontierCode task analysis `[VERIFIED]`:

**Good delegation candidates:**
- "Modernize search.js to ES6 and verify with the full make/Playwright/e2e suite" — Small rewrite, slow expensive test suite. Devin wrote the diff and handed off the slow test run
- "Rip out the OpenTracing integration across the Mattermost server, cleanly" — Mechanical removal across many files, few real judgment calls
- "Integrate LangChain4j's WebSocket MCP transport into Quarkus, reusing upstream" — Hard task but mostly mechanical: reuse what's upstream. Sidekick's changes needed no rework

**Poor delegation candidates:**
- "Handle JSON-Schema oneOf-with-const when generating Python models" — Medium feature Devin only partly solves
- "Add a team selector to the search bar (cross-team search), gated on a flag" — Hard, multi-file React/Redux feature graded on judgment calls. Devin delegated the coding and the subtle intent was lost

## Availability and Access

- **Devin CLI**: Install via `curl -fsSL https://cli.devin.ai/install.sh | bash` `[VERIFIED]`
- **Minimum versions**: CLI 3000.10.20+ and Desktop 3.10.0+ `[VERIFIED]`
- **Plan requirement**: Paid Devin plans; free and trial tiers excluded `[VERIFIED]`
- **Model selection**: When selecting Fusion, you pick two models instead of one — a frontier lead and a cost-effective sidekick `[VERIFIED]`

## Fable 5 Access Note

On June 12, 2026, access to Fable 5 was suspended in accordance with a US government directive (anthropic.com/news/fable-mythos-access). As of the local-fusion blog post (September 11, 2026), access had not been restored. Results with Fable 5 are based on measurements from before this suspension `[VERIFIED]`.

## Techniques Summary

| Technique | What it does | How it saves tokens |
| --- | --- | --- |
| Persistent cached contexts | Each agent keeps own cached context | No context re-sending on delegation; full prompt caching |
| Dynamic mid-session routing | Lightweight classifiers switch models during compaction | Switch piggybacks on compaction's unavoidable cache miss — no additional cache penalty |
| Delegation as cost avoidance | Lead avoids work by delegating to cheaper model | Fewer lead turns, fewer lead tokens, cheaper model does execution |
| Early delegation | Lead hands off after minimal reconnaissance | Prevents expensive lead from doing mechanical work |
| Constraint-rich briefs | Briefs enumerate constraints, edge cases, "done" definition | Sidekick gets it right first time; fewer review rounds |
| Stronger sidekick selection | Use SWE-2 over cheaper alternatives | Fewer attempts needed; less lead review/correction |
| Harness tuning per pair | Adjust detail level, pushback, exploration delegation per model pair | Optimizes interaction patterns for each specific model combination |

## Exclusions

- **FrontierCode benchmark methodology**: Not independently verified; relying on Cognition's published data and third-party analyses (eesel.ai, NeoTeo, AI Insiders)
- **Devin's internal harness implementation details**: Cognition deliberately omits implementation specifics (e.g., how they engineer around 5-minute cache expiry). Only architectural concepts are documented
- **Fable 5.1 model internals**: Fable is not generally available; no independent testing possible
- **SWE-2 model details**: Covered separately in `DVNSWE2` topic research
- **Cost figures**: Benchmark costs may not reflect real-world production costs; the 39% efficiency figure is an estimate based on pricing sidekick tokens at lead-model rates, not a controlled rerun

## Sources

- **DVNFUSION-IN01-SC-COGN-LCLFUS**: https://cognition.com/blog/local-fusion — Primary source: "Introducing Fusion in Devin Desktop & CLI" (September 11, 2026). Architecture overview, savings benchmarks, tuning details
- **DVNFUSION-IN01-SC-COGN-DVFUS**: https://cognition.com/blog/devin-fusion — Original announcement: "Devin Fusion: Frontier Performance at 60% Lower Cost" (June 29, 2026). Sidekick architecture, dynamic mid-session routing, cache miss engineering
- **DVNFUSION-IN01-SC-COGN-FABOP**: https://cognition.com/blog/making-fable-cheaper-than-opus — "Making Fable Cheaper Than Opus". Detailed cost analysis, 3,000 session study, delegation patterns, management style comparison
- **DVNFUSION-IN01-SC-NTEO-FUSION**: https://www.neoteo.com/en/cognition-fusion-brings-a-lead-and-sidekick-coding-workflow-to-devin — NeoTeo analysis (September 14, 2026). Benchmark table, availability details, version numbers
- **DVNFUSION-IN01-SC-EESL-FUSION**: https://www.eesel.ai/blog/devin-fusion — eesel AI analysis. Harness definition, sidekick mechanism explanation, cache miss analysis
- **DVNFUSION-IN01-SC-EESL-REV**: https://www.eesel.ai/blog/devin-fusion-review — eesel AI review. Technical assessment of dynamic routing and cache efficiency
- **DVNFUSION-IN01-SC-AINS-DUAL**: https://aiinsiders.net/article/cognition-ships-a-dual-agent-cost-cutter-for-devin — AI Insiders analysis. Architecture summary, economics argument
- **DVNFUSION-IN01-SC-COGN-EVENT**: https://cognition.com/events/whats-new-in-devin-08-05-26 — "What's New in Devin" event (August 5, 2026). Technical deep dive on Fusion and cost controls
- **DVNFUSION-IN01-SC-COGN-CLI**: https://cognition.com/blog/devin-for-terminal — Devin CLI announcement. Local agent with cloud handoff capability

## Document History

**[2026-09-15 10:33]**
- Fixed: "+275% cheaper per token" → "+275% more expensive" (F28 — reversed source meaning)
- Added: Vals AI as co-evaluator alongside Artificial Analysis
- Added: Pure-run scores (Fable 60.8 vs Opus 55.4) to counterintuitive finding section
- Added: "3 handoffs per run" statistic to management style section
- Added: Third-party source attribution for June 29 announcement date

**[2026-09-15 10:30]**
- Initial research document created from cognition.com/blog/local-fusion and linked sources
