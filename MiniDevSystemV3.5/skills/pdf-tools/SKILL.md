---
name: pdf-tools
description: Apply when converting, processing, or analyzing PDF files
---

# PDF Tools Guide

Rules and usage for PDF tools in `[WORKSPACE_FOLDER]/../.tools/`.

## MUST-NOT-FORGET

- Check existing conversions before converting
- Default output: `../.tools/_pdf_to_jpg_converted/[PDF_FILENAME]/`
- Use 120 DPI for screen/transcription, 300 DPI for OCR
- Two-pass downsizing: Ghostscript (images) then QPDF (structure)

## PDF to JPG Conversion

### Script: `DevSystemV2/skills/pdf-tools/convert-pdf-to-jpg.py`

```powershell
python DevSystemV2/skills/pdf-tools/convert-pdf-to-jpg.py invoice.pdf --dpi 200 --pages 1-2
```

- Default output: `../.tools/_pdf_to_jpg_converted/[PDF_FILENAME]/`
- Each PDF gets own subfolder; files named `[PDF_FILENAME]_page001.jpg`, etc.
- Check for existing subfolder to skip re-conversion
- `--output`: Output directory (default: `../.tools/_pdf_to_jpg_converted/`)
- `--dpi`: Resolution (default: 120)
- `--pages`: Page range - "1", "1-3", or "all" (default: all)

## 7-Zip CLI Tools

Location: `../.tools/7z/`

Required to extract Ghostscript NSIS installer (`7za.exe` cannot).

```powershell
& "../.tools/7z/7z.exe" x -y -o"output_folder" "archive.zip"
& "../.tools/7z/7z.exe" x -y -o"output_folder" "installer.exe"   # NSIS
& "../.tools/7z/7z.exe" l "archive.zip"                           # list
```

## Poppler CLI Tools

Location: `../.tools/poppler/Library/bin/`

```powershell
& "../.tools/poppler/Library/bin/pdftoppm.exe" -jpeg -r 150 "input.pdf" "output_prefix"
& "../.tools/poppler/Library/bin/pdftotext.exe" "input.pdf" "output.txt"
& "../.tools/poppler/Library/bin/pdfinfo.exe" "input.pdf"
& "../.tools/poppler/Library/bin/pdfseparate.exe" "input.pdf" "output_%d.pdf"
& "../.tools/poppler/Library/bin/pdfunite.exe" "page1.pdf" "page2.pdf" "merged.pdf"
& "../.tools/poppler/Library/bin/pdfimages.exe" -list "input.pdf"   # page, dims, colorspace, DPI, size
```

## QPDF CLI Tools

Location: `../.tools/qpdf/bin/`

```powershell
& "../.tools/qpdf/bin/qpdf.exe" --empty --pages file1.pdf file2.pdf -- merged.pdf
& "../.tools/qpdf/bin/qpdf.exe" input.pdf --pages . 1-5 -- output.pdf          # extract pages
& "../.tools/qpdf/bin/qpdf.exe" --decrypt --password=secret encrypted.pdf decrypted.pdf
& "../.tools/qpdf/bin/qpdf.exe" --replace-input damaged.pdf                     # repair
& "../.tools/qpdf/bin/qpdf.exe" --linearize input.pdf output.pdf                # optimize for web
```

## Smart PDF Compression Script

### Script: `DevSystemV2/skills/pdf-tools/compress-pdf.py`

```powershell
python DevSystemV2/skills/pdf-tools/compress-pdf.py report.pdf --compression high --output archive.pdf
```

Compression levels:
- **high**: Target 50%+ reduction, aggressive (72 DPI)
- **medium**: Target 25%+ reduction, balanced (150 DPI)
- **low**: Target 10%+ reduction, preserve quality (300 DPI)

Analyzes PDF structure, predicts compression potential, escalates strategies if target not met, reverts if insufficient improvement. Output: `../.tools/_pdf_output/[PDF_FILENAME]_compressed.pdf`

## Simple PDF Downsizing Script

### Script: `DevSystemV2/skills/pdf-tools/downsize-pdf-images.py`

