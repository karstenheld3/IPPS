<DevSystem MarkdownTablesAllowed=true />

# INFO: VSTO Excel Complete API Reference

**Doc ID**: AXCEL-IN08-API
**Goal**: Comprehensive documentation of all VSTO namespaces, classes, and host controls for Excel development
**Version Scope**: VSTO 2022 / Visual Studio 2022 (2026-02-27)
**Source**: Microsoft Learn - Microsoft.Office.Tools.Excel Namespace

**Depends on:**
- `_INFO_AXCEL-IN08_VSTO.md [AXCEL-IN08]` for VSTO overview and usage
- `_INFO_AXCEL-IN02_COM_API.md [AXCEL-IN02-API]` for underlying COM Interop API

## Table of Contents

1. API Overview
2. VSTO Namespaces
3. Host Items (Workbook, Worksheet, ChartSheet)
4. Host Controls (NamedRange, ListObject, Chart)
5. Globals Class and Factory
6. Application-Level Events
7. Ribbon Customization
8. Data Binding
9. Windows Forms Controls on Worksheets
10. Code Examples from Official Documentation

**Out of Scope**: Word and Outlook VSTO APIs, Office Add-ins (JavaScript).

**Key Insight**: VSTO extends the COM Interop API with host items (extended Workbook/Worksheet) and host controls (NamedRange, ListObject) that add .NET events, data binding, and designer support. Access COM objects via `Globals.ThisAddIn.Application`.

`[VERIFIED] (https://learn.microsoft.com/en-us/dotnet/api/microsoft.office.tools.excel?view=vsto-2022)`

## 1. API Overview

### 1.1 VSTO Architecture

VSTO provides two layers on top of the Excel COM object model:

- **Primary Interop Assemblies (PIA)**: `Microsoft.Office.Interop.Excel` - Direct COM wrapper
- **VSTO Extensions**: `Microsoft.Office.Tools.Excel` - Host items, host controls, and enhanced features

### 1.2 Project Types

| Type | Description | Key Class |
|------|-------------|-----------|
| VSTO Add-in | Application-level, loads with Excel | `ThisAddIn` |
| Document-Level | Attached to specific workbook | `ThisWorkbook`, `Sheet1` |

### 1.3 Key Assemblies

- **Microsoft.Office.Tools.Excel.dll** - VSTO Excel extensions
- **Microsoft.Office.Tools.Common.dll** - Common VSTO types
- **Microsoft.Office.Interop.Excel.dll** - Excel PIA (COM wrapper)
- **Microsoft.Vbe.Interop.dll** - VBA project access

### 1.4 Runtime Requirements

- **VSTO Runtime**: Visual Studio 2010 Tools for Office Runtime
- **.NET Framework**: 4.7.2 or later (4.8 recommended)
- **Visual Studio**: 2022 with Office/SharePoint development workload

**COM Cleanup**: VSTO still wraps COM objects. Unsubscribe events in `ThisAddIn_Shutdown`, avoid storing COM references in class fields, and use `Marshal.ReleaseComObject()` for intensive loops. See `_INFO_AXCEL-IN02_COM_API.md` for full COM cleanup guidance.

## 2. VSTO Namespaces

`[VERIFIED] (https://learn.microsoft.com/en-us/dotnet/api/microsoft.office.tools.excel?view=vsto-2022)`

### 2.1 Microsoft.Office.Tools.Excel

Primary VSTO namespace for Excel extensions.

**Classes:**
- `WorkbookBase` - Base class for ThisWorkbook in document-level projects
- `WorksheetBase` - Base class for Sheet classes in document-level projects
- `ChartSheetBase` - Base class for chart sheet host items
- `ControlExtensions` - Extension methods to add Windows Forms controls

**Interfaces (Host Items):**
- `Workbook` - Extended workbook with VSTO features
- `Worksheet` - Extended worksheet with host controls and events
- `ChartSheet` - Extended chart sheet

**Interfaces (Host Controls):**
- `NamedRange` - Named range with events and data binding
- `ListObject` - Excel table with data binding support
- `Chart` - Embedded chart control
- `XmlMappedRange` - Range mapped to XML schema

