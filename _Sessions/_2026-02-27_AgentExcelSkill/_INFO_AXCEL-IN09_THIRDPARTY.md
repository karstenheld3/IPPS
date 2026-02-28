# INFO: Third-Party Libraries (Python, PowerShell)

**Doc ID**: AXCEL-IN09
**Goal**: Document third-party Excel automation libraries
**Version Scope**: Current versions as of 2026-02-27

**Depends on:**
- `__EXCEL_APIS_SOURCES.md [AXCEL-SOURCES-01]` for source references

## Overview

Multiple third-party libraries exist for Excel automation, particularly in Python and PowerShell. These libraries fall into two categories: **file-based** (manipulate .xlsx files directly without Excel) and **COM-based** (automate Excel application via COM). The choice depends on whether you need live Excel interaction or just file manipulation.

## Library Categories

### File-Based (No Excel Required)

- **openpyxl** (Python): Read/write .xlsx files
- **XlsxWriter** (Python): Write-only .xlsx with charts
- **ImportExcel** (PowerShell): Read/write .xlsx without Excel

### COM-Based (Excel Required, Windows Only)

- **xlwings** (Python): COM automation + macOS support
- **pywin32/win32com** (Python): Direct COM access
- **PowerShell COM**: Native COM support via New-Object

## openpyxl (Python)

### Features

- **Read cells/data**: Yes
- **Write cells/data**: Yes
- **Read formulas**: Yes (as strings)
- **Write formulas**: Yes (as strings, not calculated)
- **Remote control**: No - File-based
- **Cross-platform**: Yes
- **Excel required**: No

### Installation

```bash
pip install openpyxl
```

### Code Examples

```python
from openpyxl import Workbook, load_workbook

# Create new workbook
wb = Workbook()
ws = wb.active
ws['A1'] = "Hello"
ws['B1'] = 123
ws['C1'] = "=A1&B1"
wb.save("output.xlsx")

# Read existing workbook
wb = load_workbook("input.xlsx")
ws = wb.active

# Read values and formulas
for row in ws.iter_rows(min_row=1, max_row=10, values_only=True):
    print(row)

# Read formula text (not result)
print(ws['C1'].value)  # Returns formula string
```

### Limitations

- No formula calculation (stores formula text only)
- No VBA/macro support
- No live Excel interaction

## xlwings (Python)

### Features

- **Read cells/data**: Yes
- **Write cells/data**: Yes
- **Read formulas**: Yes (with calculated values)
- **Write formulas**: Yes (calculated by Excel)
- **Remote control**: Yes - COM-based
- **Cross-platform**: Windows + macOS
- **Excel required**: Yes

### Installation

```bash
pip install xlwings
```

### Code Examples

```python
import xlwings as xw

# Attach to running Excel or start new
app = xw.apps.active  # Running instance
# OR
app = xw.App(visible=True)  # New instance

# Access workbook
wb = app.books.active
# OR
wb = xw.Book("path/to/file.xlsx")

# Read/write cells
ws = wb.sheets.active
ws.range("A1").value = "xlwings"
ws.range("B1").formula = "=NOW()"

# Trigger calculation
app.calculate()

# Read calculated value
print(ws.range("B1").value)

# Export all sheets to CSV
import os
for sheet in wb.sheets:
    data = sheet.used_range.value
    # Convert to CSV string
    csv_data = "\n".join([",".join(map(str, row)) for row in data])
    with open(f"{sheet.name}.csv", "w") as f:
        f.write(csv_data)
```

### Remote Control Example

```python
import xlwings as xw

# Connect to existing Excel instance with specific workbook
wb = xw.Book("C:\\path\\to\\open\\workbook.xlsx")
app = wb.app

# Write to user's open workbook
ws = wb.sheets[0]
ws.range("A1").value = "Written by xlwings"

# Navigate to cell
ws.range("Z100").select()

# Trigger calculation
app.calculate()
```

## pywin32 / win32com (Python)

### Features

Same as COM Interop - full Excel object model access.

### Installation

```bash
pip install pywin32
```

### Code Examples

See `_INFO_AXCEL-IN02_COM.md` for detailed win32com examples.

```python
import win32com.client

# Attach to running Excel
excel = win32com.client.GetActiveObject("Excel.Application")

# Or start new instance
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = True
```

## ImportExcel (PowerShell)

### Features

- **Read cells/data**: Yes
- **Write cells/data**: Yes
- **Read formulas**: Partial (as strings)
- **Write formulas**: Yes (as strings)
- **Remote control**: No - File-based
- **Cross-platform**: Yes (PowerShell Core)
- **Excel required**: No

### Installation

```powershell
Install-Module ImportExcel -Scope CurrentUser
```

### Code Examples

```powershell
# Export data to Excel
$data = @(
    [PSCustomObject]@{Name="Alice"; Score=95}
    [PSCustomObject]@{Name="Bob"; Score=87}
)
$data | Export-Excel -Path "output.xlsx" -AutoSize -TableName "Scores"

# Import from Excel
$imported = Import-Excel -Path "input.xlsx"
$imported | ForEach-Object { Write-Host $_.Name, $_.Score }

# Multiple sheets
$data | Export-Excel -Path "multi.xlsx" -WorksheetName "Sheet1"
$data | Export-Excel -Path "multi.xlsx" -WorksheetName "Sheet2" -Append

# Export all sheets to CSV
$excel = Open-ExcelPackage -Path "input.xlsx"
foreach ($ws in $excel.Workbook.Worksheets) {
    $csvPath = "$($ws.Name).csv"
    # Export each worksheet
    Import-Excel -Path "input.xlsx" -WorksheetName $ws.Name | 
        Export-Csv -Path $csvPath -NoTypeInformation
}
```

### Advantages

- No Excel installation required
- Works on Linux/macOS with PowerShell Core
- Rich formatting options (conditional formatting, charts)
- Maintained by MVP Doug Finke

## Comparison Matrix

| Feature | openpyxl | xlwings | win32com | ImportExcel |
|---------|----------|---------|----------|-------------|
| Excel Required | No | Yes | Yes | No |
| Cross-Platform | Yes | Win+Mac | Windows | Yes |
| Read Formulas | Text only | Calculated | Calculated | Text only |
| Remote Control | No | Yes | Yes | No |
| VBA Access | No | Limited | Yes | No |
| Performance | Fast | Medium | Medium | Fast |

## Recommendations by Use Case

### Agent Remote Control (Windsurf Cascade)

- **Windows**: `win32com` or `xlwings` - Full COM access, attach to running Excel
- **Cross-platform file ops**: `openpyxl` - File manipulation without Excel

### Batch File Processing

- **Python**: `openpyxl` - Fast, no Excel dependency
- **PowerShell**: `ImportExcel` - Great for scripts, no Excel needed

### VBA Manipulation

- **Only option**: `win32com` with VBE reference - Third-party libs don't support VBA

## Sources

- `[COMMUNITY] (AXCEL-SC-GH-IMPEXL)` - ImportExcel GitHub
- `[COMMUNITY] (AXCEL-SC-WEB-XLWNG)` - xlwings website
- `[COMMUNITY] (AXCEL-SC-SO-PYCOMP)` - Python libraries comparison

## Document History

**[2026-02-27 13:55]**
- Initial document creation with Python and PowerShell libraries
