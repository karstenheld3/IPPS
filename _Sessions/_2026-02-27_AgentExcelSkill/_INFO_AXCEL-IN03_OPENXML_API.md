# INFO: Open XML SDK Complete API Reference

**Doc ID**: AXCEL-IN03-API
**Goal**: Comprehensive documentation of all Open XML SDK classes for Excel/SpreadsheetML manipulation
**Version Scope**: Open XML SDK 3.0+ (2026-02-27)
**Source**: Microsoft Learn - DocumentFormat.OpenXml Namespace

**Depends on:**
- `_INFO_AXCEL-IN03_OPENXML.md [AXCEL-IN03]` for Open XML SDK overview and usage

## Table of Contents

1. Namespace Overview
2. Packaging Classes (DocumentFormat.OpenXml.Packaging)
3. Spreadsheet Classes (DocumentFormat.OpenXml.Spreadsheet)
4. Core Document Elements
5. Cell and Data Classes
6. Formatting Classes
7. Table and PivotTable Classes
8. Chart Classes
9. Shared String and Comment Classes
10. Enumerations
11. Common Patterns
12. Code Examples from Official Documentation

**Out of Scope**: Word (WordprocessingML) and PowerPoint (PresentationML) classes.

**Key Insight**: Open XML SDK provides strongly-typed classes that map directly to the XML elements in SpreadsheetML (.xlsx files). Unlike COM/VBA, there is no formula calculation - formulas are stored as text strings.

`[VERIFIED] (https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.spreadsheet?view=openxml-3.0.1)`

## 1. Namespace Overview

### 1.1 Package Information

- **NuGet Package**: DocumentFormat.OpenXml (v3.0+)
- **Primary Namespace**: DocumentFormat.OpenXml.Packaging
- **Spreadsheet Namespace**: DocumentFormat.OpenXml.Spreadsheet
- **Target Frameworks**: .NET Framework 4.6.2+, .NET 5/6/7/8+

**Thread Safety**: Open XML SDK is NOT thread-safe. Multiple threads cannot safely access the same SpreadsheetDocument, even for read-only operations. Each thread should open its own document instance.

### 1.2 Namespace Structure

```
DocumentFormat.OpenXml
├── Packaging
│   ├── SpreadsheetDocument        # Main document class
│   ├── WorkbookPart               # Contains Workbook
│   ├── WorksheetPart              # Contains Worksheet
│   ├── SharedStringTablePart      # Shared strings
│   └── WorkbookStylesPart         # Styles
├── Spreadsheet
│   ├── Workbook, Worksheet        # Structure elements
│   ├── SheetData, Row, Cell       # Data elements
│   ├── CellValue, CellFormula     # Cell contents
│   ├── Font, Fill, Border         # Formatting
│   └── PivotTable, Table          # Data features
└── Office2013.Excel               # Excel 2013+ features
```

### 1.3 Class Count by Category

- **Packaging classes**: 50+ (document parts and relationships)
- **Spreadsheet classes**: 500+ (SpreadsheetML elements)
- **Enumerations**: 100+ (value constraints)

## 2. Packaging Classes

The `DocumentFormat.OpenXml.Packaging` namespace contains classes for working with the Open XML package structure.

`[VERIFIED] (https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.packaging?view=openxml-3.0.1)`

### 2.1 SpreadsheetDocument Class

The main entry point for Excel documents.

**Static Methods:**
- Create(string, SpreadsheetDocumentType) - Create new document
- Create(Stream, SpreadsheetDocumentType) - Create to stream
- CreateFromTemplate(string) - Create from template
- Open(string, bool) - Open existing document
- Open(Stream, bool) - Open from stream

**Instance Properties:**
- WorkbookPart - Gets the WorkbookPart
- DocumentType - Gets the document type
- Package - Gets the underlying package

**Instance Methods:**
- AddWorkbookPart() - Add workbook part
- Save() - Save changes
- Clone() - Clone document
- Dispose() - Release resources

### 2.2 WorkbookPart Class

Contains the workbook and links to all worksheet parts.

**Properties:**
- Workbook - Gets/sets the Workbook element
- SharedStringTablePart - Shared strings
- WorkbookStylesPart - Styles
- WorksheetParts - All worksheet parts
- GetPartsOfType<T>() - Get parts by type

**Methods:**
- AddNewPart<T>() - Add new part
- GetIdOfPart(OpenXmlPart) - Get relationship ID
- GetPartById(string) - Get part by ID

