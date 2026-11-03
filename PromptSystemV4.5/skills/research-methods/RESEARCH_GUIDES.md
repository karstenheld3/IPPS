# Research Orchestration Guide

Read BEFORE selecting a research tier, executing research with `/research`, `/deep-research`, or `/research-program`, or packaging sources with `/bundle`.

## 1. Purpose and Reader Outcome

After reading this GUIDE, you can select the appropriate execution tier for any research mandate, define calibrated scopes, choose between curated (MEPI) and exhaustive (MCPI) strategies, route domain areas and entity profiles, enforce prompt load boundaries, architect scalable multi-approach programs without context overflow, and configure knowledge bundles.

## 2. Research Decisions in Working Order

Executing research follows seven core strategic decisions in the sequence below.

### Decision 1: Execution Tier Selection (Tier 1 vs Tier 2 vs Tier 3)

- **Question**: Which execution depth and time envelope governs the research task?
- **Options**:
  - Tier 1 (Single-turn research, `/research`): 2-10 minutes. One conversation turn producing one standalone `_INFO_*.md` document. No STRUT, no prompt files, no topic folders. Best for factual verification, single questions, or rapid due diligence.
  - Tier 2 (Planned deep research, `/deep-research`): 10-60 minutes. Single `T##_` topic folder containing `__STRUT_[TOPIC].md` and one compiled PROMPTS file (3-10 prompts). Runs headlessly without pause; produces full C1 Knowledge Library (Summary, Sources, topic files, `_SOURCES/`).
  - Tier 3 (Program research, `/research-program`): 2-20 hours. Multi-approach program (1-4 approaches as `T##_` folders). Governed by session STRUT and 2-8 compiled PROMPTS files (10-35 prompts total). Pauses for human review between prompt files. Ends with session-level program Summary comparing approaches.
- **Criterion**: Base choice strictly on prompt scope and time budget:
  - If question is narrow (<1 hour investigation needed) -> Tier 1.
  - If single focused topic requires multi-source depth and topic decomposition -> Tier 2.
  - If goal requires evaluating competing approaches, multi-faceted programs, or spans 2+ hours -> Tier 3.
- **Rule Reference**: Section 2.3, NFR-02, DRSYNART-FR-02.

### Decision 2: Research Scope Definition

- **Question**: How broad is the dimensional reach of the research question?
- **Options**:
  - FOCUSED: 1-4 dimensions (e.g. technical, financial, operational). Deep inquiry into a bounded problem or specific decision.
  - COMPARATIVE: 2-4 explicit approaches or architectural options evaluated across shared dimensions.
  - EXPLORATORY: 5-9 dimensions (e.g. legal, strategic, organizational, administrative, cultural). Broad landscape mapping of an unfamiliar domain.
- **Criterion**: Scope determines decomposition depth. Narrow questions stay in 1 dimension. Decision trade-offs use COMPARATIVE. Strategic or high-risk initiatives use EXPLORATORY.
- **Rule Reference**: SKILL.md Prompt Decomposition Q2.

### Decision 3: Strategy Selection (MEPI vs MCPI)

- **Question**: Does the user need the best-evidenced recommendation or an exhaustive inventory?
- **Options**:
  - MEPI (Most Executable Point of Information): curated best options per topic, actionable comparisons, and explicit recommendations. Time-constrained, reversible decisions. Point to `RESEARCH_STRATEGY_MEPI.md`.
  - MCPI (Most Complete Point of Information): exhaustive coverage, documenting every viable option and edge case. High-stakes (legal, financial, medical compliance), foundational archives. Point to `RESEARCH_STRATEGY_MCPI.md`.
- **Criterion**: Default to MEPI for operational and technical decisions. Use MCPI only when completeness is explicitly requested or when omission introduces catastrophic compliance risk.
- **Rule Reference**: SKILL.md Strategy Selection.

### Decision 4: Domain Area and Entity Profile Selection

- **Question**: Which domain rules or entity templates apply to the subject?
- **Options**:
  - Domain Areas (`research_areas/`):
    - `software/DOMAIN_SOFTWARE.md`: APIs, SDKs, developer tooling, libraries.
    - `market-intel/DOMAIN_MARKET_INTEL.md`: Company financials, market share, competitive intelligence.
    - `legal/DOMAIN_LEGAL.md`: Statutes, regulations, administrative law, case law.
    - `default/DOMAIN_DEFAULT.md`: General topics not matching specialized areas.
  - Entity Profiles (`research_profiles/`):
    - `PERSONAL_PROFILE_TEMPLATE.md` + `_RULES.md`: People, biographies, leadership diligence.
    - `COMPANY_PROFILE_TEMPLATE.md` + `_RULES.md`: Commercial corporations, startups, vendors.
    - `ORGA_PROFILE_TEMPLATE.md` + `_RULES.md`: Universities, standards bodies, NGOs, agencies.
    - `NETWORK_PROFILE_TEMPLATE.md` + `_RULES.md`: Professional networks, inner circles, clusters.
