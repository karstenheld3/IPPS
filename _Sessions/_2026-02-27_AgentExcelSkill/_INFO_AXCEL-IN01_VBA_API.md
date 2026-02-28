# INFO: Excel VBA Complete API Reference

**Doc ID**: AXCEL-IN01-API
**Goal**: Comprehensive documentation of all Excel VBA exposed objects, methods, properties, and events
**Version Scope**: Excel 2016+ / Microsoft 365 (2026-02-27)
**Source**: Microsoft Learn - Office VBA Reference

**Depends on:**
- `_INFO_AXCEL-IN01_VBA.md [AXCEL-IN01]` for VBA overview and usage

## Table of Contents

1. Object Hierarchy Overview
2. Application Object
3. Workbook Object
4. Worksheet Object
5. Range Object
6. Supporting Objects
7. Collections
8. Enumerations
9. WorksheetFunction Object
10. Code Examples from Official Documentation

**Out of Scope**: This reference focuses on core Excel automation objects. The following are not covered but documented on Microsoft Learn: Power Pivot/Data Model (Model, ModelTable, ModelRelationship), Power Query (WorkbookQuery, Queries), Slicers/Timelines (Slicer, SlicerCache, TimelineState).

## 1. Object Hierarchy Overview

The Excel VBA object model follows a hierarchical structure:

```
Application
├── Workbooks (collection)
│   └── Workbook
│       ├── Worksheets (collection)
│       │   └── Worksheet
│       │       ├── Range / Cells / Rows / Columns
│       │       ├── Charts / PivotTables / ListObjects
│       │       ├── Shapes / Comments / Hyperlinks
│       ├── Charts (collection)
│       ├── Names (collection)
│       └── VBProject
├── Windows (collection)
├── AddIns (collection)
└── WorksheetFunction
```

`[VERIFIED] (https://learn.microsoft.com/en-us/office/vba/api/overview/excel/object-model)`

## 2. Application Object

Represents the entire Microsoft Excel application.

`[VERIFIED] (https://learn.microsoft.com/en-us/office/vba/api/excel.application(object))`

### 2.1 Application Events (45 events)

- AfterCalculate, NewWorkbook
- ProtectedViewWindowActivate, ProtectedViewWindowBeforeClose, ProtectedViewWindowBeforeEdit
- ProtectedViewWindowDeactivate, ProtectedViewWindowOpen, ProtectedViewWindowResize
- SheetActivate, SheetBeforeDelete, SheetBeforeDoubleClick, SheetBeforeRightClick
- SheetCalculate, SheetChange, SheetDeactivate, SheetFollowHyperlink
- SheetLensGalleryRenderComplete, SheetPivotTableAfterValueChange
- SheetPivotTableBeforeAllocateChanges, SheetPivotTableBeforeCommitChanges
- SheetPivotTableBeforeDiscardChanges, SheetPivotTableUpdate
- SheetSelectionChange, SheetTableUpdate
- WindowActivate, WindowDeactivate, WindowResize
- WorkbookActivate, WorkbookAddinInstall, WorkbookAddinUninstall
- WorkbookAfterSave, WorkbookAfterXmlExport, WorkbookAfterXmlImport
- WorkbookBeforeClose, WorkbookBeforePrint, WorkbookBeforeSave
- WorkbookBeforeXmlExport, WorkbookBeforeXmlImport
- WorkbookDeactivate, WorkbookModelChange, WorkbookNewChart
- WorkbookNewSheet, WorkbookOpen, WorkbookPivotTableCloseConnection
- WorkbookPivotTableOpenConnection, WorkbookRowsetComplete, WorkbookSync

### 2.2 Application Methods (48 methods)

- ActivateMicrosoftApp, AddCustomList, Calculate, CalculateFull
- CalculateFullRebuild, CalculateUntilAsyncQueriesDone
- CentimetersToPoints, CheckAbort, CheckSpelling, ConvertFormula
- DDEExecute, DDEInitiate, DDEPoke, DDERequest, DDETerminate
- DeleteCustomList, DisplayXMLSourcePane, DoubleClick, Evaluate
- ExecuteExcel4Macro, FindFile, GetCustomListContents, GetCustomListNum
- GetOpenFilename, GetPhonetic, GetSaveAsFilename, Goto, Help
- InchesToPoints, InputBox, Intersect, MacroOptions
- MailLogoff, MailLogon, NextLetter, OnKey, OnRepeat, OnTime, OnUndo
- Quit, RecordMacro, RegisterXLL, Repeat, Run, SendKeys
- SharePointVersion, Undo, Union, Volatile, Wait

### 2.3 Application Properties (150+ properties)

**Active Elements:**
- ActiveCell, ActiveChart, ActiveEncryptionSession, ActivePrinter
- ActiveProtectedViewWindow, ActiveSheet, ActiveWindow, ActiveWorkbook

**Collections:**
- AddIns, AddIns2, Charts, Columns, CommandBars, COMAddIns, Dialogs
- Names, ProtectedViewWindows, RecentFiles, Rows, Sheets, Windows, Workbooks, Worksheets

**Calculation:**
- Calculation, CalculateBeforeSave, CalculationInterruptKey
- CalculationState, CalculationVersion, Iteration, MaxChange, MaxIterations

**Display:**
- DisplayAlerts, DisplayClipboardWindow, DisplayCommentIndicator
- DisplayFormulaAutoComplete, DisplayFormulaBar, DisplayFullScreen
- DisplayNoteIndicator, DisplayPasteOptions, DisplayScrollBars
- DisplayStatusBar, ScreenUpdating, Visible

