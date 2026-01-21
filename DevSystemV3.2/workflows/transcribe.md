---
description: Transcribe PDFs and web pages to complete markdown with 100% content preservation
auto_execution_mode: 1
---

# Transcribe Workflow

Convert Portable Document Format (PDF) files and web pages to complete markdown files. **Nothing may be omitted.**

## Required Skills

- @pdf-tools for PDF to image conversion
- @ms-playwright-mcp for web page screenshots

## Core Principle

**Maximum 4 pages per transcription call.** Write output to file immediately after each chunk.

## Source Types

| Source | Detection | Processing |
|--------|-----------|------------|
| Local PDF | File path ends in `.pdf` | Convert to JPG, transcribe |
| URL to PDF | URL ends in `.pdf` | Download first, then process |
| Web page | URL to HTML | Screenshot, transcribe |

## Step 1: Prepare Source

### For Local PDF
```powershell
python .windsurf/skills/pdf-tools/convert-pdf-to-jpg.py "path/to/document.pdf" --dpi 300  # 300 DPI (Dots Per Inch)
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
$chunks = [math]::Ceiling($totalPages / 2)
Write-Host "Total pages: $totalPages, Chunks needed: $chunks"
```

## Step 3: Determine Output Strategy

| Total Pages | Output Strategy |
|-------------|-----------------|
| 1-20 | Single markdown file |
| 21-50 | Single file, write after each 4-page chunk |
| 51-100 | Multiple section files + index, merge optional |
| 100+ | Multiple chapter files + index |

## Step 4: Create Output File with Header

```markdown
# [Document Title]

<!-- TRANSCRIPTION PROGRESS
Chunk: 1 of [total_chunks]
Pages completed: 0 of [total]
-->

## Table of Contents
[Generate after first pass or from PDF Table of Contents (TOC)]
```

## Step 5: Transcribe in 4-Page Chunks

For each chunk (pages 1-4, 5-8, 9-12, etc.):

### 5a. Read exactly 4 page images (or fewer for final chunk)
```
read_file(file_path: "[path]_page001.jpg")
read_file(file_path: "[path]_page002.jpg")
read_file(file_path: "[path]_page003.jpg")
read_file(file_path: "[path]_page004.jpg")
```

### 5b. Extract ALL content from these pages
- Every heading, paragraph, list, footnote
- Every figure → See **Figure Transcription Protocol** below
- Every table → Markdown table
- Every caption, label, reference

### Special Characters for Accurate Transcription

Use proper Unicode characters to match the original document:

**Superscripts (footnotes, exponents):**
```
¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ ⁰   (use instead of ^1 ^2 ^3)
ᵃ ᵇ ᶜ ᵈ ᵉ ᶠ ᵍ ʰ ⁱ ʲ ᵏ ˡ ᵐ ⁿ ᵒ ᵖ ʳ ˢ ᵗ ᵘ ᵛ ʷ ˣ ʸ ᶻ
```

**Subscripts:**
```
₀ ₁ ₂ ₃ ₄ ₅ ₆ ₇ ₈ ₉
ₐ ₑ ₕ ᵢ ⱼ ₖ ₗ ₘ ₙ ₒ ₚ ᵣ ₛ ₜ ᵤ ᵥ ₓ
```

**Greek letters:**
```
α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω
Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω
```

**Common symbols:**
```
© ® ™ § ¶ † ‡ ° ′ ″ ‴   (copyright, registered, trademark, section, pilcrow, dagger, degree, prime)
```

**Math formulas:** Use standard Markdown math extension (LaTeX syntax):
- Inline: `$E = mc^2$` renders as $E = mc^2$
- Block: `$$\sum_{i=1}^{n} x_i$$` for display equations
- Avoid Unicode math operators (± × ÷ ≠ ≈) and arrows (→ ←) - use LaTeX instead

**Fractions:**
```
½ ⅓ ⅔ ¼ ¾ ⅕ ⅖ ⅗ ⅘ ⅙ ⅚ ⅛ ⅜ ⅝ ⅞
```

## Figure Transcription Protocol

**MANDATORY**: Every figure MUST have BOTH ASCII art AND XML description.

### Step F1: Create ASCII Art (Required)

Generate ASCII representation using these character sets:

