# NOTES: Reliable Model Inventory

**Doc ID**: MDLRGUP-MDLINVNTRY-NOTES

## MUST-NOT-FORGET

- `[PROMPTSYSTEM_FOLDER]` is the source of truth. Never edit `.devin/` directly. After P5 edits: `robocopy "[PROMPTSYSTEM_FOLDER]" "[AGENT_FOLDER]" /MIR /XD .git`
- DESIGN → IMPLEMENT gate: `DD-01` (b-variant), `DD-06`, `DD-07`, `DD-08` answered 2026-10-29 14:17; `DD-02..05` still open (WF kept by implication of `DD-07`; Profile, Devin cost, Section 3.2, provider scope unchanged until answered)
- Label is permanent (`release_date` year + frozen `eci_band`); Comp is regenerated and wraps on May 1. Prompts files cite Label, never Comp
- `capability_label` is script-derived; never hand-edit it in `model-registry.json` (`update-model-inventory.py` aborts on mismatch, Gate 9.4 checks the derivation)
- Goal 2 (general purpose): nothing in the inventory or the planning method may depend on Devin, Cascade, or IPPS workflow names. Environment data (cost multipliers, display names) stays in environment registries
- Goal 3 (lean): the outcome is fewer rules and fewer numbers, not the same numbers relabeled `[ASSUMED]`. Target `MODEL_INVENTORY.md` under 60 lines
- MECT: one name per concept. A time-independent model tier record already exists (KarstensWorkspace `_!AINewsResearch/NOTES.md` "Model and Hardware Tiers", 2026-10-25): Vendor generation, Universal Class UC-1..5, ECI band from Epoch, generation equivalent. Do not keep a second tiering scheme (`YY-L`) beside it without a decision
- Capability evidence: Epoch ECI read from `https://epoch.ai/eci` only. Not used for tiering (QS-12 precedent): Artificial Analysis index, LMArena Elo, "gap to frontier"
- Every number without a source is `[ASSUMED]` and counts against Goal 3. Prefer dropping a number over inventing one
- GLOB-FL-037: every change propagates to all sibling locations (inventory, both guides, PRMT-SC-05, `write-prompts.md`, `update-model-registry.md` 9.4, registry `_comment`, `LLMCAPCLS-IN01`, `edird-phase-planning` SKILL.md)
- Pre-Write Privacy Gate: the template in the session may carry real paths; skill files stay generic
- Timestamps from request metadata (`2026-10-28 18:45 UTC+01:00` for this STRUT)
- Playwright for all provider and Epoch pages. `search_web` / `read_url_content` only for discovery
- `update-model-registry.md` distributes JSONs to `e:\Dev\Lana-V1\config` and `e:\Dev\Lana-V2\config`: never run it inside this STRUT without explicit [ACTOR] confirmation

## Table of Contents

