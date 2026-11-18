#!/usr/bin/env python3
"""
update-model-inventory.py - Regenerate the model tables of MODEL_INVENTORY.md from the llm-tools registries (MDLRGUP-MDLINVNTRY-SP01 FR-08, FR-13, IG-04).

Section 3.1 columns: Model | Depth | ECI Score | Items | Context | Efforts | In USD | Cache USD | Out USD | Value | Notes
  Depth  D[n] from registry depth, D[n]* when depth_estimated
  ECI Score  registry eci_score with 1 decimal, "-" when no Epoch score
  Items  registry items as [n]m (measured), else the default from the rung: D10+ 8, D7-D9 6, D4-D6 5, D1-D3 4
  Context  `floor(context_window / 1000)` from `model-registry.json`, suffixed with `K`; `-` when the registry value is `null`
  Value  price score within the rung (DD-20): 1 + 4 * (ln(max_cost) - ln(cost)) / (ln(max_cost) - ln(min_cost)), cost = 0.8 * In + 0.2 * Out, free models cost 0.01;
         shown as five star symbols (full, half, empty; nearest 0.5) plus the score with 1 decimal; "-" when the rung has one model, all costs are equal, or the row has no price
  Notes  depth_evidence; UC-n; Epoch score [interval] or "no Epoch score"; status; scope guard strict; long-context price; No reasoning effort; inventory_note; CSV rows; adaptive Medium warning
Section 3.1: every text model not retired, sorted by 1) Depth descending, 2) Model ascending.
Section 3.2 "Devin Model Deviations" (DD-22, only with --devin-dom-file; otherwise left unchanged): Model | Depth | Items | Efforts | In USD | Cache USD | Out USD | Notes
  Source: Self-serve tab of the Devin DOM file. A Devin model is listed when it has no registry model or when its In, Cache read, or Out price differs from Section 3.1 by more than 0.5%.
  Rungs of Devin-only models come from devin_only[] of --depth-edges-file (set once by a vendor statement, EC-6), D[n]*.
Header line "Top rung: D[n] (YYYY-MM-DD)" = maximum depth in Section 3.1, dated --today.

Usage:
  python update-model-inventory.py --skill-folder <skills/llm-tools> --inventory-file <skills/llm-tools/MODEL_INVENTORY.md> [--today YYYY-MM-DD]
    [--devin-dom-file <[DATE]_Devin-Models-DOM.json> --depth-edges-file <[DATE]_Depth-Edges.json>]
"""
import argparse, datetime, json, math, pathlib, re, sys

if hasattr(sys.stdout, "reconfigure"):
  sys.stdout.reconfigure(encoding="utf-8", errors="replace")
  sys.stderr.reconfigure(encoding="utf-8", errors="replace")

NON_TEXT = {"computer-use-preview", "gpt-image-1.5"}
EXCLUDED_STATUS = {"retired"}
HEADERS_31 = ["Model", "Depth", "ECI Score", "Items", "Context", "Efforts", "In USD", "Cache USD", "Out USD", "Value", "Notes"]
HEADERS_32 = ["Model", "Depth", "Items", "Efforts", "In USD", "Cache USD", "Out USD", "Notes"]
EFFORT_CODES = [("low", "L"), ("medium", "M"), ("high", "H"), ("xhigh", "X"), ("max", "MX")]
DEVIN_EFFORT_WORDS = {"Low": "L", "Medium": "M", "High": "H", "XHigh": "X", "Max": "MX"}
DEVIN_STRIP_WORDS = set(DEVIN_EFFORT_WORDS) | {"Thinking", "Fast"}
DEVIN_NAME_MAP = {}
DEVIN_TAB_SELF_SERVE = "Self-serve"
DEVIN_TAB_ENTERPRISE = "Enterprise (ACUs)"
PRICE_TOLERANCE = 0.005
FREE_COST_FLOOR = 0.01
SECTION_31 = "### 3.1 API Models (llm-tools registry)"
SECTION_32_PATTERN = r"### 3\.2 [^\r\n]*"
SECTION_32_HEADING = "### 3.2 Devin Model Deviations"
STAR_FULL, STAR_HALF, STAR_EMPTY = "\u2605", "\u2bea", "\u2606"

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
  if prefix.get("method") == "thinking":
    if provider in ("deepseek", "moonshot"): return "on/off"
    return "M" if provider == "zai" else "L M H X"
  codes = []
  supported = set(prefix.get("effort", []))
  for name, code in EFFORT_CODES:
    if name in supported: codes.append(code)
  return " ".join(codes) if codes else "-"

