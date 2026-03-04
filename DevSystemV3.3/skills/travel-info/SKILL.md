# Travel Info Skill

Find flights, trains, and public transport information across Europe.

## How to Use (3 Steps)

**Step 1: Pick ONE file**
- Country mentioned? Use that country file (DE.md, FR.md, etc.)
- No country? Use mode file (FLIGHTS.md, TRAINS.md, TRANSIT.md)
- Cross-border (Eurostar, Thalys)? Use EUROPE.md

**Step 2: Read the file and find a URL**
- Look for a resource matching the query
- Copy the URL

**Step 3: Fetch the URL**
- Success? Done.
- Failed? Use Brave Search to find a working URL.
- Still stuck? Use Perplexity for a summary.

## File Index

- **EUROPE.md** - Pan-European, cross-border (Eurostar, Thalys, FlightStats)
- **FLIGHTS.md** - Global flight tracking (Flightradar24, FlightAware, cancellations)
- **TRAINS.md** - European trains (Zugfinder, live maps, station boards)
- **TRANSIT.md** - City transit (Moovit, GTFS, metro apps)
- **DE.md** - Germany (DB, Frankfurt/Munich airports, BVG)
- **FR.md** - France (SNCF, CDG/ORY airports, RATP)
- **UK.md** - UK (National Rail, Heathrow, TfL)
- **AT.md** - Austria (OBB, Vienna airport)
- **CH.md** - Switzerland (SBB, Zurich airport)
- **IT.md** - Italy (Trenitalia, Rome/Milan airports)
- **BE.md** - Belgium (SNCB, Brussels airport, Eurostar hub)
- **NL.md** - Netherlands (NS, Schiphol)
- **ES.md** - Spain (Renfe, Madrid/Barcelona airports)

## Quick Reference

```
"Frankfurt flight delays"
-> Read: DE.md
-> Use: Flightradar24 or Frankfurt Airport site

"Eurostar disruptions"
-> Read: EUROPE.md
-> Use: Eurostar status page

"Paris to London train"
-> Read: EUROPE.md (cross-border)
-> Use: Eurostar or Trainline

"Berlin public transport"
-> Read: DE.md
-> Use: BVG website

"What flights are delayed in Europe?"
-> Read: FLIGHTS.md
-> Use: Flightradar24 or FlightAware

"Train delays in Italy"
-> Read: IT.md
-> Use: Trenitalia or ViaggiaTreno

"Amsterdam to Brussels train"
-> Read: EUROPE.md (cross-border)
-> Use: NS International or Thalys

"Munich airport arrivals"
-> Read: DE.md
-> Use: Munich Airport website

"Swiss train map"
-> Read: CH.md
-> Use: SBB live map

"General European flight tracker"
-> Read: FLIGHTS.md
-> Use: Flightradar24
```

## API Strategy

### Tier 0: Direct HTTP Fetch ($0)
- Use when: URL known from resource files
- Tool: web_fetch or HTTP GET
- Try this first, always

### Tier 1: Brave Search (~$0.005/query)
- Use when: URL not working, need to find alternative
- Best for: site: searches, URL discovery

### Tier 2: Perplexity Sonar (~$0.01/query)
- Use when: Need synthesized answer
- Best for: "What trains are delayed?" questions

### Tier 3: Anthropic Web Search (~$0.03/query)
- Use when: Complex multi-source research
- Best for: Itinerary planning, disruption analysis
- Use only as last resort
