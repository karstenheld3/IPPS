#!/usr/bin/env python3
"""
update-model-inventory.py - Regenerate the model tables in MODEL_INVENTORY.md from the llm-evaluation registries.

Label  = YY-L from release_date year and eci_band (anchor(YY) = 170 + 15 * (YY - 26), one letter per 5 ECI points, A-Z)
Comp   = same band expressed in the comparison year (wraps on May 1)
WF     = 2.0 * 2^(-(170 - eci_band) / 10) at High effort (halved for models without effort levels)

Usage:
  python update-model-inventory.py --skill-folder <skills/llm-evaluation> --inventory-file <MODEL_INVENTORY.md> [--today YYYY-MM-DD]
"""
import argparse
import datetime
import json
import pathlib
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
  sys.stdout.reconfigure(encoding="utf-8", errors="replace")
  sys.stderr.reconfigure(encoding="utf-8", errors="replace")

NON_TEXT = {"computer-use-preview", "gpt-image-1.5"}
EXCLUDED_STATUS = {"retired"}
HEADERS = ["Model", "Label", "Comp", "Profile", "Context", "Efforts", "WF", "In USD", "Cache USD", "Out USD", "Devin cost", "Notes"]
EFFORT_CODES = [("low", "L"), ("medium", "M"), ("high", "H"), ("xhigh", "X"), ("max", "MX")]
OLD_WF_COLS = [("Low", "L"), ("Medium", "M"), ("High", "H"), ("XHigh", "X"), ("Max", "MX")]

# Confirmed reliable CSV extraction rows per effort (LLM-Research TBLF-IN02 Section 5.1, May 2026)
CSV_ROWS = {
  "claude-opus-4-7": "M12 H843+", "gpt-5-mini": "L65 M500 H675+", "claude-opus-4-6": "M6 H667", "claude-opus-4-8": "H492",
  "gpt-5.4": "M492", "gpt-5": "L356 M450 H492", "gpt-5.5": "M437", "gpt-5.2": "M215", "claude-opus-4-5": "M177",
  "claude-sonnet-4-5": "M168", "claude-haiku-4-5": "9 (no thinking)", "gpt-4o-mini": "6", "gpt-4o": "4",
}
CSV_NOTE_PREFIX = "CSV rows"
ADAPTIVE_NOTE = "Medium may skip reasoning on structured data (TBLF E1)"


def anchor(yy):
  return 170 + 15 * (yy - 26)


def comp_year(today):
  retVal = today.year if today >= datetime.date(today.year, 5, 1) else today.year - 1
  return retVal % 100


def letter_index(yy, band_value):
  idx = (anchor(yy) - band_value) // 5
  if idx < 0:
    idx = 0
  if idx > 25:
    idx = 25
  return idx


def label_from(yy, band_value):
  return f"{yy:02d}-{chr(65 + letter_index(yy, band_value))}"


def band_from_label(label):
  yy_str, letter = label.split("-")
  retVal = anchor(int(yy_str)) - 5 * (ord(letter) - ord("A"))
  return retVal


def wf_high(band_value):
  return 2.0 * (2.0 ** (-(170 - band_value) / 10.0))


def fmt_wf(v):
  if v is None:
    return "-"
  steps = [0.03, 0.05, 0.06, 0.09, 0.13, 0.19, 0.25, 0.38, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0]
  best = steps[0]
  for s in steps:
    if abs(s - v) < abs(best - v):
      best = s
  retVal = f"{best:.2f}" if best < 0.1 else (f"{best:.1f}" if abs(best - round(best, 1)) < 1e-9 else f"{best:.2f}")
  return retVal


def fmt_price(v):
  if v is None:
    return "-"
  s = f"{float(v):.3f}"
  if s.endswith("0"):
    s = s[:-1]
  return s


def find_prefix(mid, prefixes):
  retVal = None
  for p in prefixes:
    if mid.startswith(p["prefix"]) and (retVal is None or len(p["prefix"]) > len(retVal["prefix"])):
      retVal = p
  return retVal


def efforts_for(mid, provider, prefix):
  if prefix is None:
    return "-"
  method = prefix.get("method")
  if method == "temperature":
    return "-"
  if method == "thinking":
    retVal = "M" if provider == "zai" else "L M H X"
    return retVal
  codes = []
  supported = set(prefix.get("effort", []))
  for name, code in EFFORT_CODES:
    if name in supported:
      codes.append(code)
  retVal = " ".join(codes) if codes else "-"
  return retVal


def wf_for(efforts, band_value):
  base = wf_high(band_value)
  if efforts in ("-", "M"):
    base = base * 0.5
  return fmt_wf(base)


