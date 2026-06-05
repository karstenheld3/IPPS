# INFO: xlwings Python Excel Automation

**Doc ID**: AXCEL-IN14
**Goal**: Comprehensive documentation of xlwings for agent-based Excel automation with persistent server
**Version Scope**: xlwings 0.33.x / Python 3.9+ (2026-02-27)

**Depends on:**
- `_INFO_AXCEL-IN02_COM.md [AXCEL-IN02]` for underlying COM architecture
- `_INFO_AXCEL-IN09_THIRDPARTY.md [AXCEL-IN09]` for Python library comparison
- `_INFO_AXCEL-IN13_SKILL_OPTIONS.md [AXCEL-IN13]` for skill implementation options

## Summary

- **xlwings** is a BSD-licensed Python library for Excel automation via COM (Windows) and AppleScript (macOS) [VERIFIED]
- **Persistent COM connection**: Maintains connection to Excel, eliminating per-call startup overhead [VERIFIED]
- **REST API built-in**: `xlwings restapi run` exposes workbooks via HTTP endpoints [VERIFIED]
- **Attach to running Excel**: `xw.apps.active` or `xw.Book('filename')` connects to user's open workbooks [VERIFIED]
- **Full object model**: Apps, Books, Sheets, Ranges, Charts, Pictures, Names, Shapes [VERIFIED]
- **Converters**: Native support for pandas DataFrame, NumPy arrays, datetime [VERIFIED]
- **PRO features**: xlwings Server for remote interpreter, Office.js add-ins, Google Sheets support (license required) [VERIFIED]
- **Agent latency**: 20-100ms per operation with persistent connection vs 250-550ms per PowerShell call [ASSUMED]

## Table of Contents

1. Overview
2. Architecture
3. Installation and Setup
4. Core API
5. Connecting to Workbooks
6. Reading and Writing Data
7. Built-in REST API
8. Custom Server Implementation
9. VBA Integration
10. PRO Features (License Required)
11. Limitations and Gotchas
12. Agent Skill Implementation
13. Sources
14. Next Steps
15. Document History

## 1. Overview

xlwings is an open-source Python library that enables bidirectional communication between Python and Excel. It wraps COM automation on Windows and AppleScript on macOS, providing a Pythonic API for Excel manipulation.

### Key Capabilities

- **Scripting**: Automate Excel from Python scripts
- **Macros**: Call Python functions from Excel VBA
- **UDFs**: Create User Defined Functions in Python (Windows only)
- **Jupyter**: Interactive Excel manipulation from notebooks
- **REST API**: Built-in HTTP server for remote access

### Licensing

- **Open Source (BSD)**: Core functionality, COM automation, REST API
- **PRO (Commercial)**: xlwings Server, Office.js add-ins, Google Sheets, Reports

`[VERIFIED] (AXCEL-IN14-SC-XLWNGS-DOCS | https://docs.xlwings.org/)`

## 2. Architecture

### COM-Based Architecture (Windows)

```
┌─────────────────┐     COM      ┌─────────────────┐
│  Python Process │─────────────>│  Excel.exe      │
│  (xlwings)      │<─────────────│  (User's)       │
└─────────────────┘              └─────────────────┘
        │
        └── Persistent connection (no per-call overhead)
```

### Server Architecture (Agent Use Case)

```
┌─────────────────┐   HTTP   ┌─────────────────┐   COM   ┌─────────────────┐
│  Cascade Agent  │─────────>│  Python Server  │────────>│  Excel.exe      │
│  (run_command)  │<─────────│  (xlwings+Flask)│<────────│  (User's)       │
└─────────────────┘          └─────────────────┘         └─────────────────┘
```

### Object Hierarchy

```
xw.apps (Apps)
└── xw.App (single Excel instance)
    └── app.books (Books)
        └── xw.Book (single workbook)
            ├── book.sheets (Sheets)
            │   └── xw.Sheet (single worksheet)
            │       ├── sheet.range() (Range)
            │       ├── sheet.charts (Charts)
            │       ├── sheet.pictures (Pictures)
            │       └── sheet.shapes (Shapes)
            └── book.names (Names)
```

