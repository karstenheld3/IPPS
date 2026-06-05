# SPEC: xlwings Excel Skill for Windsurf Cascade

**Doc ID**: AXCEL-SP01
**Feature**: XLWINGS_SKILL
**Goal**: Specify a Python-based xlwings skill providing fast Excel automation for the Windsurf Cascade agent
**Timeline**: Created 2026-02-27
**Target file**: `.windsurf/skills/agent-excel/`

**Depends on:**
- `_INFO_AXCEL-IN14_XLWINGS.md [AXCEL-IN14]` for xlwings API and server implementation
- `_INFO_AXCEL-IN12_VBAMANIP.md [AXCEL-IN12]` for VBA export/import implementation
- `_INFO_AXCEL-IN11_REMOTECONTROL.md [AXCEL-IN11]` for remote control patterns

## MUST-NOT-FORGET

- xlwings is NOT thread-safe - Flask server MUST use `threaded=False`
- VBA manipulation requires "Trust access to the VBA project object model" enabled in Excel
- Document modules (Sheet, ThisWorkbook) cannot be imported/exported directly - only code extraction
- Server binds to 127.0.0.1 only (localhost) - no external access
- Lazy connection: Server starts without Excel, connects on first request
- Validate COM connection before each request - Excel may crash or close
- Request timeout: 30 seconds to prevent indefinite hangs on modal dialogs
- Workbook name ambiguity: Error when multiple workbooks match same name
- CSV export uses UTF-8 encoding explicitly

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
10. [Implementation Details](#10-implementation-details)
11. [Document History](#11-document-history)

## 1. Scenario

**Problem:** The Windsurf Cascade agent needs fast, programmatic access to Excel workbooks for an end-to-end agent-based Excel solution development cycle. Current PowerShell-based approach has 250-550ms latency per operation due to process startup and COM initialization overhead. This breaks the conversational flow when the agent needs to explore ideas, get feedback, and iterate quickly.

**Solution:**
- Python-based HTTP server using xlwings with persistent COM connection
- REST API endpoints for all Excel operations (read, write, navigate, calculate, VBA)
- 3-10x faster response times (20-100ms vs 250-550ms)
- Startup/shutdown scripts for easy server management
- Fallback PowerShell scripts when server is not running

**What we don't want:**
- Complex installation requirements (no VSTO, no add-ins)
- Threading issues (no multi-threaded Flask)
- Hardcoded paths or workbook names
- Cryptic COM error messages (provide clear feedback)
- Server that requires Excel to be running before startup (use lazy connection)
- Indefinite hangs when Excel shows modal dialogs (use timeouts)
- Silent wrong workbook selection when same name in multiple instances

## 2. Context

This skill is part of the Agent Excel Skill research session (`_2026-02-27_AgentExcelSkill`). The xlwings approach was selected after evaluating three options:
- Option 1: PowerShell scripts (simple but slow, 250-550ms)
- Option 2: VSTO Add-In (fast but complex installation)
- Option 3: xlwings Python Server (balanced - fast, minimal installation)

The skill enables five core use cases from the session requirements:
- UC-1: Export Excel workbooks as CSV
- UC-2: Write into Excel workbooks (data and formulas)
- UC-3: Remote control Excel workbooks (navigate, calculate)
- UC-4: Export VBA code from XLSM files
- UC-5: Add/update VBA code in Excel workbooks

## 3. Domain Objects

### ExcelServer

The **ExcelServer** is a Flask HTTP server that maintains a persistent COM connection to Excel via xlwings.

**Location:** `.windsurf/skills/agent-excel/excel_server.py`
**Port:** 5001 (configurable)
**Binding:** 127.0.0.1 (localhost only)

**Key properties:**
- `port` - HTTP port (default: 5001)
- `threaded` - Must be False (xlwings is not thread-safe)

### Workbook

A **Workbook** represents an open Excel workbook in the user's Excel instance.

**Identification:** By name (`Budget.xlsx`) or full path (`C:\Users\...\Budget.xlsx`)

**Key properties:**
- `name` - Filename without path
- `fullname` - Full absolute path
- `pid` - Process ID of Excel instance

### Sheet

A **Sheet** represents a worksheet within a workbook.

**Identification:** By name (`Sheet1`) or 0-based index (`0`)

**Key properties:**
- `name` - Sheet name
- `index` - 0-based position

### Range

A **Range** represents a cell or cell range in a worksheet.

**Identification:** A1 notation (`A1`, `A1:C10`) or R1C1 notation

**Key properties:**
- `address` - A1 address with $ anchors
- `value` - Cell value(s) - scalar or 2D array
- `formula` - Cell formula(s) - scalar or 2D array

### VBAComponent

A **VBAComponent** represents a VBA module, class, or form in a workbook's VBProject.

**Location:** Workbook VBProject
**Types:** Standard module (.bas), Class module (.cls), UserForm (.frm), Document module (Sheet/ThisWorkbook)

**Key properties:**
- `name` - Component name
- `type` - Component type (1=Module, 2=Class, 3=Form, 100=Document)
- `code` - Source code content
- `line_count` - Number of code lines

## 4. Functional Requirements

**AXCEL-FR-01: Server Lifecycle Management**
- Start server with `start-server.ps1` script
- Stop server with `stop-server.ps1` script
- Store PID in `.server.pid` file for process tracking
- Detect if server already running before starting
- `start-server.ps1` validates PID is alive (not just file exists) - removes stale PID file
- `stop-server.ps1` attempts graceful stop, force-kills after 5 seconds if still running
- Health check endpoint at `/health` returns server version and Excel connection status
- Server starts without Excel (lazy connection) - connects on first request
- Request timeout: 30 seconds per request to prevent indefinite hangs

**AXCEL-FR-02: List Open Workbooks**
- Endpoint: `GET /books`
- Return all open workbooks across all Excel instances
- Include name, fullname, and Excel PID for each
- Return empty list with warning if Excel not running

**AXCEL-FR-03: Read Cell Range**
- Endpoint: `POST /read`
- Parameters: workbook (optional), sheet (optional), range (required), pid (optional)
- Return value, formula, and address
- Support A1 notation for range specification
- Default to active workbook/sheet if not specified
- Error if workbook name matches multiple files (require full path or pid)
- Values reflect current calculation state (may be stale if calculation mode is manual)

**AXCEL-FR-04: Write Cell Value**
- Endpoint: `POST /write`
- Parameters: workbook (optional), sheet (optional), range (required), value (optional), formula (optional)
- Write value or formula to specified range
- Support scalar values and 2D arrays
- Return success status and written address

**AXCEL-FR-05: Navigate to Cell**
- Endpoint: `POST /navigate`
- Parameters: workbook (optional), sheet (optional), range (required)
- Activate sheet and select range
- Bring cell into view for user

**AXCEL-FR-06: Trigger Calculation**
- Endpoint: `POST /calculate`
- Parameters: workbook (optional)
- Calculate specified workbook or all open workbooks
- Return success status

**AXCEL-FR-07: Export to CSV**
- Endpoint: `POST /export-csv`
- Parameters: workbook (required), output_folder (required), sheets (optional, default: all), encoding (optional, default: utf-8)
- Export specified sheets or all sheets to CSV files
- One CSV per sheet, named `{workbook}_{sheet}.csv`
- UTF-8 encoding by default (explicit, not locale-dependent)
- Return list of exported files

**AXCEL-FR-08: Export VBA Code**
- Endpoint: `POST /vba/export`
- Parameters: workbook (required), output_folder (required)
- Export all VBA components to files (.bas, .cls, .frm)
- Skip empty components (no code)
- Document modules (Sheet, ThisWorkbook): Export code content only (cannot be reimported as modules)
- Return list of exported files with component types

**AXCEL-FR-09: Import VBA Module**
- Endpoint: `POST /vba/import`
- Parameters: workbook (required), file_path (required)
- Import .bas, .cls, or .frm file into workbook
- Replace existing component with same name
- Skip document modules (Sheet, ThisWorkbook) with warning - cannot be imported
- Return success status and component name

**AXCEL-FR-10: Read VBA Code**
- Endpoint: `POST /vba/read`
- Parameters: workbook (required), component (required)
- Return source code of specified VBA component
- Include component name, type, and line count

**AXCEL-FR-11: List VBA Components**
- Endpoint: `POST /vba/list`
- Parameters: workbook (required)
- Return list of all VBA components
- Include name, type, and line count for each

**AXCEL-FR-12: Error Handling**
- All endpoints return JSON with `error` field on failure
- Validate COM connection before each request - detect Excel crash/close
- Provide clear error messages (not raw COM exceptions)
- HTTP 400 for client errors, HTTP 500 for server errors
- Specific errors: "Excel not running", "Workbook not found", "Multiple workbooks match - specify full path or pid"

**AXCEL-FR-13: VBA Trust Status**
- Endpoint: `GET /vba/status`
- Check if "Trust access to VBA project object model" is enabled
- Return trust status before attempting VBA operations
- Provide guidance on enabling if disabled

## 5. Design Decisions

**AXCEL-DD-01:** Use Flask with `threaded=False`. Rationale: xlwings wraps COM which is apartment-threaded; concurrent requests cause crashes.

**AXCEL-DD-02:** Bind to 127.0.0.1 only. Rationale: Security - no external network access needed for agent use case.

**AXCEL-DD-03:** Use port 5001 (not 5000). Rationale: Port 5000 often conflicts with other services (e.g., AirPlay on macOS).

**AXCEL-DD-04:** Default to active workbook/sheet. Rationale: Most agent operations target what user is currently viewing; reduces parameter verbosity.

**AXCEL-DD-05:** Store server PID in `.server.pid`. Rationale: Enables reliable process management without port scanning.

**AXCEL-DD-06:** Use POST for all operations except list/health. Rationale: Operations may have side effects; POST semantics are clearer.

**AXCEL-DD-07:** Return both value and formula for reads. Rationale: Agent often needs to see both the result and the calculation logic.

**AXCEL-DD-08:** Separate VBA export/import from read/write. Rationale: VBA operations are distinct from cell operations and require different security settings.

**AXCEL-DD-09:** Lazy connection - server starts without Excel. Rationale: Avoids startup race condition; user can start Excel after server.

**AXCEL-DD-10:** 30-second request timeout. Rationale: Prevents indefinite hangs when Excel shows modal dialogs.

**AXCEL-DD-11:** Error on multiple workbook name matches. Rationale: Silent wrong workbook selection is worse than explicit error.

## 6. Implementation Guarantees

**AXCEL-IG-01:** Server starts successfully without Excel running - connects lazily on first request.

**AXCEL-IG-02:** All REST responses are valid JSON with consistent structure.

**AXCEL-IG-03:** COM errors are caught and translated to user-friendly messages.

**AXCEL-IG-04:** Server cleanup is handled properly - no orphan processes.

**AXCEL-IG-05:** VBA operations fail gracefully if "Trust access to VBA project" is disabled.

**AXCEL-IG-06:** COM connection validated before each request - detects Excel crash/close with clear error.

**AXCEL-IG-07:** Request timeout of 30 seconds prevents indefinite hangs.

## 7. Key Mechanisms

### Lazy COM Connection

The server uses lazy connection - starts without Excel and connects on first request. Connection is validated before each request to detect Excel crash/close.

```python
import xlwings as xw

def ensure_excel_connection():
    """Validate Excel is running and accessible."""
    if not xw.apps.keys():
        raise Exception("Excel not running. Please open Excel first.")
    # Test connection with simple operation
    try:
        _ = xw.apps.active.visible
    except Exception:
        raise Exception("Excel connection lost. Please restart server.")
```

### Request Timeout

All requests have a 30-second timeout to prevent indefinite hangs when Excel shows modal dialogs (save prompts, error dialogs).

**Known limitation**: If Excel is in modal state (showing dialog), COM calls block until user dismisses dialog. Timeout ensures server remains responsive.

### Excel Instance Discovery

xlwings provides access to all running Excel instances via `xw.apps.keys()` which returns PIDs. The server can enumerate all workbooks across all instances:

```python
for pid in xw.apps.keys():
    app = xw.apps[pid]
    for book in app.books:
        # Access workbook
```

### VBA Trust Check

VBA operations require the "Trust access to VBA project object model" setting. The server catches the COM error and provides a helpful message:

```python
try:
    workbook.VBProject.VBComponents
except Exception as e:
    if "programmatic access" in str(e).lower():
        raise Exception("Enable 'Trust access to VBA project object model' in Excel Trust Center")
```

## 8. Action Flow

### Agent reads cell value

```
Agent calls: Invoke-RestMethod -Uri "http://localhost:5001/read" -Method Post -Body '{"range":"A1:B2"}'
├─> Flask receives POST /read
│   ├─> get_book() - find workbook (active if not specified)
│   │   ├─> Check xw.apps.keys() - Excel running?
│   │   └─> Return xw.books.active or xw.Book(name)
│   ├─> get_sheet() - find sheet (active if not specified)
│   ├─> sheet.range(data['range']) - get Range object
│   └─> Return JSON: {value, formula, address}
└─> Agent receives: {"range":"A1:B2", "value":[[1,2],[3,4]], "formula":[["1","2"],["3","4"]], "address":"$A$1:$B$2"}
```

### Agent exports VBA code

```
Agent calls: Invoke-RestMethod -Uri "http://localhost:5001/vba/export" -Method Post -Body '{"workbook":"Budget.xlsm","output_folder":"C:/temp/vba"}'
├─> Flask receives POST /vba/export
│   ├─> get_book('Budget.xlsm') - find workbook
│   ├─> Access workbook.api.VBProject.VBComponents
│   │   └─> On error: Return helpful message about Trust settings
│   ├─> For each component with code:
│   │   ├─> Determine extension (.bas, .cls, .frm)
│   │   └─> component.Export(path)
│   └─> Return JSON: {files: [{name, type, path}, ...]}
└─> Agent receives: {"files":[{"name":"Module1","type":"module","path":"C:/temp/vba/Module1.bas"},...]}
```

## 9. Data Structures

### Health Check Response

```json
{"status": "ok", "excel_instances": [10559, 12340]}
```

### List Books Response

```json
{
  "books": [
    {"name": "Budget.xlsx", "fullname": "C:\\Users\\User\\Budget.xlsx", "pid": 10559},
    {"name": "Report.xlsm", "fullname": "C:\\Users\\User\\Report.xlsm", "pid": 10559}
  ]
}
```

### Read Range Request/Response

```json
// Request
{"workbook": "Budget.xlsx", "sheet": "Q1", "range": "A1:C3"}

// Response
{
  "range": "A1:C3",
  "value": [["Item", "Q1", "Q2"], ["Sales", 1000, 1200], ["Cost", 800, 850]],
  "formula": [["Item", "Q1", "Q2"], ["Sales", "1000", "1200"], ["Cost", "800", "850"]],
  "address": "$A$1:$C$3"
}
```

### Write Range Request/Response

```json
// Request - write value
{"range": "A1", "value": "Hello"}

// Request - write formula
{"range": "B1", "formula": "=SUM(A1:A10)"}

// Request - write 2D array
{"range": "A1", "value": [["Name", "Score"], ["Alice", 95], ["Bob", 87]]}

// Response
{"success": true, "address": "$A$1"}
```

### Export CSV Request/Response

```json
// Request
{"workbook": "Budget.xlsx", "output_folder": "C:\\temp\\csv"}

// Response
{
  "success": true,
  "files": [
    {"sheet": "Q1", "path": "C:\\temp\\csv\\Budget_Q1.csv"},
    {"sheet": "Q2", "path": "C:\\temp\\csv\\Budget_Q2.csv"}
  ]
}
```

### VBA Export Request/Response

```json
// Request
{"workbook": "Report.xlsm", "output_folder": "C:\\temp\\vba"}

// Response
{
  "success": true,
  "files": [
    {"name": "Module1", "type": "module", "extension": ".bas", "path": "C:\\temp\\vba\\Module1.bas"},
    {"name": "Sheet1", "type": "document", "extension": ".cls", "path": "C:\\temp\\vba\\Sheet1.cls"}
  ]
}
```

### VBA List Response

```json
{
  "components": [
    {"name": "Module1", "type": "module", "type_id": 1, "lines": 45},
    {"name": "ClassHelper", "type": "class", "type_id": 2, "lines": 120},
    {"name": "Sheet1", "type": "document", "type_id": 100, "lines": 10},
    {"name": "ThisWorkbook", "type": "document", "type_id": 100, "lines": 5}
  ]
}
```

### Error Response

```json
{"error": "Excel not running. Please open Excel first."}
{"error": "Workbook not found: Budget.xlsx"}
{"error": "Enable 'Trust access to VBA project object model' in Excel Trust Center"}
```

## 10. Implementation Details

### File Structure

```
.windsurf/skills/agent-excel/
├── SKILL.md                # Skill documentation for agent
├── SETUP.md                # Installation and setup guide
├── excel_server.py         # Flask server with xlwings
├── start-server.ps1        # Start server script
├── stop-server.ps1         # Stop server script
├── setup-venv.ps1          # Create venv and install dependencies
├── requirements.txt        # Python dependencies
├── .server.pid             # PID file (created at runtime)
└── README.md               # Human-readable usage guide

[WORKSPACE_FOLDER]\..\tools\
└── xlwings-venv/           # Shared Python virtual environment
```

### Server Endpoints Summary

- `GET /health` - Health check, list Excel PIDs
- `GET /books` - List all open workbooks
- `POST /read` - Read cell range (value + formula)
- `POST /write` - Write value or formula to range
- `POST /navigate` - Navigate to cell range
- `POST /calculate` - Trigger workbook calculation
- `POST /export-csv` - Export sheets to CSV files
- `POST /vba/list` - List VBA components
- `POST /vba/read` - Read VBA component code
- `POST /vba/export` - Export all VBA to files
- `POST /vba/import` - Import VBA file

### Dependencies

```
# requirements.txt
xlwings>=0.30.0
flask>=2.0.0
```

### Setup Process

**Virtual environment location**: `[WORKSPACE_FOLDER]\..\tools\xlwings-venv`

`setup-venv.ps1` performs:
1. Check if Python 3.10+ available
2. Create venv at shared `.tools` location (if not exists)
3. Install dependencies from requirements.txt
4. Verify xlwings and flask imports work

`start-server.ps1` activates the venv before launching the server.

**First-time setup**:
```powershell
& "$env:USERPROFILE\.windsurf\skills\agent-excel\setup-venv.ps1"
```

### Agent Usage Examples (SKILL.md content)

```powershell
# Start the Excel server
& "$env:USERPROFILE\.windsurf\skills\agent-excel\start-server.ps1"

# Health check
Invoke-RestMethod -Uri "http://localhost:5001/health"

# List workbooks
Invoke-RestMethod -Uri "http://localhost:5001/books"

# Read cells
$body = @{range='A1:C10'} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5001/read" -Method Post -Body $body -ContentType "application/json"

# Write value
$body = @{range='A1'; value='Hello World'} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5001/write" -Method Post -Body $body -ContentType "application/json"

# Write formula
$body = @{range='B1'; formula='=SUM(A1:A10)'} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5001/write" -Method Post -Body $body -ContentType "application/json"

# Export VBA
$body = @{workbook='Report.xlsm'; output_folder='C:\temp\vba'} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5001/vba/export" -Method Post -Body $body -ContentType "application/json"

# Stop server
& "$env:USERPROFILE\.windsurf\skills\agent-excel\stop-server.ps1"
```

### Known Limitations

- **Sequential requests**: All requests are processed sequentially (xlwings is not thread-safe). Health check blocked during long operations.
- **Modal dialog blocking**: If Excel shows a modal dialog (save prompt, error), COM calls block until user dismisses it. The 30-second timeout returns control to agent but does not cancel the operation.
- **Excel restart**: If user closes and reopens Excel, server auto-reconnects to new instance on next request.

### Agent Recovery Workflow

When a request times out:

```
1. Request times out (30s)
2. Wait 2s, call GET /health with 5s timeout
3. If health responds:
   - Server recovered, verify state with /read before retrying write
4. If health times out:
   - Server stuck on COM call
   - Run stop-server.ps1 (force-kills after 5s)
   - Run start-server.ps1
   - Retry operation
5. If still failing:
   - Inform user: "Excel may be showing a dialog. Please check Excel window."
```

**Read-to-verify pattern**: After write timeout, read the target cell to check if write succeeded before retrying.

## 11. Document History

**[2026-02-28 08:50]**
- Added: SETUP.md to file structure
- Added: setup-venv.ps1 script for venv creation
- Added: Setup Process section (venv at .tools/xlwings-venv)
- Added: requirements.txt to file structure

**[2026-02-28 08:45]**
- Added: Known Limitations section (sequential requests, modal blocking, Excel restart)
- Added: Agent Recovery Workflow section (timeout handling, read-to-verify pattern)
- Changed: AXCEL-FR-01 (PID validation, force-kill on stop)
- Review: Robustness critique findings addressed (4 of 8 confirmed, implemented)

**[2026-02-27 17:00]**
- Added: AXCEL-FR-13 (VBA Trust Status endpoint)
- Added: AXCEL-DD-09 to DD-11 (lazy connection, timeout, ambiguity handling)
- Added: AXCEL-IG-06 to IG-07 (connection validation, request timeout)
- Changed: AXCEL-FR-01 (lazy connection, timeout)
- Changed: AXCEL-FR-03 (pid parameter, ambiguity error)
- Changed: AXCEL-FR-07 (explicit UTF-8 encoding)
- Changed: AXCEL-FR-08/09 (document module behavior clarified)
- Changed: AXCEL-IG-01 (lazy connection instead of fail-on-startup)
- Review: `_SPEC_XLWINGS_SKILL_REVIEW.md` findings addressed (11 of 11)

**[2026-02-27 16:45]**
- Initial specification created
- All 5 use cases covered (CSV export, write data, remote control, VBA export, VBA import)
- 12 functional requirements defined
- 8 design decisions documented
