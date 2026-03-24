<DevSystem MarkdownTablesAllowed=true />

# INFO: Interactive Browser Authentication

**Doc ID**: SPAUTH-AM04
**Goal**: Detailed guide for interactive browser authentication in FastAPI Azure Web Apps
**Version Scope**: Azure Identity 1.x, MSAL Python 1.x, Microsoft Entra ID (2026)

**Depends on:**
- `__AUTH_MECHANISMS_SOURCES.md [SPAUTH-SOURCES]` for source references

## 1. Intended Scenario and Recommended Use

### When to Use Interactive Browser

Interactive browser authentication is for **delegated** scenarios where a user is present:

- **Admin tools/dashboards** - User logs in to perform administrative tasks
- **User-initiated operations** - Operations that should run as the signed-in user
- **Personal account fallback** - When managed identity isn't available
- **Development/testing** - Quick auth without setting up service principals
- **Web applications with UI** - Users accessing via browser

### User Flow

```
┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐
│ User clicks  │───>│ Browser opens   │───>│ User logs in     │
│ "Login"      │    │ login.microsoft │    │ (may have MFA)   │
└──────────────┘    └─────────────────┘    └──────────────────┘
                                                   │
                    ┌─────────────────┐            │
                    │ Token returned  │<───────────┘
                    │ to application  │
                    └─────────────────┘
```

### When NOT to Use

- **Background services** - No user present (use certificate/managed identity)
- **Automated jobs** - Cannot interact with browser (use app-only)
- **Headless servers** - No browser available (use device code)
- **API-to-API calls** - Use app credentials or on-behalf-of

### Recommendation Level

| Scenario | Recommendation |
|----------|----------------|
| Admin dashboard (user logs in) | **RECOMMENDED** |
| User-specific operations | **RECOMMENDED** |
| Local development | Good for testing |
| Production background jobs | **NOT RECOMMENDED** |
| Azure App Service (API only) | **NOT RECOMMENDED** |

## 2. Public Client vs Confidential Client

MSAL defines two client types. The choice determines whether a certificate or secret is needed.

**PublicClientApplication** - No client credential (no secret, no certificate)
- PKCE alone protects the auth code exchange
- Used by: PnP PowerShell, CLI tools, desktop apps, mobile apps
- App registration: SPA platform redirect URI
- Refresh tokens: 24h inactive timeout, 90d max lifetime (with rotation)

**ConfidentialClientApplication** - Requires client credential (secret or certificate)
- Client credential + optional PKCE protects the exchange
- Used by: Server-side web apps that need to prove their own identity
- App registration: "Web" platform redirect URI
- Refresh tokens: full lifetime (configurable by tenant policy)

### When is ConfidentialClient needed?

Confidential client identity proof matters when:
- **Metered APIs** - billing tracks which app called
- **App impersonation risk** - bad actors could reuse the client_id
- **S2S communication** - service authenticating to another service

For an **admin tool / internal dashboard** where the USER authenticates interactively, `PublicClientApplication` with PKCE is sufficient. The user's identity (not the app's) determines access. This is exactly what PnP PowerShell does across all tenants without any certificate or secret.

### Recommendation for Interactive Browser in web apps

Use `PublicClientApplication` unless you have a specific reason to prove the app's identity independently of the user. For internal admin tools: PublicClient + PKCE is correct and simpler.

## 3. How to Use in FastAPI Azure Web App

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│ User's Browser                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ FastAPI Web UI                                              │ │
│ │                                                             │ │
│ │  ┌───────────┐    ┌──────────────────────────────────────┐  │ │
│ │  │ Login Btn │───>│ /auth/login endpoint                 │  │ │
│ │  └───────────┘    │ Redirects to Microsoft login         │  │ │
│ │                   └──────────────────────────────────────┘  │ │
│ │                              │                              │ │
│ │                              v                              │ │
│ │  ┌──────────────────────────────────────────────────────┐   │ │
│ │  │ Microsoft Login Page (login.microsoftonline.com)     │   │ │
│ │  │ User enters credentials, completes MFA               │   │ │
│ │  └──────────────────────────────────────────────────────┘   │ │
│ │                              │                              │ │
│ │                              v                              │ │
│ │  ┌──────────────────────────────────────────────────────┐   │ │
│ │  │ /auth/callback - Receives auth code                  │   │ │
│ │  │ Exchanges for tokens, stores in session              │   │ │
│ │  └──────────────────────────────────────────────────────┘   │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Complete FastAPI Implementation (Public Client)

