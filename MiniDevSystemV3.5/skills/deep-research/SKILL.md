---
name: deep-research
description: Apply when conducting deep research on technologies, APIs, frameworks, or other software development topics requiring systematic investigation
---

# Deep Research Skill

Systematic research using MCPI (Most Complete Point of Information) or MEPI (Most Executable Point of Information) approaches.

## When to Use

- Making informed decisions between alternatives
- Understanding something deeply before acting
- Preparing for complex undertakings
- Evaluating risks, trade-offs, or consequences
- Gathering exhaustive knowledge on a topic

## Quick Start

1. Read this SKILL.md
2. Read appropriate strategy file (MCPI or MEPI)
3. Follow Phases 1-4
4. Output as INFO document

## Phase Model (Global)

**Phase 1 - Preflight**: Decompose prompt, document assumptions, collect sources, verify/correct, create STRUT with QA pipelines, run first VCRIV

**Phase 2 - Planning**: Create TOC, topic template, TASKS plan, run second VCRIV

**Phase 3 - Research**: Topic-by-topic file-by-file per TASKS/STRUT, run VCRIV per granularity rules

**Phase 4 - Final Verification and Sync**: Dimension coverage, completeness check, metadata, final VCRIV

Strategy files (MCPI/MEPI) define details for each phase.

## Prompt Decomposition (Phase 1, Step 1)

Answer 7 questions before any source collection:

1. **Q1 - Goal**: User's intent (1-2 sentences)
2. **Q2 - Scope**: NARROW (1 dim), FOCUSED (2-4 dim), EXPLORATORY (5-9 dim)
3. **Q3 - Dimensions**: legal, financial, administrative, practical, technical, professional, medical, psychological, personal, organizational, strategic, security, cultural, educational, historical, or custom
4. **Q4 - Topics**: 3-5 topics per dimension
5. **Q5 - Strategy**: MCPI (exhaustive) or MEPI (curated)
6. **Q6 - Domain**: SOFTWARE, MARKET_INTEL, DOCUMENT_INTEL, LEGAL, or DEFAULT
7. **Q7 - Discovery Platforms**: What databases/platforms index this entity type? Test each, classify access level.

Store PromptDecomposition in STRUT plan. Do NOT proceed to source collection until all 7 answered.

### PromptDecomposition Schema

```json
{
  "goal": "string (1-2 sentences)",
  "scope": "NARROW | FOCUSED | EXPLORATORY",
  "dimensions": ["list of dimension names"],
  "topics_per_dimension": { "dimension": ["topics"] },
  "strategy": "MCPI | MEPI",
  "strategy_rationale": "string",
  "domain": "DEFAULT | SOFTWARE | MARKET_INTEL | DOCUMENT_INTEL | LEGAL",
  "domain_rationale": "string",
  "effort_estimate": "N hours minimum",
  "discovery_platforms": {
    "identified": ["platforms"],
    "tested": { "platform_name": "FREE | PAID | PARTIAL" },
    "selected": ["FREE or PARTIAL only"]
  }
}
```

### Scope Examples

- NARROW: "Rate limits for Microsoft Graph API?" -> 1 dimension (technical)
- FOCUSED: "PostgreSQL or MongoDB for event sourcing?" -> 3 dimensions (technical, operational, financial)
- EXPLORATORY: "Startup SOC 2 compliance?" -> 6 dimensions (legal, technical, organizational, financial, operational, educational)

## MUST-NOT-FORGET

- **STRUT required** for all research sessions (include pipeline steps and time log)
- **Assumptions check first** - write down what you think you know before researching
- **Discovery platforms tested** - identify, test, classify (FREE/PAID/PARTIAL) before source collection
- **Primary sources > secondary > community** - verify tier 1-3 before accepting tier 6-8
- **Access dates required**: `Accessed: YYYY-MM-DD` on all sources
- **Track time** - log task start/end for net research time calculation
- **Quality pipeline 3x** (not optional): TOC+template, each topic, complete set
- **Source completeness**: Full PDF transcription via pipeline, no agent-selected chunks
- **Download and store** all sources in session folder (web content changes)
- **Inline citations** on critical conclusions: `[LABEL] (SOURCE_ID | URL or filename)`
- **Identify domain** during Preflight, read corresponding DOMAIN_*.md profile
- **Document strategy choice** - OUTPUT document must include strategy (MEPI/MCPI) + domain + rationale for both in header block
- **Distinguish** facts from opinions from assumptions
- **Autonomous after Phase 1** - no user interaction until delivery (except [CONSULT])

