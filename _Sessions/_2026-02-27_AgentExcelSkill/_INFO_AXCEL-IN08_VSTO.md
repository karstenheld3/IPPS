# INFO: Visual Studio Tools for Office (VSTO)

**Doc ID**: AXCEL-IN08
**Goal**: Document VSTO capabilities for .NET-based Excel solutions
**Version Scope**: VSTO 2022 (2026-02-27)

**Depends on:**
- `__EXCEL_APIS_SOURCES.md [AXCEL-SOURCES-01]` for source references

## Overview

Visual Studio Tools for Office (VSTO) is a .NET development platform for creating Office add-ins and document-level customizations. VSTO add-ins are managed assemblies that load into Excel's process space, providing rich integration with the Excel object model using C# or VB.NET. VSTO offers the COM Interop API with managed code benefits like IntelliSense, strong typing, and .NET libraries. `[VERIFIED] (AXCEL-SC-MSFT-VSTOV)`

VSTO supports two project types: Add-ins (application-level, like COM add-ins) and Document-Level Customizations (attached to specific workbooks). VSTO is Windows-only and considered legacy for new development; Microsoft recommends Office Add-ins (JavaScript) for cross-platform scenarios. However, VSTO remains powerful for Windows-only enterprise solutions requiring deep Excel integration. `[VERIFIED] (AXCEL-SC-MSFT-VSTOW)`

## Supported Features

- **Read cells/data**: Yes - Full Excel object model via Interop
- **Write cells/data**: Yes - Same as COM Interop
- **Read formulas**: Yes - Range.Formula property
- **Write formulas**: Yes - Range.Formula assignment
- **Remote control open workbook**: Yes - Add-in runs inside Excel process
- **Export to CSV**: Yes - Workbook.SaveAs with CSV format
- **Export VBA code**: Yes - VBProject access (requires trust setting)
- **Import VBA code**: Yes - VBComponents.Import (requires trust setting)
- **Works without Excel**: No - Requires Excel as host
- **Cross-platform**: No - Windows only

## Intended Use Cases

1. **Enterprise add-ins**: Complex business logic integrated into Excel
2. **Ribbon customization**: Custom tabs, buttons, and UI elements
3. **Document-level solutions**: Workbooks with embedded .NET functionality
4. **Data connectivity**: Database integration, web service clients
5. **Legacy migration**: Modernizing VBA solutions to .NET

## Limitations

- **Windows only**: VSTO does not work on macOS or web
- **Legacy platform**: Microsoft recommends Office Add-ins for new development
- **Deployment complexity**: Requires ClickOnce or MSI installer
- **Version coupling**: Must match Office version or use version-neutral techniques
- **No cross-platform**: Cannot share with Mac users
- **Visual Studio required**: Needs Visual Studio with Office development workload

## Security Setup

### Trust Requirements

1. **Signed assemblies**: Production add-ins should be signed with a certificate
2. **ClickOnce deployment**: Uses .NET trust policies
3. **VSTO Runtime**: Must be installed on client machines

### For VBProject Access

Same as COM Interop - enable "Trust access to the VBA project object model"

## Platform Support

- **Windows**: Yes - Primary platform
- **macOS**: No - VSTO not supported
- **Web**: No - Desktop only
- **Linux**: No - Windows technology

## Prerequisites

- Visual Studio 2022 with "Office/SharePoint development" workload
- Excel 2013+ or Microsoft 365
- VSTO Runtime installed on target machines
- .NET Framework 4.7.2+ (or .NET 4.8)

## Code Examples

### C#: VSTO Add-in Startup