`[VERIFIED] (AXCEL-IN14-SC-XLWNGS-API | https://docs.xlwings.org/en/stable/api.html)`

## 3. Installation and Setup

### Basic Installation

```bash
pip install xlwings
```

### With Optional Dependencies

```bash
# For REST API
pip install xlwings flask

# For DataFrames
pip install xlwings pandas numpy

# For Reports (PRO)
pip install xlwings[reports]
```

### Verify Installation

```python
import xlwings as xw
print(xw.__version__)

# Check for running Excel instances
print(xw.apps.keys())  # Returns PIDs of running Excel instances
```

### Excel Add-in (Optional)

For calling Python from Excel:

```bash
xlwings addin install
```

`[VERIFIED] (AXCEL-IN14-SC-XLWNGS-INST | https://docs.xlwings.org/en/stable/installation.html)`

## 4. Core API

### Apps Collection

```python
import xlwings as xw

# All running Excel instances
xw.apps           # Apps collection
xw.apps.keys()    # PIDs of running instances
xw.apps.active    # Active Excel instance
xw.apps[10559]    # Specific instance by PID

# Create new Excel instance
app = xw.App(visible=True)
app = xw.App(visible=False)  # Hidden

# Context manager (auto-cleanup)
with xw.App() as app:
    wb = app.books.add()
    # ... work with workbook
# Excel closes automatically
```

### App Properties and Methods

```python
app = xw.apps.active

# Properties
app.visible           # True/False
app.screen_updating   # True/False (performance)
app.display_alerts    # True/False (suppress dialogs)
app.calculation       # 'automatic', 'manual', 'semiautomatic'
app.version           # Excel version string
app.pid               # Process ID

# Methods
app.calculate()       # Trigger calculation
app.quit()            # Close Excel (without saving)
app.kill()            # Force kill process
```

### Books Collection

```python
# From active app
xw.books              # Books in active app
xw.books.active       # Active workbook
xw.books.add()        # New workbook
xw.books.open(path)   # Open file

# From specific app
app.books
app.books['Book1']
app.books.open(r'C:\path\to\file.xlsx')
```

### Book Object

```python
# Connect to book
wb = xw.Book('Book1')           # By name (searches all apps)
wb = xw.Book(r'C:\path\file.xlsx')  # By path (opens if needed)

# Properties
wb.name               # Filename
wb.fullname           # Full path
wb.app                # Parent App
wb.sheets             # Sheets collection
wb.names              # Named ranges
wb.selection          # Current selection

# Methods
wb.save()
wb.save(r'C:\path\new.xlsx')
wb.close()
wb.activate()
wb.to_pdf(r'C:\path\output.pdf')
```

### Sheets Collection

```python
wb.sheets             # All sheets
wb.sheets.active      # Active sheet
wb.sheets[0]          # By index (0-based)
wb.sheets['Sheet1']   # By name
wb.sheets.add()       # Add new sheet
wb.sheets.add('NewName', after=wb.sheets[0])
```

### Sheet Object

```python
sheet = wb.sheets.active

# Properties
sheet.name            # Sheet name
sheet.index           # Sheet index
sheet.book            # Parent Book
sheet.cells           # All cells
sheet.used_range      # Used range
sheet.api             # Raw COM object

# Methods
sheet.range('A1')     # Get Range
sheet.range('A1:C10')
sheet.range((1,1))    # Row, Col tuple
sheet.range((1,1), (10,3))  # Start, End tuples
sheet.activate()
sheet.clear()
sheet.clear_contents()
sheet.delete()
sheet.copy(after=sheet)
```

`[VERIFIED] (AXCEL-IN14-SC-XLWNGS-QS | https://docs.xlwings.org/en/stable/quickstart.html)`

## 5. Connecting to Workbooks

