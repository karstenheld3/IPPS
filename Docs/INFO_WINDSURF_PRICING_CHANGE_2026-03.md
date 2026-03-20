<DevSystem MarkdownTablesAllowed=true />

# INFO: Windsurf Pricing Change Impact Analysis (March 2026)

**Doc ID**: WSRF-IN02
**Goal**: Analyze impact of Windsurf's new quota-based pricing on heavy users (500+ requests/day)

## Summary - CRITICAL FINDINGS

**Effective Date Status** [VERIFIED 2026-03-20]:
- **Announced**: Mar 19, 2026 (blog post)
- **Actual transition**: Mar 20, 2026 ~09:00 (recorded from dashboard screenshots)
- **Credit conversion**: 34,267 credits → $1,368.54 (~$0.04/credit)
- **MAX upgrade**: Same day, immediate quota increase

**The Math (500+ premium requests/day):**

| System                       | Estimated Monthly Cost (500 msg/day)            |
|------------------------------|-------------------------------------------------|
| OLD (credits)                | ~$500-800/month (Pro + add-ons)                 |
| NEW (Sonnet/GPT-5.x mix)     | ~$400-600/month (Max + overage)                 |
| NEW (Opus 4.6 no thinking)   | ~$1,700/month (Opus 4.6 $5/$25)                 |
| NEW (Opus 4.6 light thinking)| ~$3,700/month                                   |
| NEW (Opus 4.6 med thinking)  | ~$7,100/month                                   |
| NEW (Opus 4/4.1 no thinking) | ~$4,200/month (old Opus $15/$75)                |

**Key findings:** [VERIFIED from model-pricing.json + screenshots]

- **Old system**: ~$0.03-0.05 per premium message via credits
- **New system**: Quota exhausted daily, overage at API pricing
- **Opus 4.6 CHEAPER**: $5/$25 per 1M tokens (~$0.11/msg) vs Opus 4/4.1 at $15/$75 (~$0.33/msg)
- **GPT-5.4 very cheap**: $1.25/$7.50 per 1M tokens (~$0.03/msg)
- **Max plan ($200/mo)**: Only covers 42-170 premium messages/day - YOU WILL EXCEED THIS

**Immediate actions:**
1. Add-on credits converted at ~$0.04/credit (34,267 credits → $1,368.54 recorded)
2. Monitor dashboard - migration may not happen immediately after announcement
3. Consider BYOK (Bring Your Own Key) for direct API access at same rates but no Windsurf markup
4. Prefer Opus 4.6 ($0.11/msg) or GPT-5.4 ($0.03/msg) over Opus 4/4.1 ($0.33/msg)

## Key Dates

- **Mar 19, 2026**: New pricing announced effective (email received)
- **Mar 19, 2026 12:19 - Mar 20 07:54**: Still on OLD credit system (22 screenshots recorded)
- **Mar 20, 2026 ~09:00**: Transition to NEW quota system (recorded)
- **Mar 20, 2026 10:21**: Upgraded to MAX subscription
- **Apr 20, 2026**: Next billing cycle (after MAX upgrade)

## Recommended Action Plan

1. **This week (free trial)**: Monitor actual daily usage in new system
2. **Track overage costs**: Note how much USD gets consumed from converted credits
3. **Evaluate Max plan**: If overage exceeds ~$200/mo, Max may be worth it
4. **Set up BYOK**: Add your own API keys for models you use most
5. **Optimize model selection**: Use Arena Mode to find cheaper models that work for your tasks
6. **Consider batching**: Longer, more complete prompts = fewer messages = lower cost

## Current Dashboard Status [VERIFIED from screenshots 2026-03-19]

**Dashboard still shows OLD credit system as of Mar 19, 2026:**

