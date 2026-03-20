"""MinifyIPPS Compression Pipeline - Entry point (IS-16)."""
import argparse
import json
import logging
import sys
from pathlib import Path

from lib.pipeline_state import init_state, load_state, save_state, update_step
from lib.run_manager import create_run, snapshot_config

log = logging.getLogger("mipps")

BASE_DIR = Path(__file__).parent


def _load_config(config_path: Path = None) -> dict:
    """Load pipeline_config.json. EC-04: create default if missing."""
    if config_path is None:
        config_path = BASE_DIR / "pipeline_config.json"
    if not config_path.exists():
        log.warning("Config not found at '%s', creating default", config_path)
        default = {
            "source_dir": ".windsurf/",
            "models": {
                "mother": "claude-opus-4-6-20260204",
                "verifier": "gpt-5-mini",
            },
            "reasoning_effort": "high",
            "output_length": "high",
            "thresholds": {"judge_min_score": 3.5, "max_refinement_attempts": 1,
                           "exclusion_max_lines": 100, "exclusion_max_references": 2,
                           "target_reduction_percent": 60, "max_manual_review_files": 5},
            "cache": {"ttl": "1h"},
            "budget": {"max_total_usd": 100.0, "warning_threshold": 0.8},
            "file_type_map": {"*": "compress_other"},
            "include_patterns": ["*.md"],
            "skip_patterns": [],
            "never_compress": [],
            "api_timeout_seconds": 120,
        }
        config_path.write_text(json.dumps(default, indent=2), encoding="utf-8")
        return default
    return json.loads(config_path.read_text(encoding="utf-8"))


def _state_path() -> Path:
    return BASE_DIR / "pipeline_state.json"


def _require_step(state: dict, min_step: int, step_name: str):
    """EC-05: Check prerequisite step completed."""
    if state["current_step"] < min_step:
        print(f"Error: Run '{step_name}' first (current step: {state['current_step']}, need: {min_step}).")
        sys.exit(1)


def cmd_bundle(args):
    """Step 1: Scan source directory and generate bundle."""
    from lib.file_bundle_builder import scan_source_dir, generate_bundle

    config = _load_config()
    state = load_state(_state_path())

    source_dir = Path(args.source_dir) if args.source_dir else Path(config["source_dir"])
    if not source_dir.is_absolute():
        source_dir = BASE_DIR / source_dir

    categories = scan_source_dir(
        source_dir,
        include_patterns=config.get("include_patterns", ["*.md"]),
        skip_patterns=config.get("skip_patterns", []),
    )
    context_dir = BASE_DIR / "context"
    result = generate_bundle(categories, source_dir, context_dir / "all_files_bundle.md")

    all_files = [f for files in categories.values() for f in files]
    state["files_total"] = result["file_count"]
    update_step(state, 1)
    save_state(_state_path(), state)

    print(f"Bundle created: {result['file_count']} files, ~{result['token_count']} tokens")
    print(f"Written to: {context_dir / 'all_files_bundle.md'}")


