# INFO: Factuality Foundations for Factcheck Workflow Design

**Doc ID**: FCTCHECK-IN01
**Goal**: Establish the epistemological framework that a factcheck workflow must implement to verify claims in agent-generated documents
**Timeline**: Created 2026-08-30, Updated 5 times (2026-08-30 - 2026-08-30)

## Summary

- A document with less than 100% factuality contains claims that do not correspond to verifiable reality, ranging from subtle inaccuracies to complete fabrications [VERIFIED]
- Primary sources are the actual shipped artifacts (running APIs, SDK binaries, source code, executed test output); documentation is already secondary because it is someone's description of the product, not the product itself [VERIFIED]
- Facts are independently verifiable observations; conclusions are derived statements whose correctness depends on both the facts and the reasoning connecting them [VERIFIED]
- LLM hallucinations are not random errors but systematic pattern-completions that produce plausible, internally consistent, yet factually wrong statements [VERIFIED]
- Interpolated knowledge (LLM filling gaps from training patterns) is the most dangerous failure mode because it reads as confident and specific, making it indistinguishable from sourced knowledge without verification [VERIFIED]
- A factcheck workflow must separately verify 1) factual claims against sources, and 2) derivative claims against the logic connecting them to supporting facts [VERIFIED]
- The cost of undetected factual errors compounds through document dependency chains: wrong INFO leads to wrong SPEC leads to wrong IMPL leads to wrong code [VERIFIED]
- **Separation of concerns**: `fact-check.md` verifies "Is it true?" (correspondence to external reality). `verify.md` verifies "Does it conform?" (conformance to DevSystem rules, upstream documents like SPEC for IMPL, templates, and instructions). These are orthogonal. A document can pass verify and fail fact-check, or vice versa. [VERIFIED]
- SOCAS-10 (Gaps in Reasoning) and SOCAS-06 (Incomplete Specifications) are the boundary rules: they check internal logic quality, not external truth. Both stay in `verify.md`. `fact-check.md` goes outside the document to test claims against reality. [VERIFIED]
- Seven SOCAS/APAPALAN/MECT patterns serve as hallucination detection signals that `fact-check.md` should use as input: SOCAS-08 generic phrasing, SOCAS-12 stale information, SOCAS-13 empty structure, AP-PR-07 vague claims, MW-WC-01 wrong term precision, SOCAS-10 assumptions-as-facts, SOCAS-06 unsupported conclusions [VERIFIED]
- **The primary reason for `fact-check.md` is AI agent gullibility.** LLM agents trust all text unconditionally, cannot distinguish aspirational docs from actual behavior, treat documentation as ground truth rather than as claims about ground truth, and have no mechanism to detect when a source is wrong. Without a systematic adversarial process, the agent will build on unverified claims. [VERIFIED]
- **Statistical distribution is not evidence.** LLM confidence measures popularity of a claim in training data, not its truth. In the 1960s, published consensus said sugar was healthy and smoking was safe - the statistical distribution was wrong. An agent that uses "most sources agree" as verification is using popularity as a proxy for truth. The only valid verification terminates in direct observation of the actual system. [VERIFIED]

## Questions

Q1: What does it mean to have less than 100% factuality?
A1: The document contains at least one claim that does not correspond to independently verifiable reality. See Section 1. [VERIFIED]

Q2: What are primary sources and what are secondary sources?
A2: Primary sources are the actual shipped artifacts (running system, source code, test output). Documentation is already secondary - it is someone's description of the product, not the product itself. See Section 2. [VERIFIED]

Q3: What does it mean to have evidence and proof of factuality?
A3: Evidence supports a claim with varying strength. Proof is evidence sufficient for a rational actor to accept the claim as established. See Section 3. [VERIFIED]

Q4: What is the difference between facts and conclusions?
A4: Facts are directly observable and verifiable. Conclusions are derived via reasoning from facts and inherit the uncertainty of their weakest link. See Section 4. [VERIFIED]

Q5: What is the impact of low factuality, hallucinations, and interpolated knowledge?
A5: Cascading errors through document dependencies, trust erosion, wasted implementation time, and silent defects in production systems. See Section 5 and 7. [VERIFIED]

Q6: Why do AI agents need a fact-check workflow that humans do not?
A6: Humans develop calibrated skepticism through experience. Agents have none. An agent trusts all text equally - official docs, blog posts, its own previous hallucinations, and actual source code are all just "information" with no inherent trustworthiness ranking. The agent cannot ask "who wrote this, when, and did they test it?" unless a workflow forces it. See Section 6.1. [VERIFIED]

Q7: What is the correct trust hierarchy for verifying claims?
A7: Observed behavior > source code > official documentation > community sources > LLM output. Every verification action must push toward the left of this chain. Reading more text (even authoritative text) is weaker than a single direct observation of the actual system. See Section 6.4. [VERIFIED]

Q8: Why is consensus not evidence?
A8: Statistical distribution of text measures popularity, not truth. If 95% of training data says X, the LLM produces X with high confidence - but the 95% may all derive from the same wrong source, or the consensus itself may be wrong (1960s medical literature on sugar/tobacco). "Multiple sources agree" only adds value when sources independently observed reality, not when they independently read the same docs. See Section 6.5. [VERIFIED]

Q9: What is the difference between fact-check.md and verify.md?
A9: `verify.md` = "Does it conform?" Compares artifact to governing sources (rules, SPEC, IMPL, templates). Trusts upstream documents as authoritative. `fact-check.md` = "Is it true?" Compares claims to external reality. Trusts nothing. Verify catches "IMPL forgot FR-03 from SPEC." Fact-check catches "FR-03 is based on a hallucinated API feature." See Section 10. [VERIFIED]

Q10: What makes a verification valid?
A10: A verification is valid only if the evidence chain terminates in direct observation of the actual system (calling the API, reading the source code, running the test). Reading text - however authoritative, however many sources - produces claims about reality, not evidence of reality. "I read it in three places" is not verification. "I called the API and got this response" is verification. See Section 3.1 and 6.5. [VERIFIED]

Q11: How do you fact-check code?
A11: Code is both a claim and a testable artifact. Five categories: claims IN code (comments vs actual behavior), claims ABOUT code (IMPL says X but code does Y), code ITSELF as implicit behavioral claim (run it), dependency claims (does this import/method/signature actually exist?), and configuration claims (is this value actually used?). The strongest fact-check for code is execution. See Section 9.3. [VERIFIED]

Q12: Which claims should be prioritized for verification?
A12: Two priority axes. By input type: deep research and INFO first (highest claim density, first in document chain), SPEC and IMPL second (hallucinated requirements propagate downstream). By triage signal: claims matching hallucination patterns (generic phrasing, no source citation, excessive specificity, confident negatives, cross-version blending) are verified first. See Sections 9.4 and 12. [VERIFIED]

Q13: Can you fact-check an opinion?
A13: No. Unfalsifiable claims ("the code is clean," "performance is acceptable") are not factual claims and cannot be tested against reality. The workflow must distinguish falsifiable claims (can be confirmed or refuted) from subjective assessments (can only be argued). Flag unfalsifiable claims, do not try to verify them. See Section 8.6. [VERIFIED]

Q14: When in the document lifecycle should fact-checking happen?
A14: Before verification. Recommended sequence: `/fact-check` first (are the claims true?), then `/verify` (does it conform?). Catching a wrong claim before it enters the SPEC prevents verify from faithfully propagating it through IMPL, Code, and TEST. The cost model strongly favors early detection. See Sections 7.4 and 10.4. [VERIFIED]

Q15: Why is documentation not a primary source?
A15: Documentation is written by humans who may misunderstand the product, write docs before the feature ships, fail to update docs when behavior changes, describe intended behavior rather than actual behavior, or simplify for readability at the cost of accuracy. The shipped product (running API, SDK source code, test output) is the primary source. Documentation is a claim about the product, not the product itself. See Section 2.1. [VERIFIED]

## Table of Contents

