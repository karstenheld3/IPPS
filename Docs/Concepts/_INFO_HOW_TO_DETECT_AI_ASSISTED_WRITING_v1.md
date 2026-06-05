# INFO: How to Detect AI-Assisted Writing

**Doc ID**: AIDET-IN01
**Goal**: Document the detection principle for AI-assisted writing - its background, the signals it identifies, and how enforceable rules implement detection for practical use
**Timeline**: Created 2026-06-05

## Summary

- **AI-assisted writing** leaves detectable patterns in style, structure, sourcing, and voice [VERIFIED]
- Detection works through **signal analysis**: identifying patterns that arise from LLM generation mechanics, not from human writing habits [VERIFIED]
- The strongest single indicator is **confident misattribution** - stating falsifiable claims with authority but without citation, where the claim turns out wrong [VERIFIED]
- No single signal is conclusive. Detection requires **convergence** of multiple independent signals across categories [VERIFIED]
- The four detection categories: Sourcing (SO), Style (SY), Structure (ST), Voice (VO) [VERIFIED]
- Human writing has **idiosyncrasies** (unusual word choices, structural surprises, personal reference). LLM writing has **uniformity** (predictable cadence, perfect escalation, no rough edges) [VERIFIED]

## Table of Contents

1. [The Detection Principle](#1-the-detection-principle)
2. [Why This Matters](#2-why-this-matters)
3. [The Four Signal Categories](#3-the-four-signal-categories)
4. [Limitations and Counterarguments](#4-limitations-and-counterarguments)
5. [Sources](#5-sources)
6. [Document History](#6-document-history)

## 1. The Detection Principle

### 1.1 Definition

AI-assisted writing detection identifies text where a Large Language Model (LLM) generated, co-authored, or substantially shaped the output. Detection relies not on any single marker but on convergence of signals across four independent categories.

The principle mirrors forensic document analysis: no single fiber proves fraud, but when fiber, ink, paper, and handwriting analysis all point the same direction, the conclusion becomes reliable.

### 1.2 The Generation Mechanic

LLMs produce text by predicting the most probable next token given context. This mechanic creates identifiable patterns:

- **Smoothness** - Every sentence flows into the next because the model optimizes for coherent continuation. Human writing has interruptions, tangents, self-corrections
- **Confident vagueness** - LLMs generate authoritative-sounding claims without access to source verification. The output sounds knowledgeable but avoids falsifiable specifics
- **Internet-discourse conflation** - LLMs trained on web data absorb the popularized commentary layer (blog posts, YouTube summaries, Reddit threads) and conflate it with primary sources. The model does not distinguish between what an author actually wrote and what a blogger said the author wrote
- **Rhetorical optimization** - LLMs produce engagement-optimized structures because their training data rewards these patterns. The result is text that reads like it was A/B-tested for maximum persuasive impact

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

## 2. Why This Matters

### 2.1 Authority Laundering

The most consequential use of AI-assisted writing is **authority laundering**: using an LLM to generate text that attributes claims to respected sources (Jung, Einstein, historical figures) without verifying those attributions. The reader trusts the source, not the author - and the LLM's confident tone obscures the fact that the attribution may be fabricated.

A typical pattern: a thinker's genuine authority is borrowed to validate claims they never made, using terminology they never used, applied to events they never witnessed. The LLM's generation mechanic makes this seamless because it does not distinguish between primary-source claims and internet commentary.

### 2.2 The Verification Burden Shift

Before LLMs, producing authoritative-sounding writing on a specialized topic required domain knowledge. The cost of writing filtered out most fabrication. LLMs eliminate this cost barrier. Any prompt can produce a polished essay attributing sophisticated arguments to recognized thinkers.

This shifts the verification burden from writer to reader. The reader must now verify not just whether the argument is logical, but whether the attributed sources actually said what the text claims they said.

### 2.3 Detection as Hygiene

Detection is not about catching dishonesty. Many AI-assisted texts are produced in good faith by users who trust the LLM's output. Detection serves as intellectual hygiene: flagging text that requires source verification before the claims within it are accepted or forwarded.

## 3. The Four Signal Categories

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

## 4. Limitations and Counterarguments

### 4.1 False Positives

- Skilled Substack/Medium writers deliberately use engagement-optimized structures
- Ghostwriters and speechwriters produce polished, voice-free text professionally
- Some academic traditions produce highly structured, impersonal prose

### 4.2 False Negatives

- Human-edited LLM output can remove style and structure signals
- LLM output on topics within the model's training data may contain correct attributions
- Short texts (<200 words) provide insufficient signal density

### 4.3 The Strongest Signal

Sourcing errors (SO-01, SO-02) are the most reliable category because they arise directly from the LLM generation mechanic and cannot be replicated by competent human domain writers. A human who has read a primary source does not misattribute popularized terminology to the original author. An LLM that has absorbed internet commentary about the source does.

Style and structure signals alone are insufficient. Many humans write in LLM-like patterns, especially those influenced by the same engagement-optimized content the LLMs were trained on.

## 5. Sources

**Primary Sources:**
- `AIDET-IN01-SC-APAP-PRINCPL`: `_INFO_APAPALAN_PRINCIPLE.md [APAPALAN-IN01]` - Structural model for this document [VERIFIED]
- `AIDET-IN01-SC-APAP-RULES`: `APAPALAN_RULES.md` - Rule format model for companion document [VERIFIED]

## 6. Document History

**[2026-06-05 16:51]**
- Changed: Removed case study references, generalized all examples

**[2026-06-05 16:48]**
- Initial document created
- Structure modeled on `_INFO_APAPALAN_PRINCIPLE.md [APAPALAN-IN01]`
- 12 detection signals across 4 categories
