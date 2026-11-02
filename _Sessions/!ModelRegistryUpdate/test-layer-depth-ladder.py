#!/usr/bin/env python3
"""
test-layer-depth-ladder.py - Regression test for layer-depth-ladder.py (MDLRGUP-MDLINVNTRY-SP01 NFR-01, IG-02, IG-03, IG-05).

TC-01..03 re-layer the 2026-10-28 Epoch snapshot with the two FR-03 manual edges in bootstrap mode and compare against
_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md [LLMCAPCLS-IN01] Section 3 (92 models, 12 rungs). The model set is restricted
to those 92 models so later registry additions do not change the snapshot.

Usage:
  python test-layer-depth-ladder.py [--registry-file <model-registry.json>] [--match-file <2026-10-28_Epoch-ECI-Match.json>]
"""
import argparse, copy, importlib.util, json, sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
  sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SESSION_FOLDER = Path(__file__).resolve().parent
DEFAULT_REGISTRY = SESSION_FOLDER.parents[1] / "PromptSystemV4.5" / "skills" / "llm-tools" / "model-registry.json"
DEFAULT_MATCH = SESSION_FOLDER / "_2026-10-28_PRICES" / "2026-10-28_Epoch-ECI-Match.json"

# LLMCAPCLS-IN01 Section 3 (rung per model; "*" = E6 estimate)
EXPECTED_BY_RUNG = {
  "12": "claude-fable-5-1 claude-fable-5 claude-mythos-5 claude-mythos-5-1",
  "11": "gpt-6-astra claude-opus-5-5 gpt-5.6-cyber",
  "10": "claude-sonnet-5-5 gpt-6.1-sol gpt-6-sol gpt-5.6-sol gpt-5.5-pro gpt-5.5-cyber gemini-4-argon",
  "9": "claude-opus-5 gpt-5.5 gpt-5.4-pro gpt-5.6-terra gpt-6.1-terra",
  "8": "claude-opus-4-8 claude-opus-4-7 claude-opus-4-6 claude-sonnet-5 gpt-5.4 gpt-5.6-luna gpt-6-luna grok-4.6 glm-5.3 gemini-3.8-flash claude-haiku-5-5 gpt-5.2-pro grok-4.7",
  "7": "gpt-5.2 gpt-5.3-codex gemini-3-flash-preview gemini-3.1-pro-preview gemini-3.6-flash claude-sonnet-4-6 grok-4.5 glm-5.3-flash glm-5.3-flashx glm-5.3-flashx-legal gpt-5-pro",
  "6": "gpt-5 gpt-5.1 claude-opus-4-5 glm-5.1 glm-5.2 gpt-5.4-mini grok-4.3 grok-4.20-0309-reasoning grok-4.20-multi-agent-0309 o3-pro o3-deep-research",
  "5": "gemini-2.5-pro o3 gpt-5-mini claude-sonnet-4-5 glm-5 gpt-5.4-nano o1-pro o4-mini-deep-research grok-4.20-0309-non-reasoning*",
  "4": "o1 o4-mini gemini-2.5-flash claude-haiku-4-5 glm-4.7 gemini-3.1-flash-lite gemini-3.5-flash-lite",
  "3": "gpt-4.1 o3-mini glm-4.5 glm-4.5-x glm-4.6",
  "2": "o1-mini claude-3-5-sonnet gpt-4.1-mini gemini-2.5-flash-lite gpt-5-nano glm-4.5-airx glm-4.5v glm-4.7-flash* glm-4.7-flashx* glm-4.6v*",
  "1": "gpt-4o gpt-4o-2024-05-13 gpt-4o-mini gpt-4.1-nano glm-4.5-flash* glm-4-air* grok-build-0.1*",
}

FR03_EDGES = {
  "claude-fable-5-1": {"model": "claude-opus-5-5", "kind": "E1", "source": "https://platform.claude.com/docs/en/models/fable-5-1/overview", "accessed": "2026-11-02", "statement": "test"},
  "claude-fable-5": {"model": "claude-opus-5-5", "kind": "E1", "source": "https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1.md", "accessed": "2026-11-02", "statement": "test"},
}

