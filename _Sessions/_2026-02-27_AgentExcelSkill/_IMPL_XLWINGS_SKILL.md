# IMPL: xlwings Excel Skill

**Doc ID**: AXCEL-IP01
**Feature**: XLWINGS_SKILL
**Goal**: Implement Python-based xlwings skill with Flask server and PowerShell management scripts
**Timeline**: Created 2026-02-28

**Target files**:
- `.windsurf/skills/agent-excel/excel_server.py` (NEW ~350 lines)
- `.windsurf/skills/agent-excel/start-server.ps1` (NEW ~40 lines)
- `.windsurf/skills/agent-excel/stop-server.ps1` (NEW ~30 lines)
- `.windsurf/skills/agent-excel/setup-venv.ps1` (NEW ~50 lines)
- `.windsurf/skills/agent-excel/requirements.txt` (NEW ~5 lines)
- `.windsurf/skills/agent-excel/SKILL.md` (NEW ~100 lines)
- `.windsurf/skills/agent-excel/SETUP.md` (NEW ~60 lines)
- `.windsurf/skills/agent-excel/README.md` (NEW ~40 lines)

**Depends on:**
- `_SPEC_XLWINGS_SKILL.md [AXCEL-SP01]` for functional requirements and design decisions

## MUST-NOT-FORGET

- Flask server MUST use `threaded=False` (xlwings is not thread-safe)
- VBA operations require "Trust access to VBA project object model" enabled
- Document modules (Sheet, ThisWorkbook) cannot be imported - only code extraction
- Server binds to 127.0.0.1 only (localhost)
- Lazy connection: Server starts without Excel
- Validate COM connection before each request
- `start-server.ps1` must validate PID is alive (not just file exists)
- `stop-server.ps1` must force-kill after 5 seconds if graceful stop fails

## Table of Contents