### 2.3 WorksheetPart Class

Contains a single worksheet.

**Properties:**
- Worksheet - Gets/sets the Worksheet element
- DrawingsPart - Drawings/charts
- TableDefinitionParts - Tables
- PivotTableParts - Pivot tables

**Methods:**
- AddNewPart<T>() - Add new part
- GetIdOfPart(OpenXmlPart) - Get relationship ID

### 2.4 SharedStringTablePart Class

Contains shared strings for efficient storage.

**Properties:**
- SharedStringTable - Gets/sets the SharedStringTable element

### 2.5 WorkbookStylesPart Class

Contains styles (fonts, fills, borders, cell formats).

**Properties:**
- Stylesheet - Gets/sets the Stylesheet element

### 2.6 Other Part Classes

- **ChartPart** - Chart data and formatting
- **TableDefinitionPart** - Table definitions
- **PivotTablePart** - Pivot table definitions
- **PivotTableCacheDefinitionPart** - Pivot cache
- **DrawingsPart** - Drawings and shapes
- **VmlDrawingPart** - VML drawings (legacy)
- **ThemePart** - Document theme
- **CalculationChainPart** - Calculation order

## 3. Spreadsheet Classes

The `DocumentFormat.OpenXml.Spreadsheet` namespace contains 500+ classes representing SpreadsheetML elements.

`[VERIFIED] (https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.spreadsheet?view=openxml-3.0.1)`

### 3.1 Workbook Class

Root element of the workbook.

**Child Elements:**
- FileVersion, FileSharing, WorkbookProperties
- WorkbookProtection, BookViews
- Sheets - Collection of Sheet references
- DefinedNames - Named ranges/formulas
- CalculationProperties
- PivotCaches, WebPublishing
- ExtensionList

**Properties (inherited from OpenXmlElement):**
- Parent, FirstChild, LastChild
- ChildElements, Descendants()
- InnerText, InnerXml, OuterXml

**Methods:**
- Append(params OpenXmlElement[])
- PrependChild<T>(T)
- AppendChild<T>(T)
- RemoveChild<T>(T)
- GetFirstChild<T>()
- Elements<T>()
- Save()

### 3.2 Sheets Class

Collection of Sheet elements.

**Child Elements:**
- Sheet - Reference to worksheet

### 3.3 Sheet Class

References a worksheet part.

**Properties:**
- Id (StringValue) - Relationship ID to WorksheetPart
- SheetId (UInt32Value) - Unique sheet ID
- Name (StringValue) - Sheet name
- State (EnumValue<SheetStateValues>) - Hidden/visible

### 3.4 Worksheet Class

Root element of a worksheet part.

**Child Elements:**
- SheetProperties, SheetDimension
- SheetViews - View settings
- SheetFormatProperties
- Columns - Column definitions
- SheetData - Cell data (main content)
- SheetCalculationProperties
- SheetProtection, AutoFilter
- MergeCells - Merged cell ranges
- ConditionalFormatting
- DataValidations
- Hyperlinks, PrintOptions
- PageMargins, PageSetup
- HeaderFooter, Drawing
- LegacyDrawing, TableParts
- ExtensionList

## 4. Core Document Elements

### 4.1 SheetData Class

Container for all row and cell data.

**Child Elements:**
- Row - Data rows

**Usage Pattern:**
```csharp
SheetData sheetData = worksheet.GetFirstChild<SheetData>();
foreach (Row row in sheetData.Elements<Row>())
{
    foreach (Cell cell in row.Elements<Cell>())
    {
        // Process cell
    }
}
```

### 4.2 Row Class

Represents a row of cells.

**Properties:**
- RowIndex (UInt32Value) - 1-based row number
- Spans (ListValue<StringValue>) - Column spans
- Height (DoubleValue) - Row height
- CustomHeight (BooleanValue) - Custom height flag
- Hidden (BooleanValue) - Hidden flag
- StyleIndex (UInt32Value) - Style reference
- Collapsed (BooleanValue) - Collapsed state
- OutlineLevel (ByteValue) - Outline level

**Child Elements:**
- Cell - Cells in this row

### 4.3 Columns Class

Container for column definitions.

**Child Elements:**
- Column - Column properties

### 4.4 Column Class

Defines column width and formatting.

