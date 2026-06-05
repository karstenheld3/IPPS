# INFO: Excel COM/Interop Complete API Reference

**Doc ID**: AXCEL-IN02-API
**Goal**: Comprehensive documentation of all Excel COM/Interop exposed interfaces, methods, properties, and events
**Version Scope**: Excel 2016+ / Microsoft 365 (2026-02-27)
**Source**: Microsoft Learn - Microsoft.Office.Interop.Excel Namespace

**Depends on:**
- `_INFO_AXCEL-IN02_COM.md [AXCEL-IN02]` for COM overview and usage
- `_INFO_AXCEL-IN01_VBA_API.md [AXCEL-IN01-API]` for underlying object model (identical)

## Table of Contents

1. Namespace Overview
2. Core Interfaces
3. Application Interface
4. Workbook Interface
5. Worksheet Interface
6. Range Interface
7. Supporting Interfaces
8. Collections
9. Enumerations
10. Event Delegates
11. COM-Specific Patterns
12. Code Examples from Official Documentation

**Out of Scope**: Internal interfaces (prefixed with `I` reserved for internal use), SinkHelper classes.

**Key Insight**: The COM Interop API exposes the **same object model as VBA** through .NET interfaces. Every VBA object has a corresponding COM interface. This reference focuses on COM-specific patterns; see `_INFO_AXCEL-IN01_VBA_API.md` for detailed object model documentation.

`[VERIFIED] (https://learn.microsoft.com/en-us/dotnet/api/microsoft.office.interop.excel?view=excel-pia)`

## 1. Namespace Overview

The `Microsoft.Office.Interop.Excel` namespace provides managed access to Excel's COM type library.

### 1.1 Assembly Information

- **Assembly**: Microsoft.Office.Interop.Excel.dll
- **Namespace**: Microsoft.Office.Interop.Excel
- **Type**: Primary Interop Assembly (PIA)
- **COM Type Library**: Excel.exe (embedded)

**Threading Note**: COM requires Single-Threaded Apartment (STA). Console apps must use `[STAThread]` attribute on Main method.

### 1.2 Type Categories

**Classes** (13 internal):
- ApplicationClass, WorkbookClass, WorksheetClass, ChartClass, OLEObjectClass, QueryTableClass, GlobalClass
- Event sink helpers: AppEvents_SinkHelper, ChartEvents_SinkHelper, DocEvents_SinkHelper, WorkbookEvents_SinkHelper, OLEObjectEvents_SinkHelper, RefreshEvents_SinkHelper

**Interfaces** (300+):
- Primary interfaces: Application, Workbook, Worksheet, Range, Chart
- Collection interfaces: Workbooks, Worksheets, Sheets, Charts, Names
- Supporting interfaces: Font, Interior, Border, Validation, etc.
- Event interfaces: AppEvents_Event, WorkbookEvents_Event, DocEvents_Event

**Enumerations** (200+):
- XlCalculation, XlFileFormat, XlChartType, XlDirection, etc.

**Delegates** (45+):
- Event handlers for Application, Workbook, Worksheet, Chart events

### 1.3 Interface Naming Conventions

- **Primary Interface**: `_Application`, `_Workbook`, `_Worksheet` - Use for method calls when name conflicts with events
- **Coclass Interface**: `Application`, `Workbook`, `Worksheet` - Main interface for general use
- **Events Interface**: `AppEvents_Event`, `WorkbookEvents_Event` - Connect to events
- **Internal Interface**: `IApplication`, `IWorkbook` (I prefix) - Reserved for internal use

## 2. Core Interfaces

### 2.1 Primary COM Interfaces

- **Application** - Represents the entire Excel application
- **Workbook** - Represents a single Excel workbook
- **Worksheet** - Represents a single worksheet
- **Range** - Represents a cell, row, column, or selection of cells
- **Chart** - Represents a chart (embedded or chart sheet)
- **Global** - Provides global methods and properties

### 2.2 Interface Hierarchy

```
Application
├── Workbooks (collection) → Workbook
│   ├── Worksheets (collection) → Worksheet
│   │   ├── Range / Cells / Rows / Columns
│   │   ├── ChartObjects → ChartObject → Chart
│   │   ├── ListObjects → ListObject
│   │   ├── PivotTables → PivotTable
│   │   ├── Shapes → Shape
│   │   └── Comments → Comment
│   ├── Charts (collection) → Chart
│   ├── Names (collection) → Name
│   └── VBProject
├── Windows (collection) → Window
├── AddIns (collection) → AddIn
└── WorksheetFunction
```

## 3. Application Interface

Represents the entire Microsoft Excel application.

`[VERIFIED] (https://learn.microsoft.com/en-us/dotnet/api/microsoft.office.interop.excel.application?view=excel-pia)`

### 3.1 Application Properties (150+)

**Active Elements:**
- ActiveCell, ActiveChart, ActivePrinter, ActiveSheet, ActiveWindow, ActiveWorkbook

**Collections:**
- AddIns, AddIns2, Charts, Columns, CommandBars, Dialogs, Names, RecentFiles, Rows, Sheets, Windows, Workbooks, Worksheets

**Calculation:**
- Calculation, CalculateBeforeSave, CalculationInterruptKey, CalculationState, CalculationVersion, Iteration, MaxChange, MaxIterations

**Display:**
- DisplayAlerts, DisplayClipboardWindow, DisplayCommentIndicator, DisplayFormulaAutoComplete, DisplayFormulaBar, DisplayFullScreen, DisplayNoteIndicator, DisplayPasteOptions, DisplayScrollBars, DisplayStatusBar, ScreenUpdating, Visible

**Enable:**
- EnableAnimations, EnableAutoComplete, EnableCancelKey, EnableEvents, EnableLargeOperationAlert, EnableLivePreview, EnableSound

