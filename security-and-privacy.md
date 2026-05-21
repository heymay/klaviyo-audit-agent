# Klaviyo Audit Katie — Security and Privacy Requirements

**Version:** 1.0
**Owner:** National Positions
**Classification:** Internal Operating Framework — Phase 1
**Last Updated:** 2026-05-10

---

## Overview

This document defines all security and privacy requirements for handling Klaviyo API credentials, account data, and personally identifiable information (PII) in the context of the Klaviyo Audit Katie system. These requirements are non-negotiable and apply to all phases of development and operation.

---

## Core Security Principles

1. **Minimal access.** Request only the permissions necessary to conduct the audit (read-only).
2. **No write access.** The system never requests, holds, or exercises write permissions on any Klaviyo account.
3. **Credential isolation.** API keys and OAuth tokens are never visible in logs, outputs, URLs, or client-facing documents.
4. **Server-side only.** All API calls are made server-side. Credentials never touch a browser environment.
5. **Data minimization.** Only the data required for the audit is pulled and processed. Unnecessary data is not retained.
6. **User control.** Users can revoke access at any time and request deletion of their data.

---

## API Credential Security

### Private API Key (MVP / Internal)

| Rule | Requirement |
|---|---|
| Storage | Environment variable only (`KLAVIYO_API_KEY`) |
| Logging | Never log the key value — only log the timestamp, endpoint, and response status code |
| Frontend | Never expose in frontend code, HTML, JavaScript, or browser network requests |
| URL | Never include as a URL query parameter |
| Email / Chat | Never transmit via email, Slack, or any unencrypted channel |
| Code files | Never hardcode in any source file — not even .env files committed to version control |
| At-rest encryption | If persisted for session management, encrypt at rest using AES-256 or equivalent |
| Rotation | Keys should be treated as single-use for each audit session and revoked after use |
| Confirmation | Before any data pull, confirm the key is read-only via a test API call |

### OAuth Token (Production)

| Rule | Requirement |
|---|---|
| Scope request | Request only read-only scopes — never request write scopes |
| Token storage | Encrypt access and refresh tokens at rest |
| Token transmission | Use HTTPS only — never transmit over HTTP |
| Token expiry | Respect token expiry; use refresh token to renew, not to extend write-access scope |
| Revocation | Provide a one-click disconnect that revokes the OAuth token via Klaviyo's revocation endpoint |
| Token logging | Never log token values — only log token metadata (expiry, scope) |

---

## Data Handling

### What Data Is Pulled

Katie pulls only the data fields defined in `klaviyo-data-map.md`. No data beyond what is listed there is retrieved.

### Profile Data Rules

- **Aggregate only.** Katie retrieves aggregate statistics about profiles (total count, engagement counts, suppression counts) — never individual profile records.
- **No PII.** Individual names, email addresses, phone numbers, or purchase histories are never retrieved, stored, or included in any output.
- **No export.** Profile-level data is never exported to a file, email, or external system.
- **Session scope only.** Any profile aggregate data retrieved during an audit session is used for scoring only and is not retained after the session ends (unless the processed audit result is stored per the data retention policy below).

### Raw API Response Storage

- Raw API responses (JSON payloads) are **not persisted** after the audit completes
- Only processed, normalized results (scores, findings, recommendations) are stored
- Raw payloads are held in memory only for the duration of the audit computation

---

## Data Retention Policy

| Data Type | Retention |
|---|---|
| Audit results (scores, findings, recommendations) | Retained per client agreement — typically 12 months, then deleted |
| Lead capture form data | Retained in CRM per NP data retention policy |
| API keys / OAuth tokens | Not retained after audit session unless explicitly needed for recurring audits — revoked on disconnect |
| Raw API response payloads | Not retained — deleted from memory after processing |
| Audit logs (timestamps, endpoints, status codes) | Retained for 90 days for security review, then deleted |
| PII (individual profile records) | Never retrieved; therefore not retained |

---

## User Consent Requirements

Before any Klaviyo data is accessed:

1. User must be presented with a clear explanation of what data will be accessed and why
2. User must check a consent checkbox confirming authorization
3. Consent record must be timestamped and stored
4. User must be informed that access is read-only and no changes will be made
5. User must be told how to revoke access (delete the API key in Klaviyo)