### Connect to Running Excel

```python
import xlwings as xw

# Method 1: Active workbook in active Excel
wb = xw.books.active

# Method 2: By name (searches all Excel instances)
wb = xw.Book('Budget.xlsx')

# Method 3: By full path (opens if not open)
wb = xw.Book(r'C:\Users\User\Documents\Budget.xlsx')

# Method 4: Specific Excel instance
app = xw.apps[10559]  # By PID
wb = app.books['Budget.xlsx']
```

### Handle Multiple Excel Instances

```python
# List all running Excel instances
for pid in xw.apps.keys():
    app = xw.apps[pid]
    print(f"PID {pid}: {[b.name for b in app.books]}")

# Connect to specific instance
if 10559 in xw.apps.keys():
    app = xw.apps[10559]
    wb = app.books['MyWorkbook.xlsx']
```

### Create vs Connect Logic

```python
def get_or_create_workbook(path):
    """Connect to open workbook or open it."""
    try:
        # Try to find already open
        return xw.Book(path)
    except Exception:
        # Open it
        return xw.books.open(path)
```

`[VERIFIED] (AXCEL-IN14-SC-XLWNGS-CONN | https://docs.xlwings.org/en/stable/connect_to_workbook.html)`

## 6. Reading and Writing Data

### Basic Read/Write

```python
sheet = xw.books.active.sheets.active

# Single cell
sheet['A1'].value = 'Hello'
value = sheet['A1'].value

# Range
sheet['A1:C3'].value = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
data = sheet['A1:C3'].value  # Returns nested list

# Named range
sheet.range('A1').name = 'MyRange'
sheet['MyRange'].value = 100
```

### Formulas

```python
# Write formula
sheet['B1'].formula = '=SUM(A1:A10)'
sheet['C1'].formula = '=A1*2'

# Read formula
formula = sheet['B1'].formula      # '=SUM(A1:A10)'
formula_r1c1 = sheet['B1'].formula2  # R1C1 format

# Read calculated value
sheet.book.app.calculate()
result = sheet['B1'].value
```

### Options and Converters

```python
# Expand to data region
sheet['A1'].expand().value           # Expands down and right
sheet['A1'].expand('down').value     # Expands down only
sheet['A1'].expand('right').value    # Expands right only

# Transpose
sheet['A1'].options(transpose=True).value = [1, 2, 3]

# Empty cells
sheet['A1'].options(empty='NA').value  # Replace None with 'NA'

# Numbers only
sheet['A1'].options(numbers=int).value
```

### Pandas Integration

```python
import pandas as pd

# Write DataFrame
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
sheet['A1'].value = df                    # With index and header
sheet['A1'].options(index=False).value = df  # Without index

# Read as DataFrame
df = sheet['A1'].options(pd.DataFrame, expand='table').value
df = sheet['A1'].options(pd.DataFrame, index=False, header=True).value
```

### NumPy Integration

```python
import numpy as np

# Write array
arr = np.array([[1, 2], [3, 4]])
sheet['A1'].value = arr

# Read as array
arr = sheet['A1'].options(np.array, expand='table').value
```

`[VERIFIED] (AXCEL-IN14-SC-XLWNGS-DATA | https://docs.xlwings.org/en/stable/datastructures.html)`

## 7. Built-in REST API

xlwings includes a built-in REST API server for remote access to Excel workbooks.

### Start Server

```bash
# Basic start (Flask development server)
xlwings restapi run

# With options
xlwings restapi run --host 0.0.0.0 --port 5000

# Via Flask directly
set FLASK_APP=xlwings.rest.api
flask run
```

### Endpoints

**Book endpoints:**
- `GET /book/<name>` - Get book info
- `GET /book/<name>/sheets` - List sheets
- `GET /book/<name>/sheets/<sheet>/range/<range>` - Read range

**Books collection:**
- `GET /books` - List all books in active app
- `GET /books/<index>` - Get book by index

