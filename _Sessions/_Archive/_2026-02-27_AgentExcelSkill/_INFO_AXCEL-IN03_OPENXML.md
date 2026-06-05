# INFO: Open XML SDK

**Doc ID**: AXCEL-IN03
**Goal**: Document Open XML SDK capabilities for Excel file manipulation without Excel
**Version Scope**: Open XML SDK 3.0+ (2026-02-27)

**Depends on:**
- `__EXCEL_APIS_SOURCES.md [AXCEL-SOURCES-01]` for source references

## Overview

The Open XML SDK is a .NET library for creating, reading, and modifying Office Open XML documents (Word, Excel, PowerPoint) without requiring Office installation. For Excel, it works with SpreadsheetML - the XML format inside .xlsx files. The SDK provides strongly-typed classes representing the XML structure, enabling direct file manipulation. `[VERIFIED] (AXCEL-SC-MSFT-OXML)`

Open XML SDK is ideal for server-side scenarios, batch processing, and environments where Excel cannot be installed. It manipulates files at the document structure level, not through Excel's object model. This means formulas are stored as strings - the SDK does not calculate them. For calculated values, you must either pre-calculate or use a formula engine library. `[VERIFIED] (AXCEL-SC-MSFT-OXPAR)`

## Supported Features

- **Read cells/data**: Yes - Read cell values from SharedStringTable or inline
- **Write cells/data**: Yes - Write cell values, create worksheets, define structure
- **Read formulas**: Yes - Read formula strings from Cell.CellFormula
- **Write formulas**: Yes - Write formula strings (not evaluated by SDK)
- **Remote control open workbook**: No - File-based only, no process interaction
- **Export to CSV**: No - Must implement conversion logic manually
- **Export VBA code**: No - VBA is stored in vbaProject.bin (binary, not XML)
- **Import VBA code**: No - Cannot manipulate VBA content
- **Works without Excel**: Yes - Primary advantage
- **Cross-platform**: Yes - Works on Windows, Linux, macOS via .NET

## Intended Use Cases

1. **Server-side document generation**: Create Excel reports on web servers
2. **Batch file processing**: Modify thousands of files without Excel overhead
3. **Template-based generation**: Fill templates with data programmatically
4. **Data extraction**: Read data from xlsx files for import/ETL
5. **Cross-platform automation**: Process Excel files on Linux/Docker

## Limitations

- **No formula calculation**: Formulas stored as text, not evaluated
- **No VBA support**: Cannot read/write macro code (vbaProject.bin is binary)
- **No .xls support**: Only .xlsx/.xlsm (Open XML format), not legacy .xls
- **Complexity**: Lower-level than COM; must understand SpreadsheetML structure
- **No live Excel interaction**: Cannot attach to running Excel instance
- **Formatting complexity**: Styles and formatting require verbose XML manipulation
- **Limited chart support**: Charts are complex; easier via template modification

## Security Setup

No special security settings required. Open XML SDK operates on files directly without Office involvement.

### NuGet Package

```
Install-Package DocumentFormat.OpenXml
```

## Platform Support

- **Windows**: Yes - Full support
- **macOS**: Yes - Via .NET 5+/6+/7+/8+
- **Web**: Yes - ASP.NET Core, Azure Functions
- **Linux**: Yes - Via .NET 5+/6+/7+/8+, Docker compatible

## Prerequisites

- .NET Framework 4.6.2+ or .NET 5+/6+/7+/8+
- NuGet package: DocumentFormat.OpenXml (v3.0+ recommended)
- No Office installation required

## Code Examples

### C#: Create Workbook with Data

```csharp
using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Spreadsheet;

string filePath = @"C:\temp\output.xlsx";

using (SpreadsheetDocument document = SpreadsheetDocument.Create(
    filePath, SpreadsheetDocumentType.Workbook))
{
    // Add workbook part
    WorkbookPart workbookPart = document.AddWorkbookPart();
    workbookPart.Workbook = new Workbook();
    
    // Add worksheet part
    WorksheetPart worksheetPart = workbookPart.AddNewPart<WorksheetPart>();
    worksheetPart.Worksheet = new Worksheet(new SheetData());
    
    // Add sheet to workbook
    Sheets sheets = workbookPart.Workbook.AppendChild(new Sheets());
    Sheet sheet = new Sheet()
    {
        Id = workbookPart.GetIdOfPart(worksheetPart),
        SheetId = 1,
        Name = "Sheet1"
    };
    sheets.Append(sheet);
    
    // Get sheet data and add rows
    SheetData sheetData = worksheetPart.Worksheet.GetFirstChild<SheetData>();
    
    // Row 1: Headers
    Row headerRow = new Row() { RowIndex = 1 };
    headerRow.Append(CreateCell("A1", "Name", CellValues.String));
    headerRow.Append(CreateCell("B1", "Value", CellValues.String));
    sheetData.Append(headerRow);
    
    // Row 2: Data
    Row dataRow = new Row() { RowIndex = 2 };
    dataRow.Append(CreateCell("A2", "Test", CellValues.String));
    dataRow.Append(CreateCell("B2", "123", CellValues.Number));
    sheetData.Append(dataRow);
    
    // Row 3: Formula (stored as string, not calculated)
    Row formulaRow = new Row() { RowIndex = 3 };
    Cell formulaCell = new Cell() { CellReference = "B3" };
    formulaCell.CellFormula = new CellFormula("SUM(B2:B2)*2");
    formulaRow.Append(formulaCell);
    sheetData.Append(formulaRow);
    
    workbookPart.Workbook.Save();
}

Cell CreateCell(string reference, string value, CellValues dataType)
{
    return new Cell()
    {
        CellReference = reference,
        CellValue = new CellValue(value),
        DataType = dataType
    };
}
```