def cmd_analyze(args):
    """Steps 2-4: Mother analysis (call tree, complexity, strategy)."""
    from lib.llm_client import LLMClient
    from lib.mother_analyzer import (
        analyze_call_tree, analyze_complexity, generate_strategy,
        identify_excluded_files, parse_load_frequencies,
    )

    config = _load_config()
    state = load_state(_state_path())
    _require_step(state, 1, "bundle")

    bundle_path = BASE_DIR / "context" / "all_files_bundle.md"
    if not bundle_path.exists():
        print("Error: Bundle not found. Run 'bundle' first.")
        sys.exit(1)
    bundle = bundle_path.read_text(encoding="utf-8")

    mother_model = config["models"]["mother"]
    effort = config.get("reasoning_effort", "high")
    client = LLMClient(mother_model, reasoning_effort=effort,
                       timeout=config.get("api_timeout_seconds", 120))
    prompts_dir = BASE_DIR / "prompts" / "step"

    # Step 2: Call tree
    print("Step 2: Analyzing call tree...")
    s2_prompt = (prompts_dir / "s2_call_tree.md").read_text(encoding="utf-8")
    call_tree = analyze_call_tree(client, bundle, s2_prompt, BASE_DIR)
    freqs = parse_load_frequencies(call_tree)
    update_step(state, 2)
    save_state(_state_path(), state)

    # Step 3: Complexity map
    print("Step 3: Analyzing complexity...")
    s3_prompt = (prompts_dir / "s3_complexity_map.md").read_text(encoding="utf-8")
    complexity = analyze_complexity(client, bundle, s3_prompt, BASE_DIR)
    update_step(state, 3)
    save_state(_state_path(), state)

    # Identify never_compress files
    from lib.mother_analyzer import get_never_compress_files
    from lib.file_bundle_builder import scan_source_dir as _scan
    source_dir = Path(config["source_dir"])
    if not source_dir.is_absolute():
        source_dir = BASE_DIR / source_dir
    categories = _scan(source_dir, config.get("include_patterns", ["*.md"]), config.get("skip_patterns", []))
    all_rel = [f.relative_to(source_dir).as_posix() for files in categories.values() for f in files]
    never_compress_files = get_never_compress_files(all_rel, config.get("never_compress", []))
    state["_never_compress_files"] = never_compress_files

    # Identify excluded files (never_compress files removed from exclusion candidates)
    excluded = identify_excluded_files(complexity, freqs, config)
    excluded = [f for f in excluded if f not in never_compress_files]
    state["files_excluded"] = len(excluded) + len(never_compress_files)
    state["_excluded_files"] = excluded

    # Step 4: Strategy
    print("Step 4: Generating compression strategy...")
    s4_prompt = (prompts_dir / "s4_compression_strategy.md").read_text(encoding="utf-8")
    generate_strategy(client, bundle, s4_prompt, excluded, BASE_DIR)
    update_step(state, 4)
    save_state(_state_path(), state)

    print(f"Analysis complete. {len(excluded)} files excluded from compression.")


def cmd_check(args):
    """Verify Mother output using spot-check."""
    from lib.llm_client import LLMClient
    from lib.mother_output_checker import spot_check_document, report_issues
    from lib.file_bundle_builder import scan_source_dir

    config = _load_config()
    state = load_state(_state_path())
    _require_step(state, 4, "analyze")

    verifier = LLMClient(config["models"]["verifier"],
                          timeout=config.get("api_timeout_seconds", 120))
    source_dir = Path(config["source_dir"])
    if not source_dir.is_absolute():
        source_dir = BASE_DIR / source_dir

    # Load source files for comparison
    categories = scan_source_dir(source_dir, config.get("include_patterns", ["*.md"]))
    source_files = []
    for files in categories.values():
        for f in files:
            rel = f.relative_to(source_dir).as_posix()
            source_files.append((rel, f.read_text(encoding="utf-8")))

    # Check each Mother output document
    for doc_name in ["_01_FILE_CALL_TREE.md", "_02_FILE_COMPLEXITY_MAP.md", "_03_FILE_COMPRESSION_STRATEGY.md"]:
        doc_path = BASE_DIR / doc_name
        if doc_path.exists():
            print(f"Checking {doc_name}...")
            doc = doc_path.read_text(encoding="utf-8")
            result = spot_check_document(verifier, doc, source_files)
            if result["issues"]:
                print(report_issues(result["issues"]))
            else:
                print(f"  {doc_name}: OK ({result['checked_count']} files checked)")

    print("Spot-check complete.")


def cmd_generate(args):
    """Step 5: Generate compression and evaluation prompts."""
    from lib.llm_client import LLMClient
    from lib.compression_prompt_builder import generate_compression_prompts, save_prompts

    config = _load_config()
    state = load_state(_state_path())
    _require_step(state, 4, "analyze")

    bundle_path = BASE_DIR / "context" / "all_files_bundle.md"
    bundle = bundle_path.read_text(encoding="utf-8")

    strategy_path = BASE_DIR / "_03_FILE_COMPRESSION_STRATEGY.md"
    strategy = strategy_path.read_text(encoding="utf-8")

    mother_model = config["models"]["mother"]
    effort = config.get("reasoning_effort", "high")
    client = LLMClient(mother_model, reasoning_effort=effort,
                       timeout=config.get("api_timeout_seconds", 120))
    file_types = list(set(config.get("file_type_map", {}).values()))
    s5_prompt = (BASE_DIR / "prompts" / "step" / "s5_generate_prompts.md").read_text(encoding="utf-8")

    print("Generating compression prompts...")
    prompts = generate_compression_prompts(client, bundle, strategy, file_types, s5_prompt)
    save_prompts(
        prompts,
        BASE_DIR / "prompts" / "transform",
        BASE_DIR / "prompts" / "eval",
    )
    update_step(state, 5)
    save_state(_state_path(), state)

    print(f"Generated {len(prompts)} prompt pairs.")


