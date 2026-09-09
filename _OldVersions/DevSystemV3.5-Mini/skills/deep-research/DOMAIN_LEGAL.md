# Domain Profile: Legal Research

Research domain for legislation, case law, regulatory frameworks, and legal analysis.

## When to Use

- Subject is legislation, regulation, legal framework, or case law
- Prompt mentions: law, regulation, article, section, statute, directive, compliance, court decision, legal basis
- Output consumed by legal teams, compliance officers, or policy analysts

## Source Tiers

- Tier 1 (official/primary): Full legislation text, court decisions, official gazettes, regulatory body publications
- Tier 2 (vendor/issuer): Legal commentary from law firms, regulatory guidance documents, official FAQs
- Tier 3 (community/analyst): Legal blogs, academic papers, conference presentations, industry compliance guides

## Document Handling

- Download and transcribe FULL legislation texts - No summarization, no excerpts. Complete text MUST be in `_SOURCES/`.
- EU/national legislation: Download official PDF from EUR-Lex or national gazette, transcribe fully
- Court decisions: Download full text, transcribe fully
- Model selection: `gpt-5-mini` exclusively (99.5% accuracy). Wrong article numbers or terminology have regulatory consequences.
- Cross-reference between statutes and case law
- Storage structure:
  ```
  _SOURCES/
  ├── eu-ai-act-2024.pdf              # Original legislation PDF
  ├── eu-ai-act-2024.md               # Full verbatim transcription
  ├── eu-ai-act-2024_data.jsonl       # Extracted tables (if any)
  ├── eu-ai-act-2024_transcribed/     # Individual pages
  └── case-law-c-123-24.md            # Court decision transcription
  ```

## Template Additions

- Statutory References - Exact article/section numbers with full quoted text
- Case Law Summary - Relevant court decisions with citations
- Regulatory Timeline - Effective dates, transition periods, deadlines
- Compliance Requirements - Actionable obligations derived from legislation
- Definitions - Legal definitions as stated in legislation (verbatim)

## Quality Criteria

- Every legal conclusion MUST cite exact article/section number
- Full source text of cited articles MUST be in `_SOURCES/` (not agent memory)
- Regulation numbers verified exactly (e.g., "2024/1689" not "2024/689") - cross-check against source PDF
- Legal terminology used exactly as defined in legislation (no paraphrasing defined terms)
- Effective dates and transition periods verified against official publication
- Distinction between "shall" (mandatory), "should" (recommended), "may" (optional) preserved exactly
- No legal advice or interpretation beyond source text - mark any inference as `[ASSUMED]`