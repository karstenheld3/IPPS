# INFO: Summary - Model Behavioral Parameter Benchmarks

**Doc ID**: MDLRGUP-MDLBHVPRM-IN01
**Goal**: Find benchmarks and data sources to populate `eagerness` (0.5-2.0) and `instruction_following` (0.2-1.0) for all models in the model registry
**Strategy**: MEPI | **Domain**: DEFAULT
**Research stats**: ~40m net | 3 docs | 21 sources

## Research Question

Which publicly available benchmarks and datasets can provide first-assessment values for two new model registry parameters: `eagerness` (how much a model over/under-delivers relative to task scope, 0.5-2.0) and `instruction_following` (adherence to complex instructions, 0.2-1.0)?

## Key Findings

### instruction_following: Well-Served by Existing Benchmarks

**IFEval** (Google, 2023) is the industry standard with the broadest model coverage (850+ results). Its prompt-level strict accuracy produces a 0-1 score that maps directly to our parameter with no transformation needed. Coverage includes most OpenAI and Anthropic models in our registry. Z.AI (GLM) coverage is sparse but available via WildBench.

**Problem**: IFEval is saturating. Frontier models cluster at 85-95%, reducing discrimination. **IFBench** (Allen AI, 2026) and **IFEval-Hard** provide harder alternatives where leading models score 40-80%, offering better spread.

**Data availability**: HIGH. Multiple public leaderboards maintain up-to-date scores. IFEval can be run locally via HuggingFace for models without published scores.

### eagerness: Emerging Research Area, Fragmented Data

"Eagerness" maps to a 2025-2026 research wave under names: overeager behavior, scope expansion, over-authorization, verbosity. Five benchmarks measure aspects of it:

1. **OverAct SIR** - Scope Inflation Ratio (tools called / tools needed). Most direct mapping to our scale. But only 7 models tested, none from OpenAI or Anthropic.
2. **OverEager-Bench/SNARE** - Overeager coding agent rate. 6 base models tested including Sonnet-4.6 and GPT-5.3-Codex. Critical finding: framework accounts for 56% of effect, model only 21%.
3. **YapBench** - Verbosity measurement. 76 models, best coverage. But measures text length, not action scope.
4. **ScopeBench** - Scope adherence under pressure. 8 models, security context.
5. **DNR Bench** - Over-reasoning in reasoning models. Token inefficiency up to 70x.

**Data availability**: LOW-MEDIUM. No single benchmark covers both our model set AND the full eagerness concept. Composite scoring from multiple sources is required, with many gaps filled by expert estimates.

### Critical Finding: Eagerness Is Framework-Dependent

OverEager-Bench found that Sonnet-4.6 alone spans 1.1-27.7% overeager rate across different agent frameworks. The framework (permission model, tool gating) dominates the base model's inherent eagerness. Our registry tracks base models, but eagerness manifests differently depending on how the model is deployed.

**Implication**: Registry eagerness values should be treated as "intrinsic tendency" baselines, not deployment-specific predictions.

## Comparison: Benchmarks for Our Two Parameters

### instruction_following data landscape

- **IFEval**: 850+ models, 0-1 scale, direct mapping, HIGH coverage -> PRIMARY
- **IFBench**: ~72 models, 0-1 scale, harder, MEDIUM coverage -> SECONDARY
- **WildBench**: 68 models, 0-100 scale, broader tasks, HIGH coverage -> SUPPLEMENTARY
- **IFEval-Hard**: 7 models, 0-1 scale, hard subset -> SUPPLEMENTARY

### eagerness data landscape

- **OverAct**: 7 models, SIR ratio, direct mapping, LOW coverage -> PRIMARY (where available)
- **SNARE/OverEager**: 5-6 models, % rate, agent-specific, LOW coverage -> SECONDARY
- **YapBench**: 76 models, excess chars, verbosity only, HIGH coverage -> SUPPLEMENTARY
- **ScopeBench**: 8 models, scope adherence, security context -> SUPPLEMENTARY
- **DNR Bench**: 8 models, token inefficiency, reasoning-specific -> SUPPLEMENTARY

## Recommendation

### Phase 1: Populate from existing benchmark data (automated)

1. **instruction_following**: Scrape IFEval prompt-level strict accuracy from public leaderboards for all registry models. Map directly to 0.2-1.0 scale. Fill gaps with WildBench scores (normalize 0-100 to 0-1).

2. **eagerness**: Scrape OverAct SIR where available. Scrape YapBench YapIndex for broader coverage. Compute composite: `eagerness = 1.0 + (normalized_excess * scaling_factor)`. Mark all values with source benchmark.

### Phase 2: Fill gaps via own testing (semi-automated)

3. Create a small **eagerness probe**: 20-30 prompts with defined scope boundaries, run against each model, measure scope inflation. This is more feasible than running full benchmark suites. Can be integrated into the model update workflow.

4. Create an **instruction_following probe**: Run IFEval's public 541 prompts against models lacking scores, using the published verification code.

### Phase 3: Continuous maintenance

5. Add both parameters to `model-registry.json` schema. Add benchmark source field.
6. Include probe execution in the `update-model-registry.md` workflow.

### Implementation Priority

Start with `instruction_following` - data is abundant, mapping is direct, one afternoon of scraping populates most models. `eagerness` requires more work: composite scoring methodology, gap filling via own probes, careful documentation of data provenance.

## Limitations

- Z.AI (GLM) models have minimal coverage across all benchmarks
- Older models (GPT-4o-2024-05-13, Claude 3-3.5 family) may lack recent benchmark data
- Eagerness under-delivery subscale (0.5-1.0) has no reliable benchmark source
- IFEval contamination risk is high - models may be specifically trained on its constraints
- All eagerness benchmarks are <18 months old; methodology and leaderboards may shift

## Source Files

- `_INFO_MDLBHVPRM-02_Sources.md` - Full source list with IDs
- `_INFO_MDLBHVPRM-03_InstructionFollowingBenchmarks.md` - Detailed IF benchmark analysis
- `_INFO_MDLBHVPRM-04_EagernessBenchmarks.md` - Detailed eagerness benchmark analysis

## Document History

**[2026-10-19 16:50]**
- Initial summary with cross-document synthesis
