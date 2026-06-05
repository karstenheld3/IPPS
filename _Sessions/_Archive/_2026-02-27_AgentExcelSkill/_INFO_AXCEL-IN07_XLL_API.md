<DevSystem MarkdownTablesAllowed=true />

# INFO: Excel XLL SDK Complete API Reference

**Doc ID**: AXCEL-IN07-API
**Goal**: Comprehensive documentation of all Excel XLL SDK C API functions, callbacks, and data types
**Version Scope**: Excel XLL SDK for Excel 2013+ (2026-02-27)
**Source**: Microsoft Learn - Excel XLL SDK API Function Reference

**Depends on:**
- `_INFO_AXCEL-IN07_XLL.md [AXCEL-IN07]` for XLL SDK overview and usage

## Table of Contents

1. API Overview
2. Data Types (XLOPER/XLOPER12)
3. Add-in Manager and XLL Interface Functions
4. C API Callback Functions (Excel4/Excel12)
5. C API Functions (DLL/XLL Only)
6. Essential XLM Functions
7. Framework Library Functions
8. Return Codes
9. Type Strings for Registration
10. Code Examples from Official Documentation

**Out of Scope**: Cluster connector functions, Generic DLL functions.

**Key Insight**: The XLL SDK provides the fastest Excel integration via direct C/C++ callbacks. All interaction with Excel goes through `Excel4`/`Excel12` callback functions using `XLOPER`/`XLOPER12` variant data types.

`[VERIFIED] (https://learn.microsoft.com/en-us/office/client-developer/excel/excel-xll-sdk-api-function-reference)`

## 1. API Overview

### 1.1 SDK Components

- **Header Files**: xlcall.h (main), xlcall32.lib (32-bit) / xlcall.lib (64-bit)
- **Architecture**: Must compile separate 32-bit and 64-bit XLLs for each Excel version
- **Callback Functions**: Excel4, Excel12, Excel4v, Excel12v
- **Data Types**: XLOPER (Excel 2003), XLOPER12 (Excel 2007+)
- **Interface Functions**: xlAutoOpen, xlAutoClose, etc.

### 1.2 Function Categories

The XLL SDK API is organized into these categories:

- **Add-in Manager Interface** (7 functions): xlAutoOpen, xlAutoClose, xlAutoAdd, xlAutoRemove, xlAutoFree, xlAutoRegister, xlAddInManagerInfo
- **Callback Functions** (4 variants): Excel4, Excel12, Excel4v, Excel12v
- **C API Functions** (19 functions): xlCoerce, xlFree, xlSet, xlGetName, etc.
- **XLM Functions** (200+): Worksheet and macro sheet functions accessible via callbacks
- **Framework Library**: Helper functions for memory and string handling

### 1.3 Thread Safety

Functions can be marked thread-safe for parallel calculation:
- Use `$` suffix in type string to mark function as thread-safe
- Thread-safe functions can run on multiple threads during recalculation
- Must not modify global state or call non-thread-safe Excel functions

## 2. Data Types (XLOPER/XLOPER12)

The `XLOPER` and `XLOPER12` structures are variant data types that can hold different Excel value types.

`[VERIFIED] (https://learn.microsoft.com/en-us/office/client-developer/excel/data-types-used-by-excel)`

### 2.1 XLOPER12 Structure

**String Format**: XLOPER12 strings are Pascal-style counted strings. The first WCHAR contains the length (not null-terminated). Example: `L"\005Hello"` represents "Hello" (length 5 as first character). Maximum length: 32767 characters.

