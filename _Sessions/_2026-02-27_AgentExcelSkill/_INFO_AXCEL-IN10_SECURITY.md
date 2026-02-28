# INFO: Security and Trust Settings

**Doc ID**: AXCEL-IN10
**Goal**: Document security requirements for Excel automation across all APIs
**Version Scope**: Excel 2016+ / Microsoft 365 (2026-02-27)

**Depends on:**
- `__EXCEL_APIS_SOURCES.md [AXCEL-SOURCES-01]` for source references

## Overview

Excel automation involves multiple security layers depending on the API used. This document consolidates security requirements across all Excel APIs, providing a single reference for configuring trust settings, understanding security implications, and making informed decisions about security trade-offs.

## Security Settings Matrix

| Setting | VBA | COM | VSTO | JS API | Required For |
|---------|-----|-----|------|--------|--------------|
| Macro Security | Yes | No | No | No | Running VBA macros |
| Trust VBA Project | Yes | Yes | Yes | No | VBA code export/import |
| Trusted Locations | Yes | No | No | No | Auto-enable macros |
| Digital Signatures | Yes | No | Yes | Yes | Enterprise deployment |
| Admin Consent | No | No | No | No | Graph API permissions |

## Macro Security Settings

### Location

File > Options > Trust Center > Trust Center Settings > Macro Settings

### Options

1. **Disable all macros without notification**: Most secure, blocks all VBA
2. **Disable all macros with notification**: Recommended - user can enable per-workbook
3. **Disable all macros except digitally signed**: Allows signed macros only
4. **Enable all macros**: Not recommended - security risk

### Programmatic Access

Cannot change macro settings programmatically - by design for security.

## Trust Access to VBA Project Object Model

### What It Enables

- Read VBA code from workbooks
- Write/modify VBA code
- Export VBA modules to files
- Import VBA modules from files
- Access VBProject, VBComponents, CodeModule objects

### How to Enable

1. Excel > File > Options > Trust Center
2. Click "Trust Center Settings..."
3. Select "Macro Settings"
4. Check "Trust access to the VBA project object model"
5. Click OK

### Security Implications

**WARNING**: Enabling this setting allows any macro to:
- Read VBA code from all open workbooks
- Inject malicious code into other workbooks
- Modify existing macros
- Create new macros

**Recommendations**:
- Enable only when needed for specific automation
- Disable after automation task completes
- Use COM automation from external process for better isolation
- Consider using separate Excel instance for sensitive operations

`[VERIFIED] (AXCEL-SC-MSFT-SECVB)`

## Trusted Locations

### Purpose

Workbooks in trusted locations:
- Macros run without security prompts
- ActiveX controls enabled
- External data connections allowed

### How to Configure

1. Trust Center > Trusted Locations
2. Add new location (local folder or network path)
3. Optionally allow subfolders

### Security Considerations

- Do not trust network locations unless necessary
- Do not trust folders with user-uploaded content
- Limit trusted locations to specific automation folders

## Digital Signatures

### For VBA Projects

1. Obtain code signing certificate (self-signed for dev, CA-issued for production)
2. Open VBA Editor (Alt+F11)
3. Tools > Digital Signature
4. Choose certificate
5. Save workbook

### For VSTO Add-ins

```xml
<!-- In .vsto manifest -->
<publisherIdentity name="CN=YourCompany" issuerKeyHash="..." />
```

### For Office Add-ins (JS)

- SSL certificate required for hosting
- Submit to AppSource for verification
- Or use centralized deployment with admin trust

`[VERIFIED] (AXCEL-SC-MSFT-SECNT)`

## Graph API Permissions

### Delegated Permissions (User Context)

- `Files.Read` - Read user's files
- `Files.ReadWrite` - Read/write user's files
- `Files.Read.All` - Read all files user can access
- `Files.ReadWrite.All` - Read/write all accessible files

### Application Permissions (Daemon/Service)

- `Files.Read.All` - Read all files in tenant
- `Files.ReadWrite.All` - Read/write all files
- `Sites.Read.All` - Read SharePoint sites
- `Sites.ReadWrite.All` - Read/write SharePoint sites

### Admin Consent

Application permissions require admin consent in Azure AD.

## Security Best Practices

### For Agent-Based Automation (Windsurf Cascade)

1. **Use separate Excel instance**: Start dedicated Excel process for automation
2. **Minimal permissions**: Request only needed file access
3. **Temporary trust**: Enable VBA trust only during code manipulation
4. **Process isolation**: COM automation from external process limits blast radius
5. **Cleanup**: Release COM objects, close Excel when done

### For Production Deployment

1. **Sign all code**: VBA projects, VSTO add-ins, Office Add-ins
2. **Trusted publishers**: Add signing certificates to trusted publishers
3. **Group Policy**: Configure macro settings via GPO for enterprise
4. **Audit logging**: Monitor automation activities
5. **Least privilege**: Use delegated permissions where possible

## Group Policy Settings (Enterprise)

### Location

Computer Configuration > Administrative Templates > Microsoft Excel > Security

### Key Policies

- **VBA Macro Notification Settings**: Control macro behavior
- **Trust access to Visual Basic Project**: Enable/disable VBProject access
- **Trusted Locations**: Define via policy instead of UI
- **Block macros from Internet**: Recommended to enable

## Error Messages and Resolutions

### "Programmatic access to Visual Basic Project is not trusted"

**Cause**: VBProject access attempted without trust setting enabled

**Resolution**: Enable "Trust access to the VBA project object model"

### "The macro may not be available..."

**Cause**: Macro security blocking execution

**Resolution**: Enable macros for the workbook or add to trusted location

### "This workbook contains macros or ActiveX controls that are disabled"

**Cause**: Protected View blocking macros from downloaded files

**Resolution**: Click "Enable Editing" then "Enable Content"

## Sources

- `[VERIFIED] (AXCEL-SC-MSFT-SECNT)` - Security notes for developers
- `[VERIFIED] (AXCEL-SC-MSFT-SECVB)` - Programmatic access to VBA

## Document History

**[2026-02-27 14:00]**
- Initial document creation with consolidated security settings