**Enable:**
- EnableAnimations, EnableAutoComplete, EnableCancelKey, EnableEvents
- EnableLargeOperationAlert, EnableLivePreview, EnableMacroAnimations, EnableSound

**Other Key Properties:**
- Application, Build, Caller, Caption, Cells, CutCopyMode
- DataEntryMode, DecimalSeparator, DefaultFilePath, DefaultSaveFormat
- EditDirectlyInCell, FixedDecimal, Interactive, MoveAfterReturn
- Name, OperatingSystem, Path, Range, ReferenceStyle, Selection
- StandardFont, StandardFontSize, StatusBar, ThisCell, ThisWorkbook
- ThousandsSeparator, UserName, VBE, Version, WorksheetFunction

## 3. Workbook Object

Represents a Microsoft Excel workbook.

`[VERIFIED] (https://learn.microsoft.com/en-us/office/vba/api/excel.workbook)`

### 3.1 Workbook Events (40+ events)

- Activate, AddinInstall, AddinUninstall, AfterRemoteChange, AfterSave
- AfterXmlExport, AfterXmlImport, BeforeClose, BeforePrint
- BeforeRemoteChange, BeforeSave, BeforeXmlExport, BeforeXmlImport
- Deactivate, ModelChange, NewChart, NewSheet, Open
- PivotTableCloseConnection, PivotTableOpenConnection, RowsetComplete
- SheetActivate, SheetBeforeDelete, SheetBeforeDoubleClick
- SheetBeforeRightClick, SheetCalculate, SheetChange, SheetDeactivate
- SheetFollowHyperlink, SheetPivotTableUpdate, SheetSelectionChange
- SheetTableUpdate, Sync, WindowActivate, WindowDeactivate, WindowResize

### 3.2 Workbook Methods (60+ methods)

- AcceptAllChanges, Activate, AddToFavorites, ApplyTheme, BreakLink
- CanCheckIn, ChangeFileAccess, ChangeLink, CheckIn, CheckInWithVersion
- Close, ConvertComments, CreateForecastSheet, DeleteNumberFormat
- EnableConnections, EndReview, ExclusiveAccess, ExportAsFixedFormat
- FollowHyperlink, GetWorkflowTasks, GetWorkflowTemplates
- HighlightChangesOptions, LinkInfo, LinkSources, LockServerFile
- MergeWorkbook, NewWindow, OpenLinks, PivotCaches, Post, PrintOut
- PrintPreview, Protect, ProtectSharing, PublishToDocs
- PurgeChangeHistoryNow, RefreshAll, RejectAllChanges, ReloadAs
- RemoveDocumentInformation, RemoveUser, Reply, ReplyAll
- ReplyWithChanges, ResetColors, RunAutoMacros, Save, SaveAs
- SaveCopyAs, SendForReview, SendMail, SetLinkOnData
- SetPasswordEncryptionOptions, ToggleFormsDesign, Unprotect
- UnprotectSharing, UpdateFromFile, UpdateLink, WebPagePreview
- XmlImport, XmlImportXml

### 3.3 Workbook Properties (100+ properties)

- AccuracyVersion, ActiveChart, ActiveSheet, ActiveSlicer, Application
- AutoSaveOn, AutoUpdateFrequency, BuiltinDocumentProperties
- CalculationVersion, CaseSensitive, ChangeHistoryDuration
- ChartDataPointTrack, Charts, CheckCompatibility, CodeName, Colors
- CommandBars, ConflictResolution, Connections, ConnectionsDisabled
- Container, ContentTypeProperties, CreateBackup, Creator
- CustomDocumentProperties, CustomViews, CustomXMLParts, Date1904
- DefaultPivotTableStyle, DefaultSlicerStyle, DefaultTableStyle
- DisplayDrawingObjects, EnableAutoRecover, EncryptionProvider
- Excel4IntlMacroSheets, Excel4MacroSheets, Excel8CompatibilityMode
- FileFormat, Final, ForceFullCalculation, FullName, FullNameURLEncoded
- HasPassword, HasVBProject, HighlightChangesOnScreen, IconSets
- InactiveListBorderVisible, IsAddin, IsInplace, KeepChangeHistory
- ListChangesOnNewSheet, Model, MultiUserEditing, Name, Names, Parent
- Password, Path, Permission, PersonalViewListSettings, PivotTables
- PrecisionAsDisplayed, ProtectStructure, ProtectWindows, PublishObjects
- Queries, ReadOnly, ReadOnlyRecommended, Research, RevisionNumber
- Saved, SaveLinkValues, Sheets, ShowConflictHistory
- ShowPivotTableFieldList, Signatures, SlicerCaches, SmartDocument
- Styles, TableStyles, Theme, UpdateLinks, UserStatus, VBASigned
- VBProject, WebOptions, Windows, Worksheets, WritePassword
- WriteReserved, WriteReservedBy, XmlMaps, XmlNamespaces

## 4. Worksheet Object

Represents a worksheet.

`[VERIFIED] (https://learn.microsoft.com/en-us/office/vba/api/excel.worksheet)`

### 4.1 Worksheet Events (17 events)

- Activate, BeforeDelete, BeforeDoubleClick, BeforeRightClick
- Calculate, Change, Deactivate, FollowHyperlink
- LensGalleryRenderComplete, PivotTableAfterValueChange
- PivotTableBeforeAllocateChanges, PivotTableBeforeCommitChanges
- PivotTableBeforeDiscardChanges, PivotTableChangeSync
- PivotTableUpdate, SelectionChange, TableUpdate

### 4.2 Worksheet Methods (29 methods)

