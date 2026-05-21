# Klaviyo Audit Katie — Klaviyo Connection Plan

**Version:** 1.0
**Owner:** National Positions
**Classification:** Internal Operating Framework — Phase 1
**Last Updated:** 2026-05-10

---

## Important Disclaimer

**All API endpoints, required permissions, response formats, and availability described in this document must be verified against the current Klaviyo API documentation before implementation begins.**

Klaviyo's API evolves with each version release. Endpoint paths, authentication mechanisms, available scopes, rate limits, and response schemas may differ from what is documented here. This document is an architectural plan, not a verified API reference.

Current Klaviyo API documentation: https://developers.klaviyo.com/en/reference/api_overview

---

## Klaviyo API Overview

Klaviyo provides a REST API that exposes most account data in JSON:API format. The API uses versioned endpoints (e.g., `2024-02-15`). Authentication is handled via either a private API key (for server-side, internal tools) or OAuth 2.0 (for third-party application integrations).

For Klaviyo Audit Katie, all API calls are:
- **Read-only** — no write, create, update, or delete operations
- **Server-side only** — the API key or OAuth token never touches a browser or client-side environment
- **Rate-limit-aware** — all calls respect Klaviyo's documented rate limits with exponential backoff

---

## Connection Options

### Option 1 — Private API Key (MVP / Internal Use)

**Use for:** Phase 2–3 development, internal NP audits, trusted client testing

**How it works:**
1. Client generates a private API key in their Klaviyo account (Settings → API Keys → Create Private API Key)
2. Client selects **read-only** scopes only
3. Client provides the key securely to NP (never via email — use a secure form or password manager share)
4. NP stores the key in an environment variable (`KLAVIYO_API_KEY`)
5. All API calls include the header: `Authorization: Klaviyo-API-Key {key}`

**Limitations:**
- Private keys are long-lived and require manual rotation
- No OAuth consent flow — requires client trust and manual key handling
- Keys with write permissions could be dangerous if mishandled — always confirm read-only before use

**Guidance for clients:**
> In your Klaviyo account, go to Settings → API Keys → Create Private API Key. When selecting permissions, choose "Read Access" for all scopes and do not enable any write permissions. Copy the key and share it through the secure form provided by National Positions.

---

### Option 2 — OAuth 2.0 (Production / Public-Facing Tool)

**Use for:** Phase 5+ public web app, self-service lead gen audit tool

**How it works:**
1. User clicks "Connect Klaviyo" in the NP audit tool
2. User is redirected to Klaviyo's OAuth authorization page
3. User reviews and approves the requested read-only scopes
4. Klaviyo returns an authorization code to NP's redirect URI
5. NP backend exchanges the code for an access token + refresh token
6. All subsequent API calls use the access token in the Authorization header
7. Refresh token is used to renew access without requiring re-authorization

**Advantages over private key:**
- No manual key handling by the client
- Scoped to exactly what NP requests
- Tokens can be revoked by the client at any time in Klaviyo settings
- Standard OAuth security model

**Required OAuth scopes (read-only):**
These scope names must be verified against current Klaviyo OAuth documentation:
- `read_accounts`
- `read_campaigns`
- `read_flows`
- `read_forms`
- `read_lists`
- `read_segments`
- `read_profiles`
- `read_metrics`
- `read_events`
- `read_templates`
- `read_coupons`
- `read_tags`

---

## API Authentication

### Private Key Authentication
```
Header: Authorization: Klaviyo-API-Key {KLAVIYO_PRIVATE_KEY}
Header: revision: {API_VERSION}  (e.g., 2024-02-15)
Header: Content-Type: application/json
```

### OAuth Authentication
```
Header: Authorization: Bearer {ACCESS_TOKEN}
Header: revision: {API_VERSION}
Header: Content-Type: application/json
```

---

## Secure Credential Handling Rules

These rules are absolute and cannot be overridden:

1. **Never log the API key or access token.** Log only the request timestamp, endpoint path, and response status code.
2. **Never expose credentials in the frontend.** All API calls are server-side only.
3. **Never store credentials in code files.** Use environment variables exclusively.
4. **Never include credentials in URLs.** API keys must not appear as query parameters.
5. **Never send credentials via email or unencrypted channels.** Use secure forms, encrypted vaults, or OAuth flows.
6. **Encrypt credentials at rest.** If tokens are persisted for session management, they must be encrypted in the database.
7. **Scope minimally.** Request only the read permissions actually needed — nothing more.
8. **Confirm read-only before proceeding.** Before any data pull, validate that the provided credentials do not have write permissions.

---

## API Validation Process

Before pulling audit data, Katie must validate the connection:

**Step 1 — Test authentication:**
```
GET /api/accounts/
```
- Success (200): Connection valid, proceed
- 401 Unauthorized: Invalid or expired key — stop, request new credentials
- 403 Forbidden: Insufficient permissions — stop, request read-access key
- 5xx: Klaviyo server error — retry with backoff, then escalate if persistent

**Step 2 — Confirm account identity:**
- Log the Klaviyo account name and account ID (do not log the API key)
- Confirm this matches the expected client account before proceeding

