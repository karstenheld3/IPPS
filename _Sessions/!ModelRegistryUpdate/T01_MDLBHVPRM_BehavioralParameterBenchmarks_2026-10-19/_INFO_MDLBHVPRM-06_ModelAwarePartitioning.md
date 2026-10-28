# INFO: Model-Aware Workload Partitioning for /write-prompts

**Doc ID**: MDLRGUP-MDLBHVPRM-IN06
**Goal**: Find how `/write-prompts` can use model inventory data (capacity, instruction following, eagerness) to size prompts per model, so a sequence written for GLM-5.2 High does not skip instructions and a sequence written for Claude Fable 5.1 High is not fragmented
**Target file**: `.devin/workflows/write-prompts.md`, `.devin/skills/write-documents/PROMPTS_GUIDES.md` (Sections 1c, 1f, 5), `.devin/skills/llm-evaluation/model-registry.json`

**Depends on:**
- `_INFO_MDLBHVPRM-05_CoverageMatrix.md [MDLRGUP-MDLBHVPRM-IN05]` for benchmark coverage per model
- `_INFO_MDLBHVPRM-03/04` for benchmark definitions and scores

## Summary

- **Root cause**: The current method sizes prompts by one axis only - `effort` (PRMT-SC-05) - with qualitative guidance ("low effort = one file, one edit"). Two models at the same effort get the same partition. GLM-5.2 High and Claude Fable 5.1 High differ by at least two independent behavioral axes that effort does not capture. [VERIFIED - read of PROMPTS_GUIDES.md 1c/1f, PROMPTS_RULES.md PRMT-SC-05/07]
- **Three orthogonal axes** must drive partitioning: 1) **capacity** (how much work per run: context, max_output, effort), 2) **instruction_following** (how many instruction items per prompt survive without being dropped), 3) **eagerness** (how much scope discipline the prompt must enforce). Effort only scales axis 1. [VERIFIED - user observation + OverEager/IFEval findings]
- **Your precision paradox has a mechanism**: more precise prompts carry more instruction items; models with low instruction following drop items from the middle of long lists (lost-in-the-middle, already noted in PROMPTS_GUIDES.md Section 5 as "5-8 rules, threshold varies by model"). The threshold is the variable that must become model-specific. Fix is not less precision - it is fewer items per prompt plus a checkpoint after every prompt. [VERIFIED]
- **Benchmark data is a weak proxy for instruction_following in our use case**: IFEval estimates GLM-5.2 at 93.2% (same as GPT-5.4), which contradicts observed skipping. IFEval tests 1-3 format constraints on short prompts, not 8-15 item agentic instruction lists. IFBench/IFEval-Hard discriminate better but cover almost none of our models. [VERIFIED - benchgap.net, IFEval-Hard dataset card]
- **Benchmark data is a usable proxy for eagerness of GLM**: OverAct SIR 2.00 for GLM-5.2 and OverEager rate 25.8% for GLM-5 (highest in both studies) match the observed over-eager interpretation. No eagerness data exists for any Claude Fable/Opus 5 or GPT-5.4+ model. [VERIFIED - OverAct, SNARE papers]
- **Recommendation**: Option 2 (behavior tiers in the model inventory, seeded from benchmarks and corrected by observation) now; Option 3 (IPPS probe + checkpoint feedback loop) as the data source that refines tiers into per-model numbers (Option 1) later. Details in Sections 5-7.

## 1. Current Method (As-Is)

Workload per prompt is decided in four places, all qualitative:

- **PRMT-SC-05 / Guides 1c** - `effort` in frontmatter sets scope: low = one file/one edit; high = multi-file. "Model name, context window size, and effort level together determine how many prompts a task needs" - but no lookup exists; the writing agent judges from the model name alone. [VERIFIED]
- **PRMT-SC-07 / Guides 1f** - load of workflow invocations on three axes (input volume, output volume, reasoning depth) compared against "the run budget from the frontmatter". Budget is never quantified. [VERIFIED]
- **Guides Section 5** - density heuristic: 5-8 high-priority instructions per prompt, "exact threshold varies by model and task". The model dependency is acknowledged but not parameterized. [VERIFIED]
- **STRUT Strategy** - optional AWT estimate and free-text model hints ("Opus for analysis, Sonnet for fixes"). `edird-phase-planning` adds step calibration: >30 min AWT or >3 files = decompose; <2 min = combine. Model-agnostic. [VERIFIED]