def cmd_compress(args):
    """Step 6: Compress files using generated prompts."""
    from lib.llm_client import LLMClient
    from lib.file_compressor import run_compression_step

    config = _load_config()
    state = load_state(_state_path())
    _require_step(state, 5, "generate")

    bundle_path = BASE_DIR / "context" / "all_files_bundle.md"
    if not bundle_path.exists():
        print("Error: Run 'bundle' first.")
        sys.exit(1)
    bundle = bundle_path.read_text(encoding="utf-8")

    # Load prompts
    prompts = {}
    transform_dir = BASE_DIR / "prompts" / "transform"
    eval_dir = BASE_DIR / "prompts" / "eval"
    if transform_dir.exists():
        for f in transform_dir.glob("*.md"):
            name = f.stem
            eval_path = eval_dir / f.name
            prompts[name] = {
                "transform": f.read_text(encoding="utf-8"),
                "eval": eval_path.read_text(encoding="utf-8") if eval_path.exists() else "",
            }

    source_dir = Path(config["source_dir"])
    if not source_dir.is_absolute():
        source_dir = BASE_DIR / source_dir

    # Create isolated run folder
    run_dir, run_id = create_run(BASE_DIR, label="compress")
    output_dir = run_dir / "output"
    output_dir.mkdir(exist_ok=True)
    snapshot_config(config, run_dir, run_id)

    mother_model = config["models"]["mother"]
    effort = config.get("reasoning_effort", "high")
    client = LLMClient(mother_model, reasoning_effort=effort,
                       timeout=config.get("api_timeout_seconds", 120))
    verifier = LLMClient(config["models"]["verifier"],
                         timeout=config.get("api_timeout_seconds", 120))

    state["run_id"] = run_id
    state["run_dir"] = str(run_dir)

    print(f"Starting compression (run: {run_id})...")
    state = run_compression_step(
        client, verifier, bundle, source_dir, output_dir, config, state, prompts,
    )
    update_step(state, 6)
    save_state(_state_path(), state)

    print(f"Compression complete. {state['files_passed']} passed, {state['files_failed']} failed.")


def cmd_verify(args):
    """Step 7: Generate verification report."""
    from lib.llm_client import LLMClient
    from lib.compression_report_builder import verify_file, check_cross_references, generate_report

    config = _load_config()
    state = load_state(_state_path())
    _require_step(state, 6, "compress")

    source_dir = Path(config["source_dir"])
    if not source_dir.is_absolute():
        source_dir = BASE_DIR / source_dir

    # Use run_dir from state if available, else fallback
    run_dir = Path(state["run_dir"]) if state.get("run_dir") else BASE_DIR / "runs" / "latest"
    output_dir = run_dir / "output"

    s7_prompt = (BASE_DIR / "prompts" / "step" / "s7_verify_file.md").read_text(encoding="utf-8")
    verifier = LLMClient(config["models"]["verifier"],
                         timeout=config.get("api_timeout_seconds", 120))

    # Collect compressed files
    compressed_files = {}
    results = []
    for md_file in sorted(output_dir.rglob("*.md")):
        rel = md_file.relative_to(output_dir).as_posix()
        compressed = md_file.read_text(encoding="utf-8")
        compressed_files[rel] = compressed

        original_path = source_dir / rel
        if original_path.exists():
            original = original_path.read_text(encoding="utf-8")
            print(f"Verifying: {rel}")
            result = verify_file(verifier, original, compressed, s7_prompt, rel)
            results.append(result)

    # Cross-reference check
    excluded = state.get("_excluded_files", [])
    cross_issues = check_cross_references(compressed_files, excluded)
    state["broken_references"] = len(cross_issues)

    # Generate report
    report = generate_report(results, cross_issues, run_dir / "verification" / "_04_FILE_COMPRESSION_REPORT.md")
    update_step(state, 7)
    save_state(_state_path(), state)

    # Generate run summary (TK-014)
    from lib.run_manager import generate_run_summary
    from lib.cost_tracker import load_costs
    costs = load_costs(run_dir)
    summary_path = generate_run_summary(run_dir, state, costs)
    print(f"Report generated: {len(results)} files verified, {len(cross_issues)} broken references.")
    print(f"Run summary: {summary_path}")


