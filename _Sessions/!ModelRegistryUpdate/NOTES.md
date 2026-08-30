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

## Migration History

**[2026-08-30]** Restructured from in-skill workflow to workspace-level workflow.
- Moved `update-model-registry.md` from `skills/llm-evaluation/` to workspace root
- Moved `model-sources/` artifacts from `skills/llm-evaluation/model-sources/` to this session
- Deleted `model-sources/` from both DevSystemV4.2 and .devin
