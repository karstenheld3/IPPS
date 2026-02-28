# INFO: Remote Control Scenarios

**Doc ID**: AXCEL-IN11
**Goal**: Document approaches for remote-controlling Excel from Windsurf Cascade agent
**Version Scope**: Excel 2016+ / Microsoft 365 (2026-02-27)

**Depends on:**
- `__EXCEL_APIS_SOURCES.md [AXCEL-SOURCES-01]` for source references
- `_INFO_AXCEL-IN02_COM.md [AXCEL-IN02]` for COM API details

## Overview

Remote control of Excel means programmatically interacting with an Excel instance that the user already has open. This is distinct from file manipulation (Open XML) or creating new Excel instances. The primary use case for Windsurf Cascade is to write to cells, navigate, and trigger calculations in workbooks the user is actively working with.

## Viable Approaches for Remote Control

Only certain APIs support true remote control:

| API | Remote Control | Method |
|-----|----------------|--------|
| COM/Interop | Yes | GetActiveObject, BindToMoniker |
| VBA | Yes | Application.Workbooks (from add-in) |
| VSTO | Yes | Add-in runs inside Excel process |
| xlwings | Yes | COM wrapper |
| win32com | Yes | COM wrapper |
| XLL | Yes | Runs inside Excel process |
| JS API | Partial | Add-in must be installed in workbook |
| Graph API | No | Cloud files only |
| Open XML | No | File-based only |
| Office Scripts | No | File-based, not live instance |

## Recommended Approach: COM Automation

For Windsurf Cascade agent on Windows, **COM automation via PowerShell or Python** is the best approach:

### Advantages

- No add-in installation required
- Works with any open workbook
- Full Excel object model access
- Can attach to existing instance
- Process isolation from Excel

### Architecture

```
┌─────────────────┐     COM      ┌─────────────────┐
│  Windsurf       │─────────────>│  Excel.exe      │
│  Cascade Agent  │              │  (User's)       │
│  (PowerShell)   │<─────────────│                 │
└─────────────────┘              └─────────────────┘
```

## Implementation: PowerShell Script for Cascade

### Script: excel-remote-control.ps1

```powershell
param(
    [Parameter(Mandatory=$false)]
    [string]$WorkbookPath,
    
    [Parameter(Mandatory=$false)]
    [string]$SheetName,
    
    [Parameter(Mandatory=$false)]
    [string]$Range,
    
    [Parameter(Mandatory=$false)]
    [string]$Value,
    
    [Parameter(Mandatory=$false)]
    [string]$Formula,
    
    [Parameter(Mandatory=$false)]
    [switch]$Read,
    
    [Parameter(Mandatory=$false)]
    [switch]$Calculate,
    
    [Parameter(Mandatory=$false)]
    [switch]$Navigate,
    
    [Parameter(Mandatory=$false)]
    [switch]$ListWorkbooks
)

# Attach to running Excel
try {
    $excel = [Runtime.InteropServices.Marshal]::GetActiveObject("Excel.Application")
}
catch {
    Write-Error "No running Excel instance found. Please open Excel first."
    exit 1
}

# List workbooks
if ($ListWorkbooks) {
    $excel.Workbooks | ForEach-Object {
        Write-Output "- $($_.Name) [$($_.FullName)]"
    }
    exit 0
}

# Get workbook
if ($WorkbookPath) {
    $workbook = $excel.Workbooks | Where-Object { $_.FullName -eq $WorkbookPath -or $_.Name -eq $WorkbookPath }
    if (-not $workbook) {
        Write-Error "Workbook not found: $WorkbookPath"
        exit 1
    }
} else {
    $workbook = $excel.ActiveWorkbook
    if (-not $workbook) {
        Write-Error "No active workbook"
        exit 1
    }
}

# Get worksheet
if ($SheetName) {
    $worksheet = $workbook.Worksheets | Where-Object { $_.Name -eq $SheetName }
    if (-not $worksheet) {
        Write-Error "Worksheet not found: $SheetName"
        exit 1
    }
} else {
    $worksheet = $workbook.ActiveSheet
}

# Operations
if ($Read -and $Range) {
    $rangeObj = $worksheet.Range($Range)
    $values = $rangeObj.Value2
    $formulas = $rangeObj.Formula
    
    $result = @{
        Range = $Range
        Values = $values
        Formulas = $formulas
    }
    $result | ConvertTo-Json -Depth 10
}

if ($Value -and $Range) {
    $worksheet.Range($Range).Value2 = $Value
    Write-Output "Set $Range = $Value"
}

if ($Formula -and $Range) {
    $worksheet.Range($Range).Formula = $Formula
    Write-Output "Set $Range formula = $Formula"
}

if ($Calculate) {
    $excel.Calculate()
    Write-Output "Calculation triggered"
}

if ($Navigate -and $Range) {
    $worksheet.Activate()
    $worksheet.Range($Range).Select()
    Write-Output "Navigated to $Range"
}

# Cleanup
[Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
```

### Usage Examples