def format_markdown_table(headers, rows):
  widths = [len(h) for h in headers]
  for r in rows:
    for i, cell in enumerate(r):
      if len(cell) > widths[i]:
        widths[i] = len(cell)
  lines = []
  lines.append("|" + "|".join(f" {headers[i].ljust(widths[i])} " for i in range(len(headers))) + "|")
  lines.append("|" + "|".join("-" * (widths[i] + 2) for i in range(len(headers))) + "|")
  for r in rows:
    lines.append("|" + "|".join(f" {r[i].ljust(widths[i])} " for i in range(len(headers))) + "|")
  return "\n".join(lines)


def parse_table(section_text):
  header = None
  retVal = {}
  for line in section_text.splitlines():
    if not line.startswith("|") or line.startswith("|--"):
      continue
    cols = [c.strip() for c in line.strip().strip("|").split("|")]
    if header is None:
      header = cols
      continue
    row = {}
    for i, name in enumerate(header):
      key = "Comp" if name.startswith("Comp") else name
      row[key] = cols[i] if i < len(cols) else ""
    retVal[row["Model"]] = row
  return retVal


def efforts_from_old_row(row):
  codes = []
  for col, code in OLD_WF_COLS:
    if row.get(col, "-") != "-":
      codes.append(code)
  retVal = " ".join(codes) if codes else "-"
  return retVal


def strip_cap_prefix(notes):
  parts = notes.split("; ", 1)
  if re.match(r"^UC-\d, (E\d{3} \([^)]*\)|ECI pending.*)$", parts[0]):
    retVal = parts[1] if len(parts) > 1 else ""
  else:
    retVal = notes
  return retVal


def cap_part(m):
  uc_short = m.get("uc_class", "").split(" ")[0] if m.get("uc_class") else "UC-?"
  band = m.get("eci_band", "-")
  if m.get("eci_band_source"):
    src = m["eci_band_source"].replace("sibling:", "sibling ").replace("uc_default", "UC default")
    retVal = f"{uc_short}, {band} (fallback {src})"
  elif m.get("eci_score") is not None:
    retVal = f"{uc_short}, {band} ({m['eci_score']:.2f})"
  else:
    retVal = f"{uc_short}, {band}"
  return retVal


def extra_notes(mid, short_id, m, p, prefix, existing_tail):
  parts = []
  if existing_tail:
    parts.append(existing_tail)
  if not existing_tail:
    if p.get("long_context") and p["long_context"].get("threshold_k"):
      lc = p["long_context"]
      parts.append(f"<={lc['threshold_k']}K tokens (${fmt_price(lc['input_per_1m'])}/${fmt_price(lc['output_per_1m'])} >{lc['threshold_k']}K)")
    if prefix is not None and prefix.get("method") == "temperature":
      parts.append("No reasoning effort")
  joined = "; ".join(parts) if len(parts) <= 1 else parts[0] + "; " + ", ".join(parts[1:])
  status_note = None
  if m.get("status") == "untested":
    status_note = "API untested"
  elif m.get("status") in ("legacy", "deprecated", "no_access"):
    status_note = f"Status {m['status']}"
  if status_note and status_note not in joined and not (m.get("status") == "deprecated" and "Deprecated" in joined):
    joined = (joined + "; " if joined else "") + status_note
  if short_id in CSV_ROWS and CSV_NOTE_PREFIX not in joined:
    joined = (joined + "; " if joined else "") + f"{CSV_NOTE_PREFIX} {CSV_ROWS[short_id]}"
  if prefix is not None and prefix.get("method") == "adaptive_thinking" and "Medium may skip" not in joined:
    joined = (joined + "; " if joined else "") + ADAPTIVE_NOTE
  return joined


def sort_key(row):
  comp_idx = ord(row[2].split("-")[1]) - ord("A")
  yy_str, letter = row[1].split("-")
  return (comp_idx, -int(yy_str), ord(letter), row[0].lower())