- Activate, Calculate, ChartObjects, CheckSpelling, CircleInvalid
- ClearArrows, ClearCircles, Copy, Delete, Evaluate, ExportAsFixedFormat
- Move, OLEObjects, Paste, PasteSpecial, PivotTables, PivotTableWizard
- PrintOut, PrintPreview, Protect, ResetAllPageBreaks, SaveAs, Scenarios
- Select, SetBackgroundPicture, ShowAllData, ShowDataForm, Unprotect
- XmlDataQuery, XmlMapQuery

### 4.3 Worksheet Properties (60+ properties)

- Application, AutoFilter, AutoFilterMode, Cells, CircularReference
- CodeName, Columns, Comments, CommentsThreaded, ConsolidationFunction
- ConsolidationOptions, ConsolidationSources, Creator, CustomProperties
- DisplayPageBreaks, DisplayRightToLeft, EnableAutoFilter
- EnableCalculation, EnableFormatConditionsCalculation, EnableOutlining
- EnablePivotTable, EnableSelection, FilterMode, HPageBreaks
- Hyperlinks, Index, ListObjects, MailEnvelope, Name, Names, Next
- Outline, PageSetup, Parent, Previous, PrintedCommentPages
- ProtectContents, ProtectDrawingObjects, Protection, ProtectionMode
- ProtectScenarios, QueryTables, Range, Rows, ScrollArea, Shapes
- Sort, SpellingOptions, StandardHeight, StandardWidth, Tab
- TransitionExpEval, TransitionFormEntry, Type, UsedRange, Visible
- VPageBreaks

## 5. Range Object

The most important object in Excel VBA. Represents a cell, row, column, or selection of cells.

`[VERIFIED] (https://learn.microsoft.com/en-us/office/vba/api/excel.range(object))`

### 5.1 Range Methods (75+ methods)

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

### 5.2 Range Properties (90+ properties)

**Values:** Value, Value2, Text, Formula, FormulaArray, FormulaLocal, FormulaR1C1, FormulaR1C1Local, FormulaHidden, HasFormula, HasArray, HasRichDataType

**References:** Address, AddressLocal, Item, Offset, Range, Resize, Cells, Rows, Columns, Row, Column, EntireRow, EntireColumn, Areas, End, Next, Previous, CurrentArray, CurrentRegion

**Dependencies:** Dependents, DirectDependents, Precedents, DirectPrecedents

**Formatting:** Font, Interior, Borders, Style, DisplayFormat, FormatConditions, NumberFormat, NumberFormatLocal, HorizontalAlignment, VerticalAlignment, Orientation, IndentLevel, ShrinkToFit, WrapText, AddIndent, ReadingOrder, Locked, Hidden

**Size:** Width, Height, ColumnWidth, RowHeight, Left, Top, UseStandardHeight, UseStandardWidth

**Count:** Count, CountLarge

**Merge:** MergeCells, MergeArea

**Dynamic Arrays (Excel 365):** HasSpill, SpillingToRange, SpillParent

**Other:** AllowEdit, Characters, Comment, CommentThreaded, Creator, Errors, Hyperlinks, ID, LinkedDataTypeState, ListHeaderRows, ListObject, LocationInTable, MDX, Name, PageBreak, Parent, Phonetic, Phonetics, PivotCell, PivotField, PivotItem, PivotTable, PrefixCharacter, QueryTable, ServerActions, ShowDetail, SoundNote, SparklineGroups, Summary, Validation, Worksheet, XPath

## 6. Supporting Objects

### 6.1 Chart Object

Represents a chart in a workbook.

**Methods:** Activate, ApplyChartTemplate, ApplyDataLabels, ApplyLayout, Axes, ChartWizard, ClearToMatchStyle, Copy, CopyPicture, Delete, Export, ExportAsFixedFormat, FullSeriesCollection, GetChartElement, Location, Move, Paste, PrintOut, PrintPreview, Protect, Refresh, SaveAs, SaveChartTemplate, Select, SeriesCollection, SetBackgroundPicture, SetDefaultChart, SetElement, SetSourceData, Unprotect

**Properties:** Application, AutoScaling, BackWall, BarShape, CategoryLabelLevel, ChartArea, ChartColor, ChartStyle, ChartTitle, ChartType, CodeName, Creator, DataTable, DepthPercent, DisplayBlanksAs, Elevation, Floor, GapDepth, HasAxis, HasDataTable, HasLegend, HasTitle, HeightPercent, Hyperlinks, Index, Legend, Name, PageSetup, Parent, Perspective, PivotLayout, PlotArea, PlotBy, PlotVisibleOnly, PrintedCommentPages, ProtectContents, ProtectData, ProtectDrawingObjects, ProtectFormatting, ProtectGoalSeek, ProtectionMode, ProtectSelection, RightAngleAxes, Rotation, SeriesNameLevel, Shapes, ShowAllFieldButtons, ShowAxisFieldButtons, ShowDataLabelsOverMaximum, ShowLegendFieldButtons, ShowReportFilterFieldButtons, ShowValueFieldButtons, SideWall, Tab, Visible, Walls

### 6.2 PivotTable Object

Represents a PivotTable report on a worksheet.

**Methods:** AddDataField, AddFields, AllocateChanges, CalculatedFields, ChangeConnection, ChangePivotCache, ClearAllFilters, ClearTable, CommitChanges, ConvertToFormulas, CreateCubeFile, DiscardChanges, DrillDown, DrillTo, DrillUp, GetData, GetPivotData, ListFormulas, PivotCache, PivotFields, PivotSelect, PivotTableWizard, PrintPreview, PrintOut, RefreshDataSourceValues, RefreshTable, RepeatAllLabels, RowAxisLayout, ShowPages, SubtotalLocation, Update

