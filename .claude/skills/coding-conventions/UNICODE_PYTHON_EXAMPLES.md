# Unicode Python Examples

Canonical patterns for reading and writing text in Python 3.10+. Every example passes an explicit encoding, so behavior is identical before and after the Python 3.15 UTF-8 default (PEP 686) and on every OS [TESTED: 3.12.6, Windows]. Rules and reasons: `UNICODE_RULES.md`.

Convention: write `'utf-8'`, read `'utf-8-sig'` (reads files with and without Byte Order Mark (BOM)). Write `'utf-8-sig'` only for Excel CSV.

## Table of Contents

1. [Find Missing Encodings](#1-find-missing-encodings)
2. [Text Files (TXT, MD, LOG)](#2-text-files-txt-md-log)
3. [Legacy ANSI Files](#3-legacy-ansi-files)
4. [JSON](#4-json)
5. [CSV](#5-csv)
6. [XML](#6-xml)
7. [Other Formats](#7-other-formats)
8. [Console Output](#8-console-output)
9. [Subprocesses](#9-subprocesses)
10. [HTTP](#10-http)
11. [Detection and Verification](#11-detection-and-verification)
12. [Anti-Patterns](#12-anti-patterns)

## 1. Find Missing Encodings

Python 3.10+, test suite and CI only: run tests with `EncodingWarning` as error; every `open()`, `read_text()`, `subprocess(text=True)` without encoding fails the run [VERIFIED: PEP 597] [TESTED: 3.12]. Production runs need no flag - the explicit `encoding=` arguments are the fix:

```
python -X warn_default_encoding -W error::EncodingWarning -m pytest
```

## 2. Text Files (TXT, MD, LOG)

```python
from pathlib import Path

path = Path('data/notes.txt')
text = path.read_text(encoding='utf-8-sig')                 # whole file, BOM stripped if present
lines = text.splitlines()                                   # lines without line endings, no second read

with open(path, 'r', encoding='utf-8-sig') as file:         # streaming, line by line
  for line in file:
    print(line.rstrip('\n'))

path.write_text(text, encoding='utf-8')                     # write, no BOM
with open(path, 'a', encoding='utf-8') as file:             # append
  file.write('appended line\n')
```

Control line endings explicitly when the consumer cares (`newline='\n'` for Unix tools and shell scripts, `newline='\r\n'` for batch files):

```python
with open('script.sh', 'w', encoding='utf-8', newline='\n') as file:
  file.write('#!/bin/sh\necho done\n')
```

Crash-safe overwrite (temp file + atomic replace):

```python
import os
from pathlib import Path

def write_text_atomic(path: Path, text: str) -> None:
  temp_path = path.with_name(path.name + '.tmp')
  temp_path.write_text(text, encoding='utf-8')
  os.replace(temp_path, path)
```

## 3. Legacy ANSI Files

Read legacy input with the code page of the machine that produced it, write UTF-8. Detect first (section 11) - reading UTF-8 as ANSI creates mojibake.

```python
import locale
from pathlib import Path

text = Path('legacy.txt').read_text(encoding=locale.getencoding())   # produced on this machine: system ANSI code page (3.11+, ignores UTF-8 mode)
text = Path('legacy.txt').read_text(encoding=source_codec)           # foreign source: codec configured per source (e.g. 'cp1251')
Path('legacy_utf8.txt').write_text(text, encoding='utf-8')
```

## 4. JSON

JSON is UTF-8 without BOM (RFC 8259). `ensure_ascii=False` keeps characters readable in the file; `ensure_ascii=True` (default) writes `\uXXXX` escapes - use it for pipes, console, and legacy consumers.

```python
import json
from pathlib import Path

config_path = Path('config.json')
with open(config_path, 'r', encoding='utf-8-sig') as file:  # tolerates BOM from PowerShell 5.1 / Notepad
  config = json.load(file)

with open(config_path, 'w', encoding='utf-8') as file:
  json.dump(config, file, ensure_ascii=False, indent=2)
  file.write('\n')
```

JSON Lines:

```python
import json

records = []
with open('records.jsonl', 'r', encoding='utf-8-sig') as file:
  for line in file:
    if line.strip(): records.append(json.loads(line))

with open('records.jsonl', 'w', encoding='utf-8', newline='\n') as file:
  for record in records:
    file.write(json.dumps(record, ensure_ascii=False) + '\n')
```

## 5. CSV

Always `newline=''` with the `csv` module (without it, Windows writes `\r\r\n`). The delimiter is a property of the file, not of the code: US and UK files use `,`, files from Excel in decimal-comma locales (German, French) use `;`. Never hard-code it for input.

```python
import csv, sys
if sys.platform == 'win32': import winreg

# Delimiter from a sample of the file; ',' when undetectable (single column)
def detect_csv_delimiter(sample: str) -> str:
  try:
    retVal = csv.Sniffer().sniff(sample, delimiters=',;\t|').delimiter
  except csv.Error:
    retVal = ','
  return retVal

# Windows list separator of the current user (Excel uses it to open and save CSV); ',' elsewhere
def get_excel_list_separator() -> str:
  retVal = ','
  if sys.platform == 'win32':
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Control Panel\International') as key: retVal = winreg.QueryValueEx(key, 'sList')[0]
  return retVal

with open('rows.csv', 'r', encoding='utf-8-sig', newline='') as file:  # BOM would otherwise prefix the first column name
  delimiter = detect_csv_delimiter(file.read(65536))
  file.seek(0)
  rows = list(csv.DictReader(file, delimiter=delimiter))

with open('rows.csv', 'w', encoding='utf-8', newline='') as file:      # for programs: RFC 4180 comma, no BOM
  writer = csv.DictWriter(file, fieldnames=['Name', 'City'])
  writer.writeheader()
  writer.writerows(rows)

with open('rows_excel.csv', 'w', encoding='utf-8-sig', newline='') as file:  # for Excel on this machine: BOM, user's list separator
  writer = csv.DictWriter(file, fieldnames=['Name', 'City'], delimiter=get_excel_list_separator())
  writer.writeheader()
  writer.writerows(rows)
```

`csv` writes numbers with `str()` (`1.5`) and dates as ISO 8601 - correct for programs. Excel in decimal-comma locales reads `1.5` as text or date; for Excel files with numbers for users in other locales, write XLSX instead of CSV.

## 6. XML

Parse from the path or bytes; the parser honors BOM and `encoding` declaration.

```python
import xml.etree.ElementTree as ET

tree = ET.parse('doc.xml')
root = tree.getroot()
tree.write('doc.xml', encoding='utf-8', xml_declaration=True)   # UTF-8, no BOM, declaration matches bytes
xml_text = ET.tostring(root, encoding='unicode')               # str without declaration
```

`tree.write(path)` without `encoding` writes US-ASCII with character references (`Caf&#233;`); `encoding='unicode'` writes UTF-8 without declaration [VERIFIED: CPython `_get_writer`] [TESTED]. Use `encoding='utf-8', xml_declaration=True`. Never decode XML with a guessed encoding before parsing.

## 7. Other Formats

TOML (`tomllib`, 3.11+): requires binary mode and fails on a BOM. Strip it:

```python
import codecs, tomllib
from pathlib import Path

data = Path('settings.toml').read_bytes()
if data.startswith(codecs.BOM_UTF8): data = data[len(codecs.BOM_UTF8):]
settings = tomllib.loads(data.decode('utf-8'))
```

INI (`configparser`): BOM causes `MissingSectionHeaderError` unless read with `utf-8-sig`:

```python
import configparser

config = configparser.ConfigParser()
config.read('settings.ini', encoding='utf-8-sig')
with open('settings.ini', 'w', encoding='utf-8') as file:
  config.write(file)
```

Logging to file:

```python
import logging

logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.INFO)  # encoding parameter: 3.9+
handler = logging.FileHandler('other.log', encoding='utf-8')
```

Compressed text, temp files, archives:

```python
import ctypes, gzip, tempfile, zipfile

with gzip.open('data.txt.gz', 'wt', encoding='utf-8') as file: file.write('text\n')
with gzip.open('data.txt.gz', 'rt', encoding='utf-8') as file: content = file.read()
with tempfile.NamedTemporaryFile('w', encoding='utf-8', suffix='.txt', delete=False) as file: file.write('text\n')
creator_oem_codec = f'cp{ctypes.windll.kernel32.GetOEMCP()}'   # archive created on this machine; foreign archive: creator's OEM code page (spec says cp437)
with zipfile.ZipFile('legacy.zip', metadata_encoding=creator_oem_codec) as archive: names = archive.namelist()  # 3.11+, only for names without UTF-8 flag
```

YAML (PyYAML, third party): `yaml.safe_load(file)` with a file opened as `encoding='utf-8-sig'`; write with `yaml.safe_dump(data, file, allow_unicode=True)` - without `allow_unicode` non-ASCII is escaped [VERIFIED: PyYAML emitter source].

HTML, Markdown, SVG: text files (section 2). HTML needs `<meta charset="utf-8">` within the first 1024 bytes.

## 8. Console Output

Interactive Windows consoles accept any character. Redirected or piped stdout uses the ANSI code page before 3.15 and raises `UnicodeEncodeError`. Reconfigure at program start:

```python
import sys

def main():
  if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
  if hasattr(sys.stderr, 'reconfigure'): sys.stderr.reconfigure(encoding='utf-8', errors='backslashreplace')
  print('Caf\u00e9 \u6771\u4eac')
```

The reader of the pipe must decode UTF-8 too (PowerShell: `[Console]::OutputEncoding`, see `UNICODE_POWERSHELL_EXAMPLES.md` section 8).

## 9. Subprocesses

Never `text=True` without `encoding`. Force UTF-8 on both sides:

```python
import os, subprocess, sys

environment = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8')   # Python children only; PyInstaller executables ignore PYTHON* variables
completed = subprocess.run([sys.executable, 'child.py', 'Caf\u00e9'], capture_output=True, encoding='utf-8', env=environment)
output = completed.stdout
```

PowerShell child: set its output encoding inside the command:

```python
import subprocess

command = "[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding $false; Write-Output ('Caf' + [char]0x00E9)"
completed = subprocess.run(['powershell.exe', '-NoProfile', '-Command', command], capture_output=True, encoding='utf-8')
```

Arguments (`['tool', 'Caf\u00e9']`) are passed as UTF-16 on Windows and arrive intact; prefer arguments and files over stdin text.

## 10. HTTP

Decode the body with the declared charset, UTF-8 as fallback:

```python
import json, urllib.request

with urllib.request.urlopen(url) as response:
  charset = response.headers.get_content_charset() or 'utf-8'
  body = response.read().decode(charset)
data = json.loads(body)
```

`requests` without `charset` in the header [VERIFIED: requests `get_encoding_from_headers`]: `text/*` decodes as ISO-8859-1 (mojibake in `response.text` and `response.json()`), `application/json` as UTF-8, other types are guessed. Safe for any type: `response.content.decode('utf-8')`, or set `response.encoding = 'utf-8'` before `response.text`.

## 11. Detection and Verification

Read with detection (BOM, then strict UTF-8, then declared fallback) - only at input boundaries for files of unknown origin, once per file (UNICODE-GN-05). One read, one decode; the caller logs the returned codec when it is the fallback:

```python
import codecs, locale
from pathlib import Path

# Order matters: UTF-32 LE BOM starts with the UTF-16 LE BOM. 'utf-16' / 'utf-32' / 'utf-8-sig' strip the BOM
BOM_CODECS = [(codecs.BOM_UTF32_LE, 'utf-32'), (codecs.BOM_UTF32_BE, 'utf-32'), (codecs.BOM_UTF8, 'utf-8-sig'), (codecs.BOM_UTF16_LE, 'utf-16'), (codecs.BOM_UTF16_BE, 'utf-16')]

# Returns (text, codec)
def read_text_detected(path: Path, fallback_codec: str = None) -> tuple:
  fallback_codec = fallback_codec or locale.getencoding()   # default: system ANSI code page, not a hard-coded cp1252
  data = path.read_bytes()
  for bom, codec in BOM_CODECS:
    if data.startswith(bom): return (data.decode(codec), codec)
  try:
    retVal = (data.decode('utf-8'), 'utf-8')
  except UnicodeDecodeError:
    retVal = (data.decode(fallback_codec), fallback_codec)
  return retVal
```

Detect mojibake (UTF-8 decoded as Windows-1252) - diagnostics and tests only, not per record in production (UNICODE-GN-07):

```python
import re

MOJIBAKE_RUN_PATTERN = re.compile(r'[\u0080-\uffff]{2,}')

# True if text contains runs like 'Ã©', 'Å‘', 'â€™' that reverse to valid UTF-8
def has_mojibake(text: str) -> bool:
  for match in MOJIBAKE_RUN_PATTERN.finditer(text):
    try:
      repaired = match.group(0).encode('cp1252').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
      continue
    if repaired != match.group(0): return True
  return False
```

`has_mojibake` is a check only and misses runs containing the 5 Windows-1252 bytes Python's `cp1252` codec does not map (e.g. `Á` = `C3 81` appears as `Ã` + U+0081). For repair use `repair_mojibake_win-1252.py` (handles undefined Windows-1252 bytes U+0081, U+008D, U+008F, U+0090, U+009D and multiple encoding levels).

Encoding test for a write path - test suite only, production code writes once without read-back (UNICODE-GN-07):

```python
from pathlib import Path

# pytest: write_report is the production writer under test
def test_write_report_utf8_without_bom(tmp_path: Path):
  sample = 'Caf\u00e9 \u0151 \u6771\u4eac \u20ac'
  output_path = tmp_path / 'report.txt'
  write_report(output_path, sample)
  assert output_path.read_bytes() == sample.encode('utf-8')   # exact bytes: no BOM, no '?', no U+FFFD
```

## 12. Anti-Patterns

- `open(path)`, `Path.read_text()`, `Path.write_text(text)` without `encoding` → locale encoding before 3.15
- `encoding='utf-8'` for reading files from Windows tools → BOM stays as `\ufeff`, breaks `json.loads`, `configparser`, first CSV column name
- `encoding='utf-8-sig'` for writing JSON, TOML, scripts → BOM
- `csv` without `newline=''` → `\r\r\n` on Windows
- `subprocess.run(..., text=True)` without `encoding` → locale decoding, child may crash with `UnicodeEncodeError`
- `errors='ignore'` / `errors='replace'` on stored data → silent data loss
- `text.encode('ascii', 'ignore')` to "clean" names → data loss; normalize with `unicodedata.normalize('NFC', text)` instead
- `json.dump(..., ensure_ascii=False)` into a stream opened without `encoding='utf-8'` → `UnicodeEncodeError` or ANSI file
- `tomllib.load(open(path))` → `TypeError: File must be opened in binary mode`
- `csv.reader(file, delimiter=';')` hard-coded for input → US files (`,`) load as one column. Use `detect_csv_delimiter`
- `encoding='cp1252'` as legacy fallback → wrong on Central European, Cyrillic, and East Asian systems. Use `locale.getencoding()` or the codec configured for the source
- Comparing user input or file names without NFC normalization → `Café` (NFD) != `Café` (NFC); fix once at input, not with `normalize()` inside comparison loops (UNICODE-GN-08)
- Re-reading a just-written file to verify it in production → doubles I/O. Prove the write path in a test (UNICODE-GN-07)
- Detecting the encoding of files with a known encoding, or per line → wasted work and false fallbacks. Detect once per file of unknown origin (UNICODE-GN-05)
