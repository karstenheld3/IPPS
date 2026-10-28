# INFO: Sources for Reliable Model Inventory Research

**Doc ID**: MDLRGUP-MDLINVNTRY-IN02
**Goal**: Register every local file and known web source relevant to the model inventory audit, with status and extraction notes
**Version scope**: 2026-10-28
**Preflight accuracy**: pending

## Table of Contents

- [Local Sources](#local-sources)
- [Provider Documentation](#provider-documentation)
- [Capability Evidence](#capability-evidence)
- [Agent Environments](#agent-environments)

## Local Sources

### Files Under Review

- **MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV** - `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md`
  - Content: Model capability labels, WF formula, effort multipliers, price assumptions, profile thresholds, 28-model table
  - Role: Primary audit target (P1-S3)

- **MDLRGUP-MDLINVNTRY-SC-IPPS-TSKGD** - `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\TASKS_GUIDES.md`
  - Content: Default label, HWH buckets, AWH formula, WF/max_items/max_files, Time Log reference
  - Role: Audit target, partitioning rules (P1-S3)

- **MDLRGUP-MDLINVNTRY-SC-IPPS-PRMGD** - `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\PROMPTS_GUIDES.md`
  - Content: Sections 1c (effort), 1f (load), 1g (model), 3a (checkpoints), 5 (density) - partitioning formulas and rules
  - Role: Audit target, overlapping partitioning sections (P1-S3)

- **MDLRGUP-MDLINVNTRY-SC-IPPS-PRMRL** - `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\PROMPTS_RULES.md` (PRMT-SC-05)
  - Content: Verification rule checking prompts files against MODEL_INVENTORY.md numbers
  - Role: Audit target, depends on inventory values (P1-S3)

- **MDLRGUP-MDLINVNTRY-SC-IPPS-MREG** - `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-registry.json`
  - Content: 28 model entries with capability_label, behavior_profile, context_window, max_output, effort_levels
  - Role: Canonical registry; sourced fields (context_window, max_output) vs assumed fields (capability_label, behavior_profile)

- **MDLRGUP-MDLINVNTRY-SC-IPPS-MPRC** - `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-pricing.json`
  - Content: Per-model pricing (input, cached_input, output per 1M tokens)
  - Role: Sourced from provider DOM extraction (update-model-registry.md Phase 2)

- **MDLRGUP-MDLINVNTRY-SC-IPPS-MPRMP** - `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-parameter-mapping.json`
  - Content: Effort level names, thinking factors (anthropic_thinking_factor), reasoning effort mappings
  - Role: Canonical source #3 in MODEL_INVENTORY.md L15; sourced evidence for thinking models Max=XHigh (audit L57)

- **MDLRGUP-MDLINVNTRY-SC-IPPS-WMREG** - `e:\dev\IPPS\PromptSystemV4.5\skills\devin-auto-model-switcher\windsurf-model-registry.json`
  - Content: Devin/Cascade model display names, tier mappings, model IDs
  - Role: Environment-specific registry (Goal 2: general-purpose inventory must not depend on this)

- **MDLRGUP-MDLINVNTRY-SC-IPPS-UMREG** - `e:\dev\IPPS\update-model-registry.md`
  - Content: DOM extraction procedure, Sources section (A1-A4, O1-O3, Z1-Z3), verification gates, distribution targets
  - Role: Procedure of record for sourcing provider data; source of provider URLs

### Prior Research

- **MDLRGUP-MDLINVNTRY-SC-LOCAL-LLMCAP** - `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md` [LLMCAPCLS-IN01]
  - Content: YY-L label design, WF formula derivation, behavior profile definition, ledger concept
  - Role: Documents the assumptions this audit reviews; Section 6 states labels were chosen to reproduce the previous table (circular)

- **MDLRGUP-MDLINVNTRY-SC-KWRK-ANTIER** - `e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\NOTES.md` "Model and Hardware Tiers" section
  - Content: 4-field model tier record (vendor generation, UC-1..5, ECI band, generation equivalent), design rule, Reference List, rejected sources, HT-1..4
  - Role: Existing tier design that may replace YY-L (DD-01 candidate option a)

- **MDLRGUP-MDLINVNTRY-SC-KWRK-MODTIR** - `e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_INFO_AINWSRCH-MODELTIER-01_GenerationTiering.md` [AINWSRCH-MODELTIER-IN01]
  - Content: Full rationale - problem statement, vendor class analysis, Fable vs Opus case, capability scale evaluation, recommended 4-field scheme, worked examples, limitations, 24 primary + 5 secondary sources
  - Role: Evidence base for the existing tier design; rejected alternatives documented with reasons

- **MDLRGUP-MDLINVNTRY-SC-LOCAL-PARTTN** - `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19\_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md` [MDLRGUP-MDLBHVPRM-IN06]
  - Content: How /write-prompts uses model inventory data (capacity, instruction following, eagerness) to size prompts per model
  - Role: Consumer of inventory data; defines what fields the partitioning system needs

- **MDLRGUP-MDLINVNTRY-SC-LOCAL-FDBKLP** - `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19\_INFO_MDLBHVPRM-07_PromptFeedbackLoop.md` [MDLRGUP-MDLBHVPRM-IN07]
  - Content: Drift-detection checkpoint design, per-prompt planned-vs-actual observations, _agent_work/ folder definition
  - Role: Defines the feedback loop that calibrates WF; checkpoint ledger concept

- **MDLRGUP-MDLINVNTRY-SC-KWRK-TMPLTE** - `e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_PROMPTS_AI-News-Research_TEMPLATE.md`
  - Content: Context management section shows GLM-5.2 high running prompts of ~90k tokens (P02), session A ~165k across 4 prompts, 10-prompt pipeline completing without skipped items
  - Role: Empirical evidence of GLM-5.2 prompt sizes in production use (feeds assumption #5 verification)

## Provider Documentation

Status: unchecked (web navigation deferred to P1-S7)

- **MDLRGUP-MDLINVNTRY-SC-ANTH-PRC** - `https://docs.anthropic.com/en/docs/about-claude/pricing` (A1)
  - Content: Anthropic model pricing table
  - Status: unchecked

- **MDLRGUP-MDLINVNTRY-SC-ANTH-MDLS** - `https://docs.anthropic.com/en/docs/about-claude/models` (A2)
  - Content: Anthropic model API IDs, context windows, max output
  - Status: unchecked

- **MDLRGUP-MDLINVNTRY-SC-ANTH-MDLOV** - `https://platform.claude.com/docs/en/about-claude/models/overview` (A3)
  - Content: Anthropic models overview
  - Status: unchecked

- **MDLRGUP-MDLINVNTRY-SC-ANTH-DEPR** - `https://platform.claude.com/docs/en/about-claude/model-deprecations` (A4)
  - Content: Anthropic model deprecation schedule
  - Status: unchecked

- **MDLRGUP-MDLINVNTRY-SC-OAI-STDPRC** - `https://developers.openai.com/api/docs/pricing?latest-pricing=standard` (O1)
  - Content: OpenAI standard pricing table
  - Status: unchecked

- **MDLRGUP-MDLINVNTRY-SC-OAI-BCHPRC** - `https://developers.openai.com/api/docs/pricing?latest-pricing=batch` (O2)
  - Content: OpenAI batch pricing table
  - Status: unchecked

- **MDLRGUP-MDLINVNTRY-SC-OAI-CMPRE** - `https://platform.openai.com/docs/models/compare` (O3)
  - Content: OpenAI model comparison (context windows, max output, effort levels)
  - Status: unchecked

- **MDLRGUP-MDLINVNTRY-SC-ZAI-PRC** - `https://docs.z.ai/guides/overview/pricing` (Z1)
  - Content: Z.AI pricing table
  - Status: unchecked

- **MDLRGUP-MDLINVNTRY-SC-ZAI-MDLS** - `https://docs.z.ai/guides/overview/overview` (Z2)
  - Content: Z.AI model overview
  - Status: unchecked

- **MDLRGUP-MDLINVNTRY-SC-ZAI-APIREF** - `https://docs.z.ai/api-reference` (Z3)
  - Content: Z.AI API reference
  - Status: unchecked

## Capability Evidence

Status: unchecked (web navigation deferred to P1-S4..S6)

- **MDLRGUP-MDLINVNTRY-SC-EPOCH-ECI** - `https://epoch.ai/eci`
  - Content: Per-model ECI scores, confidence intervals, benchmark count. CSV download: `https://epoch.ai/data/eci_scores.csv` and leaderboard button `eci-leaderboard-general.csv` (271 models, 6 columns)
  - Status: unchecked (CSV shape confirmed in prompt [02/06])
  - Extraction: CSV download, no DOM extraction needed

- **MDLRGUP-MDLINVNTRY-SC-METR-TMHOR** - `https://metr.org/time-horizons/`
  - Content: Per-model 50% and 80% task completion horizons
  - Status: unchecked

- **MDLRGUP-MDLINVNTRY-SC-GOOG-GMPRC** - `https://ai.google.dev/gemini-api/docs/pricing`
  - Content: Google Gemini API pricing table
  - Status: unchecked

- **MDLRGUP-MDLINVNTRY-SC-GOOG-GMMDL** - `https://ai.google.dev/gemini-api/docs/models`
  - Content: Google Gemini API model list, context windows, capabilities
  - Status: unchecked

## Agent Environments

Sources for which model IDs and effort levels each agent environment exposes. Deferred to P1-S7 or later.

(none registered yet - web research needed)

## Document History

**[2026-10-28 19:13]**
- Added: `MDLRGUP-MDLINVNTRY-SC-IPPS-MPRMP` (model-parameter-mapping.json) - was canonical source #3 in MODEL_INVENTORY.md but missing from this file (verify checkpoint F4)

**[2026-10-28 19:12]**
- Initial creation with 14 local sources, 10 provider documentation entries, 4 capability evidence entries
- All web entries status "unchecked"
