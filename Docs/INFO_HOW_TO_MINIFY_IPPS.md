# INFO: How to Minify IPPS

**Doc ID**: MIPPS-IN01
**Goal**: Document the MinifyIPPS pipeline for compressing DevSystem markdown files
**Timeline**: Created 2026-03-20

## Summary

- MinifyIPPS compresses `.windsurf/` markdown files using LLM-based compression with quality verification
- Pipeline location: `_Sessions/_2026-03-19_MinifyIPPS/_run_templateV2/`
- 7-step workflow: bundle -> analyze -> check -> generate -> compress -> verify -> iterate
- Configuration via `pipeline_config.json` - key setting: `target_compression_percent`
- Post-processing minification: `strip_bold` removes `**bold**` markers via regex

## Table of Contents

1. [Quick Start](#1-quick-start)
2. [Pipeline Steps](#2-pipeline-steps)
3. [Configuration Reference](#3-configuration-reference)
4. [File Structure](#4-file-structure)
5. [Post-Pipeline: Copy Functional Files](#5-post-pipeline-copy-functional-files)

## 1. Quick Start

```powershell
cd E:\Dev\IPPS\_Sessions\_2026-03-19_MinifyIPPS\_run_templateV2

# Full pipeline
python mipps_pipeline.py bundle
python mipps_pipeline.py analyze
python mipps_pipeline.py check
python mipps_pipeline.py generate
python mipps_pipeline.py compress
python mipps_pipeline.py verify

# Check status anytime
python mipps_pipeline.py status
```

## 2. Pipeline Steps

| Step | Command | Description |
|------|---------|-------------|
| 1 | `bundle` | Scan source_dir, create `all_files_bundle.md` |
| 2 | `analyze` | Mother model builds call tree, complexity map, compression strategy |
| 3 | `check` | Spot-check Mother outputs for accuracy |
| 4 | `generate` | Create per-file transform/eval prompts |
| 5 | `compress` | Compress each file, judge quality, refine if needed |
| 6 | `verify` | Verify compressed files, check cross-references |
| 7 | `iterate` | Review failures, recompress problem files |

## 3. Configuration Reference

File: `pipeline_config.json`

### Core Settings

```json
{
  "source_dir": "E:/Dev/IPPS/.windsurf/",
  "models": {
    "mother": "claude-opus-4-6-20260204",
    "verifier": "gpt-5-mini"
  },
  "reasoning_effort": "high",
  "output_length": "high"
}
```

- `source_dir` - Input folder to compress
- `mother` - Main compression model (Anthropic)
- `verifier` - Quality judge model (OpenAI)
- `reasoning_effort` - Model thinking depth: low/medium/high
- `output_length` - Max output tokens: low/medium/high

### Thresholds

```json
"thresholds": {
  "judge_min_score": 3.5,
  "max_refinement_attempts": 1,
  "exclusion_max_lines": 100,
  "exclusion_max_references": 2,
  "target_compression_percent": 40,
  "max_manual_review_files": 5
}
```

- `judge_min_score` - Minimum quality score (1-5) to accept compression
- `max_refinement_attempts` - Retries if judge rejects
- `target_compression_percent` - Target output size as % of original (40 = 60% reduction)
- `exclusion_max_lines` - Files under this size may be excluded
- `max_manual_review_files` - Cap on files sent to manual review queue

### Budget

```json
"budget": {
  "max_total_usd": 100.0,
  "warning_threshold": 0.8
}
```

- `max_total_usd` - Hard stop when budget exceeded
- `warning_threshold` - Warn at 80% of budget

### File Routing

```json
"file_type_map": {
  "rules/*.md": "compress_rules",
  "workflows/*.md": "compress_workflows",
  "skills/*/SKILL.md": "compress_skill_docs",
  "skills/*/*_RULES.md": "compress_rules",
  "*": "compress_other"
}
```

Maps file patterns to prompt types in `prompts/eval/` and `prompts/transform/`.

### Minification (Post-Processing)

```json
"minify": {
  "strip_bold": true
}
```

- `strip_bold` - Remove `**text**` markers after LLM compression (regex: `\*\*([^*]+)\*\*` -> `$1`)

### Exclusions

```json
"include_patterns": ["*.md"],
"skip_patterns": ["__pycache__/*"],
"never_compress": [
  "skills/llm-evaluation/prompts/*",
  "skills/llm-transcription/prompts/*"
]
```

- `include_patterns` - Only process matching files
- `skip_patterns` - Exclude from processing
- `never_compress` - Copy verbatim, no compression

## 4. File Structure

```
_run_templateV2/
├── mipps_pipeline.py          # CLI entry point
├── pipeline_config.json       # Configuration
├── lib/
│   ├── cost_tracker.py        # Budget tracking
│   ├── file_bundle_builder.py # Step 1: bundle
│   ├── file_compressor.py     # Step 5: compress
│   ├── compression_report_builder.py  # Step 6: verify
│   ├── llm_client.py          # Anthropic + OpenAI clients
│   ├── mother_analyzer.py     # Steps 2-4: analysis
│   ├── pipeline_state.py      # State persistence
│   └── run_manager.py         # Run directory management
├── prompts/
│   ├── step/                  # Per-step prompts (s2-s7)
│   ├── eval/                  # Generated eval prompts
│   └── transform/             # Generated transform prompts
└── tests/                     # Unit tests
```

## 5. Post-Pipeline: Copy Functional Files

The pipeline only compresses `.md` files. Functional files (scripts, configs) must be copied separately to make the output usable.

### Identify Missing Files

```powershell
$src = "E:\Dev\IPPS\DevSystemV3.5"
$dst = "E:\Dev\IPPS\DevSystemV3.5-Mini"

# Find files in source but not in destination (excluding cache/temp)
$srcFiles = Get-ChildItem -Path $src -Recurse -File |
    Where-Object { $_.FullName -notmatch "__pycache__|\. tmp_|pricing-sources|registry-sources" } |
    ForEach-Object { $_.FullName.Substring($src.Length + 1) }

$dstFiles = Get-ChildItem -Path $dst -Recurse -File |
    ForEach-Object { $_.FullName.Substring($dst.Length + 1) }

$missing = $srcFiles | Where-Object { $_ -notin $dstFiles }
Write-Host "Missing files: $($missing.Count)"
$missing
```

### Copy Functional Files

```powershell
# Copy each missing file, creating directories as needed
foreach ($f in $missing) {
    $s = Join-Path $src $f
    $d = Join-Path $dst $f
    $dir = Split-Path $d
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    Copy-Item $s $d -Force
    Write-Host "Copied: $f"
}
```

### What to Copy

| Type | Examples | Action |
|------|----------|--------|
| Python scripts | `*.py` | Copy as-is |
| PowerShell scripts | `*.ps1` | Copy as-is |
| JSON configs | `model-registry.json`, `model-pricing.json` | Copy as-is |
| `__pycache__/` | Compiled Python | Skip |
| `pricing-sources/` | Reference images | Skip |
| `registry-sources/` | Transcription cache | Skip |
| `.tmp_*` files | Temporary scripts | Skip |

## Document History

**[2026-03-20 20:19]**
- Added: Section 5 "Post-Pipeline: Copy Functional Files" with PowerShell scripts and file type table

**[2026-03-20 19:33]**
- Initial document created
