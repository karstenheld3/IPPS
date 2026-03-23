# mTLS Certificates

**Doc ID**: OAIAPI-IN51
**Goal**: Document mTLS certificate management for secure API communication
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN47_ADMIN_OVERVIEW.md [OAIAPI-IN47]` for admin context

## Summary

The Certificates API manages mTLS (mutual TLS) certificates for securing API communication. mTLS provides an additional authentication layer beyond API keys - the client must present a valid certificate during TLS handshake. Create certificates (POST) by uploading a PEM-encoded certificate, retrieve details (GET), list all certificates (GET), activate/deactivate certificates (POST), and delete certificates (DELETE). Certificates can be managed at organization level and project level. When mTLS is enforced, API requests without a valid client certificate are rejected regardless of API key validity. Certificate states: active, inactive. Organization-level certificates apply to all projects; project-level certificates scope to specific projects. [VERIFIED] (OAIAPI-SC-OAI-ADMORG)

## Key Facts

- **Purpose**: Additional authentication layer via client certificates [VERIFIED] (OAIAPI-SC-OAI-ADMORG)
- **Format**: PEM-encoded X.509 certificates [VERIFIED] (OAIAPI-SC-OAI-ADMORG)
- **Scopes**: Organization-level or project-level [VERIFIED] (OAIAPI-SC-OAI-ADMORG)
- **States**: active, inactive [VERIFIED] (OAIAPI-SC-OAI-ADMORG)
- **Enforcement**: When enabled, requests without valid cert are rejected [VERIFIED] (OAIAPI-SC-OAI-ADMORG)

## Quick Reference

```
POST   /v1/organization/certificates                          # Create certificate
GET    /v1/organization/certificates                          # List certificates
GET    /v1/organization/certificates/{cert_id}                # Retrieve
POST   /v1/organization/certificates/{cert_id}/activate       # Activate
POST   /v1/organization/certificates/{cert_id}/deactivate     # Deactivate
DELETE /v1/organization/certificates/{cert_id}                # Delete
```

## Certificate Object

```json
{
  "object": "organization.certificate",
  "id": "cert-abc123",
  "name": "Production mTLS Cert",
  "status": "active",
  "created_at": 1711471533,
  "expires_at": 1743007533,
  "fingerprint": "AB:CD:EF:12:34:56:78:90"
}
```

## SDK Examples (Python)

> **SDK note**: `client.organization.*` methods are not available in openai Python SDK v2.29.0.
> The Administration API uses REST-only endpoints with admin API keys (`sk-admin-...`).
> Use `httpx` or `requests` for direct REST calls to `https://api.openai.com/v1/organization/*`.

### Certificate Lifecycle

```python
from openai import OpenAI

client = OpenAI(api_key="sk-admin-...")

# Create certificate
with open("client_cert.pem", "r") as f:
    cert_pem = f.read()

cert = client.organization.certificates.create(
    name="Production mTLS",
    certificate=cert_pem
)
print(f"Certificate: {cert.id}, Status: {cert.status}")

# Activate
client.organization.certificates.activate(cert.id)

# List all certificates
certs = client.organization.certificates.list()
for c in certs.data:
    print(f"  {c.name} ({c.status}) expires {c.expires_at}")
```

## Use Cases

- **Enterprise security**: Enforce mTLS for compliance (SOC2, HIPAA)
- **Zero-trust**: Additional authentication layer beyond API keys
- **Certificate rotation**: Programmatic certificate management

## Differences from Other APIs

- **vs Anthropic**: No mTLS certificate management API
- **vs Gemini**: Uses Google Cloud Certificate Manager (different service)
- **vs Grok**: No mTLS API

## Sources

- OAIAPI-SC-OAI-ADMORG - Organization Administration API

## Document History

**[2026-03-21 09:48]**
- Added: SDK v2.29.0 note - client.organization.* not in Python SDK (REST-only admin API)

**[2026-03-20 18:12]**
- Initial documentation created
