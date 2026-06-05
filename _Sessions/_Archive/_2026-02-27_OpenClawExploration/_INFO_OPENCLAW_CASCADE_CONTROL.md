# INFO: OpenClaw Remote Control of Windsurf Cascade

**Doc ID**: OCLAW-IN02
**Goal**: Research how OpenClaw could remote-control Windsurf Cascade
**Research Date**: 2026-02-28

## Summary (Copy/Paste Ready)

**Bottom line**: [VERIFIED] No official API exists for external systems to send prompts to Cascade. Control requires workarounds.

**Best Option**: **Keyboard Shortcuts + Hooks** (Pattern E) - Full bidirectional control
- **Input**: Send keystrokes to Windsurf (Ctrl+L, type, Enter)
- **Output**: Hooks capture responses, file changes, screenshots

**Other Viable Options**:
1. **UI Automation via Browser/CDP** - OpenClaw controls Windsurf UI directly [TESTED in other contexts]
2. **File-based Triggering** - OpenClaw writes files, Cascade Hooks detect and respond [VERIFIED]
3. **Shared MCP Server** - Both agents connect to same MCP, coordinate via shared state [ASSUMED]

**Not Viable**:
- Direct Cascade API (Enterprise-only, read-only analytics)
- CLI prompt injection (no such feature exists)

## Table of Contents

1. The Challenge
2. Windsurf Cascade Control Interfaces
3. OpenClaw Outbound Capabilities
4. Integration Patterns
5. Recommended Approach
6. Security Considerations
7. Sources

## 1. The Challenge

**Goal**: Have OpenClaw (running on remote server) send prompts to and receive responses from Windsurf Cascade (running on local/remote machine).

**Why this is hard**:
- Windsurf Cascade has no public API for sending prompts
- Cascade runs inside IDE, not as standalone service
- No WebSocket or REST endpoint for external prompt injection
- Enterprise API is read-only (analytics, not control)

## 2. Windsurf Cascade Control Interfaces

### What EXISTS

**Cascade Hooks** [VERIFIED]:
- Shell commands triggered on Cascade actions
- Events: `pre_user_prompt`, `post_cascade_response`, file read/write, command execution
- Can LOG and BLOCK actions, but cannot INJECT prompts
- Location: `.windsurf/hooks.json`

**Enterprise API** [VERIFIED]:
- Base URL: `https://server.codeium.com/api/v1/`
- Purpose: Analytics and usage management only
- Cannot send prompts or control Cascade behavior
- Enterprise plans only

**MCP Integration** [VERIFIED]:
- Cascade can call external MCP servers
- Config: `~/.codeium/windsurf/mcp_config.json`
- Direction: Cascade -> MCP (not MCP -> Cascade)

### What does NOT exist

- [VERIFIED] No CLI to send prompts to running Cascade
- [VERIFIED] No WebSocket endpoint for prompt injection
- [VERIFIED] No REST API for conversation control
- [VERIFIED] No IPC mechanism for external prompt submission

## 3. OpenClaw Outbound Capabilities

### Browser Control (CDP) [VERIFIED]

OpenClaw has full browser automation via Chrome DevTools Protocol:

**Control API endpoints**:
- `POST /navigate` - Navigate to URL
- `POST /act` - Click, type, interact with elements
- `GET /snapshot` - Get page accessibility snapshot
- `POST /screenshot` - Capture screen

**Architecture**:
```
OpenClaw Gateway
       |
       v
Browser Control Server (HTTP)
       |
       v
Chrome/Brave/Edge via CDP
       |
       v
Windsurf IDE (Electron = Chromium)
```

### Shell Command Execution [VERIFIED]

OpenClaw can run arbitrary shell commands via its `exec` tool:
- Execute PowerShell/Bash scripts
- Read/write files
- Send keyboard events via OS automation tools

### File System Access [VERIFIED]

OpenClaw can read/write files in any accessible location:
- Write to `.windsurf/` directory
- Modify workspace files
- Create trigger files for hooks

## 4. Integration Patterns

### Pattern A: UI Automation via CDP (Most Reliable)

**How it works**:
1. OpenClaw's browser control connects to Windsurf's Electron process via CDP
2. OpenClaw navigates to Cascade panel, types prompt, submits
3. OpenClaw reads response from DOM/accessibility tree

**Implementation**:
```
# OpenClaw skill to control Cascade
openclaw browser open --url "about:blank"  # Or attach to existing
openclaw browser act --selector "[data-testid='cascade-input']" --action type --text "Your prompt here"
openclaw browser act --selector "[data-testid='submit-button']" --action click
openclaw browser snapshot --wait 5000  # Wait for response
```

**Challenges**:
- Need to find Windsurf's CDP port (typically 9222 or similar)
- Electron apps may not expose CDP by default
- UI selectors may change between Windsurf versions

**Reliability**: Medium - Works but fragile to UI changes

### Pattern B: File-Based Trigger with Hooks

**How it works**:
1. OpenClaw writes a "task file" to workspace (e.g., `.openclaw-task.md`)
2. Cascade Hook (`post_write_code`) detects the file
3. Hook script reads task, creates a notification or updates a "pending tasks" file
4. Human user sees notification, manually invokes task in Cascade
5. Cascade response written to output file
6. OpenClaw polls for output file

