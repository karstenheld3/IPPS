# INFO: VBA Code Manipulation

**Doc ID**: AXCEL-IN12
**Goal**: Document approaches for exporting and importing VBA code programmatically
**Version Scope**: Excel 2016+ / Microsoft 365 (2026-02-27)

**Depends on:**
- `__EXCEL_APIS_SOURCES.md [AXCEL-SOURCES-01]` for source references
- `_INFO_AXCEL-IN10_SECURITY.md [AXCEL-IN10]` for security settings

## Overview

VBA code manipulation (export, import, read, modify) requires access to the VBProject object model. This is only available through VBA itself or COM automation (including VSTO and Python win32com). No other APIs (Open XML, Graph, JS API, Office Scripts) support VBA manipulation.

**Critical Requirement**: "Trust access to the VBA project object model" must be enabled.

## Supported APIs for VBA Manipulation

| API | Export VBA | Import VBA | Read Code | Modify Code |
|-----|------------|------------|-----------|-------------|
| VBA | Yes | Yes | Yes | Yes |
| COM/Interop | Yes | Yes | Yes | Yes |
| VSTO | Yes | Yes | Yes | Yes |
| win32com (Python) | Yes | Yes | Yes | Yes |
| PowerShell COM | Yes | Yes | Yes | Yes |
| Open XML SDK | No | No | No | No |
| Graph API | No | No | No | No |
| JS API | No | No | No | No |

## VBProject Object Model

### Key Objects

- **VBProject**: The VBA project container
- **VBComponents**: Collection of all VBA components (modules, classes, forms)
- **VBComponent**: Individual module, class, or form
- **CodeModule**: The actual code within a component

### Component Types

| Type | Value | Extension | Description |
|------|-------|-----------|-------------|
| vbext_ct_StdModule | 1 | .bas | Standard module |
| vbext_ct_ClassModule | 2 | .cls | Class module |
| vbext_ct_MSForm | 3 | .frm | UserForm |
| vbext_ct_Document | 100 | .cls | Document module (Sheet, ThisWorkbook) |

## Export VBA Code

### VBA Implementation

```vba
Sub ExportAllVBACode()
    Dim vbComp As VBComponent
    Dim exportPath As String
    Dim ext As String
    
    exportPath = ThisWorkbook.Path & "\VBA_Export\"
    
    ' Create folder
    On Error Resume Next
    MkDir exportPath
    On Error GoTo 0
    
    For Each vbComp In ThisWorkbook.VBProject.VBComponents
        ' Determine file extension
        Select Case vbComp.Type
            Case vbext_ct_StdModule: ext = ".bas"
            Case vbext_ct_ClassModule: ext = ".cls"
            Case vbext_ct_MSForm: ext = ".frm"
            Case vbext_ct_Document: ext = ".cls"
            Case Else: ext = ".txt"
        End Select
        
        ' Export if has code
        If vbComp.CodeModule.CountOfLines > 0 Then
            vbComp.Export exportPath & vbComp.Name & ext
        End If
    Next vbComp
    
    MsgBox "Exported to: " & exportPath
End Sub
```

### PowerShell Implementation

```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$WorkbookPath,
    
    [Parameter(Mandatory=$true)]
    [string]$ExportFolder
)

# Create export folder
New-Item -ItemType Directory -Path $ExportFolder -Force | Out-Null

# Attach to Excel
$excel = [Runtime.InteropServices.Marshal]::GetActiveObject("Excel.Application")
$workbook = $excel.Workbooks | Where-Object { $_.FullName -eq $WorkbookPath }

if (-not $workbook) {
    Write-Error "Workbook not found: $WorkbookPath"
    exit 1
}

# Export each component
foreach ($comp in $workbook.VBProject.VBComponents) {
    $ext = switch ($comp.Type) {
        1 { ".bas" }  # Standard module
        2 { ".cls" }  # Class module
        3 { ".frm" }  # UserForm
        100 { ".cls" } # Document module
        default { ".txt" }
    }
    
    if ($comp.CodeModule.CountOfLines -gt 0) {
        $filePath = Join-Path $ExportFolder "$($comp.Name)$ext"
        $comp.Export($filePath)
        Write-Output "Exported: $($comp.Name)$ext"
    }
}

Write-Output "Export complete: $ExportFolder"
```

### Python Implementation

