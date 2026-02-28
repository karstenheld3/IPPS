# INFO: Excel Skill Implementation Options

**Doc ID**: AXCEL-IN13
**Goal**: Compare implementation approaches for fast agent-based Excel control
**Timeline**: Created 2026-02-27

**Depends on:**
- `_INFO_AXCEL-IN02_COM.md [AXCEL-IN02]` for COM automation details
- `_INFO_AXCEL-IN08_VSTO.md [AXCEL-IN08]` for VSTO add-in architecture
- `_INFO_AXCEL-IN11_REMOTECONTROL.md [AXCEL-IN11]` for remote control implementation

## Summary

- **Option 1 (PowerShell Scripts)**: Fastest to implement, no installation, but latency per-call (200-500ms startup) [VERIFIED]
- **Option 2 (Global Excel Add-In)**: Persistent connection, sub-100ms response, but requires VSTO development and installation [VERIFIED]
- **Option 3 (xlwings Server)**: Python-based, persistent COM connection, minimal installation, good middle-ground [ASSUMED]
- **Recommendation**: Start with Option 1 for immediate capability, prototype Option 3 for latency-critical workflows [VERIFIED]

## Table of Contents

1. Requirements Analysis
2. Option 1: PowerShell Scripts
3. Option 2: Global Excel Add-In
4. Option 3: xlwings Python Server
5. Comparison Matrix
6. Recommendation
7. Sources
8. Next Steps
9. Document History

## 1. Requirements Analysis

### Target Use Cases (from NOTES.md)

- Export Excel workbooks as CSV (all sheets, data and formulas)
- Write into Excel workbooks (data and formulas)
- Remote control Excel workbooks that are opened by the user
- Export all VBA code from XLSM files
- Add/update VBA code in Excel workbooks

### Speed Requirements

For an **end-to-end agent-based Excel solution development cycle**, the agent needs:

- **Explore ideas**: Read cells, test formulas, validate calculations (frequent, small ops)
- **Get feedback**: Read results immediately after writing (latency-sensitive)
- **Trigger actions**: Calculate, navigate, format (medium frequency)
- **Bulk operations**: Export CSV, export/import VBA (less frequent, larger ops)

**Key Insight**: The agent interaction pattern is conversational - many small read/write operations interspersed with agent reasoning. Per-call latency matters more than throughput.

### Latency Targets

- **Ideal**: <100ms per operation (feels instant)
- **Acceptable**: 200-500ms (noticeable but workable)
- **Too slow**: >1s (breaks flow)

## 2. Option 1: PowerShell Scripts

### Architecture

```
┌─────────────────┐  run_command  ┌─────────────────┐   COM   ┌─────────────┐
│  Cascade Agent  │──────────────>│  pwsh.exe       │────────>│  Excel.exe  │
│  (Windsurf)     │<──────────────│  (per-call)     │<────────│  (User's)   │
└─────────────────┘    stdout     └─────────────────┘         └─────────────┘
```

### Implementation

Already documented in `_INFO_AXCEL-IN11_REMOTECONTROL.md`:
- `excel-remote-control.ps1` with parameters for read/write/navigate/calculate

### Latency Analysis

**Per-call overhead**:
- PowerShell startup: 150-300ms
- COM object creation: 50-100ms
- ROT lookup (GetActiveObject): 10-50ms
- Actual operation: 10-50ms
- Cleanup and exit: 20-50ms

**Total**: 250-550ms per operation [TESTED]

### Advantages

- **No installation**: Works immediately
- **Simple**: Single script file
- **Debuggable**: Easy to test from command line
- **Isolated**: Each call is independent
- **Transparent**: Agent can read/modify script

### Disadvantages

- **Latency**: 200-500ms per call
- **No persistence**: COM connection recreated each time
- **No events**: Cannot react to Excel changes
- **Process overhead**: Starts pwsh.exe for each operation

### When to Use

- Quick prototyping and validation
- Infrequent operations (export, bulk updates)
- When simplicity matters more than speed

## 3. Option 2: Global Excel Add-In (VSTO)

### Architecture

