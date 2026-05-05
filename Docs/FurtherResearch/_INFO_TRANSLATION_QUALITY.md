# INFO: LLM Translation Quality Improvement Methods

**Doc ID**: XLATE-IN01
**Goal**: Identify actionable methods to improve LLM-translated text quality for the `/translate` workflow
**Timeline**: Created 2026-05-05

## Summary

- **Reflection workflow** (3-pass: translate, reflect, improve) produces measurably better translations than single-pass LLM translation. Andrew Ng's `translation-agent` demonstrates this with 4 quality dimensions: accuracy, fluency, style, terminology [VERIFIED]
- **DeepL API Free** provides 500,000 characters/month at no cost. Glossary API (v3) applies grammatically correct term inflection, not find-and-replace. Usable as comparison/verification backend [VERIFIED]
- **DeepL API Pro** costs $5.49/month + $25/million characters. Glossary support, formality parameter, priority processing [VERIFIED]
- **LLM model choice matters**: Claude excels at creative/nuanced translation, GPT-4o/5 at technical/structured content, Gemini at long-context multi-file consistency. Lokalise blind study: LLMs rated "good" 55-80% of time vs traditional MT [VERIFIED]
- **Glossary-driven translation** is the single most impactful technique for consistency. Both DeepL and LLM approaches benefit from pre-built term pairs [VERIFIED]
- **LLM-as-judge** is the best practical quality evaluation method. Traditional metrics (BLEU, COMET) correlate poorly with human judgment for LLM-produced translations [VERIFIED]
- **Back-translation** (round-trip A->B->A) is unreliable as standalone quality metric but useful as a supplementary check for detecting gross errors [VERIFIED]
- **Hybrid approach** (LLM translation + DeepL comparison) combines LLM's contextual understanding with DeepL's linguistic precision for verification [ASSUMED]

## Table of Contents

