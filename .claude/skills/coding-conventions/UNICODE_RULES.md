# Unicode and Encoding Rules

Rules for reading, writing, and passing text so that non-ASCII characters (`é`, `ő`, `ß`, `ø`, `東京`) survive every boundary: file, console, pipe, network, archive.

Read before writing any code that reads or writes files, calls external programs, or processes network responses. Acronyms: BOM = Byte Order Mark, ANSI = Windows system code page, OEM = Windows console code page, NFC / NFD = Unicode Normalization Form C / D (see Core Concepts). Language-specific patterns: `UNICODE_POWERSHELL_EXAMPLES.md`, `UNICODE_PYTHON_EXAMPLES.md`. Repair tool: `repair_mojibake_win-1252.py`.

Verification labels: `[TESTED]` = reproduced locally (Windows PowerShell 5.1.26100, PowerShell 7.5, Python 3.12, Windows-1252 system code page), `[VERIFIED]` = official documentation, specification, or source code, `[REPORTED]` = community source with reproduction (issue tracker, Stack Overflow), not in official documentation.

## Table of Contents

1. [Rule Index](#rule-index)
2. [Core Concepts](#core-concepts)
3. [Mojibake Patterns](#mojibake-patterns)
4. [General Rules (GN)](#general-rules-gn)
5. [BOM Rules per File Type (BM)](#bom-rules-per-file-type-bm)
6. [Process Boundary Rules (PR)](#process-boundary-rules-pr)
7. [Platform Defaults](#platform-defaults)

## Rule Index

General (GN)
- UNICODE-GN-01: Specify the encoding explicitly on every read and every write
- UNICODE-GN-02: New files are UTF-8 without BOM unless a BM rule says otherwise
- UNICODE-GN-03: Decode once at input, encode once at output, process text as strings
- UNICODE-GN-04: Read files of unknown origin BOM-tolerant
- UNICODE-GN-05: Detect only at input boundaries of unknown origin: BOM first, then strict UTF-8, then declared fallback
- UNICODE-GN-06: Never silently drop or replace characters in data
- UNICODE-GN-07: Prove encoding correctness in tests, not by re-reading output in production
- UNICODE-GN-08: Normalize external text to NFC once at the input boundary
- UNICODE-GN-09: Keep source code ASCII-only where the runtime reads it in a legacy code page
- UNICODE-GN-10: Repair mojibake as a one-off data fix with a strict, reversible method - never as a pipeline step

BOM per file type (BM)
- UNICODE-BM-01: JSON / JSONL - UTF-8, no BOM
- UNICODE-BM-02: CSV - no BOM for machines, BOM for Excel; delimiter and number format follow the file or consumer, never hard-coded
- UNICODE-BM-03: XML - UTF-8 no BOM with matching declaration; UTF-16 always with BOM
- UNICODE-BM-04: HTML - UTF-8 no BOM, `<meta charset="utf-8">` in first 1024 bytes
- UNICODE-BM-05: Python, shell, YAML, TOML, Markdown, TXT, logs - UTF-8, no BOM
- UNICODE-BM-06: PowerShell scripts - ASCII-only, or UTF-8 with BOM when non-ASCII is needed
- UNICODE-BM-07: Batch files (`.bat`, `.cmd`) - never a BOM, never UTF-16
- UNICODE-BM-08: UTF-16 only when the consumer requires it, always with BOM

Process boundaries (PR)
- UNICODE-PR-01: Never parse non-ASCII from a child process's plain stdout without fixing the encoding on both sides
- UNICODE-PR-02: Prefer ASCII-safe interchange (JSON with `\uXXXX` escapes) or files over console text
- UNICODE-PR-03: Decode HTTP responses from raw bytes when the server sends no `charset`
- UNICODE-PR-04: Set the encoding of archive member names explicitly

## Core Concepts

- Character: Abstract symbol with a Unicode code point (`é` = U+00E9)
- Encoding: Mapping from code points to bytes. Same character, different bytes: `é` = `C3 A9` (UTF-8), `E9` (Windows-1252), `E9 00` (UTF-16LE)
- UTF-8: 1-4 bytes per character, ASCII-compatible, no byte order. Default for files, web, JSON, Linux
- UTF-16LE / UTF-16BE: 2 or 4 bytes per character. Windows internal string format, .NET `string`, PowerShell 5.1 `Out-File` default
- UTF-32: 4 bytes per character, rare in files
- ANSI: Windows "system code page" (Windows-1252 on Western European systems, 1250 Central European, 1251 Cyrillic). Single byte, max 256 characters. Cannot represent `ő` (Windows-1252) or `東`
- OEM: Console code page (437 US, 850 Western Europe). Used by `cmd.exe` and console programs. Differs from ANSI on the same machine
- Latin-1 (ISO-8859-1): Maps bytes 0x00-0xFF 1:1 to U+0000-U+00FF. Differs from Windows-1252 in 0x80-0x9F
- BOM (Byte Order Mark): Character U+FEFF at file start, used as an encoding signature:
  - UTF-8: `EF BB BF` (no byte-order meaning, signature only)
  - UTF-16LE: `FF FE`
  - UTF-16BE: `FE FF`
  - UTF-32LE: `FF FE 00 00` (check before UTF-16LE - same first 2 bytes)
  - UTF-32BE: `00 00 FE FF`
- Mojibake: Text decoded with a different encoding than it was encoded with
- NFC / NFD: Unicode normalization forms. `é` is either 1 code point (NFC, U+00E9) or 2 (NFD, `e` + U+0301). Both render identically, compare unequal [TESTED]

## Mojibake Patterns

Read the symptom, identify the wrong decoding, fix the reader or writer - not the data.

- `CafÃ©`, `MÃ¼ller`, `Å‘`, `â€™` (’), `â€“` (–), `â€œ` (“), `Â·` (·) - UTF-8 bytes decoded as Windows-1252. Most common case. Cause: legacy default reader (`Get-Content` in PowerShell 5.1, Python `open()` without `encoding` before 3.15). Reversible [TESTED]
- `ÃƒÂ©` - Same error applied twice. Reversible by repeating the reversal [TESTED]
- `Caf├⌐`, `∩╗┐` - UTF-8 bytes decoded as OEM code page 437 (console output, `cmd.exe`) [TESTED]
- `ï»¿` at file start, `'∩╗┐@echo' is not recognized` - UTF-8 BOM read by a reader that does not expect it [TESTED]
- `Caf�` (U+FFFD) - Windows-1252 bytes decoded as UTF-8 with replacement. Lossy, not reversible [TESTED]
- `Caf? ? ?` - Text encoded to ASCII or ANSI that cannot represent the characters (`Export-Csv` default in 5.1, `[Text.Encoding]::ASCII`). Data lost at write time [TESTED]
- `o` instead of `ő` - Best-fit mapping during ANSI encoding (`Set-Content` default in 5.1). Data lost silently [TESTED]
- `C\0a\0f\0` or `ÿþ`, `■` - UTF-16LE read as single-byte text (`>` redirect output from PowerShell 5.1) [TESTED]
- `Cafe\u0301` vs `Café` not equal - NFD vs NFC (macOS file names, some web forms). Not an encoding error; normalize (UNICODE-GN-08)

## General Rules (GN)

### UNICODE-GN-01: Explicit Encoding Everywhere

Every API call that converts between bytes and text gets an explicit encoding argument: file read/write, CSV/JSON/XML/INI/TOML libraries, stream readers/writers, `subprocess`, HTTP response decoding, logging file handlers. Platform defaults differ between versions and machines (PowerShell 5.1 vs 7, Python 3.14 vs 3.15, Windows code page settings).

BAD: `Get-Content $path`, `open(path)`, `Set-Content $path $text`, `subprocess.run(cmd, text=True)`
GOOD: `Get-Content -LiteralPath $path -Encoding UTF8`, `open(path, encoding='utf-8')`, `subprocess.run(cmd, capture_output=True, encoding='utf-8')`

Python 3.10+: run tests with `python -X warn_default_encoding` to get an `EncodingWarning` for every `open()`, `Path.read_text()`, `io.TextIOWrapper()` call without encoding [VERIFIED: PEP 597]; `subprocess.run(..., text=True)` without encoding also warns in 3.12 [TESTED].

### UNICODE-GN-02: UTF-8 Without BOM by Default

Write new text files as UTF-8 without BOM. Exceptions only per BM rules (Excel CSV, PowerShell 5.1 scripts with non-ASCII, UTF-16 consumers). Reason: BOMs break JSON parsers, shebang lines, batch files, Unix tools, and file concatenation [VERIFIED: about_Character_Encoding].

Trap: in .NET and PowerShell, `[Text.Encoding]::UTF8` writes a BOM; `New-Object System.Text.UTF8Encoding $false` does not [TESTED]. `[IO.File]::WriteAllText($path, $text)` without encoding writes UTF-8 without BOM [TESTED].

BAD: `[IO.File]::WriteAllText($path, $text, [Text.Encoding]::UTF8)`, Python `open(path, 'w', encoding='utf-8-sig')` for a config file
GOOD: `[IO.File]::WriteAllText($path, $text, (New-Object System.Text.UTF8Encoding $false))`, Python `open(path, 'w', encoding='utf-8')`

### UNICODE-GN-03: Decode Once, Encode Once

Convert bytes to text at the input boundary, process strings internally, convert to bytes at the output boundary. Never encode with one codec and decode with another inside the program. Never concatenate bytes from differently encoded sources.

### UNICODE-GN-04: BOM-Tolerant Reading

Files from Windows tools (PowerShell 5.1, Notepad, Excel, Visual Studio) may start with a UTF-8 BOM. Read them with a BOM-stripping decoder:
- Python: `encoding='utf-8-sig'` (reads files with and without BOM). Plain `'utf-8'` keeps U+FEFF as first character, which breaks `json.loads`, `configparser`, and header matching in CSV [TESTED]
- .NET / PowerShell: `[IO.File]::ReadAllText($path, [Text.Encoding]::UTF8)` and `Get-Content -Encoding UTF8` strip the BOM [TESTED]

Write with `'utf-8'` (no BOM), read with `'utf-8-sig'`.

BAD: `json.loads(Path(path).read_text(encoding='utf-8'))` on a file saved by PowerShell 5.1 → `JSONDecodeError: Unexpected UTF-8 BOM`
GOOD: `json.loads(Path(path).read_text(encoding='utf-8-sig'))`

### UNICODE-GN-05: Detect, Never Guess

Scope: input boundaries that receive files of unknown origin (user uploads, foreign exports, legacy archives). Sources with a known encoding (own files, APIs with declared charset, configured legacy feeds) are read with that encoding directly - no detection. Detect once per file, never per record or per line. For large files, decode with a strict streaming decoder instead of loading the file for detection.

When the encoding of an input file is unknown:
1. Check BOM bytes (UTF-32 before UTF-16, see Core Concepts)
2. No BOM: decode as strict UTF-8 (throw on invalid bytes). Success = UTF-8. Pure ASCII is valid UTF-8
3. Strict UTF-8 fails: use the fallback configured for this input source and log that fallback was used. Default for files produced on the same machine: system ANSI code page (Python `locale.getencoding()`, PowerShell registry `HKLM:\SYSTEM\CurrentControlSet\Control\Nls\CodePage` value `ACP`). Never hard-code `1252` - it is wrong on Central European, Cyrillic, Greek, Turkish, and East Asian systems
4. Format with own declaration (XML, HTML): let the format parser read bytes and honor the declaration

Do not use statistical detectors (`chardet`, `charset_normalizer`) for files you control; use them only for foreign data and log the detected encoding and confidence.

### UNICODE-GN-06: No Silent Character Loss

Never use `errors='ignore'` or `errors='replace'` on data that is stored or forwarded. Allowed only for diagnostic display (log lines, console). Never encode data to ASCII or ANSI; `[Text.Encoding]::ASCII` replaces every non-ASCII character with `?` without error [TESTED].

BAD: `name.encode('ascii', 'ignore').decode()` → `Mller`; `data.decode('utf-8', errors='replace')` before saving → `M�ller`
GOOD: `data.decode('utf-8')` (raises on invalid bytes, caller decides); `print(text.encode(sys.stdout.encoding, 'replace').decode(sys.stdout.encoding))` for console display only

### UNICODE-GN-07: Prove Encoding Correctness in Tests

Production code writes once with an explicit encoding (UNICODE-GN-01) and does not re-read, compare, or scan its own output - that doubles I/O and hides the real defect. Correctness is proven where it is cheap and repeatable:
- Test suite: one test per write path (file type x writer) that writes a fixed non-ASCII sample (`Café ő 東京 €`) and asserts the exact bytes: BOM state, UTF-8 round trip, no U+FFFD, no `?`
- SPEC: state encoding and BOM per output format as acceptance criteria
- IMPL / TEST plans: list each write path and its encoding test case
- Diagnostics only: mojibake scans (`Test-Mojibake`, `has_mojibake`) for investigating existing data, not per-record checks in production

BAD: `[IO.File]::WriteAllText($logPath, $text, $utf8NoBom); if ([IO.File]::ReadAllText($logPath) -ne $text) { throw }` in production
GOOD: test `test_report_writer_utf8_no_bom` writes `Café ő` through the production writer and asserts `data == 'Café ő'.encode('utf-8')`

### UNICODE-GN-08: Normalize Once at the Input Boundary

Normalize text from external sources (file names from disk, user input, web forms, third-party APIs) to NFC once when it enters the program (UNICODE-GN-03), before it is stored, compared, deduplicated, or used as a key: Python `unicodedata.normalize('NFC', text)`, .NET `$text.Normalize([Text.NormalizationForm]::FormC)`. Internal comparisons then use plain equality - no normalization per comparison. Keep the original form when writing file names back to disk.

BAD: `if title == existing_title:` with `title` from a macOS file name (NFD) → `False` for identical-looking `Café`; or `normalize()` inside a comparison loop over 100,000 records
GOOD: `title = unicodedata.normalize('NFC', path.stem)` when the file list is read; later `if title == existing_title:`

### UNICODE-GN-09: ASCII-Only Source Code for Legacy Runtimes

Windows PowerShell 5.1 reads `.ps1` files without BOM as ANSI; `cmd.exe` reads batch files in the active console code page (OEM by default). Non-ASCII string literals in such files become mojibake [TESTED]. Options:
- Preferred: keep source ASCII-only, build non-ASCII characters from code points: `'Caf' + [char]0x00E9`
- Or follow UNICODE-BM-06 / UNICODE-BM-07

Non-ASCII characters in comments are harmless but still trigger editor and diff noise; avoid them.

BAD: `$name = 'Café'` in a BOM-less `.ps1` run by `powershell.exe` → `CafÃ©`
GOOD: `$name = 'Caf' + [char]0x00E9`

### UNICODE-GN-10: Strict, Reversible Repair

Scope: one-off repair of data already damaged, after the writer is fixed. Never add automatic repair to a production pipeline - it masks the writer defect and can alter genuine text.

Mojibake of type "UTF-8 decoded as Windows-1252" can be reversed losslessly: encode the text as Windows-1252 (keeping U+0080-U+009F as raw bytes 0x80-0x9F), decode as strict UTF-8. Apply only to runs of non-ASCII characters and only when strict decoding succeeds; genuine text (`Café`, `Müller`) does not form valid UTF-8 sequences and stays unchanged [TESTED]. False positive only for text that genuinely contains pairs like `Ã©` - review the dry-run output. Use `repair_mojibake_win-1252.py`, run with `--dry-run` first. Lossy patterns (`?`, `�`, best-fit `o`) cannot be repaired - re-create the data from the source.

## BOM Rules per File Type (BM)

### UNICODE-BM-01: JSON / JSONL - UTF-8, No BOM

RFC 8259 section 8.1: JSON exchanged between systems MUST be UTF-8; implementations MUST NOT add a BOM; parsers MAY ignore one [VERIFIED]. Python `json.loads` on text with BOM raises `JSONDecodeError: Unexpected UTF-8 BOM` [TESTED].

Trap: PowerShell 5.1 `ConvertTo-Json | Set-Content -Encoding UTF8` writes a BOM [TESTED]. Use `[IO.File]::WriteAllText($path, $json, (New-Object System.Text.UTF8Encoding $false))`. Read JSON BOM-tolerant (UNICODE-GN-04) because other tools produce BOMs anyway.

BAD: `$config | ConvertTo-Json -Depth 10 | Set-Content $path -Encoding UTF8` (BOM in 5.1)
GOOD: `[IO.File]::WriteAllText($path, ($config | ConvertTo-Json -Depth 10), $utf8NoBom)` with `$utf8NoBom = New-Object System.Text.UTF8Encoding $false`

### UNICODE-BM-02: CSV - Consumer Decides

CSV has no encoding declaration.
- For programs, databases, Unix tools: UTF-8 without BOM
- For Excel (double-click open): UTF-8 with BOM. Excel opens UTF-8 CSV normally only with BOM; without BOM use Data > Get Data > From Text/CSV [VERIFIED: Microsoft Support]. Without BOM non-ASCII appears as mojibake [REPORTED]
- Reading: always BOM-tolerant (Python `utf-8-sig`); a BOM otherwise ends up in the first column name
- Python: open CSV files with `newline=''`; without it, Windows writes `\r\r\n` [TESTED]
- Delimiter: Excel uses the Windows list separator for opening and saving CSV [VERIFIED: Microsoft Learn]; it is `,` in en-US and `;` in de-DE [TESTED: .NET `TextInfo.ListSeparator`]. Reading: detect the delimiter from a bounded sample of the first records (count outside quotes, same count in every record; header-only counting fails on headers like `Kunde, Name;Ort`; never read the whole file or an unbounded line to detect) or configure it per source; never hard-code `,` or `;`. Writing for programs: `,` (RFC 4180). Writing for Excel on the same machine: the user's list separator
- Numbers and dates: PowerShell `ConvertTo-Csv` / `Export-Csv` format them with the current culture (de-DE: `1,5`, `15.01.2026`) [TESTED]. For programs: invariant culture, ISO 8601 dates. Python `csv` uses `str()` (`1.5`, ISO dates) - correct for programs, misread by Excel in decimal-comma locales
- Excel users in several locales: write XLSX; no single CSV opens correctly in both `,` and `;` locales

BAD: Python `open('report.csv', 'w', encoding='utf-8', newline='')` for a file users double-click in Excel → mojibake; `Import-Csv -Delimiter ';'` in reusable code → US files load as one column
GOOD: `encoding='utf-8-sig'` for the Excel file, `encoding='utf-8'` for the file a program imports; delimiter detected from a bounded sample of the first records

### UNICODE-BM-03: XML - Declaration Must Match Bytes

- Write UTF-8 without BOM plus `<?xml version="1.0" encoding="utf-8"?>`
- UTF-16 XML MUST begin with a BOM [VERIFIED: XML 1.0 section 4.3.3]
- Read with the XML parser from the file path or bytes, never via a text reader with default encoding: PowerShell 5.1 `[xml](Get-Content $path)` corrupts UTF-8 without BOM; `XmlDocument.Load($path)` reads correctly [TESTED]
- Trap: .NET `XmlDocument.Save($path)` writes a UTF-8 BOM [TESTED]; use `XmlWriter` with `UTF8Encoding($false)` for no BOM

BAD: `$xml = [xml](Get-Content $path)` in 5.1
GOOD: `$xml = New-Object System.Xml.XmlDocument; $xml.Load($fullPath)`

### UNICODE-BM-04: HTML - UTF-8, Meta Charset Early

UTF-8 without BOM; `<meta charset="utf-8">` as first element in `<head>`, completely within the first 1024 bytes [VERIFIED: WHATWG HTML]. HTTP header `Content-Type: text/html; charset=utf-8` when served.

### UNICODE-BM-05: Code, Config, and Text Files - UTF-8, No BOM

- Python `.py`: UTF-8 is the default source encoding; a BOM before `#!` breaks the shebang [VERIFIED]
- Shell scripts (`.sh`, `.bash`): UTF-8 without BOM, LF line endings. The kernel recognizes a shebang only if `#!` are the first 2 bytes; a BOM makes it `#!/bin/bash: No such file or directory` [REPORTED: Stack Overflow 19065522]
- YAML: UTF-8 without BOM. YAML 1.2.2 allows a BOM at the start of any document and recommends UTF-8 output [VERIFIED: YAML 1.2.2 section 5.2]; not all tools strip the BOM [REPORTED]
- TOML: UTF-8 without BOM. Python `tomllib` fails on a BOM (`Invalid statement (at line 1, column 1)`) and requires binary mode `'rb'` [TESTED]
- INI: UTF-8 without BOM. Python `configparser` with `encoding='utf-8'` fails on a BOM (`MissingSectionHeaderError`); read with `utf-8-sig` [TESTED]
- Markdown, TXT, logs: UTF-8 without BOM

### UNICODE-BM-06: PowerShell Scripts (`.ps1`, `.psm1`, `.psd1`)

Windows PowerShell 5.1 reads script files without BOM as ANSI [VERIFIED: about_Character_Encoding] [TESTED].
- Preferred: ASCII-only scripts (UNICODE-GN-09)
- Non-ASCII required and script must run in 5.1: save as UTF-8 with BOM
- PowerShell 7 only: UTF-8 without BOM works

Launchers decide the version: `powershell.exe` = 5.1, `pwsh.exe` = 7. A `.bat` that calls `powershell` runs every script in 5.1.

BAD: `.ps1` saved as UTF-8 without BOM, containing `Write-Host 'Grüße'`, started by `powershell -File script.ps1`
GOOD: same script saved as UTF-8 with BOM, or literal rewritten as `'Gr' + [char]0x00FC + [char]0x00DF + 'e'`

### UNICODE-BM-07: Batch Files (`.bat`, `.cmd`) - Never BOM, Never UTF-16

`cmd.exe` reads batch files in the current console code page and treats a UTF-8 BOM as part of the first command: `'∩╗┐@echo' is not recognized as an internal or external command` [TESTED]. A UTF-16LE file runs as a single line containing only its first character: the null byte after it reads as end of file [VERIFIED: The Old New Thing].
- Preferred: ASCII-only content
- Non-ASCII required (paths, names): UTF-8 without BOM, `chcp 65001 >nul` as one of the first lines before any non-ASCII line [TESTED: Windows 11]
- Generating batch files: write with `UTF8Encoding($false)` or ASCII after verifying the content is pure ASCII; the ASCII encoder replaces non-ASCII with `?` silently [TESTED]

BAD: `Set-Content run.bat $commands -Encoding UTF8` in 5.1 (BOM) or `$commands > run.bat` in 5.1 (UTF-16LE)
GOOD: ``[IO.File]::WriteAllText($batchPath, "@echo off`r`nchcp 65001 >nul`r`n$commands", $utf8NoBom)``

### UNICODE-BM-08: UTF-16 Only on Demand

Use UTF-16 only when the consumer requires it (some Windows tools, APIs, or legacy formats). Always with BOM (UTF-16LE `FF FE`). Avoid accidental UTF-16: PowerShell 5.1 `Out-File` and `>` / `>>` write UTF-16LE by default [TESTED]; `>>` appends in its default encoding regardless of the existing file's encoding [VERIFIED: about_Character_Encoding].

## Process Boundary Rules (PR)

### UNICODE-PR-01: Fix Both Sides of a Pipe

Text between processes is bytes; the writer encodes, the reader decodes, often with different defaults:
- Python child writing to a pipe: uses the ANSI code page before 3.15; printing `ő` raises `UnicodeEncodeError: 'charmap' codec can't encode` [TESTED]. Fix: run child with `-X utf8` or set env `PYTHONUTF8=1` / `PYTHONIOENCODING=utf-8`, and decode with `encoding='utf-8'` in the parent [TESTED]
- PyInstaller-built executables (e.g. `yt-dlp.exe`): ignore all `PYTHON*` environment variables [VERIFIED: PyInstaller docs]. Use the tool's own option (`yt-dlp --encoding utf-8`, marked experimental [VERIFIED: yt-dlp README]) or ASCII-safe output (UNICODE-PR-02)
- PowerShell calling a native program: decodes the program's stdout with `[Console]::OutputEncoding` (OEM, e.g. 437) [TESTED]. Set `[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding $false` before the call, only if the program writes UTF-8
- PowerShell sending to a native program's stdin: uses `$OutputEncoding`. Does not affect files [VERIFIED: about_Character_Encoding]
- Console printing in Python: interactive Windows consoles use the Unicode console API; redirection to a file or pipe does not [TESTED]. Call `sys.stdout.reconfigure(encoding='utf-8')` in scripts whose output is redirected

BAD: `$output = & python child.py` with default `[Console]::OutputEncoding` and no `PYTHONUTF8` → `UnicodeEncodeError` in the child or mojibake in `$output`
GOOD: set `$env:PYTHONUTF8 = '1'` and `[Console]::OutputEncoding = $utf8NoBom` before the call, restore afterwards (`UNICODE_POWERSHELL_EXAMPLES.md` section 8)

### UNICODE-PR-02: Prefer ASCII-Safe Interchange

Exchange non-ASCII data between processes as files with explicit encoding, or as JSON with `\uXXXX` escapes. yt-dlp `-j` and Python `json.dumps` (default `ensure_ascii=True`) emit pure ASCII and survive any code page [TESTED]. Pass arguments, not stdin text: the Windows command line is UTF-16 and arrives intact in programs that read it as UTF-16 (Python, .NET, PowerShell) [TESTED]. Programs using the ANSI `main()` / `GetCommandLineA` receive it converted to the ANSI code page

### UNICODE-PR-03: HTTP Responses Without Charset

Windows PowerShell 5.1 `Invoke-WebRequest` and `Invoke-RestMethod` decode responses without `charset` in `Content-Type` (e.g. `application/json`) as ISO-8859-1 → mojibake for UTF-8 [TESTED] [REPORTED: PowerShell issue 20488]. Decode the raw bytes: `[Text.Encoding]::UTF8.GetString($response.RawContentStream.ToArray())` [TESTED]. PowerShell 7.0+ decodes JSON responses without charset as UTF-8, 7.4+ also other text responses [REPORTED: PowerShell issue 20488, PR 18219] [TESTED: 7.5]; 7.4+ also encodes request bodies as UTF-8 by default [VERIFIED: Invoke-WebRequest docs].

Python `requests` without `charset` in the header [VERIFIED: requests source `get_encoding_from_headers`]:
- `text/*` (`text/plain`, `text/html`, `text/csv`): `response.encoding = 'ISO-8859-1'` → `response.text` and `response.json()` produce mojibake for UTF-8
- `application/json`: `'utf-8'` (correct)
- Other types: `None` → `response.text` guesses with `charset_normalizer` / `chardet`
- Fix: `response.content.decode('utf-8')` when the server is known to send UTF-8, or set `response.encoding = 'utf-8'` before `response.text`

BAD: `(Invoke-RestMethod $url).name` in 5.1 for a server sending `Content-Type: application/json` → `CafÃ©`
GOOD: `$utf8NoBom.GetString((Invoke-WebRequest $url -UseBasicParsing).RawContentStream.ToArray()) | ConvertFrom-Json`

### UNICODE-PR-04: Archive Member Names

ZIP general purpose bit 11 (Language Encoding Flag, EFS) marks names and comments as UTF-8; without it the specification defines IBM code page 437 [VERIFIED: PKWARE APPNOTE 4.4.4, Appendix D]. Many Windows tools write names without the flag in the OEM code page of the creating system (e.g. 850, 866), not 437 [REPORTED]. Python 3.11+: `zipfile.ZipFile(path, metadata_encoding='cp850')` for such archives [TESTED: parameter exists in 3.12]. When creating archives, Python stores ASCII names without flag and non-ASCII names as UTF-8 with bit 11 set [VERIFIED: CPython `ZipInfo._encodeFilenameFlags`].

BAD: `zipfile.ZipFile(path).namelist()` on an archive created with OEM code page 850 → `S¢rensen.txt` instead of `Sørensen.txt` [TESTED]
GOOD: `zipfile.ZipFile(path, metadata_encoding='cp850').namelist()` after confirming the creator's OEM code page

## Platform Defaults

Defaults that cause most encoding bugs. Never rely on them (UNICODE-GN-01); know them to diagnose.

Windows PowerShell 5.1 (`powershell.exe`) [VERIFIED: about_Character_Encoding] [TESTED]
- `Get-Content`, `Import-PowerShellDataFile`, script files: read as ANSI when no BOM → mojibake for UTF-8
- `Import-Csv`, `Import-Clixml`, `Select-String`: assume UTF-8 when no BOM (correct)
- `Set-Content`, `Add-Content` (new file): write ANSI → `?` and best-fit losses (`ő` → `o`)
- `Out-File`, `>`, `>>`, `Export-Clixml`, `New-ModuleManifest`: write UTF-16LE with BOM
- `Export-Csv`: writes ASCII → every non-ASCII character becomes `?`
- `[Text.Encoding]::Default`: ANSI code page in 5.1, UTF-8 in 7 [TESTED] - not usable as legacy fallback in code for both versions
- `-Encoding UTF8`: always writes a BOM; no `-Encoding` value writes UTF-8 without BOM. Only `New-Item -ItemType File -Value` writes UTF-8 without BOM
- `Invoke-WebRequest`, `Invoke-RestMethod`: decode responses without `charset` as ISO-8859-1
- `$PSDefaultParameterValues['*:Encoding'] = 'utf8'` makes all cmdlets UTF-8 - with BOM in 5.1

PowerShell 7 (`pwsh.exe`) [VERIFIED] [TESTED: 7.5]
- All cmdlets read and write UTF-8 without BOM by default; `>` writes UTF-8 without BOM
- `-Encoding utf8` = no BOM; `-Encoding utf8BOM` = with BOM
- Reading an ANSI file shows `�` for non-ASCII bytes (lossy - pass the source's code page for legacy files, e.g. `-Encoding 1251`; code page numbers supported since 6.2)

.NET (both PowerShell versions) [TESTED]
- `[IO.File]::WriteAllText/WriteAllLines/AppendAllText($path, $text)` without encoding: UTF-8 without BOM
- `[Text.Encoding]::UTF8` as argument: writes BOM. `New-Object System.Text.UTF8Encoding $false`: no BOM
- `[IO.File]::ReadAllText($path, $encoding)`: BOM detection wins over the argument, BOM is stripped
- Relative paths resolve against the process working directory, not the PowerShell location: `Set-Location` does not affect `[IO.File]` [TESTED]. Pass absolute paths

Python [VERIFIED: PEP 686] [TESTED: 3.12]
- `open()`, `Path.read_text()`, `subprocess(text=True)` without encoding before 3.15: locale encoding (`cp1252` on Western Windows) → mojibake for UTF-8 files
- Python 3.15+: UTF-8 by default (PEP 686) [VERIFIED: What's New 3.15]. 3.15.0 final is scheduled for 2026-10-09 [VERIFIED: PEP 790]; explicit `encoding=` remains required for code that runs on older versions
- `-X utf8` or `PYTHONUTF8=1`: UTF-8 mode on 3.7-3.14
- Pipes and redirected stdout before 3.15: locale encoding → `UnicodeEncodeError` for characters outside the code page

Windows console and cmd.exe [VERIFIED] [TESTED]
- Console code page (`chcp`): OEM (437, 850), not ANSI and not UTF-8
- `cmd.exe` reads batch files in the active console code page; `chcp 65001` switches to UTF-8 for the rest of the file
- Windows option "Beta: Use Unicode UTF-8 for worldwide language support" sets registry values `ACP`, `OEMCP`, `MACCP` under `HKLM\SYSTEM\CurrentControlSet\Control\Nls\CodePage` to 65001 machine-wide [REPORTED: Stack Overflow 56419639]; Microsoft documents it as the system-wide UTF-8 switch for GDI [VERIFIED: Microsoft Learn]. Never depend on it being on or off

Not covered: EBCDIC, UTF-7 (deprecated), database collations, terminal font rendering. For multi-byte code pages (932, 936, 949, 950) apply UNICODE-GN-03: decode to Unicode before any byte-level search for `\`, quotes, or delimiters - trail bytes can equal `0x5C` [TESTED].