def eci_cell(model):
  retVal = "-"
  if model.get("eci_score") is not None: retVal = f"{model['eci_score']:.1f}"
  return retVal

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
  if pricing_entry.get("off_peak_factor"): parts.append(f"off-peak price x{pricing_entry['off_peak_factor']:g}")
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

def blended_cost(price_in, price_out):
  retVal = 0.8 * price_in + 0.2 * price_out
  if retVal < FREE_COST_FLOOR: retVal = FREE_COST_FLOOR
  return retVal

def star_text(score):
  rounded = round(score, 1)
  half_steps = int(math.floor(rounded * 2 + 0.5))
  full = half_steps // 2
  has_half = half_steps % 2 == 1
  empty = 5 - full - (1 if has_half else 0)
  return STAR_FULL * full + (STAR_HALF if has_half else "") + STAR_EMPTY * empty + f" ({rounded:.1f})"

def value_cells(entries):
  groups = {}
  for short_id, depth, cost in entries:
    if cost is not None: groups.setdefault(depth, []).append(cost)
  retVal = {}
  for short_id, depth, cost in entries:
    retVal[short_id] = "-"
    if cost is None: continue
    low, high = min(groups[depth]), max(groups[depth])
    if len(groups[depth]) < 2 or high <= low * (1 + 1e-9): continue
    retVal[short_id] = star_text(1 + 4 * (math.log(high) - math.log(cost)) / (math.log(high) - math.log(low)))
  return retVal

def sort_key(row):
  return (-depth_number(row[1]), row[0].lower())

def parse_devin_price(cell):
  match = re.match(r"^\$([0-9.]+)$", cell.strip())
  return float(match.group(1)) if match else None

def devin_words(display_name):
  return display_name.replace("\u2020", "").split()

def devin_family_name(display_name):
  words = devin_words(display_name)
  while words and words[-1] in DEVIN_STRIP_WORDS: words.pop()
  return " ".join(words)

def match_registry_id(family_name, known_ids):
  if DEVIN_NAME_MAP.get(family_name): return DEVIN_NAME_MAP[family_name]
  slug = family_name.lower().replace(" ", "-")
  for candidate in (slug, slug.replace(".", "-")):
    if candidate in known_ids: return candidate
  return None

def prices_differ(devin_price, registry_price):
  if devin_price is None and registry_price is None: return False
  if devin_price is None or registry_price is None: return True
  return abs(devin_price - registry_price) > PRICE_TOLERANCE * max(abs(registry_price), 1e-9)

def active_promotions(devin_doc, family_name, today):
  retVal = []
  for promo in devin_doc.get("promotions", []):
    if promo.get("model") != family_name: continue
    if (promo.get("until") and promo["until"] >= today) or (promo.get("from") and promo["from"] > today): retVal.append(promo)
  return retVal

def promotion_note(promo):
  tab = "Enterprise" if promo["tab"].startswith("Enterprise") else promo["tab"]
  boundary = f"until {promo['until']}" if promo.get("until") else f"from {promo['from']}"
  prices = ""
  if promo.get("list_input") is not None and promo.get("list_output") is not None:
    prices = f", list ${fmt_price(promo['list_input'])}/${fmt_price(promo['list_output'])}"
  return f"{tab} {promo['kind']} {boundary}{prices}"