**Apps collection:**
- `GET /apps` - List all Excel instances
- `GET /apps/<pid>/books` - Books in specific instance

### Example Requests

```bash
# Read cell range
curl "http://127.0.0.1:5000/book/Book1/sheets/0/range/A1:B2"

# Response:
{
  "value": [[1.0, 2.0], [3.0, 4.0]],
  "formula": [["1", "2"], ["3", "4"]],
  "address": "$A$1:$B$2"
}

# With options
curl "http://127.0.0.1:5000/book/Book1/sheets/0/range/A1?expand=table&transpose=true"
```

### Limitations

- **GET only**: Built-in API is read-only (no POST/PUT for writes)
- **Single-threaded**: Flask dev server is single-threaded
- **No authentication**: No built-in auth mechanism

`[VERIFIED] (AXCEL-IN14-SC-XLWNGS-REST | https://docs.xlwings.org/en/0.26.1/rest_api.html)`

## 8. Custom Server Implementation

For agent use cases, implement a custom server with write capabilities.

### Flask Server with Read/Write

```python
# excel_server.py
from flask import Flask, request, jsonify
import xlwings as xw
import json

app = Flask(__name__)

def get_book(name=None):
    """Get workbook by name or active workbook."""
    if not xw.apps.keys():
        raise Exception("Excel not running. Please open Excel first.")
    if name:
        return xw.Book(name)
    if xw.books.active is None:
        raise Exception("No active workbook. Please open a workbook in Excel.")
    return xw.books.active

def get_sheet(book, sheet=None):
    """Get sheet by name/index or active sheet."""
    if sheet is not None:
        if isinstance(sheet, int):
            return book.sheets[sheet]
        return book.sheets[sheet]
    return book.sheets.active

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    try:
        apps = list(xw.apps.keys())
        return jsonify({'status': 'ok', 'excel_instances': apps})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/books', methods=['GET'])
def list_books():
    """List all open workbooks."""
    books = []
    for pid in xw.apps.keys():
        app = xw.apps[pid]
        for book in app.books:
            books.append({
                'name': book.name,
                'fullname': book.fullname,
                'pid': pid
            })
    return jsonify({'books': books})

@app.route('/read', methods=['POST'])
def read_range():
    """Read cell range. Body: {workbook?, sheet?, range}"""
    data = request.json
    try:
        book = get_book(data.get('workbook'))
        sheet = get_sheet(book, data.get('sheet'))
        rng = sheet.range(data['range'])
        
        return jsonify({
            'range': data['range'],
            'value': rng.value,
            'formula': rng.formula,
            'address': rng.address
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/write', methods=['POST'])
def write_range():
    """Write to cell range. Body: {workbook?, sheet?, range, value?, formula?}"""
    data = request.json
    try:
        book = get_book(data.get('workbook'))
        sheet = get_sheet(book, data.get('sheet'))
        rng = sheet.range(data['range'])
        
        if 'value' in data:
            rng.value = data['value']
        if 'formula' in data:
            rng.formula = data['formula']
        
        return jsonify({'success': True, 'address': rng.address})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calculate', methods=['POST'])
def calculate():
    """Trigger workbook calculation."""
    data = request.json or {}
    try:
        if 'workbook' in data:
            book = get_book(data['workbook'])
            book.app.calculate()
        else:
            xw.apps.active.calculate()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/navigate', methods=['POST'])
def navigate():
    """Navigate to cell range. Body: {workbook?, sheet?, range}"""
    data = request.json
    try:
        book = get_book(data.get('workbook'))
        sheet = get_sheet(book, data.get('sheet'))
        rng = sheet.range(data['range'])
        
        sheet.activate()
        rng.select()
        
        return jsonify({'success': True, 'address': rng.address})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("Starting xlwings server on http://127.0.0.1:5001")
    print("Excel instances:", list(xw.apps.keys()))
    # CRITICAL: threaded=False is required - xlwings is NOT thread-safe
    # Flask's default threaded=True will cause COM errors and crashes
    app.run(port=5001, threaded=False)
```

