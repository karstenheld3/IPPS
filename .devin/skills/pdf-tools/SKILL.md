---
name: pdf-tools
description: Apply when converting, processing, or analyzing PDF files with the command line tools Poppler, QPDF, Ghostscript, 7-Zip or the skill scripts
---

# PDF Tools Guide

Rules and usage for PDF tools in `[WORKSPACE_FOLDER]/../.tools/` (`[SKILL_TOOLS_FOLDER]`). Every `powershell` example in this file and in `GHOSTSCRIPT.md` is executed by `_test/test-pdf-tools.py`; copy them as they are. Examples use `input.pdf`, `input2.pdf`, `encrypted.pdf` (password `userpw`), `damaged.pdf`, and `notes.txt` in the current folder.

## MUST-NOT-FORGET

- PowerShell splits an unquoted argument that starts with `-` at the first `.` and does not expand `$variables` inside it. Quote every `-option=value` argument (`"-sOutputFile=$out"`, `"--show-attachment=notes.txt"`, `"-o$folder"`) or pass an argument array (`& $tool @toolArguments`). Unquoted forms produce the Ghostscript error "requires an output file", missing files, and files named `$out`
- Ghostscript: read `GHOSTSCRIPT.md` before the first call; use `Invoke-Gs` from it. Never type long `gswin64c.exe` lines inline in the agent terminal
- Exit codes lie: QPDF exits 3 for "succeeded with warnings" (output is usable); Ghostscript exits 0 after `**** Error` (output is empty or incomplete). Verify the output file and `pdfinfo` `Pages:`
- Never lose an original: before changing a user file, copy it to `[NAME]_vNN.pdf` in the same folder (`report_v01.pdf`). No backup folders. Keep it until the user confirms the goal
- A size limit ("under 800 KB") is an upper bound: try `compress-pdf.py --compression low`, then `medium`, then `high`; stop at the first result below the limit and report size and setting
- Check existing conversions before converting; default output of `convert-pdf-to-jpg.py`: `../.tools/_pdf_to_jpg_converted/[PDF_FILENAME]/`
- DPI: 120 for screen and transcription, 300 for OCR, 72 for archive and web
- Two-pass downsizing: Ghostscript (images) then QPDF (structure)
- Paths with spaces, umlauts, `!`, or parentheses are fine when passed as one quoted argument
- After a tool update or a skill edit run `& $python "$skillDirectory/_test/test-pdf-tools.py"` (about 1-2 minutes, see Tests)

## Choose the tool

- Compress or downsize: `compress-pdf.py` (automatic strategy), `downsize-pdf-images.py` (fixed DPI), Ghostscript (custom flags), QPDF (structure only)
- Pages to images for vision analysis: `convert-pdf-to-jpg.py`; other formats: `pdftoppm`, `pdftocairo`
- Text: `pdftotext`; HTML: `pdftohtml`; PostScript: `pdftops`, `pdftocairo -ps`
- Facts: `pdfinfo` (pages, size, metadata), `pdfimages -list`, `pdffonts`
- Merge, split, rotate, encrypt, decrypt, repair, linearize: `qpdf`; simple merge or split: `pdfunite`, `pdfseparate`
- Embedded files: `pdfattach`, `pdfdetach`, `qpdf --add-attachment`
- Archives: `7z` (also extracts the NSIS installer of Ghostscript)

## Setup block

The examples assume this block. `Invoke-Qpdf` accepts exit code 0 and 3, throws otherwise.

```powershell
# setup
$tools = "../.tools"
$skillDirectory = ".devin/skills/pdf-tools"
$poppler = "$tools/poppler/Library/bin"
$qpdf = "$tools/qpdf/bin/qpdf.exe"
$gs = "$tools/gs/bin/gswin64c.exe"
$sevenZip = "$tools/7z/7z.exe"
$python = "$tools/llm-venv/Scripts/python.exe"
function Invoke-Qpdf([string[]]$Arguments) {
  $PSNativeCommandUseErrorActionPreference = $false
  & $qpdf @Arguments
  if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne 3) { throw "qpdf failed: exit $LASTEXITCODE" }
  $global:LASTEXITCODE = 0
}
function Get-PdfPages([string]$Path) { return [int](((& "$poppler/pdfinfo.exe" $Path | Select-String "^Pages:").Line -split "\s+")[1]) }
```