- **Criterion**: If research subject is an entity, load template from `research_profiles/`. For thematic research, load area profile from `research_areas/`.
- **Rule Reference**: DRSYNART-DD-05.

### Decision 5: Discovery Platforms and Source Tiers

- **Question**: What platforms index the target entities and how are sources vetted?
- **Options**:
  - Systematic platform testing: identify candidate platforms (e.g. Google Scholar, SEC EDGAR, Handelsregister, GitHub), classify access level (FREE, PAID, PARTIAL), and query FREE and PARTIAL platforms.
  - Source tier classification: Tier 1 (official legislation, specifications, primary PDFs) > Tier 2 (official documentation, filings) > Tier 3 (maintainer blogs, expert conference talks) > Tier 4-5 (reputable blogs, Stack Overflow) > Tier 6-8 (community forums, Discord, Reddit, labeled `[COMMUNITY]`).
- **Criterion**: Enforce tier thresholds: critical legal, financial, or technical claims require Tier 1-3 primary sources. Community sources provide gotchas and limitations but never establish primary facts without corroboration.
- **Rule Reference**: SKILL.md Prompt Decomposition Q7, Source Hierarchy.

### Decision 6: Load Unit per Prompt

- **Question**: How is research workload partitioned into discrete prompt steps?
- **Options**:
  - Guarded profile unit: at most 4 numbered items, 2 content files changed, 2 topic files loaded per prompt.
  - Monolithic prompt: bundling research, transcription, and multi-file drafting into a single turn.
- **Criterion**: Always enforce the guarded profile. Overloaded prompts lead to truncated outputs and hallucinated sources. Every implementation prompt must be followed by a separate `/verify` + `/fix` checkpoint prompt.
- **Rule Reference**: DRSYNART-NFR-01, DRSYNART-NFR-05.

### Decision 7: Program Structure and Scaling (Tier 3 Only)

- **Question**: How is a multi-approach research program structured without exceeding model limits?
- **Options**:
  - Capped multi-approach layout: 1 session STRUT with pre-research assumptions (A1..An), 1-4 approach subfolders (`T01_`, `T02_`), each governed by 1-2 prompt files. Session Summary synthesizes Approach Comparison.
  - Unbounded single-folder crawl: accumulating dozens of topic files in one flat folder.
- **Criterion**: Never exceed NFR-01 caps: max 8 prompt files, 35 prompts total including checkpoints, 12 deliverables, 3 VCRIV gates, and at most 4 approaches. If mandate exceeds caps, refuse start and split into sequential programs. Extend programs only by adding a new `T##_` folder or prompt file, never by editing executed prompts.
- **Rule Reference**: DRSYNART-NFR-01, Section 10.5.

### Decision 8: Per-Dimension Topic File Structure and Summary Synthesis

- **Question**: How are individual topic findings organized and synthesized into the Knowledge Library?
- **Options**:
  - Standard topic file structure: Header block with version/date scope, Summary (5-10 sentences), Key Facts with `[VERIFIED]` labels, Detailed Findings, Limitations and Known Issues, Gotchas and Quirks, and GRUC-Implications section.
  - Summary cross-document synthesis: `_INFO_[TOPIC]-01_Summary.md` synthesizes findings across all topic files, answering each research question with explicit topic-file and source citations, rather than merely concatenating topic intros.
- **Criterion**: Every topic file must include a section on implications for downstream GRUC assets (how findings affect rules, templates, or workflows). The Summary must provide substantive cross-topic synthesis, explicit trade-offs, and an actionable decision matrix.
- **Rule Reference**: RESEARCH_SUMMARY_RULES.md, DRSYNART-FR-10.

### Decision 9: Knowledge Bundle Configuration (Optional `/bundle`)

- **Question**: When and how are research assets packaged into an IPPS bundle?
- **Options**:
  - IPPSKBNDL-SP01 bundle (`_BUNDLE_[TOPIC].md`): compiles C1 summary, sources, and full Markdown transcriptions into a portable standalone file using `@skills:llm-tools`.
  - Omitted bundle: downstream layers read C1 files directly from the research folder.
