# Research Tools Reference

Goal: Document available tools for research workflows

## Source Collection Tools

- `search_web` (Built-in) - Web search, initial source discovery
- `read_url_content` (Built-in) - Fetch web page content, direct URL scraping
- `browser_navigate` (ms-playwright-mcp) - Navigate browser, dynamic/auth-required sites
- `browser_snapshot` (ms-playwright-mcp) - Accessibility tree, page structure extraction
- `browser_screenshot` (ms-playwright-mcp) - Capture page image, visual documentation
- `browser_evaluate` (ms-playwright-mcp) - Execute JavaScript, dynamic content extraction

## Document Processing Tools

- `convert-pdf-to-jpg.py` (pdf-tools) - PDF pages to JPG, vision analysis
- `pdftotext.exe` (pdf-tools) - Extract text from searchable PDFs
- `pdfinfo.exe` (pdf-tools) - PDF metadata, dates, page counts
- `compress-pdf.py` (pdf-tools) - Reduce PDF size for archiving

## Transcription Tools

- `transcribe-image-to-markdown.py` (llm-transcription) - Image to structured markdown
- `transcribe-audio-to-markdown.py` (llm-transcription) - Audio to markdown transcript

## Tool Selection Priority

Always try built-in tools first (faster, cheaper), escalate to Playwright on failure.

```
START: Need to collect source
├─> URL known? → read_url_content → Success? Done / Fail? Playwright
├─> No URL? → search_web → get URL → retry
├─> File (not web)?
│   ├─> PDF → pdf-tools (pdftotext or jpg→transcribe)
│   ├─> DOCX/PPTX → pandoc or direct read
│   ├─> XLSX/CSV → pandas or direct parse
│   └─> Other → text-based? read / else convert
├─> Auth/consent required? → Playwright persistent profile
├─> Dynamic/JS content? → Playwright browser_snapshot
├─> Full visual capture? → Playwright screenshot(fullPage)
└─> Visual source?
    ├─> Image → transcribe-image-to-markdown.py
    └─> Audio → transcribe-audio-to-markdown.py
```

## When to Use Built-in Tools

`search_web`: Discovering sources, official docs URLs, GitHub repos, Stack Overflow
`read_url_content`: Known URL, static content, no JS rendering, no auth/consent needed

## When to Escalate to Playwright

ms-playwright-mcp is DEFAULT browser tool (public content). playwriter MCP is EXCEPTION (user credentials/MFA required).

Escalate when:
- `read_url_content` returns empty/garbled (JS-heavy, SPA, lazy load)
- Site requires login, cookie consent, CAPTCHA, form submission, age verification
- Need full-page visual capture or document downloads behind interaction

Debugging fallback: If Playwright fails, use `& "[DEVSYSTEM_FOLDER]/skills/windows-desktop-control/simple-screenshot.ps1"` to diagnose popups/blockers.

Source access failure handling (after 2 retries of both tools):
1. Document as `[INACCESSIBLE]` in `__[TOPIC]_SOURCES.md` with reason
2. Search for alternative (mirror, archive.org, cache)
3. If no alternative, proceed without - document gap
4. Max 3 inaccessible sources before escalating to user

## PDF Processing Workflow

```
1. INSPECT: pdfinfo + pdfimages -list
2. Many large images? → YES: image path / NO: try pdftotext first
3. Text insufficient? → convert-pdf-to-jpg --dpi 150
4. Review 3-5 images, assess quality
5. BATCH: transcribe-image-to-markdown.py --workers N (start 10, increase if stable)
6. ARCHIVE: compress-pdf.py, store .md + compressed PDF (preserve timestamps)
```

Decision criteria:
- 0-5 small images OR native digital → text path (`pdftotext`)
- Many large images (>100KB) OR scanned OR garbled/whitespace output → image path (`convert-pdf-to-jpg`)

Commands:
```powershell
pdfinfo.exe "source.pdf"
pdfimages -list "source.pdf"
pdftotext.exe "source.pdf" "source.txt"
python convert-pdf-to-jpg.py "source.pdf" --dpi 150 --output "[SESSION]/pdf_images/"
python transcribe-image-to-markdown.py --input-folder "[SESSION]/pdf_images/" --output-folder "[SESSION]/transcribed/" --workers 60
python compress-pdf.py "source.pdf" --output "[SESSION]/compressed/"
```

Session folder structure:
```
[SESSION]/
├── pdf_sources/       [original PDFs]
├── pdf_images/[PDF_NAME]/   page_001.jpg, page_002.jpg...
├── transcribed/[PDF_NAME]/  page_001.md, page_002.md...
└── compressed/        [PDF_NAME]_compressed.pdf
```

## LLM Transcription

`transcribe-image-to-markdown.py`: Screenshots, architecture diagrams, slides, UI mockups, handwritten notes
`transcribe-audio-to-markdown.py`: Conference talks, podcasts, video tutorials (audio track), meeting recordings

## Anti-Patterns

- Using Playwright first - always try built-in tools first
- Skipping PDF analysis - use `pdfinfo` before choosing extraction method
- Screenshots without transcription - visual captures need markdown conversion
- Single extraction attempt - retry with different tool if first fails

## Tool Locations

- pdf-tools - `../.tools/` (binaries), `[DEVSYSTEM_FOLDER]/skills/pdf-tools/` (scripts)
- llm-transcription - `[DEVSYSTEM_FOLDER]/skills/llm-transcription/`
- ms-playwright-mcp - MCP server (configured in mcp_config.json)