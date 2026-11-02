<PromptSystem MarkdownTablesAllowed=true />

# Model Inventory

Model data for planning documents that depend on model, effort level, and context window. Gives per model: depth rung, Items, context window, supported effort levels, and standard-tier USD prices per 1M tokens (`In USD`, `Cache USD`, `Out USD`).

This file holds data only. Part of `@skills:llm-tools` (same folder as the source JSONs). Planning techniques that use it (`@skills:write-documents`):
- `PROMPTS_GUIDES.md` Section 1g - prompt count, checkpoints, scope guard, context fit per model
- `TASKS_GUIDES.md` - HWH estimation, task and STRUT step sizing, AWH estimation
- `PROMPTS_RULES.md` PRMT-SC-05 - verification of prompts files against this data

Sources (canonical, update this file when they change):
- `skills/llm-tools/model-registry.json` 1.12.0 (2026-11-02) - context window, supported effort levels, `uc_class`, `release_date`, `eci_score`, `eci_ci`, `depth`, `depth_evidence`, `deeper_than`, `items`, `scope_guard`, `inventory_note`
- `skills/llm-tools/model-pricing.json` (2026-10-28) - standard tier USD prices per 1M tokens
- `skills/llm-tools/model-parameter-mapping.json` 2.4.0 (2026-09-05) - effort level names and thinking factors
- `skills/devin-auto-model-switcher/windsurf-model-registry.json` 2.0 (2026-08-30) - Devin cost multipliers and Devin-exposed effort levels
- Epoch Capabilities Index `https://epoch.ai/eci` (CSV `https://epoch.ai/data/eci_scores.csv`, snapshot 2026-10-28) - `eci_score` and 95% interval `eci_ci`
- LLM-Research `TBLF-IN02` Section 5.1 (May 2026) - confirmed reliable CSV extraction rows per model and effort (`CSV rows` in Notes)

## 1. Definitions

- Depth `D[n]`: ordinal rung of provable reasoning depth. `D1` = shallowest listed model; higher = more may stay implicit in a prompt. Assigned once, never regraded. `D[n]*` = estimate, replaced by evidence when it arrives. Equal rung = equal prompt shape, not equal quality
- Items: numbered instruction items one implementation prompt may hold so that all complete without skips. `[n]m` = measured from the observation ledger; unmarked = default from the rung (Section 2)
- HWH (Human Work Hours): hours a skilled human expert needs for the same work unit without AI. Model-independent task size; one prompt carries at most 1 HWH
- Context: maximum input tokens in thousands (K). Input read per prompt stays at or below 50% of Context
- Efforts: supported effort levels `L` Low, `M` Medium, `H` High, `X` XHigh, `MX` Max; `-` = no effort parameter. Choosing an unlisted level is a PRMT-SC-05 violation
- In USD / Cache USD / Out USD: standard-tier USD price per 1M input, cached input, and output tokens (`-` if not published or unsupported)
- Notes: the edge that set the rung, `UC-n` (Universal Class: 1 Apex, 2 Flagship, 3 Balanced, 4 Efficient), Epoch score with 95% interval, status, `scope guard strict`, `CSV rows` (confirmed reliable rows for 7-column CSV extraction per effort), adaptive Medium warning, `squeezed by`, `unplaced`

## 2. Value Derivation

Depth edges (`x > y` = x provably deeper than y; the rung is the longest chain of edges below the model):
- E1 vendor tier: same provider and point version, higher class (strict). Across point versions only from the vendor's model-selection guidance (`E1m`, recorded with source and quote)
- E2 successor: same provider, class, and series, later release: rung at least the predecessor's. E3 benchmark: Epoch 95% intervals do not overlap (strict)
- E4 in-house observation naming both models on the same task (strict, `E4m`, overrides E3). E5 sibling tie: unscored model = scored sibling of the same point version and class
- E6 estimate (`*`): unscored model without a sibling tie: rung of the nearest-class sibling minus the class distance, floor `D1`; no sibling = `D1*` `unplaced`
- New models insert between frozen rungs; no free integer = `squeezed by X`. Silence of the named source = tie, never a judgment edge

