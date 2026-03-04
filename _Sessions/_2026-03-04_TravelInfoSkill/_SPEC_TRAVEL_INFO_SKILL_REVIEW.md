# Devil's Advocate Review: TRVL-SP01

**Doc ID**: TRVL-SP01-RV01
**Reviewed**: 2026-03-04 15:25
**Source**: `_SPEC_TRAVEL_INFO_SKILL.md [TRVL-SP01]`
**Reviewer**: Devil's Advocate workflow

## MUST-NOT-FORGET (Verified)

- [x] Goal: Agent skill for travel info with progressive disclosure + cost-based API escalation
- [x] 14 files total: 1 SKILL.md + 4 modes + 9 countries
- [x] APIs must escalate T0 -> T1 -> T2 -> T3 (cheapest first)
- [x] All URLs must be tested and working
- [x] Country files contain all modes; mode files only pan-European

## Industry Research Findings

### 1. AI Agent Skills Patterns (LangChain, Claude)

**Finding**: Industry best practice is **3-layer progressive disclosure**:
- Layer 1: Index/metadata only (titles, descriptions)
- Layer 2: Full content on demand
- Layer 3: Deep dive materials

**Gap in spec**: TRVL-SP01 specifies file structure but not metadata layer. All 14 files would need to be read to understand what's available. No lightweight index exists.

**Source**: honra.io/articles/progressive-disclosure-for-ai-agents

### 2. Travel API Reliability Issues

**Common failure modes**:
- Authentication/token expiration errors
- Rate limiting during peak hours
- Version incompatibility after API updates
- Data mapping inconsistencies
- Delayed response times

**Gap in spec**: No error handling strategy defined. What happens when T0 fetch fails? When T1 Brave returns no results? TRVL-FR-03 defines escalation but not failure recovery.

**Source**: supportsave.com/blog/travel-api-integration-issues

### 3. Progressive Disclosure for AI

**Best practice**: "Context rot" occurs when irrelevant information accumulates. Agents need to load only relevant context per query.

**Strength in spec**: TRVL-FR-02 limits to 3 file reads maximum - good constraint.

**Gap**: No mechanism to prioritize which sections within a file to read first.

### 4. API Cost Optimization

**Gap**: Spec assumes linear escalation (T0->T1->T2->T3) but some queries may benefit from skipping tiers. Complex research queries should go directly to T3.

### 5. Stale Data Handling

**Gap**: TRVL-IG-01 requires URLs tested "within 30 days" but provides no mechanism to detect or handle stale data at runtime.

## Critical Issues

**TRVL-RV-C01: No Metadata Index Layer**

- **What**: Spec requires reading full files to understand capabilities
- **Where**: File Structure (Section 8), TRVL-FR-02
- **Why it's a problem**: Agent must read SKILL.md + potentially 3 files = 4 file reads minimum. No lightweight discovery mechanism.
- **Industry pattern**: Claude Skills use name+description metadata loaded at startup, full content on demand
- **Suggested fix**: Add `INDEX.md` or metadata section in SKILL.md listing all files with 1-line descriptions and keyword tags

**TRVL-RV-C02: No Failure/Error Handling Strategy**

- **What**: TRVL-FR-03 defines escalation but not what happens when each tier fails
- **Where**: Section 4, TRVL-FR-03
- **Why it's a problem**: T0 fetch can fail (site down, blocked). T1 Brave can return empty. T2/T3 can timeout or exceed rate limits.
- **Suggested fix**: Add TRVL-FR-07 defining failure modes and recovery actions per tier

## High Priority Issues

**TRVL-RV-H01: UK is Not ISO 3166-1 Alpha-2**

- **What**: Spec uses "UK" but ISO 3166-1 alpha-2 code is "GB"
- **Where**: TRVL-DD-06, TRVL-FR-05, File Structure
- **Why it's a problem**: Inconsistency with stated design decision. "UK" is common usage but violates TRVL-DD-06.
- **Suggested fix**: Either use "GB" consistently, or change DD-06 to "ISO 3166-1 alpha-2 codes, except UK for readability"

**TRVL-RV-H02: No Cache/TTL Strategy**

- **What**: Travel data is highly time-sensitive but no caching strategy defined
- **Where**: Missing from spec entirely
- **Why it's a problem**: Flight delays change by minute. Train disruptions resolve. Fetched data can be stale within seconds.
- **Suggested fix**: Add TRVL-FR-08 defining TTL per data type (real-time: 0, disruptions: 5min, schedules: 1hr)

**TRVL-RV-H03: Query Resolution Algorithm Assumes Single Match**

