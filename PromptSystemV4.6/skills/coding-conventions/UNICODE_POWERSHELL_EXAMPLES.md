# Unicode PowerShell Examples

Canonical patterns for reading and writing text in PowerShell. Every example runs identically in Windows PowerShell 5.1 (`powershell.exe`) and PowerShell 7 (`pwsh.exe`) [TESTED: 5.1.26100, 7.5.0]. Rules and reasons: `UNICODE_RULES.md`.

## Table of Contents

1. [Setup Block](#1-setup-block)
2. [Text Files (TXT, MD, LOG)](#2-text-files-txt-md-log)
3. [Legacy ANSI Files](#3-legacy-ansi-files)
4. [JSON](#4-json)
5. [CSV](#5-csv)
6. [XML](#6-xml)
7. [Other Formats](#7-other-formats)
8. [Native Programs](#8-native-programs)
9. [Web Requests](#9-web-requests)
10. [Detection and Verification](#10-detection-and-verification)
11. [Anti-Patterns](#11-anti-patterns)

## 1. Setup Block

Put at the top of every script that reads or writes text. Cmdlet `-Encoding UTF8` writes a Byte Order Mark (BOM) in 5.1 and none in 7; the .NET encoding objects behave identically in both.

```powershell
$utf8NoBom = New-Object System.Text.UTF8Encoding $false          # default for all output
$utf8Bom = New-Object System.Text.UTF8Encoding $true             # Excel CSV, 5.1 scripts with non-ASCII
$strictUtf8 = New-Object System.Text.UTF8Encoding $false, $true  # throws on invalid bytes (detection)
# System ANSI code page (1252 Western, 1250 Central European, 1251 Cyrillic, 932 Japanese, ...); [Text.Encoding]::Default is UTF-8 in PowerShell 7
$systemAnsi = [System.Text.Encoding]::GetEncoding([int](Get-ItemProperty -LiteralPath 'HKLM:\SYSTEM\CurrentControlSet\Control\Nls\CodePage').ACP)

# .NET resolves relative paths against the process directory, not the PowerShell location
function Get-FullPath([string]$Path) { return $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Path) }
```

## 2. Text Files (TXT, MD, LOG)

Read (BOM-tolerant: strips UTF-8 BOM, detects UTF-16/32 BOM):

```powershell
$path = Get-FullPath '.\data\notes.txt'
$text = [System.IO.File]::ReadAllText($path, $utf8NoBom)      # whole file as one string
$lines = [System.IO.File]::ReadAllLines($path, $utf8NoBom)    # string[] without line endings
$text = Get-Content -LiteralPath $path -Raw -Encoding UTF8     # cmdlet alternative, same result
```

Write (UTF-8 without BOM):

```powershell
[System.IO.File]::WriteAllText($path, $text, $utf8NoBom)
[System.IO.File]::WriteAllLines($path, [string[]]$lines, $utf8NoBom)  # cast: a single string would otherwise bind wrong
[System.IO.File]::AppendAllText($path, "$line`r`n", $utf8NoBom)       # append, never adds a BOM
```

Large files (streaming, line by line):

```powershell
$reader = New-Object System.IO.StreamReader($inputPath, $utf8NoBom, $true)   # $true = detect BOM
$writer = New-Object System.IO.StreamWriter($outputPath, $false, $utf8NoBom) # $false = overwrite
try {
  while ($null -ne ($line = $reader.ReadLine())) { $writer.WriteLine($line) }
}
finally { $reader.Dispose(); $writer.Dispose() }
```

Crash-safe overwrite (write temp file, then replace):

```powershell
$tempPath = "$path.tmp"
[System.IO.File]::WriteAllLines($tempPath, [string[]]$lines, $utf8NoBom)
Move-Item -LiteralPath $tempPath -Destination $path -Force
```

## 3. Legacy ANSI Files

Read legacy input with the code page of the machine that produced it, write UTF-8. Detect first (section 10) - reading UTF-8 as ANSI creates mojibake.

```powershell
$text = [System.IO.File]::ReadAllText($legacyPath, $systemAnsi)                      # legacy file produced on this machine
$text = [System.IO.File]::ReadAllText($legacyPath, [System.Text.Encoding]::GetEncoding($sourceCodePage))  # foreign source: code page configured per source (e.g. 1251)
[System.IO.File]::WriteAllText($utf8Path, $text, $utf8NoBom)
```

## 4. JSON

JSON is UTF-8 without BOM (RFC 8259). `ConvertTo-Json` default `-Depth` is 2 - deeper objects are flattened to strings, silently in 5.1, with a warning in 7.1+ [VERIFIED: ConvertTo-Json docs]; always pass `-Depth`.

```powershell
# Read (BOM-tolerant)
$config = [System.IO.File]::ReadAllText($jsonPath, $utf8NoBom) | ConvertFrom-Json

# Write (no BOM)
$json = $config | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText($jsonPath, $json, $utf8NoBom)
```

JSON Lines (one object per line):

```powershell
$records = New-Object System.Collections.Generic.List[object]   # List.Add is O(1); array += copies the whole array
foreach ($line in [System.IO.File]::ReadLines($jsonlPath, $utf8NoBom)) {    # streams, does not load the file
  if ($line.Trim()) { $records.Add(($line | ConvertFrom-Json)) }
}
$outputLines = New-Object System.Collections.Generic.List[string]
foreach ($record in $records) { $outputLines.Add(($record | ConvertTo-Json -Depth 10 -Compress)) }
[System.IO.File]::WriteAllLines($jsonlPath, $outputLines.ToArray(), $utf8NoBom)
```

## 5. CSV

The delimiter is a property of the file, not of the script: US and UK files use `,`, files from Excel in decimal-comma locales (German, French) use `;`. Never hard-code it for input.

```powershell
# Delimiter from the first $MaxRecords records, reading at most $MaxChars characters: constant time and memory for any file size,
# no ReadLine (a file without line breaks would load completely). Winner: the candidate with the same non-zero count outside quotes
# in every sampled record (header-only counting fails on headers like 'Kunde, Name;Ort'); ties -> higher count, then list order.
# No consistent candidate (ragged rows) -> most frequent in the header; no candidate at all -> ',' (single column)
function Get-CsvDelimiter([string]$Path, [int]$MaxRecords = 10, [int]$MaxChars = 65536) {
  $candidates = [char[]](',', ';', "`t", '|')
  $quote = [char]'"'; $lineFeed = [char]10; $carriageReturn = [char]13
  $buffer = New-Object char[] $MaxChars
  $reader = New-Object System.IO.StreamReader((Get-FullPath $Path), $utf8NoBom, $true)   # $true = honor BOM
  try { $charCount = $reader.ReadBlock($buffer, 0, $MaxChars) } finally { $reader.Dispose() }   # ReadBlock fills the buffer unless end of file
  $isEndOfFile = $charCount -lt $MaxChars

  # One pass, all candidates at once. Line breaks inside quoted fields belong to the field (RFC 4180); '""' toggles twice
  $records = New-Object System.Collections.Generic.List[object]   # one int[] of candidate counts per record
  $counts = New-Object int[] $candidates.Length
  $insideQuotes = $false; $hasContent = $false
  for ($index = 0; $index -lt $charCount -and $records.Count -lt $MaxRecords; $index++) {
    $character = $buffer[$index]
    if ($character -eq $quote) { $insideQuotes = -not $insideQuotes; $hasContent = $true }
    elseif (-not $insideQuotes -and ($character -eq $lineFeed -or $character -eq $carriageReturn)) {
      if ($hasContent) { $records.Add($counts); $counts = New-Object int[] $candidates.Length; $hasContent = $false }   # blank lines and CRLF skipped
    }
    else {
      $hasContent = $true
      if (-not $insideQuotes) { $candidateIndex = [Array]::IndexOf($candidates, $character); if ($candidateIndex -ge 0) { $counts[$candidateIndex]++ } }
    }
  }
  # Pending record: complete at end of file; cut off at $MaxChars it is used only when it is the header (header longer than the sample)
  if ($hasContent -and $records.Count -lt $MaxRecords -and ($isEndOfFile -or $records.Count -eq 0)) { $records.Add($counts) }

  $retVal = [char]','; $bestCount = 0
  if ($records.Count -eq 0) { return $retVal }
  $header = $records[0]
  for ($candidateIndex = 0; $candidateIndex -lt $candidates.Length; $candidateIndex++) {
    if ($header[$candidateIndex] -le $bestCount) { continue }
    $isConsistent = $true
    foreach ($record in $records) { if ($record[$candidateIndex] -ne $header[$candidateIndex]) { $isConsistent = $false; break } }
    if ($isConsistent) { $retVal = $candidates[$candidateIndex]; $bestCount = $header[$candidateIndex] }
  }
  if ($bestCount -gt 0) { return $retVal }
  for ($candidateIndex = 0; $candidateIndex -lt $candidates.Length; $candidateIndex++) {
    if ($header[$candidateIndex] -gt $bestCount) { $retVal = $candidates[$candidateIndex]; $bestCount = $header[$candidateIndex] }
  }
  return $retVal
}

# Read: Import-Csv assumes UTF-8 without BOM in 5.1 and 7; -Encoding UTF8 also handles BOM
$rows = Import-Csv -LiteralPath $csvPath -Delimiter (Get-CsvDelimiter $csvPath) -Encoding UTF8

# Write for programs: RFC 4180 comma, culture-independent numbers and dates, UTF-8 without BOM
# ConvertTo-Csv formats numbers and dates with the current culture (de-DE: "1,5", "15.01.2026"); format dates as ISO 8601 strings before export
$previousCulture = [System.Threading.Thread]::CurrentThread.CurrentCulture
[System.Threading.Thread]::CurrentThread.CurrentCulture = [System.Globalization.CultureInfo]::InvariantCulture
try { $csvLines = $rows | ConvertTo-Csv -NoTypeInformation -Delimiter ',' }
finally { [System.Threading.Thread]::CurrentThread.CurrentCulture = $previousCulture }
[System.IO.File]::WriteAllLines($csvPath, [string[]]$csvLines, $utf8NoBom)

# Write for Excel on this machine: user's list separator and current culture (Excel parses with both), UTF-8 with BOM
$excelLines = $rows | ConvertTo-Csv -NoTypeInformation -Delimiter ([System.Globalization.CultureInfo]::CurrentCulture.TextInfo.ListSeparator)  # same culture ConvertTo-Csv formats with
[System.IO.File]::WriteAllLines($excelCsvPath, [string[]]$excelLines, $utf8Bom)
```

Never use `Export-Csv` without `-Encoding` in 5.1 (writes ASCII, all non-ASCII becomes `?`). Excel files for users in other locales: write XLSX instead of CSV - no CSV satisfies both `,` and `;` locales.

## 6. XML

The XML parser reads bytes and honors BOM and `encoding` declaration. Never parse XML from `Get-Content` output.

```powershell
# Read
$xml = New-Object System.Xml.XmlDocument
$xml.Load((Get-FullPath $xmlPath))

# Write UTF-8 without BOM (XmlDocument.Save($path) would add a BOM)
$settings = New-Object System.Xml.XmlWriterSettings
$settings.Encoding = $utf8NoBom
$settings.Indent = $true
$writer = [System.Xml.XmlWriter]::Create((Get-FullPath $xmlPath), $settings)
try { $xml.Save($writer) } finally { $writer.Dispose() }
```

## 7. Other Formats

- HTML, Markdown, SVG: text files (section 2). HTML needs `<meta charset="utf-8">` within the first 1024 bytes
- PowerShell data files (`.psd1`): `Import-PowerShellDataFile` reads ANSI in 5.1 when no BOM. Keep `.psd1` ASCII-only or save with `$utf8Bom`
- Generated PowerShell scripts that contain non-ASCII and run in 5.1: write with `$utf8Bom`
- Generated batch files: never a BOM. Prefer ASCII; verify before writing (`$batchContent` = commands without `@echo off`):

```powershell
$isAscii = $true
foreach ($character in $batchContent.ToCharArray()) { if ([int]$character -gt 127) { $isAscii = $false; break } }
if ($isAscii) {
  [System.IO.File]::WriteAllText($batchPath, "@echo off`r`n$batchContent", $utf8NoBom)
} else {
  [System.IO.File]::WriteAllText($batchPath, "@echo off`r`nchcp 65001 >nul`r`n$batchContent", $utf8NoBom)
}
```

- Transcripts and logs from cmdlets: `Start-Transcript` writes UTF-8 with BOM in 5.1; write own log files with `AppendAllText` and `$utf8NoBom`
- CLIXML (`Export-Clixml` / `Import-Clixml`): UTF-16LE in 5.1, UTF-8 without BOM in 7 [VERIFIED: Export-Clixml docs]; PowerShell-only format, do not hand to other tools

## 8. Native Programs

PowerShell decodes native stdout with `[Console]::OutputEncoding` (OEM code page by default). Set it only when the program writes UTF-8, and restore it afterwards.

```powershell
$previousConsoleEncoding = [Console]::OutputEncoding
$previousOutputEncoding = $OutputEncoding
try {
  [Console]::OutputEncoding = $utf8NoBom   # decode child stdout as UTF-8
  $OutputEncoding = $utf8NoBom             # encode text piped into child stdin as UTF-8
  $env:PYTHONIOENCODING = 'utf-8'          # Python children write UTF-8; PyInstaller executables (yt-dlp.exe) ignore PYTHON* variables
  $env:PYTHONUTF8 = '1'
  $output = & $pythonPath $scriptPath $inputPath 2>&1
}
finally {
  [Console]::OutputEncoding = $previousConsoleEncoding
  $OutputEncoding = $previousOutputEncoding
}
```

Prefer machine-readable ASCII-safe output over console text: tools with JSON output (`yt-dlp -j`, Python `json.dumps` with default `ensure_ascii=True`) escape non-ASCII as `\uXXXX`. Or let the tool write a UTF-8 file and read that file. Pass non-ASCII values as arguments (`& $tool $name`), not via stdin.

## 9. Web Requests

PowerShell 5.1 decodes responses without `charset` in `Content-Type` as ISO-8859-1 (mojibake for UTF-8). Decode raw bytes; works in 5.1 and 7:

```powershell
$response = Invoke-WebRequest -Uri $url -UseBasicParsing
$body = $utf8NoBom.GetString($response.RawContentStream.ToArray())
$data = $body | ConvertFrom-Json
```

Request bodies with non-ASCII: send bytes and declare the charset:

```powershell
$bodyBytes = $utf8NoBom.GetBytes(($payload | ConvertTo-Json -Depth 10))
Invoke-WebRequest -Uri $url -Method Post -Body $bodyBytes -ContentType 'application/json; charset=utf-8' -UseBasicParsing
```

## 10. Detection and Verification

Detect encoding (BOM, then strict UTF-8, then legacy) - only at input boundaries for files of unknown origin, once per file (UNICODE-GN-05):

```powershell
# Returns: utf-32le-bom | utf-32be-bom | utf-8-bom | utf-16le-bom | utf-16be-bom | utf-8 (includes pure ASCII) | ansi
# Streams 1 MB chunks through one strict native decoder: constant memory, no 2 GB limit (ReadAllBytes fails above 2 GB),
# stops at the first invalid sequence. The stateful Decoder carries multi-byte sequences split across chunk borders
function Get-TextFileEncoding([string]$Path) {
  $buffer = New-Object byte[] 1048576
  $stream = New-Object System.IO.FileStream((Get-FullPath $Path), [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite, 65536, [System.IO.FileOptions]::SequentialScan)
  try {
    $byteCount = $stream.Read($buffer, 0, $buffer.Length)
    if ($byteCount -ge 4 -and $buffer[0] -eq 0xFF -and $buffer[1] -eq 0xFE -and $buffer[2] -eq 0 -and $buffer[3] -eq 0) { return 'utf-32le-bom' }
    if ($byteCount -ge 4 -and $buffer[0] -eq 0 -and $buffer[1] -eq 0 -and $buffer[2] -eq 0xFE -and $buffer[3] -eq 0xFF) { return 'utf-32be-bom' }
    if ($byteCount -ge 3 -and $buffer[0] -eq 0xEF -and $buffer[1] -eq 0xBB -and $buffer[2] -eq 0xBF) { return 'utf-8-bom' }
    if ($byteCount -ge 2 -and $buffer[0] -eq 0xFF -and $buffer[1] -eq 0xFE) { return 'utf-16le-bom' }
    if ($byteCount -ge 2 -and $buffer[0] -eq 0xFE -and $buffer[1] -eq 0xFF) { return 'utf-16be-bom' }
    $decoder = (New-Object System.Text.UTF8Encoding $false, $true).GetDecoder()   # $true = throw on invalid bytes
    $chars = New-Object char[] ($buffer.Length + 4)   # UTF-8 never yields more chars than bytes; +4 for a carried-over sequence
    $retVal = 'utf-8'
    try {
      while ($byteCount -gt 0) {
        [void]$decoder.GetChars($buffer, 0, $byteCount, $chars, 0, $false)
        $byteCount = $stream.Read($buffer, 0, $buffer.Length)
      }
      [void]$decoder.GetChars($buffer, 0, 0, $chars, 0, $true)   # flush: a sequence truncated at end of file is invalid
    }
    catch [System.Text.DecoderFallbackException] { $retVal = 'ansi' }
    return $retVal
  }
  finally { $stream.Dispose() }
}
```

Detect mojibake (UTF-8 decoded as Windows-1252) - diagnostics and tests only, not per record in production (UNICODE-GN-07):

```powershell
# True if text contains sequences like 'Ã©', 'Å‘', 'â€™' that reverse to valid UTF-8
function Test-Mojibake([string]$Text) {
  # exception fallback: characters outside Windows-1252 (genuine CJK, Cyrillic) throw instead of becoming '?'
  $ansi1252 = [System.Text.Encoding]::GetEncoding(1252, [System.Text.EncoderFallback]::ExceptionFallback, [System.Text.DecoderFallback]::ExceptionFallback)
  $strictUtf8 = New-Object System.Text.UTF8Encoding $false, $true
  foreach ($match in [regex]::Matches($Text, '[\u0080-\uFFFF]{2,}')) {
    try {
      $repaired = $strictUtf8.GetString($ansi1252.GetBytes($match.Value))
      if ($repaired -ne $match.Value) { return $true }
    } catch { }
  }
  return $false
}
```

`Test-Mojibake` is a check only; for repair use `repair_mojibake_win-1252.py` (handles undefined Windows-1252 bytes and multiple encoding levels).

Encoding test for a write path - test suite only, production code writes once without read-back (UNICODE-GN-07):

```powershell
# Pester-style test body: $writeReport is the production writer under test
$sample = 'Caf' + [char]0x00E9 + ' ' + [char]0x0151 + ' ' + [char]0x6771 + [char]0x4EAC + ' ' + [char]0x20AC
& $writeReport -Path $testPath -Text $sample
$expected = $utf8NoBom.GetBytes($sample)
$actual = [System.IO.File]::ReadAllBytes($testPath)
if ([Convert]::ToBase64String($actual) -ne [Convert]::ToBase64String($expected)) { throw "Encoding test failed for '$testPath'" }
```

## 11. Anti-Patterns

- `Get-Content $path` → ANSI in 5.1. Use `-Encoding UTF8` or `[IO.File]::ReadAllText($path, $utf8NoBom)`
- `Set-Content $path $text` / `Add-Content` → ANSI in 5.1, lossy. Use `[IO.File]::WriteAllText`
- `$text > $path`, `Out-File $path` → UTF-16LE in 5.1. Use `[IO.File]::WriteAllText`
- `Set-Content -Encoding UTF8` for JSON → BOM in 5.1, breaks JSON parsers
- `[IO.File]::WriteAllText($path, $text, [Text.Encoding]::UTF8)` → BOM. Use `$utf8NoBom`
- `Export-Csv $path` → ASCII in 5.1. Use `ConvertTo-Csv` + `WriteAllLines`
- `[xml](Get-Content $path)` → corrupts UTF-8 in 5.1. Use `XmlDocument.Load`
- `(Invoke-WebRequest $url).Content` / `Invoke-RestMethod $url` for UTF-8 without charset in 5.1. Decode `RawContentStream`
- `[IO.File]::ReadAllText('.\file.txt')` after `Set-Location` → wrong folder. Use `Get-FullPath`
- `[Text.Encoding]::ASCII.GetBytes($text)` → silent `?`. Verify ASCII first or use UTF-8
- `$PSDefaultParameterValues['*:Encoding'] = 'utf8'` as fix → still BOM in 5.1
- `Import-Csv -Delimiter ';'` hard-coded → US files (`,`) load as one column. Use `Get-CsvDelimiter`
- Sampling or detecting with `ReadAllBytes` / `ReadAllText` / `ReadLine()` on files of unknown size → `ReadAllBytes` fails above 2 GB, all load the whole file; a file without line breaks makes one `ReadLine()` load everything. Read a bounded block (`ReadBlock`) or stream fixed-size chunks
- `ConvertTo-Csv` / `Export-Csv` for programs under the user's culture → `1,5` and `15.01.2026` on German systems. Use invariant culture and ISO 8601 dates
- `GetEncoding(1252)` or `[Text.Encoding]::Default` as legacy fallback → wrong on non-Western systems, UTF-8 in PowerShell 7. Use `$systemAnsi` or the code page configured for the source
- `$array += $item` in loops over file lines or records → copies the array on every append (quadratic). Use `System.Collections.Generic.List[T]`
- Re-reading a just-written file to verify it in production → doubles I/O. Prove the write path in a test (UNICODE-GN-07)
- Non-ASCII string literals in a BOM-less `.ps1` run by `powershell.exe` → use `[char]0x00E9` or save with BOM
