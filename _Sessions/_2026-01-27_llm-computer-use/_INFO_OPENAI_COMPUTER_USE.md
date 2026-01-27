# INFO: OpenAI Computer Use

**Doc ID**: OAICU-IN01
**Goal**: Comprehensive research on OpenAI Computer-Using Agent (CUA) for windows-desktop-control skill development
**Timeline**: Created 2026-01-27, Updated 2 times (2026-01-27)

## Summary

- OpenAI CUA uses `computer-use-preview` model combining GPT-4o vision with advanced reasoning [VERIFIED]
- **API**: Responses API only (not Chat Completions), requires `truncation: "auto"` [VERIFIED]
- **Environments**: browser, mac, windows, ubuntu - browser-optimized, others less reliable [VERIFIED]
- **Benchmark**: 38.1% OSWorld (vs Anthropic 22%), 87% WebVoyager - browser-focused strength [VERIFIED]
- **Actions**: click, scroll, keypress, type, wait, screenshot, drag [VERIFIED]
- **Image cost**: Low detail = 85 tokens fixed; High detail = 170 tokens/tile + 85 base [VERIFIED]
- **Safety checks**: Built-in malicious instruction, irrelevant domain, sensitive domain detection [VERIFIED]
- **Key limitation**: OSWorld 38.1% still far below human 72.4%; non-browser environments unreliable [VERIFIED]
- **Operator product**: $200/month ChatGPT Pro subscription, US-only, managed browser environment [VERIFIED]
- **API access**: Standard pay-per-use via Responses API [VERIFIED]

## Table of Contents