- **Criterion**: `/bundle` is optional; Layer 2 and Layer 3 operate directly on C1 folders without it. Create a bundle only when exporting knowledge across repositories or packaging for offline LLM consumption.
- **Rule Reference**: DRSYNART-DD-03, DRSYNART-DD-31.

## 3. Robustness Rules (MUST-NOT-FORGET)

- **Cascade Law Domain Ban**: Research on German legal statutes at `gesetze-im-internet.de` MUST use Playwright MCP. Tools `search_web` and `read_url_content` crash the conversation on this domain.
- **Google Search Extraction Principle**: Use Playwright to search google.com for PDF whitepapers (`filetype:pdf`) and primary docs. Google is for URL discovery only: never extract text from AI Overviews, Featured Snippets, Knowledge Panels, or People Also Ask. Always click through to the source website.
- **Source Registration**: Every cited source must be registered with an ID in `_INFO_[TOPIC]-02_Sources.md` before citation.
- **Source Retention**: Never delete checked sources; document checked URLs with minimal findings to prevent redundant searches.

## 4. Named Failure Modes

- **Snippet-Only Sourcing**: Relying on search engine result snippets or meta tags rather than reading full source pages.
  - *Prevention*: Always use `read_url_content` or Playwright MCP to inspect primary source text directly.
- **Unregistered Source**: Citing an ad-hoc URL in topic files without logging an entry in `_INFO_[TOPIC]-02_Sources.md`.
  - *Prevention*: Register source ID immediately upon URL discovery.
- **Topic File Without GRUC Implications**: Authoring empirical findings without explaining their architectural consequence for downstream rules or templates.
  - *Prevention*: Include a dedicated implications section in every topic file.
- **Summary That Restates Instead of Synthesizes**: Authoring a Summary that merely copies opening paragraphs from topic files.
  - *Prevention*: Write an overarching comparative narrative answering core research questions directly with cross-topic citations.
- **Program Above Caps**: Planning a Tier 3 program with >4 approaches, >8 prompt files, or >35 prompts.
  - *Prevention*: Run preflight cap check in Phase 1; refuse execution and partition into parts if caps are exceeded.
- **Executed Prompt Edited**: Editing prompts that have already run to extend scope.
  - *Prevention*: Append new prompt files or approach folders; executed prompts are immutable history.

## 5. Quality Heuristics

1. **Primary Evidence Dominance**: Primary documentation, specifications, and whitepapers (Tiers 1-3) must substantiate all core technical, architectural, or legal claims.
2. **Substantive Synthesis**: Summary documents must compare dimensions across topics and resolve contradictions rather than providing isolated topical recaps.
3. **Strict Load Partitioning**: Respect model context envelopes by strictly observing the guarded prompt profile (<=4 items, <=2 content files).
4. **Complete Traceability**: Every conclusion in topic and summary files links directly to registered source IDs in `_INFO_[TOPIC]-02_Sources.md`.
5. **Immutable Execution History**: Once a prompt file has completed, its contents are immutable; subsequent extensions run as new prompt files or topic folders.

## 6. Self-Review Questions

1. Does the selected tier match the time envelope and decision stakes (Tier 1 <10m, Tier 2 <1h, Tier 3 <20h)?
2. Is the strategy (MEPI vs MCPI) chosen based on user need (curated recommendation vs exhaustive audit)?
3. Are all entity profiles sourced from `research_profiles/` and domain guides from `research_areas/`?
4. Were discovery platforms tested and classified before source collection began?
5. Does every prompt in the plan conform to the guarded profile (<=4 items, <=2 content files)?
6. Does the Tier 3 program plan strictly respect NFR-01 caps (<=4 approaches, <=8 prompt files, <=35 prompts)?
7. Does each topic file include architectural implications and does the Summary synthesize rather than restate?
8. Were all Google search results inspected on their primary websites rather than scraped from snippets?

## 7. Annotated Exemplar Links

- `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-01_Summary.md [DRSYNART-RSRCHMTHD-IN01]`: Demonstrates cross-document qualitative synthesis, method chaining, trade-off matrices, and research stats metadata.
- `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-02_Sources.md [DRSYNART-RSRCHMTHD-IN02]`: Demonstrates exhaustive source registry with tier classification, access dates, and SOCAS evaluation flags.
