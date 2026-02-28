# Excel APIs - Source Collection

**Doc ID**: AXCEL-SOURCES-01
**Version Scope**: Excel 2016+ / Microsoft 365 (as of 2026-02-27)
**Preflight Accuracy**: [pending verification]

## Identified Excel APIs

Based on research, the following **9 distinct Excel APIs/approaches** have been identified:

1. **Excel VBA** - Built-in macro language with full Excel object model access
2. **Excel COM/Interop API** - Windows COM automation (Microsoft.Office.Interop.Excel)
3. **Open XML SDK** - Direct file manipulation without Excel installed
4. **Microsoft Graph API** - REST API for Excel Online / cloud workbooks
5. **Excel JavaScript API** - Office Add-ins for web-based extensibility
6. **Office Scripts** - TypeScript-based automation for Excel on the web
7. **Excel XLL SDK (C API)** - High-performance native add-ins via C/C++
8. **VSTO (Visual Studio Tools for Office)** - .NET-based Office solutions
9. **Third-party Libraries** - Python (openpyxl, xlwings, win32com), PowerShell (ImportExcel)

## Official Sources (Tier 1)

### Excel VBA

- **AXCEL-SC-MSFT-VBAREF**: Excel VBA Reference
  - URL: https://learn.microsoft.com/en-us/office/vba/api/overview/excel
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-VBAOBJ**: Excel Object Model for VBA
  - URL: https://learn.microsoft.com/en-us/office/vba/api/overview/excel/object-model
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-VBEXT**: Visual Basic Add-In Model Objects
  - URL: https://learn.microsoft.com/en-us/office/vba/language/reference/visual-basic-add-in-model/objects-visual-basic-add-in-model
  - Accessed: 2026-02-27

### Excel COM/Interop API

- **AXCEL-SC-MSFT-INTNS**: Microsoft.Office.Interop.Excel Namespace
  - URL: https://learn.microsoft.com/en-us/dotnet/api/microsoft.office.interop.excel
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-INTAPP**: Application Interface (Interop)
  - URL: https://learn.microsoft.com/en-us/dotnet/api/microsoft.office.interop.excel.application
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-INTAUT**: Automate Excel from Visual C#
  - URL: https://learn.microsoft.com/en-us/previous-versions/office/troubleshoot/office-developer/automate-excel-from-visual-c
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-RUNINS**: Automate Running Instance
  - URL: https://learn.microsoft.com/en-us/previous-versions/office/troubleshoot/office-developer/use-visual-c-automate-run-program-instance
  - Accessed: 2026-02-27

### Open XML SDK

- **AXCEL-SC-MSFT-OXML**: About the Open XML SDK
  - URL: https://learn.microsoft.com/en-us/office/open-xml/about-the-open-xml-sdk
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-OXCRE**: Create Spreadsheet by File Name
  - URL: https://learn.microsoft.com/en-us/office/open-xml/spreadsheet/how-to-create-a-spreadsheet-document-by-providing-a-file-name
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-OXPAR**: Parse Large Spreadsheet
  - URL: https://learn.microsoft.com/en-us/office/open-xml/spreadsheet/how-to-parse-and-read-a-large-spreadsheet
  - Accessed: 2026-02-27

### Microsoft Graph API

- **AXCEL-SC-MSFT-GRPOV**: Excel Workbooks and Charts API Overview
  - URL: https://learn.microsoft.com/en-us/graph/excel-concept-overview
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-GRPWK**: Working with Excel in Graph
  - URL: https://learn.microsoft.com/en-us/graph/api/resources/excel
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-GRPWR**: Write Data to Excel Workbook
  - URL: https://learn.microsoft.com/en-us/graph/excel-write-to-workbook
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-GRPBP**: Best Practices for Excel API
  - URL: https://learn.microsoft.com/en-us/graph/workbook-best-practice
  - Accessed: 2026-02-27

### Excel JavaScript API

- **AXCEL-SC-MSFT-JSOV**: Excel JavaScript API Overview
  - URL: https://learn.microsoft.com/en-us/office/dev/add-ins/reference/overview/excel-add-ins-reference-overview
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-JSOBJ**: Excel JS Object Model
  - URL: https://learn.microsoft.com/en-us/office/dev/add-ins/excel/excel-add-ins-core-concepts
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-JSREF**: Office JS API Reference
  - URL: https://learn.microsoft.com/en-us/javascript/api/overview
  - Accessed: 2026-02-27

### Office Scripts

