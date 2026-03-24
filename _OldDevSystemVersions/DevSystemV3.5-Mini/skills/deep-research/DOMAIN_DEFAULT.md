# Domain Profile: DEFAULT

Generic profile. Use when no specific domain profile matches (SOFTWARE, MARKET_INTEL, DOCUMENT_INTEL, LEGAL).

## When to Use

- Topic doesn't fit existing profiles
- Multi-domain or personal/lifestyle topics
- General knowledge synthesis
- Open-ended exploratory research

## Source Tiers

1. Tier 1 - Official/Authoritative: Government, legislation, official publications, academic papers
2. Tier 2 - Professional: Industry reports, established news, professional associations
3. Tier 3 - Expert: Technical blogs by recognized experts, conference talks
4. Tier 4 - Community Quality: Stack Overflow (high votes), GitHub issues (many reactions), Reddit (top posts)
5. Tier 5 - Community General: Forums, Discord, personal blogs, social media

Verify Tier 4-5 claims against Tier 1-3 when possible. Label Tier 4-5 with `[COMMUNITY]`.

## Document Handling

- PDFs: Full transcription via `@skills:pdf-tools` + `@skills:llm-transcription`
- Web pages: `read_url_content` or Playwright MCP
- Media: Podcast/video transcription when relevant
- Large documents: Process completely (no agent-selected chunks)

## Available QA Tools

### Source Collection
- `search_web`, `read_url_content`, `Playwright MCP`, `Playwriter MCP` (authenticated)

### Document Processing
- `@skills:pdf-tools` - PDF to JPG (`convert-pdf-to-jpg.py`)
- `@skills:llm-transcription` - Image/PDF to markdown
- Full transcription required - every page

### Media Processing
- Podcast/video/audio transcription via web tools, APIs, or Whisper

### Source Handling
- Primary sources: Download, store in `_SOURCES/`
- Source IDs: `[TOPIC]-SC-[SOURCE]-[DOCNAME]`
- Secondary sources: Cite with `[COMMUNITY]` label
- All sources MUST include `Accessed: YYYY-MM-DD`

## Template Additions

- Limitations and Known Issues - What we couldn't verify, caveats
- Recommendations - Clear actionable guidance
- Source Access Dates - When each source was accessed

## Quality Criteria

- Critical claims have inline citations with verification labels
- Legal/financial/medical claims MUST have Tier 1-2 citations
- All sources have access dates
- Limitations section populated honestly
- Recommendations section exists
- Tier 4-5 sources labeled `[COMMUNITY]` with limitations noted

## Effort Validation

- Decomposition MUST estimate minimum research hours
- Actual time < 50% of estimate → agent MUST justify or expand
- Goal: outperform 16 hours of human research for EXPLORATORY scope

## VCRIV Pipeline

Runs per scope-based granularity:
`V` `/verify` → `C` `/critique` (produces `_REVIEW.md`) → `R` `/reconcile` → `I` implement (delete `_REVIEW.md`) → `V` `/verify` (final)

## MUST-NOT-FORGET

- Run full VCRIV: `/verify` -> `/critique` -> `/reconcile` -> implement -> `/verify`
- NARROW (1 dim): VCRIV per topic file
- FOCUSED/EXPLORATORY (2+ dim): VCRIV per dimension
- Final VCRIV on synthesis document