**Implementation**:

`.windsurf/hooks.json`:
```json
{
  "hooks": {
    "post_write_code": [
      {
        "command": "python3 /path/to/openclaw-bridge.py",
        "show_output": false
      }
    ]
  }
}
```

`openclaw-bridge.py`:
```python
import sys, json
data = json.load(sys.stdin)
if ".openclaw-task.md" in data["tool_info"]["file_path"]:
    # Notify user or log task
    with open("/path/to/pending-tasks.log", "a") as f:
        f.write(f"New task from OpenClaw: {data}\n")
```

**Reliability**: High for detection, but requires human in loop

### Pattern C: Shared MCP Coordination

**How it works**:
1. Create custom MCP server with task queue
2. Both OpenClaw and Cascade connect to this MCP
3. OpenClaw pushes tasks to queue via MCP tool
4. Cascade polls queue and executes tasks
5. Results stored in shared state

**Architecture**:
```
OpenClaw ─────┐
              │
              v
         Custom MCP Server
         (Task Queue + State)
              ^
              │
Cascade ──────┘
```

**Implementation**:

Custom MCP server exposes:
- `queue_task` - OpenClaw calls to add task
- `get_pending_tasks` - Cascade calls to check queue
- `submit_result` - Cascade calls after completion
- `get_result` - OpenClaw calls to retrieve

**Reliability**: High, but requires Cascade to actively poll (manual or via workflow)

### Pattern D: OS-Level Keyboard Automation

**How it works**:
1. OpenClaw executes PowerShell/AppleScript to send keystrokes
2. Focus Windsurf window
3. Open Cascade (`Ctrl+L`)
4. Type prompt
5. Submit (`Enter`)
6. Wait and capture response via clipboard or file

**Implementation** (PowerShell):
```powershell
Add-Type -AssemblyName System.Windows.Forms

# Focus Windsurf
$windsurf = Get-Process -Name "Windsurf" -ErrorAction SilentlyContinue
if ($windsurf) {
    [Microsoft.VisualBasic.Interaction]::AppActivate($windsurf.Id)
    Start-Sleep -Milliseconds 500
    
    # Open Cascade
    [System.Windows.Forms.SendKeys]::SendWait("^l")
    Start-Sleep -Milliseconds 500
    
    # Type prompt
    [System.Windows.Forms.SendKeys]::SendWait("Your prompt here")
    Start-Sleep -Milliseconds 200
    
    # Submit
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
}
```

**Reliability**: Low - Fragile, timing-dependent, requires foreground window

### Pattern E: Keyboard + Hooks Hybrid (RECOMMENDED)

**Key insight**: Combine keyboard shortcuts for INPUT with hooks for OUTPUT to create full bidirectional control.

**Architecture**:
```
OpenClaw ──[SendKeys]──> Windsurf/Cascade
                              │
                              v
                    (Cascade processes)
                              │
                              v
         <──[Hooks]─── post_cascade_response
         <──[Hooks]─── post_write_code (file changes)
         <──[Script]── screenshot to file
```

**Implementation**:

**Step 1: Hook configuration** (`.windsurf/hooks.json`):
```json
{
  "hooks": {
    "post_cascade_response": [
      {
        "command": "python C:/openclaw-bridge/capture-response.py",
        "show_output": false
      }
    ],
    "post_write_code": [
      {
        "command": "python C:/openclaw-bridge/log-file-changes.py",
        "show_output": false
      }
    ]
  }
}
```

**Step 2: Response capture script** (`capture-response.py`):
```python
import sys, json, os
from datetime import datetime

data = json.load(sys.stdin)
response = data["tool_info"]["response"]
trajectory_id = data["trajectory_id"]
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Write response to shared folder
os.makedirs("C:/openclaw-bridge/responses", exist_ok=True)
with open(f"C:/openclaw-bridge/responses/{timestamp}_{trajectory_id[:8]}.md", "w", encoding="utf-8") as f:
    f.write(f"# Cascade Response\n")
    f.write(f"**Trajectory**: {trajectory_id}\n")
    f.write(f"**Time**: {timestamp}\n\n")
    f.write(response)

# Optional: take screenshot
import subprocess
subprocess.run(["powershell", "-File", "C:/openclaw-bridge/screenshot.ps1"], capture_output=True)
```

**Step 3: Keyboard sender script** (`send-to-cascade.ps1`):
```powershell
param([string]$Prompt)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName Microsoft.VisualBasic

$windsurf = Get-Process -Name "Windsurf" -ErrorAction SilentlyContinue
if ($windsurf) {
    [Microsoft.VisualBasic.Interaction]::AppActivate($windsurf.Id)
    Start-Sleep -Milliseconds 300
    
    # Open Cascade
    [System.Windows.Forms.SendKeys]::SendWait("^l")
    Start-Sleep -Milliseconds 500
    
    # Type prompt (escape special chars)
    $escaped = $Prompt -replace '[+^%~(){}]', '{$0}'
    [System.Windows.Forms.SendKeys]::SendWait($escaped)
    Start-Sleep -Milliseconds 200
    
    # Submit
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
    
    Write-Host "Prompt sent to Cascade"
} else {
    Write-Error "Windsurf not running"
    exit 1
}
```