Prompt shape (read from the row; compute nothing else):
- Effective rung: `H`, `X`, `MX` = Depth; `M` = Depth, except adaptive-thinking models (Notes `adaptive`) one rung lower; `L` one lower; `-` two lower
- Explicitness by effective rung: `D10+` goal-level (0.5 items per outcome unit), `D7-D9` outcome plus named files (1), `D4-D6` step-level (2.5), `D1-D3` keystroke-level (4)
- Items default by effective rung: `D10+` 8, `D7-D9` 6, `D4-D6` 5, `D1-D3` 4. Items 8: max 6 files, checkpoint every 3 prompts; Items 6: 3 files, every 2; Items 5 or less: 2 files, after every prompt
- `prompt_count = max(ceil(expanded_items / Items), ceil(files / max_files), ceil(task_HWH / 1))`
- Notes `scope guard strict`: every prompt states "Do ONLY the numbered items below. Do not refactor, rename, add tests, or touch files not listed. Report any item you could not complete as NOT DONE". Items unchanged
- Cost per prompt: `(0.8 * In USD + 0.2 * Out USD) * tokens / 1M`. Devin-only rows: `Out USD = cost * 2.50`, `In USD = cost * 0.50` [ASSUMED input at 1/5 of output]

## 3. Model Table

Top rung: D12 (2026-11-02)

Model resolution: match `intended_model` by longest prefix (same rule as `model_id_startswith` in `model-registry.json`). Devin display names map by family (`Claude Opus 5 High` → `claude-opus-5`, effort High).

Row set: every text model in `model-registry.json` except `status: retired` (image and computer-use models excluded). Sort: 1) Depth descending, 2) Model ascending.

### 3.1 API Models (llm-tools registry)