**Properties:** ActiveFilters, Allocation, AllocationMethod, AllocationValue, AllocationWeightExpression, AllowMultipleFilters, AlternativeText, CacheIndex, CalculatedMembers, ChangeList, ColumnFields, ColumnGrand, ColumnRange, CompactLayoutColumnHeader, CompactLayoutRowHeader, CompactRowIndent, Creator, CubeFields, DataBodyRange, DataFields, DataLabelRange, DataPivotField, DisplayContextTooltips, DisplayEmptyColumn, DisplayEmptyRow, DisplayErrorString, DisplayFieldCaptions, DisplayImmediateItems, DisplayMemberPropertyTooltips, DisplayNullString, EnableDataValueEditing, EnableDrilldown, EnableFieldDialog, EnableFieldList, EnableWizard, EnableWriteback, ErrorString, FieldListSortAscending, GrandTotalName, HasAutoFormat, Hidden, HiddenFields, InGridDropZones, InnerDetail, LayoutRowDefault, Location, ManualUpdate, MDX, MergeLabels, Name, NullString, PageFieldOrder, PageFields, PageFieldStyle, PageFieldWrapCount, PageRange, PageRangeCells, Parent, PivotCache, PivotColumnAxis, PivotFormulas, PivotRowAxis, PivotSelection, PreserveFormatting, PrintDrillIndicators, PrintTitles, RefreshDate, RefreshName, RepeatItemsOnEachPrintedPage, RowFields, RowGrand, RowRange, SaveData, SelectionMode, ShowDrillIndicators, ShowTableStyleColumnHeaders, ShowTableStyleRowStripes, ShowValuesRow, Slicers, SmallGrid, SortUsingCustomLists, SourceData, SubtotalHiddenPageItems, Summary, TableRange1, TableRange2, TableStyle2, Tag, TotalsAnnotation, Value, Version, ViewCalculatedMembers, VisibleFields, VisualTotals

### 6.3 ListObject Object (Table)

Represents a list object (table) on a worksheet.

**Methods:** Delete, ExportToVisio, Publish, Refresh, Resize, Unlink, Unlist

**Properties:** Active, AlternativeText, AutoFilter, Comment, Creator, DataBodyRange, DisplayName, DisplayRightToLeft, HeaderRowRange, InsertRowRange, ListColumns, ListRows, Name, Parent, QueryTable, Range, SharePointURL, ShowAutoFilter, ShowAutoFilterDropDown, ShowHeaders, ShowTableStyleColumnStripes, ShowTableStyleFirstColumn, ShowTableStyleLastColumn, ShowTableStyleRowStripes, ShowTotals, Slicers, Sort, SourceType, Summary, TableStyle, TotalsRowRange, XmlMap

### 6.4 Name Object

Represents a defined name for a range of cells.

**Methods:** Delete

**Properties:** Application, Category, CategoryLocal, Comment, Creator, Index, MacroType, Name, NameLocal, Parent, RefersTo, RefersToLocal, RefersToR1C1, RefersToR1C1Local, RefersToRange, ShortcutKey, ValidWorkbookParameter, Value, Visible, WorkbookParameter

### 6.5 Comment Object

Represents a cell comment.

**Methods:** Delete, Next, Previous, Text

**Properties:** Application, Author, Creator, Parent, Shape, Visible

### 6.6 CommentThreaded Object

Represents a modern threaded comment.

**Methods:** AddReply, Delete, Next, Previous, Text

**Properties:** Application, Author, Creator, Date, Parent, Replies, Resolved, Text

### 6.7 Hyperlink Object

Represents a hyperlink.

**Methods:** AddToFavorites, CreateNewDocument, Delete, Follow

**Properties:** Address, Application, Creator, EmailSubject, Name, Parent, Range, ScreenTip, Shape, SubAddress, TextToDisplay, Type

### 6.8 Shape Object

Represents an object in the drawing layer.

**Methods:** Apply, Copy, CopyPicture, Cut, Delete, Duplicate, Flip, IncrementLeft, IncrementRotation, IncrementTop, PickUp, RerouteConnections, ScaleHeight, ScaleWidth, Select, SetShapesDefaultProperties, Ungroup, ZOrder

**Properties:** Adjustments, AlternativeText, Application, AutoShapeType, BackgroundStyle, BlackWhiteMode, BottomRightCell, Callout, Chart, Child, ConnectionSiteCount, Connector, ConnectorFormat, ControlFormat, Creator, Decorative, Fill, FormControlType, Glow, GraphicStyle, GroupItems, HasChart, HasSmartArt, Height, HorizontalFlip, Hyperlink, ID, Left, Line, LinkFormat, LockAspectRatio, Locked, Model3D, Name, Nodes, OLEFormat, OnAction, Parent, ParentGroup, PictureFormat, Placement, Reflection, Rotation, Shadow, ShapeStyle, SmartArt, SoftEdge, TextEffect, TextFrame, TextFrame2, ThreeD, Title, Top, TopLeftCell, Type, VerticalFlip, Vertices, Visible, Width, ZOrderPosition

### 6.9 Font Object

Represents the font attributes of an object.

**Properties:** Application, Background, Bold, Color, ColorIndex, Creator, FontStyle, Italic, Name, OutlineFont, Parent, Shadow, Size, Strikethrough, Subscript, Superscript, ThemeColor, ThemeFont, TintAndShade, Underline

### 6.10 Interior Object

Represents the interior of an object.

**Properties:** Application, Color, ColorIndex, Creator, Gradient, InvertIfNegative, Parent, Pattern, PatternColor, PatternColorIndex, PatternThemeColor, PatternTintAndShade, ThemeColor, TintAndShade

### 6.11 Border/Borders Object

Represents the border of an object.

**Properties (Border):** Application, Color, ColorIndex, Creator, LineStyle, Parent, ThemeColor, TintAndShade, Weight

