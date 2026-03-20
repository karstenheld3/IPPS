# SPEC: MinifyIPPS V2 Compression Pipeline

**Doc ID**: MIPPS-SP03
**Feature**: MIPPS-V2-PIPELINE
**Goal**: Consolidated specification for MinifyIPPS (Intelligent Prompt and Pipeline System) V2 compression pipeline with run isolation, unified Large Language Model (LLM) client, and config-based model settings
**Timeline**: Created 2026-03-20
**Target file**: `_run_templateV2/mipps_pipeline.py` (orchestrator script)

**Depends on:**
- None (this is the authoritative V2 specification)

**Does not depend on:**
- `_SPEC_IPPS_MINIFICATION_MOTHER_MODEL.md [MIPPS-SP01]` (V1 spec, superseded)
- `_SPEC_IPPS_MINIFICATION_MOTHER_MODEL_CHANGES.md [MIPPS-SP02]` (V2 changes, merged into this doc)
- `_OPTION_A_PIPELINE_WITH_PROMPTS.md [MIPPS-OPT-A]` (rejected: no cross-file awareness)
- `_OPTION_C_DEPENDENCY_ORDERED.md [MIPPS-OPT-C]` (rejected: over-engineered)

## MUST-NOT-FORGET

- Mother compresses ALL .md files - no delegation to cheaper models. Verification model judges EVERY compressed file independently
- Only .md files compressed; non-.md files (.py, .json, .ps1, .png, etc.) SHOULD be copied as-is (not yet implemented - Known Gap). `__pycache__` folders excluded from output
- File exclusion: .md files < 100 lines AND rarely loaded -> copy as-is, do not compress
- Source directory configurable via `source_dir` in `pipeline_config.json`
- Step 7 report: exactly 5 lines per file (structural, removed, simplified, sacrificed, impact)
- Target: reduce total token count by >= 60%, max 5 files in manual review queue
- Anthropic cache Time To Live (TTL) is 5 minutes (ephemeral). Cache expiry detection exists in `cost_tracker.track_call()` but is not wired up (Known Gap)
- Each compression run creates isolated subfolder under `runs/` (currently only `cmd_compress` creates run folders)
- V2 unified `LLMClient` from `lib/llm_client.py` replaces V1 `llm_clients.py` + `api_cost_tracker.py`
- Model configs and pricing loaded from JSON files co-located in `lib/`, not hardcoded
- Per-file cost tracking with cache hit/miss status SHOULD be in `run_costs.json` (not yet wired up - Known Gap). Pricing must use standard API rates (not batch tier)
- Run summary (`run_summary.md`) generated per run after Step 7
- `build_api_params()` uses `thinking: {"type": "enabled", "budget_tokens": N}` for thinking models; adaptive thinking for Opus 4.6 not yet implemented (known gap per DD-18)

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

**Problem:** The IPPS DevSystem (~1MB, ~104 files) exceeds what cheaper LLMs can process effectively. Rules, workflows, and skills loaded into context consume ~300K tokens. Cheaper models (GPT-5-mini, Claude Haiku 4.5) cannot follow the full instruction set reliably. V1 MinifyIPPS had additional architectural limitations:
- Run artifacts overwrite each other (no history, no comparison)
- Cost data lost on state reset
- Hardcoded model configs scattered across code
- No tooling to compare runs or generate reports

**Solution:**
- Use Claude Opus 4.6 (1M context) as "Mother" model to analyze and compress all files
- Mother sees the entire system while compressing each file, preserving cross-file references
- Verification model (GPT-5-mini) independently judges each compression
- Iterative refinement: Mother reviews verification report, re-compresses failed files
- Pipeline script orchestrates the process with subcommands per step
- Run-based subfolder isolation preserves all artifacts per run
- Unified LLM client with JSON-based model configs
- Automatic cost tracking from standardized pricing files
- Run comparison and report generation tools

**What we don't want:**
- Independent per-file compression without cross-file awareness (Option A failure mode)
- Complex layer management with cascade failure risk (Option C over-engineering)
- Compression that breaks cross-file references
- Manual compression - must be automated and repeatable
- Mother evaluating its own output (independence requirement)
- Compression of Python scripts or JSON configs (copy as-is)
- Config file drift (copied JSONs becoming stale vs source)
- Breaking existing compression logic (Steps 1-7 behavior unchanged from V1)

## 2. Context

This pipeline is part of the IPPS (Intelligent Prompt and Pipeline System) project. The DevSystem is a set of rules, workflows, and skills that guide AI agents (primarily in Windsurf IDE). The system has grown to ~1MB, making it expensive to load into context for every interaction.

The compressed output is deployed as a drop-in replacement for the full DevSystem in `.windsurf/` folders of repositories where cheaper LLMs are used.

**Selected approach**: Option B (Mother-Compresses-All) chosen over:
- Option A (cheap pipeline): insufficient quality without cross-file awareness
- Option C (dependency-ordered): 2x cost of B for marginal quality gain
- Option D (test-driven): deferred, requires test case design first