**Properties:**
- Min (UInt32Value) - First column (1-based)
- Max (UInt32Value) - Last column (1-based)
- Width (DoubleValue) - Column width
- CustomWidth (BooleanValue) - Custom width flag
- Style (UInt32Value) - Default cell style
- Hidden (BooleanValue) - Hidden flag
- BestFit (BooleanValue) - Auto-fit flag
- Collapsed (BooleanValue) - Collapsed state
- OutlineLevel (ByteValue) - Outline level

## 5. Cell and Data Classes

### 5.1 Cell Class

Represents a single cell.

**Date Handling**: Dates are stored as serial numbers (days since 1899-12-30 for 1900 date system, or 1904-01-01 for 1904 date system). Use `DateTime.FromOADate(double)` to convert. Check `Workbook.WorkbookProperties.Date1904` for date system.

**Properties:**
- CellReference (StringValue) - Cell address (e.g., "A1")
- StyleIndex (UInt32Value) - Style reference
- DataType (EnumValue<CellValues>) - Cell data type
- CellMetaIndex (UInt32Value) - Metadata index
- ValueMetaIndex (UInt32Value) - Value metadata
- ShowPhonetic (BooleanValue) - Show phonetic

**Child Elements:**
- CellFormula - Formula (if any)
- CellValue - Cell value
- InlineString - Inline rich text
- ExtensionList

### 5.2 CellValue Class

Contains the cell's value.

**Properties:**
- Text - The value as string

**Usage:**
```csharp
Cell cell = new Cell() { CellReference = "A1" };
cell.CellValue = new CellValue("Hello");
cell.DataType = CellValues.String;
```

### 5.3 CellFormula Class

Contains a formula.

**Properties:**
- Text - Formula string (without = prefix)
- FormulaType (EnumValue<CellFormulaValues>) - Normal, Array, DataTable, Shared
- Reference (StringValue) - Range for array/shared formulas
- SharedIndex (UInt32Value) - Shared formula index
- AlwaysCalculateArray (BooleanValue) - Force calculation
- CalculateCell (BooleanValue) - Calculate on open
- DataTable2D (BooleanValue) - 2D data table
- DataTableRow (BooleanValue) - Data table row
- Input1Deleted (BooleanValue) - Input 1 deleted
- Input2Deleted (BooleanValue) - Input 2 deleted
- R1 (StringValue) - Input cell 1
- R2 (StringValue) - Input cell 2

### 5.4 CellValues Enum

Defines cell data types.

**Values:**
- Boolean - Boolean value
- Date - Date value (stored as number)
- Error - Error value
- InlineString - Inline string
- Number - Numeric value (default)
- SharedString - Index to shared string table
- String - String value

### 5.5 SharedStringTable Class

Contains shared strings for the workbook.

**Child Elements:**
- SharedStringItem - Individual shared strings

**Properties:**
- Count (UInt32Value) - Total references
- UniqueCount (UInt32Value) - Unique strings

### 5.6 SharedStringItem Class

A single shared string.

**Child Elements:**
- Text - Plain text content
- PhoneticRun - Phonetic text
- Run - Rich text run

## 6. Formatting Classes

### 6.1 Stylesheet Class

Root element for styles.

**Child Elements:**
- NumberingFormats - Number formats
- Fonts - Font definitions
- Fills - Fill definitions
- Borders - Border definitions
- CellStyleFormats - Base cell styles
- CellFormats - Cell format combinations
- CellStyles - Named styles
- DifferentialFormats - Conditional formats
- TableStyles - Table styles
- Colors - Color palette
- ExtensionList

### 6.2 Fonts Class

Collection of font definitions.

**Child Elements:**
- Font

### 6.3 Font Class

Font definition.

**Child Elements:**
- Bold, Italic, Underline, Strike
- Condense, Extend, Outline, Shadow
- Color - Font color
- FontSize - Size in points
- FontName - Font family name
- FontFamilyNumbering - Font family
- FontCharSet - Character set
- FontScheme - Theme font

### 6.4 Fills Class

Collection of fill definitions.

**Child Elements:**
- Fill

### 6.5 Fill Class

Fill definition.

**Child Elements:**
- PatternFill - Pattern fill
- GradientFill - Gradient fill

### 6.6 PatternFill Class

Pattern-based fill.

**Properties:**
- PatternType (EnumValue<PatternValues>) - Pattern type

**Child Elements:**
- ForegroundColor - Pattern foreground
- BackgroundColor - Pattern background

### 6.7 PatternValues Enum

