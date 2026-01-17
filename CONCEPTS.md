# CONCEPTS

Inventory of named concepts used in the DevSystem. Brief definitions only - see referenced specs for details.

## Frameworks

- **AGEN** - Agentic English. Controlled vocabulary for agent-human communication. See `SPEC_AGEN_AGENTIC_ENGLISH.md`
- **EDIRD** - Explore, Design, Implement, Refine, Deliver. 5-phase workflow model. See `SPEC_EDIRD_PHASE_MODEL.md`
- **STRUT** - Structured Thinking (proposed). Method for planning and tracking complex autonomous work
- **TRACTFUL** - Traceable Requirements Artifacts and Coded Templates For Unified Lifecycle (proposed). Document framework

## Identifiers

- **FEATURE_SLUG** - Kebab-case feature identifier (e.g., `user-authentication`)
- **TOPIC** - 2-6 uppercase letters identifying a component (e.g., `AUTH`, `CRWL`). Must be registered in NOTES.md
- **TDID** - Tractful Document ID. Format: `[TOPIC]-[DOC][NN]`. Guarantees workspace-wide uniqueness

## Measurement

- **HHW** - Human Hours of Work. Partition target: max 0.5 HHW per task
- **AHW** - Agentic Hours of Work. Agent time estimate

## Strategies

- **MEPI** - Most Executable Point of Information. Prioritize actionable over comprehensive
- **MCPI** - Most Complete Point of Information. Traditional exhaustive research
- **SOCAS** - Signs Of Confusion And Sloppiness. Quality evaluation heuristic (10 criteria)

## Document Types

- **INFO** (IN) - Research and analysis documents
- **SPEC** (SP) - Technical specifications (FR, DD, IG)
- **IMPL** (IP) - Implementation plans (IS, EC)
- **TEST** (TP) - Test plans (TC, VC)
- **TASKS** (TK) - Partitioned work items
- **FIX** - Fix tracking during implementation
- **REVIEW** (RV) - Review findings

## Tracking Documents

- **NOTES** - Key decisions, topic registry, current phase. Agent MUST read
- **PROGRESS** - To Do, In Progress, Done, phase plan
- **PROBLEMS** - Issues discovered during session. Sync on `/session-close`
- **FAILS** - Failure log (lessons learned). Agent MUST read during `/prime`

## Document History

**[2026-01-17 14:44]**
- Simplified to inventory format - removed spec replication

**[2026-01-17 14:41]**
- Synced ALL concepts from session and DevSystemV3.1

**[2026-01-17 14:12]**
- Initial creation