### Start Server

```powershell
# Start server (keep running)
python excel_server.py

# Or run in background
Start-Process python -ArgumentList "excel_server.py" -WindowStyle Hidden
```

### Agent Usage

```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:5001/health" -Method Get

# List workbooks
Invoke-RestMethod -Uri "http://localhost:5001/books" -Method Get

# Read range
$body = @{range='A1:C10'} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5001/read" -Method Post -Body $body -ContentType "application/json"

# Write value
$body = @{range='A1'; value='Hello from Agent'} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5001/write" -Method Post -Body $body -ContentType "application/json"

# Write formula
$body = @{range='B1'; formula='=SUM(A1:A10)'} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5001/write" -Method Post -Body $body -ContentType "application/json"

# Calculate
Invoke-RestMethod -Uri "http://localhost:5001/calculate" -Method Post

# Navigate
$body = @{range='Z100'} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5001/navigate" -Method Post -Body $body -ContentType "application/json"
```

## 9. VBA Integration

xlwings can call Python from Excel VBA and vice versa.

### Call Python from VBA (RunPython)

```vba
' In Excel VBA module
Sub CallPython()
    RunPython "import mymodule; mymodule.main()"
End Sub
```

```python
# mymodule.py (same folder as workbook)
import xlwings as xw

def main():
    wb = xw.Book.caller()  # Get calling workbook
    sheet = wb.sheets.active
    sheet['A1'].value = 'Called from VBA!'
```

### User Defined Functions (Windows only)

```python
# udfs.py
import xlwings as xw

@xw.func
def double_value(x):
    """Double the input value."""
    return x * 2

@xw.func
@xw.arg('data', pd.DataFrame)
@xw.ret(expand='table')
def process_data(data):
    """Process DataFrame and return."""
    return data * 2
```

Use in Excel: `=double_value(A1)` or `=process_data(A1:C10)`

`[VERIFIED] (AXCEL-IN14-SC-XLWNGS-MACRO | https://docs.xlwings.org/en/stable/vba.html)`

## 10. PRO Features (License Required)

xlwings PRO requires a commercial license for these features:

### xlwings Server

Remote Python interpreter for Excel on the web and Google Sheets:
- Run Python on a server (Linux, Docker, Azure Functions)
- Excel calls server via HTTP
- No local Python installation needed

### Office.js Add-ins

Build Office Add-ins with Python backend:
- Cross-platform (Windows, macOS, Web)
- Task pane UI
- Custom functions

### Reports

Template-based reporting with Jinja2:
- Excel templates with placeholders
- Batch report generation

### Google Sheets

Same xlwings API for Google Sheets:
- Read/write cells
- Charts and pictures

`[VERIFIED] (AXCEL-IN14-SC-XLWNGS-PRO | https://www.xlwings.org/pro)`

## 11. Limitations and Gotchas

### Platform Limitations

- **Windows**: Full feature support via COM
- **macOS**: Limited features via AppleScript (no UDFs)
- **Linux**: No direct Excel control (use xlwings Server PRO)

### COM Quirks

- **Single-threaded**: COM is apartment-threaded; avoid concurrent access
- **Process tie**: Python process tied to Excel process
- **Cleanup**: Use context managers or explicit cleanup

### Performance Tips

```python
# Disable screen updating for bulk operations
app = xw.apps.active
app.screen_updating = False
try:
    # ... bulk operations
finally:
    app.screen_updating = True

# Disable calculation for bulk writes
app.calculation = 'manual'
try:
    # ... write operations
finally:
    app.calculation = 'automatic'
    app.calculate()

# Use arrays instead of cell-by-cell
# BAD:
for i in range(1000):
    sheet[f'A{i+1}'].value = i

# GOOD:
sheet['A1'].value = [[i] for i in range(1000)]
```

### Error Handling