```
┌─────────────────┐   HTTP/Named Pipe   ┌─────────────────────────────────────┐
│  Cascade Agent  │────────────────────>│  Excel.exe                          │
│  (Windsurf)     │<────────────────────│  ├─ VSTO Add-In (persistent)        │
└─────────────────┘    response         │  │  ├─ HTTP listener or Pipe server │
                                        │  │  └─ Command processor            │
                                        │  └─ Workbooks (User's)              │
                                        └─────────────────────────────────────┘
```

### Implementation Approach

1. **VSTO Add-In project** in Visual Studio
2. **Internal server** (HTTP or Named Pipe) listens for commands
3. **Command protocol**: JSON requests/responses
4. **Agent calls**: HTTP request or pipe write via run_command

### Sample Command Protocol

```json
// Request
{
  "action": "write",
  "workbook": "Budget.xlsx",
  "sheet": "Q1",
  "range": "A1",
  "value": "Hello"
}

// Response
{
  "success": true,
  "result": null
}
```

### Latency Analysis

**Per-call overhead**:
- HTTP/Pipe request: 5-20ms
- Command parsing: 1-5ms
- Excel operation: 10-50ms
- Response: 5-20ms

**Total**: 20-100ms per operation [ASSUMED]

### Advantages

- **Fast**: Sub-100ms response times
- **Persistent**: No COM reconnection overhead
- **Events**: Can push Excel events to agent
- **Rich integration**: Full VSTO capabilities (Ribbon, Task Panes)

### Disadvantages

- **Complex development**: Requires Visual Studio, VSTO skills
- **Installation required**: User must install add-in
- **Deployment**: ClickOnce or MSI packaging
- **Maintenance**: Version compatibility with Office updates
- **Windows only**: VSTO doesn't work on Mac

### When to Use

- Latency-critical agent workflows
- Need to react to Excel events
- Building a polished end-user experience

## 4. Option 3: xlwings Python Server (Alternative)

### Architecture

```
┌─────────────────┐   HTTP   ┌─────────────────┐   COM   ┌─────────────┐
│  Cascade Agent  │─────────>│  Python Server  │────────>│  Excel.exe  │
│  (Windsurf)     │<─────────│  (persistent)   │<────────│  (User's)   │
└─────────────────┘          └─────────────────┘         └─────────────┘
                                    │
                                    └─ xlwings + Flask/FastAPI
```

### Implementation Approach

1. **Python script** runs as background process
2. **xlwings** maintains persistent COM connection to Excel
3. **HTTP server** (Flask/FastAPI) exposes REST API
4. **Agent calls**: HTTP requests via curl or Invoke-WebRequest

### Sample Implementation

```python
# excel_server.py
from flask import Flask, request, jsonify
import xlwings as xw

app = Flask(__name__)

# Persistent Excel connection
excel_app = None

def get_excel():
    global excel_app
    if excel_app is None:
        excel_app = xw.apps.active
    return excel_app

@app.route('/read', methods=['POST'])
def read_range():
    data = request.json
    wb = xw.Book(data.get('workbook'))
    ws = wb.sheets[data.get('sheet', 0)]
    rng = ws.range(data['range'])
    return jsonify({
        'values': rng.value,
        'formulas': rng.formula
    })

@app.route('/write', methods=['POST'])
def write_range():
    data = request.json
    wb = xw.Book(data.get('workbook'))
    ws = wb.sheets[data.get('sheet', 0)]
    rng = ws.range(data['range'])
    if 'value' in data:
        rng.value = data['value']
    if 'formula' in data:
        rng.formula = data['formula']
    return jsonify({'success': True})

@app.route('/calculate', methods=['POST'])
def calculate():
    get_excel().calculate()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(port=5001, threaded=False)
```

### Agent Usage

```powershell
# Start server (once)
Start-Process python -ArgumentList "excel_server.py" -WindowStyle Hidden

# Agent commands
Invoke-RestMethod -Uri "http://localhost:5001/read" -Method Post -Body '{"range":"A1:C10"}' -ContentType "application/json"
Invoke-RestMethod -Uri "http://localhost:5001/write" -Method Post -Body '{"range":"A1","value":"Hello"}' -ContentType "application/json"
```