```csharp
using Excel = Microsoft.Office.Interop.Excel;
using Microsoft.Office.Tools.Ribbon;

public partial class ThisAddIn
{
    private void ThisAddIn_Startup(object sender, EventArgs e)
    {
        // Access Excel application
        Excel.Application excelApp = this.Application;
        
        // Subscribe to events
        excelApp.WorkbookOpen += ExcelApp_WorkbookOpen;
        excelApp.SheetChange += ExcelApp_SheetChange;
    }
    
    private void ExcelApp_WorkbookOpen(Excel.Workbook wb)
    {
        MessageBox.Show($"Opened: {wb.Name}");
    }
    
    private void ExcelApp_SheetChange(object sheet, Excel.Range target)
    {
        // React to cell changes
        System.Diagnostics.Debug.WriteLine($"Changed: {target.Address}");
    }
    
    private void ThisAddIn_Shutdown(object sender, EventArgs e)
    {
        // Cleanup
    }
}
```

### C#: Custom Ribbon Button

```csharp
// In Ribbon1.cs (Ribbon Designer)
private void button1_Click(object sender, RibbonControlEventArgs e)
{
    Excel.Application app = Globals.ThisAddIn.Application;
    Excel.Worksheet ws = app.ActiveSheet;
    
    // Write to active sheet
    ws.Range["A1"].Value = "VSTO was here";
    ws.Range["B1"].Formula = "=NOW()";
    
    // Trigger calculation
    app.Calculate();
    
    // Export to CSV
    string csvPath = Path.Combine(
        Environment.GetFolderPath(Environment.SpecialFolder.Desktop),
        "export.csv"
    );
    app.ActiveWorkbook.SaveAs(csvPath, Excel.XlFileFormat.xlCSV);
}
```

### C#: Export VBA Modules via VSTO

```csharp
// Requires: Trust access to VBA project object model
// Requires: Reference to Microsoft.Vbe.Interop

using Microsoft.Vbe.Interop;

public void ExportVbaModules(string exportPath)
{
    Excel.Workbook wb = Globals.ThisAddIn.Application.ActiveWorkbook;
    VBProject vbProj = wb.VBProject;
    
    Directory.CreateDirectory(exportPath);
    
    foreach (VBComponent comp in vbProj.VBComponents)
    {
        string ext = comp.Type switch
        {
            vbext_ComponentType.vbext_ct_StdModule => ".bas",
            vbext_ComponentType.vbext_ct_ClassModule => ".cls",
            vbext_ComponentType.vbext_ct_MSForm => ".frm",
            _ => ".txt"
        };
        
        if (comp.CodeModule.CountOfLines > 0)
        {
            comp.Export(Path.Combine(exportPath, comp.Name + ext));
        }
    }
}
```

## Gotchas and Quirks

- **VSTO Runtime**: Must be installed; not always present on client machines
- **Office version mismatch**: Targeting newer Office may fail on older versions
- **Cleanup on shutdown**: Must unsubscribe events and release COM objects
- **Ribbon caching**: Ribbon XML may be cached; clear cache during development
- **ClickOnce updates**: Automatic updates can be tricky with signed assemblies
- **64-bit Office**: Must build for AnyCPU or correct architecture `[VERIFIED] (AXCEL-SC-MSFT-VSTOEX)`

## Main Documentation Links

- [Office Solutions Development Overview](https://learn.microsoft.com/en-us/visualstudio/vsto/office-solutions-development-overview-vsto)
- [Create VSTO Add-in for Excel](https://learn.microsoft.com/en-us/visualstudio/vsto/walkthrough-creating-your-first-vsto-add-in-for-excel)
- [Excel Object Model Overview](https://learn.microsoft.com/en-us/visualstudio/vsto/excel-object-model-overview)
- [Create VSTO Add-ins for Office](https://learn.microsoft.com/en-us/visualstudio/vsto/create-vsto-add-ins-for-office-by-using-visual-studio)

## Sources

- `[VERIFIED] (AXCEL-SC-MSFT-VSTOV)` - VSTO overview
- `[VERIFIED] (AXCEL-SC-MSFT-VSTOW)` - VSTO walkthrough
- `[VERIFIED] (AXCEL-SC-MSFT-VSTOEX)` - Excel object model overview

## Document History

**[2026-02-27 13:50]**
- Initial document creation
