# Validation Report: [Topic Title]

**Doc ID**: [TOPIC]-IN[NN]
<!-- Topic ID: [TOPIC] -->
**Document Type**: validation-report
**Input Provenance**: [Hypothesis register path or statement source description]

## Items

<!-- Repeat for each hypothesis or statement under validation -->
- [ITEM-ID]: [Statement or candidate hypothesis under test]

## Evidence Weights

<!-- Repeat for each diagnostic evidence link -->
### Evidence Weight: [ITEM-ID] x [FINDING-ID]

- Grounds: [FINDING-ID] ([SOURCE-ID], Tier [1-5]) [[VERIFIED|ASSUMED|TESTED|PROVEN]] "[Verbatim finding text]"
- Toulmin Warrant: [Explicit sentence explaining logical connection between finding and hypothesis]
- Polarity: [Consistent|Inconsistent|Not Applicable]
- Diagnosticity: [High|Moderate|Low]

<!-- Repeat for each hypothesis evaluated -->
### Hypothesis Certainty: [ITEM-ID]

- Inconsistencies: [N] of [M] diagnostic findings
- GRADE Certainty: [High|Moderate|Low|Very Low] (downgrades: [Specific downgrade factors or "None"])

## ACH Matrix

<!-- Repeat for each diagnostic finding row across competing items. Labeled lines format, no Markdown tables -->
### Evidence Row: [FINDING-ID]

- Description: "[Summary of empirical finding or observation]"
- Consistency per Item:
  - [ITEM-ID-1]: [Consistent|Inconsistent|Not Applicable]
  - [ITEM-ID-2]: [Consistent|Inconsistent|Not Applicable]
- Audit Note: [Diagnostic value, discrimination power, and search direction note]

## Disconfirmation Log

<!-- Repeat for each active refutation attempt -->
### Disconfirmation Log: [DL-NN]

- Hypothesis: [ITEM-ID]
- Predicted observation: [Concrete observation that would challenge or refute hypothesis]
- Search query: "[Targeted search query, code test, or telemetry inspection path]"
- Result: [Observed finding or zero-result log]
- Matrix cell update: [Consistent|Inconsistent]
- Exhausted: [Yes|No]

## Ranking

<!-- Strict 0-8 scale: 0 (refuted), 1 (remote), 2 (highly unlikely), 3 (unlikely), 4 (roughly even chance), 5 (likely), 6 (highly likely), 7 (almost certain), 8 (proven). No tied ranks permitted. Prose phrasing per DD-06 -->
1. [ITEM-ID] (Scale Position: [0-8] - [Refuted|Remote|Highly unlikely|Unlikely|Roughly even chance|Likely|Highly likely|Almost certain|Proven]; Analytic Confidence: [Low|Moderate|High] confidence)
   - Likelihood Statement: "[Prose sentence stating estimated likelihood]"
   - Confidence Assessment: "[Prose sentence stating evidence confidence level]"
   - Tie-break: [Recorded rationale distinguishing item from same scale position, or "None required - unique position"]
   - Evidence Threshold Record: [Refuting evidence ID for position 0; [PROVEN] or [TESTED] citation for position 8]

## Research Questions for Layer 1

<!-- Repeat for each open item with low confidence and exhausted: yes in disconfirmation log -->
- [RQ-ID]: [Targeted research question for unsettled item]
  - Prompted by: [ITEM-ID] (low confidence, disconfirmation exhausted)
  - Recommended Layer 1 action: [Targeted search query or deep-research direction]

## Writing Implications

- Primary Thesis: [Highest-ranking surviving hypothesis and governing thought recommendation for Layer 3]
- Nuances and Caveats: [Scope conditions, assumptions, and lower-confidence areas to acknowledge in prose]
- Counter-Arguments to Address: [Refuted candidate explanations and key rebuttals to address in deliverable]
