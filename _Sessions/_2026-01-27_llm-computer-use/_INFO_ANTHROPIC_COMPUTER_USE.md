# INFO: Anthropic Computer Use

**Doc ID**: ANTCU-IN01
**Goal**: Comprehensive research on Anthropic Claude Computer Use for windows-desktop-control skill development
**Timeline**: Created 2026-01-27, Updated 2 times (2026-01-27)

## Summary

- Claude Computer Use is a beta API feature enabling desktop automation via screenshots, mouse, and keyboard [VERIFIED]
- **Supported models**: Claude Opus 4.5, Sonnet 4.5, Haiku 4.5, Sonnet 4, Opus 4, Opus 4.1, Sonnet 3.7 [VERIFIED]
- **Tool versions**: `computer_20251124` (Opus 4.5 with zoom), `computer_20250124` (all others) [VERIFIED]
- **Image sizing**: Max 1568px long edge, ~1.15 megapixels, ~1,600 tokens per screenshot [VERIFIED]
- **Image cost formula**: `tokens = (width * height) / 750` [VERIFIED]
- **Pricing (Sonnet 4.5)**: $3/MTok input, $15/MTok output; screenshots ~$4.80/1K images at max size [VERIFIED]
- **System prompt overhead**: 466-499 tokens added for computer use [VERIFIED]
- **Latency**: Too slow for real-time human-AI interactions; best for background tasks [VERIFIED]
- **Latency benchmark**: Claude Sonnet 4.5 ~2s TTFT, ~0.030s per token [ASSUMED - third-party source]
- **Key limitation**: Prompt injection vulnerability via screenshot content [VERIFIED]
- **Recommendation**: Use virtual machines/containers, limit to trusted environments [VERIFIED]

## Table of Contents