1. [File Structure](#1-file-structure)
2. [Edge Cases](#2-edge-cases)
3. [Implementation Steps](#3-implementation-steps)
4. [Test Cases](#4-test-cases)
5. [Verification Checklist](#5-verification-checklist)
6. [Document History](#6-document-history)

## 1. File Structure

```
.windsurf/skills/agent-excel/
├── SKILL.md                # Skill documentation for agent (~100 lines) [NEW]
├── SETUP.md                # Installation and setup guide (~60 lines) [NEW]
├── README.md               # Human-readable usage guide (~40 lines) [NEW]
├── excel_server.py         # Flask server with xlwings (~350 lines) [NEW]
├── start-server.ps1        # Start server script (~40 lines) [NEW]
├── stop-server.ps1         # Stop server script (~30 lines) [NEW]
├── setup-venv.ps1          # Create venv and install deps (~50 lines) [NEW]
└── requirements.txt        # Python dependencies (~5 lines) [NEW]

[WORKSPACE_FOLDER]\..\tools\
└── xlwings-venv/           # Shared Python venv (created by setup-venv.ps1)
```

## 2. Edge Cases

### Input Boundaries

- **AXCEL-IP01-EC-01**: Empty range string -> Return error "Range is required"
- **AXCEL-IP01-EC-02**: Invalid range format (e.g., "ZZZ999999") -> Return xlwings error message
- **AXCEL-IP01-EC-03**: Very large range (A1:Z10000) -> May timeout, return partial or error

### State Transitions

- **AXCEL-IP01-EC-04**: Excel not running on first request -> Return error "Excel not running. Please open Excel first."
- **AXCEL-IP01-EC-05**: Excel closes while server running -> Next request returns "Excel connection lost"
- **AXCEL-IP01-EC-06**: Excel shows modal dialog -> Request blocks, 30s timeout returns control to agent
- **AXCEL-IP01-EC-07**: Server already running on start -> Return "Server already running on port 5001"

### External Failures

- **AXCEL-IP01-EC-08**: Workbook not found by name -> Return "Workbook 'X' not found"
- **AXCEL-IP01-EC-09**: Multiple workbooks with same name -> Return "Multiple workbooks match 'X' - specify full path or pid"
- **AXCEL-IP01-EC-10**: VBA trust not enabled -> Return helpful error with Trust Center instructions
- **AXCEL-IP01-EC-11**: Output folder doesn't exist (CSV/VBA export) -> Create folder or return error
- **AXCEL-IP01-EC-12**: Stale PID file after crash -> start-server.ps1 removes it and starts normally

### Data Anomalies

- **AXCEL-IP01-EC-13**: Cell contains error value (#REF!, #N/A) -> Return error value as string
- **AXCEL-IP01-EC-14**: Empty VBA component (no code) -> Skip during export, return empty list
- **AXCEL-IP01-EC-15**: Document module import attempted -> Skip with warning, return success=false

## 3. Implementation Steps

### Phase 1: Setup Infrastructure

#### AXCEL-IP01-IS-01: Create requirements.txt

**Location**: `.windsurf/skills/agent-excel/requirements.txt`

**Action**: Create new file

**Code**:
```
xlwings>=0.30.0
flask>=2.0.0
```

#### AXCEL-IP01-IS-02: Create setup-venv.ps1

**Location**: `.windsurf/skills/agent-excel/setup-venv.ps1`

**Action**: Create new file

**Code**:
```powershell
# Setup virtual environment for xlwings Excel server
# Creates venv at [WORKSPACE_FOLDER]\..\tools\xlwings-venv

$ErrorActionPreference = "Stop"
$ScriptDir = $PSScriptRoot
$WorkspaceRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$VenvPath = Join-Path (Split-Path -Parent $WorkspaceRoot) ".tools\xlwings-venv"
$RequirementsFile = Join-Path $ScriptDir "requirements.txt"
# Check Python version
$pythonVersion = python --version 2>&1
if ($pythonVersion -notmatch "Python 3\.1[0-9]") {
    Write-Error "Python 3.10+ required. Found: $pythonVersion"
    exit 1
}

# Create venv if not exists
if (-not (Test-Path $VenvPath)) {
    Write-Host "Creating virtual environment at $VenvPath..."
    python -m venv $VenvPath
}

# Activate and install
& "$VenvPath\Scripts\Activate.ps1"
pip install -r $RequirementsFile

# Verify imports
python -c "import xlwings; import flask; print('OK')"
Write-Host "Setup complete. Venv at: $VenvPath"
```

**Note**: Uses workspace-relative path `[WORKSPACE_FOLDER]\..\tools\` as shared location.

### Phase 2: Server Management Scripts

#### AXCEL-IP01-IS-03: Create start-server.ps1

**Location**: `.windsurf/skills/agent-excel/start-server.ps1`

**Action**: Create new file

**Code**:
```powershell
# Start Excel server
$ErrorActionPreference = "Stop"
$ScriptDir = $PSScriptRoot
$WorkspaceRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$VenvPath = Join-Path (Split-Path -Parent $WorkspaceRoot) ".tools\xlwings-venv"
$PidFile = Join-Path $ScriptDir ".server.pid"
$ServerScript = Join-Path $ScriptDir "excel_server.py"

# Check for stale PID file
if (Test-Path $PidFile) {
    $oldPid = Get-Content $PidFile
    $proc = Get-Process -Id $oldPid -ErrorAction SilentlyContinue
    if ($proc) {
        Write-Host "Server already running (PID $oldPid)"
        exit 0
    }
    Remove-Item $PidFile  # Stale PID
}

# Activate venv and start server with logging
& "$VenvPath\Scripts\Activate.ps1"
$LogFile = Join-Path $ScriptDir ".server.log"
$proc = Start-Process -FilePath "python" -ArgumentList $ServerScript `
    -PassThru -NoNewWindow `
    -RedirectStandardOutput $LogFile `
    -RedirectStandardError $LogFile
$proc.Id | Out-File $PidFile
Write-Host "Server started (PID $($proc.Id)). Log: $LogFile"
```

**Note**: Validates PID is alive, removes stale PID file per AXCEL-FR-01. Logs to `.server.log` for debugging.

#### AXCEL-IP01-IS-04: Create stop-server.ps1

**Location**: `.windsurf/skills/agent-excel/stop-server.ps1`

**Action**: Create new file

**Code**:
```powershell
# Stop Excel server (graceful, then force)
$ScriptDir = $PSScriptRoot
$PidFile = Join-Path $ScriptDir ".server.pid"

if (-not (Test-Path $PidFile)) {
    Write-Host "Server not running (no PID file)"
    exit 0
}

$pid = Get-Content $PidFile
$proc = Get-Process -Id $pid -ErrorAction SilentlyContinue

if (-not $proc) {
    Remove-Item $PidFile
    Write-Host "Server not running (stale PID)"
    exit 0
}

# Graceful stop via /shutdown endpoint
try {
    Invoke-RestMethod -Uri "http://localhost:5001/shutdown" -Method Post -TimeoutSec 5
} catch {}

# Wait up to 5 seconds
$waited = 0
while ($waited -lt 5) {
    Start-Sleep -Seconds 1
    $waited++
    if (-not (Get-Process -Id $pid -ErrorAction SilentlyContinue)) { break }
}

# Force kill if still running
if (Get-Process -Id $pid -ErrorAction SilentlyContinue) {
    Stop-Process -Id $pid -Force
    Write-Host "Server force-killed (PID $pid)"
} else {
    Write-Host "Server stopped (PID $pid)"
}

Remove-Item $PidFile -ErrorAction SilentlyContinue
```

**Note**: 5-second graceful stop, then force-kill per AXCEL-FR-01.

### Phase 3: Flask Server Core

#### AXCEL-IP01-IS-05: Create excel_server.py - Imports and globals

**Location**: `.windsurf/skills/agent-excel/excel_server.py`

**Action**: Create new file with imports and Flask app

**Code**:
```python
"""xlwings Excel Server for Windsurf Cascade Agent."""
import os
import sys
import json
import signal
from functools import wraps
from flask import Flask, request, jsonify
import xlwings as xw

app = Flask(__name__)
SERVER_VERSION = "1.0.0"
REQUEST_TIMEOUT = 30
```

#### AXCEL-IP01-IS-06: Create helper functions

**Location**: `excel_server.py` > after imports

**Action**: Add helper functions for connection validation and workbook lookup

**Code**:
```python
def ensure_excel_connection():
    """Validate Excel is running and accessible."""
    if not xw.apps.keys():
        raise Exception("Excel not running. Please open Excel first.")
    try:
        _ = xw.apps.active.visible
    except Exception:
        raise Exception("Excel connection lost. Please restart server.")

def get_book(name=None, pid=None):
    """Get workbook by name, path, or active."""
    ensure_excel_connection()
    if name is None:
        return xw.books.active
    # Check for ambiguity
    matches = [b for b in xw.books if b.name == name or b.fullname == name]
    if pid:
        matches = [b for app in xw.apps if app.pid == pid for b in app.books if b.name == name]
    if len(matches) == 0:
        raise Exception(f"Workbook '{name}' not found")
    if len(matches) > 1:
        raise Exception(f"Multiple workbooks match '{name}' - specify full path or pid")
    return matches[0]

def get_sheet(book, name=None):
    """Get sheet by name, index, or active."""
    if name is None:
        return book.sheets.active
    if isinstance(name, int):
        return book.sheets[name]
    return book.sheets[name]
```

#### AXCEL-IP01-IS-07: Create error handler decorator

**Location**: `excel_server.py` > after helpers

**Action**: Add decorator for consistent error handling

**Code**:
```python
def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_msg = str(e)
            # Translate COM errors
            if "programmatic access" in error_msg.lower():
                error_msg = "Enable 'Trust access to VBA project object model' in Excel Trust Center"
            return jsonify({"error": error_msg}), 400
    return wrapper
```

#### AXCEL-IP01-IS-08: Create health and books endpoints

**Location**: `excel_server.py` > after decorator

**Action**: Add GET /health and GET /books endpoints

**Code**:
```python
@app.route('/health', methods=['GET'])
def health():
    pids = list(xw.apps.keys()) if xw.apps else []
    return jsonify({
        "status": "ok",
        "version": SERVER_VERSION,
        "excel_instances": pids
    })

@app.route('/books', methods=['GET'])
@handle_errors
def list_books():
    ensure_excel_connection()
    books = []
    for pid in xw.apps.keys():
        app = xw.apps[pid]
        for book in app.books:
            books.append({
                "name": book.name,
                "fullname": book.fullname,
                "pid": pid
            })
    return jsonify({"books": books})
```

#### AXCEL-IP01-IS-09: Create read/write endpoints

**Location**: `excel_server.py` > after books endpoint

**Action**: Add POST /read and POST /write endpoints

**Code**:
```python
@app.route('/read', methods=['POST'])
@handle_errors
def read_range():
    data = request.json
    if not data.get('range'):
        return jsonify({"error": "Range is required"}), 400
    book = get_book(data.get('workbook'), data.get('pid'))
    sheet = get_sheet(book, data.get('sheet'))
    rng = sheet.range(data['range'])
    return jsonify({
        "range": data['range'],
        "value": rng.value,
        "formula": rng.formula,
        "address": rng.address
    })

@app.route('/write', methods=['POST'])
@handle_errors
def write_range():
    data = request.json
    if not data.get('range'):
        return jsonify({"error": "Range is required"}), 400
    book = get_book(data.get('workbook'), data.get('pid'))
    sheet = get_sheet(book, data.get('sheet'))
    rng = sheet.range(data['range'])
    if 'formula' in data:
        rng.formula = data['formula']
    elif 'value' in data:
        rng.value = data['value']
    return jsonify({"success": True, "address": rng.address})
```

#### AXCEL-IP01-IS-10: Create navigate and calculate endpoints

**Location**: `excel_server.py` > after write endpoint

**Action**: Add POST /navigate and POST /calculate endpoints

**Code**:
```python
@app.route('/navigate', methods=['POST'])
@handle_errors
def navigate():
    data = request.json
    if not data.get('range'):
        return jsonify({"error": "Range is required"}), 400
    book = get_book(data.get('workbook'), data.get('pid'))
    sheet = get_sheet(book, data.get('sheet'))
    sheet.activate()
    rng = sheet.range(data['range'])
    rng.select()
    return jsonify({"success": True, "address": rng.address})

@app.route('/calculate', methods=['POST'])
@handle_errors
def calculate():
    data = request.json or {}
    if data.get('workbook'):
        book = get_book(data['workbook'], data.get('pid'))
        book.app.calculate()
    else:
        ensure_excel_connection()
        xw.apps.active.calculate()
    return jsonify({"success": True})
```

#### AXCEL-IP01-IS-11: Create CSV export endpoint

**Location**: `excel_server.py` > after calculate endpoint

**Action**: Add POST /export-csv endpoint

**Code**:
```python
@app.route('/export-csv', methods=['POST'])
@handle_errors
def export_csv():
    data = request.json
    if not data.get('workbook') or not data.get('output_folder'):
        return jsonify({"error": "workbook and output_folder required"}), 400
    book = get_book(data['workbook'], data.get('pid'))
    output_folder = data['output_folder']
    os.makedirs(output_folder, exist_ok=True)
    encoding = data.get('encoding', 'utf-8')
    sheets = data.get('sheets') or [s.name for s in book.sheets]
    files = []
    for sheet_name in sheets:
        sheet = book.sheets[sheet_name]
        filename = f"{book.name.rsplit('.', 1)[0]}_{sheet_name}.csv"
        filepath = os.path.join(output_folder, filename)
        # Export using xlwings range to get values
        used_range = sheet.used_range
        if used_range:
            import csv
            with open(filepath, 'w', newline='', encoding=encoding) as f:
                writer = csv.writer(f)
                for row in used_range.value or []:
                    writer.writerow(row if isinstance(row, list) else [row])
            files.append({"sheet": sheet_name, "path": filepath})
    return jsonify({"files": files})
```

#### AXCEL-IP01-IS-12: Create VBA endpoints

**Location**: `excel_server.py` > after CSV endpoint

**Action**: Add VBA list, read, export, import, status endpoints

**Code**:
```python
@app.route('/vba/status', methods=['GET'])
@handle_errors
def vba_status():
    ensure_excel_connection()
    try:
        _ = xw.books.active.api.VBProject.VBComponents
        return jsonify({"trust_enabled": True})
    except Exception:
        return jsonify({
            "trust_enabled": False,
            "guidance": "Enable 'Trust access to VBA project object model' in Excel Trust Center > Macro Settings"
        })

@app.route('/vba/list', methods=['POST'])
@handle_errors
def vba_list():
    data = request.json
    book = get_book(data.get('workbook'), data.get('pid'))
    components = []
    for comp in book.api.VBProject.VBComponents:
        components.append({
            "name": comp.Name,
            "type": comp.Type,
            "line_count": comp.CodeModule.CountOfLines
        })
    return jsonify({"components": components})

@app.route('/vba/read', methods=['POST'])
@handle_errors
def vba_read():
    data = request.json
    book = get_book(data.get('workbook'), data.get('pid'))
    comp = book.api.VBProject.VBComponents(data['component'])
    code = comp.CodeModule.Lines(1, comp.CodeModule.CountOfLines)
    return jsonify({
        "name": comp.Name,
        "type": comp.Type,
        "line_count": comp.CodeModule.CountOfLines,
        "code": code
    })

@app.route('/vba/export', methods=['POST'])
@handle_errors
def vba_export():
    data = request.json
    book = get_book(data.get('workbook'), data.get('pid'))
    output_folder = data['output_folder']
    os.makedirs(output_folder, exist_ok=True)
    files = []
    type_ext = {1: '.bas', 2: '.cls', 3: '.frm', 100: '.txt'}
    for comp in book.api.VBProject.VBComponents:
        if comp.CodeModule.CountOfLines == 0:
            continue
        ext = type_ext.get(comp.Type, '.txt')
        filepath = os.path.join(output_folder, f"{comp.Name}{ext}")
        if comp.Type == 100:  # Document module
            code = comp.CodeModule.Lines(1, comp.CodeModule.CountOfLines)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
        else:
            comp.Export(filepath)
        files.append({"name": comp.Name, "type": comp.Type, "path": filepath})
    return jsonify({"files": files})

@app.route('/vba/import', methods=['POST'])
@handle_errors
def vba_import():
    data = request.json
    book = get_book(data.get('workbook'), data.get('pid'))
    file_path = data['file_path']
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ['.bas', '.cls', '.frm']:
        return jsonify({"error": f"Cannot import {ext} files", "success": False}), 400
    name = os.path.splitext(os.path.basename(file_path))[0]
    # Remove existing component if present
    try:
        existing = book.api.VBProject.VBComponents(name)
        book.api.VBProject.VBComponents.Remove(existing)
    except Exception:
        pass
    book.api.VBProject.VBComponents.Import(file_path)
    return jsonify({"success": True, "component": name})
```

#### AXCEL-IP01-IS-13: Create shutdown endpoint and main

**Location**: `excel_server.py` > at end

**Action**: Add shutdown endpoint and main entry point

**Code**:
```python
@app.route('/shutdown', methods=['POST'])
def shutdown():
    # werkzeug.server.shutdown removed in Werkzeug 2.1+
    # Use os._exit after returning response
    import threading
    def exit_server():
        import time
        time.sleep(0.5)
        os._exit(0)
    threading.Thread(target=exit_server).start()
    return jsonify({"status": "shutting down"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, threaded=False)
```

### Phase 4: Documentation

#### AXCEL-IP01-IS-14: Create SKILL.md

**Location**: `.windsurf/skills/agent-excel/SKILL.md`

**Action**: Create skill documentation for agent

**Note**: Include all endpoints, usage examples, and recovery workflow from spec.

#### AXCEL-IP01-IS-15: Create SETUP.md

**Location**: `.windsurf/skills/agent-excel/SETUP.md`

**Action**: Create installation guide

**Note**: Cover prerequisites (Python 3.10+), setup-venv.ps1 usage, troubleshooting.

#### AXCEL-IP01-IS-16: Create README.md

**Location**: `.windsurf/skills/agent-excel/README.md`

**Action**: Create human-readable overview

**Note**: Brief description, quick start, link to SKILL.md for full docs.

## 4. Test Cases

### Category 1: Server Lifecycle (5 tests)

- **AXCEL-IP01-TC-01**: Start server when not running -> ok=true, server starts, PID file created
- **AXCEL-IP01-TC-02**: Start server when already running -> ok=true, "already running" message
- **AXCEL-IP01-TC-03**: Stop server gracefully -> ok=true, server stops, PID file removed
- **AXCEL-IP01-TC-04**: Stop server with stale PID file -> ok=true, stale PID removed
- **AXCEL-IP01-TC-05**: Force stop after 5s timeout -> ok=true, process killed

### Category 2: Health and Discovery (3 tests)

- **AXCEL-IP01-TC-06**: GET /health when Excel running -> ok=true, returns PIDs
- **AXCEL-IP01-TC-07**: GET /health when Excel not running -> ok=true, empty PIDs array
- **AXCEL-IP01-TC-08**: GET /books with multiple workbooks -> ok=true, returns all with names and PIDs

### Category 3: Read/Write Operations (6 tests)

- **AXCEL-IP01-TC-09**: POST /read with valid range -> ok=true, returns value, formula, address
- **AXCEL-IP01-TC-10**: POST /read with empty range -> ok=false, "Range is required"
- **AXCEL-IP01-TC-11**: POST /write value to cell -> ok=true, cell updated
- **AXCEL-IP01-TC-12**: POST /write formula to cell -> ok=true, formula written
- **AXCEL-IP01-TC-13**: POST /write 2D array -> ok=true, range filled
- **AXCEL-IP01-TC-14**: POST /read non-existent workbook -> ok=false, "Workbook not found"

### Category 4: Navigation and Calculation (3 tests)

- **AXCEL-IP01-TC-15**: POST /navigate to cell -> ok=true, cell selected in Excel
- **AXCEL-IP01-TC-16**: POST /calculate specific workbook -> ok=true, workbook recalculated
- **AXCEL-IP01-TC-17**: POST /calculate all -> ok=true, all workbooks recalculated

### Category 5: CSV Export (3 tests)

- **AXCEL-IP01-TC-18**: POST /export-csv all sheets -> ok=true, CSV files created
- **AXCEL-IP01-TC-19**: POST /export-csv specific sheets -> ok=true, only specified sheets exported
- **AXCEL-IP01-TC-20**: POST /export-csv UTF-8 encoding -> ok=true, files are UTF-8

### Category 6: VBA Operations (6 tests)

- **AXCEL-IP01-TC-21**: GET /vba/status with trust enabled -> ok=true, trust_enabled=true
- **AXCEL-IP01-TC-22**: GET /vba/status with trust disabled -> ok=true, trust_enabled=false with guidance
- **AXCEL-IP01-TC-23**: POST /vba/list -> ok=true, returns components with types
- **AXCEL-IP01-TC-24**: POST /vba/export -> ok=true, files created
- **AXCEL-IP01-TC-25**: POST /vba/import .bas file -> ok=true, module imported
- **AXCEL-IP01-TC-26**: POST /vba/import document module -> ok=false, warning returned

## 5. Verification Checklist

### Prerequisites

- [ ] **AXCEL-IP01-VC-01**: Spec AXCEL-SP01 read and understood
- [ ] **AXCEL-IP01-VC-02**: Python 3.10+ available on system
- [ ] **AXCEL-IP01-VC-03**: Excel installed and can be opened

### Phase 1: Setup Infrastructure

- [ ] **AXCEL-IP01-VC-04**: IS-01 requirements.txt created
- [ ] **AXCEL-IP01-VC-05**: IS-02 setup-venv.ps1 creates venv and installs deps

### Phase 2: Server Management

- [ ] **AXCEL-IP01-VC-06**: IS-03 start-server.ps1 starts server, creates PID file
- [ ] **AXCEL-IP01-VC-07**: IS-03 start-server.ps1 detects running server
- [ ] **AXCEL-IP01-VC-08**: IS-03 start-server.ps1 removes stale PID file
- [ ] **AXCEL-IP01-VC-09**: IS-04 stop-server.ps1 stops server gracefully
- [ ] **AXCEL-IP01-VC-10**: IS-04 stop-server.ps1 force-kills after 5s

### Phase 3: Flask Server

- [ ] **AXCEL-IP01-VC-11**: IS-05 to IS-07 Server imports and helpers work
- [ ] **AXCEL-IP01-VC-12**: IS-08 GET /health returns status and PIDs
- [ ] **AXCEL-IP01-VC-13**: IS-08 GET /books lists all open workbooks
- [ ] **AXCEL-IP01-VC-14**: IS-09 POST /read returns value and formula
- [ ] **AXCEL-IP01-VC-15**: IS-09 POST /write updates cell
- [ ] **AXCEL-IP01-VC-16**: IS-10 POST /navigate selects cell in Excel
- [ ] **AXCEL-IP01-VC-17**: IS-10 POST /calculate triggers recalculation
- [ ] **AXCEL-IP01-VC-18**: IS-11 POST /export-csv creates CSV files
- [ ] **AXCEL-IP01-VC-19**: IS-12 VBA endpoints work with trust enabled
- [ ] **AXCEL-IP01-VC-20**: IS-13 POST /shutdown stops server

### Phase 4: Documentation

- [ ] **AXCEL-IP01-VC-21**: IS-14 SKILL.md created with all endpoints
- [ ] **AXCEL-IP01-VC-22**: IS-15 SETUP.md created with installation guide
- [ ] **AXCEL-IP01-VC-23**: IS-16 README.md created

### Validation

- [ ] **AXCEL-IP01-VC-24**: All test cases TC-01 to TC-26 pass
- [ ] **AXCEL-IP01-VC-25**: Server runs with `threaded=False`
- [ ] **AXCEL-IP01-VC-26**: Server binds to 127.0.0.1 only
- [ ] **AXCEL-IP01-VC-27**: Error messages are user-friendly (no raw COM errors)

## 6. Document History

**[2026-02-28 09:00]**
- Fixed: IS-13 shutdown endpoint (replaced deprecated werkzeug.server.shutdown with os._exit)
- Fixed: IS-03 start-server.ps1 (added .server.log for debugging)
- Fixed: IS-02, IS-03 venv paths to workspace-relative `[WORKSPACE_FOLDER]\\..\\tools\\`
- Review: `_IMPL_XLWINGS_SKILL_REVIEW.md` findings addressed (3 of 8 confirmed)
- Reverted: AXCEL-FL-001 - venv path incorrectly changed to USERPROFILE

**[2026-02-28 08:50]**
- Initial implementation plan created
- 16 implementation steps across 4 phases
- 15 edge cases identified
- 26 test cases defined
- 27 verification checklist items