**Other Key Properties:**
- Application, Build, Caller, Caption, Cells, CutCopyMode, DataEntryMode, DecimalSeparator, DefaultFilePath, DefaultSaveFormat, EditDirectlyInCell, FixedDecimal, Interactive, MoveAfterReturn, Name, OperatingSystem, Path, Range, ReferenceStyle, Selection, StandardFont, StandardFontSize, StatusBar, ThisWorkbook, ThousandsSeparator, UserName, Version, WorksheetFunction

### 3.2 Application Methods (48)

- ActivateMicrosoftApp, AddCustomList, Calculate, CalculateFull, CalculateFullRebuild, CalculateUntilAsyncQueriesDone
- CentimetersToPoints, CheckAbort, CheckSpelling, ConvertFormula
- DDEExecute, DDEInitiate, DDEPoke, DDERequest, DDETerminate
- DeleteCustomList, DisplayXMLSourcePane, DoubleClick, Evaluate, ExecuteExcel4Macro
- FindFile, GetCustomListContents, GetCustomListNum, GetOpenFilename, GetPhonetic, GetSaveAsFilename
- Goto, Help, InchesToPoints, InputBox, Intersect
- MacroOptions, MailLogoff, MailLogon, NextLetter
- OnKey, OnRepeat, OnTime, OnUndo
- Quit, RecordMacro, RegisterXLL, Repeat, Run
- SendKeys, SharePointVersion, Undo, Union, Volatile, Wait

### 3.3 Application Events (45)

Events are accessed via the `AppEvents_Event` interface:

- AfterCalculate, NewWorkbook
- ProtectedViewWindowActivate, ProtectedViewWindowBeforeClose, ProtectedViewWindowBeforeEdit, ProtectedViewWindowDeactivate, ProtectedViewWindowOpen, ProtectedViewWindowResize
- SheetActivate, SheetBeforeDelete, SheetBeforeDoubleClick, SheetBeforeRightClick, SheetCalculate, SheetChange, SheetDeactivate, SheetFollowHyperlink, SheetPivotTableAfterValueChange, SheetPivotTableBeforeAllocateChanges, SheetPivotTableBeforeCommitChanges, SheetPivotTableBeforeDiscardChanges, SheetPivotTableUpdate, SheetSelectionChange, SheetTableUpdate
- WindowActivate, WindowDeactivate, WindowResize
- WorkbookActivate, WorkbookAddinInstall, WorkbookAddinUninstall, WorkbookAfterSave, WorkbookAfterXmlExport, WorkbookAfterXmlImport, WorkbookBeforeClose, WorkbookBeforePrint, WorkbookBeforeSave, WorkbookBeforeXmlExport, WorkbookBeforeXmlImport, WorkbookDeactivate, WorkbookModelChange, WorkbookNewChart, WorkbookNewSheet, WorkbookOpen, WorkbookPivotTableCloseConnection, WorkbookPivotTableOpenConnection, WorkbookRowsetComplete, WorkbookSync

## 4. Workbook Interface

Represents a single Excel workbook.

`[VERIFIED] (https://learn.microsoft.com/en-us/dotnet/api/microsoft.office.interop.excel.workbook?view=excel-pia)`

### 4.1 Workbook Properties (100+)

- AccuracyVersion, ActiveChart, ActiveSheet, ActiveSlicer, Application, AutoSaveOn, AutoUpdateFrequency
- BuiltinDocumentProperties, CalculationVersion, CaseSensitive, ChangeHistoryDuration, ChartDataPointTrack, Charts, CheckCompatibility, CodeName, Colors, CommandBars, ConflictResolution, Connections, ConnectionsDisabled, Container, ContentTypeProperties, CreateBackup, Creator, CustomDocumentProperties, CustomViews, CustomXMLParts, Date1904
- DefaultPivotTableStyle, DefaultSlicerStyle, DefaultTableStyle, DisplayDrawingObjects
- EnableAutoRecover, EncryptionProvider, Excel4IntlMacroSheets, Excel4MacroSheets, Excel8CompatibilityMode
- FileFormat, Final, ForceFullCalculation, FullName, FullNameURLEncoded
- HasPassword, HasVBProject, HighlightChangesOnScreen, IconSets, InactiveListBorderVisible, IsAddin, IsInplace
- KeepChangeHistory, ListChangesOnNewSheet, Model, MultiUserEditing, Name, Names, Parent, Password, Path, Permission, PersonalViewListSettings, PivotTables, PrecisionAsDisplayed, ProtectStructure, ProtectWindows, PublishObjects
- Queries, ReadOnly, ReadOnlyRecommended, Research, RevisionNumber
- Saved, SaveLinkValues, Sheets, ShowConflictHistory, ShowPivotTableFieldList, Signatures, SlicerCaches, SmartDocument, Styles
- TableStyles, Theme, UpdateLinks, UserStatus, VBASigned, VBProject
- WebOptions, Windows, Worksheets, WritePassword, WriteReserved, WriteReservedBy, XmlMaps, XmlNamespaces

### 4.2 Workbook Methods (60+)

- AcceptAllChanges, Activate, AddToFavorites, ApplyTheme, BreakLink
- CanCheckIn, ChangeFileAccess, ChangeLink, CheckIn, CheckInWithVersion, Close, ConvertComments, CreateForecastSheet
- DeleteNumberFormat, EnableConnections, EndReview, ExclusiveAccess, ExportAsFixedFormat
- FollowHyperlink, GetWorkflowTasks, GetWorkflowTemplates, HighlightChangesOptions
- LinkInfo, LinkSources, LockServerFile, MergeWorkbook
- NewWindow, OpenLinks, PivotCaches, Post, PrintOut, PrintPreview, Protect, ProtectSharing, PublishToDocs, PurgeChangeHistoryNow
- RefreshAll, RejectAllChanges, ReloadAs, RemoveDocumentInformation, RemoveUser, Reply, ReplyAll, ReplyWithChanges, ResetColors, RunAutoMacros
- Save, SaveAs, SaveCopyAs, SendForReview, SendMail, SetLinkOnData, SetPasswordEncryptionOptions
- ToggleFormsDesign, Unprotect, UnprotectSharing, UpdateFromFile, UpdateLink
- WebPagePreview, XmlImport, XmlImportXml