| Model                        | Depth | Items | Context | Efforts    | In USD | Cache USD | Out USD | Devin cost | Notes                                                                                                                                               |
|------------------------------|-------|-------|---------|------------|--------|-----------|---------|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| claude-fable-5               | D12   | 8     | 1000K   | L M H X MX | 10.00  | 1.00      | 50.00   | 20x        | E1m > claude-opus-5-5; UC-1; 163.4 [160.5-168.2]; API untested; adaptive: Medium may skip reasoning (TBLF E1)                                       |
| claude-fable-5-1             | D12   | 8     | 1000K   | L M H X MX | 10.00  | 0.25      | 50.00   | -          | E1m > claude-opus-5-5; UC-1; 166.5 [163.5-171.3]; API untested; adaptive: Medium may skip reasoning (TBLF E1)                                       |
| claude-mythos-5              | D12   | 8     | 1000K   | L M H X MX | 10.00  | 1.00      | 50.00   | -          | E5 = claude-fable-5; UC-1; no Epoch score; Status no_access; adaptive: Medium may skip reasoning (TBLF E1)                                          |
| claude-mythos-5-1            | D12   | 8     | 1000K   | L M H X MX | 10.00  | 0.25      | 50.00   | -          | E2 >= claude-fable-5-1; UC-1; no Epoch score; Status no_access; adaptive: Medium may skip reasoning (TBLF E1)                                       |
| claude-opus-5-5              | D11   | 8     | 1000K   | L M H X MX | 4.00   | 0.20      | 20.00   | -          | E1 > claude-sonnet-5-5; UC-2; 168.8 [165.2-173.9]; API untested; adaptive: Medium may skip reasoning (TBLF E1)                                      |
| gpt-5.6-cyber                | D11   | 8     | -       | L M H X    | 12.50  | 1.25      | 75.00   | -          | E1 > gpt-5.6-sol; UC-1; no Epoch score; API untested                                                                                                |
| gpt-6-astra                  | D11   | 8     | 1050K   | L M H X MX | 10.00  | 1.00      | 50.00   | -          | E1 > gpt-6-sol; UC-1; 168.8 [165.4-174.5]; API untested; not in Devin                                                                               |
| claude-sonnet-5-5            | D10   | 8     | 1000K   | L M H X MX | 2.00   | 0.10      | 10.00   | -          | E3 > gpt-5.4-pro; UC-3; 166.2 [163.1-171.3]; API untested; adaptive: Medium may skip reasoning (TBLF E1)                                            |
| gemini-4-argon               | D10   | 8     | 1049K   | L M H      | 2.00   | 0.10      | 10.00   | -          | E3 > gpt-5.4-pro; UC-2; 166.4 [163.2-171.5]; Status no_access; $2/$10 through 2026-11-30, $4/$20 from 2026-12-01                                    |
| gpt-5.5-cyber                | D10   | 8     | -       | L M H X    | 12.50  | 1.25      | 75.00   | -          | E1 > gpt-5.5; UC-1; no Epoch score; API untested                                                                                                    |
| gpt-5.5-pro                  | D10   | 8     | 1050K   | L M H X    | 30.00  | -         | 180.00  | -          | E1 > gpt-5.5; UC-1; 162.9 [160.0-166.6]                                                                                                             |
| gpt-5.6-sol                  | D10   | 8     | 1050K   | L M H X    | 4.00   | 0.40      | 20.00   | 12x        | E1 > gpt-5.6-terra; UC-2; 162.8 [160.2-167.1]; Max 4.0 in Devin only                                                                                |
| gpt-6-sol                    | D10   | 8     | 1050K   | L M H X MX | 2.00   | 0.20      | 10.00   | -          | E2 >= gpt-5.6-sol; UC-2; 163.7 [160.9-167.4]; API untested                                                                                          |
| gpt-6.1-sol                  | D10   | 8     | 1050K   | L M H X MX | 2.00   | 0.10      | 10.00   | -          | E3 > gpt-5.4-pro; UC-2; 168.4 [165.0-174.4]; API untested                                                                                           |
| claude-opus-5                | D9    | 6     | 1000K   | L M H X MX | 5.00   | 0.50      | 25.00   | 10x        | E3 > gpt-5.2-pro; UC-2; 163.9 [161.1-168.2]; API untested; adaptive: Medium may skip reasoning (TBLF E1)                                            |
| gpt-5.4-pro                  | D9    | 6     | 1048K   | L M H X    | 30.00  | -         | 180.00  | -          | E1 > gpt-5.4; UC-1; 159.6 [157.1-162.7]; API untested                                                                                               |
| gpt-5.5                      | D9    | 6     | 1050K   | L M H X    | 5.00   | 0.50      | 30.00   | 12x        | E3 > grok-4.7; UC-2; 159.7 [157.3-163.7]; CSV rows M437                                                                                             |
| gpt-5.6-terra                | D9    | 6     | 1050K   | L M H X    | 2.00   | 0.20      | 12.00   | 4.8x       | E1 > gpt-5.6-luna; UC-3; 160.1 [157.3-163.3]; Max 2.0 in Devin only                                                                                 |
| gpt-6.1-terra                | D9    | 6     | 1050K   | L M H X MX | 1.00   | 0.05      | 5.00    | -          | E2 >= gpt-5.6-terra; UC-3; no Epoch score; API untested                                                                                             |
| claude-haiku-5-5             | D8    | 6     | 1000K   | L M H X MX | 0.10   | 0.01      | 0.50    | -          | E3 > gpt-5-pro; UC-4; 159.3 [156.2-162.5]; API untested; <=100K tokens ($0.50/$2.50 >100K); adaptive: Medium may skip reasoning (TBLF E1)           |
| claude-opus-4-6              | D8    | 6     | 1000K   | L M H MX   | 5.00   | 0.50      | 25.00   | 10x        | E3 > gemini-3-flash-preview; UC-2; 155.7 [153.8-158.1]; API untested; CSV rows M6 H667; adaptive: Medium may skip reasoning (TBLF E1)               |
| claude-opus-4-7              | D8    | 6     | 1000K   | L M H X MX | 5.00   | 0.50      | 25.00   | 10x        | E3 > gpt-5-pro; UC-2; 156.8 [154.9-159.2]; API untested; CSV rows M12 H843+; adaptive: Medium may skip reasoning (TBLF E1)                          |
| claude-opus-4-8              | D8    | 6     | 1000K   | L M H X MX | 5.00   | 0.50      | 25.00   | 10x        | E3 > gpt-5-pro; UC-2; 159.0 [156.9-161.9]; API untested; CSV rows H492; adaptive: Medium may skip reasoning (TBLF E1)                               |
| claude-sonnet-5              | D8    | 6     | 1000K   | L M H X MX | 2.00   | 0.20      | 10.00   | 4x         | E3 > gemini-3-flash-preview; UC-3; 156.9 [154.1-159.7]; API untested; price reduced $3/$15 -> $2/$10; adaptive: Medium may skip reasoning (TBLF E1) |
| gemini-3.8-flash             | D8    | 6     | 1049K   | L M H      | 0.75   | 0.075     | 3.75    | -          | E3 > gpt-5-pro; UC-3; 157.4 [155.1-161.1]; minimal unsupported                                                                                      |
| glm-5.3                      | D8    | 6     | 1000K   | L H MX     | 1.40   | 0.26      | 4.40    | -          | E3 > gemini-3-flash-preview; UC-2; 156.0 [154.2-158.3]; Medium rejected by API (HTTP 400)                                                           |
| gpt-5.2-pro                  | D8    | 6     | 256K    | L M H X    | 21.00  | -         | 168.00  | -          | E1 > gpt-5.2; UC-1; 156.3 [153.9-160.0]; API untested                                                                                               |
| gpt-5.4                      | D8    | 6     | 1048K   | L M H X    | 2.50   | 0.25      | 15.00   | 6x         | E3 > gpt-5-pro; UC-2; 157.3 [155.4-159.8]; CSV rows M492                                                                                            |
| gpt-5.6-luna                 | D8    | 6     | 1050K   | L M H X    | 0.20   | 0.02      | 1.20    | 0.5x       | E3 > gpt-5-pro; UC-4; 156.5 [154.2-159.3]; Max 0.5 in Devin only                                                                                    |
| gpt-6-luna                   | D8    | 6     | 1050K   | L M H X MX | 0.10   | 0.01      | 0.50    | -          | E3 > gpt-5-pro; UC-4; 156.8 [154.3-159.4]; API untested                                                                                             |
| grok-4.6                     | D8    | 6     | 500K    | L M H X    | 2.00   | 0.50      | 6.00    | -          | E3 > gpt-5-pro; UC-2; 156.6 [154.7-159.2]; API untested; <=200K tokens ($4.00/$12.00 >200K)                                                         |
| grok-4.7                     | D8    | 6     | 500K    | L M H X    | 2.00   | 0.50      | 6.00    | -          | E2 >= grok-4.6; UC-2; 154.4 [152.6-157.1]; API untested; <=200K tokens ($4.00/$12.00 >200K)                                                         |
| claude-sonnet-4-6            | D7    | 6     | 1000K   | L M H X    | 3.00   | 0.30      | 15.00   | 6x         | E3 > o3-pro; UC-3; 152.8 [150.2-155.1]; API untested; Thinking budget                                                                               |
| gemini-3-flash-preview       | D7    | 6     | 1049K   | L M H      | 0.50   | 0.05      | 3.00    | 1.2x       | E3 > o3-pro; UC-3; 151.9 [150.4-153.6]; supports minimal..high                                                                                      |
| gemini-3.1-pro-preview       | D7    | 6     | 1049K   | L M H      | 2.00   | 0.20      | 12.00   | 4.8x       | E3 > o3-pro; UC-2; 155.3 [153.3-158.1]; Status no_access; <=200K tokens ($4.00/$18.00 >200K)                                                        |
| gemini-3.6-flash             | D7    | 6     | 1049K   | L M H      | 0.75   | 0.075     | 3.75    | 3x         | E3 > o3-pro; UC-3; 154.5 [152.8-156.6]; supports minimal..high                                                                                      |
| glm-5.3-flash                | D7    | 6     | 1000K   | L H MX     | 0.15   | 0.03      | 0.50    | -          | E3 > o3-pro; UC-3; 153.1 [150.8-155.5]; Medium rejected by API (HTTP 400)                                                                           |
| glm-5.3-flashx               | D7    | 6     | 1000K   | L H MX     | 0.37   | 0.075     | 1.25    | -          | E5 = glm-5.3-flash; UC-3; no Epoch score                                                                                                            |
| glm-5.3-flashx-legal         | D7    | 6     | 1000K   | L H MX     | 0.37   | 0.075     | 1.25    | -          | E5 = glm-5.3-flash; UC-3; no Epoch score; Status no_access; legal domain                                                                            |
| gpt-5-pro                    | D7    | 6     | 256K    | H          | 15.00  | -         | 120.00  | -          | E1 > gpt-5; UC-1; 150.6 [148.9-154.2]; API untested                                                                                                 |
| gpt-5.2                      | D7    | 6     | 256K    | L M H X    | 1.75   | 0.175     | 14.00   | 5.6x       | E3 > o3-pro; UC-2; 153.7 [152.1-155.4]; CSV rows M215                                                                                               |
| gpt-5.3-codex                | D7    | 6     | -       | L M H      | 1.75   | 0.175     | 14.00   | 5.6x       | E3 > o3-pro; UC-2; 157.1 [153.6-161.4]; API untested                                                                                                |
| grok-4.5                     | D7    | 6     | 500K    | L M H      | 2.00   | 0.30      | 6.00    | -          | E3 > o3-pro; UC-2; 154.1 [152.4-156.2]; API untested; <=200K tokens ($4.00/$12.00 >200K)                                                            |
| claude-opus-4-5              | D6    | 5     | 200K    | L M H      | 5.00   | 0.50      | 25.00   | 10x        | E3 > gemini-2.5-pro; UC-2; 150.1 [147.8-153.0]; Registry max_output 8K is a request limit; CSV rows M177                                            |
| glm-5.1                      | D6    | 5     | 200K    | M          | 1.40   | 0.26      | 4.40    | -          | E3 > gemini-2.5-pro; UC-2; 149.8 [147.7-151.9]; Thinking on or off only                                                                             |
| glm-5.2                      | D6    | 5     | 1000K   | L M H X MX | 1.40   | 0.26      | 4.40    | 1.8x       | E3 > gemini-2.5-pro; UC-2; 151.9 [150.0-154.1]; scope guard strict; scope guard source: OverAct SIR 2.00 (over-eagerness)                           |
| gpt-5                        | D6    | 5     | 256K    | L M H      | 1.25   | 0.125     | 10.00   | 4x         | E1 > gpt-5-mini; UC-2; 150.0 (no interval); CSV rows L356 M450 H492                                                                                 |
| gpt-5.1                      | D6    | 5     | 256K    | L M H      | 1.25   | 0.125     | 10.00   | 4x         | E3 > gemini-2.5-pro; UC-2; 149.8 [148.4-151.7]                                                                                                      |
| gpt-5.4-mini                 | D6    | 5     | 272K    | L M H X    | 0.75   | 0.075     | 4.50    | 1.8x       | E3 > gemini-2.5-pro; UC-3; 148.7 [146.9-150.5]; API untested                                                                                        |
| grok-4.20-0309-reasoning     | D6    | 5     | 1000K   | L M H      | 1.25   | 0.20      | 2.50    | -          | E3 > gemini-2.5-pro; UC-3; 152.1 [149.6-154.5]; API untested; <=200K tokens ($2.50/$5.00 >200K)                                                     |
| grok-4.20-multi-agent-0309   | D6    | 5     | 1000K   | L M H X    | 1.25   | 0.20      | 2.50    | -          | E3 > gemini-2.5-pro; UC-3; 152.1 [149.6-154.5]; API untested; <=200K tokens ($2.50/$5.00 >200K)                                                     |
| grok-4.3                     | D6    | 5     | 1000K   | L M H      | 1.25   | 0.20      | 2.50    | -          | E3 > gemini-2.5-pro; UC-3; 148.8 [147.2-150.3]; API untested; <=200K tokens ($2.50/$5.00 >200K)                                                     |
| o3-deep-research             | D6    | 5     | 200K    | L M H      | 10.00  | 2.50      | 40.00   | -          | E1 > o3; UC-1; no Epoch score; API untested                                                                                                         |
| o3-pro                       | D6    | 5     | 200K    | L M H      | 20.00  | -         | 80.00   | -          | E1 > o3; UC-1; 147.3 [145.6-150.1]; API untested                                                                                                    |
| claude-sonnet-4-5            | D5    | 5     | 200K    | L M H X    | 3.00   | 0.30      | 15.00   | 6x         | E3 > o1; UC-3; 146.7 [145.0-148.3]; Status deprecated; Deprecated 2026-09-30 (retires 2026-11-30); CSV rows M168                                    |
| gemini-2.5-pro               | D5    | 5     | 1049K   | L M H      | 1.25   | 0.125     | 10.00   | 4x         | E3 > o1; UC-2; 145.1 [143.4-146.7]; Status legacy; <=200K tokens ($2.50/$15.00 >200K)                                                               |
| glm-5                        | D5    | 5     | 200K    | M          | 1.00   | 0.20      | 3.20    | -          | E3 > o1; UC-2; 145.8 [143.8-147.7]; Thinking on or off only                                                                                         |
| gpt-5-mini                   | D5    | 5     | 256K    | L M H      | 0.25   | 0.025     | 2.00    | -          | E3 > o1; UC-3; 145.3 [143.3-147.1]; CSV rows L65 M500 H675+                                                                                         |
| gpt-5.4-nano                 | D5    | 5     | 272K    | L M H X    | 0.20   | 0.02      | 1.25    | -          | E3 > o1; UC-4; 146.0 [143.6-148.2]; API untested                                                                                                    |
| grok-4.20-0309-non-reasoning | D5*   | 5     | 1000K   | -          | 1.25   | 0.20      | 2.50    | -          | E6 from grok-4.20-0309-reasoning; UC-4; no Epoch score; API untested; <=200K tokens ($2.50/$5.00 >200K); No reasoning effort                        |
| o1-pro                       | D5    | 5     | 200K    | L M H      | 150.00 | -         | 600.00  | -          | E1 > o1; UC-1; no Epoch score; API untested                                                                                                         |
| o3                           | D5    | 5     | 200K    | L M H      | 2.00   | 0.50      | 8.00    | 3.2x       | E3 > o1; UC-2; 146.7 [144.8-148.5]; API untested                                                                                                    |
| o4-mini-deep-research        | D5    | 5     | 200K    | L M H      | 2.00   | 0.50      | 8.00    | -          | E1 > o4-mini; UC-2; no Epoch score; API untested                                                                                                    |
| claude-haiku-4-5             | D4    | 5     | 200K    | L M H X    | 1.00   | 0.10      | 5.00    | 2x         | E3 > gpt-4.1; UC-4; 142.2 [139.4-144.1]; Thinking budget; provider max output 64K; CSV rows 9 (no thinking)                                         |
| gemini-2.5-flash             | D4    | 5     | 1049K   | L M H      | 0.30   | 0.03      | 2.50    | -          | E3 > gpt-4.1; UC-3; 142.9 [139.1-146.2]; Status legacy                                                                                              |
| gemini-3.1-flash-lite        | D4    | 5     | 1049K   | L M H      | 0.25   | 0.025     | 1.50    | -          | E3 > o3-mini; UC-4; 144.3 [142.3-145.7]; supports minimal..high                                                                                     |
| gemini-3.5-flash-lite        | D4    | 5     | 1049K   | L M H      | 0.30   | 0.03      | 2.50    | -          | E3 > o3-mini; UC-4; 144.9 [142.4-146.3]; supports minimal..high                                                                                     |
| glm-4.7                      | D4    | 5     | 200K    | M          | 0.60   | 0.11      | 2.20    | -          | E3 > gpt-4.1; UC-2; 143.6 [141.4-145.8]                                                                                                             |
| o1                           | D4    | 5     | 200K    | L M H      | 15.00  | 7.50      | 60.00   | -          | E3 > gpt-4.1; UC-2; 141.7 [139.7-142.9]; API untested                                                                                               |
| o4-mini                      | D4    | 5     | 200K    | L M H      | 1.10   | 0.275     | 4.40    | -          | E3 > o3-mini; UC-3; 145.5 [142.9-147.2]; API untested                                                                                               |
| glm-4.5                      | D3    | 4     | 128K    | M          | 0.60   | 0.11      | 2.20    | -          | E1 > glm-4.5-airx; UC-2; no Epoch score                                                                                                             |
| glm-4.5-x                    | D3    | 4     | 128K    | M          | 2.20   | 0.45      | 8.90    | -          | E1 > glm-4.5-airx; UC-2; no Epoch score                                                                                                             |
| glm-4.6                      | D3    | 4     | 200K    | M          | 0.60   | 0.11      | 2.20    | -          | E1 > glm-4.6v; UC-2; no Epoch score                                                                                                                 |
| gpt-4.1                      | D3    | 4     | 1048K   | -          | 2.00   | 0.50      | 8.00    | 3.2x       | E1 > gpt-4.1-mini; UC-2; 136.7 [133.6-138.3]; No reasoning effort                                                                                   |
| o3-mini                      | D3    | 4     | 200K    | L M H      | 1.10   | 0.55      | 4.40    | -          | E3 > gpt-4.1-mini; UC-3; 140.2 [137.0-141.8]; API untested                                                                                          |
| claude-3-5-sonnet            | D2    | 4     | 200K    | -          | 3.00   | 0.30      | 15.00   | -          | E3 > gpt-4o-mini; UC-3; 133.4 [129.2-137.8]; Status deprecated; No reasoning effort                                                                 |
| gemini-2.5-flash-lite        | D2    | 4     | 1049K   | L M H      | 0.10   | 0.01      | 0.40    | -          | E3 > gpt-4o-mini; UC-4; 133.8 [130.3-136.2]; Status legacy                                                                                          |
| glm-4.5-airx                 | D2    | 4     | 128K    | M          | 1.10   | 0.22      | 4.50    | -          | E1 > glm-4.5-flash; UC-3; no Epoch score                                                                                                            |
| glm-4.5v                     | D2    | 4     | 64K     | M          | 0.60   | 0.11      | 1.80    | -          | E1 > glm-4.5-flash; UC-3; no Epoch score                                                                                                            |
| glm-4.6v                     | D2*   | 4     | 128K    | M          | 0.30   | 0.05      | 0.90    | -          | E6 from glm-4.6; UC-3; no Epoch score                                                                                                               |
| glm-4.7-flash                | D2*   | 4     | 200K    | M          | 0.00   | 0.00      | 0.00    | -          | E6 from glm-4.7; UC-4; no Epoch score                                                                                                               |
| glm-4.7-flashx               | D2*   | 4     | 200K    | M          | 0.07   | 0.01      | 0.40    | -          | E6 from glm-4.7; UC-4; no Epoch score                                                                                                               |
| gpt-4.1-mini                 | D2    | 4     | 1048K   | -          | 0.40   | 0.10      | 1.60    | -          | E3 > gpt-4o-mini; UC-3; 134.9 [131.0-136.5]; No reasoning effort                                                                                    |
| gpt-5-nano                   | D2    | 4     | 128K    | L M H      | 0.05   | 0.005     | 0.40    | -          | E3 > gpt-4o; UC-4; 139.2 [134.1-141.2]                                                                                                              |
| o1-mini                      | D2    | 4     | 128K    | L M H      | 1.10   | 0.55      | 4.40    | -          | E3 > gpt-4o; UC-3; 135.7 [132.4-137.2]; Status no_access                                                                                            |
| glm-4-air                    | D1*   | 4     | 128K    | M          | 0.20   | 0.03      | 1.10    | -          | unplaced; UC-4; no Epoch score                                                                                                                      |
| glm-4.5-flash                | D1*   | 4     | 200K    | M          | 0.00   | 0.00      | 0.00    | -          | E6 from glm-4.5-airx; UC-4; no Epoch score                                                                                                          |
| gpt-4.1-nano                 | D1    | 4     | 1048K   | -          | 0.10   | 0.025     | 0.40    | -          | bottom; UC-4; 129.5 [123.3-131.8]; No reasoning effort                                                                                              |
| gpt-4o                       | D1    | 4     | 128K    | -          | 2.50   | 1.25      | 10.00   | -          | bottom; UC-2; 129.0 [124.6-131.2]; No reasoning effort; CSV rows 4                                                                                  |
| gpt-4o-2024-05-13            | D1    | 4     | 128K    | -          | 5.00   | -         | 15.00   | -          | bottom; UC-2; 129.0 [124.6-131.2]; Status legacy; No reasoning effort                                                                               |
| gpt-4o-mini                  | D1    | 4     | 128K    | -          | 0.15   | 0.075     | 0.60    | -          | bottom; UC-4; 126.5 [120.1-128.5]; No reasoning effort; CSV rows 6                                                                                  |
| grok-build-0.1               | D1*   | 4     | 256K    | L M H      | 1.00   | 0.20      | 2.00    | -          | unplaced; UC-3; no Epoch score; API untested; <=200K tokens ($2.00/$4.00 >200K)                                                                     |

