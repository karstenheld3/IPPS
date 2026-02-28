# Excel APIs - Table of Contents

**Doc ID**: AXCEL-TOC-01
**Research stats**: 180m net | 19 docs | 52 sources
**Coverage**: 100% (all 9 APIs documented, 5 comprehensive API refs, all 5 use cases addressed, skill implementation researched)

## Summary

This research documents all available Excel APIs for programmatic automation, with special focus on agent-based remote control scenarios for the Windsurf Cascade agent. Nine distinct APIs/approaches are covered: Excel VBA (built-in macro language), COM/Interop API (Windows automation), Open XML SDK (file manipulation without Excel), Microsoft Graph API (cloud/REST access), Excel JavaScript API (Office Add-ins), Office Scripts (TypeScript automation), XLL SDK (native C/C++ add-ins), VSTO (Visual Studio Tools for Office), and third-party libraries (Python, PowerShell). Each API is evaluated for supported features, use cases, limitations, security requirements, and suitability for specific automation scenarios including remote control of open workbooks, VBA code manipulation, and CSV export.

## Feature Comparison Matrix

| Capability | VBA | COM | Open XML | Graph | JS API | Scripts | XLL | VSTO | 3rd Party |
|------------|-----|-----|----------|-------|--------|---------|-----|------|-----------|
| Read cells/data | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Write cells/data | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Read formulas | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Partial |
| Write formulas | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Partial |
| Remote control open workbook | Yes | Yes | No | No | Yes* | No | Yes | Yes | Partial |
| Export to CSV | Yes | Yes | No | No | Yes | Yes | No | Yes | Yes |
| Export VBA code | Yes | Yes | No | No | No | No | No | Yes | Partial |
| Import VBA code | Yes | Yes | No | No | No | No | No | Yes | Partial |
| Works without Excel | No | No | Yes | Yes | No | No | No | No | Partial |
| Cross-platform | No | No | Yes | Yes | Yes | Yes | No | No | Partial |
| Requires Excel installed | Yes | Yes | No | No | Yes* | No | Yes | Yes | Partial |

*JS API requires Excel running as host for add-in

## Decision Workflow

```
START: What is your use case?
│
├─> Need to control Excel while user has it open?
│   ├─> Windows only? -> COM/Interop API or VBA
│   └─> Cross-platform? -> Excel JS API (Add-in)
│
├─> Need to manipulate VBA code?
│   ├─> Export VBA? -> VBA + VBProject or COM + VBProject
│   └─> Import VBA? -> VBA + VBProject or COM + VBProject
│
├─> Need to work without Excel installed?
│   ├─> Local files? -> Open XML SDK or ImportExcel (PowerShell)
│   └─> Cloud files? -> Microsoft Graph API
│
├─> Need high-performance calculations?
│   └─> -> XLL SDK (C/C++)
│
├─> Need to deploy as Excel add-in?
│   ├─> Web-based? -> Excel JS API
│   └─> Desktop .NET? -> VSTO
│
└─> Simple read/write Excel files?
    ├─> Python? -> openpyxl (file) or xlwings (COM)
    ├─> PowerShell? -> ImportExcel module
    └─> C#/.NET? -> Open XML SDK or COM Interop
```

## API Documentation Files

### Core Microsoft APIs (Overview)

- [x] `_INFO_AXCEL-IN01_VBA.md` - Excel VBA (Built-in Macro Language)
- [x] `_INFO_AXCEL-IN02_COM.md` - Excel COM/Interop API
- [x] `_INFO_AXCEL-IN03_OPENXML.md` - Open XML SDK
- [x] `_INFO_AXCEL-IN04_GRAPH.md` - Microsoft Graph API
- [x] `_INFO_AXCEL-IN05_JSAPI.md` - Excel JavaScript API
- [x] `_INFO_AXCEL-IN06_SCRIPTS.md` - Office Scripts
- [x] `_INFO_AXCEL-IN07_XLL.md` - Excel XLL SDK (C API)
- [x] `_INFO_AXCEL-IN08_VSTO.md` - Visual Studio Tools for Office

### Comprehensive API References

