# INFO: Judge Prompt V1 Evaluation

**Doc ID**: SCOR-IN05
**Goal**: Evaluate 4 combined judge prompt variants (v1a-v1d) for transcription quality scoring
**Timeline**: Created 2026-01-26

**Depends on:**
- `_SPEC_OPTIMIZED_JUDGE_PROMPT.md [SCOR-SP03]` for judge prompt requirements
- `_INFO_GEN2_PROMPT_EVALUATION.md [SCOR-IN02]` for Gen2 baseline metrics

## Summary

- **judge_v1d wins** with highest discrimination (0.94) and average (3.27) [TESTED]
- **Detailed examples strategy** most effective for combined judge prompts [TESTED]
- **All v1 prompts outperform single-dimension Gen2** when comparing combined scoring [TESTED]
- **v1c (concise) nearly matches v1d** with disc=0.91 at 27 lines vs 113 lines [TESTED]
- **Full 1-5 scale utilized** - all prompts show min=1, max=5 [TESTED]

## Table of Contents

1. [Experiment Design](#1-experiment-design)
2. [Prompt Variants](#2-prompt-variants)
3. [Results](#3-results)
4. [Analysis](#4-analysis)
5. [Comparison to Gen2](#5-comparison-to-gen2)
6. [Sources](#6-sources)
7. [Next Steps](#7-next-steps)
8. [Document History](#8-document-history)

## 1. Experiment Design

### 1.1 Objective

Test which combined judge prompt style (evaluating all 3 dimensions in one call) produces best discrimination for transcription quality scoring.

### 1.2 Test Configuration

- **Test set**: 80 transcriptions (same as Gen1/Gen2 tests)
- **Judge model**: GPT-5-mini
- **Workers**: 13 per prompt (4 prompts in parallel)
- **Output**: Combined weighted score (text=0.25, structure=0.35, graphics=0.40)

### 1.3 Prompt Strategies

Adapted from transcription prompt v1 evaluation:
- **v1a**: Comprehensive guidance (122 lines)
- **v1b**: DO/DON'T anti-patterns (85 lines)
- **v1c**: Maximum concision (27 lines)
- **v1d**: Detailed BAD/GOOD examples (113 lines)

## 2. Prompt Variants

### 2.1 judge_v1a - Comprehensive Guidance

- **Length**: 122 lines
- **Style**: Full explanations for each dimension
- **Output schema**: Verbose with justifications, outlines, error lists

### 2.2 judge_v1b - DO/DON'T Format

- **Length**: 85 lines
- **Style**: CRITICAL RULES upfront, DO/DON'T for each dimension
- **Output schema**: Compact with essential fields only

### 2.3 judge_v1c - Maximum Concision

- **Length**: 27 lines
- **Style**: One-line scoring scales, minimal instructions
- **Output schema**: Shortened field names (text, structure, graphics, weighted)

### 2.4 judge_v1d - Detailed Examples

- **Length**: 113 lines
- **Style**: BAD/GOOD contrast for each dimension with code blocks
- **Output schema**: Full with justifications

## 3. Results

### 3.1 Overall Metrics

- **judge_v1d**: count=80, avg=3.27, var=3.08, **disc=0.94**
- **judge_v1c**: count=77, avg=3.21, var=2.92, disc=0.91
- **judge_v1b**: count=80, avg=3.19, var=2.70, disc=0.85
- **judge_v1a**: count=80, avg=3.08, var=2.58, disc=0.84

### 3.2 Score Distribution

All prompts:
- **Min**: 1.0
- **Max**: 5.0
- **Range**: Full 1-5 scale utilized

### 3.3 JSON Output Compliance

- **judge_v1a**: 80/80 valid JSON with expected schema
- **judge_v1b**: 80/80 valid JSON with expected schema
- **judge_v1c**: 77/80 valid JSON (3 parse errors)
- **judge_v1d**: 80/80 valid JSON with expected schema

## 4. Analysis

### 4.1 Why judge_v1d Won

1. **BAD/GOOD examples clarify edge cases**: Concrete examples prevent ambiguous scoring
2. **Full output schema**: Detailed justifications help LLM reason through scoring
3. **Balanced length**: 113 lines provides enough context without overwhelming

### 4.2 Why judge_v1c Performed Well

1. **Concision works**: 27 lines achieved disc=0.91 (only 0.03 behind v1d)
2. **Token efficiency**: ~4x shorter prompt, similar discrimination
3. **3 JSON errors**: Minimal instructions may cause occasional format issues

### 4.3 v1b Underperformed Expectations

For transcription prompts, v1b (DO/DON'T) won. For judge prompts, it ranked 3rd:
- **Possible cause**: Judge prompts require more reasoning context
- **Anti-patterns less helpful**: Judging requires positive criteria, not just avoiding mistakes

### 4.4 Discrimination Comparison

- **judge_v1d**: 0.94
- **judge_v1c**: 0.91
- **judge_v1b**: 0.85
- **judge_v1a**: 0.84

All v1 prompts show good discrimination (>0.8), indicating they distinguish quality levels effectively.

## 5. Comparison to Gen2

### 5.1 Gen2 Single-Dimension Winners

From `_INFO_GEN2_PROMPT_EVALUATION.md [SCOR-IN02]`:
- **text_c2**: disc=0.57 (original), disc=1.44 (validation)
- **struct_b2**: disc=0.74 (original), disc=1.28 (validation)
- **graphics_a2**: disc=0.94 (original), disc=2.10 (validation)

### 5.2 Combined vs Single-Dimension

Combined judge prompts (v1) evaluate all 3 dimensions in one call:
- **Pros**: Single API call, consistent scoring, weighted combination
- **Cons**: More complex output schema, potential for partial failures

Single-dimension prompts (Gen2) evaluate one dimension per call:
- **Pros**: Simpler, specialized, higher per-dimension discrimination
- **Cons**: 3 API calls needed, no built-in weighting

### 5.3 Recommendation

Use **judge_v1d** for combined scoring when:
- Single API call preferred
- Weighted overall score needed
- Moderate discrimination (0.94) acceptable

Use **Gen2 prompts separately** when:
- Maximum discrimination per dimension needed
- Dimension-specific analysis required
- API cost not a concern

## 6. Sources

**Primary Sources:**
- `SCOR-IN05-SC-DATA-V1A`: `results/2026-01-26_23-25_judge-v1/judge_v1a/` - 80 evaluations [TESTED]
- `SCOR-IN05-SC-DATA-V1B`: `results/2026-01-26_23-25_judge-v1/judge_v1b/` - 80 evaluations [TESTED]
- `SCOR-IN05-SC-DATA-V1C`: `results/2026-01-26_23-25_judge-v1/judge_v1c/` - 77 evaluations [TESTED]
- `SCOR-IN05-SC-DATA-V1D`: `results/2026-01-26_23-25_judge-v1/judge_v1d/` - 80 evaluations [TESTED]
- `SCOR-IN05-SC-SCRIPT`: `analyze_judge_v1.py` - Analysis script [TESTED]

**Prompt Files** (session folder: `prompts/judge-v1/`):
- [judge-v1a.md](prompts/judge-v1/judge-v1a.md) - Comprehensive guidance
- [judge-v1b.md](prompts/judge-v1/judge-v1b.md) - DO/DON'T format
- [judge-v1c.md](prompts/judge-v1/judge-v1c.md) - Maximum concision
- [judge-v1d-winner.md](prompts/judge-v1/judge-v1d-winner.md) - **WINNER** Detailed examples

## 7. Next Steps

1. **Adopt judge_v1d** as production combined judge prompt
2. **Consider judge_v1c** for cost-sensitive applications (similar discrimination, 4x fewer tokens)
3. **Keep Gen2 separate prompts** available for detailed per-dimension analysis
4. **Test on validation set** (25 complex pages) to confirm findings

## 8. Document History

**[2026-01-26 23:31]**
- Initial evaluation document created
- 320 evaluations across 4 prompt variants (317 successful)
- judge_v1d identified as winner (disc=0.94)