### 3.2 Devin-Only Models (no API registry entry)

Context window is not published in the sources (`-`). Rungs set by hand from the vendor's comparison, routing, or lineage statement (EC-6) and marked `*`; prices use the Devin-only formula from Section 2.

| Model            | Depth | Items | Context | Efforts | In USD | Cache USD | Out USD | Devin cost | Notes                                                                                                                                                      |
|------------------|-------|-------|---------|---------|--------|-----------|---------|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Kimi K3          | D9*   | 6     | -       | H       | 3.00   | -         | 15.00   | 6x         | EC-6: vendor states it still trails claude-fable-5 (D12) and gpt-5.6-sol (D10), one below the lower reference; Epoch 157.9; High only; released 2026-07-16 |
| Gemini 3.7 Flash | D8*   | 6     | -       | L M H   | 1.50   | -         | 7.50    | 3x         | EC-6: Gemini API routes it to gemini-3.8-flash (D8) since 2026-10-08; Epoch 158.0                                                                          |
| Gemini 3.5 Flash | D7*   | 6     | -       | L M H   | 1.80   | -         | 9.00    | 3.6x       | EC-6: Gemini API routes it to gemini-3.6-flash (D7) since 2026-10-08; Epoch 154.9                                                                          |
| SWE-1.7          | D6*   | 5     | -       | M MX    | 0.50   | -         | 2.50    | 1x         | EC-6: vendor states it is trained from Kimi K2.7, a Flagship-class base [ASSUMED rung]; Medium and Max only; released 2026-07-08                           |

Models not listed: add the model to `model-registry.json` and run the registry update; until then plan it as `D1` with keystroke-level prompts.

## 4. Maintenance

- Section 3.1 and the `Top rung` line are generated from the registries; hand edits are overwritten. Section 3.2 rows are hand-maintained and re-evaluated only when the referenced model's rung or the vendor statement changes
- Every registry update: new models receive `release_date`, `uc_class`, Epoch score and interval, and edge-case outcomes from vendor pages, then the layering inserts their rungs. Existing rungs never move; only `*` estimates may change to measured
- Manual edges (`deeper_than`) carry model, kind, source, access date, and quoted statement; an edge without them, or one that closes a cycle, stops the update
- Items: `observed.items` from the ledger replaces the default after 3 sequences; a skip observation lowers it to the largest fully completed value. Items never changes Depth
- Scope guard: `scope_guard: strict` is set with the FAILS or ledger reference in `inventory_note`
