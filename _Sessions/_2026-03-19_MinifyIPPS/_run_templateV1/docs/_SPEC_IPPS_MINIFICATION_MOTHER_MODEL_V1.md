# SPEC: MinifyIPPS Compression Pipeline

**Doc ID**: MIPPS-SP01
**Goal**: Specify a pipeline that compresses the ~1MB DevSystem into a smaller version usable by cheaper LLMs, using Mother model (Claude Opus 4.6 1M context) for all compression with full cross-file awareness
**Timeline**: Created 2026-03-19, Updated 10 times (last: 2026-03-20)
**Target file**: `mipps_pipeline.py` (orchestrator script)

**Depends on:**
- `_OPTION_B_MOTHER_COMPRESSES_ALL.md [MIPPS-OPT-B]` for architecture decisions
- `_OPTION_ABCD_COMPARISON.md [MIPPS-COMP-01]` for option selection rationale
- `NOTES.md [2026-03-19_MinifyIPPS-NOTES]` for original 7-step process

**Does not depend on:**
- `_OPTION_A_PIPELINE_WITH_PROMPTS.md [MIPPS-OPT-A]` (rejected: no cross-file awareness)
- `_OPTION_C_DEPENDENCY_ORDERED.md [MIPPS-OPT-C]` (rejected: over-engineered, 2x cost for marginal gain)
- `_OPTION_D_TEST_DRIVEN.md [MIPPS-OPT-D]` (deferred: requires test case design)

## MUST-NOT-FORGET

