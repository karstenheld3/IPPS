# LLM Tools - Computer Use

Function of `@skills:llm-tools`. Desktop automation via LLM vision. The AI sees your screen, decides what to click/type, and executes actions.

Files: `cli.py` (entry point), `core.py` (ScreenCapture, Actions, AgentSession, AnthropicProvider). Pricing is read from `../model-pricing.json` (longest prefix match).

## When to Use

Apply when automating desktop interactions that require visual understanding:
- Opening and controlling applications
- Clicking buttons, menus, or UI elements
- Typing text into fields
- Navigating file systems
- Browser automation
- System tasks

## Requirements

- Python 3.10+ with `anthropic`, `mss`, `pillow`, `pyautogui` (see `../SETUP.md`)
- Anthropic API key (`ANTHROPIC_API_KEY` environment variable or `--keys-file`)
- Windows

## CLI Usage

```powershell
$venv = "[SKILL_TOOLS_FOLDER]\llm-venv\Scripts\python.exe"
$cli = "[AGENT_FOLDER]\skills\llm-tools\computer-use\cli.py"

# Dry-run (safe, no actions executed)
& $venv $cli "Click the Start button"

# Execute mode
& $venv $cli -x "Open Notepad and type Hello World"

# With API key file
& $venv $cli -x -k [API_KEYS_FILE] "Open Calculator"
```

## Options

- `-x, --execute` - Execute actions (default: dry-run)
- `-n, --max-iterations` - Max iterations (default: 10, ~$0.01-0.02 each)
- `-m, --model` - Model: claude-sonnet-4-5 (default), claude-haiku-4-5, claude-opus-4-5
- `-k, --keys-file` - API keys file path
- `-s, --save-log` - Save session log as JSON
- `-q, --quiet` - Minimal output

## Programmatic Usage

```python
import sys
sys.path.insert(0, "[AGENT_FOLDER]/skills/llm-tools/computer-use")

from core import AgentSession

session = AgentSession(
    task_prompt="Open Notepad",
    max_iterations=5,
    dry_run=False,
    model="claude-sonnet-4-5"
)

summary = session.run()
print(f"Cost: ${summary['estimated_cost_usd']:.4f}")
```

## Cost Estimate

Rates come from `../model-pricing.json`. Per iteration (one screenshot + response):
- `claude-opus-4-5` - ~$0.02-0.04
- `claude-sonnet-4-5` - ~$0.01-0.02
- `claude-haiku-4-5` - ~$0.004-0.007

Multiply by `--max-iterations` for the session ceiling.

## Safety

- Dry-run by default (no actions executed)
- High-risk action confirmation (Alt+F4, delete, shutdown)
- Iteration limits prevent runaway costs
- pyautogui fail-safe (move mouse to corner to abort)

## Version

0.6.0 (flat layout inside `llm-tools`, pricing from shared JSON)