## Skill scripts

Scripts use Python argument lists, so they are immune to the PowerShell quoting problem. Syntax:

```text
python convert-pdf-to-jpg.py <input.pdf> [--output <dir>] [--dpi <dpi>] [--pages <1|1-3|all>]
python compress-pdf.py <input.pdf> [--compression high|medium|low] [--output <file.pdf>]
python downsize-pdf-images.py <input.pdf> [--output <dir>] [--dpi <dpi>] [--preset screen|ebook|printer|prepress]
```

### convert-pdf-to-jpg.py

Writes `[output]/[PDF_FILENAME]/[PDF_FILENAME]_page001.jpg` (one subfolder per PDF, default DPI 120, quality 90). Exit 1 on a missing or unreadable PDF.

```powershell
& $python "$skillDirectory/convert-pdf-to-jpg.py" input.pdf --output jpgs --dpi 60 --pages 1-2
Get-ChildItem jpgs/input
```

### compress-pdf.py

Analyzes the PDF, tries strategies until the target is reached: `high` 50 percent reduction (72 DPI), `medium` 25 percent (150 DPI), `low` 10 percent (300 DPI). Default output `../.tools/_pdf_output/[PDF_FILENAME]_compressed.pdf`; `--output` creates missing folders. The result can be larger than the input when the PDF is already optimized: compare sizes.

```powershell
& $python "$skillDirectory/compress-pdf.py" input.pdf --compression high --output compressed/input-high.pdf
"{0} -> {1} bytes" -f (Get-Item input.pdf).Length, (Get-Item compressed/input-high.pdf).Length
```

### downsize-pdf-images.py

Direct Ghostscript wrapper. `--preset` overrides `--dpi`. Output `[output]/[PDF_FILENAME]_[DPI]dpi.pdf` (`printer` and `prepress` both write `_300dpi`).

```powershell
& $python "$skillDirectory/downsize-pdf-images.py" input.pdf --output downsized --preset screen
& $python "$skillDirectory/downsize-pdf-images.py" input.pdf --output downsized --dpi 100
Get-ChildItem downsized
```

## Poppler tools

Location: `../.tools/poppler/Library/bin/` (version 24.08.0). All tools: `-h` prints usage, `-upw <password>` / `-opw <password>` open encrypted files, exit code 0 = success, 1 = cannot open the PDF, 2 = cannot write the output, 99 = command line error. "Syntax Error: No display font for ..." on stderr is a harmless warning for PDFs with unembedded standard fonts.

### pdfinfo - facts about a PDF

```powershell
& "$poppler/pdfinfo.exe" input.pdf
& "$poppler/pdfinfo.exe" -f 1 -l 2 -box input.pdf
& "$poppler/pdfinfo.exe" -upw userpw encrypted.pdf
& "$poppler/pdfinfo.exe" -dests -url input.pdf
```

Other options: `-meta` (XMP), `-custom`, `-isodates`, `-rawdates`, `-js`, `-struct`, `-enc UTF-8`, `-listenc`. Page size shows the paper name (`letter`, `A4`).

### pdftotext - extract text

Output file `-` writes to stdout; without an output name the text goes to `[PDF_FILENAME].txt`. Pages are separated by a form feed unless `-nopgbrk`.

```powershell
& "$poppler/pdftotext.exe" -layout -f 1 -l 3 input.pdf text.txt
& "$poppler/pdftotext.exe" -enc UTF-8 -nopgbrk input.pdf -
& "$poppler/pdftotext.exe" -bbox-layout -f 1 -l 1 input.pdf words.html
& "$poppler/pdftotext.exe" -tsv -f 1 -l 1 input.pdf words.tsv
```

Other options: `-raw` (content stream order), `-fixed <pitch>`, `-eol unix|dos|mac`, `-htmlmeta`, `-x -y -W -H` (crop area in pixels at `-r` DPI, default 72), `-cropbox`, `-nodiag`, `-colspacing <fp>`. A scanned PDF without a text layer gives empty pages: render to images and use OCR instead.