def build_deviation_rows(devin_doc, devin_only, rows_by_id, prices_by_id, today):
  tab_rows = devin_doc["tabs"][DEVIN_TAB_SELF_SERVE]
  enterprise_rows = {}
  for row in devin_doc["tabs"].get(DEVIN_TAB_ENTERPRISE, [])[1:]: enterprise_rows[row[0]] = row
  families, order = {}, []
  for row in tab_rows[1:]:
    family = devin_family_name(row[0])
    if family not in families:
      families[family] = {"prices": None, "efforts": set(), "enterprise_differs": False}
      order.append(family)
    entry = families[family]
    for word in devin_words(row[0]):
      if word in DEVIN_EFFORT_WORDS: entry["efforts"].add(DEVIN_EFFORT_WORDS[word])
    prices = [parse_devin_price(row[1]), parse_devin_price(row[2]), parse_devin_price(row[4])]
    if prices[0] is not None and entry["prices"] is None: entry["prices"] = prices
    enterprise = enterprise_rows.get(row[0])
    if enterprise and [enterprise[1], enterprise[2], enterprise[4]] != [row[1], row[2], row[4]]: entry["enterprise_differs"] = True

  retVal = []
  for family in order:
    entry = families[family]
    promos = active_promotions(devin_doc, family, today)
    prices = entry["prices"]
    if prices is None:
      prices = [None, None, None]
      for promo in promos:
        if promo.get("list_input") is not None and promo["tab"] == DEVIN_TAB_SELF_SERVE and promo["kind"] == "free":
          prices = [promo["list_input"], promo.get("list_cache_read"), promo["list_output"]]
          break
    matched = match_registry_id(family, rows_by_id)
    notes = []
    if matched:
      registry_prices = prices_by_id[matched]
      if not any(prices_differ(prices[index], registry_prices[index]) for index in range(3)): continue
      depth_cell, items_cell = rows_by_id[matched][1], rows_by_id[matched][3]
      notes.append(f"Devin price differs from Section 3.1 (${fmt_price(registry_prices[0])}/${fmt_price(registry_prices[1])}/${fmt_price(registry_prices[2])})".replace("$-", "-"))
      name = matched
    else:
      placed = devin_only.get(family)
      depth_cell = f"D{placed['depth']}*" if placed else "D1*"
      items_cell = str(default_items(depth_number(depth_cell)))
      if placed: entry["efforts"] |= set(placed.get("efforts", []))
      notes.append(f"{placed['evidence']}; {placed['statement']}" if placed else "unplaced")
      notes.append("no registry model")
      name = family
    for promo in promos: notes.append(promotion_note(promo))
    if entry["enterprise_differs"]: notes.append("Enterprise prices differ from Self-serve")
    efforts_cell = " ".join(code for _, code in EFFORT_CODES if code in entry["efforts"]) or "-"
    retVal.append([name, depth_cell, items_cell, efforts_cell, fmt_price(prices[0]), fmt_price(prices[1]), fmt_price(prices[2]), "; ".join(notes)])
  retVal.sort(key=sort_key)
  return retVal

# ----------------------------------------- END: Cell formatting ---------------------------------------------------------------


# ----------------------------------------- START: Main ------------------------------------------------------------------------

