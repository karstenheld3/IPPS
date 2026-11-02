#!/usr/bin/env python3
"""
layer-depth-ladder.py - Layer the append-only depth ladder into model-registry.json (MDLRGUP-MDLINVNTRY-SP01 FR-01 to FR-03).

Edges (x dominates y):
  E1        strict    same provider and point version, lower uc_class number
  E2        weak      same provider, tier, and series; immediate predecessor by release_date (specialized models have none)
  E3        strict    Epoch ECI 95% intervals do not overlap: ci_low(x) > ci_high(y)
  E5        tie       no Epoch score; same provider, point version, and tier sibling with a score
  E6        estimate  no score, no E5 sibling, rung D1: D(sibling) - (tier(x) - tier(sibling)) from the nearest-tier sibling of the same point version
  E1m, E4m  strict    manual deeper_than entries {model, kind, source, accessed, statement}
Direct conflict (x > y and y > x): precedence E4 > E1 > E3, the lower edge is dropped and reported. Any other cycle aborts without writing.

Modes:
  default      insert-only: models without depth, and estimated models that gained evidence, get floor capped by their dominators; existing rungs never move
  --bootstrap  one-time fixed-point layering of all models; refused when any depth exists

Usage:
  python layer-depth-ladder.py --registry-file <model-registry.json> [--match-file <[DATE]_Epoch-ECI-Match.json>] [--log-file <path>] [--bootstrap] [--dry-run]
"""
import argparse, importlib.util, json, re, sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
  sys.stdout.reconfigure(encoding="utf-8", errors="replace")
  sys.stderr.reconfigure(encoding="utf-8", errors="replace")

NON_TEXT = {"computer-use-preview", "gpt-image-1.5"}
SPECIALIZED = re.compile(r"(codex|cyber|deep-research|legal|non-reasoning|multi-agent|build|v$)")
MANUAL_KINDS = {"E1", "E4"}
MANUAL_FIELDS = ["model", "kind", "source", "accessed", "statement"]
PRECEDENCE = {"E4m": 3, "E4": 3, "E1m": 2, "E1": 2, "E3": 1}

# ----------------------------------------- START: Logging ---------------------------------------------------------------------

class Logger:
  def __init__(self):
    self.lines = []

  def log(self, line):
    print(line)
    self.lines.append(line)

  def write(self, log_file):
    if log_file:
      Path(log_file).write_text("\n".join(self.lines) + "\n", encoding="utf-8")

def plural(count, word):
  return f"{count} {word}" + ("" if count == 1 else "s")

# ----------------------------------------- END: Logging -----------------------------------------------------------------------


# ----------------------------------------- START: Model attributes ------------------------------------------------------------

def base_id(model_id):
  return re.sub(r"-\d{8}$", "", model_id)

def tier_of(uc_class):
  match = re.match(r"UC-(\d)", uc_class or "")
  return int(match.group(1)) if match else 9

def point_version(provider, model_id):
  retVal = None
  if provider == "anthropic":
    match = re.match(r"claude-(opus|sonnet|haiku|fable|mythos)-(.+)$", model_id)
    if match: retVal = "claude-" + match.group(2)
    elif model_id.startswith("claude-3-5-sonnet"): retVal = "claude-3-5"
  elif provider == "openai":
    match = re.match(r"(gpt-\d+(?:\.\d+)?|o\d)(?:-.*)?$", model_id)
    if match: retVal = match.group(1)
  elif provider == "google":
    match = re.match(r"gemini-(\d+(?:\.\d+)?)-", model_id)
    if match: retVal = "gemini-" + match.group(1)
  elif provider == "zai":
    match = re.match(r"glm-(\d+(?:\.\d+)?)", model_id)
    if match: retVal = "glm-" + match.group(1)
  elif provider == "xai":
    match = re.match(r"grok-(\d+(?:\.\d+)?)", model_id)
    if match: retVal = "grok-" + match.group(1)
  return retVal or model_id

