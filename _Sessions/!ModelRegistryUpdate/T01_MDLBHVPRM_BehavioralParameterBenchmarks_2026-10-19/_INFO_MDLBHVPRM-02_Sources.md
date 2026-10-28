# INFO: Sources - Model Behavioral Parameter Benchmarks

**Doc ID**: MDLRGUP-MDLBHVPRM-IN02
**Strategy**: MEPI | **Domain**: DEFAULT
**Preflight accuracy**: 6/7 verified (assumption 2 was wrong - multiple eagerness benchmarks exist)

## Instruction Following Benchmarks

- **MDLBHVPRM-SC-GOOG-IFEVAL**: IFEval - Instruction-Following Evaluation for Large Language Models (Zhou et al., Google, 2023-11). Paper: `https://arxiv.org/abs/2311.07911`. 541 prompts, 25 verifiable constraint types, programmatic scoring. [VERIFIED] Accessed: 2026-10-19
- **MDLBHVPRM-SC-LLMST-IFEVLB**: IFEval Leaderboard at llm-stats.com. `https://llm-stats.com/benchmarks/ifeval`. 70 models with scores. [VERIFIED] Accessed: 2026-10-19
- **MDLBHVPRM-SC-BNCGP-IFEVAL**: IFEval Leaderboard at benchgap.net. `https://benchgap.net/b/ifeval/current`. 139+ models with measured and estimated scores. [VERIFIED] Accessed: 2026-10-19
- **MDLBHVPRM-SC-LLMBT-IFEVAL**: IFEval Tracker at alloevil.github.io. `https://alloevil.github.io/llm-benchmarks-tracker/b/ifeval/`. Full ledger with source conditions. [VERIFIED] Accessed: 2026-10-19
- **MDLBHVPRM-SC-BNRG-IFEVAL**: IFEval at Benchmark Registry. `https://benchmarkregistry.org/benchmarks/ifeval/original`. Gemma 4 results (98.5-98.9%). [VERIFIED] Accessed: 2026-10-19
- **MDLBHVPRM-SC-AI2-IFBNCH**: IFBench - Generalizing Verifiable Instruction Following (Allen AI, 2026). Paper: `https://arxiv.org/abs/2507.02833`. 58 new constraints, leading models <50%. [VERIFIED] Accessed: 2026-10-19
- **MDLBHVPRM-SC-HFDS-IFHRD**: IFEval-Hard dataset (Singhal et al., 2026). `https://huggingface.co/datasets/rahul-singhal/IFEval-Hard`. 148 hard examples. GPT-5 82.4%, GPT-4.1 58.1%. [VERIFIED] Accessed: 2026-10-19
- **MDLBHVPRM-SC-ARXI-WIFEVL**: WildIFEval - Instruction Following in the Wild (2025). Paper: `https://arxiv.org/abs/2503.06573`. 7K real user instructions, best models ~70%. [VERIFIED] Accessed: 2026-10-19
- **MDLBHVPRM-SC-BNLD-WLDBCH**: WildBench (HELM) leaderboard. `https://www.benchleader.com/benchmarks/helm_wildbench`. 68 models, Stanford CRFM. [VERIFIED] Accessed: 2026-10-19
- **MDLBHVPRM-SC-SRNT-CMPRE**: Claude Sonnet 4.5 vs GPT-5 comparison. `https://serenitiesai.com/benchmark/compare/claude-sonnet-4-5-vs-gpt-5`. IFEval: GPT-5 90%, Sonnet 4.5 88%. [VERIFIED] Accessed: 2026-10-19

## Eagerness / Scope Expansion Benchmarks

- **MDLBHVPRM-SC-ARXI-OVRGEN**: OverEager-Gen / OverEager-Bench (2026-05). Paper: `https://arxiv.org/abs/2605.18583`. 500 scenarios, 4 agents, 6 models, ~7500 runs. [VERIFIED] Accessed: 2026-10-19
- **MDLBHVPRM-SC-ARXI-SNARE**: SNARE / OverEager adaptive benchmark (2026-05). Paper: `https://arxiv.org/abs/2605.28122`. 4 agents x 5 models, 10K runs, 19.51% grand mean overeager rate. [VERIFIED] Accessed: 2026-10-19
- **MDLBHVPRM-SC-ARXI-OVRACT**: OverAct - Proactive Over-Authorization (2026-10). Paper: `https://arxiv.org/abs/2610.01508`. SIR metric (Scope Inflation Ratio), 7 models, 130K runs. [VERIFIED] Accessed: 2026-10-19
- **MDLBHVPRM-SC-ARXI-SCPBNCH**: ScopeBench - Engagement Boundaries Under Goal Pressure (2026-09). Paper: `https://arxiv.org/abs/2609.30325`. 30 tasks, 8 models, raw capability vs scope adherence. [VERIFIED] Accessed: 2026-10-19
- **MDLBHVPRM-SC-THAG-OVREG**: OverEager-Bench Leaderboard at The Aggregate. `https://theaggregate.ai/benchmark?slug=overeager-bench-claude-code`. Per-agent leaderboards. [VERIFIED] Accessed: 2026-10-19
- **MDLBHVPRM-SC-BNLS-OVREG**: OverEager Benchmark at BenchmarkList. `https://benchmarklist.com/benchmarks/overeager/`. 20 agent-model pairs ranked. [VERIFIED] Accessed: 2026-10-19
- **MDLBHVPRM-SC-LTKB-OVRACT**: OverAct Leaderboard at LetTokenBurn. `https://lettokenburn.com/b/overact/`. 7 models with SIR scores. [VERIFIED] Accessed: 2026-10-19

## Verbosity / Over-Generation Benchmarks

- **MDLBHVPRM-SC-ARXI-YAPBNCH**: YapBench - Do Chatbot LLMs Talk Too Much? (2026-01). Paper: `https://arxiv.org/abs/2601.00624`. YapIndex metric, 76 models, excess character measurement. [VERIFIED] Accessed: 2026-10-19
- **MDLBHVPRM-SC-ARXI-BNCHOF**: BenchOverflow - Measuring Overflow in LLMs (2026-01). Paper: `https://arxiv.org/abs/2601.08490`. CSR metric, 9 models, overflow behavior. [VERIFIED] Accessed: 2026-10-19
- **MDLBHVPRM-SC-AAAI-DNRBNCH**: DNR Bench - Over-Reasoning in Reasoning LLMs (AAAI 2026). Paper: `https://ojs.aaai.org/index.php/AAAI/article/view/41055`. 150 prompts, token inefficiency up to 70x. [VERIFIED] Accessed: 2026-10-19
- **MDLBHVPRM-SC-ACL-VRBCMP**: Verbosity Compensation in LLMs (ACL 2025). Paper: `https://aclanthology.org/2025.uncertainlp-main.14.pdf`. 14 LLMs, 5 datasets, VC frequency analysis. [VERIFIED] Accessed: 2026-10-19
