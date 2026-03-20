---
description: Transcribe PDFs and web pages to complete markdown with 100% content preservation
auto_execution_mode: 1
---

# Transcribe Workflow

Convert PDF files and web pages to complete markdown. **Nothing may be omitted.**

## Required Skills

- @pdf-tools for PDF to image conversion
- @ms-playwright-mcp for web page screenshots
- @llm-transcription (optional) for advanced LLM-based transcription

## MUST-NOT-FORGET

- Ensure complete file is stitched together and file path is noted
- Run `/verify` after transcription complete
- Keep source images for verification

## Step 1: Detect Transcription Mode

```powershell
$skillPath = ".windsurf/skills/llm-transcription/transcribe-image-to-markdown.py"
$keysFile = "[WORKSPACE_FOLDER]\..\.tools\.api-keys.txt"
$hasSkill = Test-Path $skillPath
$hasKeys = Test-Path $keysFile
if ($hasSkill -and $hasKeys) { Write-Host "MODE: Advanced LLM Transcription" }
else { Write-Host "MODE: Built-in Transcription (workflow prompt)" }
```

**Mode A**: skill + keys available → `transcribe-image-to-markdown.py` with ensemble + judge + refinement
**Mode B**: fallback → built-in prompt in Appendix

## Core Principle

**Maximum 4 pages per transcription call.** Write output to file immediately after each chunk.

## Source Types

- Local PDF (path ends `.pdf`) → Convert to JPG, transcribe
- URL to PDF (URL ends `.pdf`) → Download first, then process as local PDF
- Web page (URL to HTML) → Screenshot, transcribe

## Step 2: Prepare Source

### For Local PDF
```powershell
python .windsurf/skills/pdf-tools/convert-pdf-to-jpg.py "path/to/document.pdf" --dpi 120
```

### For URL to PDF
```powershell
$url = "https://example.com/document.pdf"
$filename = [System.IO.Path]::GetFileName($url)
Invoke-WebRequest -Uri $url -OutFile "[SESSION_FOLDER]/$filename"
python .windsurf/skills/pdf-tools/convert-pdf-to-jpg.py "[SESSION_FOLDER]/$filename" --dpi 120
```

### For Web Page
```
mcp0_browser_navigate(url: "https://example.com/page")
mcp0_browser_evaluate(function: "window.scrollTo(0, document.body.scrollHeight)")
mcp0_browser_wait_for(time: 2)
mcp0_browser_evaluate(function: "window.scrollTo(0, 0)")
mcp0_browser_take_screenshot(fullPage: true, filename: "../.tools/_web_screenshots/[domain]/page-001.png")
```

## Step 3: Count and Plan

```powershell
$images = Get-ChildItem "../.tools/_pdf_to_jpg_converted/[NAME]/" -Filter "*.jpg"
$totalPages = $images.Count
$chunks = [math]::Ceiling($totalPages / 4)
Write-Host "Total pages: $totalPages, Chunks needed: $chunks"
```

## Step 4: Determine Output Strategy

- 1-20 pages: Single markdown file
- 21-50: Single file, write after each 4-page chunk
- 51-100: Multiple section files + index, merge optional
- 100+: Multiple chapter files + index

## Step 5: Create Output File with Header

```markdown
# [Document Title]

<!-- TRANSCRIPTION PROGRESS
Chunk: 1 of [total_chunks]
Pages completed: 0 of [total]
-->

## Table of Contents
[Generate after first pass or from PDF TOC]
```

## Step 6: Transcribe in 4-Page Chunks

For each chunk (pages 1-4, 5-8, 9-12, etc.):

### 6a. Choose Transcription Method

**Mode A: Advanced LLM Transcription**

```powershell
$venv = "../.tools/llm-venv/Scripts/python.exe"
$skill = ".windsurf/skills/llm-transcription"

# Single file
& $venv "$skill/transcribe-image-to-markdown.py" `
    --input-file "../.tools/_pdf_to_jpg_converted/[NAME]/page_001.jpg" `
    --output-file "[SESSION_FOLDER]/[DocName]_page001.md" `
    --keys-file "[WORKSPACE_FOLDER]\..\.tools\.api-keys.txt" `
    --model gpt-5-mini `
    --workers 4

