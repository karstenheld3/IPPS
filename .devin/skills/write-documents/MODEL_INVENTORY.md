<PromptSystem MarkdownTablesAllowed=true />

# Model Inventory

Model data for planning documents that depend on model, effort level, and context window. Gives per model: capability label, comparison label for the current year, behavior profile, context window, supported effort levels, workload factor, and standard-tier USD prices per 1M tokens (`In USD`, `Cache USD`, `Out USD`).

Comparison year: `26` (generated 2026-10-29)

This file holds data only. Planning techniques that use it:
- `PROMPTS_GUIDES.md` Section 1g - prompt count, checkpoints, scope guard, context fit per model
- `TASKS_GUIDES.md` - HWH estimation, task and STRUT step sizing, AWH estimation
- `PROMPTS_RULES.md` PRMT-SC-05 - verification of prompts files against this data

Sources (canonical, update this file when they change):
- `skills/llm-evaluation/model-registry.json` 1.11.0 (2026-10-29) - context window, max output request limit, supported effort levels, `release_date`, `uc_class`, `eci_band`, `eci_score`, `gen_equivalent`, `capability_label`, `capability_note`, `behavior_profile`
- `skills/llm-evaluation/model-pricing.json` (2026-10-28) - standard tier USD prices per 1M tokens
- `skills/llm-evaluation/model-parameter-mapping.json` 2.4.0 (2026-09-05) - effort level names and thinking factors
- `skills/devin-auto-model-switcher/windsurf-model-registry.json` 2.0 (2026-08-30) - Devin cost multipliers and Devin-exposed effort levels
- Epoch Capabilities Index `https://epoch.ai/eci` (CSV `https://epoch.ai/data/eci_scores.csv`, snapshot 2026-10-28) - `eci_score`, rounded to the 5-point `eci_band`
- LLM-Research `TBLF-IN02` Section 5.1 (May 2026) - confirmed reliable CSV extraction rows per model and effort (`CSV rows` in Notes)

## 1. Definitions

- HWH (Human Work Hours): hours a skilled human expert needs for the same work unit without AI (read, analyze, edit, verify). Model-independent task size
- Workload factor (WF): HWH one prompt can complete in one run at High effort without skipping items or truncating. WF 1.0 = one prompt carries 1 human work hour
- ECI band: Epoch Capabilities Index score rounded to the nearest 5 (`E145`, `E150`, ...). Frozen at first assignment; the only capability measurement in this file
- Label `YY-L`: release year `YY` plus letter `L` for the model's ECI band relative to that year's anchor (A highest, one letter per 5 ECI points, A-Z). Permanent
- Comp `YY-L`: the same ECI band expressed relative to the comparison year's anchor. Equal Comp = equal capability, whatever the release year. Regenerated at every update; wraps on May 1
- Behavior profile: `precise`, `standard`, or `guarded`. Determines prompt shape (items, files, checkpoints, scope guard)
- Efforts: supported effort levels `L` Low, `M` Medium, `H` High, `X` XHigh, `MX` Max; `-` = no effort parameter (temperature model). Choosing an unlisted level is a PRMT-SC-05 violation
- In USD / Cache USD / Out USD: standard-tier USD price per 1M input, cached input, and output tokens (`-` if not published or unsupported)
- Context: maximum input tokens in thousands (K)
- `CSV rows` (Notes): confirmed reliable rows for 7-column CSV extraction per effort (`L65 M500 H675+`), from `TBLF-IN02`; the only in-house measured capability number

## 2. Value Derivation [ASSUMED]

No benchmark measures HWH per prompt. WF values are estimates within a factor of 2. The checkpoint ledger (`partition-observations.jsonl`, aggregated into `model-registry.json` `observed`) replaces estimates with measurements over time.

Year anchor (ECI band that earns letter A in year YY):
- `anchor(YY) = 170 + 15 * (YY - 26)`: 2024 `E140`, 2025 `E155`, 2026 `E170`, 2027 `E185`. Measured top bands of 2024-2026 (o1, gpt-5.2, gpt-6.1-sol) rose exactly 15 ECI per year; the constant is [ASSUMED] for later years and reviewed at each May 1 wrap, never changed for past years