- [MUST-NOT-FORGET](#must-not-forget)
- [Initial Request](#initial-request)
- [Session Info](#session-info)
- [Agent Instructions](#agent-instructions)
- [Key Decisions](#key-decisions)
- [Important Findings](#important-findings)
- [Topic Registry](#topic-registry)
- [Significant Prompts Log](#significant-prompts-log)

## Initial Request

````text
/session-load E:\dev\IPPS\_Sessions\!ModelRegistryUpdate\

MODEL_INVENTORY.md is full of unreliable information and assumptions
review also
TASKS_GUIDES.md
PROMPTS_GUIDES.md

Goals:
1. We must find a workable solution for agentic work planning in TASKS and PROMPTS files.
2. I want these files to be as general purpose as is needed to be used with any agent or agentic environment.
3. inventory and instructions should not be over-engineered and not consume unnecessary tokens
4. We need reliable sources so that we can use a prompts template that is used to write a prompts file with full instructions to update all model inventories. Like here e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_PROMPTS_AI-News-Research_TEMPLATE.md  Each run should get its own folder.

Then think hard what is needed to reach the goal. Use deep-research.md and write-template.md and other prompt system workflows

/write-strut for 1 AWH
````

## Session Info

- **Started**: 2026-10-28
- **Goal**: Replace assumption-based content in `MODEL_INVENTORY.md`, `TASKS_GUIDES.md`, `PROMPTS_GUIDES.md` 1g with source-backed data and a lean planning method usable in any agentic environment; deliver a prompts template that updates all model inventories, one run folder per run
- **Operation Mode**: IMPL-ISOLATED
- **Output Location**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28`

## Agent Instructions

- **Strategy**: MEPI
- **Scope**: FOCUSED
- **Domain**: DEFAULT
- **Dimensions**: technical (sources, extraction) and practical (planning use, token cost)
- Playwright for every web page (provider pages, Epoch, METR)
- Epoch ECI from `https://epoch.ai/eci` only
- Not used for tiering or capability evidence: Artificial Analysis index, LMArena Elo, "gap to frontier" values

## Key Decisions

- **[2026-10-29 14:17] DD-01 = b-variant** (user-directed, supersedes recommendation `a`): keep `YY-L`, but the letter is the Epoch ECI band relative to a year anchor (`anchor(YY) = 170 + 15 * (YY - 26)`, one letter per 5 ECI points, A-Z). Former R2 (UC tier), R3 (October cap), R5 (max-output cap) removed
- **[2026-10-29 14:17] DD-06 = 1**: inventory lists every text model in `model-registry.json` except `status: retired` (92 rows + 4 Devin-only)
- **[2026-10-29 14:17] DD-07 = 1**: one `WF` column (High, from the band: `2.0 * 2^(-(170 - band) / 10)`) plus `Efforts` column; per-effort columns removed
- **[2026-10-29 14:17] DD-08 = A-Z**: no floor letter; index clamps only below A
- New column `Comp YY` (comparison year = `year(today)` from May 1, else previous year); sort order Comp, Label year desc, Model name
- `DD-02..05` open (see `IN01` Section 5)

## Important Findings

- **Year anchors (2026-10-29)**: top Epoch ECI band per release year is `E140` (2024, o1), `E155` (2025, gpt-5.2), `E170` (2026, gpt-6.1-sol / gpt-6-astra / claude-opus-5-5): +15 per year, basis of `anchor(YY)`. Under UC-tier letters, `26-C` held 22 models spanning ECI 145.8-168.8; under band letters 2026 spreads over A-F
- **TBLF-IN02 cross-check (2026-10-29)**: LLM-Research CSV extraction limits (May 2026) do not order models within E145-E160 (`gpt-5-mini` M500 ~ `gpt-5.4` M492 ~ `gpt-5` H492) but show effort and thinking method dominate (`claude-opus-4-6` M6 vs H667). Used as `CSV rows` Notes marker and adaptive-thinking Medium warning, not as letter source
- **Epoch ECI CSV**: Leaderboard tab at `https://epoch.ai/eci?view=graph&tab=leaderboard` has a "Download table" button producing `eci-leaderboard-general.csv` (271 models, 6 columns: Model, Lab, ECI, ECI CI low, ECI CI high, Benchmarks). Stable direct-download URL: `https://epoch.ai/data/eci_scores.csv`. No DOM extraction needed. User confirmed 2026-10-28 19:18
- **YY-L Rule Fix (2026-10-29 13:37, superseded 14:30 by band-based letters, kept for history)**:
  1. **R3 Release-month rule**: `YY-A` is never assigned to models released before October of `YY` (no retroactive October promotion of Jan–Sep models). Only `UC-1 Apex` models released in Oct–Dec of `YY` can receive `YY-A`.
  2. **R2 Strict vendor-tier separation**: Within any release year, `UC-1 Apex` (`claude-fable-5`, `claude-fable-5-1`, `gpt-6-astra`), `UC-2 Flagship` (`claude-opus-*`, `gpt-*-sol`, `gpt-5.5/5.4`, `gemini-4-argon`, `gemini-3.1-pro-preview`, `glm-5.3`, `glm-5.2`, `glm-5.1`, `glm-5`, `grok-4.7/4.6/4.5`), `UC-3 Balanced` (`claude-sonnet-*`, `gpt-*-terra`, `gpt-5.4-mini`, `gemini-3.8/3.6-flash`, `glm-5.3-flash*`, `grok-4.3/4.20`), and `UC-4 Efficient` (`claude-haiku-*`, `gpt-*-luna`, `gemini-*-flash-lite`) occupy distinct letter tiers (`26-B`, `26-C`, `26-D`, `26-E`). `Opus`, `Fable`, `Sonnet`, and `Haiku` are never placed in the same category.
  3. **GLM-5.2 placement**: `glm-5.2` is `UC-2 Flagship` (`26-C`, `guarded` profile) because its documented issue is over-eagerness (`OverAct SIR 2.00`), which changes only `behavior_profile` (`MODEL_INVENTORY.md` Section 4).

## Topic Registry

**Global topics** (registered in ID-REGISTRY.md):
- `MDLRGUP` - Model Registry Update (parent session topic)

**Subtopics** (session-local):
- `MDLINVNTRY` - Model Inventory Reliability (nested as MDLRGUP-MDLINVNTRY; IDs: `MDLRGUP-MDLINVNTRY-*`)

## Significant Prompts Log

- (none yet)
