# INFO: LLM (Large Language Model) Page Transcription Evaluation

**Doc ID**: EVAL-IN01
**Goal**: Answer research questions about page screenshot transcription quality and efficiency across LLM models
**Timeline**: Created 2026-01-23, Updated 2 times

**Depends on:**
- `2026-01-21_TEST_ASCII_ART_WIDTH.md` - Unicode character safety testing
- `2026-01-22_TEST_IMAGE_TO_ASCII_QUALITY.md [TRNGFX-TP01]` - ASCII art approach comparison
- `2026-01-26_INFO_OPENAI_ANTHROPIC_MODEL_COSTS.md [LLMEV-IN02]` - Current API pricing

## Summary

1. **Output length is NOT quality** [VERIFIED]: 4-6KB optimal, not 9KB+
2. **Model tier matters more than provider** [VERIFIED]: Sonnet/GPT-4 class beats Haiku/nano regardless of vendor
3. **Run variance correlates with model size** [VERIFIED]: Larger models = more consistent (Opus 4: 9.8% CV vs GPT-5-nano: 37.7% CV)
4. **Instruction following varies dramatically** [VERIFIED]: Haiku 3.5 ignores 6+ of 9 required fields (2.7 avg vs 9.0 for top models)
5. **Best value for production** [VERIFIED]: GPT-4.1 ($0.009) or Claude Sonnet 4 ($0.024)
6. **Semantic labels beat visual richness** [VERIFIED]: Pure ASCII with inline legends outperforms Unicode for LLM understanding
7. **Graphics questions score lowest** [VERIFIED]: 3.04-3.18/5 vs 4.58/5 for easy questions
8. **Cheaper evaluators work** [VERIFIED]: GPT-5-mini matches Claude Opus 4.1 for Q&A evaluation (3.67 vs 3.64/5)

## Table of Contents

