# INFO: Transcription Prompt V1 Evaluation

**Doc ID**: SCOR-IN04
**Goal**: Document findings from evaluating 4 transcription prompt variants (v1a-v1d) for image-to-markdown conversion
**Timeline**: Created 2026-01-26

**Depends on:**
- `_SPEC_OPTIMIZED_TRANSCRIPTION.md [SCOR-SP02]` for prompt requirements

## Summary

- **v1b wins overall** with average score 4.19/5 across all dimensions [TESTED]
- **GPT-5-mini outperforms Claude_Sonnet_4** by ~1 point on average [TESTED]
- **DO/DON'T rules format** (v1b) more effective than detailed examples (v1d) [TESTED]
- **Concise prompts perform comparably** to verbose ones (v1c vs v1a) [TESTED]
- **Structure scores highest** (4.27-4.83) across all prompts [TESTED]
- **Graphics dimension most variable** (3.12-4.21), biggest differentiator [TESTED]

## Table of Contents

1. [Experiment Design](#1-experiment-design)
2. [Prompt Variants](#2-prompt-variants)
3. [Results](#3-results)
4. [Analysis](#4-analysis)
5. [Sources](#5-sources)
6. [Next Steps](#6-next-steps)
7. [Document History](#7-document-history)

## 1. Experiment Design

### 1.1 Objective

Test which transcription prompt style produces highest quality image-to-markdown transcriptions, measured by calibrated judge prompts from Gen2 evaluation.

### 1.2 Test Configuration

- **Images**: 2 complex document pages from `PageTranscriptionDataSet02/01_input_preflight/`
  - `DEU_21_VA_page009.jpg` - German energy report with charts
  - `edf-ddr-2017-accessible-version-en_page014.jpg` - EDF report page
- **Models**: GPT-5-mini, Claude_Sonnet_4
- **Runs**: 3 per image per model per prompt
- **Total transcriptions**: 72 (4 prompts x 2 models x 2 images x 3 runs)
- **Total scores**: 216 (72 transcriptions x 3 judge prompts)

### 1.3 Judge Prompts (from Gen2 winners)

- **text_c2**: Text accuracy with format tolerances
- **struct_b2**: Semantic outline matching
- **graphics_a2**: Essential graphics filter

## 2. Prompt Variants

### 2.1 v1a - Baseline with Backported Improvements

- **Length**: 206 lines
- **Style**: Explanatory sections with quality checklist
- **Features**: CRITICAL RULES section, `[unclear]` markers, multi-column handling, sidebar format
- **Philosophy**: Comprehensive guidance with explanations

### 2.2 v1b - DO/DON'T Rules Format

- **Length**: 134 lines
- **Style**: Explicit BAD/GOOD contrasts, prioritized rules
- **Features**: DO/DON'T section upfront, removed scoring weights, critical rules first
- **Philosophy**: Clear anti-patterns prevent common mistakes

### 2.3 v1c - Maximum Concision

- **Length**: 67 lines
- **Style**: Imperative statements, minimal examples
- **Features**: All FR requirements covered in compact format
- **Philosophy**: LLMs don't need verbose explanations

### 2.4 v1d - Detailed Examples

- **Length**: 156 lines
- **Style**: BAD/GOOD contrasts for every rule
- **Features**: 10 concrete examples, special characters guidance, table handling
- **Philosophy**: One good example worth many instructions

## 3. Results

### 3.1 Overall Scores by Prompt

- **v1b**: text=3.83, struct=4.54, graphics=4.21, **avg=4.19**
- **v1c**: text=3.75, struct=4.83, graphics=3.58, avg=4.06
- **v1a**: text=3.67, struct=4.79, graphics=3.12, avg=3.86
- **v1d**: text=3.67, struct=4.27, graphics=3.50, avg=3.81

### 3.2 Scores by Model

**GPT-5-mini:**
- v1b: text=4.83, struct=4.50, graphics=4.75, **avg=4.69**
- v1d: text=4.50, struct=5.00, graphics=4.17, avg=4.56
- v1c: text=4.83, struct=5.00, graphics=3.67, avg=4.50
- v1a: text=4.75, struct=4.67, graphics=3.42, avg=4.28

**Claude_Sonnet_4:**
- v1b: text=2.83, struct=4.58, graphics=3.67, **avg=3.69**
- v1c: text=2.67, struct=4.67, graphics=3.50, avg=3.61
- v1a: text=2.58, struct=4.92, graphics=2.83, avg=3.44
- v1d: text=2.83, struct=3.40, graphics=2.83, avg=3.02

### 3.3 Score Distribution by Dimension

**Text Accuracy:**
- Range: 3.67 - 3.83
- Lowest variance dimension
- GPT-5-mini significantly better than Claude (4.73 vs 2.73 avg)

**Structure:**
- Range: 4.27 - 4.83
- Highest scores across all prompts
- Both models perform well (4.79 GPT vs 4.39 Claude)

**Graphics:**
- Range: 3.12 - 4.21
- Highest variance dimension
- Biggest differentiator between prompt styles

## 4. Analysis

### 4.1 Why v1b Won

1. **DO/DON'T format prevents mistakes**: Explicit anti-patterns catch common errors that verbose descriptions miss
2. **Prioritized rules**: Critical rules first ensures LLM attention
3. **Removed scoring weights**: Simplified instructions reduce confusion
4. **Balanced length**: 134 lines - enough detail without overwhelming

### 4.2 Why v1d Underperformed

1. **Example overload**: 10 BAD/GOOD examples may dilute focus
2. **Table usage**: Markdown table in prompt (L11-14) may confuse some models
3. **Excessive detail**: More instructions created more opportunities for partial compliance
4. **Length penalty**: 156 lines approaches attention threshold

### 4.3 Why v1c Performed Well

1. **Concision works**: 67 lines covered all requirements effectively
2. **Imperative style**: Direct commands clear for LLMs
3. **One example per concept**: Sufficient without overload
4. **Close second to v1b**: Only 0.13 points behind

### 4.4 Model Performance Gap

**GPT-5-mini advantage:**
- Text: +2.0 points over Claude
- Structure: +0.4 points
- Graphics: +0.7 points

**Possible causes:**
- GPT-5-mini better at instruction following
- Claude thinking tokens may not help transcription tasks
- Different tokenization of special characters

### 4.5 Dimension Insights

**Structure highest**: All prompts clearly convey header hierarchy requirements

**Graphics most variable**: Essential vs decorative distinction requires judgment - prompt style significantly impacts this

**Text most model-dependent**: Character-level accuracy more model capability than prompt design

## 5. Sources

**Primary Sources:**
- `SCOR-IN04-SC-DATA-TRANS`: `LLMResearch/PageTranscriptionDataSet02/03_transcriptions1/` - 72 transcription outputs [TESTED]
- `SCOR-IN04-SC-DATA-SCORE`: `LLMResearch/PageTranscriptionDataSet02/03_transcriptions1_scores/` - 216 score JSONs [TESTED]
- `SCOR-IN04-SC-SCRIPT`: `LLMResearch/PageTranscriptionDataSet02/analyze_scores.py` - Analysis script [TESTED]

**Related Documents:**
- `_SPEC_OPTIMIZED_TRANSCRIPTION.md [SCOR-SP02]` - Prompt requirements
- `_INFO_GEN2_PROMPT_EVALUATION.md [SCOR-IN02]` - Judge prompt calibration
- `_INFO_GEN2_GEN3_VALIDATION.md [SCOR-IN03]` - Judge prompt validation

**Prompt Files** (session folder: `prompts/transcription-v1/`):
- [transcription-prompt-1a.md](prompts/transcription-v1/transcription-prompt-1a.md) - Baseline with backported improvements
- [transcription-prompt-1b-winner.md](prompts/transcription-v1/transcription-prompt-1b-winner.md) - **WINNER** DO/DON'T rules format
- [transcription-prompt-1c.md](prompts/transcription-v1/transcription-prompt-1c.md) - Maximum concision
- [transcription-prompt-1d.md](prompts/transcription-v1/transcription-prompt-1d.md) - Detailed examples

## 6. Next Steps

1. **Adopt v1b as production prompt** for image-to-markdown transcription
2. **Use GPT-5-mini** as primary transcription model
3. **Test on larger dataset** (full 25 images from PageTranscriptionDataSet02)
4. **Consider v1c for cost optimization** if token limits become concern
5. **Investigate Claude underperformance** - may need model-specific prompt tuning

## 7. Document History

**[2026-01-26 23:14]**
- Added prompt files section with relative links to session folder

**[2026-01-26 23:09]**
- Initial evaluation document created
- 72 transcriptions scored across 3 dimensions
- v1b identified as winner (4.19 avg)