### 4.3 Workbook Events (40+)

Events are accessed via the `WorkbookEvents_Event` interface:

- Activate, AddinInstall, AddinUninstall, AfterRemoteChange, AfterSave, AfterXmlExport, AfterXmlImport
- BeforeClose, BeforePrint, BeforeRemoteChange, BeforeSave, BeforeXmlExport, BeforeXmlImport
- Deactivate, ModelChange, NewChart, NewSheet, Open
- PivotTableCloseConnection, PivotTableOpenConnection, RowsetComplete
- SheetActivate, SheetBeforeDelete, SheetBeforeDoubleClick, SheetBeforeRightClick, SheetCalculate, SheetChange, SheetDeactivate, SheetFollowHyperlink, SheetPivotTableUpdate, SheetSelectionChange, SheetTableUpdate
- Sync, WindowActivate, WindowDeactivate, WindowResize

## 5. Worksheet Interface

Represents a single worksheet.

`[VERIFIED] (https://learn.microsoft.com/en-us/dotnet/api/microsoft.office.interop.excel.worksheet?view=excel-pia)`

### 5.1 Worksheet Properties (60+)

- Application, AutoFilter, AutoFilterMode, Cells, CircularReference, CodeName, Columns, Comments, CommentsThreaded
- ConsolidationFunction, ConsolidationOptions, ConsolidationSources, Creator, CustomProperties
- DisplayPageBreaks, DisplayRightToLeft, EnableAutoFilter, EnableCalculation, EnableFormatConditionsCalculation, EnableOutlining, EnablePivotTable, EnableSelection, FilterMode
- HPageBreaks, Hyperlinks, Index, ListObjects, MailEnvelope
- Name, Names, Next, Outline, PageSetup, Parent, Previous, PrintedCommentPages
- ProtectContents, ProtectDrawingObjects, Protection, ProtectionMode, ProtectScenarios
- QueryTables, Range, Rows, ScrollArea, Shapes, Sort, SpellingOptions
- StandardHeight, StandardWidth, Tab, TransitionExpEval, TransitionFormEntry, Type, UsedRange, Visible, VPageBreaks

### 5.2 Worksheet Methods (29)

- Activate, Calculate, ChartObjects, CheckSpelling, CircleInvalid, ClearArrows, ClearCircles
- Copy, Delete, Evaluate, ExportAsFixedFormat
- Move, OLEObjects, Paste, PasteSpecial, PivotTables, PivotTableWizard
- PrintOut, PrintPreview, Protect, ResetAllPageBreaks
- SaveAs, Scenarios, Select, SetBackgroundPicture, ShowAllData, ShowDataForm
- Unprotect, XmlDataQuery, XmlMapQuery

### 5.3 Worksheet Events (17)

Events are accessed via the `DocEvents_Event` interface:

- Activate, BeforeDelete, BeforeDoubleClick, BeforeRightClick
- Calculate, Change, Deactivate, FollowHyperlink
- LensGalleryRenderComplete, PivotTableAfterValueChange, PivotTableBeforeAllocateChanges, PivotTableBeforeCommitChanges, PivotTableBeforeDiscardChanges, PivotTableChangeSync, PivotTableUpdate
- SelectionChange, TableUpdate

## 6. Range Interface

The most important interface for cell manipulation.

`[VERIFIED] (https://learn.microsoft.com/en-us/dotnet/api/microsoft.office.interop.excel.range?view=excel-pia)`

### 6.1 Range Properties (90+)

**Values:**
- Value, Value2, Text, Formula, FormulaArray, FormulaLocal, FormulaR1C1, FormulaR1C1Local, FormulaHidden, HasFormula, HasArray, HasRichDataType

**References:**
- Address, AddressLocal, Item, Offset, Range, Resize, Cells, Rows, Columns, Row, Column, EntireRow, EntireColumn, Areas, End, Next, Previous, CurrentArray, CurrentRegion

**Dependencies:**
- Dependents, DirectDependents, Precedents, DirectPrecedents

**Formatting:**
- Font, Interior, Borders, Style, DisplayFormat, FormatConditions, NumberFormat, NumberFormatLocal, HorizontalAlignment, VerticalAlignment, Orientation, IndentLevel, ShrinkToFit, WrapText, AddIndent, ReadingOrder, Locked, Hidden

**Size:**
- Width, Height, ColumnWidth, RowHeight, Left, Top, UseStandardHeight, UseStandardWidth

**Count:**
- Count, CountLarge

**Merge:**
- MergeCells, MergeArea

**Dynamic Arrays (Excel 365):**
- HasSpill, SpillingToRange, SpillParent

**Other:**
- AllowEdit, Characters, Comment, CommentThreaded, Creator, Errors, Hyperlinks, ID, LinkedDataTypeState, ListHeaderRows, ListObject, LocationInTable, MDX, Name, PageBreak, Parent, Phonetic, Phonetics, PivotCell, PivotField, PivotItem, PivotTable, PrefixCharacter, QueryTable, ServerActions, ShowDetail, SoundNote, SparklineGroups, Summary, Validation, Worksheet, XPath

### 6.2 Range Methods (75+)

**Navigation:** Activate, Select

**Editing:** Clear, ClearComments, ClearContents, ClearFormats, ClearHyperlinks, ClearNotes, ClearOutline, Copy, Cut, Delete, Insert, Merge, UnMerge

**Fill:** AutoFill, DataSeries, FillDown, FillLeft, FillRight, FillUp

