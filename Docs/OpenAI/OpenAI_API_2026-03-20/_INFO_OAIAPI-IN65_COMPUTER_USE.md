# Computer Use (CUA) [PREVIEW]

**Doc ID**: OAIAPI-IN65
**Goal**: Document the [PREVIEW] computer_use tool for UI-based agent automation - screenshots, clicks, typing, scrolling
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

Computer Use Agent (CUA) enables models to operate software through the user interface. The `computer_use` tool type in the Responses API lets models inspect screenshots and return interface actions (click, type, scroll, keypress, etc.) for the developer's code to execute. The model receives a screenshot, analyzes visible UI elements, and returns the next action to take. The developer executes the action on the target environment (virtual machine, browser, desktop) and sends back a new screenshot. This loop continues until the task is complete. CUA supports multiple environments: virtual desktop, browser, and custom harnesses. The model can handle complex multi-step workflows like form filling, navigation, data entry, and application testing. Actions include click (with coordinates), type (text input), scroll, keypress, drag, double_click, and screenshot requests. The tool requires specifying display dimensions (width, height) for coordinate mapping. CUA works with `computer-use-preview` and newer models optimized for UI understanding. [VERIFIED] (OAIAPI-SC-OAI-GCUA)

## Key Facts

- **Tool type**: `computer_use` in Responses API [VERIFIED] (OAIAPI-SC-OAI-GCUA)
- **Loop pattern**: Screenshot -> model analyzes -> returns action -> execute -> screenshot [VERIFIED] (OAIAPI-SC-OAI-GCUA)
- **Actions**: click, type, scroll, keypress, drag, double_click, screenshot [VERIFIED] (OAIAPI-SC-OAI-GCUA)
- **Environments**: Virtual desktop, browser, custom harness [VERIFIED] (OAIAPI-SC-OAI-GCUA)
- **Models**: computer-use-preview and newer [VERIFIED] (OAIAPI-SC-OAI-GCUA)
- **Display config**: Must specify width and height for coordinate system [VERIFIED] (OAIAPI-SC-OAI-GCUA)

## Use Cases

- **UI testing**: Automated visual testing of web/desktop applications
- **Data entry**: Fill forms across applications that lack APIs
- **Process automation**: Automate multi-step workflows in legacy systems
- **Web scraping**: Navigate dynamic sites with JS rendering
- **Application monitoring**: Check UI state and capture screenshots

## Quick Reference

```json
{
  "model": "computer-use-preview",
  "tools": [
    {
      "type": "computer_use",
      "display_width": 1280,
      "display_height": 720,
      "environment": "browser"
    }
  ],
  "input": [
    {
      "type": "message",
      "role": "user",
      "content": "Go to example.com and find the contact page"
    }
  ]
}
```

## Action Types

- **click**: Click at coordinates (x, y). Options: left/right/middle button
- **double_click**: Double-click at coordinates
- **type**: Type text string
- **keypress**: Press key combination (e.g., "ctrl+c", "enter")
- **scroll**: Scroll at coordinates (x, y) with direction (up/down/left/right)
- **drag**: Drag from (x1, y1) to (x2, y2)
- **screenshot**: Request a new screenshot (no action, just observe)
- **wait**: Wait for specified duration

## CUA Loop Pattern

```
1. Send task + initial screenshot to model
2. Model returns computer_use action (e.g., click at 640,360)
3. Execute action on environment
4. Capture new screenshot
5. Send screenshot back to model
6. Model returns next action or final response
7. Repeat 3-6 until task complete
```

## SDK Examples (Python)

### Basic CUA Loop

```python
from openai import OpenAI
import base64

client = OpenAI()

def encode_screenshot(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def run_cua_task(task: str, initial_screenshot: str):
    """Run a computer use agent task"""
    screenshot_b64 = encode_screenshot(initial_screenshot)
    
    response = client.responses.create(
        model="computer-use-preview",
        tools=[{
            "type": "computer_use",
            "display_width": 1280,
            "display_height": 720,
            "environment": "browser"
        }],
        input=[
            {
                "type": "message",
                "role": "user",
                "content": [
                    {"type": "text", "text": task},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{screenshot_b64}"
                        }
                    }
                ]
            }
        ]
    )
    
    return response

# Execute
response = run_cua_task(
    "Click the Login button",
    "screenshot.png"
)

# Process actions from response
for item in response.output:
    if item.type == "computer_call":
        action = item.action
        print(f"Action: {action.type}")
        if hasattr(action, 'x'):
            print(f"  Coordinates: ({action.x}, {action.y})")
        if hasattr(action, 'text'):
            print(f"  Text: {action.text}")
```