# Batch mode (entire folder)
& $venv "$skill/transcribe-image-to-markdown.py" `
    --input-folder "../.tools/_pdf_to_jpg_converted/[NAME]/" `
    --output-folder "[SESSION_FOLDER]/transcribed/" `
    --keys-file "[WORKSPACE_FOLDER]\..\.tools\.api-keys.txt" `
    --model gpt-5-mini `
    --initial-candidates 1 `
    --workers 12
```

**Mode B: Built-in Transcription** (no skill or keys)

Read up to 4 images per call, apply built-in prompt from Appendix.

### 6b. Content Extraction Rules (Mode B)

Extract ALL content: headings, paragraphs, lists, footnotes, figures (see Figure Protocol), tables (markdown), captions, labels, references.

**Special Characters:**
- Superscripts/subscripts: Unicode (¹ ² ³, ₁ ₂ ₃) not ASCII
- Greek letters: actual Unicode (α β γ)
- Math: LaTeX syntax (`$E = mc^2$`)
- Symbols: proper Unicode (© ® ™ § † ‡ °)

### Page Boundary Markers

**Footer** BEFORE `---`: `<transcription_page_footer> Page 5 | Company Name | Confidential </transcription_page_footer>`
**Header** AFTER `---`: `<transcription_page_header> Annual Report 2024 | Section 3 </transcription_page_header>`

Single-line or multi-line format both acceptable. Capture: page numbers, doc title, company name, classification, version/date, navigation text. Omit tag if absent in source.

### 6c. Append to output file IMMEDIATELY

### 6d. Update progress marker
```markdown
<!-- TRANSCRIPTION PROGRESS
Chunk: 2 of 5
Pages completed: 4 of 20
-->
```

### 6e. Continue with next chunk until all pages processed.

## Figure Transcription Protocol

**MANDATORY**: Every figure MUST have BOTH ASCII art AND `<transcription_notes>`.

### F0: Analyze Before Drawing
1. **Subject**: diagram type, subject matter
2. **Elements**: 3-7 main components
3. **Relationships**: spatial, logical, flow
4. **Priority**: what matters most

### F1: Create ASCII Art

**Mode A: Structural** (flowcharts, diagrams, architecture, UI): `+ - | / \ _ [ ] ( ) { } < > -> <- v ^`
**Mode B: Shading** (photographs, complex graphics): `@#%&8BWM*oahkbd=+-:.`

**Maximize semantics**: title header, inline legends, semantic labels on every node, state annotations, result summaries. LLMs understand labels better than visual patterns.

**Layout**: 80-120 chars wide (max 180), double horizontal spacing for aspect ratio. **PURE ASCII ONLY** - no Unicode box-drawing.

````
<transcription_image>
**Figure [N]: [Caption from original]**

```ascii
[ASCII art representation here]
```

<transcription_notes>
- Mode: Structural | Shading
- Dimensions: [width]x[height] characters
- ASCII captures: What the ASCII diagram successfully represents
- ASCII misses: Visual elements that cannot be shown in ASCII
- Colors:
  - [color name] - what it represents
- Layout: Spatial arrangement, panels, relative positions
- Details: Fine details, textures, gradients, 3D effects, icons
- Data: Specific values, measurements, labels, or quantities visible
- Reconstruction hint: Key detail needed to imagine original
</transcription_notes>
</transcription_image>
````

### F2b: Self-Verify
- [ ] All labeled elements from original present?
- [ ] Spatial relationships preserved?
- [ ] Flow or hierarchy clear?
- [ ] Readable without seeing original?

If any check fails, revise before continuing.

### Figure Protocol Rules
1. Every figure wrapped in `<transcription_image>...</transcription_image>`
2. No exceptions - even photographs get ASCII + notes
3. Photographs: ASCII shows composition; notes describe subject
4. Graphs/Charts: ASCII shows axes/trend; notes provide data points
5. Network Diagrams: ASCII shows topology; notes describe colors/links
6. 3D: ASCII shows 2D projection; notes describe depth

## Step 7: Stitch Transcribed Pages