**Calculation:** Calculate, CalculateRowMajorOrder, Dirty

**Data:** AdvancedFilter, AutoFilter, AutoOutline, Consolidate, CopyFromRecordset, Parse, RemoveDuplicates, RemoveSubtotal, Sort, SortSpecial, SpecialCells, Subtotal, Table, TextToColumns

**Search:** AutoComplete, Find, FindNext, FindPrevious, Replace

**Comparison:** ColumnDifferences, RowDifferences

**Comments:** AddComment, AddCommentThreaded, NoteText

**Formatting:** ApplyNames, ApplyOutlineStyles, AutoFit, BorderAround, InsertIndent

**Output:** CopyPicture, ExportAsFixedFormat, PrintOut, PrintPreview

**Other:** AllocateChanges, CheckSpelling, DialogBox, DiscardChanges, FunctionWizard, Group, Justify, ListNames, NavigateArrow, PasteSpecial, Run, SetPhonetic, Show, ShowDependents, ShowErrors, ShowPrecedents, Speak, Ungroup

## 7. Supporting Interfaces

### 7.1 Chart Interface

Represents a chart in a workbook.

**Methods:** Activate, ApplyChartTemplate, ApplyDataLabels, ApplyLayout, Axes, ChartWizard, ClearToMatchStyle, Copy, CopyPicture, Delete, Export, ExportAsFixedFormat, FullSeriesCollection, GetChartElement, Location, Move, Paste, PrintOut, PrintPreview, Protect, Refresh, SaveAs, SaveChartTemplate, Select, SeriesCollection, SetBackgroundPicture, SetDefaultChart, SetElement, SetSourceData, Unprotect

**Properties:** Application, AutoScaling, BackWall, BarShape, CategoryLabelLevel, ChartArea, ChartColor, ChartStyle, ChartTitle, ChartType, CodeName, Creator, DataTable, DepthPercent, DisplayBlanksAs, Elevation, Floor, GapDepth, HasAxis, HasDataTable, HasLegend, HasTitle, HeightPercent, Hyperlinks, Index, Legend, Name, PageSetup, Parent, Perspective, PivotLayout, PlotArea, PlotBy, PlotVisibleOnly, ProtectContents, ProtectData, ProtectDrawingObjects, ProtectFormatting, ProtectGoalSeek, ProtectionMode, ProtectSelection, RightAngleAxes, Rotation, SeriesNameLevel, Shapes, Visible, Walls

### 7.2 PivotTable Interface

Represents a PivotTable report on a worksheet.

**Methods:** AddDataField, AddFields, AllocateChanges, CalculatedFields, ChangeConnection, ChangePivotCache, ClearAllFilters, ClearTable, CommitChanges, ConvertToFormulas, CreateCubeFile, DiscardChanges, DrillDown, DrillTo, DrillUp, GetData, GetPivotData, ListFormulas, PivotCache, PivotFields, PivotSelect, PivotTableWizard, PrintPreview, PrintOut, RefreshDataSourceValues, RefreshTable, RepeatAllLabels, RowAxisLayout, ShowPages, SubtotalLocation, Update

**Properties:** ActiveFilters, Allocation, AllocationMethod, AllocationValue, AllocationWeightExpression, AllowMultipleFilters, AlternativeText, CacheIndex, CalculatedMembers, ChangeList, ColumnFields, ColumnGrand, ColumnRange, CompactLayoutColumnHeader, CompactLayoutRowHeader, CompactRowIndent, Creator, CubeFields, DataBodyRange, DataFields, DataLabelRange, DataPivotField, DisplayContextTooltips, DisplayEmptyColumn, DisplayEmptyRow, DisplayErrorString, DisplayFieldCaptions, DisplayImmediateItems, DisplayMemberPropertyTooltips, DisplayNullString, EnableDataValueEditing, EnableDrilldown, EnableFieldDialog, EnableFieldList, EnableWizard, EnableWriteback, ErrorString, GrandTotalName, HasAutoFormat, Hidden, HiddenFields, InGridDropZones, InnerDetail, LayoutRowDefault, Location, ManualUpdate, MDX, MergeLabels, Name, NullString, PageFieldOrder, PageFields, Parent, PivotCache, PivotFormulas, PivotSelection, PreserveFormatting, PrintDrillIndicators, PrintTitles, RefreshDate, RefreshName, RowFields, RowGrand, RowRange, SaveData, SelectionMode, Slicers, SmallGrid, SortUsingCustomLists, SourceData, SubtotalHiddenPageItems, Summary, TableRange1, TableRange2, TableStyle2, Tag, TotalsAnnotation, Value, Version, ViewCalculatedMembers, VisibleFields, VisualTotals

### 7.3 ListObject Interface (Table)

Represents a list object (table) on a worksheet.

**Methods:** Delete, ExportToVisio, Publish, Refresh, Resize, Unlink, Unlist

**Properties:** Active, AlternativeText, AutoFilter, Comment, Creator, DataBodyRange, DisplayName, DisplayRightToLeft, HeaderRowRange, InsertRowRange, ListColumns, ListRows, Name, Parent, QueryTable, Range, SharePointURL, ShowAutoFilter, ShowAutoFilterDropDown, ShowHeaders, ShowTableStyleColumnStripes, ShowTableStyleFirstColumn, ShowTableStyleLastColumn, ShowTableStyleRowStripes, ShowTotals, Slicers, Sort, SourceType, Summary, TableStyle, TotalsRowRange, XmlMap

### 7.4 Name Interface

Represents a defined name for a range of cells.

**Methods:** Delete

**Properties:** Application, Category, CategoryLocal, Comment, Creator, Index, MacroType, Name, NameLocal, Parent, RefersTo, RefersToLocal, RefersToR1C1, RefersToR1C1Local, RefersToRange, ShortcutKey, ValidWorkbookParameter, Value, Visible, WorkbookParameter