**Interfaces (Infrastructure):**
- `Factory` - Creates host items and controls (document-level)
- `ApplicationFactory` - Creates host items and controls (add-in)
- `ControlCollection` - Collection of managed controls on worksheet

**Enums:**
- `ChangeReason` - Why ListObject data was restored
- `ChangeType` - How ListObject restored data
- `FailureReason` - Why data binding failed
- `FormatSettings` - Formatting applied to bound ListObject
- `ListRanges` - Which ListObject range changed

### 2.2 Microsoft.Office.Tools

Common VSTO namespace shared across Office applications.

**Key Types:**
- `AddInBase` - Base class for ThisAddIn
- `CustomTaskPane` - Custom task pane support
- `IRibbonExtension` - Ribbon customization interface
- `ActionsPaneControl` - Actions pane for document-level projects

### 2.3 Microsoft.Office.Interop.Excel

COM Interop namespace (not VSTO-specific but essential).

**Key Types:**
- `Application` - Excel application object
- `Workbook`, `Workbooks` - Workbook objects
- `Worksheet`, `Worksheets` - Worksheet objects
- `Range` - Cell/range object
- `Chart`, `Charts` - Chart objects

## 3. Host Items

Host items are VSTO wrappers around Excel objects that add .NET features.

`[VERIFIED] (https://learn.microsoft.com/en-us/visualstudio/vsto/excel-object-model-overview?view=vs-2022)`

### 3.1 Workbook Host Item

**Class**: `Microsoft.Office.Tools.Excel.WorkbookBase` (document-level)
**Interface**: `Microsoft.Office.Tools.Excel.Workbook`

**Key Properties:**
- `Application` - Excel Application object
- `InnerObject` - Underlying Interop.Excel.Workbook
- `VstoSmartTags` - Smart tags collection (deprecated)
- `DefaultSaveFormat` - Default save format

**Key Methods:**
- `GetVstoObject()` - Get VSTO wrapper for native workbook
- `Save()`, `SaveAs()` - Save workbook
- `Close()` - Close workbook

**Key Events:**
- `BeforeClose` - Before workbook closes
- `BeforeSave` - Before workbook saves
- `Open` - When workbook opens
- `SheetChange` - Any sheet cell changes
- `SheetSelectionChange` - Selection changes on any sheet
- `NewSheet` - New sheet added
- `SheetActivate`, `SheetDeactivate` - Sheet focus changes

### 3.2 Worksheet Host Item

**Class**: `Microsoft.Office.Tools.Excel.WorksheetBase` (document-level)
**Interface**: `Microsoft.Office.Tools.Excel.Worksheet`

**Key Properties:**
- `Application` - Excel Application object
- `InnerObject` - Underlying Interop.Excel.Worksheet
- `Controls` - ControlCollection of host controls
- `Name` - Sheet name
- `Range` - Access Range object
- `Cells` - All cells
- `Rows`, `Columns` - Row/column collections
- `UsedRange` - Used range

**Key Methods:**
- `GetVstoObject()` - Get VSTO wrapper for native worksheet
- `Range()` - Get Range by address or name
- `Activate()` - Activate sheet
- `Calculate()` - Recalculate sheet
- `Delete()` - Delete sheet
- `Copy()`, `Move()` - Copy/move sheet
- `PrintOut()`, `PrintPreview()` - Print sheet

**Key Events:**
- `Change` - Cell value changed
- `SelectionChange` - Selection changed
- `BeforeDoubleClick` - Before double-click
- `BeforeRightClick` - Before right-click
- `Activate`, `Deactivate` - Sheet focus changes
- `Calculate` - After sheet calculates
- `FollowHyperlink` - Hyperlink clicked

### 3.3 ChartSheet Host Item

**Class**: `Microsoft.Office.Tools.Excel.ChartSheetBase`
**Interface**: `Microsoft.Office.Tools.Excel.ChartSheet`

Represents a chart that occupies an entire sheet.

**Key Properties:**
- `InnerObject` - Underlying Interop.Excel.Chart
- `ChartType` - Type of chart
- `HasTitle` - Whether chart has title
- `ChartTitle` - Chart title object

**Key Events:**
- `Activate`, `Deactivate` - Focus changes
- `Calculate` - Chart recalculated
- `Resize` - Chart resized
- `Select` - Element selected
- `SeriesChange` - Series data changed

