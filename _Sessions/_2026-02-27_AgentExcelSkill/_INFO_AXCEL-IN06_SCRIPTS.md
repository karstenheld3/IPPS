# INFO: Office Scripts

**Doc ID**: AXCEL-IN06
**Goal**: Document Office Scripts capabilities for Excel Online automation
**Version Scope**: Office Scripts (2026-02-27)

**Depends on:**
- `__EXCEL_APIS_SOURCES.md [AXCEL-SOURCES-01]` for source references

## Overview

Office Scripts is a TypeScript-based automation platform for Excel on the web. It enables users to record, edit, and share automation scripts that can be triggered manually or via Power Automate. Scripts are stored in OneDrive and can be shared within organizations. Office Scripts bridges the gap between macro recording (like VBA) and cloud-first automation. `[VERIFIED] (AXCEL-SC-MSFT-SCROV)`

Unlike VBA, Office Scripts run in the cloud and work only with Excel on the web (not desktop Excel). They use a TypeScript API similar to the Excel JavaScript API but designed for automation scenarios rather than add-in development. Scripts can be scheduled to run automatically or triggered from Power Automate flows. `[VERIFIED] (AXCEL-SC-MSFT-SCRFN)`

## Supported Features

- **Read cells/data**: Yes - Workbook, Worksheet, Range objects
- **Write cells/data**: Yes - Range.setValues(), Range.setValue()
- **Read formulas**: Yes - Range.getFormulas()
- **Write formulas**: Yes - Range.setFormulas()
- **Remote control open workbook**: No - Scripts run on file, not live user session
- **Export to CSV**: Yes - Can construct CSV string and return via Power Automate
- **Export VBA code**: No - No VBProject access
- **Import VBA code**: No - No VBProject access
- **Works without Excel**: Yes - Runs in cloud; Excel desktop not required
- **Cross-platform**: Yes - Cloud-based, any browser

## Intended Use Cases

1. **Repetitive task automation**: Record actions and replay across workbooks
2. **Power Automate integration**: Automate Excel as part of business workflows
3. **Scheduled data processing**: Run scripts on schedule via Power Automate
4. **Team collaboration**: Share scripts with colleagues
5. **No-code to low-code**: Action Recorder for non-programmers, Code Editor for customization

## Limitations

- **Excel on web only**: Does not work with Excel desktop application
- **Microsoft 365 required**: Requires commercial Microsoft 365 license
- **No VBA access**: Cannot manipulate VBA code
- **No live control**: Scripts run on files, not on user's open session
- **Cloud storage only**: Files must be in OneDrive or SharePoint
- **No external HTTP calls**: Cannot make fetch() calls (security restriction)
- **Execution timeout**: Scripts have time limits
- **Limited licensing**: Not available on all Microsoft 365 plans

## Security Setup

### License Requirements

Office Scripts requires:
- Microsoft 365 Business Standard or higher
- Microsoft 365 E3/E5
- Office 365 E1/E3/E5

### Admin Settings

1. Microsoft 365 admin center > Settings > Org settings > Office Scripts
2. Enable/disable Office Scripts for organization
3. Control Power Automate integration permissions

### Script Sharing

- Scripts stored in user's OneDrive (My Files > Office Scripts)
- Can share with specific people or entire organization
- Scripts can be embedded in workbooks for easier distribution

## Platform Support

- **Windows**: Yes - Via browser (Excel on web)
- **macOS**: Yes - Via browser (Excel on web)
- **Web**: Yes - Primary platform
- **Mobile**: No - Not supported

## Prerequisites

- Microsoft 365 commercial subscription with Office Scripts enabled
- Excel on the web (not desktop)
- Files stored in OneDrive or SharePoint
- Modern browser (Edge, Chrome, Firefox, Safari)

## Code Examples

### TypeScript: Read and Write Data

```typescript
function main(workbook: ExcelScript.Workbook) {
    // Get active worksheet
    const sheet = workbook.getActiveWorksheet();
    
    // Read range
    const readRange = sheet.getRange("A1:C10");
    const values = readRange.getValues();
    const formulas = readRange.getFormulas();
    
    console.log("Values:", JSON.stringify(values));
    console.log("Formulas:", JSON.stringify(formulas));
    
    // Write data
    const writeRange = sheet.getRange("E1:F2");
    writeRange.setValues([
        ["Header1", "Header2"],
        ["Data", 123]
    ]);
    
    // Write formula
    const formulaRange = sheet.getRange("G1");
    formulaRange.setFormula("=SUM(F:F)");
}
```

### TypeScript: Export Sheet to CSV String

```typescript
function main(workbook: ExcelScript.Workbook): string {
    const sheet = workbook.getActiveWorksheet();
    const usedRange = sheet.getUsedRange();
    const values = usedRange.getValues();
    
    // Convert to CSV
    const csv = values.map(row => 
        row.map(cell => {
            const str = String(cell ?? "");
            // Escape commas and quotes
            if (str.includes(",") || str.includes('"')) {
                return `"${str.replace(/"/g, '""')}"`;
            }
            return str;
        }).join(",")
    ).join("\n");
    
    return csv;
}
```

### TypeScript: Process All Sheets

```typescript
function main(workbook: ExcelScript.Workbook) {
    const sheets = workbook.getWorksheets();
    
    for (const sheet of sheets) {
        console.log(`Processing: ${sheet.getName()}`);
        
        const usedRange = sheet.getUsedRange();
        if (usedRange) {
            const rowCount = usedRange.getRowCount();
            const colCount = usedRange.getColumnCount();
            console.log(`  Size: ${rowCount} rows x ${colCount} columns`);
        }
    }
}
```

### Power Automate: Run Script and Get Result

```json
{
    "type": "OpenApiConnection",
    "inputs": {
        "host": {
            "connectionName": "shared_excelonlinebusiness",
            "operationId": "RunScript",
            "apiId": "/providers/Microsoft.PowerApps/apis/excelonlinebusiness"
        },
        "parameters": {
            "source": "me",
            "drive": "OneDrive",
            "file": "/Documents/data.xlsx",
            "script": "Export to CSV",
            "ScriptParameters": {}
        }
    }
}
```

## Gotchas and Quirks

- **No fetch/HTTP**: Cannot make external API calls from scripts (security)
- **Return values**: Can return data to Power Automate for further processing
- **Sync execution**: Unlike JS API, Office Scripts are synchronous
- **No events**: Cannot subscribe to cell change events
- **console.log**: Outputs appear in Action Recorder log, not browser console
- **Script storage**: Scripts stored in OneDrive, not in workbook
- **Workbook vs Application**: No access to Excel application settings

## Main Documentation Links

- [Office Scripts Overview](https://learn.microsoft.com/en-us/office/dev/scripts/overview/excel)
- [Scripting Fundamentals](https://learn.microsoft.com/en-us/office/dev/scripts/develop/scripting-fundamentals)
- [Power Automate Integration](https://learn.microsoft.com/en-us/office/dev/scripts/develop/power-automate-integration)

## Sources

- `[VERIFIED] (AXCEL-SC-MSFT-SCROV)` - Office Scripts overview
- `[VERIFIED] (AXCEL-SC-MSFT-SCRFN)` - Scripting fundamentals
- `[VERIFIED] (AXCEL-SC-MSFT-SCRPA)` - Power Automate integration

## Document History

**[2026-02-27 13:40]**
- Initial document creation