### C#: Read All Data from Workbook

```csharp
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Spreadsheet;

string filePath = @"C:\temp\input.xlsx";

using (SpreadsheetDocument document = SpreadsheetDocument.Open(filePath, false))
{
    WorkbookPart workbookPart = document.WorkbookPart;
    SharedStringTablePart stringTable = workbookPart.SharedStringTablePart;
    
    foreach (Sheet sheet in workbookPart.Workbook.Sheets)
    {
        Console.WriteLine($"Sheet: {sheet.Name}");
        
        WorksheetPart worksheetPart = (WorksheetPart)workbookPart.GetPartById(sheet.Id);
        SheetData sheetData = worksheetPart.Worksheet.GetFirstChild<SheetData>();
        
        foreach (Row row in sheetData.Elements<Row>())
        {
            foreach (Cell cell in row.Elements<Cell>())
            {
                string value = GetCellValue(cell, stringTable);
                string formula = cell.CellFormula?.Text ?? "";
                
                Console.WriteLine($"  {cell.CellReference}: {value}" + 
                    (formula != "" ? $" [Formula: {formula}]" : ""));
            }
        }
    }
}

string GetCellValue(Cell cell, SharedStringTablePart stringTable)
{
    if (cell.CellValue == null) return "";
    
    string value = cell.CellValue.Text;
    
    // If shared string, look up actual value
    if (cell.DataType != null && cell.DataType == CellValues.SharedString)
    {
        return stringTable.SharedStringTable
            .ElementAt(int.Parse(value)).InnerText;
    }
    
    return value;
}
```

### C#: Export to CSV (Manual Implementation)

```csharp
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Spreadsheet;
using System.Text;

void ExportSheetToCsv(string xlsxPath, string sheetName, string csvPath)
{
    using (SpreadsheetDocument document = SpreadsheetDocument.Open(xlsxPath, false))
    {
        WorkbookPart workbookPart = document.WorkbookPart;
        SharedStringTablePart stringTable = workbookPart.SharedStringTablePart;
        
        Sheet sheet = workbookPart.Workbook.Sheets.Elements<Sheet>()
            .FirstOrDefault(s => s.Name == sheetName);
        
        if (sheet == null) throw new Exception($"Sheet '{sheetName}' not found");
        
        WorksheetPart worksheetPart = (WorksheetPart)workbookPart.GetPartById(sheet.Id);
        SheetData sheetData = worksheetPart.Worksheet.GetFirstChild<SheetData>();
        
        var sb = new StringBuilder();
        
        foreach (Row row in sheetData.Elements<Row>())
        {
            var cells = row.Elements<Cell>().ToList();
            var values = new List<string>();
            
            foreach (Cell cell in cells)
            {
                string value = GetCellValue(cell, stringTable);
                // Escape CSV: quote if contains comma or quote
                if (value.Contains(",") || value.Contains("\""))
                {
                    value = "\"" + value.Replace("\"", "\"\"") + "\"";
                }
                values.Add(value);
            }
            
            sb.AppendLine(string.Join(",", values));
        }
        
        File.WriteAllText(csvPath, sb.ToString(), Encoding.UTF8);
    }
}
```

## Gotchas and Quirks

- **Shared strings**: Text values are often stored in SharedStringTable, not inline. Must look up by index.
- **Cell references sparse**: Cells only exist if they have content. Empty cells are not in XML.
- **Column letters**: Must calculate column letters from index (A, B, ..., Z, AA, AB, ...).
- **Formula results**: Excel caches formula results in CellValue. SDK doesn't update these.
- **Date handling**: Dates stored as serial numbers. Use DateTime.FromOADate() to convert.
- **Large files**: Use SAX reader (OpenXmlReader) for large files to avoid memory issues. `[VERIFIED] (AXCEL-SC-MSFT-OXPAR)`
- **Styles complexity**: Cell formatting requires separate Stylesheet part with complex structure.

## Main Documentation Links

- [About the Open XML SDK](https://learn.microsoft.com/en-us/office/open-xml/about-the-open-xml-sdk)
- [Working with SpreadsheetML](https://learn.microsoft.com/en-us/office/open-xml/spreadsheet/overview)
- [Create Spreadsheet Document](https://learn.microsoft.com/en-us/office/open-xml/spreadsheet/how-to-create-a-spreadsheet-document-by-providing-a-file-name)
- [Parse Large Spreadsheet](https://learn.microsoft.com/en-us/office/open-xml/spreadsheet/how-to-parse-and-read-a-large-spreadsheet)

## Sources

- `[VERIFIED] (AXCEL-SC-MSFT-OXML)` - About Open XML SDK
- `[VERIFIED] (AXCEL-SC-MSFT-OXCRE)` - Create spreadsheet
- `[VERIFIED] (AXCEL-SC-MSFT-OXPAR)` - Parse large spreadsheet
- `[COMMUNITY] (AXCEL-SC-SO-OLEXML)` - OLE DB vs Open XML vs Interop comparison

## Document History

**[2026-02-27 13:15]**
- Initial document creation with Open XML SDK coverage