Model inventory today (`model-registry.json` 1.9.0): provider, model_id, context_window, status, effort levels, max_output, API method. **No behavioral fields.** `windsurf-model-registry.json` has name and cost only. `/switch-model` has three hard-coded tiers (HIGH/MID/LOW) by name. [VERIFIED]

```
Current:   effort ──────────────────────> prompt scope (qualitative)

Needed:    capacity (ctx, max_output, effort) ──> work units per prompt
           instruction_following ─────────────> max instruction items per prompt, checkpoint interval
           eagerness ─────────────────────────> scope-guard strictness, blast-radius containment
```

## 2. Failure Modes Observed vs Axes

| Observation                                        | Axis                  | Partition response                                              |
|----------------------------------------------------|-----------------------|-----------------------------------------------------------------|
| GLM-5.2 High skips instructions in precise prompts | instruction_following | Fewer items per prompt, critical items at edges, verify every prompt |
| GLM-5.2 High does more than asked                  | eagerness             | Explicit "only these items" guard, negative-constraint list, smaller units |
| Fable 5.1 High completes very large prompts        | capacity + IF         | Fewer, broader prompts; checkpoint every 3                      |
| Same model, different agent framework, 1-28% overeager | deployment context | Treat registry value as intrinsic baseline; prompt guards are the per-deployment control |

GLM-5.2 combines low instruction following with high eagerness - the worst quadrant: it drops requested items and adds unrequested ones. The two must be controlled by different prompt mechanisms; neither is fixed by raising effort (user reports High effort still skips). [VERIFIED - user report]

## 3. What the Benchmark Data Can and Cannot Give

**instruction_following** [VERIFIED - IN03, IN05]:
- IFEval (prompt-level strict) covers 43% of llm-evaluation registry, 53% of Devin base models. Scores for frontier models cluster 85-95% - low discrimination.
- IFEval does not predict multi-item agentic compliance: GLM-5.2 93.2% (estimated) vs GPT-5.4 93.5% while observed behavior differs sharply.
- IFEval-Hard shows the real spread hidden by IFEval: GPT-5 82.4% vs GPT-4.1 58.1% vs GPT-4o 39.9%. Only 7 models tested.
- WildIFEval (multi-constraint, real prompts) is conceptually the right benchmark - best models reach only ~70% strict - but publishes only 14 models, none current.
- **Usable as**: a lower-bound sanity check and a tie-breaker; not as the primary source for partition thresholds.

**eagerness** [VERIFIED - IN04, IN05]:
- OverAct SIR is the metric closest to our 0.5-2.0 scale (1.0 = exact scope). Covers GLM-5.2 (2.00), DeepSeek-v3 (1.18), Kimi-K2.7 (1.60). No OpenAI, no Anthropic.
- OverEager/SNARE: Sonnet-4.6 21%, GPT-5.3-Codex 10%, GLM-5 26%, Gemini-2.5-Pro 22%. Framework explains 56% of variance, base model 21%.
- YapBench covers 76 models but measures text verbosity, not action scope.
- **Usable as**: seed values for GLM, Kimi, Sonnet-4.6, GPT-5.3-Codex families; family inheritance for the rest with `[ASSUMED]`.

**Coverage verdict**: 8-20% of our models have eagerness data; 43-53% have instruction-following data of weak relevance. Any option must work with missing values. [VERIFIED - IN05]

## 4. Partition Parameters a Model Profile Must Produce

Whatever the option, `/write-prompts` needs these five numbers per `intended_model` + `effort`:

- **max_items** - instruction/constraint items per prompt before drop-out risk. Base 8 (Guides Section 5) scaled: `round(8 * instruction_following)`. IF 1.0 = 8, IF 0.75 = 6, IF 0.5 = 4.
- **max_files** - files touched per implementation prompt. From capacity tier (context_window, max_output, effort): 1 / 3 / 6+. Reduce by 1 when eagerness > 1.3 (smaller blast radius for scope creep).
- **checkpoint_interval** - implementation prompts between `/verify` + `/fix` checkpoints (PRMT-SQ-04 currently fixed at 2-3). IF >= 0.9 = 3, 0.75-0.9 = 2, < 0.75 = 1.
- **scope_guard** - `normal` (current constraints block) or `strict` (adds: "Do ONLY the numbered items below. Do not refactor, rename, add tests, or touch files not listed. Report any item you could not complete as NOT DONE"). `strict` when eagerness > 1.3 or IF < 0.75.
- **heavy_workflows_per_prompt** - from PRMT-SC-07: 1 for capacity tier low/mid, 2 for high only when IF >= 0.9.

Then `prompt_count = ceil(total_items / max_items)` bounded by `max_files` and chain length (PRMT-SC-04), plus checkpoints.

## 5. Option 1 - Per-Model Behavioral Fields in the Registry (Data-Driven)

**What**: Add to each `model-registry.json` entry:
```json
"behavior": { "instruction_following": 0.70, "eagerness": 1.8, "capacity_tier": "high",
              "source": "IFEval 93.2 est (benchgap); OverAct SIR 2.00; observed skipping 2026-10", "confidence": "low" }
```
`/write-prompts` Step 1 reads `intended_model`, resolves the entry (prefix match like `model_id_startswith`), computes Section 4 parameters, states them in the file's opening commentary. Missing entry = fall back to family default, then to current qualitative method, and write a PROBLEMS.md entry.

**Why it works**: One source of truth, machine-readable, reusable by STRUT model hints, `/switch-model`, and the llm-evaluation CLI. Partition becomes reproducible and reviewable.

**Implication**: Seeding 75 + ~40 models with numbers that are 50% proxy and 90% assumed produces false precision - a `0.70` next to a `0.93` looks measured when neither is. Needs confidence field discipline and a maintenance step in `update-model-registry.md`. Benchmarks must be re-scraped per release. [ASSUMED - effort estimate]

## 6. Option 2 - Behavior Tiers Seeded from Benchmarks, Corrected by Observation (RECOMMENDED)

**What**: Define 3 partition tiers in `PROMPTS_GUIDES.md` Section 1c and map models to tiers in one small file (extend `/switch-model` HIGH/MID/LOW into a `model-behavior-tiers.json` in `llm-evaluation`, or a section in the registry `_comment`):

- **TIER-A** (IF >= 0.9, eagerness 1.0-1.2): Claude Opus 4.6-4.8, Fable 5.x, GPT-5.4/5.5, o3 - max_items 8, max_files 6, checkpoint every 3, scope_guard normal
- **TIER-B** (IF 0.75-0.9 or eagerness 1.2-1.5): Sonnet 4.5/4.6, GPT-5/5.1/5.2, GPT-4.1, Gemini 3.x Pro - max_items 6, max_files 3, checkpoint every 2, scope_guard normal + explicit file list
- **TIER-C** (IF < 0.75 or eagerness > 1.5): GLM-5.x, GLM-4.x, Flash/mini/nano variants, Kimi - max_items 4, max_files 1-2, checkpoint every 1, scope_guard strict

Tier assignment rule: benchmark seed (IFEval-Hard, OverAct, OverEager where available) sets the initial tier; a documented observation (FAILS.md or findings-card entry naming model + skipped items) overrides upward in strictness. GLM-5.2 lands in TIER-C by observation despite IFEval 93%.

**Why it works**: Works with 8% eagerness coverage because tiers need only an ordinal decision, not a calibrated number. Matches the HIGH/MID/LOW mental model already in use. Experience overrides benchmarks explicitly, which is the correct precedence given Section 3. Writing agent gets concrete numbers (Section 4) without false precision.

**Implication**: Coarse - a low-IF but low-eagerness model gets the same strict scope guard as a high-eagerness one (harmless but adds tokens). Tier file is a second model list to maintain; mitigated by keying on `model_id` prefixes so new variants inherit. Changes: PROMPTS_GUIDES 1c/1f/5, write-prompts Step 1 (read tier, state parameters in commentary), PRMT-SC-05 text (effort AND tier), new PRMT rule for the strict scope guard.