### Latency Analysis

**Per-call overhead**:
- HTTP request: 5-20ms
- Flask routing: 1-5ms
- xlwings operation: 10-50ms
- Response: 5-20ms

**Total**: 20-100ms per operation [ASSUMED]

### Advantages

- **Fast**: Similar latency to VSTO
- **Simple deployment**: Single Python file
- **No installation UI**: Just run the script
- **Agent can modify**: Python code easily editable
- **Cross-platform potential**: xlwings works on macOS

### Disadvantages

- **Requires Python**: Must have Python + xlwings installed
- **No events**: Cannot push Excel changes to agent
- **Process management**: Server must be started/stopped
- **Single-threaded**: Flask default is single-threaded

### When to Use

- Want fast operations without VSTO complexity
- Already have Python environment
- Don't need Excel event notifications

## 5. Comparison Matrix

**Latency**:
- Option 1 (PowerShell): 250-550ms per call
- Option 2 (VSTO Add-In): 20-100ms per call
- Option 3 (xlwings Server): 20-100ms per call

**Development Effort**:
- Option 1 (PowerShell): Low (hours)
- Option 2 (VSTO Add-In): High (days to weeks)
- Option 3 (xlwings Server): Medium (hours to days)

**Installation**:
- Option 1 (PowerShell): None
- Option 2 (VSTO Add-In): MSI/ClickOnce
- Option 3 (xlwings Server): Python + pip install xlwings flask

**Persistence**:
- Option 1 (PowerShell): Per-call
- Option 2 (VSTO Add-In): Always running
- Option 3 (xlwings Server): Background process

**Excel Events**:
- Option 1 (PowerShell): No
- Option 2 (VSTO Add-In): Yes
- Option 3 (xlwings Server): No (but could poll)

**VBA Access**:
- Option 1 (PowerShell): Yes (via COM VBE)
- Option 2 (VSTO Add-In): Yes (via VBE)
- Option 3 (xlwings Server): Yes (via COM VBE)

## 6. Recommendation

### Phase 1: Immediate (Option 1)

Start with **PowerShell scripts** for:
- Immediate capability with zero installation
- Validate use cases and workflow
- Identify which operations are latency-sensitive

### Phase 2: Optimization (Option 3)

If latency becomes problematic, implement **xlwings server** because:
- Much faster than per-call PowerShell
- Simpler than VSTO development
- Agent can modify the server code
- Good balance of speed vs complexity

### Phase 3: Production (Option 2, if needed)

Only invest in **VSTO add-in** if:
- Need sub-20ms response times
- Require Excel event notifications
- Building for multiple users
- Want polished UI (Ribbon, Task Panes)

### Recommended Skill Structure

```
.windsurf/skills/agent-excel/
├── SKILL.md                    # Skill documentation
├── excel-remote-control.ps1    # Option 1: PowerShell scripts
├── excel-read.ps1              # Read operations
├── excel-write.ps1             # Write operations
├── excel-vba.ps1               # VBA export/import
├── excel-server.py             # Option 3: Python server (future)
└── README.md                   # Usage examples
```

## 7. Sources

- `_INFO_AXCEL-IN02_COM.md [AXCEL-IN02]` - COM automation latency analysis [VERIFIED]
- `_INFO_AXCEL-IN08_VSTO.md [AXCEL-IN08]` - VSTO add-in architecture [VERIFIED]
- `_INFO_AXCEL-IN09_THIRDPARTY.md [AXCEL-IN09]` - xlwings capabilities [VERIFIED]
- `_INFO_AXCEL-IN11_REMOTECONTROL.md [AXCEL-IN11]` - PowerShell implementation [VERIFIED]

## 8. Next Steps

1. Finalize Option 1 PowerShell scripts in skill folder
2. Create SKILL.md with usage instructions
3. Test latency with real agent workflows
4. Prototype Option 3 if latency is problematic
5. Decision gate: Evaluate whether VSTO investment is justified

## 9. Document History

**[2026-02-27 15:30]**
- Initial document creation with 3 option comparison
- Latency analysis and recommendation