1. [Overview](#1-overview)
2. [Supported Models and Tool Versions](#2-supported-models-and-tool-versions)
3. [API Specifications](#3-api-specifications)
4. [Available Actions](#4-available-actions)
5. [Screenshot Handling](#5-screenshot-handling)
6. [Pricing](#6-pricing)
7. [Rate Limits](#7-rate-limits)
8. [Latency and Response Times](#8-latency-and-response-times)
9. [Best Practices](#9-best-practices)
10. [Limitations](#10-limitations)
11. [Security Considerations](#11-security-considerations)
12. [Implementation Architecture](#12-implementation-architecture)
13. [Sources](#13-sources)
14. [Next Steps](#14-next-steps)
15. [Document History](#15-document-history)

## 1. Overview

Computer Use is a beta feature that enables Claude to interact with desktop environments through:

- **Screenshot capture**: See what's currently displayed on screen
- **Mouse control**: Click, drag, and move the cursor
- **Keyboard input**: Type text and use keyboard shortcuts
- **Desktop automation**: Interact with any application or interface

The feature works through an agent loop where:
1. You send Claude a user prompt with the computer use tool
2. Claude returns tool use requests (screenshot, click, type, etc.)
3. Your application executes those actions on the actual computer
4. You send results (screenshots, success/error) back to Claude
5. Loop continues until Claude completes the task or reaches max iterations

**Critical**: Claude does NOT directly connect to any computer. Your application is responsible for:
- Receiving Claude's tool requests
- Translating them into actual actions
- Capturing results
- Returning results to Claude

## 2. Supported Models and Tool Versions

### Model Compatibility

All Claude 4.x models and Sonnet 3.7 support computer use:

- **Claude Opus 4.5** - Uses `computer_20251124` (newest, includes zoom action)
- **Claude Sonnet 4.5** - Uses `computer_20250124`
- **Claude Haiku 4.5** - Uses `computer_20250124`
- **Claude Sonnet 4** - Uses `computer_20250124`
- **Claude Opus 4** - Uses `computer_20250124`
- **Claude Opus 4.1** - Uses `computer_20250124`
- **Claude Sonnet 3.7** - Uses `computer_20250124` (introduced thinking capability)

### Tool Versions

- **`computer_20251124`**
  - Beta flag: `computer-use-2025-11-24`
  - Models: Claude Opus 4.5 only
- **`computer_20250124`**
  - Beta flag: `computer-use-2025-01-24`
  - Models: All other supported models

**Important**: Tool versions are NOT backwards-compatible. Always use the version matching your model.

## 3. API Specifications

### Endpoint

```
POST https://api.anthropic.com/v1/messages
```

### Required Headers

```
Content-Type: application/json
x-api-key: $ANTHROPIC_API_KEY
anthropic-version: 2023-06-01
anthropic-beta: computer-use-2025-01-24
```

### Basic Request Structure

```python
import anthropic

client = anthropic.Anthropic()
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[
        {
            "type": "computer_20250124",
            "name": "computer",
            "display_width_px": 1024,
            "display_height_px": 768,
            "display_number": 1,
        },
        {
            "type": "text_editor_20250728",
            "name": "str_replace_based_edit_tool"
        },
        {
            "type": "bash_20250124",
            "name": "bash"
        }
    ],
    messages=[{"role": "user", "content": "Save a picture of a cat to my desktop."}],
    betas=["computer-use-2025-01-24"]
)
```

### Tool Parameters

- **type**: `computer_20251124` or `computer_20250124`
- **name**: Must be `"computer"`
- **display_width_px**: Screen width in pixels
- **display_height_px**: Screen height in pixels
- **display_number**: Display number (typically 1)
- **enable_zoom**: (Opus 4.5 only) Set to `true` to enable zoom action

### Companion Tools

Computer use is often combined with:
- **Bash tool** (`bash_20250124`): Execute shell commands
- **Text editor tool** (`text_editor_20250728`): Edit files

### Authentication

Standard Anthropic API key authentication via `x-api-key` header.

## 4. Available Actions

### Basic Actions (All Versions)

- **`screenshot`** - Capture current display (no parameters)
- **`left_click`** - Click at coordinates (`coordinate: [x, y]`)
- **`type`** - Type text string (`text: string`)
- **`key`** - Press key or combo (`key: string`, e.g., "ctrl+s")
- **`mouse_move`** - Move cursor (`coordinate: [x, y]`)

### Enhanced Actions (computer_20250124)

Available in Claude 4 models and Sonnet 3.7:

- **`scroll`** - Scroll in any direction (`direction, amount`)
- **`left_click_drag`** - Click and drag (`start, end coordinates`)
- **`right_click`** - Right mouse button (`coordinate: [x, y]`)
- **`middle_click`** - Middle mouse button (`coordinate: [x, y]`)
- **`double_click`** - Double click (`coordinate: [x, y]`)
- **`triple_click`** - Triple click (`coordinate: [x, y]`)
- **`left_mouse_down`** - Press mouse button (`coordinate: [x, y]`)
- **`left_mouse_up`** - Release mouse button (`coordinate: [x, y]`)
- **`hold_key`** - Hold key for duration (`key, duration_seconds`)
- **`wait`** - Pause between actions (`duration_seconds`)

### Opus 4.5 Exclusive (computer_20251124)

- **`zoom`** - View region at full resolution (`region: [x1, y1, x2, y2]`)

Requires `enable_zoom: true` in tool definition.

## 5. Screenshot Handling

### Size Constraints

- **Maximum dimensions**: 8000x8000 pixels (rejected if exceeded)
- **Multi-image limit**: 2000x2000 px when sending >20 images per request
- **Optimal dimensions**: 1568px max on long edge, ~1.15 megapixels total
- **Minimum size**: >200px on each edge (smaller degrades performance)

### Automatic Resizing

The API automatically resizes images exceeding limits:
- Long edge > 1568px: Scaled down preserving aspect ratio
- Total pixels > ~1.15 megapixels: Scaled to fit

**Impact**: Oversized images increase Time-to-First-Token (TTFT) without improving performance.

### Token Calculation

```
tokens = (width_px * height_px) / 750
```

**Examples at ~1,600 tokens (max recommended)**:
- 1568 x 764 (16:9)
- 1184 x 1016 (4:3)
- 1072 x 1120 (1:1)

### Supported Formats

- JPEG
- PNG
- GIF
- WebP

### Quality Recommendations

- Ensure images are clear, not blurry or pixelated
- Text must be legible, not too small
- Avoid cropping key visual context to enlarge text

### Coordinate Scaling

**Critical for higher resolutions**: The API downsamples large images but Claude returns coordinates in the downsampled space. You must scale coordinates back up:

```python
import math

def get_scale_factor(width, height):
    """Calculate scale factor to meet API constraints."""
    long_edge = max(width, height)
    total_pixels = width * height
    long_edge_scale = 1568 / long_edge
    total_pixels_scale = math.sqrt(1_150_000 / total_pixels)
    return min(1.0, long_edge_scale, total_pixels_scale)

# When capturing screenshot
scale = get_scale_factor(screen_width, screen_height)
scaled_width = int(screen_width * scale)
scaled_height = int(screen_height * scale)

# When handling Claude's coordinates, scale them back up
def execute_click(x, y):
    screen_x = x / scale
    screen_y = y / scale
    perform_click(screen_x, screen_y)
```

## 6. Pricing

### Model Token Pricing (Claude Sonnet 4.5)

- **Base Input**: $3 / MTok
- **Output**: $15 / MTok
- **Cache Write (5-min)**: $3.75 / MTok (1.25x)
- **Cache Write (1-hour)**: $6 / MTok (2x)
- **Cache Read**: $0.30 / MTok (0.1x)

### Computer Use Overhead

- **System prompt**: 466-499 tokens added automatically
- **Tool definition tokens**: Additional per-tool overhead

### Screenshot Costs

At maximum recommended size (~1,600 tokens per image):

```
Cost per screenshot = 1,600 tokens * $3 / 1,000,000
                    = ~$0.0048 per screenshot
                    = ~$4.80 per 1,000 screenshots
```

**⚠️ Task Cost Reality**: Typical tasks require multiple iterations:
- Browser tasks: 10-20 iterations
- Desktop tasks: 50+ iterations
- **Multiply per-screenshot cost by iteration count for realistic budget**
- Example: 20-iteration task = 20 * $0.0048 = **$0.096 per task**

### Companion Tool Overhead

- **Bash tool**: +245 input tokens
- **Text editor tool**: Model-dependent, see pricing docs

### Cost Optimization Strategies

1. **Use appropriate models**: Haiku for simple tasks, Sonnet for complex reasoning
2. **Prompt caching**: Reduce costs for repeated context (up to 90% savings on cache hits)
3. **Batch API**: 50% discount for async, non-time-sensitive tasks
4. **Screenshot sizing**: Pre-resize to optimal dimensions to avoid wasted tokens

### Example Agent Cost

Customer support agent (10,000 tickets):
- ~3,700 tokens per conversation average
- Total: ~$22.20 for 10,000 tickets using Sonnet 4.5

## 7. Rate Limits

### Tier System

Anthropic uses tiered rate limits based on cumulative spend:

- **Tier 1**: $100/month limit (initial tier)
- **Tier 2**: $500/month limit (requires $50 cumulative purchases)
- **Tier 3**: $2,000/month limit (requires $200 cumulative purchases)
- **Tier 4**: $5,000/month limit (requires $1,000 cumulative purchases)
- **Custom**: Negotiable (contact sales)

### Rate Limit Types

- **RPM (Requests Per Minute)**: Maximum API calls allowed per minute
- **ITPM (Input Tokens Per Minute)**: Maximum input tokens processed per minute
- **OTPM (Output Tokens Per Minute)**: Maximum output tokens generated per minute

### Handling Rate Limits

429 errors include a `retry-after` header indicating wait time. Implement exponential backoff.

**Token bucket algorithm**: Capacity replenishes continuously, not at fixed intervals. Short bursts can exceed limits.

### Acceleration Limits

Sharp usage increases can trigger 429 errors even within rate limits. Recommendation: Ramp up traffic gradually.

## 8. Latency and Response Times

### Key Metrics

- **Baseline latency**: Time for model to process prompt and generate response
- **TTFT (Time to First Token)**: Time until first token arrives
- **Per-token latency**: Time between subsequent tokens

### Benchmark Data (Third-Party)

Claude Sonnet 4.5 [ASSUMED - external source]:
- **TTFT**: ~2 seconds
- **Per-token latency**: ~0.030 seconds

### Computer Use Latency Reality

From Anthropic documentation [VERIFIED]:
> "The current computer use latency for human-AI interactions may be too slow compared to regular human-directed computer actions."

**Recommended use cases**:
- Background information gathering
- Automated software testing
- Non-time-critical workflows

**Not recommended for**:
- Real-time user interactions
- Speed-critical automation

### Latency Reduction Strategies

1. **Choose faster models**: Haiku 4.5 for speed-critical tasks
2. **Optimize prompts**: Fewer tokens = faster processing
3. **Use streaming**: See results as they generate
4. **Pre-resize images**: Avoid API-side resizing overhead
5. **Limit max_tokens**: Set appropriate output limits
6. **Lower temperature**: Can produce more focused, shorter responses

## 9. Best Practices

### Prompting

1. **Be explicit**: Specify simple, well-defined tasks with explicit instructions for each step

2. **Verify actions**: Add verification prompts:
   ```
   After each step, take a screenshot and carefully evaluate if you have achieved 
   the right outcome. Explicitly show your thinking: "I have evaluated step X..." 
   If not correct, try again. Only when you confirm a step was executed correctly 
   should you move on to the next one.
   ```

3. **Use keyboard shortcuts**: For tricky UI elements (dropdowns, scrollbars), prompt model to use keyboard shortcuts instead of mouse

4. **Provide examples**: For repeatable tasks, include example screenshots and tool calls of successful outcomes

5. **Credentials handling**: Provide login credentials in XML tags:
   ```xml
   <robot_credentials>
   username: ...
   password: ...
   </robot_credentials>
   ```

### Implementation

1. **Set iteration limits**: Prevent infinite loops and runaway API costs
   ```python
   max_iterations = 10  # Reasonable limit
   ```

2. **Implement proper error handling**: Tool execution failures should be reported back to Claude

3. **Use sandboxed environments**: Docker containers or VMs with minimal privileges

4. **Handle coordinate scaling**: For resolutions exceeding API limits

5. **Enable thinking mode** (Sonnet 3.7+): Adds visibility into reasoning
   ```python
   thinking = {"type": "enabled", "budget_tokens": 1024}
   ```

### Agent Loop Pattern

```python
iterations = 0
while iterations < max_iterations:
    iterations += 1
    response = client.beta.messages.create(...)
    
    # Process response
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            result = execute_tool(block.name, block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result
            })
    
    # Check completion
    if not tool_results:
        break  # Task complete
    
    # Continue loop
    messages.append({"role": "user", "content": tool_results})
```

## 10. Limitations

### Accuracy Issues

1. **Coordinate accuracy**: Claude may make mistakes or hallucinate specific coordinates
2. **Tool selection**: May select wrong tools or take unexpected actions
3. **Niche applications**: Lower reliability with specialized software
4. **Multiple applications**: Reduced accuracy when interacting with several apps simultaneously

### Functional Limitations

1. **Spatial reasoning**: Limited ability for precise localization (analog clocks, chess positions)
2. **Counting**: Approximate counts only, especially with many small objects
3. **AI image detection**: Cannot reliably detect AI-generated images
4. **People identification**: Will NOT identify (name) people in images (policy restriction)

### Platform Restrictions

1. **Social media**: Limited ability to create accounts, generate/share content on social platforms
2. **Content generation**: Cannot engage in human impersonation on communications platforms

### Vision Limitations

1. **Low-quality images**: May hallucinate or make mistakes
2. **Rotated images**: Accuracy degrades
3. **Very small images**: Under 200px causes performance degradation
4. **Complex diagnostics**: Not designed for CT/MRI interpretation

## 11. Security Considerations

### Prompt Injection Vulnerability

**Critical**: Claude may follow instructions found in screenshot content, even conflicting with user instructions.

Example: A malicious website could display text that overrides your automation instructions.

### Mitigations

1. **Sandboxed environment**: Use dedicated VM or container with minimal privileges
2. **Avoid sensitive data access**: Don't give computer use access to sensitive accounts without oversight
3. **Internet allowlist**: Limit web access to specific trusted domains
4. **Human confirmation**: Require human approval for:
   - Meaningful real-world consequences
   - Affirmative consent actions (cookies, financial transactions, ToS)
5. **Classifier protection**: Anthropic runs automatic classifiers to flag potential prompt injections and steer model to ask for confirmation

### Opting Out of Protection

If automated prompt injection protection interferes with your use case (e.g., no human in loop), contact Anthropic support to opt out.

### User Consent

Inform end users of relevant risks and obtain consent before enabling computer use features.

### Security Implementation Requirements

**⚠️ Prompt Injection Risk**: Documented exploits exist (GPT-Store leaks, ChatGPT memory exploits). Before production deployment:

1. **Screenshot content scanning**: Implement detection for suspicious instructions in screenshots
2. **Action logging**: Log all actions for audit trail and forensic analysis
3. **Suspicious action detection**: Define high-risk actions requiring human confirmation
4. **Human confirmation flow**: Require explicit approval for:
   - File deletions or modifications
   - Financial transactions
   - Account access or credential entry
   - System configuration changes

## 12. Implementation Architecture

### Reference Implementation

Anthropic provides a complete reference implementation:
https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo

Components:
- **Docker container**: Sandboxed Linux environment (Xvfb, Mutter, Tint2)
- **Tool implementations**: Python handlers for screenshot, click, type, etc.
- **Agent loop**: Handles Claude API interaction and tool execution
- **Web interface**: User interaction with the container

### Custom Implementation Requirements

1. **Computing environment**: Virtualized display (Xvfb or similar)
2. **Tool implementations**: Translate Claude's abstract requests to actual actions
3. **Agent loop**: Communication between Claude and environment
4. **API/UI**: Accept user input to start automation

### Windows Desktop Considerations

For windows-desktop-control skill:

1. **Screenshot capture**: Use Win32 API or libraries (PIL, pyautogui, mss)
2. **Input simulation**: Win32 API SendInput or pyautogui
3. **Coordinate translation**: Handle DPI scaling and multi-monitor setups
4. **Safety**: Implement dry-run mode, confirmation prompts

**⚠️ Windows DPI Scaling Complexity**: Coordinate translation is more complex than simple division due to:
- Fractional scaling (125%, 150%, 175%)
- Per-monitor DPI differences
- DPI-aware vs DPI-unaware application behavior
- Windows Desktop Window Manager (DWM) bitmap stretching

**Recommendation**: Test on target Windows DPI settings before production deployment. Consider using Win32 API to query actual DPI per monitor.

## 13. Sources

**Primary Sources (Anthropic Official)**:

- `ANTCU-IN01-SC-PLATF-CMPU`: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
  - Complete computer use tool documentation [VERIFIED]

- `ANTCU-IN01-SC-PLATF-PRIC`: https://platform.claude.com/docs/en/about-claude/pricing
  - Token pricing, tool overhead, agent examples [VERIFIED]

- `ANTCU-IN01-SC-PLATF-VISN`: https://platform.claude.com/docs/en/build-with-claude/vision
  - Image sizing, token calculation, quality guidelines [VERIFIED]

- `ANTCU-IN01-SC-PLATF-MODL`: https://platform.claude.com/docs/en/about-claude/models/overview
  - Model comparison, capabilities [VERIFIED]

- `ANTCU-IN01-SC-PLATF-RATE`: https://platform.claude.com/docs/en/api/rate-limits
  - Rate limit tiers and handling [VERIFIED]

- `ANTCU-IN01-SC-PLATF-LATN`: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency
  - Latency metrics and reduction strategies [VERIFIED]

- `ANTCU-IN01-SC-CLAUD-PRIC`: https://claude.com/pricing
  - Consumer pricing tiers [VERIFIED]

**Secondary Sources**:

- `ANTCU-IN01-SC-AIMLT-LTCY`: https://research.aimultiple.com/llm-latency-benchmark/
  - Third-party latency benchmarks [ASSUMED - requires verification]

**Reference Implementation**:

- `ANTCU-IN01-SC-GTHUB-DEMO`: https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo
  - Official reference implementation [VERIFIED]

## 14. Provider Selection Guide

### For Windows Desktop Automation

**✅ Recommended: Anthropic Computer Use**
- Desktop-first architecture
- Works with native Windows applications
- Full OS integration (any application)
- Self-managed environment = full control
- OSWorld: 22% (Linux-based benchmark)

**❌ Not Recommended: OpenAI CUA**
- Browser-optimized (87% WebVoyager vs 38.1% OSWorld)
- 48.9 percentage points worse on desktop tasks
- Non-browser environments have "lower reliability"

### For Browser Automation

**❌ Anthropic Computer Use**
- WebVoyager: 56%
- Works but not optimized for browser

**✅ OpenAI CUA**
- WebVoyager: 87%
- Browser-first design
- Built-in safety checks

### Hybrid Approach

Consider using both:
- **OpenAI CUA** for web-based tasks (forms, navigation, search)
- **Anthropic Computer Use** for native Windows applications

### Platform Considerations

**⚠️ Benchmark Limitation**: OSWorld benchmarks are Linux-based (Ubuntu). Windows desktop reliability is untested but expected to be similar since the model processes screenshots, not OS-specific APIs.

## 15. Next Steps

1. **Proof of Concept**: Build minimal windows-desktop-control implementation using pyautogui
2. **Benchmark latency**: Measure actual TTFT and per-action latency in our environment
3. **Cost modeling**: Calculate expected costs for typical automation workflows
4. **Safety framework**: Design dry-run mode and confirmation flow
5. **Skill architecture**: Define skill interface for LLM-computer-use integration

## 15. Document History

**[2026-01-27 19:05]**
- Added: Provider Selection Guide (Section 14) - Anthropic recommended for Windows desktop
- Added: Windows DPI Scaling complexity warning in Implementation Architecture
- Added: Task Cost Reality calculation with iteration multipliers
- Added: Security Implementation Requirements with prompt injection mitigation checklist
- Added: Platform Considerations note about Linux-based benchmarks

**[2026-01-27 18:46]**
- Fixed: Converted 7 Markdown tables to lists (per core conventions)
- Fixed: Expanded acronyms on first use (TTFT, RPM, ITPM, OTPM)
- Fixed: Timeline format corrected

**[2026-01-27 18:36]**
- Initial research document created
- Researched: model compatibility, API specs, pricing, vision, rate limits, latency, best practices, limitations, security