```powershell
python DevSystemV2/skills/pdf-tools/downsize-pdf-images.py input.pdf --dpi 150 --preset ebook
```

- `--output`: Output directory (default: `../.tools/_pdf_output/`)
- `--dpi`: Resolution (default: 150)
- `--preset`: screen (72), ebook (150), printer (300), prepress (300)
- Output: `../.tools/_pdf_output/[PDF_FILENAME]_[DPI]dpi.pdf`

## Ghostscript CLI Tools

Location: `../.tools/gs/bin/`

```powershell
# Compress images
& "../.tools/gs/bin/gswin64c.exe" -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dDownsampleColorImages=true -dColorImageResolution=72 -dDownsampleGrayImages=true -dGrayImageResolution=72 -dDownsampleMonoImages=true -dMonoImageResolution=72 -dNOPAUSE -dQUIET -dBATCH -sOutputFile=output.pdf input.pdf

# Remove all images (text only)
& "../.tools/gs/bin/gswin64c.exe" -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dFILTERIMAGE=true -dNOPAUSE -dQUIET -dBATCH -sOutputFile=output.pdf input.pdf
```

Presets (`-dPDFSETTINGS`): `/screen` (72 DPI), `/ebook` (150), `/printer` (300), `/prepress` (300 color-preserving)

## Two-Pass Downsizing Workflow

### Pass 1: Ghostscript (image compression)
```powershell
& "../.tools/gs/bin/gswin64c.exe" -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dDownsampleColorImages=true -dColorImageResolution=72 -dDownsampleGrayImages=true -dGrayImageResolution=72 -dNOPAUSE -dQUIET -dBATCH -sOutputFile=temp.pdf input.pdf
```

### Pass 2: QPDF (structure optimization)
```powershell
& "../.tools/qpdf/bin/qpdf.exe" --linearize --object-streams=generate --stream-data=compress --compress-streams=y --optimize-images --flatten-annotations=screen temp.pdf output.pdf
Remove-Item temp.pdf
```

## Optimization Strategies

### Aggressive (best for large reductions)
```powershell
cmd /c "& '../.tools/gs/bin/gswin64c.exe' -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dDetectDuplicateImages=true -dCompressFonts=true -dSubsetFonts=true -dConvertCMYKImagesToRGB=true -dColorImageDownsampleType=/Bicubic -dNOPAUSE -dBATCH -sOutputFile=output.pdf input.pdf"
```

### Balanced
```powershell
cmd /c "& '../.tools/gs/bin/gswin64c.exe' -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dDetectDuplicateImages=true -dCompressFonts=true -dSubsetFonts=true -dConvertCMYKImagesToRGB=true -dNOPAUSE -dBATCH -sOutputFile=output.pdf input.pdf"
```

### Structure only (no quality loss)
```powershell
& "../.tools/qpdf/bin/qpdf.exe" --linearize --object-streams=generate --compress-streams=y --recompress-flate input.pdf output.pdf
```

Key flags: `-dDetectDuplicateImages` (dedup), `-dCompressFonts` + `-dSubsetFonts` (font optimization), `-dConvertCMYKImagesToRGB` (smaller colorspace), `-dColorImageDownsampleType=/Bicubic` (quality downsampling)

Compression factors: JPEG2000 compresses dramatically to JPEG; high DPI (200+) benefits most from downsampling; already-optimized PDFs compress less; many small images resist compression.

## Best Practices

1. Analyze first with `pdfimages -list` before optimizing
2. Check existing conversions in `_pdf_to_jpg_converted/`
3. DPI: 72 web/archive, 150 screen, 300 print/OCR
4. Use `--pages` for large PDFs
5. Two-pass for maximum compression: Ghostscript then QPDF

## Setup

See `SETUP.md` in this skill folder.

Tool locations: 7-Zip `../.tools/7z/`, Poppler `../.tools/poppler/`, QPDF `../.tools/qpdf/`, Ghostscript `../.tools/gs/`, JPG output `../.tools/_pdf_to_jpg_converted/`, PDF output `../.tools/_pdf_output/`