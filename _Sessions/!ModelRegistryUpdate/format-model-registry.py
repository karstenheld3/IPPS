"""Re-serialize model-registry.json to the canonical 1-line-per-entry layout.

Layout (matches registry <= v1.9.0):
  - Header keys (_version, _updated, _comment) one per line, blank line before each array
  - models[]:              4-space indent, compact {"k": v, ...} per line
  - model_id_startswith[]: 4-space indent, { "k": v, ... } per line (spaces inside braces)
  - temp_max rendered with 2 decimals (2.00)

Usage:
  python format-model-registry.py --registry-file <path> [--check]
  --check: exit 1 if file is not already in canonical layout, write nothing
"""
import argparse
import json
import sys
from pathlib import Path

def dump_scalar(value, key=None):
  if key == "temp_max" and isinstance(value, float):
    return f"{value:.2f}"
  return json.dumps(value, ensure_ascii=False)

def dump_compact(obj, key=None):
  if isinstance(obj, dict):
    parts = []
    for k, v in obj.items():
      parts.append(f"{json.dumps(k)}: {dump_compact(v, k)}")
    return "{" + ", ".join(parts) + "}"
  if isinstance(obj, list):
    return "[" + ", ".join(dump_compact(v) for v in obj) + "]"
  return dump_scalar(obj, key)

def format_registry(data: dict) -> str:
  lines = ["{"]
  header_keys = [k for k in data if not isinstance(data[k], list)]
  for i, k in enumerate(header_keys):
    comma = "," if i < len(header_keys) - 1 or any(isinstance(data[x], list) for x in data) else ""
    lines.append(f"  {json.dumps(k)}: {json.dumps(data[k], ensure_ascii=False)}{comma}")
  array_keys = [k for k in data if isinstance(data[k], list)]
  for ai, k in enumerate(array_keys):
    lines.append("  ")
    lines.append(f"  {json.dumps(k)}: [")
    items = data[k]
    spaced = k == "model_id_startswith"
    for ii, item in enumerate(items):
      body = dump_compact(item)
      if spaced:
        body = "{ " + body[1:-1] + " }"
      comma = "," if ii < len(items) - 1 else ""
      lines.append(f"    {body}{comma}")
    comma = "," if ai < len(array_keys) - 1 else ""
    lines.append(f"  ]{comma}")
  lines.append("}")
  return "\n".join(lines) + "\n"

def main():
  parser = argparse.ArgumentParser(description="Format model-registry.json to 1-line-per-entry layout")
  parser.add_argument("--registry-file", type=Path, required=True)
  parser.add_argument("--check", action="store_true", help="Verify only, exit 1 on mismatch")
  args = parser.parse_args()
  original_text = args.registry_file.read_text(encoding="utf-8")
  data = json.loads(original_text)
  formatted = format_registry(data)
  if json.loads(formatted) != data:
    print("ERROR: round-trip mismatch, aborting", file=sys.stderr)
    sys.exit(2)
  if args.check:
    if original_text == formatted:
      print(f"OK: {args.registry_file} is in canonical layout")
      sys.exit(0)
    print(f"FAIL: {args.registry_file} is not in canonical layout", file=sys.stderr)
    sys.exit(1)
  args.registry_file.write_text(formatted, encoding="utf-8")
  retVal = formatted.count("\n")
  print(f"Formatted {args.registry_file}: {len(data.get('models', []))} models, {len(data.get('model_id_startswith', []))} prefixes, {retVal} lines")

if __name__ == "__main__":
  main()