def series_of(provider, model_id):
  retVal = "main"
  if provider == "openai" and re.match(r"o\d", model_id): retVal = "o-series"
  if SPECIALIZED.search(model_id): retVal = "specialized:" + model_id
  return retVal

# Build the layering view of every text model that is not retired; score and interval come from the match file when present, else from the registry
def load_models(registry, match_data):
  match_by_id = {}
  if match_data:
    for entry in match_data.get("matches", []):
      match_by_id[entry["model_id"]] = entry
  retVal = []
  for entry in registry["models"]:
    model_id = entry["model_id"]
    if model_id in NON_TEXT or entry.get("status") == "retired": continue
    short_id = base_id(model_id)
    matched = match_by_id.get(model_id) or match_by_id.get(short_id)
    if matched:
      score, ci_low, ci_high = matched.get("eci_score"), matched.get("eci_ci_low"), matched.get("eci_ci_high")
    else:
      interval = entry.get("eci_ci") or [None, None]
      score, ci_low, ci_high = entry.get("eci_score"), interval[0], interval[1]
    retVal.append({
      "id": short_id, "entry": entry, "provider": entry["provider"], "tier": tier_of(entry.get("uc_class")),
      "release_date": entry.get("release_date") or "9999-12-31", "score": score, "ci_low": ci_low, "ci_high": ci_high,
      "point_version": point_version(entry["provider"], short_id), "series": series_of(entry["provider"], short_id),
      "depth": entry.get("depth"), "estimated": bool(entry.get("depth_estimated")),
    })
  retVal.sort(key=lambda model: (model["release_date"], model["id"]))
  return retVal

# ----------------------------------------- END: Model attributes --------------------------------------------------------------


# ----------------------------------------- START: Edges -----------------------------------------------------------------------

# Validate deeper_than entries; returns (valid edges [(x, y, kind)], rejection messages)
def validate_manual_edges(models):
  ids = set()
  for model in models:
    ids.add(model["id"])
  valid = []
  rejected = []
  for model in models:
    for item in model["entry"].get("deeper_than", []) or []:
      target = base_id(str(item.get("model", "")))
      problem = None
      for field in MANUAL_FIELDS:
        if not item.get(field):
          problem = f"missing '{field}'"
          break
      if problem is None and item["kind"] not in MANUAL_KINDS: problem = f"kind '{item['kind']}' is not E1 or E4"
      if problem is None and not re.match(r"^\d{4}-\d{2}-\d{2}$", str(item["accessed"])): problem = f"accessed '{item['accessed']}' is not YYYY-MM-DD"
      if problem is None and target not in ids: problem = f"model '{target}' is not a layered registry model"
      if problem is None and target == model["id"]: problem = "model references itself"
      if problem: rejected.append(f"REJECTED {model['id']} > {target or '?'}: {problem}")
      else: valid.append((model["id"], target, item["kind"] + "m"))
  return valid, rejected

def build_edges(models, manual_edges):
  strict, weak, ties = {}, {}, {}
  for model in models:
    strict[model["id"]], weak[model["id"]], ties[model["id"]] = [], [], []
  counts = {"E1": 0, "E2": 0, "E3": 0, "E5": 0, "manual": 0}
  for (x_id, y_id, kind) in manual_edges:
    strict[x_id].append((y_id, kind))
    counts["manual"] += 1
  for x in models:
    for y in models:
      if x is y: continue
      if x["provider"] == y["provider"] and x["point_version"] == y["point_version"] and x["tier"] < y["tier"]:
        strict[x["id"]].append((y["id"], "E1"))
        counts["E1"] += 1
      if x["ci_low"] is not None and y["ci_high"] is not None and x["ci_low"] > y["ci_high"]:
        strict[x["id"]].append((y["id"], "E3"))
        counts["E3"] += 1
  for x in models:
    if not x["series"].startswith("specialized"):
      predecessor = None
      for y in models:
        if y["provider"] == x["provider"] and y["tier"] == x["tier"] and y["series"] == x["series"] and y["release_date"] < x["release_date"]: predecessor = y
      if predecessor is not None:
        weak[x["id"]].append((predecessor["id"], "E2"))
        counts["E2"] += 1
    if x["score"] is None:
      for y in models:
        if y is not x and y["provider"] == x["provider"] and y["point_version"] == x["point_version"] and y["tier"] == x["tier"] and y["score"] is not None:
          ties[x["id"]].append((y["id"], "E5"))
          counts["E5"] += 1
  return strict, weak, ties, counts

