# Personal Profile Rules

Rules for writing and verifying personal profile INFO documents with GOOD/BAD examples.

## Rule Index

Header (HD)
- PP-HD-01: Depth tier set and sections match tier
- PP-HD-02: Related profiles field links to existing profile Doc IDs
- PP-HD-03: Connection to requester states relationship type and evidence

Summary (SM)
- PP-SM-01: 3-5 sentences covering role, location, arc, distinguishing feature, relevance
- PP-SM-02: No claims without source backing in body sections

Timeline (TL)
- PP-TL-01: Career timeline reverse chronological, no gaps >2 years without explanation
- PP-TL-02: Dates consistent across Career Timeline, Current Occupation, and Company Factsheets
- PP-TL-03: Education timeline includes institution, degree, field, years

Topics (TP)
- PP-TP-01: Each topic has status and qualifier in heading
- PP-TP-02: Conversation angle ends each topic with a concrete question

Character (CH)
- PP-CH-01: Self-description uses actual quotes from LinkedIn/bio
- PP-CH-02: Career pattern uses arrow notation with spaces

Networking (NW)
- PP-NW-01: Engagement Strategy has at least one concrete, actionable recommendation
- PP-NW-02: Touchpoints reference specific events, not vague categories

Sensitivity (SN)
- PP-SN-01: Sensitive topics flagged with `[SENSITIVE: reason. Safe angle: ...]`
- PP-SN-02: No private data beyond what is publicly available

Sources (SC)
- PP-SC-01: All sources include access date
- PP-SC-02: Source recency - flag if all sources older than 12 months

Cross-Reference (XR)
- PP-XR-01: Referenced persons/companies use `(see [TOPIC]-IN[NN])` when profile exists
- PP-XR-02: Company Factsheets kept minimal when company profile exists separately

## Header Rules

### PP-HD-01: Depth Tier Compliance

Depth tier must be set. Sections must match:
- BRIEF profiles contain only Summary + Career Timeline + Networking Relevance
- STANDARD profiles skip Education Timeline, empty Additional Activities subsections, Company Factsheets
- FULL profiles fill all applicable sections

**BAD:**
```
**Depth tier**: FULL

## Summary
[filled]
## Career Timeline
[filled]
## Education Timeline
[empty - no data found]
## Additional Activities
### Publications
[empty]
### Speaking Engagements
[empty]
### Board Memberships
[empty]
```

**GOOD:**
```
**Depth tier**: STANDARD

## Summary
[filled]
## Career Timeline
[filled]
## Additional Activities
### Board Memberships
- **2019-present**: Advisory Board, FinTech Association Germany (invited member)
```

### PP-HD-03: Connection Statement

Connection must state relationship type and basis.

**BAD:**
```
**Connection to Karsten Held**: Connected on LinkedIn.
```

**GOOD:**
```
**Connection to Karsten Held**: 2nd-degree via Thomas Mueller (shared tenure at SAP 2015-2018). Overlapping interest in AI-driven due diligence.
```

## Timeline Rules

### PP-TL-01: Career Timeline Completeness

Reverse chronological. Gaps >2 years require explanation.

**BAD:**
```
## Career Timeline

- **2020-present**: CEO at NewCo, Berlin
- **2012-2015**: VP Engineering at OldCorp, Munich
```

**GOOD:**
```
## Career Timeline

- **Since 2020**: CEO at NewCo, Berlin (AI-powered compliance platform)
- **2015-2020**: Sabbatical and angel investing [ASSUMED - no public role found]
- **2012-2015**: VP Engineering at OldCorp, Munich (led team of 45)
```

### PP-TL-02: Date Consistency

Dates must match across sections.

**BAD:**
```
## Career Timeline
- **Since 2019**: CEO at FinCo

## Current Occupation
### FinCo (CEO, since 2020)
```

**GOOD:**
```
## Career Timeline
- **Since 2019**: CEO at FinCo, Frankfurt (regulatory technology)

## Current Occupation
### FinCo (CEO, since 2019)
```

## Topic Rules

### PP-TP-01: Status and Qualifier

Every topic heading needs status and qualifier.

**BAD:**
```
### Artificial Intelligence
```

**GOOD:**
```
### Artificial Intelligence (primary, via FinCo product)
```

### PP-TP-02: Conversation Angle

Each topic ends with a specific, askable question.

**BAD:**
```
Conversation angle: "Ask about AI"
```

**GOOD:**
```
Conversation angle: "How did you decide to build the compliance engine on LLMs rather than rule-based systems?"
```

## Character Assessment Rules

### PP-CH-01: Self-Description from Source

Use actual quotes, not paraphrases.

**BAD:**
```
- **Self-description**: She describes herself as a technology leader.
```

**GOOD:**
```
- **Self-description**: "Building the future of regulatory intelligence | Ex-SAP, Ex-McKinsey | Board Member @FinTechDE"
```

### PP-CH-02: Career Pattern Arrow Notation

Use `->` arrows with spaces for career arc.

**BAD:**
```
- **Career pattern**: Consulting to product to founder
```

**GOOD:**
```
- **Career pattern**: Management consulting (McKinsey) -> Corporate tech leadership (SAP) -> Founder/CEO (FinCo)
```

## Networking Rules

### PP-NW-01: Actionable Engagement

Recommendations must be specific enough to execute.

**BAD:**
```
- **Recommended approach**: Reach out via LinkedIn
```

**GOOD:**
```
- **Recommended approach**: Request introduction via Thomas Mueller (shared SAP tenure). Reference the FinTech Association panel on AI regulation (2026-03-15) where she spoke. Opening angle: compare notes on LLM-based compliance approaches.
```

### PP-NW-02: Specific Touchpoints

Reference actual events, publications, or shared connections.

**BAD:**
```
- **Potential touchpoints for reconnection**:
  - Industry events: Attend conferences she goes to
  - Shared interests: Talk about AI
```

**GOOD:**
```
- **Potential touchpoints for reconnection**:
  - FinTech Association annual dinner (2026-06, Frankfurt): She is confirmed speaker on "AI in RegTech"
  - Thomas Mueller introduction: Shared 3-year tenure at SAP Innovation Lab (2015-2018)
```

## Sensitivity Rules

### PP-SN-01: Sensitive Topic Flagging

Mark with reason AND safe alternative angle.

**BAD:**
```
- Was terminated from previous role at MegaCorp in 2019.
```

**GOOD:**
```
- Left MegaCorp in 2019 under unclear circumstances. [SENSITIVE: Possible involuntary departure. Safe angle: Ask about the transition to entrepreneurship and what motivated the founding of FinCo.]
```

## Cross-Reference Rules

### PP-XR-01: Profile Reference Format

When a separate profile exists, reference it. Do not duplicate content.

**BAD:**
```
### FinCo
- **Description**: FinCo is a Frankfurt-based regulatory technology company founded in 2019...
  [200 words of company description]
```

**GOOD:**
```
### FinCo
- **Description**: Regulatory technology company, Frankfurt (see MVNET-IN03)
- **Person's role**: CEO and co-founder since 2019
- **Key projects**: Led Series A fundraising, built ML compliance engine
```