Label and Comp from the ECI band:
- `letter_index = (anchor(YY) - eci_band) / 5`, letter = `A` + index (`A`..`Z`, no floor); index below 0 clamps to `A`
- Label uses `YY` = release year (`release_date` in `model-registry.json`). Comp uses `YY` = comparison year: `year(today)` from May 1, else `year(today) - 1`
- Example: `gpt-5.2` ECI 153.66 → `E155`, released 2025 → `25-A` (anchor E155); Comp 26 → `26-D` (anchor E170). `gpt-5.4` `E155`, released 2026 → `26-D`, Comp `26-D`: same band, same Comp
- ECI pending (fewer than 4 Epoch benchmarks): band from the nearest same-tier sibling (`glm-5.3-flashx` ← `glm-5.3-flash`) or the UC default `anchor - 5/10/15/20/25` for `UC-1..5`; Notes says `fallback`. The band is replaced once Epoch publishes a score (the only label change besides R4)

Rules:
- R1 Year: `YY` = year of general availability. Never changes
- R2 Band freeze: the ECI band is read once from the Epoch snapshot and never re-read. Newer models do not move older labels
- R4 Observation downgrade: a documented observation (FAILS.md or findings-card entry naming model and skipped items) lowers the letter by one step within the same year; `capability_note` records the evidence. Labels never move up by observation

WF at High effort from the ECI band (`WF` column):
- `WF_high = 2.0 * 2^(-(170 - eci_band) / 10)`: WF halves every 10 ECI points = every two letters. E170 2.0, E165 1.5, E160 1.0, E155 0.75, E150 0.5, E145 0.38, E140 0.25, E135 0.19, E130 0.13, E125 0.09, E120 0.06 [ASSUMED anchor and slope; 1.5 doublings per year sits inside METR's measured 1-4 doublings]
- Models with Efforts `M` or `-` (thinking on/off, temperature): the `WF` column shows their single value `WF_high * 0.5`

Behavior profile (independent of effort level):
- Thresholds: `precise` = IF >= 0.90 and EG <= 1.20; `guarded` = IF < 0.75 or EG > 1.50; `standard` = all others. IF (instruction following) = items_done / items_planned; EG (eagerness) = 1 + extra_actions / items_planned
- Evidence priority: 1) ledger `observed.if` and `observed.eg` with `sequences >= 3`, 2) documented observation (stricter only), 3) benchmark seed (IFEval-Hard, OverAct, OverEager; not plain IFEval), 4) no data = `standard`
- Change rule: one step at a time; upgrade only after 3 sequences at the current profile meet the next threshold; downgrade immediately on a documented observation

Profile parameters:
- `precise`: max_items 8, max_files 6, checkpoint_interval 3, scope_guard normal, heavy_workflows_per_prompt 2
- `standard`: max_items 6, max_files 3, checkpoint_interval 2, scope_guard normal plus explicit file list, heavy_workflows_per_prompt 1
- `guarded`: max_items 4, max_files 2, checkpoint_interval 1, scope_guard strict, heavy_workflows_per_prompt 1
- max_items = numbered instruction items per implementation prompt; max_files = files one implementation prompt may change; checkpoint_interval = implementation prompts between verification checkpoints; heavy_workflows_per_prompt = heavy workflow invocations per prompt

Effort multiplier (relative to the `WF` column):
- Low 0.25, Medium 0.5, High 1.0, XHigh 1.5, Max 2.0 [ASSUMED]
- Thinking-budget models (method `thinking`, Efforts `L M H X`): Max maps to `anthropic_thinking_factor` 1.0 like XHigh in `model-parameter-mapping.json`; plan XHigh
- Adaptive-thinking models (Notes `Medium may skip reasoning`): `TBLF-IN02` measured `claude-opus-4-6` 6 rows and `claude-opus-4-7` 12 rows at Medium against 667 and 843+ at High (adaptive thinking may skip the reasoning phase). For structured-data work plan Low or High, not Medium; other adaptive-thinking models inherit the API mechanism [ASSUMED]

Prices per 1M tokens (`In USD`, `Cache USD`, `Out USD`):
- API models: `In USD = input_per_1m`, `Cache USD = cached_per_1m` (`-` if not published), `Out USD = output_per_1m` from `model-pricing.json` (standard tier)
- Devin-only models: `Out USD = cost_multiplier * 2.50` per `windsurf-model-registry.json`; `In USD = cost_multiplier * 0.50` (input price assumed at 1/5 of output); `Cache USD = -`
- Estimated cost for 1 HWH of agent work (WF 1.0 ≈ 1M tokens, 80% input / 20% output): `0.8 * In USD + 0.2 * Out USD` uncached. Prompt caching lowers the input share by up to 90%