### Full CUA Loop - Production Ready

```python
from openai import OpenAI
import base64
import time

client = OpenAI()

class CUAAgent:
    """Computer Use Agent with loop execution"""
    
    def __init__(self, environment="browser", width=1280, height=720, max_steps=20):
        self.environment = environment
        self.width = width
        self.height = height
        self.max_steps = max_steps
    
    def run(self, task: str, screenshot_provider, action_executor):
        """
        Execute CUA task.
        screenshot_provider: callable returning screenshot bytes
        action_executor: callable(action) that executes the action
        """
        screenshot = screenshot_provider()
        screenshot_b64 = base64.b64encode(screenshot).decode()
        
        input_messages = [
            {
                "type": "message",
                "role": "user",
                "content": [
                    {"type": "text", "text": task},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{screenshot_b64}"
                        }
                    }
                ]
            }
        ]
        
        for step in range(self.max_steps):
            response = client.responses.create(
                model="computer-use-preview",
                tools=[{
                    "type": "computer_use",
                    "display_width": self.width,
                    "display_height": self.height,
                    "environment": self.environment
                }],
                input=input_messages
            )
            
            # Check for computer_call actions
            computer_calls = [o for o in response.output if o.type == "computer_call"]
            
            if not computer_calls:
                # No more actions - task complete
                text_output = response.output_text
                print(f"Task complete after {step + 1} steps")
                return text_output
            
            for call in computer_calls:
                action = call.action
                print(f"Step {step + 1}: {action.type}", end="")
                if hasattr(action, 'x'):
                    print(f" at ({action.x}, {action.y})", end="")
                print()
                
                # Execute action
                action_executor(action)
                time.sleep(0.5)  # Wait for UI to update
            
            # Capture new screenshot
            screenshot = screenshot_provider()
            screenshot_b64 = base64.b64encode(screenshot).decode()
            
            # Send screenshot as tool result
            input_messages = [{
                "type": "computer_call_output",
                "call_id": computer_calls[-1].call_id,
                "output": {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{screenshot_b64}"
                    }
                }
            }]
        
        print(f"Max steps ({self.max_steps}) reached")
        return None

# Usage with Playwright (example)
# agent = CUAAgent()
# result = agent.run(
#     "Navigate to example.com and click About",
#     screenshot_provider=lambda: page.screenshot(),
#     action_executor=lambda a: execute_playwright_action(page, a)
# )
```

## Error Responses

- **400 Bad Request** - Invalid display dimensions or action type
- **422 Unprocessable Entity** - Screenshot not provided when expected
- **429 Too Many Requests** - Rate limit exceeded

## Rate Limiting / Throttling

- **Per-step billing**: Each CUA iteration counts as a model call
- **Image tokens**: Screenshots consume vision tokens
- **Standard rate limits**: RPM and TPM apply

## Differences from Other APIs

- **vs Anthropic Computer Use**: Very similar concept. Anthropic launched computer use first (2024). Different action format but same loop pattern
- **vs Gemini**: No equivalent computer use tool
- **vs Grok**: No equivalent computer use tool
- **vs Playwright/Selenium**: CUA uses visual understanding; Playwright uses DOM selectors. CUA works on any visual interface

## Limitations and Known Issues

- **Coordinate accuracy**: Model may occasionally click wrong coordinates [VERIFIED] (OAIAPI-SC-OAI-GCUA)
- **Speed**: Each step requires model inference + screenshot capture [VERIFIED] (OAIAPI-SC-OAI-GCUA)
- **Complex UIs**: Dense or non-standard UIs may confuse the model [ASSUMED]
- **No direct DOM access**: Works purely from screenshots, no HTML inspection [VERIFIED] (OAIAPI-SC-OAI-GCUA)

## Gotchas and Quirks

- **Display dimensions must match**: Specified width/height must match actual screenshot dimensions [VERIFIED] (OAIAPI-SC-OAI-GCUA)
- **Wait after actions**: UI may need time to update after action execution [VERIFIED] (OAIAPI-SC-OAI-GCUA)
- **Max steps**: Always set a max step limit to prevent infinite loops [VERIFIED] (OAIAPI-SC-OAI-GCUA)
- **Environment hint**: The environment parameter helps model understand context (browser vs desktop) [VERIFIED] (OAIAPI-SC-OAI-GCUA)

## Sources

- OAIAPI-SC-OAI-GCUA - Computer Use Guide

## Document History

**[2026-03-20 19:56]**
- Added: [PREVIEW] status tag to title and goal

**[2026-03-20 18:36]**
- Initial documentation created