**Properties (Borders):** Application, Color, ColorIndex, Count, Creator, Item, LineStyle, Parent, ThemeColor, TintAndShade, Value, Weight

### 6.12 Validation Object

Represents data validation for a worksheet range.

**Methods:** Add, Delete, Modify

**Properties:** AlertStyle, Application, Creator, ErrorMessage, ErrorTitle, Formula1, Formula2, IgnoreBlank, IMEMode, InCellDropdown, InputMessage, InputTitle, Operator, Parent, ShowError, ShowInput, Type, Value

### 6.13 FormatCondition Object

Represents a conditional format.

**Methods:** Delete, Modify, ModifyAppliesToRange, SetFirstPriority, SetLastPriority

**Properties:** Application, AppliesTo, Borders, Creator, DateOperator, Font, Formula1, Formula2, Interior, NumberFormat, Operator, Parent, Priority, PTCondition, ScopeType, StopIfTrue, Text, TextOperator, Type

### 6.14 PageSetup Object

Represents page setup description.

**Properties:** AlignMarginsHeaderFooter, Application, BlackAndWhite, BottomMargin, CenterFooter, CenterFooterPicture, CenterHeader, CenterHeaderPicture, CenterHorizontally, CenterVertically, Creator, DifferentFirstPageHeaderFooter, Draft, EvenPage, FirstPage, FirstPageNumber, FitToPagesTall, FitToPagesWide, FooterMargin, HeaderMargin, LeftFooter, LeftFooterPicture, LeftHeader, LeftHeaderPicture, LeftMargin, OddAndEvenPagesHeaderFooter, Order, Orientation, Pages, PaperSize, Parent, PrintArea, PrintComments, PrintErrors, PrintGridlines, PrintHeadings, PrintNotes, PrintQuality, PrintTitleColumns, PrintTitleRows, RightFooter, RightFooterPicture, RightHeader, RightHeaderPicture, RightMargin, ScaleWithDocHeaderFooter, TopMargin, Zoom

### 6.15 VBProject Object

Represents a Visual Basic project.

**Methods:** SaveAs

**Properties:** BuildFileName, Creator, Description, FileName, HelpContextID, HelpFile, Mode, Name, Protection, References, Type, VBComponents, VBE

### 6.16 VBComponent Object

Represents a VBA module, class, or form.

**Methods:** Activate, DesignerWindow, Export

**Properties:** CodeModule, Collection, Designer, DesignerID, HasOpenDesigner, Name, Properties, Type

### 6.17 AutoFilter Object

Represents autofiltering for a worksheet.

**Methods:** ApplyFilter, ShowAllData

**Properties:** Application, Creator, FilterMode, Filters, Parent, Range, Sort

**Related:** Filter object (individual column filter criteria), Filters collection

## 7. Collections

### 7.1 Core Collections

- **Workbooks** - All open Workbook objects
- **Worksheets** - All Worksheet objects in a workbook
- **Sheets** - All sheets (worksheets, chart sheets, macro sheets)
- **Charts** - All Chart objects in a workbook
- **Windows** - All Window objects
- **Names** - All Name objects in a workbook/worksheet

### 7.2 Range-Related Collections

- **Areas** - A collection of ranges within a selection
- **Cells** - All cells on a worksheet
- **Rows** - All rows on a worksheet
- **Columns** - All columns on a worksheet

### 7.3 Data Collections

- **PivotTables** - All PivotTable objects on a worksheet
- **PivotCaches** - All PivotCache objects in a workbook
- **PivotFields** - All PivotField objects in a PivotTable
- **PivotItems** - All PivotItem objects in a PivotField
- **ListObjects** - All ListObject (table) objects on a worksheet
- **ListColumns** - Columns in a ListObject
- **ListRows** - Rows in a ListObject
- **QueryTables** - All QueryTable objects on a worksheet

### 7.4 Formatting Collections

- **Styles** - All Style objects in a workbook
- **Borders** - All borders of a Range
- **FormatConditions** - All FormatCondition objects for a range
- **ColorScales** - ColorScale objects for conditional formatting
- **DataBars** - DataBar objects for conditional formatting
- **IconSets** - IconSet objects for conditional formatting
- **TableStyles** - All TableStyle objects in a workbook

### 7.5 Shape Collections

- **Shapes** - All Shape objects on a worksheet/chart
- **GroupShapes** - Shapes within a grouped shape
- **ShapeNodes** - Nodes in a freeform shape
- **Connectors** - Connector shapes

### 7.6 Comment Collections

- **Comments** - All Comment objects on a worksheet
- **CommentsThreaded** - All threaded comments on a worksheet

### 7.7 Other Collections

- **Hyperlinks** - All Hyperlink objects in a range/worksheet
- **AddIns** - All AddIn objects
- **CommandBars** - All CommandBar objects
- **RecentFiles** - Recently used files
- **CustomViews** - Custom views in a workbook
- **Scenarios** - What-if scenarios on a worksheet
- **HPageBreaks** - Horizontal page breaks
- **VPageBreaks** - Vertical page breaks
- **SlicerCaches** - Slicer caches in a workbook
- **Slicers** - Slicers in a slicer cache
- **SparklineGroups** - Sparkline groups on a worksheet
- **Connections** - Data connections in a workbook
- **XmlMaps** - XML maps in a workbook

## 8. Enumerations

Excel VBA includes 200+ enumerations. Key enumerations organized by category:

### 8.1 Calculation Enumerations

- **XlCalculation** - xlCalculationAutomatic, xlCalculationManual, xlCalculationSemiautomatic
- **XlCalculationState** - xlCalculating, xlDone, xlPending
- **XlCalculationInterruptKey** - xlAnyKey, xlEscKey, xlNoKey