## 3. Model Table

Model resolution: match `intended_model` by longest prefix (same rule as `model_id_startswith` in `model-registry.json`). Unlisted variants inherit the row of their prefix [ASSUMED]: `claude-fable-5.1` → `claude-fable-5`, `claude-opus-5.5` → `claude-opus-5`. Devin display names map by family (`Claude Opus 5 High` → `claude-opus-5`, effort High).

Row set: every text model in `model-registry.json` except `status: retired` (image and computer-use models excluded). `Status legacy`, `deprecated`, or `no_access` is stated in Notes.

Sort order: 1) `Comp` (letter `A` to `Z`), 2) `Label` (newest release year first), 3) `Model` name (ascending).

### 3.1 API Models (llm-evaluation registry)

| Model                        | Label | Comp 26 | Profile  | Context | Efforts    | WF   | In USD | Cache USD | Out USD | Devin cost | Notes                                                                                                                        |
|------------------------------|-------|---------|----------|---------|------------|------|--------|-----------|---------|------------|------------------------------------------------------------------------------------------------------------------------------|
| claude-opus-5-5              | 26-A  | 26-A    | standard | 1000K   | L M H X MX | 2.0  | 4.00   | 0.20      | 20.00   | -          | UC-2, E170 (168.83); API untested; Medium may skip reasoning on structured data (TBLF E1)                                    |
| gpt-6-astra                  | 26-A  | 26-A    | standard | 1050K   | L M H X MX | 2.0  | 10.00  | 1.00      | 50.00   | -          | UC-1, E170 (168.81); API untested, not in Devin                                                                              |
| gpt-6.1-sol                  | 26-A  | 26-A    | standard | 1050K   | L M H X MX | 2.0  | 2.00   | 0.10      | 10.00   | -          | UC-2, E170 (168.37); API untested                                                                                            |
| claude-fable-5               | 26-B  | 26-B    | standard | 1000K   | L M H X MX | 1.5  | 10.00  | 1.00      | 50.00   | 20x        | UC-1, E165 (163.42); API untested; Medium may skip reasoning on structured data (TBLF E1)                                    |
| claude-fable-5-1             | 26-B  | 26-B    | standard | 1000K   | L M H X MX | 1.5  | 10.00  | 0.25      | 50.00   | -          | UC-1, E165 (166.49); API untested; Medium may skip reasoning on structured data (TBLF E1)                                    |
| claude-mythos-5              | 26-B  | 26-B    | standard | 1000K   | L M H X MX | 1.5  | 10.00  | 1.00      | 50.00   | -          | UC-1, E165 (fallback sibling claude-fable-5); Status no_access; Medium may skip reasoning on structured data (TBLF E1)       |
| claude-mythos-5-1            | 26-B  | 26-B    | standard | 1000K   | L M H X MX | 1.5  | 10.00  | 0.25      | 50.00   | -          | UC-1, E165 (fallback sibling claude-fable-5-1); Status no_access; Medium may skip reasoning on structured data (TBLF E1)     |
| claude-opus-5                | 26-B  | 26-B    | standard | 1000K   | L M H X MX | 1.5  | 5.00   | 0.50      | 25.00   | 10x        | UC-2, E165 (163.94); API untested; Medium may skip reasoning on structured data (TBLF E1)                                    |
| claude-sonnet-5-5            | 26-B  | 26-B    | standard | 1000K   | L M H X MX | 1.5  | 2.00   | 0.10      | 10.00   | -          | UC-3, E165 (166.18); API untested; Medium may skip reasoning on structured data (TBLF E1)                                    |
| gemini-4-argon               | 26-B  | 26-B    | standard | 1049K   | L M H      | 1.5  | 2.00   | 0.10      | 10.00   | -          | UC-2, E165 (166.45); $2/$10 through 2026-11-30, $4/$20 from 2026-12-01; Status no_access                                     |
| gpt-5.5-cyber                | 26-B  | 26-B    | standard | -       | L M H X    | 1.5  | 12.50  | 1.25      | 75.00   | -          | UC-1, E165 (fallback sibling gpt-5.5-pro); API untested                                                                      |
| gpt-5.5-pro                  | 26-B  | 26-B    | standard | 1050K   | L M H X    | 1.5  | 30.00  | -         | 180.00  | -          | UC-1, E165 (162.91)                                                                                                          |
| gpt-5.6-cyber                | 26-B  | 26-B    | standard | -       | L M H X    | 1.5  | 12.50  | 1.25      | 75.00   | -          | UC-1, E165 (fallback UC default); API untested                                                                               |
| gpt-5.6-sol                  | 26-B  | 26-B    | standard | 1050K   | L M H X    | 1.5  | 4.00   | 0.40      | 20.00   | 12x        | UC-2, E165 (162.79); Max 4.0 in Devin only                                                                                   |
| gpt-6-sol                    | 26-B  | 26-B    | standard | 1050K   | L M H X MX | 1.5  | 2.00   | 0.20      | 10.00   | -          | UC-2, E165 (163.73); API untested                                                                                            |
| claude-haiku-5-5             | 26-C  | 26-C    | standard | 1000K   | L M H X MX | 1.0  | 0.10   | 0.01      | 0.50    | -          | UC-4, E160 (159.32); <=100K tokens ($0.50/$2.50 >100K), API untested; Medium may skip reasoning on structured data (TBLF E1) |
| claude-opus-4-8              | 26-C  | 26-C    | standard | 1000K   | L M H X MX | 1.0  | 5.00   | 0.50      | 25.00   | 10x        | UC-2, E160 (159.01); API untested; CSV rows H492; Medium may skip reasoning on structured data (TBLF E1)                     |
| gpt-5.4-pro                  | 26-C  | 26-C    | standard | 1048K   | L M H X    | 1.0  | 30.00  | -         | 180.00  | -          | UC-1, E160 (159.57); API untested                                                                                            |
| gpt-5.5                      | 26-C  | 26-C    | standard | 1050K   | L M H X    | 1.0  | 5.00   | 0.50      | 30.00   | 12x        | UC-2, E160 (159.68); CSV rows M437                                                                                           |
| gpt-5.6-terra                | 26-C  | 26-C    | standard | 1050K   | L M H X    | 1.0  | 2.00   | 0.20      | 12.00   | 4.8x       | UC-3, E160 (160.09); Max 2.0 in Devin only                                                                                   |
| claude-opus-4-6              | 26-D  | 26-D    | standard | 1000K   | L M H MX   | 0.75 | 5.00   | 0.50      | 25.00   | 10x        | UC-2, E155 (155.66); API untested; CSV rows M6 H667; Medium may skip reasoning on structured data (TBLF E1)                  |
| claude-opus-4-7              | 26-D  | 26-D    | standard | 1000K   | L M H X MX | 0.75 | 5.00   | 0.50      | 25.00   | 10x        | UC-2, E155 (156.79); API untested; CSV rows M12 H843+; Medium may skip reasoning on structured data (TBLF E1)                |
| claude-sonnet-4-6            | 26-D  | 26-D    | standard | 1000K   | L M H X    | 0.75 | 3.00   | 0.30      | 15.00   | 6x         | UC-3, E155 (152.79); Thinking budget, API untested                                                                           |
| claude-sonnet-5              | 26-D  | 26-D    | standard | 1000K   | L M H X MX | 0.75 | 2.00   | 0.20      | 10.00   | 4x         | UC-3, E155 (156.88); price reduced $3/$15 -> $2/$10; Medium may skip reasoning on structured data (TBLF E1); API untested    |
| gemini-3.1-pro-preview       | 26-D  | 26-D    | standard | 1049K   | L M H      | 0.75 | 2.00   | 0.20      | 12.00   | 4.8x       | UC-2, E155 (155.34); <=200K tokens ($4/$18 >200K); Status no_access                                                          |
| gemini-3.6-flash             | 26-D  | 26-D    | standard | 1049K   | L M H      | 0.75 | 0.75   | 0.075     | 3.75    | 3x         | UC-3, E155 (154.53); supports minimal..high                                                                                  |
| gemini-3.8-flash             | 26-D  | 26-D    | standard | 1049K   | L M H      | 0.75 | 0.75   | 0.075     | 3.75    | -          | UC-3, E155 (157.44); minimal unsupported                                                                                     |
| glm-5.3                      | 26-D  | 26-D    | standard | 1000K   | L H MX     | 0.75 | 1.40   | 0.26      | 4.40    | -          | UC-2, E155 (155.99); Medium rejected by API (HTTP 400)                                                                       |
| glm-5.3-flash                | 26-D  | 26-D    | standard | 1000K   | L H MX     | 0.75 | 0.15   | 0.03      | 0.50    | -          | UC-3, E155 (153.08); Medium rejected by API (HTTP 400)                                                                       |
| glm-5.3-flashx               | 26-D  | 26-D    | standard | 1000K   | L H MX     | 0.75 | 0.37   | 0.075     | 1.25    | -          | UC-3, E155 (fallback sibling glm-5.3-flash); API untested                                                                    |
| glm-5.3-flashx-legal         | 26-D  | 26-D    | standard | 1000K   | L H MX     | 0.75 | 0.37   | 0.075     | 1.25    | -          | UC-3, E155 (fallback sibling glm-5.3-flash); legal domain, API untested; Status no_access                                    |
| gpt-5.3-codex                | 26-D  | 26-D    | standard | -       | L M H      | 0.75 | 1.75   | 0.175     | 14.00   | 5.6x       | UC-2, E155 (157.09); API untested                                                                                            |
| gpt-5.4                      | 26-D  | 26-D    | standard | 1048K   | L M H X    | 0.75 | 2.50   | 0.25      | 15.00   | 6x         | UC-2, E155 (157.31); CSV rows M492                                                                                           |
| gpt-5.6-luna                 | 26-D  | 26-D    | standard | 1050K   | L M H X    | 0.75 | 0.20   | 0.02      | 1.20    | 0.5x       | UC-4, E155 (156.50); Max 0.5 in Devin only                                                                                   |
| gpt-6-luna                   | 26-D  | 26-D    | standard | 1050K   | L M H X MX | 0.75 | 0.10   | 0.01      | 0.50    | -          | UC-4, E155 (156.75); API untested                                                                                            |
| gpt-6.1-terra                | 26-D  | 26-D    | standard | 1050K   | L M H X MX | 0.75 | 1.00   | 0.05      | 5.00    | -          | UC-3, E155 (fallback UC default); API untested                                                                               |
| grok-4.5                     | 26-D  | 26-D    | standard | 500K    | L M H      | 0.75 | 2.00   | 0.30      | 6.00    | -          | UC-2, E155 (154.07); <=200K tokens ($4.00/$12.00 >200K), API untested                                                        |
| grok-4.6                     | 26-D  | 26-D    | standard | 500K    | L M H X    | 0.75 | 2.00   | 0.50      | 6.00    | -          | UC-2, E155 (156.57); <=200K tokens ($4.00/$12.00 >200K), API untested                                                        |
| grok-4.7                     | 26-D  | 26-D    | standard | 500K    | L M H X    | 0.75 | 2.00   | 0.50      | 6.00    | -          | UC-2, E155 (154.37); <=200K tokens ($4.00/$12.00 >200K), API untested                                                        |
| grok-build-0.1               | 26-D  | 26-D    | standard | 256K    | L M H      | 0.75 | 1.00   | 0.20      | 2.00    | -          | UC-3, E155 (fallback UC default); <=200K tokens ($2.00/$4.00 >200K), API untested                                            |
| gpt-5.2                      | 25-A  | 26-D    | standard | 256K    | L M H X    | 0.75 | 1.75   | 0.175     | 14.00   | 5.6x       | UC-2, E155 (153.66); CSV rows M215                                                                                           |
| gpt-5.2-pro                  | 25-A  | 26-D    | standard | 256K    | L M H X    | 0.75 | 21.00  | -         | 168.00  | -          | UC-1, E155 (156.33); API untested                                                                                            |
| glm-4.7-flash                | 26-E  | 26-E    | standard | 200K    | M          | 0.25 | 0.00   | 0.00      | 0.00    | -          | UC-4, E150 (fallback UC default)                                                                                             |
| glm-4.7-flashx               | 26-E  | 26-E    | standard | 200K    | M          | 0.25 | 0.07   | 0.01      | 0.40    | -          | UC-4, E150 (fallback UC default)                                                                                             |
| glm-5.1                      | 26-E  | 26-E    | standard | 200K    | M          | 0.25 | 1.40   | 0.26      | 4.40    | -          | UC-2, E150 (149.82); Thinking on or off only                                                                                 |
| glm-5.2                      | 26-E  | 26-E    | guarded  | 1000K   | L M H X MX | 0.5  | 1.40   | 0.26      | 4.40    | 1.8x       | UC-2, E150 (151.94); over-eagerness (OverAct SIR 2.00) sets profile guarded, no R4                                           |
| gpt-5.4-mini                 | 26-E  | 26-E    | standard | 272K    | L M H X    | 0.5  | 0.75   | 0.075     | 4.50    | 1.8x       | UC-3, E150 (148.70); API untested                                                                                            |
| grok-4.20-0309-non-reasoning | 26-E  | 26-E    | standard | 1000K   | -          | 0.25 | 1.25   | 0.20      | 2.50    | -          | UC-4, E150 (fallback UC default); <=200K tokens ($2.50/$5.00 >200K), No reasoning effort, API untested                       |
| grok-4.20-0309-reasoning     | 26-E  | 26-E    | standard | 1000K   | L M H      | 0.5  | 1.25   | 0.20      | 2.50    | -          | UC-3, E150 (152.11); <=200K tokens ($2.50/$5.00 >200K), API untested                                                         |
| grok-4.20-multi-agent-0309   | 26-E  | 26-E    | standard | 1000K   | L M H X    | 0.5  | 1.25   | 0.20      | 2.50    | -          | UC-3, E150 (152.11); <=200K tokens ($2.50/$5.00 >200K), API untested                                                         |
| grok-4.3                     | 26-E  | 26-E    | standard | 1000K   | L M H      | 0.5  | 1.25   | 0.20      | 2.50    | -          | UC-3, E150 (148.81); <=200K tokens ($2.50/$5.00 >200K), API untested                                                         |
| claude-opus-4-5              | 25-B  | 26-E    | standard | 200K    | L M H      | 0.5  | 5.00   | 0.50      | 25.00   | 10x        | UC-2, E150 (150.11); Registry max_output 8K is a request limit; CSV rows M177                                                |
| gemini-3-flash-preview       | 25-B  | 26-E    | standard | 1049K   | L M H      | 0.5  | 0.50   | 0.05      | 3.00    | 1.2x       | UC-3, E150 (151.88); supports minimal..high                                                                                  |
| gpt-5                        | 25-B  | 26-E    | standard | 256K    | L M H      | 0.5  | 1.25   | 0.125     | 10.00   | 4x         | UC-2, E150 (150.00); CSV rows L356 M450 H492                                                                                 |
| gpt-5-pro                    | 25-B  | 26-E    | standard | 256K    | H          | 0.5  | 15.00  | -         | 120.00  | -          | UC-1, E150 (150.59); API untested                                                                                            |
| gpt-5.1                      | 25-B  | 26-E    | standard | 256K    | L M H      | 0.5  | 1.25   | 0.125     | 10.00   | 4x         | UC-2, E150 (149.76)                                                                                                          |
| gemini-3.1-flash-lite        | 26-F  | 26-F    | standard | 1049K   | L M H      | 0.38 | 0.25   | 0.025     | 1.50    | -          | UC-4, E145 (144.26); supports minimal..high                                                                                  |
| gemini-3.5-flash-lite        | 26-F  | 26-F    | standard | 1049K   | L M H      | 0.38 | 0.30   | 0.03      | 2.50    | -          | UC-4, E145 (144.91); supports minimal..high                                                                                  |
| glm-5                        | 26-F  | 26-F    | standard | 200K    | M          | 0.19 | 1.00   | 0.20      | 3.20    | -          | UC-2, E145 (145.80); Thinking on or off only                                                                                 |
| gpt-5.4-nano                 | 26-F  | 26-F    | standard | 272K    | L M H X    | 0.38 | 0.20   | 0.02      | 1.25    | -          | UC-4, E145 (146.03); API untested                                                                                            |
| claude-sonnet-4-5            | 25-C  | 26-F    | standard | 200K    | L M H X    | 0.38 | 3.00   | 0.30      | 15.00   | 6x         | UC-3, E145 (146.74); Deprecated 2026-09-30 (retires 2026-11-30); CSV rows M168                                               |
| gemini-2.5-flash             | 25-C  | 26-F    | standard | 1049K   | L M H      | 0.38 | 0.30   | 0.03      | 2.50    | -          | UC-3, E145 (142.90); Status legacy                                                                                           |
| gemini-2.5-pro               | 25-C  | 26-F    | standard | 1049K   | L M H      | 0.38 | 1.25   | 0.125     | 10.00   | 4x         | UC-2, E145 (145.13); <=200K tokens ($2.50/$15 >200K); Status legacy                                                          |
| glm-4.5                      | 25-C  | 26-F    | standard | 128K    | M          | 0.19 | 0.60   | 0.11      | 2.20    | -          | UC-2, E145 (fallback UC default)                                                                                             |
| glm-4.5-x                    | 25-C  | 26-F    | standard | 128K    | M          | 0.19 | 2.20   | 0.45      | 8.90    | -          | UC-2, E145 (fallback UC default)                                                                                             |
| glm-4.6                      | 25-C  | 26-F    | standard | 200K    | M          | 0.19 | 0.60   | 0.11      | 2.20    | -          | UC-2, E145 (fallback UC default)                                                                                             |
| glm-4.7                      | 25-C  | 26-F    | standard | 200K    | M          | 0.19 | 0.60   | 0.11      | 2.20    | -          | UC-2, E145 (143.59)                                                                                                          |
| gpt-5-mini                   | 25-C  | 26-F    | standard | 256K    | L M H      | 0.38 | 0.25   | 0.025     | 2.00    | -          | UC-3, E145 (145.34); CSV rows L65 M500 H675+                                                                                 |
| o3                           | 25-C  | 26-F    | standard | 200K    | L M H      | 0.38 | 2.00   | 0.50      | 8.00    | 3.2x       | UC-2, E145 (146.73); API untested                                                                                            |
| o3-deep-research             | 25-C  | 26-F    | standard | 200K    | L M H      | 0.38 | 10.00  | 2.50      | 40.00   | -          | UC-1, E145 (fallback sibling o3); API untested                                                                               |
| o3-pro                       | 25-C  | 26-F    | standard | 200K    | L M H      | 0.38 | 20.00  | -         | 80.00   | -          | UC-1, E145 (147.33); API untested                                                                                            |
| o4-mini                      | 25-C  | 26-F    | standard | 200K    | L M H      | 0.38 | 1.10   | 0.275     | 4.40    | -          | UC-3, E145 (145.46); API untested                                                                                            |
| o4-mini-deep-research        | 25-C  | 26-F    | standard | 200K    | L M H      | 0.38 | 2.00   | 0.50      | 8.00    | -          | UC-2, E145 (fallback sibling o4-mini); API untested                                                                          |
| claude-haiku-4-5             | 25-D  | 26-G    | standard | 200K    | L M H X    | 0.25 | 1.00   | 0.10      | 5.00    | 2x         | UC-4, E140 (142.15); Thinking budget; provider max output 64K; CSV rows 9 (no thinking)                                      |
| glm-4.5-airx                 | 25-D  | 26-G    | standard | 128K    | M          | 0.13 | 1.10   | 0.22      | 4.50    | -          | UC-3, E140 (fallback UC default)                                                                                             |
| glm-4.5v                     | 25-D  | 26-G    | standard | 64K     | M          | 0.13 | 0.60   | 0.11      | 1.80    | -          | UC-3, E140 (fallback UC default)                                                                                             |
| glm-4.6v                     | 25-D  | 26-G    | standard | 128K    | M          | 0.13 | 0.30   | 0.05      | 0.90    | -          | UC-3, E140 (fallback UC default)                                                                                             |
| gpt-5-nano                   | 25-D  | 26-G    | standard | 128K    | L M H      | 0.25 | 0.05   | 0.005     | 0.40    | -          | UC-4, E140 (139.21)                                                                                                          |
| o1-pro                       | 25-D  | 26-G    | standard | 200K    | L M H      | 0.25 | 150.00 | -         | 600.00  | -          | UC-1, E140 (fallback sibling o1); API untested                                                                               |
| o3-mini                      | 25-D  | 26-G    | standard | 200K    | L M H      | 0.25 | 1.10   | 0.55      | 4.40    | -          | UC-3, E140 (140.20); API untested                                                                                            |
| o1                           | 24-A  | 26-G    | standard | 200K    | L M H      | 0.25 | 15.00  | 7.50      | 60.00   | -          | UC-2, E140 (141.72); API untested                                                                                            |
| gemini-2.5-flash-lite        | 25-E  | 26-H    | standard | 1049K   | L M H      | 0.19 | 0.10   | 0.01      | 0.40    | -          | UC-4, E135 (133.82); Status legacy                                                                                           |
| glm-4.5-flash                | 25-E  | 26-H    | standard | 200K    | M          | 0.09 | 0.00   | 0.00      | 0.00    | -          | UC-4, E135 (fallback UC default)                                                                                             |
| gpt-4.1                      | 25-E  | 26-H    | standard | 1048K   | -          | 0.09 | 2.00   | 0.50      | 8.00    | 3.2x       | UC-2, E135 (136.65); No reasoning effort                                                                                     |
| gpt-4.1-mini                 | 25-E  | 26-H    | standard | 1048K   | -          | 0.09 | 0.40   | 0.10      | 1.60    | -          | UC-3, E135 (134.89); No reasoning effort                                                                                     |
| claude-3-5-sonnet            | 24-B  | 26-H    | standard | 200K    | -          | 0.09 | 3.00   | 0.30      | 15.00   | -          | UC-3, E135 (133.43); No reasoning effort; Status deprecated                                                                  |
| o1-mini                      | 24-B  | 26-H    | standard | 128K    | L M H      | 0.19 | 1.10   | 0.55      | 4.40    | -          | UC-3, E135 (135.70); Status no_access                                                                                        |
| gpt-4.1-nano                 | 25-F  | 26-I    | standard | 1048K   | -          | 0.06 | 0.10   | 0.025     | 0.40    | -          | UC-4, E130 (129.54); No reasoning effort                                                                                     |
| gpt-4o                       | 24-C  | 26-I    | standard | 128K    | -          | 0.06 | 2.50   | 1.25      | 10.00   | -          | UC-2, E130 (128.99); No reasoning effort; CSV rows 4                                                                         |
| gpt-4o-2024-05-13            | 24-C  | 26-I    | standard | 128K    | -          | 0.06 | 5.00   | -         | 15.00   | -          | UC-2, E130 (128.99); No reasoning effort; Status legacy                                                                      |
| gpt-4o-mini                  | 24-D  | 26-J    | standard | 128K    | -          | 0.05 | 0.15   | 0.075     | 0.60    | -          | UC-4, E125 (126.46); No reasoning effort; CSV rows 6                                                                         |
| glm-4-air                    | 24-E  | 26-K    | standard | 128K    | M          | 0.03 | 0.20   | 0.03      | 1.10    | -          | UC-4, E120 (fallback UC default)                                                                                             |

