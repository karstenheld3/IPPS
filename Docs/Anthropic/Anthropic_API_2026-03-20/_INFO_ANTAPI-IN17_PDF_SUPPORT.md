# PDF Support

**Doc ID**: ANTAPI-IN17
**Goal**: Document PDF input via document content blocks, formats, and limitations
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` for Messages API content block types

## Summary

Claude accepts PDF documents as input via `document` content blocks with `media_type: "application/pdf"`. PDFs can be provided as base64-encoded data, via URL, or by file_id reference (Files API). Claude extracts and processes both text and visual content from PDFs. PDF support is available on all current Claude models. When combined with citations, PDF text is extracted and chunked into sentences for citation by page location.

## Key Facts

- **Content Block**: `{"type": "document", "source": {...}}`
- **Source Types**: `base64`, `url`, `file` (via file_id)
- **Media Type**: `application/pdf`
- **Text Extraction**: Automatic for text-based PDFs
- **Visual Processing**: Renders pages as images for visual content
- **Citations**: Supported with `page_location` citation type
- **Status**: GA

## Usage Examples

### PDF from URL

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "url",
                        "url": "https://example.com/report.pdf",
                    },
                },
                {"type": "text", "text": "Summarize the key findings of this report."},
            ],
        }
    ],
)
```

### PDF from Base64

```python
import anthropic
import base64

client = anthropic.Anthropic()

with open("document.pdf", "rb") as f:
    pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data,
                    },
                },
                {"type": "text", "text": "Extract all tables from this document."},
            ],
        }
    ],
)
```

### PDF from Files API

```python
import anthropic

client = anthropic.Anthropic()

# Upload first via Files API (beta)
uploaded = client.beta.files.upload(
    file=open("document.pdf", "rb"),
    purpose="messages",
)

# Reference by file_id
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": uploaded.id,
                    },
                },
                {"type": "text", "text": "What does this document describe?"},
            ],
        }
    ],
)
```

### PDF with Citations

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data,
                    },
                    "title": "Research Paper",
                    "citations": {"enabled": True},
                },
                {"type": "text", "text": "What methodology was used? Cite your sources."},
            ],
        }
    ],
)
```

## Token Costs Per Page

- **Text tokens**: 1,500-3,000 tokens per page depending on content density
- **Image tokens**: Each page is also converted to an image; same cost calculation as vision (`width*height/750`)
- **Combined**: A typical 3-page PDF uses ~7,000 tokens with full visual processing
- No additional PDF-specific fees beyond standard token pricing
- Use `count_tokens` endpoint to estimate costs for specific PDFs

## Platform Availability

- **Claude API (Anthropic)** - Full support
- **Google Vertex AI** - Full support
- **Amazon Bedrock** - Supported with caveats:
  - **Converse API without citations**: Falls back to basic text extraction only (no visual analysis, ~1,000 tokens/3 pages)
  - **Converse API with citations enabled**: Full visual understanding (~7,000 tokens/3 pages)
  - **InvokeModel API**: Full control over PDF processing without forced citations
- All active models support PDF processing

## Gotchas and Quirks

- Scanned PDFs without extractable text can be processed visually but cannot produce text citations
- PDF page images consume tokens based on rendered dimensions
- **Dense PDFs** (small font, complex tables, heavy graphics) can fill context window before reaching page limit
- Large PDFs can fail even with Files API; split documents or downsample embedded images
- `.csv`, `.xlsx`, `.docx` files cannot be provided as document blocks; convert to plain text first
- URL PDFs must be publicly accessible
- Request payload limit: 32 MB (use Files API + `file_id` for large PDFs)
- **Bedrock Converse API**: Must enable citations for visual PDF analysis; without it, only basic text extraction

## Related Endpoints

- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` - Messages API (document blocks)
- `_INFO_ANTAPI-IN15_CITATIONS.md [ANTAPI-IN15]` - Citations with PDFs
- `_INFO_ANTAPI-IN16_VISION.md [ANTAPI-IN16]` - Visual processing
- `_INFO_ANTAPI-IN28_FILES_API.md [ANTAPI-IN28]` - File upload for PDF references

## Sources

- ANTAPI-SC-ANTH-PDF - https://platform.claude.com/docs/en/build-with-claude/pdf-support - PDF guide
- ANTAPI-SC-ANTH-MSGCRT - https://platform.claude.com/docs/en/api/messages/create - Document block schema

## Document History

**[2026-03-20 05:00]**
- Added: Token costs per page (1,500-3,000 text + image tokens)
- Added: Platform availability (API, Vertex full; Bedrock with citation caveat)
- Added: Dense PDF context warnings, 32 MB payload limit

**[2026-03-20 03:25]**
- Initial documentation created from PDF support guide