### pdftoppm - render pages to PPM, PNG, JPEG, TIFF

Output name is `[prefix]-[page].[ext]`; the page number is zero-padded to the width of the page count (3 pages: `page-1.png`, 12 pages: `page-01.png`). `-singlefile` writes `[prefix].[ext]`. Default resolution is 150 DPI.

```powershell
& "$poppler/pdftoppm.exe" -png -r 150 -f 1 -l 2 input.pdf page
& "$poppler/pdftoppm.exe" -jpeg -jpegopt "quality=80,progressive=y" -scale-to 1200 -singlefile -f 1 input.pdf thumbnail
& "$poppler/pdftoppm.exe" -png -r 72 -x 0 -y 0 -W 300 -H 200 -singlefile -f 1 input.pdf cropped
& "$poppler/pdftoppm.exe" -gray -r 100 -o input.pdf odd-pages
Get-ChildItem *.png, *.jpg, *.pgm | Select-Object Name
```

Other options: `-tiff -tiffcompression lzw`, `-mono`, `-e` (even pages), `-sep <char>`, `-forcenum`, `-scale-to-x/-scale-to-y`, `-rx/-ry`, `-sz`, `-cropbox`, `-hide-annotations`, `-aa/-aaVector no`, `-progress`, `-q`.

### pdftocairo - render to PNG, JPEG, TIFF, SVG, PDF, PS, EPS

Same page and naming options as `pdftoppm`. `-pdf`, `-ps`, `-eps`, `-svg` write vector output to the given file name (`-eps`, `-svg` take one page: use `-f`/`-l`).

```powershell
& "$poppler/pdftocairo.exe" -png -r 100 -f 1 -l 1 -singlefile -transp input.pdf cairo-page
& "$poppler/pdftocairo.exe" -svg -f 1 -l 1 input.pdf page1.svg
& "$poppler/pdftocairo.exe" -pdf -f 1 -l 2 input.pdf first-two-pages.pdf
& "$poppler/pdftocairo.exe" -ps -paper A4 input.pdf print.ps
```

### pdftohtml, pdftops

```powershell
& "$poppler/pdftohtml.exe" -q -s -noframes -i input.pdf all-pages
& "$poppler/pdftohtml.exe" -q -xml -f 1 -l 1 input.pdf layout
& "$poppler/pdftops.exe" -level3 -f 1 -l 1 input.pdf page1.ps
& "$poppler/pdftops.exe" -eps -f 1 -l 1 input.pdf page1.eps
```

`pdftohtml -s` writes `[name]-html.html` for the single document form; `-c` complex mode and `-fmt png|jpg` write page images next to the HTML. `pdftops` options: `-level1|2|3`, `-paper`, `-expand`, `-noshrink`, `-nocenter`, `-origpagesizes`, `-rasterize always|never`, `-r <dpi>`.

### pdfimages and pdffonts - what is inside

`pdfimages -list` shows page, number, type, pixel size, color, bits, encoding, DPI, size; use it before compressing. Extraction writes `[prefix]-[number].[ext]` (`-p` adds the page number); `-j` keeps JPEG data as `.jpg`, `-all` keeps every format native.

```powershell
& "$poppler/pdfimages.exe" -list input.pdf
(& "$poppler/pdfimages.exe" -list input.pdf | Select-Object -Skip 2).Count
& "$poppler/pdfimages.exe" -png -p input.pdf extracted
& "$poppler/pdfimages.exe" -all -f 2 -l 2 input.pdf native
& "$poppler/pdffonts.exe" input.pdf
```

### pdfseparate and pdfunite - split and merge

`pdfseparate` needs `%d` (page number) or `%03d` in the output pattern when the file has more than one page; otherwise it fails. `pdfunite` takes input files in order and the output last.

```powershell
& "$poppler/pdfseparate.exe" -f 1 -l 3 input.pdf "page-%d.pdf"
& "$poppler/pdfunite.exe" page-3.pdf page-1.pdf input2.pdf united.pdf
Get-PdfPages united.pdf
```

### pdfattach and pdfdetach - embedded files

