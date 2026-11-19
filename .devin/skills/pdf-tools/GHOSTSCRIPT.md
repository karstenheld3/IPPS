# Ghostscript Guide

Goal: The agent runs Ghostscript (`gswin64c.exe`) in PowerShell and never gets the error "Device 'pdfwrite' requires an output file but no file was specified", silent no-output runs, or wrong sizes.

Binary: `[SKILL_TOOLS_FOLDER]/gs/bin/gswin64c.exe` (console build). Never use `gswin64.exe` (opens a GUI window). All `powershell` examples below run by the test suite `_test/test-pdf-tools.py` (`test_doc_examples_ghostscript_md`).

## MUST-NOT-FORGET

- PowerShell breaks unquoted `-name=value` arguments: it splits at the first `.` (`-dCompatibilityLevel=1.4` becomes `-dCompatibilityLevel=1` plus `.4`) and does NOT expand `$variables` inside them. Quote every such argument: `"-sOutputFile=$out"`, or use an argument array and `& $gs @gsArgs`
- Ghostscript reads arguments left to right. Put all options (`-sDEVICE=`, `-sOutputFile=`, `-d...`) BEFORE the input file. A stray argument (like `.4`) is taken as an input file and opens the device before `-sOutputFile=` is seen: that is the reported error
- Exit code 0 is not success: wrong or missing password, unreadable input, and similar errors print `**** Error` and still exit 0 with an empty output PDF. After every run: check the output file exists, `pdfinfo` shows the expected `Pages:`, and the output text has no `**** Error`
- Never write `-sOutputFile=` to an original. Use a new `[NAME]_vNN.pdf` name in the same folder. A size limit is an upper bound: try `/printer`, then `/ebook`, then `/screen`; stop at the first result below the limit
- Always pass `-dNOPAUSE -dBATCH` (or use `-o out.pdf`, which implies both). Add `-dQUIET` to drop the banner
- Long or complex command lines: write the arguments one per line into a text file and run `& $gs '@args.txt'` (quote it: unquoted `@args.txt` is PowerShell splatting)
- Do not type long `gswin64c.exe` lines inline in the agent terminal; use a `.ps1` script file (see Method 2) so quoting is exactly what you wrote

## Root cause of the reported error

- Reproduced 2026-11-19 with pwsh 7.5.0 [TESTED]; known PowerShell bug PowerShell/PowerShell#6291 (unquoted argument starting with `-` is split at the first `.`) [VERIFIED]
- Every failed variant of the report (`-sOutputFile=`, `"-sOutputFile=..."`, `#`, `-o`) also contained an unquoted `-dCompatibilityLevel=1.4`: the `.4` came before the output option
- Unquoted `-sOutputFile=$out` passes the literal text `$out`; Ghostscript then writes a file named `$out` into the current folder and exits 0
- File names with umlauts, spaces, `!`, `(`, `;`, `&`, `,`, `'`, `#` are NOT a problem for Ghostscript when the argument is passed as one quoted token [TESTED]

## Setup

`Invoke-Gs` adds `-dNOPAUSE -dBATCH -dQUIET`, takes the arguments as an array (no PowerShell parsing problem), writes stderr to a file (never `2>&1`), and throws on a non-zero exit code or any `**** Error` line. Paste it once per script. Every recipe below uses it.