**Values:** None, Solid, MediumGray, DarkGray, LightGray, DarkHorizontal, DarkVertical, DarkDown, DarkUp, DarkGrid, DarkTrellis, LightHorizontal, LightVertical, LightDown, LightUp, LightGrid, LightTrellis, Gray125, Gray0625

### 6.8 Borders Class

Collection of border definitions.

**Child Elements:**
- Border

### 6.9 Border Class

Border definition.

**Child Elements:**
- LeftBorder, RightBorder
- TopBorder, BottomBorder
- DiagonalBorder
- Vertical, Horizontal

**Properties:**
- DiagonalUp (BooleanValue)
- DiagonalDown (BooleanValue)
- Outline (BooleanValue)

### 6.10 BorderStyleValues Enum

**Values:** None, Thin, Medium, Dashed, Dotted, Thick, Double, Hair, MediumDashed, DashDot, MediumDashDot, DashDotDot, MediumDashDotDot, SlantDashDot

### 6.11 CellFormats Class

Collection of cell format combinations.

**Child Elements:**
- CellFormat

### 6.12 CellFormat Class

Combines font, fill, border, number format.

**Properties:**
- NumberFormatId (UInt32Value) - Number format
- FontId (UInt32Value) - Font index
- FillId (UInt32Value) - Fill index
- BorderId (UInt32Value) - Border index
- FormatId (UInt32Value) - Base format
- ApplyNumberFormat (BooleanValue)
- ApplyFont (BooleanValue)
- ApplyFill (BooleanValue)
- ApplyBorder (BooleanValue)
- ApplyAlignment (BooleanValue)
- ApplyProtection (BooleanValue)

**Child Elements:**
- Alignment - Text alignment
- Protection - Cell protection

### 6.13 Alignment Class

Cell alignment settings.

**Properties:**
- Horizontal (EnumValue<HorizontalAlignmentValues>)
- Vertical (EnumValue<VerticalAlignmentValues>)
- TextRotation (UInt32Value) - 0-180 degrees
- WrapText (BooleanValue)
- Indent (UInt32Value)
- ShrinkToFit (BooleanValue)
- ReadingOrder (UInt32Value)
- JustifyLastLine (BooleanValue)

### 6.14 HorizontalAlignmentValues Enum

**Values:** General, Left, Center, Right, Fill, Justify, CenterContinuous, Distributed

### 6.15 VerticalAlignmentValues Enum

**Values:** Top, Center, Bottom, Justify, Distributed

## 7. Table and PivotTable Classes

### 7.1 Table Class

Represents an Excel table (ListObject).

**Properties:**
- Id (UInt32Value) - Table ID
- Name (StringValue) - Table name
- DisplayName (StringValue) - Display name
- Reference (StringValue) - Range reference
- TotalsRowCount (UInt32Value) - Totals rows
- HeaderRowCount (UInt32Value) - Header rows

**Child Elements:**
- AutoFilter - Auto filter settings
- SortState - Sort settings
- TableColumns - Column definitions
- TableStyleInfo - Table style

### 7.2 TableColumns Class

Collection of table columns.

**Child Elements:**
- TableColumn

### 7.3 TableColumn Class

Table column definition.

**Properties:**
- Id (UInt32Value) - Column ID
- Name (StringValue) - Column name
- TotalsRowFunction (EnumValue<TotalsRowFunctionValues>)
- TotalsRowLabel (StringValue)
- DataFormatId (UInt32Value)

**Child Elements:**
- CalculatedColumnFormula
- TotalsRowFormula

### 7.4 TotalsRowFunctionValues Enum

**Values:** None, Sum, Min, Max, Average, Count, CountNumbers, StdDev, Var, Custom

### 7.5 PivotTableDefinition Class

Root element for pivot tables.

**Properties:**
- Name (StringValue) - Pivot table name
- CacheId (UInt32Value) - Cache ID
- DataCaption (StringValue) - Data caption
- RowHeaderCaption (StringValue)
- ColHeaderCaption (StringValue)
- Outline (BooleanValue)
- OutlineData (BooleanValue)
- CompactData (BooleanValue)
- GridDropZones (BooleanValue)
- ShowHeaders (BooleanValue)
- PageOverThenDown (BooleanValue)

**Child Elements:**
- Location - Position in worksheet
- PivotFields - Field definitions
- RowFields, RowItems
- ColumnFields, ColumnItems
- PageFields - Page/filter fields
- DataFields - Value fields
- ConditionalFormats
- PivotTableStyle

