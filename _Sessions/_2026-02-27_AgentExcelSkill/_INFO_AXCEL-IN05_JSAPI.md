# INFO: Excel JavaScript API (Office Add-ins)

**Doc ID**: AXCEL-IN05
**Goal**: Document Excel JavaScript API for Office Add-in development
**Version Scope**: ExcelApi 1.17+ (2026-02-27)

**Depends on:**
- `__EXCEL_APIS_SOURCES.md [AXCEL-SOURCES-01]` for source references

## Overview

The Excel JavaScript API is the modern extensibility platform for Excel, enabling web-based add-ins that run inside Excel across Windows, Mac, and Web. Add-ins are web applications that interact with Excel through a strongly-typed JavaScript/TypeScript object model. The API provides access to worksheets, ranges, tables, charts, PivotTables, and more. `[VERIFIED] (AXCEL-SC-MSFT-JSOV)`

Office Add-ins use web technologies (HTML, CSS, JavaScript/TypeScript) and run in a task pane or content area within Excel. They work across all Excel platforms where add-ins are supported. The Excel-specific API (ExcelApi) supplements the Common API that works across Office apps. API capabilities are versioned as "requirement sets" (e.g., ExcelApi 1.17). `[VERIFIED] (AXCEL-SC-MSFT-JSOBJ)`

## Supported Features

- **Read cells/data**: Yes - Range.values, Table.getRange()
- **Write cells/data**: Yes - Range.values = [[...]]
- **Read formulas**: Yes - Range.formulas, Range.formulasR1C1
- **Write formulas**: Yes - Range.formulas = [[...]]
- **Remote control open workbook**: Yes* - Add-in runs inside Excel, has full access
- **Export to CSV**: Partial - Can read data but must construct CSV manually
- **Export VBA code**: No - No VBProject access
- **Import VBA code**: No - No VBProject access
- **Works without Excel**: No - Add-in requires Excel as host
- **Cross-platform**: Yes - Windows, Mac, Web (not mobile)

*Add-in must be installed/opened in the workbook; cannot attach from external process

## Intended Use Cases

1. **Custom task panes**: UI extensions within Excel for specialized workflows
2. **Custom functions**: JavaScript-based UDFs that work like native Excel functions
3. **Data connectors**: Pull external data into Excel through web APIs
4. **Cross-platform add-ins**: Single codebase for Windows/Mac/Web
5. **Content add-ins**: Interactive content embedded in worksheets

## Limitations

- **Requires add-in deployment**: Cannot run standalone like COM automation
- **No external process control**: Cannot attach from outside Excel
- **No VBA access**: Cannot read/write VBA code or VBProject
- **Async model**: All API calls are asynchronous (Promise-based)
- **Sandbox restrictions**: Limited file system access, no native code
- **Requirement sets**: Features vary by Excel version; must check availability
- **No .xls support**: Works with modern formats only
- **Performance**: Web-based execution slower than native COM

## Security Setup

### Add-in Deployment Options

1. **Sideloading** (development):
   - Insert > Get Add-ins > Upload My Add-in
   - Or use manifest file in network share

2. **Centralized Deployment** (organization):
   - Microsoft 365 admin center > Settings > Integrated apps
   - Deploy to users/groups

3. **AppSource** (public):
   - Submit to Microsoft AppSource marketplace

### Manifest Permissions

```xml
<Permissions>ReadWriteDocument</Permissions>
```

Options: Restricted, ReadDocument, ReadAllDocument, WriteDocument, ReadWriteDocument

## Platform Support

- **Windows**: Yes - Excel 2016+, Microsoft 365
- **macOS**: Yes - Excel 2016+, Microsoft 365
- **Web**: Yes - Excel Online
- **iOS/Android**: Partial - Limited add-in support

## Prerequisites

- Excel 2016+ or Excel Online
- Node.js and npm (for development)
- Yeoman generator for Office Add-ins (`yo office`)
- HTTPS for hosting (localhost with certs for dev)

## Code Examples

### TypeScript: Read and Write Range

