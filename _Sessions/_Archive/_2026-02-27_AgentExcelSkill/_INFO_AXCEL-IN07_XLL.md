# INFO: Excel XLL SDK (C API)

**Doc ID**: AXCEL-IN07
**Goal**: Document Excel XLL SDK for high-performance native add-ins
**Version Scope**: Excel 2013+ XLL SDK (2026-02-27)

**Depends on:**
- `__EXCEL_APIS_SOURCES.md [AXCEL-SOURCES-01]` for source references

## Overview

The Excel XLL SDK provides a C/C++ API for creating high-performance native add-ins (XLLs) for Excel. XLLs are DLLs that Excel loads directly, providing the fastest possible integration for custom worksheet functions, commands, and data providers. The C API offers direct access to Excel's calculation engine with minimal overhead. `[VERIFIED] (AXCEL-SC-MSFT-XLLWC)`

XLLs are used when performance is critical - financial modeling, real-time data feeds, complex calculations. They can register custom functions that appear in Excel's function wizard. The SDK includes header files, libraries, and sample projects for Visual Studio. `[VERIFIED] (AXCEL-SC-MSFT-XLLPR)`

## Supported Features

- **Read cells/data**: Yes - Via xlCoerce and callback functions
- **Write cells/data**: Yes - Via xlSet and return values from UDFs
- **Read formulas**: Limited - Can read formula results, not formula text
- **Write formulas**: No - Cannot write formulas programmatically
- **Remote control open workbook**: Yes - Via C API callbacks from loaded XLL
- **Export to CSV**: No - Not designed for file operations
- **Export VBA code**: No - No VBProject access
- **Import VBA code**: No - No VBProject access
- **Works without Excel**: No - XLL must be loaded by Excel
- **Cross-platform**: No - Windows only (DLL technology)

## Intended Use Cases

1. **High-performance UDFs**: Custom functions needing maximum speed
2. **Real-time data feeds**: RTD servers and live data streaming
3. **Financial modeling**: Complex calculations with large data sets
4. **Scientific computing**: Integration with numerical libraries
5. **Legacy C/C++ integration**: Wrap existing C libraries for Excel

## Limitations

- **C/C++ only**: Requires native code development skills
- **Windows only**: DLLs are Windows-specific
- **Complex development**: Low-level API, manual memory management
- **No VBA integration**: Cannot manipulate VBA code
- **Limited documentation**: Less community support than COM/VBA
- **Debugging difficulty**: Harder to debug than managed code
- **32/64-bit variants**: Must build separate versions for each architecture

## Security Setup

### XLL Loading

1. File > Options > Add-ins > Manage: Excel Add-ins > Go
2. Browse to .xll file and enable
3. Or place in trusted XLSTART folder for auto-loading

### Trust Settings

- XLLs may be blocked by macro security settings
- Digitally sign XLLs for enterprise deployment
- Add XLL location to Trusted Locations

## Platform Support

- **Windows**: Yes - Primary platform
- **macOS**: No - DLLs not supported
- **Web**: No - Native code not applicable
- **Linux**: No - DLLs not supported

## Prerequisites

- Visual Studio (C/C++ development)
- Excel XLL SDK (download from Microsoft)
- Excel 2013+ installed
- xlcall32.lib for linking

## Code Examples

### C: Simple UDF (Add Two Numbers)

```c
#include <windows.h>
#include "xlcall.h"

// Register function with Excel
__declspec(dllexport) int WINAPI xlAutoOpen(void)
{
    static XLOPER12 xDLL;
    Excel12f(xlGetName, &xDLL, 0);
    
    // Register the AddNumbers function
    Excel12f(xlfRegister, 0, 11,
        &xDLL,                          // DLL name
        TempStr12(L"AddNumbers"),       // Function name in DLL
        TempStr12(L"BBB"),              // Return and arg types
        TempStr12(L"AddNumbers"),       // Function name in Excel
        TempStr12(L"Num1,Num2"),        // Argument names
        TempStr12(L"1"),                // Function type (1 = worksheet)
        TempStr12(L"MyCategory"),       // Category
        TempStr12(L""),                 // Shortcut
        TempStr12(L""),                 // Help topic
        TempStr12(L"Adds two numbers"), // Function description
        TempStr12(L"First number"),     // Arg 1 description
        TempStr12(L"Second number"));   // Arg 2 description
    
    Excel12f(xlFree, 0, 1, &xDLL);
    return 1;
}

// The actual function implementation
__declspec(dllexport) double WINAPI AddNumbers(double num1, double num2)
{
    return num1 + num2;
}

__declspec(dllexport) int WINAPI xlAutoClose(void)
{
    return 1;
}
```

### C: Read Cell Value

```c
#include "xlcall.h"

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

## Gotchas and Quirks

- **XLOPER types**: Complex data structure with many variants (xltypeNum, xltypeStr, etc.)
- **Memory management**: Must free XLOPER memory with xlFree
- **Thread safety**: Functions marked as thread-safe can run in parallel
- **Async functions**: Supported but complex to implement
- **String handling**: Uses Pascal-style counted strings, not null-terminated
- **Registration**: Must register functions in xlAutoOpen
- **Cluster support**: Can create cluster-safe functions for HPC scenarios `[VERIFIED] (AXCEL-SC-MSFT-XLLCR)`

## Main Documentation Links

- [Excel XLL SDK Welcome](https://learn.microsoft.com/en-us/office/client-developer/excel/welcome-to-the-excel-software-development-kit)
- [Programming with the C API](https://learn.microsoft.com/en-us/office/client-developer/excel/programming-with-the-c-api-in-excel)
- [Creating XLLs](https://learn.microsoft.com/en-us/office/client-developer/excel/creating-xlls)
- [XLL SDK API Reference](https://learn.microsoft.com/en-us/office/client-developer/excel/excel-xll-sdk-api-function-reference)

## Sources

- `[VERIFIED] (AXCEL-SC-MSFT-XLLWC)` - XLL SDK welcome
- `[VERIFIED] (AXCEL-SC-MSFT-XLLPR)` - Programming with C API
- `[VERIFIED] (AXCEL-SC-MSFT-XLLCR)` - Creating XLLs

## Document History

**[2026-02-27 13:45]**
- Initial document creation