def cmd_iterate(args):
    """Review report and re-compress flagged files."""
    from lib.llm_client import LLMClient
    from lib.compression_refiner import review_report, update_strategy, get_files_to_recompress

    config = _load_config()
    state = load_state(_state_path())

    run_dir = Path(state["run_dir"]) if state.get("run_dir") else BASE_DIR / "runs" / "latest"
    report_path = run_dir / "verification" / "_04_FILE_COMPRESSION_REPORT.md"
    if not report_path.exists():
        # EC-07: Run verify first
        print("No report found. Running 'verify' first...")
        cmd_verify(args)

    report = report_path.read_text(encoding="utf-8")
    bundle_path = BASE_DIR / "context" / "all_files_bundle.md"
    bundle = bundle_path.read_text(encoding="utf-8")

    mother_model = config["models"]["mother"]
    effort = config.get("reasoning_effort", "high")
    client = LLMClient(mother_model, reasoning_effort=effort,
                       timeout=config.get("api_timeout_seconds", 120))

    print("Reviewing report...")
    review = review_report(client, bundle, report)

    strategy_path = BASE_DIR / "_03_FILE_COMPRESSION_STRATEGY.md"
    if review["updates"]:
        print(f"Updating strategy with {len(review['updates'])} changes...")
        update_strategy(strategy_path, review["updates"])

    files = review["files_to_recompress"]
    if files:
        print(f"Files to recompress: {len(files)}")
        for f in files:
            print(f"  - {f}")
        # Remove from files_completed to trigger recompression
        state["files_completed"] = [
            f for f in state.get("files_completed", []) if f not in files
        ]
        state["iteration"] = state.get("iteration", 1) + 1
        save_state(_state_path(), state)
        print("Run 'compress' then 'verify' to recompress flagged files.")
    else:
        print("No files need recompression.")


def cmd_status(args):
    """Show current pipeline state."""
    state = load_state(_state_path())
    step_names = {
        0: "Not started", 1: "Bundle created", 2: "Call tree done",
        3: "Complexity map done", 4: "Strategy done", 5: "Prompts generated",
        6: "Compression done", 7: "Verification done",
    }
    step = state.get("current_step", 0)
    if state.get("run_id"):
        print(f"Run: {state['run_id']}")
    print(f"Step: {step} - {step_names.get(step, 'Unknown')}")
    print(f"Iteration: {state.get('iteration', 1)}")
    print(f"Files: {state.get('files_compressed', 0)}/{state.get('files_total', 0)} compressed")
    print(f"  Passed: {state.get('files_passed', 0)}")
    print(f"  Failed: {state.get('files_failed', 0)}")
    print(f"  Excluded: {state.get('files_excluded', 0)}")
    cost = state.get("cost", {})
    print(f"Cost: ${cost.get('total', 0):.4f}")
    print(f"  Mother: ${cost.get('mother_input', 0) + cost.get('mother_output', 0):.4f}")
    print(f"  Verification: ${cost.get('verification_input', 0) + cost.get('verification_output', 0):.4f}")
    print(f"  Cache read: ${cost.get('cache_read', 0):.4f}")
    print(f"  Cache write: ${cost.get('cache_write', 0):.4f}")
    if state.get("broken_references", 0) > 0:
        print(f"Broken references: {state['broken_references']}")


COMMANDS = {
    "bundle": cmd_bundle,
    "analyze": cmd_analyze,
    "check": cmd_check,
    "generate": cmd_generate,
    "compress": cmd_compress,
    "verify": cmd_verify,
    "iterate": cmd_iterate,
    "status": cmd_status,
}


def main():
    logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")

    parser = argparse.ArgumentParser(description="MinifyIPPS Compression Pipeline")
    subparsers = parser.add_subparsers(dest="command")

    sub_bundle = subparsers.add_parser("bundle", help="Step 1: Scan and bundle source files")
    sub_bundle.add_argument("--source-dir", help="Override source directory")

    subparsers.add_parser("analyze", help="Steps 2-4: Mother analysis")
    subparsers.add_parser("check", help="Verify Mother output")
    subparsers.add_parser("generate", help="Step 5: Generate compression prompts")
    subparsers.add_parser("compress", help="Step 6: Compress files")
    subparsers.add_parser("verify", help="Step 7: Generate verification report")
    subparsers.add_parser("iterate", help="Review report and re-compress flagged files")
    subparsers.add_parser("status", help="Show pipeline state")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    handler = COMMANDS.get(args.command)
    if handler:
        handler(args)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
