# INFO: Microsoft Graph API (Excel REST API)

**Doc ID**: AXCEL-IN04
**Goal**: Document Microsoft Graph API capabilities for cloud Excel automation
**Version Scope**: Graph API v1.0 (2026-02-27)

**Depends on:**
- `__EXCEL_APIS_SOURCES.md [AXCEL-SOURCES-01]` for source references

## Overview

Microsoft Graph API provides REST endpoints for reading and modifying Excel workbooks stored in OneDrive, SharePoint, or other Microsoft 365 storage. The Excel REST API exposes workbook resources including worksheets, ranges, tables, charts, and named items through standard HTTP methods. It enables cloud-first automation scenarios without requiring Excel installation. `[VERIFIED] (AXCEL-SC-MSFT-GRPOV)`

Graph API supports .xlsx files only (not .xls or .xlsm with macros). The API calculates formulas server-side, making it suitable for scenarios requiring computed values. It's ideal for web applications, mobile apps, and cloud services that need Excel data access. Rate limiting applies based on tenant and application thresholds. `[VERIFIED] (AXCEL-SC-MSFT-GRPWK)`

## Supported Features

- **Read cells/data**: Yes - GET on range or table resources
- **Write cells/data**: Yes - PATCH on range values
- **Read formulas**: Yes - Include formulas in range response
- **Write formulas**: Yes - PATCH with formula strings (calculated server-side)
- **Remote control open workbook**: No - File-based, not live instance
- **Export to CSV**: No - Must implement conversion from JSON response
- **Export VBA code**: No - .xlsm not supported
- **Import VBA code**: No - .xlsm not supported
- **Works without Excel**: Yes - Cloud service, no client needed
- **Cross-platform**: Yes - REST API works from any platform

## Intended Use Cases

1. **Cloud-first applications**: Web/mobile apps reading SharePoint Excel data
2. **Serverless automation**: Azure Functions processing Excel files
3. **Power Platform integration**: Extend Power Automate with custom Excel operations
4. **Cross-platform clients**: iOS, Android, or Linux apps accessing Excel data
5. **Real-time dashboards**: Read Excel data for business intelligence

## Limitations

- **Cloud storage only**: Works with OneDrive/SharePoint files, not local files
- **No .xls support**: Only .xlsx format supported
- **No VBA/macros**: Cannot work with .xlsm files for macro operations
- **Rate limiting**: Throttling based on tenant/app (no fixed published limits)
- **Session management**: Long operations require session ID management
- **Authentication complexity**: Requires Azure AD app registration, OAuth 2.0
- **Latency**: REST calls slower than local COM automation
- **No live control**: Cannot interact with user's open Excel application

## Security Setup

### Azure AD App Registration

1. Register application in Azure Portal > Azure Active Directory > App registrations
2. Add API permissions:
   - `Files.ReadWrite` (delegated) - for user's files
   - `Files.ReadWrite.All` (application) - for all files
   - `Sites.ReadWrite.All` - for SharePoint files
3. Create client secret or certificate
4. Configure redirect URIs for OAuth flow

### Authentication Flow

```
# Delegated (user context)
POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
grant_type=authorization_code
scope=https://graph.microsoft.com/Files.ReadWrite

# Application (daemon/service)
POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
grant_type=client_credentials
scope=https://graph.microsoft.com/.default
```

## Platform Support

- **Windows**: Yes - Any HTTP client
- **macOS**: Yes - Any HTTP client
- **Web**: Yes - JavaScript fetch/axios
- **Linux**: Yes - curl, any HTTP library

## Prerequisites

- Microsoft 365 subscription with OneDrive/SharePoint
- Azure AD app registration with appropriate permissions
- OAuth 2.0 access token
- Excel files stored in OneDrive or SharePoint (not local)

## Code Examples

### REST: Read Range Values

```http
GET https://graph.microsoft.com/v1.0/me/drive/items/{file-id}/workbook/worksheets/{sheet-name}/range(address='A1:C10')
Authorization: Bearer {access-token}

Response:
{
  "address": "Sheet1!A1:C10",
  "values": [
    ["Name", "Value", "Formula"],
    ["Test", 123, 246]
  ],
  "formulas": [
    ["Name", "Value", "Formula"],
    ["Test", 123, "=B2*2"]
  ]
}
```

