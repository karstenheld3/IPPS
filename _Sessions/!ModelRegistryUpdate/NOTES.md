# NOTES: Model Registry Update

**Doc ID**: MDLRGUP-NOTES

Permanent session for updating LLM model registry, pricing, and parameter mapping JSONs.

## Purpose

Fetch current model data from Anthropic and OpenAI provider websites, update canonical JSON files in `[DEVSYSTEM_FOLDER]/skills/llm-evaluation/`, and distribute to all target locations.

## Key Paths

- **Workflow**: `[WORKSPACE_FOLDER]/update-model-registry.md`
- **Canonical JSONs**: `[DEVSYSTEM_FOLDER]/skills/llm-evaluation/`
  - `model-registry.json`
  - `model-pricing.json`
  - `model-parameter-mapping.json`
- **Artifacts**: This session folder (screenshots, DOM extracts, transcriptions)
- **Distribution targets**: `.devin/skills/llm-evaluation/`

## Current Phase

**[2026-10-28 18:55]** EXPLORE (P1 not started). Plan: `_agent_work/__STRUT_MDLINVNTRY.md [MDLRGUP-MDLINVNTRY-STRUT]`, budget 1 AWH for P1-P4.
- Trigger: `MODEL_INVENTORY.md`, `TASKS_GUIDES.md`, `PROMPTS_GUIDES.md` 1g (all rewritten 2026-10-28 via `__TASKS_LLMCAPCLS.md`) rest on unmeasured values; review findings in STRUT "Known Knowns"
- Next: P1 `/deep-research` MEPI FOCUSED into `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28/`, then P2 decisions DD-01..05 to user, then P3 `/write-template` prompts branch
- Gate: P5 (edits to PromptSystem files) only after the user answers DD-01..05

## Key Decisions

- (DD-01..05 pending, see STRUT P2)

## Topic Registry

**Global topics** (registered in ID-REGISTRY.md):
- `MDLRGUP` - Model Registry Update (this session; parent topic for nested IDs)
- `MDLBHVPRM` - Model Behavioral Parameters (eagerness and instruction-following benchmarks)
- `LLMCAPCLS` - LLM Capability Classes (year-letter labels; under review by MDLINVNTRY)

**Subtopics** (session-local):
- `MDLINVNTRY` - Model Inventory Reliability: source-backed inventory, lean TASKS/PROMPTS planning method, recurring inventory update template (nested as MDLRGUP-MDLINVNTRY)

## Topic Folders

- **T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19** - Research benchmarks for eagerness and instruction_following model parameters
- **T02_MDLINVNTRY_ReliableModelInventory_2026-10-28** - (planned, STRUT P1) audit of inventory values, reliable sources per field, work-per-prompt options

## Related External Design

- KarstensWorkspace `_Sessions\_!AINewsResearch\NOTES.md` "Model and Hardware Tiers" (2026-10-25) and `_INFO_AINWSRCH-MODELTIER-01_GenerationTiering.md`: time-independent model tier record (Vendor generation, Universal Class UC-1..5, Epoch ECI band with snapshot date, generation equivalent). QS-12: no Artificial Analysis scores for tiering. Candidate replacement for the `YY-L` scheme (DD-01)
- KarstensWorkspace `_Sessions\_!AINewsResearch\_PROMPTS_AI-News-Research_TEMPLATE.md`: exemplar for the run-folder prompts template (STRUT P3)

## Migration History

**[2026-08-30]** Restructured from in-skill workflow to workspace-level workflow.
- Moved `update-model-registry.md` from `skills/llm-evaluation/` to workspace root
- Moved `model-sources/` artifacts from `skills/llm-evaluation/model-sources/` to this session
- Deleted `model-sources/` from both DevSystemV4.2 and .devin

## Significant Prompts Log

[2026-10-28 18:45] User reopened the session after the LLMCAPCLS rewrite; set four goals and asked for a 1 AWH STRUT
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
