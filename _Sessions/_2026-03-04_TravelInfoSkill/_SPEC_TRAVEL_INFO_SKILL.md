# SPEC: Travel Information Skill

**Doc ID**: TRVL-SP01
**Feature**: TRAVEL_INFO_SKILL
**Goal**: Specify an agent skill for retrieving European travel information with progressive disclosure and cost-based API escalation
**Timeline**: Created 2026-03-04
**Target file**: `[DEVSYSTEM_FOLDER]/skills/travel-info/SKILL.md`

**Depends on:**
- `_INFO_TRAVEL_RESEARCH_LINKS.md [OCLAW-IN05]` for curated resource list

## MUST-NOT-FORGET

- Use lists, not Markdown tables
- Progressive disclosure: general -> specific (continent -> country -> mode)
- API escalation: cheapest first (HTTP fetch -> Brave -> Perplexity -> Anthropic)
- All URLs must be tested and working
- Country codes use ISO 3166-1 alpha-2 (DE, FR, UK, etc.)

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Design Decisions](#5-design-decisions)
6. [Implementation Guarantees](#6-implementation-guarantees)
7. [Key Mechanisms](#7-key-mechanisms)
8. [File Structure](#8-file-structure)
9. [Document History](#9-document-history)

## 1. Scenario

**Problem:** Agent needs travel information (flights, trains, transit) but lacks structured knowledge of which sources to query, in what order, and at what cost.

**Solution:**
- Create skill with lookup table mapping query patterns to resource files
- Implement progressive disclosure: continent -> country -> travel mode
- Define cost-based API escalation strategy
- Provide tested URLs for direct HTTP fetch

**What we don't want:**
- Hardcoded URLs in SKILL.md (use separate files)
- API calls when HTTP fetch suffices
- Expensive APIs for simple queries
- Untested or broken URLs

## 2. Context

This skill supports OpenClaw and similar AI agents in travel research tasks. The skill organizes 30+ European travel resources from `_INFO_TRAVEL_RESEARCH_LINKS.md [OCLAW-IN05]` into a queryable structure with progressive disclosure.

**Use cases:**
- "Flight delays at Frankfurt" -> DE.md + FLIGHTS.md
- "Eurostar disruptions" -> EUROPE.md (cross-border)
- "Munich to Vienna trains" -> DE.md + AT.md + TRAINS.md
- "Berlin public transport" -> DE.md + TRANSIT.md

## 3. Domain Objects

### ResourceFile

A **ResourceFile** is a markdown file containing travel resources for a specific scope.

**Storage:** `.windsurf/skills/travel-info/`

**Key properties:**
- `scope` - Geographic or modal scope (continent, country, mode)
- `resources` - List of URLs with metadata
- `priority` - Query order (1=first)

**Types:**
- **Continent files**: `EUROPE.md` - Pan-European and cross-border resources
- **Country files**: `DE.md`, `FR.md`, `UK.md` - Country-specific resources
- **Mode files**: `FLIGHTS.md`, `TRAINS.md`, `TRANSIT.md` - Travel mode resources

### LookupEntry

A **LookupEntry** maps query patterns to resource files.

**Key properties:**
- `pattern` - Keywords or regex to match
- `primary` - First file to consult
- `fallback` - Secondary file if primary insufficient
- `apis` - Allowed API tiers for this pattern

### APITier

An **APITier** defines a search API with cost and capability.

**Tiers:**
- `T0-FETCH` - Direct HTTP fetch ($0)
- `T1-BRAVE` - Brave Search API (~$0.005/query)
- `T2-PERPLEXITY` - Perplexity Sonar (~$0.01/query)
- `T3-ANTHROPIC` - Anthropic Web Search (~$0.03/query)

## 4. Functional Requirements

**TRVL-FR-01: Lookup Table**
- SKILL.md contains pattern-to-file mapping
- Patterns support keywords and country codes
- Each entry specifies primary and fallback files
- Entries ordered by specificity (most specific first)

**TRVL-FR-02: Progressive Disclosure**
- Start with most specific match (country + mode)
- Fall back to broader scope (continent, then mode-only)
- Stop when query is answered
- Maximum 3 file reads per query

**TRVL-FR-03: API Escalation**
- Always try T0 (HTTP fetch) first if URL available
- Escalate to T1 (Brave) for URL discovery
- Escalate to T2 (Perplexity) for synthesis
- Escalate to T3 (Anthropic) only for complex multi-source research

**TRVL-FR-04: Resource File Format**
- Each resource has: name, URL, description, test status
- URLs grouped by category (real-time, static, API)
- Include example queries for each resource
- Mark blocked sites with workaround notes

**TRVL-FR-05: Country Coverage**
- Required countries: DE, FR, UK, AT, CH, IT, BE, NL, ES
- Each country file includes: flights, trains, transit
- Cross-border resources in EUROPE.md
- For countries without dedicated files, use EUROPE.md + mode file as fallback

**TRVL-FR-06: Mode Coverage**
- FLIGHTS.md: airport trackers, cancellation lists, delay maps
- TRAINS.md: live train maps, station boards, disruption alerts
- TRANSIT.md: city transit apps, GTFS feeds, journey planners

## 5. Design Decisions

**TRVL-DD-01:** Flat file structure with 2-letter country codes. Rationale: Simple navigation, no nested folders, grep-friendly.

**TRVL-DD-02:** SKILL.md contains only lookup logic and API strategy, not URLs. Rationale: Separation of concerns, easier maintenance.

**TRVL-DD-03:** Cost-based API ordering (cheapest first). Rationale: Minimize expenses, most queries solvable with HTTP fetch.

**TRVL-DD-04:** Country files contain all modes for that country. Rationale: One file per geographic context, reduces file count.

**TRVL-DD-05:** Mode files contain pan-European and global trackers. Rationale: Avoid duplication with country files while providing global coverage.

**TRVL-DD-06:** ISO 3166-1 alpha-2 country codes, using UK instead of GB for readability. Rationale: Standard codes with pragmatic exception for universal recognition.

## 6. Implementation Guarantees

**TRVL-IG-01:** All URLs in resource files tested within 30 days of last update.

**TRVL-IG-02:** Each resource file has at least 3 working URLs.

**TRVL-IG-03:** Blocked sites documented with alternative or workaround.

**TRVL-IG-04:** API cost estimates updated when pricing changes.

## 7. Key Mechanisms

### 7.1 How to Use (Simple 3 Steps)

**Step 1: Pick ONE file from the File Index**
- Country mentioned? Use that country file (DE.md, FR.md, etc.)
- No country? Use mode file (FLIGHTS.md, TRAINS.md, TRANSIT.md)
- Cross-border (Eurostar, Thalys)? Use EUROPE.md

**Step 2: Read the file and find a URL**
- Look for a resource matching the query
- Copy the URL

**Step 3: Try to fetch the URL**
- Success? Done.
- Failed? Use Brave Search to find a working URL.
- Still stuck? Use Perplexity for a summary.

### 7.2 Quick Reference (Copy These Examples)

```
"Frankfurt flight delays"
→ Read: DE.md
→ Use: Flightradar24 or Frankfurt Airport site

"Eurostar disruptions"
→ Read: EUROPE.md
→ Use: Eurostar status page

"Paris to London train"
→ Read: EUROPE.md (cross-border)
→ Use: Eurostar or Trainline

"Berlin public transport"
→ Read: DE.md
→ Use: BVG website

"What flights are delayed in Europe?"
→ Read: FLIGHTS.md
→ Use: Flightradar24 or FlightAware

"Train delays in Italy"
→ Read: IT.md
→ Use: Trenitalia or ViaggiaTreno

"Amsterdam to Brussels train"
→ Read: EUROPE.md (cross-border)
→ Use: NS International or Thalys

"Munich airport arrivals"
→ Read: DE.md
→ Use: Munich Airport website

"Swiss train map"
→ Read: CH.md
→ Use: SBB live map

"General European flight tracker"
→ Read: FLIGHTS.md
→ Use: Flightradar24
```

### 7.3 API Strategy Section Format

```markdown
## API Strategy

### Tier 0: Direct HTTP Fetch ($0)
- Use when: URL known from resource files
- Tool: web_fetch, HTTP GET
- Latency: ~500ms

### Tier 1: Brave Search (~$0.005/query)
- Use when: Need to find specific URL
- Best for: site: searches, URL discovery
- Latency: ~400ms

### Tier 2: Perplexity Sonar (~$0.01/query)
- Use when: Need synthesized answer
- Best for: "What trains are delayed?" questions
- Latency: ~2s

### Tier 3: Anthropic Web Search (~$0.03/query)
- Use when: Complex multi-source research
- Best for: Itinerary planning, disruption analysis
- Latency: ~4s
```

### 7.4 Resource Entry Format

```markdown
### [Resource Name] [STATUS]

- **URL**: https://example.com/path
- **Scope**: [country code or "pan-European"]
- **Real-time**: Yes/No
- **Free**: Yes/Freemium/No
- **Best for**: [use case description]
- **Example query**: "Frankfurt departures today"
- **Example URL**: https://example.com/airport/FRA/departures
```

### 7.5 File Index (for SKILL.md)

SKILL.md must include a lightweight file index for progressive disclosure:

```markdown
## File Index

- **EUROPE.md** - Pan-European, cross-border (Eurostar, Thalys, FlightStats)
- **FLIGHTS.md** - Global flight tracking (Flightradar24, FlightAware, cancellations)
- **TRAINS.md** - European trains (Zugfinder, live maps, station boards)
- **TRANSIT.md** - City transit (Moovit, GTFS, metro apps)
- **DE.md** - Germany (DB, Frankfurt/Munich airports, BVG)
- **FR.md** - France (SNCF, CDG/ORY airports, RATP)
- **UK.md** - UK (National Rail, Heathrow, TfL)
- **AT.md** - Austria (ÖBB, Vienna airport)
- **CH.md** - Switzerland (SBB, Zurich airport)
- **IT.md** - Italy (Trenitalia, Rome/Milan airports)
- **BE.md** - Belgium (SNCB, Brussels airport, Eurostar hub)
- **NL.md** - Netherlands (NS, Schiphol)
- **ES.md** - Spain (Renfe, Madrid/Barcelona airports)
```

## 8. File Structure

```
.windsurf/skills/travel-info/
├── SKILL.md          # Lookup table + API strategy + usage instructions
├── EUROPE.md         # Pan-European, cross-border resources
├── FLIGHTS.md        # Flight tracking (global + European airports)
├── TRAINS.md         # Train tracking (European focus)
├── TRANSIT.md        # Public transport, GTFS, city apps
├── DE.md             # Germany (DB, airports, BVG, MVV)
├── FR.md             # France (SNCF, airports, RATP)
├── UK.md             # UK (National Rail, airports, TfL)
├── AT.md             # Austria (ÖBB, VIE airport)
├── CH.md             # Switzerland (SBB, ZRH airport)
├── IT.md             # Italy (Trenitalia, airports)
├── BE.md             # Belgium (SNCB, BRU airport, Eurostar hub)
├── NL.md             # Netherlands (NS, AMS airport)
└── ES.md             # Spain (Renfe, airports)
```

**File count:** 14 files (1 SKILL + 4 modes + 9 countries)

## 9. Document History

**[2026-03-04 15:45]**
- Changed: Simplified algorithm to 3 steps for smaller models
- Added: Quick Reference with 10 concrete examples (7.2)
- Removed: Complex lookup table format (too hard for mini models)

**[2026-03-04 15:35]**
- Added: File Index section (7.5) for progressive disclosure
- Changed: DD-05 to include global trackers
- Changed: DD-06 to acknowledge UK exception
- Added: Multi-country handling to algorithm (7.1)
- Added: Escalation-on-failure to algorithm
- Added: Fallback for missing countries to FR-05

**[2026-03-04 15:20]**
- Initial specification created
- Defined 6 functional requirements, 6 design decisions
- Specified file structure with 14 files
- Documented lookup table and API strategy formats