## 4. Host Controls

Host controls extend native Excel objects with .NET events and data binding.

### 4.1 NamedRange Control

**Interface**: `Microsoft.Office.Tools.Excel.NamedRange`

A range with a name, events, and simple data binding support.

`[VERIFIED] (https://learn.microsoft.com/en-us/visualstudio/vsto/namedrange-control?view=vs-2022)`

**Key Properties:**
- `Name` - Range name
- `Value`, `Value2` - Cell values
- `Formula`, `FormulaR1C1` - Formulas
- `Text` - Display text
- `Address` - Cell address
- `Cells`, `Rows`, `Columns` - Sub-ranges
- `RefersTo` - Reference string
- `InnerObject` - Underlying Interop.Excel.Range

**Key Methods:**
- `Select()` - Select the range
- `Copy()`, `Cut()`, `Clear()` - Clipboard operations
- `Delete()` - Delete cells
- `AutoFit()` - Auto-fit columns/rows
- `Find()`, `FindNext()` - Search
- `Sort()` - Sort range
- `Merge()`, `UnMerge()` - Merge cells

**Key Events:**
- `Change` - Value changed
- `SelectionChange` - Selection within range changed
- `BeforeDoubleClick` - Before double-click
- `BeforeRightClick` - Before right-click

**Data Binding:**
- Supports simple binding via `DataBindings.Add()`
- Single value binding only (not multi-cell)

### 4.2 ListObject Control

**Interface**: `Microsoft.Office.Tools.Excel.ListObject`

An Excel table with complex data binding support.

`[VERIFIED] (https://learn.microsoft.com/en-us/visualstudio/vsto/how-to-add-listobject-controls-to-worksheets?view=vs-2022)`

**Key Properties:**
- `Name` - Table name
- `Range` - Table range
- `DataSource` - Bound data source
- `DataMember` - Data member name
- `HeaderRowRange` - Header row
- `DataBodyRange` - Data rows
- `TotalsRowRange` - Totals row
- `ListColumns` - Column collection
- `ListRows` - Row collection
- `ShowHeaders` - Show header row
- `ShowTotals` - Show totals row
- `AutoSetDataBoundColumnHeaders` - Auto-set headers from data

**Key Methods:**
- `SetDataBinding()` - Bind to data source
- `Disconnect()` - Disconnect from data source
- `Resize()` - Resize table
- `Delete()` - Delete table

**Key Events:**
- `Change` - Cell changed in table
- `SelectedIndexChanged` - Selection changed
- `BeforeAddDataBoundRow` - Before adding bound row
- `ErrorAddDataBoundRow` - Error adding bound row
- `OriginalDataRestored` - Data restored after edit rejected

**Data Binding:**
- Complex binding to DataTable, List<T>, BindingSource
- Automatic column mapping
- Two-way binding support

### 4.3 Chart Control

**Interface**: `Microsoft.Office.Tools.Excel.Chart`

An embedded chart with events.

**Key Properties:**
- `ChartType` - Type of chart (XlChartType enum)
- `HasTitle` - Has chart title
- `ChartTitle` - Title object
- `Legend` - Legend object
- `PlotArea` - Plot area
- `ChartArea` - Chart area
- `SeriesCollection` - Data series

**Key Methods:**
- `SetSourceData()` - Set data range
- `ApplyLayout()` - Apply chart layout
- `Export()` - Export as image
- `Delete()` - Delete chart

**Key Events:**
- `Activate`, `Deactivate` - Focus changes
- `Calculate` - Chart recalculated
- `Resize` - Chart resized
- `Select` - Element selected

### 4.4 XmlMappedRange Control

**Interface**: `Microsoft.Office.Tools.Excel.XmlMappedRange`

A range mapped to an XML schema element.

**Key Properties:**
- `XPath` - XPath expression
- `Value`, `Value2` - Cell values
- Similar to NamedRange

**Key Events:**
- `Change` - Value changed
- `SelectionChange` - Selection changed

## 5. Globals Class and Factory

### 5.1 Globals Class

Static class providing access to VSTO objects from anywhere in the project.

**Add-in Projects:**
```csharp
// Access Excel Application
Excel.Application app = Globals.ThisAddIn.Application;

// Access Factory for creating host items
Microsoft.Office.Tools.Excel.ApplicationFactory factory = Globals.Factory;
```