### REST: Write Range Values

```http
PATCH https://graph.microsoft.com/v1.0/me/drive/items/{file-id}/workbook/worksheets/{sheet-name}/range(address='A1:B2')
Authorization: Bearer {access-token}
Content-Type: application/json

{
  "values": [
    ["Header1", "Header2"],
    ["Data1", 100]
  ]
}
```

### REST: Write Formula

```http
PATCH https://graph.microsoft.com/v1.0/me/drive/items/{file-id}/workbook/worksheets/{sheet-name}/range(address='C2')
Authorization: Bearer {access-token}
Content-Type: application/json

{
  "formulas": [["=A2&B2"]]
}
```

### C#: Using Microsoft Graph SDK

```csharp
using Microsoft.Graph;
using Azure.Identity;

// Authentication
var credential = new ClientSecretCredential(tenantId, clientId, clientSecret);
var graphClient = new GraphServiceClient(credential);

// Get workbook item
var driveItem = await graphClient.Me.Drive.Root
    .ItemWithPath("Documents/data.xlsx")
    .GetAsync();

string itemId = driveItem.Id;

// Read range
var range = await graphClient.Me.Drive.Items[itemId]
    .Workbook.Worksheets["Sheet1"]
    .Range("A1:C10")
    .GetAsync();

// Values are in range.Values as object[][]
foreach (var row in range.Values)
{
    Console.WriteLine(string.Join(", ", row));
}

// Write values
var updateRange = new WorkbookRange
{
    Values = new object[][] {
        new object[] { "Updated", 999 }
    }
};

await graphClient.Me.Drive.Items[itemId]
    .Workbook.Worksheets["Sheet1"]
    .Range("A1:B1")
    .PatchAsync(updateRange);
```

### Python: Using requests

```python
import requests

access_token = "your_access_token"
file_id = "your_file_id"
base_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/workbook"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Read range
response = requests.get(
    f"{base_url}/worksheets/Sheet1/range(address='A1:C10')",
    headers=headers
)
data = response.json()
print("Values:", data["values"])
print("Formulas:", data["formulas"])

# Write values
payload = {
    "values": [
        ["Python", 42],
        ["Data", 100]
    ]
}
response = requests.patch(
    f"{base_url}/worksheets/Sheet1/range(address='A1:B2')",
    headers=headers,
    json=payload
)

# Create session for long operations
session_response = requests.post(
    f"{base_url}/createSession",
    headers=headers,
    json={"persistChanges": True}
)
session_id = session_response.json()["id"]

# Use session in subsequent requests
headers["workbook-session-id"] = session_id
```

## Gotchas and Quirks

- **Session management**: Long-running operations need createSession/closeSession to avoid conflicts `[VERIFIED] (AXCEL-SC-MSFT-GRPBP)`
- **Throttling**: No fixed limits; varies by tenant size and concurrent usage
- **Formula evaluation**: Formulas are calculated server-side; results included in response
- **Null values**: Empty cells return null in values array
- **Date serialization**: Dates returned as OLE Automation dates (serial numbers)
- **Large ranges**: Paginate large range reads; consider using tables instead
- **File locking**: Concurrent edits may cause conflicts; use sessions
- **Permissions scope**: Delegated vs Application permissions have different capabilities

## Main Documentation Links

- [Excel Workbooks and Charts API Overview](https://learn.microsoft.com/en-us/graph/excel-concept-overview)
- [Working with Excel in Graph](https://learn.microsoft.com/en-us/graph/api/resources/excel)
- [Write Data to Workbook](https://learn.microsoft.com/en-us/graph/excel-write-to-workbook)
- [Best Practices for Excel API](https://learn.microsoft.com/en-us/graph/workbook-best-practice)

## Sources

- `[VERIFIED] (AXCEL-SC-MSFT-GRPOV)` - Excel API overview
- `[VERIFIED] (AXCEL-SC-MSFT-GRPWK)` - Working with Excel
- `[VERIFIED] (AXCEL-SC-MSFT-GRPWR)` - Write data to workbook
- `[VERIFIED] (AXCEL-SC-MSFT-GRPBP)` - Best practices

## Document History

**[2026-02-27 13:25]**
- Initial document creation with Graph API coverage