### 7.5 Font Interface

Represents the font attributes of an object.

**Properties:** Application, Background, Bold, Color, ColorIndex, Creator, FontStyle, Italic, Name, OutlineFont, Parent, Shadow, Size, Strikethrough, Subscript, Superscript, ThemeColor, ThemeFont, TintAndShade, Underline

### 7.6 Interior Interface

Represents the interior of an object.

**Properties:** Application, Color, ColorIndex, Creator, Gradient, InvertIfNegative, Parent, Pattern, PatternColor, PatternColorIndex, PatternThemeColor, PatternTintAndShade, ThemeColor, TintAndShade

### 7.7 Border/Borders Interfaces

Represents the border of an object.

**Border Properties:** Application, Color, ColorIndex, Creator, LineStyle, Parent, ThemeColor, TintAndShade, Weight

**Borders Properties:** Application, Color, ColorIndex, Count, Creator, Item, LineStyle, Parent, ThemeColor, TintAndShade, Value, Weight

### 7.8 Validation Interface

Represents data validation for a worksheet range.

**Methods:** Add, Delete, Modify

**Properties:** AlertStyle, Application, Creator, ErrorMessage, ErrorTitle, Formula1, Formula2, IgnoreBlank, IMEMode, InCellDropdown, InputMessage, InputTitle, Operator, Parent, ShowError, ShowInput, Type, Value

### 7.9 AutoFilter Interface

Represents autofiltering for a worksheet.

**Methods:** ApplyFilter, ShowAllData

**Properties:** Application, Creator, FilterMode, Filters, Parent, Range, Sort

### 7.10 Slicer Interface

Represents a slicer in a workbook.

**Methods:** Copy, Cut, Delete

**Properties:** ActiveItem, Application, Caption, ColumnWidth, Creator, DisableMoveResizeUI, DisplayHeader, Height, Left, Locked, Name, NumberOfColumns, Parent, RowHeight, Shape, SlicerCache, SlicerCacheLevel, SlicerCacheType, Style, TimelineViewState, Top, Width

### 7.11 SlicerCache Interface

Represents the current filter state for a slicer.

**Methods:** ClearAllFilters, ClearDateFilter, ClearManualFilter, Delete

**Properties:** Application, Creator, CrossFilterType, FilterCleared, Index, List, ListObject, Name, OLAP, Parent, PivotTables, ShowAllItems, SlicerCacheLevels, SlicerCacheType, SlicerItems, Slicers, SortItems, SortUsingCustomLists, SourceName, SourceType, TimelineState, VisibleSlicerItems, VisibleSlicerItemsList, WorkbookConnection

### 7.12 Shape Interface

Represents an object in the drawing layer.

**Methods:** Apply, Copy, CopyPicture, Cut, Delete, Duplicate, Flip, IncrementLeft, IncrementRotation, IncrementTop, PickUp, RerouteConnections, ScaleHeight, ScaleWidth, Select, SetShapesDefaultProperties, Ungroup, ZOrder

**Properties:** Adjustments, AlternativeText, Application, AutoShapeType, BackgroundStyle, BlackWhiteMode, BottomRightCell, Callout, Chart, Child, ConnectionSiteCount, Connector, ConnectorFormat, ControlFormat, Creator, Decorative, Fill, FormControlType, Glow, GraphicStyle, GroupItems, HasChart, HasSmartArt, Height, HorizontalFlip, Hyperlink, ID, Left, Line, LinkFormat, LockAspectRatio, Locked, Model3D, Name, Nodes, OLEFormat, OnAction, Parent, ParentGroup, PictureFormat, Placement, Reflection, Rotation, Shadow, ShapeStyle, SmartArt, SoftEdge, TextEffect, TextFrame, TextFrame2, ThreeD, Title, Top, TopLeftCell, Type, VerticalFlip, Vertices, Visible, Width, ZOrderPosition

### 7.13 Window Interface

Represents a window.

**Methods:** Activate, ActivateNext, ActivatePrevious, Close, LargeScroll, NewWindow, PointsToScreenPixelsX, PointsToScreenPixelsY, PrintOut, PrintPreview, RangeFromPoint, ScrollIntoView, ScrollWorkbookTabs, SmallScroll

**Properties:** ActiveCell, ActiveChart, ActivePane, ActiveSheet, ActiveSheetView, Application, AutoFilterDateGrouping, Caption, Creator, DisplayFormulas, DisplayGridlines, DisplayHeadings, DisplayHorizontalScrollBar, DisplayOutline, DisplayRightToLeft, DisplayRuler, DisplayVerticalScrollBar, DisplayWhitespace, DisplayWorkbookTabs, DisplayZeros, EnableResize, FreezePanes, GridlineColor, GridlineColorIndex, Height, Index, Left, OnWindow, Panes, Parent, RangeSelection, ScrollColumn, ScrollRow, SelectedSheets, Selection, SheetViews, Split, SplitColumn, SplitHorizontal, SplitRow, SplitVertical, TabRatio, Top, Type, UsableHeight, UsableWidth, View, Visible, VisibleRange, Width, WindowNumber, WindowState, Zoom

### 7.14 VBProject Interface

Represents a Visual Basic project. Requires Microsoft Visual Basic for Applications Extensibility reference.

**Methods:** SaveAs

**Properties:** BuildFileName, Creator, Description, FileName, HelpContextID, HelpFile, Mode, Name, Protection, References, Type, VBComponents, VBE

### 7.15 Model Interface

Represents the Data Model in a workbook.

**Methods:** AddConnection, CreateModelWorkbookConnection, Initialize, Refresh

**Properties:** Application, Creator, DataModelConnection, ModelFormatBoolean, ModelFormatCurrency, ModelFormatDate, ModelFormatDecimalNumber, ModelFormatGeneral, ModelFormatPercentageNumber, ModelFormatScientificNumber, ModelFormatWholeNumber, ModelMeasures, ModelRelationships, ModelTables, Name, Parent

