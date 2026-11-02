#!/usr/bin/env python3
"""
update-model-inventory.py - Regenerate the model tables of MODEL_INVENTORY.md from the llm-tools registries (MDLRGUP-MDLINVNTRY-SP01 FR-08, FR-13, IG-04).

Columns: Model | Depth | Items | Context | Efforts | In USD | Cache USD | Out USD | Devin cost | Notes
  Depth  D[n] from registry depth, D[n]* when depth_estimated
  Items  registry items as [n]m (measured), else the default from the rung: D10+ 8, D7-D9 6, D4-D6 5, D1-D3 4
  Notes  depth_evidence; UC-n; Epoch score [interval] or "no Epoch score"; status; scope guard strict; long-context price; No reasoning effort; inventory_note; CSV rows; adaptive Medium warning
Section 3.1: every text model not retired, sorted by 1) Depth descending, 2) Model ascending. Section 3.2: hand-maintained Devin-only rows (Depth, Context, Efforts, Devin cost, Notes kept; Items and prices recomputed).
Header line "Top rung: D[n] (YYYY-MM-DD)" = maximum depth in Section 3.1, dated --today.

Usage:
  python update-model-inventory.py --skill-folder <skills/llm-tools> --inventory-file <skills/llm-tools/MODEL_INVENTORY.md> [--today YYYY-MM-DD]
"""
import argparse, datetime, json, pathlib, re, sys

if hasattr(sys.stdout, "reconfigure"):
  sys.stdout.reconfigure(encoding="utf-8", errors="replace")
  sys.stderr.reconfigure(encoding="utf-8", errors="replace")

NON_TEXT = {"computer-use-preview", "gpt-image-1.5"}
EXCLUDED_STATUS = {"retired"}
HEADERS = ["Model", "Depth", "Items", "Context", "Efforts", "In USD", "Cache USD", "Out USD", "Devin cost", "Notes"]
EFFORT_CODES = [("low", "L"), ("medium", "M"), ("high", "H"), ("xhigh", "X"), ("max", "MX")]
SECTION_31 = "### 3.1 API Models (llm-tools registry)"
SECTION_32 = "### 3.2 Devin-Only Models (no API registry entry)"

# Confirmed reliable CSV extraction rows per effort (LLM-Research TBLF-IN02 Section 5.1, May 2026)
CSV_ROWS = {
  "claude-opus-4-7": "M12 H843+", "gpt-5-mini": "L65 M500 H675+", "claude-opus-4-6": "M6 H667", "claude-opus-4-8": "H492",
  "gpt-5.4": "M492", "gpt-5": "L356 M450 H492", "gpt-5.5": "M437", "gpt-5.2": "M215", "claude-opus-4-5": "M177",
  "claude-sonnet-4-5": "M168", "claude-haiku-4-5": "9 (no thinking)", "gpt-4o-mini": "6", "gpt-4o": "4",
}
ADAPTIVE_NOTE = "adaptive: Medium may skip reasoning (TBLF E1)"

# ----------------------------------------- START: Cell formatting -------------------------------------------------------------

def fmt_price(value):
  if value is None: return "-"
  retVal = f"{float(value):.3f}"
  if retVal.endswith("0"): retVal = retVal[:-1]
  return retVal

def default_items(depth):
  retVal = 4
  if depth >= 10: retVal = 8
  elif depth >= 7: retVal = 6
  elif depth >= 4: retVal = 5
  return retVal

def depth_number(depth_cell):
  return int(depth_cell.lstrip("D").rstrip("*"))

def find_prefix(model_id, prefixes):
  retVal = None
  for prefix in prefixes:
    if model_id.startswith(prefix["prefix"]) and (retVal is None or len(prefix["prefix"]) > len(retVal["prefix"])): retVal = prefix
  return retVal

def efforts_for(provider, prefix):
  if prefix is None or prefix.get("method") == "temperature": return "-"
  if prefix.get("method") == "thinking": return "M" if provider == "zai" else "L M H X"
  codes = []
  supported = set(prefix.get("effort", []))
  for name, code in EFFORT_CODES:
    if name in supported: codes.append(code)
  return " ".join(codes) if codes else "-"