```powershell
# List open workbooks
.\excel-remote-control.ps1 -ListWorkbooks

# Read cell range
.\excel-remote-control.ps1 -Range "A1:C10" -Read

# Write value
.\excel-remote-control.ps1 -Range "D5" -Value "Hello from Cascade"

# Write formula
.\excel-remote-control.ps1 -Range "E5" -Formula "=SUM(A1:A10)"

# Trigger calculation
.\excel-remote-control.ps1 -Calculate

# Navigate to cell
.\excel-remote-control.ps1 -Range "Z100" -Navigate

# Target specific workbook and sheet
.\excel-remote-control.ps1 -WorkbookPath "Budget.xlsx" -SheetName "Q1" -Range "A1" -Value "Updated"
```

## Implementation: Python Script for Cascade

### Script: excel_remote_control.py

```python
import sys
import json
import argparse
import pythoncom
import win32com.client

def get_excel():
    """Attach to running Excel instance"""
    try:
        return win32com.client.GetActiveObject("Excel.Application")
    except pythoncom.com_error:
        print("ERROR: No running Excel instance found", file=sys.stderr)
        sys.exit(1)

def list_workbooks(excel):
    """List all open workbooks"""
    for wb in excel.Workbooks:
        print(f"- {wb.Name} [{wb.FullName}]")

def get_workbook(excel, path=None):
    """Get workbook by path or active workbook"""
    if path:
        for wb in excel.Workbooks:
            if wb.FullName == path or wb.Name == path:
                return wb
        print(f"ERROR: Workbook not found: {path}", file=sys.stderr)
        sys.exit(1)
    return excel.ActiveWorkbook

def main():
    parser = argparse.ArgumentParser(description="Remote control Excel")
    parser.add_argument("--workbook", help="Workbook name or path")
    parser.add_argument("--sheet", help="Worksheet name")
    parser.add_argument("--range", help="Cell range (e.g., A1:C10)")
    parser.add_argument("--value", help="Value to write")
    parser.add_argument("--formula", help="Formula to write")
    parser.add_argument("--read", action="store_true", help="Read range")
    parser.add_argument("--calculate", action="store_true", help="Trigger calculation")
    parser.add_argument("--navigate", action="store_true", help="Navigate to range")
    parser.add_argument("--list", action="store_true", help="List workbooks")
    
    args = parser.parse_args()
    
    excel = get_excel()
    
    if args.list:
        list_workbooks(excel)
        return
    
    wb = get_workbook(excel, args.workbook)
    ws = wb.Worksheets(args.sheet) if args.sheet else wb.ActiveSheet
    
    if args.read and args.range:
        rng = ws.Range(args.range)
        result = {
            "range": args.range,
            "values": rng.Value,
            "formulas": rng.Formula
        }
        print(json.dumps(result, default=str, indent=2))
    
    if args.value and args.range:
        ws.Range(args.range).Value = args.value
        print(f"Set {args.range} = {args.value}")
    
    if args.formula and args.range:
        ws.Range(args.range).Formula = args.formula
        print(f"Set {args.range} formula = {args.formula}")
    
    if args.calculate:
        excel.Calculate()
        print("Calculation triggered")
    
    if args.navigate and args.range:
        ws.Activate()
        ws.Range(args.range).Select()
        print(f"Navigated to {args.range}")

if __name__ == "__main__":
    main()
```

## Cascade Agent Skill Integration

For Windsurf Cascade to use these scripts, create a skill with:

### SKILL.md

```markdown
# Excel Remote Control Skill

Control Excel workbooks that the user has open.

## Available Operations

- **List workbooks**: See all open workbooks
- **Read cells**: Get values and formulas from a range
- **Write cells**: Set values or formulas
- **Calculate**: Trigger workbook calculation
- **Navigate**: Select a cell/range in Excel

## Usage

Run the PowerShell script with appropriate parameters.
```

### Commands

```powershell
# Agent can run these via run_command tool
pwsh -File excel-remote-control.ps1 -ListWorkbooks
pwsh -File excel-remote-control.ps1 -Range "A1:B5" -Read
pwsh -File excel-remote-control.ps1 -Range "C1" -Value "Agent wrote this"
```

## Timing Considerations

### ROT Registration Delay

Excel registers in the Running Object Table (ROT) after losing focus. If GetActiveObject fails immediately after Excel starts:

```powershell
# Wait for Excel to register
Start-Sleep -Seconds 2
$excel = [Runtime.InteropServices.Marshal]::GetActiveObject("Excel.Application")
```

### Multiple Excel Instances

GetActiveObject returns the first registered instance. For specific workbooks, use BindToMoniker:

```csharp
// C#: Attach to specific file
var workbook = (Excel.Workbook)Marshal.BindToMoniker(@"C:\path\to\file.xlsx");
```

## Sources

- `[VERIFIED] (AXCEL-SC-MSFT-RUNINS)` - Automate running instance
- `[COMMUNITY] (AXCEL-SC-SO-ATTACH)` - Attach to existing instance

## Document History

**[2026-02-27 14:05]**
- Initial document creation with remote control implementation
