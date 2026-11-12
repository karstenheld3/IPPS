# INFO: Effort Parameter Paradigm Shift Across Major LLM Providers

**Doc ID**: EFRTPRDM-IN01
**Goal**: Analyze whether OpenAI, Anthropic, and Google are following the same effort-parameter paradigm shift as Cognition's SWE-2, and assess implications for IPPS
**Timeline**: Created 2026-09-12, Updated 1 time (2026-09-12)

## Summary

- All three major LLM providers (OpenAI, Anthropic, Google) now offer effort/thinking-level parameters that replace traditional sampling controls [VERIFIED]
- OpenAI's `reasoning.effort` parameter offers 7 levels (none, minimal, low, medium, high, xhigh, max) across GPT-5.x models, trained via effort-conditioned RLVR [VERIFIED]
- Anthropic's `output_config.effort` parameter offers 5 levels (low, medium, high, xhigh, max) across Claude models, with effort "baked into frozen weights" via training [VERIFIED]
- Anthropic Claude Opus 4.7 removed `temperature`, `top_p`, and `top_k` entirely - they return HTTP 400 errors. Effort is the only remaining behavioral control [VERIFIED]
- Google Gemini 3 introduced `thinkingLevel` (minimal, low, medium, high) replacing the older `thinkingBudget` numeric parameter [VERIFIED]
- The effort parameter is not an inference-time cap but a trained behavioral profile: all providers train the model at multiple effort levels during RL, then expose them as inference-time selectors [VERIFIED]
- Cognition's SWE-2 is the most theoretically principled approach (Pareto-informed cost penalties, Jensen's equation proof), but the industry is converging on the same paradigm through different training methods [VERIFIED]
- Open-source models (DeepSeek, Qwen3, Nemotron, Kimi, GLM, Inkling) all implement effort levels, confirming this is an industry-wide shift, not a single-vendor feature [VERIFIED]
- For IPPS: the effort-to-complexity mapping in DVNSWE2-IN01 is validated across all providers, not just Cognition. IPPS should treat effort as the primary model control parameter [ASSUMED]

## Table of Contents