def epoch_part(model):
  interval = model.get("eci_ci")
  if model.get("eci_score") is None: return "no Epoch score"
  if not interval: return f"{model['eci_score']:.1f} (no interval)"
  return f"{model['eci_score']:.1f} [{interval[0]:.1f}-{interval[1]:.1f}]"

def notes_for(short_id, model, pricing_entry, prefix):
  parts = [model.get("depth_evidence", "no depth"), (model.get("uc_class") or "UC-?").split(" ")[0], epoch_part(model)]
  status = model.get("status")
  if status == "untested": parts.append("API untested")
  elif status in ("legacy", "deprecated", "no_access"): parts.append(f"Status {status}")
  if model.get("scope_guard") == "strict": parts.append("scope guard strict")
  long_context = pricing_entry.get("long_context")
  if long_context and long_context.get("threshold_k"):
    parts.append(f"<={long_context['threshold_k']}K tokens (${fmt_price(long_context['input_per_1m'])}/${fmt_price(long_context['output_per_1m'])} >{long_context['threshold_k']}K)")
  if prefix is not None and prefix.get("method") == "temperature": parts.append("No reasoning effort")
  if model.get("inventory_note"): parts.append(model["inventory_note"])
  if short_id in CSV_ROWS: parts.append(f"CSV rows {CSV_ROWS[short_id]}")
  if prefix is not None and prefix.get("method") == "adaptive_thinking": parts.append(ADAPTIVE_NOTE)
  return "; ".join(parts)

def format_markdown_table(headers, rows):
  widths = []
  for header in headers:
    widths.append(len(header))
  for row in rows:
    for index, cell in enumerate(row):
      if len(cell) > widths[index]: widths[index] = len(cell)
  lines = []
  lines.append("|" + "|".join(f" {headers[i].ljust(widths[i])} " for i in range(len(headers))) + "|")
  lines.append("|" + "|".join("-" * (widths[i] + 2) for i in range(len(headers))) + "|")
  for row in rows:
    lines.append("|" + "|".join(f" {row[i].ljust(widths[i])} " for i in range(len(headers))) + "|")
  return "\n".join(lines)

def parse_table(section_text):
  header = None
  retVal = {}
  for line in section_text.splitlines():
    if not line.startswith("|") or line.startswith("|--"): continue
    cells = []
    for cell in line.strip().strip("|").split("|"):
      cells.append(cell.strip())
    if header is None:
      header = cells
      continue
    row = {}
    for index, name in enumerate(header):
      row[name] = cells[index] if index < len(cells) else ""
    retVal[row["Model"]] = row
  return retVal

def sort_key(row):
  return (-depth_number(row[1]), row[0].lower())

# ----------------------------------------- END: Cell formatting ---------------------------------------------------------------


# ----------------------------------------- START: Main ------------------------------------------------------------------------