```typescript
async function readWriteRange() {
    await Excel.run(async (context) => {
        // Get active worksheet
        const sheet = context.workbook.worksheets.getActiveWorksheet();
        
        // Read range
        const readRange = sheet.getRange("A1:C10");
        readRange.load(["values", "formulas", "address"]);
        await context.sync();
        
        console.log(`Range: ${readRange.address}`);
        console.log(`Values:`, readRange.values);
        console.log(`Formulas:`, readRange.formulas);
        
        // Write data
        const writeRange = sheet.getRange("E1:F2");
        writeRange.values = [
            ["Header1", "Header2"],
            ["Data", 123]
        ];
        
        // Write formula
        const formulaRange = sheet.getRange("G1");
        formulaRange.formulas = [["=SUM(F:F)"]];
        
        await context.sync();
        console.log("Data written successfully");
    });
}
```

### TypeScript: Export All Sheets to CSV-like Format

```typescript
async function exportSheetsData(): Promise<{[sheetName: string]: string}> {
    const csvData: {[sheetName: string]: string} = {};
    
    await Excel.run(async (context) => {
        const sheets = context.workbook.worksheets;
        sheets.load("items/name");
        await context.sync();
        
        for (const sheet of sheets.items) {
            const usedRange = sheet.getUsedRange();
            usedRange.load("values");
            await context.sync();
            
            // Convert to CSV string
            const csv = usedRange.values
                .map(row => row.map(cell => {
                    const str = String(cell ?? "");
                    return str.includes(",") ? `"${str}"` : str;
                }).join(","))
                .join("\n");
            
            csvData[sheet.name] = csv;
        }
    });
    
    return csvData;
}
```

### TypeScript: Custom Function (UDF)

```typescript
// In functions.ts
/**
 * Adds two numbers.
 * @customfunction
 * @param first First number
 * @param second Second number
 * @returns Sum of two numbers
 */
function add(first: number, second: number): number {
    return first + second;
}

/**
 * Fetches data from API (async)
 * @customfunction
 * @param url API endpoint
 * @returns API response
 */
async function fetchData(url: string): Promise<string> {
    const response = await fetch(url);
    const data = await response.json();
    return JSON.stringify(data);
}

// Register functions
CustomFunctions.associate("ADD", add);
CustomFunctions.associate("FETCHDATA", fetchData);
```

### TypeScript: Trigger Calculation

```typescript
async function triggerCalculation() {
    await Excel.run(async (context) => {
        // Calculate entire workbook
        context.workbook.application.calculate(Excel.CalculationType.full);
        
        // Or calculate specific range
        const sheet = context.workbook.worksheets.getActiveWorksheet();
        const range = sheet.getRange("A1:Z100");
        // Note: Range-level calculate not directly available
        // Use workbook.application.calculate() instead
        
        await context.sync();
    });
}
```

## Gotchas and Quirks

- **Async everywhere**: All API calls return Promises; must use Excel.run() context
- **context.sync()**: Must call sync() to execute queued operations and get results
- **Load before read**: Must call .load(["properties"]) before reading object properties
- **Proxy objects**: API returns proxy objects, not actual data until sync()
- **5-minute timeout**: Long Excel.run operations may timeout
- **Requirement set checks**: Use `Office.context.requirements.isSetSupported()` for feature detection
- **Event handlers**: Use `onChanged`, `onSelectionChanged` for reactive updates
- **Error handling**: Wrap in try/catch; errors may be cryptic

## Main Documentation Links

- [Excel JavaScript API Overview](https://learn.microsoft.com/en-us/office/dev/add-ins/reference/overview/excel-add-ins-reference-overview)
- [Excel Object Model](https://learn.microsoft.com/en-us/office/dev/add-ins/excel/excel-add-ins-core-concepts)
- [Office JS API Reference](https://learn.microsoft.com/en-us/javascript/api/excel)
- [Custom Functions](https://learn.microsoft.com/en-us/office/dev/add-ins/excel/custom-functions-overview)

## Sources

- `[VERIFIED] (AXCEL-SC-MSFT-JSOV)` - Excel JS API overview
- `[VERIFIED] (AXCEL-SC-MSFT-JSOBJ)` - Excel JS object model
- `[VERIFIED] (AXCEL-SC-MSFT-JSREF)` - Office JS API reference

## Document History

**[2026-02-27 13:35]**
- Initial document creation with Excel JS API coverage