### 3.2 Devin-Only Models (no API registry entry)

Context window is not published in the sources (`-`). Price uses the Devin-only formula from Section 2. Labels (from the ECI band in Notes) and profiles for these models live only in this table.

| Model            | Label | Comp 26 | Profile  | Context | Efforts | WF   | In USD | Cache USD | Out USD | Devin cost | Notes                                                                     |
|------------------|-------|---------|----------|---------|---------|------|--------|-----------|---------|------------|---------------------------------------------------------------------------|
| Gemini 3.7 Flash | 26-C  | 26-C    | standard | -       | L M H   | 1.0  | 1.50   | -         | 7.50    | 3x         | E160 (157.97); Gemini API routes it to 3.8 Flash since 2026-10-08         |
| Kimi K3          | 26-C  | 26-C    | standard | -       | H       | 1.0  | 3.00   | -         | 15.00   | 6x         | E160 (157.86); High only; released 2026-07-16                             |
| Gemini 3.5 Flash | 26-D  | 26-D    | standard | -       | L M H   | 0.75 | 1.80   | -         | 9.00    | 3.6x       | E155 (154.88); Gemini API routes it to 3.6 Flash since 2026-10-08         |
| SWE-1.7          | 26-D  | 26-D    | standard | -       | M MX    | 0.75 | 0.50   | -         | 2.50    | 1x         | E155 (fallback UC default UC-3); Medium and Max only; released 2026-07-08 |

Models not listed: use the UC default band of the release year (Section 2) and profile `standard`, or add the model to `model-registry.json` first.

## 4. Maintenance and Calibration

Section 3.1 is generated by `update-model-inventory.py` (session `!ModelRegistryUpdate`) from the registries; Label must equal `capability_label` in `model-registry.json`, which the script derives from `release_date` and `eci_band` and refuses to override. Every registry update: 1) adds `release_date` and the Epoch band for new models, 2) replaces fallback bands that received an Epoch score, 3) regenerates Comp for the current comparison year, 4) reviews ledger `profile_suggested` values with the Section 2 change rule.

May 1 wrap: the comparison year advances; `anchor(YY)` for the new year is appended with the +15 default and the measured top band of the previous year is recorded in `LLMCAPCLS-IN01` Section 3. Prompts files cite Label (permanent); Comp is for choosing a model.

Calibration:
- Skipped items or truncated runs recorded in FAILS.md or a findings card: apply R4 and move the profile one step toward `guarded`; record the evidence in `capability_note` and the Notes column
- Over-eagerness alone (unrequested changes): change only the profile