# Direct conflicts x > y and y > x: drop the lower-precedence edge (E4 > E1 > E3); equal precedence stays and is caught as a cycle
def resolve_direct_conflicts(strict):
  retVal = []
  for x_id in list(strict.keys()):
    for (y_id, kind_xy) in list(strict[x_id]):
      for (z_id, kind_yx) in list(strict.get(y_id, [])):
        if z_id != x_id: continue
        rank_xy, rank_yx = PRECEDENCE.get(kind_xy, 0), PRECEDENCE.get(kind_yx, 0)
        if rank_xy > rank_yx:
          strict[y_id].remove((x_id, kind_yx))
          retVal.append(f"CONTRADICTION {x_id} {kind_xy}> {y_id} vs {y_id} {kind_yx}> {x_id}: dropped {kind_yx} (EC-8)")
  return retVal

# Find a cycle that contains a strict edge; returns a description naming both edges, or None
def find_cycle(models, strict, weak, ties):
  adjacency = {}
  for model in models:
    adjacency[model["id"]] = []
    for edges in (strict, weak, ties):
      for (y_id, kind) in edges[model["id"]]:
        adjacency[model["id"]].append((y_id, kind))
  for model in models:
    x_id = model["id"]
    for (y_id, kind) in strict[x_id]:
      previous = {y_id: None}
      queue = [y_id]
      while queue:
        current = queue.pop(0)
        if current == x_id: break
        for (next_id, next_kind) in adjacency[current]:
          if next_id not in previous:
            previous[next_id] = (current, next_kind)
            queue.append(next_id)
      if x_id in previous:
        closing = previous[x_id]
        return f"CYCLE {x_id} {kind}> {y_id} and {closing[0]} {closing[1]}> {x_id} (path back from {y_id} to {x_id})"
  return None

# ----------------------------------------- END: Edges -------------------------------------------------------------------------


# ----------------------------------------- START: Layering --------------------------------------------------------------------

def floor_of(x_id, rung, strict, weak, ties):
  floor, evidence = 1, "bottom"
  for (y_id, kind) in strict[x_id]:
    if y_id in rung and rung[y_id] + 1 > floor: floor, evidence = rung[y_id] + 1, f"{kind} > {y_id}"
  for (y_id, kind) in weak[x_id]:
    if y_id in rung and rung[y_id] > floor: floor, evidence = rung[y_id], f"{kind} >= {y_id}"
  for (y_id, kind) in ties[x_id]:
    if y_id in rung and rung[y_id] > floor: floor, evidence = rung[y_id], f"{kind} = {y_id}"
  return floor, evidence

def cap_of(x_id, rung, strict, weak, ties):
  cap, evidence = None, ""
  for z_id in rung:
    for (y_id, kind) in strict[z_id]:
      if y_id == x_id and (cap is None or rung[z_id] - 1 < cap): cap, evidence = rung[z_id] - 1, f"{kind} < {z_id}"
    for edges in (weak, ties):
      for (y_id, kind) in edges[z_id]:
        if y_id == x_id and (cap is None or rung[z_id] < cap): cap, evidence = rung[z_id], f"{kind} <= {z_id}"
  return cap, evidence

