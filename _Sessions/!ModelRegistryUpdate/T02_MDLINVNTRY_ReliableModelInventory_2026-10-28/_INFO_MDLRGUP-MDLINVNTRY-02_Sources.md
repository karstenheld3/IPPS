# INFO: Sources for Reliable Model Inventory Research

**Doc ID**: MDLRGUP-MDLINVNTRY-IN02
**Goal**: Register every local file and known web source relevant to the model inventory audit, with status and extraction notes
**Timeline**: Created 2026-10-28, Updated 3 times (2026-10-28 - 2026-10-28)
**Version scope**: 2026-10-28
**Preflight accuracy**: 7/7 verified (3 CORRECT, 4 PARTIAL, 0 WRONG)

## Table of Contents

- [Local Sources](#local-sources)
- [Provider Documentation](#provider-documentation)
- [Capability Evidence](#capability-evidence)
- [Agent Environments](#agent-environments)
- [Document History](#document-history)

## Local Sources

### Files Under Review

- **MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV** - `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md` (Accessed: 2026-10-28)
  - Content: Model capability labels, Workload Factor (WF) formula, effort multipliers, price assumptions, profile thresholds, 28-model table
  - Role: Primary audit target (P1-S3)

- **MDLRGUP-MDLINVNTRY-SC-IPPS-TSKGD** - `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\TASKS_GUIDES.md` (Accessed: 2026-10-28)
  - Content: Default label, Human Work Hours (HWH) buckets, Agent Work Hours (AWH) formula, WF/max_items/max_files, Time Log reference
  - Role: Audit target, partitioning rules (P1-S3)

- **MDLRGUP-MDLINVNTRY-SC-IPPS-PRMGD** - `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\PROMPTS_GUIDES.md` (Accessed: 2026-10-28)
  - Content: Sections 1c (effort), 1f (load), 1g (model), 3a (checkpoints), 5 (density) - partitioning formulas and rules
  - Role: Audit target, overlapping partitioning sections (P1-S3)

- **MDLRGUP-MDLINVNTRY-SC-IPPS-PRMRL** - `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\PROMPTS_RULES.md` (PRMT-SC-05) (Accessed: 2026-10-28)
  - Content: Verification rule checking prompts files against MODEL_INVENTORY.md numbers
  - Role: Audit target, depends on inventory values (P1-S3)

- **MDLRGUP-MDLINVNTRY-SC-IPPS-MREG** - `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-registry.json` (Accessed: 2026-10-28)
  - Content: 28 model entries with capability_label, behavior_profile, context_window, max_output, effort_levels (69 total models)
  - Role: Canonical registry; sourced fields (context_window, max_output) vs assumed fields (capability_label, behavior_profile)

- **MDLRGUP-MDLINVNTRY-SC-IPPS-MPRC** - `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-pricing.json` (Accessed: 2026-10-28)
  - Content: Per-model pricing (input, cached_input, output per 1M tokens)
  - Role: Sourced from provider Document Object Model (DOM) extraction (update-model-registry.md Phase 2)

- **MDLRGUP-MDLINVNTRY-SC-IPPS-MPRMP** - `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-parameter-mapping.json` (Accessed: 2026-10-28)
  - Content: Effort level names, thinking factors (anthropic_thinking_factor), reasoning effort mappings
  - Role: Canonical source #3 in MODEL_INVENTORY.md L15; sourced evidence for thinking models Max=XHigh (audit L57)

- **MDLRGUP-MDLINVNTRY-SC-IPPS-WMREG** - `e:\dev\IPPS\PromptSystemV4.5\skills\devin-auto-model-switcher\windsurf-model-registry.json` (Accessed: 2026-10-28)
  - Content: Devin/Cascade model display names, tier mappings, model IDs (22/28 coverage of Section 3.1 models)
  - Role: Environment-specific registry (Goal 2: general-purpose inventory must not depend on this)

- **MDLRGUP-MDLINVNTRY-SC-IPPS-UMREG** - `e:\dev\IPPS\update-model-registry.md` (Accessed: 2026-10-28)
  - Content: DOM extraction procedure, Sources section (A1-A4, O1-O3, Z1-Z3), verification gates, distribution targets
  - Role: Procedure of record for sourcing provider data; source of provider URLs

- **MDLRGUP-MDLINVNTRY-SC-IPPS-FAILS** - `e:\dev\IPPS\FAILS.md` and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md` (Accessed: 2026-10-28)
  - Content: Workspace failure log and sequence findings card with Partition Observations ledger
  - Role: Empirical observation source for R4 downgrades and behavior evidence (1/28 coverage: `glm-5.2`)

### Prior Research

- **MDLRGUP-MDLINVNTRY-SC-LOCAL-LLMCAP** - `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md` [LLMCAPCLS-IN01] (Accessed: 2026-10-28)
  - Content: YY-L label design, WF formula derivation, behavior profile definition, ledger concept
  - Role: Documents the assumptions this audit reviews; Section 6 states labels were chosen to reproduce the previous table (circular)

- **MDLRGUP-MDLINVNTRY-SC-KWRK-ANTIER** - `e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\NOTES.md` "Model and Hardware Tiers" section (Accessed: 2026-10-28)
  - Content: 4-field model tier record (vendor generation, Universal Class (UC) UC-1..5, Epoch Capabilities Index (ECI) band, generation equivalent), design rule, Reference List, rejected sources, Hardware Tier (HT) HT-1..4
  - Role: Existing tier design that may replace YY-L (DD-01 candidate option a)

- **MDLRGUP-MDLINVNTRY-SC-KWRK-MODTIR** - `e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_INFO_AINWSRCH-MODELTIER-01_GenerationTiering.md` [AINWSRCH-MODELTIER-IN01] (Accessed: 2026-10-28)
  - Content: Full rationale - problem statement, vendor class analysis, Fable vs Opus case, capability scale evaluation, recommended 4-field scheme, worked examples, limitations, 24 primary + 5 secondary sources
  - Role: Evidence base for the existing tier design; rejected alternatives documented with reasons

- **MDLRGUP-MDLINVNTRY-SC-LOCAL-COVMTX** - `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19\_INFO_MDLBHVPRM-05_CoverageMatrix.md` [MDLRGUP-MDLBHVPRM-IN05] (Accessed: 2026-10-28)
  - Content: Benchmark coverage matrix across 75 evaluation registry models and ~40 Devin base models (IFEval, WildBench, OverAct Scope Inflation Rate (SIR), OverEager, YapBench)
  - Role: Source for Behavior evidence coverage (IFEval-Hard 0/28, OverAct SIR 1/28)

- **MDLRGUP-MDLINVNTRY-SC-LOCAL-PARTTN** - `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19\_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md` [MDLRGUP-MDLBHVPRM-IN06] (Accessed: 2026-10-28)
  - Content: How /write-prompts uses model inventory data (capacity, instruction following, eagerness) to size prompts per model
  - Role: Consumer of inventory data; defines what fields the partitioning system needs

- **MDLRGUP-MDLINVNTRY-SC-LOCAL-FDBKLP** - `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19\_INFO_MDLBHVPRM-07_PromptFeedbackLoop.md` [MDLRGUP-MDLBHVPRM-IN07] (Accessed: 2026-10-28)
  - Content: Drift-detection checkpoint design, per-prompt planned-vs-actual observations, _agent_work/ folder definition
  - Role: Defines the feedback loop that calibrates WF; checkpoint ledger concept

- **MDLRGUP-MDLINVNTRY-SC-KWRK-TMPLTE** - `e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_PROMPTS_AI-News-Research_TEMPLATE.md` (Accessed: 2026-10-28)
  - Content: Context management section shows GLM-5.2 high running prompts of ~90k tokens (P02), session A ~165k across 4 prompts, 10-prompt pipeline completing without skipped items
  - Role: Empirical evidence of GLM-5.2 prompt sizes in production use (feeds assumption #5 verification)

## Provider Documentation

Status: checked (Accessed: 2026-10-28 via HTTP resolution batch; 5 checked, 4 redirected among A1-A4/O1-O3/Z1-Z2, plus Z3 redirected, 0 dead)

- **MDLRGUP-MDLINVNTRY-SC-ANTH-PRC** - `https://docs.anthropic.com/en/docs/about-claude/pricing` (A1) (Accessed: 2026-10-28)
  - Content: Anthropic model pricing table
  - Status: redirected to [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) (HTTP 200)

- **MDLRGUP-MDLINVNTRY-SC-ANTH-MDLS** - `https://docs.anthropic.com/en/docs/about-claude/models` (A2) (Accessed: 2026-10-28)
  - Content: Anthropic model API IDs, context windows, max output
  - Status: redirected to [platform.claude.com/docs/en/models/overview](https://platform.claude.com/docs/en/models/overview) (HTTP 200)

- **MDLRGUP-MDLINVNTRY-SC-ANTH-MDLOV** - `https://platform.claude.com/docs/en/about-claude/models/overview` (A3) (Accessed: 2026-10-28)
  - Content: Anthropic models overview
  - Status: redirected to [platform.claude.com/docs/en/models/overview](https://platform.claude.com/docs/en/models/overview) (HTTP 200)

- **MDLRGUP-MDLINVNTRY-SC-ANTH-DEPR** - `https://platform.claude.com/docs/en/about-claude/model-deprecations` (A4) (Accessed: 2026-10-28)
  - Content: Anthropic model deprecation schedule
  - Status: checked (HTTP 200)

- **MDLRGUP-MDLINVNTRY-SC-OAI-STDPRC** - `https://developers.openai.com/api/docs/pricing?latest-pricing=standard` (O1) (Accessed: 2026-10-28)
  - Content: OpenAI standard pricing table
  - Status: checked (HTTP 200)

- **MDLRGUP-MDLINVNTRY-SC-OAI-BCHPRC** - `https://developers.openai.com/api/docs/pricing?latest-pricing=batch` (O2) (Accessed: 2026-10-28)
  - Content: OpenAI batch pricing table
  - Status: checked (HTTP 200)

- **MDLRGUP-MDLINVNTRY-SC-OAI-CMPRE** - `https://platform.openai.com/docs/models/compare` (O3) (Accessed: 2026-10-28)
  - Content: OpenAI model comparison (context windows, max output, effort levels)
  - Status: redirected to [developers.openai.com/api/docs/models/compare](https://developers.openai.com/api/docs/models/compare) (HTTP 200)

- **MDLRGUP-MDLINVNTRY-SC-ZAI-PRC** - `https://docs.z.ai/guides/overview/pricing` (Z1) (Accessed: 2026-10-28)
  - Content: Z.AI pricing table
  - Status: checked (HTTP 200)

- **MDLRGUP-MDLINVNTRY-SC-ZAI-MDLS** - `https://docs.z.ai/guides/overview/overview` (Z2) (Accessed: 2026-10-28)
  - Content: Z.AI model overview
  - Status: checked (HTTP 200)

- **MDLRGUP-MDLINVNTRY-SC-ZAI-APIREF** - `https://docs.z.ai/api-reference` (Z3) (Accessed: 2026-10-28)
  - Content: Z.AI API reference
  - Status: redirected to [docs.z.ai/api-reference/introduction](https://docs.z.ai/api-reference/introduction) (HTTP 200)

## Capability Evidence

Status: checked (Accessed: 2026-10-28)

- **MDLRGUP-MDLINVNTRY-SC-EPOCH-ECI** - `https://epoch.ai/eci` (Accessed: 2026-10-28)
  - Content: Per-model ECI scores, Confidence Intervals (CI), benchmark count. CSV download: `https://epoch.ai/data/eci_scores.csv` and leaderboard button `eci-leaderboard-general.csv` (270 data rows, 6 columns)
  - Status: checked (28/28 Section 3.1 models matched in `_SOURCES/2026-10-28_Epoch-ECI-Match.json`)
  - Extraction: CSV download, no DOM extraction needed

- **MDLRGUP-MDLINVNTRY-SC-METR-TMHOR** - `https://metr.org/time-horizons/` (Accessed: 2026-10-28)
  - Content: Model Evaluation and Threat Research (METR) per-model 50% and 80% task completion horizons (backed by `https://metr.org/assets/benchmark_results_1_1.yaml`, 26 models, raw values in minutes of human expert completion time)
  - Status: checked (via Playwright; 6/28 exact, 7/28 with family prefix in `_SOURCES/2026-10-28_METR-TimeHorizons-DOM.json`; page banner states no longer actively updated since 2026-09-08)

- **MDLRGUP-MDLINVNTRY-SC-GOOG-GMPRC** - `https://ai.google.dev/gemini-api/docs/pricing` (Accessed: 2026-10-28)
  - Content: Google Gemini API pricing tables (88 HTML tables across per-model H2 sections with Standard/Batch/Flex/Priority/Contributor tabs; last updated 2026-10-27 UTC)
  - Status: checked (via Playwright; saved to `_SOURCES/2026-10-28_Google-Pricing-DOM.json`)

- **MDLRGUP-MDLINVNTRY-SC-GOOG-GMMDL** - `https://ai.google.dev/gemini-api/docs/models` (Accessed: 2026-10-28)
  - Content: Google Gemini API model index (11 HTML tables with Model/Description/Endpoint) and per-model detail subpages (`/gemini-api/docs/models/<slug>`, Token limits + Capabilities)
  - Status: checked (via Playwright; saved to `_SOURCES/2026-10-28_Google-Models-DOM.json`)

- **MDLRGUP-MDLINVNTRY-SC-GOOG-GMTHK** - `https://ai.google.dev/gemini-api/docs/thinking` (Accessed: 2026-10-28)
  - Content: Google Gemini API thinking configuration and per-model supported thinking effort levels table (`Model`, `Default Thinking`, `Levels Supported`)
  - Status: checked (via Playwright; included in `_SOURCES/2026-10-28_Google-Models-DOM.json`)

## Agent Environments

Inventoried from local `windsurf-model-registry.json` (`MDLRGUP-MDLINVNTRY-SC-IPPS-WMREG`, Accessed: 2026-10-28, 22/28 coverage of Section 3.1 models). Claude Code, OpenAI Codex CLI, and Cursor are not inventoried.

## Document History

**[2026-10-28 20:32]**
- Fixed: Added `Timeline` header field, explicit `(Accessed: 2026-10-28)` dates on all 32 source entries (`SC-03`), first-use acronym expansions (`MW-WC-09`), clickable redirect links (`QA-12`), and dedicated source entries `MDLRGUP-MDLINVNTRY-SC-IPPS-FAILS` and `MDLRGUP-MDLINVNTRY-SC-GOOG-GMTHK` (`SC-02`)

**[2026-10-28 20:21]**
- Changed: Updated `Preflight accuracy` to `7/7 verified (3 CORRECT, 4 PARTIAL, 0 WRONG)`
- Changed: Updated Provider Documentation (A1-A4, O1-O3, Z1-Z3) and Capability Evidence (Epoch, METR, Google Pricing, Google Models) from pending to `checked` / `redirected to [URL]` with access date `2026-10-28`
- Added: `MDLRGUP-MDLINVNTRY-SC-LOCAL-COVMTX` (`_INFO_MDLBHVPRM-05_CoverageMatrix.md`) under Prior Research

**[2026-10-28 19:13]**
- Added: `MDLRGUP-MDLINVNTRY-SC-IPPS-MPRMP` (model-parameter-mapping.json) - was canonical source #3 in MODEL_INVENTORY.md but missing from this file (verify checkpoint F4)

**[2026-10-28 19:12]**
- Initial creation with 14 local sources, 10 provider documentation entries, 4 capability evidence entries
- Web entries initially deferred to P1-S4..S7
