# LLM Computer Use Skill

**Version**: 0.3.0
**Status**: POC (Proof of Concept)

## Overview

Desktop automation via LLM vision. Captures screenshots, sends to Anthropic Computer Use API, executes returned actions (mouse, keyboard).

## Requirements

```
mss>=9.0.1
Pillow>=10.0.0
anthropic>=0.50.0
pyautogui>=0.9.54
```

## Installation

```bash
pip install mss Pillow anthropic pyautogui
```

## Usage

### CLI

```bash
# Dry run (default) - preview actions without executing
python -m llm_computer_use "Open Notepad and type 'Hello World'"

# Execute mode - actually perform actions
python -m llm_computer_use --execute "Open Calculator"

# With API key file
python -m llm_computer_use -k e:\Dev\.api-keys.txt "Task description"

# Custom model and iterations
python -m llm_computer_use -n 10 -m claude-haiku-4-5 "Simple task"
```

### Python API

```python
from llm_computer_use import ScreenCapture, AgentSession

# Screenshot only
sc = ScreenCapture(max_edge=1568, jpeg_quality=85)
result = sc.capture_for_api()
print(f"Size: {result['resized_size']}, Time: {result['capture_ms']}ms")

# Full session
session = AgentSession(
    task_prompt="Open Notepad and type 'Hello World'",
    max_iterations=20,
    dry_run=True,  # Safe mode
)
summary = session.run()
print(f"Status: {summary['status']}, Actions: {summary['actions_count']}")
```

## Features

- **Screenshot capture**: DPI-aware via mss, resizes to 1568px max edge
- **Anthropic integration**: Computer Use API with tool_use handling
- **Action execution**: Mouse (click, drag, scroll) and keyboard (type, hotkeys)
- **Safety controls**: Dry-run mode (default), high-risk action detection
- **Cost estimation**: Per-session cost tracking based on model pricing
- **Latency tracking**: API response time measurement
- **Duration tracking**: Total session time including overhead
- **Session logging**: JSON logs with timestamps, tokens, and costs

## Benchmarks

- Screenshot + resize + base64: **143ms avg** (104-386ms range)
- API latency: **7-10 seconds** typical (Sonnet 4.5)
- Cost per iteration: **~$0.01-0.02** (Sonnet 4.5, ~3400 input tokens)

## Limitations

- Windows only (uses mss and pyautogui)
- Single monitor support (primary)
- Anthropic API required (no offline mode)

## Files

```
llm_computer_use/
├── __init__.py         # Package exports
├── __main__.py         # CLI entry
├── cli.py              # Argument parsing
├── screen_capture.py   # Screenshot + resize
├── actions.py          # Action execution
├── session.py          # Agent loop
└── providers/
    ├── __init__.py
    └── anthropic_provider.py
```