### 7.16 WorkbookQuery Interface

Represents a Power Query query.

**Properties:** Application, Creator, Description, Formula, Name, Parent

## 8. Collections

### 8.1 Core Collections

- **Workbooks** - All open Workbook objects
- **Worksheets** - All Worksheet objects in a workbook
- **Sheets** - All sheets (worksheets, chart sheets, macro sheets)
- **Charts** - All Chart objects in a workbook
- **Windows** - All Window objects
- **Names** - All Name objects in a workbook/worksheet

### 8.2 Range-Related Collections

- **Areas** - A collection of ranges within a selection
- **Cells** - All cells on a worksheet (returns Range)
- **Rows** - All rows on a worksheet (returns Range)
- **Columns** - All columns on a worksheet (returns Range)

### 8.3 Data Collections

- **PivotTables** - All PivotTable objects on a worksheet
- **PivotCaches** - All PivotCache objects in a workbook
- **PivotFields** - All PivotField objects in a PivotTable
- **PivotItems** - All PivotItem objects in a PivotField
- **ListObjects** - All ListObject (table) objects on a worksheet
- **ListColumns** - Columns in a ListObject
- **ListRows** - Rows in a ListObject
- **QueryTables** - All QueryTable objects on a worksheet
- **Queries** - All Power Query queries in a workbook

### 8.4 Formatting Collections

- **Styles** - All Style objects in a workbook
- **Borders** - All borders of a Range
- **FormatConditions** - All FormatCondition objects for a range
- **ColorScales** - ColorScale objects for conditional formatting
- **DataBars** - DataBar objects for conditional formatting
- **IconSets** - IconSet objects for conditional formatting
- **TableStyles** - All TableStyle objects in a workbook

### 8.5 Shape Collections

- **Shapes** - All Shape objects on a worksheet/chart
- **GroupShapes** - Shapes within a grouped shape
- **ShapeNodes** - Nodes in a freeform shape

### 8.6 Slicer Collections

- **SlicerCaches** - All SlicerCache objects in a workbook
- **Slicers** - All Slicer objects in a SlicerCache
- **SlicerItems** - All SlicerItem objects in a slicer

### 8.7 Comment Collections

- **Comments** - All Comment objects on a worksheet
- **CommentsThreaded** - All threaded comments on a worksheet

### 8.8 Other Collections

- **Hyperlinks** - All Hyperlink objects in a range/worksheet
- **AddIns** - All AddIn objects
- **CommandBars** - All CommandBar objects
- **RecentFiles** - Recently used files
- **CustomViews** - Custom views in a workbook
- **Scenarios** - What-if scenarios on a worksheet
- **HPageBreaks** - Horizontal page breaks
- **VPageBreaks** - Vertical page breaks
- **Connections** - Data connections in a workbook
- **XmlMaps** - XML maps in a workbook

## 9. Enumerations

Excel COM Interop includes 200+ enumerations. Key enumerations by category:

### 9.1 Calculation Enumerations

- **XlCalculation**: xlCalculationAutomatic, xlCalculationManual, xlCalculationSemiautomatic
- **XlCalculationState**: xlCalculating, xlDone, xlPending
- **XlCalculationInterruptKey**: xlAnyKey, xlEscKey, xlNoKey

### 9.2 File Format Enumerations

- **XlFileFormat**: xlCSV, xlCSVUTF8, xlExcel8, xlOpenXMLWorkbook, xlOpenXMLWorkbookMacroEnabled, xlWorkbookDefault, xlXMLSpreadsheet (50+ values)

### 9.3 Direction Enumerations

- **XlDirection**: xlDown, xlToLeft, xlToRight, xlUp
- **XlDeleteShiftDirection**: xlShiftToLeft, xlShiftUp
- **XlInsertShiftDirection**: xlShiftDown, xlShiftToRight

### 9.4 Cell Type Enumerations

- **XlCellType**: xlCellTypeAllFormatConditions, xlCellTypeAllValidation, xlCellTypeBlanks, xlCellTypeComments, xlCellTypeConstants, xlCellTypeFormulas, xlCellTypeLastCell, xlCellTypeSameFormatConditions, xlCellTypeSameValidation, xlCellTypeVisible

### 9.5 Alignment Enumerations

- **XlHAlign**: xlHAlignCenter, xlHAlignCenterAcrossSelection, xlHAlignDistributed, xlHAlignFill, xlHAlignGeneral, xlHAlignJustify, xlHAlignLeft, xlHAlignRight
- **XlVAlign**: xlVAlignBottom, xlVAlignCenter, xlVAlignDistributed, xlVAlignJustify, xlVAlignTop

### 9.6 Border Enumerations

- **XlBordersIndex**: xlDiagonalDown, xlDiagonalUp, xlEdgeBottom, xlEdgeLeft, xlEdgeRight, xlEdgeTop, xlInsideHorizontal, xlInsideVertical
- **XlBorderWeight**: xlHairline, xlMedium, xlThick, xlThin
- **XlLineStyle**: xlContinuous, xlDash, xlDashDot, xlDashDotDot, xlDot, xlDouble, xlLineStyleNone, xlSlantDashDot

### 9.7 Chart Enumerations

- **XlChartType**: xlArea, xlAreaStacked, xlBarClustered, xlBarStacked, xlColumnClustered, xlColumnStacked, xlLine, xlLineMarkers, xlPie, xlPieExploded, xlXYScatter (70+ chart types)
- **XlChartLocation**: xlLocationAsNewSheet, xlLocationAsObject, xlLocationAutomatic
- **XlAxisType**: xlCategory, xlSeriesAxis, xlValue
- **XlAxisGroup**: xlPrimary, xlSecondary

### 9.8 Sort Enumerations