- [x] `_INFO_AXCEL-IN01_VBA_API.md` - VBA Object Model Complete Reference (745 lines)
- [x] `_INFO_AXCEL-IN02_COM_API.md` - COM/Interop Complete Reference (850+ lines)
- [x] `_INFO_AXCEL-IN03_OPENXML_API.md` - Open XML SDK Complete Reference (700+ lines)
- [x] `_INFO_AXCEL-IN07_XLL_API.md` - XLL SDK C API Complete Reference (600+ lines)
- [x] `_INFO_AXCEL-IN08_VSTO_API.md` - VSTO API Complete Reference (700+ lines)

### Third-Party and Supplementary

- [x] `_INFO_AXCEL-IN09_THIRDPARTY.md` - Third-Party Libraries (Python, PowerShell)

### Cross-Cutting Topics

- [x] `_INFO_AXCEL-IN10_SECURITY.md` - Security and Trust Settings
- [x] `_INFO_AXCEL-IN11_REMOTECONTROL.md` - Remote Control Scenarios
- [x] `_INFO_AXCEL-IN12_VBAMANIP.md` - VBA Code Manipulation

### Skill Implementation

- [x] `_INFO_AXCEL-IN13_SKILL_OPTIONS.md` - Skill Implementation Options (PowerShell vs Add-In vs Server)
- [x] `_INFO_AXCEL-IN14_XLWINGS.md` - xlwings Python Server (comprehensive, 850+ lines)

## Topic Structure (Per API)

Each API document follows this structure:

1. **Overview** - What it is, when introduced, current status
2. **Supported Features** - Capabilities matrix
3. **Intended Use Cases** - Primary scenarios
4. **Limitations** - What it cannot do
5. **Security Setup** - Trust settings, permissions, signing
6. **Platform Support** - Windows, Mac, Web, Linux
7. **Prerequisites** - What needs to be installed
8. **Code Examples** - Working samples in relevant languages
9. **Gotchas and Quirks** - Undocumented behavior, edge cases
10. **Main Documentation Links** - Official references
11. **Sources** - All sources with IDs

## Use Case Coverage

### UC-1: Export Excel Workbooks as CSV

**Requirements**: All sheets, data and formulas

**Recommended APIs**:
- **COM/Interop** - Best for preserving formula results, can export all sheets
- **VBA** - Same capabilities as COM, runs within Excel
- **Open XML SDK** - Can read formulas as strings, but no calculation

### UC-2: Write into Excel Workbooks

**Requirements**: Data and formulas

**Recommended APIs**:
- **COM/Interop** - Full write access, formulas evaluated
- **Open XML SDK** - Write formulas as strings, no evaluation
- **Graph API** - Write to cloud workbooks via REST

### UC-3: Remote Control Open Workbooks

**Requirements**: Write cells, navigation, trigger calculation

**Recommended APIs**:
- **COM/Interop** - GetActiveObject or BindToMoniker to attach
- **VBA** - If running from within Excel or another workbook
- **Excel JS API** - If deployed as add-in within the workbook

### UC-4: Export VBA Code from XLSM

**Requirements**: Extract all VBA modules, forms, class modules

**Recommended APIs**:
- **COM/Interop + VBProject** - Full access to VBA components
- **VBA** - Direct VBProject access from within Excel

**Security**: Requires "Trust access to the VBA project object model"

### UC-5: Add/Update VBA Code in Workbooks

**Requirements**: Programmatically modify VBA code

**Recommended APIs**:
- **COM/Interop + VBProject** - Import/export .bas, .cls, .frm files
- **VBA** - VBComponents.Import, CodeModule.InsertLines

**Security**: Requires "Trust access to the VBA project object model"

## Document History

**[2026-02-27 16:30]**
- Updated TOC with all 19 INFO documents
- Added Comprehensive API References section (5 deep-dive docs)
- Updated research stats: 180m net, 19 docs, 52 sources

**[2026-02-27 12:45]**
- Initial TOC creation with 12 planned documents
- Feature comparison matrix drafted
- Decision workflow created
- Use case coverage mapped to APIs
