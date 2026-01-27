# LLM Computer Use

Desktop automation via LLM vision. The AI sees your screen, decides what to click/type, and executes actions to complete tasks.

## How It Works

1. You describe a task: "Open Notepad and type Hello World"
2. AI takes a screenshot and analyzes the screen
3. AI decides the next action (click, type, scroll, etc.)
4. Action is executed (or simulated in dry-run mode)
5. Repeat until task is complete or max iterations reached

## Requirements

- Python 3.10+
- Anthropic API key
- Windows

## Quick Start

```bash
pip install -r requirements.txt

# Dry-run (safe, no actions executed)
python -m llm_computer_use -k path/to/api-keys.txt "Click the Start button"

# Execute mode (actions are performed)
python -m llm_computer_use -x -k path/to/api-keys.txt "Open Notepad"
```

## Example Use Cases

**Application Control**
```bash
# Open and control applications
python -m llm_computer_use -x "Open Notepad and type Hello World"
python -m llm_computer_use -x "Open Calculator and compute 15 * 7"
python -m llm_computer_use -x "Open Settings and enable Dark Mode"
```

**File Management**
```bash
# Navigate and manage files
python -m llm_computer_use -x "Open File Explorer and navigate to Documents"
python -m llm_computer_use -x "Create a new folder called Projects on Desktop"
```

**Browser Automation**
```bash
# Web tasks (requires browser already open)
python -m llm_computer_use -x "Open Chrome and go to github.com"
python -m llm_computer_use -x "Search for Python tutorials on Google"
```

**System Tasks**
```bash
# System settings and info
python -m llm_computer_use -x "Open Task Manager"
python -m llm_computer_use -x "Check WiFi connection status"
```

**Testing and Exploration**
```bash
# Dry-run to see what AI would do (no execution)
python -m llm_computer_use "What applications are open right now?"
python -m llm_computer_use "Describe the current screen"
```

## CLI Options

```
python -m llm_computer_use [OPTIONS] TASK

Options:
  -x, --execute          Execute actions (default: dry-run)
  -n, --max-iterations   Max iterations (default: 10)
  -m, --model            Model: claude-sonnet-4-5 (default), claude-haiku-4-5 (cheaper)
  -k, --keys-file        API keys file path
  -s, --save-log         Save session log as JSON
  -q, --quiet            Minimal output
  -V, --version          Show version
```

## Example Output

```
============================================================
Session 20260127_203631 started
Task: Click the Start button...
Max iterations: 2
Dry run: False
============================================================

--- Iteration 1/2 ---
Model: I'll take a screenshot first to see the current state of the screen...
Action: screenshot

--- Iteration 2/2 ---
Model: I can see the Windows Start button in the bottom-left corner. I'll click on it now...
Action: left_click at (21, 862)
  -> OK

============================================================
SESSION SUMMARY
============================================================
Status:      max_iterations_reached
Model:       claude-sonnet-4-5
Iterations:  2/2
Actions:     1
Tokens:      8432 in / 176 out
Duration:    7473 ms
Cost:        $0.028 USD
============================================================
```

## Cost Estimate

| Model | Cost per Iteration | 10 Iterations |
|-------|-------------------|---------------|
| claude-opus-4 | ~$0.05-0.10 | ~$0.50-1.00 |
| claude-sonnet-4-5 | ~$0.01-0.02 | ~$0.10-0.20 |
| claude-haiku-4-5 | ~$0.003-0.005 | ~$0.03-0.05 |

**Cost drivers:**
- Each screenshot = ~3400 input tokens
- Complex tasks need more iterations
- Haiku is cheaper but less accurate

## Safety

- **Dry-run by default**: Actions are simulated, not executed
- **High-risk detection**: Prompts for confirmation before destructive actions (Alt+F4, delete, shutdown)
- **Iteration limits**: Prevents runaway costs
- **Fail-safe**: pyautogui fail-safe enabled (move mouse to corner to abort)

## Files

```
llm_computer_use/
├── __init__.py   # Package exports (ScreenCapture, AgentSession, execute_action)
├── core.py       # All logic: capture, actions, API, session management
└── cli.py        # CLI entry point and argument parsing
```

## Programmatic Usage

```python
from llm_computer_use import AgentSession

session = AgentSession(
    task_prompt="Open Notepad",
    max_iterations=5,
    dry_run=False,
    model="claude-sonnet-4-5"
)

summary = session.run()
print(f"Cost: ${summary['estimated_cost_usd']:.4f}")
```

## Version

0.5.0 - Minimal 3-file package with full action support