```powershell
$folder = "[OUTPUT_FOLDER]/02_transcribed_pages"
$output = "[OUTPUT_FOLDER]/[DocName].md"
$files = Get-ChildItem $folder -Filter "*.md" | Where-Object { $_.Name -notlike "_*" } | Sort-Object Name
$content = @()
$pageNum = 1
foreach ($file in $files) {
    if ($pageNum -eq 1) {
        $content += "<!-- Page {0:D3} -->`n`n" -f $pageNum
    } else {
        $content += "`n---`n<!-- Page {0:D3} -->`n`n" -f $pageNum
    }
    $content += (Get-Content $file.FullName -Raw).TrimEnd()
    $pageNum++
}
$finalContent = ($content -join "").TrimEnd()
$finalContent | Out-File $output -Encoding UTF8
Write-Output "Merged $($files.Count) files to $output"
```

Filename convention: original name, no suffixes (e.g., `Report-2023.md` not `Report-2023_COMPLETE.md`).

## Step 8: Finalize

1. Remove progress markers
2. Generate/verify Table of Contents
3. Log metadata to session NOTES.md (source, pages, figures, date)

## Output Locations

- Converted images: `../.tools/_pdf_to_jpg_converted/[NAME]/`
- Transcribed pages: `[SESSION_FOLDER]/02_transcribed_pages/`
- Final merged output: `[SESSION_FOLDER]/[DocName].md`
- Web screenshots: `../.tools/_web_screenshots/[DOMAIN]/`

## Long Document Strategy (50+ pages)

```
[SESSION_FOLDER]/
├── [DocName]_INDEX.md      # TOC and metadata
├── [DocName]_Part01.md     # Pages 1-20
├── [DocName]_Part02.md     # Pages 21-40
└── ...
```

## Verification

Run `/verify`:
1. Compare page count
2. Check all sections present
3. All figures have BOTH ` ```ascii ` AND `<transcription_notes>`
4. Page boundary markers: `<transcription_page_header>` after `---`, `<transcription_page_footer>` before `---`
5. Cross-check text accuracy
6. Validate XML tags well-formed

## Appendix: Built-in Transcription Prompt (Mode B)

**Transcription Prompt v1B**

Transcribe this document page image to Markdown. **Accuracy over speed.**

**Key Areas:** Graphics (labeled ASCII + data extraction), Structure (semantic hierarchy), Text (character-level accuracy)

**DO:**
- Label every node: `[DATABASE]`, `[PROCESS]`, `(pending)`
- Extract ALL data values from charts (numbers > visual fidelity)
- Match header levels to visual hierarchy (H1=title, H2=sections, H3=subsections)
- Use `[unclear]` for unreadable text

**DON'T:**
- Don't transcribe UI chrome (toolbars, ribbons, browser elements)
- Don't count decorative logos/separators as missed graphics
- Don't use headers for formatting convenience - only for real sections
- Don't guess numbers - mark as `[unclear: ~value?]`

**Graphics:**

TRANSCRIBE: Charts, diagrams, flowcharts, infographics, data visualizations, maps, technical illustrations
SKIP: UI chrome, toolbars, logos, watermarks → `<!-- Decorative: [list] -->`

Every essential graphic MUST have:

```markdown
<transcription_image>
**Figure N: [Caption]**

```ascii
[TITLE - WHAT THIS SHOWS]
[Visual with INLINE labels - every node named]
Legend: [A]=Item1 [B]=Item2
```

<transcription_notes>
- Data: [all numbers, percentages, values]
- Colors: [color] = [meaning]
- ASCII misses: [what couldn't be shown]
</transcription_notes>
</transcription_image>
```

**Structure:**
- H1 = Document title (one per page max)
- H2 = Major sections
- H3 = Subsections
- Multi-column: top-to-bottom per column, mark with `<!-- Column N -->`

**Text Accuracy:**
- Every word exactly as shown, numbers exact
- Mark unclear: `[unclear]` or `[unclear: best guess?]`
- Superscripts: Unicode. Greek: Unicode. Math: LaTeX. Symbols: Unicode.

**Output Structure:**

```markdown
# [Document Title]

<transcription_page_header> [if present] </transcription_page_header>

## [Section]

[Content...]

<transcription_image>
**Figure 1: [Caption]**
[ASCII with inline labels]
<transcription_notes>[Data, colors, misses]</transcription_notes>
</transcription_image>

<transcription_page_footer> [if present] </transcription_page_footer>
```