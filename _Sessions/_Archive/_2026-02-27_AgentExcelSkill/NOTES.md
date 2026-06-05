# Session Notes

**Doc ID**: 2026-02-27_AgentExcelSkill-NOTES
**TOPIC**: AXCEL (registered in ID-REGISTRY.md)
**Started**: 2026-02-27
**Goal**: Explore possibilities for creating an Agent Excel skill with maximum Excel file control from Windsurf Cascade Agent

## Current Phase

**Phase**: EXPLORE (completed) -> DESIGN (pending)
**Workflow**: SOLVE (RESEARCH) -> BUILD
**Assessment**: COMPLEXITY-MEDIUM (multi-file skill with scripts)

## User Prompts

I want to explore the possibilities of creating an Agent Excel skill. The aim is to have as much control over excel files as possible from the Winsurf Cascade Agent.

Here are the use cases we need:
- Export Excel workbooks as CSV (all sheets, data and formulas)
- Write into Excel workbooks (data and formulas)
- Remote control Excel workbooks that are opened by the user (write into cells, navigation, trigger calculation, etc.)
- Export all VBA code from XLSM files
- Add / update VBA code in Excel workbooks

## IMPORTANT: Cascade Agent Instructions

1. **Source/Sync Rule**: DevSystem is source, `.windsurf` is sync target. Never edit `.windsurf` directly.
2. **Gate Evidence**: Phase transitions require actual deliverables (files created).
3. **MNF Technique**: Create MUST-NOT-FORGET list for critical items.
4. **MEPI Research**: Default to 2-3 curated options, not exhaustive lists.
5. **TOPIC Registration**: New TOPICs must be registered in ID-REGISTRY.md.

## Key Decisions

1. **Remote Control**: Use COM automation (PowerShell/Python) - only viable approach for attaching to user's open Excel
2. **VBA Manipulation**: Requires "Trust access to VBA project object model" - security trade-off documented
3. **File Operations**: Open XML SDK or ImportExcel for file-only operations without Excel
4. **Recommended Stack**: PowerShell scripts for Cascade agent (native COM support, no dependencies)

## Important Findings

### Excel APIs Identified (9 total)

1. **Excel VBA** - Built-in macro language, full object model
2. **COM/Interop** - External process automation, Windows only
3. **Open XML SDK** - File manipulation without Excel, cross-platform
4. **Microsoft Graph** - Cloud/REST API for SharePoint/OneDrive files
5. **Excel JS API** - Office Add-ins, cross-platform
6. **Office Scripts** - TypeScript for Excel on web
7. **XLL SDK** - High-performance C/C++ add-ins
8. **VSTO** - .NET desktop add-ins
9. **Third-party** - openpyxl, xlwings, ImportExcel

### Use Case Recommendations

| Use Case | Best API | Alternative |
|----------|----------|-------------|
| Export CSV (all sheets) | COM/VBA | Open XML + manual |
| Write data/formulas | COM | Open XML (no calc) |
| Remote control open Excel | COM | xlwings (Python) |
| Export VBA code | COM + VBProject | VBA macro |
| Import VBA code | COM + VBProject | VBA macro |

### Remote Control Key Points

- Use `GetActiveObject("Excel.Application")` to attach to running Excel
- Excel registers in ROT after losing focus (add delay if needed)
- For specific workbook: `BindToMoniker(path)` instead of GetActiveObject
- Full implementation in `_INFO_AXCEL-IN11_REMOTECONTROL.md`

### VBA Manipulation Key Points

- Requires trust setting: File > Options > Trust Center > Macro Settings > "Trust access to VBA project object model"
- Export: `VBComponent.Export(path)`
- Import: `VBProject.VBComponents.Import(path)`
- Document modules (Sheet, ThisWorkbook) cannot be exported/imported directly
- Full implementation in `_INFO_AXCEL-IN12_VBAMANIP.md`

## Workflows to Run on Resume

1. `/prime` - reload context
2. `/recap` - assess current status