### 7.6 PivotField Class

Pivot table field definition.

**Properties:**
- Name (StringValue)
- Axis (EnumValue<PivotTableAxisValues>)
- ShowAll (BooleanValue)
- Compact (BooleanValue)
- Outline (BooleanValue)
- SubtotalTop (BooleanValue)
- InsertBlankRow (BooleanValue)
- ServerField (BooleanValue)
- DefaultSubtotal (BooleanValue)
- SumSubtotal, CountSubtotal
- AvgSubtotal, MaxSubtotal, MinSubtotal

### 7.7 DataField Class

Pivot table value field.

**Properties:**
- Name (StringValue) - Display name
- Field (UInt32Value) - Field index
- Subtotal (EnumValue<DataConsolidateFunctionValues>)
- ShowDataAs (EnumValue<ShowDataAsValues>)
- BaseField (Int32Value)
- BaseItem (UInt32Value)
- NumberFormatId (UInt32Value)

### 7.8 DataConsolidateFunctionValues Enum

**Values:** Average, Count, CountNumbers, Max, Min, Product, StdDev, StdDevP, Sum, Var, VarP

## 8. Chart Classes

### 8.1 ChartSpace Class

Root element for charts (in Drawing namespace).

Located in `DocumentFormat.OpenXml.Drawing.Charts`

**Child Elements:**
- Date1904 - Date system
- EditingLanguage
- RoundedCorners
- Style - Chart style
- Chart - Main chart element
- PrintSettings
- UserShapes
- ExtensionList

### 8.2 Chart Class

Main chart container.

**Child Elements:**
- Title - Chart title
- AutoTitleDeleted
- PivotFormats
- View3D - 3D view settings
- Floor, SideWall, BackWall
- PlotArea - Plot area
- Legend - Legend
- PlotVisibleOnly
- DisplayBlanksAs
- ShowDataLabelsOverMaximum
- ExtensionList

### 8.3 PlotArea Class

Contains chart series.

**Child Elements (one or more):**
- AreaChart, Area3DChart
- BarChart, Bar3DChart
- LineChart, Line3DChart
- PieChart, Pie3DChart
- DoughnutChart
- ScatterChart, BubbleChart
- RadarChart
- StockChart, SurfaceChart

## 9. Shared String and Comment Classes

### 9.1 Comments Class

Root element for comments.

**Child Elements:**
- Authors - Comment authors
- CommentList - All comments

### 9.2 CommentList Class

Collection of comments.

**Child Elements:**
- Comment

### 9.3 Comment Class

A single comment.

**Properties:**
- Reference (StringValue) - Cell reference
- AuthorId (UInt32Value) - Author index
- Guid (StringValue) - Comment GUID

**Child Elements:**
- CommentText - Comment content

### 9.4 DefinedNames Class

Named ranges and formulas.

**Child Elements:**
- DefinedName

### 9.5 DefinedName Class

A named range or formula.

**Properties:**
- Name (StringValue) - Name
- Comment (StringValue) - Description
- LocalSheetId (UInt32Value) - Sheet scope
- Hidden (BooleanValue)
- Function (BooleanValue)
- VbProcedure (BooleanValue)

**Content:** Formula or range reference

## 10. Enumerations

### 10.1 Cell-Related Enums

- **CellValues** - Boolean, Date, Error, InlineString, Number, SharedString, String
- **CellFormulaValues** - Normal, Array, DataTable, Shared

### 10.2 Format-Related Enums

- **BorderStyleValues** - None, Thin, Medium, Thick, Double, Hair, Dashed, Dotted, etc.
- **PatternValues** - None, Solid, MediumGray, DarkGray, LightGray, etc.
- **HorizontalAlignmentValues** - General, Left, Center, Right, Fill, Justify
- **VerticalAlignmentValues** - Top, Center, Bottom, Justify, Distributed

### 10.3 Sheet-Related Enums

- **SheetStateValues** - Visible, Hidden, VeryHidden
- **OrientationValues** - Default, Portrait, Landscape
- **SheetViewValues** - Normal, PageBreakPreview, PageLayout
- **PaneStateValues** - Split, Frozen, FrozenSplit

### 10.4 Table/PivotTable Enums

- **TotalsRowFunctionValues** - None, Sum, Min, Max, Average, Count, etc.
- **DataConsolidateFunctionValues** - Average, Count, Max, Min, Sum, Var, etc.
- **PivotTableAxisValues** - AxisRow, AxisCol, AxisPage, AxisValues
- **ShowDataAsValues** - Normal, Difference, Percent, etc.