```python
import os
import win32com.client

def export_vba_code(workbook_path: str, export_folder: str):
    """Export all VBA modules from a workbook"""
    os.makedirs(export_folder, exist_ok=True)
    
    excel = win32com.client.GetActiveObject("Excel.Application")
    
    # Find workbook
    workbook = None
    for wb in excel.Workbooks:
        if wb.FullName == workbook_path:
            workbook = wb
            break
    
    if not workbook:
        raise ValueError(f"Workbook not found: {workbook_path}")
    
    # Component type to extension mapping
    type_ext = {
        1: ".bas",   # Standard module
        2: ".cls",   # Class module
        3: ".frm",   # UserForm
        100: ".cls"  # Document module
    }
    
    exported = []
    for comp in workbook.VBProject.VBComponents:
        ext = type_ext.get(comp.Type, ".txt")
        
        if comp.CodeModule.CountOfLines > 0:
            file_path = os.path.join(export_folder, f"{comp.Name}{ext}")
            comp.Export(file_path)
            exported.append(comp.Name)
    
    return exported
```

## Import VBA Code

### VBA Implementation

```vba
Sub ImportVBAModule(filePath As String)
    Dim vbProj As VBProject
    Dim moduleName As String
    
    Set vbProj = ThisWorkbook.VBProject
    
    ' Extract module name from file path
    moduleName = Mid(filePath, InStrRev(filePath, "\") + 1)
    moduleName = Left(moduleName, InStrRev(moduleName, ".") - 1)
    
    ' Remove existing module with same name
    On Error Resume Next
    vbProj.VBComponents.Remove vbProj.VBComponents(moduleName)
    On Error GoTo 0
    
    ' Import
    vbProj.VBComponents.Import filePath
End Sub

Sub ImportAllFromFolder(folderPath As String)
    Dim fileName As String
    
    ' Import .bas files
    fileName = Dir(folderPath & "*.bas")
    Do While fileName <> ""
        ImportVBAModule folderPath & fileName
        fileName = Dir()
    Loop
    
    ' Import .cls files
    fileName = Dir(folderPath & "*.cls")
    Do While fileName <> ""
        ImportVBAModule folderPath & fileName
        fileName = Dir()
    Loop
End Sub
```

### PowerShell Implementation

```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$WorkbookPath,
    
    [Parameter(Mandatory=$true)]
    [string]$ImportFolder
)

$excel = [Runtime.InteropServices.Marshal]::GetActiveObject("Excel.Application")
$workbook = $excel.Workbooks | Where-Object { $_.FullName -eq $WorkbookPath }

if (-not $workbook) {
    Write-Error "Workbook not found: $WorkbookPath"
    exit 1
}

$vbProject = $workbook.VBProject

# Import all .bas and .cls files
Get-ChildItem -Path $ImportFolder -Include "*.bas", "*.cls" -File | ForEach-Object {
    $moduleName = $_.BaseName
    
    # Remove existing module
    try {
        $existing = $vbProject.VBComponents.Item($moduleName)
        if ($existing) {
            $vbProject.VBComponents.Remove($existing)
        }
    } catch {}
    
    # Import
    $vbProject.VBComponents.Import($_.FullName)
    Write-Output "Imported: $($_.Name)"
}

Write-Output "Import complete"
```

## Read VBA Code Without Export

### Read Code Lines Directly

```vba
Sub ReadModuleCode(moduleName As String)
    Dim comp As VBComponent
    Dim codeModule As CodeModule
    Dim i As Long
    Dim codeLine As String
    
    Set comp = ThisWorkbook.VBProject.VBComponents(moduleName)
    Set codeModule = comp.CodeModule
    
    For i = 1 To codeModule.CountOfLines
        codeLine = codeModule.Lines(i, 1)
        Debug.Print codeLine
    Next i
End Sub
```

### PowerShell: Read Code to String

```powershell
param(
    [string]$WorkbookPath,
    [string]$ModuleName
)

$excel = [Runtime.InteropServices.Marshal]::GetActiveObject("Excel.Application")
$workbook = $excel.Workbooks | Where-Object { $_.FullName -eq $WorkbookPath }
$comp = $workbook.VBProject.VBComponents.Item($ModuleName)

$lineCount = $comp.CodeModule.CountOfLines
$code = $comp.CodeModule.Lines(1, $lineCount)

Write-Output $code
```

## Modify VBA Code In-Place

### Insert Lines

```vba
Sub InsertCodeAtEnd(moduleName As String, newCode As String)
    Dim comp As VBComponent
    Dim codeModule As CodeModule
    
    Set comp = ThisWorkbook.VBProject.VBComponents(moduleName)
    Set codeModule = comp.CodeModule
    
    codeModule.InsertLines codeModule.CountOfLines + 1, newCode
End Sub
```