**USE** (JetBrains Mono OK):
`←→↑↓↔↕↖↗↘↙` `┌─┬┐│├┼┤└┘` `╔═╦╗║╠╬╣╚╝` `╭╮╰╯` `┏━┳┓┃┣╋┫┗┛` `░▒▓█▀▄▌▐` `▖▗▘▙▚▛▜▝▞▟` `+-x:=<>` `/\X╱╲╳` `·⋯⋮`

**DONT USE** (broken width):
`⇐⇒⇑⇓⇔⇕` `◀▶▲▼◄►△▽◁▷` `○●◎◉⊙◯⬤◐◑◒◓` `□■▢▣◇◆☆★` `(){}[]<>⟨⟩〈〉` `∈⊂⊃∩∪∧∨¬⊕⊗` `•◦✓✗☐☑☒❖✦✧‣⁃➔➜➤➡⌒⌓◜◝◞◟…`

````
**Figure [N]: [Caption from original]**

```ascii
[ASCII art representation here]
```
````

### Step F2: Compare and Describe (Required)

After creating ASCII, compare with original image and add description using standard markdown inside XML tags:

```
<transcribe_figure>
- ASCII captures: What the ASCII diagram successfully represents
- ASCII misses: Visual elements that cannot be shown in ASCII
- Colors:
  - [color name] - what it represents
  - [color name] - what it represents
- Layout: Spatial arrangement, panels, relative positions
- Details: Fine details, textures, gradients, 3D effects
- Data: Specific values, measurements, or quantities visible
</transcribe_figure>
```

### Step F3: Example

Original: A flowchart with colored boxes showing data flow

```markdown
**Figure 3: Data Processing Pipeline**

```ascii
┌─────────┐     ┌─────────┐     ┌─────────┐
│  Input  │────>│ Process │────>│ Output  │
└─────────┘     └─────────┘     └─────────┘
     │               │               │
     v               v               v
┌─────────┐     ┌─────────┐     ┌─────────┐
│  Log A  │     │  Log B  │     │  Log C  │
└─────────┘     └─────────┘     └─────────┘
```

<transcribe_figure>
- ASCII captures: Box structure, flow direction, hierarchical logging
- ASCII misses: Rounded corners, shadow effects, icon inside Process box
- Colors:
  - Blue - input/output stages
  - Green - processing stage
  - Gray - logging components
- Layout: Horizontal flow left-to-right, vertical drops to log boxes
- Details: Process box contains gear icon; arrows have gradient fill
- Data: None
</transcribe_figure>
```

### Figure Protocol Rules

1. **NO EXCEPTIONS**: Every figure gets ASCII + XML, even photographs
2. **Photographs**: ASCII shows composition/layout; XML describes subject matter
3. **Graphs/Charts**: ASCII shows axes and trend; XML provides data points
4. **Network Diagrams**: ASCII shows topology; XML describes node colors and link types
5. **3D Visualizations**: ASCII shows 2D projection; XML describes depth and perspective

### 5c. Append to output file IMMEDIATELY
Do not wait until end. Write after each chunk.

### 5d. Update progress marker
```markdown
<!-- TRANSCRIPTION PROGRESS
Chunk: 2 of 5
Pages completed: 4 of 20
-->
```

### 5e. Continue with next chunk
Repeat until all pages processed.

## Step 6: Finalize

1. Remove progress markers
2. Generate/verify Table of Contents
3. Log metadata to session NOTES.md (source, pages, figures, date) per core-conventions.md

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

## Parts

1. [Part01](./[DocName]_Part01.md) - Pages 1-20: [Chapter names]
2. [Part02](./[DocName]_Part02.md) - Pages 21-40: [Chapter names]
...
```

## Verification

After transcription, run `/verify` to:
1. Compare page count
2. Check all sections present
3. Verify all figures have BOTH:
   - ASCII art block (` ```ascii `)
   - XML description block (`<transcribe_figure>`)
4. Cross-check text accuracy
5. Validate XML tags are well-formed

## Best Practices

1. **4 pages max per call** - Prevents context overflow and ensures quality
2. **Write immediately** - Append to file after each chunk
3. **Track progress** - Use progress markers for resumability
4. **300 DPI for PDFs** - Higher quality for accurate transcription
5. **Keep source images** - Required for `/verify`
6. **No omissions** - Every piece of content must be transcribed
7. **ASCII + XML for figures** - Every figure requires both ASCII art and `<transcribe_figure>` XML block