### 10.5 Validation Enums

- **DataValidationValues** - None, Whole, Decimal, List, Date, Time, TextLength, Custom
- **DataValidationOperatorValues** - Between, NotBetween, Equal, NotEqual, LessThan, etc.
- **DataValidationErrorStyleValues** - Stop, Warning, Information

### 10.6 Conditional Formatting Enums

- **ConditionalFormatValues** - Expression, CellIs, ColorScale, DataBar, IconSet, etc.
- **ConditionalFormattingOperatorValues** - LessThan, LessThanOrEqual, Equal, etc.

## 11. Common Patterns

### 11.1 Creating a Workbook

```csharp
using (SpreadsheetDocument document = SpreadsheetDocument.Create(path, SpreadsheetDocumentType.Workbook))
{
    WorkbookPart workbookPart = document.AddWorkbookPart();
    workbookPart.Workbook = new Workbook();
    
    WorksheetPart worksheetPart = workbookPart.AddNewPart<WorksheetPart>();
    worksheetPart.Worksheet = new Worksheet(new SheetData());
    
    Sheets sheets = workbookPart.Workbook.AppendChild(new Sheets());
    Sheet sheet = new Sheet()
    {
        Id = workbookPart.GetIdOfPart(worksheetPart),
        SheetId = 1,
        Name = "Sheet1"
    };
    sheets.Append(sheet);
    workbookPart.Workbook.Save();
}
```

### 11.2 Adding Cells

```csharp
SheetData sheetData = worksheetPart.Worksheet.GetFirstChild<SheetData>();

Row row = new Row() { RowIndex = 1 };
Cell cell = new Cell()
{
    CellReference = "A1",
    CellValue = new CellValue("Hello"),
    DataType = CellValues.String
};
row.Append(cell);
sheetData.Append(row);
```

### 11.3 Reading Cells

**Performance Warning**: The `ElementAt(index)` method on SharedStringTable is O(n) - extremely slow for large files. For files with many shared strings, pre-cache to a Dictionary for O(1) lookup.

```csharp
// SLOW for large files: ElementAt is O(n)
Cell cell = worksheetPart.Worksheet.Descendants<Cell>()
    .FirstOrDefault(c => c.CellReference == "A1");

if (cell != null)
{
    string value = cell.CellValue?.Text;
    
    // Handle shared strings
    if (cell.DataType?.Value == CellValues.SharedString)
    {
        int index = int.Parse(value);
        value = workbookPart.SharedStringTablePart.SharedStringTable
            .ElementAt(index).InnerText;
    }
}

// FAST: Pre-cache SharedStringTable to Dictionary for O(1) lookup
var stringTable = workbookPart.SharedStringTablePart?.SharedStringTable;
var stringCache = stringTable?.Elements<SharedStringItem>()
    .Select((item, idx) => new { idx, text = item.InnerText })
    .ToDictionary(x => x.idx, x => x.text) ?? new Dictionary<int, string>();

// Then use: stringCache[index] instead of ElementAt(index)
```

### 11.4 Adding Styles

```csharp
// Create stylesheet part
WorkbookStylesPart stylesPart = workbookPart.AddNewPart<WorkbookStylesPart>();
stylesPart.Stylesheet = new Stylesheet(
    new Fonts(new Font()),  // Default font
    new Fills(
        new Fill(new PatternFill() { PatternType = PatternValues.None }),
        new Fill(new PatternFill() { PatternType = PatternValues.Gray125 })
    ),
    new Borders(new Border()),  // Default border
    new CellFormats(new CellFormat())  // Default format
);
```

### 11.5 Cell Reference Utilities

```csharp
// Get column name from number (1 -> A, 27 -> AA)
string GetColumnName(int columnNumber)
{
    string name = "";
    while (columnNumber > 0)
    {
        int mod = (columnNumber - 1) % 26;
        name = (char)('A' + mod) + name;
        columnNumber = (columnNumber - mod) / 26;
    }
    return name;
}

// Get column number from name (A -> 1, AA -> 27)
int GetColumnNumber(string columnName)
{
    int number = 0;
    foreach (char c in columnName)
    {
        number = number * 26 + (c - 'A' + 1);
    }
    return number;
}
```

### 11.6 SAX Approach for Large Files

