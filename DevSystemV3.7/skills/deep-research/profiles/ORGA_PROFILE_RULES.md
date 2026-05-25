# Organization Profile Rules

Rules for writing and verifying organization profile INFO documents with GOOD/BAD examples.

## Rule Index

Header (HD)
- OP-HD-01: Depth tier set and sections match tier
- OP-HD-02: Organization type clearly identified (university, industry body, NGO, etc.)
- OP-HD-03: Related profiles link to person/company profiles of key members

Summary (SM)
- OP-SM-01: 3-5 sentences covering type, founding, scale, mission, relevance
- OP-SM-02: Distinguish stated mission from actual focus

Data (DT)
- OP-DT-01: Legal form matches jurisdiction (e.V., Stiftung, 501(c)(3), etc.)
- OP-DT-02: Size metric appropriate to type (members, students, employees, budget)
- OP-DT-03: Rankings/accreditations sourced and dated

Governance (GV)
- OP-GV-01: Leadership entries include appointment mechanism (elected, appointed, hereditary)
- OP-GV-02: Decision-making process explicitly stated
- OP-GV-03: Accountability direction clear (to whom does leadership answer)

Membership (MB)
- OP-MB-01: Entry criteria distinguish explicit (formal) from implicit (unspoken)
- OP-MB-02: Notable members relevant to research context, not just famous names
- OP-MB-03: Membership tiers described with distinguishing privileges

Programs (PG)
- OP-PG-01: Each program entry includes audience, format, frequency, scale
- OP-PG-02: Events include date/frequency, not just name

Engagement (EN)
- OP-EN-01: Entry points are specific paths (application, event, committee), not vague
- OP-EN-02: Timing tied to org's calendar (membership cycles, annual events)
- OP-EN-03: At least one concrete, actionable recommendation

Sensitivity (SN)
- OP-SN-01: Political/ideological orientation stated only when discernible from evidence
- OP-SN-02: Criticism section balanced with source attribution

Sources (SC)
- OP-SC-01: All sources include access date
- OP-SC-02: Official org sources (website, annual report) prioritized over third-party descriptions

Cross-Reference (XR)
- OP-XR-01: Key governance members reference personal profiles when they exist
- OP-XR-02: Partner organizations reference their own profiles when they exist

## Header Rules

### OP-HD-01: Depth Tier Compliance

Sections must match tier:
- BRIEF: Summary + Organization Data + Mission and Purpose + Engagement Strategy only
- STANDARD: Skip Funding Model, detailed Programs subsections
- FULL: All sections filled

**BAD:**
```
**Depth tier**: BRIEF

## Summary
[filled]
## Organization Data
[filled]
## Mission and Purpose
[filled]
## Governance Structure
[filled - should not appear in BRIEF]
## Membership and Constituency
[filled - should not appear in BRIEF]
```

**GOOD:**
```
**Depth tier**: BRIEF

## Summary
[filled]
## Organization Data
[filled]
## Mission and Purpose
[filled]
## Engagement Strategy
[filled]
## Sources
[filled]
```

## Mission Rules

### OP-SM-02: Stated vs Actual Focus

Distinguish between official narrative and observable behavior.

**BAD:**
```
## Mission and Purpose

- **Official mission**: Advancing digital innovation in financial services
- **Actual focus**: Same as above
```

**GOOD:**
```
## Mission and Purpose

- **Official mission**: "Advancing digital innovation in financial services for sustainable growth" (charter, 2018)
- **Actual focus**: Lobbying platform for incumbent banks against fintech regulation. 80% of published position papers defend existing banking regulations. [ASSUMED - based on publication analysis]
- **Target constituency**: C-level executives at banks with >EUR 10B assets
- **Value proposition**: Regulatory early-warning system and peer networking among non-competing institutions
```

## Governance Rules

### OP-GV-01: Appointment Mechanism

How leaders got there matters for understanding power dynamics.

**BAD:**
```
### Leadership
- **Dr. Hans Mueller** - President (since 2021)
```

**GOOD:**
```
### Leadership
- **Dr. Hans Mueller** - President (since 2021). Elected by general assembly for 3-year term. Previously board member (2018-2021). CEO of Deutsche FinanzBank.
```

### OP-GV-02: Decision-Making Clarity

Specify how decisions flow.

**BAD:**
```
- **Decision-making**: Board decides things
```

**GOOD:**
```
- **Decision-making**: 7-member executive board (majority vote). Strategic decisions require supervisory board approval (15 members, rotating industry representatives). Budget >EUR 500K requires general assembly ratification.
```

## Membership Rules

### OP-MB-01: Explicit vs Implicit Criteria

Separate formal requirements from unspoken ones.

**BAD:**
```
- **Membership criteria**: Companies in financial services can join
```

**GOOD:**
```
- **Membership criteria**: Formal: registered financial institution in DACH region, annual revenue >EUR 100M, nomination by existing member. Implicit: traditional banking background preferred - fintech/neobank applications reportedly deprioritized [ASSUMED - based on member composition analysis showing 0 neobanks among 45 members]
```

## Program Rules

### OP-PG-01: Program Entry Completeness

Each program needs enough detail to evaluate attendance value.

**BAD:**
```
- **Annual Conference**: Big event, many attendees
- **Working Groups**: Members collaborate
```

**GOOD:**
```
- **Annual Banking Summit**: Purpose: Peer networking and regulatory briefing. Audience: C-level from member institutions (120-150 attendees). Format: 2-day conference, invitation-only dinners. Frequency: Annual (November). Scale: EUR 800K budget, 30 speakers.
- **RegTech Working Group**: Purpose: Joint position papers on fintech regulation. Audience: Compliance heads and legal counsel. Format: Monthly virtual meetings + quarterly in-person. Frequency: 12x/year. Scale: 25 active participants from 18 institutions.
```

## Engagement Rules

### OP-EN-01: Specific Entry Points

Name the actual path in, not categories.

**BAD:**
```
- **Entry points**: Membership, events, partnerships
```

**GOOD:**
```
- **Entry points**:
  - Guest attendance at Annual Banking Summit (apply via website by August, EUR 2,500 non-member fee, requires member recommendation)
  - RegTech Working Group observer status (request via Dr. Mueller's office, no fee, 3-month trial)
  - Associate membership (EUR 25K/year, simplified application for technology vendors, limited voting rights)
```

### OP-EN-02: Calendar-Aligned Timing

Tie recommendations to the org's actual schedule.

**BAD:**
```
- **Timing considerations**: Apply when ready
```

**GOOD:**
```
- **Timing considerations**:
  - Membership applications reviewed in Q1 (January-March) for April intake
  - Annual Summit registration opens August, fills by September
  - Working Group new observer slots available after annual restructuring (January)
  - Board election year 2027 - turnover creates openness to new relationships
```

## Sensitivity Rules

### OP-SN-01: Political Orientation from Evidence

Only state when supported by observable indicators.

**BAD:**
```
- **Political/ideological orientation**: Conservative, anti-innovation
```

**GOOD:**
```
- **Political/ideological orientation**: Pro-incumbent banking regulation. Evidence: 8 of 10 recent position papers oppose open banking mandates. Board composition 100% traditional banking. No fintech representation despite stated "innovation" mission. [ASSUMED - inferred from publication and membership patterns]
```