### 8.2 Cell Type Enumerations

- **XlCellType** - xlCellTypeAllFormatConditions, xlCellTypeAllValidation, xlCellTypeBlanks, xlCellTypeComments, xlCellTypeConstants, xlCellTypeFormulas, xlCellTypeLastCell, xlCellTypeSameFormatConditions, xlCellTypeSameValidation, xlCellTypeVisible

### 8.3 Direction Enumerations

- **XlDirection** - xlDown, xlToLeft, xlToRight, xlUp
- **XlDeleteShiftDirection** - xlShiftToLeft, xlShiftUp
- **XlInsertShiftDirection** - xlShiftDown, xlShiftToRight

### 8.4 File Format Enumerations

- **XlFileFormat** - xlCSV, xlCSVUTF8, xlExcel8, xlOpenXMLWorkbook, xlOpenXMLWorkbookMacroEnabled, xlWorkbookDefault, xlXMLSpreadsheet (50+ values)

### 8.5 Alignment Enumerations

- **XlHAlign** - xlHAlignCenter, xlHAlignCenterAcrossSelection, xlHAlignDistributed, xlHAlignFill, xlHAlignGeneral, xlHAlignJustify, xlHAlignLeft, xlHAlignRight
- **XlVAlign** - xlVAlignBottom, xlVAlignCenter, xlVAlignDistributed, xlVAlignJustify, xlVAlignTop

### 8.6 Border Enumerations

- **XlBordersIndex** - xlDiagonalDown, xlDiagonalUp, xlEdgeBottom, xlEdgeLeft, xlEdgeRight, xlEdgeTop, xlInsideHorizontal, xlInsideVertical
- **XlBorderWeight** - xlHairline, xlMedium, xlThick, xlThin
- **XlLineStyle** - xlContinuous, xlDash, xlDashDot, xlDashDotDot, xlDot, xlDouble, xlLineStyleNone, xlSlantDashDot

### 8.7 Color Enumerations

- **XlColorIndex** - xlColorIndexAutomatic, xlColorIndexNone, plus numeric values 1-56
- **XlThemeColor** - xlThemeColorAccent1-6, xlThemeColorDark1-2, xlThemeColorFollowedHyperlink, xlThemeColorHyperlink, xlThemeColorLight1-2

### 8.8 Chart Enumerations

- **XlChartType** - xlArea, xlAreaStacked, xlBarClustered, xlBarStacked, xlColumnClustered, xlColumnStacked, xlLine, xlLineMarkers, xlPie, xlPieExploded, xlXYScatter (70+ chart types)
- **XlChartLocation** - xlLocationAsNewSheet, xlLocationAsObject, xlLocationAutomatic
- **XlAxisType** - xlCategory, xlSeriesAxis, xlValue
- **XlAxisGroup** - xlPrimary, xlSecondary

### 8.9 PivotTable Enumerations

- **XlPivotFieldCalculation** - xlDifferenceFrom, xlIndex, xlPercentDifferenceFrom, xlPercentOf, xlPercentOfColumn, xlPercentOfParent, xlPercentOfRow, xlPercentOfTotal, xlRunningTotal
- **XlPivotFieldOrientation** - xlColumnField, xlDataField, xlHidden, xlPageField, xlRowField
- **XlConsolidationFunction** - xlAverage, xlCount, xlCountNums, xlMax, xlMin, xlProduct, xlStDev, xlStDevP, xlSum, xlVar, xlVarP

### 8.10 Protection Enumerations

- **XlSheetVisibility** - xlSheetHidden, xlSheetVeryHidden, xlSheetVisible
- **XlEnableSelection** - xlNoRestrictions, xlNoSelection, xlUnlockedCells

### 8.11 Find/Replace Enumerations

- **XlLookAt** - xlPart, xlWhole
- **XlSearchOrder** - xlByColumns, xlByRows
- **XlSearchDirection** - xlNext, xlPrevious
- **XlFindLookIn** - xlComments, xlCommentsThreaded, xlFormulas, xlValues

### 8.12 Sort Enumerations

- **XlSortOrder** - xlAscending, xlDescending
- **XlSortOn** - xlSortOnCellColor, xlSortOnFontColor, xlSortOnIcon, xlSortOnValues
- **XlSortOrientation** - xlSortColumns, xlSortRows
- **XlSortDataOption** - xlSortNormal, xlSortTextAsNumbers

### 8.13 AutoFill Enumerations

- **XlAutoFillType** - xlFillCopy, xlFillDays, xlFillDefault, xlFillFormats, xlFillMonths, xlFillSeries, xlFillValues, xlFillWeekdays, xlFillYears, xlGrowthTrend, xlLinearTrend

### 8.14 Validation Enumerations

- **XlDVType** - xlValidateCustom, xlValidateDate, xlValidateDecimal, xlValidateInputOnly, xlValidateList, xlValidateTextLength, xlValidateTime, xlValidateWholeNumber
- **XlDVAlertStyle** - xlValidAlertInformation, xlValidAlertStop, xlValidAlertWarning
- **XlFormatConditionOperator** - xlBetween, xlEqual, xlGreater, xlGreaterEqual, xlLess, xlLessEqual, xlNotBetween, xlNotEqual

### 8.15 Page Setup Enumerations

- **XlPageOrientation** - xlLandscape, xlPortrait
- **XlPaperSize** - xlPaperA3, xlPaperA4, xlPaperA5, xlPaperLegal, xlPaperLetter (40+ paper sizes)
- **XlOrder** - xlDownThenOver, xlOverThenDown
- **XlPrintLocation** - xlPrintInPlace, xlPrintNoComments, xlPrintSheetEnd