# E6: nearest-tier sibling of the same point version with an evidence-based rung; (1, "unplaced") without one
def e6_estimate(x, models, rung, estimated):
  best = None
  for y in models:
    if y is x or y["id"] not in rung or y["id"] in estimated: continue
    if y["provider"] != x["provider"] or y["point_version"] != x["point_version"] or y["tier"] == x["tier"]: continue
    key = (abs(y["tier"] - x["tier"]), 0 if y["score"] is not None else 1, y["id"])
    if best is None or key < best[0]: best = (key, y)
  if best is None: return 1, "unplaced"
  sibling = best[1]
  retVal = max(1, rung[sibling["id"]] - (x["tier"] - sibling["tier"]))
  return retVal, f"E6 from {sibling['id']}"

def raise_to_fixed_point(models, rung, strict, weak, ties):
  for _ in range(len(models) + 2):
    changed = False
    for x in models:
      floor, _evidence = floor_of(x["id"], rung, strict, weak, ties)
      if floor > rung[x["id"]]:
        rung[x["id"]] = floor
        changed = True
    if not changed: return True
  return False

def bootstrap_layering(models, strict, weak, ties):
  rung = {}
  for model in models:
    rung[model["id"]] = 1
  converged = raise_to_fixed_point(models, rung, strict, weak, ties)
  estimated = {}
  if converged:
    for x in models:
      if x["score"] is None and not ties[x["id"]] and rung[x["id"]] == 1:
        estimated[x["id"]] = True
    for x in models:
      if x["id"] in estimated: rung[x["id"]], estimated[x["id"]] = e6_estimate(x, models, rung, estimated)
    converged = raise_to_fixed_point(models, rung, strict, weak, ties)
  evidence = {}
  for x in models:
    floor, reason = floor_of(x["id"], rung, strict, weak, ties)
    if x["id"] in estimated:
      floor_target = reason.split(" ")[-1]
      if floor < rung[x["id"]] or reason == "bottom" or floor_target in estimated: reason = estimated[x["id"]]
      else: del estimated[x["id"]]
    evidence[x["id"]] = reason
  return rung, evidence, estimated, converged

# Insert models without depth in dependency order; existing rungs never move
def insert_layering(models, pending_ids, rung, strict, weak, ties):
  placed = []
  pending = []
  for model in models:
    if model["id"] in pending_ids: pending.append(model)
  estimated_ids = {}
  for model in models:
    if model["estimated"] and model["id"] in rung: estimated_ids[model["id"]] = True
  while pending:
    ready = None
    for x in pending:
      blocked = False
      for edges in (strict, weak, ties):
        for (y_id, _kind) in edges[x["id"]]:
          for other in pending:
            if other["id"] == y_id and other is not x: blocked = True
      if not blocked:
        ready = x
        break
    if ready is None: ready = pending[0]
    pending.remove(ready)
    floor, evidence = floor_of(ready["id"], rung, strict, weak, ties)
    is_estimated = False
    if floor == 1 and ready["score"] is None and not ties[ready["id"]]:
      floor, evidence = e6_estimate(ready, models, rung, estimated_ids)
      is_estimated = True
    cap, cap_evidence = cap_of(ready["id"], rung, strict, weak, ties)
    value, squeezed = floor, None
    if cap is not None and floor > cap:
      value, squeezed = max(cap, 1), cap_evidence
      evidence = f"{evidence}; squeezed by {cap_evidence}"
    rung[ready["id"]] = value
    if is_estimated: estimated_ids[ready["id"]] = True
    placed.append({"model": ready, "depth": value, "evidence": evidence, "estimated": is_estimated, "squeezed": squeezed, "floor": floor})
  return placed

# Report existing rungs that no longer satisfy an edge between two placed models (report only, never rewrite)
def check_consistency(models, rung, strict, weak, ties):
  retVal = []
  for x in models:
    x_id = x["id"]
    if x_id not in rung: continue
    for (y_id, kind) in strict[x_id]:
      if y_id in rung and not rung[x_id] > rung[y_id]: retVal.append(f"{x_id} D{rung[x_id]} {kind}> {y_id} D{rung[y_id]}")
    for edges in (weak, ties):
      for (y_id, kind) in edges[x_id]:
        if y_id in rung and not rung[x_id] >= rung[y_id]: retVal.append(f"{x_id} D{rung[x_id]} {kind}>= {y_id} D{rung[y_id]}")
  return retVal

