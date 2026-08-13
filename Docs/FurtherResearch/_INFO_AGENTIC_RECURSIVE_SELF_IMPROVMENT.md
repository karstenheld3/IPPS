# INFO: Agentic Recursive Self-Improvement

**Doc ID**: RECSLFIM-IN01
**Goal**: Map the current state of Recursive Self-Improvement (RSI) in AI - what it is, where it stands, what it implies for agentic development systems like IPPS
**Timeline**: Created 2026-08-13, Updated 3 times (2026-08-13 - 2026-08-13)

## Summary

- Recursive Self-Improvement (RSI) is AI systems materially participating in their own development cycle - writing code, running experiments, optimizing architectures - not yet full autonomous self-redesign [VERIFIED]
- [Anthropic](https://www.anthropic.com/institute/recursive-self-improvement) reports >80% of merged production code at Anthropic authored by Claude as of 2026-05, with 8x engineer output increase since 2024 [VERIFIED]
- [METR (Model Evaluation and Threat Research)](https://metr.org/time-horizons/) time horizon measurements show AI task completion doubling every ~4 months (accelerating from earlier 7-month trend), with Claude Opus 4.6 managing 12-hour tasks [VERIFIED]
- [Weco AI](https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement) demonstrated AIDE2, claimed first experimental Level 1 RSI: an outer-loop agent improved its own inner-loop agent beyond 2 years of human tuning in 8 unattended days [VERIFIED]
- [Discovery Loop](https://techcrunch.com/2026/08/05/jeff-dean-and-other-top-ai-researchers-are-leaving-google-to-launch-their-own-startup/), Jeff Dean's new startup, explicitly targets RSI for scientific research - using AI to automate complete experimental loops [VERIFIED]
- The remaining human bottleneck is research taste and direction-setting (choosing which problems to work on), not execution [VERIFIED]
- Academic taxonomy distinguishes bounded self-refinement (convergent, evaluable, already industrial practice) from open-ended RSI (unbounded, still theoretical) [VERIFIED]
- Full autonomous RSI (AI rewriting its own weights without human involvement) remains speculative; current reality is "RSI-adjacent" operations under human supervision [VERIFIED]
- Safety/governance frameworks lag behind RSI capabilities: the [2026 International AI Safety Report](https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026) identifies RSI as a national-security-level risk [VERIFIED]
- Information-theoretic impossibility results show that classifier-based safety gates cannot simultaneously permit unbounded self-improvement and maintain bounded cumulative risk [VERIFIED]
- The [Institute for Security and Technology](https://securityandtechnology.org/blog/ist-launches-rsi-initative/) launched an $875K RSI governance initiative (2026-08-11), signaling institutional urgency [VERIFIED]

## Table of Contents

1. [Definition and Taxonomy](#1-definition-and-taxonomy)
2. [Evidence: RSI in Practice](#2-evidence-rsi-in-practice)
3. [Academic Foundations](#3-academic-foundations)
4. [Safety and Governance](#4-safety-and-governance)
5. [Implications for Agentic Development Systems](#5-implications-for-agentic-development-systems)
6. [Conclusions](#6-conclusions)
7. [Next Steps](#7-next-steps)
8. [Sources](#8-sources)

## 1. Definition and Taxonomy

### 1.1 What RSI Is

Recursive Self-Improvement (RSI) is the capacity of an AI system to meaningfully accelerate or enhance its own development. The concept traces back to I.J. Good's 1965 "ultraintelligent machine" thought experiment: a machine that surpasses all human intellectual activity and can therefore design even better machines, triggering an "intelligence explosion."

In practice, RSI operates on a spectrum. A [2026 arXiv survey](https://arxiv.org/html/2607.07663) of 1,250 papers (2024-2026) identifies two fundamental categories:

- **Bounded self-refinement** - convergent, evaluable, already industrial practice. Includes self-refine, self-reward, self-play methods where the system improves its outputs within a fixed loop
- **Open-ended RSI** - the system improves the improvement process itself, potentially without bound. Remains bounded in practice by grounding requirements, collapse dynamics, and compute constraints

### 1.2 The RSI Ladder

[Weco AI](https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement) proposed a 4-level ladder for grading RSI:

- Level 0 - **Delegation**: Autonomous system runs R&D loop end-to-end but improves more slowly than human R&D
- Level 1 - **Net positive**: System improves itself more efficiently than humans improving the same system. Requires: fair human baseline, sustained multi-step trend, generalization beyond optimized measurement, fixed budget
- Level 2 - **Ignition**: System improves its own ability to improve (the improved agent becomes a better optimizer than its predecessor)
- Level 3 - **Inflection**: Progress stops slowing at fixed budget and starts accelerating

Most current "self-improvement" claims are Level 0. AIDE2 is claimed as Level 1. No system has demonstrated Level 2 or 3.

### 1.3 What RSI Is Not (Yet)

Full autonomous RSI - an AI system rewriting its own weights without human involvement - remains speculative. What has emerged is an earlier, operationally significant threshold: AI systems materially participating in the development of successor AI systems under human supervision. The [Cloud Security Alliance](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/06/AI_recursive_self_improvement_security_implications_v1.0-csa-styled.pdf) terms this "RSI-adjacent" operations.

## 2. Evidence: RSI in Practice

### 2.1 Anthropic: AI Building AI

Anthropic's ["When AI Builds Itself"](https://www.anthropic.com/institute/recursive-self-improvement) (2026-05) is the first public quantitative account by a frontier AI developer of RSI-adjacent operations within its own development. Key metrics:

- **Code authorship**: >80% of merged production code authored by Claude (2026-05), up from low single digits before Claude Code launch (2025-02)
- **Productivity multiplier**: Engineers merge 8x as much code per day as in 2024. Median employee self-report: ~4x output increase
- **Quality parity**: Claude-written code quality reached rough parity with human-written code at Anthropic in 2026. Automated Claude reviewer catches ~33% of bugs that caused past incidents before reaching production
- **Research execution**: Claude achieved ~52x speedup on code optimization tasks (2026-04), up from ~3x (2025-05). Skilled human baseline: ~4x in 4-8 hours
- **Open-ended research**: In a weak-to-strong supervision experiment, Claude agents recovered 97% of the performance gap over 800 cumulative hours ($18K compute), vs 23% by two human researchers over ~1 week
- **Research judgment**: Claude's next-step suggestions judged better than human researcher choices 64% of the time on challenging moments (2026-04), up from 51% (2025-11)

Anthropic identifies a narrowing human role: "the doing now costs almost nothing in human time." The remaining comparative advantage is research taste and judgment - choosing which problems matter.

### 2.2 METR Time Horizons

[METR](https://metr.org/time-horizons/) measures the task-completion time horizon: the task duration (measured by human expert completion time) at which an AI agent succeeds with 50% reliability. The trajectory:

- 2024-03: Claude Opus 3 managed ~4-minute tasks
- 2025-03: Claude Sonnet 3.7 managed ~90-minute tasks
- 2026-03: Claude Opus 4.6 managed 12-hour tasks
- Claude Mythos Preview worked "at least" 16 hours, at upper end of what METR can measure

The doubling time has accelerated from ~7 months (2019-2025 trend) to ~4 months (post-2023 trend under TH1.1 methodology). If the trend holds, week-long tasks come into range in 2027. METR projects month-long task capability (167 working hours) between mid-2028 and mid-2031.

Important caveat from METR: doubling the time horizon does not double the degree of automation. Longer tasks fail in more complex ways requiring more human labor per intervention.

### 2.3 Discovery Loop: RSI for Science

[Discovery Loop](https://techcrunch.com/2026/08/05/jeff-dean-and-other-top-ai-researchers-are-leaving-google-to-launch-their-own-startup/), founded 2026-08 by Jeff Dean, Sanjay Ghemawat, Quoc Le, and Oriol Vinyals (all ex-Google), is a public benefit corporation explicitly targeting RSI for scientific discovery. Their thesis: "While science and engineering have tremendously advanced society, progress has traditionally relied on slow, sequential human iterations, creating a significant bottleneck." The company plans to use AI to automate complete experimental loops and explicitly pursues "using AI to help create more powerful AI." Backed by Alphabet, Radical Ventures, and Khosla Ventures.

### 2.4 AIDE2: First Claimed Level 1 RSI

[Weco AI's AIDE2](https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement) (2026) demonstrated a bi-level optimization: an outer-loop agent (hand-tuned AIDE) optimizing the inner-loop agent's harness code. Over 100 outer-loop iterations in 8 unattended days:

- Discovered 7 successive improved agent versions
- Best agent (AIDE85) beat 2 years of human tuning on held-out benchmarks
- Novel discoveries: multi-armed bandit search policy, 16x context compression, 3-layer reward hacking prevention, even fixing a bug in the evaluation script rather than exploiting it
- Cut reward hacking rate from 63% to 34%
- Did NOT achieve Level 2 (ignition): the improved inner-loop agent did not become a better outer-loop agent

### 2.5 Self-Evolving Coding Agents

A [2026 survey on self-evolving coding agents](https://arxiv.org/html/2608.03392v1) identifies software engineering as a natural domain for agent self-evolution because executable artifacts provide concrete, repeatable feedback signals (unit tests, compiler diagnostics, runtime traces, CI logs). Key systems:

- **Ouroboros** ([arxiv](https://arxiv.org/html/2608.08311)): Self-developing agent harness whose tools, prompts, and core implementation improve through reviewed commits. "Hope" deployment ran 161 days of live self-evolution. Scored 86.97% on Terminal-Bench 2.1, 90.69% on OSWorld-Verified (state of the art)
- **RSEA** ([arxiv](https://arxiv.org/html/2606.28374)): Recursive Self-Evolving Agent carrying 3-layer natural-language state (strategy, skills, playbook). Key insight: strict held-out keep-better gate makes self-evolution monotone-safe - never significantly underperforms base agent
- **MetaSkill-Evolve** ([arxiv](https://arxiv.org/html/2607.05297v1)): Two-timescale framework where task skills evolve on a fast loop and meta-skills (the improvement procedure itself) evolve on a slow loop. Represents bounded one-level recursion. +23.54 points on OfficeQA over no-skill baseline

## 3. Academic Foundations

### 3.1 Taxonomy of Self-Improvement

The [arXiv survey by Phan et al.](https://arxiv.org/html/2607.07663) (2026-07) organizes 1,250 papers along two axes:

- **What the system improves**: behavior in deployment, policy through training, evaluator, or the research process itself
- **Degree of loop closure**: human-in-the-loop to fully closed

The survey introduces a verification hierarchy for self-improvement signals, ordered from strongest to weakest: formal verifiers, unit tests, process reward models, LLM judges, rubrics, meta-evaluation, intrinsic self-assessment. Key finding: demonstrated self-improvement strength tracks this hierarchy. Failure modes (self-confirming loops, model collapse, diversity collapse) follow from violations of the hierarchy. The "research direction-setting" bottleneck that keeps humans in the loop sits at the hierarchy's top.

### 3.2 Information-Theoretic Limits

A [2026 paper on information-theoretic limits](https://arxiv.org/abs/2603.28650v2) formalizes a fundamental tension: can a safety gate permit unbounded beneficial self-modification while maintaining bounded cumulative risk? The answer, for practically relevant risk schedules, is no. Any classifier-based gate under overlapping safe/unsafe distributions forces: either unsafe modifications accumulate, or the system stops improving. Verifier-based approaches (formal proofs, unit tests) can break this impossibility because they provide certainty rather than classification.

### 3.3 PAST-Bench: Benchmarking RSI Foundations

[PAST-Bench](https://arxiv.org/html/2608.04003) (2026-08) tests whether retained experience actually improves agents over time. Across 7 base models and 4 agent frameworks: improvement is real but uneven across capabilities. Agents with the same headline gain can differ markedly in whether that gain is supported by evidence of the intended save-retrieve-update pathway. Notably, the benchmark references OpenClaw and Hermes as agent frameworks that treat persistent workspaces, memories, skills, and tool execution as first-class runtime components - directly relevant to IPPS's approach.

## 4. Safety and Governance

### 4.1 The Governance Gap

The [2026 International AI Safety Report](https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026), authored by 100+ independent experts, identifies loss of control through AI recursive self-improvement as among the most consequential national-security-level risks. Existing governance frameworks (National Institute of Standards and Technology (NIST) AI Risk Management Framework (RMF), ISO/IEC 42001, EU AI Act) operate on annual or multi-year update cycles while AI capability advancement is measured in months.

The [Cloud Security Alliance](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/06/AI_recursive_self_improvement_security_implications_v1.0-csa-styled.pdf) characterizes the structural mismatch: RSI creates new high-value targets for adversaries, new vulnerability propagation channels, new capability uplift mechanisms, and new compounding alignment challenges. Current enterprise security frameworks were developed before RSI-adjacent operations at observed scale.

### 4.2 Institutional Response

The [Institute for Security and Technology](https://securityandtechnology.org/blog/ist-launches-rsi-initative/) launched an $875K RSI governance initiative (2026-08-11) in partnership with the Future of Life Institute. Goal: establish governance frameworks and control mechanisms for RSI-capable systems. Key quote from Hamza Chaudhry (Future of Life Institute): "Recursive self-improvement will compress years of AI development into days, and no one is quite sure what governance or control frameworks would effectively mitigate the risks."

Anthropic's Responsible Scaling Policy v3.0 (2026-02) shifted from binding capability-triggered pause commitments to voluntary transparency mechanisms (public Frontier Safety Roadmap, periodic Risk Reports with third-party review). This governance model change - from binding ex-ante constraints to transparent ex-post accountability - has direct implications for enterprises relying on Anthropic's models.

### 4.3 Anthropic's Three Futures

Anthropic outlines three scenarios based on whether current trends continue:

1. **Trend stalls**: Current capabilities diffuse widely but S-curve bends. Even frozen capabilities produce major changes (Project Glasswing found 10,000+ critical vulnerabilities in weeks). Anthropic considers this unlikely - no measured capability has shown the curve bending yet
2. **Compounding efficiency gains**: AI development substantially automated but humans still set research directions. 100-person companies do work of 10,000-100,000-person organizations. Amdahl's law applies: bottleneck shifts to human code review, idea prioritization. Anthropic says current evidence points here
3. **Full RSI**: AI systems design and refine themselves. Human role reduces to oversight, validation, verification. Alignment problem resolution unclear - misalignment could compound through successor generations. Physical-world bottlenecks (Amdahl's law) still constrain felt pace of change

Anthropic states it would slow down or temporarily pause if other frontier developers did so verifiably, but unilateral pause merely changes who leads rather than creating deliberative process.

## 5. Implications for Agentic Development Systems

### 5.1 RSI Is Already Here in Bounded Form

Every agentic development system that improves its own workflows from experience is performing bounded self-refinement (Level 0 in Weco's taxonomy). IPPS's skill evolution pattern - where execution traces inform skill file updates, and FAILS.md prevents repeated mistakes across sessions - is a manual version of exactly what MetaSkill-Evolve and RSEA automate. The gap between IPPS and RSI-adjacent systems is:

- IPPS: human reviews execution, updates skill files, commits changes
- MetaSkill-Evolve: agent reviews execution, updates skill files, validates against held-out set
- AIDE2: agent reviews execution, updates the agent that updates skill files

### 5.2 The Verification Hierarchy Applies to IPPS

The academic finding that self-improvement strength tracks the verification hierarchy has direct implications. IPPS's strongest improvement signals are:

- `/verify` workflow with concrete rule checks (analogous to formal verifiers)
- `/drift-detect` and `/drift-correct` with GRUC (Guides, Rules, Checks) files (analogous to test suites)
- FAILS.md entries with prevention rules (analogous to regression tests)

The weakest signal is unstructured agent self-assessment ("I think this looks good"). IPPS already prioritizes structured verification over self-assessment, which aligns with the academic evidence.

### 5.3 The Safety Gate Problem

The information-theoretic impossibility result is directly relevant: any classifier-based safety gate (including human review) faces a fundamental tradeoff between permitting improvement and preventing harm. The way out is verifier-based approaches - formal proofs, test suites, structured rule checking. This validates IPPS's investment in concrete GRUC files over vague "be careful" instructions.

### 5.4 The Amdahl's Law Bottleneck

Anthropic's observed bottleneck shift - from code writing to code review, from experiment execution to direction-setting - mirrors what single-programmer agentic systems already experience. As agents produce more output, the human bottleneck shifts to:

1. Reviewing agent output quality
2. Deciding what to work on next
3. Maintaining coherence across growing codebases

IPPS's structured workflows (EDIRD phases, gate checks, TRACTFUL documents) are exactly the mechanisms needed to manage this bottleneck - they make review efficient and direction-setting explicit.

### 5.5 Methodological Limitations

- **Self-reported metrics**: Anthropic's productivity data (80% code, 8x output, 64% judgment superiority) is self-reported with no independent audit. Incentive structure favors optimistic framing. METR's time horizon data is independently measured but covers a narrow task definition
- **Survivorship bias**: Published RSI results (AIDE2, Ouroboros, RSEA) represent successful experiments. Failed attempts at self-improvement are unpublished. The actual success rate of RSI approaches is unknown
- **Definitional ambiguity**: Whether current AI-assisted development constitutes "self-improvement" or "sophisticated tool use" remains debated. The RSI ladder (Weco) provides gradation but Level 1 criteria are contested
- **Snapshot in time**: This document captures August 2026 state. The field moves fast enough that findings may be outdated within months. METR projections extrapolate from 2 years of data

### 5.6 Exclusions

Not covered in this research:

- **OpenAI/Google DeepMind internal RSI metrics** - not publicly disclosed at the same granularity as Anthropic's May 2026 data. Anthropic's disclosure is currently the only first-party quantitative account
- **Pre-2024 theoretical RSI literature** - I.J. Good (1965), Schmidhuber's Gödel Machine (2003), Omohundro (2008) are referenced briefly but not surveyed in depth. Focus is on 2024-2026 empirical evidence
- **Hardware-level RSI** - AI-driven chip design (e.g., Google's Tensor Processing Unit (TPU) layout optimization) excluded; scope limited to software/model-level self-improvement
- **Chinese AI lab RSI activities** - limited English-language primary sources available for comparable analysis
- **Biological/neuroscience-inspired approaches** - evolutionary algorithms and neuroevolution excluded; scope limited to LLM-based self-improvement

## 6. Conclusions

- RSI is transitioning from theoretical concept to observable operational reality. The evidence is strongest for RSI-adjacent operations (AI materially participating in AI development under human supervision) and weakest for full autonomous RSI
- The primary bottleneck preventing full RSI is research taste and direction-setting, not execution capability. This bottleneck may or may not yield to scaling
- Safety frameworks for RSI governance are in early formation. The fundamental information-theoretic tension between permitting improvement and bounding risk suggests that verifier-based approaches (tests, proofs, structured rules) will be more robust than classifier-based approaches (human judgment alone)
- Agentic development systems like IPPS are already performing bounded self-refinement. The gap to automated self-improvement is narrow and closing. The key differentiator will be verification infrastructure quality

## 7. Next Steps

1. Monitor METR time horizon updates for trend acceleration or S-curve bending
2. Evaluate whether IPPS's skill evolution pattern could be partially automated with held-out validation (RSEA-style keep-better gate)
3. Track IST/FLI governance framework development for applicable control mechanisms
4. Assess AIDE2's context engineering findings (16x compression) for applicability to IPPS skill files

## 8. Sources

**Primary Sources:**
- `RECSLFIM-IN01-SC-ANTHR-RSI`: https://www.anthropic.com/institute/recursive-self-improvement - Anthropic's "When AI Builds Itself" disclosure: >80% code authored by Claude, 8x productivity, research judgment improving to 64% superiority on challenging moments [VERIFIED]
- `RECSLFIM-IN01-SC-TCRNCH-DSCVL`: https://techcrunch.com/2026/08/05/jeff-dean-and-other-top-ai-researchers-are-leaving-google-to-launch-their-own-startup/ - Discovery Loop startup: Jeff Dean et al. founding RSI-focused scientific research company [VERIFIED]
- `RECSLFIM-IN01-SC-WECOAI-AIDE2`: https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement - AIDE2: first claimed Level 1 RSI, 8-day autonomous loop beating 2 years of human tuning [VERIFIED]
- `RECSLFIM-IN01-SC-METR-THRZN`: https://metr.org/time-horizons/ - METR time horizon measurements: 50%-reliability task duration doubling ~4 months post-2023 [VERIFIED]
- `RECSLFIM-IN01-SC-METR-TH11`: https://metr.org/blog/2026-1-29-time-horizon-1-1/ - METR TH1.1 update: 228-task suite, accelerating doubling time from 196 to 131 days [VERIFIED]
- `RECSLFIM-IN01-SC-METR-LIMIT`: https://metr.org/notes/2026-01-22-time-horizon-limitations/ - METR limitations clarification: time horizon does not equal automation degree [VERIFIED]
- `RECSLFIM-IN01-SC-ARXIV-SRVY1`: https://arxiv.org/html/2607.07663 - Survey: "Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops" (1,250 papers, verification hierarchy) [VERIFIED]
- `RECSLFIM-IN01-SC-ARXIV-SRVY2`: https://arxiv.org/html/2607.13104 - Survey: "Self-Improvements in Modern Agentic Systems" (system-level framework, update operator formalization) [VERIFIED]
- `RECSLFIM-IN01-SC-ARXIV-MTSKL`: https://arxiv.org/html/2607.05297v1 - MetaSkill-Evolve: two-timescale recursive meta-skill evolution, +23.54 on OfficeQA [VERIFIED]
- `RECSLFIM-IN01-SC-ARXIV-RSEA`: https://arxiv.org/html/2606.28374 - RSEA: held-out keep-better gate makes self-evolution monotone-safe [VERIFIED]
- `RECSLFIM-IN01-SC-ARXIV-OURBR`: https://arxiv.org/html/2608.08311 - Ouroboros: self-developing agent with 161-day live deployment, state-of-art on Terminal-Bench and OSWorld [VERIFIED]
- `RECSLFIM-IN01-SC-ARXIV-PASTB`: https://arxiv.org/html/2608.04003 - PAST-Bench: benchmarking RSI foundations in personal agents [VERIFIED]
- `RECSLFIM-IN01-SC-ARXIV-INFTH`: https://arxiv.org/abs/2603.28650v2 - Information-theoretic limits of safety verification for self-improving systems [VERIFIED]
- `RECSLFIM-IN01-SC-ARXIV-SVCDA`: https://arxiv.org/html/2608.03392v1 - Survey: self-evolving coding agents taxonomy [VERIFIED]
- `RECSLFIM-IN01-SC-CSA-RSISEC`: https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/06/AI_recursive_self_improvement_security_implications_v1.0-csa-styled.pdf - CSA: RSI security implications, threat landscape mapping [VERIFIED]
- `RECSLFIM-IN01-SC-CSA-GOVGAP`: https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/06/CSA_research_note_RSI_governance_compliance_gap_20260610-csa-styled.pdf - CSA: RSI governance-compliance gap, RSP v3.0 analysis [VERIFIED]
- `RECSLFIM-IN01-SC-IST-RSIINIT`: https://securityandtechnology.org/blog/ist-launches-rsi-initative/ - IST/FLI: $875K RSI governance initiative launched 2026-08-11 [VERIFIED]
- `RECSLFIM-IN01-SC-INTL-SAFTY`: https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026 - 2026 International AI Safety Report: RSI as national-security-level risk [VERIFIED]
- `RECSLFIM-IN01-SC-METR-PAPER`: https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/ - Original METR time horizon paper: 7-month doubling time over 6 years [VERIFIED]

## Document History

**[2026-08-13 15:20]**
- Added: Section 5.5 Methodological Limitations (/improve Phase 3)
- Changed: Exclusions renumbered to 5.6

**[2026-08-13 15:15]**
- Fixed: NIST, RMF, TPU acronym expansions (AP-PR-06)
- Fixed: "Goedel" to "Gödel" (core-conventions encoding)

**[2026-08-13 15:10]**
- Added: Section 5.5 Exclusions (drift correction)
- Fixed: METR and GRUC acronym expansions (AP-PR-06)

**[2026-08-13 14:55]**
- Initial research document created