### 8.16 Error Value Enumerations

- **XlCVError** - xlErrBlocked, xlErrCalc, xlErrConnect, xlErrDiv0, xlErrField, xlErrGettingData, xlErrNA, xlErrName, xlErrNull, xlErrNum, xlErrRef, xlErrSpill, xlErrUnknown, xlErrValue

## 9. WorksheetFunction Object

Provides access to Excel worksheet functions from VBA.

`[VERIFIED] (https://learn.microsoft.com/en-us/office/vba/api/excel.worksheetfunction)`

### 9.1 Math and Trigonometry Functions

Abs, Acos, Acosh, Aggregate, Arabic, Asin, Asinh, Atan, Atan2, Atanh, Base, Ceiling, Ceiling_Math, Ceiling_Precise, Combin, Combina, Cos, Cosh, Cot, Coth, Csc, Csch, Decimal, Degrees, Even, Exp, Fact, FactDouble, Floor, Floor_Math, Floor_Precise, Gcd, Int, Iso_Ceiling, Lcm, Ln, Log, Log10, MDeterm, MInverse, MMult, Mod, MRound, Multinomial, MUnit, Odd, Pi, Power, Product, Quotient, Radians, Rand, RandBetween, Roman, Round, RoundDown, RoundUp, Sec, Sech, SeriesSum, Sign, Sin, Sinh, Sqrt, SqrtPi, Subtotal, Sum, SumIf, SumIfs, SumProduct, SumSq, SumX2MY2, SumX2PY2, SumXMY2, Tan, Tanh, Trunc

### 9.2 Statistical Functions

Average, AverageA, AverageIf, AverageIfs, BetaDist, Beta_Dist, BetaInv, Beta_Inv, BinomDist, Binom_Dist, Binom_Dist_Range, Binom_Inv, ChiDist, ChiInv, ChiSq_Dist, ChiSq_Dist_RT, ChiSq_Inv, ChiSq_Inv_RT, ChiSq_Test, ChiTest, Confidence, Confidence_Norm, Confidence_T, Correl, Count, CountA, CountBlank, CountIf, CountIfs, Covar, Covariance_P, Covariance_S, CritBinom, DevSq, ExponDist, Expon_Dist, FDist, F_Dist, F_Dist_RT, FInv, F_Inv, F_Inv_RT, Fisher, FisherInv, Forecast, Forecast_ETS, Forecast_ETS_ConfInt, Forecast_ETS_Seasonality, Forecast_ETS_STAT, Forecast_Linear, Frequency, FTest, F_Test, Gamma, GammaDist, Gamma_Dist, GammaInv, Gamma_Inv, GammaLn, GammaLn_Precise, Gauss, GeoMean, Growth, HarMean, HypGeomDist, HypGeom_Dist, Intercept, Kurt, Large, LinEst, LogEst, LogInv, LogNorm_Dist, LogNorm_Inv, LogNormDist, Max, MaxA, MaxIfs, Median, Min, MinA, MinIfs, Mode, Mode_Mult, Mode_Sngl, NegBinomDist, NegBinom_Dist, NormDist, Norm_Dist, NormInv, Norm_Inv, NormSDist, Norm_S_Dist, NormSInv, Norm_S_Inv, Pearson, Percentile, Percentile_Exc, Percentile_Inc, PercentRank, PercentRank_Exc, PercentRank_Inc, Permut, Permutationa, Phi, Poisson, Poisson_Dist, Prob, Quartile, Quartile_Exc, Quartile_Inc, Rank, Rank_Avg, Rank_Eq, RSq, Skew, Skew_p, Slope, Small, Standardize, StDev, StDev_P, StDev_S, StDevA, StDevP, StDevPA, StEyx, TDist, T_Dist, T_Dist_2T, T_Dist_RT, TInv, T_Inv, T_Inv_2T, Trend, TrimMean, TTest, T_Test, Var, Var_P, Var_S, VarA, VarP, VarPA, Weibull, Weibull_Dist, ZTest, Z_Test

### 9.3 Lookup and Reference Functions

Address, Areas, Choose, Column, Columns, GetPivotData, HLookup, Hyperlink, Index, Indirect, Lookup, Match, Offset, Row, Rows, RTD, Transpose, VLookup, XLookup, XMatch

### 9.4 Text Functions

Asc, Bahttext, Char, Clean, Code, Concat, Dollar, Exact, Find, FindB, Fixed, Left, LeftB, Len, LenB, Lower, Mid, MidB, NumberValue, Phonetic, Proper, Replace, ReplaceB, Rept, Right, RightB, Search, SearchB, Substitute, T, Text, TextJoin, Trim, Unichar, Unicode, Upper, Value

### 9.5 Date and Time Functions

Date, DateDiff, DateSerial, DateValue, Day, Days, Days360, EDate, EOMonth, Hour, IsoWeekNum, Minute, Month, NetworkDays, NetworkDays_Intl, Now, Second, Time, TimeSerial, TimeValue, Today, Weekday, WeekNum, WorkDay, WorkDay_Intl, Year, YearFrac

### 9.6 Logical Functions

And, False, If, IfError, IfNa, Ifs, Not, Or, Switch, True, Xor

### 9.7 Information Functions

Cell, Error_Type, IsErr, IsError, IsEven, IsFormula, IsLogical, IsNA, IsNonText, IsNumber, IsOdd, IsRef, IsText, N, NA, Sheet, Sheets, Type

### 9.8 Financial Functions

