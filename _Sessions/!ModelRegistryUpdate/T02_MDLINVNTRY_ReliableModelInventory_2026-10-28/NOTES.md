# NOTES: Reliable Model Inventory

**Doc ID**: MDLRGUP-MDLINVNTRY-NOTES

## MUST-NOT-FORGET

- `[PROMPTSYSTEM_FOLDER]` is the source of truth. Never edit `.devin/` directly. After P5 edits: `robocopy "[PROMPTSYSTEM_FOLDER]" "[AGENT_FOLDER]" /MIR /XD .git`
- DESIGN → IMPLEMENT gate: no edit to the three skill files, PRMT-SC-05, or the registry before [ACTOR] answers the DDs of P2
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

- (DD-01..05 pending, see STRUT P2)

## Important Findings

- **Epoch ECI CSV**: Leaderboard tab at `https://epoch.ai/eci?view=graph&tab=leaderboard` has a "Download table" button producing `eci-leaderboard-general.csv` (271 models, 6 columns: Model, Lab, ECI, ECI CI low, ECI CI high, Benchmarks). Stable direct-download URL: `https://epoch.ai/data/eci_scores.csv`. No DOM extraction needed. User confirmed 2026-10-28 19:18

## Topic Registry

**Global topics** (registered in ID-REGISTRY.md):
- `MDLRGUP` - Model Registry Update (parent session topic)

**Subtopics** (session-local):
- `MDLINVNTRY` - Model Inventory Reliability (nested as MDLRGUP-MDLINVNTRY; IDs: `MDLRGUP-MDLINVNTRY-*`)

## Significant Prompts Log

- (none yet)