**Document-Level Projects:**
```csharp
// Access ThisWorkbook
Globals.ThisWorkbook

// Access Sheet1, Sheet2, etc.
Globals.Sheet1

// Access Factory
Globals.Factory
```

### 5.2 ApplicationFactory (Add-in)

**Interface**: `Microsoft.Office.Tools.Excel.ApplicationFactory`

Creates host items from native Excel objects in add-in projects.

**Key Methods:**
- `HasVstoObject(Workbook/Worksheet)` - Check if host item already exists
- `GetVstoObject(Workbook)` - Get Workbook host item
- `GetVstoObject(Worksheet)` - Get Worksheet host item
- `CreateListObject()` - Create ListObject
- `CreateSmartTag()` - Create smart tag (deprecated)

**Note**: Use `HasVstoObject()` before `GetVstoObject()` to check if a host item already exists for the native object.

**Usage:**
```csharp
// Convert native worksheet to VSTO host item
Excel.Worksheet nativeSheet = Globals.ThisAddIn.Application.ActiveSheet;
Microsoft.Office.Tools.Excel.Worksheet vstoSheet = 
    Globals.Factory.GetVstoObject(nativeSheet);

// Now can add host controls
NamedRange range = vstoSheet.Controls.AddNamedRange(
    vstoSheet.Range["A1:B5"], "MyRange");
```

### 5.3 Factory (Document-Level)

**Interface**: `Microsoft.Office.Tools.Excel.Factory`

Similar to ApplicationFactory but for document-level projects.

## 6. Application-Level Events

Excel Application events available through VSTO.

### 6.1 Workbook Events

```csharp
private void ThisAddIn_Startup(object sender, EventArgs e)
{
    this.Application.WorkbookOpen += Application_WorkbookOpen;
    this.Application.WorkbookBeforeClose += Application_WorkbookBeforeClose;
    this.Application.WorkbookBeforeSave += Application_WorkbookBeforeSave;
    this.Application.WorkbookNewSheet += Application_WorkbookNewSheet;
}
```

**Events:**
- `WorkbookOpen` - Workbook opened
- `WorkbookBeforeClose` - Before workbook closes
- `WorkbookBeforeSave` - Before workbook saves
- `WorkbookAfterSave` - After workbook saves (Excel 2010+)
- `WorkbookNewSheet` - New sheet created
- `WorkbookActivate`, `WorkbookDeactivate` - Focus changes
- `NewWorkbook` - New workbook created

### 6.2 Sheet Events

```csharp
this.Application.SheetChange += Application_SheetChange;
this.Application.SheetSelectionChange += Application_SheetSelectionChange;
this.Application.SheetActivate += Application_SheetActivate;
```

**Events:**
- `SheetChange` - Cell changed on any sheet
- `SheetSelectionChange` - Selection changed on any sheet
- `SheetActivate`, `SheetDeactivate` - Sheet focus changes
- `SheetBeforeDoubleClick` - Before double-click
- `SheetBeforeRightClick` - Before right-click
- `SheetCalculate` - Sheet recalculated
- `SheetFollowHyperlink` - Hyperlink clicked

### 6.3 Window Events

- `WindowActivate`, `WindowDeactivate` - Window focus
- `WindowResize` - Window resized

## 7. Ribbon Customization

### 7.1 Ribbon Designer

Visual Studio provides a Ribbon Designer for creating custom ribbons.

**Key Classes:**
- `Microsoft.Office.Tools.Ribbon.RibbonBase` - Base class for ribbons
- `RibbonTab` - Custom tab
- `RibbonGroup` - Group within tab
- `RibbonButton` - Button control
- `RibbonToggleButton` - Toggle button
- `RibbonCheckBox` - Checkbox
- `RibbonComboBox` - Dropdown
- `RibbonEditBox` - Text input
- `RibbonGallery` - Gallery control
- `RibbonMenu` - Menu
- `RibbonSplitButton` - Split button
- `RibbonSeparator` - Separator

### 7.2 Ribbon XML

Alternative approach using Ribbon XML for more control.

**Interface**: `Microsoft.Office.Core.IRibbonExtensibility`

