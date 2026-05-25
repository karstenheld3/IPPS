# Network Profile Rules

Rules for writing and verifying network profile INFO documents with GOOD/BAD examples.

## Rule Index

Header (HD)
- NP-HD-01: Depth tier set and sections match tier
- NP-HD-02: Network type and formality level clearly identified
- NP-HD-03: Related profiles link to member personal profiles

Summary (SM)
- NP-SM-01: 3-5 sentences covering type, size, scope, themes, vitality
- NP-SM-02: Lifecycle stage supported by evidence

Identity (ID)
- NP-ID-01: Formality level distinguishes formal/semi-formal/informal with criteria
- NP-ID-02: Lifecycle stage matches observable indicators

Focus (FC)
- NP-FC-01: Open Value Analysis based on public claims with source citations
- NP-FC-02: Hidden Value Analysis labeled with assessment confidence (HIGH/MEDIUM/LOW)
- NP-FC-03: Evidence for hidden analysis comes from observable patterns, not speculation

Inner Circle (IC)
- NP-IC-01: Core members limited to 5-15 people with disproportionate influence
- NP-IC-02: Each member entry has day job, network role, and influence mechanism
- NP-IC-03: Succession risk assessed for central nodes

Structure (ST)
- NP-ST-01: Topology described using standard types (hub-spoke, distributed, hierarchical, clustered, chain)
- NP-ST-02: Sub-clusters have binding topic, members, and bridge persons identified
- NP-ST-03: Communication channels include frequency and rhythm

Entry (EN)
- NP-EN-01: Explicit and implicit barriers separated
- NP-EN-02: Recommended entry path specific to requester's position
- NP-EN-03: Entry cost quantified (financial, time, social capital)

Member Analysis (MA)
- NP-MA-01: Full format for inner circle, 1-line format for peripherals
- NP-MA-02: Contribution/extraction balance assessed per member
- NP-MA-03: Influence score relative within network (HIGH/MEDIUM/LOW)

Value Flow (VF)
- NP-VF-01: Tangible and intangible outputs separated
- NP-VF-02: Value distribution identifies asymmetries (who benefits vs contributes most)
- NP-VF-03: Free riders identified with evidence

Strategic (SA)
- NP-SA-01: Entry feasibility realistic (not aspirational)
- NP-SA-02: Alternative networks named when access is difficult
- NP-SA-03: Risks of engagement explicitly stated

Sensitivity (SN)
- NP-SN-01: Hidden dynamics labeled `[ASSUMED]` with confidence level
- NP-SN-02: Power dynamics described without judgmental language
- NP-SN-03: Exclusion patterns stated as observation, not accusation

Sources (SC)
- NP-SC-01: All sources include access date
- NP-SC-02: Hidden analysis sources clearly distinguished from open analysis sources

## Header Rules

### NP-HD-01: Depth Tier Compliance

Sections must match tier:
- BRIEF: Summary + Network Identity + Inner Circle + Strategic Assessment only
- STANDARD: Skip Value Flow Analysis, detailed Sub-Clusters
- FULL: All sections filled. Full Member Analysis for inner circle, 1-line for peripherals.

**BAD:**
```
**Depth tier**: BRIEF

## Summary
[filled]
## Network Identity
[filled]
## Focus and Purpose
[filled - should not appear in BRIEF]
## Inner Circle
[filled]
## Network Structure
[filled - should not appear in BRIEF]
## Member Analysis
[filled - should not appear in BRIEF]
```

**GOOD:**
```
**Depth tier**: BRIEF

## Summary
[filled]
## Network Identity
[filled]
## Inner Circle
[filled]
## Strategic Assessment
[filled]
## Sources
[filled]
```

## Focus Rules

### NP-FC-01: Open Value Analysis Sourced

Claims about the network's stated purpose need citations.

**BAD:**
```
### Stated Focus (Open Value Analysis)
- **Official mission**: They want to promote innovation
- **Stated goals**: Be innovative and collaborative
```

**GOOD:**
```
### Stated Focus (Open Value Analysis)
- **Official mission**: "Connecting leaders shaping the future of European financial services" (website header, accessed 2026-05-20)
- **Stated goals**: 1) Cross-pollinate ideas between banking and tech, 2) Create deal flow for members, 3) Influence EU fintech regulation (annual report 2025, p.3)
- **Key claims**:
  - "50+ deals facilitated in 2025" - Evidence: 12 verifiable from press releases, remainder [ASSUMED]
  - "Non-hierarchical peer network" - Evidence: Contradicted by inner circle analysis below
```

### NP-FC-02: Hidden Analysis Confidence

Hidden value analysis requires explicit confidence assessment.

**BAD:**
```
### Hidden Focus (Hidden Value Analysis)
- **Actual binding mechanism**: Money and power
- **Unstated value exchange**: They all get rich together
```

**GOOD:**
```
### Hidden Focus (Hidden Value Analysis)
- **Actual binding mechanism**: Shared exit from Deutsche FinanzBank 2015 restructuring. 8 of 12 inner circle members were DVPs+ at DFB before 2016. Maintained deal-flow relationships post-exit.
- **Unstated value exchange**: Pre-market deal flow (members see investment opportunities before public announcement). Talent pipeline (junior hires rotate between member companies).
- **Common characteristics of members**: Male (11/12 inner circle), 45-55 age range, MBA from INSEAD or St. Gallen, German-speaking, minimum EUR 5M personal net worth [ASSUMED]
- **Exclusion patterns**: No women in inner circle despite 3 qualified female executives in broader network. No members from neobanks/fintechs despite stated "innovation" mission.

**Assessment confidence**: MEDIUM - based on 4 confirmed data points (career histories, event attendance, deal announcements) + 3 inferred patterns
```