| Field                  | Example Value                           |
|------------------------|-----------------------------------------|
| System displayed       | OLD credit-based (not new quota system) |
| User Prompt credits    | 500/500 used (0 left)                   |
| Add-on credits used    | ~15,000 / 50,000                        |
| Add-on credits left    | ~35,000                                 |
| Next plan refresh      | Next billing cycle                      |
| Next billing cycle     | ~1 week after announcement              |

**What dashboard does NOT show:**
- Daily/weekly quota
- Overage charges
- API pricing
- "Extra usage" balance

**Conclusion:** Transition occurred Mar 20, 2026 ~09:00 (day after announcement). Old credits converted at ~$0.04/credit to "Extra usage balance".

**Recorded:** Full transition log in `_PrivateSessions/_2026-03-19_WindsurfTokenUsageLogging/_WINDSURF_PRICING_MODEL_TRANSITION_LOG.md`

## Before vs After Comparison

### OLD System (Credit-Based) [VERIFIED]

| Component          | Details                                            |
|--------------------|----------------------------------------------------|
| Base plan          | Pro $20/mo with 500 credits/month                  |
| Add-on credits     | Purchased in bulk, rollover, ~$0.02-0.05/credit    |
| Premium model cost | 1-3 credits per message (Sonnet ~1, Opus ~2-3)     |
| Heavy user example | ~800 credits/day average (15K used in 20 days)     |
| Effective cost     | ~$20 base + ~$500-800/mo add-ons = ~$520-820/month |

### NEW System (Quota + API Pricing) [VERIFIED from blog, effective Mar 19, 2026]

| Plan      | Price      | Premium Plus/day | Premium/day | Lightweight/day |
|-----------|------------|------------------|-------------|-----------------|
| Pro       | $20/mo     | 7-27             | 8-101       | 47-190          |
| Teams     | $40/seat   | 7-27             | 8-101       | 47-190          |
| **Max**   | **$200/mo**| **42-170**       | **47-63**   | **281-190**     |

**Premium Plus**: Claude Opus 4.6, GPT-5.4, GPT-5.3-Codex
**Premium**: Claude Sonnet 4.6, GPT-5.2, Gemini 3 Pro
**Lightweight**: Haiku, Flash

**Overage pricing**: Direct API cost pass-through

## API Pricing Reference [VERIFIED from model-pricing.json 2026-03-12]

| Model            | Input/1M tokens | Output/1M tokens | Est. cost/message* |
|------------------|-----------------|------------------|--------------------|
| Claude Opus 4.6  | $5.00           | $25.00           | ~$0.11             |
| Claude Opus 4/4.1| $15.00          | $75.00           | ~$0.33             |
| Claude Sonnet 4.6| $3.00           | $15.00           | ~$0.07             |
| GPT-5.4          | $1.25           | $7.50            | ~$0.03             |
| GPT-5.2          | $0.875          | $7.00            | ~$0.03             |
| Haiku 4.5        | $1.00           | $5.00            | ~$0.02             |
*Estimated per message: 2K input tokens, 4K output tokens (conservative for coding tasks)

## Cost Projections (Heavy User)

**Profile**: Heavy user, 500+ messages/day, primarily premium models (Sonnet/GPT-5.x class)

### Scenario A: Max Plan + Overage

| Component      | Calculation                      | Monthly Cost   |
|----------------|----------------------------------|----------------|
| Max plan       | Base fee                         | $200           |
| Included quota | ~100 premium messages/day (avg)  | $0             |
| Overage        | 400 messages/day x 30 x $0.07    | ~$840          |
| **Total**      |                                  | **~$1,040/mo** |

### Scenario B: Pro Plan + Heavy Overage

| Component      | Calculation                      | Monthly Cost   |
|----------------|----------------------------------|----------------|
| Pro plan       | Base fee                         | $20            |
| Included quota | ~50 premium messages/day (avg)   | $0             |
| Overage        | 450 messages/day x 30 x $0.07    | ~$945          |
| **Total**      |                                  | **~$965/mo**   |

### Scenario C: Opus-Heavy User (Without Thinking)

