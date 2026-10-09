#!/usr/bin/env python3
"""
repair_mojibake_win-1252.py - Repair double-encoded UTF-8 text: UTF-8 bytes that were decoded as Windows-1252
(or Latin-1) and saved again as UTF-8.

Examples: 'CafÃ©' -> 'Café', 'MÃ¼ller' -> 'Müller', 'Å‘' -> 'ő', 'â€™' -> '’', 'ÃƒÂ©' -> 'é' (2 levels)

Method: each run of non-ASCII characters is encoded back to Windows-1252 bytes and decoded as strict UTF-8.
The run is replaced only if this succeeds; genuine text ('Café', 'Müller', '東京') does not form valid UTF-8 and
stays unchanged. Characters U+0080-U+009F map to bytes 0x80-0x9F, so the 5 bytes undefined in Windows-1252
(0x81, 0x8D, 0x8F, 0x90, 0x9D, kept by .NET as control characters) are restored losslessly.
BOM and line endings of the input are preserved.

Usage:
  python repair_mojibake_win-1252.py input.txt                   # repair in place
  python repair_mojibake_win-1252.py input.txt output.txt        # write repaired copy, input unchanged
  python repair_mojibake_win-1252.py input.txt --dry-run         # show changes, write nothing
  python repair_mojibake_win-1252.py input.txt --max-levels 1    # undo only one level of double encoding

Exit codes: 0 = OK (repaired or nothing to repair), 1 = error (file not found, input not valid UTF-8)
"""

import argparse, os, re, sys
from pathlib import Path

UTF8_BOM = b'\xef\xbb\xbf'
NON_ASCII_RUN_PATTERN = re.compile(r'[^\x00-\x7f]+')

# ----------------------------------------- START: Repair ---------------------------------------------------------------

# Reverse one level of 'UTF-8 bytes decoded as Windows-1252'. Returns the input unchanged if the result is not valid UTF-8.
def reverse_windows_1252_once(text: str) -> str:
  byte_values = bytearray()
  for character in text:
    code_point = ord(character)
    if code_point < 0x100:
      byte_values.append(code_point)   # Latin-1 range incl. U+0080-U+009F (undefined Windows-1252 bytes kept as controls)
      continue
    try:
      byte_values.extend(character.encode('cp1252'))
    except UnicodeEncodeError:
      return text   # character outside Windows-1252 (e.g. genuine CJK) -> run cannot be mojibake
  try:
    retVal = bytes(byte_values).decode('utf-8')
  except UnicodeDecodeError:
    return text
  return retVal

# Repeat reversal for multiple encoding levels
def repair_run(run: str, max_levels: int) -> str:
  retVal = run
  for level in range(max_levels):
    repaired = reverse_windows_1252_once(retVal)
    if repaired == retVal: break
    retVal = repaired
  return retVal

# Returns (repaired_text, changes) with changes = list of (line_number, original_run, repaired_run)
def repair_text(text: str, max_levels: int) -> tuple:
  segments = []
  changes = []
  position = 0
  for match in NON_ASCII_RUN_PATTERN.finditer(text):
    original_run = match.group(0)
    repaired_run = repair_run(original_run, max_levels)
    segments.append(text[position:match.start()])
    segments.append(repaired_run)
    position = match.end()
    if repaired_run != original_run:
      line_number = text.count('\n', 0, match.start()) + 1
      changes.append((line_number, original_run, repaired_run))
  segments.append(text[position:])
  retVal = (''.join(segments), changes)
  return retVal

# ----------------------------------------- END: Repair -----------------------------------------------------------------


# ----------------------------------------- START: File IO --------------------------------------------------------------

# Returns (text, has_bom). Raises UnicodeDecodeError if the file is not valid UTF-8.
def read_utf8_file(path: Path) -> tuple:
  data = path.read_bytes()
  has_bom = data.startswith(UTF8_BOM)
  if has_bom: data = data[len(UTF8_BOM):]
  retVal = (data.decode('utf-8'), has_bom)
  return retVal

# Write UTF-8 (BOM only if requested) via temp file + atomic replace. Line endings are written as contained in text.
def write_utf8_file(path: Path, text: str, has_bom: bool) -> None:
  data = text.encode('utf-8')
  if has_bom: data = UTF8_BOM + data
  temp_path = path.with_name(path.name + '.tmp_repair')
  temp_path.write_bytes(data)
  os.replace(temp_path, path)

# ----------------------------------------- END: File IO ----------------------------------------------------------------


# ----------------------------------------- START: Main -----------------------------------------------------------------

def parse_args():
  parser = argparse.ArgumentParser(description='Repair double-encoded UTF-8 text (UTF-8 decoded as Windows-1252). Preserves BOM and line endings.')
  parser.add_argument('input_file', type=Path, help='UTF-8 text file containing mojibake')
  parser.add_argument('output_file', type=Path, nargs='?', default=None, help='Output file (default: overwrite input file)')
  parser.add_argument('--dry-run', '-n', action='store_true', help='Show changes without writing')
  parser.add_argument('--max-levels', type=int, default=3, help='Maximum number of double-encoding levels to undo (default: 3)')
  return parser.parse_args()

def main():
  if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
  if hasattr(sys.stderr, 'reconfigure'): sys.stderr.reconfigure(encoding='utf-8', errors='backslashreplace')
  args = parse_args()
  input_file = args.input_file
  output_file = args.output_file if args.output_file else input_file

  if not input_file.is_file():
    print(f"ERROR: Input file not found: '{input_file}'.", file=sys.stderr)
    sys.exit(1)
  if args.max_levels < 1:
    print(f"ERROR: --max-levels must be 1 or higher, got {args.max_levels}.", file=sys.stderr)
    sys.exit(1)

  try:
    text, has_bom = read_utf8_file(input_file)
  except UnicodeDecodeError as error:
    print(f"ERROR: '{input_file}' is not valid UTF-8 (byte offset {error.start}) -> legacy-encoded, not mojibake. Read with its code page (e.g. cp1252), write UTF-8.", file=sys.stderr)
    sys.exit(1)

  repaired_text, changes = repair_text(text, args.max_levels)
  mode = "DRY RUN" if args.dry_run else ("IN PLACE" if output_file == input_file else "COPY")
  print(f"Repairing '{input_file}' ({mode}, BOM: {'yes' if has_bom else 'no'})...")
  for line_number, original_run, repaired_run in changes:
    print(f"  line {line_number}: '{original_run}' -> '{repaired_run}'")

  changed_line_numbers = set()
  for change in changes: changed_line_numbers.add(change[0])
  changed_lines = len(changed_line_numbers)
  run_word = "run" if len(changes) == 1 else "runs"
  line_word = "line" if changed_lines == 1 else "lines"

  if args.dry_run:
    print(f"OK. {len(changes)} {run_word} in {changed_lines} {line_word} would be repaired. Nothing written.")
    return
  if not changes and output_file == input_file:
    print("OK. Nothing to repair. File unchanged.")
    return
  try:
    write_utf8_file(output_file, repaired_text, has_bom)
  except OSError as error:
    print(f"ERROR: Writing '{output_file}' failed -> {error}", file=sys.stderr)
    sys.exit(1)
  print(f"OK. {len(changes)} {run_word} in {changed_lines} {line_word} repaired -> '{output_file}'.")

if __name__ == '__main__':
  main()

# ----------------------------------------- END: Main -------------------------------------------------------------------
