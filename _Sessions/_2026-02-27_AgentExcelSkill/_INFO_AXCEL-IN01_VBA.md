# INFO: Excel VBA (Visual Basic for Applications)

**Doc ID**: AXCEL-IN01
**Goal**: Document Excel VBA capabilities, limitations, and usage for Excel automation
**Version Scope**: Excel 2016+ / Microsoft 365 (2026-02-27)

**Depends on:**
- `__EXCEL_APIS_SOURCES.md [AXCEL-SOURCES-01]` for source references

## Overview

Excel VBA (Visual Basic for Applications) is the built-in macro programming language embedded directly in Microsoft Excel since Excel 5.0 (1993). VBA provides full programmatic access to the Excel object model, enabling automation of virtually any Excel operation including cell manipulation, formatting, chart creation, data analysis, and interaction with external systems. VBA code is stored within the workbook itself (in .xlsm, .xlsb, or .xla files) and executes within the Excel process. `[VERIFIED] (AXCEL-SC-MSFT-VBAREF)`

VBA remains the most comprehensive API for Excel automation when code runs from within Excel. It provides direct access to VBProject for manipulating VBA code itself, making it essential for scenarios requiring VBA code export/import. Microsoft continues to support VBA in Microsoft 365, though new development is encouraged toward Office Add-ins (JavaScript API) for cross-platform scenarios. `[VERIFIED] (AXCEL-SC-MSFT-VBAOBJ)`

## Supported Features

- **Read cells/data**: Yes - Full Range object access, all cell properties
- **Write cells/data**: Yes - Direct cell value assignment, bulk operations via arrays
- **Read formulas**: Yes - Range.Formula, Range.FormulaR1C1, Range.FormulaLocal
- **Write formulas**: Yes - Assign formula strings to Range.Formula property
- **Remote control open workbook**: Yes - Can control any open workbook via Application.Workbooks
- **Export to CSV**: Yes - Workbook.SaveAs with xlCSV format
- **Export VBA code**: Yes - VBProject.VBComponents, CodeModule.Lines (requires trust setting)
- **Import VBA code**: Yes - VBComponents.Import for .bas/.cls/.frm files (requires trust setting)
- **Works without Excel**: No - VBA requires Excel as host application
- **Cross-platform**: Partial - Works on Windows and macOS Excel, not web

## Intended Use Cases

1. **Workbook-embedded automation**: Macros that travel with the workbook, run by end users
2. **Complex calculations**: Custom functions (UDFs) that extend Excel's formula capabilities
3. **Data processing pipelines**: ETL operations within Excel (import, transform, export)
4. **Report generation**: Automated report creation with formatting and charts
5. **VBA code management**: Export/import/backup VBA modules across workbooks

## Limitations

- **No headless execution**: Requires Excel application running with UI
- **Single-threaded**: VBA code runs on Excel's main thread, can freeze UI during long operations
- **No async/await**: Synchronous execution model only
- **Security restrictions**: Modern Excel defaults block macros; users must enable
- **Version brittleness**: Code may break across Excel versions if using undocumented features
- **No REST/HTTP native**: Requires external libraries (WinHTTP, XMLHTTP) for web requests
- **No JSON native**: JSON parsing requires custom code or libraries
- **macOS limitations**: Some Windows-specific features unavailable (e.g., ActiveX controls)

## Security Setup

### Required Settings for VBA Execution

1. **Macro Security Level**: Must be set to allow macros
   - File > Options > Trust Center > Trust Center Settings > Macro Settings
   - Options: "Disable all macros with notification" (recommended) or "Enable all macros" (not recommended)

2. **Trusted Locations**: Add folder paths where macro-enabled files are trusted
   - Trust Center > Trusted Locations > Add new location

3. **Digital Signatures**: Sign VBA projects for distribution
   - Developer tab > Visual Basic > Tools > Digital Signature

### Required Settings for VBProject Access (VBA Code Manipulation)

**Critical**: To export/import VBA code programmatically:

1. Open Excel > File > Options > Trust Center > Trust Center Settings
2. Click "Macro Settings"
3. Check "Trust access to the VBA project object model"

`[VERIFIED] (AXCEL-SC-MSFT-SECVB)`

### Security Risks

- Enabling "Trust access to VBA project object model" allows any macro to read/modify VBA code in any open workbook
- Malicious macros could inject code into other workbooks
- Recommendation: Enable only when needed, disable after use
- Alternative: Use COM automation from external process (same security requirement but process isolation)

## Platform Support

- **Windows**: Yes - Full feature support
- **macOS**: Partial - Core VBA works, some Windows-specific features missing (ActiveX, certain API calls)
- **Web**: No - Excel for the web does not support VBA
- **Linux**: No - Excel not available on Linux

## Prerequisites

- Microsoft Excel installed (2016 or later recommended)
- Workbook saved as macro-enabled format (.xlsm, .xlsb, .xlam)
- Macro security settings configured to allow execution
- For VBProject access: "Trust access to VBA project object model" enabled

## Code Examples

### VBA: Read All Cells from Active Sheet to Array

```vba
Sub ReadSheetToArray()
    Dim ws As Worksheet
    Dim lastRow As Long, lastCol As Long
    Dim data As Variant
    
    Set ws = ActiveSheet
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column
    
    ' Read entire range to 2D array (fast)
    data = ws.Range(ws.Cells(1, 1), ws.Cells(lastRow, lastCol)).Value
    
    ' Access: data(row, col) - 1-based indexing
    Debug.Print "Cell A1: " & data(1, 1)
End Sub
```