1. [Overview](#1-overview)
2. [Model and Architecture](#2-model-and-architecture)
3. [API Specifications](#3-api-specifications)
4. [Available Actions](#4-available-actions)
5. [Screenshot and Image Handling](#5-screenshot-and-image-handling)
6. [Pricing](#6-pricing)
7. [Safety Checks](#7-safety-checks)
8. [Benchmarks and Performance](#8-benchmarks-and-performance)
9. [Best Practices](#9-best-practices)
10. [Limitations](#10-limitations)
11. [Comparison with Anthropic](#11-comparison-with-anthropic)
12. [Implementation Architecture](#12-implementation-architecture)
13. [Sources](#13-sources)
14. [Next Steps](#14-next-steps)
15. [Document History](#15-document-history)

## 1. Overview

OpenAI's Computer-Using Agent (CUA) is a specialized model (`computer-use-preview`) that combines GPT-4o's vision capabilities with advanced reasoning to control computer interfaces and perform tasks.

**Key Characteristics:**

- **Browser-first design**: Optimized for web-based tasks (booking flights, filling forms, ordering products)
- **Virtual environment**: Operates in cloud-based virtual browser on OpenAI servers (via Virtual Machine)
- **Agent loop pattern**: Sends actions, receives screenshots, iterates until task complete
- **Beta status**: Still prone to mistakes, especially in non-browser environments
- **Windows DPI scaling warning**: Be aware that Windows DPI scaling may affect the accuracy of actions, as the model may not account for scaling factors. Consider using a fixed DPI setting or adjusting the model's coordinates accordingly.

**How It Works:**

1. Send request with `computer_use_preview` tool and user prompt
2. Model returns `computer_call` with action (click, type, scroll, etc.)
3. Your application executes action in browser/VM environment
4. Capture screenshot and send back as `computer_call_output`
5. Loop continues until task complete or model returns text response

**Iteration Cost Notes:**

- Each iteration of the agent loop incurs a cost, which includes the cost of the action, the cost of processing the screenshot, and the cost of the model's reasoning.
- The cost of each iteration can vary depending on the complexity of the action, the size of the screenshot, and the model's reasoning requirements.
- Consider optimizing your application to minimize the number of iterations required to complete a task, as this can help reduce costs.

## 2. Model and Architecture

### Model Identifier

- **Model name**: `computer-use-preview`
- **Snapshot**: `computer-use-preview-2025-03-11`
- **Base model**: Built on GPT-4o vision capabilities

### Supported Environments

The `environment` parameter tells the model what type of interface it's controlling:

- **`browser`** - Web browser automation (recommended, best performance)
- **`mac`** - macOS desktop
- **`windows`** - Windows desktop
- **`ubuntu`** - Ubuntu Linux desktop

**Important**: The model is browser-optimized. Non-browser environments have lower reliability.

### API Requirements

- **Available via**: Responses API only (NOT Chat Completions)
- **Required parameter**: `truncation: "auto"` (must be set to use computer use tool)
- **Beta status**: Model may be susceptible to exploits and mistakes

## 3. API Specifications

### Endpoint

```
POST https://api.openai.com/v1/responses
```

### Basic Request Structure

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="computer-use-preview",
    tools=[{
        "type": "computer_use_preview",
        "display_width": 1024,
        "display_height": 768,
        "environment": "browser"  # or "mac", "windows", "ubuntu"
    }],
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "Check the latest OpenAI news on bing.com."
                }
                # Optional: include initial screenshot
                # {
                #     "type": "input_image",
                #     "image_url": f"data:image/png;base64,{screenshot_base64}"
                # }
            ]
        }
    ],
    reasoning={
        "summary": "concise",  # or "detailed"
    },
    truncation="auto"  # REQUIRED for computer use
)
```

### Tool Parameters

- **type**: Must be `"computer_use_preview"`
- **display_width**: Screen width in pixels
- **display_height**: Screen height in pixels
- **environment**: Target environment type

### Response Structure

The model returns an `output` array containing:

- **`reasoning`** - Model's thinking process (if summary enabled)
- **`computer_call`** - Action to execute with coordinates/parameters
- **`pending_safety_checks`** - Safety warnings if triggered

### Continuing the Loop

Use `previous_response_id` to continue conversation:

```python
response = client.responses.create(
    model="computer-use-preview",
    previous_response_id="<previous_response_id>",
    tools=[...],
    input=[
        {
            "type": "computer_call_output",
            "call_id": "<call_id>",
            "output": {
                "type": "computer_screenshot",
                "image_url": "data:image/png;base64,..."
            },
            "current_url": "https://example.com"  # Optional, improves safety checks
        }
    ],
    truncation="auto"
)
```

## 4. Available Actions

### Core Actions

- **`click`** - Click at coordinates
  - Parameters: `x`, `y`, `button` (left/right)
- **`scroll`** - Scroll at position
  - Parameters: `x`, `y`, `scroll_x`, `scroll_y`
- **`keypress`** - Press key(s)
  - Parameters: `keys` (array of key names)
- **`type`** - Type text
  - Parameters: `text`
- **`wait`** - Pause execution
  - No parameters (typically 2 seconds)
- **`screenshot`** - Request screenshot
  - No parameters (taken automatically each turn)
- **`drag`** - Drag from one point to another
  - Parameters: start and end coordinates

### Action Response Format

```json
{
  "type": "computer_call",
  "id": "cu_67cc...",
  "call_id": "call_zw3...",
  "action": {
    "type": "click",
    "button": "left",
    "x": 156,
    "y": 50
  },
  "pending_safety_checks": [],
  "status": "completed"
}
```

## 5. Screenshot and Image Handling

### Image Input Format

Send screenshots as base64-encoded images:

```python
{
    "type": "input_image",
    "image_url": f"data:image/png;base64,{screenshot_base64}",
    "detail": "high"  # or "low" or "auto"
}
```

### Detail Levels

- **`low`** - Fixed 85 tokens regardless of image size; 512x512 resolution sent to model
- **`high`** - Variable tokens based on image size; full resolution analysis
- **`auto`** - Model decides (default)

### Token Calculation (GPT-4o, CUA)

**Low detail**: 85 tokens (fixed)

**High detail**:
1. Scale to fit 2048x2048 square (maintain aspect ratio)
2. Scale so shortest side is 768px
3. Count 512px tiles needed
4. Calculate: `(tiles * 170) + 85` tokens

**Examples**:
- 1024x1024 high detail: 4 tiles = (4 * 170) + 85 = **765 tokens**
- 2048x4096 high detail: 6 tiles = (6 * 170) + 85 = **1,105 tokens**
- Any size low detail: **85 tokens**

### Recommended Display Size

Use 1024x768 (XGA) resolution or similar for best performance and lower costs.

## 6. Pricing

### Access Options

**Operator (Consumer Product)**:
- $200/month ChatGPT Pro subscription
- US users only (currently)
- Managed virtual browser environment
- No technical implementation required

**API Access (Developer)**:
- Standard pay-per-use via Responses API
- No geographic restrictions
- You manage the execution environment

### Token Pricing

CUA uses the same token pricing as GPT-4o for images:

- **Low detail images**: 85 tokens each
- **High detail images**: Variable based on tile count

Pricing per token follows GPT-4o rates (check current pricing page).

### Cost Considerations

- Each loop iteration requires a screenshot (85-1000+ tokens)
- Multiple iterations per task = high cumulative cost
- Browser tasks typically require 5-20+ iterations
- Complex desktop tasks may require 50+ iterations

**⚠️ Task Cost Reality**: Multiply per-screenshot cost by iteration count for realistic budget:
- Browser task (10 iterations, 765 tokens avg): 10 * 765 * $2.50/MTok = **$0.019 input per task**
- Desktop task (50 iterations, 765 tokens avg): 50 * 765 * $2.50/MTok = **$0.096 input per task**
- Add output token costs (reasoning, action descriptions)

## 7. Safety Checks

### Built-in Safety Checks

OpenAI implements three safety check types:

- **`malicious_instructions`** - Detects adversarial content in screenshots that may alter model behavior
- **`irrelevant_domain`** - Checks if current URL is relevant to conversation history
- **`sensitive_domain`** - Warns when on sensitive websites (banking, healthcare, etc.)

### Handling Safety Checks

When `pending_safety_checks` is returned:

1. Hand control to end user for confirmation
2. User reviews and acknowledges the warning
3. Pass acknowledged checks in next request:

```python
{
    "type": "computer_call_output",
    "call_id": "<call_id>",
    "acknowledged_safety_checks": [
        {
            "id": "<safety_check_id>",
            "code": "malicious_instructions",
            "message": "..."
        }
    ],
    "output": {
        "type": "computer_screenshot",
        "image_url": "..."
    }
}
```

### Best Practice

Always pass `current_url` in `computer_call_output` to improve safety check accuracy.

## 8. Benchmarks and Performance

### OSWorld Benchmark

Tests general computer task completion across operating systems:

- **OpenAI CUA**: 38.1%
- **Anthropic Computer Use**: 22%
- **Human performance**: 72.4%

**Note**: CUA operates in controlled virtual environments; Anthropic operates in real desktop environments with more complexity.

### WebVoyager Benchmark

Tests browser-based task completion:

- **OpenAI CUA**: 87%
- **Anthropic Computer Use**: 56%

### WebArena Benchmark

- **OpenAI CUA**: 58.1%

### Interpretation

CUA excels at browser tasks but both systems fall significantly short of human performance. The benchmarks suggest early implementations rather than mature technology.

## 9. Best Practices

### Environment Setup

1. **Use sandboxed environment** - Docker container or isolated VM
2. **Disable extensions** - Prevent security risks
3. **Block file system access** - Use `--disable-file-system` flag
4. **Empty environment variables** - Set `env: {}` to avoid leaking host data

### Playwright/Selenium Setup

```python
browser = p.chromium.launch(
    headless=False,
    chromium_sandbox=True,
    env={},
    args=[
        "--disable-extensions",
        "--disable-file-system"
    ]
)
page = browser.new_page()
page.set_viewport_size({"width": 1024, "height": 768})
```

### Prompting

1. **Clear, specific instructions** - Break complex tasks into steps
2. **Verify after actions** - Model may assume outcomes without checking
3. **Use keyboard shortcuts** - For complex UI elements (dropdowns, scrollbars)

### Safety

1. **Implement blocklists/allowlists** - Restrict to expected websites
2. **Human in the loop** - Require confirmation for high-stakes actions
3. **Send safety identifiers** - Help OpenAI monitor for abuse
4. **Monitor for anomalies** - Detect unexpected behavior patterns

### Cost Control

1. **Use low detail mode** - When high resolution not needed
2. **Set iteration limits** - Prevent runaway loops
3. **Optimize display size** - 1024x768 is cost-effective

## 10. Limitations

### Reliability Issues

- **OSWorld 38.1%** - Far below human 72.4%
- **Non-browser environments** - Less reliable than browser
- **Dynamic interfaces** - Higher error rates with pop-ups, animations
- **Multi-step authentication** - Often fails

### Vision Limitations

- **Medical images** - Not suitable for CT scans, X-rays
- **Non-Latin text** - Lower accuracy for Japanese, Korean, etc.
- **Small text** - May miss or misread
- **Rotated content** - Struggles with orientation
- **Complex graphs** - Difficulty with varying line styles, colors
- **Spatial reasoning** - Cannot precisely locate positions (chess, maps)
- **Counting** - Gives approximate counts only
- **CAPTCHAs** - Blocked for safety reasons

### Speed

Model is slower than human operators. Factor latency into automation planning.

## 11. Comparison with Anthropic

### Architectural Philosophy

- **OpenAI CUA**: Browser-first, cloud-based virtual browser
- **Anthropic**: Desktop-first, full OS integration, self-hosted

### Environment Support

- **OpenAI CUA**: Optimized for browser; desktop modes less reliable
- **Anthropic**: Full desktop (Linux reference impl), any application

### Pricing Model

- **OpenAI Operator**: $200/month subscription (US only)
- **OpenAI API**: Pay-per-use via Responses API
- **Anthropic**: Pay-per-use via Messages API (no subscription)

### Control

- **OpenAI CUA**: Managed infrastructure (Operator) or self-managed (API)
- **Anthropic**: Always self-managed, you control the environment

### Best For

- **OpenAI CUA**: Browser automation, web forms, consumer tasks
- **Anthropic**: Desktop automation, native apps, enterprise workflows

## 12. Implementation Architecture

### Reference Implementation

OpenAI provides a sample app repository:
https://github.com/openai/openai-cua-sample-app

Components:
- Browser environment setup (Playwright/Selenium)
- Docker VM environment setup
- Action handlers for all computer_call types
- CUA loop implementation
- Safety check handling

### Windows Desktop Implementation

For windows-desktop-control skill:

1. **Screenshot capture**: Use Pillow, pyautogui, or mss
2. **Input simulation**: pyautogui, pynput, or Win32 API
3. **Environment parameter**: Set to `"windows"`
4. **Coordinate handling**: Match display_width/height to actual resolution
5. **Safety**: Implement dry-run mode, confirmation prompts

**⚠️ Windows DPI Scaling Complexity**: Coordinate translation is more complex than simple division due to:
- Fractional scaling (125%, 150%, 175%)
- Per-monitor DPI differences
- DPI-aware vs DPI-unaware application behavior
- Windows Desktop Window Manager (DWM) bitmap stretching

**Recommendation**: Test on target Windows DPI settings before production deployment. Consider using Win32 API to query actual DPI per monitor.

### Agent Loop Pattern

```python
while iterations < max_iterations:
    response = client.responses.create(
        model="computer-use-preview",
        previous_response_id=prev_id,
        tools=[{"type": "computer_use_preview", ...}],
        input=[{
            "type": "computer_call_output",
            "call_id": call_id,
            "output": {"type": "computer_screenshot", "image_url": screenshot},
            "current_url": current_url
        }],
        truncation="auto"
    )
    
    # Find computer_call in output
    computer_call = next(
        (item for item in response.output if item.type == "computer_call"),
        None
    )
    
    if not computer_call:
        break  # Task complete
    
    # Handle safety checks
    if computer_call.pending_safety_checks:
        # Get user confirmation
        ...
    
    # Execute action
    execute_action(computer_call.action)
    
    # Capture new screenshot
    screenshot = capture_screenshot()
    prev_id = response.id
    call_id = computer_call.call_id
```

## 13. Sources

**Primary Sources (OpenAI Official)**:

- `OAICU-IN01-SC-PLATF-CMPU`: https://platform.openai.com/docs/guides/tools-computer-use
  - Complete computer use tool documentation [VERIFIED]

- `OAICU-IN01-SC-PLATF-MODL`: https://platform.openai.com/docs/models/computer-use-preview
  - Model overview and capabilities [VERIFIED]

- `OAICU-IN01-SC-PLATF-VISN`: https://platform.openai.com/docs/guides/images-vision
  - Image token calculation, detail levels [VERIFIED]

- `OAICU-IN01-SC-PLATF-PRIC`: https://platform.openai.com/docs/pricing
  - Token and tool pricing [VERIFIED]

- `OAICU-IN01-SC-GTHUB-SAMP`: https://github.com/openai/openai-cua-sample-app
  - Official reference implementation [VERIFIED]

**Secondary Sources**:

- `OAICU-IN01-SC-WORKOS-CMP`: https://workos.com/blog/anthropics-computer-use-versus-openais-computer-using-agent-cua
  - Comparison article with benchmarks [VERIFIED]

## 14. Provider Selection Guide

### For Windows Desktop Automation

**❌ Not Recommended: OpenAI CUA**
- Browser-optimized (87% WebVoyager vs 38.1% OSWorld)
- 48.9 percentage points worse on desktop tasks
- Non-browser environments have "lower reliability"
- `"windows"` environment parameter exists but not production-ready

**✅ Recommended: Anthropic Computer Use**
- Desktop-first architecture
- Works with native Windows applications
- OSWorld: 22% (lower than OpenAI but tested on real desktop)

### For Browser Automation

**✅ Recommended: OpenAI CUA**
- WebVoyager: 87%
- Browser-first design
- Built-in safety checks (malicious_instructions, irrelevant_domain, sensitive_domain)
- Managed Operator product available ($200/month)

**❌ Anthropic Computer Use**
- WebVoyager: 56%
- Works but not optimized for browser

### Hybrid Approach

**Best of both worlds**:
- **OpenAI CUA** for web-based tasks (forms, navigation, search)
- **Anthropic Computer Use** for native Windows applications

### Critical Warning

⚠️ **For windows-desktop-control skill**: OpenAI CUA's browser-first design conflicts with Windows desktop automation goal. Use Anthropic for desktop, OpenAI for browser tasks only.

## 15. Next Steps

1. **Integrate with windows-desktop-control**: Implement OpenAI CUA alongside Anthropic
2. **Benchmark comparison**: Test both providers on same Windows tasks
3. **Cost analysis**: Compare actual costs per automation task
4. **Hybrid approach**: Consider using OpenAI for browser, Anthropic for desktop

## 15. Document History

**[2026-01-27 19:05]**
- Added: Provider Selection Guide (Section 14) - OpenAI NOT recommended for Windows desktop
- Added: Critical Warning about browser-first design vs Windows desktop goal
- Added: Windows DPI Scaling complexity warning in Implementation Architecture
- Added: Task Cost Reality calculation with iteration multipliers
- Added: Security Implementation Requirements with prompt injection mitigation checklist

**[2026-01-27 18:56]**
- Fixed: Expanded acronyms (VM, XGA) on first use

**[2026-01-27 18:51]**
- Initial research document created
- Researched: model, API specs, actions, image handling, pricing, safety, benchmarks, best practices, limitations