**Why recommended**: Solves the GLM-5.2 vs Fable 5.1 problem on day one with data we already have, keeps the door open to Option 1 as tier evidence accumulates, and costs the least.

## 7. Option 3 - IPPS Probe plus Checkpoint Feedback Loop (Measure, Do Not Estimate)

**What**: Two data sources that measure the actual quantity instead of a proxy:
1. **Probe**: a fixed `_PROMPTS_` file in `llm-evaluation` with N=12 numbered, independently checkable instruction items and an explicit scope boundary, run per model via `call-llm.py` (or Lana for Devin-only models). instruction_following = items completed / N. eagerness = 1 + (out-of-scope actions / N). Results written to the registry `behavior` block with `confidence: measured`.
2. **Feedback loop**: every verification checkpoint already runs `/verify` + `/fix`; extend the findings card entry format with `skipped_items: N/M` and `out_of_scope: N`. `/session-finalize` aggregates per `intended_model` into the registry.

**Why it works**: Measures multi-item agentic compliance - the quantity IFEval does not. Covers every model you have API access to, including Fable 5.1 and GLM-5.2 where benchmarks are silent. Values improve with use at no extra cost.

**Implication**: Upfront build (probe design, scorer, registry writer) and API spend per model per release. Probe must avoid IPPS-specific phrasing so it measures the model, not familiarity. Devin-internal models (SWE-*, Arena) cannot be probed via API. Framework dependence (56% of variance) means probe values from `call-llm.py` under-estimate eagerness seen inside Cascade - the feedback loop corrects this over time. [ASSUMED - effort and cost]

## 8. Exclusions

- **Dynamic in-run adaptation** (agent re-partitions mid-sequence based on its own skips): excluded - breaks PRMT-SC-02 self-containment and makes sequences non-reproducible.
- **Using Devin cost multiplier as capability proxy**: excluded - cost tracks price tier, not instruction compliance (GLM-5.2 High 1.8x, GPT-5.6 Luna 0.5x).
- **YapBench as primary eagerness source**: excluded - verbosity is not action scope; kept as tie-breaker only.
- **MT-Bench, AlpacaEval, Arena Elo**: excluded - preference/helpfulness, not compliance or scope.

## Sources

- `_INFO_MDLBHVPRM-02_Sources.md` - 21 benchmark sources with IDs (IFEval, IFBench, IFEval-Hard, WildIFEval, WildBench, OverAct, OverEager/SNARE, ScopeBench, YapBench, DNR Bench)
- `_INFO_MDLBHVPRM-05_CoverageMatrix.md` - per-model coverage for both registries
- `.devin/skills/write-documents/PROMPTS_GUIDES.md` Sections 1c, 1e, 1f, 5 - current partition method
- `.devin/skills/write-documents/PROMPTS_RULES.md` PRMT-SC-04, SC-05, SC-07, SQ-04
- `.devin/workflows/write-prompts.md` Step 1
- `.devin/skills/write-documents/STRUT_TEMPLATE.md` - Strategy node, AWT, model hints
- `.devin/skills/edird-phase-planning/SKILL.md` - Scope Calibration, AWT budgets
- `.devin/skills/llm-evaluation/model-registry.json` 1.9.0, `model-parameter-mapping.json` 2.4.0
- `.devin/skills/devin-auto-model-switcher/windsurf-model-registry.json` 2.1
- `.devin/workflows/switch-model.md` - HIGH/MID/LOW tiers
- `https://benchgap.net/b/ifeval/current` - GLM-5.2 93.2% est, GPT-5.4 93.2% est (accessed 2026-10-19)
- `https://huggingface.co/datasets/rahul-singhal/IFEval-Hard` - GPT-5 82.4%, GPT-4.1 58.1%, GPT-4o 39.9% (accessed 2026-10-19)
- `https://lettokenburn.com/b/overact/` - GLM-5.2 SIR 2.00 (accessed 2026-10-19)
- `https://arxiv.org/abs/2605.28122` - SNARE: framework 56% vs model 21% of variance (accessed 2026-10-19)

## Document History

**[2026-10-19 16:45]**
- Initial research: current method analysis, axis model, three options with recommendation