### VBA: Export All Sheets to CSV

```vba
Sub ExportAllSheetsToCSV()
    Dim ws As Worksheet
    Dim wb As Workbook
    Dim savePath As String
    
    savePath = ThisWorkbook.Path & "\"
    
    For Each ws In ThisWorkbook.Worksheets
        ws.Copy
        Set wb = ActiveWorkbook
        wb.SaveAs savePath & ws.Name & ".csv", xlCSV
        wb.Close SaveChanges:=False
    Next ws
    
    MsgBox "Exported " & ThisWorkbook.Worksheets.Count & " sheets to CSV"
End Sub
```

### VBA: Export All VBA Modules to Files

```vba
Sub ExportVBAModules()
    ' REQUIRES: Trust access to VBA project object model
    Dim vbComp As Object
    Dim exportPath As String
    Dim ext As String
    
    exportPath = ThisWorkbook.Path & "\VBA_Export\"
    
    ' Create folder if not exists
    On Error Resume Next
    MkDir exportPath
    On Error GoTo 0
    
    For Each vbComp In ThisWorkbook.VBProject.VBComponents
        Select Case vbComp.Type
            Case 1: ext = ".bas"  ' Standard module
            Case 2: ext = ".cls"  ' Class module
            Case 3: ext = ".frm"  ' UserForm
            Case 100: ext = ".cls" ' Document module (ThisWorkbook, Sheet)
            Case Else: ext = ".txt"
        End Select
        
        If vbComp.CodeModule.CountOfLines > 0 Then
            vbComp.Export exportPath & vbComp.Name & ext
        End If
    Next vbComp
    
    MsgBox "VBA modules exported to: " & exportPath
End Sub
```

### VBA: Import VBA Module from File

```vba
Sub ImportVBAModule(filePath As String)
    ' REQUIRES: Trust access to VBA project object model
    Dim vbProj As Object
    Dim moduleName As String
    
    Set vbProj = ThisWorkbook.VBProject
    
    ' Remove existing module with same name (optional)
    moduleName = Mid(filePath, InStrRev(filePath, "\") + 1)
    moduleName = Left(moduleName, InStrRev(moduleName, ".") - 1)
    
    On Error Resume Next
    vbProj.VBComponents.Remove vbProj.VBComponents(moduleName)
    On Error GoTo 0
    
    ' Import the module
    vbProj.VBComponents.Import filePath
End Sub
```

### VBA: Write Formulas to Range

```vba
Sub WriteFormulasToRange()
    Dim ws As Worksheet
    Set ws = ActiveSheet
    
    ' Single formula
    ws.Range("B2").Formula = "=SUM(A1:A10)"
    
    ' Formula with relative references (auto-adjusts when copied)
    ws.Range("C2:C10").Formula = "=A2*B2"
    
    ' R1C1 style formula
    ws.Range("D2").FormulaR1C1 = "=RC[-1]*2"
    
    ' Array formula (legacy)
    ws.Range("E2:E10").FormulaArray = "=A2:A10*B2:B10"
    
    ' Dynamic array formula (Excel 365)
    ws.Range("F2").Formula2 = "=UNIQUE(A2:A100)"
End Sub
```

## Gotchas and Quirks

- **VBProject access error 1004**: Occurs if "Trust access to VBA project object model" is not enabled `[COMMUNITY] (AXCEL-SC-SO-VBAIMP)`
- **Password-protected VBProject**: Cannot access VBProject if it has a password; no API to unlock
- **Document modules**: Cannot export/import Sheet or ThisWorkbook modules directly; must copy code lines
- **UserForm binary**: .frm files require companion .frx binary files for images/controls
- **Reference library**: Early-bound references may break on machines with different Office versions
- **64-bit compatibility**: Some Declare statements need PtrSafe keyword for 64-bit Excel
- **Application.Run limitations**: Cannot run macros in add-ins (.xlam) that are not installed `[COMMUNITY] (AXCEL-SC-SO-VBAEXP)`

## Main Documentation Links

- [Excel VBA Reference](https://learn.microsoft.com/en-us/office/vba/api/overview/excel)
- [Excel Object Model](https://learn.microsoft.com/en-us/office/vba/api/overview/excel/object-model)
- [VBA Extensibility Reference](https://learn.microsoft.com/en-us/office/vba/language/reference/visual-basic-add-in-model/objects-visual-basic-add-in-model)
- [Security Notes for Developers](https://learn.microsoft.com/en-us/office/vba/library-reference/concepts/security-notes-for-microsoft-office-solution-developers)

## Sources

- `[VERIFIED] (AXCEL-SC-MSFT-VBAREF)` - Excel VBA Reference main page
- `[VERIFIED] (AXCEL-SC-MSFT-VBAOBJ)` - Excel Object Model documentation
- `[VERIFIED] (AXCEL-SC-MSFT-VBEXT)` - Visual Basic Add-In Model
- `[VERIFIED] (AXCEL-SC-MSFT-SECVB)` - Programmatic access to VBA project
- `[COMMUNITY] (AXCEL-SC-SO-VBAIMP)` - Import VBA modules programmatically
- `[COMMUNITY] (AXCEL-SC-SO-VBAEXP)` - Export VBA to text files

## Document History

**[2026-02-27 12:55]**
- Initial document creation with full VBA coverage