## Inner Circle Rules

### NP-IC-02: Member Entry Completeness

Each inner circle member needs role, function, and mechanism.

**BAD:**
```
- **Thomas Mueller** (CEO of FinCo). Important member.
- **Anna Schmidt** (Investor). Very connected.
```

**GOOD:**
```
- **Thomas Mueller** (CEO, FinCo GmbH). Network role: Convener. Influence: Hosts quarterly dinners, controls guest list. Only person with direct relationships to all other inner circle members.
- **Anna Schmidt** (Partner, Capital Partners AG). Network role: Gatekeeper. Influence: Controls deal flow access. Her "no" excludes companies from syndicate rounds.
```

### NP-IC-03: Succession Risk

Assess what happens when key nodes depart.

**BAD:**
```
- **Succession risk**: Network would be fine without anyone.
```

**GOOD:**
```
- **Succession risk**: HIGH for Thomas Mueller (sole convener, only full-mesh node). Network likely fragments into 3 sub-clusters without him. LOW for any single peripheral member. MEDIUM for Anna Schmidt (deal flow would redirect to competitor syndicate within 6 months).
```

## Entry Barrier Rules

### NP-EN-01: Explicit vs Implicit Separation

Formal and informal barriers are different things.

**BAD:**
```
- **Entry barriers**: Hard to get in, need connections
```

**GOOD:**
```
- **Explicit requirements**: None formally published. Attendance at quarterly dinner requires personal invitation from inner circle member.
- **Implicit requirements**: EUR 1M+ personal investment capacity (minimum to participate in syndicate rounds). DACH-region financial services background. Male (observed, not stated). Age 40+ (youngest member is 43).
- **Introduction mechanism**: Existing member brings you as +1 to dinner. If accepted, receive direct invitations thereafter. Trial period: ~2 dinners before inclusion in deal flow communications.
```

### NP-EN-02: Requester-Specific Entry Path

Tailor the entry recommendation.

**BAD:**
```
- **Recommended entry path**: Get introduced by someone
```

**GOOD:**
```
- **Recommended entry path**: 1) Warm introduction via Thomas Mueller (2nd-degree via shared SAP tenure). 2) Attend FinTech Association annual dinner (November) where 6 inner circle members are confirmed. 3) Position as AI/compliance expert - fills a gap in network's capability set (currently no deep tech expertise among members).
```

## Member Analysis Rules

### NP-MA-01: Format by Importance

Inner circle gets full analysis. Peripherals get one line.

**BAD:**
```
### Thomas Mueller (CEO)
[full analysis]

### Random Attendee #1 (Unknown)
[full analysis - wastes space for peripheral member]
```

**GOOD:**
```
### Thomas Mueller (CEO, FinCo GmbH)
- **Network role**: Convener / Core
- **Joined/Connected since**: 2016 (founding member)
- **Contributions to network**: Deal flow origination (3-4 opportunities/quarter), event hosting, introductions to institutional LPs
- **Extractions from network**: Co-investment capital for FinCo portfolio, talent referrals, board member recruitment
- **Influence score**: HIGH
- **Bridge function**: Connects to London VC scene via Capital Partners relationship

**Peripheral members:**
- **Klaus Weber** (CFO, MidBank AG) - Contributes: Due diligence expertise. Extracts: Deal flow. Bridge: None.
- **Stefan Gross** (Partner, LawFirm) - Contributes: Legal structuring. Extracts: Client referrals. Bridge: Regulatory network.
```

## Value Flow Rules

### NP-VF-02: Asymmetry Identification

Who gets more than they give?

**BAD:**
```
- **Who benefits most**: Everyone benefits equally
```

**GOOD:**
```
- **Who benefits most**: Thomas Mueller (FinCo received EUR 8M in co-investment from network members in 2024-2025, while contributing primarily social capital/hosting). Anna Schmidt (uses network for proprietary deal sourcing, estimated 40% of her fund's pipeline originates here).
- **Who contributes most**: Klaus Weber (provides 15-20 hours/quarter of pro-bono due diligence for network deals, extracts only 1-2 co-investment slots/year).
- **Free riders**: Stefan Gross - attended 8 of 12 dinners in 2025, contributed 0 deals, extracted 3 client mandates. [ASSUMED - based on event attendance and no visible deal contribution]
```

## Strategic Assessment Rules

### NP-SA-01: Realistic Feasibility

Don't overstate access potential.

**BAD:**
```
- **Entry feasibility**: Easy - just attend an event
```

**GOOD:**
```
- **Entry feasibility**: MEDIUM. Path exists via Thomas Mueller (warm 2nd-degree connection). Barrier: Current investment capacity below network norm (EUR 1M+). Mitigant: AI/compliance expertise fills genuine gap. Timeline: 3-6 months from first dinner to deal flow inclusion.
```

### NP-SA-02: Alternatives When Access is Difficult

Name backup options.

**BAD:**
```
- **Alternative networks**: Other networks exist
```

**GOOD:**
```
- **Alternative networks**:
  - FinTech Association DACH (formal, easier entry via membership application, EUR 5K/year, less exclusive deal flow)
  - Munich Angel Network (open applications quarterly, lower ticket sizes EUR 25-250K, broader tech focus)
  - RegTech Founders Circle (WhatsApp group, introduction via any existing member, purely operational/product focus, no investment component)
```