- **XlSortOrder**: xlAscending, xlDescending
- **XlSortOn**: xlSortOnCellColor, xlSortOnFontColor, xlSortOnIcon, xlSortOnValues
- **XlSortOrientation**: xlSortColumns, xlSortRows
- **XlSortDataOption**: xlSortNormal, xlSortTextAsNumbers

### 9.9 Find/Replace Enumerations

- **XlLookAt**: xlPart, xlWhole
- **XlSearchOrder**: xlByColumns, xlByRows
- **XlSearchDirection**: xlNext, xlPrevious
- **XlFindLookIn**: xlComments, xlCommentsThreaded, xlFormulas, xlValues

### 9.10 Validation Enumerations

- **XlDVType**: xlValidateCustom, xlValidateDate, xlValidateDecimal, xlValidateInputOnly, xlValidateList, xlValidateTextLength, xlValidateTime, xlValidateWholeNumber
- **XlDVAlertStyle**: xlValidAlertInformation, xlValidAlertStop, xlValidAlertWarning

### 9.11 Sheet Visibility Enumerations

- **XlSheetVisibility**: xlSheetHidden, xlSheetVeryHidden, xlSheetVisible

### 9.12 Error Value Enumerations

- **XlCVError**: xlErrBlocked, xlErrCalc, xlErrConnect, xlErrDiv0, xlErrField, xlErrGettingData, xlErrNA, xlErrName, xlErrNull, xlErrNum, xlErrRef, xlErrSpill, xlErrUnknown, xlErrValue

## 10. Event Delegates

Event delegates are used to handle COM events in .NET.

### 10.1 Application Event Delegates

- AppEvents_AfterCalculateEventHandler
- AppEvents_NewWorkbookEventHandler
- AppEvents_SheetActivateEventHandler
- AppEvents_SheetBeforeDoubleClickEventHandler
- AppEvents_SheetBeforeRightClickEventHandler
- AppEvents_SheetCalculateEventHandler
- AppEvents_SheetChangeEventHandler
- AppEvents_SheetDeactivateEventHandler
- AppEvents_SheetFollowHyperlinkEventHandler
- AppEvents_SheetSelectionChangeEventHandler
- AppEvents_WindowActivateEventHandler
- AppEvents_WindowDeactivateEventHandler
- AppEvents_WindowResizeEventHandler
- AppEvents_WorkbookActivateEventHandler
- AppEvents_WorkbookAfterSaveEventHandler
- AppEvents_WorkbookBeforeCloseEventHandler
- AppEvents_WorkbookBeforePrintEventHandler
- AppEvents_WorkbookBeforeSaveEventHandler
- AppEvents_WorkbookDeactivateEventHandler
- AppEvents_WorkbookNewSheetEventHandler
- AppEvents_WorkbookOpenEventHandler

### 10.2 Workbook Event Delegates

- WorkbookEvents_ActivateEventHandler
- WorkbookEvents_AfterSaveEventHandler
- WorkbookEvents_BeforeCloseEventHandler
- WorkbookEvents_BeforePrintEventHandler
- WorkbookEvents_BeforeSaveEventHandler
- WorkbookEvents_DeactivateEventHandler
- WorkbookEvents_NewSheetEventHandler
- WorkbookEvents_OpenEventHandler
- WorkbookEvents_SheetActivateEventHandler
- WorkbookEvents_SheetChangeEventHandler
- WorkbookEvents_SheetSelectionChangeEventHandler

### 10.3 Worksheet Event Delegates

- DocEvents_ActivateEventHandler
- DocEvents_BeforeDeleteEventHandler
- DocEvents_BeforeDoubleClickEventHandler
- DocEvents_BeforeRightClickEventHandler
- DocEvents_CalculateEventHandler
- DocEvents_ChangeEventHandler
- DocEvents_DeactivateEventHandler
- DocEvents_FollowHyperlinkEventHandler
- DocEvents_SelectionChangeEventHandler

## 11. COM-Specific Patterns

### 11.1 Creating Excel Application

```csharp
// Create new Excel instance
var excelApp = new Microsoft.Office.Interop.Excel.Application();
excelApp.Visible = true;
```

### 11.2 Attaching to Running Excel

**Note**: `GetActiveObject` is only available in .NET Framework. For .NET 5+, use P/Invoke or `BindToMoniker`.

