# INFO: Human Writing Patterns

**Doc ID**: HMNWRTPTN-IN01
**Goal**: Document research-validated patterns that distinguish human writing from AI-generated text, providing the evidence base for CONVERSATION_HUMANIZING_RULES.md
**Timeline**: Created 2026-07-16, Updated 1 time
**Strategy**: MEPI (curated patterns over exhaustive catalog) | **Domain**: DEFAULT

**Related documents:**
- `AI_WRITING_DETECTION_RULES.md` - Inverse perspective: detecting AI writing (this doc focuses on replicating human writing)
- `_INFO_HOW_TO_DETECT_AI_ASSISTED_WRITING.md [AIDET-IN01]` - Background on detection principle
- `CONVERSATION_HUMANIZING_RULES.md` - Enforceable rules derived from these findings

## Summary

1. **Burstiness** - Human writing has significantly higher variance in sentence length and complexity than Large Language Model (LLM) output. LLMs produce uniform sentence-length profiles; humans alternate between short punchy sentences and longer flowing ones [VERIFIED] (HMNWRTPTN-SC-ARXV-DIFFDT, HMNWRTPTN-SC-PSICL-FTRCOMP)
2. **Discourse particles** - Sentence-initial discourse particles (well, now, anyway, actually) are among the top 5 features LLMs underuse compared to humans. These markers signal informal register and thinking-in-progress [VERIFIED] (HMNWRTPTN-SC-ARXV-BIBVAR)
3. **Idiolect consistency** - Forensic linguists identify authorship through habitual word sequences (n-grams), function word preferences, punctuation patterns, and greeting/closing repertoires. These are stable across texts by the same author [VERIFIED] (HMNWRTPTN-SC-WRIGHT-NGRAM, HMNWRTPTN-SC-RANLP-STYLMOD)
4. **Email greetings/closings** - Individual greeting and farewell patterns are highly diagnostic for authorship attribution. Less frequent variants are more individuating [VERIFIED] (HMNWRTPTN-SC-WRIGHT-GREET)
5. **Orthographic idiosyncrasies** - Spelling errors, punctuation habits, and formatting choices are stable per-person markers. Human text contains sporadic mistakes; LLM output has near-zero error rate [VERIFIED] (HMNWRTPTN-SC-ARXV-DIFFDT, HMNWRTPTN-SC-KOPPEL-IDIOSYN)
6. **Grammar error rate** - Human text contains sporadic grammatical errors that are part of the individual's writing profile. LLMs produce near-perfect grammar, which is itself a detection signal [VERIFIED] (HMNWRTPTN-SC-ARXV-DIFFDT)

## Research Question

How do experts determine whether text was written by a human? Which measurable features of human writing are absent or reduced in LLM output, and can an AI agent replicate them when ghostwriting?

## Table of Contents