### Replace Lines

```vba
Sub ReplaceCode(moduleName As String, oldText As String, newText As String)
    Dim comp As VBComponent
    Dim codeModule As CodeModule
    Dim i As Long
    Dim line As String
    
    Set comp = ThisWorkbook.VBProject.VBComponents(moduleName)
    Set codeModule = comp.CodeModule
    
    For i = 1 To codeModule.CountOfLines
        line = codeModule.Lines(i, 1)
        If InStr(line, oldText) > 0 Then
            line = Replace(line, oldText, newText)
            codeModule.ReplaceLine i, line
        End If
    Next i
End Sub
```

### Delete Lines

```vba
Sub DeleteLines(moduleName As String, startLine As Long, count As Long)
    Dim comp As VBComponent
    Set comp = ThisWorkbook.VBProject.VBComponents(moduleName)
    comp.CodeModule.DeleteLines startLine, count
End Sub
```

## Document Module Handling

Document modules (Sheet1, Sheet2, ThisWorkbook) cannot be exported/imported directly. You must copy code lines:

```vba
Sub CopyDocumentModuleCode(sourceWb As Workbook, targetWb As Workbook, _
                           sourceName As String, targetName As String)
    Dim sourceComp As VBComponent
    Dim targetComp As VBComponent
    Dim code As String
    
    Set sourceComp = sourceWb.VBProject.VBComponents(sourceName)
    Set targetComp = targetWb.VBProject.VBComponents(targetName)
    
    ' Clear existing code
    If targetComp.CodeModule.CountOfLines > 0 Then
        targetComp.CodeModule.DeleteLines 1, targetComp.CodeModule.CountOfLines
    End If
    
    ' Copy code
    If sourceComp.CodeModule.CountOfLines > 0 Then
        code = sourceComp.CodeModule.Lines(1, sourceComp.CodeModule.CountOfLines)
        targetComp.CodeModule.InsertLines 1, code
    End If
End Sub
```

## Cascade Agent Integration

### Export VBA Script for Skill

```powershell
# excel-export-vba.ps1
param(
    [Parameter(Mandatory=$true)]
    [string]$ExportFolder
)

$excel = [Runtime.InteropServices.Marshal]::GetActiveObject("Excel.Application")
$workbook = $excel.ActiveWorkbook

if (-not $workbook) {
    Write-Error "No active workbook"
    exit 1
}

New-Item -ItemType Directory -Path $ExportFolder -Force | Out-Null

$result = @{
    Workbook = $workbook.Name
    Modules = @()
}

foreach ($comp in $workbook.VBProject.VBComponents) {
    $ext = switch ($comp.Type) {
        1 { ".bas" }
        2 { ".cls" }
        3 { ".frm" }
        100 { ".cls" }
        default { ".txt" }
    }
    
    if ($comp.CodeModule.CountOfLines -gt 0) {
        $fileName = "$($comp.Name)$ext"
        $filePath = Join-Path $ExportFolder $fileName
        $comp.Export($filePath)
        $result.Modules += @{
            Name = $comp.Name
            Type = $comp.Type
            File = $fileName
            Lines = $comp.CodeModule.CountOfLines
        }
    }
}

$result | ConvertTo-Json -Depth 3
```

## Gotchas and Quirks

- **Password-protected VBProject**: Cannot access if project has password; no programmatic unlock
- **UserForm binary files**: .frm files need companion .frx files for embedded images/controls
- **Document modules**: Cannot export Sheet/ThisWorkbook modules; must copy code lines
- **Component name conflicts**: Import fails silently if module name already exists; delete first
- **Trust setting scope**: Setting is per-user, not per-workbook
- **XLSM required**: VBA only stored in macro-enabled formats (.xlsm, .xlsb, .xlam)

## Sources

- `[VERIFIED] (AXCEL-SC-MSFT-VBEXT)` - VBA Extensibility reference
- `[VERIFIED] (AXCEL-SC-MSFT-SECVB)` - VBProject trust settings
- `[COMMUNITY] (AXCEL-SC-SO-VBAIMP)` - Import VBA programmatically
- `[COMMUNITY] (AXCEL-SC-SO-VBAEXP)` - Export VBA to files

## Document History

**[2026-02-27 14:10]**
- Initial document creation with VBA manipulation coverage
