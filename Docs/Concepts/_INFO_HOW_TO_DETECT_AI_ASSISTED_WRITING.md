# INFO: How to Detect AI-Assisted Writing

**Doc ID**: AIDET-IN01
**Goal**: Document the detection principle for AI-assisted writing - its background, the signals it identifies, and how enforceable rules implement detection for practical use
**Timeline**: Created 2026-06-05

## Summary

- **AI-assisted writing** leaves detectable patterns in style, structure, sourcing, voice, and lexical choice [VERIFIED]
- Detection works through **signal analysis**: identifying patterns that arise from Large Language Model (LLM) generation mechanics, not from human writing habits [VERIFIED]
- The strongest single indicator is **confident misattribution** - stating falsifiable claims with authority but without citation, where the claim turns out wrong [VERIFIED]
- No single signal is conclusive. Detection requires **convergence** of multiple independent signals across categories [VERIFIED]
- The five detection categories: Sourcing (SO), Style (SY), Structure (ST), Voice (VO), Lexical (LX) [VERIFIED]
- Human writing has **idiosyncrasies** (unusual word choices, structural surprises, personal reference). LLM writing has **uniformity** (predictable cadence, perfect escalation, no rough edges) [VERIFIED]
- Computational research confirms these patterns persist in reasoning models (o1, o3). The PLOS One 2025 study found no difference between o1 and GPT-4o in detectable writing patterns [VERIFIED] (STYLO-SC-PLOS-STYLJP)
- Human judges perform at chance (50%) when asked to identify AI text. Pattern-based detection achieves 99.8% accuracy on the same texts. The signals are real but invisible to casual reading [VERIFIED] (STYLO-SC-PLOS-STYLJP)

## Table of Contents