For files with 50k+ rows, the DOM approach (used above) loads the entire document into memory and can cause `OutOfMemoryException`. Use SAX (streaming) approach instead:

- **OpenXmlReader** - Streaming read, processes one element at a time
- **OpenXmlWriter** - Streaming write, creates elements without full DOM
- **OpenXmlPartReader/Writer** - Part-level streaming

SAX is required for production scenarios with large files. See Microsoft documentation for streaming patterns.

## 12. Code Examples from Official Documentation

### 12.1 Create Workbook with Data

```csharp
using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Spreadsheet;

public static void CreateSpreadsheetWorkbook(string filepath)
{
    // Create a spreadsheet document by supplying the filepath.
    SpreadsheetDocument spreadsheetDocument = SpreadsheetDocument.Create(
        filepath, SpreadsheetDocumentType.Workbook);

    // Add a WorkbookPart to the document.
    WorkbookPart workbookPart = spreadsheetDocument.AddWorkbookPart();
    workbookPart.Workbook = new Workbook();

    // Add a WorksheetPart to the WorkbookPart.
    WorksheetPart worksheetPart = workbookPart.AddNewPart<WorksheetPart>();
    worksheetPart.Worksheet = new Worksheet(new SheetData());

    // Add Sheets to the Workbook.
    Sheets sheets = workbookPart.Workbook.AppendChild(new Sheets());

    // Append a new worksheet and associate it with the workbook.
    Sheet sheet = new Sheet()
    {
        Id = workbookPart.GetIdOfPart(worksheetPart),
        SheetId = 1,
        Name = "mySheet"
    };
    sheets.Append(sheet);

    workbookPart.Workbook.Save();

    // Dispose the document.
    spreadsheetDocument.Dispose();
}
```

`[VERIFIED] (https://learn.microsoft.com/en-us/office/open-xml/spreadsheet/how-to-create-a-spreadsheet-document-by-providing-a-file-name)`

### 12.2 Insert Text into Cell

```csharp
public static void InsertText(string docName, string text)
{
    // Open the document for editing.
    using (SpreadsheetDocument spreadSheet = 
        SpreadsheetDocument.Open(docName, true))
    {
        // Get the SharedStringTablePart. If it does not exist, create a new one.
        SharedStringTablePart shareStringPart;
        if (spreadSheet.WorkbookPart.GetPartsOfType<SharedStringTablePart>().Count() > 0)
        {
            shareStringPart = spreadSheet.WorkbookPart.GetPartsOfType<SharedStringTablePart>().First();
        }
        else
        {
            shareStringPart = spreadSheet.WorkbookPart.AddNewPart<SharedStringTablePart>();
        }

        // Insert the text into the SharedStringTablePart.
        int index = InsertSharedStringItem(text, shareStringPart);

        // Insert a new worksheet.
        WorksheetPart worksheetPart = InsertWorksheet(spreadSheet.WorkbookPart);

        // Insert cell A1 into the new worksheet.
        Cell cell = InsertCellInWorksheet("A", 1, worksheetPart);

        // Set the value of cell A1.
        cell.CellValue = new CellValue(index.ToString());
        cell.DataType = new EnumValue<CellValues>(CellValues.SharedString);

        // Save the new worksheet.
        worksheetPart.Worksheet.Save();
    }
}
```

`[VERIFIED] (https://learn.microsoft.com/en-us/office/open-xml/spreadsheet/how-to-insert-text-into-a-cell-in-a-spreadsheet)`

### 12.3 Get Worksheet Information

```csharp
public static void GetSheetInfo(string fileName)
{
    // Open file as read-only.
    using (SpreadsheetDocument mySpreadsheet = 
        SpreadsheetDocument.Open(fileName, false))
    {
        S sheets = mySpreadsheet.WorkbookPart.Workbook.Sheets;

        // For each sheet, display the sheet information.
        foreach (E sheet in sheets)
        {
            Console.WriteLine($"Sheet: {sheet.Name}");
            Console.WriteLine($"  SheetId: {sheet.SheetId}");
            Console.WriteLine($"  Id: {sheet.Id}");
        }
    }
}
```

`[VERIFIED] (https://learn.microsoft.com/en-us/office/open-xml/spreadsheet/how-to-get-worksheet-information-from-a-package)`

### 12.4 Read Cell Values