**V2 consolidation**: This spec merges V1 pipeline behavior (MIPPS-SP01) with V2 architecture changes (MIPPS-SP02). All functional requirements, design decisions, and implementation guarantees are renumbered into a single sequence.

## 3. Domain Objects

### Bundle

A **Bundle** is the concatenated content of all .md source files, used as cached context for Mother.

- **Storage**: `context/all_files_bundle.md`
- **Size**: ~300K tokens (~1MB text)
- **Lifetime**: Created once in Step 1, reused for all subsequent Mother calls via prompt caching

### FileInventory

A **FileInventory** categorizes all source files by type and compressibility.

- **Source**: configurable via `source_dir` (default: `.windsurf/`)
- **Categories**:
  - `rules` - 8 md files (always compressible)
  - `workflows` - 36 md files (compressible unless excluded)
  - `skill_docs` - 24 md files (compressible unless excluded)
  - `skill_prompts` - 7 md files (compressible unless excluded)
- **Total**: ~75 .md files (compressible)
- **Non-.md files**: All copied to output as-is (scripts, configs, images, etc.)
- **Excluded from output**: `__pycache__` folders only

### ExclusionCriteria

An **ExclusionCriteria** defines which compressible files should be skipped.

- **Rule**: file has < 100 lines AND is referenced by <= 2 other files (per call tree analysis in Step 2)
- **Threshold**: `exclusion_max_lines: 100`, `exclusion_max_references: 2` in `pipeline_config.json`
- **Effect**: file copied as-is to output, not sent to Mother for compression
- **Expected reduction**: ~20-30% fewer files to compress (~50-55 files instead of 75)

### NeverCompress

A **NeverCompress** list defines paths always copied as-is, regardless of size or reference count.

- **Config**: `never_compress` array in `pipeline_config.json`
- **Format**: glob patterns relative to `source_dir` (e.g., `skills/llm-evaluation/prompts/*`)
- **Use case**: specialized prompts, templates, or content where compression would break functionality
- **Bundle**: included in `all_files_bundle.md` (Mother sees full context), but NOT sent to Mother for compression
- **Evaluation order**: `skip_patterns` (exclude entirely) -> `never_compress` (copy as-is) -> ExclusionCriteria (copy as-is) -> compress
- **Overlap rule**: file matching both `skip_patterns` AND `never_compress` is excluded entirely (`skip_patterns` wins)

### CompressionStrategy

A **CompressionStrategy** classifies every concept, rule, and feature across the system.

