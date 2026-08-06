# INFO: How to Create Auditable Research Summaries

**Doc ID**: AUDITCITE-IN01
**Goal**: Define the citation and source-linking standard for research summaries targeting regulated businesses (100% audit chain)
**Timeline**: Created 2026-08-05, Updated 1 time (2026-08-05 - 2026-08-05)

## Summary

- Every factual claim must trace to a source with full URL, publication date, and archived copy
- Three-layer audit architecture: inline citation (Layer 1) → source registry (Layer 2) → source archive (Layer 3)
- Inline format: `(SOURCE-ID | https://exact-url YYYY[-MM[-DD]])` on first mention; `(SOURCE-ID YYYY[-MM[-DD]])` on subsequent
- Deep-research multi-file output MUST produce `_Sources.md` as separate file; single-file output MUST include Sources section
- Source registry MUST include: Published date, Data vintage, Accessed date, Archived filename, Tier classification
- Bare source IDs without URL and year are non-compliant - they fail the "can an auditor verify this in 30 seconds?" test
- Citation = in-text source marker; Quotation = verbatim source text + citation. Quotations required for editorial conclusions and foundational arguments

## Table of Contents

1. [Why This Exists](#1-why-this-exists)
2. [What It Must Guarantee](#2-what-it-must-guarantee)
3. [The Three-Layer Architecture](#3-the-three-layer-architecture)
4. [Layer 1: Inline Citations](#4-layer-1-inline-citations)
5. [Layer 2: Source Registry](#5-layer-2-source-registry)
6. [Layer 3: Source Archive](#6-layer-3-source-archive)
7. [Multi-File vs Single-File Output](#7-multi-file-vs-single-file-output)
8. [Real-World Examples](#8-real-world-examples)
9. [Compliance Checklist](#9-compliance-checklist)
10. [When to Apply This Standard](#10-when-to-apply-this-standard)
11. [Document History](#11-document-history)

## 1. Why This Exists

### 1.1 The Problem

Research summaries inform business decisions in regulated industries (financial services, insurance, compliance). When a claim like "Germany Regulatory Technology (RegTech) market is USD 5B" appears in an investor deck or compliance filing:

- **An auditor asks**: Where does this number come from? When was it measured? Is it still current?
- **A regulator asks**: Can you demonstrate the provenance of this assertion?
- **An investor asks**: Is this 2024 data or 2026 data? Was the source credible?

If the research summary only says `(REGCMPLSW-SC-RSMKT-DERGM)` - the auditor must:
1. Find the Sources file
2. Look up the ID
3. Find the URL
4. Check if the URL still works
5. Determine the data vintage

This is a **5-step verification process** for a single claim. In a document with 50+ claims, this is unacceptable for regulated contexts.

### 1.2 The Solution

Make every claim **traceable to source at point of use**. An auditor reading a citation should instantly know:
- **What source** (unique ID for registry lookup)
- **Where exactly** (clickable URL with `https://` on first mention; ID for registry lookup thereafter)
- **When published** (publication date of the source)

One citation. Three questions answered. Zero ambiguity.

### 1.3 Who This Serves

- **Compliance officers** verifying claims in regulatory filings
- **Investors** performing due diligence on market data
- **Auditors** tracing assertions to primary sources
- **Future researchers** assessing whether data is still current
- **The author** defending claims months later when context is forgotten

### 1.4 Terminology

- **Source**: The original document, article, report, or dataset where information originates
- **Source ID**: Unique identifier for a source (e.g., `AIAUTMFIN-SC-KPMG-BKPLS1`)
- **Citation**: In-text marker linking a claim to its source. Format: `(SOURCE-ID | https://url YYYY)`. Does not reproduce source text.
- **Quotation**: Verbatim reproduction of source text, followed by a citation. Allows the reader to judge whether the author's interpretation is warranted.
- **Reference**: Full bibliographic entry in the Source Registry (Layer 2) - includes metadata, URL, dates, tier, archived filename.
- **Source Registry**: Structured file (`_Sources.md` or Sources section) containing all references for a document.
- **Source Archive**: Local folder (`_SOURCES/`) containing permanent copies of sources (transcribed markdown, downloaded PDFs).
- **Publication date**: When the source was released. Always appears in citations.
- **Data vintage**: What time period the data describes. Stated in prose when it differs significantly from publication date.

## 2. What It Must Guarantee

### 2.1 The Audit Chain (Non-Negotiable)

```
CLAIM in document
  │
  ├─ Layer 1: Inline citation visible at point of use
  │    → Source identity (SOURCE-ID)
  │    → Exact URL (https://...)
  │    → Publication date (as precise as known)
  │
  ├─ Layer 2: Source registry entry
  │    → Full metadata (published, accessed, type, tier)
  │    → Data vintage description (what period data describes)
  │    → Key data points extracted
  │    → Verification label
  │
  └─ Layer 3: Archived source copy
       → Transcribed or downloaded content
       → Permanent, URL-independent
       → Survives link rot
```

### 2.2 Five Guarantees

1. **Traceability**: Every quantitative claim has a source ID
2. **Accessibility**: Every source ID resolves to a clickable URL (first mention)
3. **Temporality**: Every citation includes publication date; prose states data vintage when it differs
4. **Permanence**: Every source has a local archived copy (survives link rot)
5. **Verifiability**: Any person can verify any claim within 30 seconds using only the document and its companion files

### 2.3 What Breaks the Chain (Failures)

- Bare source ID without URL: `(AIAUTMFIN-SC-KPMG-BKPLS1)` → auditor cannot verify without opening a separate file
- Domain without scheme: `(SOURCE-ID | kpmg.com)` → not clickable, violates URL conventions
- Citation without year: `(SOURCE-ID | https://kpmg.com/report)` → data currency unknown
- Informal attribution: "according to KPMG" → which KPMG report? Which year? Which page?
- Source not archived: URL goes dead → claim becomes unverifiable

## 3. The Three-Layer Architecture

```
┌───────────────────────────────────────────────────────────┐
│ Layer 1: INLINE CITATION (in Summary / Topic files)       │
│                                                           │
│ Visible at point of use. Answers: What? Where? When?      │
│ Format: (SOURCE-ID | https://url PUB-DATE)                │
└───────────────────────────┬───────────────────────────────┘
                            │ SOURCE-ID lookup
┌───────────────────────────v───────────────────────────────┐
│ Layer 2: SOURCE REGISTRY (_Sources.md or Sources section) │
│                                                           │
│ Full metadata. Answers: Published when? Accessed when?    │
│ What tier? What was extracted? Verification status?       │
└───────────────────────────┬───────────────────────────────┘
                            │ Archived filename
┌───────────────────────────v───────────────────────────────┐
│ Layer 3: SOURCE ARCHIVE (_SOURCES/ folder)                │
│                                                           │
│ Permanent copy. Survives link rot. Full source content.   │
│ Transcribed PDFs, saved web pages, downloaded reports.    │
└───────────────────────────────────────────────────────────┘
```

## 4. Layer 1: Inline Citations

### 4.1 Format Specification

**Web sources** (URL is the locator):
```
FIRST MENTION:
  (SOURCE-ID | https://exact-url.com/path/to/article 2026-03-15)

SUBSEQUENT:
  (SOURCE-ID 2026-03-15)
```

**Document sources** (PDF, Google Doc, Microsoft Office - filename + URL + page):
```
FIRST MENTION:
  (SOURCE-ID | `filename.pdf` https://original-url.com/report.pdf p.42 2026-03-15)
  (SOURCE-ID | `filename.docx` https://docs.google.com/document/d/abc123 p.7 2026-03)

SUBSEQUENT:
  (SOURCE-ID p.42 2026-Q1)
```

**Multiple sources:**
```
FIRST MENTION:
  (SOURCE-ID-A | https://url-a.com 2026-03, SOURCE-ID-B | `filename.pdf` https://url-b.com p.7 2025-11)

SUBSEQUENT:
  (SOURCE-ID-A 2026-03, SOURCE-ID-B p.7 2025-11)
```

**Element order** (left to right, after `|`):
1. `filename.ext` - local file in backticks (documents only, omit for web sources)
2. `https://...` - full original URL (always, may become unavailable)
3. `p.NN` or `p.NN-MM` - page number or range (documents only, when known from transcription)
4. Publication date - as precise as known (see Date Precision below)

**DATE in the citation = PUBLICATION DATE** (when the source was released).

**DATA VINTAGE goes in the prose**, not in the citation:
- If data is from the same period as publication: no extra note needed
- If data is significantly older: state it in the claim text itself

### 4.2 Publication Date vs Data Vintage

The date in the citation is always the **publication date** - when the source was released.

If the underlying data is from a significantly different period (e.g., a 2026 report using 2024 data), the **prose text must state this explicitly**:

**Data matches publication (no extra note needed):**
```markdown
82% of firms report AI adoption (SOURCE-ID | https://url.com/survey 2026-Q1)
```
Reader infers: Q1 2026 survey, Q1 2026 data. Correct.

**Data is older than publication (state in prose):**
```markdown
Based on FY2024 data, the market reached $8.29B (SOURCE-ID | `filename.pdf` https://url.com/report.pdf p.12 2026-01)
```
Reader sees: "FY2024 data" in the text + source published Jan 2026. No ambiguity.

**BAD (silent staleness):**
```markdown
The market reached $8.29B (SOURCE-ID | https://url.com/report.pdf 2026-01)
```
Reader assumes: $8.29B is 2026 data. But it's actually FY2024. Misleading.

**Rule**: When data vintage differs from publication year, the claim text MUST include a temporal qualifier ("FY2024 data", "based on 2023 figures", "as of Q3 2024"). The citation date alone is not sufficient to communicate data staleness.

### 4.3 Date Precision

Use the most precise publication date available:
- `2026-03-15` - exact date known (best)
- `2026-03` - month known
- `2026-Q1` - quarter known but not month
- `2026-H1` - half-year known (for semi-annual reports)
- `2026` - only year known (last resort for undated sources)

Supported formats: `YYYY-MM-DD`, `YYYY-MM`, `YYYY-QN`, `YYYY-HN`, `YYYY`

### 4.4 First-Mention Rule

Each unique SOURCE-ID gets its full URL **once** on first appearance in the document. All subsequent uses omit the URL (the reader already saw it or can search upward). This keeps paragraphs with repeated citations readable.

### 4.5 Citation vs Quotation

Standard terminology (aligned with APA/Harvard/Chicago conventions):

- **Citation**: In-text marker linking a claim to its source. The reader trusts the author's interpretation.
  Format: `(SOURCE-ID | https://url YYYY)`
- **Quotation**: Reproduces source text verbatim, followed by a citation. The reader judges the interpretation independently.
  Format: blockquote with verbatim text + citation on attribution line
- **Reference**: Full bibliographic entry in the Source Registry (Layer 2). Not visible at point of use - the reader looks it up via the SOURCE-ID from a citation.

A quotation always includes a citation. A citation does not include verbatim text. Both point to a reference via SOURCE-ID.

**When a quotation is required** (citation alone is insufficient):

- Strong editorial conclusions ("the market WILL consolidate", "this approach is superior")
- Foundational arguments that other conclusions build upon
- Claims where the author's interpretation could reasonably be disputed
- Contradictions between sources (quote both so the reader sees the conflict)
- Quantitative claims that seem surprising or counterintuitive

**When a citation is sufficient:**

- Widely accepted facts restated from a source
- Data points where the number speaks for itself ("revenue was $8.29B")
- Claims supported by multiple converging sources (consensus)

**Quotation format:**

```markdown
> "Exact verbatim quote from the source, preserving original wording."
> -- (SOURCE-ID | https://url.com/report p.42 YYYY-MM)

Therefore, [author's conclusion based on the quote].
```

**Multiple quotations supporting one argument:**

```markdown
> "First verbatim quote establishing premise A."
> -- (SOURCE-ID-A | https://url-a.com p.12 2026-Q1)

> "Second verbatim quote establishing premise B."
> -- (SOURCE-ID-B | `report.pdf` https://url-b.com/report.pdf p.7 2025-11)

Combining A and B: [author's synthesis or conclusion].
```

**GOOD (quotation for editorial conclusion):**

```markdown
> "Banks that deployed AI agents in Q1 2026 reduced compliance review time by 47%
> while maintaining zero regulatory findings."
> -- (AIAUTMFIN-SC-KPMG-BKPLS1 | https://kpmg.com/us/en/articles/banking-leaders-pulse-survey-q1-2026.html p.23 2026-Q1)

This demonstrates that the compliance-speed tradeoff is a false dichotomy -
early movers achieved both simultaneously.
```

The reader can verify: Does the KPMG source actually say "47% reduction" and "zero regulatory findings"? Does the editorial conclusion ("false dichotomy") logically follow?

**BAD (editorial conclusion with citation only - no quotation):**

```markdown
The compliance-speed tradeoff is a false dichotomy - early movers achieved both
simultaneously (AIAUTMFIN-SC-KPMG-BKPLS1 | https://kpmg.com/... 2026-Q1).
```

The reader cannot judge whether the source supports the "false dichotomy" interpretation without opening the source and reading page 23.

**Rule**: When the author draws a conclusion that goes BEYOND restating data (interpretation, editorial judgment, strategic implication), the source text must be quoted verbatim so the reader can independently assess whether the conclusion is warranted.

## 5. Layer 2: Source Registry

### 5.1 Required Fields

```
### SOURCE-ID
- **Title**: [Report/article/paper name]
- **URL**: https://exact-url.com/full/path/to/source
- **Published**: YYYY-MM-DD (or YYYY-MM, or YYYY if only year known)
- **Data vintage**: [What period the data describes, e.g., "FY2024", "Q1 2026 survey", "2024 calendar year"]
- **Accessed**: YYYY-MM-DD
- **Archived**: `_SOURCES/[filename.md or filename.pdf]`
- **Type**: [Survey Report | Market Report | Press Release | Academic Paper | Official Document | Blog/Analysis | Vendor Whitepaper]
- **Tier**: [1 = Official/Primary | 2 = Consulting/Vendor | 3 = Community/Analyst]
- **Key Data Points**: [2-5 bullet points of what was extracted]
- **[VERIFICATION LABEL]**
```

### 5.2 Tier Classification

- **Tier 1**: Official/primary sources (regulators, central banks, official statistics, peer-reviewed research)
- **Tier 2**: Consulting/vendor (KPMG, McKinsey, Gartner, Deloitte, vendor reports with methodology)
- **Tier 3**: Community/analyst (blog posts, opinion pieces, community surveys, individual analysts)

### 5.3 Published vs Accessed vs Data Vintage

Three distinct temporal dimensions:

- **Published**: When the source document was released to the public
- **Accessed**: When we retrieved it (important for link verification and versioning)
- **Data vintage**: What time period the DATA inside describes (critical for currency assessment)

Example: A KPMG report published 2026-03-15, accessed 2026-07-18, containing survey data collected in Jan-Feb 2026. The publication date `2026-03-15` goes in the inline citation. If the claim text uses a figure based on the Jan-Feb survey period, the prose states "Based on Q1 2026 survey data, ...".

## 6. Layer 3: Source Archive

### 6.1 Purpose

URLs break. Paywalls appear. Content gets updated without notice. The archive guarantees permanent verifiability regardless of internet state.

### 6.2 Structure

**`_DOWNLOADS_gitignore/`** - Original artifacts as-downloaded. Untouched originals. Gitignored (not committed).

**`_SOURCES/`** - Transcribed content only (`.md` files). Git-tracked. Human-readable. The verification layer.

```
[Research Folder]/
├─ _SOURCES/                              ← Transcribed content (git-tracked)
│   ├─ kpmg-banking-leaders-q1-2026.md        ← Transcribed from PDF
│   ├─ gartner-hype-cycle-agentic-2026.md     ← Transcribed from paywall summary
│   ├─ ecb-safe-survey-2025.md                ← Transcribed from PDF
│   └─ svb-state-of-markets-2025.md           ← Transcribed from web page
├─ _DOWNLOADS_gitignore/                  ← Original binaries (gitignored)
│   ├─ kpmg-report-original.pdf               ← Downloaded PDF
│   ├─ ecb-safe-full-report.pdf               ← Downloaded PDF
│   ├─ chart-ai-market-growth.jpg             ← Screenshot
│   └─ interview-cto-recording.mp3            ← Audio recording
```

### 6.3 Rules

**File organization:**
- Every source in the registry MUST have a corresponding transcribed `.md` file in `_SOURCES/`
- `_SOURCES/` contains ONLY `.md` files (transcribed content). No binaries (PDF, JPG, MP3, etc.)
- `_DOWNLOADS_gitignore/` contains originals with original filenames (PDFs, images, screenshots, audio)
- Archive filename convention: `[source-shortname]-[topic]-[year].md` (lowercase, hyphens)

**Transcription by source type:**
- PDFs: download to `_DOWNLOADS_gitignore/`, transcribe to `_SOURCES/` as `.md`
- Web pages: transcribe key content to `_SOURCES/` as `.md` (preserve all data, tables, figures)
- Images/screenshots: download to `_DOWNLOADS_gitignore/`, transcribe visible content to `_SOURCES/` as `.md`
- Audio: download to `_DOWNLOADS_gitignore/`, transcribe speech to `_SOURCES/` as `.md`
- Paywalled sources: archive the publicly available summary/excerpt; note paywall limitation in registry

**Documentation requirements:**
- After transcription, the source registry entry MUST include the transcribed markdown filename and relative path in the **Archived** field: `_SOURCES/kpmg-banking-leaders-q1-2026.md`
- File paths MUST always be in backticks (handles spaces, ensures visual distinction): `_SOURCES/ecb safe survey 2025.md`

### 6.4 Page Number Handling

Page numbers apply to **documents** (PDF, Google Doc, Word, etc.). Web articles have no pages - the URL is sufficient.

**Page locator format**: `p.NN` or `p.NN-MM` (placed after URL, before dates):
```
(SOURCE-ID | `banking-pulse-q1-2026.pdf` https://kpmg.com/reports/pulse.pdf p.42 2026-Q1)
(SOURCE-ID | `strategy-deck.pptx` https://docs.google.com/presentation/d/xyz p.12 2026-03)
```

**Page locator variants:**
- `p.42` - single page
- `p.42-45` - page range
- `p.42,p.67` - multiple non-contiguous pages

**Requirement**: Page numbers SHOULD have a corresponding markdown transcription in `_SOURCES/` for archival verification. Page numbers MAY be cited from direct observation of the source document; mark the source registry entry as `Archived: pending transcription` until transcription is complete.

**In the source registry**, Key Data Points MUST reference page numbers:
```
- **Key Data Points**:
  - p.12: $8.29B (2025) market size
  - p.15-17: CAGR methodology and regional breakdown
  - p.42: Germany-specific segment ($5B estimate)
  - Fig.3 (p.28): Growth trajectory chart
```

**In the transcribed archive** (`_SOURCES/filename.md`), headings map to pages:
```markdown
## Page 12 - Market Size Overview

The global AI agents market reached $8.29B in 2025...

## Page 15-17 - Methodology and Regional Breakdown
...
```

This creates a verifiable chain: inline `p.42` → registry Key Data Points `p.42` → transcription heading `## Page 42 - ...`.

## 7. Multi-File vs Single-File Output

### 7.1 Multi-File Output (3+ topic files)

When research produces multiple topic files, the source registry is a **dedicated file**:

```
[Topic Folder]/
├─ _INFO_[TOPIC]-01_Summary.md         ← References sources by ID
├─ _INFO_[TOPIC]-02_Sources.md         ← FULL SOURCE REGISTRY (Layer 2)
├─ _INFO_[TOPIC]-03_TopicFile.md       ← References sources by ID
├─ _INFO_[TOPIC]-04_TopicFile.md
├─ _SOURCES/                           ← Layer 3 archive
└─ _DOWNLOADS_gitignore/               ← Raw downloads
```

The `_Sources.md` file is **mandatory** for multi-file research output. It MUST contain ALL sources referenced across all topic files and the summary. No source ID may appear in any file without a corresponding entry in `_Sources.md`.

### 7.2 Single-File Output (standalone INFO documents)

When research is a single document, the source registry is a **section within the document**:

```markdown
## Sources

### Tier 1: Primary Sources

- **TOPIC-IN01-SC-SITE-PAGE**
  - Title: [Name]
  - URL: https://exact-url.com
  - Published: YYYY-MM-DD
  - Data vintage: [period]
  - Accessed: YYYY-MM-DD
  - Key Data: [what was extracted]
  -

### Tier 2: Consulting/Vendor
...
```

### 7.3 Decision Criteria

- 5+ sources → use separate `_Sources.md` file
- <5 sources → Sources section within the document is acceptable
- Multiple topic files → ALWAYS separate `_Sources.md` (mandatory per RS-02)

## 8. Real-World Examples

### GOOD: Full Audit Chain (B2BAGTMKT Per-Topic Key Findings)

```markdown
- Total B2B AI agent market: $10-12B (2026), 45-50% CAGR
  (B2BAGTMKT-SC-TBRC-MKTSZE | https://thebusinessresearchcompany.com/report/artificial-intelligence-agents-global-market-report 2026,
   B2BAGTMKT-SC-GVR-MKTSZE | https://grandviewresearch.com/industry-analysis/ai-agents-market-report 2025)
```

What an auditor sees:
- Claim: "$10-12B (2026), 45-50% CAGR"
- Two independent sources (analyst consensus)
- Both clickable URLs
- Publication dates: 2026 (TBRC) and 2025 (GVR) - reader knows GVR report is older
- Verification label:
- Can click URL immediately to verify

### GOOD: Source Registry Entry (B2BAGTMKT)

```markdown
### B2BAGTMKT-SC-TBRC-MKTSZE
- **Title**: AI Agents Global Market Report 2026-2030
- **URL**: https://thebusinessresearchcompany.com/report/artificial-intelligence-agents-global-market-report
- **Published**: 2026-01 (exact date unknown, Q1 2026 release)
- **Data vintage**: 2025 actual, 2026-2030 projected
- **Accessed**: 2026-08-04
- **Archived**: `_SOURCES/tbrc-ai-agents-market-report-2026.md`
- **Type**: Market Report
- **Tier**: 1 (Analyst Research, Primary)
- **Key Data Points**: $8.29B (2025) -> $12.06B (2026) -> $53.2B (2030), CAGR 44.9%
- **[VERIFIED]**
```

### BAD: Bare Source ID (No URL, No Year)

```markdown
US banks project $177M average AI spend in 2026, up 33% from $133M in Q4 2025
(AIAUTMFIN-SC-KPMG-BKPLS1)
```

Problems:
- No URL → auditor cannot verify without opening Sources file
- No year → is this Q1 2026 data? Annual 2025 data?
- No scheme → even if domain were shown, not clickable

### BAD: Informal Attribution (No Source ID)

```markdown
US banks project $177M average AI spend in 2026, up 33% from $133M in Q4 2025
(KPMG Banking Q1 2026).
```

Problems:
- No SOURCE-ID → cannot look up in registry
- No URL → cannot verify
- "KPMG Banking Q1 2026" is ambiguous - which specific KPMG publication?
- No verification label

### BAD: Domain Without Scheme

```markdown
- 7 frameworks converge: Plan + Act + Loop + Tools = Agent
  (B2BAGTMKT-SC-GRTNR-40PCT26 | gartner.com)
```

Problems:
- `gartner.com` is not clickable (no `https://`)
- No specific page path - could be any Gartner page
- No data vintage year

### GOOD: Correct First + Subsequent Pattern

```markdown
Seven frameworks converge on a minimum viable agent definition: software that plans,
acts via tools, loops with self-correction, and persists state
(B2BAGTMKT-SC-GRTNR-40PCT26 | https://gartner.com/en/newsroom/press-releases/2025-08-26-gartner-40-percent-enterprise-apps-agents 2025,
 B2BAGTMKT-SC-SEQCAP-GLDLK | https://sequoiacap.com/article/goldilocks-agents 2024,
 B2BAGTMKT-SC-MENLO-AGNT | https://menlovc.com/perspective/ai-agents-enterprise-automation 2024).

...later in same document...

Only 16-17% of enterprise deployments qualify as true agents
(B2BAGTMKT-SC-MENLO-AGNT 2024).
```

What works:
- First mention: full URL + year for each source
- Subsequent mention: ID + year only (URL already shown earlier)
- Year stays with every citation (temporal context always visible)

### GOOD: Source with Quarter Precision

```markdown
US banks project $177M average AI spend, up 33% from Q4 2025
(AIAUTMFIN-SC-KPMG-BKPLS1 | https://kpmg.com/us/en/articles/banking-leaders-pulse-survey-q1-2026.html 2026-Q1)
```

What works:
- Quarter precision: `2026-Q1` tells the auditor when this source was published
- Full URL with scheme: clickable, verifiable
- Verification label:

## 9. Compliance Checklist

Use this to verify any research document meets the auditable citation standard.

### 9.1 Per-Claim Verification

- [ ] Claim has a SOURCE-ID
- [ ] SOURCE-ID includes full URL with `https://` (first mention) or was already introduced earlier in document
- [ ] Publication date present in citation (YYYY-MM-DD, YYYY-MM, YYYY-QN, YYYY-HN, or YYYY)
- [ ] Verification label present: [ASSUMED],, [TESTED], or [PROVEN]

### 9.2 Per-Source Verification

- [ ] Source registry entry exists (in `_Sources.md` or Sources section)
- [ ] Registry entry has: Title, URL, Published, Data vintage, Accessed, Archived, Type, Tier
- [ ] Archived copy exists in `_SOURCES/` folder (transcribed markdown or PDF)
- [ ] Archived copy preserves page numbers as headings (for multi-page sources)

### 9.3 Per-Document Verification

- [ ] No bare source IDs without URL on first mention
- [ ] No informal attributions ("according to KPMG") without source ID
- [ ] No URLs without `https://` scheme
- [ ] No citations missing publication date
- [ ] Multi-file output has dedicated `_Sources.md`
- [ ] All source IDs in document appear in registry
- [ ] All registry entries have archived copies

## 10. When to Apply This Standard

### 10.1 Compliance Levels

- **Level 3 (Full / Audit-Ready)**: `(SOURCE-ID | https://full-url YYYY)` + source registry + archive. Required for investor materials, regulatory filings, external-facing research.
- **Level 2 (Interim / Internal)**: `(SOURCE-ID | https://full-url)` + source registry. No publication date required. Archive optional. Acceptable for internal research summaries and working documents.
- **Level 1 (Minimum)**: `(SOURCE-ID)` bare. Acceptable ONLY for exploratory notes, hypotheses, and draft sections marked [ASSUMED].

All levels require `https://` scheme when a URL is present (Section 2.3: bare domains are never acceptable). Level 2 differs from Level 3 only in omitting publication date and archive.

Existing T02 research targeting Level 2 is compliant for internal use. Upgrade to Level 3 when research feeds investor-facing deliverables.

### 10.2 Applicability

- **Level 3 required**: Research summaries informing business decisions, investor materials, regulatory filings
- **Level 2 acceptable**: Internal working notes, multi-file deep research output (default target for active migration)
- **Level 1 acceptable**: Opinion pieces, strategic commentary, hypotheses sections marked [ASSUMED]

### 10.3 Relationship to INFO-SC-05

This standard complements INFO-SC-05 (entity/tool linking with markdown hyperlinks). INFO-SC-05 links entities for navigation: `[Microsoft OAuth docs](https://url)`. This standard links claims to evidence for audit: `(SOURCE-ID | https://url YYYY)`. Both coexist in the same document. They serve different purposes and never conflict.

## 11. Document History

**[2026-08-05 15:12]**
- Fixed: "First-Reference Rule" renamed to "First-Mention Rule" - eliminates polysemy with "reference" = bibliographic entry (MW-WC-05)
- Fixed: All "first reference" → "first mention" throughout document (7 occurrences)
- Fixed: Undefined [COMMUNITY] label removed from Section 9.1 checklist (SOCAS-06)
- Changed: Section 6.3 rules grouped into 3 clusters: file organization, transcription by type, documentation requirements (AP-ST-07)

**[2026-08-05 15:10]**
- Added: Section 1.4 "Terminology" - defines all key terms upfront
- Added: Section 4.5 "Citation vs Quotation" - distinguishes in-text citation from verbatim quotation
- Fixed: Terminology aligned with academic standards (APA/Harvard/Chicago): citation = in-text marker, quotation = verbatim text
- Quotation required for editorial conclusions and foundational arguments; citation sufficient for factual data

**[2026-08-05 15:05]**
- Fixed: Section 10.1 Level 2 format contradicted Section 2.3 (`domain.com` listed as failure but also as Level 2 format)
- Changed: Level 2 redefined as `(SOURCE-ID | https://full-url)` - full URL with scheme, no date required, archive optional
- Added: Explicit note that all levels require `https://` scheme when URL is present

**[2026-08-05 14:50]**
- Fixed: "Self-verifying at point of use" replaced with "traceable to source at point of use" (resolves contradiction with first-reference-only pattern)
- Added: Compliance Levels (Level 1/2/3) to Section 10 - resolves conflict with TASKS V2 migration target
- Added: INFO-SC-05 disambiguation (Section 10.3) - clarifies coexistence of two inline formats
- Changed: Page number requirement softened from MUST to SHOULD (allows citing from direct observation with pending transcription)

**[2026-08-05 14:35]**
- Fixed: Internal contradictions ("data vintage" references in citation context replaced with "publication date")
- Fixed: Timeline format per INFO-HD-03
- Fixed: Subsection numbering per INFO-SN-02
- Changed: Section 3 diagram format updated to `YYYY-MM[-DD]`

**[2026-08-05 14:30]**
- Removed: Workflow/rule dependencies. Document is self-contained.
- Added: Compliance Checklist (Section 9) and applicability scope (Section 10).
- Changed: Date model simplified - citation carries publication date only, data vintage in prose.
- Added: Document sources (PDF, Google Doc, Word) with filename + URL + page format.
- Added: Date precision hierarchy (YYYY-MM-DD, YYYY-MM, YYYY-QN, YYYY-HN, YYYY).

**[2026-08-05 14:25]**
- Initial document created. Defines three-layer audit architecture for research citations.
