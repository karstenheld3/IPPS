# INFO: SWE-2 Model Analysis and Implications for IPPS Instruction Following

**Doc ID**: DVNSWE2-IN01
**Goal**: Analyze Cognition's SWE-2 model capabilities, classify it within IPPS taxonomy, and assess implications for instruction following with IPPS workflows and skills
**Timeline**: Created 2026-09-12, Updated 3 times (2026-09-12 - 2026-09-12)

## Summary

- SWE-2 is Cognition's most advanced coding model, post-trained from Kimi K3 (2.8T parameters), achieving 50.0% on FrontierCode 1.1 Main, within 1 point of Fable 5.1 at 64% lower cost (vendor-reported, not independently verified) [VERIFIED]
- SWE-2 is specifically trained with instruction-following overlays: keeping multiple instructions in context without losing sight of the underlying task [VERIFIED]
- Within IPPS taxonomy, SWE-2 is a BUILD-class agent engine in the Cognition SWE model family, operating across all EDIRD phases [VERIFIED]
- SWE-2 effort levels (medium, high, max) map to IPPS complexity levels (COMPLEXITY-LOW, COMPLEXITY-MEDIUM, COMPLEXITY-HIGH) [ASSUMED]
- SWE-2 behavioral improvements (focused exploration, verification discipline, test coverage) directly match IPPS EDIRD phase behaviors and AGEN verbs [VERIFIED]
- SWE-2 is absent from the IPPS model registry (last updated 2026-08-30); registry contains SWE-1.6 and SWE-1.7 but not SWE-2 [VERIFIED]
- SWE-2's instruction-following training directly addresses IPPS's core challenge of layered instruction tracking across rules, workflows, skills, and MUST-NOT-FORGET lists [ASSUMED]
- SWE-2 reduces exploration overhead: first edit after median 18 steps vs 48 for SWE-1.7, matching IPPS EXPLORE phase principle of focused understanding [VERIFIED]
- SWE-2's Pareto-informed RL training uses a linear cost penalty R = S - lambda_e * C per effort level, where lambda_e matches the local slope of the base model's Pareto frontier. This is derived from first principles via Jensen's functional equation: only a linear penalty is distribution-invariant under averaging [VERIFIED]
- The length-weighted reward baseline (used since SWE-1.6) approximates the optimal baseline b* by substituting rollout length L_i for the expensive gradient-norm term, reducing gradient variance at no extra cost [VERIFIED]

## Table of Contents