1. [The Detection Principle](#1-the-detection-principle)
2. [Why This Matters](#2-why-this-matters)
3. [The Five Signal Categories](#3-the-five-signal-categories)
4. [Research Validation](#4-research-validation)
5. [Limitations and Counterarguments](#5-limitations-and-counterarguments)
6. [Sources](#6-sources)
7. [Document History](#7-document-history)

## 1. The Detection Principle

### 1.1 Definition

AI-assisted writing detection identifies text where a Large Language Model (LLM) generated, co-authored, or substantially shaped the output. Detection relies not on any single marker but on convergence of signals across five independent categories.

The principle mirrors forensic document analysis: no single fiber proves fraud, but when fiber, ink, paper, and handwriting analysis all point the same direction, the conclusion becomes reliable.

### 1.2 The Generation Mechanic

LLMs produce text by predicting the most probable next token given context. This mechanic creates identifiable patterns:

- **Smoothness** - Every sentence flows into the next because the model optimizes for coherent continuation. Human writing has interruptions, tangents, self-corrections
- **Confident vagueness** - LLMs generate authoritative-sounding claims without access to source verification. The output sounds knowledgeable but avoids falsifiable specifics
- **Internet-discourse conflation** - LLMs trained on web data absorb the popularized commentary layer (blog posts, YouTube summaries, Reddit threads) and conflate it with primary sources. The model does not distinguish between what an author actually wrote and what a blogger said the author wrote
- **Rhetorical optimization** - LLMs produce engagement-optimized structures because their training data rewards these patterns. The result is text that reads like it was A/B-tested for maximum persuasive impact
- **Grammatical standardization** - LLMs produce more uniform grammatical patterns than human writers. Where humans vary sentence construction idiosyncratically, LLMs converge on predictable Part-of-Speech sequences. This uniformity is computationally measurable but invisible to casual reading [VERIFIED] (STYLO-SC-ARXV-STYLOREC)

### 1.3 Signal vs Proof

No detection method is definitive. Skilled human writers can produce LLM-like patterns. LLM outputs can be edited to remove telltale markers. Detection produces a **confidence assessment**, not a binary verdict.

The assessment strengthens when:
- Multiple independent signals converge
- Signals span different categories (sourcing AND style AND structure)
- The text contains factual errors consistent with LLM hallucination patterns

The assessment weakens when:
- Only style signals are present (some humans write in LLM-like cadence)
- The text is heavily edited (human post-processing removes generation artifacts)
- The domain is one where formulaic writing is conventional (legal, academic abstracts)
- The text is shorter than 10 sentences - detection reliability drops significantly below this threshold [VERIFIED] (STYLO-SC-ARXV-STYLOREC)

**Human judges cannot do this:** A study of 403 participants found human accuracy at distinguishing AI from human text was near chance (50%). Worse, more advanced LLMs like o1 led humans to INCORRECTLY believe text was human-written with HIGHER confidence. This confirms that pattern-based detection identifies signals invisible to human perception [VERIFIED] (STYLO-SC-PLOS-STYLJP)

## 2. Why This Matters

### 2.1 Authority Laundering

The most consequential use of AI-assisted writing is **authority laundering**: using an LLM to generate text that attributes claims to respected sources (Jung, Einstein, historical figures) without verifying those attributions. The reader trusts the source, not the author - and the LLM's confident tone obscures the fact that the attribution may be fabricated.

A typical pattern: a thinker's genuine authority is borrowed to validate claims they never made, using terminology they never used, applied to events they never witnessed. The LLM's generation mechanic makes this seamless because it does not distinguish between primary-source claims and internet commentary.

### 2.2 The Verification Burden Shift

Before LLMs, producing authoritative-sounding writing on a specialized topic required domain knowledge. The cost of writing filtered out most fabrication. LLMs eliminate this cost barrier. Any prompt can produce a polished essay attributing sophisticated arguments to recognized thinkers.

This shifts the verification burden from writer to reader. The reader must now verify not just whether the argument is logical, but whether the attributed sources actually said what the text claims they said.

### 2.3 Detection as Hygiene

Detection is not about catching dishonesty. Many AI-assisted texts are produced in good faith by users who trust the LLM's output. Detection serves as intellectual hygiene: flagging text that requires source verification before the claims within it are accepted or forwarded.

## 3. The Five Signal Categories

### 3.1 Sourcing Signals (SO)

How the text relates to its claimed sources. Strongest detection category because sourcing errors arise directly from the LLM generation mechanic.

- **SO-01: Confident misattribution** - Falsifiable claims stated with authority, where verification reveals the claim is wrong. The hallmark of LLM hallucination: the model generates plausible-sounding attributions from its training distribution without access to the primary source
- **SO-02: Internet-discourse terminology** - Using popularized terms from secondary sources (blogs, videos, social media) instead of the primary source's own terminology. Reveals that the training data, not the source text, shaped the output
- **SO-03: Absence of citation** - Making specific factual claims (dates, quotes, concepts) without any source reference. Human experts cite; human non-experts at least name the source. LLMs do neither because citation requires retrieval, which the base model cannot perform
- **SO-04: Temporal impossibility** - Applying a historical figure's ideas to events that postdate the figure's work, without acknowledging the interpretive leap. The LLM treats all training data as contemporaneous

### 3.2 Style Signals (SY)

How the text reads at the sentence and paragraph level.

- **SY-01: Staccato fragment pattern** - Short declarative sentences followed by one-word or two-word fragments for emphasis. ("Not metaphorically. Psychologically. Collectively.") Common in LLM persuasive output, rare in sustained human writing
- **SY-02: Perfect tricolon escalation** - Three parallel phrases with ascending intensity, cleanly balanced. ("It was hard in 1957. It was almost impossible in 2020. But it was never more necessary.") Humans produce rough tricolons; LLMs produce polished ones consistently
- **SY-03: Absence of rough edges** - No idiosyncratic word choices, no unexpected metaphors, no self-corrections, no tangents. The text is uniformly smooth. Human writing, even polished human writing, has personality artifacts

### 3.3 Structure Signals (ST)

How the text is organized at the macro level.

- **ST-01: Engagement-optimized arc** - Text follows a template: establish authority, explain mechanism, apply to current events, emotional close. This arc is over-represented in LLM training data (blog posts, Substack essays, Medium articles) and reproduces reliably
- **ST-02: Perfect paragraph progression** - Every paragraph builds on the previous in a clean narrative ramp. No structural surprises, no digressions, no revisitations. Human essays meander; LLM essays march
- **ST-03: Absence of structural surprise** - The reader can predict the next section's function after reading two sections. This predictability arises from the model's tendency to reproduce the most common essay structures from its training data

### 3.4 Voice Signals (VO)

Who appears to be speaking.

- **VO-01: No personal reference** - No "I," no anecdote, no specific professional experience, no disclosed perspective. The text speaks from a position of disembodied authority. Humans anchor arguments in personal experience; LLMs lack experience to anchor in
- **VO-02: Generated authority** - The text reads as if written by an expert but contains errors an expert would not make. The authority is performed, not earned. A domain scholar would not misattribute terminology to an author because they would know the actual terms used
- **VO-03: Emotional manipulation without emotional investment** - The text produces emotional responses (urgency, moral clarity, righteous anger) through technique rather than personal stake. The writer is not present in the emotion they generate

### 3.5 Lexical Signals (LX)

What specific words and phrases the text uses.

- **LX-01: High-frequency LLM vocabulary** - The text contains words that appear with disproportionate frequency in LLM output: "delve," "crucial," "pivotal," "nuanced," "multifaceted," "landscape" (non-geographic), "tapestry," "foster," "leverage," "underscore." These words are not wrong - they are statistically over-represented in generated text because they occupy high-probability positions in common contexts
- **LX-02: Qualifier stacking** - Multiple qualifiers piled on a single claim without adding precision: "fundamentally important and deeply significant development." Remove the qualifiers and the meaning is unchanged. LLMs generate qualifiers because they appear in formal training data and are safe, low-cost tokens
- **LX-03: Conjunctive adverb overuse** - Heavy reliance on formal connectives ("However," "Nevertheless," "Consequently," "Furthermore") where simpler words ("but," "so," "and," "still") would serve. LLMs default to high-register connectives because their training data skews formal

## 4. Research Validation

Computational stylometric research (2024-2026) confirms the detection principle described in this document.

### 4.1 The Signals Are Real

The writing patterns this document describes as SO, SY, ST, VO, and LX signals have computational counterparts. Stylometric analysis extracts quantifiable features from text - function word frequencies, grammatical sequence patterns, sentence length distributions, vocabulary diversity - and classifiers trained on these features distinguish human from LLM text with near-perfect accuracy.

The signals our rules target at the human-perceptible level are the same patterns computational methods measure. Our rules are a human-readable approximation of what stylometric classifiers detect computationally. [VERIFIED] (STYLO-SC-ARXV-STYLOREC)

### 4.2 Reasoning Models Do Not Escape Detection

The PLOS One 2025 study tested 7 LLMs including ChatGPT o1 (a reasoning model) and found "no significant difference" between o1 and GPT-4o in detectable writing patterns. Accuracy: 99.8% across all models. The internal chain-of-thought reasoning process does not change the surface-level writing patterns of the output. [VERIFIED] (STYLO-SC-PLOS-STYLJP)

This means the detection signals described in this document remain valid for post-2025 reasoning models. The patterns arise from the token-prediction mechanic, which reasoning models still use for output generation.

### 4.3 Key Research Findings (High-Level)

- LLMs show **"greater grammatical standardization"** than human writers - more uniform sentence construction patterns [VERIFIED] (STYLO-SC-ARXV-STYLOREC)
- **10-sentence samples are sufficient** for reliable detection [VERIFIED] (STYLO-SC-ARXV-STYLOREC)
- **Paraphrase attacks reduce but do not eliminate** detectable patterns - rephrased AI text retains some signature of the original generator [VERIFIED] (STYLO-SC-ARXV-STYLOREC)
- **No single detection method works universally** across all text types. Performance degrades when the text domain differs from what the detector was trained on [VERIFIED] (STYLO-SC-ARXV-SPOTBLND)
- **All detectors fail on at least one text type** - evaluation data is "highly predictive of model performance" [VERIFIED] (STYLO-SC-ARXV-SPOTBLND)

### 4.4 What This Means for Our Rules

Our rule-based approach (SO, SY, ST, VO, LX) targets the same patterns that computational methods confirm are real and persistent:
- **Sourcing signals (SO)** are the most reliable because they arise directly from the LLM generation mechanic (lack of retrieval capability)
- **Style signals (SY)** correspond to the "grammatical standardization" that classifiers detect
- **Structure signals (ST)** correspond to the predictable essay arc patterns in training data
- **Voice signals (VO)** correspond to the absence of idiosyncratic variation
- **Lexical signals (LX)** correspond to the vocabulary biases classifiers exploit

The convergence approach (multiple signals across categories) is validated by research: no single feature is conclusive, but convergence of independent signals is highly diagnostic.

## 5. Limitations and Counterarguments

### 5.1 False Positives

- Skilled Substack/Medium writers deliberately use engagement-optimized structures
- Ghostwriters and speechwriters produce polished, voice-free text professionally
- Some academic traditions produce highly structured, impersonal prose

### 5.2 False Negatives

- Human-edited LLM output can remove style and structure signals
- LLM output on topics within the model's training data may contain correct attributions
- Short texts (<200 words) provide insufficient signal density

### 5.3 The Strongest Signal

Sourcing errors (SO-01, SO-02) are the most reliable category because they arise directly from the LLM generation mechanic and cannot be replicated by competent human domain writers. A human who has read a primary source does not misattribute popularized terminology to the original author. An LLM that has absorbed internet commentary about the source does.

Style and structure signals alone are insufficient. Many humans write in LLM-like patterns, especially those influenced by the same engagement-optimized content the LLMs were trained on.

## 6. Sources

**Primary Sources:**
- `AIDET-IN01-SC-APAP-PRINCPL`: `_INFO_APAPALAN_PRINCIPLE.md [APAPALAN-IN01]` - Structural model for this document [VERIFIED]
- `AIDET-IN01-SC-APAP-RULES`: `APAPALAN_RULES.md` - Rule format model for companion document [VERIFIED]

**Research Sources:**
- `STYLO-SC-PLOS-STYLJP`: "Stylometry can reveal AI authorship, but humans struggle" (PLOS One 2025). Tests 7 LLMs including o1. 99.8% accuracy. Human judges at chance. [VERIFIED]
  - URL: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369
- `STYLO-SC-ARXV-STYLOREC`: "Stylometry recognizes human and LLM-generated texts in short samples" (Expert Systems with Applications 2025, arXiv 2507.00838). StyloMetrix features, 10-sentence samples, multiclass attribution. [VERIFIED]
  - URL: https://arxiv.org/abs/2507.00838
- `STYLO-SC-ARXV-SPOTBLND`: "Spotlights and Blindspots: Evaluating Machine-Generated Text Detection" (April 2026, arXiv 2604.16607). 15 detection systems, 8 datasets. Feature-based models match transformers. [VERIFIED]
  - URL: https://arxiv.org/html/2604.16607v2

## 7. Document History

**[2026-06-05 18:20]**
- Added: Section 3.5 Lexical Signals (LX) - aligns with companion rules file
- Added: Section 4 Research Validation - PLOS One 2025, arxiv 2507.00838, arxiv 2604.16607
- Added: 3 research sources to Sources section
- Changed: 4 signal categories expanded to 5 (added LX)
- Changed: Research confirms reasoning models (o1) produce same detectable patterns
- Changed: Added human judge failure finding (50% accuracy vs 99.8% computational)
- Changed: Added grammatical standardization insight to generation mechanic
- Changed: Added 10-sentence minimum threshold

**[2026-06-05 16:51]**
- Changed: Removed case study references, generalized all examples

**[2026-06-05 16:48]**
- Initial document created
- Structure modeled on `_INFO_APAPALAN_PRINCIPLE.md [APAPALAN-IN01]`
- 12 detection signals across 4 categories