# ----------------------------------------- END: Layering ----------------------------------------------------------------------


# ----------------------------------------- START: Main ------------------------------------------------------------------------

def load_formatter():
  formatter_path = Path(__file__).with_name("format-model-registry.py")
  spec = importlib.util.spec_from_file_location("format_model_registry", formatter_path)
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module

def layer_registry(registry, match_data, bootstrap, logger):
  """
  Layer the registry in place (entries receive depth, depth_evidence, depth_estimated). Returns a result dict.

  Example result: {"ok": True, "inserted": 2, "squeezed": 1, "top": 12, "rung": {"gpt-4o": 1, ...}, "evidence": {...}, "estimated": {...}}
  """
  retVal = {"ok": False, "inserted": 0, "squeezed": 0, "top": 0, "rung": {}, "evidence": {}, "estimated": {}}
  models = load_models(registry, match_data)
  with_depth = 0
  for model in models:
    if model["depth"] is not None: with_depth += 1
  if bootstrap and with_depth > 0:
    logger.log(f"  ERROR: --bootstrap refused: {plural(with_depth, 'model')} already carry depth (MDLRGUP-MDLINVNTRY-IG-02).")
    return retVal
  manual_edges, rejected = validate_manual_edges(models)
  strict, weak, ties, counts = build_edges(models, manual_edges)
  contradictions = resolve_direct_conflicts(strict)
  logger.log(f"  {plural(len(models), 'model')}, {with_depth} with depth.")
  logger.log(f"  Manual edges: {len(manual_edges)} valid, {len(rejected)} rejected.")
  for message in rejected:
    logger.log(f"    {message}")
  logger.log(f"  Edges: E1 {counts['E1']}, E2 {counts['E2']}, E3 {counts['E3']}, E5 {counts['E5']}, manual {counts['manual']}.")
  for message in contradictions:
    logger.log(f"  {message}")
  if rejected:
    logger.log(f"  ERROR: {plural(len(rejected), 'rejected deeper_than item')}; nothing written (MDLRGUP-MDLINVNTRY-IG-03).")
    return retVal
  cycle = find_cycle(models, strict, weak, ties)
  if cycle:
    logger.log(f"  {cycle}")
    logger.log("  ERROR: 1 cycle; nothing written (MDLRGUP-MDLINVNTRY-IG-05).")
    return retVal
  entry_by_id = {}
  for model in models:
    entry_by_id[model["id"]] = model["entry"]
  if bootstrap:
    rung, evidence, estimated, converged = bootstrap_layering(models, strict, weak, ties)
    if not converged:
      logger.log("  ERROR: layering did not converge (cycle); nothing written.")
      return retVal
    for model in sorted(models, key=lambda item: (-rung[item["id"]], item["id"])):
      marker = "*" if model["id"] in estimated else ""
      logger.log(f"  D{rung[model['id']]}{marker:<1} {model['id']:<30} {evidence[model['id']]}")
    for model in models:
      entry = model["entry"]
      entry["depth"], entry["depth_evidence"] = rung[model["id"]], evidence[model["id"]]
      if model["id"] in estimated: entry["depth_estimated"] = True
      else: entry.pop("depth_estimated", None)
    retVal.update({"ok": True, "inserted": len(models), "top": max(rung.values()), "rung": rung, "evidence": evidence, "estimated": estimated})
    retVal["summary"] = f"OK: {plural(len(models), 'model')} layered, top D{retVal['top']}, {len(estimated)} estimated, 0 cycles."
    return retVal
  rung = {}
  pending_ids = {}
  for model in models:
    gained_evidence = model["estimated"] and (model["score"] is not None or ties[model["id"]])
    if model["depth"] is None or gained_evidence: pending_ids[model["id"]] = True
    else: rung[model["id"]] = model["depth"]
  inconsistent = check_consistency(models, rung, strict, weak, ties)
  logger.log(f"  {plural(len(pending_ids), 'model')} to insert.")
  placed = insert_layering(models, pending_ids, rung, strict, weak, ties)
  squeezed = 0
  for index, item in enumerate(placed, start=1):
    model, entry = item["model"], item["model"]["entry"]
    marker = "*" if item["estimated"] else ""
    if item["squeezed"]:
      squeezed += 1
      dominator_id = item["squeezed"].split(" ")[-1]
      logger.log(f"  [ {index} / {len(placed)} ] {model['id']}: D{item['depth']}{marker}, squeezed by {item['squeezed']} (D{rung[dominator_id]}); floor was D{item['floor']}")
    else:
      logger.log(f"  [ {index} / {len(placed)} ] {model['id']}: D{item['depth']}{marker} ({item['evidence']})")
    if model["estimated"] and not item["estimated"]: logger.log(f"    estimate replaced by evidence: was D{model['depth']}*")
    entry["depth"], entry["depth_evidence"] = item["depth"], item["evidence"]
    if item["estimated"]: entry["depth_estimated"] = True
    else: entry.pop("depth_estimated", None)
  inconsistent_ids = {}
  for message in inconsistent:
    inconsistent_ids[message.split(" ")[0]] = True
  existing_count = len(rung) - len(placed)
  logger.log(f"  Existing rungs consistent: {existing_count - len(inconsistent_ids)} / {existing_count}.")
  for message in inconsistent:
    logger.log(f"    INCONSISTENT {message} (report only, rung kept)")
  for model in models:
    retVal["rung"][model["id"]] = rung[model["id"]]
  retVal.update({"ok": True, "inserted": len(placed), "squeezed": squeezed, "top": max(rung.values()) if rung else 0})
  retVal["summary"] = f"OK: {len(placed)} inserted, {squeezed} squeezed, 0 cycles."
  return retVal