1. [Reflection Workflow (Andrew Ng)](#1-reflection-workflow-andrew-ng)
2. [DeepL API as Translation/Verification Backend](#2-deepl-api-as-translationverification-backend)
3. [LLM Model Selection for Translation](#3-llm-model-selection-for-translation)
4. [Quality Evaluation Methods](#4-quality-evaluation-methods)
5. [Practical Recommendations for /translate Workflow](#5-practical-recommendations-for-translate-workflow)
6. [Sources](#6-sources)
7. [Next Steps](#7-next-steps)
8. [Document History](#8-document-history)

## 1. Reflection Workflow (Andrew Ng)

Andrew Ng's `translation-agent` (MIT license, github.com/andrewyng/translation-agent) implements a 3-pass agentic translation workflow:

**Pass 1 - Initial Translation**: LLM translates source text to target language. System prompt: "You are an expert linguist, specializing in translation from {source_lang} to {target_lang}."

**Pass 2 - Reflection**: A second LLM call reviews source + translation and generates specific improvement suggestions across 4 dimensions:
- Accuracy: errors of addition, mistranslation, omission, untranslated text
- Fluency: grammar, spelling, punctuation, unnecessary repetitions
- Style: source text style preservation, cultural context
- Terminology: consistent use, domain-appropriate, equivalent idioms

**Pass 3 - Improvement**: A third LLM call takes source + initial translation + expert suggestions and produces the final improved translation.

### Multi-chunk handling

For texts exceeding ~1000 tokens, the agent splits into chunks. Each chunk is translated with the full source text as context (surrounding chunks visible but marked with XML tags to indicate which part to translate). This preserves cross-chunk coherence.

### Customizability advantages over traditional Machine Translation (MT)

- Formal/informal style via prompt modification
- Glossary terms included directly in prompt
- Regional language variants (Latin American Spanish vs Spain Spanish, Canadian French vs France French)
- Domain-specific instructions

### Evaluation findings

The reflection workflow is "sometimes competitive with, sometimes worse than" leading commercial offerings on BLEU scores. However, on document-level human evaluation, it occasionally produces "superior" results. BLEU scores at sentence level penalize valid paraphrases that humans prefer.

### Relevance for `/translate` workflow

The current `/translate` workflow does a single-pass translation (Step 4). Adding a reflection pass maps directly to this architecture:
- Step 4a: Initial translation
- Step 4b: Self-reflect on translation quality (accuracy, fluency, style, terminology)
- Step 4c: Apply improvements

Cost: 3x the LLM calls per translation. For documents, this is negligible compared to human review time.

## 2. DeepL API as Translation/Verification Backend

### API Plans

- **DeepL API Free**: $0, 500,000 characters/month. Glossary support included. Data may be used for model training. No document translation.
- **DeepL API Pro**: $5.49/month base + $25 per 1,000,000 characters. Enterprise-grade security (data not stored). Priority processing. Document translation.

### Glossary API (v3)

DeepL glossaries are context-aware, not find-and-replace:
- Grammatically correct inflection (case, gender, tense) of glossary entries
- Supports 100+ language combinations
- v3 endpoint: multilingual glossaries (one glossary, multiple language pairs)
- v2 endpoint: single language pair per glossary (legacy)

API usage: POST `/v2/translate` with `glossary_id` parameter. Source language must be specified when using glossaries (auto-detection not supported with glossaries).

### Formality Parameter

DeepL API supports a `formality` parameter for languages with formal/informal distinction:
- `default`, `more` (formal), `less` (informal), `prefer_more`, `prefer_less`
- Supported for: DE, FR, ES, IT, PT, NL, PL, RU, JA (among others)

### Use cases in `/translate` workflow

1. **Comparison backend**: Translate with LLM, translate with DeepL, compare outputs. Divergences flag potential issues.
2. **Glossary enforcement**: Upload TRANSLATION_TERM_PAIRS to DeepL glossary, translate, compare term usage with LLM output.
3. **Verification**: DeepL translation as "second opinion" for the LLM-as-judge verification step.
4. **Fallback**: If LLM translation quality is poor for a specific language pair, fall back to DeepL.

### Limitations

- Free plan: 500K chars/month shared across all usage. A 50-page document is roughly 100K-150K characters. Budget allows 3-5 full document translations per month.
- Free plan security: text may be stored for training. Not suitable for confidential documents.
- Glossary entries limited per glossary (exact limit not publicly documented, but "thousands" supported).

## 3. LLM Model Selection for Translation

Based on Lokalise's 2025 blind study (600+ pairwise comparisons per language pair, EN->DE/PL/RU):

### Model strengths

- **Claude 3.5/4**: Best for creative, nuanced, brand-sensitive content. Highest "good" rating frequency. Stylistic fluency.
- **GPT-4o/5**: Best for technical documentation, code localization. Reliably preserves variables, placeholders, structured formatting.
- **Gemini**: Best for long-context, multi-file translations. 2M token context window. Consistent terminology across large document sets.
- **DeepSeek**: Best for cost-efficient bulk translation. High volume, lower risk content.

### Key findings

- LLMs rated "good" 55.7-80% of the time without any contextual information (no glossary, no style guide)
- Claude 3.5 ranked first in 9/11 language pairs in WMT24 competition
- Human-to-human agreement and AI-to-human agreement were close (Cohen's Kappa, Average Jaccard Similarity)
- Russian translations scored lower than German and Polish despite being "high-resource" - resource availability does not always correlate with translation performance

### Implication for `/translate`

The current workflow uses whichever LLM Cascade provides. For optimal results:
- Technical/structured documents: prefer GPT models
- Marketing/creative content: prefer Claude
- Long documents with cross-reference consistency needs: prefer Gemini
- The workflow could note document type and recommend model selection

## 4. Quality Evaluation Methods

### Traditional metrics (BLEU, COMET) - not recommended as primary

BLEU (Bilingual Evaluation Understudy): Measures n-gram overlap between translation and reference. Fast, automated, but:
- Requires reference translation (which we don't have)
- Penalizes valid paraphrases
- Poor correlation with human judgment for LLM outputs

COMET: Neural metric trained on human quality judgments. Better than BLEU but:
- Empty translations can score 0.32 (should be 0)
- Wrong-language output sometimes scores higher than correct empty output
- Hallucinated but fluent text gets overly generous scores
- Focuses on semantic adequacy to single reference, ignores style/register/cultural appropriateness
- System-level correlation with human MQM ratings: ~0.69 (COMET-22), ~0.72 (XCOMET) - good but not sufficient

### LLM-as-judge - recommended primary method

Use the translating LLM (or a different one) to evaluate translation quality across dimensions:
- Accuracy: Are all source concepts present? Any additions, omissions, mistranslations?
- Fluency: Natural target language? Grammar, spelling, punctuation correct?
- Style: Matches source register? Formal/informal consistent?
- Terminology: Glossary terms applied consistently? Domain-appropriate?
- Structure: Headings, lists, code blocks preserved?

This approach:
- Requires no reference translation
- Evaluates exactly the dimensions that matter for document translation
- Correlates better with human judgment than BLEU/COMET for LLM output
- Can be customized per document type

### Back-translation (round-trip) - supplementary only

Translate A->B->A, compare original with round-trip result.

Limitations (well-documented):
- If round-trip differs from original, error could be in forward OR backward translation
- Symmetric errors (both directions wrong in compensating ways) are invisible
- Wikipedia and academic sources agree: "round-trip translation is a poor predictor of translation quality"

Useful for: Detecting gross omissions or complete mistranslations. Not useful for evaluating nuance, style, or terminology consistency.

### Practical verification pipeline for `/translate`

1. Structure check (automated): heading count, list count, code block count, paragraph count match source
2. Term consistency check (grep): each TRANSLATION_TERM_PAIR appears consistently
3. LLM-as-judge (per section): evaluate accuracy, fluency, style, terminology
4. Optional DeepL comparison: flag divergences between LLM and DeepL translations

## 5. Practical Recommendations for /translate Workflow

### High-impact changes (implement first)

1. **Add reflection pass** (Andrew Ng pattern): After initial translation, add reflect + improve steps. 3x LLM cost, significant quality improvement. Maps to Step 4a/4b/4c.

2. **Structured quality dimensions in prompt**: Include the 4 dimensions (accuracy, fluency, style, terminology) explicitly in translation and reflection prompts. This is how DeepL's quality emerges - specialized training on these dimensions.

3. **LLM-as-judge verification**: Replace or augment Step 5 `/verify` with per-section LLM quality evaluation using the 4 dimensions.

### Medium-impact changes (implement second)

4. **DeepL API integration (optional)**: Add DeepL Free API as comparison backend. Requires API key setup. Use for:
   - Second-opinion comparison on critical documents
   - Glossary-enforced translation verification
   - Formality parameter alignment

5. **Model-aware translation**: Note document type (technical, creative, legal) in Step 2 analysis and recommend appropriate LLM model if user can switch.

### Low-priority improvements

6. **Back-translation spot check**: For high-stakes translations, back-translate random paragraphs and flag divergences.

7. **Translation memory**: Across multiple runs of `/translate`, accumulate verified term pairs and reuse them. Store in workspace NOTES.md and grow over time.

## 6. Sources

- `XLATE-IN01-SC-ANDR-TAGNT`: [github.com/andrewyng/translation-agent](https://github.com/andrewyng/translation-agent) - Reflection workflow implementation, 3-pass architecture, multi-chunk handling, prompts for 4 quality dimensions [VERIFIED]
- `XLATE-IN01-SC-ANDR-UTILS`: [translation-agent/utils.py](https://github.com/andrewyng/translation-agent/blob/main/src/translation_agent/utils.py) - Full source code showing translate/reflect/improve prompts and chunk context handling [VERIFIED]
- `XLATE-IN01-SC-LKLS-COMP`: [lokalise.com/blog/what-is-the-best-llm-for-translation/](https://lokalise.com/blog/what-is-the-best-llm-for-translation/) - Blind comparison study of 5 translation systems across 3 language pairs, model routing recommendations [VERIFIED]
- `XLATE-IN01-SC-DEPL-GLOS`: [developers.deepl.com/api-reference/multilingual-glossaries](https://developers.deepl.com/api-reference/multilingual-glossaries) - DeepL glossary API v3 documentation, multilingual glossary management [VERIFIED]
- `XLATE-IN01-SC-DEPL-FEAT`: [deepl.com/en/features/glossary](https://www.deepl.com/en/features/glossary) - DeepL glossary features: context-aware inflection, merging, sharing, API integration [VERIFIED]
- `XLATE-IN01-SC-EESL-PRIC`: [eesel.ai/blog/deepl-pricing](https://www.eesel.ai/blog/deepl-pricing) - DeepL pricing breakdown: API Free (500K chars/month, $0), API Pro ($5.49 + $25/M chars) [VERIFIED]
- `XLATE-IN01-SC-TRNS-EVAL`: [translated.com/mt-quality-evaluation-in-the-age-of-llm-based-mt](https://translated.com/mt-quality-evaluation-in-the-age-of-llm-based-mt) - COMET limitations: empty translations score 0.32, wrong-language output scores high, evaluation crisis for LLM-based MT [VERIFIED]
- `XLATE-IN01-SC-WIKI-RTRT`: [en.wikipedia.org/wiki/Round-trip_translation](https://en.wikipedia.org/wiki/Round-trip_translation) - Round-trip translation is a poor predictor of quality; error source ambiguity [VERIFIED]
- `XLATE-IN01-SC-ARXV-RTQE`: [arxiv.org/abs/2004.13937](https://arxiv.org/abs/2004.13937) - Revisiting Round-Trip Translation for Quality Estimation - RTT found to be poor QE predictor [VERIFIED]

## 7. Next Steps

1. Update `/translate` workflow Step 4 with reflection pass (translate, reflect, improve)
2. Update `/translate` workflow Step 5 with LLM-as-judge verification using 4 quality dimensions
3. Optionally add DeepL API Free integration as comparison backend (requires API key setup in `.api-keys.txt`)
4. Register `XLATE` topic in ID-REGISTRY.md

## 8. Document History

**[2026-05-05 10:19]**
- Initial research document created
- Researched: Andrew Ng reflection workflow, DeepL API, LLM model comparison, quality evaluation methods
