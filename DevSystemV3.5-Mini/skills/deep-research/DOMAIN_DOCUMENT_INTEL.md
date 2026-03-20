# Domain Profile: Document Intelligence

Research domain for extracting structured data, tables, and key information from documents.

## When to Use

- Extracting tables, data points, or structured information from documents
- Prompt mentions: extract data, parse tables, compare documents, cross-reference
- Source documents are contracts, reports, datasets, specifications, technical standards
- Output will be structured data (JSON, CSV) alongside narrative analysis

## Source Tiers

- **Tier 1 (official/primary)**: Original source documents (contracts, reports, datasets, standards, specifications)
- **Tier 2 (vendor/issuer)**: Annotated/summarized versions, metadata, companion documents
- **Tier 3 (community/analyst)**: Commentary, analysis, implementation guides

## Document Handling

- **Transcribe ALL documents fully** - No partial reads, no summarization
- Extract tables via `<transcription_json>` tags (automatic from transcription pipeline)
- For already-transcribed docs: Grep `<transcription_json>` and `<transcription_table>` tags
- Create cross-reference matrices when comparing multiple documents
- Store in `_SOURCES/`:
  ```
  _SOURCES/
  ├── document.pdf                    # Original
  ├── document.md                     # Full transcription
  ├── document_data.jsonl             # All tables/charts as JSON
  ├── document_transcribed/           # Individual pages
  └── cross_reference.json            # Cross-reference matrix (if applicable)
  ```
- **Model selection**: `gpt-5-mini` for all document transcription (accuracy critical)

## Template Additions

- **Data Extraction Summary** - Overview of extracted data types and counts
- **Table Index** - All extracted tables with page references and JSON file locations
- **Cross-Reference Matrix** - Mapping between related data points across documents
- **Data Quality Notes** - Confidence levels, unclear values, reconciliation issues

## Quality Criteria

- Every extracted table verified against source (spot-check minimum 20%)
- All `<transcription_json>` data parseable as valid JSON
- Cross-reference matrix complete for all overlapping data points
- `[unclear]` markers documented and flagged in data quality notes
- No data points cited without page/section reference to source
- Numerical values cross-checked for unit consistency (currency, percentages, dates)