def main():
  parser = argparse.ArgumentParser(description="Layer the append-only depth ladder into model-registry.json")
  parser.add_argument("--registry-file", type=Path, required=True, help="Path to model-registry.json")
  parser.add_argument("--match-file", type=Path, default=None, help="Run Epoch match file ([DATE]_Epoch-ECI-Match.json); registry eci_score / eci_ci are used when omitted")
  parser.add_argument("--log-file", type=Path, default=None, help="Write the log to this file as well")
  parser.add_argument("--bootstrap", action="store_true", help="One-time layering of all models; refused when any depth exists")
  parser.add_argument("--dry-run", action="store_true", help="Compute and log, write nothing")
  args = parser.parse_args()
  logger = Logger()
  registry = json.loads(args.registry_file.read_text(encoding="utf-8"))
  match_data = json.loads(args.match_file.read_text(encoding="utf-8")) if args.match_file else None
  match_name = args.match_file.name if args.match_file else "registry eci_ci"
  logger.log(f"Layering depth ladder ({'bootstrap' if args.bootstrap else 'insert-only'}) from {args.registry_file.name} {registry.get('_version')} and {match_name}...")
  result = layer_registry(registry, match_data, args.bootstrap, logger)
  if result["ok"] and not args.dry_run:
    formatter = load_formatter()
    args.registry_file.write_text(formatter.format_registry(registry), encoding="utf-8")
    logger.log(f"  Wrote {args.registry_file}.")
  elif result["ok"]:
    logger.log("  Dry run: nothing written.")
  logger.log(result["summary"] if result["ok"] else "FAIL: depth ladder not layered.")
  logger.write(args.log_file)
  if not result["ok"]: sys.exit(1)

if __name__ == "__main__":
  main()

# ----------------------------------------- END: Main --------------------------------------------------------------------------