## Strategy Selection

**MEPI** (Default) - curated options, deeply researched, compare and recommend
- Use for: specific intent, danger of analysis-paralysis
- File: [RESEARCH_STRATEGY_MEPI.md](RESEARCH_STRATEGY_MEPI.md)

**MCPI** (Exception) - exhaustive coverage, document everything
- Use for: broad intent, wants whole picture
- File: [RESEARCH_STRATEGY_MCPI.md](RESEARCH_STRATEGY_MCPI.md)

## Source Hierarchy

1. Official PDFs/papers (legislation, specs, whitepapers)
2. Official documentation
3. Official blog/changelog
4. GitHub repo
5. Conference talks by maintainers
6. Reputable tech blogs
7. Stack Overflow
8. Community forums/Discord

**Enforcement** (legal/financial/medical): MUST cite tier 1-3 for critical claims. Label tier 6-8 as `[COMMUNITY]`. Violation triggers `[CONSULT]`.

## Verification Labels

- `[VERIFIED]` - Confirmed from official docs
- `[ASSUMED]` - Inferred, not explicit
- `[TESTED]` - Manually tested
- `[PROVEN]` - Multiple independent sources
- `[COMMUNITY]` - Community sources (cite ID)

## Quality Pipeline (VCRIV)

`verify → critique → reconcile → implement → verify`

- **V** - `/verify` formal correctness
- **C** - `/critique` find gaps, produces `*_REVIEW.md`
- **R** - `/reconcile` prioritize findings
- **I** - `/implement` apply findings, delete `*_REVIEW.md`
- **V** - Final verify

**Four mandatory checkpoints:**
1. Preflight deliverables (STRUT, SOURCES, PromptDecomposition)
2. Planning deliverables (TOC, template, TASKS)
3. Each research output (per granularity rules)
4. Complete research set ex-post

**Granularity** (scope-based): NARROW: per topic file | FOCUSED/EXPLORATORY: per dimension | Final VCRIV on synthesis document

**Termination**: Max 2 cycles per checkpoint, then [CONSULT].

## Inline Citations

Critical conclusions MUST have: `[VERIFICATION_LABEL] (SOURCE_ID | URL or filename)`

Example: `[VERIFIED] (GRPH-SC-MSFT-RATELMT | https://learn.microsoft.com/graph/throttling)`

Referenced files MUST exist in `_SOURCES/` subfolder.

## Domain Profiles

Read one per session based on Q6:
- [DOMAIN_SOFTWARE.md](DOMAIN_SOFTWARE.md) - APIs, frameworks, libraries
- [DOMAIN_MARKET_INTEL.md](DOMAIN_MARKET_INTEL.md) - Companies, financials
- [DOMAIN_DOCUMENT_INTEL.md](DOMAIN_DOCUMENT_INTEL.md) - Table extraction
- [DOMAIN_LEGAL.md](DOMAIN_LEGAL.md) - Legislation, case law
- [DOMAIN_DEFAULT.md](DOMAIN_DEFAULT.md) - Generic fallback

## Output Format

INFO document: Research Question, Strategy & Domain (with rationale), Key Findings, Detailed Analysis, Limitations, Sources (with verification labels), Recommendations

MEPI uses its own output format (see RESEARCH_STRATEGY_MEPI.md) with Comparison and Recommendation sections.

## Planning Structure

**STRUT** (high-level, REQUIRED): Phases, objectives, deliverables, transitions, time log. File: `STRUT_[TOPIC].md`

**TASKS** (low-level, Phase 2): Flat task list with durations and done-when criteria. File: `TASKS.md`

## Reference Files

- [RESEARCH_TOOLS.md](RESEARCH_TOOLS.md) - Tools, source processing, configuration
- [RESEARCH_TOC_TEMPLATE.md](RESEARCH_TOC_TEMPLATE.md) - TOC structure
- [RESEARCH_CREATE_TOC.md](RESEARCH_CREATE_TOC.md) - TOC creation workflow

**File naming**: `__[SUBJECT]_TOC.md`, `__[SUBJECT]_SOURCES.md`, `_INFO_[SUBJECT]-IN[XX]_[TOPIC].md`

**Source ID format**: `[SUBJECT]-SC-[SOURCE]-[DOCNAME]`