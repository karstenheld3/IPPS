"""CLI entry point for LLM Computer Use."""
import argparse
import sys
import os

__version__ = "0.3.0"

def load_api_key(keys_file: str = None) -> str:
    """Load API key from file or environment."""
    if keys_file and os.path.exists(keys_file):
        with open(keys_file, "r") as f:
            for line in f:
                if line.startswith("ANTHROPIC_API_KEY="):
                    return line.split("=", 1)[1].strip()
    return os.environ.get("ANTHROPIC_API_KEY", "")

def main():
    parser = argparse.ArgumentParser(
        description="LLM Computer Use - Desktop automation via LLM vision",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (default) - preview actions without executing
  python -m llm_computer_use "Open Notepad and type 'Hello World'"
  
  # Execute mode - actually perform actions
  python -m llm_computer_use --execute "Open Calculator"
  
  # With custom settings
  python -m llm_computer_use --max-iterations 10 --model claude-haiku-4-5 "Simple task"
        """
    )
    
    parser.add_argument("task", help="Task description for the LLM")
    parser.add_argument("--execute", "-x", action="store_true",
                       help="Execute actions (default is dry-run)")
    parser.add_argument("--max-iterations", "-n", type=int, default=10,
                       help="Maximum iterations (default: 10, each ~$0.01)")
    parser.add_argument("--model", "-m", default="claude-sonnet-4-5",
                       help="Model to use (default: claude-sonnet-4-5)")
    parser.add_argument("--keys-file", "-k",
                       help="Path to API keys file")
    parser.add_argument("--quiet", "-q", action="store_true",
                       help="Minimal output")
    parser.add_argument("--save-log", "-s", action="store_true",
                       help="Save session log to JSON file")
    parser.add_argument("--version", "-V", action="version",
                       version=f"llm-computer-use {__version__}")
    
    args = parser.parse_args()
    
    api_key = load_api_key(args.keys_file)
    if api_key:
        os.environ["ANTHROPIC_API_KEY"] = api_key
    
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not found")
        print("Set via environment variable or --keys-file")
        sys.exit(1)
    
    from .session import AgentSession
    
    session = AgentSession(
        task_prompt=args.task,
        max_iterations=args.max_iterations,
        dry_run=not args.execute,
        model=args.model,
    )
    
    def confirm_action(action):
        """Prompt user for confirmation on high-risk actions."""
        print(f"\n⚠️  HIGH-RISK ACTION DETECTED: {action.action_type.value}")
        if action.text:
            print(f"    Text: {action.text}")
        if action.key:
            print(f"    Key: {action.key}")
        response = input("Allow this action? (y/N): ").strip().lower()
        return response == "y"
    
    if args.execute:
        session.set_confirm_callback(confirm_action)
    
    try:
        summary = session.run(verbose=not args.quiet)
    except KeyboardInterrupt:
        print("\nSession interrupted by user")
        summary = {"status": "cancelled", "error": "User interrupt"}
    
    if args.save_log:
        log_path = session.save_log()
        print(f"\nLog saved: {log_path}")
    
    if not args.quiet:
        print(f"\n{'='*60}")
        print("SESSION SUMMARY")
        print(f"{'='*60}")
        print(f"Status:      {summary.get('status', 'unknown')}")
        print(f"Model:       {summary.get('model', 'unknown')}")
        print(f"Iterations:  {summary.get('iterations', 0)}/{summary.get('max_iterations', 0)}")
        print(f"Actions:     {summary.get('actions_count', 0)}")
        print(f"Tokens:      {summary.get('total_input_tokens', 0)} in / {summary.get('total_output_tokens', 0)} out")
        latency = summary.get('total_api_latency_ms', 0)
        duration = summary.get('total_duration_ms', 0)
        print(f"Duration:    {duration:.0f} ms (API: {latency:.0f} ms)")
        cost = summary.get('estimated_cost_usd', 0)
        print(f"Cost:        ${cost:.6f} USD")
        if summary.get("error"):
            print(f"Error:       {summary['error']}")
        print(f"{'='*60}")
    
    sys.exit(0 if summary.get("status") in ["completed", "pending"] else 1)

if __name__ == "__main__":
    main()
