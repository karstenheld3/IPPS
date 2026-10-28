<PromptSystem MarkdownTablesAllowed=true />

# INFO: Inventory Audit - Value and Rule Classification

**Doc ID**: MDLRGUP-MDLINVNTRY-IN03
**Goal**: Classify every value and rule in the four audited scopes as SOURCED, DERIVED, or ASSUMED
**Timeline**: Created 2026-10-28, Updated 2 times (2026-10-28 - 2026-10-28)
**Version scope**: 2026-10-28

**Depends on:**
- `_INFO_MDLRGUP-MDLINVNTRY-02_Sources.md [MDLRGUP-MDLINVNTRY-IN02]` for source IDs and evidence links

## Summary

- **ASSUMED share**: `MODEL_INVENTORY.md` 59% (`26/44`), `TASKS_GUIDES.md` 40% (`4/10`), `PROMPTS_GUIDES.md` 29% (`6/21`), `PROMPTS_RULES.md` 14% (`1/7`). The inventory file carries the highest assumption density because it defines all base values `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV | e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md)`
- **Most load-bearing assumption**: the Workload Factor (WF) formula (`MODEL_INVENTORY.md` L33). Every WF column value, prompt count calculation, checkpoint interval, and `PRMT-SC-05` sizing check derives from it. Removing it collapses the entire partitioning system `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV | e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md)`
- **If ASSUMED rows removed**: Model IDs, Context windows, effort support flags, Devin cost multipliers, provider prices, and observed Agent Work Hours (AWH) survive as `SOURCED`. All partitioning formulas, sizing rules, profile parameters, label assignments, and verification numeric checks lose their basis `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-MREG | e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-registry.json)`
- **DERIVED propagates assumptions**: most `DERIVED` rows compute from the WF formula or profile parameters, both `ASSUMED`. `DERIVED` class overstates confidence; `20 of 27` `DERIVED` rows depend on at least one `ASSUMED` input `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-PRMGD | e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\PROMPTS_GUIDES.md)`
- **Volume**: `4,717` words (`315` lines) across four scopes; `MODEL_INVENTORY.md` Section 2 (`37` lines, L28-64) contains `60%` of all `ASSUMED` items `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV | e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md)`

## Table of Contents