def main():
  parser = argparse.ArgumentParser(description="Regenerate MODEL_INVENTORY.md tables")
  parser.add_argument("--skill-folder", required=True, help="Path to skills/llm-evaluation")
  parser.add_argument("--inventory-file", required=True, help="Path to MODEL_INVENTORY.md")
  parser.add_argument("--today", default=None, help="Comparison date YYYY-MM-DD (default: today)")
  args = parser.parse_args()

  skill_dir = pathlib.Path(args.skill_folder)
  inv_path = pathlib.Path(args.inventory_file)
  today = datetime.date.fromisoformat(args.today) if args.today else datetime.date.today()
  cyy = comp_year(today)
  comp_header = f"Comp {cyy:02d}"
  headers = [comp_header if h == "Comp" else h for h in HEADERS]

  reg = json.loads((skill_dir / "model-registry.json").read_text(encoding="utf-8"))
  prc_doc = json.loads((skill_dir / "model-pricing.json").read_text(encoding="utf-8"))
  map_doc = json.loads((skill_dir / "model-parameter-mapping.json").read_text(encoding="utf-8"))
  prc = prc_doc["pricing"]
  inv_text = inv_path.read_text(encoding="utf-8")

  sec31_text = inv_text.split("### 3.1 API Models (llm-evaluation registry)")[1].split("### 3.2 Devin-Only Models")[0]
  existing_31 = parse_table(sec31_text)
  sec32_text = inv_text.split("### 3.2 Devin-Only Models (no API registry entry)")[1].split("\nModels not listed:")[0]
  existing_32 = parse_table(sec32_text)

  rows_31 = []
  for m in reg["models"]:
    mid = m["model_id"]
    if mid in NON_TEXT or m.get("status") in EXCLUDED_STATUS or not m.get("capability_label") or not m.get("eci_band") or not m.get("release_date"):
      continue
    short_id = re.sub(r"-\d{8}$", "", mid)
    prov = m["provider"]
    p = prc.get(prov, {}).get(mid) or prc.get(prov, {}).get(short_id)
    if not p:
      raise RuntimeError(f"Missing pricing entry in model-pricing.json for {prov}/{mid}")
    prefix = find_prefix(mid, reg["model_id_startswith"])
    band_value = int(m["eci_band"][1:])
    yy = int(m["release_date"][2:4])
    label = label_from(yy, band_value)
    if label != m["capability_label"]:
      raise RuntimeError(f"capability_label {m['capability_label']} for {mid} does not match release_date + eci_band ({label}); rerun the registry derivation")
    comp = label_from(cyy, band_value)
    efforts = efforts_for(mid, prov, prefix)
    ctx_val = m.get("context_window")
    ctx_str = f"{round(ctx_val / 1000)}K" if ctx_val else "-"
    ex = existing_31.get(short_id)
    devin_cost = ex["Devin cost"] if ex else "-"
    tail = strip_cap_prefix(ex["Notes"]) if ex else ""
    extra = extra_notes(mid, short_id, m, p, prefix, tail)
    notes = cap_part(m) + ("; " + extra if extra else "")
    rows_31.append([short_id, label, comp, m.get("behavior_profile", "standard"), ctx_str, efforts, wf_for(efforts, band_value),
                    fmt_price(p.get("input_per_1m")), fmt_price(p.get("cached_per_1m")), fmt_price(p.get("output_per_1m")), devin_cost, notes])
  rows_31.sort(key=sort_key)

  rows_32 = []
  for name, ex in existing_32.items():
    label = ex["Label"]
    band_value = band_from_label(label)
    comp = label_from(cyy, band_value)
    efforts = ex["Efforts"] if "Efforts" in ex else efforts_from_old_row(ex)
    mult = float(ex["Devin cost"].rstrip("x"))
    rows_32.append([name, label, comp, ex.get("Profile", "standard"), ex.get("Context", "-"), efforts, wf_for(efforts, band_value),
                    fmt_price(mult * 0.50), "-", fmt_price(mult * 2.50), ex["Devin cost"], ex["Notes"]])
  rows_32.sort(key=sort_key)

  table_31 = format_markdown_table(headers, rows_31)
  table_32 = format_markdown_table(headers, rows_32)

  inv_text = re.sub(r"- `skills/llm-evaluation/model-registry\.json` [0-9.]+ \(\d{4}-\d{2}-\d{2}\)", f"- `skills/llm-evaluation/model-registry.json` {reg['_version']} ({reg['_updated']})", inv_text)
  inv_text = re.sub(r"- `skills/llm-evaluation/model-pricing\.json` \(\d{4}-\d{2}-\d{2}\)", f"- `skills/llm-evaluation/model-pricing.json` ({prc_doc['last_updated']})", inv_text)
  inv_text = re.sub(r"- `skills/llm-evaluation/model-parameter-mapping\.json` [0-9.]+ \(\d{4}-\d{2}-\d{2}\)", f"- `skills/llm-evaluation/model-parameter-mapping.json` {map_doc['_version']} ({map_doc['_updated']})", inv_text)
  inv_text = re.sub(r"Comparison year: `\d{2}` \(generated \d{4}-\d{2}-\d{2}\)", f"Comparison year: `{cyy:02d}` (generated {today.isoformat()})", inv_text)
  inv_text = re.sub(r"(### 3\.1 API Models \(llm-evaluation registry\)\r?\n\r?\n)(\|[\s\S]*?)(\r?\n\r?\n### 3\.2 Devin-Only Models)", lambda mm: mm.group(1) + table_31 + mm.group(3), inv_text)
  inv_text = re.sub(r"(### 3\.2 Devin-Only Models \(no API registry entry\)\r?\n\r?\n.*?\r?\n\r?\n)(\|[\s\S]*?)(\r?\n\r?\nModels not listed:)", lambda mm: mm.group(1) + table_32 + mm.group(3), inv_text)

  inv_path.write_text(inv_text, encoding="utf-8")
  print(f"Updated {inv_path}: {len(rows_31)} Section 3.1 rows, {len(rows_32)} Section 3.2 rows, comparison year {cyy:02d}")


if __name__ == "__main__":
  main()
