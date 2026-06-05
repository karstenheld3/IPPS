# INFO: Excel COM/Interop API

**Doc ID**: AXCEL-IN02
**Goal**: Document Excel COM/Interop API capabilities for external process automation
**Version Scope**: Excel 2016+ / Microsoft 365 (2026-02-27)

**Depends on:**
- `__EXCEL_APIS_SOURCES.md [AXCEL-SOURCES-01]` for source references

## Overview

The Excel COM (Component Object Model) API, also known as Office Interop, allows external applications to control Excel programmatically. The .NET wrapper is Microsoft.Office.Interop.Excel, which provides strongly-typed access to Excel's COM objects. This is the **primary method for remote-controlling Excel from external processes** on Windows, including attaching to already-running Excel instances. `[VERIFIED] (AXCEL-SC-MSFT-INTNS)`

COM automation has been available since Excel 97 and remains fully supported in Microsoft 365. It provides the same object model as VBA but accessed from external processes (C#, VB.NET, Python, PowerShell, C++). The key advantage over VBA is process isolation - automation code runs in a separate process, providing stability and the ability to control Excel without modifying workbooks. `[VERIFIED] (AXCEL-SC-MSFT-INTAUT)`

## Supported Features

- **Read cells/data**: Yes - Full Range object access identical to VBA
- **Write cells/data**: Yes - Direct cell value assignment, array operations
- **Read formulas**: Yes - Range.Formula, Range.FormulaR1C1
- **Write formulas**: Yes - Assign formula strings to cells
- **Remote control open workbook**: Yes - GetActiveObject() or BindToMoniker() to attach
- **Export to CSV**: Yes - Workbook.SaveAs with XlFileFormat.xlCSV
- **Export VBA code**: Yes - VBProject access (requires trust setting + reference)
- **Import VBA code**: Yes - VBComponents.Import (requires trust setting + reference)
- **Works without Excel**: No - Requires Excel installation
- **Cross-platform**: No - Windows only (COM is Windows technology)

## Intended Use Cases

1. **Agent-based automation**: External process (like Windsurf Cascade) controlling Excel
2. **Batch processing**: Process multiple workbooks from command-line tools
3. **Integration scenarios**: Connect Excel to other systems (databases, APIs)
4. **Remote control**: Attach to user's open Excel and manipulate it
5. **Background automation**: Run Excel operations without blocking main application

## Limitations

- **Windows only**: COM is a Windows technology; no macOS/Linux support
- **Excel required**: Must have Excel installed on the machine
- **Process overhead**: Each automation session starts Excel process (unless attaching)
- **Memory leaks**: Must explicitly release COM objects or face memory issues
- **Single-threaded apartment**: COM threading model can cause issues in async code
- **Version coupling**: Interop assemblies tied to specific Office versions (use PIA or dynamic)
- **No headless mode**: Excel window exists (can be hidden but process is visible)
- **ROT registration timing**: GetActiveObject may fail if Excel hasn't registered yet

## Security Setup

### Required Settings for Basic Automation

No special settings required for basic cell read/write operations.

### Required Settings for VBProject Access

Same as VBA - must enable "Trust access to the VBA project object model":

1. Excel > File > Options > Trust Center > Trust Center Settings
2. Macro Settings > Check "Trust access to the VBA project object model"

Additionally, add reference to VBA Extensibility library:
- Microsoft Visual Basic for Applications Extensibility 5.3

`[VERIFIED] (AXCEL-SC-MSFT-SECNT)`

### DCOM Settings (for remote machine automation)

For controlling Excel on a remote machine (not recommended):
- Configure DCOM settings via dcomcnfg.exe
- Grant Launch and Activation permissions
- Note: Microsoft does not support server-side Office automation

## Platform Support

- **Windows**: Yes - Full support
- **macOS**: No - COM not available
- **Web**: No - Not applicable
- **Linux**: No - COM not available

## Prerequisites

- Microsoft Excel installed
- .NET Framework or .NET 5+ (for Microsoft.Office.Interop.Excel)
- Reference to Excel PIA (Primary Interop Assembly) or use dynamic/late binding
- For Python: pywin32 package (`pip install pywin32`)
- For PowerShell: No additional requirements (COM is built-in)

## Code Examples

### C#: Create New Workbook and Write Data

```csharp
using Excel = Microsoft.Office.Interop.Excel;

// Create new Excel instance
var excelApp = new Excel.Application();
excelApp.Visible = true;

// Add workbook
Excel.Workbook workbook = excelApp.Workbooks.Add();
Excel.Worksheet worksheet = workbook.ActiveSheet;

// Write data
worksheet.Cells[1, 1] = "Name";
worksheet.Cells[1, 2] = "Value";
worksheet.Cells[2, 1] = "Test";
worksheet.Cells[2, 2] = 123;

// Write formula
worksheet.Cells[3, 2].Formula = "=SUM(B2:B2)*2";

// Save and cleanup
workbook.SaveAs(@"C:\temp\output.xlsx");
workbook.Close();
excelApp.Quit();

// Release COM objects
System.Runtime.InteropServices.Marshal.ReleaseComObject(worksheet);
System.Runtime.InteropServices.Marshal.ReleaseComObject(workbook);
System.Runtime.InteropServices.Marshal.ReleaseComObject(excelApp);
```

### C#: Attach to Running Excel Instance

```csharp
using System.Runtime.InteropServices;
using Excel = Microsoft.Office.Interop.Excel;

// Method 1: GetActiveObject - gets any running Excel
try
{
    var excelApp = (Excel.Application)Marshal.GetActiveObject("Excel.Application");
    Console.WriteLine($"Connected to Excel with {excelApp.Workbooks.Count} workbooks");
    
    // Access active workbook
    Excel.Workbook wb = excelApp.ActiveWorkbook;
    Excel.Worksheet ws = wb.ActiveSheet;
    
    // Write to active cell
    ws.Range["A1"].Value = "Written by external process";
    
    // Trigger calculation
    excelApp.Calculate();
}
catch (COMException ex)
{
    Console.WriteLine("No running Excel instance found: " + ex.Message);
}

// Method 2: BindToMoniker - attach to specific file
try
{
    var workbook = (Excel.Workbook)Marshal.BindToMoniker(@"C:\path\to\file.xlsx");
    Excel.Application excelApp = workbook.Application;
    // ... work with workbook
}
catch (COMException ex)
{
    // If file not open, this starts new Excel instance and opens file
}
```

### C#: Export VBA Modules via COM

```csharp
// Requires: Trust access to VBA project object model
// Requires: Reference to Microsoft.Vbe.Interop

using Excel = Microsoft.Office.Interop.Excel;
using Microsoft.Vbe.Interop;

var excelApp = (Excel.Application)Marshal.GetActiveObject("Excel.Application");
Excel.Workbook workbook = excelApp.ActiveWorkbook;

VBProject vbProject = workbook.VBProject;
string exportPath = @"C:\temp\vba_export\";
Directory.CreateDirectory(exportPath);

foreach (VBComponent component in vbProject.VBComponents)
{
    string ext = component.Type switch
    {
        vbext_ComponentType.vbext_ct_StdModule => ".bas",
        vbext_ComponentType.vbext_ct_ClassModule => ".cls",
        vbext_ComponentType.vbext_ct_MSForm => ".frm",
        vbext_ComponentType.vbext_ct_Document => ".cls",
        _ => ".txt"
    };
    
    if (component.CodeModule.CountOfLines > 0)
    {
        component.Export(Path.Combine(exportPath, component.Name + ext));
    }
}
```

### PowerShell: Remote Control Excel

```powershell
# Attach to running Excel
$excel = [Runtime.InteropServices.Marshal]::GetActiveObject("Excel.Application")

# Or create new instance
# $excel = New-Object -ComObject Excel.Application
# $excel.Visible = $true

# Access active workbook
$workbook = $excel.ActiveWorkbook
$worksheet = $workbook.ActiveSheet

# Read cell
$value = $worksheet.Range("A1").Value2
Write-Host "A1 contains: $value"

# Write to cell
$worksheet.Range("B1").Value2 = "Hello from PowerShell"

# Write formula
$worksheet.Range("C1").Formula = "=A1+B1"

# Trigger calculation
$excel.Calculate()

# Export to CSV
$csvPath = "C:\temp\export.csv"
$workbook.SaveAs($csvPath, 6)  # 6 = xlCSV

# Don't quit if we attached to running instance
# $excel.Quit()

# Release COM object
[Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
```

### Python: COM Automation with win32com

```python
import win32com.client
import pythoncom

# Attach to running Excel
try:
    excel = win32com.client.GetActiveObject("Excel.Application")
    print(f"Connected to Excel with {excel.Workbooks.Count} workbooks")
except pythoncom.com_error:
    print("No running Excel, starting new instance")
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = True

# Access or create workbook
if excel.Workbooks.Count > 0:
    wb = excel.ActiveWorkbook
else:
    wb = excel.Workbooks.Add()

ws = wb.ActiveSheet

# Read/write cells
ws.Range("A1").Value = "Python was here"
ws.Range("B1").Formula = "=NOW()"

# Read formula result
excel.Calculate()
print(f"B1 value: {ws.Range('B1').Value}")

# Export all sheets to CSV
import os
for sheet in wb.Worksheets:
    sheet.Copy()
    temp_wb = excel.ActiveWorkbook
    csv_path = os.path.join("C:\\temp", f"{sheet.Name}.csv")
    temp_wb.SaveAs(csv_path, FileFormat=6)  # 6 = xlCSV
    temp_wb.Close(SaveChanges=False)
```

## Gotchas and Quirks

- **GetActiveObject timing**: Excel registers in ROT (Running Object Table) only after losing focus. If Excel just started, GetActiveObject may fail. Add delay or use BindToMoniker. `[VERIFIED] (AXCEL-SC-MSFT-RUNINS)`
- **Multiple Excel instances**: GetActiveObject returns the first registered instance, not necessarily the one you want. Use BindToMoniker with file path for specific workbook. `[COMMUNITY] (AXCEL-SC-SO-ATTACH)`
- **COM object cleanup**: Failing to release COM objects causes Excel.exe to remain in memory. Use Marshal.ReleaseComObject or Marshal.FinalReleaseComObject.
- **Two-dot rule**: Avoid chaining like `excel.Workbooks[1].Worksheets[1].Range["A1"]` - store intermediate references for proper cleanup.
- **Embed Interop Types**: Set "Embed Interop Types" = true in project reference to avoid PIA deployment issues.
- **Dynamic binding**: Use `dynamic` keyword in C# to avoid version-specific PIA references.
- **DisplayAlerts**: Set `excel.DisplayAlerts = false` to suppress save prompts in automation.
- **ScreenUpdating**: Set `excel.ScreenUpdating = false` for performance, restore to true when done.

## Main Documentation Links

- [Microsoft.Office.Interop.Excel Namespace](https://learn.microsoft.com/en-us/dotnet/api/microsoft.office.interop.excel)
- [Automate Excel from Visual C#](https://learn.microsoft.com/en-us/previous-versions/office/troubleshoot/office-developer/automate-excel-from-visual-c)
- [Automate Running Instance](https://learn.microsoft.com/en-us/previous-versions/office/troubleshoot/office-developer/use-visual-c-automate-run-program-instance)
- [How to Access Office Interop Objects](https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/interop/how-to-access-office-interop-objects)

## Sources

- `[VERIFIED] (AXCEL-SC-MSFT-INTNS)` - Interop namespace documentation
- `[VERIFIED] (AXCEL-SC-MSFT-INTAUT)` - Automate Excel from C#
- `[VERIFIED] (AXCEL-SC-MSFT-RUNINS)` - Automate running instance
- `[VERIFIED] (AXCEL-SC-MSFT-SECNT)` - Security notes for developers
- `[COMMUNITY] (AXCEL-SC-SO-ATTACH)` - Attach to existing Excel instance

## Document History

**[2026-02-27 13:05]**
- Initial document creation with COM/Interop coverage
- Added attach-to-running-instance examples for C#, PowerShell, Python