Accrint, AccrintM, AmorDegrc, AmorLinc, Coupdaybs, Coupdays, Coupdaysnc, Coupncd, Coupnum, Couppcd, CumIPmt, CumPrinc, Db, Ddb, Disc, DollarDe, DollarFr, Duration, Effect, Fv, FvSchedule, IntRate, Ipmt, Irr, IsPmt, MDuration, Mirr, Nominal, Nper, Npv, OddFPrice, OddFYield, OddLPrice, OddLYield, PDuration, Pmt, Ppmt, Price, PriceDisc, PriceMat, Pv, Rate, Received, Rri, Sln, Syd, TBillEq, TBillPrice, TBillYield, Vdb, Xirr, Xnpv, Yield, YieldDisc, YieldMat

### 9.9 Engineering Functions

Besseli, Besselj, Besselk, Bessely, Bin2Dec, Bin2Hex, Bin2Oct, Bitand, Bitlshift, Bitor, Bitrshift, Bitxor, Complex, Convert, Dec2Bin, Dec2Hex, Dec2Oct, Delta, Erf, Erf_Precise, Erfc, Erfc_Precise, Gestep, Hex2Bin, Hex2Dec, Hex2Oct, ImAbs, Imaginary, ImArgument, ImConjugate, ImCos, ImCosh, ImCot, ImCsc, ImCsch, ImDiv, ImExp, ImLn, ImLog10, ImLog2, ImPower, ImProduct, ImReal, ImSec, ImSech, ImSin, ImSinh, ImSqrt, ImSub, ImSum, ImTan, Oct2Bin, Oct2Dec, Oct2Hex

### 9.10 Database Functions

DAverage, DCount, DCountA, DGet, DMax, DMin, DProduct, DStDev, DStDevP, DSum, DVar, DVarP

### 9.11 Cube Functions

CubeKPIMember, CubeMember, CubeMemberProperty, CubeRankedMember, CubeSet, CubeSetCount, CubeValue

## 10. Code Examples from Official Documentation

### 10.1 Application Object Examples

**Activating a Window:**
```vba
Application.Windows("book1.xls").Activate
```

**Creating Excel Application:**
```vba
Set xl = CreateObject("Excel.Sheet")
xl.Application.Workbooks.Open "newbook.xls"
```

**Setting Active Cell Font:**
```vba
ActiveCell.Font.Bold = True
```

### 10.2 Workbook Object Examples

**Activating First Workbook:**
```vba
Workbooks(1).Activate
```

**Setting Workbook Author:**
```vba
ActiveWorkbook.Author = "Jean Selva"
```

**Sending Worksheet via Email:**
```vba
Sub SendTab()
    Dim wks As Worksheet
    Application.ScreenUpdating = False
    Set wks = ActiveSheet
    Worksheets(Range("C1").Value).Copy
    ActiveWorkbook.SendMail wks.Range("A1").Value, wks.Range("B1").Value
    ActiveWorkbook.Close savechanges:=False
    Application.ScreenUpdating = True
End Sub
```

### 10.3 Worksheet Object Examples

**Hiding a Worksheet:**
```vba
Worksheets(1).Visible = False
```

**Protecting a Worksheet:**
```vba
Dim strPassword As String
strPassword = InputBox("Enter the password for the worksheet")
Worksheets("Sheet1").Protect password:=strPassword, scenarios:=True
```

**Setting Page Orientation and Printing:**
```vba
Worksheets("Sheet1").Activate
ActiveSheet.PageSetup.Orientation = xlLandscape
ActiveSheet.PrintOut
```

**BeforeDoubleClick Event Handler:**
```vba
Private Sub Worksheet_BeforeDoubleClick(ByVal Target As Range, Cancel As Boolean)
    Dim sFile As String, sPath As String, sTxt As String, sExe As String, sSfx As String
    If Target.Address <> "$A$1" Then Exit Sub
    Cancel = True
    sPath = Range("D1").Value
    sExe = Range("D2").Value
    sSfx = Range("D3").Value
    sFile = Range("A1").Value
    sFile = WorksheetFunction.Substitute(sFile, " ", "")
    Do While InStr(sFile, ",")
        sTxt = sPath & "\" & Left(sFile, InStr(sFile, ",") - 1) & "." & sSfx
        If Dir(sTxt) <> "" Then Shell sExe & " " & sTxt, vbNormalFocus
        sFile = Right(sFile, Len(sFile) - InStr(sFile, ","))
    Loop
    sTxt = sPath & "\" & sFile & "." & sSfx
    If Dir(sTxt) <> "" Then Shell sExe & " " & sTxt, vbNormalNoFocus
End Sub
```

### 10.4 Range Object Examples

**Setting Cell Value:**
```vba
Range("A1").Value = 123
```

**Clearing Range Contents:**
```vba
Range("A1:B2").ClearContents
```

**Copying Range:**
```vba
Range("A1").Copy Destination:=Range("B1")
```

**Setting Formula:**
```vba
Range("A1").Formula = "=SUM(B1:B10)"
```

**Selecting a Range:**
```vba
Range("A1").Select
```

## Document History

**[2026-02-27 12:55]**
- Added: Dynamic Array properties (HasSpill, SpillingToRange, SpillParent) to Range section
- Added: AutoFilter object (Section 6.17) with methods/properties
- Added: Out of Scope note for Power Pivot, Power Query, Slicer/Timeline objects
- Review: `_INFO_AXCEL-IN01_VBA_API_REVIEW.md` findings addressed

**[2026-02-27 Session]**
- Created: Comprehensive VBA API reference document
- Source: Microsoft Learn Office VBA Reference
- Coverage: Application, Workbook, Worksheet, Range objects with complete methods/properties/events
- Added: Supporting objects, collections, enumerations, WorksheetFunction categories
- Added: Code examples from official Microsoft documentation

