# Release Notes: 2026-08-30

## Summary

This release covers work from 2026-07-30 to 2026-08-30, spanning 16 commits across DevSystemV4.2, skills, workflows, documentation, and model registry updates. Major themes: V4.2 stabilization, new skills (hosting, image-tools, seo-tools), model registry refresh with 4 new Anthropic models, and artifact storage refactoring.

## Changes Since v4.1

### Model Registry and Pricing

- **4 new Anthropic models**: claude-fable-5, claude-mythos-5, claude-opus-5, claude-sonnet-5
- **gpt-5.6-sol price reduction**: input $5 -> $4/MTok, output $30 -> $20/MTok (confirmed by OpenAI Aug 24 email, promotional through 2026-11-21)
- **3 Anthropic models retired**: claude-opus-4.1, claude-opus-4, claude-sonnet-4
- **gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna** added (from v4.1 cycle, first committed 2026-07-30)
- Registry bumped v1.7.0 -> v1.8.0
- Synced to `.devin/skills/llm-evaluation/` and `llm-transcription/`

### New Skills

- **hosting** - Platform-specific deployment templates (Netlify, Vercel, Azure App Service, SharePoint, Zola) with SETUP, UNINSTALL, and deploy scripts (.ps1/.bat)
- **image-tools** - Image conversion, resizing, compression via ImageMagick and Pillow
- **seo-tools** - DataForSEO API, Google Search Console, IndexNow, Plausible analytics

### New Workflows

- **deploy.md** - Deploy project to configured hosting platform
- **write-template.md** - Create purpose-built document templates

### Refactoring

- **Model sources migrated** from `DevSystemV4.2/skills/llm-evaluation/model-sources/` to `_Sessions/!ModelRegistryUpdate/model-sources/` (permanent session folder)
- **update-model-registry.md** moved from skill folder to workspace root
- Phase 9 rewritten for multi-target distribution (agent folder + dependent skills)
- Removed `__pycache__` directories and `.tmp_` artifacts from DevSystemV4.2

### Skill and Workflow Updates

- **write-documents**: APAPALAN rules, conversation humanizing rules, conversation template, skill guides/rules, DEFERRED_IMPROVEMENTS template
- **deep-research**: RESEARCH_TOOLS, RESEARCH_SUMMARY_RULES, profile templates
- **ms-playwright-mcp**: SKILL.md updates
- **windsurf-auto-model-switcher**: registry and script updates
- **coding-conventions**: LOGGING-RULES updates
- **Workflows updated**: cleanup, conversation-draft, improve, remove, critique, verify, propose-minto, research, sync, write-* family

### Rules

- **agent-behavior.md**: Updated behavioral rules
- **core-conventions.md**: Updated formatting and writing conventions
- **tools-and-skills.md**: Updated tool locations and skill registry

### Documentation

- **Concepts**: Cross-reference links, removed [VERIFIED] markers
- **README**: Updated with V4.2 references and missing workflows
- **INFO_HOW_DEVIN_WORKS**: Updated research document
- **RECSLFIM-IN01**: New INFO document on Recursive Self-Improvement

### Deploy Script

- **deploy-to-all-repos.md**: Updated with new skills, deprecated files, and workflow filters

## Sessions

### !ModelRegistryUpdate (permanent)

**Goal**: Centralized storage for model registry update artifacts

**Artifacts:**
- DOM extracts (JSON) for Anthropic pricing, model IDs, OpenAI standard/batch
- Screenshots archive (6 source pages, 44 images total for 2026-08-30)
- Historical data migrated from 2026-01-24 through 2026-07-31

### _2026-01-26_llm-transcription-skill (pre-existing)

Pre-dates this release. No changes.

### _2026-01-27_llm-computer-use (pre-existing)

Pre-dates this release. No changes.

### _2026-03-19_MinifyIPPS (pre-existing)

Pre-dates this release. No changes.

## Statistics

- **Commits since v4.1**: 16
- **Files changed**: 456
- **New skills**: 3 (hosting, image-tools, seo-tools)
- **New workflows**: 2 (deploy, write-template)
- **New models**: 4 (claude-fable-5, claude-mythos-5, claude-opus-5, claude-sonnet-5)
- **Price changes**: 1 (gpt-5.6-sol reduction)
- **Status changes**: 3 (retired)
- **Date range**: 2026-07-30 to 2026-08-30

## Pending (Not Blocking Release)

- Context windows for claude-fable-5, claude-mythos-5, claude-sonnet-5 (set to null)
- Prefix entries for 4 new Anthropic models in `model_id_startswith` (method, max_output config)
- LLM_EVALUATION_TESTED_MODELS.md is workspace-local, not distributed

## Document History

**[2026-08-30 15:00]**
- Initial release notes created
