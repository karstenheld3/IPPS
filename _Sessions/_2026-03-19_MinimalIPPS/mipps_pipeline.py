"""MinimalIPPS Compression Pipeline - Entry point."""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="MinimalIPPS Compression Pipeline")
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

    # Stub: dispatch to command handlers
    print(f"Command '{args.command}' not yet implemented.")
    sys.exit(1)


if __name__ == "__main__":
    main()