Known defect: `pdfdetach -savefile <name>` always fails with "Invalid file name" (exit 99) in this build. Use `-list` and `-save <number>` or `-saveall` (the suite guards this with `test_pdfdetach_savefile_known_defect`).

```powershell
& "$poppler/pdfattach.exe" input.pdf notes.txt with-notes.pdf
& "$poppler/pdfdetach.exe" -list with-notes.pdf
& "$poppler/pdfdetach.exe" -save 1 -o saved-notes.txt with-notes.pdf
New-Item -ItemType Directory -Force extracted | Out-Null
Push-Location extracted; & "$poppler/pdfdetach.exe" -saveall ../with-notes.pdf; Pop-Location
```

## QPDF

Location: `../.tools/qpdf/bin/` (`qpdf.exe` 12.3.0, `fix-qdf.exe`, `zlib-flate.exe`). Examples pass arguments as arrays through `Invoke-Qpdf`. Exit codes: 0 success, 2 error (nothing written), 3 success with warnings (output written; a damaged input always gives 3). Manual: https://qpdf.readthedocs.io

### Inspect

```powershell
Invoke-Qpdf "--check", "input.pdf"
Invoke-Qpdf "--show-npages", "input.pdf"
Invoke-Qpdf "--show-encryption", "--password=userpw", "encrypted.pdf"
Invoke-Qpdf "--json=latest", "--json-key=pages", "input.pdf"
```

`--is-encrypted` exits 0 for encrypted, 2 for plain files (not an error); `--requires-password` exits 0 when a password is needed.

### Merge, select, reorder, rotate, split

Page ranges: `1-3`, `3,1`, `z` (last), `r1` (last page counted from the end), `1-z:odd`, `1-z:even`. `.` means the main input file. Several inputs: list files, each optionally followed by its range.

```powershell
Invoke-Qpdf "--empty", "--pages", "input.pdf", "input2.pdf", "--", "merged.pdf"
Invoke-Qpdf "input.pdf", "--pages", ".", "1-2", "--", "first-two.pdf"
Invoke-Qpdf "input.pdf", "--pages", ".", "3,1", "--", "reordered.pdf"
Invoke-Qpdf "input.pdf", "--pages", ".", "1-z:odd", "--", "odd-pages.pdf"
Invoke-Qpdf "input.pdf", "--rotate=+90:1", "rotated.pdf"
Invoke-Qpdf "--split-pages=1", "input.pdf", "split.pdf"
Invoke-Qpdf "--empty", "--pages", "encrypted.pdf", "--password=userpw", "1-2", "--", "from-encrypted.pdf"
Get-ChildItem split-*.pdf | Select-Object Name
```

### Encrypt and decrypt

qpdf 12 refuses RC4 (128-bit and weaker) unless `--allow-weak-crypto`; use 256-bit, or `--use-aes=y` with 128. A wrong password gives exit 2 and writes nothing.

```powershell
Invoke-Qpdf "--encrypt", "userpw", "ownerpw", "256", "--", "input.pdf", "locked.pdf"
Invoke-Qpdf "--encrypt", "", "ownerpw", "256", "--print=none", "--modify=none", "--", "input.pdf", "restricted.pdf"
Invoke-Qpdf "--decrypt", "--password=userpw", "encrypted.pdf", "decrypted.pdf"
Get-PdfPages decrypted.pdf
```

### Repair, replace in place, linearize, optimize

`--replace-input` overwrites the input file (write a copy first when the original matters). A damaged file is rebuilt and reported with exit 3.

```powershell
Invoke-Qpdf "damaged.pdf", "repaired.pdf"
Invoke-Qpdf "--replace-input", "--linearize", "input.pdf"
Invoke-Qpdf "--check-linearization", "input.pdf"
Invoke-Qpdf "--object-streams=generate", "--compress-streams=y", "--recompress-flate", "--compression-level=9", "input2.pdf", "optimized.pdf"
Get-PdfPages repaired.pdf
```

Other options: `--optimize-images`, `--flatten-annotations=screen`, `--flatten-rotation`, `--coalesce-contents`, `--normalize-content=y`, `--remove-restrictions`, `--stream-data=compress|uncompress|preserve`, `--object-streams=disable|preserve|generate`, `--collate`, `--underlay`.