- **AXCEL-SC-MSFT-SCROV**: Office Scripts in Excel
  - URL: https://learn.microsoft.com/en-us/office/dev/scripts/overview/excel
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-SCRFN**: Office Scripts Fundamentals
  - URL: https://learn.microsoft.com/en-us/office/dev/scripts/develop/scripting-fundamentals
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-SCRPA**: Office Scripts with Power Automate
  - URL: https://learn.microsoft.com/en-us/office/dev/scripts/develop/power-automate-integration
  - Accessed: 2026-02-27

### Excel XLL SDK (C API)

- **AXCEL-SC-MSFT-XLLWC**: Welcome to Excel SDK
  - URL: https://learn.microsoft.com/en-us/office/client-developer/excel/welcome-to-the-excel-software-development-kit
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-XLLPR**: Programming with the C API
  - URL: https://learn.microsoft.com/en-us/office/client-developer/excel/programming-with-the-c-api-in-excel
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-XLLCR**: Creating XLLs
  - URL: https://learn.microsoft.com/en-us/office/client-developer/excel/creating-xlls
  - Accessed: 2026-02-27

### VSTO

- **AXCEL-SC-MSFT-VSTOV**: Office Solutions Development Overview
  - URL: https://learn.microsoft.com/en-us/visualstudio/vsto/office-solutions-development-overview-vsto
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-VSTOW**: Create VSTO Add-in for Excel
  - URL: https://learn.microsoft.com/en-us/visualstudio/vsto/walkthrough-creating-your-first-vsto-add-in-for-excel
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-VSTOEX**: Excel Object Model Overview
  - URL: https://learn.microsoft.com/en-us/visualstudio/vsto/excel-object-model-overview
  - Accessed: 2026-02-27

### Security and Trust

- **AXCEL-SC-MSFT-SECNT**: Security Notes for Office Developers
  - URL: https://learn.microsoft.com/en-us/office/vba/library-reference/concepts/security-notes-for-microsoft-office-solution-developers
  - Accessed: 2026-02-27

- **AXCEL-SC-MSFT-SECVB**: Programmatic Access to VBA Project
  - URL: https://support.microsoft.com/en-us/topic/programmatic-access-to-office-vba-project-is-denied-960d5265-6592-9400-31bc-b2ddfb94b445
  - Accessed: 2026-02-27

## Community Sources (Tier 3)

### Stack Overflow

- **AXCEL-SC-SO-INTALT**: Excel Interop Alternative
  - URL: https://stackoverflow.com/questions/7002256/excel-interop-alternative
  - Accessed: 2026-02-27
  - Summary: Comparison of interop alternatives

- **AXCEL-SC-SO-OLEXML**: OLE DB vs Open XML vs Interop
  - URL: https://stackoverflow.com/questions/10365434/ole-db-vs-open-xml-sdk-vs-excel-interop
  - Accessed: 2026-02-27
  - Summary: Comparison of approaches for Excel file access

- **AXCEL-SC-SO-ATTACH**: Attach to Existing Excel Instance
  - URL: https://stackoverflow.com/questions/23655210/attach-to-existing-excel-instance
  - Accessed: 2026-02-27
  - Summary: How to connect to running Excel

- **AXCEL-SC-SO-VBAIMP**: Import VBA Code Programmatically
  - URL: https://stackoverflow.com/questions/12049894/import-code-modules-programmatically-to-excel-workbook
  - Accessed: 2026-02-27
  - Summary: VBProject manipulation techniques

- **AXCEL-SC-SO-VBAEXP**: Export VBA to Text Files
  - URL: https://gist.github.com/steve-jansen/7589478
  - Accessed: 2026-02-27
  - Summary: Macro to export all VBA code

### Third-Party Libraries

- **AXCEL-SC-GH-IMPEXL**: ImportExcel PowerShell Module
  - URL: https://github.com/dfinke/ImportExcel
  - Accessed: 2026-02-27
  - Summary: PowerShell Excel automation without Excel installed

- **AXCEL-SC-WEB-XLWNG**: xlwings Python Library
  - URL: https://www.xlwings.org/
  - Accessed: 2026-02-27
  - Summary: Python Excel automation with COM and macOS support

- **AXCEL-SC-SO-PYCOMP**: Python Excel Libraries Comparison
  - URL: https://stackoverflow.com/questions/58328776/differences-between-xlwings-vs-openpyxl
  - Accessed: 2026-02-27
  - Summary: xlwings vs openpyxl comparison

## Related Technologies (Not Covered)

- **Excel Services** (SharePoint Server) - Deprecated, superseded by Excel Online
- **Excel Calculation Services** - Part of Excel Services, deprecated
- **Excel Web Services** - SOAP API, deprecated in favor of Graph API
- **Power Query M language** - Data transformation, not general automation

## Document History

**[2026-02-27 12:30]**
- Initial source collection: 28 official sources, 8 community sources
- Identified 9 distinct Excel APIs/approaches