```python
import xlwings as xw
from xlwings import XlwingsError

try:
    wb = xw.Book('NonExistent.xlsx')
except XlwingsError as e:
    print(f"xlwings error: {e}")
except Exception as e:
    print(f"General error: {e}")
```

### Server Considerations

- **Flask single-threaded**: Use `threaded=False` to avoid COM issues
- **Process management**: Server must stay running
- **No events**: Cannot push Excel events to client (must poll)

## 12. Agent Skill Implementation

### Recommended Setup

```
.windsurf/skills/agent-excel/
├── SKILL.md                    # Skill documentation
├── excel_server.py             # xlwings HTTP server
├── excel-remote-control.ps1    # Fallback PowerShell scripts
├── start-server.ps1            # Server startup script
├── stop-server.ps1             # Server shutdown script
└── README.md                   # Usage examples
```

### Server Startup Script

```powershell
# start-server.ps1
$serverPath = Join-Path $PSScriptRoot "excel_server.py"
$pidFile = Join-Path $PSScriptRoot ".server.pid"

# Check if already running
if (Test-Path $pidFile) {
    $pid = Get-Content $pidFile
    if (Get-Process -Id $pid -ErrorAction SilentlyContinue) {
        Write-Host "Server already running (PID: $pid)"
        exit 0
    }
}

# Start server
$process = Start-Process python -ArgumentList $serverPath -WindowStyle Hidden -PassThru
$process.Id | Out-File $pidFile
Write-Host "Server started (PID: $($process.Id))"
```

### Server Shutdown Script

```powershell
# stop-server.ps1
$pidFile = Join-Path $PSScriptRoot ".server.pid"

if (Test-Path $pidFile) {
    $pid = Get-Content $pidFile
    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    Remove-Item $pidFile
    Write-Host "Server stopped"
} else {
    Write-Host "Server not running"
}
```

### Latency Comparison

- **PowerShell per-call**: 250-550ms (process startup + COM init)
- **xlwings server**: 20-100ms (HTTP + existing COM connection)
- **Improvement**: 3-10x faster response times

## 13. Sources

**Primary Sources:**
- `AXCEL-IN14-SC-XLWNGS-DOCS`: https://docs.xlwings.org/ - Main documentation [VERIFIED]
- `AXCEL-IN14-SC-XLWNGS-API`: https://docs.xlwings.org/en/stable/api.html - API reference [VERIFIED]
- `AXCEL-IN14-SC-XLWNGS-QS`: https://docs.xlwings.org/en/stable/quickstart.html - Quickstart guide [VERIFIED]
- `AXCEL-IN14-SC-XLWNGS-REST`: https://docs.xlwings.org/en/0.26.1/rest_api.html - REST API docs [VERIFIED]
- `AXCEL-IN14-SC-XLWNGS-CONN`: https://docs.xlwings.org/en/stable/connect_to_workbook.html - Connect to books [VERIFIED]
- `AXCEL-IN14-SC-XLWNGS-DATA`: https://docs.xlwings.org/en/stable/datastructures.html - Data structures [VERIFIED]
- `AXCEL-IN14-SC-XLWNGS-MACRO`: https://docs.xlwings.org/en/stable/vba.html - VBA integration [VERIFIED]
- `AXCEL-IN14-SC-XLWNGS-PRO`: https://www.xlwings.org/pro - PRO features [VERIFIED]

**Access Date**: 2026-02-27

## 14. Next Steps

1. Create `excel_server.py` in skill folder
2. Create startup/shutdown scripts
3. Test latency improvement vs PowerShell
4. Document API in SKILL.md
5. Add VBA export/import endpoints to server

## 15. Document History

**[2026-02-27 16:20]**
- Added: Threading warning comment in server code (CRITICAL)
- Added: Excel connection error handling in get_book()
- Review: `_INFO_AXCEL-IN14_XLWINGS_REVIEW.md` findings addressed

**[2026-02-27 16:00]**
- Initial comprehensive xlwings documentation
- Custom server implementation with read/write endpoints
- Agent skill integration recommendations