```powershell
# setup
$tools = "../.tools"
$gs = "$tools/gs/bin/gswin64c.exe"
$poppler = "$tools/poppler/Library/bin"
$qpdf = "$tools/qpdf/bin/qpdf.exe"
function Invoke-Gs([string[]]$Arguments) {
  $text = & $gs -dNOPAUSE -dBATCH -dQUIET @Arguments 2> gs-errors.txt
  $all = (@($text) + @(Get-Content -LiteralPath gs-errors.txt -ErrorAction SilentlyContinue)) -join "`n"
  Remove-Item -LiteralPath gs-errors.txt -Force -ErrorAction SilentlyContinue
  if ($LASTEXITCODE -ne 0 -or $all -match '\*\*\*\* Error|Unrecoverable') { throw "Ghostscript failed (exit $LASTEXITCODE): $all" }
  return $all
}
function Get-PdfPages([string]$Path) { return [int](((& "$poppler/pdfinfo.exe" $Path | Select-String "^Pages:").Line -split "\s+")[1]) }
```

## Method 1: quoted tokens (short commands)

```powershell
$out = "output.pdf"
& $gs -sDEVICE=pdfwrite "-dCompatibilityLevel=1.4" -dPDFSETTINGS=/ebook -dNOPAUSE -dBATCH -dQUIET "-sOutputFile=$out" input.pdf
& "$poppler/pdfinfo.exe" $out | Select-String "Pages:"
```

## Method 2: argument array (recommended in scripts)

```powershell
$in = "input.pdf"
$out = "output.pdf"
$gsArgs = @("-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", "-dPDFSETTINGS=/ebook", "-dNOPAUSE", "-dBATCH", "-dQUIET", "-sOutputFile=$out", $in)
& $gs @gsArgs
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $out)) { throw "Ghostscript failed: exit $LASTEXITCODE" }
& "$poppler/pdfinfo.exe" $out | Select-String "Pages:"
```

## Method 3: argument file (long command lines)

```powershell
Set-Content -LiteralPath args.txt -Value @("-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", "-dPDFSETTINGS=/screen", "-dNOPAUSE", "-dBATCH", "-dQUIET", "-sOutputFile=small.pdf", "input.pdf")
& $gs '@args.txt'
& "$poppler/pdfinfo.exe" small.pdf | Select-String "Pages:"
```

## Recipes

`input.pdf` is the file to process. Output goes next to it unless stated. Each recipe is a tested example.

### Reduce file size with a preset

`-dPDFSETTINGS` presets: `/screen` 72 DPI (smallest), `/ebook` 150 DPI, `/printer` 300 DPI, `/prepress` 300 DPI color-preserving, `/default`. Images are downsampled only when their resolution is above 1.5 times the target DPI.

```powershell
$null = Invoke-Gs "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", "-dPDFSETTINGS=/ebook", "-sOutputFile=small.pdf", "input.pdf"
"{0} -> {1} bytes, {2} pages" -f (Get-Item input.pdf).Length, (Get-Item small.pdf).Length, (Get-PdfPages small.pdf)
```

### Reach a size limit (example: under 800 KB)

```powershell
$limit = 800KB
foreach ($preset in "ebook", "screen") {
  $null = Invoke-Gs "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", "-dPDFSETTINGS=/$preset", "-sOutputFile=limit-$preset.pdf", "input.pdf"
  $size = (Get-Item -LiteralPath "limit-$preset.pdf").Length
  "$preset gives $size bytes"
  if ($size -lt $limit) { Copy-Item -LiteralPath "limit-$preset.pdf" -Destination limited.pdf; break }
}
Test-Path limited.pdf
```

Still too large with `/screen`: lower the DPI further (next recipe), convert to grayscale, or check what uses the space with `pdfimages -list` and `pdffonts`.

### Explicit image resolution and strategy flags

```powershell
$gsArguments = "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", "-dPDFSETTINGS=/screen",
  "-dDownsampleColorImages=true", "-dColorImageResolution=50", "-dDownsampleGrayImages=true", "-dGrayImageResolution=50",
  "-dDownsampleMonoImages=true", "-dMonoImageResolution=50", "-dColorImageDownsampleType=/Bicubic",
  "-dDetectDuplicateImages=true", "-dCompressFonts=true", "-dSubsetFonts=true", "-dConvertCMYKImagesToRGB=true",
  "-sOutputFile=dpi50.pdf", "input.pdf"
