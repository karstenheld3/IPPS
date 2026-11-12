# Release Notes: v4.5 (2026-11-03)

## Summary

This release covers work from 2026-09-23 to 2026-11-03, spanning 42 commits across PromptSystemV4.5. Major themes: full research-to-writing toolchain (document types, writing techniques, personas, analysis-methods skill, and 15 new research/analysis/deliverable-writing workflows), unified `llm-tools` skill (consolidating evaluation, transcription, and computer-use) with depth ladder capability model (D1-D12), `terminal-robustness` skill with agent variants and robustness cards, `renderings` skill and `/render` workflow for Markdown-to-HTML/PDF, Devin agent rule split (`devin-cascade.md` / `devin-devin.md`) with tool-call payload limits (`PRMT-HS-11`), and rebranding to "Insanely Productive Prompt System" (IPPS).

## Changes Since v4.4

### New Skills (4)

- **analysis-methods** - Pattern detection, hypothesis generation, evidence validation, and synthesis (`ANALYSIS_GUIDES.md`, `ANALYSIS_RULES.md`, `ANALYSIS_CHECKS.md`, `INVESTIGATION_*`, templates)
- **llm-tools** - Single source of truth consolidating `llm-evaluation`, `llm-transcription`, and `llm-computer-use` into one skill with shared scripts (`call-llm.py`, `call-llm-batch.py`, `find-workers-limit.py`), canonical model registry JSONs (`1.12.0`), and `MODEL_INVENTORY.md`
- **renderings** - Markdown-to-HTML and PDF rendering via headless Chromium (`render.py`, single-language and multilingual parallel-column HTML templates)
- **terminal-robustness** - Prevention of hanging terminal commands in chat and prompt sequences, with `ClaudeCode/` and `DevinCascade/` variant subfolders and `ROBUSTNESS_CARD_TEMPLATE.md`

### Consolidated / Removed Skills (3 → 1)

- **llm-evaluation**, **llm-transcription**, **llm-computer-use** - Merged into `llm-tools` (`evaluation/`, `transcription/`, `computer-use/` subfolders)

### New Workflows (15)

- **analyze** - Qualitative coding, pattern detection, hypothesis generation, and evidence validation into a single Analysis INFO deliverable
- **draft-article**, **draft-ebook**, **draft-report** - Draft working structure, section/chapter goals, evidence placement, and style sheet
- **hypothesize** - Formulate falsifiable competing working hypotheses with rivals, falsifiers, and crucial test plans into a Hypothesis Register deliverable
- **pattern-detect** - Code findings, detect themes, catalog contradictions, evaluate assumptions, and identify research gaps into a Pattern Map deliverable
- **propose-article**, **propose-ebook**, **propose-report** - Propose outline candidates with scoring, recommendation, and optional sample bake-off (replaces `propose-minto`)
- **render** - Render Markdown files to HTML and PDF
- **research-program** - Execute a multi-approach tier-3 research program with session STRUT, approach prompt sequences, and cross-approach synthesis
- **validate** - Weight evidence, compile ACH audit trail, log disconfirmation, and rank hypotheses into a Validation Report deliverable
- **write-article**, **write-ebook**, **write-report** - Author finished publication deliverables with line pass, copy pass, and release check (replaces `write-minto`)

### Deprecated / Replaced Workflows (2)

- **propose-minto** → Replaced by `/propose-article using MINTO`
- **write-minto** → Replaced by `/write-article using MINTO`

### Research-to-Writing Toolchain & Write-Documents Expansion

- **Document types**: `ARTICLE_*`, `REPORT_*`, `EBOOK_*` guides, rules, checks, and templates
- **Writing techniques (`writing_techniques/`)**: `MINTO`, `IMINTO`, `ABTSTORY`, `KABOB`, `STA`, `PAS`, `AIDA`, `DIATAXIS`, `IMRAD` guides, rules, checks, and templates
- **Writing personas (`writing_personas/`)**: `CARMAK`, `FEYNMAN`, `GRAHAM`, `KAHNEMAN`, `LAMPORT`, `levine`, `LUU`, `McKINSEY`, `ORWELL`, `PINKER`, `SERNOVITZ`, `STRUNK`, `THOMPSON`, `TUFTE`, `ZINSSER` style sheets plus `TRAITS_CORE.md`
- **Deliverable Doc IDs**: `[TOPIC]-[ID]-OPTIONS-[NN]`, `[TOPIC]-[ID]-DRAFT-[NN]`, `[TOPIC]-[TYPE]-[NN]` in `promptsystem-ids.md`
- **AMINTON & MECT updates**: Corrected AMINTON expansion, added `MW-WC-09` acronym-from-context rule and `MW-WC-10` international English rule, prose table exemption in `core-conventions.md`