**ROT Timing**: Excel registers in Running Object Table (ROT) only after losing focus. If `GetActiveObject` fails with 0x800401E3, retry with delay. See: [Microsoft KB Article](https://support.microsoft.com/en-us/topic/getobject-or-getactiveobject-cannot-find-a-running-office-application-6cdf21a3-ac90-512b-6bff-badc5f4cc215)

```csharp
// Method 1: GetActiveObject - gets any running Excel (.NET Framework only)
var excelApp = (Application)Marshal.GetActiveObject("Excel.Application");

// Method 2: BindToMoniker - attach to specific file (works in .NET 5+)
var workbook = (Workbook)Marshal.BindToMoniker(@"C:\path\to\file.xlsx");
Application excelApp = workbook.Application;
```

### 11.3 COM Object Cleanup (Critical)

**Two-Dot Rule**: Never chain property accessors. Each dot creates an intermediate COM object that must be released.

```csharp
// BAD - Range object from worksheet.Range["A1"] is never released
worksheet.Range["A1"].Value = "test";

// GOOD - Capture and release every COM object
Range range = worksheet.Range["A1"];
range.Value = "test";
Marshal.ReleaseComObject(range);
```

**Basic Cleanup Pattern**:
```csharp
// Always release COM objects to prevent memory leaks
Marshal.ReleaseComObject(worksheet);
Marshal.ReleaseComObject(workbook);
Marshal.ReleaseComObject(excelApp);

// For thorough cleanup
GC.Collect();
GC.WaitForPendingFinalizers();
```

### 11.4 Event Handling

```csharp
// Subscribe to events
excelApp.SheetChange += new AppEvents_SheetChangeEventHandler(OnSheetChange);

// Event handler
private void OnSheetChange(object Sh, Range Target)
{
    Console.WriteLine($"Cell {Target.Address} changed to {Target.Value2}");
}

// Unsubscribe
excelApp.SheetChange -= OnSheetChange;
```

### 11.5 Working with Ranges

```csharp
// Single cell
Range cell = worksheet.Range["A1"];

// Range of cells
Range range = worksheet.Range["A1:B10"];

// Using Cells property (1-indexed)
Range cell = worksheet.Cells[1, 1]; // A1

// Using named range
Range namedRange = worksheet.Range["MyNamedRange"];
```

### 11.6 Dynamic vs Early Binding

```csharp
// Early binding (requires reference to PIA)
Excel.Application excelApp = new Excel.Application();

// Late binding (no PIA reference needed)
dynamic excelApp = Activator.CreateInstance(Type.GetTypeFromProgID("Excel.Application"));
excelApp.Visible = true;
```

## 12. Code Examples from Official Documentation

### 12.1 C# Create Workbook and Write Data

```csharp
using Excel = Microsoft.Office.Interop.Excel;

var excelApp = new Excel.Application();
excelApp.Visible = true;

Excel.Workbook workbook = excelApp.Workbooks.Add();
Excel.Worksheet worksheet = workbook.ActiveSheet;

worksheet.Cells[1, 1] = "Name";
worksheet.Cells[1, 2] = "Value";
worksheet.Cells[2, 1] = "Test";
worksheet.Cells[2, 2] = 123;

worksheet.Cells[3, 2].Formula = "=SUM(B2:B2)*2";

workbook.SaveAs(@"C:\temp\output.xlsx");
workbook.Close();
excelApp.Quit();

Marshal.ReleaseComObject(worksheet);
Marshal.ReleaseComObject(workbook);
Marshal.ReleaseComObject(excelApp);
```

`[VERIFIED] (https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/interop/how-to-access-office-interop-objects)`

### 12.2 C# Attach to Running Excel

```csharp
using System.Runtime.InteropServices;
using Excel = Microsoft.Office.Interop.Excel;

try
{
    var excelApp = (Excel.Application)Marshal.GetActiveObject("Excel.Application");
    Console.WriteLine($"Connected to Excel with {excelApp.Workbooks.Count} workbooks");
    
    Excel.Workbook wb = excelApp.ActiveWorkbook;
    Excel.Worksheet ws = wb.ActiveSheet;
    
    ws.Range["A1"].Value = "Written by external process";
    excelApp.Calculate();
}
catch (COMException ex)
{
    Console.WriteLine("No running Excel instance found: " + ex.Message);
}
```

### 12.3 PowerShell Remote Control Excel

```powershell
# Attach to running Excel
$excel = [Runtime.InteropServices.Marshal]::GetActiveObject("Excel.Application")

# Access active workbook
$workbook = $excel.ActiveWorkbook
$worksheet = $workbook.ActiveSheet

# Read cell
$value = $worksheet.Range("A1").Value2
Write-Host "A1 contains: $value"

# Write to cell
$worksheet.Range("B1").Value2 = "Hello from PowerShell"

# Write formula
$worksheet.Range("C1").Formula = "=A1+B1"

# Trigger calculation
$excel.Calculate()
```

### 12.4 C# Export VBA Modules

```csharp
// Requires: Trust access to VBA project object model
// Requires: Reference to Microsoft.Vbe.Interop

using Excel = Microsoft.Office.Interop.Excel;
using Microsoft.Vbe.Interop;

var excelApp = (Excel.Application)Marshal.GetActiveObject("Excel.Application");
Excel.Workbook workbook = excelApp.ActiveWorkbook;

VBProject vbProject = workbook.VBProject;
string exportPath = @"C:\temp\vba_export\";
Directory.CreateDirectory(exportPath);

foreach (VBComponent component in vbProject.VBComponents)
{
    string ext = component.Type switch
    {
        vbext_ComponentType.vbext_ct_StdModule => ".bas",
        vbext_ComponentType.vbext_ct_ClassModule => ".cls",
        vbext_ComponentType.vbext_ct_MSForm => ".frm",
        vbext_ComponentType.vbext_ct_Document => ".cls",
        _ => ".txt"
    };
    
    if (component.CodeModule.CountOfLines > 0)
    {
        component.Export(Path.Combine(exportPath, component.Name + ext));
    }
}
```

### 12.5 Python COM Automation

```python
import win32com.client

# Create new Excel instance
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = True

# Or attach to running instance
excel = win32com.client.GetActiveObject("Excel.Application")

# Access workbook
workbook = excel.ActiveWorkbook
worksheet = workbook.ActiveSheet

# Read/write cells
value = worksheet.Range("A1").Value
worksheet.Range("B1").Value = "Python was here"

# Export as CSV
workbook.SaveAs(r"C:\temp\export.csv", FileFormat=6)  # 6 = xlCSV
```

## Document History

**[2026-02-27 13:10]**
- Added: Two-Dot Rule warning with bad/good pattern example
- Added: STA threading requirement note
- Added: .NET 5+ compatibility note for GetActiveObject
- Added: ROT timing issue explanation with Microsoft KB link
- Review: `_INFO_AXCEL-IN02_COM_API_REVIEW.md` findings addressed

**[2026-02-27 Session]**
- Created: Comprehensive COM/Interop API reference document
- Source: Microsoft Learn Microsoft.Office.Interop.Excel Namespace
- Coverage: All core interfaces, 300+ interfaces total, 200+ enumerations
- Added: COM-specific patterns (cleanup, event handling, binding)
- Added: Code examples from official documentation (C#, PowerShell, Python)
- Note: Object model identical to VBA - see _INFO_AXCEL-IN01_VBA_API.md for detailed member lists