```csharp
public static string GetCellValue(string fileName, string sheetName, string addressName)
{
    string value = null;

    using (SpreadsheetDocument document = SpreadsheetDocument.Open(fileName, false))
    {
        WorkbookPart wbPart = document.WorkbookPart;

        // Find the sheet with the supplied name
        Sheet theSheet = wbPart.Workbook.Descendants<Sheet>()
            .FirstOrDefault(s => s.Name == sheetName);

        if (theSheet == null)
            throw new ArgumentException("Sheet not found");

        // Get the worksheet part
        WorksheetPart wsPart = (WorksheetPart)wbPart.GetPartById(theSheet.Id);

        // Find the cell
        Cell theCell = wsPart.Worksheet.Descendants<Cell>()
            .FirstOrDefault(c => c.CellReference == addressName);

        if (theCell != null && theCell.CellValue != null)
        {
            value = theCell.CellValue.InnerText;

            // If shared string, look up actual value
            if (theCell.DataType != null && 
                theCell.DataType.Value == CellValues.SharedString)
            {
                var stringTable = wbPart.GetPartsOfType<SharedStringTablePart>()
                    .FirstOrDefault();

                if (stringTable != null)
                {
                    value = stringTable.SharedStringTable
                        .ElementAt(int.Parse(value)).InnerText;
                }
            }
        }
    }

    return value;
}
```

`[VERIFIED] (https://learn.microsoft.com/en-us/office/open-xml/spreadsheet/how-to-retrieve-the-values-of-cells-in-a-spreadsheet)`

### 12.5 Delete Row from Worksheet

```csharp
public static void RemoveRow(string docName, string sheetName, uint rowIndex)
{
    using (SpreadsheetDocument document = SpreadsheetDocument.Open(docName, true))
    {
        WorkbookPart wbPart = document.WorkbookPart;
        Sheet theSheet = wbPart.Workbook.Descendants<Sheet>()
            .FirstOrDefault(s => s.Name == sheetName);

        WorksheetPart wsPart = (WorksheetPart)wbPart.GetPartById(theSheet.Id);
        SheetData sheetData = wsPart.Worksheet.GetFirstChild<SheetData>();

        Row row = sheetData.Elements<Row>().FirstOrDefault(r => r.RowIndex == rowIndex);
        if (row != null)
        {
            row.Remove();
        }

        wsPart.Worksheet.Save();
    }
}
```

### 12.6 Insert Worksheet

```csharp
private static WorksheetPart InsertWorksheet(WorkbookPart workbookPart)
{
    // Add a new worksheet part to the workbook.
    WorksheetPart newWorksheetPart = workbookPart.AddNewPart<WorksheetPart>();
    newWorksheetPart.Worksheet = new Worksheet(new SheetData());
    newWorksheetPart.Worksheet.Save();

    Sheets sheets = workbookPart.Workbook.GetFirstChild<Sheets>();
    string relationshipId = workbookPart.GetIdOfPart(newWorksheetPart);

    // Get a unique ID for the new sheet.
    uint sheetId = 1;
    if (sheets.Elements<Sheet>().Count() > 0)
    {
        sheetId = sheets.Elements<Sheet>().Select(s => s.SheetId.Value).Max() + 1;
    }

    string sheetName = "Sheet" + sheetId;

    // Append the new worksheet and associate it with the workbook.
    Sheet sheet = new Sheet() 
    { 
        Id = relationshipId, 
        SheetId = sheetId, 
        Name = sheetName 
    };
    sheets.Append(sheet);
    workbookPart.Workbook.Save();

    return newWorksheetPart;
}
```

`[VERIFIED] (https://learn.microsoft.com/en-us/office/open-xml/spreadsheet/how-to-insert-a-new-worksheet-into-a-spreadsheet)`

## Document History

**[2026-02-27 13:25]**
- Added: Thread safety warning in Section 1.1
- Added: SharedStringTable Dictionary caching pattern (performance fix)
- Added: SAX approach note with OpenXmlReader/OpenXmlWriter classes
- Added: Date serial number handling note
- Review: `_INFO_AXCEL-IN03_OPENXML_API_REVIEW.md` findings addressed

**[2026-02-27 Session]**
- Created: Comprehensive Open XML SDK API reference document
- Source: Microsoft Learn DocumentFormat.OpenXml Namespace
- Coverage: Packaging classes, 500+ Spreadsheet classes, 100+ enumerations
- Added: Common patterns for cell manipulation, styling, reading/writing
- Added: Code examples from official Microsoft documentation
- Note: SDK manipulates file structure; no formula calculation