### Prompt Sequence & Agent Robustness

- **Devin agent rule split**: Replaced `devin.md` with `devin-cascade.md` (Windsurf/Devin IDE Cascade chat agent, including 6,000-char tool-call payload limit and JSON serialization workarounds) and `devin-devin.md` (Devin CLI / Devin Desktop); updated `_PROMPTS_UpdateClaude.md`
- **Prompt sequence rules (`write-prompts`)**:
  - `PRMT-SC-04` - Up to 10 implementation prompts per file (checkpoints excluded)
  - `PRMT-SC-07` - Load-based workflow partitioning rule
  - `PRMT-SC-08` - Session anchor with absolute paths to prevent parallel session spill
  - `PRMT-NM-04` - Domain prefix in prompt filenames for uniqueness across session
  - `PRMT-HS-11` - Agent tool limits copied verbatim into robustness card `## Agent tool limits`
- **Agent behavior (`agent-behavior.md`)**: Added `Presenting Decisions` format (Problem, Context, Options with What/Why/Implication, single recommendation), `_agentwork/` operational artifact folder rules, and `Large File Writes` section

### Model Registry & Capability Depth Ladder

- **Depth ladder (`MDLRGUP-MDLINVNTRY-SP01`)**: Append-only ordinal depth ladder (`D1` to `D12`) with evidence kinds `E1`-`E6` and measured `Items` axis, replacing year-letter labels
- **Registry `1.12.0`**: Added xAI/Grok provider integration across all 5 `llm-tools` Python scripts, updated OpenAI, Anthropic, Google Gemini, xAI, and Z.AI models and pricing (`2026-10-28` and `2026-11-02` PRICES runs)
- **Tooling**: Added `layer-depth-ladder.py`, `test-layer-depth-ladder.py`, `format-model-registry.py`, `match-epoch-eci.py`, `update-model-inventory.py`, and `verify-and-distribute-registry.ps1`

### Workspace Management & Cleanup

- **`sync.ps1` fixes**: Resolved timezone comparison bug, excluded `SKIP` results from pending-change detection, added hygiene exclusions, and introduced `summary-sync.ps1`
- **`/cleanup` enhancements**: Added prompt-system stripping mode for publishing, `to [newfile]` output option, and code fence protection
- **Unicode & encoding rules**: Added `UNICODE_RULES.md` in `coding-conventions` and UTF-8 with BOM fix for audio transcripts

### Specs & INFO Documentation

- `specs/_SPEC_TERMINAL_ROBUSTNESS_SKILL.md` - Terminal robustness skill specification
- `Docs/_INFO_IPPS_AGEN_WORKFLOW_SYNTAX.md` (`AGENSYNTAX-IN03`) - AGEN workflow syntax Concept A verb sentences and platform command conflict analysis
- `Docs/_INFO_HOW_TO_CONTROL_WRITING_STYLE_WITH_PARAMETERS_AND_TRAITS.md` - Writing style control parameters and traits
- `Docs/_INFO_DEVIN_QUOTA_CONCUMPTION_INCREASE_WITH_OPUS_MODELS.md.md` - Devin quota consumption analysis
- Updated `Docs/_INFO_HOW_DEVIN_WORKS.md`, `Docs/_INFO_AGENTIC_PROBLEMS.md`, `Docs/_INFO_HOW_TO_USE_IPPS_WITH_CLAUDE_CODE.md`, and `README.md`

## Statistics

- **Commits since v4.4**: 42
- **Files changed**: 1122
- **Lines added**: 109817
- **Lines deleted**: 3432
- **New skills**: 4 (`analysis-methods`, `llm-tools`, `renderings`, `terminal-robustness`)
- **Consolidated skills**: 3 → 1 (`llm-evaluation`, `llm-transcription`, `llm-computer-use` → `llm-tools`)
- **New workflows**: 15 (`analyze`, `draft-article`, `draft-ebook`, `draft-report`, `hypothesize`, `pattern-detect`, `propose-article`, `propose-ebook`, `propose-report`, `render`, `research-program`, `validate`, `write-article`, `write-ebook`, `write-report`)
- **Replaced workflows**: 2 (`propose-minto`, `write-minto`)
- **Total active workflows**: 62 (0 broken references verified via `check_workflow_refs.ps1`)
- **Total active skills**: 25
- **Date range**: 2026-09-23 to 2026-11-03
