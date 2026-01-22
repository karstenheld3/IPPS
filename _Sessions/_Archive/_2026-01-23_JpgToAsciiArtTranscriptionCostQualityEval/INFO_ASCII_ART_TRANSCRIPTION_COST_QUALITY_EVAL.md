<DevSystem MarkdownTablesAllowed=true />

# INFO: ASCII Art Transcription Cost/Quality Evaluation

**Doc ID**: TRNGFX-IN03
**Goal**: Determine optimal multimodal LLM for ASCII art transcription based on cost/quality tradeoff
**Timeline**: Created 2026-01-23

## Summary

**Key Finding**: GPT-5-mini ($0.017/image) offers best value - 98% of premium quality at 15% of cost.

**Copy/paste recommendations:**
- **Standard production**: Use GPT-5-mini at $0.017/image (3.48/5 quality)
- **Quality-critical**: Use GPT-5.2 at $0.047/image (3.56/5 quality, ties with Opus 4)
- **Avoid**: GPT-5, GPT-4o, Claude Haiku 3.5 (poor value or quality)

**Key findings**:
- GPT-5-mini achieves 6.5x better value than Claude Opus 4
- GPT-5.2 matches Opus 4 quality at 42% of cost
- All models fail on detailed graphics questions (hard_graphics: 0.9-2.6/5)
- Easy factual questions work reliably across all models (4.4-5.0/5)

## Initial Question

Which multimodal LLM provides the best cost/quality tradeoff for transcribing document images with ASCII art graphics?

**Sub-questions:**
1. How do premium models (Claude Opus 4, GPT-5, GPT-5.2) compare to mid-tier models?
2. Is the quality difference worth the cost premium?
3. Which model should be used for production transcription workflows?

## Approach

### Evaluation Pipeline

1. **Source**: Use existing transcription outputs (already generated from prior testing)
2. **Answerer**: GPT-5-mini generates answers to questions based on transcription content
3. **Judge**: GPT-5 scores answers 0-5 against reference answers
4. **Metrics**: Average score, pass rate (>=4/5), cost per quality point

### Test Configuration

**Images** (5 diverse types):
- `Edison-Financial-Report-2023-FY2023-Results_page004` - Financial charts/tables
- `SSE-Annual-Report-2024-Group-Risk-Report_page002` - Risk matrix diagram
- `Werner_2016_Stem_Cell_Networks_page014` - Scientific diagram
- `Microsoft-365-Copilot-Adotion-Playbook_page003` - Business infographic
- `Rent_Prices_Around_the_World_SITE-2` - Data visualization map

**Models evaluated** (8 total):
- Claude: Opus 4, Sonnet 4, Haiku 3.5
- OpenAI: GPT-5.2, GPT-5, GPT-5-mini, GPT-4.1, GPT-4o

**Runs**: 3 per image (run01, run02, run03)
**Questions**: 10 per image (50 total across 5 question categories)

### Question Categories

- **easy** (2/image): Basic facts, single values
- **medium_facts** (2/image): Combined facts, comparisons
- **medium_graphics** (2/image): Visual element interpretation
- **hard_semantics** (2/image): Meaning, relationships, dependencies
- **hard_graphics** (2/image): Detailed visual specifics (colors, shapes, counts)

## Results

### Quality Ranking

| Rank | Model | Quality | Pass Rate | Cost/Image |
|------|-------|---------|-----------|------------|
| 1 | Claude Opus 4 | 3.56/5 | 66% | $0.111 |
| 1 | GPT-5.2 | 3.56/5 | 66% | $0.047 |
| 3 | GPT-5-mini | 3.48/5 | 62% | $0.017 |
| 4 | GPT-5 | 3.38/5 | 64% | $0.100 |
| 5 | GPT-4.1 | 3.36/5 | 62% | $0.045 |
| 6 | Claude Sonnet 4 | 3.08/5 | 52% | $0.024 |
| 7 | GPT-4o | 2.80/5 | 48% | $0.038 |
| 8 | Claude Haiku 3.5 | 2.70/5 | 44% | $0.004 |

### Value Ranking (Quality per Dollar)

| Rank | Model | Value (pts/$) | Quality | Cost |
|------|-------|---------------|---------|------|
| 1 | Claude Haiku 3.5 | 675.0 | 2.70/5 | $0.004 |
| 2 | **GPT-5-mini** | **204.7** | **3.48/5** | **$0.017** |
| 3 | Claude Sonnet 4 | 128.3 | 3.08/5 | $0.024 |
| 4 | GPT-5.2 | 75.7 | 3.56/5 | $0.047 |
| 5 | GPT-4.1 | 74.7 | 3.36/5 | $0.045 |
| 6 | GPT-4o | 73.7 | 2.80/5 | $0.038 |
| 7 | GPT-5 | 33.8 | 3.38/5 | $0.100 |
| 8 | Claude Opus 4 | 32.1 | 3.56/5 | $0.111 |

### Performance by Question Category