class SilentLogger:
  def __init__(self):
    self.lines = []

  def log(self, line):
    self.lines.append(line)

def load_layering_module():
  spec = importlib.util.spec_from_file_location("layer_depth_ladder", SESSION_FOLDER / "layer-depth-ladder.py")
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module

def expected_rungs():
  rungs, estimated = {}, {}
  for rung, names in EXPECTED_BY_RUNG.items():
    for name in names.split(" "):
      model_id = name.rstrip("*")
      rungs[model_id] = int(rung)
      if name.endswith("*"): estimated[model_id] = True
  return rungs, estimated

# Registry copy restricted to the snapshot models, without depth fields, with exactly the FR-03 manual edges
def snapshot_registry(registry, module, expected):
  retVal = copy.deepcopy(registry)
  kept = []
  for entry in retVal["models"]:
    if module.base_id(entry["model_id"]) not in expected: continue
    for field in ("depth", "depth_evidence", "depth_estimated", "deeper_than"):
      entry.pop(field, None)
    if entry["model_id"] in FR03_EDGES: entry["deeper_than"] = [dict(FR03_EDGES[entry["model_id"]])]
    kept.append(entry)
  retVal["models"] = kept
  return retVal

def run(module, registry, match_data, bootstrap):
  logger = SilentLogger()
  result = module.layer_registry(registry, match_data, bootstrap, logger)
  return result, logger.lines