```csharp
public class Ribbon1 : Office.IRibbonExtensibility
{
    public string GetCustomUI(string ribbonID)
    {
        return GetResourceText("MyAddin.Ribbon1.xml");
    }
    
    public void OnButtonClick(Office.IRibbonControl control)
    {
        // Handle button click
    }
}
```

## 8. Data Binding

### 8.1 Simple Data Binding (NamedRange)

```csharp
// Bind NamedRange to single value
this.namedRange1.DataBindings.Add("Value2", 
    myDataSource, "PropertyName");
```

### 8.2 Complex Data Binding (ListObject)

```csharp
// Bind ListObject to DataTable
DataTable table = GetDataTable();
this.listObject1.SetDataBinding(table);

// Or bind with column mapping
this.listObject1.SetDataBinding(table, "", 
    "Column1", "Column2", "Column3");

// Bind to List<T>
List<Customer> customers = GetCustomers();
this.listObject1.SetDataBinding(customers);

// With headers auto-set
this.listObject1.AutoSetDataBoundColumnHeaders = true;
```

### 8.3 Disconnecting Data

```csharp
// Disconnect but keep data
this.listObject1.Disconnect();

// Data remains in worksheet but no longer bound
```

## 9. Windows Forms Controls on Worksheets

VSTO allows adding Windows Forms controls to worksheets.

### 9.1 Adding Controls

```csharp
// Get VSTO worksheet
var vstoSheet = Globals.Factory.GetVstoObject(
    Globals.ThisAddIn.Application.ActiveSheet);

// Add Button
System.Windows.Forms.Button button = 
    vstoSheet.Controls.AddButton(
        vstoSheet.Range["A1"], "myButton");
button.Text = "Click Me";
button.Click += Button_Click;

// Add ComboBox
System.Windows.Forms.ComboBox combo = 
    vstoSheet.Controls.AddComboBox(
        vstoSheet.Range["B1:C1"], "myCombo");
combo.Items.AddRange(new[] { "Option 1", "Option 2" });

// Add TextBox
System.Windows.Forms.TextBox textBox = 
    vstoSheet.Controls.AddTextBox(
        vstoSheet.Range["D1:E1"], "myTextBox");
```

### 9.2 ControlCollection

**Interface**: `Microsoft.Office.Tools.Excel.ControlCollection`

**Key Methods:**
- `AddButton()`, `AddCheckBox()`, `AddComboBox()`
- `AddListBox()`, `AddTextBox()`, `AddLabel()`
- `AddNamedRange()`, `AddListObject()`, `AddChart()`
- `Remove()` - Remove control by name
- `Contains()` - Check if control exists

### 9.3 ControlExtensions

Static extension methods for adding controls.

```csharp
using Microsoft.Office.Tools.Excel;

// Extension method usage
worksheet.Controls.AddButton(range, "buttonName");
```

## 10. Code Examples from Official Documentation

### 10.1 VSTO Add-in Startup

```csharp
using Excel = Microsoft.Office.Interop.Excel;

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
        System.Diagnostics.Debug.WriteLine($"Opened: {wb.Name}");
    }
    
    private void ExcelApp_SheetChange(object sheet, Excel.Range target)
    {
        System.Diagnostics.Debug.WriteLine($"Changed: {target.Address}");
    }
    
    private void ThisAddIn_Shutdown(object sender, EventArgs e)
    {
        // Cleanup
    }
}
```

`[VERIFIED] (https://learn.microsoft.com/en-us/visualstudio/vsto/walkthrough-creating-your-first-vsto-add-in-for-excel?view=vs-2022)`

### 10.2 Adding Host Controls at Runtime

```csharp
private void AddControlsToWorksheet()
{
    // Get active worksheet as VSTO host item
    Excel.Worksheet nativeSheet = 
        Globals.ThisAddIn.Application.ActiveSheet;
    
    Microsoft.Office.Tools.Excel.Worksheet vstoSheet = 
        Globals.Factory.GetVstoObject(nativeSheet);
    
    // Add NamedRange
    Microsoft.Office.Tools.Excel.NamedRange namedRange =
        vstoSheet.Controls.AddNamedRange(
            vstoSheet.Range["A1:B5"], "CustomerRange");
    
    namedRange.Change += NamedRange_Change;
    
    // Add ListObject
    Microsoft.Office.Tools.Excel.ListObject listObject =
        vstoSheet.Controls.AddListObject(
            vstoSheet.Range["D1:G10"], "CustomerList");
    
    listObject.Change += ListObject_Change;
}

private void NamedRange_Change(
    Microsoft.Office.Tools.Excel.NamedRange target)
{
    MessageBox.Show("NamedRange changed!");
}

private void ListObject_Change(
    Excel.Range targetRange, ListRanges changedRanges)
{
    MessageBox.Show("ListObject changed!");
}
```