| Component      | Calculation                      | Monthly Cost   |
|----------------|----------------------------------|----------------|
| Max plan       | Base fee                         | $200           |
| Included quota | ~100 messages/day                | $0             |
| Overage (Opus) | 400 messages/day x 30 x $0.33    | ~$3,960        |
| **Total**      |                                  | **~$4,160/mo** |

### Scenario D: 500+ Premium Plus with Thinking

**Opus 4.5/4.6 Thinking** generates extensive reasoning tokens billed as output.

| Token Profile        | Input   | Output (incl. thinking) | Cost/message (Opus 4.6) |
|----------------------|---------|-------------------------|-------------------------|
| Light thinking       | 2K      | 10K                     | ~$0.26                  |
| Medium thinking      | 2K      | 20K                     | ~$0.51                  |
| Heavy thinking       | 3K      | 40K                     | ~$1.02                  |

*Calculation: (input × $5 + output × $25) / 1M tokens*

**Cost projection at 500 messages/day:**

| Component      | Calculation                      | Monthly Cost    |
|----------------|----------------------------------|-----------------|
| Max plan       | Base fee                         | $200            |
| Included quota | ~50 Premium Plus/day (Max avg)   | $0              |
| Overage        | 450 msg/day x 30 x $0.26 (light) | ~$3,510         |
| **Total light**|                                  | **~$3,710/mo**  |
| Overage        | 450 msg/day x 30 x $0.51 (med)   | ~$6,885         |
| **Total medium**|                                 | **~$7,085/mo**  |

**Reality check**: At $0.26-0.51 per thinking message, 500/day = **$130-255/day** = **$3,900-7,650/month** in overage.

## What Happens to Your Add-on Credits [VERIFIED]

From blog: "Your add-on credits will be converted into a dollar amount for extra usage that you can use to pay for extra usage. We will convert them at a rate equivalent to how much you paid for them."

**Actual recorded conversion:**
- Credits before transition: 34,266.70
- Extra usage balance after: $1,368.54
- Conversion rate: ~$0.04/credit (34,267 × $0.04 = $1,370.68)
- This balance covers overage at API rates until exhausted

## Options Analysis

### Option 1: Max Plan ($200/mo) [RECOMMENDED FOR EVALUATION]

**Pros:**
- Highest included quota (42-170 premium/day)
- Priority support
- Automated zero data retention
- Full model availability

**Cons:**
- Still insufficient for 500+ messages/day
- Will require overage at API pricing
- 10x price increase from Pro base

### Option 2: BYOK (Bring Your Own Key) [RECOMMENDED FOR COST CONTROL]

**Pros:**
- Same API pricing but direct to provider
- No Windsurf markup on overage
- Full control over usage
- Can use prompt caching (50-90% cost reduction)

**Cons:**
- Lose Windsurf's model abstraction
- Must manage API keys yourself
- May lose some Windsurf-specific features

**Setup**: Settings > Model Provider API Keys

### Option 3: Model Optimization Strategy

Reduce costs by strategic model selection:

| Task Type        | Current Model | Optimized Model    | Savings |
|------------------|---------------|--------------------|---------|
| Quick questions  | Opus/Sonnet   | Haiku/Flash        | 70-90%  |
| Code review      | GPT-5.4       | GPT-5.2 or Sonnet  | 30-50%  |
| Simple edits     | Premium       | SWE-1.5 (free)     | 100%    |
| Complex reasoning| Opus          | Sonnet 4.5 thinking | 80%    |

**Target**: Get 60-70% of requests to Lightweight tier = stay within quota

### Option 4: Cost-Effective THINKING Alternatives [VERIFIED 2026-03-19]

**Non-Claude alternatives with reasoning/thinking capabilities:**

**OpenAI Reasoning Models (o-series):**