1. [What Less Than 100% Factuality Means](#1-what-less-than-100-factuality-means)
2. [Primary and Secondary Sources](#2-primary-and-secondary-sources)
3. [Evidence, Proof, and Verification](#3-evidence-proof-and-verification)
4. [Facts vs Conclusions](#4-facts-vs-conclusions)
5. [LLM Hallucinations and Interpolated Knowledge](#5-llm-hallucinations-and-interpolated-knowledge)
6. [AI Agent Gullibility and the Trust Problem](#6-ai-agent-gullibility-and-the-trust-problem)
7. [Impact of Low Factuality in Document Systems](#7-impact-of-low-factuality-in-document-systems)
8. [Claim Taxonomy for Verification](#8-claim-taxonomy-for-verification)
9. [Input Types: What Can Be Fact-Checked and How](#9-input-types-what-can-be-fact-checked-and-how)
10. [Separation of Concerns: fact-check.md vs verify.md](#10-separation-of-concerns-fact-checkmd-vs-verifymd)
11. [Rule Mapping: Which Rules Belong Where](#11-rule-mapping-which-rules-belong-where)
12. [Hallucination Detection Signals from Existing Rules](#12-hallucination-detection-signals-from-existing-rules)
13. [Conclusions](#13-conclusions)
14. [Next Steps](#14-next-steps)
15. [Sources](#15-sources)
16. [Document History](#16-document-history)

## 1. What Less Than 100% Factuality Means

A document achieves 100% factuality when every claim in it corresponds to independently verifiable reality. Any deviation from this produces a factuality deficit. The deficit has distinct severity levels:

- **Inaccuracy**: A claim that is approximately correct but wrong in detail. "The API returns JSON" when it actually returns JSON-LD. The reader forms a mostly-correct mental model with a subtle flaw.
- **Misattribution**: A correct claim linked to the wrong source. "According to the OAuth2 spec, tokens expire after 1 hour." The spec says no such thing; the default is implementation-specific. The claim about expiration may be true for a specific provider, but attributing it to the spec is wrong.
- **Omission**: A factually correct statement that becomes misleading through missing context. "The function accepts a string parameter" when it actually accepts a string and an optional integer that changes behavior entirely.
- **Fabrication**: A claim with no basis in reality. "The library provides a `retryWithBackoff()` method" when no such method exists. This is the most dangerous type because the reader cannot detect it without checking.
- **Interpolation**: A claim constructed by blending real patterns into a plausible but non-existent whole. "The API uses bearer tokens with a 15-minute TTL and automatic refresh via the `/auth/renew` endpoint." Each element is plausible; the combination may be entirely invented.

The key insight: **factuality is not binary at the document level**. A document with 50 claims where 49 are correct and 1 is fabricated is 98% factual but may be 100% misleading if the wrong claim is the one the reader acts on.

### 1.1 The Verification Asymmetry

Checking factuality is asymmetric: falsifying a claim requires finding one counterexample, but verifying a claim requires exhaustive checking against the source of truth. A factcheck workflow must account for this. It is cheaper to identify claims that NEED checking than to verify every claim is correct.

### 1.2 Factuality vs Truthfulness

A factcheck workflow verifies factuality (correspondence to verifiable external reality), not truthfulness (correspondence to the author's belief). Whether an LLM "believes" its output is academically interesting but operationally irrelevant. The operational problem: an AI agent ACTS on its output. It reads a claim, treats it as fact, and builds further work on it. The agent has no skepticism mechanism. It cannot ask "wait, is this actually true?" unless a workflow forces it to. This is why `fact-check.md` must exist as a separate, adversarial process - it provides the skepticism that the agent inherently lacks.

## 2. Primary and Secondary Sources

### 2.1 Source Hierarchy

Sources form a hierarchy based on proximity to observable reality. The critical distinction: a description of reality is NOT reality. A technical writer's description of an API is that writer's CLAIM about what the API does, not what it actually does.

- **Primary sources**: The actual artifacts themselves, observable and testable
  - The running API endpoint (call it, observe the response)
  - The shipped SDK binary or source code (read it, execute it)
  - The actual database schema (query it)
  - Direct measurement or test output (reproducible observation)
  - Government records, legal documents, original datasets
  - The author's own first-hand observation or creation

- **Secondary sources**: Human descriptions of primary sources (claims about reality)
  - Official API documentation (a technical writer's interpretation of the shipped product - may be wrong, outdated, aspirational, or written before the feature was implemented)
  - RFC specifications (define what a protocol SHOULD be, not what any implementation actually IS)
  - Blog posts, tutorials, Stack Overflow answers (interpretations of docs or experience)
  - Academic papers analyzing existing data
  - News articles reporting events

- **Tertiary sources**: Compilations or summaries of secondary sources
  - Textbooks, encyclopedias, review articles
  - "Awesome lists" curating tools and resources
  - LLM training data (an implicit tertiary source blending millions of documents)

**Why official documentation is secondary, not primary**: Documentation is written by humans who may misunderstand the product, write docs before the feature ships, fail to update docs when behavior changes, describe intended behavior rather than actual behavior, or simplify for readability at the cost of accuracy. A developer who trusts the docs without testing the actual system is trusting a CLAIM about reality, not reality itself. An AI agent does this by default - it reads docs and treats them as ground truth. This is the fundamental gullibility problem.

### 2.2 The Source Degradation Chain

Each step away from the primary source introduces degradation:

```
Primary (the actual running API - call it, observe the response)
  └─> Secondary (official docs - a tech writer's description of the API)
       └─> Tertiary (blog post explaining the docs)
            └─> Quaternary (LLM training on blogs and docs)
                 └─> Quinary (LLM output claiming API behavior)
                      └─> Senary (DevSystem document quoting LLM output as fact)
```

Note: most people (and all AI agents) treat the docs as primary. This is the first and most common reasoning error. The docs already introduce one layer of human interpretation between you and reality. When an agent reads docs and writes an INFO document, the agent is already at the tertiary level - two steps removed from the actual system.

At each step:
- **Interpretation drift**: The summarizer understood 95% correctly. 5% was misinterpreted. The next summarizer inherits that 5% error and adds their own.
- **Context loss**: The actual API returns a timeout header of 30 seconds for v2.3. The docs say "default timeout is 30 seconds" without version qualifier. By the tertiary level, "the timeout is 30 seconds" becomes an absolute claim about all versions.
- **Recency decay**: The actual API was updated. Docs referencing the old behavior persist for weeks or months. Blog posts referencing old docs persist for years. LLM training data blends old and new into an inconsistent hybrid.
- **Aspirational contamination**: Docs written before a feature ships describe intended behavior. The feature ships differently, or not at all. The docs are never corrected. Every downstream source inherits the aspirational claim as fact.

### 2.3 Implications for Factchecking

A factcheck workflow must:
1. Identify whether a claim cites a source at all
2. Classify the source tier (primary, secondary, tertiary)
3. For secondary/tertiary claims, trace back toward the primary source
4. Flag claims with no source attribution as requiring verification

The existing DevSystem already partially addresses this: INFO documents require source IDs (INFO-SC-01 through INFO-SC-05), and source entries must include a primary finding. The factcheck workflow extends this by verifying that the documented finding actually matches what the source says.

## 3. Evidence, Proof, and Verification

### 3.1 Evidence Strength Spectrum

Evidence for a factual claim exists on a spectrum. The critical gap is between claims-about-reality (someone wrote something down) and observed-reality (someone ran the system and saw the result):

- **Anecdotal**: "Someone on a forum said it works this way." Weakest form. Might be true, might reflect one person's misconfigured environment.
- **Documented**: "The official docs state X." This is NOT direct evidence of system behavior. It is a CLAIM by a technical writer about system behavior. Docs can be wrong, outdated, aspirational, pre-release, or written by someone who misunderstood the product. An AI agent treats docs as ground truth. A critical thinker treats docs as a hypothesis to be tested.

  ── gap: everything above is claims about reality; everything below is observed reality ──

- **Demonstrated**: "Running the code produces output Y." Fundamentally stronger than any written claim, because it is direct observation of the actual system. May be environment-specific, but is real.
- **Measured**: "The benchmark shows 150ms p99 latency across 10,000 requests." Strongest practical evidence: quantitative, reproducible, directly observed.

AI agents almost never cross the gap. They read docs, write claims, and move on. `fact-check.md` must force the crossing: when a claim matters, demand demonstrated or measured evidence, not just a doc citation.

### 3.2 What Constitutes Proof

Proof is not absolute certainty. It is evidence sufficient for a rational actor to accept the claim for the purpose at hand. The threshold depends on stakes:

- **Low stakes** (informational context): A credible secondary source (official docs, release notes) is sufficient. "Python 3.12 added the `itertools.batched` function" can be accepted from the release notes without running Python. The risk of doc error is low and the cost of being wrong is trivial.
- **Medium stakes** (design decisions): Cross-reference docs with source code or test the actual system. Before building a system around an API feature, do not just read the docs - verify the feature exists by reading the SDK source or making a test call. Docs describe what the product SHOULD do; the actual system reveals what it DOES.
- **High stakes** (production behavior): Demonstrated proof required. Before claiming "the retry logic handles 503 errors," run a test that triggers a 503 and observe the retry. No amount of documentation can substitute for observed behavior.

### 3.3 Verification Methods

For a factcheck workflow, practical verification methods are:

- **Reproduction** (strongest): Execute code, run a test, call an API. Direct observation of the actual system. Not always feasible for an agent workflow, but the only method that produces primary evidence.
- **Source comparison**: Read the cited source, compare to the claim. Feasible for any claim with a URL or file reference. But remember: the cited source is itself a claim about reality, not reality itself.
- **Negative testing**: Search for counterexamples. If a claim says "all API responses include a `status` field," search for an endpoint that does not.
- **Logical consistency**: Check if derived claims follow from their premises. Does not verify the premises, but catches reasoning errors.
- **Cross-referencing** (weakest, often misleading): Check the claim against multiple sources. **WARNING: Consensus is not evidence.** Three sources agreeing does not increase truth probability if they all derive from the same wrong origin. Ten blog posts repeating the same incorrect documentation are ten copies of one error, not ten independent confirmations. Cross-referencing only adds value when sources reach the same conclusion through genuinely independent paths to observable reality (e.g., two people independently tested the API and got the same result). Sources that all read the same docs and restate them are not independent.

### 3.4 The Unfalsifiable Claim Problem

Some claims resist verification:
- "This is the best approach." Subjective, not factual.
- "The system handles edge cases gracefully." Vague, untestable.
- "Performance is acceptable." Depends on undefined criteria.

A factcheck workflow should flag unfalsifiable claims as unverifiable, not attempt to verify them. They may still be valid design opinions, but they are not factual claims.

## 4. Facts vs Conclusions

### 4.1 Definitions

- **Fact**: A statement about observable reality that can be independently verified. "Python 3.12 was released on 2023-10-02." "The `requests` library raises `ConnectionError` on DNS failure." Facts do not depend on interpretation.

- **Conclusion**: A statement derived from one or more facts via reasoning. "Therefore, we should use Python 3.12 for this project because it includes `itertools.batched` which simplifies our batch processing code." The conclusion depends on the facts being correct AND the reasoning being sound.

### 4.2 The Error Propagation Model

A conclusion inherits uncertainty from two independent sources:

```
Conclusion correctness = f(fact correctness, reasoning correctness)
```

Four failure combinations:

- **Correct facts + correct reasoning = correct conclusion**: The ideal case.
- **Correct facts + flawed reasoning = wrong conclusion**: "The API supports OAuth2 [fact]. Therefore we don't need API keys [wrong conclusion, because OAuth2 doesn't preclude API key support]."
- **Wrong facts + correct reasoning = wrong conclusion**: "The API has a 10-request-per-second rate limit [wrong]. Therefore we need a request queue [unnecessary conclusion based on wrong fact]."
- **Wrong facts + flawed reasoning = accidentally correct conclusion**: Dangerous. The conclusion may be right, but for the wrong reasons. Any change in context will break it.

### 4.3 Conclusion Chains

In document systems, conclusions feed into further conclusions:

```
Fact A ─────────────────────┐
Fact B ───> Conclusion 1 ───┤
Fact C ─────────────────────┘──> Conclusion 2 ──> Design Decision ──> Implementation
```

If Fact B is wrong, Conclusion 1 is suspect, Conclusion 2 inherits the uncertainty, and the implementation may be built on a flawed foundation. The deeper the chain, the harder it is to trace back to the source of error.

### 4.4 Implications for Factchecking

A factcheck workflow must handle facts and conclusions with different strategies:

- **Facts**: Verify against primary sources. Binary check: does the source confirm the claim?
- **Conclusions**: First verify the supporting facts, then evaluate the reasoning. A conclusion from verified facts with sound reasoning is trustworthy. A conclusion from unverified facts is suspect regardless of reasoning quality.

## 5. LLM Hallucinations and Interpolated Knowledge

### 5.1 Hallucination Taxonomy

LLM hallucinations are not random. They follow predictable patterns:

- **Confident fabrication**: The model generates a specific, detailed claim that sounds authoritative but has no basis. "The `requests.Session` object has a `retry_strategy` parameter that accepts a `Retry` object." Plausible, specific, wrong.

- **Pattern completion**: The model has seen similar patterns and completes them. If 80% of HTTP libraries have a `.timeout` property, the model will confidently state that the remaining 20% do too.

- **Version conflation**: The model blends information from different versions. "The API accepts `format=json` as a query parameter" may have been true in v1 but removed in v2. The model does not track version boundaries.

- **Plausible synthesis**: The model combines real elements into a non-existent whole. "The `boto3` library's `S3.Client.upload_file()` method accepts a `progress_callback` parameter." Both `upload_file` and progress callbacks exist in boto3, but not in that combination.

### 5.2 Interpolated Knowledge

Interpolated knowledge is the most insidious hallucination type. It occurs when the model fills gaps in its training data by interpolating from surrounding patterns:

- The model knows Library X has features A, B, C, D, and E
- Feature F does not exist
- But features A-E form a pattern that suggests F should exist
- The model generates a confident, detailed description of feature F

This is dangerous because:
1. The output reads like expert knowledge, not speculation
2. The claim is internally consistent with real features
3. Only someone who knows the library intimately will catch it
4. Search results may not directly contradict it (absence of evidence is not evidence of absence)

### 5.3 The Source-Grounding Principle

The antidote to hallucination is source-grounding: every factual claim must be traceable to a specific, verifiable source. A factcheck workflow enforces source-grounding by:

1. **Identifying unsourced claims**: Claims with no `[SOURCE_ID]` or inline source link
2. **Verifying sourced claims**: Checking that the source actually says what the document claims
3. **Flagging interpolations**: Claims that cite a source but extend beyond what the source states

### 5.4 Detection Signals

Hallucinations and interpolations share telltale patterns:

- **Excessive specificity without citation**: "The timeout is exactly 30 seconds" with no source
- **Confident negatives**: "The API does not support batch operations" - negative claims are harder to verify and easier to hallucinate
- **Precise numbers in qualitative context**: "This improves performance by approximately 40%" without measurement
- **Feature descriptions matching no documentation**: Detailed behavior descriptions that cannot be found in any official source
- **Cross-version blending**: Claims mixing terminology or features from different versions

## 6. AI Agent Gullibility and the Trust Problem

This section is the primary justification for `fact-check.md`. The hallucination problem (Section 5) describes what goes wrong on the OUTPUT side. The gullibility problem describes what goes wrong on the INPUT side. Together they form a closed loop: the agent generates plausible falsehoods (hallucination) and then reads and trusts those falsehoods (gullibility) in subsequent sessions.

### 6.1 The Fundamental Deficiency

An AI agent has no mechanism to distinguish between:

- Documentation that accurately describes current system behavior
- Documentation written before the feature shipped (aspirational)
- Documentation that was never updated after behavior changed (stale)
- Documentation where the technical writer misunderstood the product (wrong)
- Documentation that describes intended behavior, not actual behavior (spec vs reality)
- Marketing material dressed up as technical documentation (promotional)
- Auto-generated docs from code comments that were never reviewed (unverified)
- Stack Overflow answers that were upvoted for confidence, not correctness (popular but wrong)

To the agent, all text has equal authority. A line in the official docs, a blog post from 2019, a hallucinated claim from a previous session, and the actual source code of the system are all "information" with no inherent trustworthiness ranking. The agent cannot be skeptical. It cannot ask "wait - who wrote this, when, and did they actually test it?" unless a workflow forces it to ask those questions.

### 6.2 Six Gullibility Failure Modes

**1. Authority bias**: The agent trusts "official" sources unconditionally. Official documentation says the API supports feature X. The agent writes this into the SPEC. But feature X was announced, documented, and never shipped. The docs were never corrected. No amount of reading the docs harder will reveal this - only calling the API will.

**2. Recency blindness**: The agent cannot tell when a source was last verified against reality. A doc page may show "last updated 2024-03-15" but the update was a typo fix, not a verification of technical accuracy. The agent treats it as current.

**3. Confidence-as-evidence**: The agent treats its own confident output as evidence. If it generates "the API uses OAuth2 with PKCE" with high confidence, it processes this in future context as an established fact. Confidence is a statistical artifact of token prediction, not a measure of correspondence to reality.

**4. Consensus fallacy**: If three sources agree, the agent treats the claim as more likely true. But agreement is not evidence. In the 1960s, the overwhelming consensus in published medical literature was that sugar was healthy and dietary fat was the primary cause of heart disease. Tobacco companies funded research showing smoking was safe. The statistical distribution of published text SUPPORTED these false claims. An LLM trained on 1960s medical literature would confidently recommend sugar and dismiss smoking risks - because that is what the majority of sources said. The question "what do most sources say?" is fundamentally different from "what is true?" The agent cannot tell the difference.

**5. Negative claim credulity**: "The API does not support batch operations." The agent accepts this because it found no docs mentioning batch operations. But absence from documentation is not absence from the system. The feature may exist undocumented, or may have been added after the docs were written.

**6. Self-trust loop**: The agent reads its own previous output (INFO from session 1) as input (context for session 2). Each session adds a layer of unverified claims. By session 4, the agent is building on claims that were never verified against reality but have been repeated so many times they feel established. This is the document-system equivalent of an echo chamber.

### 6.3 Why Existing Workflows Cannot Solve This

**`/verify`** checks conformance to governing sources: Does the IMPL implement everything in the SPEC? Does the code match the IMPL plan? Are DevSystem rules (APAPALAN, MECT, SOCAS) followed? But verify TRUSTS its upstream sources as authoritative. It will catch "the IMPL forgot FR-03 from the SPEC" but it cannot catch "FR-03 in the SPEC is based on a hallucinated API feature that does not exist." A fabricated API method name written into the SPEC will be faithfully propagated to IMPL, to code, and verified as "conforming" at every stage.

**`/improve`** finds contradictions and structural issues within the document. It cannot reach outside the document to check whether claims match reality.

**`/critique`** (Devil's Advocate) questions assumptions and logic. It may flag "is this assumption verified?" but does not perform the actual verification. It identifies suspicion, not truth.

**`/research`** gathers information but is itself subject to gullibility. The research workflow reads sources and summarizes them - it does not test claims against the actual systems being described.

None of these workflows cross the gap from claims-about-reality to observed-reality (Section 3.1). `fact-check.md` is the only workflow designed to cross that gap: it takes a claim, identifies what would confirm or refute it, and executes the test.

### 6.4 The Trust Inversion

Human developers have an implicit trust model: they trust their own experience and direct observation over documentation, and documentation over blog posts. They develop calibrated skepticism through years of discovering that docs lie.

AI agents have an inverted trust model: they trust whatever text they processed most recently, weighted by token frequency in training data. This means:

- A claim repeated in 10,000 blog posts outweighs a contradicting statement in the actual source code (the agent may never read the source code)
- A confident paragraph in an LLM's previous output outweighs a tentative note in the official changelog
- An outdated but detailed explanation outweighs a terse but current error message from the actual API

`fact-check.md` must enforce the correct trust hierarchy: observed behavior > source code > official docs > community sources > LLM output. Every verification action must push toward the left of this chain, not accept evidence from the right.

### 6.5 Statistical Distribution Is Not Evidence

This is the deepest epistemological problem with LLM-based agents and the primary reason `fact-check.md` must ask "Is it true?" rather than "What is the consensus?"

An LLM's output is a function of statistical distribution in its training data. If 95% of training documents say X, the model will produce X with high confidence. But statistical distribution of text measures POPULARITY of a claim, not its TRUTH. These are fundamentally different properties:

- In the 1960s, the statistical distribution of published medical literature said sugar was healthy. The sugar industry funded research to shift blame to dietary fat. An LLM trained on that era's corpus would confidently recommend sugar and dismiss smoking risks. The distribution was wrong.
- Vendor marketing material outnumbers critical analysis by orders of magnitude. An LLM trained on the web will reproduce marketing claims more readily than their refutations, because marketing is published at scale and criticism is published by individuals.
- SEO-optimized content, astroturfing, and AI-generated text increasingly dominate web corpora. These are engineered to be statistically prominent, not to be true.
- Outdated information vastly outnumbers corrections. A claim true in 2020 and corrected in 2024 has 4 years of reinforcement vs months of correction. The statistical weight favors the outdated claim.

**The implication for AI agents**: An agent that uses "most sources agree" as evidence is using popularity as a proxy for truth. This is the same epistemological error as believing the earth is flat because most people in 1400 said so. The number of sources is irrelevant. The only question is: what does the actual system do when you test it?

**The implication for `fact-check.md`**: The workflow must never accept "multiple sources confirm" as a verification method unless those sources independently observed the actual system. The only valid verification is direct observation or a chain of evidence that terminates in direct observation. "I read it in three places" is not verification. "I called the API and got this response" is verification. "I read the source code and the function does X" is verification. The distinction is between reading claims (however many) and observing reality (even once).

**What `fact-check.md` must ask**: Not "What do sources say?" but "Is it true?" Not "Do multiple sources agree?" but "Has anyone actually tested this?" Not "Is this the consensus?" but "What happens when you run it?"

## 7. Impact of Low Factuality in Document Systems

### 7.1 The Cascading Error Problem

In the DevSystem document chain:

```
INFO (research) ──> SPEC (requirements) ──> IMPL (plan) ──> Code
```

A factual error in INFO propagates silently:

1. **INFO**: "The API requires OAuth2 with PKCE for all endpoints" [wrong: only for user-facing endpoints]
2. **SPEC**: FR-01 mandates PKCE for the internal service-to-service integration
3. **IMPL**: Implementation plan includes PKCE flow for the backend service
4. **Code**: Complex PKCE implementation where a simple API key would suffice

The cost at each stage:
- Fixing in INFO: edit one sentence
- Fixing in SPEC: rewrite requirement, check downstream
- Fixing in IMPL: rewrite implementation steps, re-estimate effort
- Fixing in Code: refactor authentication module, rewrite tests

### 7.2 Trust Erosion

When a reader discovers one factual error in a document, every other claim becomes suspect. The reader must now verify each claim independently, eliminating the document's value as a trusted reference. This is especially damaging for:
- SPEC documents that define what to build (wrong spec = wrong product)
- INFO documents used as research references across sessions
- FAILS.md entries that prevent repeating mistakes (wrong lesson = repeated mistake)

### 7.3 The Feedback Loop Problem

LLM agents that read their own previous output as context create a feedback loop:

```
Session 1: Agent writes INFO with hallucinated claim X
Session 2: Agent reads INFO, treats X as established fact
Session 3: Agent cites X in SPEC as verified requirement
Session 4: Agent implements X in code
```

Without factchecking, a single hallucination in session 1 becomes "verified" through repetition across sessions. The factcheck workflow must break this loop by verifying claims against external sources, not against other DevSystem documents.

### 7.4 Cost Asymmetry

Prevention is vastly cheaper than correction:
- **Factchecking during writing**: Minutes per document. Flag issues before they propagate.
- **Discovering errors during implementation**: Hours. Requires tracing back through document chain.
- **Discovering errors in production**: Days to weeks. Requires root cause analysis, fix, re-test, re-deploy.

This cost asymmetry is the fundamental justification for a factcheck workflow: a small investment in verification prevents large downstream costs.

## 8. Claim Taxonomy for Verification

Based on the analysis above, claims in DevSystem documents fall into distinct categories requiring different verification strategies:

### 8.1 Category 1: Factual Claims (directly verifiable)

Claims about observable, measurable reality that can be checked against a primary source.

- **Examples**: "The API returns HTTP 429 on rate limit." "Python 3.12 requires at least 3.11 syntax." "The function accepts two parameters."
- **Verification**: Observe the actual system (call the API, read the source code, run the function). If direct observation is impractical, compare to docs but mark as `[VERIFIED: docs only]` not `[VERIFIED]` - docs are claims about reality, not reality itself.
- **Evidence required**: Direct observation (strongest) or source citation with matching content (weaker)

### 8.2 Category 2: Derivative Claims (logically verifiable)

Conclusions, recommendations, or assessments derived from factual claims via reasoning.

- **Examples**: "Therefore, we should implement exponential backoff." "This means the cache TTL must be shorter than the token lifetime." "The modular approach reduces coupling."
- **Verification**: 1) Verify supporting facts, 2) Evaluate reasoning chain
- **Evidence required**: Sound logic connecting verified facts to the conclusion

### 8.3 Category 3: Sourced Attributions (citation-verifiable)

Claims that attribute a statement or finding to a specific source.

- **Examples**: "According to the OAuth2 RFC, refresh tokens MUST be bound to the client." "The benchmark results show 150ms p99 latency."
- **Verification**: Read the cited source, confirm it says what the document claims
- **Evidence required**: Direct match between source content and attributed claim

### 8.4 Category 4: Quantitative Claims (measurement-verifiable)

Claims involving specific numbers, measurements, or quantities.

- **Examples**: "The API has a 100-request-per-minute rate limit." "The response payload is 2.4KB on average." "Migration takes approximately 3 hours."
- **Verification**: Confirm the number against a primary source or measurement
- **Evidence required**: Source citation or measurement data

### 8.5 Category 5: Existence Claims (presence-verifiable)

Claims about the existence or non-existence of features, methods, files, or capabilities.

- **Examples**: "The library provides a `retry()` decorator." "The API does not support pagination." "The config file includes a `timeout` field."
- **Verification**: Check documentation, source code, or API explorer
- **Evidence required**: Source showing presence or exhaustive search showing absence
- **Special risk**: Negative existence claims ("does not support X") are hard to verify. Absence from docs does not prove absence from the system.

### 8.6 Category 6: Unfalsifiable Claims (not verifiable)

Subjective assessments, vague statements, or claims that cannot be tested.

- **Examples**: "The code is clean." "Performance is acceptable." "This is the recommended approach."
- **Verification**: Not possible. Flag as opinion/assessment, not factual claim.
- **Action**: The factcheck workflow should identify these and flag them, not try to verify them.

## 9. Input Types: What Can Be Fact-Checked and How

The claim taxonomy (Section 8) defines WHAT kinds of claims exist. This section defines WHERE those claims appear and how the verification approach changes per input type. Not all inputs are equal: an INFO document full of API behavior claims requires different treatment than a TASKS list or a PDF from an unknown author.

### 9.1 External Sources (General Writing)

Content from outside the DevSystem. The agent encounters these during `/research`, `/deep-research`, `/transcribe`, or when the user provides reference material. These sources are NEVER primary - they are always someone's claim about reality.

**Web pages (HTML)**:
- **Claim density**: Varies wildly. API docs are dense. Blog posts mix claims with opinion.
- **Volatility**: Pages change or disappear. A URL valid today may 404 tomorrow. A page updated yesterday may contradict the version the agent read last week.
- **Fact-check approach**: Identify factual claims. For each, ask: does this match the actual system? Prefer testing over trusting the page. Archive or screenshot critical pages because they may change.
- **Trust signal**: Check authorship (vendor docs vs random blog), publication date, whether the page cites its own sources. A page with no date, no author, and no sources is a low-trust input.

**PDFs**:
- **Claim density**: Often high (whitepapers, specifications, reports).
- **Volatility**: Static snapshots - content does not change, but the reality it describes may have changed since publication.
- **Fact-check approach**: Treat publication date as the upper bound of accuracy. A 2022 PDF describing a 2026 API is 4 years stale. Check whether the claims still hold.
- **Special risk**: PDFs from vendors are often marketing material formatted to look like technical documentation. The format (professional layout, charts, logos) creates false authority.

**Ebooks**:
- **Claim density**: High in technical books. The entire content is claims.
- **Volatility**: Low - published and rarely updated. But tech books become outdated faster than any other genre.
- **Fact-check approach**: Check edition and publication year. Cross-reference specific claims against current system behavior. A book about Python 3.8 may be wrong about Python 3.12.

**Press and news articles**:
- **Claim density**: Medium. Mix of factual reporting and editorial framing.
- **Fact-check approach**: Distinguish factual claims ("Company X released product Y") from editorial claims ("This will revolutionize the industry"). Check ownership and funding - press can be industry-funded, like the 1960s sugar/tobacco examples (Section 6.5). Factual claims in press are secondary sources at best.
- **Special risk**: Press releases disguised as news articles. Written by the company's PR team, published verbatim by outlets.

**Images**:
- **Claim density**: Variable. Screenshots of code, terminal output, or UI contain implicit factual claims. Diagrams encode architectural claims.
- **Fact-check approach**: Claims embedded in images cannot be text-searched or automatically extracted. Must be manually identified. A screenshot of an API response is stronger evidence than a text description of the same response (harder to fabricate, but can still be outdated or staged).
- **Special risk**: Images create false authority through visual concreteness. A screenshot from 2020 showing API behavior may not reflect 2026 behavior, but the visual specificity makes it feel current.

**Unknown source**:
- **Claim density**: Unknown.
- **Fact-check approach**: Treat EVERY claim as unverified until the source is identified and evaluated. Unknown source = unknown reliability. Do not extract claims from unknown sources into DevSystem documents without independent verification against the actual system.

### 9.2 DevSystem Document Types

Content produced by the agent or the user within the DevSystem. Each document type has a different claim profile and requires a different fact-check strategy.

**INFO documents** (highest priority for fact-checking):
- **Claim density**: Very high. The entire document is claims gathered from research.
- **Claim types**: Factual (Section 8.1), sourced attributions (8.3), quantitative (8.4), existence (8.5).
- **Fact-check approach**: This is the PRIMARY fact-check target. Every finding must trace to a source. Every source must actually say what the INFO claims. For technical INFO: test claims against the actual system where feasible. The INFO is where hallucinations enter the document chain - catching them here prevents downstream propagation.
- **What to check**: Do cited sources exist? Do they say what the document claims? Are version numbers current? Do described APIs/methods/features actually exist?

**SPEC documents** (high priority):
- **Claim density**: High. Functional requirements (FR), design decisions (DD), implementation guarantees (IG) all contain factual claims about external systems.
- **Claim types**: Factual claims about the system being specified against, existence claims about APIs/features the spec depends on, derivative claims (conclusions drawn from research).
- **Fact-check approach**: For each FR and DD, trace the factual basis. "FR-03: The system uses OAuth2 with PKCE" - is this based on verified API behavior or an assumption from reading docs? Check that external dependencies actually exist and behave as the SPEC assumes. This is where fact-check prevents verify from faithfully propagating a hallucinated requirement.
- **What to check**: Do external APIs/libraries referenced in the SPEC actually support the claimed features? Are version constraints accurate? Are performance assumptions based on measurement or guessing?

**IMPL documents** (medium priority):
- **Claim density**: Medium. Implementation steps reference specific code patterns, library methods, configuration options.
- **Claim types**: Existence claims (this method exists, this parameter is accepted), factual claims about behavior (calling X with Y produces Z).
- **Fact-check approach**: For each implementation step that depends on an external library or API, verify the method/parameter/behavior exists in the version being used. IMPL is where interpolated knowledge is most dangerous - the agent confidently specifies `library.method(param)` where the method exists but does not accept that parameter.
- **What to check**: Do referenced methods, classes, parameters exist? Do they accept the described arguments? Are import paths correct? Are version-specific features available in the target version?

**TEST documents** (medium priority):
- **Claim density**: Medium. Test cases contain expected behaviors that are factual claims.
- **Claim types**: Factual claims about expected system behavior, quantitative claims about thresholds.
- **Fact-check approach**: For each test case, verify that the expected behavior matches actual system behavior. A test that asserts "API returns 200" when the API actually returns 201 will fail at runtime - catching this during fact-check saves debugging time.
- **What to check**: Are expected status codes, response formats, error messages accurate? Are threshold values based on measurement or assumption?

**TASKS documents** (low priority):
- **Claim density**: Low. Primarily process/tracking, not factual claims about external reality.
- **Fact-check approach**: Minimal. Check that task descriptions reference real work items and that effort estimates have a basis. Not a primary fact-check target.

**RULES, GUIDES, CHECKS** (low priority, different verification):
- **Claim density**: Low for factual claims about external reality. High for claims about best practices and tool behavior.
- **Claim types**: Claims about how tools work ("Playwright MCP spawns a fresh browser instance"), claims about writing quality ("active voice improves clarity").
- **Fact-check approach**: For tool behavior claims, test the tool. For best-practice claims, these are often unfalsifiable opinions dressed as rules - flag but do not try to "verify" subjective quality judgments. Check that referenced tools, commands, and file paths actually exist.
- **What to check**: Do referenced tools exist and work as described? Are command-line examples accurate? Are file paths valid?

**TEMPLATES** (very low priority):
- **Claim density**: Near zero. Templates are structural scaffolding, not factual assertions.
- **Fact-check approach**: Not a fact-check target. Templates define form, not content. `/verify` handles template correctness.

**MINTO articles** (high priority):
- **Claim density**: Very high. The entire argument structure is built on factual claims.
- **Claim types**: Sourced attributions (Findings Inventory entries), derivative claims (the argument built from findings), quantitative claims.
- **Fact-check approach**: Every Fnn finding in the Findings Inventory must trace to a verified source. The argument structure depends on the findings being true - if a finding is wrong, the entire argument may collapse. Check the AMINTON tree bottom-up: verify leaf findings first, then evaluate whether the argument holds.
- **What to check**: Does each finding accurately represent its source? Are there findings that cite secondary sources when primary sources are available? Does the argument survive if any single finding is removed?

**Workflows and skills** (medium priority):
- **Claim density**: Medium. Workflows contain claims about tool behavior, file locations, command syntax.
- **Claim types**: Existence claims (this tool exists, this command works), factual claims about tool behavior (this flag does X).
- **Fact-check approach**: Test the commands. Run the tools. Verify file paths exist. A workflow that references `npx @playwright/mcp@latest` should be tested to confirm the package exists and works. A skill that claims `magick convert input.pdf output.jpg` works should be verified against the actual ImageMagick installation.
- **What to check**: Do referenced tools exist at the claimed paths? Do commands produce the claimed output? Are version requirements accurate?

**Deep research and research output** (highest priority):
- **Claim density**: Very high. Multiple files, many sources, dense findings.
- **Claim types**: All categories. The entire output is claims from web research.
- **Fact-check approach**: The source collection is already present (`_INFO_[TOPIC]-02_Sources.md`). For each source: does the URL still work? Does the page still say what the summary claims? For topic files: are findings accurately attributed? For the summary: do conclusions follow from verified findings? This is the highest-value fact-check target because research output feeds into all downstream documents.
- **What to check**: URL validity, source-to-claim accuracy, finding attribution, conclusion soundness, temporal accuracy (is 2024 research still valid in 2026?).

### 9.3 Code

Code is a fundamentally different input type because code is BOTH a claim and a testable artifact. A function that claims to "validate email addresses" is making a factual claim about its own behavior that can be tested by running it.

**Claims IN code** (comments, docstrings, documentation):
- **Claim density**: Variable. Well-documented code is full of claims. Undocumented code has zero explicit claims.
- **Examples**: "This function returns True if the email is valid." "Timeout is 30 seconds." "Retries up to 3 times with exponential backoff."
- **Fact-check approach**: Read the comment, then read the code. Does the code actually do what the comment says? Comments are claims about the code - they can be wrong, outdated (code changed, comment stayed), or aspirational (comment describes intended behavior, code implements something else).
- **Special risk**: Docstrings copied from similar functions that do not accurately describe THIS function. Auto-generated documentation that was never reviewed.

**Claims ABOUT code** (in SPEC, IMPL, INFO):
- **Claim density**: High in IMPL documents that describe code behavior.
- **Examples**: "The `authenticate()` function uses PKCE." "The retry logic handles 503 errors." "The cache invalidation runs every 5 minutes."
- **Fact-check approach**: Read the actual code and trace the execution path. Does `authenticate()` actually implement PKCE, or does it use a simpler flow? Does the retry logic actually catch 503, or does it only catch 500? Is the cache interval actually 5 minutes or is it configured differently?
- **Special risk**: IMPL plans that describe intended code, verified against the SPEC, but the actual code was implemented differently. `/verify` will catch "code does not match IMPL" but only if someone runs verify against the code. `/fact-check` catches "the IMPL claims the code does X, but the code actually does Y" by reading the code directly.

**The code ITSELF as a claim** (implicit behavioral claims):
- **Claim density**: Every line of code is an implicit claim about intended behavior.
- **Examples**: `response = requests.get(url, timeout=30)` implicitly claims the timeout is 30 seconds. `if status_code == 429: retry()` implicitly claims the code handles rate limiting.
- **Fact-check approach**: Run the code. Unit tests are fact-checks on code behavior. Integration tests are fact-checks on system behavior. The strongest fact-check for code is execution.
- **Key question**: Does the code actually produce the behavior it appears to produce? Edge cases, error paths, and concurrency issues are where code's implicit claims most often fail.

**Dependency claims** (code depends on external systems):
- **Claim density**: Every import, API call, and library usage is a dependency claim.
- **Examples**: `import boto3` claims boto3 is installed. `client.upload_file()` claims this method exists with this signature. `response.json()['data']['items']` claims the response has this structure.
- **Fact-check approach**: Verify that dependencies exist in the claimed version. Verify that methods accept the claimed parameters. Verify that response structures match the code's expectations. This is where interpolated knowledge causes the most runtime failures - the agent writes code against an API it has never tested.
- **What to check**: Does the dependency exist at the claimed version? Does the method signature match? Does the API response structure match what the code expects? Are there breaking changes between the version in training data and the current version?

**Configuration claims** (config files, environment variables):
- **Claim density**: Every config value is a claim about system behavior.
- **Examples**: `TIMEOUT=30` claims 30-second timeout. `MAX_RETRIES=3` claims 3 retries. `DATABASE_URL=postgres://...` claims this connection string works.
- **Fact-check approach**: Trace configuration values through the code to verify they are actually used where expected. A config value that exists but is never read is a dead claim. A config value that is read but overridden elsewhere is a misleading claim.

### 9.4 Input Type Priority Matrix

Fact-checking effort should be allocated proportionally to claim density and downstream impact:

```
Priority 1 (always fact-check):
├─> Deep research / research output (highest claim density, feeds everything)
├─> INFO documents (primary fact-check target, first in document chain)
└─> MINTO articles (argument integrity depends on finding accuracy)

Priority 2 (fact-check when claims reference external systems):
├─> SPEC documents (hallucinated requirements propagate to all downstream)
├─> IMPL documents (interpolated library/API knowledge causes runtime failures)
├─> Code dependency claims (wrong imports/methods = build failures)
└─> Workflows and skills (wrong tool paths/commands = execution failures)

Priority 3 (fact-check selectively):
├─> TEST documents (wrong expected values caught at test runtime)
├─> Code comments and docstrings (wrong docs mislead but don't break builds)
├─> RULES, GUIDES, CHECKS (wrong tool behavior claims)
└─> External sources used as references (already evaluated during research)

Priority 4 (minimal fact-checking):
├─> TASKS documents (process tracking, few external claims)
├─> TEMPLATES (structural, no factual content)
└─> Session tracking files (NOTES, PROBLEMS, PROGRESS)
```

## 10. Separation of Concerns: fact-check.md vs verify.md

The fundamental distinction:

- **`verify.md`** = "Does it conform?" Checks whether an artifact conforms to everything that governs it: DevSystem rules (APAPALAN, MECT, SOCAS, templates), upstream documents (SPEC governs IMPL, IMPL governs Code, SPEC governs TEST), session instructions, and MNF checklists. It compares artifact-to-artifact and artifact-to-rules. It trusts upstream sources as authoritative.

- **`fact-check.md`** = "Is it true?" Checks whether factual claims correspond to external reality. Goes outside the document system to primary sources (the actual running system, source code, test execution, web research). Does NOT trust any written source as ground truth. Eliminates assumptions, hallucinations, incorrect conclusions, unsupported claims, and unreliable claims.

The critical difference: `verify.md` will catch "the IMPL forgot to implement FR-03 from the SPEC." It cannot catch "FR-03 is based on a hallucinated API feature." A fabricated claim written into the SPEC will be faithfully verified as "conforming" through IMPL, Code, and TEST - because verify trusts the SPEC. Only `fact-check.md` questions whether the SPEC is correct about the real world.

### 10.1 Orthogonality Proof

A document can:
- **Pass verify, fail fact-check**: IMPL perfectly conforms to SPEC, all DevSystem rules followed, but the SPEC contains a fabricated API method name. Verify sees full conformance. Fact-check calls the API and discovers the method does not exist.
- **Pass fact-check, fail verify**: Every factual claim is verified against the actual system, but the document uses inconsistent naming, tables instead of lists, and the IMPL missed two items from the SPEC.
- **Fail both**: Non-conforming AND factually wrong.
- **Pass both**: Conforms to all governing sources AND all factual claims match reality. This is the goal.

### 10.2 What verify.md Currently Does That Borders on Factchecking

The existing `verify.md` INFO section (lines 152-166) contains:

```
Priority 1: Factuality and clarity (misinterpretation prevention)
- Verify sources. Read them again and verify or complete findings.
- Drop all sources that can't be found.
```

This is light factchecking embedded in verify. With `fact-check.md` existing, this responsibility should migrate. `verify.md` keeps the conformance check ("Is the source citation formatted correctly per INFO-SC-01? Does the INFO follow all INFO-* rules?"). `fact-check.md` takes the truth check ("Does the source actually say what the document claims? Does the system actually behave this way?").

### 10.3 Decision Boundary

```
                    verify.md                          fact-check.md
                    ─────────                          ─────────────
Question:           "Does it conform?"                 "Is it true?"
Method:             Conformance checking                Evidence-based investigation
Compares:           Artifact vs governing sources       Claims vs external reality
Governing sources:  Rules, SPEC, IMPL, templates,      The actual running system,
                    instructions, MNF checklists        source code, test output, web
Trust model:        Trusts upstream docs as correct     Trusts nothing - tests everything
Input:              The artifact + its governing         The artifact + the real world
                    sources (rules, specs, plans)
Output:             Conformance findings + fixes         Claim verdicts (confirmed/refuted/unverifiable)
Catches:            "IMPL forgot FR-03 from SPEC"       "FR-03 is based on a hallucinated API feature"
Cannot catch:       Wrong SPEC (trusted as truth)        Formatting errors, missed requirements
```

### 10.4 When to Run Each

- **`/verify`**: After writing any artifact. Always. Checks conformance to all governing sources.
- **`/fact-check`**: After writing INFO, SPEC, or any document containing factual claims about external systems, APIs, libraries, or domain knowledge. Not needed for pure process documents (session tracking, STRUT plans, TASKS).
- **Recommended sequence**: `/fact-check` first (are the claims true?), then `/verify` (does it conform?). Catching a wrong claim before it enters the SPEC prevents verify from faithfully propagating it downstream.

## 11. Rule Mapping: Which Rules Belong Where

### 11.1 Rules That Stay in verify.md (Conformance)

**Upstream document conformance** (the core of verify.md):
- IMPL conforms to SPEC: every FR-XX, DD-XX, IG-XX addressed; nothing forgotten, nothing contradicted
- Code conforms to IMPL: implementation matches the plan; all IS-XX steps realized
- TEST conforms to SPEC: every FR-XX has at least one TC-XX; every EC-XX has corresponding test
- TEST conforms to IMPL: all edge cases from IMPL have corresponding test cases
- SPEC conforms to requirements and existing code: no contradictions with current system behavior

**DevSystem rules (writing quality and structure)**:

**APAPALAN (all rules)**:
- AP-PR-01 through AP-PR-13: Precision formatting, datetime, attributes, contacts, links, IDs, acronyms, specificity, examples, patterns, literals
- AP-BR-01 through AP-BR-07: Brevity, grammar, DRY, compact definitions, show-not-describe, pipe-delimited, bold usage
- AP-ST-01 through AP-ST-07: Structure, goal-first, self-contained units, hierarchical ordering, visual grouping, cognitive load
- AP-CM-01 through AP-CM-03: Communication commitments, labeled questions, time precision
- AP-NM-01 through AP-NM-05: Naming one-per-concept, unambiguous compounds, meta-words, word pairs, standard terms

**MECT (all rules)**:
- MW-VO-01 through MW-VO-04: Active voice, reader address, simplest verb, obligation words
- MW-WC-01 through MW-WC-08: Word precision, plain language, no recursion, no product collision, no synonymy, no inverted semantics, no premature compression, language sovereignty
- MW-TD-01 through MW-TD-03: Naming structure, output-named procedures, stable naming
- MW-HS-01 through MW-HS-03: Informative headings, depth limit, audience matching
- MW-LT-01 through MW-LT-05: Two identifiers, topology grouping, indexed groups, formatting signals, adjacent comparison
- MW-DT-01 through MW-DT-03: Description lenses, audience matching, canonical forms
- MW-VR-01 through MW-VR-03: Visual previews, structural diagrams, five diagram categories

**SOCAS (internal quality subset)**:
- SOCAS-01: Inconsistencies (same concept named multiple ways)
- SOCAS-02: Ambiguous Naming (undefined concepts)
- SOCAS-03: Overlapping Concerns (redundancy)
- SOCAS-05: Ineffective Communication (scattered information)
- SOCAS-07: Confusing Elements (humor obscuring meaning)
- SOCAS-08: Noise Imbalance (verbose, filler) - the WRITING quality aspect
- SOCAS-09: Lack of Structure (no headings, no TOC)
- SOCAS-11: Unnecessary Complexity (over-engineering)
- SOCAS-12: Presentation Sloppiness (typos, formatting) - the SURFACE quality aspect
- SOCAS-13: Empty Structure (headings label topics, not ideas) - the STRUCTURAL aspect
- SOCAS-14: Arbitrary Sequencing (no discernible order)

### 11.2 Rules That Move to fact-check.md (Truth Verification)

No existing rules move entirely. Instead, `fact-check.md` introduces NEW verification concerns:

- **Claim identification**: Scan document for all factual, derivative, quantitative, existence, and attribution claims (Section 8 taxonomy)
- **Source verification**: Does the cited source actually say what the document claims? (extends INFO-SC-01 through INFO-SC-05 from format checking to content checking)
- **Primary source tracing**: For secondary/tertiary source claims, trace back toward the primary source
- **Existence testing**: Do claimed methods, endpoints, parameters, features actually exist?
- **Quantitative verification**: Are claimed numbers, measurements, thresholds from a verifiable source?
- **Logic verification**: Do conclusions follow from their premises? (goes beyond SOCAS-10 by verifying the premises against external reality first)
- **Negative claim scrutiny**: Claims about what does NOT exist are especially hard to verify and easy to hallucinate
- **Cross-version verification**: Is the claim true for the version being discussed, or conflated from another version?

### 11.3 Boundary Rules: Present in Both, Different Focus

These SOCAS criteria appear in BOTH workflows but serve different purposes:

- **SOCAS-06** (Incomplete Specifications):
  - In `verify.md`: "Are there implicit assumptions left unstated?" (writing completeness)
  - In `fact-check.md`: "Are stated assumptions actually true?" (factual accuracy)

- **SOCAS-10** (Gaps in Reasoning):
  - In `verify.md`: "Does the conclusion follow from the stated evidence?" (logical structure)
  - In `fact-check.md`: "Is the stated evidence actually correct?" (factual foundation)

- **SOCAS-12** (Presentation Sloppiness):
  - In `verify.md`: "Are there typos and formatting errors?" (surface quality)
  - In `fact-check.md`: "Is outdated information mixed with current?" (temporal factuality)

## 12. Hallucination Detection Signals from Existing Rules

Seven existing SOCAS/APAPALAN/MECT patterns serve as early-warning signals for hallucinations. `fact-check.md` should use these as **triage input** to prioritize which claims to verify first:

### 12.1 SOCAS-08: Generic Phrasing (Noise Imbalance)

"Generic phrasing where domain expertise would produce specific examples."

When an LLM does not know the real answer, it defaults to plausible generalities. A claim like "the API supports standard authentication methods" is a hallucination risk: the agent may not know WHICH methods and is covering ignorance with vagueness.

**Fact-check action**: Flag generic claims for source verification. If the agent cannot cite a specific source, the claim is suspect.

### 12.2 SOCAS-12: Stale Information (Presentation Sloppiness)

"Outdated information mixed with current."

LLMs conflate versions because training data blends old and new documentation. A claim that was true in v1 but false in v2 will persist in LLM output without version qualification.

**Fact-check action**: For any claim about a specific system/API/library, verify the claim applies to the version being discussed.

### 12.3 SOCAS-13: Empty Structure

"Section summaries describe what the section covers, not what was found."

When an LLM cannot fill a section with real findings, it generates structural scaffolding: "This section analyzes the performance characteristics of the system." This is structure without substance - a signal that the agent is generating filler instead of facts.

**Fact-check action**: Flag hollow sections as containing no verifiable claims. Request substantive content or remove the section.

### 12.4 AP-PR-07: Vague Claims (Be Specific)

"Performance should be acceptable" and "the feature works as expected" are unfalsifiable. They may also be masking the agent's inability to make a specific, verifiable claim.

**Fact-check action**: Require specific, verifiable reformulation. "Response time < 200ms for 95th percentile" is fact-checkable. "Performance is acceptable" is not.

### 12.5 MW-WC-01: Wrong Term Precision (Word-Level Precision)

Using "accuracy" when "precision" is meant, or "simple" when "simplistic" applies. This can be a genuine word choice error (verify.md territory) OR a signal that the agent does not understand the domain well enough to pick the right term (fact-check territory).

**Fact-check action**: When a term precision error affects a factual claim ("the system achieves high accuracy" vs "the system achieves high precision"), verify the underlying measurement against the source.

### 12.6 SOCAS-10: Assumptions as Facts (Gaps in Reasoning)

"Assumptions presented as facts." When an LLM states "the API requires authentication" without citing a source, it may be interpolating from patterns in training data rather than reporting a verified fact.

**Fact-check action**: Any claim without a source citation is a candidate for verification. Prioritize claims that are stated with high confidence but no attribution.

### 12.7 SOCAS-06: Unsupported Conclusions (Incomplete Specifications)

"Conclusions not supported by evidence." A derivative claim that does not reference the facts it derives from is suspect. The reasoning may be sound, but if the supporting facts are hallucinated, the conclusion is worthless.

**Fact-check action**: For every derivative claim, trace back to the supporting facts. Verify the facts first, then evaluate the reasoning.

## 13. Conclusions

The analysis reveals that a factcheck workflow must be structurally different from existing DevSystem verification workflows:

1. **AI agent gullibility is the primary reason `fact-check.md` must exist.** The agent trusts all text unconditionally: official docs, blog posts, its own previous output, and hallucinated claims all have equal authority in the agent's processing. It cannot distinguish aspirational documentation from actual system behavior. It cannot question whether a source was written by someone who tested the product or someone who guessed. Without a systematic adversarial workflow, the agent builds on unverified claims and propagates errors across sessions (Section 6).

2. **Statistical distribution of text measures popularity, not truth.** LLM confidence is a function of token frequency in training data. If the corpus is dominated by wrong claims (vendor marketing, outdated docs, industry-funded research, SEO content), the agent will confidently produce wrong output. Consensus among text sources is not evidence. The only valid verification terminates in direct observation: call the API, read the source code, run the test (Section 6.5).

3. **Documentation is NOT a primary source.** The shipped product (running API, SDK source code, executed test output) is the primary source. Documentation is a technical writer's claim about the product - it can be wrong, outdated, aspirational, or written before the feature shipped. This distinction is the single most important correction to default AI agent behavior, which treats docs as ground truth (Section 2).

4. **`/verify` checks conformance** (does the artifact conform to its governing sources - rules, specs, plans, templates?). `/fact-check` checks **correspondence** (do the factual claims match reality?). These are orthogonal. A fabricated API method written into the SPEC will be faithfully verified as "conforming" through IMPL, Code, and TEST - because verify trusts the SPEC. Only fact-check questions whether the SPEC is correct about the real world.

5. **Factchecking requires crossing the gap from claims-about-reality to observed-reality.** All existing workflows operate on text: they read text and produce text. `fact-check.md` is the only workflow designed to cross the gap between written claims and actual system behavior (Section 3.1). It must push toward the left of the trust hierarchy: observed behavior > source code > official docs > community sources > LLM output.

6. **The claim taxonomy (Section 8) defines the workflow's core loop.** For each claim type, there is a specific verification strategy. The workflow must classify claims first, then apply the appropriate strategy.

7. **Interpolated knowledge is the primary technical threat.** Gross fabrications are relatively easy to catch. The dangerous errors are the ones where an LLM combines real elements into a plausible but non-existent whole. Detection requires comparing claims to sources at a granular level, not just checking if the source exists.

8. **The cost model favors early verification.** Factchecking during or immediately after writing is orders of magnitude cheaper than discovering errors downstream. The workflow should run as part of the document creation pipeline, not as an afterthought.

9. **Seven existing rules are hallucination triage signals.** SOCAS-08, SOCAS-12, SOCAS-13, AP-PR-07, MW-WC-01, SOCAS-10, and SOCAS-06 each detect a pattern that correlates with LLM hallucination. `fact-check.md` should scan for these patterns FIRST to prioritize which claims to verify, rather than verifying every claim with equal effort.

10. **The existing `verify.md` INFO section needs adjustment.** Its "Priority 1: Factuality" currently includes light source verification ("Read them again and verify or complete findings"). With `fact-check.md` existing, this responsibility migrates there. `verify.md` retains the format/structure check ("Is the citation formatted per INFO-SC-01?").

11. **Three SOCAS rules operate on the boundary.** SOCAS-06, SOCAS-10, and SOCAS-12 each have a writing-quality aspect (stays in `verify.md`) and a truth-verification aspect (moves to `fact-check.md`). The boundary is clear: internal logic = verify, external correspondence = fact-check.

## 14. Next Steps

1. Design the `fact-check.md` workflow structure based on the claim taxonomy (Section 8), input type priorities (Section 9), gullibility failure modes (Section 6), and hallucination triage signals (Section 12)
2. Define the claim extraction process (how to identify verifiable claims in a document)
3. Define verification procedures for each claim category, including tools to use (web search, file reading, code execution)
4. Determine integration points: `fact-check.md` runs independently of `verify.md`, but both can run in sequence
5. Update `verify.md` INFO section to remove source truth-checking (moves to `fact-check.md`), retaining source format-checking
6. Write `fact-check.md` workflow following `WORKFLOW_RULES.md`

## 15. Sources

This document is based on analytical reasoning about epistemological principles applied to the DevSystem context. Section 6 is based on first-principles analysis of AI agent trust behavior. Section 9 is based on analysis of DevSystem document types and their claim profiles. Sections 10-12 are based on direct analysis of existing rule files.

**Primary Sources:**
- `FCTCHECK-IN01-SC-DVSYS-INFORULES`: `INFO_RULES.md` - Existing source citation requirements (INFO-SC-01 through INFO-SC-05) [VERIFIED]
- `FCTCHECK-IN01-SC-DVSYS-VRFY`: `verify.md` - Existing verification workflow scope and INFO section (lines 152-166) [VERIFIED]
- `FCTCHECK-IN01-SC-DVSYS-PROBS`: `!PROBLEMS.md` - DVSYS-FT-0001 item 2 factcheck requirements definition [VERIFIED]
- `FCTCHECK-IN01-SC-DVSYS-APAPALAN`: `APAPALAN_RULES.md` - 26 precision/brevity/structure/communication/naming rules [VERIFIED]
- `FCTCHECK-IN01-SC-DVSYS-MECT`: `MECT_WRITING_RULES.md` - 22 voice/word-choice/terminology/heading/list/description/visual rules [VERIFIED]
- `FCTCHECK-IN01-SC-DVSYS-SOCAS`: `SOCAS_RULES.md` - 17 quality evaluation criteria with context-appropriate subsets [VERIFIED]

## 16. Document History

**[2026-08-30 16:01]**
- Added: Section 9 (Input Types: What Can Be Fact-Checked and How) - external sources (web, PDF, ebooks, press, images, unknown), DevSystem document types (INFO through deep research), code (5 claim categories), priority matrix
- Changed: All sections 9-15 renumbered to 10-16

**[2026-08-30 15:53]**
- Added: Section 6.5 (Statistical Distribution Is Not Evidence) - LLM confidence = popularity not truth, sugar/tobacco example, vendor marketing bias, SEO contamination, outdated information weight
- Fixed: Section 3.3 verification methods reordered by strength (reproduction first, cross-referencing last with WARNING about consensus fallacy)
- Fixed: Section 6.2 consensus fallacy expanded with 1960s sugar/tobacco example
- Changed: Conclusions expanded from 10 to 11 points, statistical distribution is now conclusion 2
- Changed: Summary added statistical distribution finding

**[2026-08-30 15:49]**
- Fixed: verify.md characterization throughout document - was "Is it well-written?" (writing quality only), corrected to "Does it conform?" (conformance to ALL governing sources: DevSystem rules, upstream documents like SPEC for IMPL, templates, instructions)
- Fixed: Section 9 intro, decision boundary table, orthogonality proof examples - all now reflect verify.md's artifact-vs-artifact checking (IMPL vs SPEC, Code vs IMPL, TEST vs SPEC)
- Fixed: Section 6.3 verify.md description - now explains it trusts upstream sources as authoritative, which is the core limitation fact-check.md addresses
- Fixed: Section 10.1 heading and content - added upstream document conformance as the core of verify.md, separate from DevSystem writing rules
- Fixed: Conclusion 3 - corrected from "compliance" to "conformance" with accurate scope description
- Added: Section 9.4 recommended sequence: fact-check first, then verify
- Changed: Summary line 16 corrected

**[2026-08-30 15:47]**
- Added: Section 6 (AI Agent Gullibility and the Trust Problem) - fundamental deficiency, 6 failure modes, workflow gap analysis, trust inversion
- Fixed: Section 2.1 primary source error - documentation reclassified from primary to secondary; shipped product (running API, source code, test output) is primary
- Fixed: Section 2.2 degradation chain - starts at actual system, not docs; added aspirational contamination
- Fixed: Section 3.1 evidence spectrum - explicit gap between claims-about-reality and observed-reality; docs are hypotheses, not evidence
- Fixed: Section 3.2 medium stakes - reading docs is NOT primary verification; testing the actual system is
- Fixed: Section 1.2 - reframed from academic "LLM has no beliefs" to operational "agent acts on output and has no skepticism mechanism"
- Fixed: Section 8.1 (was 7.1) verification target - observe the system first, docs only as fallback with weaker label
- Changed: Conclusions rewritten, gullibility is now conclusion 1; expanded from 8 to 10 points
- Changed: Summary added gullibility finding as leading point

**[2026-08-30 15:44]**
- Added: Section 9 (Separation of Concerns) with orthogonality proof and decision boundary
- Added: Section 10 (Rule Mapping) classifying all APAPALAN/MECT/SOCAS rules by workflow ownership
- Added: Section 11 (Hallucination Detection Signals) mapping 7 existing rules to triage input
- Changed: Conclusions expanded from 5 to 8 points incorporating separation of concerns
- Changed: Next Steps expanded to include verify.md adjustment
- Changed: Sources expanded with APAPALAN, MECT, SOCAS source entries
- Changed: Summary expanded with 3 new findings on separation of concerns

**[2026-08-30 15:39]**
- Initial research document created
