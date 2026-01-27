# LLM Computer Use v2

Desktop automation via LLM vision. Minimal 3-file package.

## Requirements

- Python 3.10+
- Anthropic API key
- Windows

## Quick Start

```bash
pip install -r requirements.txt

# Dry-run (safe)
python -m llm_computer_use_v2 -k path/to/api-keys.txt "Click the Start button"

# Execute mode
python -m llm_computer_use_v2 -x -k path/to/api-keys.txt "Open Notepad"
```

## CLI Options

```
python -m llm_computer_use_v2 [OPTIONS] TASK

Options:
  -x, --execute          Execute actions (default: dry-run)
  -n, --max-iterations   Max iterations (default: 10, ~$0.01 each)
  -m, --model            Model (default: claude-sonnet-4-5)
  -k, --keys-file        API keys file
  -s, --save-log         Save session JSON
  -q, --quiet            Minimal output
  -V, --version          Show version
```

## Cost

- Screenshot capture: 100-400 ms
- API response: 3-10 seconds
- Cost per iteration: ~$0.01

## Files

```
llm_computer_use_v2/
├── __init__.py   # Package exports
├── core.py       # ScreenCapture, Actions, Session, Provider
└── cli.py        # CLI entry point
```

## Version

0.4.0 - Minimal package (3 files, all tests pass)