### Attachments, overlay, argument files

`@file` reads arguments, one per line; quote it in PowerShell (`'@args.txt'`) because unquoted `@name` is splatting.

```powershell
Invoke-Qpdf "input.pdf", "--add-attachment", "notes.txt", "--", "attached.pdf"
Invoke-Qpdf "--list-attachments", "attached.pdf"
Invoke-Qpdf "--show-attachment=notes.txt", "attached.pdf"
Invoke-Qpdf "input.pdf", "--overlay", "input2.pdf", "--from=1", "--to=1-2", "--", "overlay.pdf"
Set-Content -LiteralPath args.txt -Value @("input.pdf", "--pages", ".", "2", "--", "second-page.pdf")
Invoke-Qpdf '@args.txt'
```

### fix-qdf and zlib-flate

`qpdf --qdf` writes a text-editable PDF; after editing in a UTF-8 safe editor `fix-qdf` repairs offsets and stream lengths. `zlib-flate` compresses or uncompresses raw zlib streams (stdin to stdout); use `Start-Process` redirection, because PowerShell pipes corrupt binary data.

```powershell
Invoke-Qpdf "--qdf", "--object-streams=disable", "input.pdf", "edit.qdf"
& "$tools/qpdf/bin/fix-qdf.exe" edit.qdf fixed.pdf
Set-Content -LiteralPath raw.txt -Value ("zlib " * 500)
Start-Process -FilePath "$tools/qpdf/bin/zlib-flate.exe" -ArgumentList "-compress=9" -RedirectStandardInput raw.txt -RedirectStandardOutput packed.bin -NoNewWindow -Wait
Start-Process -FilePath "$tools/qpdf/bin/zlib-flate.exe" -ArgumentList "-uncompress" -RedirectStandardInput packed.bin -RedirectStandardOutput unpacked.txt -NoNewWindow -Wait
"{0} -> {1} -> {2} bytes" -f (Get-Item raw.txt).Length, (Get-Item packed.bin).Length, (Get-Item unpacked.txt).Length
```

## Ghostscript

Location: `../.tools/gs/bin/gswin64c.exe` (10.06.0). Full guide with the quoting rules, `Invoke-Gs`, and recipes (size limits, page ranges, rendering, passwords, metadata, fonts): `GHOSTSCRIPT.md` in this folder. Minimal safe call (argument array, options before the input file, output checked):

```powershell
$gsArguments = "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", "-dPDFSETTINGS=/ebook", "-dNOPAUSE", "-dBATCH", "-dQUIET", "-sOutputFile=ebook.pdf", "input.pdf"
& $gs @gsArguments
Get-PdfPages ebook.pdf
```

Presets (`-dPDFSETTINGS`): `/screen` 72 DPI, `/ebook` 150 DPI, `/printer` 300 DPI, `/prepress` 300 DPI color-preserving.

## 7-Zip

Location: `../.tools/7z/7z.exe` (24.08). Required to unpack the Ghostscript NSIS installer (`7z x -y "-o$folder" installer.exe`); the standalone `7za.exe` cannot. Commands: `a` add, `x` extract with paths, `e` extract flat, `l` list, `t` test, `d` delete, `u` update, `h` hash, `i` formats. Always add `-y` (no prompts) and `-bd` (no progress bar); quote every `-o`/`-p`/`-m` argument.

```powershell
& $sevenZip a -tzip "-mx9" -bd -y archive.zip input.pdf notes.txt
& $sevenZip l archive.zip
& $sevenZip t archive.zip
& $sevenZip x -y -bd "-oextracted" archive.zip
& $sevenZip e -y -bd "-oflat" archive.zip notes.txt
& $sevenZip a -tzip "-pSecret123" "-mem=AES256" -bd -y secure.zip input.pdf
& $sevenZip h "-scrcSHA256" input.pdf
```

A wrong password makes `t` and `x` exit non-zero; a missing archive exits non-zero.

## Workflows

### Two-pass downsizing (maximum compression)

Pass 1 Ghostscript shrinks images, pass 2 QPDF optimizes structure. Check the page count and the sizes at the end.