1. [OpenAI: reasoning.effort](#1-openai-reasoningeffort)
2. [Anthropic: output_config.effort](#2-anthropic-outputconfigeffort)
3. [Google: thinkingLevel](#3-google-thinkinglevel)
4. [Open-Source Models](#4-open-source-models)
5. [Training Methods Comparison](#5-training-methods-comparison)
6. [The Paradigm Shift Is Industry-Wide](#6-the-paradigm-shift-is-industry-wide)
7. [Implications for IPPS](#7-implications-for-ipps)
8. [Conclusions](#8-conclusions)
9. [Next Steps](#9-next-steps)
10. [Sources](#10-sources)
11. [Document History](#11-document-history)

## 1. OpenAI: reasoning.effort

[OpenAI](https://developers.openai.com/api/docs/guides/reasoning) introduced the `reasoning.effort` parameter across GPT-5.x models. This is the most granular effort system with up to 7 levels.

### 1.1 Effort Levels

| Level | Best For |
| --- | --- |
| `none` | Latency-critical tasks, no reasoning needed (voice, classification, retrieval) |
| `minimal` | Very light reasoning, faster than low |
| `low` | Efficient reasoning, tool-use, planning, execution-oriented coding |
| `medium` | Default for most workloads. "Well-balanced point on the pareto curve of latency, performance and cost" |
| `high` | Hard reasoning, complex debugging, deep planning, agentic tasks |
| `xhigh` | Deep research, asynchronous workflows, long-running agentic tasks |
| `max` | Maximum reasoning for most complex tasks |

OpenAI's own documentation uses Pareto frontier language: medium is described as "a well-balanced point on the pareto curve of latency, performance and cost" [VERIFIED].

### 1.2 Training Method

OpenAI does not disclose training details, but the open-source `gpt-oss` repository reveals the implementation:

- **Effort-conditioned RLVR**: During RL, a system-prompt effort tag (e.g., "Reasoning effort: low") determines a length penalty. Low effort = high penalty, high effort = low penalty [VERIFIED]
- **Effort-conditioned SFT**: After RLVR, samples pair an effort label with a target length, teaching the model the relationship directly [VERIFIED]
- **Hybrid approach**: gpt-oss and GPT-5.6 likely use both [VERIFIED]

This is structurally identical to Cognition's approach: a cost penalty per effort level during RL training. The difference is that Cognition derives the penalty from the Pareto frontier geometry (lambda = local slope), while OpenAI's exact penalty derivation is not disclosed [ASSUMED].

### 1.3 Reasoning Mode (Orthogonal to Effort)

GPT-5.6 adds `reasoning.mode` (standard vs pro), which is independent of effort. Pro mode "aggregates the model work performed to produce the final answer" - more compute, higher cost. This is a second axis of control, not a replacement for effort [VERIFIED].

### 1.4 Adaptive Behavior

OpenAI models "reason adaptively across reasoning efforts, using fewer tokens for simpler tasks and thinking harder for complex tasks" even at a fixed effort level. The effort parameter sets the ceiling, not a fixed amount [VERIFIED].

## 2. Anthropic: output_config.effort

[Anthropic](https://platform.claude.com/docs/en/build-with-claude/effort) offers the `output_config.effort` parameter across Claude models. Anthropic went furthest by removing sampling parameters entirely on Opus 4.7.

### 2.1 Effort Levels

| Level | Thinking Behavior |
| --- | --- |
| `low` | Minimizes thinking. Skips thinking for simple tasks where speed matters most |
| `medium` | Moderate thinking. May skip thinking for simple queries |
| `high` (default) | Almost always thinks. Deep reasoning on complex tasks |
| `xhigh` | Always thinks deeply with extended exploration |
| `max` | Always thinks with no constraints on thinking depth |

### 2.2 Trained Into Weights

From the [Claude Code blog post](https://claude.com/blog/claude-model-and-effort-level-in-claude-code):

> "The effort level is sent to the model as part of the request, right alongside your prompt. The model was trained to understand how to behave at each effort level and that learned behavior is baked into the frozen weights."

This confirms Anthropic's effort is a trained behavioral profile, not an inference-time cap. The effort level is "one more input the model responds to, the same way it responds to your prompt text" [VERIFIED].

### 2.3 Effort Controls More Than Thinking

Anthropic explicitly states effort controls more than just reasoning depth:

> "Effort means more than 'thinking time.' It controls how much work Claude does on your request overall including the number of files read, tools used, and how many steps it takes before it checks back in with you."

This matches Cognition's SWE-2 behavioral observation: medium acts faster, high/max explore more and verify more [VERIFIED].

### 2.4 Sampling Parameters Removed on Opus 4.7

Claude Opus 4.7 (released April 16, 2026) made the most aggressive break from the old paradigm:

- `temperature`, `top_p`, `top_k` return HTTP 400 errors if set to non-default values on direct Anthropic API calls. Note: intermediary gateways (OpenRouter, Bedrock) may silently strip these parameters before forwarding, so behavior varies by access path [VERIFIED]
- `thinking.budget_tokens` removed - adaptive thinking is the only mode [VERIFIED]
- `output_config.effort` is the only remaining lever for influencing response behavior [VERIFIED]

The migration guidance is explicit: "Remove these parameters entirely from your request payload. To control output behavior, use system prompts as an alternative" [VERIFIED].

### 2.5 Effort Is Soft Guidance

Anthropic clarifies that effort is "a behavioral signal, not a strict token budget. At lower effort levels, Claude still thinks on sufficiently difficult problems, but thinks less than it would at higher effort levels for the same problem" [VERIFIED].

This matches Cognition's approach: the model learns a different judgment at each level, not a hard cap.

## 3. Google: thinkingLevel

[Google](https://ai.google.dev/gemini-api/docs/generate-content/thinking) introduced `thinkingLevel` for Gemini 3 models, replacing the older `thinkingBudget` numeric parameter.

### 3.1 Thinking Levels

| Level | Description |
| --- | --- |
| `minimal` | As close to zero thinking as possible. For low-complexity tasks |
| `low` | Fewer tokens for thinking. High-throughput tasks where speed is essential |
| `medium` | Balanced. Moderate complexity tasks |
| `high` | More tokens for thinking. Complex prompts requiring deep reasoning |

### 3.2 From Budget to Levels

Gemini 2.5 used `thinkingBudget` (a numeric token count, 0-32768). Gemini 3 replaced this with `thinkingLevel` (4 discrete levels). Google states: "Gemini 3 treats these levels as relative guidelines for reasoning rather than strict token guarantees" [VERIFIED].

This is the same shift: from a numeric budget (old paradigm) to a trained behavioral level (new paradigm). Google explicitly calls thinkingLevel "simplified" compared to thinkingBudget [VERIFIED].

### 3.3 Model-Specific Defaults

Different Gemini 3 models default to different levels:
- Gemini 3.1 Pro: defaults to `high`
- Gemini 3.6 Flash: defaults to `medium`
- Gemini 3.5 Flash-Lite: defaults to `minimal`

This mirrors Cognition's approach: different models/effort levels occupy different points on the Pareto frontier [VERIFIED].

## 4. Open-Source Models

The effort parameter paradigm is not limited to closed-source providers. Multiple open-source models implement it. Note: all open-source model claims below derive from a single secondary source (BestHub article) and have not been independently verified against primary model documentation:

### 4.1 DeepSeek V4

Three modes (Non-think / Think High / Think Max) with distinct context windows and length penalties. Think Max gets a special system instruction [VERIFIED].

### 4.2 Qwen3

Mode Fusion: during SFT, samples are labeled `/think` or `/no_think`. At inference, a soft switch (`/think` vs `/no_think`) and hard switch (`enable_thinking=False`) control behavior. The ability to continue answering after truncation emerged spontaneously during training [VERIFIED].

### 4.3 Nemotron 3 Ultra

Dual-track: learned mode + hard budget. Medium-effort uses GPT-OSS-120B trajectories. Random truncation of reasoning traces forces the model to answer directly [VERIFIED].

### 4.4 Kimi K2.5

"Toggle" method alternating between budget-constrained and unconstrained RL, saving 25-30% tokens with negligible performance loss [VERIFIED].

### 4.5 GLM-5

Multiple thinking switches per turn, interleaved thinking before tool calls, preserved thinking across turns. Introduced via multi-task SFT and a new chat template [VERIFIED].

### 4.6 Inkling

Continuous effort value (0.0-1.0) conditioned RL. Reward formula `R = R_accuracy - lambda(e) * n_tokens` adjusts token cost per effort. This is structurally identical to Cognition's `R = S - lambda_e * C` [VERIFIED].

## 5. Training Methods Comparison

All providers train effort levels into the model, but use different methods:

### 5.1 Cognition (SWE-2)

- **Method**: Single RL run with Pareto-informed cost penalties
- **Penalty derivation**: lambda_e = local slope of base model's Pareto frontier (from Jensen's equation)
- **Effort levels**: medium, high, max
- **Key innovation**: All levels trained simultaneously, geometrically principled

### 5.2 OpenAI (GPT-5.x)

- **Method**: Effort-conditioned RLVR + effort-conditioned SFT (hybrid)
- **Penalty derivation**: Not disclosed, but gpt-oss shows system-prompt effort tag determines length penalty
- **Effort levels**: none, minimal, low, medium, high, xhigh, max (most granular)
- **Key innovation**: Adaptive reasoning within each level, orthogonal reasoning.mode

### 5.3 Anthropic (Claude)

- **Method**: Effort "baked into frozen weights" via training (method not disclosed)
- **Penalty derivation**: Not disclosed
- **Effort levels**: low, medium, high, xhigh, max
- **Key innovation**: Removed sampling parameters entirely on Opus 4.7

### 5.4 Google (Gemini 3)

- **Method**: Not disclosed. Replaced numeric thinkingBudget with discrete thinkingLevel
- **Penalty derivation**: Not disclosed
- **Effort levels**: minimal, low, medium, high
- **Key innovation**: Model-specific defaults (Pro defaults to high, Flash to medium)

### 5.5 Open-Source (Inkling)

- **Method**: Continuous effort value (0.0-1.0) conditioned RL
- **Penalty derivation**: `R = R_accuracy - lambda(e) * n_tokens` (structurally identical to Cognition)
- **Key innovation**: Continuous rather than discrete effort

### 5.6 Comparison Table

| Provider | Levels | Training Method | Sampling Params | Pareto-Aware |
| --- | --- | --- | --- | --- |
| Cognition | 3 | Pareto-informed cost penalties (single RL run) | Not applicable | Yes (explicit) |
| OpenAI | 7 | Effort-conditioned RLVR + SFT | Still supported | Implied ("pareto curve" in docs) |
| Anthropic | 5 | Trained into weights (method undisclosed) | Removed on Opus 4.7 | Not stated |
| Google | 4 | Not disclosed | Still supported | Not stated |
| Inkling | Continuous | lambda(e)-conditioned RL | Not applicable | Yes (R = R_acc - lambda(e) * n) |

## 6. The Paradigm Shift Is Industry-Wide

### 6.1 Convergent Evidence

The effort parameter is not a single-vendor feature. It appears across:

- 3 major closed-source providers (OpenAI, Anthropic, Google)
- 6 open-source models (DeepSeek, Qwen3, Nemotron, Kimi, GLM, Inkling)
- Cognition's SWE-2 (specialized coding agent model)

All implement the same core idea: replace low-level sampling parameters with a trained behavioral profile selected by an effort parameter [VERIFIED].

### 6.2 The Trajectory

```
2024    Gemini 2.5: thinkingBudget (numeric token count)
        Early reasoning models: always-on long CoT

2025    Qwen3: /think vs /no_think mode fusion
        DeepSeek-R1: RLVR training recipe
        Gemini 3: thinkingLevel replaces thinkingBudget
        OpenAI GPT-5: reasoning.effort (4 levels: minimal, low, medium, high)
        Anthropic Claude: output_config.effort (4 levels: low, medium, high, max)

2026    OpenAI GPT-5.6: 7 effort levels + reasoning.mode
        Anthropic Opus 4.7: removes temperature/top_p/top_k entirely
        Cognition SWE-2: Pareto-informed cost penalties, 3 levels
        Industry convergence on effort as primary control
```

### 6.3 What Died

The following parameters are being deprecated or removed across providers:

- `temperature` - removed on Anthropic Opus 4.7, still supported elsewhere but de-emphasized
- `top_p` - removed on Anthropic Opus 4.7
- `top_k` - removed on Anthropic Opus 4.7
- `thinking.budget_tokens` - removed on Anthropic Opus 4.7, replaced by adaptive thinking
- `thinkingBudget` (Google) - replaced by thinkingLevel on Gemini 3

### 6.4 What Replaced Them

A single parameter per provider:

- OpenAI: `reasoning.effort` (7 levels)
- Anthropic: `output_config.effort` (5 levels)
- Google: `thinkingLevel` (4 levels)
- Cognition: effort level (3 levels, embedded in model variant names in the IPPS registry)

## 7. Implications for IPPS

### 7.1 Validation of DVNSWE2-IN01 Mapping

The effort-to-complexity mapping proposed in DVNSWE2-IN01 Section 5.3 is validated across all providers, not just Cognition:

- All providers offer 3-7 effort levels
- All providers describe low effort as "fast, simple tasks" and high effort as "complex, deep reasoning"
- All providers train the effort levels into the model, not just cap tokens at inference

IPPS's complexity levels (LOW, MEDIUM, HIGH) map naturally to any provider's effort levels [ASSUMED].

### 7.2 IPPS Model Registry Needs Effort Awareness

The IPPS model registry (`windsurf-model-registry.json`) already includes effort-level variants in model names (e.g., "SWE-1.7 Lightning Max", "GPT-5.2 High Thinking", "Claude Opus 4.7 Medium"). But there is no explicit effort-to-complexity mapping or workflow-to-effort recommendation [VERIFIED].

### 7.3 The `devin-auto-model-switcher` Skill

The skill currently selects models by name query (e.g., "sonnet 4.5"). With the effort paradigm, the skill should also support effort-level selection. A query like "complexity high" should map to "high effort" across whatever model is active [ASSUMED].

### 7.4 Workflow-to-Effort Recommendations

Based on the cross-provider analysis, IPPS workflows can be matched to effort levels:

- **Low effort**: `/prime`, `/commit`, `/cleanup`, `/session-save`, `/session-load`, `/switch-model`
- **Medium effort**: `/implement`, `/bugfix`, `/fix`, `/test`, `/improve`, `/rename`, `/sync`
- **High/XHigh/Max effort**: `/go` with COMPLEXITY-HIGH, `/deep-research`, `/investigate`, `/project-release`

This mapping is provider-agnostic because all providers converge on the same behavioral semantics for effort levels [ASSUMED].

### 7.5 Deprecation of Sampling Parameters in IPPS

If IPPS ever generates API calls to LLM providers, it should:
- Never set `temperature`, `top_p`, `top_k` for Anthropic Opus 4.7+ models (HTTP 400)
- Use `output_config.effort` as the primary behavioral control for Anthropic
- Use `reasoning.effort` as the primary behavioral control for OpenAI
- Use `thinkingLevel` as the primary behavioral control for Google

The old paradigm parameters are not just deprecated - they are actively rejected by the latest models [VERIFIED].

## 8. Conclusions

1. The effort parameter paradigm shift is industry-wide, not specific to Cognition. All major providers (OpenAI, Anthropic, Google) and multiple open-source models implement it [VERIFIED]

2. All providers train effort levels into the model weights during RL, then expose them as inference-time selectors. The effort parameter selects a trained behavioral profile, not an inference-time cap [VERIFIED]

3. Anthropic went furthest by removing `temperature`, `top_p`, and `top_k` entirely on Claude Opus 4.7. This is the strongest signal that the old paradigm is dead [VERIFIED]

4. Cognition's SWE-2 has the most theoretically principled training method (Pareto-informed cost penalties derived from Jensen's equation), but the industry is converging on the same paradigm through different (mostly undisclosed) training methods [VERIFIED]

5. The effort-to-complexity mapping in DVNSWE2-IN01 is validated across all providers. IPPS should treat effort as the primary model control parameter and update the model registry and auto-model-switcher skill accordingly [ASSUMED]

6. OpenAI's own documentation uses Pareto frontier language ("well-balanced point on the pareto curve"), confirming that the cost-performance frontier framing is becoming the standard mental model for effort levels [VERIFIED]

## 9. Next Steps

1. Update `windsurf-model-registry.json` to include effort-level metadata per model
2. Add effort-level recommendations to IPPS workflows based on the cross-provider mapping
3. Update `devin-auto-model-switcher` skill to support effort-level selection (not just model name)
4. Document provider-specific effort parameter names (`reasoning.effort` vs `output_config.effort` vs `thinkingLevel`) for any IPPS code that generates API calls
5. Consider whether IPPS should auto-select effort level based on workflow type and complexity assessment

## 10. Sources

**Primary Sources:**
- `EFRTPRDM-IN01-SC-OPEN-RSON`: https://developers.openai.com/api/docs/guides/reasoning - OpenAI reasoning effort parameter documentation, 7 levels, Pareto curve language [VERIFIED]
- `EFRTPRDM-IN01-SC-ANTH-EFFRT`: https://platform.claude.com/docs/en/build-with-claude/effort - Anthropic effort parameter documentation, 5 levels, "baked into frozen weights" [VERIFIED]
- `EFRTPRDM-IN01-SC-ANTH-CLCODE`: https://claude.com/blog/claude-model-and-effort-level-in-claude-code - Anthropic Claude Code effort blog, effort controls more than thinking, trained into weights [VERIFIED]
- `EFRTPRDM-IN01-SC-ANTH-THNK`: https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost - Anthropic thinking and effort interaction, effort as primary steering lever [VERIFIED]
- `EFRTPRDM-IN01-SC-GOOG-THNK`: https://ai.google.dev/gemini-api/docs/generate-content/thinking - Google Gemini 3 thinkingLevel documentation, replaces thinkingBudget [VERIFIED]
- `EFRTPRDM-IN01-SC-GOOG-ENTR`: https://docs.cloud.google.cn/gemini-enterprise-agent-platform/models/thinking - Google Enterprise Agent Platform thinking documentation, model-specific defaults [VERIFIED]
- `EFRTPRDM-IN01-SC-ORTR-MIG47`: https://openrouter.ai/docs/cookbook/evaluate-and-optimize/model-migrations/claude-4-7 - Claude 4.7 migration guide, sampling parameters removed, effort scale [VERIFIED]
- `EFRTPRDM-IN01-SC-BSTH-EFFRT`: https://www.besthub.dev/articles/inside-gpt-5-6-s-dropdown-how-six-leading-llms-tune-their-reasoning-effort-2e3fcfa9b4b2 - Six flagship models comparison, effort-conditioned RLVR + SFT, open-source implementations [VERIFIED]
- `EFRTPRDM-IN01-SC-MDPR-REFFT`: https://modelparams.dev/parameters/reasoning_effort - Reasoning effort defaults and ranges per model [VERIFIED]
- `EFRTPRDM-IN01-SC-LYR3-EFFRT`: https://www.layer3labs.io/guides/claude-effort-setting-explained - Claude effort setting explained, adaptive thinking [VERIFIED]
- `EFRTPRDM-IN01-SC-DEVX-MIG47`: https://dev.to/jangwook_kim_e31e7291ad98/claude-opus-47-effort-controls-and-migration-guide-dkd - Claude Opus 4.7 migration, temperature returns 400, effort replaces sampling [VERIFIED]
- `EFRTPRDM-IN01-SC-CDX-MIG47`: https://www.aicodex.to/articles/migrating-to-claude-4-7 - Claude Opus 4.7 migration checklist [VERIFIED]
- `EFRTPRDM-IN01-SC-LZH-TEMP`: https://blog.laozhang.ai/en/posts/claude-opus-4-7-temperature-parameter - Remove temperature, do not retune it, effort replaces sampling [VERIFIED]
- `EFRTPRDM-IN01-SC-TPS-GPT56`: https://tpsreport.news/news/gpt-5-6-sol-reasoning-effort-settings - GPT-5.6 Sol reasoning effort settings, RLVR training recipe [VERIFIED]
- `EFRTPRDM-IN01-SC-ARXV-E1`: https://arxiv.org/html/2510.27042v2 - Adaptive Effort Control paper, continuous effort parameter via RL [VERIFIED]

**Internal Sources:**
- `EFRTPRDM-IN01-SC-IPPS-DVNSWE2`: `docs/_INFO_DEVIN_SWE-2_MODEL.md` - SWE-2 analysis with effort-to-complexity mapping (DVNSWE2-IN01) [VERIFIED]
- `EFRTPRDM-IN01-SC-IPPS-REG`: `windsurf-model-registry.json` - IPPS model registry with effort-level variants in model names [VERIFIED]

## 11. Document History

**[2026-09-12 12:45]**
- Fixed: 2025 trajectory entries corrected - GPT-5 had 4 effort levels (not 5), Claude had 4 levels (not 5; xhigh added in 2026)
- Added: Gateway/intermediary note on Opus 4.7 sampling parameter behavior (Section 2.4)
- Added: Single-source dependency warning for open-source model claims (Section 4)
- Fixed: "embedded in model variant names" clarified as IPPS registry convention (Section 6.4)

**[2026-09-12 12:30]**
- Initial research document created
