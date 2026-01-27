# SPEC: LLM Computer Use Skill

**Doc ID**: LLMCU-SP01
**Goal**: Specify a skill that enables LLM-driven Windows desktop automation via screenshots, mouse, and keyboard
**Timeline**: Created 2026-01-27, Updated 1 time (2026-01-27)
**Target file**: `DevSystemV3.2/skills/llm-computer-use/`

**Depends on:**
- `_INFO_ANTHROPIC_COMPUTER_USE.md [ANTCU-IN01]` for Anthropic API specifications
- `_INFO_OPENAI_COMPUTER_USE.md [OAICU-IN01]` for OpenAI API specifications
- `DevSystemV3.2/skills/windows-desktop-control/` for screenshot capture

**Does not depend on:**
- Any browser automation frameworks (Playwright, Selenium) - this is desktop-first

## MUST-NOT-FORGET

- Anthropic recommended for Windows desktop (desktop-first architecture)
- OpenAI CUA is browser-optimized, not suitable for desktop automation
- Windows DPI scaling requires Win32 API for correct physical resolution
- Prompt injection is a documented security risk - implement mitigations
- Iteration costs: 50+ iterations for complex desktop tasks
- All coordinates must be in physical pixels, not logical pixels

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Design Decisions](#5-design-decisions)
6. [Implementation Guarantees](#6-implementation-guarantees)
7. [Key Mechanisms](#7-key-mechanisms)
8. [Action Flow](#8-action-flow)
9. [Data Structures](#9-data-structures)
10. [Latency Requirements](#10-latency-requirements)
11. [Speed Modes](#11-speed-modes)
12. [Implementation Details](#12-implementation-details)
13. [Document History](#13-document-history)

## 1. Scenario

**Problem:** We need to automate Windows desktop applications using LLM vision capabilities. The LLM sees screenshots and returns actions (clicks, keystrokes) to execute. No existing framework provides this for arbitrary Windows applications.

**Solution:**
- Create a skill that captures screenshots, sends to Anthropic Computer Use API
- Receive action instructions (click, type, scroll, etc.)
- Execute actions using Win32 API or pyautogui
- Loop until task complete or max iterations reached
- Support dry-run mode for safety verification

**What we don't want:**
- Browser-only automation (OpenAI CUA limitation)
- Direct API calls without abstraction (hard to switch providers)
- Hardcoded coordinates (must work across resolutions)
- Unbounded iteration loops (cost explosion)
- Actions without confirmation for high-risk operations

## 2. Context

This skill integrates with the `windows-desktop-control` skill which already provides:
- `simple-screenshot.ps1`: DPI-aware screenshot capture using Win32 GetDeviceCaps
- Physical resolution detection (DESKTOPHORZRES/DESKTOPVERTRES)
- JPEG output with configurable region capture

The LLM Computer Use skill adds:
- Anthropic API integration for vision-based decision making
- Action execution layer (mouse, keyboard)
- Agent loop orchestration
- Safety controls and logging

## 3. Domain Objects

### ScreenCapture

A **ScreenCapture** represents a screenshot with metadata.

**Key properties:**
- `image_path` - Path to captured screenshot file
- `image_base64` - Base64-encoded image data
- `width_px` - Capture width in physical pixels
- `height_px` - Capture height in physical pixels
- `dpi_scale` - DPI scaling factor (1.0, 1.25, 1.5, 1.75, 2.0)
- `timestamp` - Capture timestamp

### Action

An **Action** represents a single operation returned by the LLM.

**Key properties:**
- `action_type` - One of: screenshot, left_click, right_click, middle_click, double_click, triple_click, scroll, type, key, mouse_move, left_click_drag, left_mouse_down, left_mouse_up, hold_key, wait, zoom
- `coordinate` - [x, y] for position-based actions
- `text` - Text string for type action
- `key` - Key name or combo for key action (e.g., "ctrl+s", "enter", "pagedown")
- `direction` - Scroll direction (up, down, left, right)
- `amount` - Scroll amount in pixels
- `duration_seconds` - Duration for wait and hold_key actions
- `start_coordinate` - Start [x, y] for drag actions
- `end_coordinate` - End [x, y] for drag actions

### AgentSession

An **AgentSession** represents an automation session.

**Key properties:**
- `session_id` - Unique session identifier
- `task_prompt` - User's task description
- `provider` - LLM provider (anthropic, openai)
- `model` - Model identifier (claude-sonnet-4-5, computer-use-preview)
- `max_iterations` - Maximum iterations allowed
- `current_iteration` - Current iteration count
- `status` - pending, running, completed, failed, cancelled
- `actions_log` - List of all executed actions
- `total_input_tokens` - Cumulative input tokens
- `total_output_tokens` - Cumulative output tokens
- `dry_run` - Boolean for preview mode

### ActionResult

An **ActionResult** represents the outcome of executing an action.

**Key properties:**
- `success` - Boolean
- `error_message` - Error description if failed
- `screenshot_after` - ScreenCapture taken after action
- `execution_time_ms` - Time to execute in milliseconds

## 4. Functional Requirements

### Mouse Control

**LLMCU-FR-01: Left Click**
- Execute left mouse click at specified [x, y] coordinates
- Coordinates in physical pixels (not logical)
- Support single click, double click, triple click variants

**LLMCU-FR-02: Right Click**
- Execute right mouse click at specified coordinates
- For context menu operations

**LLMCU-FR-03: Middle Click**
- Execute middle mouse button click
- For scroll-wheel click operations

**LLMCU-FR-04: Mouse Move**
- Move cursor to specified coordinates without clicking
- Support smooth movement option

**LLMCU-FR-05: Scroll**
- Scroll in any direction: up, down, left, right
- Configurable scroll amount in pixels or "clicks"
- Scroll at current cursor position or specified coordinates

**LLMCU-FR-06: Click and Drag**
- Click at start coordinate, drag to end coordinate, release
- Support left_click_drag as atomic operation
- Support left_mouse_down / left_mouse_up for complex drags

### Keyboard Control

**LLMCU-FR-07: Type Text**
- Type arbitrary text string
- Handle Unicode characters
- Configurable typing speed (instant vs human-like delay)

**LLMCU-FR-08: Key Press**
- Press single key or key combination
- Support modifiers: ctrl, alt, shift, win
- Format: "ctrl+s", "alt+f4", "shift+tab"

**LLMCU-FR-09: Special Keys**
- Support all special keys:
  - Navigation: up, down, left, right, home, end, pageup, pagedown
  - Function keys: f1-f12
  - Editing: insert, delete, backspace, tab, enter, escape
  - Numpad: numpad0-9, numpadadd, numpadsubtract, numpadmultiply, numpaddivide, numpadenter
  - System: printscreen, scrolllock, pause, capslock, numlock
  - Media: volumeup, volumedown, volumemute, playpause, stop, nexttrack, previoustrack

**LLMCU-FR-10: Hold Key**
- Hold key for specified duration
- For operations like "hold shift while clicking"

### Clipboard Operations

**LLMCU-FR-11: Copy**
- Execute Ctrl+C or Cmd+C
- Capture clipboard content after operation (optional)

**LLMCU-FR-12: Paste**
- Execute Ctrl+V or Cmd+V
- Support paste from programmatically set clipboard

**LLMCU-FR-13: Cut**
- Execute Ctrl+X or Cmd+X

**LLMCU-FR-14: Select All**
- Execute Ctrl+A or Cmd+A

**LLMCU-FR-15: Clipboard Read/Write**
- Read current clipboard content (text, image)
- Set clipboard content programmatically
- Support text and image clipboard types

### Screenshot Operations

**LLMCU-FR-16: Full Screen Capture**
- Capture entire screen at physical resolution
- Handle DPI scaling correctly
- Output as JPEG or PNG

**LLMCU-FR-17: Region Capture**
- Capture specified rectangular region
- Coordinates in physical pixels

**LLMCU-FR-18: Multi-Monitor Support**
- Identify available monitors
- Capture from specific monitor by index
- Capture across all monitors as single image

**LLMCU-FR-19: Image Optimization**
- Resize to optimal dimensions for LLM (max 1568px long edge)
- Calculate token cost before sending
- Support quality/size tradeoff configuration

### Agent Loop

**LLMCU-FR-20: Session Management**
- Initialize session with task prompt and configuration
- Track iteration count against maximum
- Maintain action log throughout session

**LLMCU-FR-21: API Communication**
- Send screenshot and prompt to LLM provider
- Parse action response
- Handle API errors gracefully
- Support both Anthropic and OpenAI (future)

**LLMCU-FR-22: Action Execution**
- Execute received action on Windows desktop
- Capture screenshot after each action
- Report success/failure back to LLM

**LLMCU-FR-23: Completion Detection**
- Detect when LLM indicates task complete
- Detect when max iterations reached
- Support explicit cancel by user

### Safety Controls

**LLMCU-FR-24: Dry Run Mode**
- Preview all actions without executing
- Log what would happen
- Require explicit confirmation to execute

**LLMCU-FR-25: Action Logging**
- Log all actions with timestamps
- Include screenshots before/after
- Support audit trail export

**LLMCU-FR-26: High-Risk Action Confirmation**
- Define list of high-risk patterns
- Pause and request confirmation for:
  - File deletion (del, rm, remove)
  - System commands (shutdown, reboot)
  - Credential entry
  - Financial actions

**LLMCU-FR-27: Iteration Limits**
- Configurable max iterations (default: 20)
- Warning at 80% of limit
- Hard stop at limit with status report

**LLMCU-FR-28: Cost Tracking**
- Track tokens used per iteration
- Calculate running cost
- Optional cost limit with auto-stop

### Provider Abstraction

**LLMCU-FR-29: Provider Interface**
- Abstract interface for LLM providers
- Implement Anthropic provider
- Structure for future OpenAI provider
- Switch providers via configuration

## 5. Design Decisions

**LLMCU-DD-01:** Use Anthropic as primary provider for Windows desktop. Rationale: Desktop-first architecture, 22% OSWorld accuracy vs OpenAI's browser-optimized approach.

**LLMCU-DD-02:** Physical pixel coordinates everywhere. Rationale: Windows DPI scaling causes logical/physical mismatch. Win32 GetDeviceCaps provides physical resolution.

**LLMCU-DD-03:** JPEG format for screenshots. Rationale: Smaller file size than PNG, sufficient quality for LLM vision, existing simple-screenshot.ps1 uses JPEG.

**LLMCU-DD-04:** Python as primary implementation language. Rationale: Anthropic SDK is Python-native, pyautogui available for input simulation, easy integration with Win32 via ctypes.

**LLMCU-DD-05:** Default max iterations = 20. Rationale: Balance between task completion and cost control. ~$2 per session at 20 iterations with Sonnet 4.5.

**LLMCU-DD-06:** Screenshot after every action. Rationale: LLM needs visual feedback to verify action success and plan next step.

**LLMCU-DD-07:** Dry-run mode enabled by default for new sessions. Rationale: Safety first - preview before executing irreversible actions.

**LLMCU-DD-08:** Keyboard shortcuts over mouse for tricky UI. Rationale: Anthropic best practice - dropdowns, scrollbars more reliable with keyboard.

## 6. Implementation Guarantees

**LLMCU-IG-01:** All coordinates MUST be in physical pixels, not logical pixels.

**LLMCU-IG-02:** DPI scaling factor MUST be detected using Win32 API, not assumed.

**LLMCU-IG-03:** Every action MUST be logged with before/after screenshots.

**LLMCU-IG-04:** Session MUST stop at max_iterations, never exceed.

**LLMCU-IG-05:** High-risk actions MUST pause for confirmation in non-dry-run mode.

**LLMCU-IG-06:** API errors MUST be retried with exponential backoff (max 3 attempts).

**LLMCU-IG-07:** Clipboard operations MUST preserve original clipboard content option.

**LLMCU-IG-08:** Multi-monitor MUST identify primary monitor correctly.

## 7. Key Mechanisms

### Coordinate Translation

Screenshots are captured at physical resolution. When sending to Anthropic API:
1. Capture screenshot using Win32 GetDeviceCaps for physical dimensions
2. Report `display_width_px` and `display_height_px` matching physical size
3. LLM returns coordinates in that same space
4. Execute actions using those exact coordinates (no translation needed)

If image is resized for token optimization:
1. Track resize_factor = new_size / original_size
2. Scale returned coordinates: actual_coord = llm_coord / resize_factor

### Action Mapping

Map Anthropic action types to Windows execution:

```
screenshot      -> simple-screenshot.ps1 or mss
left_click      -> pyautogui.click(x, y, button='left')
right_click     -> pyautogui.click(x, y, button='right')
middle_click    -> pyautogui.click(x, y, button='middle')
double_click    -> pyautogui.doubleClick(x, y)
triple_click    -> pyautogui.tripleClick(x, y)
mouse_move      -> pyautogui.moveTo(x, y)
scroll          -> pyautogui.scroll(amount, x, y)
type            -> pyautogui.write(text) or pyautogui.typewrite(text)
key             -> pyautogui.hotkey(*keys.split('+'))
hold_key        -> pyautogui.keyDown(key); time.sleep(dur); pyautogui.keyUp(key)
wait            -> time.sleep(duration)
left_click_drag -> pyautogui.drag(x2-x1, y2-y1, button='left')
left_mouse_down -> pyautogui.mouseDown(x, y, button='left')
left_mouse_up   -> pyautogui.mouseUp(x, y, button='left')
```

### Agent Loop Pattern

```
session = AgentSession(task_prompt, max_iterations=20)

while session.current_iteration < session.max_iterations:
    session.current_iteration += 1
    
    # Capture current state
    screenshot = capture_screenshot()
    
    # Send to LLM
    response = provider.send(screenshot, session.messages)
    session.total_input_tokens += response.input_tokens
    session.total_output_tokens += response.output_tokens
    
    # Check for completion (no tool use = done)
    actions = parse_actions(response)
    if not actions:
        session.status = "completed"
        break
    
    # Execute actions
    for action in actions:
        if session.dry_run:
            log_dry_run(action)
        else:
            if is_high_risk(action) and not confirm_action(action):
                session.status = "cancelled"
                break
            result = execute_action(action)
            session.actions_log.append((action, result))
    
    # Prepare for next iteration
    session.messages.append(tool_results)

if session.current_iteration >= session.max_iterations:
    session.status = "max_iterations_reached"
```

### High-Risk Pattern Detection

Patterns requiring confirmation:
- Key sequences: "alt+f4", "ctrl+alt+delete"
- Typed text matching: "del ", "rm ", "format", "shutdown", "reboot"
- Clipboard content matching: passwords, API keys (regex patterns)
- Actions targeting system windows: Task Manager, Control Panel, Registry Editor

## 8. Action Flow

```
User invokes session with task prompt
├─> Initialize AgentSession
│   ├─> Load configuration (provider, model, max_iterations)
│   ├─> Create session directory for logs
│   └─> Set dry_run based on config
├─> Enter Agent Loop
│   ├─> capture_screenshot()
│   │   └─> simple-screenshot.ps1 or mss
│   ├─> provider.send(screenshot, messages)
│   │   ├─> Encode image as base64
│   │   ├─> Build API request
│   │   └─> Parse response actions
│   ├─> For each action:
│   │   ├─> Log action (before)
│   │   ├─> If dry_run: log_dry_run()
│   │   ├─> Else: 
│   │   │   ├─> If high_risk: confirm_action()
│   │   │   ├─> execute_action()
│   │   │   └─> capture_screenshot() (after)
│   │   └─> Log result
│   └─> Check completion or max_iterations
└─> Output session summary
    ├─> Actions executed
    ├─> Screenshots captured
    ├─> Tokens used
    └─> Estimated cost
```

## 9. Data Structures

### API Request (Anthropic)

```json
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 1024,
  "tools": [
    {
      "type": "computer_20250124",
      "name": "computer",
      "display_width_px": 1920,
      "display_height_px": 1080,
      "display_number": 1
    }
  ],
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Open Notepad and type 'Hello World'"},
        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": "..."}}
      ]
    }
  ],
  "betas": ["computer-use-2025-01-24"]
}
```

### API Response (Action)

```json
{
  "type": "tool_use",
  "id": "toolu_123",
  "name": "computer",
  "input": {
    "action": "left_click",
    "coordinate": [156, 342]
  }
}
```

### Session Log Entry

```json
{
  "iteration": 3,
  "timestamp": "2026-01-27T19:15:23.456Z",
  "action": {
    "type": "left_click",
    "coordinate": [156, 342]
  },
  "result": {
    "success": true,
    "execution_time_ms": 45
  },
  "screenshot_before": "session_001/iter_003_before.jpg",
  "screenshot_after": "session_001/iter_003_after.jpg",
  "tokens": {"input": 1650, "output": 85}
}
```

## 10. Latency Requirements

### Target Latencies

**Per-Action Cycle Time:**
- Screenshot capture: <100ms
- Image encoding: <50ms
- API round-trip: 2000-4000ms (Anthropic TTFT ~2s)
- Action execution: <100ms
- **Total per iteration: 2500-4500ms**

### Acceptable Latency

For background automation tasks:
- Per iteration: <5 seconds acceptable
- Full task (20 iterations): <2 minutes acceptable

For semi-interactive use:
- Per iteration: <3 seconds preferred
- User should see progress updates during long operations

### Latency Optimization Strategies

1. **Pre-resize screenshots** before API call
2. **Use Haiku 4.5** for speed-critical tasks (~1.5x faster than Sonnet)
3. **Batch simple actions** where possible
4. **Streaming responses** to see progress
5. **Parallel screenshot capture** while processing response

### NOT Suitable For

- Real-time human-AI interaction
- Gaming automation
- High-frequency trading
- Anything requiring <1s response time

## 11. Speed Modes

Speed modes control the tradeoff between execution speed and verification confidence.

### SPEED-MAX

**Use case**: Proven, recorded sequences on known UI states.

**Behavior**:
- Follows pre-recorded action sequences adapted to current screenshot
- Minimal delays between actions
- Screenshot verification ONLY at sequence-defined checkpoints
- No LLM calls during sequence execution (uses pattern matching)
- LLM used only for initial state verification and sequence selection

**Verification points**: Only when sequence explicitly requires (e.g., "wait for dialog")

**Latency**: ~50-100ms per action (no API calls)

**Risk**: High - sequence may fail silently if UI changed unexpectedly

**Requirements**:
- Pre-recorded sequence library
- Screenshot template matching for state verification
- Fallback to SPEED-HIGH on sequence mismatch

### SPEED-HIGH

**Use case**: Fast automation with safety nets at critical transitions.

**Behavior**:
- Executes actions without per-action verification
- Inserts screenshot + LLM verification at crucial transition points:
  - Application switching (Alt+Tab, clicking taskbar)
  - Window open/close events
  - Dialog/popup appearance or dismissal
  - Form submission
  - Page/view navigation
- Batches simple actions between verification points

**Verification points**: ~1 per 5-10 actions (at transitions)

**Latency**: ~500ms avg per action (amortized API calls)

**Risk**: Medium - may miss mid-sequence failures

### SPEED-MEDIUM

**Use case**: Balanced automation for unfamiliar or complex UIs.

**Behavior**:
- Screenshot + LLM verification at all transition points (like SPEED-HIGH)
- Additional verification after:
  - Any click that should change UI state
  - Text input completion (after full string, not per-char)
  - Scroll operations
  - Keyboard shortcuts
- LLM confirms expected state before proceeding

**Verification points**: ~1 per 2-3 actions

**Latency**: ~1-2s avg per action

**Risk**: Low - catches most failures promptly

### SPEED-LOW

**Use case**: Maximum reliability, debugging, learning new sequences.

**Behavior**:
- Screenshot + LLM verification after EVERY atomic action:
  - Each click (left, right, middle, double, triple)
  - Each typed character sequence (word or phrase)
  - Each scroll operation
  - Each keyboard control key (Enter, Tab, Escape, shortcuts)
  - Each mouse move (if relevant to task)
- LLM explicitly confirms action success before next action

**Verification points**: 1 per action (100%)

**Latency**: ~2.5-4.5s per action (full API round-trip each time)

**Risk**: Minimal - maximum visibility into automation state

**Use for**:
- Recording new sequences for SPEED-MAX library
- Debugging failed automations
- Critical tasks where reliability > speed

### Mode Comparison

```
Mode          Verifications   Latency/Action   API Calls    Risk
-----------------------------------------------------------------
SPEED-MAX     Checkpoints     50-100ms         Minimal      High
SPEED-HIGH    Transitions     ~500ms avg       1 per 5-10   Medium
SPEED-MEDIUM  State changes   ~1-2s avg        1 per 2-3    Low
SPEED-LOW     Every action    2.5-4.5s         1 per 1      Minimal
```

### Mode Selection

**LLMCU-FR-30: Speed Mode Configuration**
- Configurable per session via `--speed` parameter
- Default: SPEED-MEDIUM (balanced)
- Override per-task based on confidence level

**LLMCU-FR-31: Automatic Mode Escalation**
- If action fails verification, escalate to next slower mode
- SPEED-MAX -> SPEED-HIGH -> SPEED-MEDIUM -> SPEED-LOW
- Log mode transitions for debugging

**LLMCU-FR-32: Sequence Recording**
- SPEED-LOW sessions can be recorded as SPEED-MAX sequences
- Capture: action, pre-screenshot template, post-screenshot template
- Store in sequence library with task description

**LLMCU-DD-09:** Default to SPEED-MEDIUM. Rationale: Balanced reliability and speed for typical desktop automation.

**LLMCU-DD-10:** Escalate on failure, never de-escalate mid-session. Rationale: Once reliability issues detected, stay cautious.

## 12. Implementation Details

### File Structure

```
DevSystemV3.2/skills/llm-computer-use/
├── SKILL.md                    # Skill documentation
├── llm_computer_use.py         # Main Python module
├── providers/
│   ├── __init__.py
│   ├── base.py                 # Abstract provider interface
│   ├── anthropic_provider.py   # Anthropic implementation
│   └── openai_provider.py      # OpenAI implementation (future)
├── actions/
│   ├── __init__.py
│   ├── mouse.py                # Mouse control functions
│   ├── keyboard.py             # Keyboard control functions
│   └── clipboard.py            # Clipboard operations
├── session.py                  # AgentSession class
├── safety.py                   # High-risk detection, confirmation
├── config.py                   # Configuration management
└── run_session.py              # CLI entry point
```

### Dependencies

```
anthropic>=0.50.0
pyautogui>=0.9.54
mss>=9.0.1
Pillow>=10.0.0
pyperclip>=1.8.2
```

### CLI Interface

```bash
# Run a session with task prompt
python run_session.py "Open Notepad and type 'Hello World'"

# Dry run mode (default)
python run_session.py --dry-run "Delete all files in temp folder"

# Execute mode
python run_session.py --execute "Open Calculator and compute 2+2"

# Custom configuration
python run_session.py --max-iterations 10 --model claude-haiku-4-5 "Simple task"

# With API key file
python run_session.py --keys-file e:\Dev\.api-keys.txt "Task prompt"
```

### Key Functions

```python
def capture_screenshot(region=None, monitor=0) -> ScreenCapture: ...
def execute_action(action: Action) -> ActionResult: ...
def is_high_risk(action: Action) -> bool: ...
def confirm_action(action: Action) -> bool: ...
def run_session(task_prompt: str, config: Config) -> AgentSession: ...
```

## 13. Document History

**[2026-01-27 19:25]**
- Added: Speed Modes section (SPEED-MAX, HIGH, MEDIUM, LOW)
- Added: FRs 30-32 (mode config, auto-escalation, sequence recording)
- Added: DDs 09-10 (default mode, escalation policy)

**[2026-01-27 19:20]**
- Initial specification created
- Defined: Domain objects, Functional requirements (29 FRs)
- Defined: Design decisions (8 DDs), Implementation guarantees (8 IGs)
- Specified: Latency requirements, Key mechanisms, File structure