- **Storage**: `_03_FILE_COMPRESSION_STRATEGY.md` (in run's `analysis/` directory)
- **Lists**:
  - `Primary` - leave mostly as-is (core function, critical rules)
  - `Secondary` - compress (reduce formatting, merge sections, simplify examples)
  - `Drop` - remove entirely (rarely used features, redundant content)

### PipelineState

A **PipelineState** tracks progress across pipeline steps.

- **Storage**: `pipeline_state.json` (at project root; V2 also stores `run_id` and `run_dir` references)
- **Fields**:
  - `run_id` - current run identifier (V2)
  - `run_dir` - path to current run folder (V2)
  - `current_step` - last completed step number
  - `iteration` - current iteration number (1 = first pass)
  - `files_total` - total file count
  - `files_compressible` - count of compressible files
  - `files_compressed` - count of files processed in Step 6
  - `files_passed` - count passing verification threshold
  - `files_failed` - count below threshold, needing refinement
  - `files_excluded` - count of excluded .md files (never_compress + ExclusionCriteria)
  - `files_excluded_md` - count of excluded .md files by ExclusionCriteria only
  - `files_completed` - list of file paths processed (enables resume)
  - `_never_compress_files` - list of file paths matching `never_compress` patterns
  - `_excluded_files` - list of file paths matching ExclusionCriteria
  - `broken_references` - count of broken cross-file references
  - `cache_last_used` - ISO timestamp of last successful cache hit (or null)
  - `cost` - nested cost tracking (mother_input, mother_output, verification_input, verification_output, cache_read, cache_write, total)

### CompressedFile

A **CompressedFile** is the output of Mother's compression for a single source file.

- **Storage**: `runs/<run-id>/output/[category]/[filename]`
- **Properties**:
  - `source_path` - original file path relative to source directory
  - `file_type` - category from FileInventory
  - `compression_ratio` - output tokens / input tokens
  - `judge_score` - verification score 1-5
  - `iteration` - which iteration produced this version

### MinificationRun

A **MinificationRun** is an isolated execution of the compression pipeline.

- **Location**: `runs/<run-id>/`
- **Run ID format**: `<YYYYMMDD>-<HHMM>-<label>` (e.g., `20260320-1430-compress`)
- **Contents** (subdirectories created at run start; populated by the step that creates the run):
  - `run_config.json` - config snapshot at run start
  - `run_summary.md` - human-readable summary (written after Step 7)
  - `run_costs.json` - detailed cost breakdown (updated after each API call)
  - `analysis/` - reserved for Steps 2-4 outputs (currently written to project root, not run folder)
  - `context/` - reserved for Step 1 output (currently written to project root)
  - `prompts/step/`, `prompts/transform/`, `prompts/eval/` - reserved for Step 5 outputs (currently written to project root)
  - `verification/` - Step 7 outputs (`_04_FILE_COMPRESSION_REPORT.md`)
  - `output/` - compressed .md files and copied non-.md files

### RunConfig

A **RunConfig** captures the configuration used for a specific run.

- **Storage**: `runs/<run-id>/run_config.json`
- **Contents**: Snapshot of `pipeline_config.json` plus runtime metadata (`run_id`, `started_at`)
- **Written before first API call** (IG-09)

### RunCosts

A **RunCosts** tracks detailed cost breakdown per file and step.

- **Storage**: `runs/<run-id>/run_costs.json`
- **Fields**:
  - `total_cost` - accumulated cost in USD
  - `input_cost`, `output_cost`, `cache_read_cost`, `cache_write_cost` - cost breakdown
  - `total_input_tokens`, `total_output_tokens`, `total_cache_read_tokens`, `total_cache_creation_tokens` - token counts
  - `api_calls` - total API call count
  - `per_file` - list of per-file cost entries with `file`, `step`, `model`, `cost`, `input_tokens`, `output_tokens`, `cache_hit`

### LLMClient

The **LLMClient** class provides unified LLM access for MinifyIPPS.

- **Source**: `lib/llm_client.py` (adapted from LLM-Research, extended with cache support)
- **Config loading**: `lib/model-registry.json`, `lib/model-pricing.json`, `lib/model-parameter-mapping.json` (co-located with Python modules)
- **Constructor**: `LLMClient(model, reasoning_effort, output_length, verbosity, api_key, timeout)`
- **Key methods**:
  - `call(prompt, max_tokens)` - unified API call (OpenAI or Anthropic), returns `{"text": str, "usage": dict, "model": str, "finish_reason": str}`
  - `call_with_cache(bundle, prompt)` - bundle as cached system prompt (Anthropic only), returns same dict with additional cache token fields in usage
  - `check_context(prompt, expected_output_tokens)` - context window check
  - `get_info()` - return client configuration info
- **Constraints**: Minimum cacheable prefix size varies by model (per Anthropic API); caching silently skipped if bundle below threshold
- **Module functions**:
  - `calculate_cost(usage, model)` - compute cost from pricing JSON (handles `cache_read_input_tokens`, `cache_creation_input_tokens`)
  - `get_model_pricing(model)` - lookup pricing by model ID (exact match, then prefix match)
  - `build_api_params(model, reasoning_effort, output_length, verbosity, seed)` - build provider-specific API parameters
  - `check_context_fit(model, prompt, expected_output_tokens)` - context window validation
  - `create_client(provider, api_key, timeout)` - create provider SDK client
  - `retry_with_backoff(fn, retries, backoff)` - retry with exponential backoff (1s, 2s, 4s)

## 4. Functional Requirements

**MIPPS-FR-01: Bundle Generation**
- Read all .md files from source directory recursively
- Concatenate into single `context/all_files_bundle.md` with file path headers
- Include file metadata: path, line count, token estimate
- Skip files matching `skip_patterns` (`__pycache__/*`)
- Non-.md files not included in bundle (not needed for Mother's compression context)

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
- Files scoring < 3.5: Mother refines with judge feedback, re-judges (max 1 refinement attempt)
- Files scoring < 3.5 after refinement: append to `_05_MANUAL_REVIEW_QUEUE.md` with source path, scores, and judge feedback
- Save best version to `runs/<run-id>/output/[category]/[filename]`

**MIPPS-FR-07: Verification Report (Step 7)**
- Verification model produces `_04_FILE_COMPRESSION_REPORT.md` in `runs/<run-id>/verification/`
- Per file, exactly 5 lines: structural changes, removed features, simplified content, sacrificed details, possible impact
- Cross-file reference check: verify all references in compressed files resolve to existing concepts
- Summary section: pass rate, total compression ratio, broken references count, files needing attention

**MIPPS-FR-08: Iteration**
- Mother reviews `_04_FILE_COMPRESSION_REPORT.md` with cached context
- Updates `_03_FILE_COMPRESSION_STRATEGY.md` based on findings
- Re-compresses only files flagged in report
- Re-runs verification for changed files only

**MIPPS-FR-09: Non-.md File Handling**
- All non-.md files (.py, .json, .ps1, .png, .jpg, .txt, etc.) copied to `output/` as-is, preserving directory structure
- Files matching `never_compress` patterns copied to `output/` as-is
- Excluded .md files (< 100 lines AND rarely loaded) copied to `output/` as-is
- Files/folders matching `skip_patterns` (`__pycache__/*`) NOT copied to output
- Evaluation order for .md files: `skip_patterns` (exclude) -> `never_compress` (copy as-is) -> ExclusionCriteria (copy as-is) -> compress

**MIPPS-FR-10: Pipeline State Tracking**
- Track progress in `pipeline_state.json` after each step
- Track accumulated cost per model with cache read/write breakdown
- Track per-file completion within Step 6 via `files_completed` list (enables resume from last file)
- Allow resuming from any step if pipeline is interrupted
- Store `run_id` and `run_dir` in state for cross-step run folder reference

**MIPPS-FR-11: Verification of Mother Outputs (Steps 2-4)**
- `check` command: Verification model spot-checks Mother analysis documents
- Compare claims against source files (10-20 random file checks per document)
- Report issues (missing files, wrong counts, incorrect call chains)
- Feed issues back to Mother for correction before proceeding

**MIPPS-FR-12: Run Isolation**
- Each compression step creates `runs/<run-id>/` subfolder
- Run ID format: `<YYYYMMDD>-<HHMM>-<label>` (e.g., `20260320-1430-compress`)
- All compression outputs written to run folder: config snapshot, costs, compressed files
- `output/` (compressed files) is `runs/<run-id>/output/`
- ID collision handling: append `-2`, `-3` suffix

**MIPPS-FR-13: Unified LLM Client**
- Replace `AnthropicClient` and `OpenAIClient` with unified `LLMClient` class
- Model selection by ID (e.g., `claude-opus-4-6-20260204`, `gpt-5-mini`)
- Auto-detect provider from model ID prefix via `model-registry.json`
- Parameter mapping via `model-parameter-mapping.json` (effort levels, thinking budgets)

**MIPPS-FR-14: Config-Based Model Settings**
- `pipeline_config.json` contains model IDs only, not parameters
- Model parameters resolved from `lib/model-registry.json`
- Pricing resolved from `lib/model-pricing.json`
- Effort mapping from `lib/model-parameter-mapping.json`

**MIPPS-FR-15: Automatic Cost Tracking**
- Every API call returns usage dict with `input_tokens`, `output_tokens` (and optionally `cache_read_input_tokens`, `cache_creation_input_tokens` for Anthropic)
- Cost calculated via `llm_client.calculate_cost(usage, model)`
- Per-call cost accumulated in RunCosts via `cost_tracker.track_call()`
- Cache hit/miss tracked per call (`cache_read_input_tokens > 0` = hit)
- Thinking tokens (extended thinking) billed as output tokens; high thinking budgets increase cost proportionally
- `run_costs.json` updated atomically after each API call

**MIPPS-FR-16: Run Summary Generation**
- After Step 7, generate `run_summary.md` with:
  - Files total, compressed, excluded, failed
  - Compression ratio
  - Total cost and files tracked
  - Cache hit rate (hits/total calls with cache_hit field)

**MIPPS-FR-17: Run Comparison Tool**
- `compare_runs.py <run_dir_a> <run_dir_b>` compares two runs
- Loads `run_config.json`, `run_costs.json`, `run_summary.md` from each run
- Output: cost delta (absolute and percentage), token delta, cache utilization change, API call count change
- Identifies regressions and improvements

**MIPPS-FR-18: Config Snapshot**
- At run start, write `pipeline_config.json` content to `runs/<run-id>/run_config.json`
- Add runtime metadata: `run_id`, `started_at`
- Must be written before first API call (IG-09)

## 5. Design Decisions

**MIPPS-DD-01:** Mother compresses all files, no delegation to cheaper models. Rationale: cross-file awareness is the primary quality requirement; only a model with full system context can guarantee reference integrity.

**MIPPS-DD-02:** Verification model is independent from Mother. Rationale: self-evaluation is unreliable; GPT-5-mini provides cheap, independent judgment.

**MIPPS-DD-03:** Single compressed version per file (no ensemble). Rationale: Mother with full context produces higher quality than multiple cheap candidates.

**MIPPS-DD-04:** Sequential compression, not parallel. Rationale: all Mother calls share the same cached context; parallelism would require multiple cache instances at higher cost.

**MIPPS-DD-05:** Exclusion criteria applied after Step 2 (call tree). Rationale: load frequency data needed to determine "rarely loaded".

**MIPPS-DD-06:** Judge threshold is 3.5/5.0. One refinement attempt; if still below, flag for manual review.

**MIPPS-DD-07:** Source directory is configurable via `source_dir` config. Default `.windsurf/`.

**MIPPS-DD-08:** Cost tracking per API call. Actual cost tracking enables budget monitoring and early termination if costs exceed budget.

**MIPPS-DD-09:** Verification model cannot validate behavioral correctness. GPT-5-mini judges structural preservation but lacks domain knowledge. Functional testing (Option D) planned as future work.

**MIPPS-DD-10:** Verification uses OpenAI Chat Completions API, not Responses API. Chat Completions is simpler and sufficient for stateless single-turn verification requests.

**MIPPS-DD-11:** V2 uses versioned Mother model ID (`claude-opus-4-6-20260204`) but unversioned verifier (`gpt-5-mini`). Verifier pinning deferred until output quality baselines established.

**MIPPS-DD-12:** Config JSON files co-located in `lib/` alongside Python modules. Rationale: simpler maintenance, no cross-directory resolution; version-locked configs per pipeline version.

**MIPPS-DD-13:** Run ID uses timestamp, not UUID. Rationale: human-readable, sortable, identifies when run occurred.

**MIPPS-DD-14:** `llm_client.py` adapted (vendored), not imported from LLM-Research. Rationale: MinifyIPPS needs `call_with_cache(bundle, prompt)` method for Anthropic prompt caching not present in source.

**MIPPS-DD-15:** Per-file cost tracking stored in `run_costs.json`, not `pipeline_state.json`. Rationale: separate concerns; state tracks progress, costs track spending.

**MIPPS-DD-16:** `compare_runs.py` is an optional tool, not a pipeline step. Core pipeline (Steps 1-7) unchanged.

**MIPPS-DD-17:** Cache TTL uses 5 minutes (Anthropic ephemeral cache default, 1.25x write cost). Sequential synchronous calls refresh cache on each hit. Pipeline's `cache.ttl` config field is informational only; actual TTL controlled by Anthropic API.

**MIPPS-DD-18:** Opus 4.6 should use `thinking: {"type": "adaptive"}` + `output_config: {"effort": ...}` (per Anthropic API). Current implementation uses `thinking: {"type": "enabled", "budget_tokens": N}` via the `model-registry.json` thinking method. Known gap: `build_api_params()` lacks adaptive thinking code path for Opus 4.6.

**MIPPS-DD-19:** `model-pricing.json` must contain standard API rates. Pipeline uses synchronous Messages/Chat Completions API, not Batch API. Batch pricing (50% discount) only applies to Batch API endpoint.

**MIPPS-DD-20:** `_call_anthropic_with_cache` joins ALL text blocks from response content (skipping thinking blocks). `_call_anthropic` (non-cached) extracts first text block only. Rationale: cached calls may produce multi-block responses due to thinking interleaving.

**MIPPS-DD-21:** Budget `warning_threshold` uses 0.0-1.0 ratio (not percentage). Example: `0.8` = warn at 80% of `max_total_usd`.

## 6. Implementation Guarantees

**MIPPS-IG-01:** Every compressed file is independently verified by a model that did not perform the compression.

**MIPPS-IG-02:** No source file is modified. All output goes to `runs/<run-id>/output/` directory.

**MIPPS-IG-03:** Pipeline can be interrupted and resumed from last completed step without data loss.

**MIPPS-IG-04:** Non-compressible files appear in output with identical content to source.

**MIPPS-IG-05:** Bundle is re-sent with every Mother call (Anthropic caches automatically). If cache expires (5-min TTL), the next call triggers cache write at ~1.25x input cost. Pipeline detects expiration via `cache_read_input_tokens == 0` on non-first calls and logs cost impact warning.

**MIPPS-IG-06:** Total cost never exceeds `max_total_usd` without `check_budget()` returning `ok=False`.

**MIPPS-IG-07:** Files matching exclusion criteria are never sent to Mother for compression.

**MIPPS-IG-08:** Run folder created atomically at compression start. If creation fails, pipeline aborts before any API calls.

**MIPPS-IG-09:** `run_config.json` written before first API call. Run is always traceable to its config.

**MIPPS-IG-10:** Cost tracking survives interruption. `run_costs.json` uses atomic write pattern (write `.tmp`, rename).

**MIPPS-IG-11:** Model pricing lookup fails gracefully. If model not in `model-pricing.json`, cost set to 0.0 with `pricing_found: false`.

## 7. Key Mechanisms

### Prompt Caching

Mother's ~300K token bundle is sent as system prompt content with `cache_control: {"type": "ephemeral"}`. First call pays cache write cost (1.25x input price). Subsequent calls within TTL hit cache read at ~0.1x base input price.

**Cost structure per cached bundle call:**
- **Cache write** (first or post-expiry call): ~1.25x input price
- **Cache read** (subsequent calls within 5-min TTL): ~0.1x input price
- **Breakeven**: After ~2 cache reads, caching saves money vs re-sending full bundle

**Cache monitoring (IG-05):**
- After each Mother call, check `cache_read_input_tokens` in usage response
- On non-first calls: `cache_read_input_tokens == 0` indicates cache expired -> `cost_tracker.track_call()` logs warning with cost delta
- Track cache miss count for cost reporting

### LLM Client Integration

```python
# V2: Unified client
from lib.llm_client import LLMClient, calculate_cost

mother = LLMClient(model="claude-opus-4-6-20260204", reasoning_effort="high")
verifier = LLMClient(model="gpt-5-mini", reasoning_effort="medium")

# Mother calls use cached system prompt
result = mother.call_with_cache(bundle, prompt)  # Anthropic only
text, usage = result["text"], result["usage"]

# Verifier calls use standard prompt
result = verifier.call(prompt)
text, usage = result["text"], result["usage"]

# Cost calculation
cost = calculate_cost(usage, model="claude-opus-4-6-20260204")
# Returns: {"input_cost", "output_cost", "cache_read_cost", "cache_write_cost", "total_cost", "pricing_found"}
```

### Cache-Aware Cost Tracking

```python
from lib.cost_tracker import init_costs, track_call, save_costs, check_budget

costs = init_costs()
track_call(costs, step="compress", file_path="rules/core.md",
           usage=result["usage"], model="claude-opus-4-6-20260204",
           cache_hit=(usage.get("cache_read_input_tokens", 0) > 0))
save_costs(costs, run_dir)
ok, msg = check_budget(costs, config)
```

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
- `*` -> `compress_other` (fallback)

### Cost Budget Guard

Pipeline tracks actual costs per API call via `cost_tracker`. If accumulated cost exceeds `max_total_usd`, `check_budget()` returns `ok=False`. Warning issued when cost reaches `warning_threshold` ratio (default: 0.8 = 80%).

## 8. Action Flow

### Full Pipeline Run

```
User runs: mipps_pipeline.py bundle --source-dir .windsurf/
├─> Scan source directory, categorize files
├─> Concatenate compressible + non-compressible file contents
├─> Write context/all_files_bundle.md
└─> Update pipeline_state.json (step: 1)

User runs: mipps_pipeline.py analyze
├─> Step 2: Mother call (bundle as cached input)
│   ├─> Produce _01_FILE_CALL_TREE.md
│   └─> Update state (step: 2)
├─> Step 3: Mother call (cached)
│   ├─> Produce _02_FILE_COMPLEXITY_MAP.md
│   ├─> Identify files matching exclusion criteria
│   ├─> Identify never_compress files
│   └─> Update state (step: 3)
└─> Step 4: Mother call (cached)
    ├─> Produce _03_FILE_COMPRESSION_STRATEGY.md
    ├─> Exclude flagged files from compression scope
    └─> Update state (step: 4)

User runs: mipps_pipeline.py check
├─> Verification model spot-checks Mother output documents
├─> Report issues
└─> If issues found: feed back to Mother, re-produce document

User runs: mipps_pipeline.py generate
├─> Mother generates type-specific compression prompts
├─> Write prompts/transform/*.md and prompts/eval/*.md
└─> Update state (step: 5)

User runs: mipps_pipeline.py compress
├─> Create run folder: runs/<YYYYMMDD-HHMM-compress>/
├─> Write run_config.json (config snapshot)
├─> For each non-excluded compressible file:
│   ├─> Mother compresses (cached context)
│   ├─> Verification judges (score 1-5)
│   ├─> If score < 3.5: Mother refines, re-judge
│   ├─> Save to runs/<run-id>/output/
│   ├─> Track cost via cost_tracker
│   └─> Update state (files_compressed++)
├─> Copy never_compress .md files to output/ as-is
├─> Copy excluded .md files to output/ as-is
└─> Update state (step: 6, run_id, run_dir)

User runs: mipps_pipeline.py verify
├─> Verification model compares each original vs compressed
├─> Produce _04_FILE_COMPRESSION_REPORT.md in runs/<run-id>/verification/
├─> Check cross-file references
├─> Generate run_summary.md
└─> Update state (step: 7)

User runs: mipps_pipeline.py iterate
├─> Mother reviews report (cached context)
├─> Updates _03_FILE_COMPRESSION_STRATEGY.md
├─> Re-compresses only flagged files
├─> Re-runs verification for changed files
└─> Update state (iteration++)
```

## 9. Data Structures

### pipeline_config.json (V2)

```json
{
  "source_dir": "E:/Dev/IPPS/.windsurf/",
  "models": {
    "mother": "claude-opus-4-6-20260204",
    "verifier": "gpt-5-mini"
  },
  "reasoning_effort": "high",
  "output_length": "high",
  "thresholds": {
    "judge_min_score": 3.5,
    "max_refinement_attempts": 1,
    "exclusion_max_lines": 100,
    "exclusion_max_references": 2,
    "target_reduction_percent": 60,
    "max_manual_review_files": 5
  },
  "cache": {
    "ttl": "5m"
  },
  "budget": {
    "max_total_usd": 100.0,
    "warning_threshold": 0.8
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
    "skills/llm-transcription/prompts/*"
  ],
  "api_timeout_seconds": 600
}
```

**Changes from V1:**
- `models.mother` is model ID string (was: object with `provider`, `model`, `thinking`, `max_context`)
- `models.verification` renamed to `models.verifier`
- Added `reasoning_effort`, `output_length` for parameter mapping
- `budget.warn_at_percent` renamed to `budget.warning_threshold` (0.0-1.0 ratio)
- Removed hardcoded API parameters (resolved from registry)
- `api_timeout_seconds` increased to 600 (was 120)

### pipeline_state.json (V2)

```json
{
  "run_id": "20260320-1430-compress",
  "run_dir": "E:/Dev/IPPS/_Sessions/_2026-03-19_MinifyIPPS/_run_templateV2/runs/20260320-1430-compress",
  "current_step": 7,
  "iteration": 1,
  "files_total": 104,
  "files_compressible": 75,
  "files_excluded": 20,
  "files_compressed": 55,
  "files_passed": 48,
  "files_failed": 7,
  "files_excluded_md": 20,
  "files_completed": ["rules/core-conventions.md", "rules/devsystem-core.md"],
  "_never_compress_files": ["skills/llm-evaluation/prompts/eval_prompt.md"],
  "_excluded_files": ["workflows/tiny-workflow.md"],
  "broken_references": 0,
  "cache_last_used": null,
  "cost": {
    "mother_input": 2.45,
    "mother_output": 38.20,
    "verification_input": 0.12,
    "verification_output": 0.08,
    "cache_read": 1.20,
    "cache_write": 3.50,
    "total": 45.55
  }
}
```

### run_costs.json

```json
{
  "total_cost": 45.32,
  "input_cost": 25.10,
  "output_cost": 12.00,
  "cache_read_cost": 3.20,
  "cache_write_cost": 5.02,
  "total_input_tokens": 8500000,
  "total_output_tokens": 250000,
  "total_cache_read_tokens": 6200000,
  "total_cache_creation_tokens": 900000,
  "api_calls": 113,
  "per_file": [
    {
      "file": "rules/core-conventions.md",
      "step": "compress",
      "model": "claude-opus-4-6-20260204",
      "cost": 0.52,
      "input_tokens": 305000,
      "output_tokens": 4200,
      "cache_hit": true
    }
  ]
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

### Module Structure

```
_run_templateV2/
├─> mipps_pipeline.py                      (entry point, Command-Line Interface (CLI))
├─> pipeline_config.json                   (template config)
├─> compare_runs.py                        (run comparison tool)
├─> lib/
│   ├─> __init__.py
│   ├─> llm_client.py                      (unified LLM client, adapted from LLM-Research)
│   ├─> model-registry.json                (model properties: provider, method, limits)
│   ├─> model-pricing.json                 (per-model token pricing)
│   ├─> model-parameter-mapping.json       (effort level mappings)
│   ├─> file_bundle_builder.py             (Step 1: file scanning, concatenation)
│   ├─> mother_analyzer.py                 (Steps 2-4: Mother analysis calls)
│   ├─> mother_output_checker.py           (verification spot-checks)
│   ├─> compression_prompt_builder.py      (Step 5: compression prompt generation)
│   ├─> file_compressor.py                 (Step 6: compression + judge loop)
│   ├─> compression_report_builder.py      (Step 7: report generation)
│   ├─> compression_refiner.py             (iteration: review + re-compress)
│   ├─> run_manager.py                     (run folder creation, config snapshot, summary)
│   ├─> cost_tracker.py                    (per-run cost tracking, replaces api_cost_tracker.py)
│   ├─> pipeline_state.py                  (pipeline_state.json read/write, atomic writes)
│   └─> test_llm_client.py                 (integration test script for llm_client.py)
├─> prompts/
│   └─> step/
│       ├─> s2_call_tree.md
│       ├─> s3_complexity_map.md
│       ├─> s4_compression_strategy.md
│       ├─> s5_generate_prompts.md
│       ├─> s6_compress_file.md
│       └─> s7_verify_file.md
├─> tests/
│   ├─> conftest.py                        (shared fixtures: tmp_run_dir, mock clients, sample data)
│   ├─> test_config.py                     (config loading and pricing tests)
│   ├─> test_llm_client.py                 (LLMClient unit tests)
│   ├─> test_run_manager.py                (run folder, config snapshot, summary tests)
│   ├─> test_cost_tracker.py               (cost tracking, atomic save, budget tests)
│   ├─> test_pipeline_state.py             (state init, load/save, cost update tests)
│   └─> test_compare_runs.py              (run comparison tests)
└─> runs/                                  (created at runtime, per-run artifacts)
```

**Deleted V1 files:**
- `lib/llm_clients.py` (V1 AnthropicClient + OpenAIClient)
- `lib/api_cost_tracker.py` (V1 hardcoded PRICING dict)

### CLI Subcommands

```python
def main():
    parser = argparse.ArgumentParser(description="MinifyIPPS Compression Pipeline")
    subparsers = parser.add_subparsers(dest="command")

    sub_bundle = subparsers.add_parser("bundle")     # Step 1 (--source-dir override)
    sub_analyze = subparsers.add_parser("analyze")    # Steps 2-4
    sub_check = subparsers.add_parser("check")        # Verify Mother output
    sub_generate = subparsers.add_parser("generate")  # Step 5
    sub_compress = subparsers.add_parser("compress")   # Step 6 (creates run folder)
    sub_verify = subparsers.add_parser("verify")       # Step 7 (generates run summary)
    sub_iterate = subparsers.add_parser("iterate")     # Review + re-compress
    sub_status = subparsers.add_parser("status")       # Show state
```

### API Client Requirements

- Anthropic SDK for Mother (Claude Opus 4.6) with extended thinking via `thinking: {"type": "enabled", "budget_tokens": N}` (thinking tokens billed as output)
- OpenAI SDK for Verification (GPT-5-mini) via Chat Completions API (`client.chat.completions.create`) or Responses API (for reasoning models)
- Prompt caching via `cache_control: {"type": "ephemeral"}` on system prompt content block (5-min TTL)
- Both SDKs have built-in retry with `max_retries` parameter; `LLMClient` adds application-level retry via `retry_with_backoff(fn, retries=3, backoff=(1, 2, 4))`
- OpenAI SDK: `OpenAI(timeout=T)` reads `OPENAI_API_KEY` env var
- Anthropic SDK: `Anthropic(timeout=T)` reads `ANTHROPIC_API_KEY` env var
- OpenAI usage response uses `prompt_tokens`/`completion_tokens`; Anthropic uses `input_tokens`/`output_tokens` - `call_llm` normalizes both to `input_tokens`/`output_tokens`
- Log API responses to stdout (via `logging` module)

### Dependencies

- `anthropic` (Anthropic Python SDK)
- `openai` (OpenAI Python SDK)
- `pathlib`, `json`, `argparse`, `datetime`, `logging`, `shutil` (stdlib)

### Known Gaps (V2 as-built)

**Bugs:**
- **Budget guard non-functional (IG-06)**: `check_budget()` reads key `total_cost` but `state["cost"]` uses key `total`. Budget check always returns ok=True. Fix: pass `{"total_cost": state["cost"]["total"]}` or change `check_budget` to read `total`.

**Missing implementations:**
- **`run_costs.json` never written (FR-15, DD-08)**: `run_compression_step()` uses `pipeline_state.update_cost()` for cost accumulation, not `cost_tracker.track_call()` + `save_costs()`. Per-file cost entries in `run_costs.json` are never created. `generate_run_summary()` and `compare_runs.py` receive empty costs.
- **Non-.md file copying (FR-09, IG-04)**: `run_compression_step()` only iterates `.md` files. Non-.md files (.py, .json, .ps1, etc.) are never copied to output directory.
- **Mother feedback loop (FR-11)**: `cmd_check` prints spot-check issues but does not feed them back to Mother for correction. Manual intervention required.
- **Report compression ratio (FR-07)**: `generate_report()` summary lacks total compression ratio and files-needing-attention count.
- **Partial re-verification (FR-08)**: `cmd_verify` processes ALL files in output_dir, not just files changed during iteration.
- **Cache expiry detection (IG-05)**: `_call_anthropic_with_cache` checks `cache_creation_input_tokens == 0` (detects "too small to cache"). The cache expiry check (`cache_read_input_tokens == 0` on non-first calls) exists in `cost_tracker.track_call()` but is never called from compression loop.

**Deferred features:**
- **Adaptive thinking (DD-18)**: `build_api_params()` lacks `thinking: {"type": "adaptive"}` code path for Opus 4.6. Uses `type: "enabled"` with `budget_tokens` instead.
- **Run isolation scope**: Only `cmd_compress` creates run folders. Steps 1-5 write to project root. Full per-step run isolation deferred.
- **CLI flags**: `--run-label` and `--run-id` global arguments not yet implemented. `cmd_compress` uses hardcoded label `"compress"`.
- **`generate_report.py`**: Optional HTML report generator not implemented (deferred per DD-16).
- **`_call_anthropic` text extraction (DD-20)**: Non-cached Anthropic calls extract first text block only (via `break`). Multi-block responses may lose content. `_call_anthropic_with_cache` correctly joins all text blocks.
- **Default config `cache.ttl`**: `_load_config()` default uses `"1h"` (informational only; actual TTL is 5m per DD-17).

## 11. Document History

**[2026-03-20 22:00]**
- Added: 7 new Known Gaps from SPEC-vs-code verification
- Added: Bug category in Known Gaps (check_budget key mismatch IG-06)
- Added: Missing implementations category (run_costs.json, non-.md copying, Mother feedback, report fields, partial re-verification, cache expiry detection)
- Changed: Known Gaps reorganized into Bugs, Missing implementations, Deferred features
- Fixed: 3 MNF items annotated with "Known Gap" where code doesn't match spec (non-.md copying, cache detection, run_costs.json)

**[2026-03-20 21:30]**
- Fixed: IPPS acronym expanded on first use in Goal line (AP-PR-06)
- Fixed: `cache_last_used` added to PipelineState domain object fields list
- Fixed: MNF list consolidated from 18 to 12 items (merged related items)
- Fixed: `cache.ttl` in config example changed from `"1h"` to `"5m"` (matches DD-17 actual TTL)
- Fixed: Bundle domain object clarified to "all .md source files"
- Fixed: MinificationRun contents annotated with current run isolation scope
- Fixed: Known Gaps `_call_anthropic` entry cross-references DD-20

**[2026-03-20 21:00]**
- Initial V2 consolidated specification
- Merged V1 pipeline behavior (MIPPS-SP01) with V2 architecture changes (MIPPS-SP02)
- Reflects as-built state of `_run_templateV2/` after all TK-001 to TK-019 tasks completed
- FR-01 to FR-11 from SP01, FR-12 to FR-18 from SP02
- DD-01 to DD-11 from SP01, DD-12 to DD-19 from SP02, DD-20 to DD-21 new
- IG-01 to IG-07 from SP01, IG-08 to IG-11 from SP02
- Added Known Gaps section documenting implementation deviations from spec
- Config files location updated from `configs/` to `lib/` (reflecting actual implementation)
- PipelineState domain object updated with V2 fields (run_id, run_dir, cache cost fields)
- RunCosts schema updated to match actual `cost_tracker.init_costs()` output