def main():
  parser = argparse.ArgumentParser(description="Regenerate MODEL_INVENTORY.md tables from the llm-tools registries")
  parser.add_argument("--skill-folder", required=True, help="Path to skills/llm-tools (holds the 3 model JSONs)")
  parser.add_argument("--inventory-file", required=True, help="Path to MODEL_INVENTORY.md")
  parser.add_argument("--today", default=None, help="Generation date YYYY-MM-DD for the Top rung line (default: today)")
  parser.add_argument("--devin-dom-file", default=None, help="[DATE]_Devin-Models-DOM.json; regenerates Section 3.2 (omitted: Section 3.2 stays unchanged)")
  parser.add_argument("--depth-edges-file", default=None, help="[DATE]_Depth-Edges.json; devin_only[] holds the rungs of Devin-only models")
  args = parser.parse_args()
  skill_dir = pathlib.Path(args.skill_folder)
  inventory_path = pathlib.Path(args.inventory_file)
  today = args.today or datetime.date.today().isoformat()
  registry = json.loads((skill_dir / "model-registry.json").read_text(encoding="utf-8"))
  pricing_doc = json.loads((skill_dir / "model-pricing.json").read_text(encoding="utf-8"))
  mapping_doc = json.loads((skill_dir / "model-parameter-mapping.json").read_text(encoding="utf-8"))
  pricing = pricing_doc["pricing"]
  inventory_text = inventory_path.read_text(encoding="utf-8")

  rows_31 = []
  entries = []
  rows_by_id = {}
  prices_by_id = {}
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
    context_cell = f"{math.floor(context / 1000)}K" if context else "-"
    price_in, price_cache, price_out = pricing_entry.get("input_per_1m"), pricing_entry.get("cached_per_1m"), pricing_entry.get("output_per_1m")
    cost = blended_cost(price_in, price_out) if price_in is not None and price_out is not None else None
    entries.append((short_id, model["depth"], cost))
    prices_by_id[short_id] = (price_in, price_cache, price_out)
    row = [short_id, depth_cell, eci_cell(model), items_cell, context_cell, efforts_for(provider, prefix), fmt_price(price_in), fmt_price(price_cache), fmt_price(price_out), "-",
           notes_for(short_id, model, pricing_entry, prefix)]
    rows_by_id[short_id] = row
    rows_31.append(row)
  values = value_cells(entries)
  for row in rows_31: row[9] = values[row[0]]
  rows_31.sort(key=sort_key)

  table_32_block = None
  deviation_count = 0
  if args.devin_dom_file:
    devin_doc = json.loads(pathlib.Path(args.devin_dom_file).read_text(encoding="utf-8"))
    devin_only = {}
    if args.depth_edges_file and pathlib.Path(args.depth_edges_file).exists():
      edges_doc = json.loads(pathlib.Path(args.depth_edges_file).read_text(encoding="utf-8"))
      for item in edges_doc.get("devin_only", []): devin_only[item["model"]] = item
    rows_32 = build_deviation_rows(devin_doc, devin_only, rows_by_id, prices_by_id, today)
    deviation_count = len(rows_32)
    price_date = devin_doc.get("page_price_date") or "unknown"
    description = (f"Source: `https://docs.devin.ai/desktop/models` Self-serve tab, prices as of {price_date}, read {today}. Lists only Devin models without a `model-registry.json` entry or with an In, Cache read, "
                   "or Out price that differs from Section 3.1 by more than 0.5%; every other Devin model equals Section 3.1. Model = registry ID when matched, Devin display name otherwise. "
                   "Devin-only rungs are set once from a vendor statement (EC-6) and marked `*`; prices are the Self-serve table price, or the list price where the table shows Free; "
                   "Efforts = the effort variant shown in the Self-serve table for that row; the Devin page also states that SWE-2 and SWE-2 Flash offer Medium, High, and Max reasoning-effort variants.")
    table_32_block = SECTION_32_HEADING + "\n\n" + description + "\n\n" + format_markdown_table(HEADERS_32, rows_32)

  top_rung = 0
  for row in rows_31:
    if depth_number(row[1]) > top_rung: top_rung = depth_number(row[1])
  table_31 = format_markdown_table(HEADERS_31, rows_31)
  inventory_text = re.sub(r"- `skills/llm-tools/model-registry\.json` [0-9.]+ \(\d{4}-\d{2}-\d{2}\)", f"- `skills/llm-tools/model-registry.json` {registry['_version']} ({registry['_updated']})", inventory_text)
  inventory_text = re.sub(r"- `skills/llm-tools/model-pricing\.json` \(\d{4}-\d{2}-\d{2}\)", f"- `skills/llm-tools/model-pricing.json` ({pricing_doc['last_updated']})", inventory_text)
  inventory_text = re.sub(r"- `skills/llm-tools/model-parameter-mapping\.json` [0-9.]+ \(\d{4}-\d{2}-\d{2}\)", f"- `skills/llm-tools/model-parameter-mapping.json` {mapping_doc['_version']} ({mapping_doc['_updated']})", inventory_text)
  inventory_text = re.sub(r"Top rung: D\d+ \(\d{4}-\d{2}-\d{2}\)", f"Top rung: D{top_rung} ({today})", inventory_text)
  inventory_text = re.sub(r"(### 3\.1 API Models \(llm-tools registry\)\r?\n\r?\n)(\|[\s\S]*?)(\r?\n\r?\n### 3\.2 )", lambda match: match.group(1) + table_31 + match.group(3), inventory_text)
  if table_32_block is not None:
    inventory_text = re.sub(SECTION_32_PATTERN + r"\r?\n\r?\n[\s\S]*?(?=\r?\n\r?\nModels not listed:)", lambda match: table_32_block, inventory_text)
  inventory_path.write_text(inventory_text, encoding="utf-8")
  section_32_text = f"{deviation_count} Section 3.2 rows" if table_32_block is not None else "Section 3.2 unchanged"
  print(f"Updated {inventory_path}: {len(rows_31)} Section 3.1 rows, {section_32_text}, Top rung D{top_rung} ({today}).")
  if args.devin_dom_file:
    for promo in devin_doc.get("promotions", []):
      boundary = promo.get("until") or promo.get("from")
      if boundary and boundary >= today: print(f"PROMOTION: {promo['model']} / {promo['tab']} / {promo['kind']} / {boundary}")

if __name__ == "__main__":
  main()

# ----------------------------------------- END: Main --------------------------------------------------------------------------