- **What**: Algorithm in 7.1 assumes one primary file match
- **Where**: Section 7.1
- **Why it's a problem**: "Munich to Vienna trains" involves DE + AT + TRAINS. Algorithm shows reading one country file, not handling cross-border queries requiring multiple files.
- **Suggested fix**: Extend algorithm to handle multi-country queries explicitly

## Medium Priority Issues

**TRVL-RV-M01: Mode Files Purpose Unclear**

- **What**: DD-05 says mode files contain "pan-European resources only" but FLIGHTS.md scope says "(global + European airports)"
- **Where**: TRVL-DD-05 vs File Structure
- **Contradiction**: Is FLIGHTS.md global or pan-European only?
- **Suggested fix**: Clarify scope - recommend "pan-European and global trackers" for consistency

**TRVL-RV-M02: No Versioning Strategy**

- **What**: No version tracking for skill files
- **Where**: Missing from spec
- **Why it matters**: When resources change, how do we track what version agent is using?
- **Suggested fix**: Add version field to SKILL.md header

**TRVL-RV-M03: Lookup Table Pattern Matching Undefined**

- **What**: TRVL-FR-01 says "patterns support keywords" but exact matching logic undefined
- **Where**: Section 4, TRVL-FR-01; Section 7.2
- **Why it matters**: Is it substring match? Regex? Fuzzy match? Agent needs clear rules.
- **Suggested fix**: Define exact matching algorithm (recommend: keyword presence, case-insensitive)

**TRVL-RV-M04: No Fallback for Missing Country**

- **What**: Only 9 countries specified. What about Poland, Sweden, Portugal, etc.?
- **Where**: TRVL-FR-05
- **Why it matters**: User asks about "Warsaw flights" - no PL.md exists
- **Suggested fix**: Define fallback to EUROPE.md + mode file for uncovered countries

## Low Priority Issues

**TRVL-RV-L01: API Tier Names Inconsistent**

- **What**: Tiers called "T0-FETCH" in Domain Objects but "Tier 0" in Key Mechanisms
- **Where**: Section 3 vs Section 7.3
- **Suggested fix**: Standardize naming

**TRVL-RV-L02: Example URL Format Not Enforced**

- **What**: Resource Entry Format (7.4) shows "Example URL" but no validation
- **Where**: Section 7.4
- **Suggested fix**: Add note that example URLs must be tested annually

## Questions That Need Answers

1. **Q1**: Should agent cache API responses? If yes, what TTL per tier?
2. **Q2**: What happens when all tiers fail for a query?
3. **Q3**: Should mode files duplicate resources from country files for completeness, or strictly avoid duplication?
4. **Q4**: How does agent handle queries spanning 3+ countries (e.g., "Paris to Berlin to Vienna")?
5. **Q5**: Should SKILL.md be readable by agent at startup, or loaded on-demand like other files?

## Devil's Advocate Summary

**Reviewed**: `_SPEC_TRAVEL_INFO_SKILL.md [TRVL-SP01]`
**Time spent**: ~15 minutes

**Research Topics Investigated**:
1. AI agent skills patterns - 3-layer progressive disclosure is industry standard
2. Travel API reliability - Token expiration, rate limiting, version conflicts common
3. Progressive disclosure - "Context rot" from over-loading; max 3 files good constraint
4. API cost optimization - Linear escalation may not suit all query types
5. Stale data handling - Real-time travel data needs TTL strategy

**Findings**:
- CRITICAL: 2
- HIGH: 3
- MEDIUM: 4
- LOW: 2

**Top 3 Risks**:
1. No metadata index = agent reads full files to discover capabilities (context rot)
2. No error handling = undefined behavior when APIs fail or timeout
3. UK vs GB inconsistency = violates own design decision

**Industry Alternatives Identified**:
- Add INDEX.md with lightweight metadata (follows Claude Skills pattern)
- Define failure modes per tier with retry/fallback logic
- Add TTL/cache strategy for time-sensitive travel data

**Files Created/Updated**:
- `_SPEC_TRAVEL_INFO_SKILL_REVIEW.md` - This file (11 findings)
- `FAILS.md` - 0 new entries (no actual failures, only potential issues)

**Recommendation**: ~~PROCEED WITH CAUTION~~ **PROCEED** - All confirmed findings addressed in spec update [2026-03-04 15:35].

## Document History

**[2026-03-04 15:25]**
- Initial Devil's Advocate review
- 5 research topics investigated
- 11 findings documented (2 critical, 3 high, 4 medium, 2 low)