```python
# app/auth/interactive_auth.py
import os
from msal import PublicClientApplication
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import logging

logger = logging.getLogger(__name__)

class InteractiveAuthService:
    """
    MSAL-based interactive authentication for FastAPI.
    Uses Authorization Code flow with PKCE via PublicClientApplication.
    No client secret or certificate required.
    """
    
    def __init__(self):
        self._client_id = os.environ["CLIENT_ID"]
        self._tenant_id = os.environ["TENANT_ID"]
        self._redirect_uri = os.environ["AUTH_REDIRECT_URI"]
        
        self._authority = f"https://login.microsoftonline.com/{self._tenant_id}"
        
        # PublicClientApplication: no client_credential parameter
        self._app = PublicClientApplication(
            client_id=self._client_id,
            authority=self._authority
        )
    
    def initiate_login(self, redirect_uri: str = None) -> dict:
        """Initiate auth code flow with PKCE. Returns flow dict with auth_uri."""
        flow = self._app.initiate_auth_code_flow(
            scopes=["https://contoso.sharepoint.com/.default"],
            redirect_uri=redirect_uri or self._redirect_uri
        )
        return flow
    
    def complete_login(self, flow: dict, auth_response: dict) -> dict:
        """Exchange authorization code for tokens using PKCE code_verifier."""
        result = self._app.acquire_token_by_auth_code_flow(
            auth_code_flow=flow,
            auth_response=auth_response
        )
        if "error" in result:
            raise HTTPException(
                status_code=400,
                detail=f"Token error: {result.get('error_description')}"
            )
        return result
    
    def get_token_silent(self, account: dict) -> dict:
        """Get token from cache or refresh."""
        accounts = self._app.get_accounts()
        matching = [a for a in accounts if a.get("username") == account.get("username")]
        if not matching:
            return None
        return self._app.acquire_token_silent(
            scopes=["https://contoso.sharepoint.com/.default"],
            account=matching[0]
        )


# app/main.py
from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.environ["SESSION_SECRET"])

auth_service = InteractiveAuthService()

@app.get("/auth/login")
async def login(request: Request):
    """Initiate login flow."""
    flow = auth_service.initiate_login()
    # Store flow in session (contains PKCE code_verifier for callback)
    request.session["auth_flow"] = flow
    return RedirectResponse(url=flow["auth_uri"])

@app.get("/auth/callback")
async def auth_callback(request: Request):
    """Handle OAuth callback."""
    flow = request.session.pop("auth_flow", None)
    if not flow:
        raise HTTPException(status_code=400, detail="No auth flow in session")
    
    # auth_response = query string params from Microsoft redirect
    result = auth_service.complete_login(flow, dict(request.query_params))
    
    request.session["user"] = {
        "name": result.get("id_token_claims", {}).get("name"),
        "email": result.get("id_token_claims", {}).get("preferred_username"),
        "access_token": result["access_token"]
    }
    return RedirectResponse(url="/")

@app.get("/auth/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/")
```

### Using Azure Identity (Simpler for Desktop/CLI)

```python
from azure.identity import InteractiveBrowserCredential

# For desktop apps or CLI tools
credential = InteractiveBrowserCredential(
    client_id="your-client-id",
    tenant_id="your-tenant-id",
    redirect_uri="http://localhost:8400"
)

# Opens browser, user logs in
token = credential.get_token("https://contoso.sharepoint.com/.default")
```

### Environment Variables

```bash
# Only these are needed for Interactive Browser login:
CLIENT_ID=abcdefab-1234-5678-abcd-abcdefabcdef
TENANT_ID=12345678-1234-1234-1234-123456789012
AUTH_REDIRECT_URI=https://myapp.azurewebsites.net/auth/callback
SESSION_SECRET=random-secret-for-session-encryption

# NOT needed: client secrets, certificates
```

## 4. Prerequisites

### Azure AD App Registration

1. **Create or reuse App Registration**
   - Can reuse an existing app registration (e.g., Crawler app) if it already has the right tenant
   - Or create new: Azure Portal > Microsoft Entra ID > App registrations > New registration
   - Supported account types: Single tenant (or multi-tenant if needed)