**Step 3 — Enumerate available endpoints:**
- Test each data object endpoint to confirm it returns data
- Log which endpoints are accessible vs. returning 403/404
- Flag any inaccessible endpoints in the audit output as "data unavailable"

---

## Error Handling

| HTTP Status | Meaning | Katie's Response |
|---|---|---|
| 200 OK | Success | Proceed normally |
| 400 Bad Request | Malformed request | Log error details, fix request format |
| 401 Unauthorized | Invalid or expired credentials | Stop audit, request new credentials |
| 403 Forbidden | Insufficient permissions | Stop audit, request read-only key with correct scopes |
| 404 Not Found | Endpoint doesn't exist | Flag as "endpoint unavailable," continue audit without that data |
| 429 Too Many Requests | Rate limit exceeded | Pause, apply exponential backoff (see below), retry |
| 500 Internal Server Error | Klaviyo server error | Retry up to 3 times with 5-second intervals, then log and escalate |
| 503 Service Unavailable | Klaviyo maintenance / overload | Wait 60 seconds, retry once, then halt and notify |

---

## Rate Limit Handling

Klaviyo enforces rate limits on API requests. Limits vary by endpoint type (verify current limits in Klaviyo documentation).

**General approach:**
- Implement a request queue with configurable concurrency
- Add `Retry-After` header respect (if provided in 429 responses)
- Use exponential backoff on rate limit errors:
  - Attempt 1: immediate
  - Attempt 2: wait 2 seconds
  - Attempt 3: wait 4 seconds
  - Attempt 4: wait 8 seconds
  - Attempt 5: wait 16 seconds — if still failing, halt and log

**Batch requests where available:**
- Prefer batch/bulk endpoints over individual record calls where Klaviyo supports them
- Use field filtering (`fields[campaign]=name,send_time,status`) to reduce response payload size

---

## Pagination Handling

Klaviyo uses cursor-based pagination for list endpoints. Large accounts may have thousands of campaigns, profiles, or events.

**Pagination pattern:**
```
Initial request: GET /api/campaigns/?page[size]=50
Response includes: data[], links.next (cursor URL if more pages exist)
Next request: GET {links.next}  (use cursor URL directly)
Repeat until: links.next is null
```

**Rules:**
- Always paginate — never assume first page contains all records
- Set a reasonable page size (50–100 per page is generally safe)
- Track total records pulled for each object type and log in audit metadata
- Set a maximum pagination cap for very large accounts (e.g., max 10,000 profiles for aggregate stats) to prevent runaway API calls
- For profile data, use aggregate metrics — do not paginate through individual profile records (privacy, performance)

---

## Data Objects to Pull

The following objects and approximate endpoint paths should be pulled for each audit. All paths and availability must be confirmed against current Klaviyo API documentation.

| Object | Estimated Endpoint | Priority | Notes |
|---|---|---|---|
| Accounts | `/api/accounts/` | Required | Account name, ID, timezone, currency |
| Campaigns | `/api/campaigns/` | Required | All campaigns in audit period |
| Campaign Messages | `/api/campaign-messages/` | Required | Message content, channel, metrics |
| Flows | `/api/flows/` | Required | All flows regardless of status |
| Flow Messages | `/api/flow-messages/` | Required | Per-message metrics and timing |
| Lists | `/api/lists/` | Required | All lists with profile counts |
| Segments | `/api/segments/` | Required | All segments with definitions |
| Profiles (aggregate) | `/api/profiles/` | Required | Aggregate counts only — no PII |
| Metrics | `/api/metrics/` | Required | Available metric definitions |
| Events | `/api/events/` | Required | Email and SMS engagement events |
| Templates | `/api/templates/` | Recommended | Template count and channel type |
| Tags | `/api/tags/` | Recommended | Organization and tagging structure |
| Forms | `/api/forms/` | Required | Signup form performance (if available) |
| Coupons | `/api/coupon-codes/` | Optional | Incentive usage in flows |
| Benchmarks | TBD — verify availability | Recommended | Industry benchmark ratings if accessible |
| Billing/Plan | TBD — verify availability | Recommended | Plan tier and profile limits if accessible |

---

## Data Freshness Rules

- Pull fresh data for every new audit — never use cached data from a prior audit session
- If a client runs two audits within the same day, re-pull all data to ensure freshness
- Data pulled during the audit is valid for the duration of that audit session only
- Raw API response payloads are not persisted after the audit completes (processed results may be stored per data retention policy)
- Timestamp all data pulls in the audit metadata

---

## Disconnect and Credential Revocation Process

**User-initiated disconnect (OAuth):**
1. User clicks "Disconnect Klaviyo" in the audit tool
2. System revokes the OAuth token via Klaviyo's revocation endpoint
3. System confirms token is no longer valid
4. System deletes the token from storage
5. User receives confirmation that access has been removed

**User-initiated disconnect (private key):**
1. User is instructed to delete the API key in their Klaviyo account (Settings → API Keys)
2. NP system removes the stored key reference from its environment
3. Audit tool confirms disconnected status

**NP-initiated revocation:**
If a key is suspected of being compromised or mishandled:
1. NP immediately removes the key from all systems
2. NP notifies the client to delete and regenerate the key in Klaviyo
3. NP documents the incident in its security log

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05-10 | Initial connection plan — Phase 1 |
