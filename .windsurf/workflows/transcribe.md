---
description: Transcribe PDFs and web pages to complete markdown with 100% content preservation
---

# Transcribe Workflow

Convert Portable Document Format (PDF) files and web pages to complete markdown files. **Nothing may be omitted.**

PDF images are converted to JPEG (JPG) format for processing.

## Required Skills

- @pdf-tools for PDF to image conversion
- @ms-playwright-mcp for web page screenshots

## Core Principle

**Maximum 1 page per transcription call.** Write output to file immediately after each page. This prevents JSON truncation errors in edit tools.

## Source Types

- **Local PDF** - File path ends in `.pdf` → Convert to JPG, transcribe
- **URL to PDF** - URL ends in `.pdf` → Download first, then process
- **Web page** - URL to HTML → Screenshot, transcribe

## Step 1: Prepare Source

### For Local PDF
```powershell
python .windsurf/skills/pdf-tools/convert-pdf-to-jpg.py "path/to/document.pdf" --dpi 300  # 300 Dots Per Inch (DPI)
```

### For URL to PDF
```powershell
$url = "https://example.com/document.pdf"
$filename = [System.IO.Path]::GetFileName($url)
# Download to: [SESSION_FOLDER] > [WORKSPACE_FOLDER]
Invoke-WebRequest -Uri $url -OutFile "[SESSION_FOLDER]/$filename"
# Then convert to JPG
python .windsurf/skills/pdf-tools/convert-pdf-to-jpg.py "[SESSION_FOLDER]/$filename" --dpi 300
```

### For Web Page
```
mcp0_browser_navigate(url: "https://example.com/page")
mcp0_browser_evaluate(function: "window.scrollTo(0, document.body.scrollHeight)")
mcp0_browser_wait_for(time: 2)
mcp0_browser_evaluate(function: "window.scrollTo(0, 0)")
mcp0_browser_take_screenshot(fullPage: true, filename: ".tools/_web_screenshots/[domain]/page-001.png")
```

## Step 2: Count and Plan

```powershell
$images = Get-ChildItem ".tools/_pdf_to_jpg_converted/[NAME]/" -Filter "*.jpg"
$totalPages = $images.Count
$chunks = [math]::Ceiling($totalPages / 4)
Write-Host "Total pages: $totalPages, Chunks needed: $chunks"
```

## Step 3: Determine Output Strategy

- **1-20 pages** - Single markdown file
- **21-50 pages** - Single file, write after each 4-page chunk
- **51-100 pages** - Multiple section files + index, merge optional
- **100+ pages** - Multiple chapter files + index

## Step 4: Create Output File with Header

```markdown
# [Document Title]

**Source**: [filename].pdf
**Pages**: [total]
**Transcribed**: [date]

<!-- TRANSCRIPTION PROGRESS
Chunk: 1 of [total_chunks]
Pages completed: 0 of [total]
-->

## Table of Contents
[Generate after first pass or from PDF Table of Contents]

---
```

## Step 5: Transcribe One Page at a Time

For each page:

### 5a. Read exactly 1 page image
```
read_file(file_path: "[path]_page001.jpg")
```

### 5b. Extract ALL content from these pages
- Every heading, paragraph, list, footnote
- Every figure → ASCII diagram OR verbalized description
- Every table → Markdown table
- Every caption, label, reference

### 5c. Append to output file IMMEDIATELY
Do not wait until end. Write after each chunk.

### 5d. Update progress marker
```markdown
<!-- TRANSCRIPTION PROGRESS
Page: 2 of 20
-->
```

### 5e. Continue with next page
Repeat until all pages processed.

## Step 6: Finalize

1. Remove progress markers
2. Generate/verify Table of Contents
3. Add Document Info section at end:
```markdown
---
**Document Info**
- Source: [filename]
- Total pages: [count]
- Figures: [count] (ASCII: [n], Verbalized: [n])
- Transcribed: [date]
- Verified: [pending/date]
```

## Output Locations

- Converted images: `.tools/_pdf_to_jpg_converted/[PDF_FILENAME]/`
- Web screenshots: `.tools/_web_screenshots/[DOMAIN]/`
- Markdown output: `[SESSION_FOLDER]/` or user-specified location

## Long Document Strategy (50+ pages)

For documents over 50 pages, create multiple files:

```
[SESSION_FOLDER]/
├── [DocName]_INDEX.md      # TOC and metadata
├── [DocName]_Part01.md     # Pages 1-20
├── [DocName]_Part02.md     # Pages 21-40
├── [DocName]_Part03.md     # Pages 41-60
└── ...
```

Index file format:
```markdown
# [Document Title] - Index

**Source**: [filename].pdf
**Total Pages**: [n]
**Parts**: [n]

## Parts

1. [Part01](./[DocName]_Part01.md) - Pages 1-20: [Chapter names]
2. [Part02](./[DocName]_Part02.md) - Pages 21-40: [Chapter names]
...
```

## Verification

After transcription, run `/verify` to:
1. Compare page count
2. Check all sections present
3. Verify all figures transcribed
4. Cross-check text accuracy

## Best Practices

1. **1 page per call** - Prevents JSON truncation errors in edit tools
2. **Write immediately** - Append to file after each page
3. **Track progress** - Use progress markers for resumability
4. **300 DPI for PDFs** - Higher quality for accurate transcription
5. **Keep source images** - Required for `/verify`
6. **No omissions** - Every piece of content must be transcribed