2. **Configure Redirect URIs (SPA platform)**
   - App registration > Authentication > Platform configurations
   - Add platform: **Single-page application** (NOT "Web")
   - Redirect URIs:
     - `https://myapp.azurewebsites.net/auth/callback` (production)
     - `http://localhost:8000/auth/callback` (development)
   - Do NOT enable "ID tokens" under Implicit grant (not needed with auth code + PKCE)
   
   **Why SPA and not Web?** The "Web" platform requires a client credential (secret or certificate) for the token exchange. The "SPA" platform allows PKCE-only token exchange, which is what `PublicClientApplication` uses. Despite the name, SPA platform works for server-side redirect callbacks too - CORS headers on the token endpoint are irrelevant for server-side requests.

3. **Configure API Permissions (Delegated)**
   
   This method uses **Delegated permissions** (user context). User's SharePoint permissions apply.
   
   - **Read-only apps:** `AllSites.Read` (SharePoint) or `Sites.Read.All` (Graph)
   - **Read-write apps:** `AllSites.Write` (SharePoint) or `Sites.ReadWrite.All` (Graph)
   - **Note:** `Sites.Selected` is NOT available for delegated permissions
   - Grant admin consent after adding permissions
   
   See [`_INFO_SPAUTH-IN07_AZURE_PERMISSION_REQUIREMENTS.md`](_INFO_SPAUTH-IN07_AZURE_PERMISSION_REQUIREMENTS.md) for full details.

4. **No Client Secret or Certificate Needed**
   
   `PublicClientApplication` with PKCE does not require any client credential. Skip the "Certificates & secrets" section entirely for Interactive Browser.

### Token Configuration (Optional)

- App registration > Token configuration
- Add optional claims for ID token:
  - `email`
  - `preferred_username`
  - `name`

## 5. Dependencies and Maintenance Problems

### Required Packages

```txt
# requirements.txt
azure-identity>=1.15.0
msal>=1.26.0
fastapi>=0.100.0
starlette>=0.27.0
itsdangerous>=2.1.0  # For session middleware
python-multipart>=0.0.6  # For form handling
```

### Maintenance Concerns

- **Redirect URI mismatch** - Auth fails completely. Keep URIs in sync between code and Azure.
- **Session expiration** - User logged out unexpectedly. Implement refresh token handling.
- **Consent prompt changes** - Users see unexpected prompts. Pre-consent via admin grant.
- **Multi-Factor Authentication** - Additional friction for users. Document user flow.
- **Token expiration** - API calls fail. Implement silent token refresh.

### Token Refresh Implementation

```python
async def get_valid_token(request: Request) -> str:
    """Get valid token, refreshing if needed."""
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Check if token is expired
    import jwt
    from datetime import datetime
    
    try:
        decoded = jwt.decode(
            user["access_token"],
            options={"verify_signature": False}
        )
        exp = datetime.fromtimestamp(decoded["exp"])
        
        # Refresh if expires within 5 minutes
        if exp < datetime.utcnow() + timedelta(minutes=5):
            result = auth_service.get_token_silent(user)
            if result and "access_token" in result:
                user["access_token"] = result["access_token"]
                request.session["user"] = user
        
        return user["access_token"]
    except Exception as e:
        logger.error(f"Token refresh failed: {e}")
        raise HTTPException(status_code=401, detail="Session expired")
```

## 6. Code Examples

### Basic Interactive Login (Azure Identity)

```python
from azure.identity import InteractiveBrowserCredential

credential = InteractiveBrowserCredential(
    client_id="your-client-id",
    tenant_id="your-tenant-id",
    redirect_uri="http://localhost:8400"
)

# Opens browser, user authenticates
token = credential.get_token("https://contoso.sharepoint.com/.default")
print(f"Token acquired for user")
```

### With Login Hint

```python
credential = InteractiveBrowserCredential(
    client_id="your-client-id",
    tenant_id="your-tenant-id",
    login_hint="user@contoso.com"  # Pre-fill username
)
```

### Using Office365-REST-Python-Client

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/hr").with_interactive(
    tenant_name_or_id="your-tenant-id",
    client_id="your-client-id"
)

# Opens browser for login
web = ctx.web.get().execute_query()
print(f"Site: {web.title}")
```

### Full MSAL Flow

```python
from msal import PublicClientApplication

app = PublicClientApplication(
    client_id="your-client-id",
    authority="https://login.microsoftonline.com/your-tenant-id"
)

# Check cache first
accounts = app.get_accounts()
if accounts:
    result = app.acquire_token_silent(
        scopes=["https://contoso.sharepoint.com/.default"],
        account=accounts[0]
    )
else:
    result = None

# Interactive login if needed
if not result:
    result = app.acquire_token_interactive(
        scopes=["https://contoso.sharepoint.com/.default"]
    )