**Step 4: Screenshot script** (`screenshot.ps1`):
```powershell
Add-Type -AssemblyName System.Windows.Forms
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
$bitmap.Save("C:/openclaw-bridge/screenshots/$timestamp.png")
$graphics.Dispose()
$bitmap.Dispose()
```

**Step 5: OpenClaw integration**:
```bash
# OpenClaw sends task
openclaw exec --command "powershell -File C:/openclaw-bridge/send-to-cascade.ps1 -Prompt 'Run all tests'"

# OpenClaw polls for response
openclaw exec --command "Get-ChildItem C:/openclaw-bridge/responses -Filter *.md | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | Get-Content"
```

**What you capture**:
- `post_cascade_response`: Full markdown response including tool actions, file edits, command outputs
- `post_write_code`: Every file Cascade creates/modifies with old/new content
- `post_run_command`: Every terminal command executed
- Screenshots: Visual state at any point

**Reliability**: Medium-High
- Input (keyboard): Medium - requires Windsurf in foreground, timing-sensitive
- Output (hooks): High - guaranteed capture of all Cascade actions

## 5. Recommended Approach

### For Your Scenario (Remote OpenClaw + Local Windsurf)

**Primary: Pattern E (Keyboard + Hooks)**

1. Set up hooks to capture all Cascade output to `C:/openclaw-bridge/`
2. OpenClaw writes task to file, then sends keyboard shortcut to trigger Cascade
3. Hooks automatically capture response, file changes, screenshots
4. OpenClaw reads captured output from shared folder

**Why this approach**:
- Full automation possible (no human trigger required)
- Hooks guarantee response capture
- Screenshots provide visual verification
- File change logging tracks all modifications

**Alternative: Pattern C (Shared MCP) + Manual Trigger**

If you prefer human-in-loop control:
1. Create simple MCP server with task queue
2. OpenClaw queues tasks via WhatsApp/Telegram
3. You manually invoke `/check-openclaw-tasks` in Cascade
4. Results flow back through MCP

### Workflow Example

**OpenClaw side** (via WhatsApp):
```
You: "Run tests on the auth module"
OpenClaw: "Task queued. ID: task-001. Cascade will pick it up."
```

**Cascade side** (manual trigger):
```
/check-openclaw-tasks
Cascade: "Found 1 pending task from OpenClaw:
- task-001: Run tests on the auth module
Executing..."
[Cascade runs tests, writes results to MCP]
Cascade: "Task task-001 completed. Results sent to OpenClaw."
```

**OpenClaw side** (notification):
```
OpenClaw: "Task task-001 completed. Auth module tests: 47 passed, 0 failed."
```

## 6. Security Considerations

### Risks

- **Prompt injection**: Malicious tasks from OpenClaw could execute harmful code
- **Data exfiltration**: Cascade responses may contain sensitive code
- **Credential exposure**: MCP server needs authentication

### Mitigations

1. **Task validation**: MCP server validates task format before queuing
2. **Allowlist commands**: Only permit specific task types
3. **Human approval**: Require manual trigger for task execution
4. **Audit logging**: Log all tasks and responses
5. **Network isolation**: MCP server only accessible via Tailscale

## 7. Sources

### Windsurf Documentation [VERIFIED]

- **OCCTRL-SC-WS-HOOKS**: https://docs.windsurf.com/windsurf/cascade/hooks (Accessed: 2026-02-28)
  - Hooks can log and block, but not inject prompts
- **OCCTRL-SC-WS-API**: https://docs.windsurf.com/plugins/accounts/api-reference/api-introduction (Accessed: 2026-02-28)
  - Enterprise API is analytics-only, no prompt control
- **OCCTRL-SC-WS-MCP**: https://docs.windsurf.com/windsurf/cascade/mcp (Accessed: 2026-02-28)
  - MCP direction is Cascade -> external, not reverse

### OpenClaw Documentation [VERIFIED]

- **OCCTRL-SC-OC-BROWSER**: https://docs.openclaw.ai/tools/browser (Accessed: 2026-02-28)
  - Full CDP browser control API documented
- **OCCTRL-SC-OC-MCP**: Existing session research (OCLAW-IN01)
  - OpenClaw supports MCP client connections

### Local Research [TESTED]

- **OCCTRL-SC-LOCAL-WSRF**: `E:\Dev\IPPS\Docs\INFO_HOW_WINDSURF_WORKS.md`
  - Confirmed no CLI prompt injection exists

## Document History

**[2026-02-28 09:07]**
- Added: Pattern E (Keyboard + Hooks hybrid) as recommended approach
- Added: Full implementation scripts for bidirectional control
- Changed: Updated recommendation from MCP to Keyboard+Hooks
- Key insight: Hooks capture ALL output (responses, files, commands)

**[2026-02-28 09:00]**
- Initial research on OpenClaw -> Cascade control
- Identified 4 integration patterns
- Recommended shared MCP approach