**Required consent language (minimum):**
> By connecting your Klaviyo account, you authorize National Positions to access your Klaviyo account data in read-only mode for the purpose of conducting a Klaviyo diagnostic audit. No changes will be made to your account. Your credentials are stored securely and never shared with third parties. You may revoke access at any time.

---

## Disconnect and Revocation Process

### User-Initiated Disconnect (OAuth)

1. User clicks "Disconnect Klaviyo" in the audit tool interface
2. System calls Klaviyo's OAuth token revocation endpoint
3. System confirms the token is no longer valid
4. System removes the token from encrypted storage
5. System displays a confirmation message to the user: "Your Klaviyo account has been disconnected. National Positions no longer has access to your account."

### User-Initiated Disconnect (Private Key)

1. User is prompted to delete their API key in Klaviyo (Settings → API Keys)
2. Step-by-step instructions are provided in the UI
3. NP system removes the stored key reference from its environment
4. User receives confirmation once NP's system has been updated

### NP-Initiated Revocation (Incident Response)

If a key or token is suspected of being compromised:
1. NP immediately removes the key from all systems
2. NP notifies the affected client within 24 hours
3. NP instructs the client to delete and regenerate the key in Klaviyo
4. NP documents the incident in its security incident log with date, scope, and resolution

---

## Audit Logging

All API activity is logged for security review purposes.

**What is logged:**
- Timestamp of each API call
- Endpoint called (e.g., `GET /api/campaigns/`)
- HTTP response status code (e.g., 200, 429)
- Number of records returned (e.g., "47 campaigns retrieved")
- Duration of the call

**What is never logged:**
- API key or OAuth token values
- Individual profile records
- Any PII (names, emails, phone numbers)
- Raw API response payloads

**Log retention:** 90 days, then automatically deleted.

---

## Frontend Security Rules

In Phase 5+ (web application):

| Rule | Requirement |
|---|---|
| HTTPS only | All pages served over HTTPS — no HTTP |
| API key input | Masked input field (type="password") — value never visible in plain text |
| Key transmission | API key POSTed directly to server — never stored in localStorage, sessionStorage, or cookies |
| CSRF protection | All forms protected with CSRF tokens |
| Content Security Policy | CSP headers configured to prevent XSS |
| No credentials in URLs | API key never appears in the URL (no query parameters) |
| Session management | Sessions expire after 30 minutes of inactivity |
| Error messages | Generic error messages returned to frontend — no stack traces or internal details exposed |

---

## Compliance Awareness

### GDPR (EU / UK)

- Klaviyo account data pulled for audit purposes is processed under the legal basis of "legitimate interest" for B2B service delivery
- PII is not collected at the profile level
- EU clients should be informed of NP's data processing practices
- Data deletion requests can be fulfilled within 30 days

### CCPA (California)

- NP does not sell audit data or lead data to third parties
- California clients may request data deletion
- Privacy policy must disclose audit data collection and use

### TCPA (SMS)

- This system does not send SMS on behalf of clients — it only audits SMS program configuration
- SMS consent data within the client's Klaviyo account is accessed read-only and never exported

### CAN-SPAM

- Not directly applicable to audit activity — applies to NP's own follow-up email sequence
- NP follow-up emails must include unsubscribe option and physical address

---

## Pre-Production Security Requirements

Before Phase 5 (web app) launches to external users:

1. **Penetration testing** — Third-party pen test of the web application before launch
2. **Security code review** — API integration code reviewed by a qualified security professional
3. **Credential vault audit** — Confirm API key storage meets encryption requirements
4. **Access control review** — Confirm only authorized NP team members can access audit data
5. **Incident response plan** — Written plan for credential compromise, data breach, or API abuse
6. **Privacy policy update** — NP's privacy policy updated to reflect Klaviyo audit data collection
7. **Terms of Service** — ToS updated to reflect audit tool use, data handling, and limitations

---

## Security Contact

For security concerns related to Klaviyo Audit Katie:
- Internal: [NP Security Lead or IT Contact — to be defined]
- External disclosures: [security@nationalpositions.com — placeholder]

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05-10 | Initial security and privacy framework — Phase 1 |