| Model     | Input/1M | Output/1M | Reasoning Cost/msg* | vs Opus 4.6 | Notes |
|-----------|----------|-----------|---------------------|-------------|-------|
| o3        | $1.00    | $4.00     | $0.08               | **-84%**    | Flagship reasoning, PhD-level math |
| o4-mini   | $0.55    | $2.20     | $0.05               | **-90%**    | Best value reasoning model |

*Reasoning tokens billed as output. Estimate: 2K in + 20K reasoning/out

**OpenAI GPT-5.x with Reasoning Effort:**

| Model         | Input/1M | Output/1M | Med Reasoning/msg* | vs Opus 4.6 | Notes |
|---------------|----------|-----------|--------------------| ------------|-------|
| GPT-5.4       | $1.25    | $7.50     | $0.15              | **-71%**    | Latest, configurable effort |
| GPT-5.2       | $0.875   | $7.00     | $0.14              | **-73%**    | Proven, adaptive reasoning |

*Reasoning effort: none, low, medium, high, xhigh. Estimate at medium.

**Google Gemini with Thinking:**

| Model            | Input/1M | Output/1M | Thinking Cost/msg* | vs Opus 4.6 | Notes |
|------------------|----------|-----------|--------------------| ------------|-------|
| Gemini 3.1 Pro   | $2.00    | $12.00    | $0.25              | **-51%**    | 77% ARC-AGI-2, thinking tokens |
| Gemini 3 Flash   | $0.50    | $3.00     | $0.06              | **-88%**    | Fast, configurable reasoning |

*Thinking tokens billed as output at standard rate.

**RECOMMENDED: o3 or GPT-5.4**

**o3** (Windsurf: "Premium Plus" tier):
- **$0.08/message** vs $0.51/message for Opus 4.6 = **84% savings**
- OpenAI's flagship reasoning model
- PhD-level math and logic

**GPT-5.4** (Windsurf: "Premium Plus" tier):
- **$0.15/message** vs $0.51/message for Opus 4.6 = **71% savings**
- 77.1% ARC-AGI-2 (massive reasoning benchmark)
- 1M context window
- Native thinking mode

**Cost comparison at 500 thinking messages/day:**

| Model                | Cost/message | Daily Cost | Monthly Cost |
|----------------------|--------------|------------|--------------|
| Opus 4.6 (medium)    | $0.51        | $255       | **$7,650**   |
| GPT-5.4 (medium)     | $0.15        | $75        | **$2,250**   |
| GPT-5.2 (medium)     | $0.14        | $70        | **$2,100**   |
| o3 (reasoning)       | $0.08        | $40        | **$1,200**   |
| o4-mini (reasoning)  | $0.05        | $25        | **$750**     |

**Savings potential**: Switch from Opus 4.6 to o3 = **$6,450/month savings**

**When to use each model:**

| Task Type           | Recommended Model       | Why |
|---------------------|-------------------------|-----|
| Complex coding      | GPT-5.4                 | Latest features, 71% cheaper |
| Heavy reasoning     | o3                      | PhD-level logic, 84% cheaper |
| Fast reasoning      | o4-mini                 | Best value, 90% cheaper |
| Budget reasoning    | GPT-5.2                 | Proven model, 73% cheaper |

### Option 5: Direct API Access (No Windsurf)

Use Claude/OpenAI APIs directly with:
- Cursor (similar IDE, different pricing model)
- Continue.dev (open source, BYOK only)
- Aider (CLI-based, very efficient)

## Grandfathering Details [VERIFIED]

From blog: "If you are a Pro or Teams user, we will grandfather in your current plan price indefinitely, but your plan will migrate to the new usage allowance system."

**This means:**
- Your Pro plan stays at current price ($15 or $20)
- BUT you get new (lower) quotas
- Overage still charged at API pricing
- Can access new plans at current price point

## Sources