def main():
  parser = argparse.ArgumentParser(description="Regression test for layer-depth-ladder.py")
  parser.add_argument("--registry-file", type=Path, default=DEFAULT_REGISTRY)
  parser.add_argument("--match-file", type=Path, default=DEFAULT_MATCH)
  args = parser.parse_args()
  module = load_layering_module()
  registry = json.loads(args.registry_file.read_text(encoding="utf-8"))
  match_data = json.loads(args.match_file.read_text(encoding="utf-8"))
  expected, expected_estimated = expected_rungs()
  results = []
  total = 8
  print("===================================== START: DEPTH LADDER REGRESSION TESTS =====================================")
  print(f"Registry '{args.registry_file.name}' {registry.get('_version')}, snapshot '{args.match_file.name}'.")
  print("")

  print(f"[ 1 / {total} ] TC-01: Bootstrap reproduces LLMCAPCLS-IN01 Section 3 rungs ({len(expected)} models)...")
  layered = snapshot_registry(registry, module, expected)
  result, lines = run(module, layered, match_data, True)
  differences = []
  if not result["ok"]: differences.append("layering failed: " + " | ".join(lines[-3:]))
  else:
    for model_id, rung in sorted(expected.items()):
      actual = result["rung"].get(model_id)
      if actual != rung: differences.append(f"{model_id}: expected D{rung}, actual D{actual} ({result['evidence'].get(model_id)})")
    for model_id in result["rung"]:
      if model_id not in expected: differences.append(f"{model_id}: not in snapshot")
  if differences:
    print(f"  FAIL: {len(differences)} rung differences")
    for line in differences:
      print(f"    {line}")
  else:
    print(f"  OK. {len(expected)} / {len(expected)} rungs equal.")
  results.append(not differences)

  print(f"[ 2 / {total} ] TC-02: E6 estimates match ({len(expected_estimated)} models)...")
  actual_estimated = result.get("estimated", {})
  missing = sorted(set(expected_estimated) - set(actual_estimated))
  extra = sorted(set(actual_estimated) - set(expected_estimated))
  if missing or extra: print(f"  FAIL: missing={missing} extra={extra}")
  else: print(f"  OK. {len(expected_estimated)} estimated: {', '.join(sorted(actual_estimated))}")
  results.append(not missing and not extra)

  print(f"[ 3 / {total} ] TC-03: Top rung is D12...")
  print(f"  [{'equal' if result['top'] == 12 else 'different'}] Top  Expected=12  Actual={result['top']}")
  results.append(result["top"] == 12)

  print(f"[ 4 / {total} ] TC-04: Insert-only run on the layered snapshot inserts nothing and keeps every rung...")
  result_insert, lines = run(module, layered, match_data, False)
  consistent_line = ""
  for line in lines:
    if "Existing rungs consistent" in line: consistent_line = line.strip()
  passed = result_insert["ok"] and result_insert["inserted"] == 0 and result_insert["rung"] == result["rung"] and "INCONSISTENT" not in " ".join(lines)
  print(f"  {'OK.' if passed else 'FAIL:'} inserted={result_insert['inserted']}; {consistent_line}")
  results.append(passed)

  print(f"[ 5 / {total} ] TC-05: Bootstrap refused when depth exists (IG-02)...")
  result_refused, lines = run(module, layered, match_data, True)
  passed = not result_refused["ok"] and "refused" in " ".join(lines)
  print(f"  {'OK. Correctly refused.' if passed else 'FAIL: bootstrap ran on a layered registry'}")
  results.append(passed)

  print(f"[ 6 / {total} ] TC-06: Insertion with squeeze (new model E3 > gpt-4o D1, E3 < o1-mini D2)...")
  squeeze_registry = copy.deepcopy(layered)
  squeeze_registry["models"].append({"provider": "openai", "model_id": "gpt-4.0-codex-test", "name": "Test", "status": "untested", "uc_class": "UC-4 Efficient", "release_date": "2026-11-02", "eci_score": 131.6, "eci_ci": [131.3, 132.0]})
  result_squeeze, lines = run(module, squeeze_registry, match_data, False)
  passed = result_squeeze["ok"] and result_squeeze["squeezed"] == 1 and result_squeeze["rung"].get("gpt-4.0-codex-test") == 1
  inserted_line = ""
  for line in lines:
    if "gpt-4.0-codex-test" in line: inserted_line = line.strip()
  print(f"  {'OK.' if passed else 'FAIL:'} {inserted_line}")
  results.append(passed)

  print(f"[ 7 / {total} ] TC-07: deeper_than item without 'accessed' is rejected (IG-03)...")
  rejected_registry = copy.deepcopy(snapshot_registry(registry, module, expected))
  for entry in rejected_registry["models"]:
    if entry["model_id"] == "claude-fable-5": entry["deeper_than"][0].pop("accessed")
  result_rejected, lines = run(module, rejected_registry, match_data, True)
  rejected_line = ""
  for line in lines:
    if "REJECTED" in line: rejected_line = line.strip()
  passed = not result_rejected["ok"] and "missing 'accessed'" in rejected_line
  print(f"  {'OK. ' + rejected_line if passed else 'FAIL: rejection not reported'}")
  results.append(passed)

  print(f"[ 8 / {total} ] TC-08: Manual edge closing a cycle aborts without writing (IG-05)...")
  cycle_registry = copy.deepcopy(snapshot_registry(registry, module, expected))
  for entry in cycle_registry["models"]:
    if entry["model_id"] == "gpt-4o-mini": entry["deeper_than"] = [{"model": "o1", "kind": "E1", "source": "test", "accessed": "2026-11-02", "statement": "test"}]
  result_cycle, lines = run(module, cycle_registry, match_data, True)
  cycle_line = ""
  for line in lines:
    if "CYCLE" in line: cycle_line = line.strip()
  passed = not result_cycle["ok"] and cycle_line != ""
  print(f"  {'OK. ' + cycle_line if passed else 'FAIL: cycle not detected'}")
  results.append(passed)

  passed_count = 0
  for passed in results:
    if passed: passed_count += 1
  print("")
  print(f"{total} tests executed. OK: {passed_count}, FAIL: {total - passed_count}.")
  print(f"RESULT: {'PASSED' if passed_count == total else 'FAILED'}")
  print("====================================== END: DEPTH LADDER REGRESSION TESTS ======================================")
  if passed_count != total: sys.exit(1)

if __name__ == "__main__":
  main()