| Category | Opus 4 | GPT-5.2 | GPT-5-mini | GPT-5 | Haiku |
|----------|--------|---------|------------|-------|-------|
| easy | 4.90 | 4.90 | 4.90 | 5.00 | 4.40 |
| medium_facts | 3.20 | 3.20 | 3.30 | 3.30 | 3.00 |
| medium_graphics | 3.80 | 3.20 | 3.20 | 3.10 | 2.50 |
| hard_semantics | 3.90 | 3.90 | 3.50 | 3.50 | 2.70 |
| hard_graphics | 2.00 | 2.60 | 2.50 | 2.00 | 0.90 |

### Performance by Image Type

| Image | Best Model | Score | Worst Model | Score |
|-------|------------|-------|-------------|-------|
| Microsoft Playbook | Opus 4 / GPT-5.2 | 4.60 | Haiku | 3.60 |
| Werner Scientific | GPT-5-mini / GPT-5.2 | 4.00 | Sonnet 4 | 2.80 |
| Edison Financial | GPT-4.1 | 4.10 | Haiku | 1.80 |
| SSE Risk Report | Opus 4 | 3.40 | Haiku | 2.30 |
| Rent Prices Map | Opus 4 | 2.30 | GPT-4o | 1.70 |

## Findings

### F1: GPT-5-mini offers best value

GPT-5-mini achieves 98% of premium model quality (3.48 vs 3.56) at 15% of the cost ($0.017 vs $0.111). This represents a **6.5x better value** than Claude Opus 4.

### F2: GPT-5.2 matches premium quality at mid-tier cost

GPT-5.2 ties with Claude Opus 4 at 3.56/5 quality while costing less than half ($0.047 vs $0.111). For quality-critical applications, GPT-5.2 is the better choice over Opus 4.

### F3: Premium GPT-5 offers no value advantage

GPT-5 scores lower (3.38) than GPT-5-mini (3.48) while costing 6x more ($0.100 vs $0.017). There is no scenario where GPT-5 is the optimal choice.

### F4: All models struggle with detailed graphics questions

Every model scored below 3.0/5 on hard_graphics questions (detailed visual specifics like colors, object counts, spatial relationships). This is a fundamental limitation of current ASCII art transcription approaches.

### F5: Easy factual questions work reliably

All models score 4.4-5.0/5 on easy questions, demonstrating that basic information extraction from transcriptions works well regardless of model choice.

### F6: Budget models have unacceptable quality drops

Claude Haiku 3.5 at $0.004/image seems attractive but loses 24% quality (2.70 vs 3.56). For document transcription where accuracy matters, this tradeoff is not acceptable.

### F7: GPT-4o underperforms its price tier

GPT-4o scores only 2.80/5 while costing more than GPT-5-mini ($0.038 vs $0.017). It offers neither quality nor value advantages.

## Recommendations

### Production Model Selection

| Use Case | Recommended Model | Cost | Quality |
|----------|-------------------|------|---------|
| **Standard production** | GPT-5-mini | $0.017 | 3.48/5 |
| **Quality-critical** | GPT-5.2 | $0.047 | 3.56/5 |
| **Maximum quality** | Claude Opus 4 | $0.111 | 3.56/5 |

### Models to Avoid

- **GPT-5**: No quality advantage over GPT-5-mini at 6x cost
- **GPT-4o**: Lower quality than GPT-5-mini at higher cost
- **Claude Haiku 3.5**: Quality too low for production use

### Workflow Implementation

For the transcription workflow with "best of 3" selection for pages with graphics:
1. Use GPT-5-mini as default transcription model
2. Generate 3 runs for pages containing complex graphics
3. Select best transcription (implementation TBD - not tested in this evaluation)

## Cost Analysis

**Evaluation budget spent**: ~$14 of $20 allocated

| Phase | Items | Estimated Cost |
|-------|-------|----------------|
| Answering (8 models x 50 questions) | 400 | ~$4 |
| Judging (8 models x 50 scores) | 400 | ~$10 |
| **Total** | 800 | ~$14 |

## Limitations

1. **Sample size**: 5 images x 3 runs = 15 transcriptions per model
2. **Question bias**: Questions generated by Claude Opus 4.1 from original images
3. **Judge bias**: GPT-5 as sole judge may favor OpenAI transcription patterns
4. **No variability analysis**: Did not test "best of 3" selection improvement

## Sources

- `TRNGFX-IN03-SC-LOCAL-RESULTS`: `_CostQualityEval/analysis_results.json`
- `TRNGFX-IN03-SC-LOCAL-SCORES`: `_CostQualityEval/scores/*/scores_gpt-5.json`
- `TRNGFX-IN03-SC-LOCAL-PRICING`: `DevSystemV3.2/skills/llm-evaluation/model-pricing.json`

## Document History

**[2026-01-23 00:35]**
- Initial report created
- 8 models evaluated: Opus 4, Sonnet 4, Haiku 3.5, GPT-5.2, GPT-5, GPT-5-mini, GPT-4.1, GPT-4o
- GPT-5-mini identified as best value, GPT-5.2 as quality leader among mid-tier