- Windsurf Blog: https://windsurf.com/blog/windsurf-pricing-plans [VERIFIED 2026-03-19]
- User screenshots of usage dashboard and blog post [VERIFIED]
- Model pricing: `.windsurf/skills/llm-evaluation/model-pricing.json` [VERIFIED 2026-03-12]
- Transition log: `_PrivateSessions/_2026-03-19_WindsurfTokenUsageLogging/_WINDSURF_PRICING_MODEL_TRANSITION_LOG.md`
- Anthropic pricing: https://platform.claude.com/docs/en/about-claude/pricing
- OpenAI pricing: https://developers.openai.com/api/docs/pricing

## Document History

**[2026-03-20 17:35]**
- Fixed: Option 4 pricing from model-pricing.json (o3: $1/$4, o4-mini: $0.55/$2.20, GPT-5.4: $1.25/$7.50)
- Removed: GPT-5.3-Codex (not in model-pricing.json)
- Recalculated: All cost/message values (o3: $0.08, o4-mini: $0.05, GPT-5.4: $0.15)
- Updated: Recommendations to o3/GPT-5.4 based on correct pricing

**[2026-03-20 17:33]**
- Fixed: Option 4 comparison table used wrong Opus pricing ($1.53 -> $0.51)
- Fixed: All "vs Opus" percentages recalculated against Opus 4.6 at $0.51/msg
- Fixed: Monthly savings ($18,600 -> $3,300) based on correct baseline

**[2026-03-20 17:30]**
- Updated: Effective Date Status with actual recorded transition (Mar 20 ~09:00, not Mar 19)
- Fixed: Credit conversion rate ~$0.04/credit (was ~$0.01-0.02) based on recorded data
- Added: Actual transition data (34,267 credits -> $1,368.54)
- Added: Key dates with precise timestamps from 34 screenshots
- Added: Reference to transition log document
- Removed: Outdated note about llm-transcription sync (already done)

**[2026-03-19 14:25]**
- Fixed: Scenario D thinking calculations used wrong Opus pricing ($15/$75 -> $5/$25)
- Corrected: Light thinking ~$0.26/msg (was $0.78), Medium ~$0.51/msg (was $1.53)
- Corrected: Monthly thinking projections ~$3,700-7,100 (was $10,700-20,800)
- Removed: Personal data, replaced with example round numbers
- Updated: Summary table with corrected Opus 4.6 thinking costs

**[2026-03-19 14:20]**
- Fixed: Claude Opus 4.6 pricing was WRONG ($15/$75 -> $5/$25) per model-pricing.json
- Added: Opus 4/4.1 row to pricing table (these are the expensive $15/$75 models)
- Updated: Cost projections significantly lower with correct Opus 4.6 pricing
- Verified: Windsurf pricing page still shows OLD credit system (Pro $15, Teams $30)
- Added: Effective Date Status subsection in Summary clarifying gradual rollout

**[2026-03-19 12:33]**
- Added: "Current Dashboard Status" section based on user screenshots
- Verified: Dashboard still shows OLD credit system (not new quota)
- Updated: Key Dates to distinguish announced vs actual status
- Note: Migration date unclear - may be Mar 28 (next billing cycle)

**[2026-03-19 10:52]**
- Replaced: Claude-focused alternatives with non-Claude options (user rejected Sonnet/Haiku)
- Added: OpenAI o-series reasoning models (o3, o4-mini)
- Added: GPT-5.x with reasoning effort (5.4, 5.3-Codex, 5.2)
- Added: Google Gemini with thinking (3.1 Pro, 3 Flash)
- Recommended: GPT-5.3-Codex ($0.29/msg) or Gemini 3.1 Pro ($0.25/msg)
- Source: OpenRouter, OpenAI docs, Google AI docs

**[2026-03-19 10:50]**
- Added: Option 4 - Cost-Effective THINKING Alternatives section
- Added: Arena Leaderboard pricing comparison table (9 models)
- Source: windsurf.com/leaderboard, OpenRouter, Anthropic docs

**[2026-03-19 10:40]**
- Initial research on Windsurf pricing change impact
- Cost projections for 500+ messages/day usage profile
- Options analysis with BYOK and model optimization strategies