1. [SWE-2 Overview](#1-swe-2-overview)
2. [Pareto Frontier RL Training Methodology](#2-pareto-frontier-rl-training-methodology)
3. [Instruction-Following Training](#3-instruction-following-training)
4. [Behavioral Patterns and IPPS EDIRD Mapping](#4-behavioral-patterns-and-ipps-edird-mapping)
5. [Model Classification Within IPPS Taxonomy](#5-model-classification-within-ipps-taxonomy)
6. [Implications for IPPS Instruction Following](#6-implications-for-ipps-instruction-following)
7. [Model Registry Gap](#7-model-registry-gap)
8. [Conclusions](#8-conclusions)
9. [Next Steps](#9-next-steps)
10. [Sources](#10-sources)
11. [Document History](#11-document-history)

## 1. SWE-2 Overview

[Cognition](https://cognition.com) introduced SWE-2 as their most advanced coding model. It pushes the Pareto frontier of capability and cost, achieving 50.0% on [FrontierCode 1.1 Main](https://cognition.com/blog/frontier-code-1.1), within one point of Fable 5.1 while being 64% cheaper (Cognition's own measurement; no absolute dollar figure published for SWE-2).

### 1.1 Architecture and Training

SWE-2 is post-trained from [Kimi K3](https://arxiv.org/abs/2607.24653), a 2.8T-parameter model that had already undergone extensive RL for agentic coding. Cognition's RL finds substantial headroom, adding 5-6 points on many benchmarks and shifting K3's entire cost-performance frontier.

Key training innovations:

- **Cost penalties**: Linear cost penalty per effort level in a single RL run, each penalty tuned to the local slope of the base model's Pareto frontier. Derived from first principles to advance the model's entire Pareto frontier while preserving its shape [VERIFIED]
- **Length-weighted reward baseline**: Reduces gradient variance at no extra cost, significantly stabilizes training. Used since SWE-1.6 [VERIFIED]
- **RL rollout serving**: Prefill delayer, DSpark speculative decoding with online draft model training, NVFP4/FP8 kernels with quantization-aware training. Lower inference-training KL divergence than SWE-1.7 despite 3x larger base model [VERIFIED]
- **Data improvements**: Tripled RL environments, instruction-following overlays, verifier hardening flywheel using previous SWE-2 checkpoints [VERIFIED]

### 1.2 Performance

SWE-2 beats SWE-1.7 and Grok 4.6 on both score and cost on FrontierCode 1.1 Main and DeepSWE 1.1. It matches GPT-5.6 Sol and Fable 5/5.1 at a fraction of their price, and comes within a few points of GPT-6 Astra at a quarter of the cost [VERIFIED].

SWE-2 medium scores higher than SWE-1.7 while taking 58% fewer turns and costing 81% less on average on FrontierCode 1.1 Main [VERIFIED].

### 1.3 Trustworthiness

SWE-2 passed 98.0% of propaganda and censorship evaluation attempts overall: 99.8% in English, 95.2% in Simplified Chinese, 99.1% in Traditional Chinese. No customer framing condition produced a statistically significant increase or decrease in vulnerability [VERIFIED].

## 2. Pareto Frontier RL Training Methodology

SWE-2's key training innovation is a principled RL algorithm that trains all reasoning-effort levels in a single run, advancing the entire cost-performance frontier. The blog calls this "Pushing the Pareto Frontier with RL."

### 2.1 What Is the Pareto Frontier

The **Pareto frontier** in this context is the set of optimal tradeoff points on a 2D plane where:

- **X-axis**: Average cost per task (a mix of inference cost in USD and rollout time)
- **Y-axis**: Solve rate (percentage of tasks solved)

A point (c, s) is on the Pareto frontier if no other point achieves a higher solve rate at equal or lower cost. The frontier is typically a concave curve: diminishing returns as you spend more. "Pushing the frontier" means achieving higher solve rates at every cost level [VERIFIED].

```
Solve Rate (s)
    │
    │         x GPT-6 Astra
    │       x Fable 5.1
    │     x SWE-2
    │   x SWE-1.7
    │ x Grok 4.6
    │
    └─────────────────── Cost (c)
```

### 2.2 The Cost-Penalized Reward Function

SWE-2 uses a reward function of the form:

```
R = S - lambda_e * C
```

Where:
- **S** in {0, 1}: whether a rollout was successful (task solved)
- **C**: cost of the rollout (inference cost in USD + rollout time)
- **e**: effort level (medium, high, max)
- **lambda_e**: penalty parameter tuned per effort level

The reward penalizes expensive rollouts. Higher lambda_e means the model is penalized more for spending tokens/time. Each effort level gets its own lambda, allowing the model to learn different cost-performance tradeoffs at each level in a single RL run [VERIFIED].

### 2.3 Why Linear? The Jensen's Functional Equation Proof

Cognition proves that the cost penalty **must** be linear (affine) if the RL objective is to depend only on average cost and average solve rate, not on the specific distribution of individual rollout outcomes.

**The claim**: Let X = (C, S) be the cost and success of a rollout, and h(X) be its reward. If the average reward E[h(X)] depends only on average cost E[C] and average solve rate E[S] (not on the full distribution of X), then h must be affine: h(C, S) = alpha + beta*S - lambda*C.

**The proof** uses Jensen's functional equation. A function h on a convex set satisfies:

```
h(t*x + (1-t)*y) = t*h(x) + (1-t)*h(y)  for all t in [0,1]
```

if and only if h(x) = c^T * x + b (affine). The condition "average reward depends only on average cost and solve rate" is exactly Jensen's equation applied to the reward function. Therefore h must be affine [VERIFIED].

**Why this matters**: Cognition needs to choose the reward function before knowing which rollout distributions training will produce. These distributions vary across models, effort levels, and training steps. A linear penalty guarantees the RL objective is well-defined regardless of the distribution. Non-linear penalties would give different rewards for the same average cost depending on whether costs are concentrated or spread across rollouts [VERIFIED].

### 2.4 Selecting lambda_e: The Tangent Condition

Setting lambda_e is not a hyperparameter tuning problem. It is determined by the geometry of the Pareto frontier.

**Key idea**: The iso-reward line for reward J has slope lambda_e on the cost-performance plane:

```
s = lambda_e * c + J
```

This line represents all (c, s) points that yield the same reward J. The goal is to push the frontier upward, not just increase reward.

**Failure case (lambda_e too large)**: If lambda_high is set too large, the iso-reward line is steeper than the frontier. The model is rewarded for reducing cost even at the expense of solve rate. The high-effort model collapses toward medium-effort behavior: cheaper but less capable. Reward increases but the Pareto frontier does not improve [VERIFIED].

**Correct choice (lambda_e = m)**: Let m be the local slope of the Pareto frontier at the current point (c, s) for effort level e. Setting lambda_e = m makes the iso-reward line tangent to the frontier. A small movement along the frontier changes solve rate by delta_s approx m * delta_c, so the change in reward is:

```
delta J = delta_s - lambda_e * delta_c = m * delta_c - m * delta_c = 0
```

The reward is unaffected by movements along the Pareto curve. Any improvement in reward must come from pushing the frontier upward, not sliding along it [VERIFIED].

```
Solve Rate (s)
    │
    │     . (c, s) on frontier
    │    /│
    │   / │  ← iso-reward line (slope = lambda_e = m)
    │  /  │    tangent to frontier at (c, s)
    │ /   │
    │/    │
    └─────┴──────── Cost (c)
         c
```

**Practical estimation**: Cognition approximates the Pareto curve tangents of the base model (Kimi K3) at each effort level, then sets lambda_e to the estimated slope. This is done once before training, not tuned during training [VERIFIED].

### 2.5 Length-Weighted Reward Baseline

Since SWE-1.6, Cognition uses a length-weighted reward baseline that reduces gradient variance at no extra cost.

**The problem**: The on-policy gradient estimator with baseline b is:

```
g_hat = (1/n) * sum_i (R_i - b) * grad(log pi(y_i | x))
```

The optimal baseline b* that minimizes the variance of the full gradient estimator is:

```
b* = sum_i ||grad(log pi(y_i | x))||^2 * R_i  /  sum_i ||grad(log pi(y_i | x))||^2
```

Computing this requires an extra backward pass per rollout to get the gradient norm term ||grad(log pi(y_i | x))||^2, which is expensive [VERIFIED].

**The insight**: The gradient norm ||grad(log pi(y_i | x))||^2 is strongly correlated with the rollout length L_i. Longer rollouts have larger gradient norms. So Cognition substitutes L_i for the gradient norm:

```
b* approx sum_i L_i * R_i / sum_i L_i
```

This is the **length-weighted group baseline**. It costs nothing extra (rollout lengths are already known), and in ablations it significantly stabilizes training. It helps keep the inference-training KL low during RL [VERIFIED].

### 2.6 RL Rollout Serving Infrastructure

SWE-2's rollout system optimizes for four goals simultaneously:

1. **Maximizing total throughput** - prefill delayer batches nearby requests, improving TPM/GPU and TPS/request by 10-20%
2. **Reducing latency** - limits staleness of off-policy rollouts
3. **Staying within KV-cache capacity** - memory budget for attention
4. **Keeping inference numerically close to training** - low inference-training KL divergence

Key components:

- **DSpark speculative decoding**: A draft model proposes tokens, the policy model verifies them. As the policy changes during training, acceptance rate degrades. Cognition trains an online draft model using SpecForge that tracks the policy, achieving 15% longer accept lengths [VERIFIED]
- **NVFP4/FP8 kernels with quantization-aware training**: Low-precision MoE inference fits more rollouts in memory. MLA layers use FP8 for K, Q, V and score computations. This is simpler than SWE-1.7's mixed precision (NoPE used FP8, RoPE stayed BF16) [VERIFIED]

### 2.7 Why This Matters for IPPS

The Pareto frontier training has direct implications for IPPS:

- **Effort levels are not arbitrary**: They are trained to occupy specific points on the cost-performance frontier. SWE-2 medium is trained to be cost-efficient on simple tasks; SWE-2 max is trained for maximum capability on complex tasks. This validates IPPS's complexity-to-effort mapping [ASSUMED]
- **The model learns cost-awareness**: SWE-2 is explicitly trained to balance cost and performance. For IPPS, this means the model naturally prefers efficient solutions over exhaustive ones, matching the `/prime` workflow's "As Little As Necessary" principle and APAPALAN [ASSUMED]
- **Single-run multi-effort training**: Unlike Kimi K3 (separate experts per domain+effort, then distilled), SWE-2 trains all effort levels in one RL run. This means the effort levels share a coherent behavioral profile, not a patchwork of specialists. For IPPS, switching effort levels does not change the model's fundamental behavior, only its intensity [VERIFIED]

### 2.8 The Effort Parameter Paradigm Shift

SWE-2's effort parameter represents a shift from low-level mechanical parameters to a holistic behavioral control mechanism. This is a qualitative change in how users interact with models.

#### From Mechanical Dials to Trained Behavior

The old paradigm controls the model with external constraints:

- `max_tokens` - hard cap on output length
- `temperature` - randomness in sampling
- `top_p` - nucleus sampling cutoff
- `frequency_penalty` - discourage repetition
- `verbosity` - "be brief" / "be detailed" in the prompt

These are constraints imposed from outside. The model wants to do X, but the user forces it to do Y by capping tokens or tweaking sampling. The model's actual behavior does not change - the output just gets truncated or made more random [ASSUMED].

The new paradigm controls the model with a trained behavioral profile. The effort parameter selects which trained policy the model uses. Each policy was RL-trained to occupy a specific point on the Pareto frontier. The model does not want to do X and get stopped - it learned to want a different thing at each level [VERIFIED].

```
Old: Model explores everything → user caps tokens at 4096 → output cut off mid-thought
New: Medium model judges what matters → stops at 18 steps because it decided to
```

The effort parameter is not a convenience wrapper around old parameters. It is a qualitatively different control mechanism:

- **Old**: Control the output. The model's internal behavior is identical regardless of settings - you just constrain what reaches you
- **New**: Control the model's judgment. The internal decision-making is different at each level. Medium does not explore less because it hit a token cap - it explores less because it was trained to judge that less exploration is sufficient [VERIFIED]

- **Old**: Parameters are orthogonal and composable. Set temperature AND max_tokens independently
- **New**: Effort is holistic. Cannot set "medium exploration but max verification" - the effort level bundles a coherent behavioral profile. Medium means medium-everything: less exploration, less planning, less verification, all calibrated together [VERIFIED]

#### Why Cognition Did This: Three Layers

**Layer 1 - User simplicity**: One parameter instead of five. Most users do not understand what temperature 0.7 vs 0.3 means. Everyone understands "try harder." The effort parameter is a UX decision - make the model controllable by non-experts [ASSUMED].

**Layer 2 - Cost-performance optimization**: Coding agents have a real cost per task. Users face a genuine tradeoff: "Is this task worth spending $5 on, or should I spend $0.50?" If you only have one model, you are stuck at one point on the Pareto frontier. Simple tasks are over-engineered (wasted money). Hard tasks are under-resourced (failed solutions). Multiple effort levels give users multiple points on the frontier - pick the one that matches the task's value [VERIFIED].

**Layer 3 - Autonomous agent economics**: Coding agents are not chatbots. A chatbot answers one question - cost is trivial. A coding agent runs autonomously for hundreds of steps (reads files, writes code, runs tests, debugs, iterates). Each task might take 50-500 turns. Cost compounds. At that scale, the difference between $0.50/task and $5.00/task is the difference between "use it for everything" and "use it only for important things." Cognition is building Devin - an autonomous coding agent. Their entire product depends on running many tasks cheaply. If every task costs $5, Devin is a luxury tool. If simple tasks cost $0.10 and only hard tasks cost $5, Devin becomes infrastructure. The effort parameter is a cost management system for autonomous agent execution at scale [ASSUMED].

#### What You Lose and Gain

**Lost**: Granular control. Cannot say "be thorough on exploration but cheap on output." The effort level is a package deal [VERIFIED].

**Gained**: Coherent behavior. The model's exploration, planning, implementation, and verification are all calibrated to the same cost-performance target. No more "model explored for 5000 tokens then got cut off before writing code because max_tokens was too low" [VERIFIED].

#### IPPS Parallel

IPPS already gates process intensity by complexity: COMPLEXITY-LOW gets an inline plan, COMPLEXITY-HIGH gets full doc sets. The effort parameter is the model-side equivalent of IPPS's complexity-gated document requirements. Both solve the same problem: "how much process is worth it for this task?" The old parameters (max_tokens, temperature) remain underneath as implementation details, but the effort parameter is becoming the primary interface because it controls what the model does, not just what it is allowed to do [ASSUMED].

## 3. Instruction-Following Training

The most IPPS-relevant aspect of SWE-2 is its instruction-following training. From the [Cognition blog post](https://cognition.com/blog/swe-2):

> "Following instructions is a crucial skill for LLMs, especially in the context of alignment and model UX. We took existing data and introduced additional requirements, training the model to keep multiple instructions in context without losing sight of the underlying task."

### 3.1 What This Means

SWE-2 was specifically trained to:

1. **Track multiple instructions simultaneously** - not just follow one instruction, but maintain awareness of several constraints at once
2. **Preserve the underlying task** - additional requirements do not cause the model to forget what it was originally asked to do
3. **Handle layered requirements** - existing data was augmented with additional requirements, creating a hierarchy of instructions

### 3.2 Mapping to IPPS Instruction Layers

IPPS uses exactly this kind of layered instruction structure:

```
IPPS Instruction Stack
├── Rules (agent-behavior.md, core-conventions.md, etc.)
│   └── Always-on constraints
├── Workflows (45+ workflows)
│   └── Step-by-step task instructions
├── Skills (21+ skills)
│   └── Domain knowledge references
├── MUST-NOT-FORGET lists
│   └── Per-workflow critical reminders
└── EDIRD Phase Model
    └── Phase gates and transitions
```

SWE-2's instruction-following training directly targets the challenge of maintaining all these layers simultaneously without losing track of the primary task [ASSUMED].

## 4. Behavioral Patterns and IPPS EDIRD Mapping

SWE-2's documented behavioral patterns map directly to IPPS EDIRD phases and AGEN verbs.

### 4.1 EXPLORE Phase

**SWE-2 behavior**: "Focused exploration: higher intelligence allows the model to judge which parts of the codebase actually matter for a task."

**IPPS mapping**: The [EXPLORE] phase principle "Understand before acting" with [RESEARCH], [ANALYZE], [ASSESS], [SCOPE] verbs. SWE-2's focused exploration directly implements the EXPLORE gate: understanding the problem without over-exploring [VERIFIED].

**Quantitative evidence**: SWE-2 medium makes its first real edit after a median of 18 steps, compared with 48 for SWE-1.7. This 62% reduction in exploration steps shows the model can judge relevance without exhaustive scanning [VERIFIED].

### 4.2 DESIGN Phase

**SWE-2 behavior**: "SWE-2 high and max hold an edge over complex tasks: planning more, exploring more of the codebase, and managing uncertainties through more complex verification."

**IPPS mapping**: The [DESIGN] phase with [PLAN], [DECOMPOSE], [WRITE-SPEC], [PROVE] verbs. Higher effort levels engage more planning, matching IPPS complexity-gated document requirements (LOW: inline plan, MEDIUM: SPEC+IMPL, HIGH: full doc set) [VERIFIED].

### 4.3 IMPLEMENT Phase

**SWE-2 behavior**: "SWE-2 medium steps into action much quicker, allowing cost-efficient performance on simple and intermediate tasks."

**IPPS mapping**: The [IMPLEMENT] phase with [IMPLEMENT], [TEST], [FIX], [COMMIT] verbs. The `/implement` workflow's "Apply changes immediately without asking for permission" principle matches SWE-2's quick action on simple tasks [VERIFIED].

### 4.4 REFINE Phase

**SWE-2 behavior**: "Test coverage: SWE-2 is better at writing tests that check an implementation end-to-end, catching regressions and edge cases more reliably."

**IPPS mapping**: The [REFINE] phase with [REVIEW], [VERIFY], [CRITIQUE], [RECONCILE] verbs. The `/test` workflow's "Check SPEC for edge cases that need test coverage" and `/verify` workflow's compliance checking both map to SWE-2's improved test coverage and verification discipline [VERIFIED].

### 4.5 DELIVER Phase

**SWE-2 behavior**: "Verification discipline: When challenged, SWE-2 re-derives conclusions rather than re-asserts. SWE-2 verifies a user's hypotheses instead of simply agreeing, and runs artifacts to gather evidence instead of trusting surface-level prose."

**IPPS mapping**: The [DELIVER] phase with [VALIDATE], [MERGE], [DEPLOY], [CLOSE] verbs. The `/verify` workflow's compliance checking and `/critique` workflow's flaw-finding both benefit from SWE-2's re-derivation behavior [VERIFIED].

### 4.6 Resourcefulness

**SWE-2 behavior**: "Resourcefulness, within the user's boundaries: When the obvious path is blocked, SWE-2 is more willing to look for another route to the same answer."

**IPPS mapping**: The `/go` workflow's autonomous mode where `[ACTOR] = agent` and the agent self-resolves blockers using [RESEARCH], [CONSULT] (self-consult), and [DECIDE] verbs. SWE-2's resourcefulness directly enables the `/go` autonomous loop's blocker handling (TECHNICAL: try 3 alternatives, KNOWLEDGE: research, SCOPE: split) [VERIFIED].

## 5. Model Classification Within IPPS Taxonomy

### 5.1 Workflow Type

SWE-2 is a **BUILD-class** agent engine. Its primary output is working code. It executes BUILD-type workflows: `/implement`, `/bugfix`, `/fix`, `/test`, `/commit`, `/improve`, `/rename`, `/project-release` [VERIFIED].

The IPPS EDIRD phase model classifies workflows as BUILD when "Primary output is working code. Triggers: 'Add a feature...', 'Build...', 'Implement...'". SWE-2's entire training is oriented toward this class [VERIFIED].

### 5.2 Model Family

SWE-2 belongs to the **Cognition SWE model family** within the IPPS model registry:

```
Cognition Models in Registry
├── SWE-1.6 (1x cost) - baseline
├── SWE-1.6 Fast (1x cost)
├── SWE-1.7 Lightning Max (5x cost)
├── SWE-1.7 Lightning Medium (5x cost)
├── SWE-1.7 Max (1x cost)
├── SWE-1.7 Medium (1x cost)
├── SWE-check (Free)
└── SWE-2 (NOT YET IN REGISTRY)
```

The SWE family is Cognition's line of models specifically trained for agentic coding via RL. Unlike general-purpose LLMs (GPT, Gemini, Claude), SWE models are post-trained with coding-specific RL environments and instruction-following overlays [VERIFIED].

### 5.3 Effort Level to Complexity Mapping

SWE-2's effort levels map to IPPS complexity levels:

- **SWE-2 medium** → COMPLEXITY-LOW: Quick action on simple tasks, minimal exploration. Matches IPPS "Single file, clear scope, no dependencies" [ASSUMED]
- **SWE-2 high** → COMPLEXITY-MEDIUM: More planning, moderate exploration. Matches IPPS "Multiple files, some dependencies" [ASSUMED]
- **SWE-2 max** → COMPLEXITY-HIGH: Complex verification, extensive exploration. Matches IPPS "Breaking changes, new patterns, external APIs" [ASSUMED]

This mapping is [ASSUMED] because IPPS does not have an explicit model-effort-to-complexity mapping documented. The behavioral descriptions in the blog align with IPPS complexity definitions, but the mapping is inferred, not stated by Cognition.

### 5.4 Capability Tier

SWE-2 is in the **frontier tier** of coding models. The blog describes it as "our closest model yet to the frontier" and "pushing the Pareto frontier." It competes with:

- Fable 5.1 (Anthropic) - within 1 point on FrontierCode 1.1 Main
- GPT-5.6 Sol (OpenAI) - matched at a fraction of price
- GPT-6 Astra (OpenAI) - within a few points at quarter cost
- Grok 4.6 (xAI) - beaten on both score and cost [VERIFIED]

### 5.5 Cost Class

Based on the model registry's cost multiplier system (1x = SWE-1.7 baseline):

- SWE-1.7: 1x (baseline)
- SWE-1.7 Lightning: 5x
- SWE-2: Not yet listed, but blog says "64% cheaper than Fable 5.1" (Fable 5.1 = 20x in registry)

SWE-2 likely sits in the 1-5x cost range, making it a **cost-efficient frontier model** [ASSUMED].

## 6. Implications for IPPS Instruction Following

### 6.1 Core Alignment

SWE-2's instruction-following training and IPPS's instruction architecture are solving the same problem from opposite ends:

- **SWE-2**: Trains the model to follow multiple layered instructions without losing the task
- **IPPS**: Structures instructions in layers (rules, workflows, skills, MNF) to be followable

The better SWE-2 follows instructions, the better IPPS workflows execute. This is a symbiotic relationship [ASSUMED].

### 6.2 Specific IPPS Mechanisms That Benefit

**MUST-NOT-FORGET lists**: SWE-2's "keep multiple instructions in context" training directly supports MNF tracking. Each IPPS workflow has 3-10 MNF items that must be maintained throughout execution. SWE-2's training specifically targets this capability [ASSUMED].

**EDIRD phase gates**: SWE-2's verification discipline ("re-derives conclusions rather than re-asserts") supports the evidence-based gate evaluation that EDIRD requires. The `edird-phase-planning.md` rule states: "Gate output is mandatory. Before each phase transition, agent MUST output explicit gate evaluation." SWE-2's re-derivation behavior makes gate evaluations more reliable [ASSUMED].

**`/go` autonomous mode**: SWE-2's resourcefulness ("when the obvious path is blocked, look for another route") directly enables the `/go` workflow's autonomous blocker handling. The `/go` workflow requires the agent to try 3 alternative approaches for TECHNICAL blockers, research for KNOWLEDGE blockers, and split for SCOPE blockers [VERIFIED].

**`/verify` and `/critique` workflows**: SWE-2's "runs artifacts to gather evidence instead of trusting surface-level prose" directly improves verification quality. The `/verify` workflow checks compliance against formal rules, specs, and conventions. SWE-2's evidence-gathering behavior makes these checks more thorough [VERIFIED].

**`/bugfix` workflow**: SWE-2's test coverage improvement ("writes tests that check an implementation end-to-end, catching regressions and edge cases") directly supports the bugfix workflow's "Test impacted functionality BEFORE committing" and "Create test cases for each impacted area BEFORE implementing fix" requirements [VERIFIED].

### 6.3 Effort Level Optimization for IPPS Workflows

Based on the effort-to-complexity mapping, IPPS workflows can be matched to SWE-2 effort levels:

- **SWE-2 medium** for: `/prime`, `/commit`, `/cleanup`, `/session-save`, `/session-load`, `/switch-model` (simple, well-defined tasks)
- **SWE-2 high** for: `/implement`, `/bugfix`, `/fix`, `/test`, `/improve`, `/rename`, `/sync` (multi-step, some dependencies)
- **SWE-2 max** for: `/go` with COMPLEXITY-HIGH tasks, `/deep-research`, `/investigate`, `/project-release` (complex, multi-phase, high-stakes)

This mapping is [ASSUMED] - IPPS does not currently have an explicit model-effort selection mechanism per workflow. The `devin-auto-model-switcher` skill allows manual switching but does not auto-select based on workflow type.

### 6.4 Trustworthiness and Instruction Integrity

SWE-2's 98% trustworthiness pass rate means the model resists context manipulation. For IPPS, this means:

- Rules in `agent-behavior.md` are less likely to be bypassed by clever prompt construction
- MUST-NOT-FORGET items are less likely to be "forgotten" under adversarial context
- Workflow steps are less likely to be skipped due to context pressure
- The model will not simply agree with user hypotheses but verify them, matching the `/critique` workflow's "disregards formal rules" mindset [ASSUMED]

## 7. Model Registry Gap

The IPPS model registry (`windsurf-model-registry.json`, version 2.0, updated 2026-08-30) does not contain SWE-2. It contains:

- SWE-1.6 (1x cost)
- SWE-1.6 Fast (1x cost)
- SWE-1.7 Lightning Max (5x cost)
- SWE-1.7 Lightning Medium (5x cost)
- SWE-1.7 Max (1x cost)
- SWE-1.7 Medium (1x cost)
- SWE-check (Free)

The blog states SWE-2 is "available starting today in Devin Desktop and CLI" and "rolling it out on Devin Web and Fusion." The registry needs updating to include SWE-2 variants (likely medium, high, max effort levels) [VERIFIED].

## 8. Conclusions

1. SWE-2 is a BUILD-class agent engine in the Cognition SWE model family, specifically trained for agentic coding with instruction-following overlays [VERIFIED]

2. SWE-2's instruction-following training ("keep multiple instructions in context without losing sight of the underlying task") directly addresses IPPS's core challenge of layered instruction tracking. This is the most significant alignment between a model's training and IPPS's architecture to date [ASSUMED]

3. SWE-2's behavioral patterns map to all five EDIRD phases: focused exploration (EXPLORE), effort-gated planning (DESIGN), quick implementation (IMPLEMENT), test coverage and verification (REFINE), and evidence-based validation (DELIVER) [VERIFIED]

4. SWE-2's effort levels (medium, high, max) provide a natural mapping to IPPS complexity levels (LOW, MEDIUM, HIGH), enabling cost-aware workflow execution [ASSUMED]

5. The IPPS model registry needs updating to include SWE-2. The `devin-auto-model-switcher` skill's `update-model-registry` workflow should be run to add SWE-2 variants [VERIFIED]

6. SWE-2's trustworthiness (98% pass rate) and verification discipline make it particularly well-suited for IPPS's compliance-heavy workflows (`/verify`, `/critique`, `/bugfix`) where evidence-based evaluation is critical [ASSUMED]

## 9. Next Steps

1. Update `windsurf-model-registry.json` to include SWE-2 variants using the `update-model-registry` workflow
2. Consider adding effort-level recommendations to IPPS workflows based on the complexity-to-effort mapping
3. Evaluate whether SWE-2's instruction-following improvements reduce the need for verbose MUST-NOT-FORGET lists or if they remain necessary
4. Test SWE-2 with IPPS's most instruction-heavy workflows (`/go`, `/bugfix`, `/deep-research`) to validate instruction-following improvements
5. Document any behavioral differences observed when running IPPS workflows with SWE-2 vs SWE-1.7

## 10. Sources

**Primary Sources:**
- `DVNSWE2-IN01-SC-COGN-SWE2`: https://cognition.com/blog/swe-2 - SWE-2 announcement, training methodology, behavioral patterns, performance benchmarks, trustworthiness evaluation [VERIFIED]
- `DVNSWE2-IN01-SC-COGN-FR11`: https://cognition.com/blog/frontier-code-1.1 - FrontierCode 1.1 benchmark methodology and leaderboard [VERIFIED]
- `DVNSWE2-IN01-SC-COGN-SWE17`: https://cognition.com/blog/swe-1-7 - SWE-1.7 predecessor model for behavioral comparison [VERIFIED]
- `DVNSWE2-IN01-SC-ARXV-KIMIK3`: https://arxiv.org/abs/2607.24653 - Kimi K3 base model paper (2.8T parameters) [VERIFIED]
- `DVNSWE2-IN01-SC-COGN-TRUST`: https://cognition.com/blog/measuring-open-source-model-trustworthiness - Trustworthiness evaluation methodology [VERIFIED]

**Internal Sources:**
- `DVNSWE2-IN01-SC-IPPS-REG`: `windsurf-model-registry.json` - IPPS model registry (v2.0, 2026-08-30), SWE-2 absence confirmed [VERIFIED]
- `DVNSWE2-IN01-SC-IPPS-EDIRD`: `edird-phase-planning.md` - EDIRD phase model definitions and gate summaries [VERIFIED]
- `DVNSWE2-IN01-SC-IPPS-AGEN`: `agentic-english.md` - AGEN verb definitions for phase mapping [VERIFIED]
- `DVNSWE2-IN01-SC-IPPS-GO`: `go.md` - Autonomous mode workflow for resourcefulness mapping [VERIFIED]
- `DVNSWE2-IN01-SC-IPPS-IMPL`: `implement.md` - Implementation workflow for BUILD-class mapping [VERIFIED]
- `DVNSWE2-IN01-SC-IPPS-BUGFX`: `bugfix.md` - Bugfix workflow for test coverage mapping [VERIFIED]
- `DVNSWE2-IN01-SC-IPPS-TEST`: `test.md` - Test workflow for REFINE phase mapping [VERIFIED]

## 11. Document History

**[2026-09-12 12:45]**
- Fixed: "Kimi K33" corrected to "Kimi K3" throughout (Summary, Section 1.1, Sources)
- Added: Vendor-reported note on 64% cost claim (Summary, Section 1)
- Fixed: Workflow count 48 → 45+, skill count 24 → 21+ (Section 3.2)

**[2026-09-12 12:20]**
- Added: Section 2.8 "The Effort Parameter Paradigm Shift" - from mechanical dials to trained behavior, three layers of why Cognition did this, what you lose and gain, IPPS parallel

**[2026-09-12 12:15]**
- Added: Section 2 "Pareto Frontier RL Training Methodology" with detailed explanation of cost-penalized reward function, Jensen's functional equation proof, tangent condition for lambda_e selection, length-weighted reward baseline, and RL rollout serving infrastructure
- Changed: All subsequent sections renumbered (2→3 through 9→10, 10→11)
- Changed: Summary updated with two new Pareto-related findings
- Changed: Timeline updated to reflect 1 update

**[2026-09-12 12:00]**
- Initial research document created