```powershell
$gsArguments = "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", "-dPDFSETTINGS=/screen", "-dDetectDuplicateImages=true", "-dCompressFonts=true",
  "-dSubsetFonts=true", "-dNOPAUSE", "-dBATCH", "-dQUIET", "-sOutputFile=pass1.pdf", "input.pdf"
& $gs @gsArguments
Invoke-Qpdf "--linearize", "--object-streams=generate", "--compress-streams=y", "--recompress-flate", "pass1.pdf", "pass2.pdf"
Remove-Item pass1.pdf
"{0} -> {1} bytes, {2} pages" -f (Get-Item input.pdf).Length, (Get-Item pass2.pdf).Length, (Get-PdfPages pass2.pdf)
```

### Analyze before optimizing

```powershell
& "$poppler/pdfinfo.exe" input.pdf
& "$poppler/pdfimages.exe" -list input.pdf
& "$poppler/pdffonts.exe" input.pdf
```

What compresses well (tested on 6 annual reports of 50-100 MB): JPEG2000 images at 200 DPI (77 MB to 4.5 MB with `/screen`), mixed content (about 57 percent), and high-DPI images (above 150 DPI). What does not: PDFs marked `Optimized: yes` (about 10 percent), thousands of tiny UI images (4 percent), image-only PDFs at or below 115 DPI. Presets only downsample images above 1.5 times the target DPI.

## Exit codes and known behavior

- QPDF: 0 ok, 2 error, 3 warnings (usable output); `--is-encrypted` exit 2 means "not encrypted"
- Ghostscript: exit 0 even after `**** Error` (wrong password, unreadable input); check the output
- Poppler: 1 cannot open the PDF (missing file, missing or wrong password), 2 cannot write the output, 99 command line error; PDFs with only owner restrictions (empty user password) open normally
- `pdfdetach -savefile` fails (exit 99); `pdftoppm` and `pdftocairo` default to 150 DPI, `pdftotext -r` to 72
- Default paper size of Ghostscript is US Letter, not A4
- qpdf 12 refuses RC4 without `--allow-weak-crypto`
- PowerShell: quote `-option=value` arguments (see MUST-NOT-FORGET)

## Tests

`_test/test-pdf-tools.py` (kept in the skill, versioned) builds its own fixtures with Ghostscript and QPDF and tests every tool, every script, and every `powershell` example of this file and `GHOSTSCRIPT.md`. Run it after a tool update or a skill edit (about 1-2 minutes; Cascade: through `run-supervised.ps1`).

```text
python .devin/skills/pdf-tools/_test/test-pdf-tools.py [--filter TEXT ...] [--keep] [--verbose] [--work-dir .tmp_DIR]
```

Exit code 0 means no test failed. Sandbox default: `[WORKSPACE_FOLDER]/_agentwork/.tmp_pdftools_test/`.

## Agent-Created Folders

- `.tmp_jpgs/[PDF_NAME]/` - role: jpgs; parent: content folder or working folder; creator: `convert-pdf-to-jpg.py --output .tmp_jpgs/`; content: page images. Rebuildable: re-run the conversion when missing
- `_download_gitignore/compressed/` - role: download (nested); parent: working folder; creator: `compress-pdf.py --output`; content: compressed PDFs
- `_test/` - role: test; parent: this skill folder; creator: maintainers; content: `test-pdf-tools.py`. Kept and versioned
- `_agentwork/.tmp_pdftools_test/` - role: agentwork (nested `.tmp_`); parent: workspace; creator: `_test/test-pdf-tools.py`; content: fixtures and test case folders. Rebuildable agent work, deleted by `/cleanup`
- Defaults of the scripts write into `../.tools/` (outside the repository, not covered by the folder standard)

## Setup

Installation of the tools: `SETUP.md` in this skill folder. Locations: 7-Zip `../.tools/7z/`, Poppler `../.tools/poppler/`, QPDF `../.tools/qpdf/`, Ghostscript `../.tools/gs/`, installers `../.tools/_installer/`, JPG output `../.tools/_pdf_to_jpg_converted/`, PDF output `../.tools/_pdf_output/`.