`[VERIFIED] (https://learn.microsoft.com/en-us/visualstudio/vsto/walkthrough-adding-controls-to-a-worksheet-at-run-time-in-vsto-add-in-project?view=vs-2022)`

### 10.3 Data Binding ListObject to DataTable

```csharp
private void BindListObjectToData()
{
    // Create sample data
    DataTable table = new DataTable("Customers");
    table.Columns.Add("ID", typeof(int));
    table.Columns.Add("Name", typeof(string));
    table.Columns.Add("Email", typeof(string));
    
    table.Rows.Add(1, "John Doe", "john@example.com");
    table.Rows.Add(2, "Jane Smith", "jane@example.com");
    
    // Get worksheet host item
    var vstoSheet = Globals.Factory.GetVstoObject(
        Globals.ThisAddIn.Application.ActiveSheet);
    
    // Create and bind ListObject
    var listObject = vstoSheet.Controls.AddListObject(
        vstoSheet.Range["A1:C3"], "CustomerTable");
    
    listObject.AutoSetDataBoundColumnHeaders = true;
    listObject.SetDataBinding(table);
}
```

`[VERIFIED] (https://learn.microsoft.com/en-us/visualstudio/vsto/how-to-add-listobject-controls-to-worksheets?view=vs-2022)`

### 10.4 Custom Ribbon Button

```csharp
// In Ribbon1.cs (using Ribbon Designer)
private void button1_Click(object sender, RibbonControlEventArgs e)
{
    Excel.Application app = Globals.ThisAddIn.Application;
    Excel.Worksheet ws = app.ActiveSheet;
    
    // Write to active sheet
    ws.Range["A1"].Value = "Hello from VSTO!";
    ws.Range["B1"].Formula = "=NOW()";
    
    // Format
    ws.Range["A1:B1"].Font.Bold = true;
    ws.Range["A1:B1"].Interior.Color = 
        System.Drawing.ColorTranslator.ToOle(System.Drawing.Color.Yellow);
}
```

### 10.5 Document-Level Worksheet Event

```csharp
// In Sheet1.cs (document-level project)
public partial class Sheet1
{
    private void Sheet1_Startup(object sender, EventArgs e)
    {
        this.Change += Sheet1_Change;
        this.SelectionChange += Sheet1_SelectionChange;
    }

    private void Sheet1_Change(Excel.Range target)
    {
        // Respond to changes in this sheet
        if (target.Column == 1) // Column A
        {
            // Validate or process
            target.Offset[0, 1].Value = DateTime.Now;
        }
    }

    private void Sheet1_SelectionChange(Excel.Range target)
    {
        // Update status or actions pane
        System.Diagnostics.Debug.WriteLine($"Selected: {target.Address}");
    }
}
```

### 10.6 Export VBA Modules

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
            vbext_ComponentType.vbext_ct_Document => ".cls",
            _ => ".txt"
        };
        
        if (comp.CodeModule.CountOfLines > 0)
        {
            comp.Export(Path.Combine(exportPath, comp.Name + ext));
        }
    }
}
```

## Document History

**[2026-02-27 13:58]**
- Added: COM cleanup warning in Section 1.4
- Added: HasVstoObject method and note in Section 5.2
- Review: `_INFO_AXCEL-IN08_VSTO_API_REVIEW.md` findings addressed

**[2026-02-27 Session]**
- Created: Comprehensive VSTO Excel API reference document
- Source: Microsoft Learn Microsoft.Office.Tools.Excel Namespace
- Coverage: 3 namespaces, host items, host controls, data binding
- Added: Globals/Factory patterns, Ribbon customization
- Added: Code examples from official documentation