```c
typedef struct xloper12 {
    union {
        double num;                    // xltypeNum
        XCHAR *str;                    // xltypeStr (counted string)
        BOOL xbool;                    // xltypeBool
        int err;                       // xltypeErr
        int w;                         // xltypeInt
        struct {
            WORD count;
            XLREF12 ref;
        } sref;                        // xltypeSRef
        struct {
            XLMREF12 *lpmref;
            IDSHEET idSheet;
        } mref;                        // xltypeRef
        struct {
            struct xloper12 *lparray;
            RW rows;
            COL columns;
        } array;                       // xltypeMulti
        struct {
            union {
                int level;
                short tbctrl;
                IDSHEET idSheet;
            } val;
            DWORD rw;
            COL col;
        } valflow;                     // xltypeFlow (internal)
        struct {
            BYTE *h;
            long cbData;
        } bigdata;                     // xltypeBigData
    } val;
    DWORD xltype;                      // Type indicator
} XLOPER12, *LPXLOPER12;
```

### 2.2 Type Constants (xltype values)

| Constant | Value | Description |
|----------|-------|-------------|
| xltypeNum | 0x0001 | IEEE 64-bit double |
| xltypeStr | 0x0002 | Counted string (first char = length) |
| xltypeBool | 0x0004 | Boolean (TRUE/FALSE) |
| xltypeRef | 0x0008 | External reference (multiple areas) |
| xltypeErr | 0x0010 | Error value (#VALUE!, #REF!, etc.) |
| xltypeFlow | 0x0020 | Internal flow control (not used by XLLs) |
| xltypeMulti | 0x0040 | Array of XLOPER12 values |
| xltypeMissing | 0x0080 | Missing argument |
| xltypeNil | 0x0100 | Empty cell |
| xltypeSRef | 0x0400 | Single rectangular reference |
| xltypeInt | 0x0800 | 16-bit signed integer |
| xltypeBigData | 0x2000 | Large binary data (Excel 2007+) |

### 2.3 Type Modifiers

| Modifier | Value | Description |
|----------|-------|-------------|
| xlbitXLFree | 0x1000 | Memory allocated by Excel, free with xlFree |
| xlbitDLLFree | 0x4000 | Memory allocated by DLL, Excel calls xlAutoFree |

### 2.4 Error Values (xltypeErr)

| Constant | Value | Excel Error |
|----------|-------|-------------|
| xlerrNull | 0 | #NULL! |
| xlerrDiv0 | 7 | #DIV/0! |
| xlerrValue | 15 | #VALUE! |
| xlerrRef | 23 | #REF! |
| xlerrName | 29 | #NAME? |
| xlerrNum | 36 | #NUM! |
| xlerrNA | 42 | #N/A |
| xlerrGettingData | 43 | #GETTING_DATA |

### 2.5 Memory Management Rules

**Critical rules to avoid memory leaks and crashes:**
- **Never free arguments**: XLOPERs passed to your function are read-only; never free() or overwrite them
- **Use xlFree only for Excel memory**: Call xlFree only on XLOPERs returned by Excel C API calls
- **Deep copy strings**: Copy Excel-allocated strings before storing; don't keep pointers to Excel memory
- **Consistent allocation**: Use same allocation method (malloc/new) throughout; set xlbitDLLFree for DLL-allocated returns

## 3. Add-in Manager and XLL Interface Functions

These functions are exported by the XLL and called by Excel.

`[VERIFIED] (https://learn.microsoft.com/en-us/office/client-developer/excel/add-in-manager-and-xll-interface-functions)`

### 3.1 xlAutoOpen

Called when XLL is loaded. Register functions and initialize here.

```c
int WINAPI xlAutoOpen(void);
```

**Return**: 1 for success, 0 for failure
**Purpose**: Register UDFs, initialize data structures, customize UI

### 3.2 xlAutoClose

Called when XLL is unloaded. Cleanup resources here.

```c
int WINAPI xlAutoClose(void);
```

**Return**: 1 for success
**Purpose**: Unregister functions, release resources, undo customizations

### 3.3 xlAutoAdd

Called when user adds XLL via Add-in Manager.

```c
int WINAPI xlAutoAdd(void);
```

**Return**: 1 for success
**Purpose**: Display welcome message, additional setup

### 3.4 xlAutoRemove

Called when user removes XLL via Add-in Manager.

```c
int WINAPI xlAutoRemove(void);
```

**Return**: 1 for success
**Purpose**: Display goodbye message, cleanup

### 3.5 xlAutoFree / xlAutoFree12

Called by Excel to free memory allocated by DLL (marked with xlbitDLLFree).

```c
void WINAPI xlAutoFree(LPXLOPER pxFree);
void WINAPI xlAutoFree12(LPXLOPER12 pxFree);
```

**Purpose**: Free memory that DLL allocated for return values

### 3.6 xlAutoRegister / xlAutoRegister12

Called when xlfRegister is called without type information.

```c
LPXLOPER WINAPI xlAutoRegister(LPXLOPER pxName);
LPXLOPER12 WINAPI xlAutoRegister12(LPXLOPER12 pxName);
```

**Purpose**: Provide type information for function registration

### 3.7 xlAddInManagerInfo / xlAddInManagerInfo12

Provides add-in name for Add-in Manager dialog.

```c
LPXLOPER WINAPI xlAddInManagerInfo(LPXLOPER pxAction);
LPXLOPER12 WINAPI xlAddInManagerInfo12(LPXLOPER12 pxAction);
```

**Purpose**: Return add-in display name when pxAction = 1

## 4. C API Callback Functions

Main interface for calling Excel from DLL/XLL.

`[VERIFIED] (https://learn.microsoft.com/en-us/office/client-developer/excel/excel4-excel12)`

### 4.1 Excel4 / Excel12

Call Excel worksheet functions, commands, or special functions.

```c
int Excel4(int iFunction, LPXLOPER pxRes, int iCount, LPXLOPER arg1, ...);
int Excel12(int iFunction, LPXLOPER12 pxRes, int iCount, LPXLOPER12 arg1, ...);
```

**Parameters:**
- `iFunction` - Function/command ID (xlf... or xlc... constant)
- `pxRes` - Pointer to result XLOPER
- `iCount` - Number of arguments (0-30 for Excel4, 0-255 for Excel12)
- `arg1, ...` - Pointers to argument XLOPERs

### 4.2 Excel4v / Excel12v

Array-based variants (arguments passed as array).

```c
int Excel4v(int iFunction, LPXLOPER pxRes, int iCount, LPXLOPER pxArgs[]);
int Excel12v(int iFunction, LPXLOPER12 pxRes, int iCount, LPXLOPER12 pxArgs[]);
```

### 4.3 Valid iFunction Values

**Special Functions** (xlXxx):
- xlAbort, xlCoerce, xlFree, xlGetName, xlStack
- xlDefineBinaryName, xlGetBinaryName
- xlSet, xlUDF, xlDisableXLMsgs, xlEnableXLMsgs
- xlGetHwnd, xlGetInst, xlSheetId, xlSheetNm

**Worksheet Functions** (xlfXxx):
- xlfRegister, xlfUnregister
- xlfCaller, xlfGetCell, xlfGetWorkbook
- Mathematical: xlfSum, xlfAverage, xlfMax, xlfMin, etc.
- Text: xlfConcatenate, xlfLen, xlfMid, xlfLeft, xlfRight
- Lookup: xlfVlookup, xlfHlookup, xlfIndex, xlfMatch

**Commands** (xlcXxx):
- xlcAlert, xlcMessage, xlcInput
- xlcDefineName, xlcDeleteName
- xlcOpen, xlcClose, xlcSave, xlcSaveAs
- xlcSelect, xlcActivate, xlcFormula

### 4.4 Function Classes

Functions are classified by when they can be called:

- **Class 1**: From worksheet during recalculation
- **Class 2**: From function macro or worksheet (# registered)
- **Class 3**: From object, macro, menu, toolbar, shortcut key

## 5. C API Functions (DLL/XLL Only)

These 19 functions can only be called from DLL/XLL code.

`[VERIFIED] (https://learn.microsoft.com/en-us/office/client-developer/excel/c-api-functions-that-can-be-called-only-from-a-dll-or-xll)`

### 5.1 xlAbort

Check if user pressed Escape to abort calculation.

```c
Excel12(xlAbort, &xRes, 1, &xBoolArg);
```

**Returns**: xltypeBool - TRUE if user requested abort

### 5.2 xlAsyncReturn

Return result from asynchronous UDF.

```c
Excel12(xlAsyncReturn, NULL, 2, &xAsyncHandle, &xResult);
```

### 5.3 xlCoerce

Convert XLOPER type or look up cell values.

```c
Excel12(xlCoerce, &xRes, 2, &xSource, &xDestType);
```

**Parameters:**
- `xSource` - Value to convert
- `xDestType` - Target type bitmask (optional)

**Example:**
```c
short WINAPI xlCoerceExample(short iVal)
{
    XLOPER12 xStr, xInt, xDestType;
    xInt.xltype = xltypeInt;
    xInt.val.w = iVal;
    xDestType.xltype = xltypeInt;
    xDestType.val.w = xltypeStr;
    
    Excel12f(xlCoerce, &xStr, 2, &xInt, &xDestType);
    Excel12f(xlcAlert, 0, 1, &xStr);
    Excel12f(xlFree, 0, 1, &xStr);
    return 1;
}
```

### 5.4 xlDefineBinaryName

Store binary data with a name.

```c
Excel12(xlDefineBinaryName, NULL, 2, &xName, &xBinaryData);
```

### 5.5 xlDisableXLMsgs / xlEnableXLMsgs

Disable/enable Excel message handling during DLL operations.

```c
Excel12(xlDisableXLMsgs, NULL, 0);
// ... perform operations ...
Excel12(xlEnableXLMsgs, NULL, 0);
```

### 5.6 xlEventRegister

Register for Excel events.

```c
Excel12(xlEventRegister, NULL, 2, &xProcName, &xEventType);
```

### 5.7 xlFree

Free memory allocated by Excel for XLOPER results.

```c
Excel12(xlFree, NULL, 1, &xResult);
```

**Critical**: Must free any XLOPER with xlbitXLFree flag set.

### 5.8 xlGetBinaryName

Retrieve binary data stored with xlDefineBinaryName.

```c
Excel12(xlGetBinaryName, &xResult, 1, &xName);
```

### 5.9 xlGetHwnd

Get Excel main window handle.

```c
Excel12(xlGetHwnd, &xHwnd, 0);
HWND hWnd = (HWND)xHwnd.val.w;  // Excel 2003
// or for Excel 2007+:
// HWND hWnd = (HWND)(DWORD_PTR)xHwnd.val.w;
```

### 5.10 xlGetInst / xlGetInstPtr

Get Excel instance handle.

```c
Excel12(xlGetInst, &xInst, 0);    // Returns HINSTANCE as integer
Excel12(xlGetInstPtr, &xInst, 0); // Returns HINSTANCE as pointer (64-bit safe)
```

### 5.11 xlGetName

Get full path of the XLL.

```c
Excel12(xlGetName, &xName, 0);
// xName.val.str contains the path
Excel12(xlFree, NULL, 1, &xName);
```

### 5.12 xlRunningOnCluster

Check if running on compute cluster.

```c
Excel12(xlRunningOnCluster, &xResult, 0);
```

### 5.13 xlSet

Write value to a cell or range.

```c
Excel12(xlSet, NULL, 2, &xRef, &xValue);
```

**Parameters:**
- `xRef` - Cell/range reference (xltypeSRef or xltypeRef)
- `xValue` - Value to write

**Example:**
```c
XLOPER12 xRef, xValue;
xRef.xltype = xltypeSRef;
xRef.val.sref.count = 1;
xRef.val.sref.ref.rwFirst = 0;  // Row 1
xRef.val.sref.ref.rwLast = 0;
xRef.val.sref.ref.colFirst = 0; // Column A
xRef.val.sref.ref.colLast = 0;

xValue.xltype = xltypeNum;
xValue.val.num = 123.456;

Excel12(xlSet, NULL, 2, &xRef, &xValue);
```

### 5.14 xlSheetId

Get sheet ID from sheet name.

```c
Excel12(xlSheetId, &xResult, 1, &xSheetName);
```

### 5.15 xlSheetNm

Get sheet name from sheet ID.

```c
Excel12(xlSheetNm, &xResult, 1, &xSheetRef);
```

### 5.16 xlStack

Get available stack space.

```c
Excel12(xlStack, &xResult, 0);
int stackSpace = xResult.val.w;
```

### 5.17 xlUDF

Call a user-defined function by name.

```c
Excel12(xlUDF, &xResult, 3, &xFuncName, &xArg1, &xArg2);
```

## 6. Essential XLM Functions

Commonly used XLM functions accessible via Excel4/Excel12.

`[VERIFIED] (https://learn.microsoft.com/en-us/office/client-developer/excel/essential-and-useful-c-api-xlm-functions)`

### 6.1 xlfRegister

Register a function with Excel. **Essential for XLLs.**

```c
Excel12(xlfRegister, &xResult, 11,
    &xDLL,           // DLL path (from xlGetName)
    &xProcName,      // Function name in DLL
    &xTypeText,      // Return and argument types
    &xFuncName,      // Function name in Excel
    &xArgNames,      // Argument names
    &xMacroType,     // 1=function, 2=command
    &xCategory,      // Function category
    &xShortcut,      // Shortcut key (commands only)
    &xHelpTopic,     // Help topic
    &xFuncDesc,      // Function description
    &xArg1Desc       // Argument descriptions...
);
```

### 6.2 xlfUnregister

Unregister a function.

```c
Excel12(xlfUnregister, NULL, 1, &xRegisterId);
```

### 6.3 xlfCaller

Get information about what called the function.

```c
Excel12(xlfCaller, &xResult, 0);
// Returns reference to calling cell, or #REF! if called from macro
```

### 6.4 xlfGetCell

Get cell properties.

```c
Excel12(xlfGetCell, &xResult, 2, &xTypeNum, &xRef);
```

**Type values**: 1=formula, 5=contents, 7=format, 17=row height, etc.

### 6.5 xlfGetWorkbook

Get workbook information.

```c
Excel12(xlfGetWorkbook, &xResult, 2, &xTypeNum, &xWorkbookName);
```

## 7. Framework Library Functions

Helper functions provided in the FRAMEWRK.C file.

### 7.1 TempNum / TempNum12

Create temporary numeric XLOPER.

```c
LPXLOPER12 TempNum12(double d);
```

### 7.2 TempStr / TempStr12

Create temporary string XLOPER (counted string).

```c
LPXLOPER12 TempStr12(LPWSTR str);
```

### 7.3 TempBool / TempBool12

Create temporary boolean XLOPER.

```c
LPXLOPER12 TempBool12(BOOL b);
```

### 7.4 TempInt / TempInt12

Create temporary integer XLOPER.

```c
LPXLOPER12 TempInt12(int i);
```

### 7.5 TempErr / TempErr12

Create temporary error XLOPER.

```c
LPXLOPER12 TempErr12(int err);
```

### 7.6 TempActiveRef / TempActiveRef12

Create reference to active sheet range.

```c
LPXLOPER12 TempActiveRef12(RW rwFirst, RW rwLast, COL colFirst, COL colLast);
```

### 7.7 Excel / Excel12f

Wrapper for Excel4/Excel12 with automatic memory management.

```c
int Excel12f(int iFunction, LPXLOPER12 pxRes, int iCount, ...);
```

**Note**: Automatically frees temporary XLOPERs created by TempXxx functions.

## 8. Return Codes

Return values from Excel4/Excel12 calls.

| Constant | Value | Description |
|----------|-------|-------------|
| xlretSuccess | 0 | Success |
| xlretAbort | 1 | User aborted (Escape pressed) |
| xlretInvXlfn | 2 | Invalid function number |
| xlretInvCount | 4 | Invalid argument count |
| xlretInvXloper | 8 | Invalid XLOPER/XLOPER12 |
| xlretStackOvfl | 16 | Stack overflow |
| xlretFailed | 32 | Command failed |
| xlretUncalced | 64 | Cell not yet calculated |
| xlretNotThreadSafe | 128 | Not thread-safe (Excel 2007+) |
| xlretInvAsynchronousContext | 256 | Invalid async context (Excel 2010+) |
| xlretNotClusterSafe | 512 | Not cluster-safe (Excel 2010+) |

## 9. Type Strings for Registration

Type codes used in xlfRegister type string.

### 9.1 Return Types

| Code | Type | Description |
|------|------|-------------|
| A | BOOL | Boolean |
| B | double | IEEE 64-bit double |
| C | char* | Null-terminated string (ANSI) |
| D | char* | Counted byte string |
| E | double* | Pointer to double |
| F | char* | Null-terminated string (modify in place) |
| G | char* | Counted byte string (modify in place) |
| H | unsigned short | WORD |
| I | short | Signed 16-bit integer |
| J | long | Signed 32-bit integer |
| K | FP* | Floating-point array |
| L | BOOL* | Pointer to BOOL |
| M | short* | Pointer to short |
| N | long* | Pointer to long |
| O | varies | Three args: count, array, array |
| P | XLOPER* | XLOPER (value types only) |
| Q | XLOPER12* | XLOPER12 (value types only) |
| R | XLOPER* | XLOPER (all types) |
| U | XLOPER12* | XLOPER12 (all types) |

### 9.2 Type Modifiers

| Modifier | Description |
|----------|-------------|
| # | Function is macro-equivalent |
| ! | Function is volatile (recalc always) |
| $ | Function is thread-safe |
| & | Function is cluster-safe |
| % | Function supports async (2010+) |
| > | Function is not allowed in cluster |

### 9.3 Example Type Strings

- `"BB"` - Returns double, takes one double
- `"BBB"` - Returns double, takes two doubles
- `"PPPP"` - Returns XLOPER, takes three XLOPERs
- `"QQQ$"` - Thread-safe, returns XLOPER12, takes two XLOPER12s
- `"B!BB"` - Volatile function, returns double

## 10. Code Examples from Official Documentation

### 10.1 Register Function (xlAutoOpen)

```c
#include <windows.h>
#include "xlcall.h"
#include "framewrk.h"

__declspec(dllexport) int WINAPI xlAutoOpen(void)
{
    static XLOPER12 xDLL;
    Excel12f(xlGetName, &xDLL, 0);
    
    // Register AddNumbers function
    Excel12f(xlfRegister, 0, 11,
        &xDLL,
        TempStr12(L"AddNumbers"),       // DLL function name
        TempStr12(L"BBB"),              // Types: returns double, 2 double args
        TempStr12(L"AddNumbers"),       // Excel function name
        TempStr12(L"Num1,Num2"),        // Argument names
        TempStr12(L"1"),                // Type 1 = worksheet function
        TempStr12(L"MyCategory"),       // Category
        TempStr12(L""),                 // Shortcut (none)
        TempStr12(L""),                 // Help topic
        TempStr12(L"Adds two numbers"), // Description
        TempStr12(L"First number"),     // Arg 1 description
        TempStr12(L"Second number")     // Arg 2 description
    );
    
    Excel12f(xlFree, 0, 1, &xDLL);
    return 1;
}
```

`[VERIFIED] (https://learn.microsoft.com/en-us/office/client-developer/excel/creating-xlls)`

### 10.2 Simple UDF

```c
__declspec(dllexport) double WINAPI AddNumbers(double num1, double num2)
{
    return num1 + num2;
}
```

### 10.3 Read Cell Value

```c
double ReadCellValue(int row, int col)
{
    XLOPER12 xRef, xVal;
    
    // Create reference to cell
    xRef.xltype = xltypeSRef;
    xRef.val.sref.count = 1;
    xRef.val.sref.ref.rwFirst = row - 1;  // 0-based
    xRef.val.sref.ref.rwLast = row - 1;
    xRef.val.sref.ref.colFirst = col - 1;
    xRef.val.sref.ref.colLast = col - 1;
    
    // Coerce to number
    Excel12f(xlCoerce, &xVal, 2, &xRef, TempNum12(xltypeNum));
    
    double result = 0.0;
    if (xVal.xltype == xltypeNum) {
        result = xVal.val.num;
    }
    
    Excel12f(xlFree, 0, 1, &xVal);
    return result;
}
```

### 10.4 Write Cell Value

```c
void WriteCellValue(int row, int col, double value)
{
    XLOPER12 xRef, xValue;
    
    xRef.xltype = xltypeSRef;
    xRef.val.sref.count = 1;
    xRef.val.sref.ref.rwFirst = row - 1;
    xRef.val.sref.ref.rwLast = row - 1;
    xRef.val.sref.ref.colFirst = col - 1;
    xRef.val.sref.ref.colLast = col - 1;
    
    xValue.xltype = xltypeNum;
    xValue.val.num = value;
    
    Excel12(xlSet, NULL, 2, &xRef, &xValue);
}
```

### 10.5 Return Array from UDF

```c
__declspec(dllexport) LPXLOPER12 WINAPI ReturnArray(void)
{
    static XLOPER12 xResult;
    static XLOPER12 xArray[4];
    
    // Create 2x2 array
    xArray[0].xltype = xltypeNum; xArray[0].val.num = 1.0;
    xArray[1].xltype = xltypeNum; xArray[1].val.num = 2.0;
    xArray[2].xltype = xltypeNum; xArray[2].val.num = 3.0;
    xArray[3].xltype = xltypeNum; xArray[3].val.num = 4.0;
    
    xResult.xltype = xltypeMulti;
    xResult.val.array.lparray = xArray;
    xResult.val.array.rows = 2;
    xResult.val.array.columns = 2;
    
    return &xResult;
}
```

### 10.6 xlAddInManagerInfo12

```c
__declspec(dllexport) LPXLOPER12 WINAPI xlAddInManagerInfo12(LPXLOPER12 pxAction)
{
    static XLOPER12 xInfo, xIntAction;
    
    Excel12f(xlCoerce, &xIntAction, 2, pxAction, TempInt12(xltypeInt));
    
    if (xIntAction.val.w == 1)
    {
        // Return add-in name
        xInfo.xltype = xltypeStr;
        xInfo.val.str = L"\015My XLL Add-in";  // Counted string
    }
    else
    {
        xInfo.xltype = xltypeErr;
        xInfo.val.err = xlerrValue;
    }
    
    return &xInfo;
}
```

### 10.7 Volatile Function

```c
// Register with "!" modifier: "B!BB"
__declspec(dllexport) double WINAPI VolatileFunc(double x, double y)
{
    // This function recalculates every time any cell changes
    return x * y + rand() / (double)RAND_MAX;
}
```

### 10.8 xlAutoClose

```c
__declspec(dllexport) int WINAPI xlAutoClose(void)
{
    // Cleanup code here
    // Unregister functions if needed
    // Release resources
    return 1;
}
```

## Document History

**[2026-02-27 13:35]**
- Added: DevSystem tag for Markdown tables
- Added: 32/64-bit architecture note in Section 1.1
- Added: Pascal string format note in Section 2.1
- Added: Memory management rules in Section 2.5
- Review: `_INFO_AXCEL-IN07_XLL_API_REVIEW.md` findings addressed

**[2026-02-27 Session]**
- Created: Comprehensive XLL SDK API reference document
- Source: Microsoft Learn Excel XLL SDK API Function Reference
- Coverage: 7 interface functions, 19 C API functions, XLOPER data types
- Added: Type strings, return codes, framework library
- Added: Code examples from official documentation
