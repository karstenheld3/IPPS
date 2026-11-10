# INFO: How to Detect AI-Assisted Writing

**Doc ID**: AIDET-IN01
**Goal**: Document the detection principle for AI-assisted writing - its background, the signals it identifies, and how enforceable rules implement detection for practical use
**Timeline**: Created 2026-06-05, Updated 3 times (2026-06-05 - 2026-11-08)

## Summary

- **AI-assisted writing** leaves detectable patterns in style, structure, sourcing, voice, and lexical choice [VERIFIED]
- Detection works through **signal analysis**: identifying patterns that arise from Large Language Model (LLM) generation mechanics, not from human writing habits [VERIFIED]
- The strongest single indicator is **confident misattribution** - stating falsifiable claims with authority but without citation, where the claim turns out wrong [VERIFIED]
- No single signal is conclusive. Detection requires **convergence** of multiple independent signals across categories [VERIFIED]
- The five detection categories cover 20 signals: Sourcing (SO, 4), Style (SY, 5), Structure (ST, 4), Voice (VO, 4), Lexical (LX, 3) [VERIFIED]
- Human writing has **idiosyncrasies** (unusual word choices, structural surprises, personal reference). LLM writing has **uniformity** (predictable cadence, perfect escalation, no rough edges) [VERIFIED]
- Computational research confirms these patterns persist in reasoning models (o1, o3). The [PLOS One 2025 study](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369) found no difference between o1 and GPT-4o in detectable writing patterns (`STYLO-SC-PLOS-STYLJP`) [VERIFIED]
- Human judges perform at chance (50%) when asked to identify AI text. Pattern-based detection achieves 99.8% accuracy on the same texts. The signals are real but invisible to casual reading ([PLOS One 2025](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369), `STYLO-SC-PLOS-STYLJP`) [VERIFIED]
- **Newer post-trained models narrow stylistic diversity further** `[IMPROVED]`: 2025-2026 research shows instruction tuning and preference learning (RLHF/DPO) reduce syntactic and lexical diversity compared to both human prose and older base models ([arXiv 2605.06030](https://arxiv.org/html/2605.06030), `AIDET-IN01-SC-ARXV-HPSG26`), amplifying discourse/structural formatting markers by **1,949%-16,853%** while suppressing complex punctuation and syntactic variety to **3.2%-23.2%** of human baseline frequencies ([arXiv 2605.28826](https://arxiv.org/abs/2605.28826), `AIDET-IN01-SC-ARXV-COLLPS`) [VERIFIED]
- **2026 frontier models shift from shared clichés to model idiolects and structural density** `[IMPROVED]`: While 2026 models reduce 2024 buzzwords, each model family exhibits a distinct "idiolect" (e.g., contraction rates varying 25x from 1,200 to 30,000 per million words across 2026 models in [arXiv 2608.06589](https://arxiv.org/abs/2608.06589), `AIDET-IN01-SC-ARXV-IDIO26`) and high noun-heavy information density ([arXiv 2604.14111](https://arxiv.org/html/2604.14111v1), `AIDET-IN01-SC-ARXV-BIBR26`) [VERIFIED]
- **AI generation vs. AI editing leave distinct footprints** `[IMPROVED]`: Across 45,000 generated and 273,420 edited texts, AI editing does not reproduce the generation footprint; instead, it decreases entropy ($d = -0.28$) and sharply shifts **lexical density** ($d = -3.10$, content-to-function word ratio) ([arXiv 2608.27855](https://arxiv.org/abs/2608.27855), `AIDET-IN01-SC-ARXV-EDTFT`) [VERIFIED]

```
LLM Generation Mechanics                   Five Signal Categories (20 Signals)             Convergence Assessment
┌────────────────────────────────────┐     ┌─────────────────────────────────────────┐     ┌────────────────────────────┐
│ Next-token probability maximization├─┬─> │ 1. Sourcing (SO-01..04)  [2x weight]    ├─┬─> │ 0-3 signals:   LOW         │
│ No primary-source retrieval        │ ├─> │ 2. Style (SY-01..05)     [1x weight]    │ ├─> │ 4-7 signals:   MODERATE    │
│ Web commentary conflation          │ ├─> │ 3. Structure (ST-01..04) [1x weight]    │ ├─> │ 8-13 signals:  HIGH        │
│ Post-training / RLHF alignment     │ ├─> │ 4. Voice (VO-01..04)     [1x weight]    │ └─> │ 14+ or SO>=3:  HIGH / V.HI │
│ Structural entropy collapse        │ └─> │ 5. Lexical (LX-01..03)   [1x weight]    │     └────────────────────────────┘
└────────────────────────────────────┘     └─────────────────────────────────────────┘
```

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
- **Grammatical standardization** - LLMs produce more uniform grammatical patterns than human writers. Where humans vary sentence construction idiosyncratically, LLMs converge on predictable Part-of-Speech sequences. This uniformity is computationally measurable but invisible to casual reading ([Expert Systems with Applications 2025 / arXiv 2507.00838](https://arxiv.org/abs/2507.00838), `STYLO-SC-ARXV-STYLOREC`) [VERIFIED]
- **Post-training stylistic collapse and prestige shift** `[IMPROVED]` - Modern alignment pipelines (instruction tuning, RLHF, DPO) narrow surface form even as semantic capability improves. Across 17 models, instruction-tuned pipelines collapse discourse and structural entropy - amplifying headers, lists, and expository framing by **1,949% to 16,853%** while suppressing complex punctuation and syntactic variety to **3.2%-23.2%** of human baseline frequencies ([arXiv 2605.28826](https://arxiv.org/abs/2605.28826), `AIDET-IN01-SC-ARXV-COLLPS`) [VERIFIED]. Preference learning shifts models toward a formal "language of prestige" ($R = 1.19\text{-}1.73$ across six model families in [arXiv 2606.00334](https://arxiv.org/html/2606.00334), `AIDET-IN01-SC-ARXV-TPSLEX`) and embeds a localized residual-stream alignment signature that drives detector visibility ([EMNLP 2026 / arXiv 2605.30526](https://arxiv.org/abs/2605.30526), `AIDET-IN01-SC-ARXV-PASTA`) [VERIFIED]
- **Noun-heavy information compression** `[IMPROVED]` - Large-scale Biber lexicogrammatical analysis across 11 LLMs and 8 genres shows chat-tuned models cluster separately from both base models and human prose, producing systematically more noun-heavy, information-dense clauses regardless of prompt nudges or decoding strategies ([arXiv 2604.14111](https://arxiv.org/html/2604.14111v1), `AIDET-IN01-SC-ARXV-BIBR26`) [VERIFIED]

### 1.3 Signal vs Proof

No detection method is definitive. Skilled human writers can produce LLM-like patterns. LLM outputs can be edited to remove telltale markers. Detection produces a **confidence assessment**, not a binary verdict.

The assessment strengthens when:
- Multiple independent signals converge
- Signals span different categories (sourcing AND style AND structure)
- The text contains factual errors consistent with LLM hallucination patterns

The assessment weakens when:
- Only style signals are present (some humans write in LLM-like cadence)
- The text is heavily edited (human post-processing removes generation artifacts; AI editing of human drafts leaves a distinct lexical-density trace rather than the full generation footprint per [arXiv 2608.27855](https://arxiv.org/abs/2608.27855), `AIDET-IN01-SC-ARXV-EDTFT`) [VERIFIED]
- The domain is one where formulaic writing is conventional (legal, academic abstracts)
- The text is shorter than 10 sentences - detection reliability drops significantly below this threshold (`STYLO-SC-ARXV-STYLOREC`) [VERIFIED]

**Human judges cannot do this:** A study of 403 participants found human accuracy at distinguishing AI from human text was near chance (50%). Worse, more advanced LLMs like o1 led humans to INCORRECTLY believe text was human-written with HIGHER confidence. This confirms that pattern-based detection identifies signals invisible to human perception ([PLOS One 2025](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369), `STYLO-SC-PLOS-STYLJP`) [VERIFIED]

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
- **SY-04: Hedge-then-assert pattern** - Introducing a claim with a superficial hedge ("It could be argued that," "Perhaps") and immediately continuing as if the hedged claim were established fact. Forward continuation is statistically more probable than sustained qualification
- **SY-05: Filler transition saturation** - Opening >50% of consecutive paragraphs or sentences with generic transitions ("Moreover," "Furthermore," "Additionally," "Indeed," "It is worth noting") that carry no logical weight

### 3.3 Structure Signals (ST)

How the text is organized at the macro level.

- **ST-01: Engagement-optimized arc** - Text follows a template: establish authority, explain mechanism, apply to current events, emotional close. This arc is over-represented in LLM training data (blog posts, Substack essays, Medium articles) and reproduces reliably
- **ST-02: Perfect paragraph progression** - Every paragraph builds on the previous in a clean narrative ramp. No structural surprises, no digressions, no revisitations. Human essays meander; LLM essays march
- **ST-03: Absence of structural surprise** - The reader can predict the next section's function after reading two sections. This predictability arises from the model's tendency to reproduce the most common essay structures from its training data
- **ST-04: Perfect list parallelism** - Bulleted or numbered lists (4+ items) where every item shares identical grammatical structure, near-identical word count (within 1-2 words), and identical rhetorical weight

### 3.4 Voice Signals (VO)

Who appears to be speaking.

- **VO-01: No personal reference** - No "I," no anecdote, no specific professional experience, no disclosed perspective. The text speaks from a position of disembodied authority. Humans anchor arguments in personal experience; LLMs lack experience to anchor in
- **VO-02: Generated authority** - The text reads as if written by an expert but contains errors an expert would not make. The authority is performed, not earned. A domain scholar would not misattribute terminology to an author because they would know the actual terms used
- **VO-03: Emotional manipulation without emotional investment** - The text produces emotional responses (urgency, moral clarity, righteous anger) through technique rather than personal stake. The writer is not present in the emotion they generate
- **VO-04: Omniscient summarizer voice** - Summarizing a thinker's body of work, historical period, or contested debate in declarative statements without acknowledging interpretive disputes or boundaries of knowledge

### 3.5 Lexical Signals (LX)

What specific words and phrases the text uses.

- **LX-01: High-frequency LLM vocabulary** - The text contains words that appear with disproportionate frequency in LLM output: "delve," "crucial," "pivotal," "nuanced," "multifaceted," "landscape" (non-geographic), "tapestry," "foster," "leverage," "underscore." These words are not wrong - they are statistically over-represented in generated text because they occupy high-probability positions in common contexts
- **LX-02: Qualifier stacking** - Multiple qualifiers piled on a single claim without adding precision: "fundamentally important and deeply significant development." Remove the qualifiers and the meaning is unchanged. LLMs generate qualifiers because they appear in formal training data and are safe, low-cost tokens
- **LX-03: Conjunctive adverb overuse** - Heavy reliance on formal connectives ("However," "Nevertheless," "Consequently," "Furthermore") where simpler words ("but," "so," "and," "still") would serve. LLMs default to high-register connectives because their training data skews formal

## 4. Research Validation

Computational stylometric research (2024-2026) confirms the detection principle described in this document.

### 4.1 The Signals Are Real

The writing patterns this document describes as SO, SY, ST, VO, and LX signals have computational counterparts. Stylometric analysis extracts quantifiable features from text - function word frequencies, grammatical sequence patterns, sentence length distributions, vocabulary diversity - and classifiers trained on these features distinguish human from LLM text with near-perfect accuracy.

The signals our rules target at the human-perceptible level are the same patterns computational methods measure. Our rules are a human-readable approximation of what stylometric classifiers detect computationally ([arXiv 2507.00838](https://arxiv.org/abs/2507.00838), `STYLO-SC-ARXV-STYLOREC`) [VERIFIED].

### 4.2 Reasoning Models Do Not Escape Detection

The [PLOS One 2025 study](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369) tested 7 LLMs including ChatGPT o1 (a reasoning model) and found "no significant difference" between o1 and GPT-4o in detectable writing patterns. Accuracy: 99.8% across all models. The internal chain-of-thought reasoning process does not change the surface-level writing patterns of the output (`STYLO-SC-PLOS-STYLJP`) [VERIFIED].

This means the detection signals described in this document remain valid for post-2025 reasoning models. The patterns arise from the token-prediction mechanic, which reasoning models still use for output generation.

### 4.3 Newer Models (2025-2026): Why Better Models Produce Stronger Structural Artifacts

A common assumption is that as LLMs scale and improve at reasoning, their writing becomes indistinguishable from human prose `[CHALLENGED]`. Empirical research from Q3-Q4 2025 and 2026 proves the opposite for surface form: **better instruction following and preference alignment narrow stylistic diversity** [VERIFIED].

```
Model Improvement Stage        Content / Semantic Capability    Surface Stylistic Diversity (Form)
┌───────────────────────────┐  ┌─────────────────────────────┐  ┌──────────────────────────────────────────────────────────┐
│ Pretrained Base Model     ├─>│ Lower validity & coherence  ├─>│ Broadest lexical/syntactic range, closer to human corpus │
├───────────────────────────┤  ├─────────────────────────────┤  ├──────────────────────────────────────────────────────────┤
│ Instruction Tuning (SFT)  ├─>│ Higher prompt adherence     ├─>│ Discourse collapse: 1,949-16,853% structure amplification│
├───────────────────────────┤  ├─────────────────────────────┤  ├──────────────────────────────────────────────────────────┤
│ Preference / RL Alignment ├─>│ Higher semantic diversity   ├─>│ Punctuation/syntax suppressed to 3.2-23.2% of baseline;  │
│ (RLHF, DPO, GRPO, o1/G3)  │  │ among valid outputs         │  │ "language of prestige" shift (R = 1.19-1.73)             │
└───────────────────────────┘  └─────────────────────────────┘  └──────────────────────────────────────────────────────────┘
```

1. **Form vs. content divergence in aligned models** `[IMPROVED]`: Head-Driven Phrase Structure Grammar (HPSG) analysis comparing two generations of LLMs against *New York Times* prose shows human news diversity remains stable over time, whereas newer instruction-tuned LLMs exhibit substantially *lower* syntactic and lexical diversity than both humans and older non-instruction-tuned models, producing parse trees that require less memory to process ([arXiv 2605.06030](https://arxiv.org/html/2605.06030), `AIDET-IN01-SC-ARXV-HPSG26`) [VERIFIED]. This occurs because reinforcement learning (PPO, GRPO) increases *effective semantic diversity* (more valid ideas) while compressing *syntactic and lexical form* into high-reward templates.
2. **Post-training alignment signature (PASTA)** `[IMPROVED]`: Comparing human prefixes, base continuations, and aligned continuations across 11 models shows that post-training actively pushes text away from human-corpus style toward detector-visible regularity. Ablating a single aligned-minus-base residual-stream direction during decoding reduces AI-detector flagging by **73.2 to 98.0 percentage points** on 8 of 11 models across 6 detectors ([EMNLP 2026 / arXiv 2605.30526](https://arxiv.org/abs/2605.30526), `AIDET-IN01-SC-ARXV-PASTA`) [VERIFIED].
3. **Discourse entropy collapse and punctuation suppression** `[IMPROVED]`: Across 17 models (410M to 100B+ parameters) and 24 linguistic probes, contemporary pipelines amplify low-entropy structural markers (headers, bulleted lists, expository framing) by **1,949%-16,853%** while suppressing complex punctuation (semicolons, parentheticals, interruptive dashes) and syntactic variety to **3.2%-23.2%** of human baseline frequencies ([arXiv 2605.28826](https://arxiv.org/abs/2605.28826), `AIDET-IN01-SC-ARXV-COLLPS`) [VERIFIED]. Once a model emits a header or list item, self-reinforcing generation loops lock subsequent tokens into parallel structure (`ST-04`).
4. **Triangulated Preference Shift (TPS) toward prestige register** `[IMPROVED]`: Triangulating across 42,000 human abstracts, base models, and instruct variants proves that overuse of formal connectives (`LX-03`) and prestige vocabulary (`LX-01`) is induced during preference learning ($R > 1$ across all 6 model families: Falcon-3 $R=1.73$, OLMo-2 $R=1.42$, Gemma-3 $R=1.41$, Llama-3.1 $R=1.19$) even when absent in the base model ([arXiv 2606.00334](https://arxiv.org/html/2606.00334), `AIDET-IN01-SC-ARXV-TPSLEX`) [VERIFIED].
5. **Generational shift from "AI language" to model idiolects (2024 vs. 2026)** `[IMPROVED]`: Comparing 2024 and 2026 model cohorts on identical prompts reveals a generational shift: 2026 models reduce obvious 2024 lexical clichés, but each model family maintains a stable **idiolect** (e.g., contraction frequencies varying 25x from 1,200 to >30,000 per million words within the 2026 cohort in [arXiv 2608.06589](https://arxiv.org/abs/2608.06589), `AIDET-IN01-SC-ARXV-IDIO26`) [VERIFIED]. Because LLMs already generate near their canonical stylistic equilibrium, rewriting AI text with an LLM produces minimal stylistic shift, whereas rewriting human text produces large divergence - enabling **StyleDecipher** to improve cross-domain detection by up to **36.30%** ([arXiv 2510.12608](https://arxiv.org/abs/2510.12608), `AIDET-IN01-SC-ARXV-STYLDC`) [VERIFIED].
6. **Frontier models (GPT-5.4, Claude Sonnet 4.6, Gemini 3.1 Pro) and Simpson's paradox in token likelihood** `[IMPROVED]`: Uncalibrated token-likelihood detectors degrade on 2025-2026 frontier models because token-level overconfidence varies across hidden-space clusters, creating a Simpson's paradox when averaged globally. Local hidden-space calibration restores detection on GPT-5.4 from **0.63 to 0.85 AUROC** (Fast-DetectGPT) and **0.689 to 0.939 AUROC** (DMAP), and on Claude Peer-Review from **0.545 to 0.932 AUROC** ([arXiv 2605.06294](https://arxiv.org/html/2605.06294), `AIDET-IN01-SC-ARXV-SIMPSN`) [VERIFIED].
7. **AI Generation vs. AI Editing footprints** `[IMPROVED]`: A 2026 study of 45,000 generated texts (8 LLMs, 5 domains) and 273,420 AI-edited texts proves that **AI editing does not look like a weaker version of AI generation**. While full AI generation exhibits jointly high entropy and lexical diversity, AI editing of human drafts slightly lowers entropy ($d = -0.28$), barely alters lexical diversity ($d = +0.24$), and strongly shifts **lexical density** ($d = -3.10$, ratio of content words to function words). Combining stylometric features with neural edit detectors achieves **0.99 AUC** separating edited from generated text and **0.94 AUC** separating edited from human text ([arXiv 2608.27855](https://arxiv.org/abs/2608.27855), `AIDET-IN01-SC-ARXV-EDTFT`) [VERIFIED].

### 4.4 Foundational Stylometric Findings

- LLMs show **"greater grammatical standardization"** than human writers - more uniform sentence construction patterns (`STYLO-SC-ARXV-STYLOREC`) [VERIFIED]
- **10-sentence samples are sufficient** for reliable detection (`STYLO-SC-ARXV-STYLOREC`) [VERIFIED]
- **Paraphrase attacks reduce but do not eliminate** detectable patterns - rephrased AI text retains some signature of the original generator (`STYLO-SC-ARXV-STYLOREC`) [VERIFIED]
- **Style features are robust to prompt nudges and decoding** `[IMPROVED]` - Prompting an LLM to "write like a human" or changing temperature/top-k has less impact on Biber lexicogrammatical style than genre and model identity ([arXiv 2604.14111](https://arxiv.org/html/2604.14111v1), `AIDET-IN01-SC-ARXV-BIBR26`) [VERIFIED]
- **No single detection method works universally** across all text types. Performance degrades when the text domain differs from what the detector was trained on ([Spotlights and Blindspots, arXiv 2604.16607](https://arxiv.org/html/2604.16607v2), `STYLO-SC-ARXV-SPOTBLND`) [VERIFIED]
- **All detectors fail on at least one text type** - evaluation data is "highly predictive of model performance" (`STYLO-SC-ARXV-SPOTBLND`) [VERIFIED]

### 4.5 What This Means for Our Rules

Our rule-based approach (SO, SY, ST, VO, LX) targets the same patterns that computational methods confirm are real and persistent across 2025-2026 model generations:
- **Sourcing signals (SO)** are the most reliable because they arise directly from the LLM generation mechanic (lack of primary-source retrieval and internet-commentary conflation)
- **Style signals (SY)** correspond to grammatical standardization (`STYLO-SC-ARXV-STYLOREC`) and the suppression of complex punctuation and syntactic variety to 3.2%-23.2% of human baseline (`AIDET-IN01-SC-ARXV-COLLPS`)
- **Structure signals (ST)** correspond to the 1,949%-16,853% post-training amplification of low-entropy discourse framing, headers, and self-reinforcing parallel lists (`AIDET-IN01-SC-ARXV-COLLPS`)
- **Voice signals (VO)** correspond to the absence of personal vulnerability and the residual-stream post-training alignment signature (`AIDET-IN01-SC-ARXV-PASTA`)
- **Lexical signals (LX)** correspond to preference-learning shifts toward a "language of prestige" (`AIDET-IN01-SC-ARXV-TPSLEX`) and noun-heavy information density (`AIDET-IN01-SC-ARXV-BIBR26`), though specific buzzwords evolve across model cohorts (`AIDET-IN01-SC-ARXV-IDIO26`)

The convergence approach (multiple signals across categories) is validated by research: no single feature is conclusive, but convergence of independent signals is highly diagnostic.

## 5. Limitations and Counterarguments

### 5.1 False Positives

- Skilled Substack/Medium writers deliberately use engagement-optimized structures
- Ghostwriters and speechwriters produce polished, voice-free text professionally
- Some academic traditions produce highly structured, impersonal prose
- **Structured and generic human writing** `[IMPROVED]`: Cross-generation error analysis of 233,428 detection judgments across 15 LLMs shows detectors systematically misclassify human writing as AI-generated when the human text is highly structured and generic ([arXiv 2609.34691](https://arxiv.org/abs/2609.34691), `AIDET-IN01-SC-ARXV-XGEN26`) [VERIFIED]

### 5.2 False Negatives

- **AI-edited human drafts** `[IMPROVED]`: Human-written text polished by an LLM does not exhibit the full AI-generation footprint (entropy decreases $d = -0.28$ instead of increasing), causing generation-tuned stylometric detectors to miss edited text unless lexical density shifts ($d = -3.10$) are checked (`AIDET-IN01-SC-ARXV-EDTFT`) [VERIFIED]
- **High factual specificity in AI text** `[IMPROVED]`: Injecting concrete details, named entities, or domain specifics into LLM prompts causes both human readers and LLM detectors to misclassify AI-generated text as human-written (`AIDET-IN01-SC-ARXV-XGEN26`) [VERIFIED]
- LLM output on topics within the model's training data or with retrieval augmentation (RAG) may contain correct citations
- Short texts (<10 sentences / <200 words) provide insufficient signal density (`STYLO-SC-ARXV-STYLOREC`) [VERIFIED]

### 5.3 The Strongest Signal

Sourcing errors (SO-01, SO-02) are the most reliable category because they arise directly from the LLM generation mechanic and cannot be replicated by competent human domain writers. A human who has read a primary source does not misattribute popularized terminology to the original author. An LLM that has absorbed internet commentary about the source does.

Style and structure signals alone are insufficient. Many humans write in LLM-like patterns, especially those influenced by the same engagement-optimized content the LLMs were trained on. As 2026 models shed 2024 lexical buzzwords (`LX-01`), structural collapse (`ST-01`..`ST-04`), punctuation/syntactic uniformity (`SY-01`..`SY-05`), and sourcing verification (`SO-01`..`SO-04`) become more durable indicators than vocabulary lists alone (`AIDET-IN01-SC-ARXV-COLLPS`, `AIDET-IN01-SC-ARXV-IDIO26`) [VERIFIED].

## 6. Sources

**Primary Sources:**
- `AIDET-IN01-SC-APAP-PRINCPL`: [`_INFO_APAPALAN_PRINCIPLE.md [APAPALAN-IN01]`](_INFO_APAPALAN_PRINCIPLE.md) - Structural model for this document [VERIFIED]
- `AIDET-IN01-SC-APAP-RULES`: `APAPALAN_RULES.md` - Rule format model for companion document [VERIFIED]

**Research Sources:**
- `STYLO-SC-PLOS-STYLJP`: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369 - "Stylometry can reveal AI authorship, but humans struggle" (PLOS One 2025); tests 7 LLMs including o1; 99.8% classifier accuracy vs human judges at chance (50%) [VERIFIED]
- `STYLO-SC-ARXV-STYLOREC`: https://arxiv.org/abs/2507.00838 - "Stylometry recognizes human and LLM-generated texts in short samples" (Expert Systems with Applications 2025, arXiv 2507.00838); StyloMetrix features, 10-sentence samples, up to 0.98 binary accuracy and 0.87 MCC across 7 classes [VERIFIED]
- `AIDET-IN01-SC-ARXV-STYLDC`: https://arxiv.org/abs/2510.12608 - "StyleDecipher: Robust and Explainable Detection of LLM-Generated Texts with Stylistic Analysis" (October 2025, arXiv 2510.12608); measures stylistic stability under semantic-preserving rewriting across 5 domains, surpassing baselines by up to 36.30% out-of-domain [VERIFIED]
- `AIDET-IN01-SC-ARXV-BIBR26`: https://arxiv.org/html/2604.14111v1 - "Interpretable Stylistic Variation in Human and LLM Writing Across Genres, Models, and Decoding Strategies" (April 2026, arXiv 2604.14111); Biber lexicogrammatical analysis across 11 LLMs, 8 genres, 4 decoding strategies; chat models cluster together with high noun density and remain robust against prompt nudges [VERIFIED]
- `STYLO-SC-ARXV-SPOTBLND`: https://arxiv.org/html/2604.16607v2 - "Spotlights and Blindspots: Evaluating Machine-Generated Text Detection" (April 2026, arXiv 2604.16607); evaluates 15 detection systems across 8 datasets; feature-based models match transformers in-domain while all detectors fail on at least one text type [VERIFIED]
- `AIDET-IN01-SC-ARXV-HPSG26`: https://arxiv.org/html/2605.06030 - "More Aligned, Less Diverse? Analyzing the Grammar and Lexicon of Two Generations of LLMs" (May 2026, arXiv 2605.06030); HPSG formal grammar comparison against NYT news showing newer instruction-tuned LLMs have reduced syntactic and lexical diversity compared to both humans and older base models [VERIFIED]
- `AIDET-IN01-SC-ARXV-SIMPSN`: https://arxiv.org/html/2605.06294 - "Log-Likelihood, Simpson's Paradox, and the Detection of Machine-Generated Text" (May 2026, arXiv 2605.06294); proves naive global token-score averaging fails on frontier models (GPT-5.4, Claude Sonnet 4.6, Gemini 3.1 Pro) due to hidden-space heterogeneity; local calibration raises Fast-DetectGPT AUROC from 0.63 to 0.85 and DMAP from 0.689 to 0.939 on GPT-5.4 [VERIFIED]
- `AIDET-IN01-SC-ARXV-COLLPS`: https://arxiv.org/abs/2605.28826 - "From Context Shift to Stylistic Collapse: Why Training Objectives Matter More Than Scale" (May 2026, arXiv 2605.28826); analyzes 17 models across 24 linguistic probes showing instruction-tuned pipelines amplify discourse/structural markers by 1,949%-16,853% while suppressing complex punctuation and syntactic variety to 3.2%-23.2% of baseline [VERIFIED]
- `AIDET-IN01-SC-ARXV-PASTA`: https://arxiv.org/abs/2605.30526 - "Measuring, Localizing, and Reducing the AI-Like Writing Style of Post-Trained LLMs" (EMNLP 2026 / May 2026, arXiv 2605.30526); isolates a post-training residual-stream alignment direction across 11 models whose ablation reduces AI-detector flagging by 73.2-98.0 percentage points on 8 of 11 models [VERIFIED]
- `AIDET-IN01-SC-ARXV-TPSLEX`: https://arxiv.org/html/2606.00334 - "Isolating LLM Lexical Bias: A Curation-Free Triangulated Metric for Preference-Stage Learning" (June 2026, arXiv 2606.00334); introduces Triangulated Preference Shift (TPS) across 42,000 PubMed prompts and 6 model families ($R = 1.19\text{-}1.73$), proving preference tuning induces "language of prestige" lexical bias not present in base models [VERIFIED]
- `AIDET-IN01-SC-ARXV-IDIO26`: https://arxiv.org/abs/2608.06589 - "Beyond 'AI Language': The case for the idiolectal nature of LLM output" (August 2026, arXiv 2608.06589); compares 2024 vs 2026 model cohorts showing a generational style shift alongside persistent model-specific idiolects (contraction frequencies varying from 1,200 to >30,000 per million words across 2026 models) [VERIFIED]
- `AIDET-IN01-SC-ARXV-EDTFT`: https://arxiv.org/abs/2608.27855 - "AI Writers Have a Consistent Stylometric Footprint, but AI Editors Do Not" (August 2026, arXiv 2608.27855); analyzes 45,000 generated and 273,420 AI-edited texts across 8 LLMs and 5 domains, showing AI editing lowers entropy ($d = -0.28$) and strongly shifts lexical density ($d = -3.10$) rather than reproducing the AI-generation footprint [VERIFIED]
- `AIDET-IN01-SC-ARXV-XGEN26`: https://arxiv.org/abs/2609.34691 - "Using LLMs to Detect LLM-Generated Texts: A Cross-Generation Analysis" (September 2026, arXiv 2609.34691); evaluates 15 LLMs across 3 generations (G1 2023-24, G2 2024-25, G3 2026; 233,428 judgments), showing G3 outputs are hardest to detect, specificity causes false negatives on AI text, and structured generic prose causes false positives on human text [VERIFIED]

## 7. Document History

**[2026-11-08 13:02]**
- Added: Section 4.3 Newer Models (2025-2026): Why Better Models Produce Stronger Structural Artifacts (7 empirical findings from Q4 2025 - Q3 2026 research)
- Added: 10 research sources (`AIDET-IN01-SC-ARXV-STYLDC`, `AIDET-IN01-SC-ARXV-BIBR26`, `AIDET-IN01-SC-ARXV-HPSG26`, `AIDET-IN01-SC-ARXV-SIMPSN`, `AIDET-IN01-SC-ARXV-COLLPS`, `AIDET-IN01-SC-ARXV-PASTA`, `AIDET-IN01-SC-ARXV-TPSLEX`, `AIDET-IN01-SC-ARXV-IDIO26`, `AIDET-IN01-SC-ARXV-EDTFT`, `AIDET-IN01-SC-ARXV-XGEN26` - 10 new, 13 total research sources)
- Added: 2 Unicode architecture/flow diagrams (Summary signal convergence diagram; Section 4.3 alignment vs surface diversity diagram) per `INFO-FT-05`
- Added: Missing signals `SY-04`, `SY-05`, `ST-04`, `VO-04` in Section 3 to synchronize with companion `specs/AI_WRITING_DETECTION_RULES.md` (20 signals total)
- Added: Generation mechanics for post-training stylistic collapse, prestige shift, and noun-heavy compression in Section 1.2
- Added: False-positive and false-negative findings for AI-edited human drafts ($d = -3.10$ lexical density shift), high-specificity AI prompts, and structured generic human prose in Section 5
- Fixed: Timeline header format (`INFO-HD-03`), Summary verification labels (`INFO-SM-02`), inline clickable source links (`INFO-SC-05`), and single-line source entries (`INFO-SC-02`)

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
- Structure modeled on [`_INFO_APAPALAN_PRINCIPLE.md [APAPALAN-IN01]`](_INFO_APAPALAN_PRINCIPLE.md)
- 12 detection signals across 4 categories