if "access_token" in result:
    print(f"Logged in as: {result.get('id_token_claims', {}).get('name')}")
else:
    print(f"Error: {result.get('error_description')}")
```

### Token Caching with Persistence

```python
from msal import PublicClientApplication, SerializableTokenCache
import os

cache_file = "token_cache.json"

# Load cache
cache = SerializableTokenCache()
if os.path.exists(cache_file):
    cache.deserialize(open(cache_file).read())

app = PublicClientApplication(
    client_id="your-client-id",
    authority="https://login.microsoftonline.com/your-tenant-id",
    token_cache=cache
)

# Acquire token...
result = app.acquire_token_interactive(scopes=["..."])

# Save cache
if cache.has_state_changed:
    with open(cache_file, "w") as f:
        f.write(cache.serialize())
```

## 7. Gotchas and Quirks

### Redirect URI Must Match Exactly

```python
# In Azure Portal: http://localhost:8000/auth/callback

# WRONG - trailing slash
redirect_uri = "http://localhost:8000/auth/callback/"  # FAILS

# WRONG - different port
redirect_uri = "http://localhost:8080/auth/callback"  # FAILS

# CORRECT - exact match
redirect_uri = "http://localhost:8000/auth/callback"
```

### Production Redirect URI Must Be HTTPS

```python
# Development (OK)
redirect_uri = "http://localhost:8000/auth/callback"

# Production (MUST be HTTPS)
redirect_uri = "https://myapp.azurewebsites.net/auth/callback"
```

### Popup Blockers

Interactive browser may open a popup. Users with popup blockers will have issues:

```python
# Consider providing instructions
@app.get("/auth/login-help")
async def login_help():
    return HTMLResponse("""
        <h1>Login Help</h1>
        <p>If login doesn't work, please:</p>
        <ol>
            <li>Disable popup blockers for this site</li>
            <li>Try a different browser</li>
            <li>Contact IT support</li>
        </ol>
    """)
```

### Session Security

```python
# WRONG - insecure session
app.add_middleware(SessionMiddleware, secret_key="hardcoded")

# CORRECT - secure random secret
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ["SESSION_SECRET"],
    same_site="lax",
    https_only=True  # In production
)
```

### MFA and Conditional Access

Users may be prompted for MFA. This is normal and handled by Microsoft's login page:

```python
# No special code needed - Microsoft handles MFA
# But inform users this may happen
```

### Token vs ID Token Claims

```python
# Access token - for API calls (don't parse in client)
access_token = result["access_token"]

# ID token claims - for user info
claims = result.get("id_token_claims", {})
user_name = claims.get("name")
user_email = claims.get("preferred_username")
```

### Multi-Tenant Considerations

```python
# Single tenant (your org only)
authority = "https://login.microsoftonline.com/your-tenant-id"

# Multi-tenant (any Azure AD)
authority = "https://login.microsoftonline.com/common"

# Consumer accounts (personal Microsoft)
authority = "https://login.microsoftonline.com/consumers"
```

## Sources

**Primary:**
- SPAUTH-SC-MSFT-AUTHCODE: Authorization code flow
- SPAUTH-SC-MSFT-MSALPYTHON: MSAL for Python
- SPAUTH-SC-MSFT-AZIDREADME: Azure Identity client library
- SPAUTH-SC-MSFT-CLIENTAPPS: Public and confidential client apps (learn.microsoft.com/en-us/entra/identity-platform/msal-client-applications)
- SPAUTH-SC-MSAL-PYDOCS: MSAL Python API reference (msal-python.readthedocs.io/en/stable/)

## Document History

**[2026-03-23 22:30]**
- Changed: FastAPI example from ConfidentialClientApplication to PublicClientApplication
- Added: Section 2 "Public Client vs Confidential Client" explaining when each is needed
- Changed: Prerequisites section - SPA platform instead of Web, no client secret/certificate step
- Changed: Environment variables - removed AZURE_CLIENT_SECRET
- Changed: Code example uses initiate_auth_code_flow/acquire_token_by_auth_code_flow (PKCE)
- Added: Sources SPAUTH-SC-MSFT-CLIENTAPPS, SPAUTH-SC-MSAL-PYDOCS
- Reason: Certificate/secret is over-engineering for interactive user login. PnP PowerShell proves PublicClient + PKCE is sufficient.

**[2026-03-14 17:15]**
- Initial document created
- FastAPI OAuth integration documented
- Session handling and token refresh patterns included
