---
description: Detect AI-generated or AI-assisted writing in a given text
---

# Detect AI Writing Workflow

Systematically analyze text for signals of AI generation or AI-assisted writing using the four-category signal framework (Sourcing, Style, Structure, Voice).

## Required Skills

- @skills:write-documents for output formatting
- @skills:ms-playwright-mcp for source verification (web search)

## MUST-NOT-FORGET

- NEVER ask questions - derive goal or best option from previous prompt or conversation context
- **Sourcing > Style** - Sourcing signals (SO) are the strongest indicator. A text with 3/4 sourcing signals is more diagnostic than one with 8/8 style+structure+voice signals
- **Convergence required** - No single signal is conclusive. Detection requires multiple independent signals across categories
- **Not a verdict** - Output is a confidence assessment, not a binary guilty/innocent judgment
- **Verify claims** - Always fact-check 2-3 specific attributions against primary sources before scoring SO rules
- **False positive awareness** - Ghostwriters, academic writers, and skilled bloggers can trigger style/structure/voice signals without AI involvement

## Input

The text to analyze. Accepted as:
- Inline text in the user's prompt
- File path to a document
- URL to a web page (use @skills:ms-playwright-mcp to retrieve)

If no specific text is provided, derive from conversation context which text the user wants analyzed.

## Step 1: First Read

Read the text completely without scoring. Note:
- Overall length (short texts <200 words have insufficient signal density)
- Genre (argumentative, informative, academic, persuasive, narrative)
- Claimed or implied sources (names, dates, concepts attributed to specific people)

Record intuitive impression: Does the text feel too smooth, too perfect, too confident?

## Step 2: Sourcing Analysis (Most Diagnostic)

Evaluate all four sourcing rules. This is the most important step.

For each SO rule, perform the detection test:

- **AD-SO-01: Confident misattribution** - Pick 2-3 specific factual claims attributed to named sources. Verify against primary sources. If wrong AND stated without hedging → DETECTED
- **AD-SO-02: Internet-discourse terminology** - Check whether terms match the claimed source's actual language or come from secondary commentary → DETECTED if secondary
- **AD-SO-03: Absence of citation** - Count specific factual claims vs citations. Ratio >5:1 on specialized topics → DETECTED
- **AD-SO-04: Temporal impossibility** - Check if historical figures are presented as commenting on events postdating their work without interpretive framing → DETECTED

**Verification method**: Use web search to check attributions against primary sources. Search for exact quotes, publication dates, and original terminology.

## Step 3: Style Analysis

Evaluate all three style rules:

- **AD-SY-01: Staccato fragment pattern** - Count fragment-after-sentence patterns. 3+ in <1000 words → DETECTED
- **AD-SY-02: Perfect tricolon escalation** - Identify rhythmically balanced, semantically escalating tricolons at structural climax points → DETECTED
- **AD-SY-03: Absence of rough edges** - Read 500+ words. If no sentence surprises stylistically (no unusual word, no structural break, no personality artifact) → DETECTED

## Step 4: Structure Analysis

Evaluate all three structure rules:

- **AD-ST-01: Engagement-optimized arc** - Map sections to the 4-beat template (authority → mechanism → application → emotional close). Exact match → DETECTED
- **AD-ST-02: Perfect paragraph progression** - Summarize each paragraph. If summaries form a strictly monotonic sequence (no revision, no backtracking) → DETECTED
- **AD-ST-03: Absence of structural surprise** - After reading 30%, predict remaining sections. If prediction matches >80% → DETECTED

## Step 5: Voice Analysis

Evaluate all three voice rules:

- **AD-VO-01: No personal reference** - Search for "I," "my," anecdotes, professional disclosures. None in 500+ words of argumentative prose → DETECTED
- **AD-VO-02: Generated authority** - Check if expert tone is contradicted by factual errors an expert would avoid → DETECTED
- **AD-VO-03: Emotional manipulation without emotional investment** - Check if text produces emotion through technique with no personal stake or vulnerability disclosed → DETECTED

**Calibration**: VO-01 does not apply to academic, journalistic, or encyclopedic writing where impersonality is conventional.

## Step 6: Convergence Assessment

Count detected signals per category and total:

**Convergence thresholds:**
- 0-2 signals: **LOW** - Insufficient evidence. Text may be human-written or heavily edited LLM output
- 3-5 signals: **MODERATE** - Warrants source verification. Text may be AI-assisted
- 6-8 signals: **HIGH** - Multiple convergent signals. Text very likely AI-assisted
- 9-12 signals: **VERY HIGH** - Signals across all categories. Text almost certainly AI-generated

**Category weighting**: If SO >= 3 regardless of other scores, assessment is minimum HIGH.

## Step 7: Output Report

Format the report as follows:

```
## AI Writing Detection Report

**Text**: [title/description/first 10 words...]
**Length**: [word count]
**Genre**: [argumentative/informative/persuasive/narrative/academic]

### Signal Scores

| Category   | Score | Signals Detected                    |
|------------|-------|-------------------------------------|
| Sourcing   | n/4   | [list which SO rules triggered]     |
| Style      | n/3   | [list which SY rules triggered]     |
| Structure  | n/3   | [list which ST rules triggered]     |
| Voice      | n/3   | [list which VO rules triggered]     |
| **Total**  | n/12  |                                     |

### Assessment: [LOW / MODERATE / HIGH / VERY HIGH]

### Key Evidence

[2-3 most diagnostic findings with specific quotes from the text and verification results]

### Limitations

[Note any factors that weaken the assessment: short text, heavily edited, conventional genre, etc.]
```

## Edge Cases

- **Text <200 words**: Report as INCONCLUSIVE due to insufficient signal density. Note which signals are present but flag low confidence.
- **Academic/legal/encyclopedic text**: Disable VO-01 (impersonal voice is conventional). Raise threshold for ST rules (formulaic structure is expected).
- **Translated text**: Style signals may reflect translator choices, not original author or LLM. Weight sourcing signals even more heavily.
- **Mixed authorship**: Some sections may be human-written, others AI-generated. If signal density varies dramatically between sections, note per-section assessment.