- [Summary](#summary)
- [MODEL_INVENTORY.md](#model_inventorymd)
- [TASKS_GUIDES.md](#tasks_guidesmd)
- [PROMPTS_GUIDES.md Sections 1c, 1f, 1g, 3a, 5](#prompts_guidesmd-sections-1c-1f-1g-3a-5)
- [PROMPTS_RULES.md PRMT-SC-05](#prompts_rulesmd-prmt-sc-05)
- [Counts](#counts)
- [Goal Violations](#goal-violations)
- [Limitations and Known Issues](#limitations-and-known-issues)
- [Sources](#sources)
- [Document History](#document-history)

## MODEL_INVENTORY.md

| Lines   | Item                                          | Class   | Evidence or reason                                                    |
|---------|-----------------------------------------------|---------|-----------------------------------------------------------------------|
| L20     | HWH = human expert hours, model-independent   | SOURCED | Standard industry concept; no model-specific values                   |
| L21     | WF = HWH one prompt completes per run         | ASSUMED | Invented metric; no external definition or benchmark                  |
| L22     | Capability label YY-L scheme                  | ASSUMED | Invented; LLMCAPCLS-IN01 Section 6: fitted to reproduce prior table  |
| L23     | Behavior profile: precise/standard/guarded    | ASSUMED | Categories and thresholds invented                                    |
| L24     | Price per WF 1 definition                     | DERIVED | From model-pricing.json prices + 80/20 token assumption               |
| L25     | Context = max input tokens in K               | SOURCED | model-registry.json context_window from provider docs                 |
| L26     | `-` = effort level not supported              | SOURCED | model-registry.json effort_levels from provider docs                  |
| L30     | "No benchmark measures HWH per prompt"        | ASSUMED | Claim without citation                                                |
| L30     | "Within a factor of 2" precision bound        | ASSUMED | No evidence for this bound                                            |
| L33     | WF formula: 2.0 * 0.5^letter * 2^(YY-26)     | ASSUMED | No source; LLMCAPCLS-IN01 S6: fitted to prior table                  |
| L34     | WF value table (25-A 1.0, 26-A 2.0, ...)     | DERIVED | Computed from WF formula                                              |
| L35     | One letter step = one year of progress        | ASSUMED | Design assertion without empirical evidence                           |
| L38     | R1: YY = year of general availability         | SOURCED | Provider GA announcements                                             |
| L39     | R2: Letter by estimated capability            | ASSUMED | Judgment heuristic; no objective criterion                            |
| L40     | R3: October rule, highest B before Oct 1      | ASSUMED | Process rule without evidence; requires manual yearly review          |
| L41     | R4: Observation downgrade by one letter       | SOURCED | FAILS.md and findings card documented observations                    |
| L42     | R5: Hard limit cap at 32K max output          | SOURCED | Provider models page max_output documentation                         |
| L45     | Profile thresholds IF>=0.90, EG<=1.20 etc.    | ASSUMED | No source; unmeasured (LLMCAPCLS-IN01 L416)                          |
| L46     | Evidence priority: ledger > obs > bench > none | ASSUMED | Ranking without external source                                       |
| L47     | Change rule: 3 sequences, one step at a time  | ASSUMED | Arbitrary threshold                                                   |
| L50     | precise: items 8, files 6, checkpoint 3       | ASSUMED | Unmeasured (LLMCAPCLS-IN01 L416)                                     |
| L51     | standard: items 6, files 3, checkpoint 2      | ASSUMED | Unmeasured (LLMCAPCLS-IN01 L416)                                     |
| L52     | guarded: items 4, files 2, checkpoint 1       | ASSUMED | Unmeasured (LLMCAPCLS-IN01 L416)                                     |
| L56     | Effort multipliers: Low 0.25 to Max 2.0       | ASSUMED | No source for ratios                                                  |
| L57     | Thinking models: Max = XHigh                  | SOURCED | model-parameter-mapping.json anthropic_thinking_factor 1.0            |
| L58     | No-reasoning models: Medium only              | SOURCED | model-registry.json effort_levels                                     |
| L61     | 1 HWH = 1M tokens assumption                 | ASSUMED | No measurement                                                        |
| L61     | 80% input, 20% output token split            | ASSUMED | No measurement                                                        |
| L62     | API price = 0.8*input + 0.2*output per 1M    | DERIVED | From model-pricing.json + 80/20 assumption                           |
| L63     | Devin price = multiplier * 2.50 * 0.36       | DERIVED | From windsurf-model-registry.json + 1/5 assumption                   |
| L63     | Devin input price = 1/5 of output             | ASSUMED | Devin-specific; no evidence                                           |
| L68     | Prefix inheritance for unlisted variants      | ASSUMED | Convention without external source                                     |
| L72-101 | Column: Model (model ID)                      | SOURCED | model-registry.json model IDs                                         |
| L72-101 | Column: Label (YY-L)                          | ASSUMED | Assigned by judgment per R1-R5                                         |
| L72-101 | Column: Profile (27 of 28 = standard)         | ASSUMED | Thresholds unmeasured; 27 identical values carry no information        |
| L72-101 | Column: Context (max input K)                 | SOURCED | model-registry.json context_window                                     |
| L72-101 | Column: WF per effort (Low..Max)              | DERIVED | WF formula + effort multipliers                                        |
| L72-101 | Column: USD per WF 1                          | DERIVED | API price formula from L62                                             |
| L72-101 | Column: Devin cost (multiplier)               | SOURCED | windsurf-model-registry.json cost_multiplier                           |
| L72-101 | Column: Notes                                 | ASSUMED | Mix of SOURCED facts and judgment; no uniform source                   |
| L107-117 | Section 3.2: 9 Devin-only model rows         | ASSUMED | Label, profile, WF from judgment; no API registry entry                |
| L119    | Default unlisted: YY-C, standard              | ASSUMED | Fallback convention without evidence                                   |
| L123    | Section 4: label/profile must equal registry  | DERIVED | Cross-reference model-registry.json                                    |
| L126-127 | Calibration: R4 + profile move on observation | ASSUMED | Process design; calibration procedure not yet exercised                 |

## TASKS_GUIDES.md

| Lines   | Item                                          | Class   | Evidence or reason                                                    |
|---------|-----------------------------------------------|---------|-----------------------------------------------------------------------|
| L13     | Default label YY-C for unknown model          | ASSUMED | Depends on YY-L scheme (MODEL_INVENTORY.md)                           |
| L19-24  | HWH size buckets: 0.25, 0.5, 1, 2, 4         | ASSUMED | Keep (STRUT Known Knowns); no empirical calibration                    |
| L25     | `Est: [N] HWH` format per task                | DERIVED | Format convention from TASKS_TEMPLATE.md                               |
| L26     | Estimated total = sum of Est values           | DERIVED | Arithmetic sum of per-task estimates                                   |
| L37     | Est <= WF sizing check                        | DERIVED | From MODEL_INVENTORY.md WF values                                      |
| L37     | items <= max_items, files <= max_files         | DERIVED | From MODEL_INVENTORY.md profile parameters                             |
| L39     | 2 HWH single-prompt ceiling                   | ASSUMED | Arbitrary safety margin; no measurement                                |
| L45     | AWH = 0.2 * HWH initial estimate              | ASSUMED | Anthropic human-in-the-loop data transferred to unattended runs        |
| L46     | AWH from prompt_count * observed minutes      | SOURCED | STRUT Time Log observations (empirical)                                |
| L56-60  | Review checklist verifies sizing              | DERIVED | Verification references MODEL_INVENTORY.md values                      |

## PROMPTS_GUIDES.md Sections 1c, 1f, 1g, 3a, 5

| Lines   | Item                                          | Class   | Evidence or reason                                                    |
|---------|-----------------------------------------------|---------|-----------------------------------------------------------------------|
| L41-46  | Effort = trained behavioral profile           | SOURCED | Documented provider behavior (RL training)                             |
| L48-49  | Scope depends on model + effort + context     | DERIVED | From MODEL_INVENTORY.md WF and context                                 |
| L50     | Frontmatter effort/context keys               | DERIVED | References MODEL_INVENTORY.md data                                     |
| L77     | Run budget: context, compute, output per model | SOURCED | Provider documentation (context window, output limits)                 |
| L88     | HWH per prompt must not exceed WF             | DERIVED | From MODEL_INVENTORY.md WF values                                      |
| L89     | Load assessment: input, output, depth axes    | ASSUMED | Heuristic; no measured thresholds for light vs heavy                   |
| L116    | Resolve model by longest prefix               | SOURCED | model-registry.json model_id_startswith matching rule                  |
| L117    | context_window_size from Context column       | SOURCED | model-registry.json context_window                                     |
| L118    | Effort supported = column not `-`             | SOURCED | model-registry.json effort_levels                                      |
| L119    | Task HWH = sum of Est values                  | DERIVED | From TASKS Est values                                                  |
| L120    | prompt_count = max(ceil(HWH/WF), items, files) | DERIVED | From WF, max_items, max_files                                         |
| L121    | Checkpoint every checkpoint_interval prompts  | ASSUMED | From unmeasured profile parameters (MODEL_INVENTORY.md L50-52)         |
| L122    | Guarded scope guard text                      | ASSUMED | Design choice; text not evidence-based                                 |
| L123    | 50% context = effective context limit         | ASSUMED | RULER benchmark on pre-2025 models; not validated on current models    |
| L124    | Opening commentary states model data          | DERIVED | References MODEL_INVENTORY.md values                                   |
| L126-128 | Example: opus-5 vs glm-5.2 sizing            | DERIVED | Computed from WF formula + profile parameters                          |
| L161    | Verification every checkpoint_interval        | DERIVED | From profile checkpoint_interval                                       |
| L163    | SecurityRemediation drift example             | SOURCED | Documented Lana-V2-Dev incident                                        |
| L170    | Verification excluded from chain length limit | ASSUMED | Design rule; no external justification                                 |
| L213    | 5-8 instructions heuristic                    | ASSUMED | General LLM observation; not measured per model                        |
| L213    | max_items takes precedence over heuristic     | DERIVED | From MODEL_INVENTORY.md profile parameters                             |

## PROMPTS_RULES.md PRMT-SC-05

| Lines     | Item                                          | Class   | Evidence or reason                                                  |
|-----------|-----------------------------------------------|---------|---------------------------------------------------------------------|
| L1351     | Frontmatter: model, context, effort required  | DERIVED | Verification references MODEL_INVENTORY.md                          |
| L1356     | intended_model resolves to a row              | DERIVED | model-registry.json model_id_startswith                             |
| L1357     | Context and effort match MODEL_INVENTORY.md   | DERIVED | model-registry.json + MODEL_INVENTORY.md                            |
| L1358     | Commentary states label, profile, WF, cost    | DERIVED | Verification: all values from MODEL_INVENTORY.md                    |
| L1359     | No prompt exceeds WF, max_items, max_files    | DERIVED | From MODEL_INVENTORY.md values (WF ASSUMED, limits ASSUMED)         |
| L1360     | Prompt count formula verification             | DERIVED | From WF, max_items, max_files (all upstream ASSUMED)                |
| L1361     | Checkpoints per profile, guarded scope guard  | ASSUMED | From unmeasured profile parameters                                  |

## Counts

| File                               | Lines | Words | SOURCED | DERIVED | ASSUMED | Rows |
|-------------------------------------|-------|-------|---------|---------|---------|------|
| MODEL_INVENTORY.md                  | 127   | 2151  | 11      | 7       | 26      | 44   |
| TASKS_GUIDES.md                     | 60    | 633   | 1       | 5       | 4       | 10   |
| PROMPTS_GUIDES.md (1c,1f,1g,3a,5)  | 115   | 1685  | 6       | 9       | 6       | 21   |
| PROMPTS_RULES.md (PRMT-SC-05)      | 13    | 248   | 0       | 6       | 1       | 7    |
| **Total**                           | 315   | 4717  | 18      | 27      | 37      | 82   |

## Goal Violations

### Goal 2: Environment-Specific Content (general-purpose inventory must not depend on one agent environment)

| File                | Lines     | Item                                             | Violation                                              |
|---------------------|-----------|--------------------------------------------------|--------------------------------------------------------|
| MODEL_INVENTORY.md  | L72-101   | Devin cost column in Section 3.1                 | Column values from windsurf-model-registry.json only   |
| MODEL_INVENTORY.md  | L107-117  | Section 3.2: 9 Devin-only model rows            | Models exist only in Devin; no API registry entry      |
| MODEL_INVENTORY.md  | L63       | Devin-only price formula                         | Formula uses Devin cost_multiplier and 1/5 assumption  |
| MODEL_INVENTORY.md  | L16       | windsurf-model-registry.json listed as source    | Devin-specific source in a general-purpose file        |
| MODEL_INVENTORY.md  | L68       | "Devin display names map by family"              | Resolution rule specific to one environment            |

### Goal 3: Rules Maintaining Other Rules / Duplicated Sections

| File                | Lines     | Item                                             | Violation                                              |
|---------------------|-----------|--------------------------------------------------|--------------------------------------------------------|
| MODEL_INVENTORY.md  | L40       | R3 October rule                                  | Process rule requiring manual yearly review; exists only to maintain label scheme |
| MODEL_INVENTORY.md  | L47       | Profile change rule (3 sequences threshold)      | Maintains the profile system; threshold unmeasured      |
| PROMPTS_GUIDES.md   | 1c,1f,1g,3a,5 | Partitioning spread over 5 sections          | Overlapping: 1c (effort), 1f (load), 1g (model), 3a (checkpoints), 5 (density) all address "how many items per prompt" |
| PROMPTS_RULES.md    | L1355-1361 | PRMT-SC-05 verifies against unmeasured numbers  | Verification rule checking prompts against ASSUMED values; precision theater |

## Limitations and Known Issues

- **Scope limited to 4 target files (`315` lines, `4,717` words)**: Sibling files that reference `YY-L` or `WF` (`write-prompts.md` Step 1, `update-model-registry.md` 9.4, `edird-phase-planning` `SKILL.md`) were inventoried for P5 propagation in `__STRUT_MDLINVNTRY.md` (`GLOB-FL-037`) rather than line-counted in this table `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV | e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md)`
- **Granularity of row grouping**: Multi-row tables in `MODEL_INVENTORY.md` Section 3.1 (28 rows) and Section 3.2 (9 rows) are grouped by column/rule rather than counted as 37 separate rows per column, preventing table row count from skewing rule-level percentages `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV | e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md)`

## Sources

- **MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV**: `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md` - Primary audit target (`127` lines, `2,151` words, `44` classified rows: `11` SOURCED, `7` DERIVED, `26` ASSUMED) (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-IPPS-TSKGD**: `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\TASKS_GUIDES.md` - Task sizing and HWH/AWH rules (`60` lines, `633` words, `10` classified rows: `1` SOURCED, `5` DERIVED, `4` ASSUMED) (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-IPPS-PRMGD**: `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\PROMPTS_GUIDES.md` - Sections 1c, 1f, 1g, 3a, 5 (`115` lines, `1,685` words, `21` classified rows: `6` SOURCED, `9` DERIVED, `6` ASSUMED) (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-IPPS-PRMRL**: `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\PROMPTS_RULES.md` - `PRMT-SC-05` (`13` lines, `248` words, `7` classified rows: `0` SOURCED, `6` DERIVED, `1` ASSUMED) (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-IPPS-MREG**: `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-registry.json` - Canonical registry for `context_window`, `max_output`, and `effort_levels` (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-IPPS-MPRC**: `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-pricing.json` - Canonical per-1M-token pricing source (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-IPPS-MPRMP**: `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-parameter-mapping.json` - Canonical effort parameter mapping (`anthropic_thinking_factor`) (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-IPPS-WMREG**: `e:\dev\IPPS\PromptSystemV4.5\skills\devin-auto-model-switcher\windsurf-model-registry.json` - Devin environment registry (`Devin cost` source) (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-LOCAL-LLMCAP**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md` - `LLMCAPCLS-IN01` Section 6 circular label derivation and L416 unmeasured profile parameters (Accessed: 2026-10-28) `[VERIFIED]`

## Document History

**[2026-10-28 20:22]**
- Fixed: Added `Timeline` header field, `[VERIFIED]` inline citations in Summary, `Limitations and Known Issues` section (`TF-05`), and `Sources` section (`TF-06`) during P4-S1 verification

**[2026-10-28 19:13]**
- Fixed: Added `Depends on:` field to header block (verify checkpoint F3)

**[2026-10-28 19:12]**
- Initial audit with 82 classified rows across 4 file scopes