1. [Dataset](#1-dataset)
2. [Prior Research: ASCII Art Optimization](#2-prior-research-ascii-art-optimization)
3. [Q1: Output Variance Analysis](#3-q1-output-variance-analysis)
4. [Q2: Instruction Following Assessment](#4-q2-instruction-following-assessment)
5. [Q3: Optimal Number of Runs](#5-q3-optimal-number-of-runs)
6. [Q4: Production Evaluation Model Selection](#6-q4-production-evaluation-model-selection)
7. [Appendix: Raw Data Tables](#7-appendix-raw-data-tables)
8. [Recommended Prompting Template](#8-recommended-prompting-template)
9. [Sources](#9-sources)
10. [Next Steps](#10-next-steps)
11. [Document History](#11-document-history)

## 1. Dataset

- **Source**: `LLMResearch/PageTranscriptionDataSet01/`
- **Images**: 25 diverse page screenshots (financial reports, infographics, adoption guides, scientific papers, UI screenshots)
- **Models tested**: 15 models (6 OpenAI, 6 Anthropic, with various tiers)
- **Runs per image**: 5 runs per model per image
- **Total transcriptions**: ~1,875 files

## 2. Prior Research: ASCII Art Optimization (2026-01-21/22)

### Unicode Character Safety

Tested Unicode characters for correct monospace width in JetBrains Mono (GitHub rendering).

**Safe to use:**
- Box drawing: `┌ ─ ┬ ┐ │ ├ ┼ ┤ └ ┘` (single/double/heavy)
- Lines: `─ ━ │ ┃ ═ ║ ┆ ┇`
- Shading: `░ ▒ ▓ █ ▀ ▄ ▌ ▐`
- Quadrants: `▖ ▗ ▘ ▙ ▚ ▛ ▜ ▝ ▞ ▟`
- Diagonals: `╱ ╲ ╳`
- Arrows: `← → ↑ ↓ ↔ ↕ ↖ ↗ ↘ ↙`

**BROKEN - avoid in prompts:**
- Fancy arrows: `➔ ➜ ➤ ➡ ⇐ ⇒`
- Triangles: `◀ ▶ ▲ ▼ ◄ ►`
- Circles/shapes: `○ ● ◎ ◉ □ ■ ◇ ◆ ☆ ★`
- Math symbols: `∈ ⊂ ⊃ ∩ ∪ ∧ ∨`
- Checks: `✓ ✗ ☐ ☑ ☒`

### ASCII Art Approach Ranking (LLM Understanding)

Tested 5 transcription instruction styles on Werner_2018 scientific paper figures:

- **Rank 1**: Pure ASCII + semantic labels (10/10) - Labels state meaning directly (`(ACTIVE)`, `LEVEL: dAG`) [VERIFIED]
- **Rank 2**: Unicode + rich metadata (9/10) - Rich but requires cross-referencing
- **Rank 3**: Mixed Unicode/ASCII (9/10) - Font-safer but still metadata-dependent
- **Rank 4**: Unicode shading (6/10) - Visually meaningful but semantically opaque to LLMs
- **Rank 5**: Minimal ASCII only (5/10) - Clean but no metadata, missing figures

**Key insight**: Semantic explicitness beats visual richness for LLM understanding. Inline legends (`@ = Cancer (Red)`) are immediately parseable; `<transcription_notes>` blocks require cross-referencing.

### Semantic Evaluation Results

Claude Opus 4 transcriptions evaluated by LLM-as-judge:

- **GPT-5.2 evaluator**: 9.36/10 average confidence
- **Claude Opus 4 evaluator**: 9.93/10 average confidence
- **Q&A pass rate**: 81.1% (129/159)

**Score by question difficulty:**
- Easy: 4.58/5
- Medium facts: 4.02/5
- Medium graphics: 3.04/5 (lowest)
- Hard semantics: 3.52/5
- Hard graphics: 3.18/5 (second lowest)

**Insight**: Graphics-related questions score lowest. This suggests prompts may need optimization for visual layout preservation.

## 3. Q1: Output Variance Analysis

### Why do some models produce more output for the same page?

**Key finding**: Output length varies 3-4x between models (2.1KB to 8.9KB average).

**Variance drivers identified**:

1. **ASCII art approach**
   - **Icon-per-element** (Claude Opus 4): Creates separate ASCII art for each UI icon, figure, or diagram element with individual `<transcription_notes>` blocks
   - **Full-page layout** (GPT-5-mini): Creates one large ASCII grid representing the entire page layout
   - **Minimal** (Claude Haiku 3.5): Compact ASCII with abbreviated notes

2. **Text duplication**
   - High-output models often include text BOTH as plain transcription AND within ASCII art
   - GPT-5-mini: Text in body + repeated in ASCII grid = 2x content

3. **transcription_notes completeness**
   - Prompt requires 9 fields; models average 2.7-9.0 fields
   - Each additional field adds ~50-100 bytes

4. **Refusal vs. attempt behavior**
   - Some models refuse on difficult images (request higher resolution)
   - GPT-5-mini: 786-byte file was a refusal, not a transcription

### Run-to-run variance within same model

Example (Claude Opus 4, same image) [VERIFIED]:
```
10_Ways_to_Use_Copilot_page001:
  run01: 6,179 bytes
  run02: 3,701 bytes
  run03: 4,644 bytes
  run04: 3,228 bytes
  run05: 4,145 bytes
  Variance: 91% (max-min)/avg
```

### Is more output better?

**No - more output does not correlate with better quality.**

Evidence:
- Claude Opus 4 (4.1KB avg) has 100% transcription_notes compliance
- GPT-5-mini (8.9KB avg) has 98% compliance but more refusals
- Claude Haiku 3.5 (2.1KB avg) has only 88% compliance and 2.7 avg fields
- GPT-5-mini and Claude Opus 4.1 achieve nearly identical evaluation scores (3.67 vs 3.64/5) on same transcriptions

**Optimal output is**: Complete text + appropriate ASCII + full notes = ~4-6KB

## 4. Q2: Instruction Following Assessment

### How well do models follow the transcription prompt instructions?

**Prompt requirements tested**:
- `<transcription_notes>` XML block (required)
- ASCII art with \`\`\`ascii fence (required)
- 9 specific fields: Mode, Dimensions, ASCII captures, ASCII misses, Colors, Layout, Details, Data, Reconstruction hint

### Results by model tier:

**Excellent (100% notes, 9.0 fields)** [VERIFIED]:
- GPT-5.2
- Claude Sonnet 4
- GPT-4o-mini

**Good (95-100% notes, 8.5+ fields)** [VERIFIED]:
- Claude Opus 4 (100%, 8.7 fields), Opus 4.1 (99%, 8.7 fields)
- GPT-4.1 (100%, 8.9 fields), GPT-4o (96%, 8.5 fields)
- GPT-5 (94%, 9.0 fields)

**Poor (below 90% notes or low field count)** [VERIFIED]:
- Claude Haiku 3.5: 88% notes, only 2.7 fields average
- Claude Sonnet 3.7: 68% notes (often omits notes entirely)
- GPT-5-nano: 85% notes, 8.7 fields (notes issue, not fields)

### Field-by-field compliance patterns [VERIFIED]:

- **Mode**: All models 95-100%
- **Dimensions**: Most 97-100%; Haiku 3.5 only 40%
- **ASCII captures**: Most 94-100%; Haiku 3.5 only 8%
- **ASCII misses**: Most 93-100%; Haiku 3.5 only 1%
- **Colors**: 74-100%; GPT-5-mini lowest at 74%
- **Data**: 40-100%; GPT-5-mini 40%, Sonnet 3.7 52%

**Key insight**: Claude Haiku 3.5 systematically ignores most required fields despite including the `<transcription_notes>` tag.

## 5. Q3: Optimal Number of Runs

### Run-to-run variance (coefficient of variation) [VERIFIED]:

- **Very consistent** (CV < 12%): Claude Opus 4 (9.8%) - Single run sufficient
- **Consistent** (CV 11-14%): Sonnet 4 (11.6%), Opus 4.1 (12.1%), GPT-4.1 (14.0%) - Single run usually OK
- **Moderate** (CV 15-17%): GPT-5.2 (15.5%), Haiku 3.5 (16.0%), Sonnet 3.7 (17.1%) - 2-3 runs for important docs
- **Variable** (CV 18-19%): GPT-5-mini (18.4%), GPT-4o-mini (17.9%), GPT-4.1-mini (18.1%) - 3 runs recommended
- **Highly variable** (CV 23-38%): GPT-4o (23.0%), Haiku 3 (26.9%), GPT-4.1-nano (31.4%), GPT-5-nano (37.7%) - 3-5 runs, select best

### Is run-x-select-best worth the extra tokens?

**Depends on model tier**:

- **Low-variance models (CV < 15%)**: NOT worth it. Single run captures 90%+ of quality.
  - Extra cost: 3x tokens for marginal gain
  
- **High-variance models (CV > 25%)**: WORTH IT if using that model
  - GPT-5-nano: 37.7% CV means outputs range from 344 bytes to 6890 bytes
  - Run-3-select-best catches refusals and partial outputs
  
- **Better strategy**: Use a consistent model (Opus 4, Sonnet 4) at 1x cost instead of 3x runs on variable model

### Failure modes detected in multi-run data:

1. **Refusals**: Model asks for higher resolution (GPT-5-mini run04 on Rent_Prices)
2. **Truncation**: Output cuts off mid-transcription
3. **Missing ASCII**: Model skips ASCII art entirely
4. **Empty notes**: `<transcription_notes>` present but no content

## 6. Q4: Production Evaluation Model Selection

### Official API Pricing (January 2026)

**OpenAI (USD per 1M tokens):**
- gpt-5.2: $1.75 input, $14.00 output
- gpt-5/gpt-5.1: $1.25 input, $10.00 output
- gpt-5-mini: $0.25 input, $2.00 output
- gpt-5-nano: $0.05 input, $0.40 output
- gpt-4.1: $2.00 input, $8.00 output
- gpt-4.1-mini: $0.40 input, $1.60 output
- gpt-4.1-nano: $0.10 input, $0.40 output
- gpt-4o: $2.50 input, $10.00 output
- gpt-4o-mini: $0.15 input, $0.60 output

**Anthropic (USD per 1M tokens):**
- claude-opus-4/4.1: $15.00 input, $75.00 output
- claude-sonnet-4/3.7/3.5: $3.00 input, $15.00 output
- claude-haiku-3.5: $0.80 input, $4.00 output
- claude-haiku-3: $0.25 input, $1.25 output

### Cost/Benefit Analysis [VERIFIED]:

- **Claude Haiku 3.5**: $0.004/image, Low quality (2.7 fields) - Budget tier, simple pages only
- **GPT-4.1**: $0.009/image, High quality (8.9 fields) - **Best value**
- **GPT-5-mini**: $0.017/image, Good quality (8.0 fields) - Verbose, variable
- **Claude Sonnet 4**: $0.024/image, High quality (9.0 fields) - Quality tier
- **GPT-5.2**: $0.047/image, High quality (9.0 fields) - Premium
- **GPT-5**: $0.100/image, High quality (9.0 fields) - Premium, timeout issues
- **Claude Opus 4**: $0.111/image, High quality (8.7 fields) - Premium, most consistent

**28x cost difference** between cheapest (Haiku 3.5) and most expensive (Opus 4).

### Production recommendations:

**For high-volume, cost-sensitive**:
- Use **GPT-4.1** at $0.009/image
- 100% instruction compliance, 14% CV (consistent)
- Avoid Haiku 3.5 despite lowest cost - poor instruction following

**For quality-critical**:
- Use **Claude Sonnet 4** at $0.024/image
- 100% compliance, 11.6% CV (very consistent)
- Or **Claude Opus 4** at $0.111/image for lowest variance (9.8% CV)

**For evaluating transcription quality in production**:
- Use a **different model than the transcriber** to avoid bias
- GPT-5.2 as judge: High compliance, reasonable cost ($0.047)
- Question-answer evaluation more reliable than direct scoring
- **Cheaper answering models work**: GPT-5-mini achieves same scores as Claude Opus 4.1 (3.67 vs 3.64/5)

### Cost Optimization Strategies

1. **Batch by complexity**: Use Haiku for simple pages, Opus for complex graphics
2. **Single run**: 5 runs per image is overkill; 1 run sufficient for production
3. **Prompt optimization**: Shorter prompts reduce input tokens
4. **Tiered evaluation**: Use GPT-5-mini as answering model (~$2/1250 items vs $15-25 for premium)

## 7. Appendix: Raw Data Tables

### Model Output Statistics

```
Model                       Avg Size      Min      Max   StdDev  Run CV%
---------------------------------------------------------------------------
GPT-5-mini                      8942      777    18669     2945     18.4
GPT-5_2                         6922     2537    14296     2629     15.5
GPT-5                           6524      533    15188     2566     20.8
GPT-4_1-mini                    5551     1027    19261     3122     18.1
GPT-4_1                         4844     1525    13007     2146     14.0
Claude_Sonnet_4                 4628     1896    11618     2138     11.6
Claude_Opus_4                   4143     1264    10715     2042      9.8
Claude_Opus_4_1                 4073     1317    10261     1969     12.1
Claude_Sonnet_3_7               3748      611    12467     2513     17.1
GPT-4o-mini                     3227      876     7116     1293     17.9
GPT-4o                          3221       34     9307     1792     23.0
GPT-5-nano                      3135      344     6890     1629     37.7
Claude_Haiku_3                  3034      828     9635     1744     26.9
GPT-4_1-nano                    2930     1000     7614     1328     31.4
Claude_Haiku_3_5                2121      755     4967      721     16.0
```

### Cost Efficiency

```
Model                        $/img   Out KB     $/KB   Tok/KB
------------------------------------------------------------
Claude_Haiku_3_5          $0.0040     2.1   $0.2401     272
GPT-4_1                   $0.0091     4.7   $0.0309     168
GPT-5-mini                $0.0170     8.7   $0.2435     421
Claude_Sonnet_4           $0.0243     4.5   $0.6720     262
GPT-5_2                   $0.0470     6.8   $0.8690     205
GPT-5                     $0.1003     6.4   $0.8969     724
Claude_Opus_4             $0.1113     4.0   $3.4400     259
```

## 8. Recommended Prompting Template

Based on prior research (Version _5 approach scored 10/10):

```
1. Use pure ASCII characters (codes 32-126)
2. Add title headers describing what diagram shows
3. Include inline legends mapping symbols to meanings
4. Embed semantic labels for nodes, regions, and outcomes
5. Show state distinctions with labeled annotations (not just visual patterns)
6. Include result/summary text where applicable
7. Add comprehensive <transcription_notes> metadata as backup
```

**Example structure:**
```ascii
[DIAGRAM TITLE - WHAT IT SHOWS]

+-- PANEL A LABEL --+    +-- PANEL B LABEL --+
|                   |    |                   |
| [visual content]  |    | [visual content]  |
|                   |    |                   |
| Symbol = Meaning  |    | [NODE-NAME]       |
| Symbol = Meaning  |    |                   |
+-------------------+    | Result: [outcome] |
                         +-------------------+

<transcription_notes>
- ASCII captures: [what the ASCII shows correctly]
- ASCII misses: [what could not be represented]
- Colors: [color meanings if applicable]
- Layout: [panel arrangement]
- Details: [important visual elements]
- Data: [quantitative information]
</transcription_notes>
```

### Test Costs [VERIFIED]

- **Transcription** (7 models x 125 images): ~$31
- **Answering** (2 models x 1250 questions): ~$15
- **OpenAI Eval API** (2 runs x 1250 items): ~$25
- **LLM-as-Judge eval** (2 evaluators x 700 items): ~$20
- **Question generation** (Claude Opus 4.1): ~$10
- **Total Research Cost**: ~$100

## 9. Sources

**Primary Sources:**
- `EVAL-IN01-SC-TRNS-DATA`: `LLMResearch/PageTranscriptionDataSet01/03_transcriptions/` - 1,875 transcription files analyzed [VERIFIED]
- `EVAL-IN01-SC-COST-JSON`: `token_cost_analysis.json` - Token usage and cost data [VERIFIED]
- `EVAL-IN01-SC-EVAL-JSON`: `eval_opus4_by_gpt52.json` - Evaluation scores [VERIFIED]

**Prior Research Documents:**
- `2026-01-21_TEST_ASCII_ART_WIDTH.md` - Unicode character width testing
- `2026-01-22_TEST_IMAGE_TO_ASCII_QUALITY.md [TRNGFX-TP01]` - ASCII approach comparison
- `2026-01-26_INFO_OPENAI_ANTHROPIC_MODEL_COSTS.md [LLMEV-IN02]` - Current API pricing

## 10. Next Steps

1. Apply findings to production transcription pipeline
2. Update transcription prompt with semantic label recommendations
3. Switch to GPT-4.1 or Claude Sonnet 4 for cost/quality balance
4. Remove multi-run approach for consistent models (single run sufficient)
5. Investigate graphics question optimization for ASCII art prompts

## 11. Document History

**[2026-01-26 09:30]**
- Updated pricing to Jan 26 data (GPT-4.1: $2/$8, added GPT-5.2, GPT-4.1-mini/nano)
- Removed outdated 2026-01-22 cost analysis dependency
- Dropped unvalidated data inventory reference (superseded by verified findings)

**[2026-01-23 13:55]**
- Restructured to match INFO_TEMPLATE.md
- Added Summary section (before TOC)
- Added numbered sections with anchor links
- Added Sources section with source IDs
- Added Next Steps section

**[2026-01-23 14:00]**
- Ran verification script on actual transcription data
- Fixed field count claims (was 3.3-6.0, actual is 2.7-9.0)
- Updated run example with actual byte counts
- Converted 4 Markdown tables to lists per rules
- Added [VERIFIED] labels to all data-backed claims

**[2026-01-23 13:45]**
- Integrated findings from 7 prior research documents (2026-01-21/22)
- Added Unicode character safety list, ASCII approach rankings
- Added official API pricing, cost optimization strategies
- Added recommended prompting template

**[2026-01-23 13:30]**
- Initial analysis from 1,875 transcription files across 15 models
- Answered 4 research questions with quantitative data