$null = Invoke-Gs $gsArguments
Get-PdfPages dpi50.pdf
```

### Convert to grayscale

```powershell
$null = Invoke-Gs "-sDEVICE=pdfwrite", "-sColorConversionStrategy=Gray", "-dProcessColorModel=/DeviceGray", "-sOutputFile=gray.pdf", "input.pdf"
& "$poppler/pdfimages.exe" -list gray.pdf
```

### Extract pages, merge, fit to A4

`-dFirstPage`/`-dLastPage` give a range; `-sPageList=1,3` gives a list (Ghostscript 10). Several input files in one call are merged. Paper size default is US Letter; force A4 with `-sPAPERSIZE=a4 -dFIXEDMEDIA -dPDFFitPage`.

```powershell
$null = Invoke-Gs "-sDEVICE=pdfwrite", "-dFirstPage=2", "-dLastPage=3", "-sOutputFile=pages-2-3.pdf", "input.pdf"
$null = Invoke-Gs "-sDEVICE=pdfwrite", "-sPageList=1,3", "-sOutputFile=pages-1-3.pdf", "input.pdf"
$null = Invoke-Gs "-sDEVICE=pdfwrite", "-sOutputFile=merged.pdf", "input.pdf", "input2.pdf"
$null = Invoke-Gs "-sDEVICE=pdfwrite", "-sPAPERSIZE=a4", "-dFIXEDMEDIA", "-dPDFFitPage", "-sOutputFile=a4.pdf", "input.pdf"
"{0} {1} {2}" -f (Get-PdfPages pages-2-3.pdf), (Get-PdfPages merged.pdf), (& "$poppler/pdfinfo.exe" a4.pdf | Select-String "Page size")
```

### Render to images and extract text

`%03d` in the output name is replaced by the page number. Doubling the percent sign (`%%`) writes a literal percent sign into a file name.

```powershell
$null = Invoke-Gs "-sDEVICE=png16m", "-r150", "-dTextAlphaBits=4", "-dGraphicsAlphaBits=4", "-sOutputFile=page-%03d.png", "input.pdf"
$null = Invoke-Gs "-sDEVICE=jpeg", "-dJPEGQ=80", "-r100", "-dFirstPage=1", "-dLastPage=1", "-sOutputFile=first.jpg", "input.pdf"
$null = Invoke-Gs "-sDEVICE=txtwrite", "-sOutputFile=text.txt", "input.pdf"
(Get-ChildItem page-*.png).Count
Select-String -Path text.txt -Pattern "Alpha"
```

### Set title and author

The `pdfmark` code must come AFTER the input file; before it, the file's own metadata overwrites it.

```powershell
$null = Invoke-Gs "-sDEVICE=pdfwrite", "-sOutputFile=titled.pdf", "input.pdf", "-c", "[ /Title (New Title) /Author (New Author) /DOCINFO pdfmark"
& "$poppler/pdfinfo.exe" titled.pdf | Select-String "Title|Author"
```

### Passwords

```powershell
$null = Invoke-Gs "-sDEVICE=pdfwrite", "-sPDFPassword=userpw", "-sOutputFile=opened.pdf", "encrypted.pdf"
$null = Invoke-Gs "-sDEVICE=pdfwrite", "-sOwnerPassword=owner1", "-sUserPassword=user1", "-dEncryptionR=3", "-dKeyLength=128", "-sOutputFile=locked.pdf", "input.pdf"
& "$poppler/pdfinfo.exe" -upw user1 locked.pdf | Select-String "Encrypted"
```

A missing or wrong password makes Ghostscript print `**** This file requires a password for access` or `Password did not work`, exit 0, and write an empty PDF. `Invoke-Gs` turns that into an exception.

### Embed fonts, remove images or text

Standard fonts (Helvetica, Courier, Times) stay unembedded unless `/NeverEmbed` is emptied.

```powershell
$null = Invoke-Gs "-sDEVICE=pdfwrite", "-dEmbedAllFonts=true", "-dSubsetFonts=true", "-sOutputFile=embedded.pdf", "-c", "<< /NeverEmbed [ ] >> setdistillerparams", "-f", "input.pdf"
$null = Invoke-Gs "-sDEVICE=pdfwrite", "-dFILTERIMAGE", "-sOutputFile=no-images.pdf", "input.pdf"
$null = Invoke-Gs "-sDEVICE=pdfwrite", "-dFILTERTEXT", "-sOutputFile=no-text.pdf", "input.pdf"
& "$poppler/pdffonts.exe" embedded.pdf
```

## Quirks and messages

- `Device 'pdfwrite' requires an output file but no file was specified`: an unquoted argument was split at a `.`, or `-sOutputFile=` stands after the input file, or it is missing. Fix: quoted tokens or `Invoke-Gs`
- `**** Error: ...` with exit code 0: Ghostscript continued after an error; the output is incomplete. Check the output file and page count
- `Syntax Error: No display font for 'Symbol'` from Poppler tools: warning for unembedded fonts, harmless, exit code 0
- `-dQUIET` hides the banner only; errors still print
- `-o out.pdf` is the short form of `-dBATCH -dNOPAUSE -sOutputFile=out.pdf`
- Default page size is US Letter (612 x 792 pt), not A4
- `-sOutputFile=` with `%` starts a page-number template: write `%%` for a literal percent sign
- Unsupported without extra setup: PDF/A output needs an ICC profile and `PDFA_def.ps`; OCR devices (`pdfocr8`) need Tesseract language data

## Sources

- `[SKILL_TOOLS_FOLDER]/gs/doc/src/Use.rst` - local Ghostscript 10.06.0 documentation: output files, `-o`, `%d` templates, argument order, `@file`, `-c`/`-f`, `-sPageList`, `-dSAFER` [VERIFIED]
- `[SKILL_TOOLS_FOLDER]/gs/doc/src/VectorDevices.rst` - pdfwrite parameters and `-dPDFSETTINGS` presets [VERIFIED]
- https://github.com/PowerShell/PowerShell/issues/6291 - PowerShell splits unquoted arguments that start with `-` at the first `.` [VERIFIED]
- `_test/test-pdf-tools.py` in this folder - every behavior above marked with a test [TESTED 2026-11-19, Ghostscript 10.06.0, PowerShell 7.5.0, Windows]