- Mother model compresses ALL .md files - no delegation to cheaper Transformers
- File exclusion: .md files < 100 lines AND rarely loaded -> copy as-is, do not compress
- Only .md files are compressed; all other files (.py, .json, .ps1, .png, etc.) are copied as-is to output
- Excluded from output: __pycache__ folders and contents only
- Source directory is configurable via `source_dir` in pipeline_config.json (default: `.windsurf/`)
- Cost estimates are +/-50% due to estimated thinking tokens
- Verification model judges EVERY compressed file - no self-evaluation by Mother
- Step 7 report format: exactly 5 lines per file (structural, removed, simplified, sacrificed, impact)
- Target: reduce total token count by >= 40%, max 5 files in manual review queue
- Anthropic cache TTL is 5 minutes (ephemeral). For 75 sequential calls (~38 min), cache will expire multiple times. Monitor `cache_read_input_tokens == 0` on non-first calls to detect expiration and log cost impact (IG-05)

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Design Decisions](#5-design-decisions)
6. [Implementation Guarantees](#6-implementation-guarantees)
7. [Key Mechanisms](#7-key-mechanisms)
8. [Action Flow](#8-action-flow)
9. [Data Structures](#9-data-structures)
10. [Implementation Details](#10-implementation-details)
11. [Document History](#11-document-history)

## 1. Scenario

**Problem:** The IPPS DevSystem (~1MB, ~104 files) exceeds what cheaper LLMs can process effectively. Rules, workflows, and skills loaded into context consume ~300K tokens, leaving little room for actual task work. Cheaper models (GPT-5-mini, Claude Haiku 4.5) cannot follow the full instruction set reliably.

**Solution:**
- Use Claude Opus 4.6 (1M context) as "Mother" model to analyze and compress all files
- Mother sees the entire system while compressing each file, preserving cross-file references
- Verification model (GPT-5-mini) independently judges each compression
- Iterative refinement: Mother reviews verification report, re-compresses failed files
- Pipeline script orchestrates the process with subcommands per step

**What we don't want:**
- Independent per-file compression without cross-file awareness (Option A failure mode)
- Complex layer management with cascade failure risk (Option C over-engineering)
- Compression that breaks cross-file references (concept X dropped in file A but still referenced in file B)
- Manual compression - must be automated and repeatable
- Mother evaluating its own output (independence requirement)
- Compression of Python scripts or JSON configs (copy as-is)
- Compressing files that are already small and rarely used

## 2. Context

This pipeline is part of the IPPS (Intelligent Prompt and Pipeline System) project. The DevSystem is a set of rules, workflows, and skills that guide AI agents (primarily in Windsurf IDE). The system has grown to ~1MB, making it expensive to load into context for every interaction.

The compressed output will be deployed as a drop-in replacement for the full DevSystem in `.windsurf/` folders of repositories where cheaper LLMs are used.

**Selected approach**: Option B (Mother-Compresses-All) was chosen over:
- Option A (cheap pipeline): insufficient quality without cross-file awareness
- Option C (dependency-ordered): 2x cost of B for marginal quality gain
- Option D (test-driven): deferred, requires test case design first

## 3. Domain Objects

### Bundle

A **Bundle** is the concatenated content of all source files, used as cached context for Mother.

- **Storage**: `context/all_files_bundle.md`
- **Size**: ~300K tokens (~1MB text)
- **Lifetime**: Created once in Step 1, reused for all subsequent Mother calls via prompt caching

### FileInventory

A **FileInventory** categorizes all source files by type and compressibility.

- **Source**: `.windsurf/` directory
- **Categories**:
  - `rules` - 8 md files (always compressible)
  - `workflows` - 36 md files (compressible unless excluded)
  - `skill_docs` - 24 md files (compressible unless excluded)
  - `skill_prompts` - 7 md files (compressible unless excluded)
- **Total**: ~75 .md files (compressible)
- **Non-.md files**: All copied to output as-is (scripts, configs, images, etc.)
- **Excluded from output**: __pycache__ folders only

### ExclusionCriteria

An **ExclusionCriteria** defines which compressible files should be skipped.

- **Rule**: file has < 100 lines AND is referenced by <= 2 other files (per call tree analysis in Step 2)
- **Threshold**: `exclusion_max_lines: 100`, `exclusion_max_references: 2` in pipeline_config.json
- **Effect**: file is copied as-is to output, not sent to Mother for compression
- **Expected reduction**: ~20-30% fewer files to compress (~50-55 files instead of 75)

### NeverCompress

A **NeverCompress** list defines paths that are always copied as-is, regardless of size or reference count.

- **Config**: `never_compress` array in pipeline_config.json
- **Format**: glob patterns relative to source_dir (e.g., `skills/llm-evaluation/prompts/*`)
- **Use case**: specialized prompts, templates, or content where compression would break functionality
- **Bundle**: included in all_files_bundle.md (Mother sees full context), but NOT sent to Mother for compression
- **Evaluation order**: `skip_patterns` (exclude entirely) -> `never_compress` (copy as-is) -> ExclusionCriteria (copy as-is) -> compress
- **Overlap rule**: file matching both `skip_patterns` AND `never_compress` is excluded entirely (`skip_patterns` wins per evaluation order)
- **Distinction from skip_patterns**: `skip_patterns` excludes from output entirely; `never_compress` copies to output as-is

### CompressionStrategy

A **CompressionStrategy** classifies every concept, rule, and feature across the system.

- **Storage**: `_03_FILE_COMPRESSION_STRATEGY.md`
- **Lists**:
  - `Primary` - leave mostly as-is (core function, critical rules)
  - `Secondary` - compress (reduce formatting, merge sections, simplify examples)
  - `Drop` - remove entirely (rarely used features, redundant content)

### PipelineState

A **PipelineState** tracks progress across pipeline steps.

- **Storage**: `pipeline_state.json`
- **Fields**:
  - `current_step` - last completed step number
  - `files_compressed` - count of files processed in Step 6
  - `files_passed` - count passing verification threshold
  - `files_failed` - count below threshold, needing refinement
  - `files_excluded_md` - count of excluded .md files (copied as-is, includes never_compress + ExclusionCriteria)
  - `_never_compress_files` - list of file paths matching never_compress patterns
  - `_excluded_files` - list of file paths matching ExclusionCriteria (excludes never_compress files)
  - `iteration` - current iteration number (1 = first pass)
  - `total_cost` - accumulated API cost in USD

### CompressedFile

A **CompressedFile** is the output of Mother's compression for a single source file.

- **Storage**: `output/[category]/[filename]`
- **Properties**:
  - `source_path` - original file path relative to `.windsurf/`
  - `file_type` - category from FileInventory
  - `compression_ratio` - output tokens / input tokens
  - `judge_score` - verification score 1-5
  - `iteration` - which iteration produced this version

## 4. Functional Requirements

**MIPPS-FR-01: Bundle Generation**
- Read all .md files from `.windsurf/` directory recursively
- Concatenate into single `context/all_files_bundle.md` with file path headers
- Include file metadata: path, line count, token estimate
- Skip files matching `skip_patterns` (__pycache__/*)
- Non-.md files are not included in bundle (not needed for Mother's compression context)

**MIPPS-FR-02: Call Tree Analysis (Step 2)**
- Mother analyzes bundle to produce `_01_FILE_CALL_TREE.md`
- Document: startup sequence, per-workflow call trees, per-skill call trees, file reference list
- Output identifies which files trigger loading of other files
- Output identifies load frequency per file (used for exclusion criteria)

**MIPPS-FR-03: Complexity Map (Step 3)**
- Mother produces `_02_FILE_COMPLEXITY_MAP.md`
- Per file: token count, concept count, rule count, step count, branching count
- Exhaustive concept list across entire system
- Flag files matching exclusion criteria (< 100 lines AND rarely loaded)

**MIPPS-FR-04: Compression Strategy (Step 4)**
- Mother produces `_03_FILE_COMPRESSION_STRATEGY.md`
- Three classification lists: Primary, Secondary, Drop
- Per-file compression guidance referencing call tree and complexity data
- Exclude files matching exclusion criteria from compression scope
- Excluded files are immutable context: compressed files must preserve all references to/from excluded files

**MIPPS-FR-05: Compression Prompt Generation (Step 5)**
- Mother generates 6 type-specific compression prompts in `prompts/transform/` (one per file type in `file_type_map`)
- Mother generates matching evaluation prompts in `prompts/eval/`
- Compression prompts reference the strategy's Primary/Secondary/Drop classifications
- Types: `compress_rules`, `compress_workflows`, `compress_skill_docs`, `compress_skill_prompts`, `compress_templates`
- Fallback: files not matching any `file_type_map` pattern use `compress_other` (generic compression prompt)

**MIPPS-FR-06: Compression Execution (Step 6)**
- For each compressible, non-excluded file: Mother compresses with full cached context
- Mother receives: file content + file type compression prompt + strategy excerpt for this file
- Verification model judges each output against eval/ criteria, scores 1-5
- Files scoring < 3.5: Mother refines with judge feedback, re-judges
- Files scoring < 3.5 after refinement: append to `_05_MANUAL_REVIEW_QUEUE.md` with source path, scores, and judge feedback
- Save best version to `output/[category]/[filename]`

**MIPPS-FR-07: Verification Report (Step 7)**
- Verification model produces `_04_FILE_COMPRESSION_REPORT.md`
- Per file, exactly 5 lines: structural changes, removed features, simplified content, sacrificed details, possible impact
- Cross-file reference check: verify all references in compressed files resolve to existing concepts in other compressed or excluded files
- Summary section: pass rate, total compression ratio, broken references count, files needing attention

**MIPPS-FR-08: Iteration**
- Mother reviews `_04_FILE_COMPRESSION_REPORT.md` with cached context
- Updates `_03_FILE_COMPRESSION_STRATEGY.md` based on findings
- Re-compresses only files flagged in report
- Re-runs verification for changed files only

**MIPPS-FR-09: Non-.md File Handling**
- All non-.md files (.py, .json, .ps1, .png, .jpg, .txt, etc.) are copied to `output/` as-is, preserving directory structure
- Files matching `never_compress` .md patterns are copied to `output/` as-is (specialized prompts, templates)
- Excluded .md files (< 100 lines AND rarely loaded) are copied to `output/` as-is
- Files/folders matching `skip_patterns` (__pycache__/*) are NOT copied to output
- Evaluation order for .md files: `skip_patterns` (exclude) → `never_compress` (copy as-is) → ExclusionCriteria (copy as-is) → compress
- Rationale: Output is a complete drop-in replacement for source directory, with only .md files compressed

**MIPPS-FR-10: Pipeline State Tracking**
- Track progress in `pipeline_state.json` after each step
- Track accumulated cost per model
- Track per-file completion within Step 6 via `files_completed` list (enables resume from last file, not step restart)
- Allow resuming from any step if pipeline is interrupted

**MIPPS-FR-11: Verification of Mother Outputs (Steps 2-4)**
- `check` command: Verification model spot-checks Mother analysis documents
- Compare claims against source files (10-20 random file checks per document)
- Report issues (missing files, wrong counts, incorrect call chains)
- Feed issues back to Mother for correction before proceeding

## 5. Design Decisions

**MIPPS-DD-01:** Mother compresses all files, no delegation to cheaper models. Rationale: cross-file awareness is the primary quality requirement; only a model with full system context can guarantee reference integrity.

**MIPPS-DD-02:** Verification model is independent from Mother. Rationale: self-evaluation is unreliable; GPT-5-mini provides cheap, independent judgment.

**MIPPS-DD-03:** Single compressed version per file (no ensemble). Rationale: Mother with full context produces higher quality than multiple cheap candidates. Ensemble adds cost without proportional quality gain when the compressor already has full context.

**MIPPS-DD-04:** Sequential compression, not parallel. Rationale: all Mother calls share the same cached context; parallelism would require multiple cache instances at higher cost.

**MIPPS-DD-05:** Exclusion criteria applied after Step 2 (call tree). Rationale: load frequency data needed to determine "rarely loaded". Cannot exclude before analysis.

**MIPPS-DD-06:** Judge threshold is 3.5/5.0. Rationale: below 3.5 indicates significant quality issues. One refinement attempt; if still below, flag for manual review rather than infinite retry.

**MIPPS-DD-07:** Source directory is configurable via `source_dir` config. Default `.windsurf/` (active deployed system). Rationale: allows minifying any DevSystem version, not just the active one.

**MIPPS-DD-08:** Cost tracking per API call. Rationale: thinking token costs are estimated at +/-50%. Actual cost tracking enables budget monitoring and early termination if costs exceed 2x estimate.

**MIPPS-DD-09:** Verification model cannot validate behavioral correctness. Rationale: GPT-5-mini can judge structural preservation but lacks domain knowledge to verify that compressed rules produce correct agent behavior. This is a known limitation; functional testing (Option D) addresses it and is planned as future work.

**MIPPS-DD-10:** Verification uses OpenAI Chat Completions API, not Responses API. Rationale: OpenAI recommends Responses API for new projects (per OAIAPI-IN05), but verification calls are stateless single-turn requests with no need for conversation state, tools, or background processing. Chat Completions is simpler and sufficient.

**MIPPS-DD-11:** V1 uses unversioned model IDs (`gpt-5-mini`, `claude-opus-4-6`). Rationale: OpenAI recommends pinned model versions for production (per OAIAPI-IN04/IN61), but V1 is an experimental pipeline. Model pinning deferred to V2 when output quality baselines are established.

## 6. Implementation Guarantees

**MIPPS-IG-01:** Every compressed file is independently verified by a model that did not perform the compression.

**MIPPS-IG-02:** No source file is modified. All output goes to `output/` directory.

**MIPPS-IG-03:** Pipeline can be interrupted and resumed from last completed step without data loss.

**MIPPS-IG-04:** Non-compressible files appear in output with identical content to source.

**MIPPS-IG-05:** Bundle is re-sent with every Mother call (Anthropic caches automatically). If cache expires (5-min TTL), the next call triggers cache write at ~1.25x input cost. Pipeline must detect expiration via `cache_read_input_tokens == 0` on non-first calls and log cost impact.

**MIPPS-IG-06:** Total cost never exceeds 2x the estimated budget without explicit user confirmation.

**MIPPS-IG-07:** Files matching exclusion criteria are never sent to Mother for compression.

## 7. Key Mechanisms

### Prompt Caching

Mother's ~300K token bundle is sent as system prompt content with `cache_control: {"type": "ephemeral"}`. First call pays cache write cost (higher than standard input). Subsequent calls within TTL hit cache read at ~0.1x base input price. See NOTES.md Anthropic Pricing Reference for exact per-model rates.

**Cost structure per cached bundle call:**
- **Cache write** (first or post-expiry call): ~1.25x input price
- **Cache read** (subsequent calls within 5-min TTL): ~0.1x input price
- **Breakeven**: After ~2 cache reads, caching saves money vs re-sending full bundle each time

**V1 TTL**: 5 minutes (Anthropic ephemeral cache). For 75 sequential calls at ~30s each (~38 min total), cache will expire ~7 times. Each expiration triggers a cache write (~1.25x input price for ~300K tokens). Budget must account for ~8 cache writes instead of 1.

**Cache monitoring (MIPPS-IG-05):**
- After each Mother call, check `cache_read_input_tokens` in usage response
- On non-first calls: `cache_read_input_tokens == 0` indicates cache expired -> log warning with cost impact
- Track cache miss count in state for cost reporting
- No re-warming action needed: bundle is re-sent every call by design (Anthropic caches automatically)

### Compression-then-Verify Loop

```
For each file:
├─> Mother compresses (cached context + compression prompt + strategy)
├─> Verification judges (score 1-5)
│   ├─> score >= 3.5: accept, save to output/
│   └─> score < 3.5: Mother refines with feedback
│       ├─> Re-judge
│       │   ├─> score >= 3.5: accept
│       │   └─> score < 3.5: flag for manual review
```

### File Type Mapping

Defined in `pipeline_config.json`, maps glob patterns to compression prompt files:

- `rules/*.md` -> `compress_rules`
- `workflows/*.md` -> `compress_workflows`
- `skills/*/SKILL.md` -> `compress_skill_docs`
- `skills/*/SETUP.md`, `UNINSTALL.md` -> `compress_skill_docs`
- `skills/*/*_RULES.md` -> `compress_rules`
- `skills/*/prompts/*.md` -> `compress_skill_prompts`
- `skills/*/*_TEMPLATE.md` -> `compress_templates`

### Cost Budget Guard

Pipeline tracks actual costs per API call. If accumulated cost exceeds `max_budget` (default: 2x estimated total), pipeline pauses and prompts for user confirmation before continuing.

## 8. Action Flow

### Full Pipeline Run

```
User runs: mipps_pipeline.py bundle --source-dir .windsurf/
├─> Scan source directory, categorize files
├─> Concatenate compressible + non-compressible file contents
├─> Write context/all_files_bundle.md
└─> Update pipeline_state.json (step: 1)

User runs: mipps_pipeline.py analyze --steps 2-4
├─> Step 2: Mother call (bundle as cached input)
│   ├─> Produce _01_FILE_CALL_TREE.md
│   └─> Update state (step: 2)
├─> Step 3: Mother call (cached)
│   ├─> Produce _02_FILE_COMPLEXITY_MAP.md
│   ├─> Identify files matching exclusion criteria
│   └─> Update state (step: 3)
└─> Step 4: Mother call (cached)
    ├─> Produce _03_FILE_COMPRESSION_STRATEGY.md
    ├─> Exclude flagged files from compression scope
    └─> Update state (step: 4)

User runs: mipps_pipeline.py check --step 2|3|4
├─> Verification model spot-checks Mother output
├─> Report issues
└─> If issues found: feed back to Mother, re-produce document

User runs: mipps_pipeline.py generate --step 5
├─> Mother generates type-specific compression prompts
├─> Write prompts/transform/*.md and prompts/eval/*.md
└─> Update state (step: 5)

User runs: mipps_pipeline.py compress --step 6
├─> For each non-excluded compressible file:
│   ├─> Mother compresses (cached context)
│   ├─> Verification judges (score 1-5)
│   ├─> If score < 3.5: Mother refines, re-judge
│   ├─> Save to output/
│   └─> Update state (files_compressed++)
├─> Copy never_compress .md files to output/ as-is (specialized prompts)
├─> Copy excluded .md files to output/ as-is (small + rarely loaded)
├─> Non-.md files are NOT copied (scripts/configs excluded)
└─> Update state (step: 6)

User runs: mipps_pipeline.py verify --step 7
├─> Verification model compares each original vs compressed
├─> Produce _04_FILE_COMPRESSION_REPORT.md
└─> Update state (step: 7)

User runs: mipps_pipeline.py iterate --update-strategy
├─> Mother reviews report (cached context)
├─> Updates _03_FILE_COMPRESSION_STRATEGY.md
├─> Re-compresses only flagged files
├─> Re-runs verification for changed files
└─> Update state (iteration++)
```

## 9. Data Structures

### pipeline_config.json

```json
{
  "source_dir": ".windsurf/",
  "output_dir": "output/",
  "models": {
    "mother": {"provider": "anthropic", "model": "claude-opus-4-6", "max_context": 1000000, "thinking": true},
    "verification": {"provider": "openai", "model": "gpt-5-mini", "max_context": 128000}
  },
  "thresholds": {
    "judge_min_score": 3.5,
    "max_refinement_attempts": 1,
    "exclusion_max_lines": 100,
    "exclusion_max_references": 2,
    "target_compression_percent": 40,
    "max_manual_review_files": 5
  },
  "cache": {
    "ttl": "1h"
  },
  "budget": {
    "max_total_usd": 100.0,
    "warn_at_percent": 80
  },
  "file_type_map": {
    "rules/*.md": "compress_rules",
    "workflows/*.md": "compress_workflows",
    "skills/*/SKILL.md": "compress_skill_docs",
    "skills/*/SETUP.md": "compress_skill_docs",
    "skills/*/UNINSTALL.md": "compress_skill_docs",
    "skills/*/*_RULES.md": "compress_rules",
    "skills/*/prompts/*.md": "compress_skill_prompts",
    "skills/*/*_TEMPLATE.md": "compress_templates",
    "*": "compress_other"
  },
  "include_patterns": ["*.md"],
  "skip_patterns": ["__pycache__/*", "**/__pycache__/*"],
  "never_compress": [
    "skills/llm-evaluation/prompts/*",
    "skills/llm-transcription/prompts/*",
    "skills/deep-research/prompts/*"
  ],
  "api_timeout_seconds": 120
}
```

### pipeline_state.json

```json
{
  "current_step": 6,
  "iteration": 1,
  "files_total": 104,
  "files_compressible": 75,
  "files_excluded": 20,
  "files_compressed": 55,
  "files_passed": 48,
  "files_failed": 7,
  "files_excluded_md": 20,
  "files_completed": ["rules/core-conventions.md", "rules/devsystem-core.md"],
  "broken_references": 0,
  "cost": {
    "mother_input": 2.45,
    "mother_output": 38.20,
    "verification_input": 0.12,
    "verification_output": 0.08,
    "total": 40.85
  }
}
```

### Step 7 Report Entry Format

```
### [relative/path/to/file.md]
1. **Structural changes**: [what sections merged, reordered, flattened]
2. **Removed features**: [what was dropped entirely]
3. **Simplified content**: [what was reduced but kept]
4. **Sacrificed details**: [examples, edge cases, formatting removed]
5. **Possible impact**: [what agent behavior may change]
```

## 10. Implementation Details

### Script Architecture

`mipps_pipeline.py` uses subcommand pattern via `argparse` for the Command-Line Interface (CLI):

```python
def main():
    parser = argparse.ArgumentParser(description="MinifyIPPS Compression Pipeline")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommands
    sub_bundle = subparsers.add_parser("bundle")     # Step 1
    sub_analyze = subparsers.add_parser("analyze")    # Steps 2-4
    sub_check = subparsers.add_parser("check")        # Verify Mother output
    sub_generate = subparsers.add_parser("generate")  # Step 5
    sub_compress = subparsers.add_parser("compress")   # Step 6
    sub_verify = subparsers.add_parser("verify")       # Step 7
    sub_iterate = subparsers.add_parser("iterate")     # Review + re-compress
    sub_status = subparsers.add_parser("status")       # Show state
```

### Module Structure

```
mipps_pipeline.py                      (entry point, CLI)
├─> lib/
│   ├─> file_bundle_builder.py         (Step 1: file scanning, concatenation)
│   ├─> mother_analyzer.py             (Steps 2-4: Mother analysis calls)
│   ├─> mother_output_checker.py       (Verification spot-checks)
│   ├─> compression_prompt_builder.py  (Step 5: compression prompt generation)
│   ├─> file_compressor.py             (Step 6: compression + judge loop)
│   ├─> compression_report_builder.py  (Step 7: report generation)
│   ├─> compression_refiner.py         (Iteration: review + re-compress)
│   ├─> llm_clients.py                 (API calls: Anthropic + OpenAI)
│   ├─> api_cost_tracker.py            (Per-call cost tracking, budget guard)
│   └─> pipeline_state.py              (pipeline_state.json read/write)
```

### API Client Requirements

- Anthropic SDK for Mother (Claude Opus 4.6) with extended thinking via `thinking: {"type": "enabled", "budget_tokens": N}` (thinking tokens billed as output)
- OpenAI SDK for Verification (GPT-5-mini) via Chat Completions API (`client.chat.completions.create`)
- Prompt caching via `cache_control: {"type": "ephemeral"}` on system prompt content block (5-min TTL)
- Both SDKs have built-in retry with `max_retries` parameter; configure to avoid double-retry with custom backoff
- OpenAI SDK: `OpenAI(timeout=T, max_retries=N)` reads `OPENAI_API_KEY` env var
- Anthropic SDK: `Anthropic(timeout=T, max_retries=N)` reads `ANTHROPIC_API_KEY` env var
- Log API responses to stdout (include `x-request-id` from OpenAI responses for debugging)
- OpenAI usage response uses `prompt_tokens`/`completion_tokens`; Anthropic uses `input_tokens`/`output_tokens` - cost_tracker must map both

### Dependencies

- `anthropic` (Anthropic Python SDK)
- `openai` (OpenAI Python SDK)
- `tiktoken` (approximate token counting; OpenAI tokenizer, ~10% variance for Anthropic models)
- `pathlib`, `json`, `argparse`, `datetime` (stdlib)

## 11. Document History

**[2026-03-20 14:06]**
- Changed: All non-.md files now copied to output as-is (was: excluded from output)
- Changed: Only __pycache__ folders excluded from output (was: all non-.md excluded)
- Changed: FR-09 renamed from "Excluded File Handling" to "Non-.md File Handling"
- Changed: FR-01 clarified that only .md files included in bundle
- Changed: skip_patterns updated to __pycache__ only (was: pricing-sources, scripts, configs)
- Changed: MNF updated to reflect complete drop-in replacement output
- Rationale: Output must be complete replacement of source directory for deployment

**[2026-03-20 10:30]**
- Fixed: Cache TTL corrected from "1-hour" to "5 minutes" (Anthropic ephemeral cache reality)
- Fixed: IG-05 rewritten with concrete cache monitoring mechanism (`cache_read_input_tokens == 0`)
- Fixed: Prompt Caching section rewritten for 5-min TTL with cache miss budget (~8 writes)
- Fixed: MNF cache entry updated with expiration risk and monitoring requirement
- Fixed: NeverCompress domain object: added bundle inclusion, skip_patterns overlap rule
- Fixed: PipelineState: added `_never_compress_files`, `_excluded_files`; removed `cache_last_used` (unimplemented)
- Fixed: Action Flow compress step: added never_compress copy line
- Fixed: Document History reordered to reverse chronological

**[2026-03-20 09:57]**
- Added: NeverCompress domain object for specialized prompts that must not be compressed
- Added: `never_compress` config array to pipeline_config.json (glob patterns)
- Changed: FR-09 updated with evaluation order: skip_patterns -> never_compress -> ExclusionCriteria -> compress
- Added: Default never_compress patterns for llm-evaluation, llm-transcription, deep-research prompts

**[2026-03-20 04:30]**
- Fixed: API logging simplified from `logs/` directory to stdout for V1 (no IMPL IS existed for logs/)

**[2026-03-20 04:05]**
- Added: Timeline field (required per /verify workflow)
- Fixed: TTL expanded to "Time To Live (TTL)" in MNF (AP-PR-06)
- Fixed: CLI format corrected to "Command-Line Interface (CLI)" (AP-PR-06)

**[2026-03-20 03:55]**
- Changed: Module names made more descriptive per MC-PR-03 (no meta-words without qualifier), synced with IMPL

**[2026-03-20 03:30]**
- Added: MIPPS-DD-10 documenting Chat Completions API choice over Responses API for verification (per OAIAPI-IN05)
- Added: MIPPS-DD-11 documenting V1 unversioned model IDs, pinning deferred to V2 (per OAIAPI-IN04/IN61)
- Added: OpenAI SDK configuration details (`timeout`, `max_retries`, `OPENAI_API_KEY` env var) to API Client Requirements
- Added: Both SDKs built-in retry note (was Anthropic-only, now covers OpenAI SDK per OAIAPI-IN62)
- Added: `x-request-id` logging for OpenAI responses (per OAIAPI-IN03/IN61)
- Added: Provider-specific usage field mapping note (`prompt_tokens`/`completion_tokens` vs `input_tokens`/`output_tokens`)

**[2026-03-20 02:35]**
- Fixed: MNF contradictory TTL (removed "5 minutes" line, kept "1-hour for V1")
- Fixed: DD-02 AP-NM-01 synonym "compression model" replaced with "Mother"
- Fixed: Prompt Caching section rewritten with correct `cache_control` API parameter, cache write/read cost structure, breakeven analysis (per Anthropic API IN18)
- Fixed: Model ID `claude-opus-4-6-thinking` replaced with `claude-opus-4-6` + `"thinking": true` config (thinking enabled via parameter, not model name per IN13)
- Fixed: "Anthropic Software Development Kit (SDK)" simplified to "Anthropic SDK"
- Fixed: Removed `cache_manager.py` from module structure (unnecessary with 1h TTL, cache control handled in llm_clients.py)
- Added: `files_excluded_md` field to PipelineState domain object (was in state JSON but undocumented)
- Added: `api_timeout_seconds: 120` to pipeline_config.json (synced from IMPL)
- Added: Extended thinking parameter documentation in API Client Requirements
- Added: SDK built-in retry note to avoid double-retry
- Added: tiktoken accuracy note (~10% variance for Anthropic models)

**[2026-03-20 00:56]**
- Changed: Source directory now configurable via `source_dir` (not hardcoded)
- Changed: DD-07 updated to reflect configurable source

**[2026-03-20 00:55]**
- Changed: Only .md files are minified; non-.md files (*.py, *.json) excluded from output entirely
- Changed: FR-09 updated to reflect .md-only output
- Changed: FileInventory simplified to .md files only
- Changed: pipeline_config.json uses `include_patterns: ["*.md"]` instead of `skip_patterns` for non-.md

**[2026-03-20 00:52]**
- Added: MIPPS-DD-09 acknowledging verification model limitation (behavioral correctness)
- Added: Success criteria to MNF (>= 40% compression, max 5 manual review files)
- Added: 1-hour cache TTL recommendation (eliminates cache warming complexity)
- Added: Quantitative exclusion threshold (`exclusion_max_references: 2`)
- Added: Cross-file reference verification to FR-07
- Added: Per-file completion tracking (`files_completed`) to FR-10 and state.json
- Added: Excluded file reference preservation rule to FR-04
- Added: `compress_other` fallback to file_type_map
- Added: `broken_references` to pipeline_state.json
- Changed: Cache mechanism simplified (TTL options, removed warming strategy)

**[2026-03-20 00:35]**
- Fixed: AP-NM-01 "guidelines" vs "compression prompts" synonym (6 occurrences)
- Fixed: AP-PR-06 expanded TTL, CLI, SDK on first use
- Fixed: AP-PR-07 "up to 10" changed to exact "6" types
- Added: Manual review mechanism (MIPPS-FR-06) writes to `_05_MANUAL_REVIEW_QUEUE.md`
- Added: skip_patterns detail in MIPPS-FR-01

**[2026-03-19 23:45]**
- Initial specification created from Option B architecture
- Winner selected: Option B (Mother-Compresses-All) over A (no cross-file awareness) and C (over-engineered)
- Option D deferred (requires test case design)