def main():
  parser = argparse.ArgumentParser(description="Regenerate MODEL_INVENTORY.md tables from the llm-tools registries")
  parser.add_argument("--skill-folder", required=True, help="Path to skills/llm-tools (holds the 3 model JSONs)")
  parser.add_argument("--inventory-file", required=True, help="Path to MODEL_INVENTORY.md")
  parser.add_argument("--today", default=None, help="Generation date YYYY-MM-DD for the Top rung line (default: today)")
  args = parser.parse_args()
  skill_dir = pathlib.Path(args.skill_folder)
  inventory_path = pathlib.Path(args.inventory_file)
  today = args.today or datetime.date.today().isoformat()
  registry = json.loads((skill_dir / "model-registry.json").read_text(encoding="utf-8"))
  pricing_doc = json.loads((skill_dir / "model-pricing.json").read_text(encoding="utf-8"))
  mapping_doc = json.loads((skill_dir / "model-parameter-mapping.json").read_text(encoding="utf-8"))
  pricing = pricing_doc["pricing"]
  inventory_text = inventory_path.read_text(encoding="utf-8")
  existing_31 = parse_table(inventory_text.split(SECTION_31)[1].split(SECTION_32)[0])
  existing_32 = parse_table(inventory_text.split(SECTION_32)[1].split("\nModels not listed:")[0])

  rows_31 = []
  for model in registry["models"]:
    model_id = model["model_id"]
    if model_id in NON_TEXT or model.get("status") in EXCLUDED_STATUS: continue
    if model.get("depth") is None: raise RuntimeError(f"{model_id} has no depth; run layer-depth-ladder.py first (MDLRGUP-MDLINVNTRY-FR-01)")
    short_id = re.sub(r"-\d{8}$", "", model_id)
    provider = model["provider"]
    pricing_entry = pricing.get(provider, {}).get(model_id) or pricing.get(provider, {}).get(short_id)
    if not pricing_entry: raise RuntimeError(f"Missing pricing entry in model-pricing.json for {provider}/{model_id}")
    prefix = find_prefix(model_id, registry["model_id_startswith"])
    depth_cell = f"D{model['depth']}" + ("*" if model.get("depth_estimated") else "")
    items_cell = f"{model['items']}m" if model.get("items") else str(default_items(model["depth"]))
    context = model.get("context_window")
    context_cell = f"{round(context / 1000)}K" if context else "-"
    existing = existing_31.get(short_id)
    devin_cost = existing["Devin cost"] if existing else "-"
    rows_31.append([short_id, depth_cell, items_cell, context_cell, efforts_for(provider, prefix), fmt_price(pricing_entry.get("input_per_1m")),
                    fmt_price(pricing_entry.get("cached_per_1m")), fmt_price(pricing_entry.get("output_per_1m")), devin_cost, notes_for(short_id, model, pricing_entry, prefix)])
  rows_31.sort(key=sort_key)

  rows_32 = []
  for name, existing in existing_32.items():
    if "Depth" not in existing: raise RuntimeError(f"Section 3.2 row '{name}' has no Depth column; convert the table to the depth ladder layout first")
    multiplier = float(existing["Devin cost"].rstrip("x"))
    rows_32.append([name, existing["Depth"], str(default_items(depth_number(existing["Depth"]))), existing.get("Context", "-"), existing["Efforts"],
                    fmt_price(multiplier * 0.50), "-", fmt_price(multiplier * 2.50), existing["Devin cost"], existing["Notes"]])
  rows_32.sort(key=sort_key)

  top_rung = 0
  for row in rows_31:
    if depth_number(row[1]) > top_rung: top_rung = depth_number(row[1])
  table_31 = format_markdown_table(HEADERS, rows_31)
  table_32 = format_markdown_table(HEADERS, rows_32)
  inventory_text = re.sub(r"- `skills/llm-tools/model-registry\.json` [0-9.]+ \(\d{4}-\d{2}-\d{2}\)", f"- `skills/llm-tools/model-registry.json` {registry['_version']} ({registry['_updated']})", inventory_text)
  inventory_text = re.sub(r"- `skills/llm-tools/model-pricing\.json` \(\d{4}-\d{2}-\d{2}\)", f"- `skills/llm-tools/model-pricing.json` ({pricing_doc['last_updated']})", inventory_text)
  inventory_text = re.sub(r"- `skills/llm-tools/model-parameter-mapping\.json` [0-9.]+ \(\d{4}-\d{2}-\d{2}\)", f"- `skills/llm-tools/model-parameter-mapping.json` {mapping_doc['_version']} ({mapping_doc['_updated']})", inventory_text)
  inventory_text = re.sub(r"Top rung: D\d+ \(\d{4}-\d{2}-\d{2}\)", f"Top rung: D{top_rung} ({today})", inventory_text)
  inventory_text = re.sub(r"(### 3\.1 API Models \(llm-tools registry\)\r?\n\r?\n)(\|[\s\S]*?)(\r?\n\r?\n### 3\.2 Devin-Only Models)", lambda match: match.group(1) + table_31 + match.group(3), inventory_text)
  inventory_text = re.sub(r"(### 3\.2 Devin-Only Models \(no API registry entry\)\r?\n\r?\n.*?\r?\n\r?\n)(\|[\s\S]*?)(\r?\n\r?\nModels not listed:)", lambda match: match.group(1) + table_32 + match.group(3), inventory_text)
  inventory_path.write_text(inventory_text, encoding="utf-8")
  print(f"Updated {inventory_path}: {len(rows_31)} Section 3.1 rows, {len(rows_32)} Section 3.2 rows, Top rung D{top_rung} ({today}).")

if __name__ == "__main__":
  main()

# ----------------------------------------- END: Main --------------------------------------------------------------------------