1. [Burstiness (Sentence Length Variation)](#1-burstiness-sentence-length-variation)
2. [Discourse Markers](#2-discourse-markers)
3. [Idiolect and Consistency Anchoring](#3-idiolect-and-consistency-anchoring)
4. [Email Greetings and Closings](#4-email-greetings-and-closings)
5. [Orthographic Consistency](#5-orthographic-consistency)
6. [Grammar Error Rate](#6-grammar-error-rate)
7. [Inverse Mapping from AI Detection Rules](#7-inverse-mapping-from-ai-detection-rules)
8. [Limitations](#8-limitations)
9. [Rule Validation Against Proposed CV-HM Rules](#9-rule-validation-against-proposed-cv-hm-rules)
10. [Sources](#10-sources)

## 1. Burstiness (Sentence Length Variation)

**Definition**: Burstiness measures the variance of sentence-level complexity within a text. Formally defined as the variance of sentence-level perplexities: `Burst(x) = Var{PP(s) | s in sentences(x)}`.

**Research evidence**: Multiple studies confirm that human writing exhibits high burstiness while LLM output is more uniform:
- "Human writing often exhibits high burstiness (varying complexity), whereas AR outputs tend to be more uniform" [VERIFIED] (HMNWRTPTN-SC-ARXV-DIFFDT)
- "LLMG texts demonstrate lower perplexity and burstiness values [...] and more consistent sentence lengths compared to HW texts" [VERIFIED] (HMNWRTPTN-SC-PSICL-FTRCOMP)
- Both autoregressive (AR) models (LLaMA) and diffusion models (LLaDA) reduce burstiness relative to human text [VERIFIED] (HMNWRTPTN-SC-ARXV-DIFFDT)

**Why it happens**: Token-by-token generation optimizes for coherent continuation at each step. The resulting text maintains a consistent register and complexity level. Human writers shift gears - a short emphatic statement after a complex explanation, a parenthetical aside interrupting a formal argument.

**Operationalization for ghostwriting**: Vary sentence length deliberately. Avoid 3+ consecutive sentences of similar word count. Mix single-clause statements (5-10 words) with multi-clause sentences (20-35 words). Match the specific burstiness profile of the person being imitated.

## 2. Discourse Markers

**Definition**: Discourse particles are words or phrases that organize discourse, signal speaker attitude, or manage conversational flow without contributing propositional content. Examples: well, actually, basically, you know, I mean, so, now, anyway, right.

**Research evidence**: The large-scale Biber feature analysis across 11 LLMs and 8 genres found discourse particles in sentence-initial position (f_50: well, now, anyway) among the **top 5 underused features** in LLM text relative to human text. This held across all models and genres tested [VERIFIED] (HMNWRTPTN-SC-ARXV-BIBVAR).

Concessive subordinators (though, although) were also among the top 5 underused features - humans hedge and qualify more naturally than LLMs [VERIFIED] (HMNWRTPTN-SC-ARXV-BIBVAR).

**Why it happens**: LLMs use formal transition words (Moreover, Furthermore, Additionally) as low-cost coherence signals. These occupy high-probability positions. Informal discourse particles (well, actually, basically) are lower-probability in the formal writing that dominates training data. The result: LLM text sounds too polished for casual communication.

**Operationalization for ghostwriting**: Include discourse markers at rates matching the target person's usage. Draw from their observed vocabulary of fillers. Common sets by language:
- English: well, actually, basically, you know, I mean, right, so, anyway
- German: na ja, halt, eigentlich, also, sozusagen, quasi, naja

Do not randomize - maintain a stable set per person. Track observed markers and their approximate frequency.

## 3. Idiolect and Consistency Anchoring

**Definition**: Idiolect = an individual's unique version of language. Forensic linguists use this concept to attribute authorship through measurable stylistic features that remain stable within a person but vary between persons.

**Research evidence**: The premise of forensic authorship attribution is "that distinctive style, however instantiated, constitutes a stable, identifiable signal" [VERIFIED] (HMNWRTPTN-SC-RANLP-STYLMOD).

Key idiolect markers identified in forensic research:
- **Word n-grams**: Habitual word sequences (2-6 words) that become "entrenched" through repeated use. Word n-grams achieved up to 100% accuracy in author identification on the 176-author Enron email corpus [VERIFIED] (HMNWRTPTN-SC-WRIGHT-NGRAM)
- **Function word frequencies**: Preferences for specific function words (the, of, and, but, so) are highly individual and topic-independent [VERIFIED] (HMNWRTPTN-SC-RANLP-STYLMOD)
- **Punctuation patterns**: Comma usage, dash preferences, exclamation marks, multiple question marks - these are stable per-author markers [VERIFIED] (HMNWRTPTN-SC-KOPPEL-IDIOSYN, HMNWRTPTN-SC-FBAUTH-SOCIAL)
- **Syntactic preferences**: Preferred sentence structures, clause ordering, use of passive voice. Part-of-Speech (POS) bigram frequencies are effective discriminators [VERIFIED] (HMNWRTPTN-SC-RANLP-STYLMOD)

**Cross-genre challenge**: Idiolect features shift across discourse types (email vs letter vs essay). The most robust features are function words and n-grams at the lexicogrammatical level, which Barlow (2013) describes as "the profile of the central components of lexicogrammar" [VERIFIED] (HMNWRTPTN-SC-AIFL-IDIOLECT).

**Operationalization for ghostwriting**: Before drafting, analyze the user's prior messages in the conversation History section. Extract:
- Sentence length distribution (short/medium/long ratio)
- Greeting and closing patterns (exact forms used)
- Punctuation habits (comma frequency, dash usage, exclamation marks)
- Discourse marker preferences (which fillers, how often)
- Habitual phrases (recurring word sequences)
Replicate these features consistently across all drafts within that conversation.

## 4. Email Greetings and Closings

**Research evidence**: Wright (2013) analyzed the Enron email corpus and found that greeting and farewell patterns are highly distinctive per author. Testing against a 126-author reference corpus using likelihood ratios, specific greeting/closing forms and combinations remained individuating [VERIFIED] (HMNWRTPTN-SC-WRIGHT-GREET).

Key findings:
- Less frequent greeting variants are MORE diagnostic than common ones ("Hi [Name]" is less individuating than "Hey [Name]," or "Good morning [Name],")
- Authors maintain a small repertoire (typically 2-4 variants); which variant appears correlates with context (recipient, register, thread type), not random alternation
- Workplace culture influences form more than status, social distance, or gender (Waldvogel 2007) [VERIFIED] (HMNWRTPTN-SC-WALDV-GREET)

**Operationalization for ghostwriting**: Maintain per-conversation greeting and closing patterns. Extract the user's repertoire from History and use the dominant form per context. Vary only when History shows a contextual pattern. Never introduce new greetings/closings not already in the user's repertoire unless instructed. Mechanical per-draft rotation is itself an artificial pattern humans do not produce.

## 5. Orthographic Consistency

**Research evidence**: Orthographic features (punctuation, spelling, formatting) are among the four key categories in stylometric authorship attribution alongside lexical, syntactic, and discourse-pragmatic features [VERIFIED] (HMNWRTPTN-SC-RANLP-STYLMOD).

Koppel et al. studied "stylistic idiosyncrasies" including systematic spelling patterns, sentence fragments, run-on sentences, punctuation sequences (multiple question marks), and CAPS usage. These features improved authorship attribution accuracy when combined with standard lexical and POS features [VERIFIED] (HMNWRTPTN-SC-KOPPEL-IDIOSYN).

For languages with orthographic variants (German ß/ss, British/American English), individuals maintain consistent preferences per word. These preferences are stable markers.

**Operationalization for ghostwriting**: Maintain a per-conversation SPELLING_VARIANTS list. Once a spelling choice is observed (e.g., the user consistently writes "weiss" instead of "weiß"), replicate it in all drafts. Same word = same spelling every time. Never randomize.

## 6. Grammar Error Rate

**Research evidence**: "Human text may contain sporadic mistakes; high-quality AI outputs often have near-zero error rate" [VERIFIED] (HMNWRTPTN-SC-ARXV-DIFFDT). The grammar error rate is a measurable discriminator between human and AI text.

**Operationalization for ghostwriting**: Do not over-polish drafts beyond the user's natural level. If the user's prior messages show occasional informal grammar (sentence fragments, missing articles in casual messages), replicate that level. Do NOT introduce artificial errors - instead, match the user's natural precision level.

## 7. Inverse Mapping from AI Detection Rules

The existing `AI_WRITING_DETECTION_RULES.md` provides additional patterns through inversion. Each AI detection signal implies a human writing pattern:

- **AD-SY-03 (Absence of Rough Edges)** implies: Human writing HAS rough edges - personality artifacts, unexpected metaphors, tonal shifts, parenthetical asides
- **AD-SY-05 (Filler Transition Saturation)** implies: Humans use varied paragraph openings, not formulaic transitions (Moreover, Furthermore, Additionally)
- **AD-LX-01 (High-Frequency LLM Vocabulary)** implies: Humans avoid "delve," "crucial," "pivotal," "nuanced," "multifaceted," "landscape" (non-geographic), "tapestry," "foster," "leverage," "underscore"
- **AD-LX-03 (Conjunctive Adverb Overuse)** implies: Humans use informal connectives (but, so, and, still) rather than formal ones (However, Nevertheless, Furthermore)
- **AD-VO-01 (No Personal Reference)** implies: Humans use first-person, anecdotes, and personal experience in non-academic contexts

These patterns are already documented and enforced via the detection rules. The humanizing rules (CV-HM-*) focus on the patterns specific to ghostwriting emails/messages that are NOT covered by general writing advice.

## 8. Limitations

1. **Person-dependent**: All patterns are relative to the individual being imitated. No universal "human frequency" exists for discourse markers, sentence length, or greeting patterns
2. **Register-dependent**: Email writing differs from essay writing differs from WhatsApp. Rules must adapt to channel
3. **Culture-dependent**: Greeting patterns vary by culture and language. German business email closings differ from English ones
4. **Observation minimum**: Reliable idiolect extraction requires sufficient prior messages. With fewer than 5-10 prior messages, anchoring is unreliable
5. **Over-humanizing risk**: Artificially inserting too many discourse markers or errors creates its own detection signal. The goal is matching, not exaggerating

## 9. Rule Validation Against Proposed CV-HM Rules

The user proposed 7 humanizing rules (CV-HM-01 through CV-HM-07). Research validated most, modified some, and dropped one.

- **CV-HM-01 (MECT/APAPALAN Override Scope)** - VALIDATED, REVISED. Initial version suspended MECT/APAPALAN entirely for user-voice drafts. Revised per user decision: MECT/APAPALAN remain the baseline; humanizing is added at 1-5% (greeting/closing, occasional discourse marker or hedge, sentence rhythm). The revision aligns with Limitation 5: over-humanizing creates its own detection signal - sparse humanizing on precise text is the research-consistent approach.
- **CV-HM-02 (Consistency Anchoring)** - VALIDATED. Forensic authorship attribution confirms that extracting and replicating idiolect markers is the foundational approach (sections 3, 4). Kept as-is.
- **CV-HM-03 (Orthographic Variation)** - VALIDATED, RENAMED from "Controlled Orthographic Variation" to "Orthographic Consistency." Research shows spelling habits are STABLE per-person markers (section 5). The rule enforces consistency, not variation.
- **CV-HM-04 (Questions Format)** - DROPPED. No forensic linguistics evidence that question formatting (e.g., numbered vs inline) is an idiolect marker or AI detection signal. This is a formatting preference, not a humanizing pattern. Would add rule overhead without research backing.
- **CV-HM-05 (Fill Words)** - VALIDATED, RENAMED to "Discourse Markers" (CV-HM-04 after renumbering). "Fill words" is colloquial; "discourse markers" is the established term in linguistics research. Biber feature analysis confirmed these are top-5 underused features in LLM text (section 2). Variable renamed from FILLER_WORDS to DISCOURSE_MARKERS.
- **CV-HM-06 (Sentence Rhythm)** - VALIDATED (CV-HM-05 after renumbering). Burstiness research provides strong quantitative backing: humans exhibit significantly higher sentence-length variance than LLMs (section 1).
- **CV-HM-07 (Opening/Closing Patterns)** - VALIDATED (CV-HM-06 after renumbering), REVISED 2026-07-16. Wright (2013) confirms greeting/closing repertoires are highly diagnostic for authorship (section 4). Initial rule operationalized the repertoire as per-draft rotation - corrected per user decision: people are consistent with their habits; use the dominant form, vary only on contextual patterns. Mechanical rotation is LLM-introduced noise.

**Additional sections** added without user proposal: Vocabulary Avoidance and Connective Register. These map directly from existing AD-LX-01 and AD-LX-03 detection rules and are guidance sections (no CV-HM-* ID), not new enforceable rules.

**Post-research additions** (user-instructed, not research-derived):
- Sentence fragments (1-3 words) added to CV-HM-05 - backed by Koppel et al. (sentence fragments as idiosyncratic features, section 5)
- Hedges and qualifiers added to CV-HM-04 - backed by concessive subordinator findings (section 2)
- "Questions and calls-to-action on separate lines" added to CV-HM-05 per user instruction for scannability. This is a formatting preference (like the dropped Questions Format rule), not a humanizing pattern - retained because it serves recipient readability, not AI-detection avoidance
- CV-HM-07 (Native Naturalness) added per user instruction: drafts in any language must read as native writing, never as literal translation from English. Related to machine-translation detection (translationese), not covered by the forensic sources above

## 10. Sources

- **HMNWRTPTN-SC-WRIGHT-NGRAM**: Wright, D. (2017). "Using word n-grams to identify authors and idiolects." International Journal of Corpus Linguistics, 22(2). Enron Email Corpus, 176 authors, n-gram entrenchment. [VERIFIED]
  - URL: https://www.jbe-platform.com/content/journals/10.1075/ijcl.22.2.03wri
- **HMNWRTPTN-SC-WRIGHT-GREET**: Wright, D. (2013). "Stylistic variation within genre conventions in the Enron email corpus." International Journal of Speech, Language and the Law, 20(1), 45-75. Greetings/farewells as authorship markers. [VERIFIED]
  - URL: https://doi.org/10.1558/ijsll.v20i1.45
- **HMNWRTPTN-SC-RANLP-STYLMOD**: Blake et al. (2025). "Modelling the Relative Contributions of Stylistic Features in Forensic Authorship Attribution." RANLP 2025. Enron + TEL corpus, logistic regression, 4 feature categories. [VERIFIED]
  - URL: https://aclanthology.org/2025.ranlp-1.123.pdf
- **HMNWRTPTN-SC-ARXV-BIBVAR**: Reinhart et al. (2025). "Interpretable Stylistic Variation in Human and LLM Writing Across Genres, Models, and Decoding Strategies." 11 LLMs, 8 genres, 67 Biber features. [VERIFIED]
  - URL: https://arxiv.org/html/2604.14111
- **HMNWRTPTN-SC-ARXV-DIFFDT**: Tarim & Onan (2025). "Can You Detect the Difference?" Burstiness, perplexity, grammar-error rate comparison: human vs AR vs diffusion models. [VERIFIED]
  - URL: https://arxiv.org/html/2507.10475
- **HMNWRTPTN-SC-PSICL-FTRCOMP**: Piasecki et al. (2025). "Feature comparison between human-written and LLM-generated documents." 2,400 pairs, 220 features, burstiness and sentence-length consistency. [VERIFIED]
  - URL: https://doi.org/10.1515/psicl-2025-0063
- **HMNWRTPTN-SC-KOPPEL-IDIOSYN**: Koppel, M. & Schler, J. (2003). "Exploiting Stylistic Idiosyncrasies for Authorship Attribution." 99 idiosyncratic features including spelling errors, punctuation sequences, formatting habits. [VERIFIED]
  - URL: https://www.researchgate.net/publication/2950237_Exploiting_Stylistic_Idiosyncrasies_for_Authorship_Attribution
- **HMNWRTPTN-SC-WALDV-GREET**: Waldvogel, J. (2007). "Greetings and Closings in Workplace Email." Journal of Computer-Mediated Communication, 12(2), 456-477. Workplace culture > status/gender for greeting form. [VERIFIED]
  - URL: https://academic.oup.com/jcmc/article/12/2/456/4583009
- **HMNWRTPTN-SC-FBAUTH-SOCIAL**: Molatudi, S. (2014). "Investigating the use of forensic stylistic and stylometric techniques in the analyses of authorship on Facebook." Punctuation, spelling, digitally mediated communication features as style markers. [VERIFIED]
  - URL: http://hdl.handle.net/10500/13324
- **HMNWRTPTN-SC-AIFL-IDIOLECT**: Danu, M. (2025). "Constructing Idiolect: Cognitive Linguistics and the challenges of cross-genre authorship." AIFL Blog. Constructions as cross-genre idiolect markers. [VERIFIED]
  - URL: https://aifl-blog.com/constructing-idiolect-cognitive-linguistics-and-the-challenges-of-cross-genre-authorship-73aa549fee43
- **HMNWRTPTN-SC-COULTHARD-IDIO**: Coulthard, M. (2004). "Author identification, idiolect, and linguistic uniqueness." Applied Linguistics, 25(4), 431-447. Foundational theory of idiolect in forensic context. [VERIFIED]
  - URL: https://doi.org/10.1093/applin/25.4.431

## Document History

**[2026-07-16 13:16]**
- Changed: Section 4 and CV-HM-07 validation - greeting/closing variation is context-driven, not rotation; mechanical per-draft rotation identified as anti-pattern

**[2026-07-16 12:45]**
- Changed: CV-HM-01 validation entry - revised from "suspend MECT/APAPALAN" to "MECT/APAPALAN baseline + 1-5% humanizing" per user decision
- Added: Post-research additions note (fragments, hedges, questions/CTA line formatting)
- Changed: Timeline updated to 1 update

**[2026-07-16 10:45]**
- Fixed: Added Timeline field (INFO-HD-03)
- Fixed: Renamed "Key Findings" to "Summary" (INFO-SM-01)
- Fixed: Numbered H2 headings (INFO-SN-01), promoted subsections to sections
- Fixed: Added Table of Contents (INFO-TC-01/02/03)
- Fixed: Wrote out acronyms on first use - LLM, AR, POS (AP-PR-06)
- Fixed: Added missing URL for Coulthard source (INFO-SC-02)
- Added: Section 9 "Rule Validation Against Proposed CV-HM Rules" documenting validation rationale for all 7 proposed rules

**[2026-07-16 10:30]**
- Initial document created
- 6 research-validated patterns documented
- 11 sources cited with verification labels
- Inverse mapping from AI_WRITING_DETECTION_RULES.md included
